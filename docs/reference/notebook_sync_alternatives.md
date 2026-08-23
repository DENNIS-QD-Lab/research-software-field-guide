# Notebook version control: approaches we considered

This is a reference doc, not onboarding. It records the three approaches the team weighed for keeping notebooks in version control, and why we chose the one we use, so a returning team member wondering "could we be doing this better?" can see the tradeoffs without rediscovering them. For the setup you actually run, see [07_notebooks.md](../onboarding/07_notebooks.md).

## Why notebooks fight with version control

A `.ipynb` file is JSON that stores not just code but also every cell's outputs and a pile of metadata. Outputs include printed text, tables, and plot images encoded as base64 text inside the file. Because outputs change every time a notebook runs, diffs are unreadable, merge conflicts are common and painful, and the repository bloats with binary image data. Three approaches address this, and they differ in what they commit.

## Option 1: Strip outputs and metadata with nbstripout (what we use)

The committed `.ipynb` has no outputs and minimal metadata. Your local working copy keeps everything, so your screen does not change. Setup is a pre-commit hook, covered in [07_notebooks.md](../onboarding/07_notebooks.md).

- Pros: simple, one tool, and students keep working in notebooks exactly as they already do.
- Cons: the committed format is still `.ipynb`, so diffs are JSON, better than before but still not pleasant to read. There is no way to import a notebook's functions into another script without converting it first.

## Option 2: Strip only metadata, keep outputs

A configuration of nbstripout that removes metadata but leaves cell outputs in the committed file.

- Pros: reviewers see the actual plots and outputs directly in the pull request.
- Cons: the repository grows with every committed plot, diffs still include base64-encoded images, and keeping outputs defeats most of the point of stripping in the first place.

## Option 3: Pair `.py` and `.ipynb` automatically with jupytext

Each notebook has a script twin. You edit either one and jupytext regenerates the other on save. Only the `.py` is committed; the `.ipynb` is generated locally on demand.

- Pros: clean text diffs, importable scripts, no output bloat, and a single source of truth.
- Cons: the user needs to understand the pairing relationship, it adds one more tool to the stack, and some pure-exploration notebooks gain nothing from being paired.

## Current decision

We use Option 1, nbstripout. It is the lowest-friction choice for a team of scientists who are not primarily software developers, and it does not change how anyone works day to day. Revisit this if the team finds itself frequently wanting to import notebook code into scripts, or if notebook merge conflicts become common. Either of those would tip the balance toward Option 3.
