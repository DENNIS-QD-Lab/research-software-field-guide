# Documentation promotion: mechanics and how to adapt it

This is the reference for how `DOCUMENT_EVERYTHING` / `promote=` actually work, for anyone who wants
to understand the mechanism precisely or adapt it to a different repo. The basics — what happens by
default, and how to change it — are in
[16_running_a_dry_lab_experiment.md](../implementing/16_running_a_dry_lab_experiment.md#choosing-how-much-gets-documented).

## Two independent switches

"Documentation" here means two separate things that happen to share one default:

1. **Promote to the doc site** — does this run's report get a page in the built Sphinx site.
2. **Archive to PDF** — does a promoted page get exported to the external, git-free archive.

They're controlled separately so you can, for example, promote something to the doc site immediately
but only archive it once it's a keeper.

## Axis 1 — promoting a run to the doc site

`RunLog`/`start_run` takes `promote: bool | None = None`. When `None` (the default), it reads the
`DOCUMENT_EVERYTHING` environment variable (`"1"`/`"true"` = on, anything else or unset = off).
Passing `True` or `False` explicitly overrides the environment variable for that one call.

When a run resolves to `promote=True`, `finalize()` additionally writes a thin stub page under
`docs/experiments/<theme>/<run-id>.md` whose body is a MyST `{include}` directive pointing back at the
real report — so the doc site never holds a second copy of the content, just a pointer.

```{note}
**Confirmed, not just suspected:** MyST/docutils' `{include}` resolves an included file's own
relative links (e.g. a report's `![...](details/<run-id>/channel_grid.png)`) against the
*including* file's directory, not the *included* file's — the general `include`-directive gotcha
does apply here, verified with a throwaway spike against this repo's pinned Sphinx 9.1.0 /
myst-parser 5.1.0. So the stub-generator cannot include a report verbatim; it must rewrite each
image link to be correct from the stub's own location before writing the stub.
```

For a promoted stub page to appear in the built site without hand-editing a toctree every run,
`docs/index.md`'s "Experiments" toctree needs a `:glob:` entry (`experiments/*`) alongside (or in
place of) a hand-maintained list of individual pages — also confirmed by spike: a new page dropped
under `docs/experiments/` appeared in the built nav with no toctree edit, and no duplicate-listing
warning when mixed with existing explicit entries.

## Axis 2 — archiving a promoted page to PDF

A separate script — not run automatically unless `DOCUMENT_EVERYTHING` is on — walks every promoted
stub page and, for each, computes the PDF's destination path in the external archive folder (a
machine-local setting, configured the same way `local_paths.py` configures `DATA_ROOT`). It renders
and copies only if that destination file does **not already exist**.

That's the whole idempotency rule, deliberately simple: because runs are PRESERVE-by-default with
unique, immutable filenames (`<YYMMDD_slug>[_NN]`), "already archived" is just a file-existence check
— no hashing or timestamps needed. The archive is a frozen, append-only record on purpose: once a run
is archived, re-running the export step never touches it again, even if the source report changes
later. Wanting a fresh snapshot is what PRESERVE's numbering is for — rerun, get a new `_NN`, archive
that as a new file, leave the old one alone.

## Adapting this to your own repo

- `DOCUMENT_EVERYTHING` is a plain environment variable — rename it if you like, but keep it a
  per-person setting (env var or gitignored local config), never a tracked constant, since the whole
  point is that two people on the same repo can disagree.
- The archive folder's location is a `local_paths.py`-style setting, not hardcoded — point it at
  whatever shared drive your team actually uses.
- The stub-generator and the export script are both small, separable pieces in
  `experiments/_common/` — read them before changing them, but neither depends on the other beyond
  the shared file-naming convention.
