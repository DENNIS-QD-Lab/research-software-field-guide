# github-sync: personal settings

Copy this file to `LOCAL.md` in the same folder and edit it to match how you work. The skill reads
`LOCAL.md` first, and its settings override the skill's defaults. `LOCAL.md` is personal: add
`.claude/skills/*/LOCAL.md` to the repository's `.gitignore` so it is never committed. Delete any
section that does not apply to you.

## GitHub access

- Mode: hand-off
  (`direct`: the assistant can fetch, push, and use `gh` itself, after asking.
  `hand-off`: the assistant cannot reach GitHub from its session, so it asks me to fetch and gives
  me every push and `gh` command to run.)

## Shell

- zsh

## Repositories to survey

- ~/code/analysis
- ~/code/pipeline

## Pushes

- Push in stages when a branch adds more than 20 MB of new data.
- HTTP/1.1 is already set (`git config http.version HTTP/1.1`) in: analysis.

## Branches that belong to other people

- analysis: `maria-imaging` (Maria). Never delete or rebase.

## Pull request descriptions

- Save description files in: /tmp
- End each description with: (an attribution line, if your lab uses one)
