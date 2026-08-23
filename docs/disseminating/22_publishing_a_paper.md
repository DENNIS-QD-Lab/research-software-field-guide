# Publishing a paper

This doc is about freezing a citable snapshot of a project for a publication: a paper is going out,
and a specific state of the code and results needs to stay findable and reproducible forever, no
matter how the project keeps moving afterward. [23_shipping_a_library.md](23_shipping_a_library.md)
covers the separate, independent case of trimming the pipeline itself into something other people
install and depend on. A project may do either, both, or neither.

## Tags and releases

A **git tag** marks one commit as a named point in history:

```
git tag -a paper-v1 -m "State used for <paper>"
git push origin paper-v1
```

A **GitHub release** builds on a tag, adding release notes and downloadable archives. Tags are how
you freeze a *scientific* result: the `paper-v1` snapshot marks the exact state used for a
manuscript, so it stays reproducible no matter how the code changes afterward
([15_experiments_and_shipping.md](../implementing/15_experiments_and_shipping.md)).

This is easy to miss coming from tools like Microsoft Office, where "keeping a version" means saving
a new file — `manuscript_v2.docx`, `manuscript_v2_final.docx`, `manuscript_v2_final_ACTUALLY.docx` —
each one a full, independent copy that starts drifting from the others immediately. Git does not
work that way: a tag is just a named pointer into existing history, not a copy of the repository.
Creating one costs nothing — no duplicated files, nothing to keep in sync by hand.

That means one repo can hold, at the same time: `main`, the lab notebook that keeps growing for as
long as the project continues, and a tagged snapshot (`paper-v1`) that reproduces one specific
paper's figures, frozen forever at the state it was in when you cut it. Neither competes for space
or attention — you check a tagged version out when you need it, by name, and go back to `main` when you don't.

The practical sequence, once a submission is close: keep working with merges to `main` as usual,
then decide what this *particular* paper actually needs — which experiment themes, which figures,
which data references — and prune the rest on a short-lived branch. Tag that state. Archive it to
Zenodo (below). Then go back to `main`, which is untouched, and keep going: the next experiment, the
next figure, the next paper. None of this endangers the fuller history sitting in every earlier
commit — a pruned tag is an additional, permanent view onto one moment of it, not a replacement for
it.

## Making a result citable: freeze, archive, cite

The end-to-end pattern:

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
is copyleft). Any new project needs one before it is meaningfully public — including a project that
never publishes a paper at all but is [shipped as a library](23_shipping_a_library.md) instead.

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

## A repo just for the paper vs. the lab notebook

Everything above assumes the tag you freeze and archive is the same repo you've been working in —
the lab notebook itself. Sometimes it should not be: a research log can hold false starts, unfiltered
commentary, or context you never meant for a public audience, and archiving a tag from that repo
publishes it right along with the code.

The reason a public tag can't just hide the sensitive parts is structural: GitHub visibility applies
to a whole repository, not to one tag or branch inside it, so there is no setting that publishes a
snapshot while keeping the rest private. The fix is two repos, not one rewritten one — keep the
working repo private, and when it's time to disseminate, create a new, empty repository and copy in
only what should be public: the library code, the experiment folders and figures relevant to this
paper, docs, README, LICENSE. [repo_ownership_and_visibility.md](../reference/repo_ownership_and_visibility.md)
covers this in full: the two-repo recipe, why it has to be a plain file copy rather than a clone, the
realistic ways this goes wrong by accident, and owning the repo through a lab organization rather
than a personal account. Decide this **before the repo ever goes public**, not after — once history
reaches a public remote, treat it as permanent.

The same two-repo pattern applies if this project is also becoming an installable library, for the
same structural reason — see
[23_shipping_a_library.md](23_shipping_a_library.md#a-shipped-repo-vs-the-lab-notebook).
