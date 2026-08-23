# What are we doing here?

Increasingly, scientists and students are able to access complex computational analysis using AI coding assistants. Accelerating scientific discovery via **vibe coding** is great, but we are still each independently responsible for our own scientific output, the repeatability of our results, and the responsible development of research software. In that context, this repo intends to give the non-computer scientist a framework and tutorial on how to (vibe) code their science rigorously, ensure the repeatability of their experiments, and be able to automatically turn their code outputs and analysis into a website for accessible viewing to facilitate discussion of the results (even with a non-coder) and/or archiving.

Regardless of whether a human or AI assistant is doing the bulk of the coding, it's critical that you maintain control of the scientific questions being asked, can follow the code generated, verify it does what you actually asked, and
run it yourself — which is exactly what this track builds toward. The coding standards and habits
taught here, and enforced later on, exist for that same reason regardless of who typed the code: they
let you, a reviewer, or future you tell whether a result is actually correct, not just
plausible-looking. [18_ai_assisted_development.md](../implementing/18_ai_assisted_development.md) and
[ai_coding_assistants.md](../reference/ai_coding_assistants.md) cover working with an assistant
directly, once you're doing that on real work.

## Python code basics

*(Wondering why this doc is numbered 00, not 01? Most programming languages, including Python, count
from zero — this guide does too, starting here.)*

This doc explains how a Python file is put together and how it differs from a notebook. It references an example, `scripts/show_h5_keys.py`, to point at each piece. Open that file alongside this one.

## The whole example, mapped

In `scripts/show_h5_keys.py`:

- The triple-quoted text at the very top is the **module docstring**.
- `import argparse` and `import h5py` are the **imports**.
- `def show_keys(path: str) -> None:` is a **function** with **type hints** and its own **docstring**.
- `pad = "  " * indent` inside it is a **variable**.
- The `if __name__ == "__main__":` block at the bottom is the **command-line entry point**.

## `.py` files versus `.ipynb` files

A `.py` file is a plain text file of Python code. You run the whole thing at once, top to bottom, usually from the command line. Scripts and importable tools are `.py` files.

A `.ipynb` file is a Jupyter notebook. A notebook is a document made of *cells* that you run one at a time, in any order, keeping the results visible in between. Notebooks are for interactive exploration: trying things, looking at data, making a quick plot.

Use a notebook while you are figuring something out. Once the logic is settled and you want to reuse it, move it into a `.py` file. You may use either or both of these file types, and [07_notebooks.md](07_notebooks.md) describes ways to manage them in parallel.

## Cells inside a notebook

A notebook has two kinds of cells. A *code cell* holds Python and runs when you press Shift+Enter. A *markdown cell* holds formatted text (headings, notes, explanations) using the same markdown syntax as these docs. Markdown cells are how you narrate what the code cells are doing. 

> **Tip:** These docs are markdown (`.md`) files. If you are reading this as raw text in an editor like VS Code, press Cmd+Shift+V (Mac) or Ctrl+Shift+V (Windows) to toggle between the raw text and the formatted preview.

## Anatomy of a Python file

Read `scripts/show_h5_keys.py` from the top. Most files have these parts in this order.

**Imports** bring in code written elsewhere. `import h5py` makes the `h5py` library available under the name `h5py`. `import argparse` does the same for a module from Python's standard library. Imports go at the top.

**Variables** are names that hold values. Inside `show_keys`, the line `pad = "  " * indent` creates a variable named `pad`. The name on the left points at the value on the right.

**Functions** are named, reusable blocks of code, defined with the keyword `def`. In the example, `def show_keys(path: str) -> None:` defines a function called `show_keys` that takes one input named `path`. Code inside the function runs only when the function is *called*, for example `show_keys("data.h5")`.

**Classes** are templates that bundle data and functions together, defined with the keyword `class`. You will see classes when you use libraries (an `h5py.File` is an object built from a class). You probably will not write your own at first, so do not worry about them yet.

**Top-level code** is any code not indented inside a function or class. It runs immediately when the file is executed. In a well-organized script most logic lives in functions, and the top level just wires them together.

## Docstrings

A *docstring* is text (a string) written as the first line inside a file, function, or class, wrapped in triple quotes (`"""like this"""`). It documents what the thing does. The example file opens with a module docstring describing the whole script, and the function `show_keys` has its own docstring describing that function.

Docstrings are not comments for you alone. Python stores them, so anyone can read them later by running `help(show_keys)` in a Python session. Writing a clear docstring is the single most useful habit for code other people (including future you) will read.

## Type hints

A *type hint* is an annotation saying what kind of value something is expected to be. In `def show_keys(path: str) -> None:`, the `: str` says `path` should be a string, and the `-> None` says the function returns nothing.

Type hints are documentation that tools can read. They help your editor catch mistakes and help readers understand the code. It's worth noting that **Python does not enforce types at runtime.** If you pass a number where a hint says `str`, Python will not stop you. Hints describe intent; they do not police it.

## `if __name__ == "__main__":`

At the bottom of the example you will see:

```python
if __name__ == "__main__":
    main()
```

This block runs when you execute the file directly from the command line, but not when you `import` it from another script. It is the standard way to make a file usable both as a library and as a script. Running `python scripts/show_h5_keys.py data.h5` triggers the block and calls `main()`, thereby running the module show_h5_keys.py on the file data.h5. Writing `from scripts.show_h5_keys import show_keys` in another file imports the function `show_keys` without running it.

[06_adding_a_script.md](06_adding_a_script.md) walks through how this script does its job.

## Further reading

This doc is a fast on-ramp for what you need in this repo. For a full self-paced lesson on Python fundamentals with more practice exercises, see Software Carpentry's [Programming with Python](https://swcarpentry.github.io/python-novice-inflammation/).
