# Daily workflow

This is the loop you repeat for every change. This can be managed through the VS Code Source Control panel GUI or the equivalent terminal commands. Use whichever you prefer; they do the same thing.

If you mess up the workflow at any point (worked on the wrong branch, committed the wrong thing, anything that feels broken), see `../reference/git_recovery.md`. Don't panic and don't delete anything until you've checked your options.

## Starting new work

Whether you just finished merging a PR or you're sitting down for a fresh session, run these three commands before making any changes:

```
git checkout main
git pull
git checkout -b <descriptive-branch-name>
```

What each does:
1. Switch to the `main` branch.
2. Pull the latest changes from GitHub into your local `main`. This catches anything your labmates merged while you were away.
3. Create a new branch off the now-up-to-date `main`, and switch to it.

(`git checkout -b <name>` and `git switch -c <name>` do exactly the same thing — create a branch and switch to it. You will see both in these docs and online; use whichever you prefer.)

This three-step ritual prevents the most common Git problems before they happen. Skipping step 2 is how branches end up "behind main" and merge conflicts proliferate.

**Branch naming:** short, descriptive, kebab-case (hyphens). Examples: `add-show-keys`, `fix-hdf5-pathing`, `clarify-notebook-docs`. The branch name will appear in the PR title and in your Git history forever, so make it informative.

**Don't reuse branch names from merged PRs.** Once `add-show-keys` has been merged, delete it (`git branch -d add-show-keys`) and start a new branch for the next change. Each branch corresponds to one logical change.


## The five-step loop

**1. Pull the latest changes.** Start current so you are not building on stale code.

In VS Code: open the Source Control panel, click the "..." menu, and choose Pull.

In the terminal:

```
git pull
```

**2. Make a branch.** Work on a parallel line, not directly on `main`.

In VS Code: click the branch name in the bottom-left status bar, choose "Create new branch," and give it a short descriptive name like `add-spectra-plotter`.

In the terminal:

```
git switch -c add-spectra-plotter
```

This creates a branch named `add-spectra-plotter` and switches to it.

**3. Do the work, then commit.** A *commit* is a saved snapshot of your changes with a message describing them.

In VS Code: in the Source Control panel, the changed files appear under "Changes." Hover a file and click + to *stage* it (mark it for the next commit). Type a message in the box at the top and click the Commit button.

In the terminal:

```
git add scripts/plot_qd_spectra.py
git commit -m "Add QD spectra plotter"
```

`git add` stages a file; `git commit` records the staged files with a message.

**4. Push.** Send your commits to GitHub.

In VS Code: click "Sync Changes," or the "..." menu then Push.

In the terminal:

```
git push
```

The first push of a new branch may ask you to set the upstream; follow the command it prints.

**5. Open a pull request.** Covered below.

## Commit messages

Write one line, in the imperative present tense, describing what the commit does. Write "Add HDF5 inspector," not "Added HDF5 inspector" and not "Adds HDF5 inspector." A good message finishes the sentence "If applied, this commit will..." Keep it under about 60 characters and specific.

## Why branches, even for small changes

We branch for every change, even a one-line fix. Two reasons. It keeps `main` working at all times, since unfinished work stays on the branch. And it gives you a low-stakes place to practice the workflow, so the habit is automatic by the time a change is large.

## Pull requests

A *pull request* (PR) proposes merging your branch into `main` and is where review happens. After you push a branch, GitHub shows a prompt to open a PR for it; click it, or go to the repository's Pull Requests tab in GitHub and click "New pull request."

In the description, write what the change does and why, in a few sentences. If it adds a script, say what the script is for and give an example call. Then request a reviewer. `08_code_review.md` covers the review itself.

## Merge conflicts

A *merge conflict* happens when two changes touch the same lines and Git cannot decide which to keep. You will recognize one by markers Git inserts into the file:

```
<<<<<<< HEAD
your version of the lines
=======
the other version of the lines
>>>>>>> main
```

The 90% case is simple: ask for help. Conflicts are routine and not a sign you did anything wrong, and an experienced colleague can resolve one with you in a couple of minutes. Do not delete the markers at random hoping it sorts itself out. (VS Code shows "Accept Current Change" / "Accept Incoming Change" buttons above each conflict, but *which* to keep is a judgment call — when you are unsure, ask before accepting.)
