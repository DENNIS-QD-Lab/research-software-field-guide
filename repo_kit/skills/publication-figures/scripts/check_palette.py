"""Check whether a set of figure colors stays distinguishable, in full color and in grayscale.

A categorical palette fails a reader when two of its colors are too close to tell apart. This
script converts each color to CIELAB and reports two different distances, because they guard against
two different failures:

- ``delta_e`` (CIE76) — overall perceptual distance in normal color vision. Two colors with a small
  ``delta_e`` look alike to everyone, so this is a hard requirement: the script's exit status fails
  if any pair falls below the threshold.
- ``lightness gap`` — the difference in perceived lightness (``L*``) alone. Lightness survives
  grayscale printing and is largely preserved under color-vision deficiency, so a pair that also
  differs in lightness stays legible when hue information is lost. This is reported as advice, not
  a failure, because a well-designed color-vision-safe palette need not separate every pair in
  lightness — the Okabe & Ito default shipped with this skill is a case in point. Where lightness
  is close, lean on redundant encoding (a different marker or line style, not color alone).

What this script does not do is simulate a specific color-vision deficiency. The lightness advice
is a dependency-free stand-in for that. For a rigorous check, simulate the palette under
deuteranopia, protanopia, and tritanopia with a dedicated library such as ``colorspacious`` or
``daltonlens``, then run this script on the simulated colors.

Example
-------
Check the Okabe & Ito default palette from the command line::

    python check_palette.py "#0072B2" "#E69F00" "#009E73" "#D55E00"
"""

from __future__ import annotations

import argparse
import itertools
import sys

# CIELAB reference white (D65, 2-degree observer), used to normalize XYZ before the Lab transform.
_D65 = (0.95047, 1.0, 1.08883)


def _srgb_to_linear(channel: float) -> float:
    """Undo the sRGB gamma curve for one 0-1 color channel.

    Parameters
    ----------
    channel : float
        One sRGB channel value in ``[0, 1]``.

    Returns
    -------
    float
        The linear-light value for that channel.

    Examples
    --------
    >>> round(_srgb_to_linear(1.0), 3)
    1.0
    """
    if channel <= 0.04045:
        return channel / 12.92
    return ((channel + 0.055) / 1.055) ** 2.4


def hex_to_lab(hex_color: str) -> tuple[float, float, float]:
    """Convert a hex color string to CIELAB ``(L*, a*, b*)``.

    Parameters
    ----------
    hex_color : str
        A color as ``"#RRGGBB"`` or ``"RRGGBB"`` (case-insensitive).

    Returns
    -------
    tuple[float, float, float]
        The color's ``L*`` (0-100), ``a*``, and ``b*`` coordinates.

    Examples
    --------
    >>> L, a, b = hex_to_lab("#000000")
    >>> round(L)
    0
    """
    text = hex_color.lstrip("#")
    if len(text) != 6:
        raise ValueError(f"expected a 6-digit hex color, got {hex_color!r}")
    r, g, b = (int(text[i : i + 2], 16) / 255 for i in (0, 2, 4))
    rl, gl, bl = (_srgb_to_linear(c) for c in (r, g, b))

    # Linear sRGB -> XYZ (D65).
    x = 0.4124564 * rl + 0.3575761 * gl + 0.1804375 * bl
    y = 0.2126729 * rl + 0.7151522 * gl + 0.0721750 * bl
    z = 0.0193339 * rl + 0.1191920 * gl + 0.9503041 * bl

    def f(t: float) -> float:
        return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116

    fx, fy, fz = f(x / _D65[0]), f(y / _D65[1]), f(z / _D65[2])
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def delta_e_76(
    lab1: tuple[float, float, float], lab2: tuple[float, float, float]
) -> float:
    """Return the CIE76 color difference between two CIELAB colors.

    Parameters
    ----------
    lab1, lab2 : tuple[float, float, float]
        Two colors as ``(L*, a*, b*)`` triples.

    Returns
    -------
    float
        The Euclidean distance in Lab space. Roughly, values under ~2.3 are indistinguishable to a
        careful eye; categorical figure colors want much more separation than that.

    Examples
    --------
    >>> round(delta_e_76((0, 0, 0), (100, 0, 0)))
    100
    """
    return sum((a - b) ** 2 for a, b in zip(lab1, lab2)) ** 0.5


def check_palette(hex_colors: list[str], min_delta_e: float = 25.0) -> list[str]:
    """Report color pairs that look too similar in normal color vision.

    This is the hard check: colors that are this close are confusable for every reader, so a pair
    below the threshold is a genuine defect in the palette.

    Parameters
    ----------
    hex_colors : list[str]
        The palette to check, as hex strings.
    min_delta_e : float, optional
        Smallest acceptable CIE76 distance between any two colors. Defaults to ``25.0``, a
        comfortable margin for categorical colors that a bare just-noticeable-difference (~2.3)
        would undershoot.

    Returns
    -------
    list[str]
        One warning per offending pair; empty if every pair is distinct enough.

    Examples
    --------
    >>> check_palette(["#000000", "#010101"])
    ['#000000 vs #010101: delta_e 0.3 (< 25.0)']
    """
    labs = [(c, hex_to_lab(c)) for c in hex_colors]
    warnings: list[str] = []
    for (c1, lab1), (c2, lab2) in itertools.combinations(labs, 2):
        de = delta_e_76(lab1, lab2)
        if de < min_delta_e:
            warnings.append(f"{c1} vs {c2}: delta_e {de:.1f} (< {min_delta_e})")
    return warnings


def grayscale_notes(
    hex_colors: list[str], min_lightness_gap: float = 15.0
) -> list[str]:
    """Report color pairs that are close in lightness, so may merge in grayscale or under CVD.

    This is advisory, not a failure. A flagged pair is fine in full color; it just relies on
    something other than color -- a distinct marker or line style -- to stay separable when hue is
    lost to grayscale printing or color-vision deficiency.

    Parameters
    ----------
    hex_colors : list[str]
        The palette to check, as hex strings.
    min_lightness_gap : float, optional
        Smallest ``L*`` difference below which a pair is flagged. Defaults to ``15.0``.

    Returns
    -------
    list[str]
        One note per close-in-lightness pair; empty if all pairs are well separated in lightness.

    Examples
    --------
    >>> grayscale_notes(["#000000", "#ffffff"])
    []
    """
    labs = [(c, hex_to_lab(c)) for c in hex_colors]
    notes: list[str] = []
    for (c1, lab1), (c2, lab2) in itertools.combinations(labs, 2):
        dl = abs(lab1[0] - lab2[0])
        if dl < min_lightness_gap:
            notes.append(
                f"{c1} vs {c2}: lightness gap {dl:.1f} (< {min_lightness_gap})"
            )
    return notes


def main() -> int:
    """Print a pass/fail palette report from hex colors given on the command line.

    Returns
    -------
    int
        ``0`` if every pair is distinct in full color, ``1`` if any pair fails, so the check can
        gate a script or CI step. Grayscale notes are printed but do not change the exit status.

    Examples
    --------
    >>> main  # doctest: +ELLIPSIS
    <function main at ...>
    """
    parser = argparse.ArgumentParser(
        description="Check a categorical figure palette for legibility."
    )
    parser.add_argument(
        "colors", nargs="+", help="hex colors, e.g. '#0072B2' '#E69F00'"
    )
    parser.add_argument("--min-delta-e", type=float, default=25.0)
    parser.add_argument("--min-lightness-gap", type=float, default=15.0)
    args = parser.parse_args()

    print("Lightness (L*, 0-100) of each color, darkest to lightest:")
    for color in sorted(args.colors, key=lambda c: hex_to_lab(c)[0]):
        print(f"  {color}  L* = {hex_to_lab(color)[0]:5.1f}")

    failures = check_palette(args.colors, args.min_delta_e)
    if failures:
        print(f"\nFAIL: {len(failures)} pair(s) look too similar to every reader:")
        for failure in failures:
            print(f"  - {failure}")
    else:
        print(f"\nOK: all {len(args.colors)} colors are distinct in full color.")

    notes = grayscale_notes(args.colors, args.min_lightness_gap)
    if notes:
        print(
            f"\nGrayscale/color-vision advice ({len(notes)} pair(s) close in lightness) — these"
        )
        print(
            "rely on a distinct marker or line style, not color alone, to stay separable:"
        )
        for note in notes:
            print(f"  - {note}")
        print(
            "\nFor a rigorous color-vision check, simulate the palette under deuteranopia,"
        )
        print(
            "protanopia, and tritanopia (colorspacious, daltonlens) and re-run this script on it."
        )

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
