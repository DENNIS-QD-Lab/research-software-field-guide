# References

External resources this project builds on — papers, methods, standards, and web resources. One row
per resource: the citation, a link/DOI, the date accessed (for web pages that can change), and the
**key relevant points** for *this* project (why it matters here, not a general summary).

Research-based work builds on existing knowledge, and the decisions in a repo rest on that knowledge.
Keeping the ledger current as sources come up — rather than reconstructing it at write-up time — is
what makes the citations, and the reasoning behind each choice, easy to recover when it is time to
write the manuscript, the docs, or the next grant. This file is both **this guide's own ledger** and a
worked example of the convention it teaches in
[docs/implementing/16_running_a_dry_lab_experiment.md](docs/implementing/16_running_a_dry_lab_experiment.md).

| Resource (citation) | Link / DOI | Accessed | Key relevant points for this project |
|---|---|---|---|
| Wilson, Bryan, Cranston, Kitzes, Nederbragt, Teal, "Good Enough Practices in Scientific Computing", *PLOS Computational Biology* 13(6), 2017 | [10.1371/journal.pcbi.1005510](https://doi.org/10.1371/journal.pcbi.1005510) | 2026-08-05 | The closest prior art to this whole guide: minimum-viable practices for data management, software, collaboration, and project organization aimed at working scientists, not developers. Grounds the "organized so future-you can find and reuse it" framing (onboarding doc 06) and the overall stance that structure serves the science. |
| The Turing Way Community, *The Turing Way: A Handbook for Reproducible, Ethical and Collaborative Research* | [book.the-turing-way.org](https://book.the-turing-way.org/) | 2026-08-05 | The broad reproducibility case behind several onboarding docs: Version Control (doc 03), Reproducible Environments (doc 04), Motivation for Using GitHub (doc 05), and the Code Reviewing Process (doc 08). We point readers here for the general "why", then teach the repo-specific "how". |
| The Carpentries (Software Carpentry) lessons — *Programming with Python*, *The Unix Shell*, *Version Control with Git* | [swcarpentry.github.io](https://swcarpentry.github.io/) | 2026-08-05 | The full self-paced fundamentals our fast on-ramps defer to: Python basics (doc 00), the shell (doc 01), and Git (doc 03). Our docs cover what a contributor needs *in this repo*; these are the deeper standalone lessons. |
| van Rossum, Warsaw, Coghlan, "PEP 8 – Style Guide for Python Code" | [peps.python.org/pep-0008](https://peps.python.org/pep-0008/) | 2026-08-05 | The Python style standard this repo enforces via `ruff format`/`ruff check` (CLAUDE.md; implementing doc 11). The reason "don't hand-format, let the tools decide" is a defensible default rather than a house preference. |
| Choose a License | [choosealicense.com](https://choosealicense.com/) | 2026-08-05 | The reference we send readers to for picking a LICENSE (implementing doc 23): permissive (MIT/BSD) vs. copyleft (GPL). Basis for the "no license means *not reusable*" point. |
| Zenodo | [zenodo.org](https://zenodo.org/) | 2026-08-05 | Mints a permanent DOI for a tagged snapshot of a repository (implementing doc 23). The archival step that makes a paper reproducible against a specific frozen version. |
| Journal of Open Source Software (JOSS) | [joss.theoj.org](https://joss.theoj.org/) | 2026-08-05 | The short, peer-reviewed software-paper route cited in implementing doc 23, for when the software is a contribution in its own right. |
| Bridgeford, Campbell, Chen, Lin, Ritz, Vandekerckhove, Poldrack, "Twelve Quick Tips for AI-Assisted Coding in Science", *PLOS Computational Biology*, 2026 | [10.1371/journal.pcbi.1014428](https://doi.org/10.1371/journal.pcbi.1014428) | 2026-08-11 | Independent confirmation of most of this guide's AI-assistant stance (docs 18–19): plan before implementing, keep durable context in external files, review generated code critically, document for reproducibility. One gap it surfaces that our docs don't yet name explicitly: AI-generated tests can be "paper tests" that pass without actually exercising the behavior (e.g. asserting a mock's own return value) — worth a line in doc 19's test-verification guidance. |
| Scientific Python Development Guide | [learn.scientific-python.org/development](https://learn.scientific-python.org/development/) | 2026-08-19 | Community-maintained (NumPy/SciPy/Astropy-ecosystem) standard for the same code-quality/CI/docs/packaging ground as implementing docs 11, 14, 20 and disseminating doc 21 — and the more authoritative, actively-updated source for it, with an automated conformance checker (`sp-repo-review`) and a scaffolding template (`scientific-python/cookie`). Explicitly does not cover Python/git basics or the dry-lab experiment framework, which is why those docs stay in place rather than deferring entirely; those four docs now point to its matching topical guide instead of re-deriving the same tooling advice. |

<!--
Cross-repo convention: keep a references.md like this in every research repo, so the "resource + why
it mattered here" pairing travels with the code that used it. The convention itself is documented in
docs/implementing/16_running_a_dry_lab_experiment.md and summarized in repo_kit/STANDARD.md.
-->
