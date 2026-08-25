# Setup playbook — bringing a repo to the research-software standard

**For your AI coding assistant.** This is the actionable procedure for setting up a new research
repository, or upgrading an existing one, to the standard described in [STANDARD.md](STANDARD.md). Read
STANDARD.md first for the *why*; this file is the *how*. The examples name Claude Code, but nothing here
depends on it.

Use it two ways:
- **New repo** → follow *Mode A: Scaffold*, in order, stopping at the pieces the project actually needs.
- **Existing repo** → *Mode B: Upgrade recipes*, à la carte — apply only the recipe(s) the scientist asks for.

The config skeletons (`ci.yml`, `conf.py`, `pyproject.toml`) are not duplicated here — use the ones in
[14](../docs/implementing/14_continuous_integration.md), [20](../docs/implementing/20_documentation_and_doc_sites.md),
and [21](../docs/disseminating/21_packaging.md) so this kit never drifts from the tutorial. Those docs
live in this guide, so keep it checked out alongside the target repo while working through these
recipes.

## Operating rules (every task)

- **Read first:** STANDARD.md, the target repo's `CLAUDE.md` (its standards), and — if touching
  experiments — its `.claude/experiments_playbook.md`. Follow the repo's own standards over any default.
- **The scientist commits.** Prepare changes and a commit-message draft; **ask before committing,
  pushing, opening a PR, or creating a tag or release**. Work on a feature branch, never directly on
  `main`. A tag or release is never folded into another task's summary — ask about it on its own,
  every time, no matter how routine it looks.
- **Every change is a draft, not a commit.** Surface a diff for review the way a colleague's PR is
  reviewed. Confident-but-wrong is the failure mode to catch.
- **Verify after every step (the verify gate):**
  - `ruff check .` and `ruff format --check .`
  - `pytest` — green once the repo has tests. Before step 4 creates `tests/`, pytest exits with code 5
    ("no tests ran"); that is expected, not a failure. If you changed structure, only import lines
    should change.
  - `sphinx-build -W -b html docs docs/_build/html` if the repo has a doc site (`-W` = warnings fail)
  Report what you ran and its result. Never report success you did not verify.
- **Never trust a number without a test.** If generated code produces results, a test guards them
  ([12](../docs/implementing/12_testing_with_pytest.md)). A clean run is not a correct analysis.
- **Ask before adding a dependency**; if approved, update the environment file and note it in the PR.

## Mode A: Scaffold a new repo

Do these in order; stop wherever the project's maturity stops. Early projects often need only 0–2 and 5.

0. **A repo and an environment to work in.** `git init` (or create the repo on GitHub and clone it).
   Copy [gitignore.template](templates/gitignore.template) → `.gitignore`, and add a root `README.md`.
   Copy [environment.template.yml](templates/environment.template.yml) → `environment.yml`, fill
   `<env-name>` and adjust the package list, then build it:
   `conda env create -f environment.yml && conda activate <env-name>`. Step 2's `pre-commit install`
   needs both a git repository and an activated environment, so neither is optional.
   ([04_environments.md](../docs/onboarding/04_environments.md))

1. **Standards file.** Copy [CLAUDE.template.md](CLAUDE.template.md) → `CLAUDE.md`; fill every
   `<PLACEHOLDER>`. This is what makes every later session follow the conventions automatically.
   Also copy [vscode_settings.template.json](templates/vscode_settings.template.json) →
   `.vscode/settings.json` (merge if one already exists) so Markdown opens rendered by default
   when this repo is opened on its own. `workbench.editorAssociations` turns out to be
   window-scoped: it is silently ignored for anyone who opens this repo as one folder inside a
   multi-root workspace alongside others, so it is not a substitute for the **User** Settings fix
   in [02_using_vs_code.md](../docs/onboarding/02_using_vs_code.md#markdown-preview) — point
   trainees at that doc as the reliable path; this file is a nice-to-have on top of it. If more than
   one person will work in this repo, also copy
   [CONTRIBUTING.template.md](templates/CONTRIBUTING.template.md) → `CONTRIBUTING.md` and fill it in
   from the repo's actual scope; skip it for a solo project.
2. **Code quality.** Copy [pre_commit_config.template.yaml](templates/pre_commit_config.template.yaml) →
   `.pre-commit-config.yaml` (ruff check + ruff format, `rev:` pinned to match `environment.yml`'s
   `ruff=` from step 0; nbstripout for notebooks, excluding `.ipynb` from ruff); `pre-commit install`;
   `pre-commit run --all-files` once. ([11](../docs/implementing/11_code_quality_tools.md))
3. **Package layout.** `src/<pkg>/` for method code + `pyproject.toml`; `pip install -e . --no-deps`.
   ([21](../docs/disseminating/21_packaging.md))
4. **Tests.** `tests/` + `pytest.ini` (or `[tool.pytest.ini_options]` in `pyproject.toml`); one real test that runs the code on a
   known input. ([12](../docs/implementing/12_testing_with_pytest.md))
5. **Experiments framework.** See recipe *B5* below — this is the core of the research-notebook job and
   is usually worth doing even when nothing else is.
6. **Doc site.** Recipe *B7*.
7. **CI.** Recipe *B8*.

## Mode B: Upgrade recipes

Each recipe is independent: *when to use → steps → verify → don't*. Apply only what is asked.

### B1 · Adopt the standards file
- **When:** the repo has no `CLAUDE.md`, or an ad-hoc one.
- **Steps:** copy [CLAUDE.template.md](CLAUDE.template.md) → `CLAUDE.md`; fill placeholders from the repo
  (purpose, structure, package name, domain abbreviations, anything frozen on `main`). If more than one
  person works in the repo and it has no `CONTRIBUTING.md`, also copy
  [CONTRIBUTING.template.md](templates/CONTRIBUTING.template.md) → `CONTRIBUTING.md` and fill it in.
- **Verify:** re-read it; confirm it matches the repo's real layout.
- **Don't:** invent constraints the repo does not actually have.

### B2 · Wire code-quality tools
- **When:** no ruff / pre-commit.
- **Steps:** add `ruff` (pinned exactly) and `pre-commit` to the existing environment file; copy
  [pre_commit_config.template.yaml](templates/pre_commit_config.template.yaml) →
  `.pre-commit-config.yaml`, matching its `rev:` to the pin just added;
  `pre-commit run --all-files` once to bring the whole tree up to standard; fix what it flags.
  ([11](../docs/implementing/11_code_quality_tools.md))
- **Verify:** `ruff check .` and `ruff format --check .` both clean.
- **Don't:** hand-format around the tool, or lint `.ipynb` (exclude them; nbstripout handles notebooks).

### B3 · Add a test suite (and seed a regression)
- **When:** no `tests/`, or results are unguarded.
- **Steps:** create `tests/`; write unit tests for pure functions; for anything with a known-good
  answer, add a regression test that pins it (`np.testing.assert_allclose` for floats). When a
  validation experiment concludes, freeze it as a `test_`. ([12](../docs/implementing/12_testing_with_pytest.md))
- **Verify:** `pytest` green; each test fails if you deliberately break the code it guards.
- **Don't:** assert exact float equality; write tests that only check "it ran without error."

### B4 · Restructure flat → `src/`
- **When:** method code sits at the repo root or is imported by relative-path hacks.
- **Steps:** move modules under `src/<pkg>/`; add `pyproject.toml`; `pip install -e . --no-deps`; update
  the tests' import lines. Tests are the safety net — if behavior is unchanged, **only import lines
  change and the suite stays green**. ([15](../docs/implementing/15_experiments_and_shipping.md),
  [21](../docs/disseminating/21_packaging.md))
- **Verify:** `pytest` green after the move; `import <pkg>` works from any directory.
- **Don't:** do this without tests in place first (add B3 first); change logic during the move.

### B5 · Add the experiments framework
- **When:** the repo runs studies/comparisons but has no reproducible record of them.
- **Steps:**
  - Create `experiments/` and copy the three templates:
    [research_log.template.md](templates/research_log.template.md) → `experiments/README.md`,
    [experiment_readme.template.md](templates/experiment_readme.template.md) → `experiments/_TEMPLATE.md`,
    and [experiments_playbook.template.md](templates/experiments_playbook.template.md) →
    `.claude/experiments_playbook.md`. Fill their placeholders.
  - Add `experiments/_common/` for shared **harness only** (run logging, comparison/plot helpers) —
    never method code; drivers import methods from `src/`. Copy
    [runlog.template.py](templates/runlog.template.py) → `experiments/_common/runlog.py` (needs
    `pyyaml`; add it to the environment file if not already present). It writes, per run,
    **provenance only** — no report file — to `details/<YYMMDD>_<slug>[_NN]/` at the theme's top level:
    `manifest.yaml` (git commit + dirty flag, params, inputs + checksum) and `metrics.csv`. **PRESERVE
    by default** (a rerun gets a fresh `_NN`; pass `overwrite=True` to refresh a run in place instead).
    The theme's own `experiments/<theme-slug>/README.md` (from B5's `_TEMPLATE.md`) is the one
    narrative document — findings, embedded figures, interpretation — written once and updated in place,
    never regenerated per run. A run's figure worth keeping visible gets embedded directly in the
    README's Findings section, from `details/<run_id>/`, with a short italic caption noting the run id —
    a caption rather than a heading, so it does not become a nav entry.
    ([16](../docs/implementing/16_running_a_dry_lab_experiment.md))
  - Also create a root-level `references.md`: the reference ledger, one row per external source with a
    *why it mattered here* note. A table header and a first row is enough to start.
    ([16](../docs/implementing/16_running_a_dry_lab_experiment.md))
  - Git-ignore heavy artifacts (`*.png`, `*.npy`, scratch) under `details/`, and commit `manifest.yaml`
    and `metrics.csv`. The one exception is a figure embedded in a theme's README: it has to be in the
    repo for GitHub or the doc site to render it, so commit that single file with `git add -f`, since it
    matches the ignored `*.png` pattern. Everything else a run produced stays ignored and regenerable.
- **Verify:** run a driver; confirm the `details/` folder appears with a manifest and metrics, and a
  rerun gets a fresh `_NN` instead of overwriting it.
- **Don't:** fork method code into a driver; overwrite a preserved run; have the driver write a
  per-run report file — the README is the report, and its interpretation stays a signed
  `> **<initials>:** _pending._` placeholder until the scientist fills it in, never guessed at.

### B6 · Normalize docstrings to NumPy style
- **When:** docstrings are missing or mixed-style (blocks a clean doc site).
- **Steps:** add/convert to NumPy-style (summary, `Parameters`, `Returns`, `Examples`) on every public
  function and module. ([20](../docs/implementing/20_documentation_and_doc_sites.md))
- **Verify:** `sphinx-build -W -b html docs docs/_build/html` produces no docstring warnings.
- **Don't:** rewrite what a function does while documenting it.

### B7 · Stand up the Sphinx doc site
- **When:** no browsable API docs.
- **Steps:** `docs/conf.py` with `autodoc` + `napoleon` + `intersphinx` + `myst_parser`, `furo` theme
  (skeleton in [20](../docs/implementing/20_documentation_and_doc_sites.md)); autodoc imports the
  package, so `pip install -e . --no-deps` first; add an API page via an `automodule` directive; preview with
  `sphinx-autobuild docs docs/_build/html`. If the repo has experiment themes, add one
  `docs/experiment_overviews/<theme-slug>_overview.md` per theme, whose whole body is the MyST
  `{include}` block from [20](../docs/implementing/20_documentation_and_doc_sites.md) (with
  `:relative-docs:` and `:relative-images:`, or embedded figures silently fail to render), and list them
  in `docs/index.md`'s `toctree`. Pin the new deps in the env file — `sphinx-build -W` makes any new
  warning fatal, so an unpinned builder can fail a build whose content never changed. For a private repo,
  make the built site reachable in CI (20's two appendices): a `workflow artifact` on every push for
  day-to-day review, a `workflow_dispatch`-triggered tagged **release** for a snapshot that needs to
  outlive the artifact's retention window.
- **Verify:** `sphinx-build -W -b html docs docs/_build/html` builds clean.
- **Don't:** paste a bare build path into a browser (it searches) — serve it or use a `file:///` URL.

### B8 · Add continuous integration
- **When:** checks only run locally.
- **Steps:** `.github/workflows/ci.yml` — recreate the env, `pip install -e . --no-deps`, `ruff check` +
  `ruff format --check`, `pytest`, and (if there is a doc site) `sphinx-build -W`. Use an OS matrix
  (`macos-latest`, `windows-latest`). Skeleton in
  [14](../docs/implementing/14_continuous_integration.md) / [20](../docs/implementing/20_documentation_and_doc_sites.md).
- **Verify:** the run is green on every matrix leg; a deliberately-missing dependency fails it (that is
  the point).
- **Don't:** install packages on the runner by hand to make it pass — add them to the environment file.

### B9 · Version for outside consumers
- **When:** other repos import this code, or you want versioned installs — going beyond the local
  package B4 already set up (that step's `pyproject.toml` + `src/` layout + `pip install -e .` are
  assumed done here, not repeated).
- **Steps:** a single source of truth for the version in `pyproject.toml`, read back via
  `importlib.metadata` rather than hardcoded a second time; tag releases (`git tag -a vX.Y.Z -m "..." && git push origin vX.Y.Z`); for a
  lighter step than PyPI, note in the README that `pip install git+<url>` already works.
  ([21](../docs/disseminating/21_packaging.md) "Going further",
  [23](../docs/disseminating/23_shipping_a_library.md))
- **Verify:** `<pkg>.__version__` matches the tag just cut; a fresh clone can `pip install git+<url>`.
- **Don't:** redo B4's `pyproject.toml`/`src/` layout from scratch — this step assumes it's already
  there.

### B10 · Publish a paper
- **When:** a line of inquiry is going out as a publication.
- **Steps:** freeze — **tag** the exact state behind the paper (`paper-v1`) with every compared
  approach still present; **archive** the tag to a DOI (Zenodo); add `LICENSE` and `CITATION.cff`
  (copy [CITATION.template.cff](templates/CITATION.template.cff), fill placeholders).
  If the working repo shouldn't be public as-is, use the two-repo pattern: a fresh, empty public
  repo with only what belongs in the paper's record.
  ([22](../docs/disseminating/22_publishing_a_paper.md),
  [repo_ownership_and_visibility](../docs/reference/repo_ownership_and_visibility.md))
- **Verify:** the tag checks out and reproduces a figure.
- **Don't:** archive from the private working repo without auditing its full history first.

### B11 · Ship a library
- **When:** the software itself is becoming a shared dependency, independent of any paper.
- **Steps:** trim `src/` to the disseminated method — directly on `main`, or on a separate branch you
  tag instead, leaving `main` untouched. This does not require a paper tag first: the commit before the
  trim stays permanently reachable by its hash, so the removed approach is never lost. Tag that commit
  (`pre-trim`) only if you would rather have a memorable name than a hash to look up. Version it
  properly (B9), then publish to PyPI. Give the shipped repo its own front door: a public-facing README
  (install, then a minimal example, not the research question) and a small `examples/` quickstart
  distinct from `experiments/`. ([23](../docs/disseminating/23_shipping_a_library.md))
- **Verify:** wherever you trimmed (`main` or a branch) still builds and tests green; a fresh
  `pip install` followed by the quickstart example actually runs.
- **Don't:** hide an old approach behind `__init__.py` instead of deleting it — it still installs and
  still costs maintenance, and the commit history already preserves it.

### B12 · Add a `figures/` folder for manuscript drafting
- **When:** drafting a specific submission; more than a couple of ad hoc figure scripts are floating
  around.
- **Steps:** one folder per figure (or figure group) under `figures/`, same theme + `details/`
  discipline as `experiments/` — a driver that imports from `src/`, dated attempts accumulating in
  `details/`, the current draft embedded in the folder's `README.md` alongside its caption. Wire the
  README into the doc site the same way an experiment theme's is: a
  `docs/figure_overviews/<fig-slug>_overview.md` page whose body is a MyST `{include}` of the
  figure's own README, so the manuscript's whole figure outline is browsable on the same site.
  ([22](../docs/disseminating/22_publishing_a_paper.md),
  [16](../docs/implementing/16_running_a_dry_lab_experiment.md))
- **Verify:** the doc site renders the figures/README page with the current image and caption visible.
- **Don't:** overwrite a figure in place when it stops earning its spot — let the superseded attempt
  sit in `details/`, same as any other run.

## When a repo already diverges from the standard

Bring it up incrementally, never in one sweep: add the safety net first (B2, B3), then structure (B4,
B5), then surfaces (B6–B8). Each step verifies green before the next. Harden the module the scientist is
working in, not the whole repo at once.
