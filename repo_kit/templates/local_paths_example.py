"""Template for machine-specific paths — copy to `local_paths.py` (gitignored).

`local_paths.py` holds paths specific to YOUR machine, so they never get
committed. Copy this file to `local_paths.py` in the repository root, edit the
paths below, and import them from a notebook or script:

    from local_paths import DATA_ROOT

Because notebooks run from the repository root (set in `.vscode/settings.json`),
this import works from any notebook with no path juggling.
"""

# Absolute path to the folder where your data lives on this machine.
DATA_ROOT = "/absolute/path/to/your/data"
