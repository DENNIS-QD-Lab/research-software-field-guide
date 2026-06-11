import os
import re
import h5py
import numpy as np
import matplotlib.pyplot as plt
from skimage import filters, measure
from scipy.ndimage import binary_fill_holes
import cv2

# ============================================================================
# MOUSE SEGMENTATION
# ============================================================================

def create_mouse_mask(broadband_image):
    if broadband_image is None:
        return None
    try:
        threshold = filters.threshold_otsu(broadband_image)
        mask = binary_fill_holes(broadband_image > threshold)
        labeled = measure.label(mask)
        regions = measure.regionprops(labeled)
        if not regions:
            return None
        largest = max(regions, key=lambda x: x.area)
        return labeled == largest.label
    except Exception as e:
        print(f"    Error creating mask: {e}")
        return None

# ============================================================================
# LAYOUT DETECTION
# ============================================================================

def detect_layout(root_folder):
    """
    Returns:
        ('pilot',    hdr_folder, raw_folder)   HDR/HDR_h5/m{N}/ subfolders, m{N}_{label}_HDR.h5
        ('new',      hdr_folder, raw_folder)   HDR/HDR_h5/ flat, DL####_day{N}_HDR.h5
        ('original', root_folder, None)        per-mouse m{N}/ subfolders at root
    """
    hdr_candidates = [
        os.path.join(root_folder, 'HDR', 'HDR_h5'),
        os.path.join(root_folder, 'HDR_h5'),
        os.path.join(root_folder, 'HDR'),
    ]
    for hdr_path in hdr_candidates:
        if not os.path.isdir(hdr_path):
            continue

        # --- pilot: look for m{N} subfolders inside HDR_h5 ---
        mouse_subs = [
            e for e in os.listdir(hdr_path)
            if os.path.isdir(os.path.join(hdr_path, e))
            and re.match(r'^m\d+$', e, re.IGNORECASE)
        ]
        if mouse_subs:
            # confirm at least one pilot-style HDR file inside
            sample_dir = os.path.join(hdr_path, mouse_subs[0])
            pilot_files = [
                f for f in os.listdir(sample_dir)
                if re.match(r'^m\d+_.+_HDR\.h5$', f, re.IGNORECASE)
            ]
            if pilot_files:
                raw_path = os.path.join(root_folder, 'raw')
                print(f"  Detected PILOT layout (HDR_h5/m{{N}}/ subfolders)")
                return 'pilot', hdr_path, raw_path if os.path.isdir(raw_path) else None

        # --- new: flat DL####_day{N}_HDR.h5 ---
        new_style = [
            f for f in os.listdir(hdr_path)
            if re.match(r'^[A-Za-z0-9]+_day\d+_HDR\.h5$', f, re.IGNORECASE)
        ]
        if new_style:
            raw_path = os.path.join(root_folder, 'raw')
            print(f"  Detected NEW layout (shared HDR folder)")
            return 'new', hdr_path, raw_path if os.path.isdir(raw_path) else None

    # --- original: m{N}/ subfolders directly under root ---
    mouse_subs = [
        e for e in os.listdir(root_folder)
        if os.path.isdir(os.path.join(root_folder, e))
        and re.match(r'^m\d+$', e, re.IGNORECASE)
    ]
    if mouse_subs:
        print(f"  Detected ORIGINAL layout (per-mouse subfolders)")
        return 'original', root_folder, None

    return 'unknown', root_folder, None

# ============================================================================
# HELPER FUNCTIONS — shared
# ============================================================================

def load_h5_metadata_and_stack(filepath):
    with h5py.File(filepath, 'r') as f:
        images = f['radiance_cube'][()]
        raw_names = f['channel_names'][()]
        if isinstance(raw_names[0], (bytes, np.bytes_)):
            channel_names = [c.decode('utf-8') for c in raw_names]
        else:
            channel_names = list(raw_names)

        lasers, filter_list = [], []
        for ch in channel_names:
            parts = ch.split('_')
            if len(parts) == 2:
                lasers.append(parts[0])
                filter_list.append(parts[1])
            else:
                lasers.append(ch)
                filter_list.append('unknown')

        name_to_idx = {ch: i for i, ch in enumerate(channel_names)}
        return images, name_to_idx, lasers, filter_list, channel_names

def load_bb_image_from_h5(filepath):
    with h5py.File(filepath, 'r') as f:
        if 'Cube' in f and 'Images' in f['Cube']:
            data = f['Cube/Images'][()]
            if len(data.shape) == 3 and data.shape[0] == 1:
                data = data[0]
            return data
        for key in ['image', 'Images', 'brightfield', 'bf', 'bb']:
            if key in f:
                data = f[key][()]
                while len(data.shape) > 2:
                    data = data[0] if data.shape[0] == 1 else data[data.shape[0] // 2]
                return data
    return None

def apply_CLAHE(img):
    if img.dtype != np.uint8:
        mn, mx = img.min(), img.max()
        img = ((img - mn) / (mx - mn) * 255).astype(np.uint8) if mx > mn \
              else np.zeros_like(img, dtype=np.uint8)
    clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(8, 8))
    return clahe.apply(img)

# ============================================================================
# ORIGINAL LAYOUT HELPERS
# ============================================================================

def parse_day_original(filename):
    """Original layout: day{N}_m{N}_HDR.h5"""
    m = re.match(r'day(\d+)_m\d+_HDR\.h5', filename, re.IGNORECASE)
    return int(m.group(1)) if m else None

def find_hdr_folder(mouse_folder):
    for sub in ['HDR/HDR_h5', 'HDR', 'hdr/hdr_h5', 'hdr']:
        path = os.path.join(mouse_folder, sub)
        if os.path.exists(path):
            if any(re.match(r'day\d+_m\d+_HDR\.h5', f, re.IGNORECASE)
                   for f in os.listdir(path)):
                return path
    if any(re.match(r'day\d+_m\d+_HDR\.h5', f, re.IGNORECASE)
           for f in os.listdir(mouse_folder)):
        return mouse_folder
    for root, _, files in os.walk(mouse_folder):
        if any(re.match(r'day\d+_m\d+_HDR\.h5', f, re.IGNORECASE) for f in files):
            return root
    return None

def find_bb_image_original(mouse_folder, day, mouse_name):
    day_folder = f"day{day}_{mouse_name}"
    bb_path = os.path.join(mouse_folder, day_folder, "bb.h5")
    if os.path.exists(bb_path):
        return bb_path
    for entry in os.listdir(mouse_folder):
        if entry.lower() == day_folder.lower():
            bb_path = os.path.join(mouse_folder, entry, "bb.h5")
            if os.path.exists(bb_path):
                return bb_path
    return None

def find_all_mice_original(root_folder):
    mice = []
    for entry in os.listdir(root_folder):
        if (os.path.isdir(os.path.join(root_folder, entry)) and
                re.match(r'^m(\d+)$', entry, re.IGNORECASE)):
            mice.append({
                'path': os.path.join(root_folder, entry),
                'mouse_name': entry,
                'label': entry
            })
    mice.sort(key=lambda x: int(re.search(r'\d+', x['mouse_name']).group()))
    return mice

# ============================================================================
# NEW LAYOUT HELPERS
# ============================================================================

def parse_new_hdr_filename(filename):
    """New layout: {MOUSEID}_day{N}_HDR.h5 → (mouse_id, day)"""
    m = re.match(r'^([A-Za-z0-9]+)_day(\d+)_HDR\.h5$', filename, re.IGNORECASE)
    return (m.group(1).upper(), int(m.group(2))) if m else (None, None)

def find_bb_image_new(raw_root, mouse_id, day):
    if raw_root is None:
        return None
    mouse_raw_dir = os.path.join(raw_root, mouse_id)
    if not os.path.isdir(mouse_raw_dir):
        return None
    day_pattern = re.compile(r'day0*' + str(day) + r'(?!\d)', re.IGNORECASE)
    for entry in sorted(os.listdir(mouse_raw_dir)):
        entry_path = os.path.join(mouse_raw_dir, entry)
        if os.path.isdir(entry_path) and day_pattern.search(entry):
            bb_path = os.path.join(entry_path, 'bb.h5')
            if os.path.exists(bb_path):
                return bb_path
    return None

def find_all_mice_new(hdr_folder):
    hdr_files = [
        f for f in os.listdir(hdr_folder)
        if re.match(r'^[A-Za-z0-9]+_day\d+_HDR\.h5$', f, re.IGNORECASE)
    ]
    dl_ids = sorted(set(
        parse_new_hdr_filename(f)[0]
        for f in hdr_files
        if parse_new_hdr_filename(f)[0] is not None
    ))
    return [{'mouse_name': dl_id, 'label': dl_id} for dl_id in dl_ids]

# ============================================================================
# PILOT LAYOUT HELPERS
# ============================================================================

def parse_day_pilot(filename):
    """
    Pilot layout: m{N}_{label}_HDR.h5
    Extract day from the last segment before _HDR.
    Only matches pure numeric-day labels: e.g. '3day' -> 3, '7day' -> 7.
    Skips labels like '0min', '4hr', 'CT', 'GI', 'organs', etc.
    Returns int day or None if not a day-type label.
    """
    m = re.match(r'^m\d+_(.+)_HDR\.h5$', filename, re.IGNORECASE)
    if not m:
        return None
    label = m.group(1)
    # last underscore-separated segment
    last_seg = label.split('_')[-1].lower()
    day_m = re.match(r'^(\d+)day$', last_seg)
    if day_m:
        return int(day_m.group(1))
    return None

def find_all_mice_pilot(hdr_folder):
    """
    Pilot layout: HDR_h5/m{N}/ subfolders, one per mouse.
    """
    mice = []
    for entry in sorted(os.listdir(hdr_folder)):
        full = os.path.join(hdr_folder, entry)
        if os.path.isdir(full) and re.match(r'^m\d+$', entry, re.IGNORECASE):
            mice.append({
                'mouse_name': entry,
                'label': entry,
                'hdr_subfolder': full
            })
    mice.sort(key=lambda x: int(re.search(r'\d+', x['mouse_name']).group()))
    return mice

def find_bb_image_pilot(raw_root, mouse_id, day):
    """
    Pilot layout: raw/{mouse_id}/{mouse_id}_{anything}_{N}day/
    Match subfolders whose last segment is {N}day.
    Grab any .h5 file inside (bb.h5 preferred, else first .h5).
    """
    if raw_root is None:
        return None
    mouse_raw_dir = os.path.join(raw_root, mouse_id)
    if not os.path.isdir(mouse_raw_dir):
        return None

    target_suffix = f"{day}day"
    for entry in sorted(os.listdir(mouse_raw_dir)):
        entry_path = os.path.join(mouse_raw_dir, entry)
        if not os.path.isdir(entry_path):
            continue
        last_seg = entry.split('_')[-1].lower()
        if last_seg != target_suffix.lower():
            continue
        # prefer bb.h5
        bb_path = os.path.join(entry_path, 'bb.h5')
        if os.path.exists(bb_path):
            return bb_path
        # fallback: first .h5 in folder
        h5_files = [f for f in os.listdir(entry_path) if f.lower().endswith('.h5')]
        if h5_files:
            return os.path.join(entry_path, sorted(h5_files)[0])
    return None

# ============================================================================
# DATA LOADING
# ============================================================================

def load_mouse_data_original(mouse_folder_path, mouse_name, target_days):
    print(f"    Loading {mouse_name} (original layout)...")
    result = {
        'mouse_name': mouse_name,
        'bb_images_by_day': {},
        'condition_data': {},
        'success': False
    }
    try:
        hdr_folder = find_hdr_folder(mouse_folder_path)
        if hdr_folder is None:
            print("      ❌ No HDR files found"); return result

        hdr_files = [f for f in os.listdir(hdr_folder)
                     if re.match(r'day\d+_m\d+_HDR\.h5', f, re.IGNORECASE)]
        if not hdr_files:
            print("      ❌ No HDR files"); return result

        _, _, lasers, filter_list, ref_channel_names = load_h5_metadata_and_stack(
            os.path.join(hdr_folder, hdr_files[0]))
        n_conditions = len(ref_channel_names)
        print(f"      Reference channels ({n_conditions}): {ref_channel_names}")

        for day in target_days:
            bb_path = find_bb_image_original(mouse_folder_path, day, mouse_name)
            if bb_path:
                try:
                    bb_img = load_bb_image_from_h5(bb_path)
                    if bb_img is not None:
                        result['bb_images_by_day'][day] = bb_img
                except Exception:
                    pass

        condition_images = {i: {} for i in range(n_conditions)}
        for f in hdr_files:
            day = parse_day_original(f)
            if day is None or day not in target_days:
                continue
            try:
                images, name_to_idx, _, _, _ = load_h5_metadata_and_stack(
                    os.path.join(hdr_folder, f))
                n_slices = images.shape[0]
                if n_slices < n_conditions:
                    missing = [c for c in ref_channel_names if c not in name_to_idx]
                    print(f"      ⚠️  Day {day}: {n_slices}/{n_conditions} slices — missing: {missing}")
                for ci, ch_name in enumerate(ref_channel_names):
                    if ch_name in name_to_idx:
                        condition_images[ci][day] = images[name_to_idx[ch_name]]
            except Exception as e:
                print(f"      ⚠️  Day {day}: failed ({e})")

        result['condition_data'] = {
            'lasers': lasers,
            'filters': filter_list,
            'condition_images': condition_images
        }
        result['success'] = True
        print(f"      ✅ {len(result['bb_images_by_day'])} BB images, {len(hdr_files)} HDR files")

    except Exception as e:
        print(f"      ❌ Error: {e}")
    return result


def load_mouse_data_new(mouse_id, hdr_folder, raw_root, target_days):
    print(f"    Loading {mouse_id} (new layout)...")
    result = {
        'mouse_name': mouse_id,
        'bb_images_by_day': {},
        'condition_data': {},
        'success': False
    }
    try:
        hdr_files = [
            f for f in os.listdir(hdr_folder)
            if re.match(r'^' + re.escape(mouse_id) + r'_day\d+_HDR\.h5$', f, re.IGNORECASE)
        ]
        if not hdr_files:
            print(f"      ❌ No HDR files found for {mouse_id}"); return result

        _, _, lasers, filter_list, ref_channel_names = load_h5_metadata_and_stack(
            os.path.join(hdr_folder, hdr_files[0]))
        n_conditions = len(ref_channel_names)
        print(f"      Reference channels ({n_conditions}): {ref_channel_names}")

        for day in target_days:
            bb_path = find_bb_image_new(raw_root, mouse_id, day)
            if bb_path:
                try:
                    bb_img = load_bb_image_from_h5(bb_path)
                    if bb_img is not None:
                        result['bb_images_by_day'][day] = bb_img
                except Exception:
                    pass

        condition_images = {i: {} for i in range(n_conditions)}
        for f in hdr_files:
            _, day = parse_new_hdr_filename(f)
            if day is None or day not in target_days:
                continue
            try:
                images, name_to_idx, _, _, _ = load_h5_metadata_and_stack(
                    os.path.join(hdr_folder, f))
                n_slices = images.shape[0]
                if n_slices < n_conditions:
                    missing = [c for c in ref_channel_names if c not in name_to_idx]
                    print(f"      ⚠️  Day {day}: {n_slices}/{n_conditions} slices — missing: {missing}")
                for ci, ch_name in enumerate(ref_channel_names):
                    if ch_name in name_to_idx:
                        condition_images[ci][day] = images[name_to_idx[ch_name]]
            except Exception as e:
                print(f"      ⚠️  Day {day}: failed ({e})")

        result['condition_data'] = {
            'lasers': lasers,
            'filters': filter_list,
            'condition_images': condition_images
        }
        result['success'] = True
        print(f"      ✅ {len(result['bb_images_by_day'])} BB images, {len(hdr_files)} HDR files")

    except Exception as e:
        print(f"      ❌ Error: {e}")
    return result


def load_mouse_data_pilot(mouse_id, hdr_subfolder, raw_root, target_days):
    print(f"    Loading {mouse_id} (pilot layout)...")
    result = {
        'mouse_name': mouse_id,
        'bb_images_by_day': {},
        'condition_data': {},
        'success': False
    }
    try:
        # All HDR files for this mouse (any label)
        all_hdr = [
            f for f in os.listdir(hdr_subfolder)
            if re.match(r'^m\d+_.+_HDR\.h5$', f, re.IGNORECASE)
        ]
        # Filter to only day-type files that fall within target_days
        day_hdr_files = []
        for f in all_hdr:
            d = parse_day_pilot(f)
            if d is not None and d in target_days:
                day_hdr_files.append((f, d))
        day_hdr_files.sort(key=lambda x: x[1])

        if not day_hdr_files:
            print(f"      ❌ No day-type HDR files found for {mouse_id}"); return result

        # Non-day files are skipped but logged
        skipped = [f for f in all_hdr if parse_day_pilot(f) is None]
        if skipped:
            print(f"      ℹ️  Skipping non-day files: {skipped}")

        # Reference channels from first day file
        _, _, lasers, filter_list, ref_channel_names = load_h5_metadata_and_stack(
            os.path.join(hdr_subfolder, day_hdr_files[0][0]))
        n_conditions = len(ref_channel_names)
        print(f"      Reference channels ({n_conditions}): {ref_channel_names}")

        # BB images
        for day in target_days:
            bb_path = find_bb_image_pilot(raw_root, mouse_id, day)
            if bb_path:
                try:
                    bb_img = load_bb_image_from_h5(bb_path)
                    if bb_img is not None:
                        result['bb_images_by_day'][day] = bb_img
                        print(f"      ✅ BB day {day}: {bb_path}")
                except Exception as e:
                    print(f"      ⚠️  BB day {day} failed: {e}")
            else:
                print(f"      ℹ️  No BB found for day {day}")

        # HDR images
        condition_images = {i: {} for i in range(n_conditions)}
        for f, day in day_hdr_files:
            try:
                images, name_to_idx, _, _, _ = load_h5_metadata_and_stack(
                    os.path.join(hdr_subfolder, f))
                n_slices = images.shape[0]
                if n_slices < n_conditions:
                    missing = [c for c in ref_channel_names if c not in name_to_idx]
                    print(f"      ⚠️  Day {day}: {n_slices}/{n_conditions} slices — missing: {missing}")
                for ci, ch_name in enumerate(ref_channel_names):
                    if ch_name in name_to_idx:
                        condition_images[ci][day] = images[name_to_idx[ch_name]]
                print(f"      ✅ Loaded day {day}: {f}")
            except Exception as e:
                print(f"      ⚠️  Day {day} ({f}): failed ({e})")

        result['condition_data'] = {
            'lasers': lasers,
            'filters': filter_list,
            'condition_images': condition_images
        }
        result['success'] = True
        print(f"      ✅ {len(result['bb_images_by_day'])} BB images, "
              f"{len(day_hdr_files)} day-HDR files")

    except Exception as e:
        print(f"      ❌ Error: {e}")
    return result

# ============================================================================
# 2×3 GRID PLOT
# ============================================================================

ROW1_DAYS = [1, 2, 3]
ROW2_DAYS = [7, 10, 14]
ALL_DAYS  = ROW1_DAYS + ROW2_DAYS

def plot_and_save_2x3_grid(mouse_data, laser, filter_set, save_folder, file_prefix):
    images_by_day = mouse_data['images_by_day']
    bb_images     = mouse_data['bb_images_by_day']

    sample_img = next((v for v in images_by_day.values()), None)
    if sample_img is None:
        print("      ⚠️  No images, skipping."); return

    img_h, img_w = sample_img.shape[:2]
    dpi     = 200
    panel_w = img_w / dpi
    panel_h = img_h / dpi
    fig_w   = 3 * panel_w
    fig_h   = 2 * panel_h

    fig = plt.figure(figsize=(fig_w, fig_h), dpi=dpi)

    for row_idx, row_days in enumerate([ROW1_DAYS, ROW2_DAYS]):
        for col_idx, day in enumerate(row_days):
            left   = (col_idx * panel_w) / fig_w
            bottom = 1 - (row_idx + 1) * panel_h / fig_h
            ax = fig.add_axes([left, bottom, panel_w / fig_w, panel_h / fig_h])
            ax.axis('off')

            if day in images_by_day:
                img = images_by_day[day]
                ax.imshow(apply_CLAHE(img), cmap='RdYlGn_r', aspect='auto')

                ax.text(0.03, 0.97, f"D{day}",
                        transform=ax.transAxes,
                        fontsize=7, fontweight='bold', color='white',
                        ha='left', va='top')

                bf_img = bb_images.get(day)
                if bf_img is not None:
                    mask = create_mouse_mask(bf_img)
                    if mask is not None:
                        if mask.shape != img.shape[:2]:
                            from skimage.transform import resize
                            mask = resize(mask, img.shape[:2], order=0,
                                          preserve_range=True, anti_aliasing=False) > 0.5
                        mask_u8 = mask.astype(np.uint8) * 255
                        contours, _ = cv2.findContours(mask_u8, cv2.RETR_EXTERNAL,
                                                       cv2.CHAIN_APPROX_SIMPLE)
                        if contours:
                            c = max(contours, key=cv2.contourArea).squeeze()
                            if c.ndim == 2 and c.shape[0] > 2:
                                ax.plot(c[:, 0], c[:, 1],
                                        color='cyan', linewidth=0.3, alpha=0.9)

    fig.suptitle(f"Laser {laser} nm, Filter {filter_set}",
                 fontsize=9, fontweight='bold', y=1.01)

    filename = f"{file_prefix}_laser{laser}_filter{filter_set}.png"
    save_path = os.path.join(save_folder, filename)
    plt.savefig(save_path, dpi=dpi, bbox_inches='tight', pad_inches=0)
    plt.close()
    print(f"      ✅ Saved: {filename}")

# ============================================================================
# SHARED PLOT LOOP (used by all layouts)
# ============================================================================

def process_and_plot_mouse(data, label, output_dir):
    """Given loaded mouse data dict, generate all 2x3 grid plots."""
    total = 0
    if not data['success']:
        print("    ❌ Skipping — failed to load data."); return 0

    bb_found = len(data['bb_images_by_day'])
    print(f"    BB images found for days: "
          f"{sorted(data['bb_images_by_day'].keys()) if bb_found else 'none'}")

    lasers      = data['condition_data']['lasers']
    filter_list = data['condition_data']['filters']
    n_cond      = len(lasers)

    mouse_out = os.path.join(output_dir, label)
    os.makedirs(mouse_out, exist_ok=True)

    for ci in range(n_cond):
        laser_val  = lasers[ci]
        filter_val = filter_list[ci]
        print(f"    [{ci+1}/{n_cond}] Laser {laser_val} nm, Filter {filter_val}...")

        cond_imgs     = data['condition_data']['condition_images'][ci]
        images_by_day = {d: cond_imgs[d] for d in ALL_DAYS if d in cond_imgs}

        try:
            plot_and_save_2x3_grid(
                {'images_by_day': images_by_day,
                 'bb_images_by_day': data['bb_images_by_day']},
                laser_val, filter_val, mouse_out, file_prefix=label
            )
            total += 1
        except Exception as e:
            print(f"      ❌ Failed: {e}")
    return total

# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 70)
    print("LONGITUDINAL TUMOR VISUALIZATION - ALL MICE, 2×3 GRIDS")
    print("=" * 70)

    root_folder = input("\nEnter ROOT folder path: ").strip().strip('"')
    if not os.path.exists(root_folder):
        print(f"❌ Folder does not exist: {root_folder}"); return

    # Day selection
    default_days = [1, 2, 3, 7, 10, 14]
    day_input = input(f"\nEnter days to include (comma-separated), or press Enter for default {default_days}: ").strip()
    if day_input:
        try:
            ALL_DAYS[:] = sorted(set(int(d.strip()) for d in day_input.split(',')))
            print(f"  Using days: {ALL_DAYS}")
        except ValueError:
            print(f"  ⚠️  Invalid input, using default days: {default_days}")
            ALL_DAYS[:] = default_days
    else:
        ALL_DAYS[:] = default_days
        print(f"  Using default days: {ALL_DAYS}")

    # Rebuild row assignments from ALL_DAYS
    global ROW1_DAYS, ROW2_DAYS
    half = len(ALL_DAYS) // 2
    ROW1_DAYS = ALL_DAYS[:half] if len(ALL_DAYS) >= 2 else ALL_DAYS
    ROW2_DAYS = ALL_DAYS[half:] if len(ALL_DAYS) >= 2 else []

    layout, hdr_or_root, raw_root = detect_layout(root_folder)

    output_dir = os.path.join(root_folder, "2x3_grids_output")
    os.makedirs(output_dir, exist_ok=True)
    print(f"\n📁 Output: {output_dir}")

    total_plots = 0

    # ------------------------------------------------------------------
    # PILOT LAYOUT
    # ------------------------------------------------------------------
    if layout == 'pilot':
        mice = find_all_mice_pilot(hdr_or_root)
        if not mice:
            print("❌ No m{N} subfolders found under HDR_h5."); return

        print(f"\n✅ Found {len(mice)} mouse(s):")
        for m in mice:
            print(f"   • {m['label']}")

        for mouse_info in mice:
            label  = mouse_info['label']
            mid    = mouse_info['mouse_name']
            hdr_sf = mouse_info['hdr_subfolder']
            print(f"\n{'─'*60}\n  {label}\n{'─'*60}")

            data = load_mouse_data_pilot(mid, hdr_sf, raw_root, ALL_DAYS)
            total_plots += process_and_plot_mouse(data, label, output_dir)

    # ------------------------------------------------------------------
    # NEW LAYOUT
    # ------------------------------------------------------------------
    elif layout == 'new':
        mice = find_all_mice_new(hdr_or_root)
        if not mice:
            print("❌ No DL-style HDR files found."); return

        print(f"\n✅ Found {len(mice)} mouse ID(s):")
        for m in mice:
            print(f"   • {m['label']}")

        for mouse_info in mice:
            label    = mouse_info['label']
            mouse_id = mouse_info['mouse_name']
            print(f"\n{'─'*60}\n  {label}\n{'─'*60}")

            data = load_mouse_data_new(mouse_id, hdr_or_root, raw_root, ALL_DAYS)
            total_plots += process_and_plot_mouse(data, label, output_dir)

    # ------------------------------------------------------------------
    # ORIGINAL LAYOUT
    # ------------------------------------------------------------------
    else:
        mice = find_all_mice_original(root_folder)
        if not mice:
            print("❌ No mouse folders found (expected mX folders under root)."); return

        print(f"\n✅ Found {len(mice)} mouse folder(s):")
        for m in mice:
            print(f"   • {m['label']}")

        for mouse_info in mice:
            label      = mouse_info['label']
            mouse_name = mouse_info['mouse_name']
            print(f"\n{'─'*60}\n  {label}\n{'─'*60}")

            data = load_mouse_data_original(mouse_info['path'], mouse_name, ALL_DAYS)
            total_plots += process_and_plot_mouse(data, label, output_dir)

    print(f"\n{'='*70}")
    print(f"✅ Done — {total_plots} total plots saved to:")
    print(f"   {output_dir}/")

if __name__ == '__main__':
    main()