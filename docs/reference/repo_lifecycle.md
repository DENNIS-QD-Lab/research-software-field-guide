# Repo lifecycle

Starting a repo, getting a copy of someone else's, and deciding who can see it. No reading order; skim
and come back when one of these comes up. This is not a full GitHub manual — for the exact click paths,
GitHub's own docs are linked below and kept current by GitHub itself.

## Starting a new repo

Covered step by step in [09_first_contribution_exercise.md](../onboarding/09_first_contribution_exercise.md#get-a-repo-to-work-in):
GitHub's **New repository** button, then clone it locally the same way you'd clone any repo.

## Cloning an existing repo

Covered step by step in [GETTING_STARTED.md](../../GETTING_STARTED.md): `git clone <url>` into wherever
you keep your projects (`~/repos/` is this guide's suggested convention, not a requirement).

## Forking vs. branching directly

A **fork** is a copy of someone else's repository, made under your own GitHub account. You branch,
commit, and push freely in your copy — none of it touches the original repository until you open a
pull request from your fork back to theirs.

The decision is about access, not preference:

- **You have write access** (your own project, your team's repo, an organization repo you belong to) —
  branch directly. That's the ordinary loop in
  [05_daily_workflow.md](../onboarding/05_daily_workflow.md), and forking would just create an
  unnecessary second copy to keep track of.
- **You don't have write access** (an open-source project, a public repo owned by someone outside your
  team) — fork it. Click **Fork** on the repository's GitHub page, clone your fork locally, then follow
  the same branch → commit → push loop. The one difference: your pull request targets the *original*
  repository, not your own fork's `main`.

For the exact click path across the web UI, GitHub CLI, and GitHub Desktop, see GitHub's own
[Fork a repository](https://docs.github.com/en/get-started/quickstart/fork-a-repo) guide.

## Public vs. private

A **public** repository is visible to anyone on the internet. A **private** repository is visible only
to you and whoever you explicitly grant access — collaborators, or (for an organization repo) certain
organization members.

This guide's own [22_publishing_a_paper.md](../disseminating/22_publishing_a_paper.md) and
[23_shipping_a_library.md](../disseminating/23_shipping_a_library.md) cover *when* a research repo
should go public — typically at or near a publication or a release, often with a private lab
notebook kept separate from the public, tagged snapshot. This section is only about the GitHub
setting itself: it lives in a repository's Settings tab, and — with a caveat that an organization owner
can restrict who's allowed to change it — visibility can be changed after creation in either direction.
See GitHub's [About repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/about-repositories)
and [Setting repository visibility](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility)
for the mechanics and the consequences of switching. For the lab-level layer on top of this — owning
repos through a GitHub Organization rather than a personal account, and why visibility is a
per-repository setting that shapes how a private lab notebook and a public paper record coexist — see
[repo_ownership_and_visibility.md](repo_ownership_and_visibility.md).
