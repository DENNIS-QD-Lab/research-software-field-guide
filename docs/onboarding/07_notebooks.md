# Notebooks

Notebooks are critical for developing scientific analysis approaches. They are great for data exploration and analysis testing, but awkward for version control. This doc explains a problem they cause with Git and a one-time setup that fixes it, then describes an approach to pairing notebooks with scripts.

## The problem notebooks cause

A `.ipynb` file stores not just your code but also every cell's output: printed text, tables, images, and an execution count for each cell. Those outputs change every time you run the notebook, even when the code is identical. Git records every change, so committed notebooks produce enormous, noisy differences that are about outputs rather than code, and two people running the same notebook generate conflicting versions of the same file. This makes notebook history nearly unreadable and merges painful.

## One-time setup after cloning

The fix is a tool called `pre-commit`, which runs a check automatically every time you commit. Our check strips the outputs out of notebooks before they are committed. Run these two commands once, from the repository root, with the `fieldguide` environment active:

```
pip install pre-commit
```

This installs the `pre-commit` tool.

```
pre-commit install
```

This activates the check in this repository, using the configuration in `.pre-commit-config.yaml`. You do this once per repository.

## What you will see when committing

When you commit a notebook, the hook strips its outputs from the version that gets committed. Your local working file on disk keeps its outputs, so your screen does not change. If the hook modifies a file as part of a commit, the commit stops and asks you to stage the now-stripped file and commit again. That is expected; stage the change and recommit. The result is that the repository stores clean, output-free notebooks while you keep your rendered results locally.

## When to pair a `.py` and a `.ipynb`

Some work exists as a single file. Some exists as both a `.py` and a `.ipynb`. Which to use is a judgment call, not a rule.

**Use just a notebook (`.ipynb`)** when the work is genuinely exploratory: loading a file to see what's in it, trying a plot to see if the data looks right, sketching an analysis you may or may not keep. The notebook *is* the deliverable; there's nothing to import.

**Use just a script (`.py`)** when it does one well-defined thing that you'd call from the command line or from other code: `show_h5_keys.py` is a good example. No interactive exploration is needed; you just want to run it.

**Use both** when the underlying logic is stable and reusable, and also benefits from interactive use. The pattern: the script holds the canonical function. The notebook imports that function and uses it, plus does whatever ad-hoc poking only makes sense by hand. Because the notebook imports from the script rather than duplicating the code, the two stay in sync: edit the script, restart the kernel, and the notebook picks up the change.

`scripts/show_h5_keys.py` and `notebooks/show_h5_keys.ipynb` are the model for the third pattern. The script defines `show_keys`. The notebook imports it and uses it interactively, then opens one dataset by hand to check its range — the kind of thing you wouldn't bake into a reusable function.

**Promoting notebook code to a script.** When you notice yourself reusing a chunk of notebook code, or wanting to call it from another notebook, move it into a script and import it back. This is the natural evolution: explore in a notebook, extract the stable parts into a script, keep using the notebook as the interactive surface.

**A note on drift.** Because the script and notebook are two separate files in this repo, they *can* get out of sync if you duplicate logic across both rather than importing. The discipline is to keep the script as the single source of truth for any function that appears in both. Tools exist that synchronize the two automatically (see [notebook_sync_alternatives.md](../reference/notebook_sync_alternatives.md)); we've chosen not to use them for now in favor of a simpler stack.


## Running a paired notebook

The notebook imports its function with `from scripts.show_h5_keys import show_keys`. For that import to work, Python must be able to find the `scripts/` folder, which means the notebook has to run from the **repository root**, not from inside `notebooks/`. This repo ships a committed `.vscode/settings.json` that sets `jupyter.notebookFileRoot` to the workspace root, so VS Code runs notebooks from the repo root for you. If you just added or pulled that setting, reload the window (Command Palette > "Developer: Reload Window") so it takes effect.

If you see this error:

```
ModuleNotFoundError: No module named 'scripts'
```

it means the notebook is running from the wrong directory. In VS Code, the committed setting fixes it. If you run notebooks another way (plain `jupyter lab`, say), start it from the repository root so `scripts/` is importable.

## Pointing at your own data without committing paths

The example notebook defaults to the committed `sample_data/example.h5`, so it runs immediately. To inspect your own file, do not type your path into a code cell: a path in a cell gets committed (nbstripout strips *outputs*, not code), which leaks machine-specific paths into the repo and churns the file every run. Instead follow the template in `local_paths_example.py` (in the repo root) to make your own file `local_paths.py` (which is gitignored), define `DATA_ROOT` there as the folder your data lives in, and read it in the notebook:

```python
from local_paths import DATA_ROOT

h5_file = f"{DATA_ROOT}/your_file.h5"
```

`DATA_ROOT` is the folder, not the full path to one file, on purpose: the machine-specific *location* is set once in the gitignored `local_paths.py`, while each notebook names the file it reads (`your_file.h5`) in the cell. So your machine-specific paths stay out of Git, *which* file an analysis uses stays visible in the committed notebook, and the same notebook runs for everyone.
