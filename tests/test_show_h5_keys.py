"""Regression test for scripts/show_h5_keys.py against the committed example fixture."""

from pathlib import Path

from scripts.show_h5_keys import show_keys

EXAMPLE = Path(__file__).resolve().parent.parent / "sample_data" / "example.h5"

EXPECTED_OUTPUT = """\
@description: Synthetic example file for the show_h5_keys tutorial
metadata/
  @instrument: synthetic
  integration_time_ms  shape=()  dtype=int64
spectra/
  @sample: synthetic
  absorbance  shape=(32,)  dtype=float64
  emission  shape=(32,)  dtype=float64
  wavelength_nm  shape=(32,)  dtype=float64
"""


def test_show_keys_prints_the_example_files_known_structure(capsys):
    show_keys(str(EXAMPLE))

    assert capsys.readouterr().out == EXPECTED_OUTPUT
