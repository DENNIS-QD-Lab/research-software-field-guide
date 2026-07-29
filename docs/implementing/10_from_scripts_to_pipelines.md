# From scripts to pipelines

You learned the daily workflow in `../onboarding/05_daily_workflow.md` on small changes: one branch, one edit, one PR, one repo per window. That workflow is correct, and you should keep using it. But as your scripts grow into a *pipeline* (a series of computational or analysis steps that build on each other, code development that takes days, working on multiple developments in parallel) a few of its defaults start to strain.

This doc names that transition and sets up the two things the rest of the implementing track assumes: a branching model that scales, and a workspace that holds more than one repo. It is the bridge from the onboarding track to everything after it, so it comes first.

## Signs you have outgrown the simple workflow

Nothing here needs to change until you feel it. The triggers:

- **Many files.** A change touches several modules that depend on each other, not one script.
- **Work that spans days.** A feature is not done in one sitting; you commit, stop, and come back.
- **More than one thing in development.** You are mid-feature when a bug needs a quick fix, and you do not want them tangled together.
- **More than one repo open.** Your pipeline imports helpers from another repo, and you are editing both.

If none of these describe you yet, `../onboarding/05_daily_workflow.md` is still all you need. Come back when they do.

## Branching as projects scale

The one-branch-per-edit model from onboarding has a name: **GitHub Flow**. Branch off `main`, do the work, open a pull request, merge, delete the branch. It scales much further than people expect, so you do not replace it. You stretch it.

What changes is what a branch *represents*. In the onboarding workflow a branch was one small edit that lived for minutes. Now a branch represents a **feature or experiment**: it holds several commits and lives for days. Name it for the feature, not the file.

In VS Code: click the branch name in the bottom-left status bar and choose "Create new branch."

In the terminal:

```
git switch -c add-dark-frame-correction
```

This creates a branch named for the work it contains. Here `add-dark-frame-correction` is an example; the point is to name the branch for the change, not for a file inside it (`edit-step2`). The name appears in the PR title and in your history forever, so describe the change.

Two habits keep a long-lived branch healthy.

**Merge `main` in regularly.** While your branch lives for days, teammates merge other work into `main`. Bring it into your branch often so the two do not drift apart.

In VS Code: open the Source Control panel, use the "..." menu, and choose Branch > Merge Branch, then pick `main`.

In the terminal:

```
git switch add-dark-frame-correction
git merge main
```

The first line makes sure you are on your feature branch; the second brings `main`'s new commits into it. Small, frequent merges mean small conflicts you can resolve in a minute, instead of one enormous conflict at the end. When a conflict does appear, `../reference/git_recovery.md` walks through it.

**Open a draft PR early.** A *draft PR* is a pull request marked "not ready to merge." Open one as soon as you have something worth showing, even half-finished, so a teammate can look while the work is in progress rather than only at the very end. On GitHub, click the arrow next to the "Create pull request" button and choose "Create draft pull request." This pairs with the doc-site review habit in `19_documentation_and_doc_sites.md`.

## When not to add complexity

There is a heavier model called **Git Flow**, built around a permanent second branch (often named `dev` or `develop`) that work piles onto before it is released. You have probably seen it mentioned. Do not adopt it here.

That machinery exists to manage **scheduled, versioned releases to outside users**, holding finished work back until a release date. An internal pipeline has no release date; `main` *is* the live pipeline. A permanent `dev` branch would just add a step and give work a place to rot. Keep `main` as the single source of truth and use short-lived feature branches off it.

Put plainly: **a long-running branch is a workspace, not an archive.** When an experiment on such a branch reaches a conclusion, it graduates onto `main` (in the SWIR_HDR exemplar, a longer-lived experiment branch was merged to `main` and then retired once the work settled). It does not live on the branch forever. Where those graduated experiments *land* on `main`, in a dedicated `experiments/` folder, is discussed in `15_experiments_and_shipping.md`.

The trigger to reconsider heavier branching is the **distribution tier**: cutting tagged public releases of a project. That is `21_versioning_and_releases.md`, and it is not now.

## The multi-root workspace

`../onboarding/02_using_vs_code.md` taught one folder, one window: open a single repo so VS Code's terminal, search, and Source Control all point at it. That is still the right default for single-repo work. But you sometimes need two repos open at once — not when one merely *consumes the other's output* (that is a data hand-off: you need the output files, not the other repo), but when you are actually **reading or editing both repos' code in the same sitting**. Common cases: scaffolding a new repo while keeping an existing one open as a template to mirror; developing the next version of a project while consulting the previous one; documenting a generic pattern in one repo from its concrete implementation in another; or co-developing a shared library alongside a repo that installs it. Do _not_ open their shared parent folder to get both in one window as this can confound the Python interpreter, the terminal's working directory, and the search scope across repos. Instead set up a **multi-root workspace**: one VS Code window holding several folders, each keeping its own identity.

**Note:** the workspace governs which repos you *see* and edit together. How one repo *depends* on another is a separate question: one repo may generate output files that become the next repo's input (`17_working_with_large_data.md`), or one repo may install another's code as a pinned package (`20_packaging.md`). Either is preferred to importing code live across sibling folders.

In VS Code:

1. Open your first repo, then choose **File > Add Folder to Workspace** and add each other repo.
2. Choose **File > Save Workspace As**. VS Code saves the list of folders into a `.code-workspace` file. Save it *outside* all the repos, so it is not committed into any of them.
3. Reopen it anytime with **File > Open Workspace from File**.

A `.code-workspace` file is just a local list of which folders to open together; the name and grouping are your choice. For example, you might group your analysis repo and the upstream stage it builds on into one workspace file named for your project, saved beside the repo folders. Any grouping that matches what you work on together is fine.

Why this beats a bare parent folder: each folder in a multi-root workspace stays its **own Source Control root**, so you see and commit each repo's changes separately, and keeps its **own Python interpreter**.

One caveat: **confirm the interpreter and kernel per folder.** A multi-root workspace does not assume a shared environment. For each repo, check the interpreter in the status bar (or Command Palette > "Python: Select Interpreter"), and for a notebook pick the matching kernel, so each repo runs against its own environment. The difference between the interpreter (for `.py` files) and the kernel (for notebooks), and why they can be mismatched, is covered in `../onboarding/04_environments.md`.

**Tip: keep one terminal open per repo.** A Git command acts on whichever repo your terminal is currently sitting in, so hopping between repos with `cd` is easy to get wrong. Instead, open a separate integrated terminal for each folder, each already rooted in its repo: right-click a folder in the Explorer and choose "Open in Integrated Terminal," then switch between the open terminals from the dropdown at the top of the terminal panel. Your shell prompt shows the current folder name, which is a quick way to confirm you are about to run a command in the repo you meant.

## Where the sharp Git tools live

Longer-lived branches eventually put you in situations the daily loop does not cover: parking half-finished work to switch tasks, copying one commit onto another branch, tidying history before a PR. Those tools (`git stash`, `git rebase`, `git cherry-pick`) are cataloged in `../reference/advanced_git.md`. Reach for it when you hit one of those moments. You do not need to learn them up front.
