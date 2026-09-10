# AI coding assistants

Setup, essential commands, and cost/context management for an AI coding assistant, using Claude Code (this repo's assistant) as the concrete example. [19_driving_an_ai_assistant.md](../implementing/19_driving_an_ai_assistant.md) covers how to work *well* with an assistant once it's running; this doc gets one running and covers the mechanical day-to-day of a session.

**This corner of the tooling moves fast.** Specific commands, menus, and pricing below reflect this doc's last update and may already be out of date — if something here doesn't match what you see on screen, trust the tool's own docs (`claude --help`, or the equivalent for your assistant) over this page, and send a PR to fix it.

## Installing Claude Code

Claude Code is fundamentally a terminal tool. A VS Code extension also exists and gives it a native editor presence — same underlying engine either way, not two separate products.

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

- **An automatic memory — the assistant writes it.** Claude Code also keeps its own memory that it updates on its own, jotting down corrections you have made and preferences it has picked up. It is on by default and stored **on your machine, outside the repo** — under `~/.claude/` in a per-project `memory/` folder, not in version control. Because it is personal and local, your collaborators never see it and it does not travel with the repo. (Note, this also means that if you work on multiple machines, e.g., a laptop and a desktop, the automatic Claude memory is specific to that computer.)

In this context, your research cannot rely on the local AI auto-memory. Anything that needs to be shared, reviewed, or reproduced like a result, a research decision, or an experimental plan belongs in a file that is actually in the repo (the standards file, or the research log of [16_running_a_dry_lab_experiment.md](../implementing/16_running_a_dry_lab_experiment.md)). 

## Skills: a procedure the assistant loads only when it applies

`CLAUDE.md` is read into every session, which is right for a small set of standards that are always relevant but wrong for a long procedure you only reach for occasionally — the steps for building a publication figure, a release checklist, a data-import routine. A **skill** is where that kind of procedure lives. It is a folder containing a `SKILL.md` file: a one-line description of when the skill applies, followed by the instructions themselves. The assistant keeps only the description in view during a normal session and reads the full instructions when a task matches, so a long procedure costs almost nothing until the moment it is needed.

Skills live in the same two places as `CLAUDE.md`, with the same sharing behavior. A **project skill** sits in the repo at `.claude/skills/<name>/` and is committed, so everyone who clones the repo has it. A **personal skill** sits at `~/.claude/skills/<name>/` on your own machine and applies across all of your projects. Claude Code also ships some skills built in, and others can be installed as plugins, so a few are available without belonging to any repo.

The assistant applies a skill on its own when a task matches the description, and you can also invoke one directly by typing `/<name>`. Because that description is what the assistant matches against, a skill is reached for only when its description says plainly *when* it applies, in the concrete terms a real request would use.

A skill can carry more than instructions. Beside `SKILL.md` it can bundle reference pages the assistant opens only when relevant, scripts it runs, and files it copies into the work — a style file, a template, a checker. The [`repo_kit/skills/publication-figures/`](../../repo_kit/skills/publication-figures/SKILL.md) skill in this repo is a worked example: a workflow for building a manuscript figure, a matplotlib style file, reference pages on color and layout, and a script that checks a palette for colorblind legibility. Copying that folder into a repo's `.claude/skills/` gives every figure the same standard, with the palette and column widths edited to the target journal. The tool's own [skills documentation](https://code.claude.com/docs/en/skills) has the exact `SKILL.md` fields.

Use a skill for a multi-step procedure that should run the same way each time and that you would otherwise re-explain; keep a single standing fact or naming rule in `CLAUDE.md`, where it stays in view every session.

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

Permission prompts (approving a file edit, a command, or a tool call) appear inline as the assistant works; how much it can do without asking is a setting you control, and it is worth starting cautious (approve each change) until you have a feel for what the assistant tends to do. A command prompt shows the literal text it wants to run — [command_line_reference.md](command_line_reference.md) covers how to read one, including compound commands that chain several actions together.

## Managing context and cost

An assistant's **context window** is the amount of conversation, file contents, and tool output it can hold at once. Every message, every file it reads, and every command's output counts against that budget. Signs you are running up against it:

- The assistant re-asks something you already told it, or seems to have "forgotten" a decision from earlier in the session.
- Responses get noticeably slower.
- `/cost` shows a session that has grown much larger than the task warrants.

The fix is usually one of: `/compact` (keep going, shed the excess), `/clear` and re-state the essentials (clean slate), or simply starting a new session for the next task rather than one marathon conversation covering unrelated work. Cost scales with how much gets read and generated — a session that opens and re-reads large files repeatedly, or one left running across many unrelated asks, costs more than several short, focused ones.

## Multi-agent / subagents

Some assistants, including Claude Code, can delegate part of a task to a separate sub-agent — for example, a research or search task run in parallel while you keep working, or a large task split into independent pieces run concurrently.

**Helps when:** the sub-tasks are genuinely independent (two unrelated files, a search that doesn't depend on the main conversation's state) and each piece is large enough that the coordination overhead is worth it — a broad codebase search, or an isolated review pass, are good candidates.

**More error-prone or costly when:** the pieces actually depend on each other (agent B needs to see what agent A just decided) or the task is small enough that one focused pass would have been faster and cheaper than orchestrating several. Each sub-agent doing real work consumes its own tokens, so running several at once adds up faster than one focused conversation.
