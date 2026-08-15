<!--
RESEARCH LOG TEMPLATE — copy to experiments/README.md in the target repo and fill the <placeholders>.
This is the "state" leg of the three-file split: the top-level record of the research. It changes almost
every session. Keep procedure (how to run experiments) out of here — that lives in
.claude/experiments_playbook.md. Delete this comment block in the copy.
-->

# <PROJECT> — research log

This is the top-level record of the research: the overarching goal, the status of every open question,
what to do next, and a dated log of decisions. **Read this first** — you should be able to answer *what
is the goal*, *what is settled*, and *what is next* without opening anything else.

- **State** (goal, question status, findings, decisions) lives here and in the per-experiment READMEs.
  This file is the index over those folders.
- **How to run and record an experiment** (runlog protocol, harness rules, tagging) lives in
  [`.claude/experiments_playbook.md`](../.claude/experiments_playbook.md) — durable procedure, not state.
- **Coding standards** live in [`CLAUDE.md`](../CLAUDE.md).
- **Rendered reports** (narrative + code + figures) live in the doc site under
  `docs/experiment_summaries/`, nested under each theme's page in `docs/experiment_overviews/` (build with
  `sphinx-build docs docs/_build/html`, or serve with `sphinx-autobuild`).

---

## Goal

<A few sentences: the question the whole project is trying to answer, and why it matters. If there is a
single gate that decides success — "is the gain over the baseline big enough to publish?" — state it.>

---

## Open questions / hypothesis status

Statuses: ✅ answered · 🟡 partial · 🔲 open · ⛔ not pursued.

| ID | Question | Status | Current answer (one line) |
|----|----------|--------|---------------------------|
| **Q1** | <the falsifiable question> | 🔲 | <one line, or "open"> |
| **Q2** | <…> | 🔲 | <…> |

<Optional: if the questions group into themes, add a themes table pointing at each experiment folder and
its report(s). Planned themes can be listed with no folder yet — the roadmap lives here. Start one by
copying `_TEMPLATE.md` to `<slug>/README.md` and adding its questions to the table above. The theme
folder is undated and permanent — you keep adding to it for as long as that line of inquiry stays open;
only the runs inside it are dated.>

---

## Current focus / what's next

1. <the next move, concretely — which experiment to run or write up>
2. <then …>

---

## Decision & milestone log

Newest first. This is the historical record to read *instead of* `git log` — the *why* behind the
current state, in the scientist's own words, inserted verbatim rather than paraphrased:

> **<initials>, <YYYY-MM-DD>:** <what was decided or reached, and why — e.g. "Dropped approach B: it did
> not change the result on the realistic range; keeping A.">

Sign with initials, not a generic "Scientist" label — nothing reads or depends on the label text, so
this stays unambiguous once a repo has more than one contributor.

---

## How this folder works

- **`_TEMPLATE.md`** — copy it to start a new experiment folder (idea → test → outcome headings).
- **`_common/`** — the shared harness the drivers reuse (run logging, comparison/plot helpers).
  Harness only — no method code; drivers import methods from `src/`.
- **`<slug>/README.md`** — the one page for the experiment: motivation, hypotheses, findings with
  their figures embedded inline, and one interpretation per finding. This is what's rendered on the
  Sphinx doc site. Written once and updated as findings accrue — not regenerated per run.
- **`<slug>/details/<YYMMDD_slug>[_NN]/`** — the provenance behind a run: `manifest.yaml` (git commit
  + dirty flag, params, inputs), `metrics.csv`, and any figures. Present for reproducibility, not meant
  to be read as a report — the README is. Preserved by default; heavy artifacts (figures, arrays) are
  git-ignored unless committed as a small report fixture.
- **Tags** — a paper's exact state is tagged (e.g. `paper-v1`). Reproduce a figure by checking out its
  tag, not the latest `main`.
- **Procedure details** (retention policy, what may be committed, CI regeneration) are in
  [`.claude/experiments_playbook.md`](../.claude/experiments_playbook.md).
