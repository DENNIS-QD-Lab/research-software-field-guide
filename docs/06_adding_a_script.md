# Adding a script

This doc covers what goes where, how to name and document a helper, and how to tell whether a piece of code belongs in this repository at all. It uses `scripts/show_h5_keys.py` as the model.

## Where things go

Runnable Python scripts (`.py` files) go in `scripts/`. Jupyter notebooks (`.ipynb` files) go in `notebooks/`. Keep the two separate so it is always clear which files are importable tools and which are exploration.

## Naming

Name scripts `verb_noun.py`: a verb saying what it does, a noun saying what it acts on. `show_h5_keys.py` shows the keys of an HDF5 file. `plot_qd_spectra.py` plots QD spectra. A name read aloud should tell a labmate what the script does before they open it. Use lowercase words joined by underscores.

## Minimum docstring

Every script needs a docstring at the top of the file. If you are unsure what a docstring is, see `docs/00_python_code_basics.md`. At minimum it states three things:

- **Purpose:** what the script does, in a sentence or two.
- **Inputs:** what it expects, for example the command-line arguments.
- **Example call:** a real command someone can copy and run.

The top of `scripts/show_h5_keys.py` is the template to copy. It defines its terms, lists its single input, and shows both the command-line call and the import.

## Does this belong here?

Helpers are small, reusable, and not tied to one project. Before adding something, ask whether you would reach for it across different studies. A script that inspects any HDF5 file is a helper and belongs here. A script that only makes sense for the data of one specific experiment is project-specific and belongs in that project's own repository, not here. When you are unsure, raise it in the pull request and let the reviewer weigh in.

## Worked example: how `show_h5_keys.py` is built

Open `scripts/show_h5_keys.py` and read it top to bottom. It is short and follows the pattern every helper should.

The **module docstring** explains the script and defines the HDF5 vocabulary (groups, datasets, attributes) on first use, then shows how to run it and how to import it.

The **imports** are `sys` (to read the command-line argument) and `h5py` (to open the file).

`show_keys(path: str) -> None` is the **importable function** that does the real work. It opens the file and walks its tree. Because the logic lives in a named function with a type-hinted signature, another script can reuse it with `from scripts.show_h5_keys import show_keys` rather than copying code. The two private helpers, `_print_group` and `_print_attrs`, keep the recursion readable; the leading underscore signals "internal detail, not part of the public interface."

`main()` reads the file path from the command line and calls `show_keys`. If the argument is missing, it prints a usage line and exits rather than failing with a confusing error.

The `if __name__ == "__main__":` block at the bottom calls `main()` only when the file is run directly, so running it as a script and importing it as a library both work. `docs/00_python_code_basics.md` explains that block in full.

Copy this shape for new helpers: a module docstring, imports, one or more well-named functions with type hints and docstrings, a `main()` for the command line, and the `if __name__` block to wire it up.
