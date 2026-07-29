# Running a dry-lab experiment

[15_experiments_and_shipping.md](15_experiments_and_shipping.md) gave you the *structure*: a `src/` library and a dated
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
- **A dated decision log** — newest first: what you decided and *why* ("switched to method B
  because it removed the artifact", "stopped pursuing the third approach because it did not change
  the result"). This is the experimental record you read to understand the scientific progress, which is often intellectually distinct from the code history in the `git log`.

The experimental log is state: it is updated almost every session. Keeping it in one committed file means the
project's status is always clear and can be understood by consulting this one document.

## The experiment folder: idea → test → outcome

Each distinct study gets its own dated, self-contained folder (`experiments/260717-crf-necessity/` —
a `YYMMDD` date prefix so folders sort chronologically)
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

## Validation: designing an experiment you can trust

An experiment can only be satisfactorily concluded if its result can actually be believed. A **validation experiment** is one designed so its answer can be checked against something you already trust — a comparison to ground truth, to an independent method, or to a synthetic dataset with a known answer. That check is what confirms the analysis does what you *intend*, as opposed to merely running without error (the verification-versus-validation distinction in [18_ai_assisted_development.md](18_ai_assisted_development.md)).

Build the check in when you design the experiment, not after:

- **A known answer.** Run on an input whose correct output you already know, from theory or a hand calculation.
- **Synthetic data.** Generate inputs with the answer built in, so any deviation from it is visible and quantifiable.
- **An independent method.** Compare against a second, unrelated route to the same quantity.

A validation experiment that concludes cleanly does double duty: it answers today's question, and — once you trust it — freezing it as a regression test ([12_testing_with_pytest.md](12_testing_with_pytest.md)) is what keeps that result true as the code keeps changing.

## Look at the data at every step

In the exploratory phase you often do not yet have a test for every step — so *looking* is the method.
Manually examining the data as it moves through the pipeline builds intuition for both the data and the
analysis, and catches problems early, while they are cheap to fix. Design your code to generate *and
present* its intermediate outputs often, not only the final number. Plot the intermediate arrays, their
distributions, or the residuals — whatever shows the *shape* of the data at that step — and check how each
step changes them. (For image work, for instance, look at the image **and** a histogram of its intensities
together, so that when a step excludes data — say, a threshold — you see what it does to both.) This is the
exploratory companion to the validation checks in [18_ai_assisted_development.md](18_ai_assisted_development.md) ("a clean run is not a correct
analysis"): the same eyes-on-the-data instinct, applied continuously before you have tests to encode it.

## Save the state of every run

A result you cannot reproduce is an anecdote, not a measurement. Reproducibility does not happen by
remembering — it happens because each run **records the state that produced it**. When a driver runs,
have it write a small **manifest** next to its outputs:

```yaml
# outputs/260717_crf-necessity/manifest.yaml   (one subdirectory per run)
git_commit: 4f7675a
git_dirty: false            # were there uncommitted changes? (honest, not aspirational)
timestamp: 2026-07-17T14:02:11
inputs:
  dataset: run_2026-06-30        # which data (see 17_working_with_large_data.md)
  dataset_sha256: 9c1f…          # so you can prove two runs used the same input
parameters:
  threshold: 0.85
  seed: 0
```

The commit hash says *which code*, the dirty flag is honest about whether that code was actually
committed or if the run used uncommitted changes (which may hinder reproduction), the parameters say *how* it was configured, and the inputs say *what it ran on*. With those four, "reproduce the run behind Figure 3" is a real instruction, not a hope. Seeding any
randomness is what lets a rerun return the *same* numbers rather than merely similar ones — the same
determinism a regression test relies on ([12_testing_with_pytest.md](12_testing_with_pytest.md)).

## Repeat runs, and track quality, without bloating the repo

You will run an experiment many times. If every run committed its figures and arrays, the repo would
balloon and its history would be permanently heavy. The rule that keeps the record complete *and*
the repo small:

- **Commit the small, non-regenerable provenance:** the `manifest.yaml`, a `metrics.csv` (the numbers
  that let you compare runs — RMSE, counts, whatever tracks quality), and a short `run_report.md`.
- **Git-ignore the heavy, regenerable artifacts:** figures (`*.png`), large arrays (`*.npy`), and any
  scratch data. A deterministic, seeded run *reproduces* these from the committed code and manifest,
  so you are keeping the recipe, not the cake.

Keep the two levels straight: the **experiment folder is per *study***, and each **run** writes its own
subdirectory *inside* that folder's `outputs/`, named by date and slug (`outputs/YYMMDD_slug/`). Runs
accumulate in the same experiment folder — you do not make a new experiment folder to re-run. **Preserve
runs by default:** re-running the same study does not overwrite the last result — the first run is
`outputs/YYMMDD_slug/` and each rerun writes the next numbered variant (`…_02/`, `…_03/`), so you can
watch a metric move across reruns and catch a regression. Overwrite in place only for a throwaway cosmetic
re-run of a deterministic result. (In the exemplar a tiny `runlog.py` helper does this, but the idea is
independent of any code: one experiment folder per study, one numbered subdirectory per run, small
provenance committed, heavy artifacts ignored.) The small carve-out for committing a figure — when it
*cannot* be regenerated in CI because it needs real data — is covered in [17_working_with_large_data.md](17_working_with_large_data.md).

## Interpretation stays with the scientist

Automate the recording, never the conclusion. In the exemplar, each run's report opens with a one-line
**Summary** (what the run was) and the scientist's **`## Interpretation (scientist)`** — a section tooling
is written to **never overwrite** — *before* the auto-filled provenance and metrics. Putting them first
means you can flip through a folder of reports and read "we did X, we found Y" from the opening lines; the
machine records the numbers, the human writes what they *mean*. That boundary is the whole point: the
framework exists to make your judgment reproducible and reviewable, not to replace it. (This division of labor is exactly the subject of [18_ai_assisted_development.md](18_ai_assisted_development.md), and it
matters most when an assistant wrote the driver.)

## How this connects

- **[15_experiments_and_shipping.md](15_experiments_and_shipping.md)** — where these folders live and how a concluded experiment's
  code graduates into the shipped library.
- **[12_testing_with_pytest.md](12_testing_with_pytest.md)** — a validation experiment that concludes cleanly becomes a
  regression test, so the result you just established stays true as the code changes.
- **[17_working_with_large_data.md](17_working_with_large_data.md)** — how the `inputs:` block above points at real data too big to
  commit, and how to pin *which* data a run used.
- **[18_ai_assisted_development.md](18_ai_assisted_development.md)** — when an assistant writes the driver, this provenance and this
  interpretation boundary are what keep the science honest.
