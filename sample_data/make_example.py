"""Generate the synthetic example HDF5 file used by the show_h5_keys tutorial.

Run from the repository root:

    python sample_data/make_example.py

Produces `sample_data/example.h5`, a tiny synthetic file (a few small datasets
and attributes) so the tutorial runs without any real data. It is seeded, so it
regenerates identically. This is a teaching fixture, not research data (see
`CLAUDE.md`).
"""

from pathlib import Path

import h5py
import numpy as np

OUT = Path(__file__).resolve().parent / "example.h5"


def main() -> None:
    """Write the synthetic example file to sample_data/example.h5.

    Returns
    -------
    None
        Writes ``sample_data/example.h5`` for its side effect; nothing is
        returned.

    Examples
    --------
    >>> main()
    """
    rng = np.random.default_rng(0)
    wavelength_nm = np.linspace(400.0, 720.0, 32)

    with h5py.File(OUT, "w") as f:
        f.attrs["description"] = "Synthetic example file for the show_h5_keys tutorial"

        spectra = f.create_group("spectra")
        spectra.attrs["sample"] = "synthetic"
        spectra.create_dataset("wavelength_nm", data=wavelength_nm)
        spectra.create_dataset("absorbance", data=rng.random(32))
        spectra.create_dataset("emission", data=rng.random(32))

        meta = f.create_group("metadata")
        meta.attrs["instrument"] = "synthetic"
        meta.create_dataset("integration_time_ms", data=np.int64(100))

    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
