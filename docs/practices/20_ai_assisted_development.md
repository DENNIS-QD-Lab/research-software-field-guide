# AI-assisted development

The lab uses AI coding assistants (Claude Code, in this repo). This doc is about using them *responsibly* for research software: where they help, where they do not, and the norms that keep AI-assisted research honest and reproducible. The tool will change; the principles here are vendor-neutral, but the examples are the lab's actual setup.

## The standards file does the heavy lifting

`../../CLAUDE.md` is the project's coding standards, and the assistant reads it automatically at the start of every session. That is why generated code already follows PEP 8, uses NumPy-style docstrings and type hints, and respects the data-handling rules, without anyone re-explaining them. Keeping standards in a file the assistant reads means the whole team gets consistent output and you are not re-typing the rules each time. Most assistants support a project-instructions file of some kind; the principle carries over even if the tool does not.

## Review every generated change

The non-negotiable rule: **AI-generated code is a draft, not a commit.** Read every change before it lands, exactly as you would a colleague's pull request (`../onboarding/08_code_review.md`). Assistants are fast and *confident*, and confident-but-wrong is precisely the failure mode review exists to catch. If you would not merge it from a labmate without reading it, do not merge it from an assistant.

## Never trust numbers without a test

The rule that matters most for *research* code: if generated or edited code produces numbers, a test guards them (`12_testing_with_pytest.md`). "Did this change the result?" is answered by a test, not by the assistant's reassurance. An assistant can produce code that runs cleanly and returns a plausible, wrong answer; a test on a known-good case is what catches it. This is the single most important norm on this page.

## What to delegate, and what to keep

Good to delegate:

- Boilerplate and mechanical refactors.
- Writing tests for behavior you already understand.
- Docstrings, configuration, converting a notebook cell into a tested function.
- "Explain what this code does" and "where would this break."

Keep with a human:

- The scientific judgment: which approach is correct, whether a number is physically plausible.
- Novel algorithm design, and deciding what is worth doing at all.
- Anything where being wrong is costly and hard to detect.

The assistant accelerates the typing, not the thinking. It is a very fast pair of hands supervised by your judgment.

## Reproducibility and honesty

- **Seed and record.** AI-generated code is no exception to the seeding and provenance rules (`10_from_scripts_to_pipelines.md`, `14_experiments_and_shipping.md`). Determinism does not care who wrote the code.
- **The standards apply to AI output too.** Generated code does not get to commit data, add a silent dependency, or skip a docstring (`../../CLAUDE.md`). Review holds it to the same bar as yours.
- **Verify, do not trust.** An assistant can invent an API that does not exist, a citation that was never written, or a number that looks right. Check against reality: run it, test it, read the docs it claims to use.
- **Be honest about its role.** Disclose AI assistance where the norms of your field or venue ask for it, the same as any other methods detail.

## The bottom line

AI assistants are powerful accelerators for the mechanical parts of research software, *under* human judgment and *behind* a test suite. The standards file, human review, and tests are exactly what make leaning on them safe.
