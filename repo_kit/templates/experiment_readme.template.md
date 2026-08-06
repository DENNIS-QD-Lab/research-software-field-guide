<!--
PER-EXPERIMENT README TEMPLATE — copy to experiments/_TEMPLATE.md in the target repo. Starting a new
study then means: copy _TEMPLATE.md to experiments/<YYMMDD-slug>/README.md, fill the sections, and add a
row to experiments/README.md (the research log) so the study shows up in the status table.

Keep the section order and headings — every experiment folder reads the same way, so a reader (or your
future self) always knows where to look: idea (Question / Hypotheses) -> test (Tests) -> outcome
(Findings). Delete this comment block in the copy.
-->

# <Study title> (YYMMDD)

One or two sentences: what this study is about and which part of the analysis it interrogates.

All method code is imported from the `<yourpkg>` library and the shared harness in
`experiments/_common/`; the drivers here only compose those pieces, record results, and render figures,
so the study tests exactly what the library provides.

If this study has a rendered report, link it here (e.g. `docs/experiments/<name>.md`).

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

- **H# (dataset, seed/params, date):** what was observed, in numbers, and what it implies.

## Reproduce

From the repo root, in the project environment:

    python experiments/<YYMMDD-slug>/run_<name>.py

Seeded/synthetic data reproduces exactly; real-data inputs are referenced by their stable identifier and
checksum (see the research log and `experiments_playbook.md`). Figures and metric dumps land in
`outputs/` (git-ignored unless committed as a fixture). To reproduce the exact state behind a paper
figure, check out the corresponding tag (e.g. `paper-v1`) rather than the latest `main`.

A run you keep is *finalized* on committed code: commit the driver and any `src/` change, re-run so the
manifest records a clean commit (`dirty: false`), confirm the metrics reproduce, then commit the
refreshed run. See `experiments_playbook.md` → *Finalizing an experiment*.

## Status & decisions

What is settled, what is still open, what has been tagged, and any decision to stop pursuing a
hypothesis (with the reason). Drivers are kept even when the *result* is unflattering — that is evidence
for a design decision. A driver is rewritten only when the *code* is wrong (bad math, wrong range,
mis-scaled units), not when the result is merely disappointing. Once the design evidence is complete,
the chosen approach is tagged and a pruned copy carried forward.
