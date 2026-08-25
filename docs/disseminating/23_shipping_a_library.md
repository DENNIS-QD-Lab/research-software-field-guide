# Shipping a library

This doc is about trimming the pipeline itself into something other people install and depend on —
pared down to the approach you settled on, versioned so an upgrade's risk is knowable at a glance,
and made approachable to someone interested in the software as a finished product, with no context on the research that produced it.
[22_publishing_a_paper.md](22_publishing_a_paper.md) covers the separate, independent case of
freezing a citable snapshot for a publication. A project may do either, both, or neither.

## Semantic versioning

Version numbers are **MAJOR.MINOR.PATCH** (for example `2.1.0`), and each part carries a promise:

- **PATCH** (`2.1.0` → `2.1.1`): bug fixes, no change to how the code behaves for users.
- **MINOR** (`2.1.0` → `2.2.0`): new features, but existing usage still works (backward-compatible).
- **MAJOR** (`2.1.0` → `3.0.0`): breaking changes; code using the old version may need updating.

The scheme tells a user, at a glance, whether upgrading is safe. There is also the **0.x convention**:
while a project is below `1.0.0`, it is signaling "still unstable, anything may change." A project
moves past that once it cuts a `v1.0` release; later work then continues on the `2.x` line, `3.x`
line, and so on. Cut the tag itself the same way as [22_publishing_a_paper.md](22_publishing_a_paper.md)
covers (`git tag -a`, `git push origin <tag>`) — the mechanics don't change, only the naming
convention behind the number.

## A single source of truth for the version

The version should live in exactly one place, so it can never disagree with itself. For example, a
project's `pyproject.toml` declares `version = "2.1.0"`, and the package reads it back at runtime
from the installed metadata (`yourpkg.__version__`) rather than hard-coding the number a second time.
One place to change, no chance of drift.

## CHANGELOG

A `CHANGELOG.md` is the human-readable companion to the version numbers: a short, dated list of what
changed in each release, grouped as Added / Changed / Fixed. The version number tells a tool what
*kind* of change happened; the changelog tells a person what actually changed.

## When a heavier branching model finally earns its keep

[10_from_scripts_to_pipelines.md](../implementing/10_from_scripts_to_pipelines.md) steered you away
from a permanent `dev` or release-branch model, because for an internal pipeline it is pure overhead.
This is the point where that can change. If you begin cutting **public releases** that must
be stabilized while development keeps going, a release-branch model is helpful.

## Avoiding the `__init__.py` trap

A tempting mistake, once you're ready to trim `src/` down to a clean, shippable library: *"If I
delete the old approach, I can't reproduce the paper that used it, so I'll keep it around, just
hidden."* Usually the hiding is done by leaving the module in place but not importing it in
`__init__.py`.

That does not work, and it's worth understanding why. **`__init__.py` controls the *exposed* public
API, not what *installs*.** Every module in `src/` still ships, still gets imported by something
eventually, and still has to be maintained when a dependency changes. This can force work when a CI test fails, even though that failure is related to dead code that no one will ever use. Thus, hiding an old approach behind
`__init__.py` does not remove its cost; it just makes the cost invisible — a permanent maintenance
tax, not a solution.

The actual resolution is what
[15_experiments_and_shipping.md](../implementing/15_experiments_and_shipping.md) already
established: every commit is already a permanent, reproducible point in history, so deleting a
module in a new commit doesn't erase it from any earlier one. Strip the non-preferred approaches —
on `main` or on a branch, whichever you choose — and the removed code is not lost: it lives on in
every commit before the removal. An experiment that needs the old approach checks out that commit,
not whatever `src/` looks like now — tag the commit first only if you'd rather have a memorable name
to check out than a hash to look up.

**The one exception.** If an alternative approach will be *deliberately used going forward* (not just
preserved for the record), then it is a supported option, not dead code. Make it first-class: tested
and documented, perhaps in a clearly named `legacy` subpackage. The rule is against *gated-off
clutter*, not against genuinely supporting more than one method when you mean to.

## Publishing to PyPI

Once a project is packaged ([21_packaging.md](21_packaging.md)), versioned (above), and licensed and
citable ([22_publishing_a_paper.md](22_publishing_a_paper.md) covers LICENSE and CITATION.cff — the
same requirement applies here even if this project never publishes a paper), the actual publishing
step is uploading it to **PyPI**, so anyone can `pip install your-package`.

A build backend (declared in `pyproject.toml`, [21_packaging.md](21_packaging.md)) builds the
distributable files, and a tool like `twine` (or your build backend's own upload command) pushes them
to PyPI. Doing this by hand from a laptop works but is easy to forget or get wrong on release day;
the natural next step is automating it in CI, uploading whenever a version tag is pushed, using
PyPI's trusted publishing so no long-lived API token has to be stored as a secret.

The full mechanics — build backends, `twine`, trusted publishing, test-PyPI as a dry run — are beyond
what this guide covers in depth; see the
[Scientific Python Development Guide's "Simple packaging" page](https://learn.scientific-python.org/development/guides/packaging-simple/)
for the complete walkthrough once you're actually at this point.

## Making a shipped repo approachable

A repo built for your own lab notebook and a repo built to hand to a stranger want different front
doors. The root `README.md` for your lab notebook is not going to have the content someone `pip install`-ing your package from PyPI or GitHub needs: what this package does, how to install it, and a minimal
example that runs. A shipped library's README leads with those, not with the research question.

A small `examples/` folder (or a single `examples/quickstart.py`) — distinct from `experiments/`'s
research-question drivers — is worth adding alongside it: a short, self-contained script showing the
most common use case, using synthetic or bundled sample data so it runs without access to your lab's
real datasets. Where `experiments/<theme>/` answers "does approach A beat approach B?" `examples/quickstart.py`
answers "how do I use this?" — a different question, for a different reader.

The Sphinx doc site ([20_documentation_and_doc_sites.md](../implementing/20_documentation_and_doc_sites.md))
already generates the API reference this reader needs; once shipping, it's worth the modest extra
effort of a short "Getting started" narrative page alongside the autodoc pages, walking through the
same example the README's quickstart shows — reusing the code, not just the concept, so the two never
drift apart.

## A shipped repo vs. the lab notebook

The same structural fact from
[22_publishing_a_paper.md](22_publishing_a_paper.md#a-repo-just-for-the-paper-vs-the-lab-notebook)
applies here: GitHub visibility is per-repository, not per-tag, so a shipped library's public release
can't simply hide the private lab notebook it grew out of. If the notebook holds anything you
wouldn't want a new user browsing, the fix is the same two-repo pattern — keep the working repo
private, and create a fresh, public repo containing just the trimmed library, its examples, and its
docs. [repo_ownership_and_visibility.md](../reference/repo_ownership_and_visibility.md) covers the
recipe in full.
