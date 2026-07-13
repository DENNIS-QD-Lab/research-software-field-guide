# Notebooks

Notebooks are great for exploration and awkward for version control. This doc explains the one problem they cause with Git and the one-time setup that fixes it, then describes an approach to pairing notebooks with scripts.

## The problem notebooks cause

A `.ipynb` file stores not just your code but also every cell's output: printed text, tables, images, and an execution count for each cell. Those outputs change every time you run the notebook, even when the code is identical. Git records every change, so committed notebooks produce enormous, noisy differences that are about outputs rather than code, and two people running the same notebook generate conflicting versions of the same file. This makes notebook history nearly unreadable and merges painful.

## One-time setup after cloning

The fix is a tool called `pre-commit`, which runs a check automatically every time you commit. Our check strips the outputs out of notebooks before they are committed. Run these two commands once, from the repository root, with the `helper` environment active:

```
pip install pre-commit
```

This installs the `pre-commit` tool.

```
pre-commit install
```

This activates the check in this repository, using the configuration in `.pre-commit-config.yaml`. You do this once per cloned copy.

## What you will see when committing

When you commit a notebook, the hook strips its outputs from the version that gets committed. Your local working file on disk keeps its outputs, so your screen does not change. If the hook modifies a file as part of a commit, the commit stops and asks you to stage the now-stripped file and commit again. That is expected; stage the change and recommit. The result is that the repository stores clean, output-free notebooks while you keep your rendered results locally.

## When to pair a `.py` and a `.ipynb`

Some helpers exist as a single file. Some exist as both a `.py` and a `.ipynb`. Which to use is a judgment call, not a rule.

**Use just a notebook (`.ipynb`)** when the work is genuinely exploratory: loading a file to see what's in it, trying a plot to see if the data looks right, sketching an analysis you may or may not keep. The notebook *is* the deliverable; there's nothing to import.

**Use just a script (`.py`)** when the helper does one well-defined thing that you'd call from the command line or from other code: `show_h5_keys.py` is a good example. No interactive exploration is needed; you just want to run it.

**Use both** when a helper has stable, reusable logic *and* a benefit from interactive use. The pattern: the script holds the canonical function. The notebook imports that function and uses it, plus does whatever ad-hoc poking only makes sense by hand. Because the notebook imports from the script rather than duplicating the code, the two stay in sync: edit the script, restart the kernel, and the notebook picks up the change.

`scripts/show_h5_keys.py` and `notebooks/show_h5_keys.ipynb` are the model for the third pattern. The script defines `show_keys`. The notebook imports it and uses it interactively, then opens one dataset by hand to check its range — the kind of thing you wouldn't bake into a reusable function.

**Promoting notebook code to a script.** When you notice yourself reusing a chunk of notebook code, or wanting to call it from another notebook, move it into a script and import it back. This is the natural evolution: explore in a notebook, extract the stable parts into a script, keep using the notebook as the interactive surface.

**A note on drift.** Because the script and notebook are two separate files in this repo, they *can* get out of sync if you duplicate logic across both rather than importing. The discipline is to keep the script as the single source of truth for any function that appears in both. Tools exist that synchronize the two automatically (see `reference/notebook_sync_alternatives.md`); we've chosen not to use them for now in favor of a simpler stack.