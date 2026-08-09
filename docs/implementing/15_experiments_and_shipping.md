# Experiments and shipping: one repo, two jobs

Your repo has started holding two kinds of code that pull in opposite directions. There is **exploratory work** that compares approaches to decide which is best, some of which may become paper figures. And there is **the code you intend to ship** (i.e., share with others for their own use), which should present only the one reliable approach. This doc gives a structure that keeps the exploratory work (and the paper) reproducible while the shipped library stays focused on the one preferred approach.

This is the repo-level counterpart to [13_software_design.md](13_software_design.md): the same "one job per unit" idea, scaled up from functions to the whole repository.

## The tension

Experiments decide which approach wins, and a good experiment is worth keeping: it may become a figure, and a reviewer may ask you to reproduce it a year later. The shipped library, meanwhile, should typically offer one clear way to do each thing, the way you settled on. Left in one flat pile, these two goals corrode each other. The shipped code slowly accumulates dead alternatives nobody dares delete, and the experiments quietly stop running because the code moved under them.

## The layout

Separate the two jobs into two places:

```
SWIR_HDR_v2/
├── src/swir_hdr/       the code library (includes all candidate approaches while comparing; trimmed to the preferred one when shipped)
├── tests/              tests for the library (seeded from validation experiments)
├── experiments/        exploratory comparisons; import from src
│   └── <topic>/          README (question + conclusion), code, pinned environment — undated and
│                           permanent; revisited for as long as the topic stays open, with dated run
│                           reports inside it
├── docs/               autodoc doc site for the library (20_documentation_and_doc_sites.md)
└── pyproject.toml
```

`src/swir_hdr/` is the library: the pipeline code that experiments and analyses import. `experiments/` holds self-describing studies, each a standing folder you keep adding dated runs to rather than a folder you make once and leave. Crucially, **experiments import from `src`**; they use the library rather than carrying their own copy of it, so an experiment is a thin script that calls the library with particular inputs and records what happened. This is what keeps a comparison honest: while you are still deciding between approaches, the competing options all live in `src` together, so the experiment tests exactly the code the library ships and never drifts out of sync with a private copy.

Each experiment folder is self-contained: a `README` stating the question it asked and the conclusion it reached, the code that ran it, and a note pinning the environment it needs (see Pinning, below). *How* you actually run one of these experiments and record its state so it reproduces — the research log, the folder template, and per-run provenance — is covered in [16_running_a_dry_lab_experiment.md](16_running_a_dry_lab_experiment.md).

## Two phases, then two disciplines

The library moves through two phases, and conflating them is the usual mistake.

**While you are comparing:** the competing approaches all live in `src` together. They are not clutter, they are live candidates, and keeping them in one place is exactly what lets an experiment import and compare them without drift. In the SWIR_HDR exemplar, for instance, the several competing methods sit together in one library module (`src/swir_hdr/radiance.py`), and the comparison in `experiments/` imports them from there.

**When you ship the clean package:** you commit to a winner and trim the library to it. "The library carries only the proven/preferred approach" describes that shipped end state — not something true from day one, and not the state the *paper* reproduces from. The paper is reproduced from a tag of the full pre-trim code (every approach still present); you trim `main` only *after* cutting that tag (see the decision below).

Two disciplines make the phases work:

**Graduation.** Once a comparison concludes, `src/` stops carrying the also-rans: the losing approaches are stripped out (see the decision below) and any newly chosen approach moves in. The rule is that `src/` does not carry *dead* options, ones no longer under comparison and no longer shipped. It is not a rule that `src/` may only ever hold one approach.

**Pinning.** An experiment stays reproducible through a frozen snapshot, not by running against the latest `main`. Its `README` states exactly how to reproduce it, for example "check out the `paper-v1` tag and run with the pinned environment." This is why seeding randomness matters ([16_running_a_dry_lab_experiment.md](16_running_a_dry_lab_experiment.md)): a pinned, seeded experiment gives the same numbers every time.

## Reproducibility versus a clean library: the decision

Here is the trap, and it is a tempting one: *"If I delete the old approach from `src/`, I can't reproduce the paper that used it, so I'll keep it around, just hidden."* Usually the hiding is done by leaving the module in place but not importing it in `__init__.py`.

That does not work, and it is worth understanding why. **`__init__.py` controls the *exposed* public API, not what *installs*.** Every module in `src/` still ships, still gets imported by something eventually, and still has to be maintained when a dependency changes. Hiding an old approach behind `__init__.py` does not remove its cost; it just makes the cost invisible. It is a permanent maintenance tax, not a solution.

The real resolution keeps the two goals separate:

1. Tag the exact state used for the paper, for example `paper-v1`, so it is frozen. This snapshot still contains *every compared approach* (in `src/`) and the experiment drivers (in `experiments/`) — which is what reproduces the paper's comparison figures, not merely the winning result. (Archiving that tag for a citable DOI is [23_concluding_a_project.md](../disseminating/23_concluding_a_project.md); here it is enough that the state is pinned.)
2. Then strip the non-preferred approaches out of `src/` on `main` and release the clean library.

The stripped code is not lost: it lives on in the tag and in git history. An experiment that needs the old approach reproduces it by checking out the tag, not by running against the latest `main`. The library on `main` stays clean, and the paper stays reproducible, because each is anchored to its own point in history. (Tags and releases are [22_versioning_and_releases.md](../disseminating/22_versioning_and_releases.md); Zenodo and DOIs are [23_concluding_a_project.md](../disseminating/23_concluding_a_project.md). Both are the "when you publish" tier.)

So two artifacts diverge at this point, preserved differently. The **shipped library** is the trimmed `main`, which keeps evolving for new users. The **publication snapshot** is the `paper-v1` tag, which keeps every compared approach and the experiment drivers, and reproduces every figure. Both live in the *same* repository: the snapshot is a tag — a named, immutable point in history — not a separate fork. A fork would be heavier and would drift out of sync; the tag costs nothing and cannot rot. Reach for a separate repo only if the paper code and the shipped package genuinely become different projects, which is rare.

**The one exception.** If an alternative approach will be *deliberately used going forward* (not just preserved for the record), then it is a supported option, not dead code. Make it first-class: tested and documented, perhaps in a clearly named `legacy` subpackage. The rule is against *gated-off clutter*, not against genuinely supporting more than one method when you mean to.

## Data still stays out of the repo

Nothing here changes the data rule ([CLAUDE.md](../../CLAUDE.md), [04_environments.md](../onboarding/04_environments.md)): experiments reference their data by path or by DOI rather than committing the dataset. The carve-out is deliberately small — a curated handful of real frames kept as a test or teaching fixture is genuinely useful and allowed; what stays out is the full depth of acquired data. A committed dataset bloats history permanently and is not what makes an experiment reproducible; a pinned code state plus an archived, referenced dataset is. The mechanics for data too big to commit — machine-local roots, DOIs, and checksums that pin *which* data a run used — are covered in [17_working_with_large_data.md](17_working_with_large_data.md).
