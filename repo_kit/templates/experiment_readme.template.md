<!--
PER-EXPERIMENT README TEMPLATE — copy to experiments/_TEMPLATE.md in the target repo. Starting a new
study then means: copy _TEMPLATE.md to experiments/<slug>/README.md (no date — this folder is a standing
address for the line of inquiry, revisited for as long as it stays open; dates live on the runs inside
it), fill the sections, and add a row to experiments/README.md (the research log) so the study shows up
in the status table.

Keep the section order and headings — every experiment folder reads the same way, so a reader (or your
future self) always knows where to look: idea (Question / Hypotheses) -> test (Tests) -> outcome
(Findings). Delete this comment block in the copy.
-->

# <Study title>

One or two sentences: what this study is about and which part of the analysis it interrogates.

All method code is imported from the `<yourpkg>` library and the shared harness in
`experiments/_common/`; the drivers here only compose those pieces, record results, and render figures,
so the study tests exactly what the library provides. This file is the study's only narrative
document — it's what's rendered on the doc site (`docs/experiment_overviews/<theme>_overview.md`
includes it directly) — updated in place as findings accrue, never regenerated per run.

## Question / motivation

Why this study exists — the open question it addresses, and what a clear answer would let you do
differently.

## Hypotheses

- **H# — short name.** The falsifiable claim, stated so a result can confirm or refute it. Note the
  metric or read-out that would settle it. Add "why it might be true / why it might not" if the tension
  is worth recording.

## Tests

| Hypothesis | Test | Metric / read-out | Driver |
|---|---|---|---|
| H# | what is run, on what data | what decides it | `run_<name>.py` |

Note any parameters, data ranges, or which metric is trustworthy on which dataset. Design a **validation
check** in from the start — a known-good case, synthetic data with a known answer, or an independent
method — so the result can be believed, not just produced.

## Findings

*(Filled in as evidence accrues. A poorly-fitting or null result is a finding, not a defect — see the
retention note below. Date each finding.)*

- **H# (dataset, seed/params, date):** what was observed, in numbers.

  ![](details/<YYMMDD_slug>/<figure>.png)
  *Run `<YYMMDD_slug>` — reproduce with `python experiments/<slug>/run_<name>.py`.*

  > **<initials>:** what it implies — pending.

The embedded figure is the *current* evidence for this finding, not a running log of every attempt —
when a rerun supersedes it, swap the image path and caption in place rather than adding a second entry
beside it. The image path is relative to this README's own location (`details/<run>/...`), which
renders correctly both here and on the doc site — see
[documentation_promotion.md](../../docs/reference/documentation_promotion.md) for why that only works
with the right `{include}` options on the overview page. The italic caption is deliberately not a
heading: it exists so the run can be reproduced, not so it can be linked to or indexed.

## Reproduce

From the repo root, in the project environment:

    python experiments/<slug>/run_<name>.py

Seeded/synthetic data reproduces exactly; real-data inputs are referenced by their stable identifier and
checksum (see the research log and `experiments_playbook.md`). Each run's manifest, metrics, and
figures land in `details/<YYMMDD_slug>[_NN]/` (git-ignored except for the manifest/metrics, unless a
figure is committed as a fixture) — provenance for reproducibility, not a report; the findings above
are. To reproduce the exact state behind a paper figure, check out the corresponding tag (e.g.
`paper-v1`) rather than the latest `main`.

A run you keep is *finalized* on committed code: commit the driver and any `src/` change, re-run so the
manifest records a clean commit (`dirty: false`), confirm the metrics reproduce, then commit the
refreshed run. See `experiments_playbook.md` → *Finalizing an experiment*.

## Status & decisions

What is settled and what is still open, what has been tagged. Any decision to stop pursuing a
hypothesis, and why, is the scientist's call:

> **<initials>:** _status and next decision — pending._

Drivers are kept even when the *result* is unflattering — that is evidence for a design decision. A
driver is rewritten only when the *code* is wrong (bad math, wrong range, mis-scaled units), not when
the result is merely disappointing. Once the design evidence is complete, the chosen approach is tagged
and a pruned copy carried forward.
