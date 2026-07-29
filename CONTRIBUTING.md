# Contributing to DENNIS_helpers

This guide is the short version. The full reasoning behind each step lives in the numbered docs, linked below. If a step is unfamiliar, follow the link before doing it.

## Before you start

Work inside the shared environment. Activate it with `conda activate helper` so your prompt shows `(helper)`. If you have not created it yet, see [04_environments.md](docs/onboarding/04_environments.md). Confirm the repository lives in a normal folder on your machine and not inside OneDrive, iCloud, or Dropbox, which corrupt Git repositories. See [03_getting_started_with_git.md](docs/onboarding/03_getting_started_with_git.md).

## The workflow

Every change, even a one-line fix, follows the same loop: pull the latest code, make a branch, do the work, commit, push, and open a pull request. The full loop with both the VS Code Source Control panel and the equivalent terminal commands is in [05_daily_workflow.md](docs/onboarding/05_daily_workflow.md). We use branches for every change because they keep the `main` branch working and give you a safe place to experiment.

Write commit messages as one line, in the imperative present tense. Write "Add HDF5 inspector," not "Added HDF5 inspector." A commit message finishes the sentence "If applied, this commit will..."

## What belongs here

Helpers are small, reusable, and not tied to a single project. A script that inspects any HDF5 file belongs here. A script that only processes the data from one specific study belongs in that study's own repository. When in doubt, ask in review.

Put runnable `.py` scripts in `scripts/` and Jupyter notebooks in `notebooks/`. Name scripts `verb_noun.py`, for example `show_h5_keys.py` or `plot_qd_spectra.py`. The full guidance on adding a script is in [06_adding_a_script.md](docs/onboarding/06_adding_a_script.md).

Every script needs a docstring at the top stating its purpose, its inputs, and an example call. [00_python_code_basics.md](docs/onboarding/00_python_code_basics.md) explains what a docstring is and why it matters.

## Notebooks

Notebooks need one extra setup step after you clone, so that Git does not record their cell outputs and execution counts. Run `pip install pre-commit` and then `pre-commit install` once. After that, the outputs are stripped from the committed version automatically while your local copy keeps them. The reasoning is in [07_notebooks.md](docs/onboarding/07_notebooks.md).

## Code review

Every pull request gets one reviewer. The reviewer checks that the code runs, has a docstring, has a sensible name, and does not duplicate a helper we already have. Reviews are collegial: ask questions rather than issue commands, suggest rather than demand, and assume the author did their best. How to review, approve, and merge in the GitHub interface is in [08_code_review.md](docs/onboarding/08_code_review.md).
