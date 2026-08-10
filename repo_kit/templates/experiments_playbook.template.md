<!--
EXPERIMENTS PLAYBOOK TEMPLATE — copy to .claude/experiments_playbook.md in the target repo and fill the
<placeholders>. This is the "durable procedure" leg of the three-file split: how this repo runs and
records experiments. Keep findings, decisions, and status OUT of here — those live in the research log
(experiments/README.md). That split is what keeps this file short. Delete this comment block in the copy.
-->

# Experiments playbook — <PROJECT>

**Read [`../experiments/README.md`](../experiments/README.md) first** for current state: the goal, each
question's status, and what to do next.

> **This file is durable procedure only** — how we *run and record* experiments here, not what we've
> found. Findings, decisions, and next steps go in the research log, never here.

Coding standards (style, docstrings, type hints, data handling) are in [`CLAUDE.md`](../CLAUDE.md).

---

## Where things live

- **Method code** → `src/<yourpkg>/` (the installable library). This is what the disseminated method
  ships as.
- **Experiments** → `experiments/<slug>/` — undated, permanent, question-driven; revisited for as long as
  that line of inquiry stays open (pipeline work loops — Stage 0, then Stage 1, back to Stage 0, add
  Stage 2 — so the theme folder is a standing address, not a snapshot of when it started). A driver
  script per question plus an optional exploration notebook; dates live on the *runs* inside, not the
  folder.
- **Shared harness** → `experiments/_common/` — the scaffolding drivers compose (run logging, comparison
  and plotting helpers, report embedding). **Harness only — never method code.**
- **Rendered reports** → `docs/experiment_summaries/*.md` (Sphinx, optionally executable via myst-nb),
  nested under each theme's page in `docs/experiment_overviews/<theme>_overview.md` in the built site.

## Harness discipline

- Drivers **only compose** `<yourpkg>` (the library) + `experiments/_common/`. They must **not fork
  method code** into the driver — so an experiment always tests exactly what the library provides. If a
  method needs to change, change it in `src/` (or `_common/` for harness-only scaffolding), not in a
  driver.
- **Two-phase `src/` model.** During research, all competing approaches **coexist** in `src/` so
  experiments import them and never drift. Prune to the single disseminated approach **only at
  publication**, after tagging the paper state and archiving it — not before.

## Runlog protocol

Every run writes to two places, name-matched by the same `<YYMMDD_slug>[_NN]` id:

- **`experiments/<slug>/<YYMMDD_slug>[_NN].md`** — the report, sitting directly in the theme folder so
  it's visible without opening a subfolder: a scan-first page with a one-line `## Summary` and the
  **`## Interpretation (scientist)`** (between protected markers, **never overwritten** by tooling — the
  scientist owns it) at the *top*, then provenance, metrics, and figures, so the opening lines read "we
  did X, we found Y."
- **`experiments/<slug>/details/<YYMMDD_slug>[_NN]/`** — the provenance behind that report, rarely
  opened directly: `manifest.yaml` (git commit + `dirty` flag — dirty means the *tracked code* had
  uncommitted changes at run time; the run's own `details/` and report are excluded from that check, so
  writing them never trips it — timestamp, parameters, inputs/checksum) and `metrics.csv` (the numeric
  read-out figures/tables in the report draw from).

Default is **PRESERVE** — a new run gets a fresh `_NN` suffix, kept in sync between the report and its
`details/` counterpart, and never clobbers a prior run. Use `--overwrite` only for throwaway cosmetic
re-runs of a deterministic result. Keep the split **additive** if a runlog helper already exists and
other drivers depend on today's co-located shape: a new optional parameter (e.g. `report_dir=`),
defaulting to the old behavior, lets one driver adopt the split without moving every other driver's runs
at the same time.

## Exploratory notebooks

A notebook exploring an idea has the same reproducibility problem a driver script solves with
`runlog` — except nothing forces you to notice an observation matters *before* you change something and
rerun. Two cheap habits close most of that gap:

- **A top-cell "What / why" and "Observed" note**, written *before* you touch anything else — the
  notebook analog of `runlog`'s protected `## Interpretation` section. The point is to make the habit
  unconditional: you cannot reliably judge in the moment which run will matter later, so the note has to
  happen every time, not just when you think it's worth it.
- **Duplicate the notebook (`_01` → `_02`) once you've written a note you'd be annoyed to lose** —
  preserves *what code produced what*, the same way `runlog`'s PRESERVE-by-default protects a driver run.
  The note is the trigger, not a pre-planned sweep; this doesn't fully solve the "I didn't know it'd
  matter" problem, and that's an honest limit rather than something to over-engineer around.

Since exploratory notebooks don't call `runlog`, they have no `details/` counterpart — a run only gets
one once it's promoted to a driver script that writes a manifest.

## Documentation promotion (`DOCUMENT_EVERYTHING`)

Promotion follows whatever `DOCUMENT_EVERYTHING` is set to in your own environment — unset means nothing
is auto-promoted; `1` promotes every run (gets it a page in the built doc site and, once exported, a PDF
in the shared archive). Override per run with `promote=True`/`False` in `start_run`. Full mechanics:
`docs/reference/documentation_promotion.md` in the research-software-field-guide; this repo follows that
convention as written, with the archive folder pointed at your own `local_paths.py`-style setting.

## Finalizing an experiment — clean-commit reproducibility

A run is only reproducible if someone can `git checkout` its recorded commit and regenerate it. The
`dirty` flag in `manifest.yaml` is the signal: it is true when the tracked code had uncommitted changes
when the run executed. Exploring is dirty by nature — edit, run, look, repeat — and those runs honestly
stamp `dirty: true`. Every run is still preserved (a losing experiment is evidence, not waste); dirtiness
is about *code provenance*, not whether a result is worth keeping.

When an experiment is a keeper, **finalize** it so its stamp points at real, checkout-able code:

1. **Commit the code** that produced it — the driver, any `src/` change, the experiment README.
2. **Re-run the driver** on the now-clean tree. The refreshed manifest records `dirty: false` and the
   real commit SHA.
3. **Confirm it reproduces.** For a seeded/synthetic run the refreshed `metrics.csv` must match the
   previous one exactly; a mismatch means the committed code is not what produced the logged numbers —
   a real finding, not a nuisance. (Real-data runs match to their documented tolerance.)
4. **Commit the refreshed run** (manifest/metrics/report), and `git tag` it if it backs a paper figure.

Your AI assistant can drive steps 2–4 — re-run the driver, diff the metrics, and hand back the commit
(and tag) for you to run; you commit the code in step 1 and review what it prepares. A reproduce
helper must diff *every* metrics file a run writes, not just `metrics.csv` — drivers often emit
several under custom names, and checking only one gives a false pass.

## Retention policy

- Keep a driver even when the **result** is unflattering (a method that loses is evidence for a design
  decision, not a bug).
- Rewrite a driver only when the **code** is wrong: bad math, wrong range, mis-scaled units.
- Once a study's design evidence is complete, tag the paper state and carry a pruned copy forward.

## Reports & CI

- Reports embed a **preserved runlog run** rather than recomputing; expensive cells embed precomputed
  outputs.
- **Deterministic (synthetic) runs regenerate in CI** before the docs build, so embedded figures exist
  on a fresh checkout.
- **Real-data runs cannot regenerate in CI** — commit their (small) figures + manifest/metrics as
  fixtures via `.gitignore` negation exceptions, within the fixture size allowance.
- View a built site with `sphinx-autobuild docs docs/_build/html --host 127.0.0.1 --port 8000` (a bare
  file path pasted into a browser is treated as a search; use the server or a `file:///` URL).

## Commit discipline

- **The scientist commits.** Prepare changes and a commit-message draft, but ask before committing,
  pushing, or opening a PR.
- `pre-commit` runs ruff (check + format) on `.py` and nbstripout on notebooks; `.ipynb` are excluded
  from ruff. Notebooks are committed with outputs stripped — assume a reviewer re-runs them.
- Data stays out of git except the committed fixtures carved out in `.gitignore`.
