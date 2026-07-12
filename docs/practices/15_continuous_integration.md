# Continuous integration

You now run tests and ruff on your own machine. **Continuous integration (CI)** runs those same checks automatically, on a fresh machine, every time you push or open a pull request. It is what catches "works on my machine" before the problem reaches `main`: a dependency you installed by hand and forgot to add to the environment file, a file you never committed, a path that only works on your laptop.

## What CI catches, and how it pairs with review

CI runs your checks on a clean virtual machine that has only what your environment file declares. So it catches the gap between "my setup" and "a fresh clone," and, with a matrix (below), bugs that only appear on another operating system. `../onboarding/08_code_review.md` is the human half of the same job: CI checks the mechanical things automatically so a reviewer can spend their attention on judgment, not on "did the tests pass."

## GitHub Actions basics

The lab uses **GitHub Actions**, GitHub's built-in CI. The vocabulary, defined once:

- A **workflow** is a YAML file in `.github/workflows/`. A repo can have several.
- A workflow has **triggers** (when it runs) and **jobs** (what it does).
- A **job** runs on a fresh **runner** (a clean VM GitHub provisions) and is a list of **steps**.

## A minimal workflow

Here is a complete `.github/workflows/ci.yml`, annotated. It recreates the conda environment, installs the package, and runs ruff and the tests.

```yaml
name: CI

on:                        # triggers: run on pushes to main and on every PR
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    defaults:
      run:
        shell: bash -l {0}   # a login shell, so `conda activate` works
    steps:
      - uses: actions/checkout@v4        # check out the repo onto the runner

      - uses: conda-incubator/setup-miniconda@v3
        with:
          environment-file: environment.yml   # build the env from the file
          activate-environment: helper         # must match the name in that file

      - name: Install the package
        run: pip install -e . --no-deps        # only if the project is a package

      - name: Lint and format check
        run: |
          ruff check .
          ruff format --check .                # --check fails if formatting is off

      - name: Run tests
        run: pytest
```

Each step must succeed for the job to pass. `ruff format --check` reports formatting problems without changing files, which is what you want on a runner. If your project is not an installable package, drop the install step.

## Test on more than one operating system

Lab members work on both macOS and Windows, and OS-specific bugs are real: path separators (`/` versus `\`), line endings, and small floating-point differences all cause code that passes on one to fail on the other. So a matrix over operating systems is **recommended here, not optional.** A *matrix* runs the same job once per combination you list:

```yaml
jobs:
  test:
    strategy:
      fail-fast: false            # let every OS finish, don't stop at the first failure
      matrix:
        os: [macos-latest, windows-latest]
    runs-on: ${{ matrix.os }}
    # ...the same steps as above
```

This runs the whole job twice, once on each OS, and reports each separately. You can also matrix over Python versions (`python-version: ["3.11", "3.12"]`), which matters most for pure-Python projects; when your environment file pins a specific Python, the OS matrix is the one that earns its keep.

## Reading a failed run

When CI fails, a red X appears next to the commit or on the PR. To find out why:

1. Click the red X, or open the repo's **Actions** tab and click the failing run.
2. Click the job that failed (for example `test (windows-latest)`).
3. Expand the step with the red X. The log shows exactly what your terminal would have shown, including the pytest or ruff output.

The most common first failure is a real "works on my machine" bug: a package that ran locally because you had it installed, but is missing from the environment file. The fix is to add it to the environment file (`../../CLAUDE.md`), not to install it on the runner by hand.
