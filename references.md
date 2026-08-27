# References

External resources this project builds on — papers, methods, standards, and web resources. One row
per resource: the citation, a link/DOI, the date accessed (for web pages that can change), and a
short note on relevance.

>Research-based work builds on existing knowledge, and the decisions in a repo rest on that knowledge.
Keeping the ledger current as sources come up — rather than reconstructing it at write-up time — is
what makes that knowledge easy to recover when it is time to write the manuscript, the docs, or the
next grant. This file is both **this guide's own ledger** and a worked example of the convention it
teaches in
[16_running_a_dry_lab_experiment.md](docs/implementing/16_running_a_dry_lab_experiment.md).

| Resource (citation) | Link / DOI | Accessed | Relevance |
|---|---|---|---|
| Wilson, Bryan, Cranston, Kitzes, Nederbragt, Teal, "Good Enough Practices in Scientific Computing", *PLOS Computational Biology* 13(6), 2017 | [10.1371/journal.pcbi.1005510](https://doi.org/10.1371/journal.pcbi.1005510) | 2026-08-05 | Publication discussing minimum-viable practices for scientists, not developers. |
| The Turing Way Community, *The Turing Way: A Handbook for Reproducible, Ethical and Collaborative Research* | [book.the-turing-way.org](https://book.the-turing-way.org/) | 2026-08-05 | Broad reproducibility case behind several onboarding docs (version control, environments, code review). |
| The Carpentries (Software Carpentry) lessons — *Programming with Python*, *The Unix Shell*, *Version Control with Git* | [swcarpentry.github.io](https://swcarpentry.github.io/) | 2026-08-05 | Fuller self-paced lessons behind this guide's fast on-ramps for Python, the shell, and git. |
| van Rossum, Warsaw, Coghlan, "PEP 8 – Style Guide for Python Code" | [peps.python.org/pep-0008](https://peps.python.org/pep-0008/) | 2026-08-05 | The style standard `ruff format`/`ruff check` enforce here. |
| Scientific Python Development Guide | [learn.scientific-python.org/development](https://learn.scientific-python.org/development/) | 2026-08-19 | Community-maintained (NumPy/SciPy/Astropy-ecosystem) standard for code quality, CI, docs, and packaging — more authoritative and more actively maintained than a house guide, with its own conformance checker and project template. |
| Bridgeford, Campbell, Chen, Lin, Ritz, Vandekerckhove, Poldrack, "Twelve Quick Tips for AI-Assisted Coding in Science", *PLOS Computational Biology*, 2026 | [10.1371/journal.pcbi.1014428](https://doi.org/10.1371/journal.pcbi.1014428) | 2026-08-11 | Independent confirmation of this guide's AI-assistant stance; flags "paper tests" (a mock asserting its own return value) as a risk to watch for. |
| Choose a License | [choosealicense.com](https://choosealicense.com/) | 2026-08-05 | Tool that helps choose the appropriate LICENSE for any project. |
| Zenodo | [zenodo.org](https://zenodo.org/) | 2026-08-05 | A free, open-access online archive hosted by CERN where researchers from any field can store and share digital files; use to archive data and/or to generate a permanent DOI for a tagged snapshot of a GitHub repository. |
| Zenodo, "Quickstart" | [help.zenodo.org/docs/get-started/quickstart](https://help.zenodo.org/docs/get-started/quickstart/) | 2026-08-26 | Walkthrough for connecting a GitHub repo and minting a DOI. |
| Journal of Open Source Software (JOSS) | [joss.theoj.org](https://joss.theoj.org/) | 2026-08-05 | Journal that publishes peer-reviewed papers describing open source software, for when the software is a contribution in its own right. |

<!--
Cross-repo convention: keep a references.md like this in every research repo, so the "resource + why
it mattered here" pairing travels with the code that used it. The convention itself is documented in
docs/implementing/16_running_a_dry_lab_experiment.md and summarized in repo_kit/STANDARD.md.
-->
