# Git recovery: when you mess up

Everyone messes up Git sometimes. Most mistakes look scarier than they are, and almost everything is recoverable as long as you don't make things worse with a panicked second action.

## How to read this doc

Don't read it front to back. Find the situation that matches what you did, follow the steps, and get back to work. The patterns are in rough order of how common they are.

## Before you do anything

If a situation feels broken and you're not sure what's happening, **stop and run `git status` first**. Git status tells you, in plain English, what branch you're on, what files have changed, and what state things are in. It's the single most useful command for diagnosing "wait, what just happened."

```
git status
```

If after reading the output you're still unsure, **ask in your team's chat before running any command that contains `--force`, `--hard`, or `rm`**. Those flags can destroy work. Almost nothing else in Git can.

---

## "I made my edits on `main` instead of a branch"

The fix depends on whether you've already committed.

**Case A: Your changes are uncommitted** (they show as "Changes" in VS Code's Source Control panel, but you haven't clicked Commit yet).

This is the easy case. Your edits aren't yet attached to any branch; they're just sitting in your working directory. Create a branch from where you are, and the edits come along:

```
git checkout -b descriptive-branch-name
```

Now you're on the new branch with all your edits, exactly as they were. Stage and commit normally.

**Case B: You committed to `main`, but haven't pushed yet.**

Two steps. First, create a branch at your current state so the work is captured somewhere:

```
git branch descriptive-branch-name
```

This makes a branch pointing at your current commit but doesn't switch to it. Your local `main` and the new branch now point at the same commit.

Then rewind your local `main` back to where GitHub thinks it should be:

```
git reset --hard origin/main
```

This is the scary command (it has `--hard` in it), so read carefully: it discards any commits on your local `main` that aren't on GitHub's `main`. Because you just created `descriptive-branch-name` pointing at those commits, the work is preserved on the branch. Your local `main` is now back in sync with GitHub.

Switch to your branch and continue working:

```
git checkout descriptive-branch-name
```

**Case C: You committed to `main` *and* pushed to GitHub.**

Stop and ask. The fix is doable but requires force-pushing, which can affect other people. Better to handle it once with someone watching than guess.

---

## "I committed to the wrong branch"

You meant to commit to `add-show-keys` but you were still on `fix-pathing-bug`. The work is fine; it's just on the wrong branch.

If you haven't pushed yet, move the most recent commit to the right branch:

```
git log --oneline -1                          # confirm the commit you want to move
git checkout add-show-keys                    # switch to the branch you wanted
git cherry-pick fix-pathing-bug               # copy the commit over
git checkout fix-pathing-bug                  # back to the wrong branch
git reset --hard HEAD~1                       # remove the commit from this branch
```

If you've pushed already, the commit is on GitHub on the wrong branch. The cleanup is similar but you'll need to force-push the corrected branch. Worth asking before doing it.

---

## "I committed something I shouldn't have"

A password, a data file, a `.env` file, a path with your username in it — something private or large that doesn't belong in version control.

**If you haven't pushed yet**, you can rewrite history:

```
git reset --soft HEAD~1                       # undo the commit, keep the changes
```

Now the bad file is still in your working directory. Delete it (or move it elsewhere), update `.gitignore` so it doesn't get re-added, then commit again with the right contents.

**If you've already pushed**, ask before doing anything. For real secrets (passwords, keys, tokens), rotate the secret immediately — assume it's compromised — *then* worry about cleaning history. For data files, the cleanup is a separate process that's manageable but worth doing carefully.

---

## "I want to undo my last commit"

If the commit is just on your machine (not pushed):

```
git reset --soft HEAD~1
```

The commit is undone; the changes from it are back in your working directory as if you'd never committed. Edit, then commit again when ready.

If you want to throw away the changes entirely (not just the commit):

```
git reset --hard HEAD~1
```

This is destructive — the changes from that commit are gone. Make sure that's what you want.

---

## "I'm on the wrong branch and want to switch, but I have uncommitted changes"

If you `git checkout other-branch` while you have uncommitted changes, Git will either let you (if the changes don't conflict with the other branch) or refuse (if they do).

The safe option: stash your changes, switch, then bring them back if you want:

```
git stash                                     # set changes aside
git checkout other-branch
git stash pop                                 # bring the changes here
```

`stash` is a temporary holding area. `pop` retrieves them. If you don't want them anymore, `git stash drop` discards.

---

## "I deleted a file I needed"

If you deleted it but haven't committed the deletion:

```
git checkout HEAD -- path/to/file
```

This restores the file to whatever the last commit had.

If you committed the deletion and want to undo it:

```
git checkout HEAD~1 -- path/to/file           # restore from the previous commit
git commit -m "Restore accidentally deleted file"
```

---

## "I have no idea what I did and everything looks broken"

Three commands to run, in order:

```
git status
git log --oneline -10
git branch
```

`status` shows your current state. `log --oneline -10` shows the last 10 commits. `branch` shows what branches exist locally.

Then either fix it yourself if the pattern matches one above, or paste all three outputs into your team's chat and ask. Git problems are usually faster to fix with a second pair of eyes than to thrash through alone.

---

## Things that look broken but probably aren't

**"Detached HEAD state"** — you've checked out a specific commit instead of a branch. Anything you commit here will be lost when you switch branches unless you create a branch first. Fix: `git checkout -b new-branch-name`. Or if you didn't mean to be here: `git checkout main`.

**"Your branch is ahead of 'origin/main' by N commits"** — you have local commits not yet on GitHub. This is normal. Push when ready.

**"Your branch is behind 'origin/main' by N commits"** — GitHub has commits you don't have locally. Run `git pull`.

**"Your branch and 'origin/main' have diverged"** — both have commits the other doesn't. This usually happens when you push from one machine and then forget to pull on another. `git pull` will try to merge; if there are conflicts, resolve them.

---

## Adding to this doc

When you hit a Git situation that wasn't covered here and you figured out the fix, add it. Use the same pattern as above: the situation in the heading, plain-language explanation, then the commands with comments.