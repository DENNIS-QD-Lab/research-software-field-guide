# First contribution exercise

This is practice, not a test. Nobody grades it and nothing breaks if you get a step wrong. The goal is
to put every concept from docs 00 through 08 through your hands once — branch, commit, push, pull
request, review, merge — before you need the workflow under pressure. Plan on 30 to 60 minutes.

Run this exercise wherever you're actually going to use it: your own project's repo, your lab's shared
repo if you have one, or — if neither exists yet — this guide's own teaching fixtures
(`scripts/`, `notebooks/`, `sample_data/`), which exist partly for this purpose. The mechanics are
identical either way; only the destination differs.

## The exercise

1. **Pick something small and real.** A script or notebook you understand well enough that your
   attention stays on the workflow rather than the code. If you're practicing on this guide, pick a
   small, genuine improvement to `scripts/show_h5_keys.py`, one of the `notebooks/`, or a doc typo you
   noticed — see [CONTRIBUTING.md](../../CONTRIBUTING.md) for what belongs here.

2. **Make a branch.** Name it for what it does, e.g. `fix-h5-keys-docstring`. See
   [05_daily_workflow.md](05_daily_workflow.md) for how to create one.

3. **Do the work, following this repo's conventions.** For a `.py` file: a module docstring, type
   hints on every function, a docstring on every function, and an `if __name__ == "__main__":` block if
   it runs from the command line. For a `.ipynb`: a markdown cell at the top describing the purpose,
   inputs, and an example call, plus docstrings on any functions it defines. Naming conventions are in
   [06_adding_a_script.md](06_adding_a_script.md).

4. **Commit and push, then open a pull request.** Write a description that explains what changed and
   why, without making a reviewer read the diff first. The format is in
   [05_daily_workflow.md](05_daily_workflow.md).

5. **Get it reviewed.** If you're in a shared repo, ask a collaborator for one substantive comment: a
   question, a suggestion, or "looks good, and here's why" — see [08_code_review.md](08_code_review.md)
   for how to do this well from either side. If you're working solo for now, reread your own diff as if
   it were someone else's PR before merging; you'll usually catch something.

6. **Merge and delete the branch.** Once it's approved (or you've done step 5's solo version), merge in
   the GitHub interface.

That is the whole loop. Every later contribution — to this repo, your own, or your team's — is a repeat
of these six steps.

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
