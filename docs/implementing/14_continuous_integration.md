# Continuous integration

You now run tests and ruff on your own machine. **Continuous integration (CI)** runs those same checks automatically, on a fresh machine, every time you push or open a pull request. It is what catches "works on [only] my machine" before the problem reaches `main`: a dependency you installed by hand and forgot to add to the environment file, a file you never committed, a path that only works on your laptop.

## What CI catches, and how it pairs with review

CI runs your checks on a clean virtual machine that has only what your environment file declares. So it catches the gap between "my setup" and "a fresh clone," and, with a matrix (below), bugs that only appear on another operating system. [08_code_review.md](../onboarding/08_code_review.md) is the human half of the same job: CI checks the mechanical things automatically so a reviewer can spend their attention on loftier concerns than "did the tests pass."

## GitHub Actions basics

This guide uses **GitHub Actions**, GitHub's built-in CI. The vocabulary, defined once:

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
          activate-environment: fieldguide     # must match the name in that file

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

Teammates often work on a mix of macOS and Windows, and OS-specific bugs are real: path separators (`/` versus `\`), line endings, and small floating-point differences all cause code that passes on one to fail on the other. A *matrix* runs the same job once per combination you list, so it catches those bugs before a teammate does:

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

### A caveat on the cost of the CI testing

GitHub host servers perform workflow Actions such as the CI testing and generating Sphinx doc sites (covered in 20) for free... to a point. Knowing your own repo/organization limits will help you choose which workflows to run at what frequency (i.e., run the cheap workflows automatically every PR, save the expensive ones for when they matter to you).

GitHub meters runner time against a monthly minutes allotment, and the meter runs at different speeds depending on the operating system: a Linux runner counts each minute as 1 minute, Windows as 2, and macOS as 10. A test job that takes six real minutes costs 6 minutes of the allotment on Linux, 12 on Windows, and 60 on macOS. That allotment is shared organization-wide, not per repository: every private repo draws against the same monthly pool, 2,000 minutes on GitHub's Free plan. Public repositories are exempt from the pool; GitHub-hosted runners are free and unlimited for public repositories, so this only matters for private repos (like internally shared lab notebook repos).

Run the macOS and Windows legs on every push and every commit to an open pull request, across a few private repos in the same organization, and the monthly allotment is gone within days, before anyone even gets to a release.

### Minutes management strategy

To test early and often while stretching those Action minutes, keep `ubuntu-latest` on `push` and `pull_request`: 1x cost, and it catches the large majority of real bugs. Move macOS and Windows to a trigger that fires far less often, for example a weekly `schedule` and/or a `workflow_dispatch` to run the full matrix by hand before tagging a release.

```yaml
on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:
  schedule:
    - cron: "0 6 * * 1"   # every Monday at 06:00 UTC

jobs:
  test:                          # every push and PR: cheap, catches most bugs
    runs-on: ubuntu-latest
    # ...the same steps as the minimal workflow above

  test-multios:                  # weekly, or on demand before a release
    if: github.event_name == 'schedule' || github.event_name == 'workflow_dispatch'
    strategy:
      fail-fast: false
      matrix:
        os: [macos-latest, windows-latest]
    runs-on: ${{ matrix.os }}
    # ...the same steps as the minimal workflow above
```

The `test` job carries no `if`, so it runs on every trigger, including the weekly schedule. That means the same cron entry also catches dependency drift (below) on the cheap runner, at no extra cost.

An organization owner can see which repository and which workflow is actually spending the allotment under the organization's Settings → Billing and plans → Usage. That page is the fastest way to find the real cost center once a monthly allotment runs out early: usage is rarely spread evenly across repos, and is often concentrated in one matrix job whose expensive steps — a full docs build or a slow test suite — run duplicated across every OS leg instead of once.

## Catching drift with a scheduled run

The triggers above, `push` and `pull_request`, catch *your* changes: a broken test the moment you
introduce it. They do not catch the world changing underneath a repo nobody has touched: a new
release of a dependency that silently changes behavior, exactly the ruff-0.16 story in
[11_code_quality_tools.md](11_code_quality_tools.md). The `schedule` trigger added above runs the same
checks on a timer, independent of anyone pushing, so a dependency-caused break surfaces within a week
instead of whenever someone next happens to push.

## Reading a failed run

When CI fails, a red X appears next to the commit or on the PR. To find out why:

1. Click the red X, or open the repo's **Actions** tab and click the failing run.
2. Click the job that failed (for example `test-multios (windows-latest)`).
3. Expand the step with the red X. The log shows exactly what your terminal would have shown, including the pytest or ruff output.

The most common first failure is a real "works on my machine" bug: a package that ran locally because you had it installed, but is missing from the environment file. The fix is to add it to the environment file, as your project's coding-standards file (here, [CLAUDE.md](../../CLAUDE.md)) requires, not to install it on the runner by hand.

## Further reading

This doc covers a conda-based workflow. For the scientific-Python ecosystem's own GitHub Actions guidance, including `uv`-based workflows and packaging-specific CI concerns beyond conda, see the [Scientific Python Development Guide's "GitHub Actions: Introduction" page](https://learn.scientific-python.org/development/guides/gha-basic/).
