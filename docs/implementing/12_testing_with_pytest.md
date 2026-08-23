# Testing with pytest

You cleaned up a function to make it faster, or clearer, or you updated a package. Did the numbers change? An automated *test* answers that in a second, every time, instead of you eyeballing a plot and hoping. This doc takes you from never having written a test to writing and running real ones.

## Why bother

Two reasons, both aimed at how research code actually goes wrong.

- **Silent breakage.** A refactor, a dependency update, or a "harmless" tweak quietly changes a result, and nothing warns you. A test that pins the expected number catches it the moment it happens, not three months later in review.
- **Confidence to change.** With tests in place you can restructure code ([13_software_design.md](13_software_design.md)) and *know* you did not alter its behavior. When you're worrying "did my refactor change the numbers?" a test is the answer.

## The kinds of tests, briefly

- **Unit test:** checks one function in isolation. Most of your tests will be these.
- **Integration test:** checks several pieces working together, such as load then calibrate then compute.
- **Regression test:** pins a specific known-good result so that a bug, once fixed, stays fixed, or a verified approach stays verified.

Most of your tests will be unit and regression tests. Don't overthink the taxonomy.

## Anatomy of a test

A test is a function whose name starts with `test_`. Inside, you run your code and `assert` that something is true. Say you have this function:

```python
# scripts/spectra.py
def normalize(values: list[float]) -> list[float]:
    """Scale values so the largest is 1.0."""
    peak = max(values)
    return [v / peak for v in values]
```

A test for it lives in a separate file:

```python
# tests/test_spectra.py
from scripts.spectra import normalize


def test_normalize_scales_peak_to_one():
    result = normalize([1.0, 2.0, 4.0])
    assert result == [0.25, 0.5, 1.0]
```

`assert` is a plain Python statement: if the expression after it is false, the test fails. The test feeds a known input and states the known correct output. That is the whole idea.

## Running your tests

In VS Code: open the **Testing** panel (the flask icon in the left sidebar). It discovers your `test_` functions and gives you a run button for each one and for the whole suite.

In the terminal:

```
pytest tests/
```

This finds and runs every `test_*` function under `tests/`. You get a `.` for each pass and an `F` for each failure, and for every failure pytest prints the exact line and the values that differed, so you can see what you asserted versus what you actually got.

## Floats: do not use `==`

The example above worked because `1/4`, `2/4`, and `4/4` land on values a computer stores exactly. Most computed floats do not. In floating-point arithmetic `0.1 + 0.2` is not equal to `0.3`, so `assert result == expected` on real computed numbers will fail *even when your code is correct*. Compare with a tolerance instead, using numpy:

```python
import numpy as np


def test_radiance_matches_reference():
    result = compute_radiance(sample_input)
    expected = np.array([0.12, 0.47, 0.91])
    np.testing.assert_allclose(result, expected, rtol=1e-6)
```

`np.testing.assert_allclose` passes when `result` is within a relative tolerance (`rtol`) of `expected`. Use it for any computed float or array. Here `rtol=1e-6` means "agree to about six significant figures"; loosen or tighten it to match what the science actually requires.

## One test, many inputs: parametrize

When you want the same check over several inputs, do not copy-paste the test. Mark it with the inputs instead:

```python
import pytest


@pytest.mark.parametrize(
    "values, expected",
    [
        ([1.0, 2.0, 4.0], [0.25, 0.5, 1.0]),
        ([5.0, 5.0], [1.0, 1.0]),
        ([3.0], [1.0]),
    ],
)
def test_normalize_cases(values, expected):
    assert normalize(values) == expected
```

pytest runs the test once per row and reports each separately, so a failure tells you exactly which case broke.

## Shared setup: fixtures and `conftest.py`

When several tests need the same starting material (a sample dataset, a loaded config), write a *fixture*: a function decorated with `@pytest.fixture` that returns the thing. A test receives it just by naming it as an argument.

```python
import pytest


@pytest.fixture
def sample_spectrum():
    return [1.0, 2.0, 4.0]


def test_peak_is_one(sample_spectrum):
    assert max(normalize(sample_spectrum)) == 1.0
```

Fixtures needed across more than one test file go in a file named `conftest.py` inside `tests/`. pytest finds it automatically; you do not import it.

## Code coverage: a signal, not a target

`pytest-cov` (`pytest --cov=scripts tests/`) reports **coverage**: the percentage of lines your test
suite actually executes. It is a real signal — a module at 0% coverage definitely has no tests
protecting it — and an easy number to compute and report. But it is not the same thing as *good*
tests: a test can execute every line of a function and still assert nothing meaningful about the
result, so 100% coverage is compatible with a suite that would not catch a real bug. Use coverage to
find code nobody has tested yet, not as a target to maximize for its own sake; the
`np.testing.assert_allclose` habit above is what actually catches a wrong answer.

## Where tests live, and two habits

- Tests live in a `tests/` directory at the repo root. Test files are named `test_*.py` and test functions `test_*`; pytest discovers them by those names.
- **When you fix a bug, add a test that would have caught it.** That regression test keeps the bug from creeping back.
- **When an experiment establishes that an approach is correct, turn it into a test.** "This input should produce this result" becomes a `test_` function guarding the shipped code forever. This is how a validation experiment graduates into a permanent safeguard, and it depends on the experiment being reproducible in the first place — the seeding ([16_running_a_dry_lab_experiment.md](16_running_a_dry_lab_experiment.md)) and pinning ([15_experiments_and_shipping.md](15_experiments_and_shipping.md)) that make a run repeatable.

## What to expect if an AI assistant writes the code

This repo's [CLAUDE.md](../../CLAUDE.md) is what tells an assistant to follow these conventions — but
only for what it actually says. Its **Testing requirements** section states this concretely: a new
function that does real computation gets a test in `tests/` following the patterns in this doc
(`assert_allclose` for floats, `parametrize` for multiple cases), and a bug fix gets a regression test
that would have caught it. That's why asking for a function here should also produce a test, unprompted.

Your own project's `CLAUDE.md` only does the same if it says so.
[repo_kit/CLAUDE.template.md](../../repo_kit/CLAUDE.template.md) carries the identical rule, ready to
copy in; without it, an assistant may hand back a clean, documented, type-hinted function with nothing
testing it. Until your standards file has this section, ask for the test directly: "add a test for
this, following this repo's conventions."

Either way, read what comes back the way you'd read the function it covers: does it assert something
meaningful, on the case that actually matters to your science, not just the easy one.
[18_ai_assisted_development.md](18_ai_assisted_development.md) covers this verification habit in full.
