# Versioning and releases

*Distribution tier, optional.* Once other people or other projects depend on your code, they need to say *which* version they depend on. This doc covers how to version and release a project. Like the rest of this tier, it applies when a project is depended on or published, not to everyday scripts.

## Semantic versioning

Version numbers are **MAJOR.MINOR.PATCH** (for example `2.1.0`), and each part carries a promise:

- **PATCH** (`2.1.0` → `2.1.1`): bug fixes, no change to how the code behaves for users.
- **MINOR** (`2.1.0` → `2.2.0`): new features, but existing usage still works (backward-compatible).
- **MAJOR** (`2.1.0` → `3.0.0`): breaking changes; code using the old version may need updating.

The scheme tells a user, at a glance, whether upgrading is safe. There is also the **0.x convention**: while a project is below `1.0.0`, it is signaling "still unstable, anything may change." For example, the SWIR_HDR project is past that: its `v1.0` was the published release, and current work is on the `2.x` line.

## Tags and releases

A **git tag** marks one commit as a named point in history:

```
git tag -a v2.1.0 -m "Release 2.1.0"
git push origin v2.1.0
```

A **GitHub release** builds on a tag, adding release notes and downloadable archives. Tags are also how you freeze a *scientific* result: the `paper-v1` snapshot tag from `15_experiments_and_shipping.md` marks the exact state used for a manuscript, so it stays reproducible no matter how the code changes afterward.

## A single source of truth for the version

The version should live in exactly one place, so it can never disagree with itself. For example, a project's `pyproject.toml` declares `version = "2.1.0"`, and the package reads it back at runtime from the installed metadata (`yourpkg.__version__`) rather than hard-coding the number a second time. One place to change, no chance of drift.

## CHANGELOG

A `CHANGELOG.md` is the human-readable companion to the version numbers: a short, dated list of what changed in each release, grouped as Added / Changed / Fixed. The version number tells a tool what *kind* of change happened; the changelog tells a person what actually changed.

## When a heavier branching model finally earns its keep

`10_from_scripts_to_pipelines.md` steered you away from a permanent `dev` or release-branch model, because for an internal pipeline it is pure overhead. This is the point where that can change. If you begin cutting **scheduled public releases** that must be stabilized while development keeps going, a release-branch model may at last be worth its weight. The trigger is real releases to outside users, and not before.

Automated release publishing (pushing tagged releases to a package index from CI ) is the next step beyond this, and out of scope here. (Note: Python package index = PyPI.)
