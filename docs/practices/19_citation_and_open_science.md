# Citation and open science

*Distribution tier, optional.* When research software becomes public or underpins a paper, it needs to be citable and reusable. This doc orients you; it is not a submission guide. The concrete candidate here is the public `SWIR_HDR` (v1), not the private v2.

## Why software citation matters

Software is a research output, like a dataset or a figure. Citing it does two things: it gives **credit** to the people who built the tool, and it supports **reproducibility**, because a reader can find the exact software, at the exact version, behind a result. "We used custom code" is not reproducible; "we used `SWIR_HDR` v2.1 (DOI ...)" is.

## LICENSE: what "reusable" actually requires

A **LICENSE** file states the terms under which others may use your code. Here is the fact scientists most often miss: **"no license" does not mean "free for anyone to use" — it means "not reusable."** With no license, default copyright applies, and others technically may not reuse the work. Choosing a license is choosing how open you want to be. Do not guess at the wording: **choosealicense.com** walks through the common options (MIT and BSD are permissive; the GPL family is copyleft). `SWIR_HDR` already carries a LICENSE; any new project needs one before it is meaningfully public.

## CITATION.cff

A **`CITATION.cff`** file at the repo root tells GitHub, and citation tools, how to cite the software. It is a small YAML file with a few fields: title, authors, version, and ideally a DOI. GitHub renders a "Cite this repository" button from it, so adding one is the lowest-effort step toward being citable.

## Zenodo and JOSS

- **Zenodo** mints a **DOI** (a permanent identifier) for a snapshot of your repository. Connect the repo once, and each tagged release, such as the `paper-v1` tag from `18_versioning_and_releases.md`, is archived and assigned its own DOI. The paper cites the DOI of that exact tagged state.
- **JOSS**, the Journal of Open Source Software, is a route to a short, peer-reviewed **software paper**: a citable publication about the software itself. It is more work than a Zenodo DOI, and worth it when the software is a contribution in its own right.

## The pattern, end to end

Tag the exact state used for the paper (`18_versioning_and_releases.md`), archive that tag to Zenodo for a DOI, and cite the DOI in the manuscript. That is how a paper stays reproducible against a specific, frozen version while the library keeps moving forward on `main` (`14_experiments_and_shipping.md`). Reproducibility comes from the archived snapshot, not from freezing the live code.
