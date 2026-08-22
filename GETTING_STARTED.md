# Getting Started

This sheet gets you from zero to a working copy of this repository on your
computer. Starting from scratch, expect 30–45 minutes. When you are done, open
[docs/onboarding/00_python_code_basics.md](docs/onboarding/00_python_code_basics.md)
inside the repository and keep going from there.

If a step takes more than about 10 minutes of fighting, stop and ask in your
team's chat. These tools are finicky, and asking is faster than thrashing.

> Throughout, `<owner>/<repo>` stands for this repository's location on GitHub.
> Whoever manages the repository will send you the exact clone command; it looks
> like the one in step 6.

<!-- TODO(public-launch): once this repo is public, step 2 and step 6 below still
assume a private, invite-only repo (an org invite, a clone URL sent by a manager).
Rewrite step 2 to drop the invite language and step 6 to give the real public
clone URL directly. -->

## 1. Install VS Code

Download from <https://code.visualstudio.com> and install with the defaults. VS
Code is a common editor: it opens code files, runs Jupyter notebooks, and gives
you a terminal, all in one window.

After installing, open VS Code and add a few extensions. Click the Extensions
icon in the left sidebar (four squares), search for each by name, and click
Install:

1. **Python** (publisher: Microsoft)
2. **Jupyter** (publisher: Microsoft)
3. **Ruff** (publisher: Astral Software) — the linter/formatter this repo uses
4. **Claude Code** (publisher: Anthropic) — optional, if your team uses it

The fuller list, with notes on what each does, is in
[docs/reference/vs_code_extensions.md](docs/reference/vs_code_extensions.md).

## 2. Make a GitHub account

Go to <https://github.com> and sign up. A university email works and makes you
eligible for GitHub's free educational benefits, but any email is fine.

Send your GitHub username to whoever manages the repository. They will add you
to the organization that hosts it, so you can see and clone the repository.

## 3. Install Git

Git is the version-control software that runs on your computer. GitHub is the
website that hosts Git repositories. You need Git locally so your computer can
talk to GitHub.

- **On Mac:** open VS Code, open a terminal (menu: Terminal → New Terminal),
  type `git --version`, and press Enter. If a version number prints, you already
  have it. If you are prompted to install the command line developer tools, click
  Install and wait for it to finish.
- **On Windows:** download Git for Windows from
  <https://git-scm.com/download/win> and install with the defaults. When the
  installer asks about a default editor, choose "Use Visual Studio Code." Leave
  everything else at defaults.

Confirm: open VS Code's terminal and type `git --version`. You should see a
version number.

## 4. Install Miniconda

Miniconda is the Python distribution and environment manager we recommend if you
are not already using one (no need to install Miniconda if you already have
Anaconda). Download the installer for your operating system from
<https://docs.conda.io/en/latest/miniconda.html> and run it with the defaults.

After installing, fully quit VS Code (Cmd+Q on Mac, close all windows on Windows)
and reopen it. This step matters: the terminal has to restart before it knows
about conda. Then open a new terminal in VS Code and type `conda --version`. You
should see a version number. If you do not, ask before going further.

## 5. Pick a home for your code

Make a folder where all your code projects will live. This folder **must be
local** — not inside iCloud Drive, OneDrive, Dropbox, or any other cloud-synced
folder. Cloud sync and Git fight each other, and some of the most painful,
hardest-to-diagnose bugs come from this. Just don't.

A good choice is `~/repos/` on Mac or `C:\Users\YourName\repos\` on Windows. In VS
Code's terminal, create it and move into it:

```
mkdir ~/repos
cd ~/repos
```

`mkdir` makes a directory; `cd` changes into it. More on these commands in
[docs/onboarding/01_command_line_basics.md](docs/onboarding/01_command_line_basics.md).

## 6. Clone the repository

"Cloning" means making a local copy of a GitHub repository on your computer. From
inside your `repos/` folder, run the command you were sent, which will look like:

```
git clone https://github.com/<owner>/<repo>.git
```

This creates a folder named after the repository inside `repos/`. Move into it
(substitute the real name):

```
cd <repo>
```

## 7. Open the repository in VS Code

Still in the terminal, type:

```
code .
```

The `.` means "the current folder." VS Code opens with the repository as your
workspace, and its files appear in the left sidebar.

## You are done with setup

Inside VS Code, open
[docs/onboarding/00_python_code_basics.md](docs/onboarding/00_python_code_basics.md).
To see it rendered nicely instead of as raw text, right-click the file tab and
choose "Open Preview" (or press Cmd+Shift+V on Mac, Ctrl+Shift+V on Windows).
Read the docs in order — they build on each other.
