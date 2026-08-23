# First contribution exercise

Time to try it out. The goal is to put the concepts from docs 00 through 08 into practice: branch, commit, push, pull request, review, merge.

## Get a repo to work in

This exercise is about applying the workflow to your own work, not practicing on this guide. Three
options, in order of preference:

**(1) You already have a repo** — your own project, or your team's. Add it to your workspace alongside this
guide: File > Add Folder to Workspace, then browse to it. That keeps these docs open for reference while
you make your first real change. [02_using_vs_code.md](02_using_vs_code.md) covers the mechanics.

**(2) You don't have a repo yet.** Start one:

1. Log into GitHub, find the `+` dropdown menu at the top of your page, click **New repository**, give it a name, and check "Add a README file." Create it. If this is lab work rather than personal practice, consider creating it under your lab's GitHub Organization instead of your own account, so it stays lab property — [repo_ownership_and_visibility.md](../reference/repo_ownership_and_visibility.md) covers why.
2. ([repo_lifecycle.md](../reference/repo_lifecycle.md) covers starting a repo, forking versus branching, and public versus private visibility.) Clone it the same way you cloned this guide: `git clone` the URL GitHub gives you, into your `~/repos/` folder or wherever you keep your projects. See [GETTING_STARTED.md](../../GETTING_STARTED.md) if you need the clone steps again.
3. Open it in VS Code: its own window, or added to this workspace alongside the guide (File > Add
   Folder to Workspace), whichever you'd rather work in.
4. Create your first file — a script in `scripts/` or a notebook in `notebooks/` — following the
   conventions in [06_adding_a_script.md](06_adding_a_script.md) and
   [07_notebooks.md](07_notebooks.md).

**(3) You'd rather not set anything up yet.** This guide's own docs and teaching fixtures (`scripts/`,
`notebooks/`, `sample_data/`) are fair game for a single practice rep: a doc typo, a small genuine
improvement to `scripts/show_h5_keys.py`. See [CONTRIBUTING.md](../../CONTRIBUTING.md) for what belongs
here. Treat this as a warm-up, not a substitute — the real payoff comes from running the loop on work
that's actually yours.

## The exercise

1. **Pick something small and real.** A script or notebook change you understand well enough that your
   attention stays on the workflow rather than the code: a small bug fix, a docstring, a new short
   script that does one useful thing.

2. **Make a branch.** Name it for what it does, e.g. `fix-h5-keys-docstring`. See
   [05_daily_workflow.md](05_daily_workflow.md) for how to create one.

3. **Do the work, following the conventions from docs 00–08.** For a `.py` file: a module docstring,
   type hints on every function, a docstring on every function, and an `if __name__ == "__main__":`
   block if it runs from the command line. For a `.ipynb`: a markdown cell at the top describing the
   purpose, inputs, and an example call, plus docstrings on any functions it defines. Naming
   conventions are in [06_adding_a_script.md](06_adding_a_script.md).

4. **Commit and push, then open a pull request.** Write a description that explains what changed and
   why, without making a reviewer read the diff first. The format is in
   [05_daily_workflow.md](05_daily_workflow.md).

5. **Get it reviewed.** If you're in a shared repo, ask a collaborator for one substantive comment: a
   question, a suggestion, or "looks good, and here's why" — see [08_code_review.md](08_code_review.md)
   for how to do this well from either side. If you're working solo for now, reread your own diff as if
   it were someone else's PR before merging; you'll usually catch something.

6. **Merge and delete the branch.** Once it's approved (or you've done step 5's solo version), merge in
   the GitHub interface.

Every later contribution — to this repo, your own, or your team's — is a repeat of these six steps.

## What good looks like

A clear pull request description tells the reviewer what changed and how to verify it, without making
them read the code first. Here is a small one for reference:

> **Title:** Add byte-size formatting to show_h5_keys output
>
> **Description:**
> `show_h5_keys.py` printed dataset shapes and dtypes but not size, which made it hard to spot the one
> huge dataset in a file with dozens of small ones. Adds a human-readable size (`KB`/`MB`/`GB`) next to
> each dataset.
>
> Example invocation: `python scripts/show_h5_keys.py sample_data/example.h5`
>
> Tested against `sample_data/example.h5` and a 2 GB file locally; output stays aligned at both sizes.
