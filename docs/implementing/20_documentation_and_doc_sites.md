# Documentation and doc sites

You already write docstrings (your project's coding-standards file, here [CLAUDE.md](../../CLAUDE.md), requires them). This doc turns them into a browsable site the whole team can read, useful for review as much as reference. A reviewer can walk the shape of a colleague's analysis at the doc-site level, seeing the modules and functions and how they fit, without getting lost in individual lines. It works alongside code review ([08_code_review.md](../onboarding/08_code_review.md)) and the draft-PR habit ([10_from_scripts_to_pipelines.md](10_from_scripts_to_pipelines.md)) as another surface for looking at each other's work — the fastest way to grasp the shape of an analysis, and a shared vocabulary for talking about it.

The same site also holds the experiment findings from [16_running_a_dry_lab_experiment.md](16_running_a_dry_lab_experiment.md) — the research log and each theme's findings — so it ends up doing two jobs at once: a browsable API reference, and a shareable, always-current lab notebook.

## The documentation hierarchy

Documentation is layered onto normal work, not a separate project. From smallest to largest:

- **Self-documenting names.** A well-named function needs less explanation.
- **Comments that explain why**, not what.
- **Docstrings** on every function and module.
- **A README** that orients a newcomer to the whole repo.
- **A generated site** that turns the docstrings into a browsable reference.

Each layer builds on the one below: a generated site pulls directly from the docstrings, so a gap or a vague docstring shows up as a gap or a vague page on the site.

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

**Autodocumentation** means generating the browsable HTML reference straight from your docstrings, rather than writing it by hand. The docs cannot drift from the code, because they *are* the code's docstrings: write the docstring once, next to the function, and the site regenerates from it.

## The tool: Sphinx

This guide recommends **Sphinx** — the documentation generator the scientific-Python ecosystem is built on (NumPy, SciPy, pandas, matplotlib, and scikit-learn all use it). It cross-links into other projects' documentation through **intersphinx** (a reference to `numpy.ndarray` becomes a link to NumPy's own docs), and it is the native format for **Read the Docs**.

Two extensions make Sphinx fit the way your team already works:

- **napoleon** teaches Sphinx to read your NumPy-style docstrings.
- **MyST** lets you author narrative pages in **Markdown**, so adopting Sphinx does not mean rewriting your prose in reStructuredText.

## Setting up Sphinx

Documentation lives in a `docs/` folder with a `conf.py` configuration file. A minimal `docs/conf.py`:

```python
project = "Your Project"
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

Sphinx's autodoc *imports* your package to read its docstrings, so the package must be installed (the editable install from [21_packaging.md](../disseminating/21_packaging.md), `pip install -e .`). Then an API page pulls the docstrings in. Because MyST is enabled you can write the page in Markdown and drop in the autodoc directive through an `eval-rst` block:

````markdown
# API reference

```{eval-rst}
.. automodule:: yourpkg.core_algorithm
   :members:
```
````

The `automodule` directive renders every documented object in `yourpkg.core_algorithm`. Build the
site once with:

```
sphinx-build -b html docs docs/_build/html
```

This builds the HTML into `docs/_build/html` and exits. While you're actively writing, rebuild on
every save instead:

```
sphinx-autobuild docs docs/_build/html
```

This serves the site at `http://127.0.0.1:8000` and rebuilds as you save.

## Rendering experiment findings into the same site

The API reference above is one half of the doc site; the other half is the experiment findings from
[16_running_a_dry_lab_experiment.md](16_running_a_dry_lab_experiment.md) — the same `docs/` build, a
second kind of page. Each theme gets exactly one:

- **`docs/experiment_overviews/<theme>_overview.md`** — one page per theme, its entire body a MyST
  `{include}` of that theme's `experiments/<theme-slug>/README.md`, so the doc site never holds a
  second copy of the findings:

  ````markdown
  ```{include} ../../experiments/<theme-slug>/README.md
  :relative-docs: ../../experiments/<theme-slug>/
  :relative-images:
  ```
  ````

  The `:relative-docs:`/`:relative-images:` options matter: without them, MyST resolves the README's
  own relative image links (`![](details/<run-id>/fig.png)`) against the *overview page's* directory
  instead of the README's own, and the figure silently fails to render. With them, the README's plain,
  self-relative paths work both through this include and when the README is viewed directly on GitHub.
  Full mechanics: [readme_to_doc_site.md](../reference/readme_to_doc_site.md).

There is no second folder of per-run report pages to keep in sync — a finding is on the site as soon
as it's written into the theme's README, figure and all.

A `figures/` folder, if you keep one for a manuscript in progress ([22_publishing_a_paper.md](../disseminating/22_publishing_a_paper.md)), uses the identical pattern under `docs/figure_overviews/` — see [example_repo_structure.md](../reference/example_repo_structure.md) for a worked example.

Wire `docs/index.md` with a `toctree` pointing at the overview pages, one per theme:

````markdown
```{toctree}
:maxdepth: 2
:caption: Experiments

experiment_overviews/theme_a_overview
experiment_overviews/theme_b_overview
```
````

**An optional exception: standalone deep-dive reports.** A hand-authored page under
`docs/experiment_summaries/<name>.md`, optionally executable via `myst-nb`, is a reasonable exception
for the rare read-out that's genuinely too complex for the README's figure-and-caption pattern. Keep it
rare, and link to it from the theme's README rather than letting it replace the Findings section —
[readme_to_doc_site.md](../reference/readme_to_doc_site.md) covers when this is actually
worth it and how to build one.

## Viewing and sharing the site

The site can reach a reader at four different levels, each trading immediacy for reach:

| Level | What it is | Good for | Triggered by | Find it at |
|---|---|---|---|---|
| Local build | `sphinx-build`/`sphinx-autobuild` on your own machine | Working on the docs yourself | Running the command | `file:///docs/_build/html/index.html`, or `sphinx-autobuild`'s live server |
| CI artifact | A fresh build attached to each CI run | Sharing the current state with colleagues with repo access; catching a broken build immediately | Automatic, on every push | The run's Actions-tab Summary, or `gh run download` |
| Tagged release | The same build, zipped and attached to a GitHub Release | Archiving or sharing one deliberate, polished snapshot | Manual (`workflow_dispatch`, or by hand) | The repo's Releases page |
| GitHub Pages / Read the Docs | A hosted website built from the docs | A public project's permanent doc site | Automatic, on every push (once configured) | The Pages/Read the Docs URL — public even if the source repo is private |

The rest of this section covers the first two; the appendices below cover the tagged release and the CI setup behind the artifact.

`sphinx-autobuild` (above) is the easiest way to look at the site while you work: it serves it at `http://127.0.0.1:8000` and reloads on save. If you instead ran a plain `sphinx-build`, open `docs/_build/html/index.html` — but note that pasting that path into a browser's address bar often triggers a *search* rather than opening the page, so prefix it with `file:///` (three slashes), or just use `sphinx-autobuild`.

To let others see it without waiting for a CI run, publish it with **Read the Docs** or **GitHub Pages**, which both build and host the site automatically on every push. Both publish at a public URL regardless of whether the source repository is private — if the work is unpublished, that's the wrong tool; building the HTML in a CI job and downloading it as an artifact keeps it visible only to people with read access to the repo (the appendix below shows the workflow).

## A dependency note

`sphinx`, the theme (`furo`), `myst-parser`, and `sphinx-autobuild` are in this repo's
`environment.yml`, pinned to exact versions. Pinning earns its keep here more than for most
dependencies, because of the `-W` flag: it promotes every warning to an error, so a new Sphinx release
that merely adds a deprecation notice is enough to fail a build whose content never changed. That is
the same drift [11_code_quality_tools.md](11_code_quality_tools.md) describes for a linter, reaching
the docs instead of the code. `myst-parser` and `furo` also each declare a supported range of Sphinx
versions, so letting one float can force a downgrade of another. Bump the four together, deliberately.

Add `myst-nb` as well if a page needs executable cells (*Rendering experiment findings into the same
site*, above). In your own project all of these are new dependencies, so per
[CLAUDE.md](../../CLAUDE.md) that means asking first, updating the environment file, and saying so in
the pull request that introduces the site.

The `gh` commands in the appendices below come from the **GitHub CLI**, also in `environment.yml`. Run
`gh auth login` once before the first use; it opens a browser to authorize the CLI against your
account.

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
          environment-file: environment.yml   # must list sphinx, furo, myst-parser
          activate-environment: fieldguide

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

For a *public* project you can instead deploy straight to GitHub Pages or connect Read the Docs; the artifact is the private-safe option, because the download is only available to people with read access to the repo — which is also why keeping project repos under one lab organization ([repo_ownership_and_visibility.md](../reference/repo_ownership_and_visibility.md)) makes this artifact reachable lab-wide instead of one invite at a time.

## Appendix: archiving a permanent snapshot

The artifact above is deliberately temporary. GitHub deletes it after `retention-days`, and that is the right behavior for day-to-day review, where only the latest build matters and a private repo shouldn't quietly accumulate a large binary download from every commit. It is the wrong mechanism for a snapshot that needs to outlive that window — handing the current docs to a collaborator who doesn't have repo access to the Actions tab, or keeping a copy tied to a specific manuscript draft. An artifact built for that purpose will have expired, whether or not anyone opened it, well before anyone needed it again.

For that case, attach the built site to a **GitHub Release** instead of a workflow artifact. A release has no retention limit, appears on the repo's own Releases page instead of inside a CI run, and its tag names the snapshot (`docs-260818`, or something version-like such as `docs-v1`) the same way a code release would. Unzip the download and open `index.html` directly — no Pages hosting and no Actions-tab access needed, only read access to the repo.

The trade-off is the artifact's retention limit in reverse: a release does not expire, so triggering this on every push accumulates one archive per commit, most of which nobody will ever open. Trigger it deliberately instead, with `workflow_dispatch` (a button in the Actions tab, or `gh workflow run`), so a release only gets created when someone decides the current docs are worth keeping:

```yaml
name: Archive docs

on:
  workflow_dispatch:   # click "Run workflow" in the Actions tab when a snapshot is wanted

jobs:
  archive-docs:
    runs-on: ubuntu-latest
    defaults:
      run:
        shell: bash -l {0}
    steps:
      - uses: actions/checkout@v4

      - uses: conda-incubator/setup-miniconda@v3
        with:
          environment-file: environment.yml
          activate-environment: fieldguide

      - name: Install the package
        run: pip install -e . --no-deps

      - name: Build the site
        run: sphinx-build -W -b html docs docs/_build/html

      - name: Zip the built site
        run: cd docs/_build/html && zip -rq ../../../docs-site.zip .

      - name: Create the release
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          TAG="docs-$(date +%y%m%d)"
          gh release create "$TAG" docs-site.zip \
            --title "Doc site archive — $(date +%Y-%m-%d)" \
            --notes "Static build of the Sphinx doc site, built from $GITHUB_SHA."
```

Most projects want both, at different frequencies: the CI artifact on every push, catching a broken build immediately and giving the team a current copy without anyone asking for one; the tagged release on demand, for the handful of moments a copy needs to survive longer than a month or reach someone by name. Tagging a paper's code state for a DOI archive is a separate practice ([22_publishing_a_paper.md](../disseminating/22_publishing_a_paper.md)) that fixes the citable state of the code itself; this workflow only preserves a copy of the rendered docs.

## Further reading

This doc focuses on Sphinx because it is the tool the scientific-Python ecosystem has standardized on. For the ecosystem's own documentation guide, covering the other frameworks it supports and more Sphinx configuration detail than fits here, see the [Scientific Python Development Guide's "Documentation" page](https://learn.scientific-python.org/development/guides/docs/).
