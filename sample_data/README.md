# sample_data

Small **synthetic** data files used by the tutorials and examples so they run
without any real data. These are teaching fixtures, not research data, and are
the one exception to the "no data in the repo" rule (see `../CLAUDE.md`).

- `example.h5` — a tiny synthetic HDF5 file (spectra + metadata) for the
  `show_h5_keys` tutorial (`../docs/onboarding/07_notebooks.md`). Regenerate it
  with `python sample_data/make_example.py`.

Real or large datasets never belong here. Keep those on a drive and pass their
paths in (see the data-path note in `../docs/onboarding/07_notebooks.md`).
