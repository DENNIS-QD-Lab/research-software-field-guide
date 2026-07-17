# Experiments and shipping: one repo, two jobs

Your repo has started holding two kinds of code that pull in opposite directions. There is **exploratory work** that compares approaches to decide which is best, some of which may become paper figures. And there is **the code you intend to ship**, which should present only the one reliable approach. This doc gives a structure that keeps the exploratory work (and the paper) reproducible while the shipped library stays focused on the blessed approach.

This is the repo-level counterpart to `13_software_design.md`: the same "one job per unit" idea, scaled up from functions to the whole repository.

## The tension

Experiments decide which approach wins, and a good experiment is worth keeping: it may become a figure, and a reviewer may ask you to reproduce it a year later. The shipped library, meanwhile, should offer exactly one way to do each thing, the way you settled on. Left in one flat pile, these two goals corrode each other. The shipped code slowly accumulates dead alternatives nobody dares delete, and the experiments quietly stop running because the code moved under them.

## The layout

Separate the two jobs into two places:

```
SWIR_HDR_v2/
├── src/swir_hdr/       shipped library — only the currently blessed approach
├── tests/              tests for the library (seeded from validation experiments)
├── experiments/        exploratory comparisons; import from src
│   └── <dated_topic>/    README (question + conclusion), code, pinned environment
├── docs/               autodoc doc site for the library (16_documentation_and_doc_sites.md)
└── pyproject.toml
```

`src/swir_hdr/` is the library: the pipeline code that experiments and analyses import. `experiments/` holds dated, self-describing studies. Crucially, **experiments import from `src`**; they use the library rather than carrying their own copy of it, so an experiment is a thin script that calls the library with particular inputs and records what happened. This is what keeps a comparison honest: while you are still deciding between approaches, the competing options all live in `src` together, so the experiment tests exactly the code the library ships and never drifts out of sync with a private copy.

Each experiment folder is self-contained: a `README` stating the question it asked and the conclusion it reached, the code that ran it, and a note pinning the environment it needs (see Pinning, below).

## Two phases, then two disciplines

The library moves through two phases, and conflating them is the usual mistake.

**While you are comparing (the phase the exemplar is in now):** the competing approaches all live in `src` together. They are not clutter, they are live candidates, and keeping them in one place is exactly what lets an experiment import and compare them without drift. All four weighting methods sit in `src/swir_hdr/radiance.py`, and the comparison in `experiments/` imports them from there.

**When you publish:** you commit to a winner and trim the library to it. "The library carries only the blessed approach" is this end state, reached by the stripping step described below, not something true from day one.

Two disciplines make the phases work:

**Graduation.** Once a comparison concludes, `src/` stops carrying the also-rans: the losing approaches are stripped out (see the decision below) and any newly chosen approach moves in. The rule is that `src/` does not carry *dead* options, ones no longer under comparison and no longer shipped. It is not a rule that `src/` may only ever hold one approach.

**Pinning.** An experiment stays reproducible through a frozen snapshot, not by running against the latest `main`. Its `README` states exactly how to reproduce it, for example "check out the `paper-v1` tag and run with the pinned environment." This is why seeding randomness matters (`10_from_scripts_to_pipelines.md`, `12_testing_with_pytest.md`): a pinned, seeded experiment gives the same numbers every time.

## Reproducibility versus a clean library: the decision

Here is the trap, and it is a tempting one: *"If I delete the old approach from `src/`, I can't reproduce the paper that used it, so I'll keep it around, just hidden."* Usually the hiding is done by leaving the module in place but not importing it in `__init__.py`.

That does not work, and it is worth understanding why. **`__init__.py` controls the *exposed* public API, not what *installs*.** Every module in `src/` still ships, still gets imported by something eventually, and still has to be maintained when a dependency changes. Hiding an old approach behind `__init__.py` does not remove its cost; it just makes the cost invisible. It is a permanent maintenance tax, not a solution.

The real resolution keeps the two goals separate:

1. Tag the exact state used for the paper, for example `paper-v1`, and archive that tag to Zenodo for a DOI. The paper cites the DOI.
2. Then strip the non-preferred approaches out of `src/` on `main` and release the clean library.

The stripped code is not lost: it lives on in the tag and in git history. An experiment that needs the old approach reproduces it by checking out the tag, not by running against the latest `main`. The library on `main` stays clean, and the paper stays reproducible, because each is anchored to its own point in history. (Tags and releases are `18_versioning_and_releases.md`; Zenodo and DOIs are `19_citation_and_open_science.md`. Both are the "when you publish" tier.)

**The one exception.** If an alternative approach will be *deliberately used going forward* (not just preserved for the record), then it is a supported option, not dead code. Make it first-class: tested and documented, perhaps in a clearly named `legacy` subpackage. The rule is against *gated-off clutter*, not against genuinely supporting more than one method when you mean to.

## Data still stays out of the repo

Nothing here changes the data rule (`../../CLAUDE.md`, `../onboarding/04_environments.md`): experiments reference their data by path or by DOI rather than committing the dataset. The carve-out is deliberately small — a curated handful of real frames kept as a test or teaching fixture is genuinely useful and allowed; what stays out is the full depth of acquired data. A committed dataset bloats history permanently and is not what makes an experiment reproducible; a pinned code state plus an archived, referenced dataset is.

## How this connects

This is where the dev-branch guidance in `10_from_scripts_to_pipelines.md` lands: a long-running branch is a workspace, and a concluded experiment *graduates onto `main` under `experiments/`*. It does not live on the branch forever. The exemplar's own `experiments/` folder was populated exactly this way, from the method-comparison work that used to live on its dev branch.
