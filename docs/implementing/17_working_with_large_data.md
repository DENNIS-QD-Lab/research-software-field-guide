# Working with data too big to commit

The data rule ([CLAUDE.md](../../CLAUDE.md), [04_environments.md](../onboarding/04_environments.md)) is simple: **data lives outside
the repo, and scripts take paths.** A real experiment, though, runs on gigabytes of acquired data
that live on a shared server or an external drive and sit in a different place on every machine. That
raises the question [16_running_a_dry_lab_experiment.md](16_running_a_dry_lab_experiment.md) depends on: if the inputs are not in git,
how is a run reproducible? The answer is to reference the data by a **stable identifier** and to
**pin which data a run used** — not to drag the data into the repo.

## Reference data by a stable identifier, not a hard-coded path

Two good ways to name where the data is, depending on its stage:

- **A machine-local root, kept out of git.** Put the one machine-specific line — where the data lives
  on *this* computer — in a git-ignored `local_paths.py` that exposes a `DATA_ROOT`, and commit a
  `local_paths_example.py` template beside it. Code imports `DATA_ROOT` and builds paths under it, so
  the scripts are identical on every machine and no one's home directory leaks into history.
- **A DOI, for archived or published data.** Once a dataset is deposited (Zenodo, a repository, a
  released benchmark), it has a permanent identifier. Reference that; the DOI resolves to the exact
  bytes forever, which a local path never can.

Either way, the experiment's `README` should say, in words, **where the canonical copy lives** (which
server/share, and where the backup is) so a teammate can actually obtain it.

## Pin *which* data a run used

Naming a folder is not enough — folders change. To make a run reproducible you have to be able to
prove a later run used the *same* input. Record, in the run's `manifest.yaml`
([16_running_a_dry_lab_experiment.md](16_running_a_dry_lab_experiment.md)), a **content hash** alongside the dataset name:

```yaml
inputs:
  dataset: run_2026-06-30
  dataset_sha256: 9c1f2a…          # hash of the file (or a manifest of the files)
```

For a multi-file dataset, commit a small **data manifest** — a text file listing each file with its
size and `sha256` — instead of the data itself. The manifest is a few kilobytes, it *is*
reproducible provenance, and it lets anyone verify their local copy matches the one behind your
result. This is the large-data analog of seeding: same inputs in, same numbers out.

## The small carve-out, and CI

The exception to "data stays out" is deliberately narrow: a **curated handful of real frames** kept
as a test or teaching fixture ([15_experiments_and_shipping.md](15_experiments_and_shipping.md), [CLAUDE.md](../../CLAUDE.md)). That is enough
to exercise the code and show a realistic case; the full acquired dataset stays out because it bloats
history permanently. This carve-out is also what lets a figure built from real data be committed
rather than regenerated: a synthetic, deterministic run can be rebuilt in CI, but a run over
gigabytes of acquired data cannot, so its (small) figure and provenance are committed as a fixture and
the report points at them.

## The bottom line

Reproducibility does not come from committing the data — a committed dataset bloats the repo forever
and still does not prove *which* version a result used. It comes from **a pinned code state** (a tag;
[22_versioning_and_releases.md](22_versioning_and_releases.md)) **plus a referenced, checksummed dataset**. Freeze the code, name
and hash the data, and the result is reproducible without a single gigabyte in git.
