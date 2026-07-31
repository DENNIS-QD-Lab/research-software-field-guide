# First contribution exercise

This is practice, not a test. Nobody grades it and nothing breaks if you get a step wrong. The goal is to put every concept from docs 00 through 08 through your hands once, using code you already understand, before you need the workflow under pressure. Plan on 30 to 60 minutes once you have read those docs.

Pick something small and real. The best candidate is a script or notebook you have already written that a collaborator might find useful. You understand it already, so your attention stays on the workflow rather than the code.

## The exercise

1. **Pick a helper.** Choose a script or notebook you have written that others might reuse. Small is good.

2. **Make a branch.** Name it `add-<your-script-name>`, for example `add-plot_spectra`. See [05_daily_workflow.md](05_daily_workflow.md) for how to create one.

3. **Add the file in the right place.** Put a `.py` in `scripts/` and a `.ipynb` in `notebooks/`, following the naming conventions in [06_adding_a_script.md](06_adding_a_script.md). Whether to also create a paired version in the other format is a judgment call per helper. If you make a pairing, say so in the pull request and explain why. See [07_notebooks.md](07_notebooks.md) for the pairing convention.

4. **Bring it up to standard with Claude.** Claude follows [CLAUDE.md](../../CLAUDE.md) automatically in this repository. For a `.py` file, work with it to add the module docstring, type hints on every function, docstrings on every function, and the `if __name__ == "__main__":` block if the file runs from the command line. For a `.ipynb`, add a markdown cell at the top describing the purpose, inputs, and an example call, plus docstrings on any functions the notebook defines.

5. **Update the docs index if needed.** If your helper adds a new category worth indexing, add a line for it in [README.md](../README.md).

6. **Commit, push, and open a pull request.** Write a description that explains what the helper does and includes an example invocation. The format is in [05_daily_workflow.md](05_daily_workflow.md).

7. **Review a collaborator before merging your own.** Find one open pull request from someone else and leave one substantive comment: a question, a suggestion, or "looks good, and here is why." This is the other half of the workflow, and [08_code_review.md](08_code_review.md) covers how to do it well.

8. **Merge your own.** Once your pull request has at least one approval, merge it yourself in the GitHub interface and delete the branch.

That is the whole loop. You have now branched, committed, pushed, opened a pull request, reviewed someone else's work, and merged. Every later contribution is a repeat of these eight steps.

## What good looks like

A clear pull request description tells the reviewer what the helper does and how to run it, without making them read the code first. Here is a small one for reference:

> **Title:** Add show_h5_keys helper
>
> **Description:**
> Adds a helper script that recursively prints the structure of an HDF5 file (groups, datasets, shapes, dtypes). Useful for inspecting unfamiliar `.h5` files before writing analysis code.
>
> Example invocation: `python scripts/show_h5_keys.py path/to/data.h5`
>
> Tested on a 2 GB SWIR imaging dataset; output truncates cleanly at large file levels.
