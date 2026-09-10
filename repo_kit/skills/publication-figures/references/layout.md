# Size, layout, and type for scientific figures

A manuscript figure is printed at a width the journal fixes, and every font size and line weight in
it is read at that final printed size. Getting the width right at the start, and leaving it alone
afterward, is what keeps the type legible and the proportions correct on the page. The values below
are neutral defaults; replace them with your target journal's numbers, which its guide for authors
states.

## Width is fixed; set it first

Most journals lay figures out in one or two columns, so a figure is sized to one of two widths:

| Placement | Typical width |
|--------------|---------------------|
| Single column | ~3.3 in (84 mm) |
| Double column | ~6.9 in (176 mm) |

Journals differ, so check the target's guide for authors and edit these. As one filled-in example,
the Dennis Lab standard is 3.2 in single and 6.5 in double. Set the figure's width from the chosen
column when you create it (`figsize=(width, height)` in matplotlib), before drawing anything.

## A row of panels sums to the column width

When several panels sit side by side, the whole row spans one column width, including the gaps
between panels. A three-across row in a double-column figure totals 6.9 in — about 2.2 in per panel
once the gaps are accounted for — rather than three panels of a fixed width added together. Sizing
each panel independently and letting the row grow produces a figure wider than the column, which the
journal then shrinks, undoing the type sizes you set.

Height is set by what the content needs and is not standardized. Only width is pinned, because only
width is constrained by the column.

## Do not rescale a saved figure

Every point size in a figure is measured against the figure size set at creation, so changing that
size after the fact rescales all of the type and line weights with it. A saved figure that is
cropped or resized — including by `bbox_inches='tight'`, which trims to the drawn content and so
changes the final width — can end up with 9-point text that is no longer 9 points on the page. Set
`figsize` correctly once, keep `savefig.bbox` at `standard`, and adjust spacing with the figure's
own margins and subplot parameters rather than by cropping the output.

## Type sizes

The sizes below form a clear hierarchy at the final printed size and are set by
`assets/publication.mplstyle`. They descend from the panel letter down to on-plot annotations, so
the eye reads the figure in that order.

| Element | Size | Weight |
|-------------------------------------|-------|---------|
| Panel letter (A, B, C) | 14 pt | bold |
| Axis title | 11 pt | bold |
| Axis tick numbering | 10 pt | regular |
| Legend and on-plot text | 9 pt | regular |
| Colorbar label (image panels only) | 10 pt | regular |
| Colorbar tick numbering | 9 pt | regular |

Any text a script draws itself — a statistical annotation, a fit label, an inset — has no shared
default, so set its size explicitly (9 pt for on-plot text) to keep it in the hierarchy.

## Panel labels

Label the panels of a multi-panel figure A, B, C, in bold, at the same size and the same corner
(usually upper-left) on every panel, so the reader finds them without hunting. Place each label in a
consistent position relative to its panel rather than nudging it by hand per panel, which drifts.

## Export

Write two files from each figure: a high-resolution raster for quick viewing and slides, and a
vector PDF for the manuscript. `assets/publication.mplstyle` sets 600 dpi for the raster and embeds
real font outlines in the vector file (`pdf.fonttype` and `ps.fonttype` 42), so the text stays
selectable and renders the same on a reviewer's machine as on yours.

```python
fig.savefig("figure3.pdf")   # vector, for the manuscript
fig.savefig("figure3.png")   # 600 dpi raster, for viewing
```

## Tailoring

The widths and type sizes here are defaults to edit, not rules to obey. Put your journal's column
widths and any house type sizes into the project's own `publication.mplstyle` and this file's copy
of the table, and the rest of the skill's guidance still applies unchanged.
