# research-software-field-guide documentation

This folder onboards newcomers from near-zero software experience to confident contributor. Read the onboarding docs in order; they build on each other and define every term on first use. Doc 09 is a hands-on exercise to do once you have read them. The reference docs are for later: skim once so you know what's there, then come back as needed. Once you are a confident contributor, the **implementing track** (docs 10–23) covers the next tier: intermediate research-software engineering for when scripts grow into real pipelines and research projects. If you are already an experienced developer and just want to apply this standard to a repository, the [`repo_kit/`](../repo_kit/) folder at the repository root is a portable kit for exactly that: setting up a new repo, or bringing an existing one up to standard.

## Before you start

The onboarding docs assume VS Code, Git, and conda are installed and that you have already cloned the repository. If that is not yet true, work through [`GETTING_STARTED.md`](../GETTING_STARTED.md) at the repository root first — it is the from-scratch setup sheet that gets you to an open workspace.

## Onboarding sequence

Read these in order. They live in [`onboarding/`](onboarding/).

| Doc | What it covers |
|-----|----------------|
| [00_python_code_basics.md](onboarding/00_python_code_basics.md) | How a Python file is put together: `.py` versus `.ipynb`, functions, docstrings, type hints, and `if __name__ == "__main__":`. |
| [01_command_line_basics.md](onboarding/01_command_line_basics.md) | Navigating the terminal, running a script, the conda commands you need, and common error messages. |
| [02_using_vs_code.md](onboarding/02_using_vs_code.md) | VS Code conventions: one folder per window, the Explorer and Source Control panels, the integrated terminal, interpreter and kernel selection, and key shortcuts. |
| [03_getting_started_with_git.md](onboarding/03_getting_started_with_git.md) | What Git and GitHub are, why the repo stays out of synced folders, branches, and the pull-work-commit-push model. |
| [04_environments.md](onboarding/04_environments.md) | Why environments exist, creating and activating the `helper` environment, and the Jupyter kernel trap. |
| [05_daily_workflow.md](onboarding/05_daily_workflow.md) | The five-step daily loop in both VS Code and the terminal, commit messages, branches, pull requests, and merge conflicts. |
| [06_adding_a_script.md](onboarding/06_adding_a_script.md) | Where files go, the naming conventions, the docstring requirement, and a walkthrough of the worked example. |
| [07_notebooks.md](onboarding/07_notebooks.md) | Why notebooks need special handling, the one-time pre-commit setup, and the `.py` / `.ipynb` pairing convention. |
| [08_code_review.md](onboarding/08_code_review.md) | What a reviewer checks, the tone norms, and how to approve and merge. |

## Practice

| Doc | What it covers |
|-----|----------------|
| [09_first_contribution_exercise.md](onboarding/09_first_contribution_exercise.md) | A walkthrough exercise for your first contribution. Recommended after reading 00 through 08. |

## Reference

Topical references you'll return to. They live in [`reference/`](reference/). No reading order; skim the list and come back as needed. (Use Ctl/Cmd+Shift+F to search the whole repository for keywords as needed.)

| Doc | What it covers |
|-----|----------------|
| [advanced_git.md](reference/advanced_git.md) | Sharp Git tools for longer-lived branches: `git stash`, `git rebase` (defensively), `git cherry-pick`, and keeping a feature branch current. A catalog to look things up in, not a tutorial. |
| [ai_coding_assistants.md](reference/ai_coding_assistants.md) | Installing an AI coding assistant, essential session commands (`/clear`, `/compact`, permissions), managing context and cost, and when multi-agent delegation helps versus adds overhead. |
| [cs_jargon.md](reference/cs_jargon.md) | Programming terms of art (snake_case, mutable, parse, refactor, etc.) defined briefly. |
| [git_recovery.md](reference/git_recovery.md) | Recovering from common Git mistakes: work done on the wrong branch, a bad commit, a file you need back, and other "what just happened" moments. |
| [git_vocabulary.md](reference/git_vocabulary.md) | Git and GitHub terms (fetch, pull, push, HEAD, origin, upstream, conflict, and others) you'll encounter. |
| [keyboard_shortcuts.md](reference/keyboard_shortcuts.md) | VS Code shortcuts worth memorizing, organized by category. |
| [markdown_formatting.md](reference/markdown_formatting.md) | Markdown syntax for docs, README files, PR descriptions, and notebook cells. |
| [notebook_sync_alternatives.md](reference/notebook_sync_alternatives.md) | Notebook version control approaches considered and why nbstripout was picked for now. |
| [vs_code_extensions.md](reference/vs_code_extensions.md) | Recommended VS Code extensions for this repo, with notes on what each does. |

## Implementing track

The implementing track ([`implementing/`](implementing/)) picks up where onboarding leaves off: the intermediate research-software-engineering skills for when your scripts grow into real pipelines and research projects. Read the onboarding track first. It is organized in three parts, read in order: **build code you can trust**, **run experiments rigorously**, and **share, sustain, and conclude**. Doc 10 is the bridge from scripts to pipelines and sets up the workflow the rest of the track assumes, so it comes first. The middle part (16–19) is a dry-lab research framework — how to run and record experiments so they stay reproducible, and how to use AI assistants responsibly and effectively within it. Documentation and doc sites (20) is a core practice, not a publishing afterthought. The distribution-tier docs (21–23) are optional until a project is actually being published.

Once you know the track, the [`repo_kit/`](../repo_kit/) folder at the repository root distills it into a portable kit — a summary of the decisions, an AI setup/upgrade playbook, and a `CLAUDE.md` template — that you can drop into another repository to bring it up to the same standard.

### Part I — Build code you can trust

| Doc | What it covers |
|-----|----------------|
| [10_from_scripts_to_pipelines.md](implementing/10_from_scripts_to_pipelines.md) | The bridge doc: signs you've outgrown the simple workflow, feature-branch and multi-root-workspace habits for pipeline-scale work, and when *not* to add complexity. |
| [11_code_quality_tools.md](implementing/11_code_quality_tools.md) | Linting, formatting, and type checking: `ruff check`, `ruff format`, and `mypy`, run by hand and via pre-commit. |
| [12_testing_with_pytest.md](implementing/12_testing_with_pytest.md) | Why and how to test: `test_*` functions, `np.testing.assert_allclose` for floats, `parametrize`, fixtures, and turning validation experiments into regression tests. |
| [13_software_design.md](implementing/13_software_design.md) | Keeping code easy to follow: decomposition, cohesion and single responsibility, and when a function, module, or class earns its keep. |
| [14_continuous_integration.md](implementing/14_continuous_integration.md) | Running your checks automatically on every push with GitHub Actions, across a macOS/Windows matrix, and reading a failed run. |

### Part II — Run experiments rigorously

| Doc | What it covers |
|-----|----------------|
| [15_experiments_and_shipping.md](implementing/15_experiments_and_shipping.md) | One repo, two jobs: a `src/` library plus dated `experiments/`, with graduation and pinning so a paper stays reproducible while the library stays clean. |
| [16_running_a_dry_lab_experiment.md](implementing/16_running_a_dry_lab_experiment.md) | Running a computational experiment as a lab notebook: the research log, the experiment-folder template, and saving each run's state (commit, inputs, parameters) so results reproduce and stay trackable without bloating the repo. |
| [17_working_with_large_data.md](implementing/17_working_with_large_data.md) | Experiments on real datasets too big to commit: referencing data by a machine-local root or a DOI, and pinning *which* data a run used with checksums. |
| [18_ai_assisted_development.md](implementing/18_ai_assisted_development.md) | Using AI assistants responsibly: the standards file, reviewing every change, validation vs. verification, and the state/procedure/standards instruction split. AI writes code; you do the science. |
| [19_driving_an_ai_assistant.md](implementing/19_driving_an_ai_assistant.md) | The practical companion to 18: writing a standards file that actually gets followed, scoping a session on purpose, planning before diffing, and a playbook for catching specific ways confident AI output fails silently. |

### Part III — Share, sustain, and conclude

| Doc | What it covers |
|-----|----------------|
| [20_documentation_and_doc_sites.md](implementing/20_documentation_and_doc_sites.md) | Turning docstrings into a browsable Sphinx site as a core review-and-communication tool: NumPy docstrings, autodoc, and local preview. |
| [21_packaging.md](implementing/21_packaging.md) | *(optional)* When a folder of scripts should become an installable package: `pyproject.toml`, the `src/` layout, and editable installs. |
| [22_versioning_and_releases.md](implementing/22_versioning_and_releases.md) | *(optional)* Semantic versioning, git tags and releases, a single source of truth for the version, and CHANGELOGs. |
| [23_concluding_a_project.md](implementing/23_concluding_a_project.md) | *(optional)* Concluding and disseminating: freezing the paper state, archiving to a Zenodo DOI, LICENSE and CITATION.cff, and how the frozen record and the shipped library diverge. |