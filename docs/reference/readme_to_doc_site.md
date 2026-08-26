# Getting a theme's findings onto the doc site

This is the reference for how an experiment theme's `README.md` ends up as a page in the built Sphinx
site, and how to keep its embedded figures resolving correctly. The practice-level view — why the
README is the one narrative document, and how to decide what's worth writing into it — is in
[16_running_a_dry_lab_experiment.md](../implementing/16_running_a_dry_lab_experiment.md#repeat-runs-and-track-quality-without-bloating-the-repo).

## One page per theme, no separate promotion step

A theme's `experiments/<slug>/README.md` *is* its doc-site page. `docs/experiment_overviews/<slug>_overview.md`
does nothing but include it:

````{code-block} markdown
:caption: docs/experiment_overviews/noise-reduction_overview.md
```{include} ../../experiments/noise-reduction/README.md
:relative-docs: ../../experiments/noise-reduction/
:relative-images:
```
````

There is no separate "promote this run" step, no per-run stub page, and no environment variable
gating whether a page exists. If the README has a Findings section with an embedded figure, that
figure is on the site the next time it's built — the only editorial decision is what you write into
the README in the first place (see the practice-level doc linked above).

It's tempting to auto-generate a separate stub page under `docs/experiment_summaries/` for every
promoted run instead, picked up by a `:glob:` toctree. Resist that: a parameter sweep of, say, 8
conditions turns into 8 separate nav entries, most of which nobody ever opens, for one genuinely useful
page's worth of content. Reach for that pattern only if your project genuinely benefits from a full,
per-run presentation in the lab notebook — the single `{include}` above is the default for good reason.

A `figures/` folder ([22_publishing_a_paper.md](../disseminating/22_publishing_a_paper.md)) uses
this identical mechanism, but with one page for the whole outline rather than one per theme:
`docs/figure_overviews/figures_overview.md` includes the single root `figures/README.md`. Everything
below — the relative-path fix, the PDF-export option, the standalone-report exception — applies to
that root README exactly as written, with `figures/` in place of `experiments/<slug>/`.
[example_repo_structure.md](example_repo_structure.md) shows a worked example.

## The `{include}` relative-path gotcha, and its fix

MyST's `{include}` directive resolves an included file's own relative links against the *including*
file's directory by default, not the included file's own — so a README's `![...](details/<run_id>/fig.png)`,
correct from the README's own location, silently resolves to the wrong path once pulled through
`{include}` from a file living somewhere else (e.g. `docs/experiment_overviews/`).

The fix is the `:relative-docs:` / `:relative-images:` options shown above, not rewriting the paths by
hand:

- `:relative-docs: ../../experiments/<slug>/` tells MyST which directory the included file's own
  relative *links* (to other docs) should resolve against.
- `:relative-images:` does the same for image paths specifically.

Under the Sphinx and myst-parser versions this guide pins (see `environment.yml`), setting
both options is enough: a README written with plain paths relative to its own directory renders
correctly both through the Sphinx include *and* when viewed directly on GitHub or in an editor. Writing
the `../../experiments/<slug>/details/...` path directly into the README instead avoids the Sphinx-side
bug but breaks the second case — the path resolves outside the repository when the README is read from
its own location. Use the include options; don't hand-rewrite the paths.

If your repo pins different Sphinx/myst-parser versions, verify this directly before relying on it: put
a real image behind a relative link in a theme README, include it with the options above, and check the
built page's `<img src>` actually resolves.

## Sharing a page outside the repo (PDF export)

Some teams want an occasional PDF of a theme's current state — for a lab meeting, or a collaborator who
won't clone the repo. This is a separate, on-demand need from day-to-day documentation and doesn't
require any change to how runs are logged or how the doc site is built:

- Build the site (`sphinx-build docs docs/_build/html`) and print the theme's page to PDF from a
  browser, or
- Use Sphinx's LaTeX/PDF builder on the single page if your repo has that set up.

Point the destination at your team's shared archive location the same way `local_paths.py` configures
any other machine-local path. There's no "archive every run automatically" mode to configure — export
when you actually need to share something.

## An optional exception: a standalone deep-dive report

Occasionally a single read-out is genuinely too complex for a README's figure-and-caption pattern — a
manuscript-figure-quality walkthrough with several panels, each needing its own explanation, meant to
be a citable, occasionally-updated centerpiece rather than one Findings entry among several. For that
rare case, a hand-authored page under `docs/experiment_summaries/<name>.md` (optionally executable via
myst-nb, dynamically locating its run rather than hardcoding a run id — see your repo's
`experiments/_common/` for a worked example if one exists) is a reasonable, deliberate exception.
Link to it from the theme's README rather than letting it replace the README's own Findings section,
and keep it rare: if every finding gets one of these, the clutter this doc describes is back.
