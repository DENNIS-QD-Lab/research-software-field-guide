# Experimenting, publishing, and shipping: one repo, multiple jobs

As your scientific project evolves, your repo may be holding code supporting multiple goals. There is **exploratory work** pursuing your scientific questions, data analysis, or comparing computational modeling approaches, the results of which may become **paper figures**. And there is the **code you might ship** (i.e., share with others for their own use), which should focus on the hardened, reliable approach. This doc gives a structure that keeps exploratory work and publishable outputs reproducible while the code evolves. Documents in the [disseminating](/dissemenating) folder discuss topics relating to shipping your code.

This is the repo-level counterpart to [13_software_design.md](13_software_design.md): the same "one job per unit" idea, scaled up from functions to the whole repository.

## The tension

Experiments used to develop a model or analyze data are iterative and comprise many intermediate steps; a good experimental record is worth keeping regardless of the results: it documents the process and informs your scientific decision-making. Code and figures for publication are the polished part of the scientific record, need to be reproducible and rigorous, and tracable figure generation will avoid massive headaches if a reviewer asks you to reproduce or modify it a year later. The shipped library, meanwhile, should typically be narrowed to sharable methods, meaning reliable code that consistently performs as expected using the method you settled on through your experimental process. Left in one flat pile, these goals compete and corrode each other as the shipped code slowly accumulates dead alternatives nobody dares delete, and the experiments quietly stop running because the code moved under them. The structure proposed below organizes your repo to support each of those goals when you need it.

## The layout

Give the jobs distinct homes:

```
your_project/
├── src/<yourpkg>/      the code library (one home for all the key methods functions and modules)
├── tests/              tests for the library (seeded from validation experiments)
├── experiments/        exploratory runs; import methods code from src, external data for model runs, data analysis, or data visualization scripts needed for this experiment— not method code
│   └── <topic>/        theme folders contain README summary and nested, dated runs
├── docs/               autodoc doc site for the library (20_documentation_and_doc_sites.md)
├── figures/            (once drafting a manuscript) same theme + dated-runs discipline as experiments/
└── pyproject.toml
```

`src/<yourpkg>/` is the library: the pipeline code that experiments and analyses import. `experiments/` holds self-describing studies, each a standing folder you keep adding dated runs to rather than a folder you make once and leave, plus a shared `_common/` harness that the theme folders import comparison and logging code from. Crucially, **experiments import method code from `src`**; they use the library rather than carrying their own copy of it, so an experiment is a thin script that calls the library with particular inputs and records what happened. This is what keeps a comparison honest: while you are still deciding between approaches, the competing options all live in `src` together, so the experiment tests the library code and never drifts out of sync with a private copy.

A third folder, `figures/`, often joins these two once you start drafting a manuscript — the same
theme-and-dated-runs discipline as `experiments/`, just for paper figures instead of research
questions. [23_concluding_a_project.md](../disseminating/23_concluding_a_project.md) covers it, and why
keeping one pays off well beyond the writing itself.

`src/`, `experiments/`, and `figures/` don't need the same visibility. The exploratory and archival work
in this doc is usually private for a long time; the shipped library it eventually produces is often
public much earlier and more fully. [repo_ownership_and_visibility.md](../reference/repo_ownership_and_visibility.md)
covers that split, plus owning the repo itself through a lab organization rather than one person's account.

Each experiment folder is self-contained: a `README` stating the question, aggregating the evidence (key tables and figures from the experiment runs), the running interpretation/conclusion, the code that ran it, and a note pinning the environment it needs (see ["Reproducible without being precious about code"](#reproducible-without-being-precious-about-code), below). *How* you actually run one of these experiments and record its state so it reproduces — the research log, the folder template, and per-run provenance — is covered in [16_running_a_dry_lab_experiment.md](16_running_a_dry_lab_experiment.md). [example_repo_structure.md](../reference/example_repo_structure.md) shows this whole layout fleshed out: several themes, multiple runs each, and a `figures/` folder mid-manuscript.

## Exploratory, archival, and shippable: three overlapping modes

A repo built this way is doing three jobs, and they are not sequential stages you finish and leave
behind. At any given time a project is likely doing some of each, and all three draw on the same
`src/`.

**Exploratory** work is applying evolving methods, examining different input data, trying out different data visualizations and statistical analyses. The functions and modules underpinning these analyses is the source code, evolving in `src/`. This code base is living and evolving through the experimental process, but keeping it organized in a centralized manner is
exactly what lets an experiment import and compare approaches with a clean, tracable record and without drift. In practice this often means
several competing methods sit together in one library module (or a small handful of them), and the
comparison in `experiments/` imports them from there.

**Archival** work is preparing a specific set of results for a manuscript, using `figures/` (above) and
experiments that have already reached a conclusion — while exploration of other, still-open questions
continues elsewhere in the same repo, at the same time.

**Shippable** work is a trimmed library containing the approach(es) you've settled on, for people who
just want to install and use it rather than see the development work and methods comparison that led there. "The library carries
only the proven approach" describes that end state; it is not something true from day one, and it is
not the state a *paper* reproduces from. A paper reproduces from a tag of the full, pre-trim code, with
every compared approach still present; the trim happens only *after* that tag is cut, and only where
you choose to make it (the decision below) — it never requires deleting anything from the record.

These three overlap in time, and they overlap in code. `src/` is not three separate folders for three
separate jobs — it is one codebase whose *state at a given point in its history* serves whichever job
you're asking of it: `main` today for ongoing exploration, the `paper-v1` tag permanently for the
archival record, a release tag for whoever installed the shipped version. The same function can be
doing exploratory duty on `main` and archival duty in a tag at the same time.

None of this requires a moment where you formally decide a comparison has "concluded" and it's time to
prune. Real research does not work that way: you revisit old questions with new data, a method you set
aside six months ago sometimes turns out to be worth another look, and there is rarely one run that
settles anything for good. So `src/` is allowed to just keep changing — add an approach, rewrite one,
delete one you no longer touch day to day, whenever you want, with no ceremony and no confidence
required first. That is not a rule you have to apply carefully; it is what keeps the whole model
low-friction enough to actually use, the same reason
[16_running_a_dry_lab_experiment.md](16_running_a_dry_lab_experiment.md) preserves every run by default
instead of asking you to decide upfront whether it matters.

It's tempting to develop a new method inside an experiment folder first, and only move it into `src/`
once you're confident it's right — "graduating" it once it has earned a place in the real library.
Resist that: it just relocates the same problem as an over-precious final document into git, since now
you are the one deciding when a method is done enough to earn a home in the shared library, and that
decision is exactly the proactive confidence-before-you-save friction the rest of this guide argues
against. Write method code in `src/` from the start, even while it's still visibly wrong or
half-working; experiments then always import the current, real state of your thinking, and there is
nothing separate left to decide to graduate.

What makes constant change in `src/` safe rather than reckless is that every experiment's manifest
already points at the exact commit that produced it
([above](#reproducible-without-being-precious-about-code)). If you rewrite how a method works and later
want to know exactly what changed since a run from six months ago, `git diff <that run's commit> --
src/<file>.py` shows you precisely that: the old version, the new version, and the difference between
them, without hunting through duplicated copies or trying to remember what you changed. That diff is
only meaningful because the method lived in one evolving file the whole time, rather than being copied
into an experiment folder, edited there, and copied back later.

**A frozen reference, when `src` itself must keep moving.** Sometimes a comparison needs to hold still
against one specific historical version of an approach even as `src` keeps evolving past it — not the
currently-shipped version, a frozen one. When that happens, keep a verbatim, frozen copy in the
experiments harness (`experiments/_common/`) rather than in `src`, and re-export the *current* version
from `src` for the other side of the comparison. This is a deliberate choice for one specific
comparison, not a general rule — most of the time, the commit history above is reference enough.

## Reproducible without being precious about code

Everything above focuses on the big, deliberate moments — cutting a `paper-v1` tag, archiving to
Zenodo. The same reproducibility actually holds continuously, at ordinary commits, long before any of
that.

A run's outputs stay where they were written.
[16_running_a_dry_lab_experiment.md](16_running_a_dry_lab_experiment.md)'s preserve-by-default
convention means a run's `manifest.yaml`, `metrics.csv`, and any committed figure are never overwritten
or deleted by later work — they sit in the theme's `details/` folder, in your working copy, whether or
not `src/` has changed since.

The doc site renders those same committed figures directly
([20_documentation_and_doc_sites.md](20_documentation_and_doc_sites.md)): a theme's page shows a run's
actual result, not a live re-computation of it. Nothing needs to be rerun just to look at what a past
experiment found — the figure and the numbers are already sitting there, on disk, committed.

That is what makes it safe to not be precious about code. You can prune an approach out of `src/`
whenever you want, refactor a function, even delete a module — and a run that used the old version
stays fully visible and readable, because its figure and numbers were already committed and never
depended on that code continuing to exist or still working.

If a result ever does need to be regenerated, not just viewed — a reviewer asks you to extend it, or
you want to double-check it after a dependency update — the manifest is what makes that possible: its
commit hash, its inputs, and its data checksum together describe exactly which code, on exactly which
data, produced this. Check out that commit, restore that data, rerun, and you get the same result back.

This rewards committing often. Every commit that a run's manifest can point to is a state you can
return to later; the more of them there are, the smaller the gap between what you have now and the
last state you know you can reproduce.

A run only reaches that state cleanly when the code behind it is actually committed, not left as
uncommitted changes on disk — [16_running_a_dry_lab_experiment.md](16_running_a_dry_lab_experiment.md)
covers *finalizing* a run, a rerun on cleanly committed code, for exactly this reason. Training an AI
assistant to do that finalizing rerun as a matter of course is part of what makes a manifest's address
reliable rather than aspirational.

None of this has an equivalent in Excel, Prism, or a folder of scripts nobody is tracking. In those
tools, keeping an old result usually means manually saving a duplicate file, and there is no compact
way to answer "what exact process produced this specific number" months later except remembering it
yourself, or reconstructing it by hand. Here, that answer is a commit hash.

## Reproducibility versus a clean library: the decision

A tempting mistake: *"If I delete the old approach from `src/`, I can't reproduce the paper that used it, so I'll keep it around, just hidden."* Usually the hiding is done by leaving the module in place but not importing it in `__init__.py`.

That does not work, and it is worth understanding why. **`__init__.py` controls the *exposed* public API, not what *installs*.** Every module in `src/` still ships, still gets imported by something eventually, and still has to be maintained when a dependency changes. Hiding an old approach behind `__init__.py` does not remove its cost; it just makes the cost invisible. It is a permanent maintenance tax, not a solution.

The real resolution keeps the two goals separate:

1. Tag the exact state used for the paper, for example `paper-v1`, so it is frozen. This snapshot still contains *every compared approach* (in `src/`) and the experiment drivers (in `experiments/`) — which is what reproduces the paper's comparison figures, not merely the winning result. (Archiving that tag for a citable DOI is [23_concluding_a_project.md](../disseminating/23_concluding_a_project.md); here it is enough that the state is pinned.)
2. If you also want a clean, installable library, strip the non-preferred approaches down to the one you're disseminating.

That second step does not have to touch `main` at all. You can make the trim directly on `main`, if
you are happy for `src/` to stay narrowed from here on — or you can make it on a separate branch and
tag *that*, leaving `main` and its history completely untouched. Coming from tools with no real
branching, it is easy to assume a branch means a copy you now have to maintain; it does not. A branch
is another named pointer into the same repository, exactly like the tag in step 1 — creating one costs
nothing, and it does not delete or hide anything sitting on `main`.

Either way, the stripped-down state is not a destructive edit: the full, untrimmed code is still sitting in the `paper-v1` tag and in every commit before it. An experiment that needs the old approach reproduces it by checking out that tag, not by running against whatever `src/` looks like now. (Tags, releases, and branches are [22_versioning_and_releases.md](../disseminating/22_versioning_and_releases.md); Zenodo and DOIs are [23_concluding_a_project.md](../disseminating/23_concluding_a_project.md). Both are the "when you publish" tier.)

So two artifacts diverge at this point, preserved differently. The **shipped library** is the trimmed state — on `main` going forward, or on its own tagged branch — which is what new users install. The **publication snapshot** is the `paper-v1` tag, which keeps every compared approach and the experiment drivers, and reproduces every figure. Both live in the *same* repository: each is a named pointer into shared history, not a separate fork. A fork would be heavier and would drift out of sync; a branch or a tag is just a pointer into commits already in the repository, so either adds no storage and nothing to maintain. Reach for a separate repo only if the paper code and the shipped package genuinely become different projects, which is rare.

**The one exception.** If an alternative approach will be *deliberately used going forward* (not just preserved for the record), then it is a supported option, not dead code. Make it first-class: tested and documented, perhaps in a clearly named `legacy` subpackage. The rule is against *gated-off clutter*, not against genuinely supporting more than one method when you mean to.

## Data still stays out of the repo

Nothing here changes the data rule ([CLAUDE.md](../../CLAUDE.md), [04_environments.md](../onboarding/04_environments.md)): experiments reference their data by path or by DOI rather than committing the dataset. The carve-out is deliberately small — a curated handful of real frames kept as a test or teaching fixture is genuinely useful and allowed; what stays out is the full depth of acquired data. A committed dataset bloats history permanently and is not what makes an experiment reproducible; a pinned code state plus an archived, referenced dataset is. The mechanics for data too big to commit — machine-local roots, DOIs, and checksums that pin *which* data a run used — are covered in [17_working_with_large_data.md](17_working_with_large_data.md).
