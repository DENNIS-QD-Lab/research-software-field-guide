# Using VS Code

VS Code is a common integrated development environment (IDE), i.e., code editor. This doc assumes you have it installed with the Python and Jupyter extensions, and that you have opened the `research-software-field-guide` repository.

## One folder, one window

When you open a folder in VS Code, that folder becomes the one thing VS Code pays attention to: the Source Control panel, the terminal's starting point, the Python interpreter, and search all follow whatever folder you opened. This works perfectly as long as the folder you open is a single repository.

Do not open parent folders containing multiple repository folders in VS Code. For example, if you open a "Projects" folder with `research-software-field-guide` and other repos sitting inside it as subfolders, VS Code has no way to tell those apart as separate projects. Instead it sees one big folder, so the Source Control panel, the terminal, and everything else end up pointed at the wrong repository, or some ambiguous mix of all of them.

Always open the repository folder itself — `research-software-field-guide`, not its parent — in its own window. Do this once per repository; switch between windows using your operating system's normal window switcher. The quickest way to open a repository correctly: right-click its folder in Finder (Mac) or File Explorer (Windows) and choose "Open with VS Code."

## Workspaces (opening more than one repository)

Every folder you open this way is technically a **workspace** — VS Code just doesn't use that word until you need more than one folder in it. For now, one workspace = one repository = one window, and you can ignore the term entirely.

Occasionally you'll want to open two repositories side by side. Instead of opening their shared parent folder, open one repository and then explicitly add the second repository as its own folder in the same window (File > Add Folder to Workspace). VS Code then keeps the two folders administratively separate: each gets its own Source Control panel, its own terminal, its own interpreter setting, instead of blending them into one ambiguous project.

Once you've added a folder this way, File > Save Workspace As saves the combination to a `.code-workspace` file — put it outside any of the repositories, for example on the Desktop. Double-clicking that file later reopens the same folders together. This also works for a single repository you open often: it's the lightest way to bookmark a project, even before you ever need a second folder.

## The Explorer sidebar

The file tree on the left is the Explorer. Files marked with a colored letter carry a Git status: a yellow **M** means modified since the last commit, a green **U** means untracked (Git does not know about this file yet), and a green **A** means staged to be added. Files shown dimmed are being ignored by Git per `.gitignore`. They are still on your disk and you can still open them; Git simply is not tracking them.

## The Outline view

At the bottom of the Explorer sidebar is the Outline view (expand the "Outline" header if it is collapsed). For a Python file it lists the functions and classes in that file. Click an entry to jump to it. This is useful for navigating longer scripts.

## The integrated terminal

Terminal > New Terminal opens a shell at the repository root. This is the same terminal used for the `git`, `conda`, and `python` commands throughout these docs. You can open several at once with the + icon in the terminal panel and switch between them with the dropdown.

## The Source Control panel

The third icon down on the far-left activity bar, shaped like a branch, is the Source Control panel. This is VS Code's Git interface. It shows the files that have changed since the last commit and lets you stage them, write a commit message, and commit. This is the recommended path for daily work. The equivalent terminal commands are in [05_daily_workflow.md](05_daily_workflow.md).

## Selecting the Python interpreter

Cmd+Shift+P (Mac) or Ctrl+Shift+P (Windows) opens the Command Palette, which runs any VS Code command by name. Typing "Python: Select Interpreter" is how you tell VS Code which environment to run `.py` files with, and VS Code remembers the choice per workspace. [04_environments.md](04_environments.md) covers creating this repo's `fieldguide` environment and selecting it here once it exists.

## Selecting the Jupyter kernel

When you open a `.ipynb` file, the kernel selector sits in the top-right of the notebook editor. The kernel is a notebook's equivalent of the interpreter above, selected separately, so the two can be mismatched — a common source of "I installed the package but the notebook says it is missing." [04_environments.md](04_environments.md) covers picking the `fieldguide` environment as both your interpreter and your kernel; [07_notebooks.md](07_notebooks.md) has more on working with notebooks day to day.

## Opening VS Code from the terminal with `code`

Once you can run `code` from a terminal, `code .` opens the current folder in VS Code and `code path/to/folder` opens any folder. This is the reverse of the "Open with VS Code" pattern from earlier and is handy once you're already in a terminal instead of Finder or File Explorer. On Mac you enable it once: open the Command Palette (Cmd+Shift+P), type "Shell Command", and choose "Shell Command: Install 'code' command in PATH". On Windows the installer adds `code` to your PATH automatically, as long as the "Add to PATH" option was left checked during installation.

## Markdown preview

For any `.md` file, including these docs, right-click the file tab and choose "Open Preview" to render the markdown instead of showing raw text. The hot key Cmd+Shift+V (Mac) or Ctrl+Shift+V (Windows) helpfully toggles between the rendered preview and the editable raw text view.

In this repo, you'll read far more markdown than you write, so it's worth flipping the default so `.md` files open *already rendered*, using Cmd+Shift+V only when you actually want to edit one:

1. Command Palette (Cmd+Shift+P / Ctrl+Shift+P) → "Preferences: Open User Settings (JSON)".
2. Add:
   ```json
   "workbench.editorAssociations": {
       "*.md": "vscode.markdown.preview.editor"
   }
   ```
3. Close and reopen any `.md` tabs that were already open — the association only applies the next time a file is opened, not retroactively to an open tab.

This has to go in your **User** settings, not a repo's `.vscode/settings.json`. It's a window-scoped setting, so per-repo settings files are silently ignored if you're using a multi-root workspace (several repos opened together, as covered in [Workspaces](#workspaces-opening-more-than-one-repository) above). That also means each person has to set it for themselves once; it doesn't travel with the repo.

## Do not drag tracked files between folders

Dragging a tracked file to a new folder in the Explorer works, but Git sees it as "delete here, create there" rather than a rename, which clutters the history. For tracked files, use `git mv oldpath newpath` in the terminal instead. For untracked files (the U-marked ones), drag freely.

## Toggle the sidebar

Cmd+B (Mac) or Ctrl+B (Windows) hides and shows the sidebar. This is useful when you want maximum screen space for reading or focused editing.

## Keyboard shortcuts worth memorizing

A fuller list, organized by category, is in [keyboard_shortcuts.md](../reference/keyboard_shortcuts.md); the extensions worth installing are in [vs_code_extensions.md](../reference/vs_code_extensions.md).

- Cmd+P / Ctrl+P: Go to File (fuzzy file search across the workspace)
- Cmd+Shift+F / Ctrl+Shift+F: Find in Files (search file contents across the workspace)
- Cmd+Shift+P / Ctrl+Shift+P: Command Palette (run any VS Code command by name)
- Ctrl+\` / Ctrl+\`: toggle the terminal
- Cmd+B / Ctrl+B: toggle the sidebar