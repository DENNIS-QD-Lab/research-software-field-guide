# AI-assisted development

Many research teams use AI coding assistants (Claude Code, in this repo). This doc is about using them *responsibly* for research software: where they help, where they do not, and the norms that keep AI-assisted research honest and reproducible. The tool will change; the principles here are vendor-neutral, but the examples reflect this repo's actual setup.

It sits here, in the experimentation part of the track, on purpose. The single principle under everything below is the division of labor: **the assistant writes code; you do the science.** Designing the experiment, judging whether a result is real, and drawing the conclusion stay with you. That split is not a nicety — it is what keeps the work trustworthy, and it matters *more*, not less, the more of the implementation you hand over.

## The standards file does the heavy lifting

Your project's coding-standards file (here, `../../CLAUDE.md`) states the standards, and the assistant reads it automatically at the start of every session. That is why generated code already follows PEP 8, uses NumPy-style docstrings and type hints, and respects the data-handling rules, without anyone re-explaining them. Keeping standards in a file the assistant reads means the whole team gets consistent output and you are not re-typing the rules each time. Most assistants support a project-instructions file of some kind; the principle carries over even if the tool does not.

## Three homes for instructions: state, procedure, standards

A standards file is one of *three* kinds of instruction a research repo keeps, and it helps to keep them separate. Two are written mainly for the assistant and the team, one is written mainly for humans:

- **State — for humans.** The research log (`16_running_a_dry_lab_experiment.md`): the goal, what has been found, what is next. The assistant reads it for context, but people own it and it changes every session.
- **Durable procedure — for the assistant.** How *this* repo runs and records experiments (the run-provenance and folder conventions of `16_running_a_dry_lab_experiment.md`), written down so the assistant follows the same discipline every session instead of improvising. In the exemplar this is a short `experiments_playbook.md` that the assistant reads alongside the standards file.
- **Standards — for both.** `../../CLAUDE.md`: the coding conventions, applied equally to human- and AI-written code.

Keeping these apart is what stops any one file from sprawling into an unreadable mix of findings, procedure, and rules — and it means the assistant is told *how we work here* without burying the researcher-facing record of *what we found*.

## Review every generated change

The non-negotiable rule: **AI-generated code is a draft, not a commit.** Read every change before it lands, exactly as you would a colleague's pull request (`../onboarding/08_code_review.md`). Assistants are fast and *confident*, and confident-but-wrong is precisely the failure mode review exists to catch. If you would not merge it from a labmate without reading it, do not merge it from an assistant.

## Never trust numbers without a test

The rule that matters most for *research* code: if generated or edited code produces numbers, a test guards them (`12_testing_with_pytest.md`). "Did this change the result?" is answered by a test, not by the assistant's reassurance. An assistant can produce code that runs cleanly and returns a plausible, wrong answer; a test on a known-good case is what catches it. This is the single most important norm on this page.

## A clean run is not a correct analysis

A passing test tells you the code *ran* and matched an expected value. It does not tell you the code ran the *right analysis*. Those are two different questions, and research code has to clear both:

- **Verification — does it run?** No error, output produced. Necessary, and the easy part.
- **Validation — does it run the analysis you actually meant?** The right method, the right units, on the right data, answering the question you asked.

An assistant clears the first bar effortlessly and can miss the second entirely — a plausible number from the wrong formula looks exactly like a correct one. So validate beyond the unit test:

- **Check a known-good case** whose answer you can get independently.
- **Check physical plausibility** — are the magnitudes, signs, and units what the science requires?
- **Cross-check against an independent method** — a second route to the same number is strong evidence; a rough hand calculation often suffices.
- **Inspect the intermediate outputs**, not only the final figure. Errors hide in the middle.

Scale your scrutiny to how much you delegated: the more of the implementation an assistant wrote, the *more* of this the result is owed, precisely because you were not watching each line as it went in. Examining results critically is ordinary research hygiene; it becomes non-negotiable when a machine wrote the code that produced them.

## What to delegate, and what to keep

Good to delegate:

- Boilerplate and mechanical refactors.
- Writing tests for behavior you already understand.
- Docstrings, configuration, converting a notebook cell into a tested function.
- "Explain what this code does" and "where would this break."

Keep with a human:

- Designing the experiment, choosing which comparisons matter, and interpreting what the results mean.
- The scientific judgment: which approach is correct, whether a number is physically plausible.
- Novel algorithm design, and deciding what is worth doing at all.
- Anything where being wrong is costly and hard to detect.

The assistant accelerates the typing, not the thinking. It is a very fast pair of hands supervised by your judgment.

## Reproducibility and honesty

- **Seed and record.** AI-generated code is no exception to the seeding and provenance rules (`10_from_scripts_to_pipelines.md`, `15_experiments_and_shipping.md`). Determinism does not care who wrote the code.
- **The standards apply to AI output too.** Generated code does not get to commit data, add a silent dependency, or skip a docstring (`../../CLAUDE.md`). Review holds it to the same bar as yours.
- **Verify, do not trust.** An assistant can invent an API that does not exist, a citation that was never written, or a number that looks right. Check against reality: run it, test it, read the docs it claims to use.
- **Be honest about its role.** Disclose AI assistance where the norms of your field or venue ask for it, the same as any other methods detail.

## The bottom line

AI assistants are powerful accelerators for the mechanical parts of research software, *under* human judgment and *behind* a test suite. The standards file, human review, and tests are exactly what make leaning on them safe.
