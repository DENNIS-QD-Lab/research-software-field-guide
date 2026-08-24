"""Sphinx configuration for the research-software-field-guide doc site."""

import sys
from pathlib import Path

# Make the repo root importable so autodoc can import `scripts` and
# `sample_data` as namespace packages. This repo has no pyproject.toml — see
# docs/disseminating/21_packaging.md's exemption for a scripts-and-docs repo.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

project = "research-software-field-guide"
copyright = "2026, Allison Dennis"
author = "Allison Dennis"

extensions = [
    "sphinx.ext.autodoc",  # generate pages from docstrings
    "sphinx.ext.napoleon",  # understand NumPy-style docstrings
    "sphinx.ext.intersphinx",  # cross-link into other projects' docs
    "myst_parser",  # author pages in Markdown, not just reStructuredText
]
html_theme = "furo"  # a clean, modern theme
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "h5py": ("https://docs.h5py.org/en/stable/", None),
}

# Register headings up to #### as cross-document link targets, so a link like
# [text](other_doc.md#some-heading) resolves instead of warning that the
# (actually-generated) anchor doesn't exist.
myst_heading_anchors = 4

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Several docs, and the {include}d root/CLAUDE.md/repo_kit files, link to files
# that live outside docs/ (or to a bare folder) so they read correctly on
# GitHub, where every relative link resolves against the file's real
# repository location. Those targets aren't documents Sphinx knows about, so
# MyST reports a cross-reference warning for each one, even though the links
# themselves are correct in their native (GitHub) reading context. Suppress
# this one warning class rather than rewriting every such link to a
# doc-site-only path.
suppress_warnings = ["myst.xref_missing"]
