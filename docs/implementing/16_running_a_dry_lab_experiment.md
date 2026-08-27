# Running a dry-lab experiment

[15_experiments_and_shipping.md](15_experiments_and_shipping.md) gave you the *structure*: a `src/` library and an
`experiments/` folder. This doc is about the *practice* — how you actually run a computational
("dry-lab") experiment and record it so the result holds up later.

A dry-lab experiment has the same arc as a bench experiment: you have a **question**, you **design**
a way to answer it, you **run** it, you **record** what happened, you **interpret** the result, and
often you **repeat** it. The repo is your ***lab notebook***: any run can be reproduced, and the whole line of inquiry can be
followed, by viewing the results and reading your interpretation, which allows for a more scientific focus than just reading the git history. Someone (including future-you) should be able to open
the folder and see what you asked, what you found, and what to do next.

## The pieces, at a glance

What follows works at three different scales: two files you keep current for the whole project,
a structure repeated for every line of inquiry, and a set of practices that make each individual
result trustworthy.

**Kept current for the whole project**
- **The research log** — one file holding current state: the goal, open questions, what's next.
- **The reference ledger** — a running list of the external knowledge (papers, specs, standards) behind your decisions.

**Repeated for each line of inquiry**
- **The experiment folder** — one per question/study theme, a chronological log of what was tried and what came of it.
- **The run manifest** — what a run writes automatically so it can be reproduced later.
- **What you write into the README** — which of those runs becomes a documented finding, and how much of its history stays visible.

**What makes a result trustworthy**
- **Validation** — designing an experiment whose answer can actually be checked, not just run.
- **Looking at the data** — catching problems while they're still cheap to fix.
- **Interpretation** — what a run records automatically, and what only you write.

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

The decision log above records *what* you decided and *why*. Research decisions
also build on **external knowledge**: a method from a paper, a published threshold, a noise model off a
spec sheet, a standard you chose to follow. A **reference ledger** ([references.md](../../references.md) saved at the repo root) records that prior knowledge alongside the work that used it. One row per source: the citation, a link
or DOI, the date accessed (web pages change), and, critically, the **key relevant
points for *this* project**: why the source mattered *here*, not a general summary of it. Keep it current as sources come up, not reconstructed at the end, for the sake of future-you as well as anyone else who may work on the project.

## The experiment folder: a chronological log, not a fixed form

Each distinct study theme gets its own self-contained folder (e.g., `experiments/01_noise-reduction/`; use the numbered prefix if you want them to appear in the order they are introduced)
built from a **template** so every experiment reads the same way. The theme folder is undated on purpose:
pipeline work loops — you build one stage, add another, loop back to fix the first, add a third — so a
theme is a standing address for a line of inquiry, revisited for as long as it stays open. Specific experiments are dated runs inside the folder (see "Save the
state of every run," below), documenting the chronological accrual of results or evidence related to that theme.

The template (`experiments/_TEMPLATE.md`) is deliberately *not* a fixed set of headings
(Question → Hypotheses → Tests → Findings → Status) — real research doesn't arrive in that
order, and sorting it into those categories after the fact divides your actual train of thought
from the record of it. Instead the README is a **chronological log**: a dated `##` section per
episode, in the order things actually happened, each a short prose narration of what was tried and
what came of it (a null result or a method that underperforms is a finding, not a failure — keep
it), plus your own interpretation in a signed blockquote right where it belongs. A **bottom-line
blockquote near the top**, in your own words, gives a reader the current state without making them
read the whole log first. Two standing sections close the file — `## Reproduce` (the exact command
and which tag/state to check out) and `## Open items` (a short tracker of what's unresolved) — and
those two aren't part of the log itself.

Copy the template to start a new experiment, and add a row to the research log so it shows up in the
status table. Rinse and repeat.

This README is also what other people see. It renders directly into the project's Sphinx doc site
([20_documentation_and_doc_sites.md](20_documentation_and_doc_sites.md)), so the same file you keep
updating as you work doubles as the easiest-to-share, easiest-to-navigate view of your lab notebook —
no separate write-up step.

[example_repo_structure.md](../reference/example_repo_structure.md) shows what several of these theme
folders, each with multiple runs, actually look like once a project has been running for a while.

## Validation: designing an experiment you can trust

An experiment can only be satisfactorily concluded if its result can actually be believed. A **validation experiment** is one designed so its answer can be checked against something you already trust — a comparison to ground truth, to an independent method, or to a synthetic dataset with a known answer. That check is what confirms the analysis does what you *intend*, as opposed to merely running without error (the verification-versus-validation distinction in [18_ai_assisted_development.md](18_ai_assisted_development.md)).

Build the check in when you design the experiment, not after:

- **A known answer.** Run on an input whose correct output you already know, from theory or a hand calculation.
- **Synthetic data.** Generate inputs with the answer built in, so any deviation from it is visible and quantifiable.
- **An independent method.** Compare against a second, unrelated route to the same quantity.

A validation experiment that concludes cleanly does double duty: it answers today's question, and — once you trust it — freezing it as a regression test ([12_testing_with_pytest.md](12_testing_with_pytest.md)) keeps that result true as the code keeps changing.

## Look at the data at every step

In the exploratory phase you often do not yet have a test for every step — so *looking* is the method.
Manually examining the data as it moves through the pipeline builds intuition for both the data and the
analysis, and catches problems early, while they are cheap to fix. Design your code to generate *and
present* its intermediate outputs often, not only the final number. Plot the intermediate arrays, their
distributions, or the residuals — whatever shows the *shape* of the data at that step — and check how each
step changes them. (For image processing work, for instance, look at the image **and** a histogram of its intensities
together, so that when a step excludes data — say, by implementing a threshold-based mask — you see what it does to both.)

## Save the state of every run

Reproducibility does not happen by
remembering — it happens because each run **records the state that produced it**. When a driver runs,
have it write a small **manifest** next to its outputs:

```yaml
# noise-reduction/details/260717_noise-reduction/manifest.yaml   (one subdirectory per run)
slug: noise-reduction
summary: "Rolling-median and Savitzky-Golay smoothing agree once the baseline is subtracted."
driver: run_noise_reduction.py
created: 2026-07-17T14:02:11
git:
  commit: 4f7675a
  dirty: false                   # were there uncommitted changes when this run happened?
inputs:
  dataset: run_2026-06-30        # which data (see 17_working_with_large_data.md)
  dataset_sha256: 9c1f…          # so you can prove two runs used the same input
experimental_params:
  threshold: 0.85
  seed: 0
```

`summary` and `driver` make a `details/` folder scannable without opening each file — what this run was
about, and which script produced it. The commit hash under `git` says *which code*, `dirty` says whether
that code was actually committed or the run used uncommitted changes instead, `experimental_params` says
*how* it was configured, and `inputs` says *what it ran on*. With those recorded, reproducing the run
behind Figure 3 means checking out that commit, restoring that input dataset, and rerunning with those
parameters. Seeding any randomness is what lets a rerun return the *same* numbers rather than merely
similar ones — the same determinism a regression test relies on
([12_testing_with_pytest.md](12_testing_with_pytest.md)).

`git.commit` and `dataset_sha256` pin *which code* and *which data* produced a run — but not *which
package versions* executed them. An `environment.yml` install can quietly drift as its dependencies
release new versions, the same drift [11_code_quality_tools.md](11_code_quality_tools.md) describes
for a single pinned tool. For a run that needs to reproduce exactly, add a fully-resolved lockfile
(`conda-lock`, `pip freeze`, or a project tool like Hatch or Pixi) alongside the manifest, so a rerun
months later installs the identical dependency graph, not just the identical `environment.yml`. Lock a
run only when it actually needs that guarantee — a lockfile captured once and never revisited just
pins the project to an aging dependency set nobody wants to build against later.

## Repeat runs, and track quality, without bloating the repo

You will run an experiment many times. If every run committed its figures and arrays, or generated
its own markdown report, the repo would balloon, its history would be permanently heavy, and the
theme folder would fill up with dozens of near-identical files for runs that mostly just re-confirmed
a driver still reproduced its prior output. Keep two things separate: what a *run* writes
automatically, and what you choose to write into the theme's README.

A run writes and commits only small, non-regenerable provenance automatically:

- **`manifest.yaml` and `metrics.csv`** (the numbers that let you compare runs — RMSE, counts, whatever tracks quality).
- **Everything else heavy is git-ignored by default**, including figures (`*.png`), large arrays (`*.npy`), and
  any scratch data. A deterministic, seeded run *reproduces* these from the committed code and
  manifest, so day to day you are keeping the recipe, not the cake.

The one exception is a figure you promote into the theme's README, below — it has to
actually be present in the repo for GitHub or the doc site to render it, so that single file gets
committed alongside the manifest (`git add -f`, since it matches the ignored `*.png` pattern).
Everything else a run produced stays ignored and regenerable.

The folder layout is the third thing to keep straight:

```
noise-reduction/                      the theme: undated, permanent, one line of inquiry
├── README.md                       the one narrative page: chronological log, figures, interpretation
└── details/
    ├── 260717_noise-reduction/       one run's provenance: manifest.yaml, metrics.csv, figures
    └── 260717_noise-reduction_02/    the same study, re-run
```

Runs accumulate inside the same theme folder, each as a new dated entry in `details/` — you never
create a new experiment folder just to re-run a study. The theme's `README.md` is the key narrative
document: written once, updated in place as findings accrue.

**Preserve runs by default.** Re-running a study does not overwrite the previous result: the first run
is `details/260717_noise-reduction/`, and each rerun writes the next numbered variant (`…_02`, `…_03`).
That is what lets you watch a metric move across reruns and catch a regression. Overwrite in place only
for a throwaway cosmetic re-run of a deterministic result.

When a run's figure is worth keeping visible — because it's the current evidence for a finding, not
because the driver merely ran again — embed it directly in the theme's README, with a short
*italic* caption noting the run id and the command that reproduces it:

```markdown
## 260717 — rolling-median vs. Savitzky-Golay agreement

Both smoothing methods agree to three decimals once the baseline is subtracted (R² ≈ 0.985/0.983).

![](details/260717_noise-reduction/method_agreement.png)
*Run `260717_noise-reduction` — reproduce with `python experiments/noise-reduction/run_noise_reduction.py`.*

> **AMD:** _what it means — pending._
```

When a rerun supersedes the embedded figure, swap the image path and caption in place;
the superseded run's own `details/` folder is untouched and still there if you need to compare against
it directly. When the comparison between runs is itself the finding, build a comparison figure
instead, citing each run by id:

```markdown
## 260720 — window-size sweep

Increasing the smoothing window reduces noise but blurs the edge past window = 5.

![](details/260718_noise-reduction/window_comparison.png)
*Runs `260715_noise-reduction`, `260717_noise-reduction`, `260718_noise-reduction` (window = 3, 5, 8) — a
small comparison script in `_common/` reads all three runs' `metrics.csv` and plots them together.*

> **AMD:** _what it means — pending._
```

Which shape best supports your science — one current result, or a comparison across several — is a
call you make per finding, not a repo-wide setting; the same README can hold both. Every run still
gets its own manifest and metrics, preserved in `details/` regardless; there's no automated switch
that decides for you whether a run becomes a documented finding at all — that stays your call, made
fresh each time a run finishes.

## Keep the assistant's writing short and factual

An assistant filling in a README tends to write more than the record needs: a paragraph of framing
before the point, a recap of context the file already shows two lines up, or a list of gaps and open
questions nobody asked for. Each of those sentences is something the scientist has to read past to
find the actual result, and a README that takes ten minutes to read stops getting read — and,
eventually, stops getting written by the person who owns it.

Ask the assistant for exactly what belongs in the record: what ran, on what data, with what
read-out, in one or two sentences — about the length a scientist writing it by hand would use. A
running commentary on what looks unresolved or worth trying next is the scientist's call, made in
their own words, in the signed blockquote below.

## Interpretation stays with the scientist

A machine can write *what ran and what it measured* — the manifest, the metrics, a figure — but only
you can write what a result *means*. That judgment belongs in the theme's `README.md`, in your own
words, right next to the finding it belongs to. The framework exists to make your judgment reproducible
and reviewable, not to replace it. (This division of labor is exactly the subject of
[18_ai_assisted_development.md](18_ai_assisted_development.md), and it matters most when an AI
assistant wrote the driver.)

A dated entry in an experiment README, a line in the research log's decision log, a note on a
theme's open items — any of these can slide into asserting what a result *means* rather than
what it *shows*. The lightweight tool that keeps the line visible is a **signed blockquote**, dropped
in wherever the *why* actually belongs:

> **AMD:** Examination of multiple curve fits shows that the monoexponential fit was the most appropriate. The biexponential had slightly improved statistics, but based on the number of data points that we have, that appears to be overfitting the data. I'm going to continue with the monoexponential fit with baseline offset for now. Re-consider the fit after examining the standard error vs. intensity to confirm what weighting should be used for the fit.

Sign it with your name or initials. The blockquote reads identically on GitHub, in an editor, and in a
built Sphinx site, so your notes are always visible wherever the doc is read.

- **Keep your own words.** Write your interpretation yourself, and if you're asking an AI assistant to
  help draft the surrounding text, make sure it inserts what you actually said verbatim in the blockquote rather than
  tightening or rephrasing it — a paraphrase quietly substitutes the assistant's voice for yours and over time erodes your scientific story.
- **If you haven't decided yet, say so.** Write a placeholder like 
> **AMD:** _Interpretation pending._

rather than leaving the spot blank — or, if you're using an assistant, rather than
  letting it draft a plausible-sounding guess on your behalf. You can't come back to fill a hole you don't know is there.

## Exploratory notebooks: the same discipline, without a manifest

An ipynb notebook is really powerful for exploring an idea, but it has a reproducibility problem that isn't easily solved with a driver script attaching a run manifest. While freely exploring in the notebook, nothing forces you to *notice* an observation matters before you change something and rerun. Two cheap habits, applied unconditionally, close most of that gap:

- **A top-cell note, written before you touch anything else.** A markdown cell at the very top of the
  notebook with "What / why" (what you're testing this run, and why) and "Observed" (what you saw) —
  filled in for real *before* the next parameter change and rerun. This is the notebook analog of the
  signed blockquote above, doing the same job: recording judgment a machine cannot write for you, at
  the moment it is cheapest to write it.
- **Duplicate the notebook if you see a result you'd be annoyed to lose** (`noise_test_01.ipynb`
  → `noise_test_02.ipynb`). This is preserve-by-default, ported to notebooks: it protects *what code
  produced what*, the same way a driver's numbered rerun does. The observation is the trigger, not a
  pre-planned sweep — you are not declaring upfront "this will be a parameter sweep," you are noticing,
  after the fact, that this particular run is worth keeping side by side with the next one.

A scientist who does not yet know something matters cannot be forced to document it by any tooling —
these two habits close most of that gap, not all of it. Because an exploratory notebook has not called
a runlog helper, it has no matching `details/` folder; a run only gets one once it is promoted to a
driver script that writes a manifest.
