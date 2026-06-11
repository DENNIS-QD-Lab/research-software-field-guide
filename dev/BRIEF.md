# DENNIS_helpers documentation build — context for Claude Code

## What we're building
An internal helper-scripts repository for the DENNIS Lab (semiconductor QD synthesis, SWIR imaging) plus a documentation set that onboards new lab members from near-zero software experience to confident contributors. The audience is bright but inexperienced graduate students. They are scientists, not software engineers. Documentation must define vocabulary on first use and not assume prior tooling familiarity.

## Tooling choices already made
- **Editor:** VS Code (assume installed, with Python and Jupyter extensions)
- **Environment manager:** conda (Miniconda)
- **Version control:** Git + GitHub
- **Notebook hygiene:** nbstripout via pre-commit. Config in `.pre-commit-config.yaml`:
```yaml
  repos:
    - repo: https://github.com/kynan/nbstripout
      rev: 0.9.1
      hooks:
        - id: nbstripout
```
- **OS coverage:** Mac and Windows. Linux not expected; do not write Linux-specific paths.
- **Workflow path:** GUI primary (VS Code Source Control panel), CLI shown as the equivalent. Not the other way around.

## Pedagogical stance
Opinionated by default, flexible by reference. Tutorials pick one path. Where alternatives exist (venv vs conda, PyCharm vs VS Code, CLI Git vs GUI Git), acknowledge in one or two sentences that they exist and move on. Do not teach the alternative.

## Style requirements
- Limit em-dash use
- No bullet points in formal narrative sections; bullets are fine for step lists and reference enumerations
- Assertive, concise prose. Avoid AI-typical flourishes ("excited to introduce," excessive exclamation points, "let's dive in")
- Target length per doc: 1 to 3 screens of reading
- Define vernacular on first use, inline, briefly
- When introducing a command, show the exact command in a code block and then say in plain English what it does

## Repo structure to create
```
DENNIS_helpers/
├── README.md
├── CONTRIBUTING.md
├── .pre-commit-config.yaml
├── .gitignore                     (use a solid Python+Jupyter default)
├── environment.yml                (minimal: python, numpy, h5py, matplotlib, jupyter, ipykernel)
├── docs/
│   ├── 00_python_code_basics.md
│   ├── 01_command_line_basics.md
│   ├── 02_using_vs_code.md
│   ├── 03_getting_started_with_git.md
│   ├── 04_environments.md
│   ├── 05_daily_workflow.md
│   ├── 06_adding_a_script.md
│   ├── 07_notebooks.md
│   └── 08_code_review.md│   
├── scripts/
│   └── show_h5_keys.py            (worked example, used in 00, 01, and 06)
└── notebooks/
    └── show_h5_keys.ipynb         (the .ipynb pairing, referenced in 07_notebooks.md)
```

## Per-doc content briefs

### 00_python_code_basics.md
- `.py` files vs `.ipynb` files: what each is, when to use which
- Inside a notebook: markdown cells vs code cells
- Anatomy of a Python file: imports, variables, functions (`def`), classes (very brief, one paragraph, "you'll see these but probably won't write them at first"), top-level code
- Docstrings: what they are, the triple-quoted convention, why they matter for `help(function_name)`
- Type hints: what they look like (`def f(x: int) -> str:`), what they do (and crucially, what they don't do: Python does not enforce them at runtime)
- `if __name__ == "__main__":` — explain in plain English. "This block runs when you execute the file directly from the command line, but not when you `import` it from another script. It's the standard way to make a file usable both as a library and as a script."
- A short worked example using `show_h5_keys.py` to point at each of these elements

### 01_command_line_basics.md
- Terminal / shell / command line are roughly synonymous for our purposes
- Where you are matters: `pwd` shows it
- Listing files: `ls` (Mac) or `dir` (Windows) — but VS Code's terminal on Windows often uses Git Bash or PowerShell where `ls` works too. Recommend `ls`.
- Moving around: `cd foldername`, `cd ..`, `cd ~`
- The working directory question, addressed head-on: "When you run a script, your current directory matters because the script may look for input files using relative paths. Rule of thumb: be in the directory the script expects, which for our helpers is usually the directory containing the data file you want to inspect. The script itself can live anywhere as long as Python can find it."
- Running a script: `python /path/to/show_h5_keys.py mydata.h5` — explain the two arguments (the script path and the data path)
- Conda environment commands:
  - `conda env list` — see all envs
  - `conda activate dennis` — turn one on
  - `conda deactivate` — turn it off
  - `conda list` — see what's installed in the active env
  - `conda install package_name` — install something into the active env
  - `pip install package_name` — fallback when conda doesn't have it; explain briefly when to prefer which
- A short troubleshooting section: "command not found," "no such file or directory," and the classic "I installed it but Python says it's not installed" (almost always: wrong environment active)

### 02_using_vs_code.md
Audience: a lab member who has VS Code installed and has just opened the `DENNIS_helpers` repo. They know nothing about VS Code's conventions beyond "it's an editor."

Sections:

**One folder, one window.** Open the repo folder itself, not a parent folder containing multiple repos. The Source Control panel, the integrated terminal's starting directory, the Python interpreter selection, and the search scope are all tied to the open folder. With multiple repos in one window, all of these become ambiguous or wrong. The standard pattern is one VS Code window per repository, switched between with Cmd+\` (Mac) or Ctrl+\` (Windows). Right-clicking a folder in Finder or File Explorer and choosing "Open with VS Code" spawns a new window directly.

**Workspaces (optional but helpful).** After opening a repo folder, File → Save Workspace As lets you save a `.code-workspace` file (put it outside the repo, e.g. on the Desktop). Double-clicking that file later opens VS Code with the same setup. This is the lightest-weight way to bookmark your projects.

**The Explorer sidebar.** The file tree on the left. Files marked with a colored letter are Git status indicators: M = modified since last commit, U = untracked (Git doesn't know about this file yet), A = staged to be added. Files dimmed in the Explorer are being ignored by Git (per `.gitignore`); they're still on your disk and you can still open them, Git just isn't tracking them.

**The Outline view.** At the bottom of the Explorer sidebar (expand the "Outline" header if collapsed). For a Python file, it lists the functions and classes in that file. Click to jump to them. Useful for navigating longer scripts.

**The integrated terminal.** Terminal → New Terminal opens a shell at the workspace root. This is the same terminal we use for `git`, `conda`, and `python` commands throughout the rest of the docs. Multiple terminals can be open at once (the + icon in the terminal panel); the dropdown switches between them. Cmd+\` (Mac) or Ctrl+\` (Windows) toggles the terminal panel open and closed.

**The Source Control panel.** The third icon down on the far-left activity bar (looks like a branch). This is VS Code's Git UI. It shows files that have changed since the last commit, lets you stage them, write a commit message, and commit. This is the GUI path we recommend for daily work; the equivalent terminal commands are in `05_daily_workflow.md`.

**Selecting the Python interpreter.** Cmd+Shift+P (Mac) or Ctrl+Shift+P (Windows) opens the Command Palette. Type "Python: Select Interpreter" and choose the `dennis` conda environment. VS Code remembers this choice per workspace. More on this in `04_environments.md`.

**Selecting the Jupyter kernel.** When you open a `.ipynb` file, the kernel selector is in the top-right of the notebook editor. It must show the `dennis` environment. If it doesn't, click it and choose the right one. The kernel is selected separately from the Python interpreter and you can have them mismatched, which is a common source of "I installed the package but the notebook says it's missing." More on this in `04_environments.md` and `07_notebooks.md`.

**Markdown preview.** For any `.md` file (including these docs), right-click the file tab and choose "Open Preview," or press Cmd+Shift+V (Mac) or Ctrl+Shift+V (Windows). This renders the markdown nicely instead of showing raw text.

**Don't drag tracked files between folders in the Explorer.** It works, but Git sees the move as "delete here, create there" rather than a rename, which clutters history. For tracked files, use `git mv oldpath newpath` in the terminal instead. For untracked files (the U-marked ones), drag freely.

**Toggle the sidebar.** Cmd+B (Mac) or Ctrl+B (Windows) hides and shows the sidebar. Useful when you want maximum screen real estate for reading or focused editing.

**Keyboard shortcuts worth memorizing.**
- Cmd+P / Ctrl+P: Go to File (fuzzy file search across the workspace)
- Cmd+Shift+F / Ctrl+Shift+F: Find in Files (search file contents across the workspace)
- Cmd+Shift+P / Ctrl+Shift+P: Command Palette (run any VS Code command by name)
- Cmd+\` / Ctrl+\`: toggle terminal
- Cmd+B / Ctrl+B: toggle sidebar



### 03_getting_started_with_git.md
- What you just did and what those words meant: define repository, Git, GitHub, clone, local vs remote
- Why the repo must not live in OneDrive/iCloud/Dropbox (repeat from starter sheet; this is the kind of thing that should be said twice)
- The daily mental model in one sentence: pull, work, commit, push
- One paragraph on branches as a forward reference to 05


### 04_environments.md
- Why environments exist: the "it works on my machine" problem in one paragraph
- Creating the lab environment from `environment.yml`: `conda env create -f environment.yml`
- Activating it: `conda activate dennis`
- Telling VS Code about it: command palette → "Python: Select Interpreter" → pick the dennis env
- **Jupyter kernel selection** (this is where students get stuck): when you open a `.ipynb`, the kernel shown in the top right corner must match the dennis env. If it doesn't, click it and choose the right one. The kernel is the Python environment the notebook will actually execute in, regardless of which interpreter VS Code says is selected for `.py` files.
- **When to restart the kernel:** after installing a new package, after editing a module you imported, when variables are in a weird state and you can't tell why. "Restart and Run All" is your friend.

### 05_daily_workflow.md
- The five-step loop with both GUI and CLI shown
- Commit messages: one line, imperative, present tense ("Add HDF5 inspector" not "Added HDF5 inspector")
- Branches: why we use them even for small changes (practice + keeps main clean), how to make one in VS Code's Source Control panel
- Pull requests: how to open one on GitHub, what to write in the description
- Merge conflicts: the 90% case is "ask for help." Briefly show what conflict markers look like so they recognize them.

### 06_adding_a_script.md
- Where things go (`scripts/` for `.py`, `notebooks/` for `.ipynb`)
- Naming: `verb_noun.py` (`show_h5_keys.py`, `plot_qd_spectra.py`)
- Minimum docstring requirement (at the top of the file): purpose, inputs, example call. Reference `00_python_code_basics.md` for what a docstring is.
- "Does this belong here?" guidance: helpers are small, reusable, not project-specific. Project-specific code goes in that project's own repo.
- Worked example walking through `show_h5_keys.py`

### 07_notebooks.md
- The diff/merge problem with notebooks in one paragraph
- One-time setup after cloning: `pip install pre-commit` then `pre-commit install`
- What you'll see when committing: the hook strips outputs from the committed version; your local working file keeps them
- The .py / .ipynb pairing convention (interactive exploration in the notebook, importable version in the script)

### 08_code_review.md
- Every PR gets one reviewer
- What to look for: does it run, does it have a docstring, does the name make sense, is it duplicating something we already have
- Tone norms: questions over commands, suggest don't demand, assume good intent
- How to approve and merge in the GitHub UI

## Worked example: show_h5_keys.py
Create a real, working script that:
1. Takes one command line argument: the path to an HDF5 file
2. Opens it with h5py
3. Recursively prints all groups and datasets with their shapes and dtypes
4. Has a proper module docstring at the top
5. Has a typed function signature for the main function
6. Uses `if __name__ == "__main__":` to wire up the CLI
7. Can be imported by other scripts as `from scripts.show_h5_keys import show_keys`

This script is referenced as the running example throughout 00, 01, and 06.

## Things deliberately out of scope for this pass
- pytest / testing
- Packaging / pyproject.toml
- Licensing (internal repo)
- Software citation / Zenodo
- GitHub issues, project boards, labels
- Advanced Git (rebase, cherry-pick, stash)

These come later when we extend to the real pipeline repos.

## Build order suggestion
1. `environment.yml` and `.gitignore` (python default gitignore already in repo) and `.pre-commit-config.yaml` first
2. `scripts/show_h5_keys.py` and its `.ipynb` pair (the worked example) next, so docs can reference real code (basic working version of show_h5_keys.ipynb exists... needs documentation added and companion .py to be generated)
3. `README.md` and `CONTRIBUTING.md`
4. `docs/` in numerical order


After each major step, pause and report what was created so I can spot-check before continuing.
