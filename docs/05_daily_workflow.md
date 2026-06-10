# Daily workflow

This is the loop you repeat for every change. It is shown with the VS Code Source Control panel first, which is the path the lab recommends, and the equivalent terminal commands second. Use whichever you prefer; they do the same thing.

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

A *pull request* (PR) proposes merging your branch into `main` and is where review happens. After you push a branch, GitHub shows a prompt to open a PR for it; click it, or go to the repository's Pull Requests tab and click "New pull request."

In the description, write what the change does and why, in a few sentences. If it adds a script, say what the script is for and give an example call. Then request a reviewer. `docs/08_code_review.md` covers the review itself.

## Merge conflicts

A *merge conflict* happens when two changes touch the same lines and Git cannot decide which to keep. You will recognize one by markers Git inserts into the file:

```
<<<<<<< HEAD
your version of the lines
=======
the other version of the lines
>>>>>>> main
```

The 90% case is simple: ask for help. Conflicts are routine and not a sign you did anything wrong, and an experienced lab member can resolve one with you in a couple of minutes. Do not delete the markers at random hoping it sorts itself out.
