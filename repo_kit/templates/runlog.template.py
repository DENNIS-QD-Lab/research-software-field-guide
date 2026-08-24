"""Run logging for experiment drivers — reproducible, preserved run directories.

RUNLOG TEMPLATE — copy this file to ``experiments/_common/runlog.py`` in the target
repo. It is generic; no placeholders to fill. It needs PyYAML for writing
``manifest.yaml`` — add ``pyyaml`` to the environment file if nothing else already
pulls it in.

Each driver call opens a run directory named ``<YYMMDD>_<slug>[_NN]`` under
``output_dir`` and writes into it: ``manifest.yaml`` (git commit + dirty flag,
timestamp, driver name, the parameters that define this run, and the inputs it
consumed) and, via :meth:`RunLog.write_metrics`, ``metrics.csv``. This is
provenance for reproducibility, not a report — the narrative (question,
findings, interpretation) lives once in the experiment theme's own
``README.md``, updated in place as findings accrue, never regenerated per run.
See 16_running_a_dry_lab_experiment.md in the research-software-field-guide.

Default behavior PRESERVES: re-running the same slug creates the next ``_NN``
variant rather than overwriting the last one. Pass ``overwrite=True`` only to
refresh the latest matching run in place — for example, when finalizing a run
on a newly clean commit (see experiments_playbook.template.md's "Finalizing an
experiment").

Examples
--------
>>> run = start_run("experiments/my-theme/details", "seed0", {"seed": 0})
>>> fig_path = run.path("comparison.png")
>>> run.write_metrics([{"method": "a", "rmse": 1.2}])
>>> run.finalize()
"""

import csv
import os
import re
import subprocess
from datetime import datetime

import yaml


def _git_stamp(repo_root: str) -> dict[str, str | bool | None]:
    """Return the git commit hash and dirty flag for a repository.

    Parameters
    ----------
    repo_root : str
        Path inside the git repository to stamp.

    Returns
    -------
    dict[str, str | bool | None]
        ``{"commit": <short hash or None>, "dirty": <bool or None>}``. ``dirty``
        means the *tracked code* had uncommitted changes when the run
        executed; every ``details/`` tree is excluded from that check, so a
        run writing its own manifest and metrics never makes itself look
        dirty. Both values are ``None`` if ``repo_root`` is not a git
        checkout.

    Examples
    --------
    >>> _git_stamp(".")
    {'commit': 'a1b2c3d', 'dirty': False}
    """

    def _run(args: list[str]) -> str:
        return subprocess.run(
            ["git", "-C", repo_root, *args],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()

    try:
        # Exclude every details/ tree from the dirty check: a run's own
        # freshly-written manifest and metrics should never make otherwise
        # clean tracked code look dirty.
        code_status = _run(
            ["status", "--porcelain", "--", ":/", ":(exclude,glob)**/details/**"]
        )
        return {
            "commit": _run(["rev-parse", "--short", "HEAD"]),
            "dirty": bool(code_status),
        }
    except (subprocess.CalledProcessError, FileNotFoundError):
        return {"commit": None, "dirty": None}


def _resolve_run_id(output_dir: str, date_slug: str, overwrite: bool) -> str:
    """Pick the run id for a dated slug, preserving prior runs by default.

    Parameters
    ----------
    output_dir : str
        The experiment theme's ``details/`` directory.
    date_slug : str
        The ``<YYMMDD>_<slug>`` prefix for this run.
    overwrite : bool
        If True, reuse the latest matching variant instead of making a new
        one.

    Returns
    -------
    str
        The bare run id (e.g. ``"260806_baseline_02"``), not a path.

    Examples
    --------
    >>> _resolve_run_id("experiments/my-theme/details", "260806_baseline", overwrite=False)
    '260806_baseline'
    """
    os.makedirs(output_dir, exist_ok=True)
    dir_pattern = re.compile(rf"^{re.escape(date_slug)}(?:_(\d+))?$")
    variants = {
        int(m.group(1)) if m.group(1) else 1
        for name in os.listdir(output_dir)
        if (m := dir_pattern.match(name))
        and os.path.isdir(os.path.join(output_dir, name))
    }
    if not variants:
        return date_slug
    latest = max(variants)
    if overwrite:
        return date_slug if latest == 1 else f"{date_slug}_{latest:02d}"
    return f"{date_slug}_{latest + 1:02d}"


class RunLog:
    """A single experiment run's directory, manifest, and metrics.

    Parameters
    ----------
    output_dir : str
        The experiment theme's ``details/`` directory.
    slug : str
        A readable signature for this run's parameters (no date), e.g.
        ``"seed0_synthetic"``.
    experimental_params : dict
        The parameters that define this run's identity; recorded in the
        manifest.
    inputs : dict, optional
        Which data this run used — a dataset identifier and a checksum are
        typical (see 17_working_with_large_data.md).
    driver : str, optional
        The driver script's name, recorded in the manifest.
    summary : str, optional
        A one-line description of the run, recorded in the manifest so
        ``details/`` is scannable without opening every file.
    repo_root : str, optional
        Repository root to git-stamp. Defaults to three levels up from this
        file, which is correct once this file lives at
        ``experiments/_common/runlog.py``.
    overwrite : bool, default False
        Refresh the latest matching run in place instead of preserving a new
        one.

    Examples
    --------
    >>> run = RunLog("experiments/my-theme/details", "seed0", {"seed": 0})
    """

    def __init__(
        self,
        output_dir: str,
        slug: str,
        experimental_params: dict,
        inputs: dict | None = None,
        driver: str | None = None,
        summary: str | None = None,
        repo_root: str | None = None,
        overwrite: bool = False,
    ) -> None:
        self.slug = slug
        self.experimental_params = experimental_params
        self.inputs = inputs or {}
        self.driver = driver
        self.summary = summary
        self._created = datetime.now()
        if repo_root is None:
            repo_root = os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            )
        self.repo_root = repo_root
        date_slug = f"{self._created.strftime('%y%m%d')}_{slug}"
        run_id = _resolve_run_id(output_dir, date_slug, overwrite)
        self.dir = os.path.join(output_dir, run_id)
        os.makedirs(self.dir, exist_ok=True)

    def path(self, filename: str) -> str:
        """Return an absolute path inside the run directory, for saving a file.

        Parameters
        ----------
        filename : str
            File name to place in the run directory.

        Returns
        -------
        str
            The absolute path ``<run dir>/<filename>``.

        Examples
        --------
        >>> run.path("comparison.png")
        '/abs/path/to/experiments/my-theme/details/260806_seed0/comparison.png'
        """
        return os.path.join(self.dir, filename)

    def write_metrics(self, rows: list[dict], filename: str = "metrics.csv") -> str:
        """Write per-method metrics to a CSV in the run directory.

        Parameters
        ----------
        rows : list of dict
            One dict per method or condition; keys become CSV columns.
        filename : str, default "metrics.csv"
            File name for the CSV.

        Returns
        -------
        str
            Path to the written CSV.

        Examples
        --------
        >>> run.write_metrics([{"method": "linear", "rmse": 1.2}])
        '/abs/path/to/experiments/my-theme/details/260806_seed0/metrics.csv'
        """
        out = self.path(filename)
        if rows:
            with open(out, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                writer.writeheader()
                writer.writerows(rows)
        return out

    def finalize(self) -> str:
        """Write ``manifest.yaml`` with the full reproducibility stamp.

        Returns
        -------
        str
            Path to the written manifest.yaml.

        Examples
        --------
        >>> run.finalize()
        '/abs/path/to/experiments/my-theme/details/260806_seed0/manifest.yaml'
        """
        out = self.path("manifest.yaml")
        manifest = {
            "slug": self.slug,
            "summary": self.summary,
            "driver": self.driver,
            "created": self._created.isoformat(timespec="seconds"),
            "git": _git_stamp(self.repo_root),
            "inputs": self.inputs,
            "experimental_params": self.experimental_params,
        }
        with open(out, "w") as f:
            yaml.safe_dump(manifest, f, sort_keys=False, default_flow_style=False)
        return out


def start_run(
    output_dir: str, slug: str, experimental_params: dict, **kwargs
) -> RunLog:
    """Open a new run directory and return its RunLog.

    Parameters
    ----------
    output_dir : str
        The experiment theme's ``details/`` directory.
    slug : str
        A readable signature for this run's parameters (no date).
    experimental_params : dict
        The parameters that define this run's identity.
    **kwargs
        Forwarded to :class:`RunLog` (``inputs``, ``driver``, ``summary``,
        ``repo_root``, ``overwrite``).

    Returns
    -------
    RunLog
        An open run whose directory has been created.

    Examples
    --------
    >>> run = start_run("experiments/my-theme/details", "seed0", {"seed": 0})
    """
    return RunLog(output_dir, slug, experimental_params, **kwargs)
