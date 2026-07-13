# Packaging: when a folder becomes an installable package

*Distribution tier, optional.* This doc is for when you are wondering whether a collection of code should become an installable package. Most lab code never needs this, so treat it as "read when the question comes up," not a required step.

## When does a folder of scripts become a package?

A folder of scripts (`../onboarding/06_adding_a_script.md`) is the right form for most work. Consider packaging only when you see these signals:

- **Other repos import it.** You are copy-pasting the same code between projects instead of installing it once.
- **You want versioned installs.** A project depends on "version 2.1 of this," not "whatever is in the folder today."
- **You want to run it from wherever your data lives.** This one is easy to miss if you are a scientist first, not a software engineer. A folder of scripts effectively has to be run from the code's own directory, or with fragile `sys.path` and path juggling. An *installed* package is importable and runnable from **any** directory, so you can `cd` into the folder where a dataset sits and have the tool read its inputs and write its outputs right there. It decouples "where the code lives" from "where you run it" — exactly what you want when data is scattered across many directories. (`SWIR_HDR`'s pipeline, designed to run in each data folder, is a case in point.)

If none of these apply, do not package. It is real overhead for no benefit.

## What a package is: `pyproject.toml` and the `src/` layout

Two pieces turn a folder into a package.

- **`pyproject.toml`** declares the package: its name, version, dependencies, and build backend. It is the modern standard and replaces the older `setup.py`.
- **The `src/` layout** puts the importable code under `src/yourlib/`. Keeping it under `src/` rather than at the repo root stops tests and experiments from accidentally importing the un-installed copy, so what you test is what installs.

The `SWIR_HDR_v2` exemplar is the worked example: `14_experiments_and_shipping.md` moved it to exactly this shape, with `src/swir_hdr/` and a `pyproject.toml` declaring `name = "swir_hdr"` and its version.

## Editable installs for development

```
pip install -e .
```

This installs the package in **editable** mode: `import swir_hdr` works from anywhere, but your edits to the source take effect immediately, with no reinstall. It is the standard local-development setup, and it is what lets the tests, the experiments, and the doc site (`16_documentation_and_doc_sites.md`) all import the library the same way. In a conda environment, add `--no-deps` so pip installs only your package and leaves the conda-managed dependencies alone.

A package can also declare a **command-line entry point** in `pyproject.toml`, so that a name like `swir-hdr` becomes a command you can run from any directory. That is the polished form of "run it where the data lives": the user works in their data folder and calls the command, with no `cd` into the code and no path juggling.

## This repo is intentionally not packaged

`DENNIS_helpers` is a collection of standalone helper scripts and training docs, not a library that other code imports. It stays a folder of scripts on purpose. Packaging is for a real project like `SWIR_HDR` once it is imported or installed elsewhere, not for this one.

## The next step, out of scope here

Once a project is packaged, versioned (`18_versioning_and_releases.md`), and licensed and citable (`19_citation_and_open_science.md`), the further step is publishing to **PyPI** so anyone can `pip install` it. That is deliberately out of scope for this track; it is named here only so you know it is the next thing that exists when you get there.
