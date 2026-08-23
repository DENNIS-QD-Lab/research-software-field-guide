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
- **Experiments** → `experiments/<theme-slug>/` — undated, permanent, question-driven; revisited for as long as
  that line of inquiry stays open (pipeline work loops — Stage 0, then Stage 1, back to Stage 0, add
  Stage 2 — so the theme folder is a standing address, not a snapshot of when it started). A driver
  script per question plus an optional exploration notebook; dates live on the *runs* inside, not the
  folder.
- **Shared harness** → `experiments/_common/` — the scaffolding drivers compose (run logging, comparison
  and plotting helpers). **Harness only — never method code.**
- **Rendered doc site** → `docs/`, built with Sphinx. Each theme's `experiments/<theme-slug>/README.md` is
  included directly as that theme's overview page — one authored page per experiment, not generated
  from individual runs.

## Harness discipline

- Drivers **only compose** `<yourpkg>` (the library) + `experiments/_common/`. They must **not fork
  method code** into the driver — so an experiment always tests exactly what the library provides. If a
  method needs to change, change it in `src/` (or `_common/` for harness-only scaffolding), not in a
  driver.
- **Two-phase `src/` model.** During research, all competing approaches **coexist** in `src/` so
  experiments import them and never drift. Prune to the single disseminated approach whenever that
  earns its keep. Pruning does not need a tag first: the commit before the trim stays permanently
  reachable by its hash, so a run that used the old approach can still be checked out and reproduced.

## Runlog protocol

Every run writes its provenance to **`experiments/<theme-slug>/details/<YYMMDD>_<slug>[_NN]/`**, rarely opened
directly: `manifest.yaml` (git commit + `dirty` flag — dirty means the *tracked code* had uncommitted
changes at run time; the run's own `details/` are excluded from that check, so writing them never trips
it — timestamp, parameters, inputs/checksum) and `metrics.csv` (the numeric read-out). This is
provenance only, not a report: it exists so a run can be reproduced, not to be read as a narrative.

Default is **PRESERVE** — a new run gets a fresh `_NN` suffix and never clobbers a prior run. Use
`--overwrite` only for throwaway cosmetic re-runs of a deterministic result.

The narrative — question, hypotheses, findings, figures, interpretation — lives once in
**`experiments/<theme-slug>/README.md`**, not regenerated per run. When a run's figure is worth keeping
visible, embed it directly in the README from `details/<run_id>/`, with a short italic caption noting
the run id for reproducibility, and swap it in place when a later run supersedes it — don't accumulate
a second entry beside the first. The signed-blockquote convention (`> **<initials>:** ...`, verbatim,
with a `_pending_` placeholder when there's no answer yet) carries the *why* wherever it belongs:
a README finding, or an entry in the research log's decision log.

## Exploratory notebooks

A notebook exploring an idea has the same reproducibility problem a driver script solves with
`runlog` — except nothing forces you to notice an observation matters *before* you change something and
rerun. Two cheap habits close most of that gap:

- **A top-cell "What / why" and "Observed" note**, written *before* you touch anything else — the
  notebook analog of the signed blockquote a README finding gets. The point is to make the habit
  unconditional: you cannot reliably judge in the moment which run will matter later, so the note has to
  happen every time, not just when you think it's worth it.
- **Duplicate the notebook (`_01` → `_02`) once you've written a note you'd be annoyed to lose** —
  preserves *what code produced what*, the same way `runlog`'s PRESERVE-by-default protects a driver run.
  The note is the trigger, not a pre-planned sweep. No tooling can make a scientist record something
  they do not yet know will matter, so these habits narrow that gap rather than closing it.

Since exploratory notebooks don't call `runlog`, they have no `details/` counterpart — a run only gets
one once it's promoted to a driver script that writes a manifest.

## Getting a finding onto the doc site

There is no promotion step or environment variable: a theme's `README.md` is included directly as its
doc-site page (`docs/experiment_overviews/<theme-slug>_overview.md`), so a finding is on the site as soon as
it's written into the README, with its figure embedded from `details/<run_id>/`. Full mechanics
(including the `{include}` options that make embedded images resolve correctly) are in
`docs/reference/documentation_promotion.md` in the research-software-field-guide; this repo follows
that convention as written.

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
4. **Commit the refreshed run** (manifest/metrics/figure), and `git tag` it if it backs a paper figure.

Your AI assistant can drive steps 2–4 — re-run the driver, diff the metrics, and hand back the commit
(and tag) for you to run; you commit the code in step 1 and review what it prepares. If you add a helper that re-runs and compares, have it diff *every*
metrics file a run writes, not just `metrics.csv` — drivers often emit several under custom names, and
checking only one gives a false pass.

## Retention policy

- Keep a driver even when the **result** is unflattering (a method that loses is evidence for a design
  decision, not a bug).
- Rewrite a driver only when the **code** is wrong: bad math, wrong range, mis-scaled units.
- Once a study's design evidence is complete, prune to the approach you are carrying forward. Tag the
  pre-prune commit first only if you want a memorable name for it; it stays reachable either way.

## Doc site & CI

- A README's embedded figures point at a **preserved runlog run's** `details/<run_id>/` rather than
  anything recomputed at build time.
- **Any figure a README embeds is committed**, deterministic or not. It has to be in the repo for
  GitHub and the doc site to render it, so commit that one file with `git add -f` — it matches the
  ignored `*.png` pattern. Everything else a run wrote stays ignored and regenerable.
- View a built site with `sphinx-autobuild docs docs/_build/html --host 127.0.0.1 --port 8000` (a bare
  file path pasted into a browser is treated as a search; use the server or a `file:///` URL).

## Commit discipline

- **The scientist commits.** Prepare changes and a commit-message draft, but ask before committing,
  pushing, or opening a PR.
- `pre-commit` runs ruff (check + format) on `.py` and nbstripout on notebooks; `.ipynb` are excluded
  from ruff. Notebooks are committed with outputs stripped — assume a reviewer re-runs them.
- Data stays out of git except the committed fixtures carved out in `.gitignore`.
