<!--
PER-THEME README TEMPLATE — copy to experiments/<theme-slug>/README.md (no date — this folder is
a standing address for one line of inquiry, revisited for as long as it stays open; dates live on
the runs inside it, in details/<YYMMDD>_<slug>[_NN]/). Add a row to experiments/README.md (the
research log) so the new theme shows up there.

This README is a chronological log, not a fixed Question/Hypotheses/Tests/Findings form — real
research doesn't arrive in that order, and forcing it into categories after the fact divides a
scientist's actual train of thought. Write dated sections in the order things actually happened;
what one section finds is allowed to change what the next one asks. A loose "objective / what I
did / what I learned" habit — not literal headings — is a reasonable way to think about what
belongs in an entry.

Put your own words in directly, as a signed blockquote (`> **<initials>:** ...`), quoted verbatim
wherever you're drawing on an actual discussion (a chat, a meeting, your own notes) rather than
paraphrased into someone else's summary — that's where the interpretation and judgment calls live,
and it's worth more of the file than the mechanical narration is. If you haven't decided something
yet, write a `_pending_` placeholder rather than leaving a gap or letting an assistant guess on
your behalf.

Delete this comment block once the first real entry is written.
-->

# <Theme title>

One or two sentences: what this theme is about and which part of the analysis it interrogates.

All method code is imported from `<yourpkg>` and the shared harness in `experiments/_common/`; the
drivers here only compose those pieces, record results, and render figures, so the theme tests
exactly what the library provides. This file is the theme's only narrative document — it's what's
rendered on the doc site (`docs/experiment_overviews/<theme-slug>_overview.md` includes it
directly) — updated in place as the log grows, never regenerated per run.

> **<initials>:** _bottom line, pending — one sentence on where this theme actually stands, so a
> reader doesn't have to read the whole log to find out._

## <YYMMDD> — <what this entry covers>

Why this line of inquiry started, what was tried, on what data, and what came of it — in plain
prose, dated, in the order it happened. A poorly-fitting or null result belongs here too; it's a
finding, not a defect. Cite a run by id and reproduce command when its result matters, and embed
its figure directly when it's worth keeping visible:

![](details/<YYMMDD>_<slug>/<figure>.png)
*Run `<YYMMDD>_<slug>` — reproduce with `python experiments/<theme-slug>/run_<name>.py`.*

The image path is relative to this README's own location, which renders correctly both here and
on the doc site — see `readme_to_doc_site.md` in the research-software-field-guide for why that
only works with the right `{include}` options on the overview page. When a rerun supersedes this
figure, swap the image path and caption in place rather than adding a second entry beside it; the
superseded run's own `details/` folder is untouched if you need to check against it.

> **<initials>:** _what it means, in your own words — pending._

## <YYMMDD> — <next entry, continuing from what the last one found>

Design a **validation check** into any new test from the start — a known-good case, synthetic
data with a known answer, or an independent method — so a result can be believed, not just
produced.

> **<initials>:** _pending._

## Reproduce

From the repo root, in the project environment:

    python experiments/<theme-slug>/run_<name>.py

Seeded/synthetic data reproduces exactly; real-data inputs are referenced by their stable
identifier and checksum (see the research log and `experiments_playbook.md`). Each run's
manifest, metrics, and figures land in `details/<YYMMDD>_<slug>[_NN]/` (git-ignored except for the
manifest/metrics, unless a figure is committed as a fixture) — provenance for reproducibility, not
a report; the log above is. To reproduce the exact state behind a paper figure, check out the
corresponding tag (e.g. `paper-v1`) rather than the latest `main`.

A run you keep is *finalized* on committed code: commit the driver and any `src/` change, re-run so
the manifest records a clean commit (`dirty: false`), confirm the metrics reproduce, then commit
the refreshed run. See `experiments_playbook.md` → *Finalizing an experiment*.

## Open items

What's still unresolved — a short tracker, not narrative. Move an item out once it's resolved
(strike it through with a one-line note, or delete it) rather than letting it silently go stale.
Any decision to stop pursuing a line of inquiry, and why, is the scientist's call, recorded here or
in the log entry it belongs to.
