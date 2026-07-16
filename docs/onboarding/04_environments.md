# Environments

## Why environments exist

Different projects need different packages, sometimes different versions of the same package. If everything shares one global Python, installing what one project needs can break another, and code that runs on your machine fails on a colleague's because the two machines have different packages. This is the "it works on my machine (and _only_ my machine)" problem. An *environment* is an isolated set of packages for one purpose. This repo shares one named `helper`, defined in `environment.yml`, so everyone runs the same software when running through the learning modules.

## Create the environment

From the repository root, run:

```
conda env create -f environment.yml
```

This reads `environment.yml` and builds an environment named `helper` containing the packages listed there. You do this once.

## Activate it

```
conda activate helper
```

This turns the environment on. Your prompt will show `(helper)`. Activate it in every new terminal before running lab code.

## Tell VS Code about it

VS Code needs to know which environment to use for `.py` files. Open the Command Palette with Cmd+Shift+P (Mac) or Ctrl+Shift+P (Windows), type "Python: Select Interpreter," and choose the `helper` environment. VS Code remembers this per workspace.

## Select the Jupyter kernel

This is where people get stuck, so read it carefully. When you open a `.ipynb` file, look at the top-right corner of the notebook. It shows the *kernel*: the Python environment the notebook will actually execute in. It must say `helper`. If it does not, click it and choose the right one.

The kernel is separate from the interpreter you picked above. The interpreter setting governs `.py` files; the kernel governs the notebook. They can be mismatched, and when they are, you get the classic confusion: you installed a package, the interpreter can see it, but the notebook cannot, because the notebook is running on a different environment. If a notebook says a package is missing that you know you installed, check the kernel first.

## When to restart the kernel

A notebook keeps everything you have run in memory, which is convenient until that memory is stale. Restart the kernel in these cases:

- After installing a new package, so the notebook picks it up.
- After editing a module you imported, so the notebook loads the new version instead of the old one held in memory.
- When variables are in a confusing state and you cannot tell why.

The "Restart and Run All" button restarts the kernel and re-runs every cell from a clean slate. This is akin to the troubleshooting advice 'turn it off and turn it back on again'-- resets help. When something seems wrong for no clear reason, try restarting the kernel. 
