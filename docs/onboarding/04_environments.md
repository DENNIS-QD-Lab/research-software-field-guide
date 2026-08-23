# Environments

## Why environments exist

Different projects need different software packages, sometimes different versions of the same package. If everything shares one global Python, installing what one project needs can break another, and code that runs on your machine fails on a colleague's because the two machines have different packages. This is the "it works on my machine (and _only_ my machine)" problem. An *environment* is an isolated set of packages for one purpose. This guide shares one environment, `fieldguide` (defined in `environment.yml`), so its worked examples run identically for anyone reading it. It's scoped to this guide's own examples — your own project will have its own environment, with whatever packages your actual analysis needs.

## Create the environment

From the repository root, run:

```
conda env create -f environment.yml
```

This reads `environment.yml` and builds an environment named `fieldguide` containing the packages listed there. You do this once.

## Activate it

```
conda activate fieldguide
```

This turns the environment on. Your prompt will show `(fieldguide)`. Activate it in every new terminal before running any code in this repo. Without an active environment, you're in `base` (note the `(base)` at the start of your prompt) — avoid installing software there, since that can create conflicts with other environments' packages later.

## Other conda commands you'll use

```
conda env list
```

Lists every environment on your machine and marks the active one.

```
conda list
```

Lists the packages installed in the active environment.

```
conda install package_name
```

Installs a package into the active environment from conda's repositories.

```
pip install package_name
```

Installs a package using pip, Python's other installer. Prefer `conda install` first, because conda manages compatibility between packages. Fall back to `pip install` only when a package is not available through conda. Whichever you use, make sure the right environment is active first.

```
conda deactivate
```

Turns the current environment off.

## Tell VS Code about it

VS Code needs to know which environment to use for `.py` files. Open the Command Palette with Cmd+Shift+P (Mac) or Ctrl+Shift+P (Windows), type "Python: Select Interpreter," and choose the `fieldguide` environment. VS Code remembers this per workspace.

## Select the Jupyter kernel

When you open a `.ipynb` file, look at the top-right corner of the notebook. It shows the *kernel*: the Python environment the notebook will actually execute in. It must say `fieldguide`. If it does not, click it and choose the right one.

The kernel is separate from the interpreter you picked above. The interpreter setting governs `.py` files; the kernel governs the notebook. They can be mismatched, and when they are, you get the classic confusion: you installed a package, the interpreter can see it, but the notebook cannot, because the notebook is running on a different environment. If a notebook says a package is missing that you know you installed, check the kernel first.

## When to restart the kernel

A notebook keeps everything you have run in memory, which is convenient until that memory is stale. Restart the kernel in these cases:

- After installing a new package, so the notebook picks it up.
- After editing a module you imported, so the notebook loads the new version instead of the old one held in memory.
- When variables are in a confusing state and you cannot tell why.

The "Restart and Run All" button restarts the kernel and re-runs every cell from a clean slate. This is akin to the troubleshooting advice "turn it off and turn it back on again" — resets help. When something seems wrong for no clear reason, try restarting the kernel.

## Further reading

This doc covers conda and Jupyter kernels as used in this repo. For the broader reproducibility case for capturing computational environments (conda, containers, and beyond), see The Turing Way's [Reproducible Environments](https://book.the-turing-way.org/reproducible-research/renv/) chapter.
