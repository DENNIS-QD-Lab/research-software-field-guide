# Driving an AI assistant

[18_ai_assisted_development.md](18_ai_assisted_development.md) covers the principles: the assistant writes code, you do the science, and every change earns review. This doc is the practical companion — the session-to-session mechanics of actually working with an assistant so those principles hold up in practice, not just in theory. The examples reflect Claude Code and this repo's setup; the mechanics generalize to other assistants with a project-instructions file and a chat-style interface.

Getting an assistant installed and running, and the concrete commands for managing a session (`/clear`, `/compact`, permissions, cost) are covered in [ai_coding_assistants.md](../reference/ai_coding_assistants.md) — start there if you don't have one set up yet. This doc assumes a working session and picks up from there.

## Write the standards file to be followed, not skimmed

A standards file only does its job if the assistant's output actually matches it. Three habits keep it that way:

- **State rules, not aspirations.** "Every function gets type hints" is followed. "Try to write clean code" is not — it is too vague to act on. If a rule in your file has never once changed generated output, rewrite it or cut it.
- **Keep it short enough to actually govern behavior.** A 900-line standards file gets skimmed, not applied — the assistant (and any human reader) loses the specific rules in the volume. If it grows past a page or two of real content, split it: durable procedure and research state belong in their own files, not folded into the standards file (see the three-way split in [18_ai_assisted_development.md](18_ai_assisted_development.md)).
- **Fix drift by editing the file, not by repeating yourself.** If you catch yourself typing the same correction in two different sessions ("no, use `np.testing.assert_allclose` for floats," say), that correction belongs in the standards file so it stops recurring. A standards file that never changes after its first draft is a sign nobody is feeding it real corrections.

## Scope the session on purpose

What the assistant can *see* is what it can edit. Two habits keep that scope deliberate rather than accidental:

- **Open only what the task needs.** A single-repo window keeps edits contained to that repo. A multi-root workspace ([10_from_scripts_to_pipelines.md](10_from_scripts_to_pipelines.md)) is for when you genuinely need the assistant to read or edit across repos in one sitting — a reference exemplar beside the repo you're building, for example. Every repo in the workspace is one it can change, so add repos for a reason, not by default.
- **Say the boundary out loud when it matters.** "Read the exemplar repo for its module layout, but only edit files in this repo" is a real instruction the assistant follows — it is not implied by which windows happen to be open. For a harder boundary, use a **git worktree**: a second working directory on its own branch, so changes land in an isolated copy you review before merging, at a fraction of the cost of a second clone ([advanced_git.md](../reference/advanced_git.md)).

## Ask for the plan before the diff

For anything beyond a one-line fix, have the assistant lay out its approach before it starts editing files — which functions it will touch, what it will add versus change, what it is deliberately leaving alone. This costs a minute and catches two common problems early: a misunderstanding of what you actually asked for, and scope creep (refactoring or "improving" code nobody asked to touch). Many assistants, including Claude Code, have an explicit read-only planning mode for this; use it for anything you would not want to redo.

Review in chunks you can actually hold in your head. A 400-line diff touching six files gets a skim, not a review, and a skimmed review is the review step failing quietly. If a change is that large, ask the assistant to split it — by file, by function, or into a sequence of smaller commits — rather than reviewing it as one block.

## A verification-in-practice playbook

[18_ai_assisted_development.md](18_ai_assisted_development.md) states the rule: a clean run is not a correct analysis. In practice, that means watching for specific failure modes and having a standard move for each:

- **A plausible number from the wrong formula.** Looks identical to a correct one until you check it. Cross-check with a known-good case, an independent method, or a hand calculation — the checks in [18_ai_assisted_development.md](18_ai_assisted_development.md) — before trusting a new result.
- **An invented API.** A function, argument, or library behavior that does not exist, stated with full confidence. Verify against the actual installed version: run it, or grep the library's source, rather than trusting the assistant's description of it.
- **Silent scope creep.** A "fix the bug" request comes back with an unrelated refactor, a new abstraction, or an added dependency. Read every changed file, not only the one you expected to change — `git diff --stat` before you read the detail, so nothing unexpected slides through.
- **A dropped edge case.** Especially during a refactor: the new version handles the common path but silently loses handling for an edge case the old code had. This is what regression tests ([12_testing_with_pytest.md](12_testing_with_pytest.md)) are for — run the existing suite before trusting a refactor, not just the new code path.
- **A test that passes without testing anything.** Asked to write tests, an assistant can produce ones that assert a mock's own return value, check only that a function didn't raise, or restate the implementation's logic instead of an independent expectation — green, and worthless. Read a generated test the way you'd read the code it covers: would it actually fail if the logic were wrong?
- **Confident overreach on ambiguous asks.** Asked something underspecified, an assistant tends to pick an interpretation and run rather than asking. If a request could reasonably mean two things, say which one — or expect to review for the one you didn't mean.
- **The assistant's interpretation, presented as if it were yours.** Asked to describe a result, an assistant will often also assert what it *means* or recommend what to do next — fluently, and not necessarily right. Keep that judgment call out of the assistant's own prose; it belongs in your own signed blockquote instead ([16_running_a_dry_lab_experiment.md](16_running_a_dry_lab_experiment.md)), even if that means leaving a `_pending_` placeholder rather than an answer filled in for you.

The common thread: none of these announce themselves. The code runs, the output looks reasonable, and the assistant sounds sure. Treat fluency and confidence as unrelated to correctness, and check accordingly.

## Ending a session

Before closing a session that made real progress, make sure anything durable is written down somewhere that outlives the chat: findings and next steps in the research log, not left in the ephemeral conversation ([16_running_a_dry_lab_experiment.md](16_running_a_dry_lab_experiment.md)). A long research thread is easy to keep going in one continuous session, but if the conversation itself becomes the only record of what was decided and why, that reasoning disappears the moment the session ends. When a session has drifted — you are re-explaining context it should already have, or corrections aren't sticking — starting a fresh session with an updated standards file and a clear research log is usually faster than continuing to patch a confused one.

## The bottom line

None of this replaces the principles in [18_ai_assisted_development.md](18_ai_assisted_development.md) — it is how you actually apply them, session after session: a standards file that is short enough to follow, a scope you set on purpose, a plan before a diff, specific checks for the ways confident output fails silently, and a research log that outlives the chat.
