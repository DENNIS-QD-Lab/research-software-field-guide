"""Compare HDR weighting functions using the default fusion method.

Runs all six weighting functions (debevec, robertson, broadhat, square,
linear, none) against a folder of multi-exposure HDF5 images and reports
the dynamic range produced by each. Reproduces the analysis in Figure 4g
of the lab's HDR paper.

Inputs:
    h5_folder:   Path to the folder containing the multi-exposure .h5 files.
    data_folder: Path to the folder containing calibration data (parameters).
    experiment:  A short name for the experiment, used in output filenames.

Example call:
    python scripts/compare_hdr_weights.py \\
        --h5_folder data/Images/ICG_images/ICGplate3 \\
        --data_folder data \\
        --experiment ICGplate3
"""

import argparse
import glob
import os

import matplotlib.pyplot as plt
import numpy as np
import tifffile
from PIL import Image

from Step1_import import load_parameters
from Step2_radiance import (
    broadhat,
    debevec,
    linear,
    none,
    process_hdr_images,
    robertson,
    square,
)

# Each entry pairs a weighting function with a human-readable description.
WEIGHTING_TESTS: list[dict] = [
    {"weight": debevec,   "desc": "Triangle (paper choice)"},
    {"weight": robertson, "desc": "Gaussian"},
    {"weight": broadhat,  "desc": "Broadhat / Reinhard"},
    {"weight": square,    "desc": "Window / Vinegoni"},
    {"weight": linear,    "desc": "Linear ramp"},
    {"weight": none,      "desc": "No weighting (uniform)"},
]


def load_calibration(data_folder: str) -> dict[str, float]:
    """Load the sensor calibration coefficients from the data folder.

    Args:
        data_folder: Path to the folder containing the calibration files
            readable by ``load_parameters``.

    Returns:
        Dictionary with keys ``Smax``, ``Sd``, and ``b``.

    Example:
        >>> coefficients = load_calibration("data")
    """
    params = load_parameters(data_folder)
    return {"Smax": params["Smax"], "Sd": params["Sd"], "b": params["b"]}


def run_single_weight(
    h5_folder: str,
    experiment: str,
    coefficients: dict[str, float],
    weight_fn,
    desc: str,
) -> dict:
    """Run HDR fusion for one weighting function and return statistics.

    Changes into ``h5_folder`` for the duration of the call, then restores
    the original working directory regardless of success or failure.

    Args:
        h5_folder:    Path to the folder of multi-exposure .h5 files.
        experiment:   Short experiment name passed to ``process_hdr_images``.
        coefficients: Calibration coefficients from ``load_calibration``.
        weight_fn:    One of the weighting function objects from Step2_radiance.
        desc:         Human-readable label for this weighting function.

    Returns:
        Dictionary with keys: ``weighting``, ``desc``, ``success``, and
        (on success) ``dynamic_range_db``, ``mean_log``, ``std_log``,
        ``min_log``, ``max_log``. On failure, includes ``error``.

    Example:
        >>> result = run_single_weight("data/h5", "ICGplate3", coefs, debevec, "Triangle")
    """
    original_dir = os.getcwd()
    result: dict = {"weighting": weight_fn.__name__, "desc": desc, "success": False}

    try:
        os.chdir(h5_folder)
        processed = process_hdr_images(
            directory=".",
            experiment_title=experiment,
            base_data_folder="",
            coefficients_dict=coefficients,
            response_curve="default",
            smoothing_lambda=1000,
            weighting_function=weight_fn,
            method="default",
        )

        if not processed:
            result["error"] = "No data returned"
            return result

        rad_map = processed[0]["radiance_map"]
        rad_linear = np.exp(rad_map)
        mean_positive = np.mean(rad_linear[rad_linear > 0])

        result.update(
            {
                "success": True,
                "mean_log": float(np.mean(rad_map)),
                "std_log": float(np.std(rad_map)),
                "min_log": float(np.min(rad_map)),
                "max_log": float(np.max(rad_map)),
                "dynamic_range_db": float(
                    20 * np.log10(np.max(rad_linear) / (mean_positive + 1e-10))
                ),
            }
        )

    except Exception as exc:
        result["error"] = str(exc)[:150]

    finally:
        os.chdir(original_dir)

    return result


def run_all_weights(
    h5_folder: str,
    experiment: str,
    coefficients: dict[str, float],
) -> list[dict]:
    """Run HDR fusion for every weighting function in WEIGHTING_TESTS.

    Args:
        h5_folder:    Path to the folder of multi-exposure .h5 files.
        experiment:   Short experiment name.
        coefficients: Calibration coefficients from ``load_calibration``.

    Returns:
        List of result dictionaries, one per weighting function. See
        ``run_single_weight`` for the dictionary structure.

    Example:
        >>> results = run_all_weights("data/h5", "ICGplate3", coefs)
    """
    results = []
    total = len(WEIGHTING_TESTS)

    for index, test in enumerate(WEIGHTING_TESTS, start=1):
        print(f"\n[{index}/{total}] {test['weight'].__name__} — {test['desc']}")
        result = run_single_weight(
            h5_folder, experiment, coefficients, test["weight"], test["desc"]
        )
        if result["success"]:
            print(f"  ✅  Dynamic range: {result['dynamic_range_db']:.2f} dB")
        else:
            print(f"  ❌  Failed: {result.get('error', 'unknown error')}")
        results.append(result)

    return results


def export_png_images(
    results: list[dict],
    final_folder: str,
) -> list[dict]:
    """Export a normalised PNG for each successful result's log-radiance TIFF.

    Searches ``final_folder`` for a TIFF whose name contains the weighting
    function name and ends in ``_log.tif``, normalises it to 0–255, and saves
    it as a PNG alongside the TIFF.

    Args:
        results:      List of result dictionaries from ``run_all_weights``.
        final_folder: Path to the folder where TIFF outputs were written.

    Returns:
        Subset of ``results`` for which a PNG was successfully written.
        Each returned dict gains ``png_file`` and ``image_data`` keys.

    Example:
        >>> exported = export_png_images(results, "data/h5/final_data")
    """
    exported = []

    for result in results:
        if not result.get("success"):
            continue

        pattern = os.path.join(final_folder, f"*{result['weighting']}*_log.tif")
        tif_files = sorted(glob.glob(pattern))

        if not tif_files:
            print(f"  No TIFF found for {result['weighting']}")
            continue

        try:
            hdr_img = tifffile.imread(tif_files[-1])
            normalised = (
                (hdr_img - hdr_img.min()) / (hdr_img.max() - hdr_img.min()) * 255
            ).astype(np.uint8)

            png_path = os.path.join(final_folder, f"{result['weighting']}.png")
            Image.fromarray(normalised).save(png_path)

            result["png_file"] = png_path
            result["image_data"] = hdr_img
            exported.append(result)
            print(f"  ✅  {os.path.basename(png_path)}")

        except Exception as exc:
            print(f"  ❌  {result['weighting']}: {exc}")

    return exported


def save_comparison_figure(
    exported_images: list[dict],
    final_folder: str,
    experiment: str,
    n_exposures: int,
) -> str:
    """Save a grid figure comparing all exported HDR images.

    Lays out the images in a 2×3 grid (or smaller if fewer than six),
    annotates each panel with its weighting function name, description,
    and dynamic range, and saves the figure as a PNG.

    Args:
        exported_images: List of result dicts that contain ``image_data``.
        final_folder:    Directory where the comparison PNG is saved.
        experiment:      Experiment name used in the figure title.
        n_exposures:     Number of input exposures, shown in the title.

    Returns:
        Absolute path to the saved comparison PNG.

    Example:
        >>> path = save_comparison_figure(exported, "data/final_data", "ICGplate3", 8)
    """
    n_imgs = len(exported_images)
    if n_imgs <= 3:
        n_rows, n_cols = 1, n_imgs
    elif n_imgs <= 4:
        n_rows, n_cols = 2, 2
    else:
        n_rows, n_cols = 2, 3

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(7 * n_cols, 6 * n_rows))
    axes_flat = np.array(axes).flatten() if n_imgs > 1 else np.array([axes])

    for idx, result in enumerate(exported_images):
        ax = axes_flat[idx]
        image = ax.imshow(result["image_data"], cmap="hot")
        ax.set_title(
            f"{result['weighting']}\n({result['desc']})\n"
            f"DR: {result['dynamic_range_db']:.1f} dB",
            fontsize=11,
            fontweight="bold",
        )
        ax.axis("off")
        plt.colorbar(image, ax=ax, fraction=0.046, pad=0.04)

    for idx in range(n_imgs, len(axes_flat)):
        axes_flat[idx].axis("off")

    fig.suptitle(
        f"Weighting Function Comparison (method=default)\n"
        f"{experiment} — {n_exposures} exposures",
        fontsize=14,
        fontweight="bold",
        y=0.98,
    )
    plt.tight_layout()

    output_path = os.path.join(final_folder, "WEIGHTING_COMPARISON_DEFAULT.png")
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close()

    return output_path


def save_report(
    results: list[dict],
    final_folder: str,
    experiment: str,
    n_exposures: int,
) -> str:
    """Write a plain-text summary report of all weighting function results.

    Args:
        results:      Full list of result dicts from ``run_all_weights``.
        final_folder: Directory where the report file is saved.
        experiment:   Experiment name written into the report header.
        n_exposures:  Number of input exposures written into the report.

    Returns:
        Absolute path to the saved report file.

    Example:
        >>> path = save_report(results, "data/final_data", "ICGplate3", 8)
    """
    report_path = os.path.join(final_folder, "WEIGHTING_COMPARISON_REPORT.txt")
    successful = [r for r in results if r.get("success")]

    with open(report_path, "w") as report_file:
        report_file.write("=" * 70 + "\n")
        report_file.write("WEIGHTING FUNCTION COMPARISON — DEFAULT METHOD\n")
        report_file.write("=" * 70 + "\n\n")
        report_file.write(f"Experiment:  {experiment}\n")
        report_file.write(f"Exposures:   {n_exposures}\n\n")

        for result in results:
            label = result.get("weighting", "unknown")
            report_file.write(f"{label} ({result.get('desc', '')}):\n")
            if result.get("success"):
                report_file.write(f"  Status:          SUCCESS\n")
                report_file.write(f"  Dynamic range:   {result['dynamic_range_db']:.2f} dB\n")
                report_file.write(
                    f"  Log radiance:    {result['min_log']:.4f} to {result['max_log']:.4f}\n"
                )
                report_file.write(
                    f"  Mean / Std:      {result['mean_log']:.4f} / {result['std_log']:.4f}\n"
                )
            else:
                report_file.write(f"  Status:  FAILED\n")
                report_file.write(f"  Error:   {result.get('error', 'unknown')}\n")
            report_file.write("\n")

        if len(successful) > 1:
            dynamic_ranges = [r["dynamic_range_db"] for r in successful]
            report_file.write("SUMMARY STATISTICS\n")
            report_file.write("-" * 70 + "\n")
            report_file.write(f"  Mean DR:   {np.mean(dynamic_ranges):.2f} dB\n")
            report_file.write(f"  Std dev:   {np.std(dynamic_ranges):.3f} dB\n")
            report_file.write(
                f"  Range:     {np.min(dynamic_ranges):.2f} – {np.max(dynamic_ranges):.2f} dB\n"
            )

    return report_path


def main() -> None:
    """Parse arguments and run the full weighting function comparison."""
    parser = argparse.ArgumentParser(
        description="Compare HDR weighting functions on a multi-exposure dataset."
    )
    parser.add_argument(
        "--h5_folder",
        required=True,
        help="Path to the folder containing the multi-exposure .h5 files.",
    )
    parser.add_argument(
        "--data_folder",
        required=True,
        help="Path to the folder containing calibration data.",
    )
    parser.add_argument(
        "--experiment",
        required=True,
        help="Short experiment name used in output filenames and titles.",
    )
    args = parser.parse_args()

    h5_files = glob.glob(os.path.join(args.h5_folder, "*.h5"))
    print(f"Dataset: {args.experiment} ({len(h5_files)} exposures)")

    print("\nLoading calibration...")
    coefficients = load_calibration(args.data_folder)

    print("\nRunning weighting function tests...")
    results = run_all_weights(args.h5_folder, args.experiment, coefficients)

    final_folder = os.path.join(args.h5_folder, "final_data")
    os.makedirs(final_folder, exist_ok=True)

    print("\nExporting PNG images...")
    exported_images = export_png_images(results, final_folder)

    if exported_images:
        print("\nSaving comparison figure...")
        figure_path = save_comparison_figure(
            exported_images, final_folder, args.experiment, len(h5_files)
        )
        print(f"  Saved: {figure_path}")

    print("\nWriting report...")
    report_path = save_report(results, final_folder, args.experiment, len(h5_files))
    print(f"  Saved: {report_path}")

    successful = [r for r in results if r.get("success")]
    print(f"\nDone. {len(successful)}/{len(results)} weighting functions succeeded.")


if __name__ == "__main__":
    main()
