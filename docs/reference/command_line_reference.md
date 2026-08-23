# Command Line Reference

More terminal commands than [01_command_line_basics.md](../onboarding/01_command_line_basics.md) covers, organized by what they do. No reading order; skim and come back as needed.

## Files and folders

| Command | What it does |
|---|---|
| `mkdir foldername` | Creates a new folder. |
| `touch filename` | Creates an empty file, or updates an existing file's timestamp. |
| `cp source destination` | Copies a file. `cp -r source destination` copies a whole folder. |
| `mv source destination` | Moves or renames a file or folder — the same command does both. |
| `rm filename` | Deletes a file. **No undo, no trash can** — deleted means gone. `rm -r foldername` deletes a whole folder; use it carefully. |

## Looking at files

| Command | What it does |
|---|---|
| `cat filename` | Prints a file's entire contents to the terminal. Good for short files. |
| `head filename` | Prints the first 10 lines. `head -n 20 filename` prints the first 20. |
| `tail filename` | Prints the last 10 lines. Useful for checking the end of a long log file. |
| `grep "text" filename` | Searches a file for lines containing `"text"`. `grep -r "text" foldername` searches every file in a folder, recursively; `grep -n` also prints line numbers. |

## Efficiency

- **Tab-completion.** Type the first few letters of a file or folder name and press Tab; the shell completes it, or shows the options if there's more than one match. Saves typing and catches a typo before it causes a "no such file" error.
- **Up-arrow.** Brings back your previous command; press it again to go further back. Faster than retyping a long command you just ran.
- **`clear`** clears the terminal window. Purely cosmetic — it doesn't affect anything running.

## Wildcards and combining commands

| Syntax | What it does |
|---|---|
| `*` | Matches any characters. `rm *.png` deletes every file ending in `.png` in the current folder. |
| `\|` (pipe) | Sends one command's output into the next as input. `grep "TODO" notes.txt \| head -5` finds matching lines, then shows only the first 5. |
| `>` | Redirects output into a file, overwriting it. `python script.py > output.txt` saves the script's printed output to a file instead of showing it on screen. |
| `>>` | Same as `>`, but appends instead of overwriting. |
| `&&` | Runs the next command only if the first one succeeded. `cd data && ls` moves into `data`, then lists it — but only lists if the `cd` actually worked. |
| `;` | Runs the next command regardless of whether the first succeeded. Use `&&` unless you specifically want this. |

## Finding your way

| Command | What it does |
|---|---|
| `man commandname` | Opens the manual page for a command (press `q` to exit). Not every command has one. |
| `commandname --help` | Prints a shorter, built-in usage summary. Works for most modern tools, including this repo's own scripts ([06_adding_a_script.md](../onboarding/06_adding_a_script.md)). |
| `which commandname` | Prints the full path to the program a command name actually runs — useful for checking whether the right environment's version is being used. |

## Reading a command an AI assistant wants to run

If you're using an AI coding assistant ([ai_coding_assistants.md](ai_coding_assistants.md)), it will
frequently ask permission to run a command before doing so. **Bash** (also called "the shell") is the
language these commands are written in — the same language and the same commands taught on this page,
so a permission prompt is asking you to approve a piece of *this* vocabulary, not something new.

The habit worth building: read the whole command, not just its first word. A prompt starting with
`echo` looks harmless — `echo` only prints text — but `echo "done" >> log.txt` still appends a line to
a file, and a compound command can chain several actions together:

```
cd experiments/theme-a && grep -rn "TODO" . | head -20
```

Read it left to right using the vocabulary above: move into `experiments/theme-a` (only if that
succeeds, because of `&&`), search recursively for lines containing "TODO", then show the first 20
matches. Nothing here writes or deletes anything — being able to tell a read-only command like this one
apart from one containing `rm`, `>`, or `mv` (which changes something) is exactly the judgment a
permission prompt is asking you to make.
