# CLAUDE.md — DENNIS Lab coding standards

This file is read automatically at the start of every Claude session in this repository. Follow these instructions for all code you write or edit here.

## Project context
This is the DENNIS Lab's internal repository of small helper scripts and notebooks for semiconductor quantum dot synthesis and SWIR imaging work. Contributors are graduate students who are scientists first, software developers second. Code in this repo will be read and modified by people with varying levels of experience, so prioritize readability over cleverness.

## Code style
- Follow PEP 8, enforced by `ruff format` and `ruff check`. Do not hand-format. If you're unsure how something should be formatted, run ruff or write it however and let the pre-commit hook fix it.
- Use snake_case for files, functions, and variables. Use PascalCase only for class names.
- Keep functions short. If a function is doing more than one thing, split it.
- Prefer explicit over implicit. Name variables for what they hold, not how short you can make the name.

## Documentation requirements
- Every function gets a docstring with: one-line summary, parameters (with types and meaning), return value, and one example call.
- Every module (`.py` file) gets a module-level docstring at the top describing what the file is for.
- Notebooks get a markdown cell at the top with the same information as a module docstring.
- Comments explain *why*, not *what*. The code itself shows what it does.

## Type hints
- Every function signature gets type hints on parameters and return value.
- Use the modern syntax: `list[int]` not `List[int]`, `dict[str, float]` not `Dict[str, float]`, `X | None` not `Optional[X]`.
- Python does not enforce type hints at runtime; they're for human readers and static checkers. Don't add runtime type assertions unless there's a specific reason.

## Naming conventions for files
- snake_case, lowercase, no hyphens, under about 30 characters.
- Verb-first for action scripts that *do* something when run: `show_keys.py`, `plot_spectra.py`, `convert_units.py`.
- Noun phrases for modules that *contain* importable functionality: `ratio_analysis.py`, `hdr_processing.py`, `broadband_segmentation.py`.
- Avoid abbreviations except universally understood domain terms (`hdf5`, `hdr`, `nir`, `qd`, `swir` are fine; `seg` for `segmentation` is not).

## Command line interfaces
- Any script that can be run from the command line uses `if __name__ == "__main__":` to wire up its CLI.
- Use `argparse` for arguments, not `sys.argv` parsing by hand.
- Scripts take file paths as arguments. Do not hardcode paths.

## Data handling
- Never commit data files to this repo. Data lives outside the repo; scripts take paths as arguments.
- If you generate intermediate files for testing, put them in a directory listed in `.gitignore` and clean them up.
- One exception: small *teaching and test fixtures* (used by tutorials, examples, and tests) may be committed, synthetic ones under `sample_data/` and test fixtures alongside the tests. A fixture may be synthetic *or* a small, curated handful of real samples — enough to exercise the code and show a realistic case, not the full depth of acquired data. The guiding line is size and purpose, not synthetic-versus-real: a few KB up to a few MB that a reader or a test actually needs is fine; an entire acquired dataset bloats history permanently and stays out of the repo.
- Keep machine-specific paths out of committed code and notebooks. Put them in a gitignored `local_paths.py` (copy `local_paths_example.py`) and import from it.

## Dependencies
- Ask before adding new dependencies. If approved, update `environment.yml` and explain why in the PR description.
- Prefer packages already in the environment over adding new ones.
- Prefer conda packages from conda-forge over pip when both are available.

## Notebooks
- Outputs are stripped on commit by nbstripout. Don't fight this; assume reviewers run the notebook themselves.
- A notebook should run top to bottom without errors. If a cell depends on a previous cell, it must appear after that cell.
- Each notebook starts with a markdown cell describing purpose, inputs, and an example invocation.

## When adding a new helper
- Place it in `scripts/` (for `.py`) or `notebooks/` (for `.ipynb`).
- If it adds a new category of functionality worth indexing, update `docs/README.md`.
- The PR description should include what the helper does and an example invocation.

## When in doubt
- Run `ruff check` and `ruff format` and fix what they flag.
- Prefer simple code over clever code.
- If style or convention is ambiguous, ask before guessing.
````