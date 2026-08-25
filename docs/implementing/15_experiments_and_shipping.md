# Experimenting, publishing, and shipping: one repo, multiple jobs

As your scientific project evolves, your repo may be holding code supporting multiple goals. There is **exploratory work** pursuing your scientific questions, data analysis, or comparing computational modeling approaches, the results of which may become **paper figures**. And there is the **code you might ship** (i.e., share with others for their own use), which should focus on the hardened, reliable approach. This doc gives a structure that keeps exploratory work and publishable outputs reproducible while the code evolves. Documents in the [disseminating](../disseminating/) folder discuss topics relating to archiving your results and shipping your code.

This doc is the *why* and *what*: the case for one repo serving as both your lab notebook and the
source for a publication, and the structure that makes that possible.
[16_running_a_dry_lab_experiment.md](16_running_a_dry_lab_experiment.md) is the *how* — the actual
practice of running and recording an experiment day to day.
[17_working_with_large_data.md](17_working_with_large_data.md) covers importing and referencing data too large to
commit, which the manifests described below depend on.

This is the repo-level counterpart to [13_software_design.md](13_software_design.md): the same "one job per unit" idea, scaled up from functions to the whole repository.

## The tension

Experiments used to develop a model or analyze data are iterative and involve many intermediate steps. A good experimental record is worth keeping regardless of the results: it documents the process and informs your scientific decision-making. Code and figures for publication are the polished part of the scientific record, need to be reproducible and rigorous, and traceable figure generation will avoid massive headaches if a reviewer asks you to reproduce or modify it a year later. The shipped library, meanwhile, should typically be narrowed to shareable methods, meaning reliable code that consistently performs as expected using the method you settled on through your experimental process. Left in one flat pile, these goals compete and corrode each other as the shipped code slowly accumulates dead alternatives nobody dares delete, and the experiments quietly stop running because the code moved under them. The structure proposed below organizes your repo to support each of those goals when you need it.

## The layout

Give the jobs distinct homes:

```
your_project/
├── src/<yourpkg>/      the code library (one home for all the methods functions and modules)
├── tests/              tests for the library (seeded from validation experiments)
├── experiments/        exploratory runs; import methods code from src and external data
│   ├── _common/          shared harness: comparison, plotting, logging scripts — not method code
│   └── <topic>/          theme folder: README, driver script(s) for this study, nested dated runs
├── docs/               autodoc doc site for the library (20_documentation_and_doc_sites.md)
├── figures/            (once drafting a manuscript) same theme + dated-runs discipline as experiments/
└── pyproject.toml
```

`src/<yourpkg>/` is the library: the pipeline code that experiments and analyses import. `experiments/` holds self-describing studies, each a standing folder you keep adding dated runs to rather than a folder you make once and leave, plus a shared `_common/` harness that the theme folders import comparison and logging code from. Crucially, **experiments import method code from `src`**; they use the library rather than carrying their own copy of it, so an experiment is a thin script that calls the library with particular inputs and records what happened. This is what keeps a comparison honest: while you are still deciding between approaches, the competing options all live in `src` together, so the experiment tests the library code and never drifts out of sync with a private copy.

That import only works once `src/<yourpkg>/` is installed as an editable package (`pip install -e .`) — a one-time setup step, not a distribution decision. [21_packaging.md](../disseminating/21_packaging.md) covers it; if you're using this layout at all, you already need that part of it.

A third folder, `figures/`, often joins these two once you start drafting a manuscript — the same
theme-and-dated-runs discipline as `experiments/`, just for paper figures instead of research
questions. [22_publishing_a_paper.md](../disseminating/22_publishing_a_paper.md) covers archiving it, and why
keeping one pays off well beyond the writing itself.

`src/`, `experiments/`, and `figures/` don't need the same visibility. The exploratory and archival work
in this doc is usually private for a long time; the shipped library it eventually produces is often
public much earlier and more fully. [repo_ownership_and_visibility.md](../reference/repo_ownership_and_visibility.md)
covers that split, plus owning the repo itself through a lab organization rather than one person's account.

Each experiment folder is self-contained: a `README` stating the question, aggregating the evidence (key tables and figures from the experiment runs), the running interpretation/conclusion, the code that generated the evidence, and a note pinning the environment it needs (see ["Reproducible without being precious about code"](#reproducible-without-being-precious-about-code), below). *How* you actually run one of these experiments and record its state so it reproduces — the research log, the folder template, and per-run provenance — is covered in [16_running_a_dry_lab_experiment.md](16_running_a_dry_lab_experiment.md). [example_repo_structure.md](../reference/example_repo_structure.md) shows this whole layout fleshed out: several themes, multiple runs each, and a `figures/` folder mid-manuscript.

## Exploratory, archival, and shippable: three overlapping modes

A repo built this way is doing three jobs, and they are not sequential stages you finish and leave
behind. At any given time a project may be doing some of each, and all three draw on the same
`src/`.

**Exploratory** work applies evolving methods, examines different input data, and tries different data visualizations and statistical analyses. The functions and modules underpinning these analyses are the evolving source code, kept in `src/`. This code base is changing throughout the experimental process, but keeping it organized in a centralized manner is exactly what lets an experiment compare approaches with a clean, traceable record and without drift. In practice this may mean that competing methods sit together in a library module, and the comparison in `experiments/` imports them from there. Alternatively one approach may be iterated upon, meaning that a module stored in `src/` changes between experimental runs. These independent runs are kept reliable and repeatable by committing the code between runs, so the exact code version that produced a result can always be retrieved.

**Archival** work is preparing a specific set of results for a manuscript, storing outputs of experiments that have reached a reportable conclusion in `figures/` while exploration of other, still-open questions
continues elsewhere in the same repo. The outputs saved in `figures/`, alongside the details needed to regenerate them, serve as an evolving manuscript outline with the figures updated or reordered throughout the writing process.

**Shippable** work is a trimmed library containing the approach(es) you've settled on, for people who
just want to install and use polished code rather than see the development work and methods comparison
that led there. Trimming, packaging, and shipping your code is covered in `docs/disseminating` when you need it.

These three overlap in time, and they overlap in code. `src/` is not three separate folders for three
separate jobs — it is one codebase whose *state at a given point in its history* serves whichever job
you're asking of it: `main` today for ongoing exploration, the `paper-v1` tag permanently for the
archival record, a release tag for installing a shipped version. The same function can be
doing exploratory duty on `main` and archival duty in a tag at the same time.

## Reproducible without being precious about code

None of this requires a moment where you formally decide a project is "done" and it's time to elevate or prune code. Real research does not work that way: you revisit old questions with new data, a method you set
aside six months ago sometimes turns out to be worth another look, and there is rarely one run that
settles anything for good. So `src/` is allowed to just keep changing — add an approach, rewrite one,
delete one you no longer touch day to day, whenever you want, with no ceremony and no certainty
required first. The routine described in [16_running_a_dry_lab_experiment.md](16_running_a_dry_lab_experiment.md) preserves every run by default, so the record stays intact well enough that you have the confidence to follow the science wherever it leads — with enough of a data trail to remember the winding path.

It's tempting to develop a new method inside an experiment folder first, and only move it into `src/`
once you're confident it's right — "graduating" it once it has earned a place in the real library.
Resist that. It doesn't remove the decision, it just moves it: instead of deciding when a document is
finished enough to save as `_final`, you're now deciding when a method is finished enough to earn a
place in `src/`. Instead, use
feature branches to write method code in `src/` from the start, even while it's still visibly wrong or
half-working; experiments then always import the current, real state of your thinking, and there is
nothing separate left to decide to graduate.

What makes constant change in `src/` safe rather than reckless is that every experiment's manifest
already points at the exact commit that produced it. If you rewrite how a method works and later
want to know exactly what changed since a run from six months ago, `git diff <that run's commit> --
src/<file>.py` shows you precisely that: the old version, the new version, and the difference between
them, without hunting through duplicated copies or trying to remember what you changed. That diff is
only meaningful because the method lived in one evolving file the whole time, rather than being copied
into experiment folders, edited in multiple places there, and moved into `src` later.

A run's outputs stay where they were written.
[16_running_a_dry_lab_experiment.md](16_running_a_dry_lab_experiment.md)'s preserve-by-default
convention means a run's `manifest.yaml`, `metrics.csv`, and any committed figure are never overwritten
or deleted by later work — they sit in the theme's `details/` folder, in your working copy, whether or
not `src/` has changed since.

The doc site renders those same committed figures and your notes about them in the README
([20_documentation_and_doc_sites.md](20_documentation_and_doc_sites.md)), generating an easily viewable "lab notebook": a theme's page shows a run's
actual result, not a live re-computation of it. Nothing needs to be rerun just to look at what a past
experiment found — the figure and the numbers are already sitting there, on disk, committed.

That is what makes it safe to not be precious about code. You can prune an approach out of `src/`
whenever you want, refactor a function, even delete a module — and a run that used the old version
stays fully visible and readable, because its figure and numbers were already committed and never
depended on that code continuing to exist or still working.

If a result does ever need to be regenerated, not just viewed — a reviewer asks you to extend it, or
you want to double-check it after a dependency update — a run manifest makes that possible: its
commit hash, its inputs, and its data checksum together describe exactly which code, on exactly which
data, produced this. Check out that commit, restore that data, rerun, and you get the same result back.

This rewards committing often. Every commit that a run's manifest can point to is a state you can
return to later, if needed. This logic is obvious for the big, deliberate moments like
cutting a `paper-v1` tag and archiving it for a permanent, citable record
([22_publishing_a_paper.md](../disseminating/22_publishing_a_paper.md)), but it holds continuously, at ordinary commits, long before that.

None of this has an equivalent in Excel, Prism, or a folder of scripts nobody is tracking. In those
tools, keeping an old result usually means manually saving a duplicate file, and there is no compact
way to answer "what exact process produced this specific number" months later except remembering it
yourself, or reconstructing it by hand. Here, that answer is a commit hash.

## Data still stays out of the repo

Nothing here changes the standard data rule ([CLAUDE.md](../../CLAUDE.md), [04_environments.md](../onboarding/04_environments.md)): experiments reference their input data by path or DOI rather than committing the dataset. The carve-out is deliberately small — a curated handful of real frames kept as a test or teaching fixture is genuinely useful and allowed; what stays out is the full depth of acquired data. A committed dataset bloats history permanently and is not what makes an experiment reproducible; a pinned code state plus an archived, referenced dataset is. The mechanics for data too big to commit — machine-local roots, DOIs, and checksums that pin *which* data a run used — are covered in [17_working_with_large_data.md](17_working_with_large_data.md).
