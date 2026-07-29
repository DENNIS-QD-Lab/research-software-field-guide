# Code quality tools: linting, formatting, and type checking

Your project's coding-standards file (here, [CLAUDE.md](../../CLAUDE.md)) says code follows PEP 8 and is formatted with ruff, and you have probably seen ruff run when you commit. This doc explains what that tooling actually does, how to run it yourself, and adds one more tool: mypy, for type checking.

## Three tools, three jobs

- **Linting** finds likely *mistakes and bad patterns*: an unused variable, a name that is never defined, a shadowed import. A linter reads your code and reports problems.
- **Formatting** rewrites *layout*: indentation, spacing, line length, quote style. It does not change what the code does, only how it looks, and it ends every argument about style by having a tool decide.
- **Type checking** reads your *type hints* and flags mismatches, such as passing a string where a function expects an integer, before you ever run the code.

This guide uses **ruff** for the linting and formatting, and **mypy** for the type checking.

## ruff format: fix the layout

```
ruff format .
```

This rewrites every Python file in the current directory and below to the standard layout. The `.` means "here." It changes only appearance, never behavior. Per [CLAUDE.md](../../CLAUDE.md), do not hand-format code; let this do it. To see what it *would* change without changing anything:

```
ruff format --diff .
```

## ruff check: find the problems

```
ruff check .
```

This scans for lint problems and prints each one; it does not modify your files. Many problems are mechanical, and ruff can fix those for you:

```
ruff check --fix .
```

This fixes the safe, automatic cases (removing an unused import, sorting imports). What it *cannot* fix, it only reports, because the fix needs a human decision. An undefined name, for example, means you have a real bug to resolve, not a formatting choice to automate.

## Reading a ruff message

A message looks like this:

```
analysis.py:42:5: F841 Local variable 'result' is assigned to but never used
```

Read it left to right: the file, the line number, the column, then a **rule code** (`F841`), then a plain description. The rule code is a stable identifier you can look up:

```
ruff rule F841
```

This prints an explanation of what the rule checks and why. The letter groups rules by family (`F` for likely bugs, `E` for PEP 8 style, `I` for import sorting, and so on). You can also search the code on the ruff website.

## These already run when you commit

ruff format and ruff check are wired into this repo's pre-commit hook, so most of the time they run *automatically* when you commit, and a commit that would introduce a problem is stopped before it lands. Running them by hand, as above, is for checking your work before you commit or fixing a whole batch at once.

Two setup commands you run once, not every day:

```
pre-commit install
```

This installs the hook into a repo so it runs on every commit. Do it once after you clone a repo that has a `.pre-commit-config.yaml`.

```
pre-commit run --all-files
```

This runs every hook over every file, instead of only the files you changed. Use it the first time you adopt the hooks on an existing codebase, to bring the whole thing up to standard in one pass.

## mypy: type checking

[00_python_code_basics.md](../onboarding/00_python_code_basics.md) introduced type hints such as `list[int]` and `str | None`. Those hints are for human readers and for checkers; Python does not enforce them when the code runs. **mypy is the checker.** It reads your hints and reports where the types do not line up, before you run anything.

```
mypy analysis.py
```

This checks the types in that file. It catches a whole class of bug statically: passing the wrong type into a function, or using a value that might be `None` without handling the `None` case. That is a bug you would otherwise only find at runtime, maybe only on the input that triggers it.

For now, **run mypy by hand.** It is not part of the pre-commit hook, so it will not block a commit; point it at the file or module you are working on. And do not add runtime type assertions just to satisfy it ([CLAUDE.md](../../CLAUDE.md) says so): the hints plus mypy are the mechanism, and the checking happens before the code runs, not during.

A caveat for real codebases: on code that is not fully type-hinted yet, mypy can be noisy at first. Do not try to fix everything at once. Start with the one module you are hardening, add hints until that module is clean, and move on. This mirrors the advice in [15_experiments_and_shipping.md](15_experiments_and_shipping.md): harden what has stabilized, not the whole repo in a single push.

## When a tool flags something

- **Formatting:** let it reformat. Do not fight it.
- **A lint problem ruff can fix:** run `ruff check --fix .`.
- **A lint problem it cannot fix, or a mypy error:** read the message. It is almost always pointing at something real. If a rule is unclear, run `ruff rule <code>` or ask a teammate.
