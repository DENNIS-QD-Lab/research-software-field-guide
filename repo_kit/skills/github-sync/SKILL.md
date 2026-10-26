---
name: github-sync
description: Bring local git repositories and GitHub into agreement — find what is unpushed, unmerged, or stale across one or several repos, push branches, open or update pull requests with real titles and descriptions, and clean up after merges. Use this whenever someone asks what needs to be pushed, pulled, or PR'd, wants to get GitHub up to date, open or describe a pull request, sync or tidy branches, or when a push fails partway ("RPC failed", "Broken pipe", "remote end hung up").
---

# Syncing repositories with GitHub

Use this skill to answer "what needs to go to GitHub?" across one or more repositories and to carry
it out: pushes, pull requests with real titles and descriptions, and cleanup once they merge. The
same steps work whether the assistant can reach GitHub itself or has to hand the commands to the
person; step 1 finds out which. A personal `LOCAL.md` beside this file records anything specific
to one person's setup, and is read first.

## 0. Read the local settings

If `LOCAL.md` exists in this skill's folder, read it before anything else and follow it where it
differs from the defaults below. It records how this person works: whether the assistant runs
GitHub commands or hands them off, their shell, the repositories to survey, known network limits on
pushes, branches that belong to other people, and where to save PR description files.
`LOCAL.example.md` shows the format. `LOCAL.md` is personal and is never committed.

## 1. Find out what you can run

Everything about the remote comes from `git fetch`. Remote-tracking refs such as `origin/main` only
change when someone fetches, so a fetch that fails leaves an old picture that looks current. Check
access before reporting anything about the remote:

- Run `git fetch --all --prune` in one of the repositories. If it fails with an authentication,
  network, or sandbox error ("could not read Username", "Device not configured", "operation not
  permitted"), this session cannot reach GitHub.
- Run `gh auth status`. If it fails, this session cannot open or edit pull requests.

A session that runs commands in a sandbox may let network commands out only when each one is sent
on its own. Before concluding that GitHub is out of reach, change into the repository's directory
with one command, then run `git fetch` (and later each `git push` or `gh` command) as a separate
command by itself. The same command chained after `cd … &&`, given `-C <path>`, or placed inside a
loop can run inside the sandbox and fail on credentials, which looks exactly like having no access.

Then work in one of two modes:

- **Direct.** Fetch the repositories yourself, one standalone command per repository. Pushes, pull
  requests, and branch deletions are visible to other people, so describe them and get the
  person's agreement before running them.
- **Hand-off.** Ask the person to fetch, and wait for them to say it is done before reading
  anything. Give them one command that covers every repository, for example
  `for r in ~/code/analysis ~/code/pipeline; do git -C "$r" fetch --all --prune; done`.
  Every push and `gh` step then becomes a command block for them to run.

## 2. Survey the repositories

Run `scripts/survey_repos.py <repo> [<repo> ...]`. It reads local refs only, so run it after the
fetch. For each repository it reports the last fetch time, the current branch and any uncommitted
changes, each local branch against its upstream, how much new file data an unpushed branch would
upload, which remote branches are already merged into the default branch, who last committed to
the others, and any extra worktrees. Read the states this way:

- **Upstream deleted on the remote** usually means the pull request merged and GitHub deleted the
  branch. Switch to the default branch, pull, and delete the local branch (step 6).
- **No upstream, but a same-named remote branch exists** means it was pushed without `-u`. Set
  tracking with `git branch --set-upstream-to=origin/<branch> <branch>`.
- **One unmerged branch contains another** (`git merge-base --is-ancestor <one> <other>`): a single
  pull request covers both. Say so in its description, and delete the contained branch after the
  merge.
- **Squash merges are not detected.** Squashing creates new commits, so a squash-merged branch
  still reads as unmerged. Check the pull request on GitHub before treating it as open work.

## 3. Plan the sync

Write one block per repository, with commands in the order they must run: push, then open or update
the pull request. Post-merge cleanup is a separate, later block.

- **Check that each branch merges cleanly** before proposing its pull request:
  `git merge-tree --write-tree --name-only origin/main <branch>` prints only a tree id when the
  merge is clean, and the conflicting file names when it is not. Check branches that will merge one
  after another against each other too.
- **Give every new pull request a title and a description file:**
  `gh pr create --base main --head <branch> --title "…" --body-file <file>`. Without them, `gh`
  either prompts interactively or opens the pull request with no description.
- **Update a pull request that already exists** instead of creating a second one. If `gh` reports
  one, or `gh pr list --head <branch>` shows one, use
  `gh pr edit <number> --title "…" --body-file <file>`. Pushing to the branch updates its commits on
  its own. Warn that `gh pr edit --body-file` replaces any description already written there.
- **Plan large pushes in stages from the start.** If the survey shows a branch adding more than
  about 20 MB of new data, or more than the limit `LOCAL.md` sets, push it commit by commit as
  `references/large_pushes.md` describes, rather than waiting for a single large push to fail.
- **Leave other people's branches alone.** Do not delete, rebase, or force-push a branch someone
  else is working on. The survey shows who last committed to each unmerged remote branch, and
  `LOCAL.md` may list owners.

## 4. Draft the pull request descriptions

Read the branch's commits and the size of its change:

```bash
git log --reverse --format='%h %s' origin/main..<branch>
git diff --stat origin/main..<branch> | tail -1
```

Write for the reviewer. Open with one or two sentences on what the branch does and why, then short
bullets grouped by area rather than one per commit. Leave out lists of what the pull request does
not do, and reports that checks passed. Follow the repository's own conventions for pull requests
where it has them (its `CLAUDE.md` or `CONTRIBUTING.md`), including any required attribution line.

Save each description to a file, in the session's scratch or temporary directory or wherever
`LOCAL.md` says, and pass it with `--body-file`. A file keeps backticks, quotes, and line breaks
intact, which a description pasted into a shell argument often loses. In hand-off mode, give the
file's full path in the command.

## 5. When a push fails partway

Errors such as `RPC failed; curl 55`, `Broken pipe`, `unexpected disconnect while reading sideband
packet`, or `the remote end hung up unexpectedly` mean the upload was cut off. The commits are still
safe locally. Before retrying anything, check what reached GitHub with
`git ls-remote origin <branch>`, then read `references/large_pushes.md` and work down its list.

## 6. After a pull request merges

1. Switch to the default branch and pull: `git checkout main && git pull`.
2. Delete the local branch with `git branch -d <branch>`. It refuses a branch git does not see as
   merged; for a squash merge, confirm the merge on GitHub first, then use `git branch -D`.
3. Delete the remote branch if GitHub has not already: `git push origin --delete <branch>`, and only
   for the person's own branches.
4. Remove any worktree made for the branch: `git worktree remove <path>`.

## Boundaries

- Ask before pushing, opening or editing pull requests, or deleting remote branches, unless the
  person has said to go ahead with that step.
- Never force-push a branch other people use, and never rewrite commits that are already pushed.
  Pull requests, reviews, and any records that cite a commit id point at those commits.
- Never create a tag or release as part of a sync. That is a separate step the person asks for.

## Files in this skill

- `scripts/survey_repos.py` — reports each repository's branches, unpushed data, merged remote
  branches, and worktrees from local refs, with the time of the last fetch.
- `references/large_pushes.md` — measuring a push, and what to try, in order, when one fails
  partway.
- `LOCAL.example.md` — the format for a personal `LOCAL.md`.
