# Concluding and disseminating a project

Every earlier doc in the experimentation part assumed the work was still moving. This one is about
the other end — and it covers two independent things "concluding" can mean.

The first is **freezing a citable snapshot**: a paper is going out, and a specific state of the code
and results needs to stay findable and reproducible forever, no matter how the project keeps moving
afterward. The second is **trimming toward a shippable library**: the pipeline itself is becoming
something other people install and depend on, pared down to the approach you settled on. A project
can do either, both, or neither — doing one does not require the other.

## The mechanics that make this free: tags, not copies

This is easy to miss coming from tools like Microsoft Office, where "keeping a version" means saving
a new file — `manuscript_v2.docx`, `manuscript_v2_final.docx`, `manuscript_v2_final_ACTUALLY.docx` —
each one a full, independent copy that starts drifting from the others immediately. Git does not
work that way, and the difference is what makes both arcs below painless rather than a chore you put
off.

A **branch** and a **tag** are both just named pointers into the same history, not copies of the
repository (the git commands for cutting one are in
[22_versioning_and_releases.md](22_versioning_and_releases.md)). Creating one costs nothing — no
duplicated files, nothing to keep in sync by hand. That means one repo can hold, at the same time:
`main`, the lab notebook that keeps growing for as long as the project continues; a tagged snapshot
(`paper-v1`) that reproduces one specific paper's figures, frozen forever at the state it was in when
you cut it; and, separately, another tagged snapshot (`v2.1.0`) of just the shipped library, trimmed
to the one approach you settled on. None of these compete for space or attention. You check one out
when you need it, by name, and go back to `main` when you don't.

The practical sequence, once a submission is close: keep working with merges to `main` as usual, then decide what
this *particular* paper actually needs — which experiment themes, which figures, which data
references — and prune the rest on a short-lived branch. Tag that state. Archive it to Zenodo (below). Then go back to `main`, which is untouched, and keep going: the next experiment, the next figure, the next paper. None of this
endangers the fuller history sitting in every earlier commit — a pruned tag is an additional,
permanent view onto one moment of it, not a replacement for it.

## Making a result citable: freeze, archive, cite

The end-to-end pattern for the first arc:

1. **Freeze** the exact state behind the result. Tag it (`paper-v1`) so that commit is pinned no
   matter how the code moves afterward.
2. **Archive** that tag for a permanent identifier. Connect the repo to **Zenodo** once, and each
   tagged release is archived and assigned its own **DOI**.
3. **Cite** the DOI in the manuscript.

This tagged, DOI'ed version of the repo ensures that a publication stays reproducible against a
specific, frozen version of the code that produced its results, even if/when the library keeps
moving forward on `main` ([15_experiments_and_shipping.md](../implementing/15_experiments_and_shipping.md)).
Reproducibility comes from the archived snapshot, not from freezing the live code.

### Why this matters beyond the DOI

Software is a research output, like a dataset or a figure. Citing it gives **credit** to the people
who built the tool, and it supports **reproducibility**, because a reader can find the exact
software, at the exact version, behind a result. "We used custom code" is not reproducible; "we used
`your_package` v2.1 (DOI ...)" is.

### LICENSE: what "reusable" actually requires

A **LICENSE** file states the terms under which others may use your code. Here is the fact
scientists most often miss: **"no license" does not mean "free for anyone to use" — it means "not
reusable."** With no license, default copyright applies, and others technically may not reuse the
work. Choosing a license is choosing how open you want to be. Do not guess at the wording:
**choosealicense.com** walks through the common options (MIT and BSD are permissive; the GPL family
is copyleft). Any new project needs one before it is meaningfully public.

### CITATION.cff

A **`CITATION.cff`** file at the repo root tells GitHub, and citation tools, how to cite the
software. It is a small YAML file with a few fields: title, authors, version, and ideally a DOI.
GitHub renders a "Cite this repository" button from it, so adding one is the lowest-effort step
toward being citable.

### Zenodo and JOSS

- **Zenodo** mints a **DOI** (a permanent identifier) for a snapshot of your repository. Connect the
  repo once, and each tagged release, such as the `paper-v1` tag above, is archived and assigned its
  own DOI. The paper cites the DOI of that exact tagged state.
- **JOSS**, the Journal of Open Source Software, is a route to a short, peer-reviewed **software
  paper**: a citable publication about the software itself. It is more work than a Zenodo DOI, and
  worth it when the software is a contribution in its own right.

## A `figures/` folder as the reproducibility package

[15_experiments_and_shipping.md](../implementing/15_experiments_and_shipping.md) and
[16_running_a_dry_lab_experiment.md](../implementing/16_running_a_dry_lab_experiment.md) cover
keeping a `figures/` folder while drafting a manuscript — the same theme-and-dated-runs discipline as
`experiments/`, applied to paper figures. That folder turns out to be most of what Zenodo wants
already: archiving *before* you submit, not after, gives you your own deposited record, under your
own account, ahead of any copyright agreement a journal attaches to the accepted manuscript. A common
shape for the archived snapshot is three folders — `data/`, `plotting_scripts/`, and `figures/` —
covering everything that produces a manuscript's figures except the manuscript text itself. If you
have been keeping a `figures/` folder all along, it *is* that folder; your figure-generating scripts
are the `plotting_scripts`; and `data/` is whatever your data references already point at
([17_working_with_large_data.md](../implementing/17_working_with_large_data.md)). Tagging for Zenodo
at that point is mostly a decision about what to leave out of this particular submission, not a
packaging effort built from scratch.

## Trimming toward a shippable library

The second arc — a tempting mistake, once you're ready to trim `src/` down to a clean, shippable
library: *"If I delete the old approach, I can't reproduce the paper that used it, so I'll keep it
around, just hidden."* Usually the hiding is done by leaving the module in place but not importing it
in `__init__.py`.

That does not work, and it's worth understanding why. **`__init__.py` controls the *exposed* public
API, not what *installs*.** Every module in `src/` still ships, still gets imported by something
eventually, and still has to be maintained when a dependency changes. Hiding an old approach behind
`__init__.py` does not remove its cost; it just makes the cost invisible — a permanent maintenance
tax, not a solution.

The actual resolution is the tag-based mechanics above: tag the full, pre-trim state first, *then*
strip the non-preferred approaches — on `main` or on a branch, whichever you chose. The stripped code
is not lost: it lives on in the tag and in git history. An experiment that needs the old approach
reproduces it by checking out that tag, not by running against whatever `src/` looks like now.

**The one exception.** If an alternative approach will be *deliberately used going forward* (not just
preserved for the record), then it is a supported option, not dead code. Make it first-class: tested
and documented, perhaps in a clearly named `legacy` subpackage. The rule is against *gated-off
clutter*, not against genuinely supporting more than one method when you mean to.

## Keeping the private notebook private, if you need to

Both arcs above assume the tag you freeze and archive is the same repo you have been working in —
the lab notebook itself. Sometimes it should not be: a research log can hold false starts, unfiltered
commentary, or context you never meant for a public audience, and archiving a tag from that repo
publishes it right along with the code.

The reason a public tag can't just hide the sensitive parts is structural: GitHub visibility applies
to a whole repository, not to one tag or branch inside it, so there is no setting that publishes a
snapshot while keeping the rest private. The fix is two repos, not one rewritten one — keep the
working repo private, and when it's time to disseminate, create a new, empty repository and copy in
only what should be public. [repo_ownership_and_visibility.md](../reference/repo_ownership_and_visibility.md)
covers this in full: the two-repo recipe, why it has to be a plain file copy rather than a clone, the
realistic ways this goes wrong by accident, and owning the repo through a lab organization rather
than a personal account. Decide this **before the repo ever goes public**, not after — once history
reaches a public remote, treat it as permanent.

## Going forward: the paper stays frozen, the library keeps moving

Concluding a project is also where the two arcs above part ways cleanly. The **experimental
record** — the research log, the `experiments/` folders, and the paper tag — is now frozen history:
it documents what was done and stays reproducible via the tag and DOI. The **shipped library** on
`main`, meanwhile, keeps moving: it is trimmed to the preferred approach and released for the next
users. A reader reproduces the paper from the frozen snapshot; a new user builds on the live library.
Neither has to compromise the other, because each is anchored to its own point in history.
