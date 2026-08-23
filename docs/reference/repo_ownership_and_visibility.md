# Repo ownership and visibility

Who owns a repo, who can see it, and and what changes as a project moves from lab notebook to
published paper to shipped tool. No reading order; skim and come back when one of these comes up.

## The three visibility postures

[15_experiments_and_shipping.md](../implementing/15_experiments_and_shipping.md) describes a repo doing
three overlapping jobs — exploratory, archival, and shippable. Those jobs usually want different
visibility, on different timelines, not one repo-wide setting:

- **Exploratory (the lab notebook)** — private, by default, indefinitely. Nothing about it needs to be
  polished for an outside reader, and it often shouldn't be read by one: false starts, unfiltered
  commentary, and preliminary results that didn't hold up all belong here.
- **Archival (the paper record)** — public, but as a curated snapshot, not the raw notebook. This is
  the tagged, DOI'ed state [22_publishing_a_paper.md](../disseminating/22_publishing_a_paper.md)
  covers.
- **Shippable (the library)** — often public earlier and more fully than the paper record, including
  its ordinary development history. That history isn't sensitive lab process, it's just normal software
  churn, and open-source norms favor showing it.

Treat "when do we go public" as two separate decisions, not one: a tool can be worth releasing well
before the paper that used it is submitted, and a paper's clean snapshot can go public while the
pipeline behind it stays an internal, unreleased part of the lab's infrastructure.

## Visibility is per-repository, not per-tag or per-branch

This is the constraint that shapes everything else here, and it's easy to assume otherwise coming from
Git's branch/tag model: GitHub visibility is a setting on the *whole repository*. You cannot make one
tag public while the rest of a repo's history stays private. If the repo is private, every commit,
branch, and tag in it is private; flip it to public, and all of that history goes public at once,
permanently — copies, forks, and caches outlive any later attempt to undo it.

This is exactly why [22_publishing_a_paper.md](../disseminating/22_publishing_a_paper.md)'s and
[23_shipping_a_library.md](../disseminating/23_shipping_a_library.md)'s "clean
public copy" patterns use **two repositories**, not one repo with a public tag: keep the private working
repo (full history, every experiment) as the actual notebook, and when it's time to disseminate, create
a *new, empty* public repository and copy in only what should be public. That's a plain file copy, not a
git operation, and it's the only mechanism that actually achieves partial exposure — there is no
"publish just this tag" setting to reach for instead.

The cost is a second repo to maintain, and the public copy carries no commit-by-commit history — the
trade for keeping the messy parts genuinely private rather than merely out of the diff. If some history
*is* worth bringing along (a clean sequence of commits you're proud to show), `git filter-repo` can
extract specific paths with their history intact; it's a separate install and a sharper tool than this
doc covers in depth — treat it as advanced, and double-check its output before pushing anywhere public.

Note that the alternative `.gitattributes` `export-ignore` entry only filters archives you build
yourself with `git archive` — it does not affect GitHub's auto-generated release ZIP, and it does
nothing to hide content from anyone browsing the repo's commit history. It trims what goes into an
archive of an otherwise-public repo; it does not make something genuinely private.

## Keeping two repos in sync across revisions

The privacy the two-repo pattern buys has an ongoing cost, not just an upfront one: the two repos
have independent histories, so nothing about them stays in sync automatically. That's fine for a
snapshot cut once and never touched again, but a paper rarely stops changing after the first tag —
reviewer comments update a figure, a bug fix changes a number, and the version a journal eventually
publishes is not the version a preprint server saw. Each of those leaves the public repo stale until
someone deliberately redoes the copy.

Treat that copy as a repeatable step, not a one-time migration. When the private repo's citable state
changes again, re-run the same "copy these paths" step into the *existing* public repo and commit the
result there as an ordinary update — the public repo accumulates its own short, honest history
(`Initial preprint`, `Revise Figure 3 per reviewer 2`, `Final published version`), even though that
history has no relationship to the private repo's commits. Tag each stage in both repos (`preprint`,
`v1-published`, ...) so a reader — or you, months later — can tell which public snapshot corresponds
to which private one, without needing shared git history to do it.

If this happens more than once, script the copy: a short list of paths to include, checked into the
private repo, run against a local checkout of the public repo. That turns "remember to re-sync" into
"run the script," and keeps the two repos' contents from drifting apart by accident between the
updates you do remember to make.

## Lab-owned, not person-owned: GitHub Organizations

A physical lab notebook belongs to the lab or university, not to whichever person filled its pages. A
repo under someone's personal GitHub account has no equivalent institutional claim: if the person who
created it leaves the lab, graduates, or has a falling out, the lab has no structural hold on it — access
can be revoked unilaterally, and the repo can go with them.

A **GitHub Organization** (`github.com/your-lab-name/`) fixes this the same way a shared notebook
cabinet does. Repos belong to the organization; people are added as members with scoped access to
specific repos; removing someone from the org doesn't touch the repos themselves. One concrete safeguard
worth calling out: an organization owner can restrict *who is allowed to change a repo's visibility at
all*, so a single contributor can't flip the lab notebook public by accident or without review — a
protection a personal-account repo simply doesn't have. (GitHub's free and paid tiers for organizations
change over time and often have education-specific options; check GitHub's current plans rather than
assuming specifics here.)

Practically: create the org once, move (or create new) lab repos under it rather than under any
individual's account — including repos with one primary contributor. "Just one person works on this
right now" is not a reason to own it personally; the point is what happens later, when that stops being
true.

The org benefits are reinforced by the autodoc habits promoted in this guide
([20_documentation_and_doc_sites.md](../implementing/20_documentation_and_doc_sites.md)): wherever org
visibility is turned on, anyone with org access can reach each repo's auto-generated Sphinx
site — the running lab notebook — without being individually invited to that specific repo. Kept under
personal accounts instead, each site stays reachable only by whoever was explicitly added to that one
repo, even for a PI who should reasonably have standing access to all of them.

## Multi-contributor models

How several people share credit and space within a lab-owned repo is genuinely specific to each lab —
there's no single right answer — but here's a menu, roughly in order of how much structure each adds:

- **Git authorship alone.** Commit history and pull-request authorship already answer "who did this,"
  permanently, for free, with no extra convention needed.
- **The signed-blockquote convention, extended to everyone.** This guide's `> **AMD:** ...` pattern
  ([16_running_a_dry_lab_experiment.md](../implementing/16_running_a_dry_lab_experiment.md)) generalizes
  cleanly to multiple contributors — each person signs their own interpretation with their own initials,
  so a shared research log stays legible about whose judgment produced which call, even inside one
  repo shared by several people.
- **One repo per project, all under the org**, rather than one repo for the whole lab. Each project
  keeps its own research log and experiment themes; the org is what ties them together as lab property
  without forcing everyone into one undifferentiated space.
- **Per-person `experiments/` (or `docs/`) subfolders within one shared project repo** — e.g.
  `experiments/<name>/<theme>/` — when several people genuinely need their own lab notebook space
  inside a single shared project, sharing the same `src/` and doc site but not commingling themes.
  This suits a project where each contributor's reproducibility setup is already somewhat personal
  anyway: `local_paths.py` and machine-local data roots
  ([17_working_with_large_data.md](../implementing/17_working_with_large_data.md)) are inherently
  per-machine, not synced to GitHub, so a per-person notebook subtree just mirrors a boundary that
  already exists at the data layer.

These aren't mutually exclusive — a lab might use one-repo-per-project as the default and drop into
per-person subfolders for the rare project several people actively co-develop.

## Avoiding accidental exposure

Two realistic ways a private lab notebook ends up public by mistake, worth naming plainly rather than
assuming they're obvious:

- **Flipping a repo's visibility setting without auditing its full history first.** The setting change
  itself takes one click; what it exposes is everything that has ever been committed, not just the
  current file tree. Decide and audit *before* the repo ever goes public, not after
  ([22_publishing_a_paper.md](../disseminating/22_publishing_a_paper.md),
  [23_shipping_a_library.md](../disseminating/23_shipping_a_library.md)).
- **Cloning the private repo and pushing that clone to a new public remote**, instead of doing the
  clean plain-file-copy the two-repo pattern above actually calls for. This looks like "just publishing
  the code" and instead drags the entire private commit history along with it.

An org-level restriction on who can change visibility (above) is the structural backstop for the first
risk; for the second, there is no setting that prevents it — it's a habit, and the habit is: a public
repo's *first* commit should be a fresh one, never `git push` of an existing private history.
