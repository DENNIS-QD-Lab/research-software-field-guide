# Git and GitHub vocabulary

A reference for the terms you'll encounter while using Git and GitHub. You don't need to memorize this. Skim it once, then come back when a term confuses you.

## The basics

**Repository (repo)**
A project tracked by Git. A folder on your computer that Git is watching, plus the history of every change made to it. The same repo can exist in multiple places (your laptop, GitHub, a collaborator's laptop) and Git keeps them in sync when you ask.

**Local**
On your computer. Your local repo is the copy of the project in a folder on your machine.

**Remote**
Not on your computer. For our purposes, "remote" almost always means GitHub.

**origin**
The default name Git gives to the remote copy of your repo on GitHub. When you see `git push origin main`, that means "push my local main branch to the GitHub copy."

**clone**
The act of making a local copy of a remote repository. `git clone <url>` downloads the entire repo and its history onto your computer.

**Fork**
A copy of someone else's repository, made under your own GitHub account, used when you don't have write access to the original. See [repo_lifecycle.md](repo_lifecycle.md) for when to fork versus when to just branch.

## Commits and changes

**Commit (noun)**
A saved snapshot of the repo at one moment, with a message describing what changed. Every commit has a unique ID (a hash like `a3f9c2d`).

**Commit (verb)**
The act of creating a commit. "Commit your changes" means "save a snapshot of your current changes with a message."

**Staging / staged**
Files you've marked as "include these in my next commit." Distinct from "files you've changed." In VS Code's Source Control panel, changed files appear under "Changes" and become "Staged Changes" once you click the plus icon next to them.

**Working directory (working tree)**
The actual files on your computer right now, as you currently see them. May or may not match the last commit, depending on what you've edited since.

**Diff**
The difference between two states of a file: what was added, what was removed. When you review a pull request, you're reading a diff.

## Branches

**Branch**
A parallel timeline of the entire repository. When you create a branch, you can make changes that don't affect the main timeline until you decide to merge them back. Every file in the repo is "on" your current branch.

**main**
The default branch name for the canonical version of the repo. Some older repos use `master` instead; same idea.

**HEAD**
Git's name for "where you are right now" in the history. Usually points to the latest commit on your current branch. If you hear "detached HEAD," something unusual is happening and it's worth asking for help.

**Checkout**
The act of switching to a branch (or to a specific commit). `git checkout main` means "switch my working directory to show the main branch."

**Merge**
Combining the history of one branch into another. When you complete a pull request on GitHub, GitHub merges your branch into main.

**Rebase**
Another way to combine branches. More advanced; ignore for now.

**Diverged**
Two branches each have commits that the other doesn't. Usually fixed by merging or rebasing. You'll see VS Code warn about this when it happens.

## Moving changes around

**Fetch**
Download new commits from GitHub into your local Git's knowledge, but don't change your working files yet. Think of it as checking the mail without opening it.

**Pull**
Fetch *and* immediately apply those new commits to your current branch. Equivalent to `git fetch` followed by `git merge`. This is what actually changes your working files. When you see "1 commit behind," running `git pull` is usually what catches you up.

**Push**
Upload your local commits to GitHub so they're visible to everyone else.

**Sync**
A VS Code term, not a Git term. The sync button (circular arrows in the lower-left) does the right combination of fetch, pull, and push to bring your local branch and the remote branch into agreement.

**Ahead / behind**
"Ahead by 2" means your local branch has 2 commits not yet on GitHub. "Behind by 3" means GitHub has 3 commits not yet on your local branch. "Ahead by 2, behind by 3" means both, and you'll need to pull (and possibly resolve conflicts) before pushing.

**Upstream**
The remote branch your local branch is set to push to and pull from. Usually the branch with the same name on origin. When Git says "your branch has no upstream," it means you haven't told Git which remote branch this one corresponds to (`git push --set-upstream origin <branch>` fixes that).

## Conflicts

**Merge conflict**
Git tried to combine two changes to the same line and couldn't decide which one wins. Git marks the conflict with special characters in the affected files (`<<<<<<<`, `=======`, `>>>>>>>`) and asks you to choose. VS Code shows these with buttons like "Accept Current Change" and "Accept Incoming Change" to make resolution easier.

**Conflict resolution**
The act of editing a file to resolve a merge conflict, then committing the result.

## Pull requests (GitHub-specific)

**Pull request (PR)**
A proposal to merge one branch into another, submitted via GitHub's web interface. It's a GitHub concept, not a Git concept. The PR is where review and discussion happen before the merge.

**Review**
Reading a PR's diff and either approving it, requesting changes, or leaving comments.

**Squash and merge**
A merge option on GitHub that collapses all the commits on your branch into a single commit on main. Recommended for our workflow: keeps main's history clean and readable.

## Things you'll see in error messages

**Untracked**
A file in your working directory that Git doesn't know about yet. Marked with `U` in VS Code's Explorer. `git add <file>` starts tracking it.

**Modified**
A tracked file that's changed since the last commit. Marked with `M` in VS Code's Explorer.

**Staged**
A change you've marked for inclusion in the next commit. Marked with `A` (for additions) or other letters in VS Code's Explorer.

**Ignored**
A file matched by `.gitignore`. Git won't track it. Shown dimmed in VS Code's Explorer.

**Stash**
A temporary holding area for changes you don't want to commit yet but need to set aside. `git stash` saves them; `git stash pop` brings them back. Useful when you've started work on the wrong branch and need to move it.

**HEAD detached at <hash>**
You've checked out a specific commit rather than a branch. Anything you commit here will be lost when you switch branches unless you create a branch first. Ask for help if you see this and didn't mean to do it.