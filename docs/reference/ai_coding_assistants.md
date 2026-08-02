# AI coding assistants

Setup, essential commands, and cost/context management for an AI coding assistant, using Claude Code (this repo's assistant) as the concrete example. [19_driving_an_ai_assistant.md](../implementing/19_driving_an_ai_assistant.md) covers how to work *well* with an assistant once it's running; this doc gets one running and covers the mechanical day-to-day of a session.

**This corner of the tooling moves fast.** Specific commands, menus, and pricing below are a snapshot, not a promise — if something here doesn't match what you see on screen, trust the tool's own docs (`claude --help`, or the equivalent for your assistant) over this page, and send a PR to fix it.

## Installing Claude Code

Claude Code runs in a terminal and integrates with an editor; it is not itself a VS Code extension you search for in the Extensions marketplace.

- **Terminal install:** follow the instructions at [claude.com/claude-code](https://claude.com/claude-code) for your OS — this typically means running an installer script or `npm install -g @anthropic-ai/claude-code`, if you have Node.js already. The first time you run it, it asks you to log in: a **paid** Claude.ai plan (Pro, Max, Team, or Enterprise) or an API key. A free Claude.ai account is not enough on its own.
- **VS Code integration:** install the **Claude Code** extension (publisher: Anthropic) from the Extensions marketplace ([vs_code_extensions.md](vs_code_extensions.md)). It gives you a sidebar panel and inline diff review, driving the same underlying tool as the terminal version.
- **Alternatives exist** — GitHub Copilot, Cursor, Codeium/Windsurf, and others each have their own install path and UI. The mechanics below (context limits, session hygiene, multi-agent tradeoffs) are the vendor-neutral part; the specific commands are Claude Code's.

## Starting a session

Open a terminal at the repository root (VS Code: Terminal > New Terminal) and run:

```
claude
```

This starts an interactive session in that folder. The assistant automatically reads this repository's `CLAUDE.md` at the start of the session — that is why generated code already follows the conventions here without you re-explaining them each time ([18_ai_assisted_development.md](../implementing/18_ai_assisted_development.md)).

## What the assistant remembers between sessions

There are two separate memory mechanisms, and it helps not to confuse them:

- **The standards file — you write it.** `CLAUDE.md` is read automatically at the start of every session (above). A project's `CLAUDE.md` lives in the repo (at the root, or in `.claude/CLAUDE.md`) and is checked in, so the whole team shares it and it is versioned like any other file. You can also keep a personal `~/.claude/CLAUDE.md` of your own preferences that applies across all your projects. These files exist only if someone creates them — a repo with no `CLAUDE.md` simply has no project memory. This is the memory you curate: standards, conventions, project context ([18_ai_assisted_development.md](../implementing/18_ai_assisted_development.md)). Edit it like any file, or just ask the assistant to update it.

- **An automatic memory — the assistant writes it.** Claude Code also keeps its own memory that it updates on its own, jotting down corrections you have made and preferences it has picked up. It is on by default and stored **on your machine, outside the repo** — under `~/.claude/` in a per-project `memory/` folder, not in version control. Because it is personal and local, your collaborators never see it and it does not travel with the repo.

That second point matters for research. Personal auto-memory is a convenience, not a record: anything that needs to be shared, reviewed, or reproduced — a standard, a decision, a finding — belongs in a file that is actually in the repo (the standards file, or the research log of [16_running_a_dry_lab_experiment.md](../implementing/16_running_a_dry_lab_experiment.md)), not left to an assistant's private memory. When it matters whether something is really "remembered," check the file, not the assistant's word for it.

## Using this guide as a live reference while you build

A useful setup for your own repos: open **this field guide alongside the repo you are building** in one multi-root workspace, so the assistant can read both at once ([10_from_scripts_to_pipelines.md](../implementing/10_from_scripts_to_pipelines.md) covers multi-root workspaces). This guide then acts as the reference — the assistant reads its docs and `repo_kit/` for how to set things up and what the standards are, while nearly all the actual editing happens in your new repo.

Keep the direction of editing deliberate ([19_driving_an_ai_assistant.md](../implementing/19_driving_an_ai_assistant.md) on scoping which repo the assistant touches): the default is "read this guide, edit my repo." But the guide is a living document — if while building you hit something it gets wrong, explains poorly, or doesn't cover yet, that is worth fixing here too, so the next person (or your next repo) has a smoother path. Make those edits as a normal contribution to this repo ([08_code_review.md](../onboarding/08_code_review.md)), separate from your project's own commits.

## Commands worth knowing on day one

Typed at the prompt, inside a session:

| Command | What it does |
|---|---|
| `/clear` | Wipes the conversation and starts over with an empty context. Use between unrelated tasks. |
| `/compact` | Summarizes the conversation so far to free up context space, keeping the gist without the full transcript. Use mid-task when a session has been running a while but you want to keep going. |
| `/help` | Lists available commands. |
| `/cost` | Shows token usage and estimated cost for the current session. |
| Esc | Interrupts whatever the assistant is currently doing — use it the moment output looks wrong, rather than waiting for it to finish. |

Permission prompts (approving a file edit, a command, or a tool call) appear inline as the assistant works; how much it can do without asking is a setting you control, and it is worth starting cautious (approve each change) until you have a feel for what the assistant tends to do.

## Managing context and cost

An assistant's **context window** is the amount of conversation, file contents, and tool output it can hold at once. Every message, every file it reads, and every command's output counts against that budget. Signs you are running up against it:

- The assistant re-asks something you already told it, or seems to have "forgotten" a decision from earlier in the session.
- Responses get noticeably slower.
- `/cost` shows a session that has grown much larger than the task warrants.

The fix is usually one of: `/compact` (keep going, shed the excess), `/clear` and re-state the essentials (clean slate), or simply starting a new session for the next task rather than one marathon conversation covering unrelated work. Cost scales with how much gets read and generated — a session that opens and re-reads large files repeatedly, or one left running across many unrelated asks, costs more than several short, focused ones.

## Multi-agent / subagents

Some assistants, including Claude Code, can delegate part of a task to a separate sub-agent — for example, a research or search task run in parallel while you keep working, or a large task split into independent pieces run concurrently.

**Helps when:** the sub-tasks are genuinely independent (two unrelated files, a search that doesn't depend on the main conversation's state) and each piece is large enough that the coordination overhead is worth it — a broad codebase search, or an isolated review pass, are good candidates.

**More error-prone or costly when:** the pieces actually depend on each other (agent B needs to see what agent A just decided) or the task is small enough that one focused pass would have been faster and cheaper than orchestrating several. Each sub-agent doing real work consumes its own tokens, so running several at once adds up faster than one focused conversation — it is not free parallelism, even when it saves *your* time.

Treat this as a tool to reach for on large, decomposable tasks, not a default mode — and expect the specifics of when it helps to keep changing as the tools mature.
