# Example repo structure

A single, extended example of what a repo built to this standard looks like once it's actually
grown into the whole shape — several experiment themes, each with multiple runs, a `figures/` folder
mid-manuscript, and the doc site generated from all of it. Doc 15's layout diagram shows the shape in
the abstract; this shows one plausible, fleshed-out instance of it, so you have something concrete to
compare your own repo against.

**This is a structure example, not a science example.** Every name below — module names, experiment
themes, figure titles, even the numbers in the manifests — is generic and invented to show the shape.


## The whole tree

```
your_project/
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   └── yourpkg/
│       ├── __init__.py
│       ├── preprocessing.py
│       ├── core_algorithm.py
│       └── postprocessing.py
├── tests/
│   ├── conftest.py
│   ├── test_preprocessing.py
│   └── test_core_algorithm.py
├── experiments/
│   ├── README.md
│   ├── _TEMPLATE.md
│   ├── _common/
│   │   ├── compare_methods.py
│   │   ├── runlog.py
│   │   └── embed_figures.py
│   ├── 01_baseline-comparison/
│   │   ├── README.md
│   │   ├── run_baseline_comparison.py
│   │   └── details/
│   │       ├── 260601_baseline/
│   │       ├── 260601_baseline_02/
│   │       └── 260615_baseline/
│   └── 02_edge-case-handling/
│       ├── README.md
│       ├── run_edge_cases.py
│       ├── notebooks/
│       │   └── explore_edge_cases_01.ipynb
│       └── details/
│           └── 260701_edge_case_sweep/
├── figures/
│   ├── README.md
│   ├── fig1_accuracy_comparison/
│   │   ├── make_fig1.py
│   │   └── details/
│   │       ├── 260810_v1/
│   │       └── 260815_v2/
│   └── fig2_edge_case_illustration/
│       ├── make_fig2.py
│       └── details/
│           └── 260812_v1/
├── docs/
│   ├── conf.py
│   ├── index.md
│   ├── api_reference.md
│   ├── experiment_overviews/
│   │   ├── 01_baseline-comparison_overview.md
│   │   └── 02_edge-case-handling_overview.md
│   ├── experiment_summaries/
│   └── figure_overviews/
│       └── figures_overview.md
├── sample_data/
│   └── example.h5
├── .claude/
│   └── experiments_playbook.md
├── local_paths_example.py
├── environment.yml
├── references.md
├── CLAUDE.md
├── pyproject.toml
└── README.md
```

`local_paths.py` itself (the one holding real machine-specific paths, copied from
`local_paths_example.py`) is deliberately not shown — it's git-ignored, per
[17_working_with_large_data.md](../implementing/17_working_with_large_data.md), and every machine
running this repo has its own.

## Why `01_baseline-comparison/details/` has three run folders

This is the part that's hard to picture from a diagram alone: a theme folder isn't one run, it's a
whole line of inquiry, and `details/` accumulates every run of it, preserved by default
([16_running_a_dry_lab_experiment.md](../implementing/16_running_a_dry_lab_experiment.md)):

- **`260601_baseline/`** — the first run.
- **`260601_baseline_02/`** — a same-day rerun (a `_NN` suffix, not an overwrite) — maybe a
  parameter was tweaked, or the first run was rerun to confirm it.
- **`260615_baseline/`** — a rerun two weeks later, likely after `src/core_algorithm.py` changed
  and the theme's README wanted a fresh number to cite.

None of the earlier two are deleted when the third lands, and not all of them reach the README. Here,
`260601_baseline_02` re-confirmed the first run without changing the answer, so neither one was ever
cited in a log entry — they just sit in `details/` as provenance, in case anything ever needs to
be checked against them. `260615_baseline` changed the result enough to matter, so it becomes the
*current* citation, swapped in for whatever the README pointed at before. When the comparison
*across* runs is itself the finding, rather than one run superseding the last,
[16_running_a_dry_lab_experiment.md](../implementing/16_running_a_dry_lab_experiment.md) covers the
other shape: citing several run ids in one entry instead of swapping one in for another.

## What one run's `details/` folder actually holds

Expanding `details/260615_baseline/`:

```
260615_baseline/
├── manifest.yaml
├── metrics.csv
└── comparison_plot.png
```

A representative `manifest.yaml`, matching the schema in
[16_running_a_dry_lab_experiment.md](../implementing/16_running_a_dry_lab_experiment.md):

```yaml
slug: baseline-comparison
summary: "Method A and Method B agree within tolerance on the synthetic baseline set."
driver: run_baseline_comparison.py
created: 2026-06-15T10:22:04
git:
  commit: a1b2c3d
  dirty: false
inputs:
  dataset: baseline_synthetic_v2
  dataset_sha256: 7e2f9a...
experimental_params:
  seed: 0
  threshold: 0.85
```

`comparison_plot.png` is the one figure worth keeping visible; a run that produced several plots but
only one worth citing would still only commit that one, git-ignoring the rest as regenerable scratch
output.

## What a theme's `README.md` looks like, filled in

An excerpt from `experiments/01_baseline-comparison/README.md` — a dated log entry citing the run
above, not a heading called "Findings":

```markdown
## 260615 — Method A vs. Method B on the full synthetic range

Method A and Method B agree to within 2% on the full synthetic range; Method A is roughly 3x
faster.

![](details/260615_baseline/comparison_plot.png)
*Run `260615_baseline` — reproduce with
`python experiments/01_baseline-comparison/run_baseline_comparison.py`.*

> **AMD:** Given the speed difference and no meaningful accuracy loss, Method A is the better default
> going forward.
```

## `figures/` mid-manuscript

`figures/README.md` is the paper's actual figure outline — every figure and supplementary figure, in
order, with its full caption, written once. `figures/fig1_accuracy_comparison/` holds only the
generation code, once that figure is built: a driver and a `details/` folder with dated attempts
(`260810_v1/`, then a revised `260815_v2/` after it was decided to switch to a log-scale axis) — no
separate README, so the caption is never duplicated. The `details/` discipline itself is nothing new
— it's `experiments/`'s own convention, reused
([22_publishing_a_paper.md](../disseminating/22_publishing_a_paper.md)). `figures/README.md` renders
into the doc site the same way an experiment theme's README does, so the manuscript's whole figure
outline is viewable and shareable as a Sphinx page, not just as files sitting in the repo.

## What the doc site generates from this

`docs/experiment_overviews/01_baseline-comparison_overview.md` is a thin page whose entire body is a
MyST `{include}` of `experiments/01_baseline-comparison/README.md` — so the log entry above,
figure and all, appears on the site exactly as written, with no separate copy to keep in sync
([readme_to_doc_site.md](readme_to_doc_site.md)). `docs/figure_overviews/figures_overview.md`
works identically, `{include}`-ing the single root `figures/README.md` instead — one page for the
whole figure outline, not one per figure. `docs/api_reference.md`
is the autodoc page generated from `src/yourpkg/`'s docstrings — named distinctly from the repo-root
`references.md` ledger of external citations, so the two are never confused. Building `sphinx-build docs docs/_build/html` turns all of
this into one browsable site: the library's API reference, the lab notebook's current findings, and the
manuscript's figure outline, all side by side, from the same commit.

## Which parts of this would typically be private

Tying back to [repo_ownership_and_visibility.md](repo_ownership_and_visibility.md): in a real project,
`experiments/` and `figures/` (mid-draft) are usually the private, unpolished parts of this tree —
a `src/` library that is disseminated may be visible much earlier.
