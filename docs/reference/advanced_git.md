# Advanced Git: tools for when the daily workflow is not enough

The daily workflow (`../onboarding/05_daily_workflow.md`) and `git_recovery.md` cover the common cases. This doc catalogs the sharper tools you reach for occasionally, mostly on the longer-lived feature branches described in `../implementing/10_from_scripts_to_pipelines.md`.

## How to read this doc

Do not read it front to back. Find the tool that matches what you need, use it, and get back to work. It is a reference, not a tutorial.

One safety rule, the same as `git_recovery.md`: before running any command with `--force` in it, or any command that rewrites history (the `git rebase` section below), ask in lab Teams if you are not sure. Those are the commands that can affect other people's work. The rest are safe to experiment with.

---

## Park work to switch tasks: `git stash`

You are partway through a change, with edits you are not ready to commit, and you need a clean working directory: to switch branches, pull the latest, or check something out. Set the edits aside:

```
git stash
```

This takes all your uncommitted changes to tracked files, saves them on a stack, and returns your working directory to a clean state matching the last commit. Your edits are not lost; they are parked.

Do the other task, then come back to your branch and restore them:

```
git stash pop
```

This reapplies the parked changes and removes them from the stack.

A few notes:

```
git stash list
```

Shows everything you currently have stashed, in case you stashed more than once or forgot about one.

```
git stash drop
```

Discards the most recent stash without reapplying it, when you decide you do not want those changes after all.

By default `git stash` leaves *untracked* files (brand-new files git is not tracking yet) in place. To stash those too, use `git stash -u`. There is a worked example of using stash to switch branches safely in `git_recovery.md`.

---

## Keep a feature branch current: merge `main` in

A feature branch that lives for days falls behind `main` as teammates merge their work. Bring `main`'s new commits into your branch so the two do not drift far apart:

```
git switch my-feature-branch
git merge main
```

The first line makes sure you are on your own branch; the second pulls `main`'s new commits into it. Do this often. Small, frequent merges produce small conflicts. If a merge does report a conflict, `git_recovery.md` has the section on reading and resolving the conflict markers.

---

## Copy one commit onto another branch: `git cherry-pick`

You have a single commit on one branch and you want a copy of just that one commit on another branch (for example, you committed a fix to the wrong branch, or you want one useful commit from an experiment).

First find the commit's hash:

```
git log --oneline
```

Each line starts with a short hash like `a1b2c3d`. Switch to the branch you want the commit on, then cherry-pick it:

```
git switch target-branch
git cherry-pick a1b2c3d
```

This copies the change from that commit onto your current branch as a new commit. `git_recovery.md` uses this in its "I committed to the wrong branch" fix.

---

## Work on two branches at once: `git worktree`

You want a second branch checked out *at the same time* as your current one — to compare two versions side by side, run a long job on one branch while you keep editing another, or let an AI assistant work on a change in an isolated copy without disturbing your main checkout. Switching branches in place would churn your working directory; a **worktree** gives you a second working directory for the same repository instead.

```
git worktree add ../myrepo-feature some-branch
```

This creates the folder `../myrepo-feature` with the same repository checked out to `some-branch`. Both folders are live at once — edit, commit, and run in either — and they share one history and `.git` database, so a worktree is far cheaper than a second `git clone`. Use an existing branch, or add `-b new-branch` to create one as you go.

List and remove them:

```
git worktree list
git worktree remove ../myrepo-feature
```

`list` shows every working directory attached to the repo; `remove` deletes one when you are done with it (commit or move anything you want to keep first). A branch can be checked out in only one worktree at a time.

---

## Rewrite history, carefully: `git rebase`

**The one rule: never rebase commits you have already pushed and shared.** Rebasing rewrites history, replacing your commits with new ones that have new hashes. If you rewrite commits other people already have, their copy and yours disagree, and untangling that is a mess for everyone. Only rebase local commits you have not pushed.

With that understood, the common safe use is updating your feature branch onto the latest `main`, as an alternative to merging it in:

```
git switch my-feature-branch
git rebase main
```

This replays your branch's commits on top of the current `main`, giving a straight-line history instead of a merge commit. If a conflict comes up, git pauses so you can resolve it, then:

```
git rebase --continue
```

resumes, or:

```
git rebase --abort
```

bails out completely and returns your branch to exactly where it was before you started, as if the rebase never happened.

When in doubt, prefer `git merge main` (the section above) over rebasing. Merge is safe, never rewrites history, and does the same job of catching your branch up. Reach for rebase only when you specifically want the cleaner linear history and the commits are still local, and ask before rebasing anything you have pushed.

---

## When it breaks

If a command here leaves you somewhere confusing, stop and go to `git_recovery.md`. Run `git status` first; it almost always tells you what state you are in. For plain-language definitions of Git terms, see `git_vocabulary.md`.
