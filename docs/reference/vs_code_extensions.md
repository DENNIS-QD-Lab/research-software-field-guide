# VS Code Extensions

VS Code has thousands of extensions. Most of them you don't need. This is the lab's curated list, in two tiers: install these, and consider these.

To install an extension: click the Extensions icon in the left sidebar (four squares), search by name, click Install.

## Install these

These are baseline for working in this repo.

| Extension | What it does |
|-----------|--------------|
| **Python** (publisher: Microsoft) | The official Python extension. Provides syntax highlighting, linting integration, the "Python: Select Interpreter" command, debugging, and integration with `ruff`. Required for VS Code to understand Python files at all. |
| **Jupyter** (publisher: Microsoft) | Lets VS Code open and run `.ipynb` files directly. Required if you want notebooks. Includes the kernel selector in the top-right of any open notebook. |
| **Pylance** (publisher: Microsoft) | Auto-installed when you install Python, but worth knowing it exists. Provides smart autocomplete, function signatures while typing, type-checking, and "go to definition" (Cmd+click a function name to jump to where it's defined). |
| **Ruff** (publisher: Astral Software) | Surface `ruff check` and `ruff format` results inline in your editor — squiggles under problem lines, format-on-save if you turn it on. The pre-commit hook will run ruff anyway, but seeing the warnings while you type is much better than discovering them at commit time. |

## Consider these

These are useful for specific situations or workflows. Skim the descriptions; install if a description matches a pain point you actually have.

| Extension | What it does |
|-----------|--------------|
| **GitLens** (publisher: GitKraken) | Adds Git context throughout the editor: shows you "this line last changed by X, 3 months ago, in commit Y" inline. Useful for understanding why code is the way it is. Some people find it too noisy; you can turn off individual features in settings. |
| **GitHub Pull Requests** (publisher: GitHub) | Lets you review and comment on PRs from inside VS Code, without bouncing to the browser. Worth it if you find yourself reviewing PRs often. |
| **Markdown All in One** (publisher: Yu Zhang) | Adds keyboard shortcuts for common markdown tasks (bold, italic, list creation, table formatting), plus auto-updates table-of-contents blocks. Pleasant for writing docs. |
| **markdownlint** (publisher: David Anson) | Flags markdown style issues (inconsistent header levels, missing blank lines around lists, etc.). Helpful if you care about clean markdown; safely skippable. |
| **Even Better TOML** (publisher: tamasfe) | Syntax highlighting and validation for `.toml` files. Useful because `pyproject.toml` is TOML, and the default support is mediocre. |
| **YAML** (publisher: Red Hat) | Same idea for `.yaml` / `.yml` files like `environment.yml` and `.pre-commit-config.yaml`. Highlights errors and validates structure. |
| **Path Intellisense** (publisher: Christian Kohler) | Autocompletes file paths as you type them in code or markdown. Saves typos when referencing files. |
| **Rainbow CSV** (publisher: mechatroner) | Colors columns in CSV files so they're readable. Saves you from squinting at comma-separated text when previewing a data file. |
| **Excalidraw** (publisher: pomdtr) | Lets you create and edit hand-drawn-style diagrams directly in VS Code, saved as `.excalidraw` files. Useful for sketching flow diagrams or system architecture for docs. |

## Settings worth turning on

These aren't extensions, but they're settings that pair well with the extensions above. Open Settings with `Cmd+,` (Mac) or `Ctrl+,` (Windows) and search:

**Format on Save** (`editor.formatOnSave`)
Runs the configured formatter every time you save. With Ruff installed and selected as the Python formatter, this means your Python files are always ruff-formatted when saved. Strongly recommended.

**Files: Auto Save** (`files.autoSave`)
Set to `onFocusChange` to automatically save when you click away from a file. Prevents lost work and surprises when Git asks "what about your unsaved changes?"

**Editor: Render Whitespace** (`editor.renderWhitespace`)
Set to `boundary` or `selection` to make trailing spaces and mixed tabs visible. Useful when invisible whitespace bugs are biting you.

**Files: Trim Trailing Whitespace** (`files.trimTrailingWhitespace`)
Removes trailing spaces on save. Small thing, makes diffs cleaner.

## How to discover good extensions later

When you find yourself doing something repeatedly in VS Code and wishing it were faster, search the Extensions marketplace for that workflow before assuming the friction is inherent. Often someone has built exactly the extension you need.

When considering a new extension, check: how many installs does it have (more is usually better, in the thousands or millions), when was it last updated (within the last year is a good sign), and what does the description actually do (vague descriptions are a warning sign).

If you find one worth recommending, add it to this doc and open a PR.