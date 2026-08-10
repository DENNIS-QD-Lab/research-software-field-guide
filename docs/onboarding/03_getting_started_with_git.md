# Getting started with Git

If you cloned this repository (see [GETTING_STARTED.md](../../GETTING_STARTED.md) if you need instructions), you used several tools and terms that deserve definitions. This doc gives the definitions, states one rule that matters more than the rest, and sets up the daily workflow covered in [05_daily_workflow.md](05_daily_workflow.md).

## Definitions

A *repository* (or *repo*) is a project folder whose entire history Git tracks: every change, who made it, and when.

*Git* is the version control software that records that history. It lets many people change the same files without overwriting each other and lets you return to any earlier state.

*GitHub* is a website that hosts repositories online. Git runs on your machine; GitHub stores a shared copy everyone can reach. They are different things with similar names.

To *clone* is to make a local copy of a repository from GitHub onto your machine, history and all. You did this once to get started; you do not clone again.

Your *local* copy is the repository on your machine. The *remote* is the shared copy on GitHub. The daily work is keeping the two in sync deliberately, not by accident.

## One rule: keep the repository out of synced folders

Do not put the repository inside OneDrive, iCloud Drive, or Dropbox. Those services sync files in the background on their own schedule. Git also manages those same files, and the two fight, which corrupts the repository's history in ways that are hard to undo. Keep the repository in a plain folder, for example `~/code/` or `Documents/code/`, that no cloud service is syncing. This is worth saying twice because it is easy to do by accident and painful to fix. It's worth saying a third time because it seems like it works... until it doesn't. Best to never get in the habit. **Sync data to the cloud using a cloud storage server like OneDrive or Dropbox; sync code to the cloud via GitHub.**

## The daily mental model

Four words: pull, work, commit, push.   
**Pull** the latest changes from GitHub so you start current.  
**Work** on the files.  
**Commit** to record your changes in Git's history with a short message.  
**Push** to send those commits up to GitHub so others have them.  

## Branches

A *branch* is a parallel timeline of the entire repository, not a flag on a single file. Every file in the repo is "on" your current branch. When you make a branch, you are making a separate line of history for the whole project that you can change without disturbing the main one.

The main line of history is called the `main` branch. You will not work directly on it. Instead you make your own branch, do the work there, and merge it back into `main` when it is ready.

Three consequences follow from "a branch is the whole repository," and they are worth holding onto:

Switching branches changes the contents of your working directory to match that timeline. Files may appear, disappear, or change content when you switch. This is normal. Git is swapping in the state that branch records, not damaging your work.

When you commit on a branch, the commit is recorded only on that branch until you merge it. Your changes are invisible to `main`, and to anyone working from `main`, until the merge happens.

"Adding a new file on a branch" is shorthand for a sequence: switch to the branch, create the file in your working directory, then stage and commit it. The branch itself does not hold just that one file. It holds the whole repository state, now including your new file.

We make a branch for every change, even a one-file addition, because the workflow is the practice. The cost of branching is almost nothing, and the habit is what matters when changes get larger. [05_daily_workflow.md](05_daily_workflow.md) shows the mechanics of making, using, and merging a branch.

## Further reading

This doc covers what you need to get moving in this repo. For a deeper, general treatment of version control, see Software Carpentry's [Version Control with Git](https://swcarpentry.github.io/git-novice/) (a full self-paced lesson) or The Turing Way's [Version Control](https://book.the-turing-way.org/reproducible-research/vcs/) chapter (why it matters for reproducible research).
