---
name: publication-figures
description: Build publication-ready scientific figures to a consistent standard — column-fitted sizing, a colorblind-safe palette, redundant encoding, A/B/C panel labels, journal typography, and vector export. Use this whenever creating, revising, or assembling any figure bound for a manuscript, paper, journal submission, poster, or thesis, including a single-panel plot or a multi-panel figure, with matplotlib or any plotting library. Reach for it even when the request just says "make a figure", "plot this", "build the panel", or "put the figure together" in a research or paper-writing context and does not use the word "publication".
---

# Publication-ready figures

Use this skill when a figure is bound for a manuscript, poster, or thesis, where it will be printed
at a fixed column width and read by people with a range of color vision and on a range of media.
The defaults here are a brand-neutral starting point. They are chosen to be defensible for most
journals, and the palette, widths, and fonts are meant to be edited for a specific journal or lab
(see Tailoring). Exploratory plots that will never leave the analysis do not need this skill.

Follow the steps below in order. Each one prevents a specific way a figure goes wrong on the page.

## 1. Decide the width, and set it first

A journal fixes a figure's printed width, and every font size in the figure is read at that width,
so choose the width before drawing anything and set `figsize` from it. Pick single-column (~3.3 in)
or double-column (~6.9 in); a row of several panels sums to one of those widths including the gaps,
not to a per-panel width times the panel count. `references/layout.md` gives the numbers, the
multi-panel rule, and why a saved figure must never be cropped or resized afterward (doing so
rescales all the type). Read it before sizing a multi-panel figure.

## 2. Apply the shared style once

Load `assets/publication.mplstyle` before building the figure. It sets the fonts, the type-size
hierarchy, the export settings, and the default color cycle, so every panel inherits the same
standard instead of each one being styled by hand.

```python
import matplotlib.pyplot as plt
plt.style.use("<path-to-this-skill>/assets/publication.mplstyle")
```

## 3. Use safe colors, and give categories a second cue

Draw categorical data from the default palette in the style file; it is colorblind-safe by design.
For continuous data use a perceptually uniform colormap (`viridis` or `cividis`), never rainbow or
jet. Because color-vision deficiency and grayscale printing both drop hue, give each category a
second, non-color cue as well — a distinct marker shape or line style — so the distinction survives.
`references/palette.md` explains the palette, the colormap choices, and redundant encoding.

Run the checker on any palette you choose or edit, and fix what it fails:

```bash
python <path-to-this-skill>/scripts/check_palette.py "#0072B2" "#E69F00" "#009E73"
```

It fails when two colors are confusable to every reader, and it advises where colors are close in
lightness (the pairs that need the redundant encoding above).

## 4. Label the panels consistently

Label a multi-panel figure A, B, C in bold, at the same size and the same corner on every panel, so
the reader locates them without hunting. Place each label at a consistent position relative to its
panel rather than nudging each one by hand. See the panel-label and typography sections of
`references/layout.md`.

## 5. Export a vector file and a raster

Write a vector PDF for the manuscript and a high-resolution PNG for viewing. The style file sets
600 dpi for the raster and embeds real fonts in the vector file, so the text stays selectable and
renders the same on a reviewer's machine.

```python
fig.savefig("figure3.pdf")   # vector, for submission
fig.savefig("figure3.png")   # raster, for viewing
```

## Checklist

- [ ] Width chosen from the target column and set with `figsize` at creation; the saved file is
  never cropped or resized.
- [ ] `publication.mplstyle` applied once before plotting.
- [ ] Categorical colors from the safe palette; continuous data on a perceptually uniform colormap;
  `check_palette.py` run on any edited palette.
- [ ] Each category carries a non-color cue (marker or line style) as well as color.
- [ ] Multi-panel figures labeled A, B, C consistently.
- [ ] Exported as vector PDF plus high-resolution PNG, with fonts embedded.

## Tailoring

The palette, column widths, and type sizes are defaults, not rules. When adopting this skill into a
project, edit `assets/publication.mplstyle` and the two reference files to the target journal's
widths and any project-specific colors (for example, a fixed shade per experimental condition), and
re-run `check_palette.py` on the new palette. The workflow above stays the same; only the values
change.

## Files in this skill

- `references/palette.md` — the colorblind-safe palette, colormap choices, and redundant encoding.
- `references/layout.md` — column widths, the multi-panel rule, type hierarchy, and export.
- `assets/publication.mplstyle` — the matplotlib style that applies fonts, sizes, colors, and
  export settings.
- `scripts/check_palette.py` — a palette legibility checker (full-color distinctness and a
  grayscale/color-vision advisory).
