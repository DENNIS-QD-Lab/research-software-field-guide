<!--
CLAUDE.md TEMPLATE — copy this to the root of a target repo as CLAUDE.md, then fill every
<PLACEHOLDER>. This is the "standards" leg of the three-file split (state / procedure / standards);
keep it lean, because it is read at the start of every session. Delete this comment block in the copy.

Fill-in checklist: <PROJECT>, <one-line purpose>, the repository-structure block, the package name in
the paths, the domain terms allowed as abbreviations, and the "What NOT to do on main" list. Also
replace every PATH-TO-GUIDE with the path to your checkout of the research-software-field-guide, or
delete those links if the guide is not checked out alongside this repo.
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
                     _common/ the shared harness, <theme-slug>/ one undated, permanent folder per
                     theme (revisited over the project's life) holding:
                       - README.md                      the theme's only narrative document: question,
                                                        findings, embedded figures, interpretation —
                                                        updated in place, never regenerated per run
                       - details/<YYMMDD>_<slug>[_NN]/   manifest.yaml, metrics.csv, and any figure
                                                        the README embeds — provenance, not a report
tests/             pytest suite (unit + regression) with committed fixtures
docs/              Sphinx doc site: API reference generated from docstrings, plus one page per theme —
                     experiment_overviews/<theme-slug>_overview.md, whose entire body is a MyST
                     {include} of that theme's README, so the site holds no second copy
figures/           (once drafting a manuscript) the paper's figure outline — same theme +
                     dated-details/ discipline as experiments/, one folder per figure; see
                     22_publishing_a_paper.md
references.md      the reference ledger: external sources + why each mattered here
local_paths.py     machine-local data paths (gitignored; copy local_paths_example.py)
```

Exploratory notebooks live inside the relevant `experiments/<theme-slug>/` folder alongside its driver(s) — see
[16_running_a_dry_lab_experiment.md](PATH-TO-GUIDE/docs/implementing/16_running_a_dry_lab_experiment.md#exploratory-notebooks-the-same-discipline-without-a-manifest).

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

## Interpretation belongs to the scientist

- **What a result *means* is written by the scientist, verbatim.** It goes in a signed blockquote
  (`> **<initials>:** …`) in the theme README, the research log's decision entries, or a figure README.
  Insert what the scientist actually said, unedited — do not paraphrase, tighten, or rewrite it. A
  paraphrase quietly substitutes the assistant's voice for theirs.
- **If there is no answer yet, say so.** Write `> **<initials>:** _pending._` rather than drafting a
  plausible-sounding interpretation on the scientist's behalf.
- Write for a scientist deciding what to do, not for an assistant implementing it. Describe what ran
  and what it measured; leave what it means to the blockquote.

## Type hints

- Every function signature gets type hints on parameters and return value.
- Use modern syntax: `list[int]` not `List[int]`, `dict[str, float]` not `Dict[str, float]`,
  `X | None` not `Optional[X]`.
- Hints are for readers and static checkers; Python does not enforce them at runtime. Do not add runtime
  type assertions unless there is a specific reason.

## Testing requirements

- A new function that does real computation (not just wiring, CLI glue, or I/O) gets a test in
  `tests/`, following
  [12_testing_with_pytest.md](PATH-TO-GUIDE/docs/implementing/12_testing_with_pytest.md):
  `np.testing.assert_allclose` for floats, `pytest.mark.parametrize` for multiple cases.
- When fixing a bug, add a regression test that would have caught it.
- Tests are part of the function, not optional follow-up work to add later.
- Checking coverage (`pytest --cov`, via `pytest-cov`) is optional and occasional — good for spotting
  code with zero tests, not a number to chase. Don't add filler tests just to raise it. See
  [12_testing_with_pytest.md](PATH-TO-GUIDE/docs/implementing/12_testing_with_pytest.md#code-coverage-is-informative-but-not-the-real-goal).

## Naming conventions for files

- snake_case, lowercase, no hyphens, under about 30 characters.
- Verb-first for action scripts that *do* something: `show_keys.py`, `plot_spectra.py`.
- Noun phrases for modules that *contain* importable functionality: `ratio_analysis.py`.
- Avoid abbreviations except universally understood domain terms (<list the ones your field accepts>).
- **Theme folders may use hyphens**, as an exception to the rule above: `experiments/<theme-slug>/`
  (a multi-word theme reads better as `dark-current-subtraction` than as one run-together word) is a
  standing address for one line of inquiry, revisited for as long as that inquiry stays open. It
  carries no date. A leading number (`01_dark-current-subtraction/`) is an optional, encouraged way to
  order themes by conception once a project has enough of them that folder order stops being obvious;
  it is not required.
- **A theme's `README.md` is its only narrative document** — question, findings, embedded figures,
  interpretation — updated in place, never regenerated per run.
- **Per-run directories are dated**, one level down in `details/<YYMMDD>_<slug>[_NN]/`, holding
  `manifest.yaml`, `metrics.csv`, and any figure the README embeds. A run directory inherits the
  theme's slug, so it may contain hyphens too; what matters is that it carries the run date and that
  `_02`, `_03`, … preserve reruns rather than overwriting them. This is provenance for reproducibility,
  not a report to read. The dating rule applies to directories, not to importable `.py` module names.

## Command line interfaces

- Any script runnable from the command line uses `if __name__ == "__main__":` to wire up its CLI.
- Use `argparse` for arguments, not hand-parsing `sys.argv`.
- Scripts take file paths as arguments. Do not hardcode paths — read the machine-local root from
  `local_paths.py`.

## Data handling

- Never commit data files. Data lives outside the repo; scripts take paths as arguments.
- One exception: small *teaching and test fixtures* (a few KB to a few MB) a reader or test actually
  needs — synthetic ones under `sample_data/`, test fixtures alongside the tests. A fixture may be
  synthetic *or* a small, curated handful of real samples; the guiding line is size and purpose, not
  synthetic-versus-real. The full acquired dataset stays out, because it bloats history permanently.
- If you generate intermediate files while testing, put them in a directory listed in `.gitignore` and
  clean them up.
- Keep machine-specific paths out of committed code and notebooks: put them in a git-ignored
  `local_paths.py` (copy `local_paths_example.py`) and import from it.

## Dependencies

- Ask before adding a new dependency. If approved, update the environment file and say why in the PR.
- Prefer packages already in the environment; prefer conda-forge over pip when both are available.
- Pin any tool whose version can change your results or break your checks — a linter, a formatter, a
  doc builder — exactly, and in every place it is declared at once (the environment file *and*
  `.pre-commit-config.yaml`'s `rev:`). Bump those pins together, deliberately, in their own commit.

## Notebooks

- Outputs are stripped on commit by nbstripout. Assume reviewers re-run the notebook.
- A notebook must run top to bottom without errors; a cell that depends on another appears after it.

## Commit discipline

- **The scientist commits.** Prepare the changes and a commit-message draft, but ask before committing,
  pushing, or opening a PR.
- Commit messages: one line, imperative present tense ("Add dark-frame correction," not "Added …"),
  under about 60 characters. Add a body only where the *why* isn't obvious from the subject, and keep it
  to a few lines. Scale the message to the change: a one-line fix gets one line.
- **Don't pad a message.** No "out of scope" or "deferred" sections, and no reporting that the linter
  and tests passed — those have to pass on every commit. Mention a check only when its *result* is the
  news. Spend the words on what would surprise a reviewer, not on what the diff already shows.
- **Prompt for a commit at natural break points as a matter of course**, not only before `/compact` or
  `/clear`: a finished task, a fixed bug, a doc section done. This matters most right before
  implementing an approved plan — check whether the working tree already holds unrelated, uncommitted
  work, and if so, prepare that commit (or ask the scientist to make it) before the plan's first edit,
  so the plan lands as its own clean, reviewable diff.

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
