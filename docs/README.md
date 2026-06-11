# DENNIS_helpers documentation

This folder onboards new lab members from near-zero software experience to confident contributor. Read the onboarding docs in order; they build on each other and define every term on first use. Doc 09 is a hands-on exercise to do once you have read them. The reference docs are for later: skim once so you know what's there, then come back as needed.

## Onboarding sequence

Read these in order. They live in [`onboarding/`](onboarding/).

- [00_python_code_basics.md](onboarding/00_python_code_basics.md) — How a Python file is put together: `.py` versus `.ipynb`, functions, docstrings, type hints, and `if __name__ == "__main__":`.
- [01_command_line_basics.md](onboarding/01_command_line_basics.md) — Navigating the terminal, running a script, the conda commands you need, and common error messages.
- [02_using_vs_code.md](onboarding/02_using_vs_code.md) — VS Code conventions: one folder per window, the Explorer and Source Control panels, the integrated terminal, interpreter and kernel selection, and key shortcuts.
- [03_getting_started_with_git.md](onboarding/03_getting_started_with_git.md) — What Git and GitHub are, why the repo stays out of synced folders, branches, and the pull-work-commit-push model.
- [04_environments.md](onboarding/04_environments.md) — Why environments exist, creating and activating the `helper` environment, and the Jupyter kernel trap.
- [05_daily_workflow.md](onboarding/05_daily_workflow.md) — The five-step daily loop in both VS Code and the terminal, commit messages, branches, pull requests, and merge conflicts.
- [06_adding_a_script.md](onboarding/06_adding_a_script.md) — Where files go, the naming conventions, the docstring requirement, and a walkthrough of the worked example.
- [07_notebooks.md](onboarding/07_notebooks.md) — Why notebooks need special handling, the one-time pre-commit setup, and the `.py` / `.ipynb` pairing convention.
- [08_code_review.md](onboarding/08_code_review.md) — What a reviewer checks, the tone norms, and how to approve and merge.

## Practice

- [09_first_contribution_exercise.md](onboarding/09_first_contribution_exercise.md) — A walkthrough exercise for your first contribution. Recommended after reading 00 through 08.

## Reference

Topical references you'll return to. They live in [`reference/`](reference/). No reading order; skim the list and come back as needed.

- [cs_jargon.md](reference/cs_jargon.md) — Programming terms of art (snake_case, mutable, parse, refactor, etc.) defined briefly.
- [git_recovery.md](reference/git_recovery.md) - what to do when your GitHub commit/push/pull routine is out of sync
- [git_vocabulary.md](reference/git_vocabulary.md) — Git and GitHub terms (fetch, pull, push, HEAD, origin, upstream, conflict, and others) you'll encounter.
- [keyboard_shortcuts.md](reference/keyboard_shortcuts.md) — VS Code shortcuts worth memorizing, organized by category.
- [markdown_formatting.md](reference/markdown_formatting.md) — Markdown syntax for docs, README files, PR descriptions, and notebook cells.
- [notebook_sync_alternatives.md](reference/notebook_sync_alternatives.md) — Notebook version control approaches the lab considered and why we picked nbstripout for now.
- [vs_code_extensions.md](reference/vs_code_extensions.md) — Recommended VS Code extensions for this repo, with notes on what each does.