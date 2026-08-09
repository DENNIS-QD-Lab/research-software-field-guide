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

Everything below is illustrated by an example repo built to this standard, `SWIR_HDR_v2`, which is set up exactly this
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

## The reference ledger: the knowledge behind the decisions

The decision log records *what* you decided and *why* — the internal reasoning. But research decisions
also build on **external knowledge**: a method from a paper, a published threshold, a noise model off a
spec sheet, a standard you chose to follow. A **reference ledger** — a `references.md` at the repo root —
records that prior knowledge alongside the work that used it. One row per source: the citation, a link
or DOI, the date accessed (web pages change), and — the part that matters most — the **key relevant
points for *this* project**: why the source mattered *here*, not a general summary of it.

Keep it current as sources come up, not reconstructed at the end, for two reasons. First, the
"why it mattered here" note is cheap to write while the decision is fresh and expensive to recover
months later. Second, research code may be headed for a manuscript: a ledger that already pairs
each source with the decision it informed is a huge help when compiling your methods section and bibliography, and is more likely to be complete when accrued as
you went rather than reverse-engineered at the end. The ledger is the outward-facing companion to
the decision log — the decision log says *we switched to method B because it removed the artifact*; the
ledger says *method B is Granados et al. (2010), and here is the equation and why it applies to our
detector*. This is a convention worth keeping in **every** research repo, so the "source + why it
mattered here" pairing always travels with the code that used it; the payoff at write-up is covered in
[23_concluding_a_project.md](../disseminating/23_concluding_a_project.md). This guide keeps one at its root
([`references.md`](../../references.md)) as a worked example.

## The experiment folder: idea → test → outcome

Each distinct study gets its own self-contained folder (`experiments/crf-necessity/` — no date prefix)
built from a **template** so every experiment reads the same way. The folder is undated on purpose:
pipeline work loops — you build one stage, add another, loop back to fix the first, add a third — so a
theme is a standing address for a line of inquiry, revisited for as long as it stays open, not a snapshot
of when it happened to start. Chronology instead lives on the *runs* inside the folder (see "Save the
state of every run," below), where it actually applies. The exemplar's template (`experiments/_TEMPLATE.md`)
has a fixed set of headings:

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
# crf-necessity/details/260717_crf-necessity/manifest.yaml   (one subdirectory per run)
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
  that let you compare runs — RMSE, counts, whatever tracks quality), and the run's report.
- **Git-ignore the heavy, regenerable artifacts:** figures (`*.png`), large arrays (`*.npy`), and any
  scratch data. A deterministic, seeded run *reproduces* these from the committed code and manifest,
  so you are keeping the recipe, not the cake.

Keep the two levels straight, and keep a third split straight alongside them: the **experiment folder is
per *theme***, undated and permanent; each **run** writes a **report** directly into that folder, named
by date and slug (`crf-necessity/YYMMDD_slug.md`) so it's visible without opening anything; and the
provenance behind that report — `manifest.yaml`, `metrics.csv`, figures — lives one level down in a
matching `details/YYMMDD_slug/`, name-matched to its report but rarely opened on a normal read-through.
Runs accumulate in the same experiment folder — you do not make a new experiment folder to re-run.
**Preserve runs by default:** re-running the same study does not overwrite the last result — the first
run is `YYMMDD_slug.md` + `details/YYMMDD_slug/` and each rerun writes the next numbered variant
(`…_02`, `…_03`, kept in sync between the report and its `details/` counterpart), so you can watch a
metric move across reruns and catch a regression. Overwrite in place only for a throwaway cosmetic
re-run of a deterministic result. (In the exemplar a tiny `runlog.py` helper does this, but the idea is
independent of any code: one experiment folder per theme, one numbered report + matching details
subdirectory per run, small provenance committed, heavy artifacts ignored.) If a runlog helper already
exists and other drivers depend on today's co-located shape, keep this split **additive** — a new
optional parameter defaulting to the old behavior — so one driver can adopt it without moving every
other driver's runs at the same time. The small carve-out for committing a figure — when it *cannot* be
regenerated in CI because it needs real data — is covered in [17_working_with_large_data.md](17_working_with_large_data.md).

## Interpretation stays with the scientist

Automate the recording, never the conclusion. In the exemplar, each run's report opens with a one-line
**Summary** (what the run was) and the scientist's **`## Interpretation (scientist)`** — a section tooling
is written to **never overwrite** — *before* the auto-filled provenance and metrics. Putting them first
means you can flip through a folder of reports and read "we did X, we found Y" from the opening lines; the
machine records the numbers, the human writes what they *mean*. That boundary is the whole point: the
framework exists to make your judgment reproducible and reviewable, not to replace it. (This division of labor is exactly the subject of [18_ai_assisted_development.md](18_ai_assisted_development.md), and it
matters most when an assistant wrote the driver.)

## Exploratory notebooks: the same discipline, without a manifest

A notebook exploring an idea has the same reproducibility problem a driver script solves with a
manifest — except nothing forces you to *notice* an observation matters before you change something and
rerun. That is the specific failure mode worth naming: in the moment, you often cannot tell which run
will turn out to matter later, so a rule that only kicks in "when it seems important" will not catch it.
Two cheap habits, applied unconditionally, close most of that gap:

- **A top-cell note, written before you touch anything else.** A markdown cell at the very top of the
  notebook with "What / why" (what you're testing this run, and why) and "Observed" (what you saw) —
  filled in for real *before* the next parameter change and rerun. This is the notebook analog of the
  protected `## Interpretation` section above, doing the same job: recording judgment a machine cannot
  write for you, at the moment it is cheapest to write it.
- **Duplicate the notebook once you've written a note you'd be annoyed to lose** (`noise_test_01.ipynb`
  → `noise_test_02.ipynb`). This is PRESERVE-by-default, ported to notebooks: it protects *what code
  produced what*, the same way a driver's numbered rerun does. The observation is the trigger, not a
  pre-planned sweep — you are not declaring upfront "this will be a parameter sweep," you are noticing,
  after the fact, that this particular run is worth keeping side by side with the next one.

Neither habit fully solves the underlying problem — a scientist who does not yet know something matters
cannot be forced to document it, by any tooling. That is an honest limit of exploratory work, not a gap
to engineer around. Because an exploratory notebook has not called a runlog helper, it has no matching
`details/` folder; a run only gets one once it is promoted to a driver script that writes a manifest.

## Choosing how much gets documented

Every run already gets a manifest, metrics, and a report inside `experiments/` — that part is not
optional, and doesn't change here. What *is* optional is whether a run's report also gets **promoted**:
given a page in the built Sphinx site, and a PDF copy dropped in the team's shared archive, so someone
can see it without opening the repo or re-running anything.

**The default you start with matters, and it's fine to change it.** Early on, you often don't know in
the moment which run will turn out to matter later — the same problem the exploratory-notebook habit
above is designed around. So the beginner default is **document everything**: every run gets promoted
automatically, no decision required. Set:

    export DOCUMENT_EVERYTHING=1

in your shell profile (alongside this repo's other machine-local settings, the way `local_paths.py`
works), and every run from then on gets a doc page and an archived PDF, whether or not it turns out to
matter. The cost is a growing pile of pages and PDFs for runs that never mattered — that's a real cost,
not a free safety net — but it's the same trade the repo already makes for the raw reports themselves:
`runlog.py` preserves every run rather than overwriting it, because a losing result is still evidence,
and it's far easier to prune a pile later than to reconstruct something you didn't know to keep.

**Once you've done this enough to know what's worth keeping, flip the default.** Unset
`DOCUMENT_EVERYTHING` (or set it to `0`), and nothing gets promoted automatically — you decide, run by
run, which ones earn a doc page. You can still promote (or deliberately skip) any single run regardless
of your default:

    run = runlog.start_run(..., promote=True)   # promote this one run
    run = runlog.start_run(..., promote=False)  # skip this one, even if your default is on

Nothing about your manifest, metrics, or report changes either way — you're only choosing whether a run
*also* gets the extra visibility of a doc page and an archived PDF. Turning "document everything" off
never loses anything already in the repo.

**This is a personal setting, not a project one.** A trainee still learning to judge what matters, and
a PI who already knows, can be working in the *same* repo with different defaults at the same time,
because the setting lives in each person's own environment, not in a file the repo tracks. The full
mechanics — how promotion and archiving actually work, and how to adapt them to your own repo — are in
[documentation_promotion.md](../reference/documentation_promotion.md).

## How this connects

- **[15_experiments_and_shipping.md](15_experiments_and_shipping.md)** — where these folders live and how a concluded experiment's
  code graduates into the shipped library.
- **[12_testing_with_pytest.md](12_testing_with_pytest.md)** — a validation experiment that concludes cleanly becomes a
  regression test, so the result you just established stays true as the code changes.
- **[17_working_with_large_data.md](17_working_with_large_data.md)** — how the `inputs:` block above points at real data too big to
  commit, and how to pin *which* data a run used.
- **[18_ai_assisted_development.md](18_ai_assisted_development.md)** — when an assistant writes the driver, this provenance and this
  interpretation boundary are what keep the science honest.
