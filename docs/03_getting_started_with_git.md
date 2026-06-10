# Getting started with Git

If you have just cloned this repository, you used several tools and terms that deserve definitions. This doc gives them, states one rule that matters more than the rest, and sets up the daily workflow covered in `docs/05_daily_workflow.md`.

## The words, defined

A *repository* (or *repo*) is a project folder whose entire history Git tracks: every change, who made it, and when.

*Git* is the version control software that records that history. It lets many people change the same files without overwriting each other and lets you return to any earlier state.

*GitHub* is a website that hosts repositories online. Git runs on your machine; GitHub stores a shared copy everyone can reach. They are different things with similar names.

To *clone* is to make a local copy of a repository from GitHub onto your machine, history and all. You did this once to get started; you do not clone again.

Your *local* copy is the repository on your machine. The *remote* is the shared copy on GitHub. The daily work is keeping the two in sync deliberately, not by accident.

## One rule: keep the repository out of synced folders

Do not put the repository inside OneDrive, iCloud Drive, or Dropbox. Those services sync files in the background on their own schedule. Git also manages those same files, and the two fight, which corrupts the repository's history in ways that are hard to undo. Keep the repository in a plain folder, for example `~/code/` or `Documents/code/`, that no cloud service is syncing. This is worth saying twice because it is easy to do by accident and painful to fix.

## The daily mental model

Four words: pull, work, commit, push. Pull the latest changes from GitHub so you start current. Work on the files. Commit to record your changes in Git's history with a short message. Push to send those commits up to GitHub so others have them.

## A word on branches

You will not work directly on the main line of history, called the `main` branch. Instead you will make a *branch*, which is a parallel line where you can work without disturbing `main`, then merge it back when it is ready. This keeps `main` working at all times. `docs/05_daily_workflow.md` shows how to make and use a branch.
