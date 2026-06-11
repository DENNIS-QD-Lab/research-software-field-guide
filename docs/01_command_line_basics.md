# Command line basics

The *command line* is a place where you type commands as text instead of clicking buttons. The words *terminal*, *shell*, and *command line* are close enough to mean the same thing for our purposes. You will use it for Git, conda, and running scripts. In VS Code, open one with Terminal > New Terminal; `docs/02_using_vs_code.md` covers that.

## Where you are matters

A terminal is always sitting in some folder, called the *current working directory*. Commands act relative to that folder unless you say otherwise. To see where you are:

```
pwd
```

This prints the working directory ("print working directory").

## Listing files

To see what is in the current folder:

```
ls
```

This lists the files and folders. On Windows the classic command is `dir`, but VS Code's terminal on Windows usually runs PowerShell or Git Bash, where `ls` also works. Use `ls`.

## Moving around

```
cd foldername
```

`cd` means "change directory." `cd foldername` moves into a folder in the current location. Two shortcuts:

```
cd ..
```

moves up one level, into the parent folder.

```
cd ~
```

moves to your home folder.

## Which directory should I be in?

This trips up everyone at first, and the answer depends on understanding what "current directory" actually controls.

**Your current directory does not control where the script lives.** As long as you give Python the full path to the script (or call it by name through other mechanisms covered later), the script can live anywhere on your machine.

**Your current directory *does* control where the script writes its output**, and it controls tab-completion for any file paths you type. Anything the script saves (a plot, a derived data file, a log) usually lands in your current directory unless the script is written to save elsewhere.

So the practical rule for DENNIS Lab helpers is:

**Stand in the directory containing your data. Call the script by its full path.**

## Running a script

```
cd /Volumes/lab_data/swir_run42
python ~/code/DENNIS_helpers/scripts/show_h5_keys.py imaging.h5
```

This command has two parts after `python`. The first, `/path/to/show_h5_keys.py`, is the path to the script you want to run. The second, `mydata.h5`, is an *argument*: a value handed to the script, here the data file you want it to inspect. The script reads that argument and acts on it.

You're in the data directory, so:
- Tab-completion works when you type `imaging.h5`
- Any outputs the script generates land alongside the input data
- The data path you pass is short (just the filename) instead of a long absolute path

The script's path is long, but you only type it once per session — and tools like shell aliases or putting `~/code/DENNIS_helpers/scripts/` on your `PATH` can shorten that too (we'll cover those later).

### A note on writing scripts that don't care about the working directory

Well-written helper scripts take file paths as arguments and open exactly those paths, with no assumptions about where the user is standing. If you find yourself writing a script that only works when run from a specific directory, that's usually a sign to refactor: take the path as an argument instead of hardcoding it or assuming a relative location.

### Why we don't put data inside the repo

You might wonder: couldn't we just keep the data in the repo with the scripts? In some projects, yes (e.g., when we're moving towards publication, have chosen what data we're including in the manuscript, and are building the specific figures for that paper; in that case the data will be included in the repo so that anyone can go from input data --> run scripts --> replicate published output). In this helper script repo, no. Much of our real datasets are imaging files that don't belong in version control. `CLAUDE.md` and our naming guide both prohibit committing data files. Data lives on lab storage; scripts live in the repo; you stand near the data and call the script.

## Conda environment commands

Conda manages the lab's software environment. `docs/04_environments.md` explains what an environment is; these are the commands you will type.

```
conda env list
```

Lists every environment on your machine and marks the active one.

```
conda activate helper
```

Turns on the `helper` environment. Your prompt will then show `(helper)`. Do this before running lab code.

```
conda deactivate
```

Turns the current environment off.

```
conda list
```

Lists the packages installed in the active environment.

```
conda install package_name
```

Installs a package into the active environment from conda's repositories.

```
pip install package_name
```

Installs a package using pip, Python's other installer. Prefer `conda install` first, because conda manages compatibility between packages. Fall back to `pip install` only when a package is not available through conda. Whichever you use, make sure the right environment is active first.

## Troubleshooting

**"command not found"** means the shell does not recognize the command. Usually the environment is not active (run `conda activate helper`) or the command is misspelled.

**"No such file or directory"** means a path you typed does not exist from where you currently are. Check with `pwd` and `ls` that the file is really there, and check the spelling of the path.

**"I installed it, but Python says it is not installed."** This is almost always the wrong environment being active. You installed the package into one environment and are running Python in another. Run `conda activate helper`, confirm with `conda list` that the package is there, and try again. In a notebook, this same problem shows up as a wrong *kernel*; see `docs/04_environments.md`.
