# Packaging: the local package, and going further

This is the first doc in the **disseminating track**: increasingly formal ways of letting other
people see and depend on your work. Packaging (here) is what lets code be installed rather than
copy-pasted; [22_publishing_a_paper.md](22_publishing_a_paper.md) covers freezing a citable snapshot
for a publication; [23_shipping_a_library.md](23_shipping_a_library.md) covers trimming and
versioning the pipeline itself into something other people install. A project may need any, all, or
none of the latter two — they're independent of each other.

**Two different questions live in this doc, and they have different answers.** The first — does
your project need a `pyproject.toml`, a `src/` layout, and an editable install — is close to a
foregone conclusion if you're using this guide's structure at all:
[15_experiments_and_shipping.md](../implementing/15_experiments_and_shipping.md)'s central move,
`experiments/` importing method code from `src/`, only works once the package is installed. That's
**the local package**, and most readers of this guide already need it. The second question —
should this package be installable by *other* repos, other people, or eventually PyPI — is the
actual distribution decision, and it's genuinely optional: most research code never needs it.

## What a package is

A **package** is a directory of code that Python's import system and its installer (`pip`) both
recognize as a single, named, versioned unit. Install it once, and `import yourpkg` works from
anywhere — the same way `import numpy` does — rather than only from inside the one folder the code
happens to sit in.

## The local package: `pyproject.toml`, the `src/` layout, and an editable install

Two pieces turn a folder into a package:

- **`pyproject.toml`** declares the package: its name, version, dependencies, and build backend. It
  is the modern standard and replaces the older `setup.py`.
- **The `src/` layout** puts the importable code under `src/yourpkg/`. Keeping it under `src/`
  rather than at the repo root stops tests and experiments from accidentally importing the
  un-installed copy, so what you test is what installs.

A minimal `pyproject.toml` for a research project is short:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "yourpkg"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = []          # conda manages these; list them here only for a pip-installable release

[tool.pytest.ini_options]
testpaths = ["tests"]
```

`[build-system]` names the tool that turns the folder into an installable package — `hatchling` is a
common, low-configuration choice. `[project]` is the metadata `pip` reads. `dependencies` can stay empty
while conda owns the environment; fill it in when the package is meant to be installed by someone else
([Going further](#going-further-making-the-package-installable-by-others), below). The
`[tool.pytest.ini_options]` table is a convenient place to keep pytest's settings, so the project needs
no separate `pytest.ini`.

Install it in **editable** mode:

```
pip install -e .
```

`import yourpkg` now works from anywhere, and edits to the source take effect immediately, with no
reinstall. This is what lets the tests, the experiments, and the doc site
([20_documentation_and_doc_sites.md](../implementing/20_documentation_and_doc_sites.md)) all import
the library the same way — it's the missing piece behind doc 15's `experiments/` → `src/` import
pattern. In a conda environment, add `--no-deps` so pip installs only your package and leaves the
conda-managed dependencies alone.

One incidental benefit worth knowing about: an installed package is importable and runnable from
**any** directory, not just its own. A folder of scripts effectively has to be run from the code's
own directory, or with fragile `sys.path` juggling; once installed, you can `cd` into the folder
where a dataset sits and have the tool read its inputs and write its outputs right there. A package
can also declare a **command-line entry point** in `pyproject.toml`, so a name like `your-tool`
becomes a command you can run from any directory — the polished form of the same idea.

## Going further: making the package installable by others

Everything above is close to a requirement for this guide's structure. What follows is a genuinely
optional decision — should code that's already a local package also be installable by other repos,
other people, or a package index? Yes, if...

- **Other repos import it.** You are copy-pasting the same code between projects instead of
  installing it once.
- **You want versioned installs consumed elsewhere.** A project depends on "version 2.1 of this,"
  not "whatever your repo's `main` looks like today."

If neither applies, stop here — the local package is already doing its job, and going further is
real overhead for no benefit. A collection of standalone scripts and training docs that
never adopts the `src/` + `experiments/` split doesn't need even the local package — see
[06_adding_a_script.md](../onboarding/06_adding_a_script.md) — that's a different, equally valid
repo shape when that's all that's needed.

### A lighter step before PyPI: installing straight from GitHub

Once a project has a `pyproject.toml`, others can install it directly from the repository, no PyPI
publication required:

```
pip install git+https://github.com/your-org/your-repo.git
```

This is a real, citable-in-a-README distribution method, worth adding to the README once a project
reaches this point, well before "publish to PyPI" is on the table.

### The next step

Once a project is a package, [23_shipping_a_library.md](23_shipping_a_library.md) covers the rest of
going further: versioning it properly, and publishing it to **PyPI** so anyone can `pip install` it.

## Further reading

This doc covers the minimum to know whether and how to package. For deeper detail — `pyproject.toml` fields, build backends, and the compiled-extension case this doc does not cover — see the [Scientific Python Development Guide's "Simple packaging" page](https://learn.scientific-python.org/development/guides/packaging-simple/). Once a project is packaged, two tools from that same ecosystem can check and scaffold it automatically: [`sp-repo-review`](https://learn.scientific-python.org/development/guides/repo-review/) checks an existing repository against the ecosystem's packaging and CI conventions, and the [scientific-python/cookie](https://github.com/scientific-python/cookie) template scaffolds a new one already conforming to them.
