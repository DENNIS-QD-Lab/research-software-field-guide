# Setup playbook — bringing a repo to the research-software standard

**For the assistant (Claude Code).** This is the actionable procedure for setting up a new research
repository, or upgrading an existing one, to the standard described in [STANDARD.md](STANDARD.md). Read
STANDARD.md first for the *why*; this file is the *how*.

Use it two ways:
- **New repo** → follow *Mode A · Scaffold*, in order, stopping at the pieces the project actually needs.
- **Existing repo** → *Mode B · Upgrade recipes*, à la carte — apply only the recipe(s) the scientist asks for.

The config skeletons (`ci.yml`, `conf.py`, `pyproject.toml`) are not duplicated here — use the ones in
[14](../docs/implementing/14_continuous_integration.md), [20](../docs/implementing/20_documentation_and_doc_sites.md),
and [21](../docs/disseminating/21_packaging.md) so this kit never drifts from the tutorial.

## Operating rules (every task)

- **Read first:** STANDARD.md, the target repo's `CLAUDE.md` (its standards), and — if touching
  experiments — its `.claude/experiments_playbook.md`. Follow the repo's own standards over any default.
- **The scientist commits.** Prepare changes and a commit-message draft; **ask before committing,
  pushing, or opening a PR**. Work on a feature branch, never directly on `main`.
- **Every change is a draft, not a commit.** Surface a diff for review the way a colleague's PR is
  reviewed. Confident-but-wrong is the failure mode to catch.
- **Verify after every step (the verify gate):**
  - `ruff check .` and `ruff format --check .`
  - `pytest` (must stay green — if you changed structure, only import lines should change)
  - `sphinx-build -W -b html docs docs/_build/html` if the repo has a doc site (`-W` = warnings fail)
  Report what you ran and its result. Never report success you did not verify.
- **Never trust a number without a test.** If generated code produces results, a test guards them
  ([12](../docs/implementing/12_testing_with_pytest.md)). A clean run is not a correct analysis.
- **Ask before adding a dependency**; if approved, update the environment file and note it in the PR.

## Mode A · Scaffold a new repo

Do these in order; stop wherever the project's maturity stops. Early projects often need only 1–2 and 5.

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
2. **Environment + code quality.** Create the environment file; add `ruff` and `pre-commit`; write
   `.pre-commit-config.yaml` (ruff check + ruff format; nbstripout for notebooks, excluding `.ipynb`
   from ruff); `pre-commit install`. ([11](../docs/implementing/11_code_quality_tools.md))
3. **Package layout.** `src/<pkg>/` for method code + `pyproject.toml`; `pip install -e . --no-deps`.
   ([21](../docs/disseminating/21_packaging.md))
4. **Tests.** `tests/` + `pytest.ini` (or `[tool.pytest]`); one real test that runs the code on a
   known input. ([12](../docs/implementing/12_testing_with_pytest.md))
5. **Experiments framework.** See recipe *B5* below — this is the core of the research-notebook job and
   is usually worth doing even when nothing else is.
6. **Doc site.** Recipe *B7*.
7. **CI.** Recipe *B8*.

## Mode B · Upgrade recipes

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
- **Steps:** add `ruff` + `pre-commit` to the env; add `.pre-commit-config.yaml`;
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
  - Add `experiments/_common/` for shared **harness only** (run logging, comparison/plot helpers,
    report embedding) — never method code; drivers import methods from `src/`.
  - Add a small `runlog` helper that writes, per run, a report at the *theme's* top level —
    `<YYMMDD_slug>[_NN].md`, immediately visible without opening a subfolder — plus a matching
    `details/<YYMMDD_slug>[_NN]/` one level down holding `manifest.yaml` (git commit + dirty flag,
    params, inputs + checksum) and `metrics.csv`. The report opens with a one-line `## Summary` and a
    **protected `## Interpretation (scientist)`** section that tooling **never overwrites**. **PRESERVE
    by default** (a rerun gets a fresh `_NN`, kept in sync between the report and its `details/`
    counterpart; never clobber). Keep the split additive if `runlog` already exists and other drivers
    depend on today's shape: a new optional parameter (e.g. `report_dir=`), defaulting to the old
    co-located behavior, lets one driver adopt the split without moving every other driver's runs at the
    same time. ([16](../docs/implementing/16_running_a_dry_lab_experiment.md))
  - Git-ignore heavy artifacts (`*.png`, `*.npy`, scratch) under `details/`; commit only the report,
    `manifest.yaml`, and `metrics.csv`.
- **Verify:** run a driver; confirm the theme-level report + matching `details/` folder + protected
  report section appear, and a rerun does not overwrite the prior run.
- **Don't:** fork method code into a driver; overwrite a preserved run; ever auto-write the
  interpretation section.

### B6 · Normalize docstrings to NumPy style
- **When:** docstrings are missing or mixed-style (blocks a clean doc site).
- **Steps:** add/convert to NumPy-style (summary, `Parameters`, `Returns`, `Examples`) on every public
  function and module. ([20](../docs/implementing/20_documentation_and_doc_sites.md))
- **Verify:** `sphinx-build -W` produces no docstring warnings.
- **Don't:** rewrite what a function does while documenting it.

### B7 · Stand up the Sphinx doc site
- **When:** no browsable API docs.
- **Steps:** `docs/conf.py` with `autodoc` + `napoleon` + `intersphinx` + `myst_parser`, `furo` theme
  (skeleton in [20](../docs/implementing/20_documentation_and_doc_sites.md)); autodoc imports the
  package, so `pip install -e .` first; add an API page via an `automodule` directive; preview with
  `sphinx-autobuild docs docs/_build/html`. Add the new deps to the env file.
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

### B9 · Package for installation
- **When:** other repos import this code, or you want versioned installs.
- **Steps:** `pyproject.toml` (name, version, deps, build backend); `src/` layout; `pip install -e .`;
  a single source of truth for the version (read back via `importlib.metadata`).
  ([21](../docs/disseminating/21_packaging.md), [22](../docs/disseminating/22_versioning_and_releases.md))
- **Verify:** a fresh `pip install -e .` works; `import <pkg>` and `<pkg>.__version__` resolve.
- **Don't:** package a loose helper/script collection that nothing imports.

### B10 · Conclude & disseminate
- **When:** a line of inquiry reaches publication or the software is becoming a shared dependency.
- **Steps:** freeze — **tag** the exact state behind the paper (`paper-v1`) with every compared approach
  still present; **archive** the tag to a DOI (Zenodo); add `LICENSE` and `CITATION.cff`. *Only after
  the tag*, trim `src/` on `main` to the disseminated method. ([23](../docs/disseminating/23_concluding_a_project.md),
  [22](../docs/disseminating/22_versioning_and_releases.md))
- **Verify:** the tag checks out and reproduces a figure; `main` still builds and tests green after the trim.
- **Don't:** delete the old approach before tagging; hide it behind `__init__.py` instead of tagging (it
  still installs and still costs maintenance).

## When a repo already diverges from the standard

Bring it up incrementally, never in one sweep: add the safety net first (B2, B3), then structure (B4,
B5), then surfaces (B6–B8). Each step verifies green before the next. Harden the module the scientist is
working in, not the whole repo at once.
