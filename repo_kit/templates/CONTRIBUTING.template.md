<!--
CONTRIBUTING.md TEMPLATE — copy this to the root of a target repo as CONTRIBUTING.md, then fill every
<PLACEHOLDER>. Only add this file once more than one person actually works in the repo; a solo project
doesn't need contribution norms written down for itself. Delete this comment block in the copy.
-->

# Contributing to <PROJECT>

This is the short version of how we work in this repo. The reasoning behind each step lives in the
research-software-field-guide's [onboarding](PATH-TO-GUIDE/docs/onboarding/) and
[implementing](PATH-TO-GUIDE/docs/implementing/) docs, linked below where relevant.

## Before you start

Work inside the shared environment (`conda activate <env-name>`; see
[04_environments.md](PATH-TO-GUIDE/docs/onboarding/04_environments.md) if you haven't made it yet).
Confirm the repo lives in a normal local folder, not inside OneDrive/iCloud/Dropbox — see
[03_getting_started_with_git.md](PATH-TO-GUIDE/docs/onboarding/03_getting_started_with_git.md).

## The workflow

Every change, even a one-line fix, follows the same loop: pull the latest code, make a branch, do the
work, commit, push, open a pull request. Full loop with VS Code and terminal equivalents:
[05_daily_workflow.md](PATH-TO-GUIDE/docs/onboarding/05_daily_workflow.md). We branch for every
change so `main` keeps working and everyone has a safe place to experiment.

Commit messages: one line, imperative present tense — "Add dark-frame correction," not "Added dark-frame
correction." A commit message finishes the sentence "If applied, this commit will..."

## What belongs here

<Describe the repo's actual scope: e.g. "Method code for the <domain> pipeline; anything specific to one
dataset or one paper belongs in that project's own experiments/ folder, not in src/." Adjust to fit —
this repo's own CLAUDE.md is the source of truth for structure.>

New method code goes in `src/<yourpkg>/`, following this repo's naming and docstring conventions
(`CLAUDE.md`). A new line of inquiry gets its own `experiments/<theme-slug>/` folder, built from
`experiments/_TEMPLATE.md` — see `.claude/experiments_playbook.md` for how runs are recorded. When in
doubt about where something goes, ask in review rather than guessing.

## Notebooks

Notebooks need one setup step after cloning, so Git doesn't record cell outputs and execution counts:
`pip install pre-commit && pre-commit install`, once. After that, outputs strip from the committed
version automatically while your local copy keeps them.
See [07_notebooks.md](PATH-TO-GUIDE/docs/onboarding/07_notebooks.md).

## Code review

Every pull request gets one reviewer. The reviewer checks that the code runs, has a docstring, follows
`CLAUDE.md`, and does not duplicate something already in `src/`. Reviews are collegial: ask questions
rather than issue commands, suggest rather than demand, assume the author did their best.
See [08_code_review.md](PATH-TO-GUIDE/docs/onboarding/08_code_review.md).
