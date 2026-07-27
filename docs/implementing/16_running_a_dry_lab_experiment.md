# Running a dry-lab experiment

`15_experiments_and_shipping.md` gave you the *structure*: a `src/` library and a dated
`experiments/` folder. This doc is about the *practice* — how you actually run a computational
("dry-lab") experiment and record it so the result holds up later.

A dry-lab experiment has the same arc as a bench experiment: you have a **question**, you **design**
a way to answer it, you **run** it, you **record** what happened, you **interpret** the result, and
often you **repeat** it. The repo is your lab notebook. The discipline that makes it a *notebook* and
not a pile of scripts is this: any run can be reproduced, and the whole line of inquiry can be
followed, **without reading the git history**. Someone (including future-you) should be able to open
the folder and see what you asked, what you found, and what to do next.

Everything below is illustrated by the lab's exemplar, `SWIR_HDR_v2`, which is set up exactly this
way.

## The research log: one place that holds the state

At the top of `experiments/` lives a single human-facing **research log** (`experiments/README.md`).
It is the index over everything else, and it holds four things:

- **The goal** — the question the whole project is trying to answer, in a few sentences.
- **Status of the open questions / hypotheses** — a table: each question, whether it is open, in
  progress, or answered, and the one-line current answer.
- **What's next** — the current focus, so you always know the next move.
- **A dated decision log** — newest first: what you decided and *why* ("switched to the joint solve
  because…", "stopped pursuing the weighting comparison because…"). This is the record you read
  *instead of* `git log`.

The log is state: it changes almost every session. Keeping it in one committed file means the
project's status is never trapped in your head, a chat transcript, or a commit message nobody will
find.

## The experiment folder: idea → test → outcome

Each distinct study gets its own dated, self-contained folder (`experiments/2026-07-crf-necessity/`)
built from a **template** so every experiment reads the same way. The exemplar's template
(`experiments/_TEMPLATE.md`) has a fixed set of headings:

- **Question / motivation** — why this experiment exists.
- **Hypotheses** — the falsifiable claims, each with the read-out that would settle it.
- **Tests** — a small table: hypothesis → what is run → metric → which driver script.
- **Findings** — filled in as evidence accrues, and *dated*. A null result or a method that loses is
  a finding, not a failure — keep it.
- **Reproduce** — the exact command, and which tag/state to check out.
- **Status & decisions** — what is settled, what is still open.

Copy the template to start a new experiment, and add a row to the research log so it shows up in the
status table. That is the whole ritual.

## Save the state of every run

A result you cannot reproduce is an anecdote, not a measurement. Reproducibility does not happen by
remembering — it happens because each run **records the state that produced it**. When a driver runs,
have it write a small **manifest** next to its outputs:

```yaml
# outputs/2026-07-15_crf-necessity/manifest.yaml
git_commit: 4f7675a
git_dirty: false            # were there uncommitted changes? (honest, not aspirational)
timestamp: 2026-07-15T14:02:11
inputs:
  dataset: mouse_qd_2026-06-30   # which data (see 17_working_with_large_data.md)
  dataset_sha256: 9c1f…          # so you can prove two runs used the same input
parameters:
  saturation_fraction: 0.85
  seed: 0
```

The commit hash says *which code*, the dirty flag is honest about whether that code was actually
committed, the parameters say *how* it was configured, and the inputs say *what it ran on*. With
those four, "reproduce the run behind Figure 3" is a real instruction, not a hope. Seeding any
randomness (`10_from_scripts_to_pipelines.md`, `12_testing_with_pytest.md`) is what lets a rerun
return the *same* numbers rather than merely similar ones.

## Repeat runs, and track quality, without bloating the repo

You will run an experiment many times. If every run committed its figures and arrays, the repo would
balloon and its history would be permanently heavy. The rule that keeps the record complete *and*
the repo small:

- **Commit the small, non-regenerable provenance:** the `manifest.yaml`, a `metrics.csv` (the numbers
  that let you compare runs — RMSE, counts, whatever tracks quality), and a short `run_report.md`.
- **Git-ignore the heavy, regenerable artifacts:** figures (`*.png`), large arrays (`*.npy`), and any
  scratch data. A deterministic, seeded run *reproduces* these from the committed code and manifest,
  so you are keeping the recipe, not the cake.

Give each run its own output directory and **preserve runs by default** — a new run writes a new
dated folder rather than overwriting the last one, so you can watch a metric move across runs and
catch a regression. (In the exemplar this is handled by a tiny `runlog.py` helper, but the idea is
independent of any code: one directory per run, small provenance committed, heavy artifacts ignored.)
The small carve-out for committing a figure — when it *cannot* be regenerated in CI because it needs
real data — is covered in `17_working_with_large_data.md`.

## Interpretation stays with the scientist

Automate the recording, never the conclusion. In the exemplar, the run report has an
`## Interpretation (scientist)` section that tooling is written to **never overwrite** — the machine
fills in the provenance and the metrics, and the human writes what the result *means*. That boundary
is the whole point: the framework exists to make your judgment reproducible and reviewable, not to
replace it. (This division of labor is exactly the subject of `18_ai_assisted_development.md`, and it
matters most when an assistant wrote the driver.)

## How this connects

- **`15_experiments_and_shipping.md`** — where these folders live and how a concluded experiment's
  code graduates into the shipped library.
- **`12_testing_with_pytest.md`** — a validation experiment that concludes cleanly becomes a
  regression test, so the result you just established stays true as the code changes.
- **`17_working_with_large_data.md`** — how the `inputs:` block above points at real data too big to
  commit, and how to pin *which* data a run used.
- **`18_ai_assisted_development.md`** — when an assistant writes the driver, this provenance and this
  interpretation boundary are what keep the science honest.
