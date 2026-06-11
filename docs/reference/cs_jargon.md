# Programming Jargon

Terms of art from software development that aren't obvious until someone defines them. Not exhaustive. Add to this list when you encounter a term that confuses you and learn what it means.

## Case styles (how identifiers are formatted)

The name "case" comes from typography (uppercase vs lowercase letters). Each case style is a convention for combining multiple words into one identifier without spaces.

**snake_case**
Lowercase letters with underscores between words. `show_keys`, `ratio_analysis`. Python's standard for variables, functions, and filenames.

**PascalCase**
Each word capitalized, no separators. `MyClass`, `HDFInspector`. Python's standard for class names.

**camelCase**
First word lowercase, subsequent words capitalized. `showKeys`, `ratioAnalysis`. Common in JavaScript and Java. Python doesn't use this; if you see it in Python code, it's usually a sign the code was translated from another language.

**kebab-case**
Lowercase with hyphens. `add-show-keys`, `fix-pathing-bug`. Common for branch names, URLs, and file names in some contexts. Python identifiers cannot contain hyphens (the hyphen is the subtraction operator), so kebab-case is never used for Python variables or function names.

**SCREAMING_SNAKE_CASE**
All uppercase with underscores. `MAX_ITERATIONS`, `DEFAULT_TIMEOUT`. Python's standard for constants.

## Code structure

**Identifier**
Any name you assign to something in code: a variable, a function, a class, a file. "What's a valid identifier in Python?" means "what names are you allowed to use?"

**Argument vs. parameter**
A *parameter* is the name in a function's definition (`def show_keys(path):` — `path` is a parameter). An *argument* is the actual value passed in when you call the function (`show_keys("data.h5")` — `"data.h5"` is an argument). People use the terms interchangeably in casual conversation, but the formal distinction is parameter = the slot, argument = the value put into the slot.

**Positional vs. keyword arguments**
Positional: identified by their order. `range(0, 10)` — 0 is the start, 10 is the stop, because of where they sit. Keyword: identified by name. `range(start=0, stop=10)` — explicit, position doesn't matter.

**Return value**
What a function gives back when it's done. `def square(x): return x * x` — `square(3)` returns `9`. A function that doesn't have a `return` statement implicitly returns `None`.

**Side effect**
Anything a function does besides return a value: printing to the screen, writing a file, modifying a global variable, changing one of its arguments in place. Functions that have only return values and no side effects are easier to reason about; functions full of side effects are harder.

**Pure function**
A function that returns the same output for the same input every time and has no side effects. `def square(x): return x * x` is pure. `def print_and_square(x): print(x); return x * x` is not (the print is a side effect).

**Mutable vs. immutable**
Mutable: can be changed after creation. Lists, dicts, sets in Python. Immutable: cannot be changed after creation. Strings, tuples, integers in Python. "Immutable" doesn't mean "constant" — you can reassign a variable to a new immutable value; you just can't modify the value in place.

## Programming concepts

**Iterate / iteration**
To repeat an operation over a sequence. A `for` loop iterates over a list. "The script iterates over the keys in the HDF5 file" means "the script processes each key, one at a time."

**Recursion / recursive**
A function that calls itself. The HDF5 inspector walks groups recursively because groups can contain groups can contain groups. Each recursive call handles one level.

**Parse / parser / parsing**
Taking raw text and turning it into structured data your program can work with. argparse parses command-line arguments. JSON parsers parse JSON text into dicts and lists.

**Serialize / deserialize**
Convert in-memory data into a format that can be saved or transmitted (serialize), then convert it back (deserialize). Saving a Python dict as JSON is serialization; loading the JSON back into a dict is deserialization.

**Refactor**
Rewriting code to be cleaner, faster, or better organized without changing what it does. "I refactored the analysis script" means the inputs and outputs are the same, but the internals are different.

**Boilerplate**
Repetitive code that has to be written to set things up, even though it doesn't carry the interesting logic. `if __name__ == "__main__":` blocks are boilerplate; the argparse setup is mostly boilerplate. Frameworks reduce boilerplate by providing the setup for you.

**Idiom / idiomatic**
A common pattern that's the "standard" way to do something in a given language. `for item in things:` is idiomatic Python; `for i in range(len(things)): item = things[i]` works but is not idiomatic. "Pythonic" means "idiomatic in Python."

## Tools and environments

**Module**
A single Python file that can be imported. `show_h5_keys.py` is a module; you can `from scripts.show_h5_keys import show_keys`.

**Package**
A directory of related modules with an `__init__.py` file, importable as a unit. NumPy is a package; matplotlib is a package.

**Library / framework**
Library: code you call from your code. NumPy is a library — your code uses it. Framework: code that calls your code. Flask and Django are frameworks — you fill in pieces and the framework runs them. The distinction is sometimes called "inversion of control."

**Dependency**
A library or package your code needs in order to run. `environment.yml` lists this repo's dependencies.

**Virtual environment**
An isolated Python installation with its own packages, separate from other projects on your machine. Lets project A use NumPy 1.x while project B uses NumPy 2.x without conflict.

**REPL**
Read-Eval-Print Loop. The interactive Python prompt where you type one line and Python runs it immediately. Jupyter notebooks are a REPL with a fancier interface.

**Standard library (stdlib)**
The modules that come with Python itself — no installation needed. `os`, `sys`, `argparse`, `pathlib`, `json` are all in the standard library.

**Third-party**
Anything not in the standard library. NumPy, matplotlib, h5py are third-party packages. Installed via conda or pip.

## Files and data

**Path**
The location of a file. Absolute paths start from the root of the filesystem (`/Users/allison/data/run42.h5`). Relative paths start from the current directory (`./data/run42.h5` or just `data/run42.h5`).

**Extension**
The part of a filename after the last dot. `show_h5_keys.py` has extension `.py`. Conventions tie extensions to file types but Python doesn't actually require them.

**Encoding**
How text characters are represented as bytes on disk. UTF-8 is the modern default. If you see weird symbols where letters should be, an encoding mismatch is often the cause.

**Binary vs. text file**
Text files are human-readable when opened in a text editor (`.py`, `.md`, `.csv`). Binary files are not (`.h5`, `.png`, `.pkl`). Git diffs binary files poorly, which is why we don't commit them.

