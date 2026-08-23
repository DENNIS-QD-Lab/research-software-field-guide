# repo_kit — a portable research-software standard

A small, reusable kit for bringing *any* research repository up to the standard the
research-software-field-guide [implementing track](../docs/implementing/) teaches. It distills
that tutorial into three single-purpose files (plus fill-in templates) so a repo can adopt the standard
without walking the whole track.

The three pieces mirror the **state / procedure / standards** split the standard itself uses, so the kit
practices what it teaches:

| File | Audience | What it is |
|------|----------|------------|
| [STANDARD.md](STANDARD.md) | a researcher who already codes | The **why**: goal, repo structure, and the key decisions with their reasoning. Read once; no tutorial. |
| [SETUP_PLAYBOOK.md](SETUP_PLAYBOOK.md) | Claude Code | The **how**: actionable recipes to scaffold a new repo or upgrade an existing one, each with a verify gate. |
| [CLAUDE.template.md](CLAUDE.template.md) | both (loaded every session) | The **standing standards**: copy to the target repo's `CLAUDE.md` and fill the placeholders. |

Plus [`templates/`](templates/) — the per-repo files the playbook installs (they are project-specific,
so they ship as fill-in templates, not static files):

- [research_log.template.md](templates/research_log.template.md) → target `experiments/README.md` (state)
- [experiment_readme.template.md](templates/experiment_readme.template.md) → target `experiments/_TEMPLATE.md`
- [experiments_playbook.template.md](templates/experiments_playbook.template.md) → target `.claude/experiments_playbook.md` (procedure)
- [vscode_settings.template.json](templates/vscode_settings.template.json) → target `.vscode/settings.json` (Markdown renders by default)
- [CONTRIBUTING.template.md](templates/CONTRIBUTING.template.md) → target `CONTRIBUTING.md` (only once more than one person works in the repo)

## How to use it

**Adopting the standard in a repo (new or existing):** open the target repo alongside this one and ask
Claude Code to follow [SETUP_PLAYBOOK.md](SETUP_PLAYBOOK.md) —
- *New repo* → the playbook's *Mode A : Scaffold* sequence (take only the pieces you need).
- *Existing repo* → *Mode B: Upgrade recipes*, à la carte (add tests, add a doc site, restructure to
  `src/` + `experiments/`, …).

**Just want the conventions?** Copy [CLAUDE.template.md](CLAUDE.template.md) into your repo as `CLAUDE.md`,
fill the `<placeholders>`, and the assistant follows it every session — no other setup required.

**Want the reasoning first?** Read [STANDARD.md](STANDARD.md); it links each decision to the
implementing-track doc that teaches it in full.

## Scope

This kit is the *summary and operational form* of the implementing and disseminating tracks — it never
contradicts them. When in doubt, the tracks (docs 10–20, then 21–23) are the source of truth, and the
config skeletons (`pyproject.toml`, `ci.yml`, `conf.py`) live there rather than being duplicated here, so
the two cannot drift.
