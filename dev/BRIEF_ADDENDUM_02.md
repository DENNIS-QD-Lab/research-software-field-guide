# BRIEF_ADDENDUM_02 — the research-software practices track

Phases 1 through 4 of `BRIEF.md` and all of `BRIEF_ADDENDUM_01.md` are complete. This
addendum specifies a new tier of documentation that extends the foundations
(onboarding docs 00–09) into the intermediate research-software-engineering practices
taught at the URSSI June 2026 summer school. Do not regenerate existing docs unless a
phase below explicitly asks for it.

## Why this tier exists

The existing onboarding track gets a near-zero-experience student to "confident
contributor" on the basics: Python anatomy, command line, VS Code, Git, environments,
daily workflow, adding a script, notebooks, and code review. The workshop assumed all
of that as prerequisite and taught the next tier: software design, testing, linting and
type checking, continuous integration, documentation sites, versioning, and citation.

Most of the lab did not attend the workshop. This track is the self-study resource that
covers the same ground, adapted to how the lab actually works. It also fills a seam the
onboarding track leaves open: the transition from writing little scripts to developing
real pipelines, where the simple "one branch per edit" workflow and one-repo-per-window
habit stop fitting.

## Scope decision: practices now, distribution later

Cover the practices that improve everyday lab code: the scripts-to-pipelines transition,
software design, structuring a research codebase, testing, linting, formatting, type
checking, continuous integration, and documentation — including autodoc doc sites
(MkDocs), which are a core practice here, not a publication afterthought (see doc 16 for
why).

Treat the narrower *distribution* topics — packaging for PyPI, tagged public releases,
Zenodo DOIs, JOSS submission — as a clearly marked "when you publish" tier. Introduce
them so students know they exist and when they apply, but do not turn every doc into a
packaging tutorial.

## The repository model

This resource spans three repositories plus each student's own work. Every practices doc
should respect this split.

- **`DENNIS_helpers` (this repo): the training hub.** The docs live here and stay
  repo-agnostic. Code shown inline is small and self-contained so a reader can grasp the
  concept without loading a real pipeline. This is what teammates read.
- **`SWIR_HDR_v2` (private, in progress): the reference exemplar.** The lab lead and
  Claude bring this pipeline up to the full standard together — tests, linting, CI,
  design, and a doc site — so a complete, worked, real example exists for the team to
  study. Docs may point to it as "here is what good looks like." This is the showcase,
  not the students' sandbox.
- **Each student's own pipeline: the practice ground.** Students learn by applying each
  practice to code they wrote and understand, the same logic as onboarding doc 09 scaled
  up. They read a doc, look at how the exemplar does it, then do it on their own repo.
- **`SWIR_HDR` (public v1): the eventual distribution example.** Already public, so it is
  the natural place to demonstrate the distribution tier (LICENSE, CITATION.cff, a Zenodo
  DOI) when the team reaches that stage. Referenced, not required reading, until then.

Rule: illustrative snippets in the docs are minimal and synthetic (or simplified
excerpts from public v1). Real repos are the application target, never the required
reading, so a student without access to a private repo can still learn everything from
the docs.

## Session setup for building this track

The docs are built in a session with `DENNIS_helpers`, `SWIR_HDR_v2`, and `SWIR_HDR`
all available, so each new doc can be applied to the exemplar immediately. Use a
VS Code multi-root workspace (Add Folder to Workspace for each repo, then Save Workspace
As, e.g. `dennis_lab.code-workspace` outside all three repos), not a bare parent folder:
a multi-root workspace keeps each repo as its own Source Control root and its own Python
interpreter, whereas opening the parent muddies the interpreter, terminal cwd, and search
scope. The multi-root workspace is taught to students in doc 10, so this build-time setup
and the student-facing guidance stay consistent.

## Applying the track to the SWIR_HDR_v2 exemplar

Neither `SWIR_HDR` nor `SWIR_HDR_v2` is up to standard yet: docstrings exist, but there
is no doc site and no tests. Bring the exemplar up to standard interleaved with the
docs, not in a big push first — write a doc, then apply it to v2 in the same session. The
doc order is also the correct engineering order (tests before CI, tests before design
refactors, repo structure before CI paths), so walking the brief top to bottom builds
v2's infrastructure in dependency order.

Guidance for the applied work, to reflect in the docs where relevant:

- **Apply to the parts that have stabilized, not the experimental frontier.** v2 is under
  active research; hardening code whose approach is still changing only creates churn.
  Harden settled modules and leave the bleeding edge until it settles. Say this in the
  docs so students do not feel behind.
- **Seed the test suite from existing experiments.** v2's dev branch already runs
  experiment examples that validate the approach. Turning "this example should produce
  this result" into `test_*` functions with `np.testing.assert_allclose` is the doc-12
  exercise done on real, meaningful code. These become the regression/validation tests
  that guard the shipped approach.
- **Use v2's real dev branch as doc 10's worked example** for the feature-branch versus
  release-branch discussion, and as doc 14's worked example for the experiment-to-shipped
  lifecycle.

## The experiment-to-shipped-code lifecycle (taught in doc 14; touches docs 10, 13, 18, 19)

The lab's real pattern: experiments decide which approach is best, those experiments may
become a paper, and the shipped software should present only the reliable approach. This
is a big enough topic to get its own doc (14). The summary that the relevant docs share:

```
SWIR_HDR_v2/
├── src/swir_hdr/     shipped library — only the currently blessed approach
├── tests/            tests for the library (seeded from validation experiments)
├── experiments/      exploratory comparisons; import from src; may become paper figures
│   └── <dated_topic>/  README (question + conclusion), code, pinned environment
├── docs/             autodoc doc site for the library
└── pyproject.toml
```

Principles, threaded into the relevant docs:

- The shipped library carries only the currently blessed approach. Keeping it focused may
  mean graduating a new approach in *or* stripping an old comparison approach out; either
  way `src/` does not accumulate dead options. (doc 14, building on doc 13)
- Reproducibility of a paper comes from a frozen snapshot, not from keeping inferior code
  alive in the live library. Note the specific trap: `__init__.py` controls the *exposed*
  public API, not what *installs* — every module still ships and must be maintained. So
  hiding old approaches behind `__init__` is not a real solution; it is a maintenance tax.
  (doc 14)
- The resolution: tag the exact state used for the paper (e.g. `paper-v1`) and archive it
  to Zenodo for a DOI; the paper cites the DOI. Then strip the non-preferred approaches
  from `src/` on `main` and release the clean library. The stripped code lives on in the
  tag and git history, so experiments that depend on it are reproduced by checking out the
  tag, not by running against the latest `main`. (doc 14, cross-referencing docs 18 and 19)
- The dev branch is a workspace for in-progress experimentation, not a permanent archive.
  A concluded experiment graduates onto `main` under `experiments/`; it does not live on
  the branch forever. (doc 10)

## Where these docs live

Create a new sibling folder to `onboarding/` and `reference/`, and add one new reference
doc:

```
docs/
├── onboarding/          (existing, docs 00–09)
├── reference/           (existing + advanced_git.md)
└── practices/           (new — docs 10–20, doc 20 optional)
```

Numbering continues from the onboarding sequence (10+) so the whole set reads as one
progression. Each doc follows the established style: opinionated by default, define
vocabulary on first use, GUI path primary where one exists with the CLI equivalent
shown, assertive concise prose, limited em-dashes, 1 to 3 screens of reading, and every
command shown in a code block followed by a plain-English explanation.

## Division of responsibility: practices teach decisions, references catalog commands

Practices docs teach *decisions and workflow* (when to branch per feature, when a doc
site is worth building). Reference docs catalog *commands* (how to stash, how to rebase).
The scripts-to-pipelines framework is a decision, so it is taught in doc 10; the sharp
Git tools it points to (stash, rebase, cherry-pick) are cataloged in
`reference/advanced_git.md`. This is how the track honors "advanced Git is deferred from
the tutorial" while still giving people a reference the moment they hit it.

## Per-doc content briefs

### 10_from_scripts_to_pipelines.md  (the bridge doc — first in the track)
Audience: someone fluent in the onboarding workflow whose scripts are turning into a
multi-file pipeline, and who is starting to feel the simple workflow strain.

Purpose: name the transition and give the "time to step it up" framework. This doc is
first because its two subjects — the multi-root workspace and feature branches — are
prerequisites for doing the rest of the track's work on a real pipeline.

- The signs you have outgrown the simple workflow: many files, work that spans days, more
  than one thing in flight, more than one repo open at once.
- **Branching as projects scale.** The onboarding "one branch per edit" model is GitHub
  Flow, and it scales further than people expect. What changes: a branch now represents a
  *feature or experiment* (multiple commits, lives days not minutes), named for the
  feature (`add-dark-frame-correction`), not the file. Keep feature branches short-lived
  and merge `main` in regularly so conflicts stay small. Use draft PRs for
  work-in-progress so a teammate can look early (ties into the doc-site review practice in
  doc 16).
- **When not to add complexity.** Explicitly steer away from a permanent `dev`/`develop`
  branch and the full Git Flow model. That machinery exists for scheduled versioned
  releases to outside users; for an internal pipeline it is pure overhead. The trigger to
  reconsider is the distribution tier (tagged public releases of `SWIR_HDR`), not now.
- **The multi-root workspace.** Working across several repos at once (a pipeline plus its
  helpers) needs more than one-folder-one-window. Teach Add Folder to Workspace and Save
  Workspace As, why a multi-root workspace beats opening a bare parent folder (each repo
  keeps its own Source Control root and Python interpreter), and the caveat to confirm the
  interpreter/kernel per folder. State plainly that one-folder-one-window (doc 02) remains
  the right default for single-repo work; this is the deliberate step up.
- Pointer to `reference/advanced_git.md` for stash, rebase, and cherry-pick when they
  come up, without teaching them here.

### 11_code_quality_tools.md
Audience: a contributor comfortable with the daily workflow who has seen ruff mentioned
in `CLAUDE.md` but never run it directly.

- What linting, formatting, and type checking are, and how they differ from each other.
- `ruff format` (layout) and `ruff check` (problems), with the exact commands and what
  each does. Note these are already wired into the pre-commit hook, so most of the time
  they run automatically on commit; show how to run them by hand too.
- `ruff check --fix` versus what must be fixed manually.
- Type checking with mypy: what static type checking buys you (catches type mismatches
  before you run), the `mypy path/to/file.py` command, and that type hints are for
  humans and checkers, not enforced at runtime (cross-reference 00).
- One-time setup recap: `pre-commit install`, and running `pre-commit run --all-files`
  the first time to bring an existing repo up to standard.
- Reading a ruff error: rule codes, and how to look one up.

### 12_testing_with_pytest.md
Audience: a scientist who has never written an automated test.

- Why tests: they catch silent breakage, and they let you change code with confidence.
  Frame around the scientist's fear: "did my refactor change the numbers?"
- The kinds of tests, briefly: unit (one function), integration (units together),
  regression (a bug you fixed stays fixed). Keep it short; most lab tests are unit tests.
- Anatomy of a test: a function named `test_*`, an `assert`, what pytest reports.
- Running tests: `pytest tests/` and reading pass/fail output.
- Numerical assertions for scientific code: `np.testing.assert_allclose` and why exact
  equality is the wrong tool for floats.
- `@pytest.mark.parametrize` to run one test over many inputs.
- Fixtures and `conftest.py` for shared setup, at an introductory level.
- Where tests live (`tests/`), naming, and the habit of adding a test when you fix a bug.
- Seeding real tests from existing validation experiments (see "Applying the track to the
  SWIR_HDR_v2 exemplar" above and doc 14): an experiment that established the winning
  approach becomes the regression test that guards it.

### 13_software_design.md
Audience: someone whose scripts have grown into a tangle and who senses there is a
better way but cannot name it.

- The goal in one sentence: minimize the mental effort required to reason about the code.
- Decomposition: splitting a long function or script into small pieces that each do one
  thing (reinforces the "keep functions short" rule in CLAUDE.md).
- Cohesion and the single responsibility idea, in plain terms.
- When to make a function, when to make a module, when a class earns its keep. Keep
  classes light: most lab code is functions and modules.
- A brief, concrete before/after refactor of a small tangled example.
- Forward pointers only: dataclasses for grouping related values, and abstract base
  classes for a shared interface across variants (e.g. multiple data sources). One
  paragraph each; do not turn this into an OOP course.
- Keep this doc focused on design *within* a codebase. Repo-level structure — separating a
  reusable library from one-off experiments — is its own topic; hand off to doc 14.

### 14_experiments_and_shipping.md
Audience: someone whose repo now holds both exploratory approach-comparison work and the
code they intend to ship, and who needs a structure that keeps the paper reproducible
while shipping only the reliable approach. This is the direct answer to "repeat the
experiments but ship focused software."

- The tension: experiments decide which approach wins and may become a paper; the shipped
  library should present only the blessed approach; the two goals pull in opposite
  directions.
- The layout: `src/` (shipped library, one blessed approach), `experiments/<dated_topic>/`
  (self-describing: question, conclusion, code, pinned environment), plus `tests/` and
  `docs/`. Experiments import from `src`; they are not part of the shipped API.
- Two disciplines that make it work:
  - **Graduation.** The shipped library carries only the currently blessed approach.
    Sometimes a new approach moves in; sometimes an old comparison approach is stripped
    out. Either way `src/` stays focused and does not accumulate dead options.
  - **Pinning.** Experiments stay reproducible through a frozen snapshot, not by running
    against the latest `main`. Each experiment README states how to reproduce it
    (e.g. `git checkout paper-v1`).
- The reproducibility-versus-clean-shipping decision, stated with the recommended answer:
  - Do not keep inferior approaches alive in the shipped package to preserve
    reproducibility. Name the trap directly: `__init__.py` controls the *exposed* public
    API, not what *installs*; every module still ships and must be maintained, so hiding
    old approaches behind `__init__` is a permanent maintenance tax, not a real fix.
  - Instead: tag the exact paper state (`paper-v1`), archive to Zenodo for a DOI (the paper
    cites the DOI), then strip the non-preferred approaches from `src/` on `main` and
    release the clean library. The stripped code lives on in the tag and git history;
    experiments that need it are reproduced by checking out the tag.
  - Cross-reference doc 18 (tags and releases) and doc 19 (Zenodo, DOIs, citation).
- The one exception: if an alternative approach will be *deliberately used* going forward,
  it is a supported option, not dead code — make it first-class (tested, documented,
  e.g. a `legacy` subpackage), not gated-off clutter.
- Data stays out of the repo (cross-reference CLAUDE.md and doc 04); experiments reference
  data by path or DOI, never by committing it.
- Connects to doc 10 (the dev branch is a workspace; concluded experiments graduate to
  `main` under `experiments/`) and doc 13 (this is repo-level modularity).

### 15_continuous_integration.md
Audience: someone who now writes tests locally and wonders how to make them run
automatically.

- What CI is: your checks (tests, ruff, mypy) run automatically on a fresh machine every
  time you push or open a PR, so "works on my machine" is caught.
- GitHub Actions basics: workflows live in `.github/workflows/`, a workflow is YAML, it
  has triggers and jobs.
- A minimal annotated `ci.yml` that installs the environment and runs the tests and ruff.
- Matrix testing across operating systems: recommended for this lab, not optional,
  because members work on both Mac and Windows and OS-specific bugs (path handling, line
  endings, floating-point differences) are real. Show a matrix over macOS and Windows,
  and briefly over Python versions.
- Reading a failed CI run on GitHub and finding the log.
- Cross-reference 08 (code review): CI is the automated half, review is the human half.

### 16_documentation_and_doc_sites.md
Audience: someone who writes docstrings (per CLAUDE.md) and is ready to turn them into a
browsable site the whole team can read.

This is a core practice, not a "when you publish" step. The doc site is a
review-and-communication tool for the lab: a reviewer can walk through the shape of a
colleague's analysis at the doc-site level without getting lost in individual lines of
code. Frame it that way and cross-reference 08 (code review) and the draft-PR habit from
doc 10.

- The documentation hierarchy: README, comments explaining why, self-documenting names,
  docstrings, and a generated site — layered onto normal work, not a separate project.
- Docstring styles: pick NumPy style for the lab (structured Parameters/Returns/Examples
  sections). Show one full example, consistent with the CLAUDE.md docstring rule.
- Autodocumentation, defined: generating a browsable HTML reference straight from
  docstrings, so the docs cannot drift from the code.
- Tool choice, stated once in the "opinionated by default, flexible by reference" style:
  autodoc tools exist in two families — Sphinx (reStructuredText, or Markdown via MyST)
  and MkDocs (Markdown-native). The lab uses **MkDocs with the Material theme and the
  mkdocstrings plugin**, because the whole docs corpus is already Markdown and the setup
  is low-friction. Acknowledge Sphinx in a sentence (its strengths are intersphinx
  cross-linking and being the scientific-Python norm) and move on; do not teach it.
- Setup, shown concretely: the `mkdocs.yml` config, the `mkdocs-material` theme, the
  `mkdocstrings[python]` plugin configured for NumPy-style docstrings, a `reference` or
  `api.md` page using the `::: swir_hdr.module` autodoc directive, `mkdocs serve` for live
  local preview, and publishing to GitHub Pages with `mkdocs gh-deploy` or a GitHub
  Actions workflow so the site rebuilds on every push.
- Dependency note: mkdocs, mkdocs-material, and mkdocstrings[python] are new dependencies.
  Per CLAUDE.md, adding them requires asking and updating `environment.yml`; flag this in
  the PR that introduces the doc site.
- A short "reviewing analyses at the doc-site level" subsection describing the lab's
  practice of walking the team through a doc site instead of a line-by-line read.

### 17_packaging.md  (distribution tier — mark as optional/when-you-publish)
Audience: someone whose helper collection is being imported across several projects and
is wondering whether it should become an installable package.

- The graduation question: when does a folder of scripts become a package? Signals:
  other repos import it, you copy-paste it between projects, you want versioned installs.
- What `pyproject.toml` is and the `src/` layout, at a conceptual level.
- Editable installs (`pip install -e .`) for local development.
- Keep PyPI publishing out of scope here; name it as the next step and stop.
- Explicit note: `DENNIS_helpers` itself is intentionally not packaged; this doc is for
  when a real project (e.g. `SWIR_HDR`) is ready to be installed.

### 18_versioning_and_releases.md  (distribution tier — mark as optional)
Audience: someone maintaining a project others depend on.

- Semantic versioning: MAJOR.MINOR.PATCH and what each bump means, plus the 0.x
  "unstable" convention.
- Git tags and GitHub releases as the mechanism, including the `paper-v1`-style snapshot
  tag from doc 14.
- CHANGELOG as the human-readable companion to version numbers.
- Single source of truth for the version. Keep automated release publishing out of scope.
- This is also the point where a heavier branching model (release branches) could earn
  its keep; cross-reference doc 10's "when not to add complexity" and note the trigger has
  now arrived if the team is cutting scheduled public releases.

### 19_citation_and_open_science.md  (distribution tier — mark as optional)
Audience: someone about to make research software public or cite it in a paper.

- Why software citation matters for reproducibility and credit.
- LICENSE: what choosing one means and that "no license" means "not reusable"; point to
  choosealicense.com rather than recommending one unilaterally.
- CITATION.cff: what it is and the minimal fields.
- Zenodo for a DOI, and JOSS as a path to a citable, peer-reviewed software paper. One
  paragraph each; this is orientation, not a submission guide.
- Anchor examples on public `SWIR_HDR` as the concrete candidate.
- Archiving the paper snapshot (the tag from docs 14 and 18) to Zenodo for a citable,
  reproducible DOI: the paper cites the DOI of a tagged state, which stays reproducible no
  matter how the library evolves afterward.

### 20_ai_assisted_development.md  (optional)
Audience: the whole lab, since they already use Claude Code in this repo.

- How the lab uses Claude Code responsibly: CLAUDE.md as the standards the assistant
  follows automatically, review every generated change, never trust numbers without a
  test.
- Good tasks to delegate versus what still needs a human.
- Reproducibility and honesty norms for AI-assisted research code.
- Keep vendor-neutral in principle but concrete about the lab's actual setup.

### reference/advanced_git.md  (new reference doc, no reading order)
Audience: someone who hit a situation the daily workflow does not cover and needs the
command, not a tutorial. Sits alongside `git_recovery.md` and `git_vocabulary.md`.

- `git stash` and `git stash pop`: park uncommitted work to switch tasks, then restore it.
- `git rebase`, with a clear caution: it rewrites history, so never rebase commits you
  have already pushed and shared. Keep the treatment short and defensive.
- `git cherry-pick`: copy a single commit onto another branch.
- Keeping a feature branch current: merging `main` in, and what a conflict looks like
  (cross-reference `git_recovery.md`).
- Framed as a catalog to look things up in, not a sequence to read through.

## Update docs/README.md

Add a new "Practices" section after "Reference" that lists docs 10–20 with one-line
descriptions in the same style as the existing entries. Note in the section intro that
these build on the onboarding track, that doc 10 is the bridge from scripts to pipelines,
that documentation and doc sites (16) are a core practice, and that the distribution-tier
docs (17–19) are optional until a project is being published. Add `advanced_git.md` to the
Reference list.

## Build order

Each practices doc is written in `DENNIS_helpers`, then immediately applied to the
`SWIR_HDR_v2` exemplar in the same session so the doc and the worked example stay in sync.

1. `10_from_scripts_to_pipelines.md` (bridge; sets up the workspace and branching model
   the rest of the track assumes).
2. `reference/advanced_git.md` (so doc 10 has something to point to).
3. `11_code_quality_tools.md` (also completes the ruff-in-pre-commit story from the
   quick-win change already applied to `.pre-commit-config.yaml`).
4. `12_testing_with_pytest.md`
5. `13_software_design.md`
6. `14_experiments_and_shipping.md` (repo structure settled before CI paths and autodoc
   targets depend on it).
7. `15_continuous_integration.md`
8. `16_documentation_and_doc_sites.md` (core; the intermediate step between testing and
   the distribution tier).
9. `17_packaging.md`, `18_versioning_and_releases.md`, `19_citation_and_open_science.md`
   (distribution tier, grouped).
10. `20_ai_assisted_development.md` (optional).
11. Update `docs/README.md` index.

After each doc, pause and report what was created so it can be spot-checked before
continuing.

## Deliberately still out of scope

- PyPI publishing and automated release workflows.
- JOSS submission mechanics beyond orientation.
- Interactive rebase and history surgery beyond the defensive treatment in
  `reference/advanced_git.md`.

These land when `SWIR_HDR` / `SWIR_HDR_v2` reach the point of needing them.
