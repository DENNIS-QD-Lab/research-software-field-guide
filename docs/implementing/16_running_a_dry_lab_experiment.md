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

You will run an experiment many times. If every run committed its figures and arrays — or generated
its own markdown report — the repo would balloon, its history would be permanently heavy, and the
theme folder would fill up with dozens of near-identical files for runs that mostly just re-confirmed
a driver still reproduced its prior output. The rule that keeps the record complete *and* the repo (and
the folder listing) small: **a run writes provenance, not prose.**

- **Commit the small, non-regenerable provenance:** the `manifest.yaml` and a `metrics.csv` (the
  numbers that let you compare runs — RMSE, counts, whatever tracks quality). Nothing else is written
  automatically.
- **Git-ignore the heavy, regenerable artifacts:** figures (`*.png`), large arrays (`*.npy`), and any
  scratch data. A deterministic, seeded run *reproduces* these from the committed code and manifest,
  so you are keeping the recipe, not the cake.

Those two rules cover what a *run* writes. The folder layout is a third thing to keep straight:

```
crf-necessity/                      the theme: undated, permanent, one line of inquiry
├── README.md                       the one narrative page: question, findings, figures, interpretation
└── details/
    ├── 260717_crf-necessity/       one run's provenance: manifest.yaml, metrics.csv, figures
    └── 260717_crf-necessity_02/    the same study, re-run
```

The theme folder is undated and permanent, and the dates live on the runs inside `details/`. Runs
accumulate there — you do not create a new experiment folder to re-run a study, and a run does not get
its own report file. The theme's `README.md` is the *only* narrative document: written once, updated
in place as findings accrue, never regenerated per run.

**Preserve runs by default.** Re-running a study does not overwrite the previous result: the first run
is `details/260717_crf-necessity/`, and each rerun writes the next numbered variant (`…_02`, `…_03`).
That is what lets you watch a metric move across reruns and catch a regression. Overwrite in place only
for a throwaway cosmetic re-run of a deterministic result.

When a run's figure is worth keeping visible — because it's the current evidence for a finding, not
because the driver merely ran again — embed it directly in the README's Findings section, with a short
*italic* caption noting the run id and the command that reproduces it:

```markdown
- **H1 (real data, 2026-07-17):** two-step and joint CRF solves agree to three decimals once dark
  current is subtracted (R² ≈ 0.985 / 0.983).

  ![](details/260717_crf-necessity/crf_fit_twostep.png)
  *Run `260717_crf-necessity` — reproduce with `python experiments/crf-necessity/run_crf_necessity.py`.*
```

That caption is deliberately *not* a heading. It exists so the run can be reproduced, not so it can be
linked to or indexed — a page full of `## Provenance` sections is the same clutter problem in a
different font. When a rerun supersedes the embedded figure, swap the image path and caption in place;
the superseded run's own `details/` folder is untouched and still there if you need to compare against
it directly.

In the exemplar a small `runlog.py` helper writes the manifest/metrics split, but the convention does
not depend on that code: one folder per theme, one `README.md`, one numbered `details/` subdirectory
per run, small provenance committed, heavy artifacts ignored. If you already have a runlog helper that
also writes a per-run report file and other drivers depend on that shape, drop the report-writing call
one driver at a time rather than all at once — each driver's own README absorbs that driver's findings
whenever you touch it next, so nothing has to move in a single pass.

[17_working_with_large_data.md](17_working_with_large_data.md) covers the small carve-out for committing
a figure that cannot be regenerated in CI because it needs real data.

## Interpretation stays with the scientist

Automate the recording, never the conclusion. A machine can write *what ran and what it measured* —
the manifest, the metrics, a figure — but it should never write *what a result means*. That judgment
lives in the theme's `README.md`, in the scientist's own words, right next to the finding it belongs
to. The machine records the numbers; the human writes what they mean. That boundary is the whole
point: the framework exists to make your judgment reproducible and reviewable, not to replace it.
(This division of labor is exactly the subject of [18_ai_assisted_development.md](18_ai_assisted_development.md), and it
matters most when an assistant wrote the driver.)

A Findings bullet in an experiment README, a line in the research log's decision log, a caveat on a
theme's Status & decisions — any of these can slide into asserting what a result *means* rather than
what it *shows*. The lightweight tool that keeps the line visible is a **signed blockquote**, dropped
in wherever the *why* actually belongs:

> **AMD:** the CRF is adding little here that a calibrated linear model doesn't already capture.

Sign it with your own initials rather than a generic "Scientist" label — nothing in the runlog or
doc-promotion tooling parses the label text, so this is free to be as specific as a multi-contributor
repo needs, and it reads identically on GitHub, in an editor, and in a built Sphinx site: a plain
markdown blockquote, no color-coding or custom syntax required. Two rules keep it worth trusting:

- **Insert it verbatim.** If the scientist writes three words, three words is what goes in the doc — an
  assistant tightening or rephrasing it quietly substitutes its own voice for theirs, which is exactly
  what this convention exists to prevent.
- **Leave a placeholder rather than guess.** When a spot calls for a judgment call nobody has made yet,
  write `> **AMD:** _Interpretation pending._` instead of filling the gap with a plausible-sounding guess
  or leaving it silently blank — a visible gap gets noticed and closed; an invisible one doesn't.

An assistant drafting or editing these docs should hold to the same split as the driver code: its own
prose stays to *method* (what ran, on what data and parameters) and *observed result* (what the numbers
or a plot show); anywhere the text would otherwise assert what a result implies, what caused it, or what
to do next, that becomes a signed blockquote instead — filled in if the scientist has already said it, a
`_pending_` placeholder if not.

## Exploratory notebooks: the same discipline, without a manifest

A notebook exploring an idea has the same reproducibility problem a driver script solves with a
manifest — except nothing forces you to *notice* an observation matters before you change something and
rerun. That is the specific failure mode worth naming: in the moment, you often cannot tell which run
will turn out to matter later, so a rule that only kicks in "when it seems important" will not catch it.
Two cheap habits, applied unconditionally, close most of that gap:

- **A top-cell note, written before you touch anything else.** A markdown cell at the very top of the
  notebook with "What / why" (what you're testing this run, and why) and "Observed" (what you saw) —
  filled in for real *before* the next parameter change and rerun. This is the notebook analog of the
  signed blockquote above, doing the same job: recording judgment a machine cannot write for you, at
  the moment it is cheapest to write it.
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

Every run already gets a manifest and metrics inside `experiments/<slug>/details/` — that part is not
optional, and doesn't change here. What *is* a judgment call is whether a run's figure and numbers are
worth writing into the theme's `README.md` at all: not every rerun is a new finding, and most reruns
just confirm a driver still reproduces its prior output. There is no automated switch or environment
variable that makes this decision for you — "documenting" a run now literally means editing the README,
so the only question is whether this run changed what you'd write there.

**Early on, err toward writing more.** You often don't know in the moment which run will turn out to
matter later — the same problem the exploratory-notebook habit above is designed around. Because
embedding a figure is a one-line edit to a file you already have open, not a new file a tool generates,
the cost of erring toward "write it down" is genuinely small: at worst the README grows a paragraph you
later trim, not a pile of pages nobody reads.

**As you learn what's worth keeping, prune the README down to the current evidence.** When a rerun
supersedes an embedded figure, replace it in place rather than adding a second entry beside it — the
superseded run's own `details/` folder is still there, untouched, if you ever need to go back to it.
The README should always read as *the current state of the finding*, not a running log of every attempt.

**Sharing outside the repo** (a PDF for a lab meeting, an external collaborator who won't clone the
repo) is a separate, occasional need from day-to-day documentation, and doesn't require promoting every
run automatically. Export the theme's README (or a specific figure) to PDF when you actually need to
share it. Mechanics for that export are in
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
