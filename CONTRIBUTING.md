# Contributing to research-software-field-guide

This repo is a teaching tool and portable standard, not a shared codebase — most readers clone it,
read it, and take what's useful into their own project. "Contributing" here means improving the guide
itself: the docs, the `repo_kit/` templates, or the small worked examples in `scripts/`, `notebooks/`,
and `sample_data/` (which exist to be read and run, not to accumulate real analysis code — see
`CLAUDE.md`'s note on teaching fixtures).

If you're using this standard for your own project or lab's repo and want real contribution norms for
*that* repo (people actually committing analysis code, reviewing each other's PRs), start from
[repo_kit/templates/CONTRIBUTING.template.md](repo_kit/templates/CONTRIBUTING.template.md) instead —
this file is about the guide, not a template for yours.

## What belongs here

- Fixes to the docs: a typo, an unclear explanation, a broken link, an outdated example.
- New or improved `repo_kit/` recipes — a scaffold step or upgrade recipe the playbook is missing.
- Small improvements to the worked examples (`scripts/show_h5_keys.py`, `notebooks/`, `sample_data/`) —
  keep them small and generic; they demonstrate conventions, not a real analysis.
- A new doc, if it fills a real gap — open an issue to discuss scope first, since the numbered tracks
  are meant to stay a coherent sequence rather than grow unbounded.

What doesn't belong: your own project's analysis scripts, notebooks, or pipeline code. That code
belongs in your own repo, built to this standard — that's the guide working as intended, not a reason
to add it here.

## The workflow

Every change, even a one-line fix, follows the same loop: pull the latest code, make a branch, do the
work, commit, push, and open a pull request. The full loop with both the VS Code Source Control panel
and the equivalent terminal commands is in [05_daily_workflow.md](docs/onboarding/05_daily_workflow.md).

Write commit messages as one line, in the imperative present tense. Write "Fix broken link in doc 16,"
not "Fixed a broken link." A commit message finishes the sentence "If applied, this commit will..."

## Notebooks

Notebooks need one extra setup step after you clone, so that Git does not record their cell outputs and
execution counts. Run `pip install pre-commit` and then `pre-commit install` once. After that, the
outputs are stripped from the committed version automatically while your local copy keeps them. The
reasoning is in [07_notebooks.md](docs/onboarding/07_notebooks.md).

## Code review

Every pull request gets one reviewer. The reviewer checks that any claim reads true, any command
actually works as written, and any doc change doesn't contradict another doc or `repo_kit/` file it
should match. Reviews are collegial: ask questions rather than issue commands, suggest rather than
demand, and assume the author did their best. How to review, approve, and merge in the GitHub interface
is in [08_code_review.md](docs/onboarding/08_code_review.md).
