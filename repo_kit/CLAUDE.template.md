<!--
CLAUDE.md TEMPLATE — copy this to the root of a target repo as CLAUDE.md, then fill every
<PLACEHOLDER>. This is the "standards" leg of the three-file split (state / procedure / standards);
keep it lean, because it is read at the start of every session. Delete this comment block in the copy.

Fill-in checklist: <PROJECT>, <one-line purpose>, the repository-structure block, the package name in
the paths, the domain terms allowed as abbreviations, and the "What NOT to do on main" list.
-->

# CLAUDE.md — <PROJECT>

This file is read automatically at the start of every Claude Code session in this repository. Follow
these instructions for all code you write or edit here.

## Project context

<One or two sentences: what this repository is and what it is for.> Contributors are scientists first
and software developers second; code here will be read and modified by people with varying experience,
so **prioritize readability over cleverness**.

## Repository structure

```
src/<yourpkg>/     the importable library — all method/analysis code (installed with `pip install -e .`)
experiments/       hypothesis-driven studies; experiments/README.md is the research log,
                     _common/ the shared harness, <slug>/ one undated, permanent folder per theme
                     (revisited over the project's life) holding:
                       - <YYMMDD_slug>[_NN].md (or .ipynb)   dated run reports, readable at a glance
                       - details/<YYMMDD_slug>[_NN]/         manifest/metrics/figures behind each report
tests/             pytest suite (unit + regression) with committed fixtures
docs/              Sphinx doc site: API reference generated from docstrings, plus rendered
                     experiment reports — experiment_overviews/<theme>_overview.md (one per theme,
                     includes its README) and experiment_summaries/*.md (the reports themselves)
references.md      the reference ledger: external sources + why each mattered here
config / local_paths.py   parameters and machine-local data paths (paths stay out of git)
```

Exploratory notebooks live inside the relevant `experiments/<slug>/` folder alongside its driver(s) — see
[16_running_a_dry_lab_experiment.md](../docs/implementing/16_running_a_dry_lab_experiment.md#exploratory-notebooks-the-same-discipline-without-a-manifest).

## The three homes for instructions

This repo keeps three kinds of written guidance separate so no file sprawls:

- **State** — the research log at `experiments/README.md` (goal, open questions, findings, decisions).
  Read it first every session; people own it.
- **Durable procedure** — `.claude/experiments_playbook.md`: how this repo runs and records
  experiments. Read it before adding or changing an experiment.
- **Standards** — this file: coding conventions, applied to human- and AI-written code alike.

## Code style

- Follow PEP 8, enforced by `ruff format` and `ruff check`. Do not hand-format; let the tools decide.
- Use snake_case for files, functions, and variables. Use PascalCase only for class names.
- Keep functions short. If a function is doing more than one thing, split it.
- Prefer explicit over implicit. Name variables for what they hold, not how short you can make the name.

## Documentation requirements

- Every function gets a docstring: one-line summary, parameters (with types and meaning), return value,
  and one example call. Use **NumPy-style** docstrings (so the Sphinx site can render them).
- Every module (`.py` file) gets a module-level docstring describing what the file is for.
- Notebooks start with a markdown cell carrying the same information as a module docstring.
- Comments explain *why*, not *what*. The code shows what it does.

## Type hints

- Every function signature gets type hints on parameters and return value.
- Use modern syntax: `list[int]` not `List[int]`, `dict[str, float]` not `Dict[str, float]`,
  `X | None` not `Optional[X]`.
- Hints are for readers and static checkers; Python does not enforce them at runtime. Do not add runtime
  type assertions unless there is a specific reason.

## Naming conventions for files

- snake_case, lowercase, no hyphens, under about 30 characters.
- Verb-first for action scripts that *do* something: `show_keys.py`, `plot_spectra.py`.
- Noun phrases for modules that *contain* importable functionality: `ratio_analysis.py`.
- Avoid abbreviations except universally understood domain terms (<list the ones your field accepts>).
- **Theme folders may use hyphens; run files may not.** `experiments/<theme-slug>/` (hyphens allowed —
  a multi-word theme name reads better as `crf-solve-and-necessity` than as one run-together word) is a
  standing address for one line of inquiry, revisited for as long as that inquiry stays open (a theme is
  not "done" the day it starts) — it carries no date. Inside it, each run's report carries the date and
  follows the normal no-hyphens rule: `YYMMDD_<slug>[_NN].md` (or `.ipynb`), `_02`/`_03` for reruns,
  sitting directly in the theme folder so it's visible without opening a subfolder. The provenance that
  produced it (`manifest.yaml`, `metrics.csv`, figures) lives one level down in
  `details/<YYMMDD>_<slug>[_NN]/`, name-matched to its report — present for reproducibility, not meant to
  be opened on a normal read-through. A promoted doc-site stub for that run follows the theme's own
  convention: `<theme-slug>-<YYMMDD_slug>[_NN].md`.

## Command line interfaces

- Any script runnable from the command line uses `if __name__ == "__main__":` to wire up its CLI.
- Use `argparse` for arguments, not hand-parsing `sys.argv`.
- Scripts take file paths as arguments. Do not hardcode paths — read them from `config`/`local_paths.py`.

## Data handling

- Never commit data files. Data lives outside the repo; scripts take paths as arguments.
- One exception: small *teaching and test fixtures* (a few KB to a few MB) a reader or test actually
  needs — synthetic under `sample_data/`, test fixtures alongside the tests. The full acquired dataset
  stays out; it bloats history permanently.
- Keep machine-specific paths out of committed code and notebooks: put them in a git-ignored
  `local_paths.py` (copy `local_paths_example.py`) and import from it.

## Dependencies

- Ask before adding a new dependency. If approved, update the environment file and say why in the PR.
- Prefer packages already in the environment; prefer conda-forge over pip when both are available.

## Notebooks

- Outputs are stripped on commit by nbstripout. Assume reviewers re-run the notebook.
- A notebook must run top to bottom without errors; a cell that depends on another appears after it.

## Commit discipline

- **The scientist commits.** Prepare the changes and a commit-message draft, but ask before committing,
  pushing, or opening a PR.
- Commit messages: one line, imperative present tense ("Add dark-frame correction," not "Added …").

## What NOT to do on main

<For a repo with a published/frozen baseline, list what must not change on `main` — e.g. algorithm
parameters, the published method, calibration constants. Delete this section if the repo has no frozen
baseline to protect.>

## Session hygiene — context and continuity

- At natural break points — an experiment concluded, a commit landed, a task finished — proactively
  remind the scientist to `/compact` or `/clear`, whichever fits: `/compact` to keep going once the
  transcript has grown large, `/clear` when moving on to unrelated work. This is responsible token
  usage; make it a regular, gentle prompt, not a one-time note.
- **Before recommending it, make sure a sudden clear would lose nothing.** Update the research log
  (`experiments/README.md`), the reference ledger (`references.md`), and any auto-memory, and commit or
  explicitly flag work in progress, *first* — then suggest compacting or clearing. Anything that must
  survive the session belongs in a file in the repo, never only in the conversation.

## When in doubt

- Run `ruff check` and `ruff format` and fix what they flag.
- Prefer simple code over clever code.
- If style or convention is ambiguous, ask before guessing.
