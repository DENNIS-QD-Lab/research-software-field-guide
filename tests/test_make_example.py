"""Regression test that sample_data/make_example.py regenerates byte-identically."""

import hashlib
from pathlib import Path

from sample_data import make_example

COMMITTED_EXAMPLE = (
    Path(__file__).resolve().parent.parent / "sample_data" / "example.h5"
)


def _md5(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


def test_make_example_regenerates_byte_identically(tmp_path, monkeypatch):
    regenerated = tmp_path / "example.h5"
    monkeypatch.setattr(make_example, "OUT", regenerated)

    make_example.main()

    assert _md5(regenerated) == _md5(COMMITTED_EXAMPLE)
