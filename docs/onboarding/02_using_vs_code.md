# Using VS Code

VS Code is a common integrated development environment (IDE)-- i.e., code editor. This doc assumes you have it installed with the Python and Jupyter extensions, and that you have opened the `research-software-field-guide` repository. It covers the conventions you need and nothing more.

## One folder, one window

Open the repository folder itself, not a parent folder that contains several repositories. The Source Control panel, the integrated terminal's starting directory, the Python interpreter selection, and the search scope are all tied to the open folder. With multiple repositories in one window, all of these become ambiguous or wrong.

This is the default for as long as you're working in one repo at a time. [10_from_scripts_to_pipelines.md](../implementing/10_from_scripts_to_pipelines.md#the-multi-root-workspace) covers the deliberate exception, once you actually need two repos open together.

The standard pattern is one VS Code window per repository. Switch between windows with the OS window switcher. The quickest way to open a repository correctly is to right-click its folder in Finder (Mac) or File Explorer (Windows) and choose "Open with VS Code," which opens it in its own window.

## Workspaces (optional but helpful)

After opening a repository folder, File > Save Workspace As lets you save a `.code-workspace` file. Put it outside the repository, for example on the Desktop. Double-clicking that file later reopens VS Code with the same setup. This is the lightest way to bookmark your projects.

## The Explorer sidebar

The file tree on the left is the Explorer. Files marked with a colored letter carry a Git status: a yellow **M** means modified since the last commit, a green **U** means untracked (Git does not know about this file yet), and a green **A** means staged to be added. Files shown dimmed are being ignored by Git per `.gitignore`. They are still on your disk and you can still open them; Git simply is not tracking them.

## The Outline view

At the bottom of the Explorer sidebar is the Outline view (expand the "Outline" header if it is collapsed). For a Python file it lists the functions and classes in that file. Click an entry to jump to it. This is useful for navigating longer scripts.

## The integrated terminal

Terminal > New Terminal opens a shell at the repository root. This is the same terminal used for the `git`, `conda`, and `python` commands throughout these docs. You can open several at once with the + icon in the terminal panel and switch between them with the dropdown. 

## Opening VS Code from the terminal with `code`

Once you can run `code` from a terminal, `code .` opens the current folder in VS Code and `code path/to/folder` opens any folder. This is the reverse of the "Open with VS Code" pattern above and is handy when you are already in a terminal. On Mac you enable it once: open the Command Palette (Cmd+Shift+P), type "Shell Command", and choose "Shell Command: Install 'code' command in PATH". On Windows the installer adds `code` to your PATH automatically, as long as the "Add to PATH" option was left checked during installation.

## The Source Control panel

The third icon down on the far-left activity bar, shaped like a branch, is the Source Control panel. This is VS Code's Git interface. It shows the files that have changed since the last commit and lets you stage them, write a commit message, and commit. This is the recommended path for daily work. The equivalent terminal commands are in [05_daily_workflow.md](05_daily_workflow.md).

## Selecting the Python interpreter

Cmd+Shift+P (Mac) or Ctrl+Shift+P (Windows) opens the Command Palette, which runs any VS Code command by name. Type "Python: Select Interpreter" and choose the `helper` conda environment. VS Code remembers this choice per workspace. There is more on this in [04_environments.md](04_environments.md).

## Selecting the Jupyter kernel

When you open a `.ipynb` file, the kernel selector sits in the top-right of the notebook editor. It must show the `helper` environment. If it does not, click it and choose the right one. The kernel is selected separately from the Python interpreter, and the two can be mismatched. That mismatch is a common source of "I installed the package but the notebook says it is missing." See [04_environments.md](04_environments.md) and [07_notebooks.md](07_notebooks.md).

## Markdown preview

For any `.md` file, including these docs, right-click the file tab and choose "Open Preview" to render the markdown instead of showing raw text. The hot key Cmd+Shift+V (Mac) or Ctrl+Shift+V (Windows) helpfully toggles between the rendered preview and the editable raw text view.

You'll read far more markdown than you write, so it's worth flipping the default so `.md` files open *already rendered*, using Cmd+Shift+V only when you actually want to edit one:

1. Command Palette (Cmd+Shift+P / Ctrl+Shift+P) → "Preferences: Open User Settings (JSON)".
2. Add:
   ```json
   "workbench.editorAssociations": {
       "*.md": "vscode.markdown.preview.editor"
   }
   ```
3. Close and reopen any `.md` tabs that were already open — the association only applies the next time a file is opened, not retroactively to an open tab.

This has to go in your **User** settings, not a repo's `.vscode/settings.json`. It's a window-scoped setting, so per-repo settings files are silently ignored if you're using a multi-root workspace (several repos opened together, as in [one folder, one window](#one-folder-one-window) above). That also means each person has to set it for themselves once; it doesn't travel with the repo.

## Do not drag tracked files between folders

Dragging a tracked file to a new folder in the Explorer works, but Git sees it as "delete here, create there" rather than a rename, which clutters the history. For tracked files, use `git mv oldpath newpath` in the terminal instead. For untracked files (the U-marked ones), drag freely.

## Toggle the sidebar

Cmd+B (Mac) or Ctrl+B (Windows) hides and shows the sidebar. This is useful when you want maximum screen space for reading or focused editing.

## Keyboard shortcuts worth memorizing

- Cmd+P / Ctrl+P: Go to File (fuzzy file search across the workspace)
- Cmd+Shift+F / Ctrl+Shift+F: Find in Files (search file contents across the workspace)
- Cmd+Shift+P / Ctrl+Shift+P: Command Palette (run any VS Code command by name)
- Ctrl+\` / Ctrl+\`: toggle the terminal
- Cmd+B / Ctrl+B: toggle the sidebar