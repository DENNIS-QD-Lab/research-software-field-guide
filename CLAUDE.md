# CLAUDE.md — coding standards for this repository

This file is read automatically at the start of every Claude session in this repository. Follow these instructions for all code you write or edit here.

## Project context
This repository is a teaching tool and portable standard for research software practices, aimed at scientists writing analytical code — often with an AI coding assistant doing much of the typing — who didn't train as software developers. Contributors and readers range from complete beginners to experienced researchers, so prioritize readability and explicitness over cleverness. The worked examples in `scripts/` and `sample_data/` are teaching fixtures, not project-specific analysis.

## Code style
- Follow PEP 8, enforced by `ruff format` and `ruff check`. Do not hand-format. If you're unsure how something should be formatted, run ruff or write it however and let the pre-commit hook fix it.
- Use snake_case for files, functions, and variables. Use PascalCase only for class names.
- Keep functions short. If a function is doing more than one thing, split it.
- Prefer explicit over implicit. Name variables for what they hold, not how short you can make the name.

## Documentation requirements
- Every function gets a docstring with: one-line summary, parameters (with types and meaning), return value, and one example call. Use **NumPy-style** docstrings (`Parameters`, `Returns`, `Examples`), the style [20_documentation_and_doc_sites.md](docs/implementing/20_documentation_and_doc_sites.md) teaches and Sphinx's napoleon extension reads.
- Every module (`.py` file) gets a module-level docstring at the top describing what the file is for.
- Notebooks get a markdown cell at the top with the same information as a module docstring.
- Comments explain *why*, not *what*. The code itself shows what it does.

## Prose in the guide's own docs (`docs/`, `repo_kit/`)
These docs are the product: a scientist teaching her team. They should read as explanation, not as a
manifesto. Every rule below is here because generated drafts violated it repeatedly.
- **Explain the mechanism; don't compress it into a maxim.** No aphoristic one-liners ("a result you
  cannot reproduce is an anecdote, not a measurement"), and no "X, not Y" antithesis as a section opener
  or closer. Say what happens and why, in plain sentences, even when that takes more words. Prefer
  naming the thing ("this tagged, DOI'ed version of the repo") over a pronoun ("that is how").
- **Don't let a document talk about itself.** Cut commentary on its own rhetoric or its place in the
  guide: "that is the whole point," "worth naming," "the single place this is defined in this track."
- **Don't argue with an imagined critic.** No pre-emptive defenses like "that's a real cost, not a free
  safety net."
- **One idea per paragraph.** If a paragraph runs past ~6 lines, or stacks more than two em-dash asides,
  split it — or make it a list, a table, or a file-tree diagram.
- **The scientist is the actor.** Write for a scientist deciding what to do, not for an assistant
  implementing it. Keep implementation notes ("verified with a throwaway spike") out of reader-facing
  prose.

## Type hints
- Every function signature gets type hints on parameters and return value.
- Use the modern syntax: `list[int]` not `List[int]`, `dict[str, float]` not `Dict[str, float]`, `X | None` not `Optional[X]`.
- Python does not enforce type hints at runtime; they're for human readers and static checkers. Don't add runtime type assertions unless there's a specific reason.

## Testing requirements
- A new function that does real computation (not just wiring, CLI glue, or I/O) gets a test in `tests/`, following [12_testing_with_pytest.md](docs/implementing/12_testing_with_pytest.md): `np.testing.assert_allclose` for floats, `pytest.mark.parametrize` for multiple cases.
- When fixing a bug, add a regression test that would have caught it.
- Tests are part of the function, not optional follow-up work to add later.
- Checking coverage (`pytest --cov`, via `pytest-cov`) is optional and occasional — good for spotting code with zero tests, not a number to chase. Don't add filler tests just to raise it. See [12_testing_with_pytest.md](docs/implementing/12_testing_with_pytest.md#code-coverage-is-informative-but-not-the-real-goal).

## Naming conventions for files
- snake_case, lowercase, no hyphens, under about 30 characters.
- Verb-first for action scripts that *do* something when run: `show_keys.py`, `plot_spectra.py`, `convert_units.py`.
- Noun phrases for modules that *contain* importable functionality: `ratio_analysis.py`, `preprocessing.py`, `peak_detection.py`.
- Avoid abbreviations except universally understood domain terms in your own field (`hdf5` is fine anywhere; `seg` for `segmentation` is not). This guide's own examples stay generic, since its readers span fields.
- **Experiment (and figure) theme folders are undated and permanent**, an exception to the "no hyphens" rule above: `experiments/<theme-slug>/` (e.g. `dark-current-subtraction/`, hyphens allowed) is a standing address for one line of inquiry, revisited for as long as it stays open — it carries no date. A leading number (`01_dark-current-subtraction/`, `02_dynamic-range-scenarios/`) is an optional, encouraged way to order themes by when they were conceived, useful once a project has enough of them that folder order stops being obvious; it is not required.
- **Per-run directories, inside a theme's `details/`, are dated** — the exception that actually needs it, since these accumulate over the theme's whole life: `<YYMMDD>_<slug>[_NN]/` (the run date, with `_02`, `_03`, … preserving reruns). This applies to dated directories, not to importable `.py` module names.

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
- Pin any tool whose version can change results or break checks — a linter, a formatter, a doc builder — exactly, and in every place it is declared at once (`environment.yml` *and* `.pre-commit-config.yaml`'s `rev:`). Bump those pins together, deliberately, in their own commit. See [11_code_quality_tools.md](docs/implementing/11_code_quality_tools.md).

## Notebooks
- Outputs are stripped on commit by nbstripout. Don't fight this; assume reviewers run the notebook themselves.
- A notebook should run top to bottom without errors. If a cell depends on a previous cell, it must appear after that cell.
- Each notebook starts with a markdown cell describing purpose, inputs, and an example invocation.

## When adding a new script or notebook
- Place it in `scripts/` (for `.py`) or `notebooks/` (for `.ipynb`).
- If it adds a new category of functionality worth indexing, update `docs/table_of_contents.md`.
- The PR description should include what it does and an example invocation.

## Commit and PR messages
Keep them short. A reviewer reads these to find out what changed and why; anything else is noise they
have to skim past.
- One imperative-present-tense subject line, under about 60 characters: "Add dark-frame correction," not
  "Added dark-frame correction."
- In the body, say what changed and why — briefly, and only where the *why* isn't already obvious from
  the subject. A few lines or a few tight bullets. Not a paragraph per file, and not a section per
  change.
- **Don't list what the change doesn't do.** No "out of scope," "not included," or "deferred to a
  follow-up" sections. If a follow-up matters, it belongs in an issue or the plan, not in this message.
- **Don't report that the checks passed.** `ruff`, `pytest`, and the pre-commit hooks have to pass on
  every commit, so saying they did adds nothing. Report a check only when its *result* is the news —
  a benchmark number, a newly-covered edge case, a deliberate exception.
- Scale the message to the change. A one-line fix gets one line. Spend words on what would surprise a
  reviewer, not on what they can see in the diff.

## Session hygiene — context and continuity
- **Prompt for a commit at natural break points as a matter of course**, not only when a `/compact` or `/clear` is imminent — a finished task, a fixed bug, a doc section done are each a candidate. This matters most right before starting to implement an approved plan: check whether the working tree already holds unrelated, uncommitted work, and if so, suggest committing or explicitly flagging it first, so the plan's changes land as their own clean, reviewable diff instead of mixed in with what came before.
- At natural break points — a task finished, a PR merged, a doc section done — proactively remind the scientist to `/compact` or `/clear`, whichever fits: `/compact` to keep going once a session's transcript has grown large, `/clear` when moving on to unrelated work. This is responsible token usage ([docs/reference/ai_coding_assistants.md](docs/reference/ai_coding_assistants.md)); make it a regular, gentle prompt, not a one-time note.
- **Before recommending it, make sure a sudden clear would lose nothing.** Update the docs and any auto-memory, and commit or explicitly flag work in progress, *first* — then suggest compacting or clearing. Anything that must survive the session belongs in a file in the repo or in memory, never only in the conversation.

## When in doubt
- Run `ruff check` and `ruff format` and fix what they flag.
- Prefer simple code over clever code.
- If style or convention is ambiguous, ask before guessing.
