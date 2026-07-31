# Adding a script

This doc covers what goes where, how to name and document a helper, and how to tell whether a piece of code belongs in this repository at all. It uses `scripts/show_h5_keys.py` as a model.

## Where things go

Runnable Python scripts (`.py` files) go in `scripts/`. Jupyter notebooks (`.ipynb` files) go in `notebooks/`. Keep the two separate so it is always clear which files are importable tools and which are exploration.

## Naming conventions

All filenames use snake_case: lowercase letters and digits, words separated by underscores, no hyphens, no camelCase, no spaces. Keep names under about 30 characters. Avoid abbreviations except universally understood ones in your field (e.g., in image-processing research like the SWIR_HDR exemplar, `hdf5`, `hdr`, `nir`, `qd`, `swir` are fine; `seg` for `segmentation` or `proc` for `processing` is not).

Beyond that, we use two grammatical patterns depending on what the file does.

**Verb-first names for action scripts.** If the file's purpose is to *do* a task, name it with a verb followed by what it acts on, so the name reads like a command. Examples: `show_h5_keys.py` (shows the metadata (a.k.a. keys) of an HDF5 file), `plot_spectra.py` (plots spectra), `convert_units.py` (converts units), `clean_metadata.py` (cleans metadata).

**Noun-phrase names for functionality modules.** If the file's purpose is to *contain* code that other scripts import and use, name it with a noun or adjective-noun phrase describing what is inside, so the name reads like a topic. Examples: `ratio_analysis.py` (contains ratio analysis code), `hdr_processing.py` (contains HDR processing code), `broadband_segmentation.py` (contains broadband segmentation code).

If you are unsure which category a file falls into, ask whether a colleague seeing it at the top of their screen will more often think "I want to run this" (verb) or "I want to import from this" (noun), and pick accordingly. If it is genuinely both, lean toward the verb form and import from it when needed.

## Minimum docstring

Every script needs a docstring at the top of the file. If you are unsure what a docstring is, see [00_python_code_basics.md](00_python_code_basics.md). At minimum it states three things:

- **Purpose:** what the script does, in a sentence or two.
- **Inputs:** what it expects, for example the command-line arguments.
- **Example call:** a real command someone can copy and run.

The top of `scripts/show_h5_keys.py` is the template to copy. It defines its terms, lists its single input, and shows both the command-line call and the import.

## Does this belong here?

Helpers are small, reusable, and not tied to one project. Before adding something, ask whether you would reach for it across different studies. A script that inspects any HDF5 file is a helper and belongs here. A script that only makes sense for the data of one specific experiment is project-specific and belongs in that project's own repository, not here. When you are unsure, raise it in the pull request and let the reviewer weigh in.

## Worked example: how `show_h5_keys.py` is built

Open `scripts/show_h5_keys.py` and read it top to bottom. It is short and follows the pattern every helper should.

The **module docstring** explains the script and defines the HDF5 vocabulary (groups, datasets, attributes) on first use, then shows how to run it and how to import it.

The **imports** are `argparse` (to define and read the command-line argument) and `h5py` (to open the file).

`show_keys(path: str) -> None` is the **importable function** that does the real work. It opens the file and walks its tree. Because the logic lives in a named function with a type-hinted signature, another script can reuse it with `from scripts.show_h5_keys import show_keys` rather than copying code. The two private helpers, `_print_group` and `_print_attrs`, keep the recursion readable; the leading underscore signals "internal detail, not part of the public interface."

`main()` uses `argparse` to define one argument, the file path, then reads it and calls `show_keys`. We use `argparse` rather than reading `sys.argv` by hand because it gives a clear error and usage message for free when the argument is missing, and a `--help` flag automatically. Try `python scripts/show_h5_keys.py --help` to see it.

The `if __name__ == "__main__":` block at the bottom calls `main()` only when the file is run directly, so running it as a script and importing it as a library both work, as was described in [00_python_code_basics.md](00_python_code_basics.md).

Copy this shape for new helpers: a module docstring, imports, one or more well-named functions with type hints and docstrings, a `main()` for the command line, and the `if __name__` block to wire it up.
