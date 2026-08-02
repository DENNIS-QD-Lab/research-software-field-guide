# Documentation and doc sites

You already write docstrings (your project's coding-standards file, here [CLAUDE.md](../../CLAUDE.md), requires them). This doc turns them into a browsable site the whole team can read. That is not a publishing afterthought; it is a **review-and-communication tool for your team.** A reviewer can walk the shape of a colleague's analysis at the doc-site level, seeing the modules and functions and how they fit, without getting lost in individual lines. Frame it alongside [08_code_review.md](../onboarding/08_code_review.md) and the draft-PR habit from [10_from_scripts_to_pipelines.md](10_from_scripts_to_pipelines.md): the doc site is another surface for looking at each other's work — the fastest way to grasp the shape of an analysis, and a shared vocabulary for talking about it.

## The documentation hierarchy

Documentation is layered onto normal work, not a separate project. From smallest to largest:

- **Self-documenting names.** A well-named function needs less explanation.
- **Comments that explain why**, not what ([CLAUDE.md](../../CLAUDE.md)).
- **Docstrings** on every function and module.
- **A README** that orients a newcomer to the whole repo.
- **A generated site** that turns the docstrings into a browsable reference.

Each layer builds on the one below. The site is only as good as the docstrings under it.

## Docstrings: pick one style

This guide recommends **NumPy-style** docstrings: a one-line summary, then structured `Parameters`, `Returns`, and `Examples` sections. It is the scientific-Python norm and reads well both in the source and on a generated site. One full example:

```python
def normalize(values: np.ndarray) -> np.ndarray:
    """Scale an array so its maximum value is 1.0.

    Parameters
    ----------
    values : np.ndarray
        The values to scale. Must contain at least one nonzero element.

    Returns
    -------
    np.ndarray
        The input scaled so its largest element is 1.0.

    Examples
    --------
    >>> normalize(np.array([1.0, 2.0, 4.0]))
    array([0.25, 0.5 , 1.  ])
    """
```

This is the same information [CLAUDE.md](../../CLAUDE.md) already asks for, in a structure a tool can parse.

## Autodocumentation

**Autodocumentation** means generating the browsable HTML reference straight from your docstrings, rather than writing it by hand. Its great virtue: the docs cannot drift from the code, because they *are* the code's docstrings. You write the docstring once, next to the function, and the site regenerates from it.

## The tool: Sphinx

This guide recommends **Sphinx** — the documentation generator the scientific-Python ecosystem is built on (NumPy, SciPy, pandas, matplotlib, and scikit-learn all use it). It cross-links into other projects' documentation through **intersphinx** (a reference to `numpy.ndarray` becomes a link to NumPy's own docs), and it is the native format for **Read the Docs**.

Two extensions make Sphinx fit the way your team already works:

- **napoleon** teaches Sphinx to read your NumPy-style docstrings.
- **MyST** lets you author narrative pages in **Markdown**, so adopting Sphinx does not mean rewriting your prose in reStructuredText.

## Setting up Sphinx

Documentation lives in a `docs/` folder with a `conf.py` configuration file. A minimal `docs/conf.py`:

```python
project = "SWIR HDR"
extensions = [
    "sphinx.ext.autodoc",      # generate pages from docstrings
    "sphinx.ext.napoleon",     # understand NumPy-style docstrings
    "sphinx.ext.intersphinx",  # cross-link into other projects' docs
    "myst_parser",             # author pages in Markdown, not just reStructuredText
]
html_theme = "furo"            # a clean, modern theme
intersphinx_mapping = {
    "numpy": ("https://numpy.org/doc/stable/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/", None),
}
```

Sphinx's autodoc *imports* your package to read its docstrings, so the package must be installed (the editable install from [21_packaging.md](21_packaging.md), `pip install -e .`). Then an API page pulls the docstrings in. Because MyST is enabled you can write the page in Markdown and drop in the autodoc directive through an `eval-rst` block:

````markdown
# API reference

```{eval-rst}
.. automodule:: swir_hdr.radiance
   :members:
```
````

The `automodule` directive renders every documented object in `swir_hdr.radiance`. Build the site, and preview it live while you edit:

```
sphinx-build -b html docs docs/_build/html
```

This builds the HTML into `docs/_build/html`. For a live-reloading preview while you write:

```
sphinx-autobuild docs docs/_build/html
```

This serves the site at `http://localhost:8000` and rebuilds as you save. Viewing a one-off build, and sharing the site, are covered next.

## Viewing and sharing the site

`sphinx-autobuild` (above) is the easiest way to look at the site while you work: it serves it at `http://127.0.0.1:8000` and reloads on save. If you instead ran a plain `sphinx-build`, open `docs/_build/html/index.html` — but note that pasting that path into a browser's address bar often triggers a *search* rather than opening the page, so prefix it with `file:///` (three slashes), or just use `sphinx-autobuild`.

To let others see it, publish it with **Read the Docs**, which builds and hosts Sphinx sites automatically on each push. If your repository is private and the work is unpublished, note that a GitHub Pages site built from it may still be publicly visible; building the HTML in a CI job and downloading it as an artifact keeps it internal (the appendix below shows the workflow).

## A dependency note

`sphinx`, the theme (`furo`), `myst-parser`, and `sphinx-autobuild` are new dependencies. Per [CLAUDE.md](../../CLAUDE.md), adding them means asking first and updating the environment file, and saying so in the pull request that introduces the site.

## Appendix: building the doc site in CI

Once the site builds locally, a CI job can build it automatically on every push — which catches a docstring that breaks the build, and (for a private repo) puts the HTML somewhere the team can reach it. This builds on the CI basics in [14_continuous_integration.md](14_continuous_integration.md); add a second job to that same `ci.yml`, or a separate `.github/workflows/docs.yml`:

```yaml
jobs:
  build-docs:
    runs-on: ubuntu-latest
    defaults:
      run:
        shell: bash -l {0}          # login shell, so `conda activate` works
    steps:
      - uses: actions/checkout@v4

      - uses: conda-incubator/setup-miniconda@v3
        with:
          environment-file: environment.yml   # this includes sphinx, furo, myst-parser
          activate-environment: helper

      - name: Install the package             # so autodoc can import it
        run: pip install -e . --no-deps

      - name: Build the site
        run: sphinx-build -b html docs docs/_build/html   # add -W to fail on warnings too

      - name: Upload the built site
        uses: actions/upload-artifact@v4
        with:
          name: docs-html
          path: docs/_build/html
          retention-days: 30
```

The build step is exactly the local command from *Setting up Sphinx*; the steps around it just recreate the environment (so autodoc can import your package) and save the result. To view it, open the run from the repo's **Actions** tab, download `docs-html` from its Summary (or run `gh run download -n docs-html`), unzip, and open `index.html`.

For a *public* project you can instead deploy straight to GitHub Pages or connect Read the Docs; the artifact is the private-safe option, because the download is only available to people with read access to the repo.
