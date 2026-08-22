# Concluding and disseminating a project

Every earlier doc in the experimentation part assumed the work was
still moving. This one is about the other end of the arc: a line of inquiry has concluded — a paper
is going out, or the software is becoming something others depend on — and the job now is to **freeze
the result, archive it, and make it citable**, so it stays findable and reproducible after you move
on.

## Concluding: freeze, archive, cite

The end-to-end pattern:

1. **Freeze** the exact state behind the result. Tag it (`paper-v1`;
   [22_versioning_and_releases.md](22_versioning_and_releases.md)) so that commit is pinned no matter how the code moves afterward.
2. **Archive** that tag for a permanent identifier. Connect the repo to **Zenodo** once, and each
   tagged release is archived and assigned its own **DOI**.
3. **Cite** the DOI in the manuscript.

This tagged, DOI'ed version of the repo ensures that a publication stays reproducible against a specific, frozen version of the code that produced its results, even if/when the library keeps
moving forward on `main` ([15_experiments_and_shipping.md](../implementing/15_experiments_and_shipping.md)). Reproducibility comes from the archived
snapshot, not from freezing the live code. Everything below supports these three steps.

## One repo holds every version — no copies needed

This is easy to miss coming from tools like Microsoft Office, where "keeping a version" means saving a
new file — `manuscript_v2.docx`, `manuscript_v2_final.docx`, `manuscript_v2_final_ACTUALLY.docx` — each
one a full, independent copy that starts drifting from the others immediately. Git does not work that
way, and the difference is what makes the freeze/archive/cite pattern above painless rather than a
chore you put off.

A **branch** and a **tag** are both just named pointers into the same history, not copies of the
repository. Creating one costs nothing — no duplicated files, nothing to keep in sync by hand. That
means one repo can hold, at the same time: `main`, the lab notebook that keeps growing for as long as
the project continues; a tagged snapshot (`paper-v1`) that reproduces one specific paper's figures,
frozen forever at the state it was in when you cut it; and, separately, another tagged snapshot
(`v2.1.0`) of just the shipped library, trimmed to the one approach you settled on
([15_experiments_and_shipping.md](../implementing/15_experiments_and_shipping.md)). None of these
compete for space or attention. You check one out when you need it, by name, and go back to `main` when
you don't.

The practical sequence, once a submission is close: keep working in `main` as usual, then decide what
this *particular* paper actually needs — which experiment themes, which figures, which data references
— and prune the rest, either directly on `main` or on a short-lived branch if you would rather decide
with a safety net. Tag that state. Archive it to Zenodo. Then go back to `main`, untouched, and keep
going: the next experiment, the next figure, the next paper. None of this endangers the fuller history
sitting in every earlier commit — a pruned tag is an additional, permanent view onto one moment of it,
not a replacement for it.

## Keeping the lab notebook private: a clean public copy

Everything above assumes the tag you freeze and archive is the same repo you have been working in
— the lab notebook itself. Sometimes it should not be: a research log can hold false starts,
unfiltered commentary, or context you never meant for a public audience, and archiving that tag
publishes it right along with the code.

Decide this **before the repo ever goes public**, not after. Once history reaches a public remote,
treat it as permanent — copies, forks, and caches outlive any attempt to scrub it later. The two-repo
pattern below is the only way to achieve this: GitHub visibility applies to a whole repository, not to
one tag or branch inside it, so there is no setting that publishes a snapshot while keeping the rest
private. [repo_ownership_and_visibility.md](../reference/repo_ownership_and_visibility.md) covers that
constraint in more depth, along with owning the repo through a lab organization rather than a personal
account.

**The safe pattern is two repos, not one rewritten one.** Keep the working repo — full history,
every experiment, the real notebook — private. When it is time to disseminate, create a **new,
empty repository** and copy in only what should be public: the library code, the `experiments/`
folders you want to show, docs, README, LICENSE. This is a plain file copy, not a git operation —
the new repo starts its own fresh history at that first commit. Tag and archive *that* repo exactly
as described above; the private repo keeps going as your actual notebook.

The cost is a second repo to maintain, and the public copy carries no commit-by-commit history —
the trade for keeping the messy parts genuinely private rather than merely out of the diff. If some
history *is* worth bringing along (a clean sequence of commits you are proud to show), `git
filter-repo` can extract specific paths with their history intact; it is a separate install and a
sharper tool than this guide covers in depth — treat it as advanced, and double-check its output
before pushing anywhere public.

Note that the alternative `.gitattributes` `export-ignore` entry only filters
archives you build yourself with `git archive` — it does not affect GitHub's auto-generated release
ZIP, and it does nothing to hide content from anyone browsing the repo's commit history. It trims
what goes into an archive of an otherwise-public repo; it does not make something genuinely private.

## Why software citation matters

Software is a research output, like a dataset or a figure. Citing it does two things: it gives
**credit** to the people who built the tool, and it supports **reproducibility**, because a reader
can find the exact software, at the exact version, behind a result. "We used custom code" is not
reproducible; "we used `your_package` v2.1 (DOI ...)" is.

## LICENSE: what "reusable" actually requires

A **LICENSE** file states the terms under which others may use your code. Here is the fact scientists
most often miss: **"no license" does not mean "free for anyone to use" — it means "not reusable."**
With no license, default copyright applies, and others technically may not reuse the work. Choosing a
license is choosing how open you want to be. Do not guess at the wording: **choosealicense.com**
walks through the common options (MIT and BSD are permissive; the GPL family is copyleft). Any new
project needs one before it is meaningfully public.

## CITATION.cff

A **`CITATION.cff`** file at the repo root tells GitHub, and citation tools, how to cite the
software. It is a small YAML file with a few fields: title, authors, version, and ideally a DOI.
GitHub renders a "Cite this repository" button from it, so adding one is the lowest-effort step
toward being citable.

## Zenodo and JOSS

- **Zenodo** mints a **DOI** (a permanent identifier) for a snapshot of your repository. Connect the
  repo once, and each tagged release, such as the `paper-v1` tag from
  [22_versioning_and_releases.md](22_versioning_and_releases.md), is archived and assigned its own DOI. The paper cites the DOI of
  that exact tagged state.
- **JOSS**, the Journal of Open Source Software, is a route to a short, peer-reviewed **software
  paper**: a citable publication about the software itself. It is more work than a Zenodo DOI, and
  worth it when the software is a contribution in its own right.

## A `figures/` folder: the manuscript's own `experiments/`

Once a project is far enough along that you are drafting a specific submission, a `figures/` folder
naturally joins `src/` and `experiments/` — the same theme-and-dated-runs discipline from
[16_running_a_dry_lab_experiment.md](../implementing/16_running_a_dry_lab_experiment.md), applied to
paper figures instead of research questions. One folder per figure (or figure group), permanent while
you're iterating on it; the code that generates it lives right there and imports from `src/` the same
way an experiment driver does; earlier attempts accumulate in `details/` rather than being overwritten,
so a figure that stopped earning its place is still on disk if you want to revisit it, not lost. The
folder's `README.md` — rendered to the doc site the same way a theme's is
([documentation_promotion.md](../reference/documentation_promotion.md)) — becomes the paper's actual
figure outline: each figure, its current draft, and a caption, readable and shareable (as a rendered
page, or exported to PDF) with a co-author or a PI who has no interest in opening the repository itself.

This is also, almost for free, the shape Zenodo wants. Archiving to Zenodo *before* you submit, not
after, has a concrete benefit beyond the DOI itself: it is your own deposited record, under your own
account, ahead of any copyright agreement a journal attaches to the accepted manuscript. A common shape
for the archived snapshot is three folders — `data/`, `plotting_scripts/`, and `figures/` — covering
everything that produces a manuscript's figures except the manuscript text itself. If you have been
keeping a `figures/` folder all along, it *is* that folder; your figure-generating scripts are the
`plotting_scripts`; and `data/` is whatever your data references already point at
([17_working_with_large_data.md](../implementing/17_working_with_large_data.md)). Tagging for Zenodo at
that point is mostly a decision about what to leave out of this particular submission, not a packaging
effort built from scratch. The paper then cites the reproducibility package's DOI, and the figures in
it stay yours, deposited before the journal's terms could apply to them.

## The experimental record and the shipped library, going forward

Concluding a project is also where the two jobs of the repo ([15_experiments_and_shipping.md](../implementing/15_experiments_and_shipping.md)) part
ways cleanly. The **experimental record** — the research log, the `experiments/` folders, and
the paper tag — is now frozen history: it documents what was done and stays reproducible via the tag
and DOI. The **shipped library** on `main`, meanwhile, keeps moving: it is trimmed to the preferred
approach and released for the next users. A reader reproduces the paper from the frozen snapshot; a
new user builds on the live library. Neither has to compromise the other, because each is anchored to
its own point in history.
