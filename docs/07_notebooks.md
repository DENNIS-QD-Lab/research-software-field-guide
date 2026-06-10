# Notebooks

Notebooks are great for exploration and awkward for version control. This doc explains the one problem they cause with Git and the one-time setup that fixes it, then describes how the lab pairs notebooks with scripts.

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

## The `.py` / `.ipynb` pairing

The lab keeps many tools in two forms. The notebook is for interactive exploration: you load a file, look at it, plot it, try things cell by cell. The script is the importable, reusable version of the settled logic. The two share the same core function so they never drift apart.

`scripts/show_h5_keys.py` and `notebooks/show_h5_keys.ipynb` are the model. The script defines `show_keys`. The notebook imports that same function and uses it interactively, then does a bit of poking that only makes sense by hand, like opening one dataset and checking its range. When you find yourself reusing notebook logic, move it into a script and import it back into the notebook, rather than copying the code.
