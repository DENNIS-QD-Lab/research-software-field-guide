# Code review

Shared code can be set up to have a review before it is merged. Review is not a gate to pass or a judgment of you. It is a second set of eyes that catches small problems early and spreads knowledge of the codebase. This doc covers what to look for, how to say it, and how to merge.

## What to look for

You do not need to audit a change line by line. Check four things:

- **Does it run?** Pull the branch, activate the appropriate environment, and run the script or notebook on a real file. Confirm it does what the description says.
- **Does it have a docstring?** Every script needs purpose, inputs, and an example call at the top. See [06_adding_a_script.md](06_adding_a_script.md).
- **Does the name make sense?** A helper should be named `verb_noun.py` and read clearly. If you cannot tell what it does from the name, say so.
- **Is it duplicating existing code?** If a script already does this, the change should extend it rather than add a near-copy.

## Tone

How you say something matters as much as what you say. Three norms:

Ask questions rather than issue commands. "What happens if the file path does not exist?" lands better than "Handle the missing-file case," and often the author already has an answer.

Suggest, do not demand. Offer a change as a recommendation the author can weigh, not an order. Mark genuinely optional thoughts as optional.

Assume good intent. The author did their best with what they knew. Review is collaborative problem-solving, not gatekeeping. Praise what is good, not only what needs fixing.

## How to approve and merge

When the change looks good, approve it in the GitHub interface: open the pull request, go to the Files changed tab, click "Review changes," select "Approve," and submit.

To merge, return to the Conversation tab and click "Merge pull request," then "Confirm merge." Delete the branch when GitHub offers, since its work now lives in `main`. The author then pulls `main` to bring the merged change back to their machine, and the loop in [05_daily_workflow.md](05_daily_workflow.md) starts again.
