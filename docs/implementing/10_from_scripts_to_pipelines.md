# From scripts to pipelines

You learned the coding/GitHub workflow in [05_daily_workflow.md](../onboarding/05_daily_workflow.md) on small changes: one branch, one edit, one PR, one repo per window. That workflow is correct, and you should keep using it. But as your scripts grow into a *pipeline* — repeated, interdependent steps that take real development time — a few of its defaults start to strain (the signs are below).

This doc is the bridge from onboarding to everything after it, so it comes first. It names that transition, then covers two things worth having in place early: a branching model that scales, and a workspace that holds more than one active repo.

## The shape of the implementing track

Onboarding taught you to write one script or notebook correctly. This track is about keeping a
*growing* collection of code that is trustworthy, reproducible, and shareable as a whole project. It falls into
four parts:

- **Docs 11–14** are coding standards and practices: the tools that keep code correct and consistent as
  it grows — linting and formatting (`ruff`), type checking (`mypy`), automated tests (`pytest`),
  decomposing code so it stays readable, and running all of it automatically on every push via
  continuous integration.
- **Docs 15–17** are about using the repo for real scientific analysis: structuring a project around a
  stable library plus dated, tracked experiments, recording each run so results stay reproducible, and
  referencing data too large to commit to the repo itself.
- **Docs 18–19** are about AI-assisted development: getting real help with the coding from an assistant
  while keeping the thinking and the scientific judgment yours.
- **Doc 20** is documentation and doc sites: turning the work into something a colleague (or maybe your
  non-coding PI) can review and understand without having to re-run the repo or adopt the practices themselves.

Adopt each part as the corresponding need arises in your own project — or ask your AI assistant to
scaffold the structure directly, using the [repo_kit](../../repo_kit/README.md), while you keep reading
to understand the goals behind it.

> **The `repo_kit`** is a set of recipes and templates for bringing a new or existing repo up to this
> standard — structure, workflow, and documentation. One way to jump-start it is to open this guide in the
> same workspace as your own repo (the next section covers the mechanics) and ask your coding assistant
> to orient itself to the practices here, then work with you to build or upgrade your repo to match,
> step by step. Keeping both repos open side by side while your assistant helps with the code and docs
> makes it easy to learn about the reasoning behind each standard as it is applied.

## The multi-root workspace

[02_using_vs_code.md](../onboarding/02_using_vs_code.md) covers the mechanics behind multi-root workspaces: adding a second repository as its own folder in the same window, and saving that combination as a `.code-workspace` file. This section is about *when* that's actually the right call, and the gotchas that show up once you're doing it for real pipeline-scale work.

Open two repos together only when you are actually **reading or editing both repos' code in the same sitting** — not when one merely *consumes the other's output* (that's a data hand-off: you need the output files, not the repo itself). Common cases: scaffolding a new repo while keeping an existing one open as a template to mirror; developing the next version of a project while consulting the previous one; documenting a generic pattern in one repo from its concrete implementation in another; or co-developing a shared library alongside a repo that installs it.

**Note:** the workspace governs which repos you *see* and edit together. How one repo *depends* on another is a separate question: one repo may generate output files that become the next repo's input ([17_working_with_large_data.md](17_working_with_large_data.md)), or one repo may install another's code as a pinned package ([21_packaging.md](../disseminating/21_packaging.md)). Either is preferred to importing code live across sibling folders.

**Confirm the interpreter and kernel per folder.** A multi-root workspace does not assume a shared environment. For each repo, check the interpreter in the status bar (or Command Palette > "Python: Select Interpreter"), and for a notebook pick the matching kernel, so each repo runs against its own environment. The difference between the interpreter (for `.py` files) and the kernel (for notebooks), and why they can be mismatched, is covered in [04_environments.md](../onboarding/04_environments.md).

**Keep one terminal open per repo.** A Git command acts on whichever repo your terminal is currently sitting in, so hopping between repos with `cd` is easy to get wrong. Instead, open a separate integrated terminal for each folder, each already rooted in its repo: right-click a folder in the Explorer and choose "Open in Integrated Terminal," then switch between the open terminals from the dropdown at the top of the terminal panel. Your shell prompt shows the current folder name, which is a quick way to confirm you are about to run a command in the repo you meant.

## Signs you have outgrown the simple workflow

Nothing here needs to change until you feel it. The triggers:

- **Many files.** A change touches several modules that depend on each other, not one script.
- **Work that spans days.** A feature is not done in one sitting; you commit, stop, and come back.
- **More than one thing in development.** You are mid-feature when a bug needs a quick fix, and you do not want them tangled together.

If none of these describe you yet, [05_daily_workflow.md](../onboarding/05_daily_workflow.md) is still all you need. Come back when they do.

## Branching as projects scale

The one-branch-per-edit model from onboarding has a name: **GitHub Flow**. Branch off `main`, do the work, open a pull request, merge, delete the branch. It scales much further than people expect, so do not replace it. Stretch it.

What changes is what a branch *represents*. In the onboarding workflow a branch was one small edit that lived for minutes. Now a branch represents a **feature or experiment**: it holds several commits and lives for days. Name it for the feature, not the file.

In VS Code: click the branch name in the bottom-left status bar and choose "Create new branch."

In the terminal:

```
git switch -c add-dark-frame-correction
```

This creates a branch named for the work it contains. Here `add-dark-frame-correction` is an example; the point is to name the branch for the change, not for a file inside it (i.e., don't use `edit-show_h5_keys`). The name appears in the PR title and in your history forever, so describe the change.

Two habits keep a long-lived branch healthy.

**Merge `main` in regularly.** While your branch lives for days, colleagues may merge other work into `main`. Bring it into your branch often so the two do not drift apart.

In VS Code: open the Source Control panel, use the "..." menu, and choose Branch > Merge Branch, then pick `main`.

In the terminal:

```
git switch add-dark-frame-correction
git merge main
```

The first line makes sure you are on your feature branch; the second brings `main`'s new commits into it. Small, frequent merges mean small conflicts you can resolve in a minute, instead of one enormous conflict at the end. When a conflict does appear, [git_recovery.md](../reference/git_recovery.md) walks through how to manage it.

**Open a draft PR early.** A *draft PR* is a pull request marked "not ready to merge." Open one as soon as you have something worth showing, even half-finished, so a colleague can look while the work is in progress rather than only at the very end. On GitHub, click the arrow next to the "Create pull request" button and choose "Create draft pull request." This pairs with the doc-site review habit in [20_documentation_and_doc_sites.md](20_documentation_and_doc_sites.md).

## Keep it simple while you can

There is a heavier model called **Git Flow**, built around a permanent second branch (often named `dev` or `develop`) that work piles onto before it is released. You have probably seen it mentioned. It's not recommended here.

That machinery exists to manage **scheduled, versioned releases to outside users**, holding finished work back until a release date. An internal pipeline has no release date; `main` *is* the live pipeline. A permanent `dev` branch would just add a step and give work a place to rot. For ongoing development, analysis, or experimental work, keep `main` as the single source of truth and use short-lived feature branches off it.

The trigger to reconsider heavier branching is the **distribution tier**: cutting tagged public releases of a project, discussed in [23_shipping_a_library.md](../disseminating/23_shipping_a_library.md).

## Where the sharp Git tools live

Longer-lived branches eventually put you in situations the daily loop does not cover: parking half-finished work to switch tasks, copying one commit onto another branch, tidying history before a PR. Those tools (`git stash`, `git rebase`, `git cherry-pick`) are cataloged in [advanced_git.md](../reference/advanced_git.md). Reach for it when you hit one of those moments. You do not need to learn them up front.
