# Using VS Code

VS Code is the lab's editor. This doc assumes you have it installed with the Python and Jupyter extensions, and that you have just opened the `DENNIS_helpers` repository. It covers the conventions you need and nothing more.

## One folder, one window

Open the repository folder itself, not a parent folder that contains several repositories. The Source Control panel, the integrated terminal's starting directory, the Python interpreter selection, and the search scope are all tied to the open folder. With multiple repositories in one window, all of these become ambiguous or wrong.

The standard pattern is one VS Code window per repository. Switch between windows with the OS window switcher. The quickest way to open a repository correctly is to right-click its folder in Finder (Mac) or File Explorer (Windows) and choose "Open with VS Code," which opens it in its own window.

## Workspaces (optional but helpful)

After opening a repository folder, File > Save Workspace As lets you save a `.code-workspace` file. Put it outside the repository, for example on the Desktop. Double-clicking that file later reopens VS Code with the same setup. This is the lightest way to bookmark your projects.

## The Explorer sidebar

The file tree on the left is the Explorer. Files marked with a colored letter carry a Git status: M means modified since the last commit, U means untracked (Git does not know about this file yet), and A means staged to be added. Files shown dimmed are being ignored by Git per `.gitignore`. They are still on your disk and you can still open them; Git simply is not tracking them.

## The Outline view

At the bottom of the Explorer sidebar is the Outline view (expand the "Outline" header if it is collapsed). For a Python file it lists the functions and classes in that file. Click an entry to jump to it. This is useful for navigating longer scripts.

## Setting up the `code` command (one-time setup)

Before you can open VS Code from the terminal with `code .`, you need to 
install the shell command once. Press Cmd+Shift+P, type "shell command", 
and select "Shell Command: Install 'code' command in PATH". You only do 
this once. After that, typing `code .` in any terminal folder opens that 
folder in VS Code.

## The integrated terminal

Terminal > New Terminal opens a shell at the repository root. This is the same terminal used for the `git`, `conda`, and `python` commands throughout these docs. You can open several at once with the + icon in the terminal panel and switch between them with the dropdown. Cmd+\` (Mac) or Ctrl+\` (Windows) toggles the terminal panel open and closed.

## The Source Control panel

The third icon down on the far-left activity bar, shaped like a branch, is the Source Control panel. This is VS Code's Git interface. It shows the files that have changed since the last commit and lets you stage them, write a commit message, and commit. This is the path the lab recommends for daily work. The equivalent terminal commands are in `docs/onboarding/05_daily_workflow.md`.

## Selecting the Python interpreter

Cmd+Shift+P (Mac) or Ctrl+Shift+P (Windows) opens the Command Palette, which runs any VS Code command by name. Type "Python: Select Interpreter" and choose the `helper` conda environment. VS Code remembers this choice per workspace. There is more on this in `docs/onboarding/04_environments.md`.

## Selecting the Jupyter kernel

When you open a `.ipynb` file, the kernel selector sits in the top-right of the notebook editor. It must show the `helper` environment. If it does not, click it and choose the right one. The kernel is selected separately from the Python interpreter, and the two can be mismatched. That mismatch is a common source of "I installed the package but the notebook says it is missing." See `docs/onboaring/04_environments.md` and `docs/onboarding/07_notebooks.md`.

## Markdown preview

For any `.md` file, including these docs, right-click the file tab and choose "Open Preview," or press Cmd+Shift+V (Mac) or Ctrl+Shift+V (Windows). This renders the markdown instead of showing raw text.

## Do not drag tracked files between folders

Dragging a tracked file to a new folder in the Explorer works, but Git sees it as "delete here, create there" rather than a rename, which clutters the history. For tracked files, use `git mv oldpath newpath` in the terminal instead. For untracked files (the U-marked ones), drag freely.

## Toggle the sidebar

Cmd+B (Mac) or Ctrl+B (Windows) hides and shows the sidebar. This is useful when you want maximum screen space for reading or focused editing.

## Keyboard shortcuts worth memorizing

- Cmd+P / Ctrl+P: Go to File (fuzzy file search across the workspace)
- Cmd+Shift+F / Ctrl+Shift+F: Find in Files (search file contents across the workspace)
- Cmd+Shift+P / Ctrl+Shift+P: Command Palette (run any VS Code command by name)
- Cmd+\` / Ctrl+\`: toggle the terminal
- Cmd+B / Ctrl+B: toggle the sidebar
