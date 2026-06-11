# DENNIS_helpers

Small, reusable helper scripts for the DENNIS Lab (quantum-dot synthesis and SWIR imaging), plus the documentation that gets new lab members from zero software experience to confident contributor.

This repository holds general-purpose tools, not project-specific analysis. A helper is something you would reach for across many projects, like a script that inspects an HDF5 data file. Code that only makes sense for one study belongs in that study's own repository.

## What's here

- `docs/` — the onboarding guide, numbered in reading order. Start at `docs/00_python_code_basics.md` and work up.
- `scripts/` — runnable Python helpers (`.py` files). The worked example is `scripts/show_h5_keys.py`.
- `notebooks/` — Jupyter notebooks (`.ipynb` files) for interactive exploration.
- `environment.yml` — the definition of the shared conda environment, named `helper`.
- `.pre-commit-config.yaml` — automatic notebook cleanup before each commit (see `docs/07_notebooks.md`).

## New here? Read the docs first

If you have never used Git, the command line, or conda, do not start by typing commands. Read the docs in order. They define every term on first use and assume no prior tooling. The whole set is short. At minimum, read `00` through `05` before you make your first change.

## Quick start

These steps assume you have already cloned the repository and have Miniconda and VS Code installed. If any of that is unfamiliar, `docs/03_getting_started_with_git.md` and `docs/04_environments.md` cover it from the beginning.

1. Create the shared environment from the definition file:

   ```
   conda env create -f environment.yml
   ```

   This reads `environment.yml` and builds a conda environment named `helper` with the packages the lab uses.

2. Turn the environment on:

   ```
   conda activate helper
   ```

   Your terminal prompt will now show `(helper)`. Every command in the docs assumes this environment is active.

3. Try the worked example on one of your own data files:

   ```
   python scripts/show_h5_keys.py path/to/data.h5
   ```

   This prints the structure of an HDF5 file: every group, every dataset with its shape and dtype, and any attached metadata. It is the example used throughout `docs/00`, `docs/01`, and `docs/06`.

## Contributing

Read `CONTRIBUTING.md` before adding a script or opening a pull request. The short version: make a branch, keep helpers small and well-named, write a docstring, and have one person review the change.

## The `dev/` folder

The `dev/` folder contains the design briefs used to build these docs and is kept for historical reference.
