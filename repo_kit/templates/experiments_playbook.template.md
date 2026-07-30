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
- **Experiments** → `experiments/<YYMMDD-slug>/` — dated (study start date), question-driven; a driver
  script per question plus an optional exploration notebook.
- **Shared harness** → `experiments/_common/` — the scaffolding drivers compose (run logging, comparison
  and plotting helpers, report embedding). **Harness only — never method code.**
- **Rendered reports** → `docs/experiments/*.md` (Sphinx, optionally executable via myst-nb).

## Harness discipline

- Drivers **only compose** `<yourpkg>` (the library) + `experiments/_common/`. They must **not fork
  method code** into the driver — so an experiment always tests exactly what the library provides. If a
  method needs to change, change it in `src/` (or `_common/` for harness-only scaffolding), not in a
  driver.
- **Two-phase `src/` model.** During research, all competing approaches **coexist** in `src/` so
  experiments import them and never drift. Prune to the single disseminated approach **only at
  publication**, after tagging the paper state and archiving it — not before.

## Runlog protocol

Every run writes one directory: `experiments/<YYMMDD-slug>/outputs/<YYMMDD_slug>[_NN]/` containing

- `manifest.yaml` — git commit + dirty flag, timestamp, parameters, inputs (dataset name + checksum).
- `metrics.csv` — the numeric read-out.
- `run_report.md` — a scan-first report: a one-line `## Summary` and the **`## Interpretation
  (scientist)`** (between protected markers, **never overwritten** by tooling — the scientist owns it)
  sit at the *top*, then provenance and metrics, so the opening lines read "we did X, we found Y."

Default is **PRESERVE** — a new run gets a fresh `_NN` suffix and never clobbers a prior run. Use
`--overwrite` only for throwaway cosmetic re-runs of a deterministic result.

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
