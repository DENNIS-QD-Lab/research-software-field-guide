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

This trips up everyone at first. When you run a script, your current directory matters because the script may look for input files using relative paths. Rule of thumb: be in the directory the script expects, which for our helpers is usually the directory containing the data file you want to inspect. The script itself can live anywhere as long as Python can find it.

## Running a script

```
python /path/to/show_h5_keys.py mydata.h5
```

This command has two parts after `python`. The first, `/path/to/show_h5_keys.py`, is the path to the script you want to run. The second, `mydata.h5`, is an *argument*: a value handed to the script, here the data file you want it to inspect. The script reads that argument and acts on it.

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
