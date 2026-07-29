# Documentation and doc sites

You already write docstrings (your project's coding-standards file, here `../../CLAUDE.md`, requires them). This doc turns them into a browsable site the whole team can read. That is not a publishing afterthought; it is a **review-and-communication tool for your team.** A reviewer can walk the shape of a colleague's analysis at the doc-site level, seeing the modules and functions and how they fit, without getting lost in individual lines. Frame it alongside `../onboarding/08_code_review.md` and the draft-PR habit from `10_from_scripts_to_pipelines.md`: the doc site is another surface for looking at each other's work.

## The documentation hierarchy

Documentation is layered onto normal work, not a separate project. From smallest to largest:

- **Self-documenting names.** A well-named function needs less explanation.
- **Comments that explain why**, not what (`../../CLAUDE.md`).
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

This is the same information `../../CLAUDE.md` already asks for, in a structure a tool can parse.

## Autodocumentation

**Autodocumentation** means generating the browsable HTML reference straight from your docstrings, rather than writing it by hand. Its great virtue: the docs cannot drift from the code, because they *are* the code's docstrings. You write the docstring once, next to the function, and the site regenerates from it.

## The tool: Sphinx

This guide recommends **Sphinx**. It is the documentation generator the scientific-Python ecosystem is built on (NumPy, SciPy, pandas, matplotlib, and scikit-learn all use it), and for documentation, which is long-lived infrastructure, that maturity matters. Choose tools you can depend on for years: Sphinx is community-governed and stable, it cross-links into other projects' documentation through **intersphinx** (a reference to `numpy.ndarray` becomes a link to NumPy's own docs), and it is the native format for **Read the Docs**. Tool governance is a real engineering criterion, not a detail; a generator with open, stable stewardship is worth more than a marginally prettier default.

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

Sphinx's autodoc *imports* your package to read its docstrings, so the package must be installed (the editable install from `20_packaging.md`, `pip install -e .`). Then an API page pulls the docstrings in. Because MyST is enabled you can write the page in Markdown and drop in the autodoc directive through an `eval-rst` block:

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

This serves the site at `http://localhost:8000` and rebuilds as you save a docstring or page. How to open a static build, and how to share the site (including from a private repo), is the next section.

## Previewing and sharing the site (including private repos)

**Viewing a build locally.** `sphinx-autobuild` (above) is the easiest path — it serves the site and reloads as you save; add `--host 127.0.0.1 --port 8000` if you need to pin the address. If you ran a plain `sphinx-build` instead, the output is just a folder of files, not a server: open `docs/_build/html/index.html`. One catch that gets everyone — pasting that path into a browser's address bar usually triggers a *search*, not a page load. Prefix it with `file:///` (three slashes), e.g. `file:///Users/you/project/docs/_build/html/index.html`, or just use `sphinx-autobuild` and sidestep it.

**Sharing it — mind the "private" part.** The obvious answer, GitHub Pages, has a trap for a private repo: on a GitHub **Pro** plan (including the educator plan), a Pages site built from a *private* repo is **still publicly reachable** — access-controlled Pages is an Enterprise-only feature. For unpublished work, such as a methods paper still in progress, that is usually not what you want. Private-safe ways to let teammates see the site:

- **A CI artifact (what the exemplar does).** Build the site in your GitHub Actions workflow (`14_continuous_integration.md`) and upload `docs/_build/html` with `actions/upload-artifact`. Anyone with **read access** to the repo gets it from the run's Summary page, or with `gh run download -n <artifact-name>`, then unzips and opens `index.html`. It is not a live URL and artifacts expire (set a retention period), but nothing is ever public.
- **Read the Docs** has a paid tier that serves private, access-controlled docs if you want a real hosted URL.
- **Cloudflare Pages** (or similar) can host with its own access control if you outgrow the artifact.

Rule of thumb: **public project → GitHub Pages or Read the Docs; private project → the CI artifact**, until you have a reason for hosted, access-controlled docs.

## A dependency note

`sphinx`, the theme (`furo`), `myst-parser`, and `sphinx-autobuild` are new dependencies. Per `../../CLAUDE.md`, adding them means asking first and updating the environment file, and saying so in the pull request that introduces the site.

## Reviewing analyses at the doc-site level

The payoff loops back to review. Instead of reading a colleague's pipeline line by line, you can open its doc site and walk the structure: what modules exist, what each function claims to do, how the pieces connect. It is the fastest way to understand the shape of an analysis, and it turns the site into a shared vocabulary for talking about the work. Pair it with a draft PR (`10_from_scripts_to_pipelines.md`) so a reviewer can look early.
