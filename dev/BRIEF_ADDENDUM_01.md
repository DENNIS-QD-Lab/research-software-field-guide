# BRIEF_ADDENDUM_01 — post-phase-4 changes

Phases 1 through 4 of `BRIEF.md` are complete. This addendum describes changes and additions to apply on top of the existing repo. Do not regenerate phase 1–4 files unless explicitly asked.


## 2. Add `docs/10_notebook_sync_alternatives.md` (reference doc)

A short reference doc describing the three approaches the team considered for notebook version control, so future-us remembers the tradeoffs.

Audience: a returning lab member who wonders "could we be doing this better?" Not for first-time onboarding.

Sections:

**Why notebooks fight with version control.** One paragraph: `.ipynb` files are JSON with embedded outputs and metadata. Diffs are unreadable, merge conflicts are nightmares, and repos bloat with binary image data from plot outputs. Three approaches exist.

**Option 1: Strip outputs and metadata with nbstripout (what we currently use).** The committed `.ipynb` has no outputs and minimal metadata; the local working copy keeps everything. Set up via pre-commit hook. Pros: simple, one tool, students keep working in notebooks the way they already do. Cons: `.ipynb` is still the committed format, so diffs are JSON (better than before, but still not great); no way to import a notebook's functions into another script without converting.

**Option 2: Strip only metadata, keep outputs.** A nbstripout configuration option. Pros: PR reviewers see the actual plots and outputs. Cons: repo size grows with every committed plot, diffs still include base64-encoded images, defeats most of the point of stripping.

**Option 3: Pair `.py` and `.ipynb` automatically with jupytext.** Each notebook has a script twin. Edit either, the other regenerates on save. Only the `.py` is committed; the `.ipynb` is generated locally on demand. Pros: clean text diffs, importable scripts, no output bloat, single source of truth. Cons: students must understand the pairing relationship; one more tool in the stack; some pure-exploration notebooks don't benefit from pairing.

**Current decision.** Option 1 (nbstripout). Revisit if the team finds itself frequently wanting to import notebook code into scripts, or if notebook merge conflicts become common.

## 3. Add `docs/09_first_contribution_exercise.md`

A walkthrough exercise. The student will:

1. Pick a script or notebook they've already written that others might find useful
2. Create a branch named `add-<their-script-name>`
3. Add the file under `scripts/` (for `.py`) or `notebooks/` (for `.ipynb`) following the naming conventions in `06_adding_a_script.md`. Whether to also create a paired version in the other format is a per-helper judgment call; document the choice in the PR.
4. Work with Claude (which will follow `CLAUDE.md` automatically) to add the docstring, type hints, and `if __name__ == "__main__":` block if it's a `.py`. For a `.ipynb`, work with Claude to add a markdown cell at the top describing purpose, inputs, and an example call, plus docstrings on any function definitions.
5. Update `docs/README.md` if the helper adds a new category worth indexing
6. Commit, push the branch, open a PR with a description that explains what the helper does and includes an example invocation
7. Before merging their own PR, review at least one labmate's open PR and leave one substantive comment (a question, a suggestion, or "looks good and here's why")
8. After their own PR has at least one approval, merge it themselves via the GitHub UI and delete the branch

Frame the exercise as practice, not a test. The goal is to put every concept through their hands once, with code they already understand, before they need it under pressure. Estimated time: 30 to 60 minutes once they've read docs 00 through 08.

Include a short "what good looks like" section at the bottom showing a small sample PR description for reference, e.g.:

> **Title:** Add show_h5_keys helper
>
> **Description:**
> Adds a helper script that recursively prints the structure of an HDF5 file (groups, datasets, shapes, dtypes). Useful for inspecting unfamiliar `.h5` files before writing analysis code.
>
> Example invocation: `python scripts/show_h5_keys.py path/to/data.h5`
>
> Tested on a 2 GB SWIR imaging dataset; output truncates cleanly at large file levels.

## 4. Update `docs/index/README.md`

Add entries for the new docs:

- `09_first_contribution_exercise.md` — A walkthrough exercise for your first contribution. Recommended after reading 00–08.
- `10_notebook_sync_alternatives.md` — Reference: notebook version control approaches we considered. Background reading, not required.

## 5. Reinforce the branch explanation in `docs/03_getting_started_with_git.md`

Verify the existing section on branches clearly states that a branch is a parallel timeline of the *entire repository*, not a flag on a single file. If the current wording is buried, ambiguous, or treats branches as a per-file concept, rewrite the relevant section to make it explicit.

The wording should hit these points:

- A branch is a parallel timeline of the entire repository. Every file in the repo is "on" your current branch.
- Switching branches changes the contents of your working directory to match that timeline. Files may appear, disappear, or change content when you switch.
- When you commit on a branch, the commit is recorded only on that branch until merged.
- "Adding a new file on a branch" is shorthand for: switch to the branch, create the file in your working directory, stage and commit it. The branch itself contains the whole repo state including your new file.
- We use branches for every change, even one-file additions, because the workflow is the practice. The cost is low; the habit matters.

Place this clarification near the start of whatever branch discussion already exists. Cross-reference `05_daily_workflow.md` for the mechanics.

## 6. Clarify naming conventions in `docs/06_adding_a_script.md`

Verify the naming conventions section distinguishes between two patterns and explains *why*. If the current wording lumps them together or is vague, rewrite as follows:

> **Naming conventions for files in this repo:**
>
> All filenames use snake_case (lowercase letters and digits, words separated by underscores, no hyphens, no camelCase, no spaces). Keep names under about 30 characters. Avoid abbreviations except universally understood ones in your field (`hdf5`, `hdr`, `nir`, `qd`, `swir` are fine; `seg` for `segmentation` or `proc` for `processing` is not).
>
> Beyond that, we use two grammatical patterns depending on what the file does:
>
> **Verb-first names for action scripts.** If the file's purpose is to *do* a task, name it with a verb followed by what it acts on. The name reads like a command.
>
> Examples: `show_keys.py` (shows the keys), `plot_spectra.py` (plots spectra), `convert_units.py` (converts units), `clean_metadata.py` (cleans metadata).
>
> **Noun-phrase names for functionality modules.** If the file's purpose is to *contain* code that other scripts import and use, name it with a noun or adjective-noun phrase describing what's inside. The name reads like a topic.
>
> Examples: `ratio_analysis.py` (contains ratio analysis code), `hdr_processing.py` (contains HDR processing code), `broadband_segmentation.py` (contains broadband segmentation code).
>
> If you're unsure which category a file falls into, ask: when this file is at the top of a colleague's screen, will they more often think "I want to run this" (verb) or "I want to import from this" (noun)? Pick accordingly. If both, lean toward the verb form and import from it when needed.

## 7. Moved `BRIEF.md` to `dev/BRIEF.md`


Add a brief note to `README.md` near the bottom — one line — that the `dev/` folder contains the design briefs used to build the docs and is kept for historical reference.

## Build order for this addendum

1. Reinforce branch wording in `docs/03_getting_started_with_git.md`
2. Clarify naming conventions in `docs/06_adding_a_script.md`
3. Create `docs/09_first_contribution_exercise.md`
4. Create `docs/10_notebook_sync_alternatives.md`
5. Update `docs/README.md` index entries
6. Add the `dev/` folder note to `README.md`

After each phase, pause and report what changed so I can spot-check.