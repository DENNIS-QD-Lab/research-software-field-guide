# Concluding and disseminating a project

*Distribution tier, optional.* Every earlier doc in the experimentation part assumed the work was
still moving. This one is about the other end of the arc: a line of inquiry has concluded — a paper
is going out, or the software is becoming something others depend on — and the job now is to **freeze
the result, archive it, and make it citable**, so it stays findable and reproducible after you move
on. It orients you; it is not a submission guide. The concrete example throughout is a project
reaching a citable public release — for example, `SWIR_HDR` (v1).

## Concluding: freeze, archive, cite

The end-to-end pattern, and the single place it is defined in this track:

1. **Freeze** the exact state behind the result. Tag it (`paper-v1`;
   [22_versioning_and_releases.md](22_versioning_and_releases.md)) so that commit is pinned no matter how the code moves afterward.
2. **Archive** that tag for a permanent identifier. Connect the repo to **Zenodo** once, and each
   tagged release is archived and assigned its own **DOI**.
3. **Cite** the DOI in the manuscript.

That is how a paper stays reproducible against a specific, frozen version while the library keeps
moving forward on `main` ([15_experiments_and_shipping.md](../implementing/15_experiments_and_shipping.md)). Reproducibility comes from the archived
snapshot, not from freezing the live code. Everything below supports these three steps.

This is also where the **reference ledger** pays off. If you kept a `references.md` current as you went
([16_running_a_dry_lab_experiment.md](../implementing/16_running_a_dry_lab_experiment.md)) — each source paired with why it
mattered for a decision — that will directly inform the manuscript's methods and bibliography. The freeze captures the code; the ledger captures the prior work it was built on.

## Why software citation matters

Software is a research output, like a dataset or a figure. Citing it does two things: it gives
**credit** to the people who built the tool, and it supports **reproducibility**, because a reader
can find the exact software, at the exact version, behind a result. "We used custom code" is not
reproducible; "we used `SWIR_HDR` v2.1 (DOI ...)" is.

## LICENSE: what "reusable" actually requires

A **LICENSE** file states the terms under which others may use your code. Here is the fact scientists
most often miss: **"no license" does not mean "free for anyone to use" — it means "not reusable."**
With no license, default copyright applies, and others technically may not reuse the work. Choosing a
license is choosing how open you want to be. Do not guess at the wording: **choosealicense.com**
walks through the common options (MIT and BSD are permissive; the GPL family is copyleft). `SWIR_HDR`
already carries a LICENSE; any new project needs one before it is meaningfully public.

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

## The experimental record and the shipped library, going forward

Concluding a project is also where the two jobs of the repo ([15_experiments_and_shipping.md](../implementing/15_experiments_and_shipping.md)) part
ways cleanly. The **experimental record** — the research log, the `experiments/` folders, and
the paper tag — is now frozen history: it documents what was done and stays reproducible via the tag
and DOI. The **shipped library** on `main`, meanwhile, keeps moving: it is trimmed to the preferred
approach and released for the next users. A reader reproduces the paper from the frozen snapshot; a
new user builds on the live library. Neither has to compromise the other, because each is anchored to
its own point in history.
