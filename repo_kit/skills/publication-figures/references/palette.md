# Color for scientific figures

The colors in a figure carry meaning, so they have to survive the ways a reader will actually
encounter them: on screen, printed, photocopied in black and white, and seen by the roughly one in
twelve men (and one in two hundred women) with a red-green color-vision deficiency. A palette chosen
only to look pleasant on the author's monitor often loses one of its distinctions in one of those
settings. The defaults below are chosen to hold up across all of them, and they are a starting
point you adjust for your journal or lab.

## The default categorical palette

The eight colors below are the Okabe & Ito set, designed so that no two remain confusable under the
common forms of color-vision deficiency. They are the default color cycle in
`assets/publication.mplstyle`, in this order:

| Order | Hex | Name |
|-------|---------|------------------|
| 1 | `#0072B2` | blue |
| 2 | `#E69F00` | orange |
| 3 | `#009E73` | bluish green |
| 4 | `#D55E00` | vermillion |
| 5 | `#56B4E9` | sky blue |
| 6 | `#CC79A7` | reddish purple |
| 7 | `#F0E442` | yellow |
| 8 | `#000000` | black |

Use as few of them as the figure needs. A reader tells three or four categories apart at a glance;
past about six, even a well-separated palette becomes a legend the reader has to keep consulting. If
a figure needs more than six categories, a different encoding (small multiples, direct labels, or
grouping) usually reads better than more colors.

## Continuous data

For a quantity that varies smoothly, such as an intensity map or a heatmap, use a perceptually
uniform colormap, where equal steps in the data map to equal-looking steps in color. `viridis` and
`cividis` are perceptually uniform and remain readable under color-vision deficiency; `cividis` is
the safer of the two for that purpose. For data that diverges around a meaningful center, such as a
difference from zero, pick a perceptually uniform diverging map (for example `PuOr`, or one of Fabio
Crameri's scientific colormaps like `vik`).

Avoid the rainbow and jet colormaps. Their brightness rises and falls unevenly across the range, so
they invent visual boundaries where the data is smooth and flatten real gradients where it is
steep, and several of their bands collapse together under color-vision deficiency.

## Do not rely on color alone

Color-vision deficiency and grayscale printing both remove hue while leaving lightness, so any
distinction carried only by color can vanish. Give each category a second cue that does not depend
on color: a distinct marker shape for scatter points, a distinct dash pattern for lines, or a direct
text label on the trace. The redundancy costs nothing for a full-color reader and keeps the figure
legible for everyone else.

## Checking a palette

`scripts/check_palette.py` takes a list of hex colors and reports two things:

- whether any two colors are too close to tell apart in normal color vision, which it treats as a
  failure, since those colors are confusable for every reader; and
- which pairs are close in lightness, reported as advice, since those are the pairs that merge in
  grayscale or under color-vision deficiency and therefore need the redundant encoding above.

```
python scripts/check_palette.py "#0072B2" "#E69F00" "#009E73" "#D55E00"
```

The lightness advice is a quick, dependency-free stand-in for a full simulation, not a substitute
for one. The Okabe & Ito palette passes the full-color check and still draws several lightness
notes, which is expected: it earns its color-vision safety through hue choices rather than by
separating every pair in lightness. For a rigorous check against a specific deficiency, simulate the
palette under deuteranopia, protanopia, and tritanopia with a library such as `colorspacious` or
`daltonlens`, then run the script on the simulated colors.

## Tailoring

The palette here is a neutral default. When a project has its own meaning-bearing colors — a set of
experimental conditions that always appear in the same shades, or a journal's house style — encode
those in the project's own copy of this skill and its `publication.mplstyle`. After changing any
colors, run `check_palette.py` on the new set so a well-intentioned edit does not quietly reintroduce
a confusable pair.
