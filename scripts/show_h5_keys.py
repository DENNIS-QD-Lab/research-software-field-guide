"""Print the structure of an HDF5 file.

HDF5 (.h5) files store data in a nested tree of *groups* (which work like
folders) and *datasets* (which work like arrays). Groups and datasets can also
carry *attributes*: small key/value pairs of metadata attached to them. This
script walks the tree and prints every group and dataset, each dataset's shape
and dtype, and any attributes, so you can see what is inside a file without
loading the data into memory.

Inputs:
    One command line argument: the path to the HDF5 file you want to inspect.

Example call:
    python scripts/show_h5_keys.py path/to/data.h5

The core function is also importable from other code:
    from scripts.show_h5_keys import show_keys
    show_keys("path/to/data.h5")
"""

import argparse

import h5py


def show_keys(path: str) -> None:
    """Print every group and dataset in an HDF5 file.

    Args:
        path: Path to the HDF5 file to inspect.

    Groups are printed with a trailing slash. Datasets are printed with their
    shape and dtype. Attributes are printed beneath their item, each prefixed
    with "@". Nesting in the file is shown by indentation.
    """
    with h5py.File(path, "r") as f:
        _print_attrs(f, indent=0)
        _print_group(f, indent=0)


def _print_group(group: h5py.Group, indent: int) -> None:
    """Recursively print the contents of one HDF5 group."""
    pad = "  " * indent
    for key, item in group.items():
        if isinstance(item, h5py.Group):
            print(f"{pad}{key}/")
            _print_attrs(item, indent + 1)
            _print_group(item, indent + 1)
        else:  # an h5py.Dataset
            print(f"{pad}{key}  shape={item.shape}  dtype={item.dtype}")
            _print_attrs(item, indent + 1)


def _print_attrs(obj: "h5py.Group | h5py.Dataset", indent: int) -> None:
    """Print the attributes attached to one group or dataset, if any."""
    pad = "  " * indent
    for key, val in obj.attrs.items():
        print(f"{pad}@{key}: {val}")


def main() -> None:
    """Parse command-line arguments and print the file's keys."""
    parser = argparse.ArgumentParser(
        description="Print the structure of an HDF5 file."
    )
    parser.add_argument("path", help="Path to the HDF5 file to inspect.")
    args = parser.parse_args()
    show_keys(args.path)


if __name__ == "__main__":
    main()
