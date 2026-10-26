"""Report where each local git repository stands against its remote, without the network.

The script reads only refs already on disk, so its answer is as current as the repo's last
``git fetch``; it prints when that was, so a stale picture is visible rather than silent. For each
repository it reports:

- the last fetch time, the current branch, and how many files have uncommitted changes;
- each local branch against its upstream: ahead, behind, no upstream, or upstream deleted on the
  remote (usually a merged pull request);
- how much new file data each branch would upload if pushed now, so a large push is planned before
  it fails partway;
- remote branches already merged into the default branch, and who last committed to the rest;
- extra worktrees.

Squash-merged branches are not recognized as merged, because squashing creates new commits.

Example
-------
Survey two repositories after fetching them::

    python survey_repos.py ~/code/analysis ~/code/pipeline
"""

from __future__ import annotations

import argparse
import subprocess
from datetime import datetime
from pathlib import Path

BYTES_PER_MB = 1024 * 1024


def run_git(repo: Path, *args: str, stdin: str | None = None) -> str:
    """Run one git command in a repository and return its standard output.

    Parameters
    ----------
    repo : Path
        The repository's working directory.
    *args : str
        Arguments after ``git``, for example ``"status", "--short"``.
    stdin : str | None, optional
        Text passed to the command's standard input. Defaults to None.

    Returns
    -------
    str
        The command's standard output, stripped of surrounding whitespace; an empty string if
        the command failed.

    Examples
    --------
    >>> run_git(Path("."), "branch", "--show-current")  # doctest: +SKIP
    'main'
    """
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        input=stdin,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def last_fetch_time(repo: Path) -> str:
    """When the repository last fetched from any remote, from ``FETCH_HEAD``'s timestamp.

    Parameters
    ----------
    repo : Path
        The repository's working directory.

    Returns
    -------
    str
        A local date and time, or ``"never"`` if the repository has not fetched.

    Examples
    --------
    >>> last_fetch_time(Path("."))  # doctest: +SKIP
    '2026-10-26 15:02'
    """
    fetch_head = Path(run_git(repo, "rev-parse", "--absolute-git-dir")) / "FETCH_HEAD"
    if not fetch_head.exists():
        return "never"
    return datetime.fromtimestamp(fetch_head.stat().st_mtime).strftime("%Y-%m-%d %H:%M")


def default_branch(repo: Path) -> str:
    """The remote's default branch, as a remote-tracking ref such as ``origin/main``.

    Parameters
    ----------
    repo : Path
        The repository's working directory.

    Returns
    -------
    str
        The ref that ``origin/HEAD`` points to, else ``origin/main`` or ``origin/master``
        if either exists, else an empty string.

    Examples
    --------
    >>> default_branch(Path("."))  # doctest: +SKIP
    'origin/main'
    """
    head = run_git(repo, "symbolic-ref", "--short", "refs/remotes/origin/HEAD")
    if head:
        return head
    for candidate in ("origin/main", "origin/master"):
        if run_git(repo, "rev-parse", "--verify", "--quiet", candidate):
            return candidate
    return ""


def unpushed_megabytes(repo: Path, branch: str) -> float:
    """New file data a push of ``branch`` would upload: blobs no remote-tracking ref reaches.

    Parameters
    ----------
    repo : Path
        The repository's working directory.
    branch : str
        A local branch name.

    Returns
    -------
    float
        Uncompressed size of those blobs in megabytes. The upload is usually a little smaller,
        because git compresses what it sends.

    Examples
    --------
    >>> unpushed_megabytes(Path("."), "feature")  # doctest: +SKIP
    12.4
    """
    objects = run_git(repo, "rev-list", "--objects", branch, "--not", "--remotes")
    if not objects:
        return 0.0
    ids = "\n".join(line.split()[0] for line in objects.splitlines()) + "\n"
    checked = run_git(
        repo, "cat-file", "--batch-check=%(objecttype) %(objectsize)", stdin=ids
    )
    sizes = [
        int(size)
        for kind, size in (line.split() for line in checked.splitlines())
        if kind == "blob"
    ]
    return sum(sizes) / BYTES_PER_MB


def branch_lines(repo: Path) -> list[str]:
    """One line per local branch: its state against its upstream and any unpushed data.

    Parameters
    ----------
    repo : Path
        The repository's working directory.

    Returns
    -------
    list[str]
        Lines such as ``"feature: ahead 3 of origin/feature, 12.4 MB to upload"``.

    Examples
    --------
    >>> branch_lines(Path("."))  # doctest: +SKIP
    ['main: in sync with origin/main']
    """
    refs = run_git(
        repo,
        "for-each-ref",
        "--format=%(refname:short)|%(upstream:short)|%(upstream:track)",
        "refs/heads",
    )
    lines = []
    for ref in refs.splitlines():
        branch, upstream, track = ref.split("|")
        if not upstream:
            same_name = f"origin/{branch}"
            if run_git(repo, "rev-parse", "--verify", "--quiet", same_name):
                state = f"no upstream set, but {same_name} exists (pushed without -u)"
            else:
                state = "no upstream: never pushed"
        elif track == "[gone]":
            state = f"upstream {upstream} deleted on the remote (merged PR?)"
        elif track:
            state = f"{track.strip('[]')} of {upstream}"
        else:
            state = f"in sync with {upstream}"
        megabytes = unpushed_megabytes(repo, branch)
        if megabytes >= 0.05:
            state += f", {megabytes:.1f} MB to upload"
        lines.append(f"{branch}: {state}")
    return lines


def remote_branch_lines(repo: Path, default: str) -> list[str]:
    """One line per remote branch other than the default: merged, or who last committed.

    Parameters
    ----------
    repo : Path
        The repository's working directory.
    default : str
        The default branch, from :func:`default_branch`.

    Returns
    -------
    list[str]
        Lines such as ``"origin/old-fix: merged into origin/main"`` or
        ``"origin/analysis: not merged; last commit 2026-10-21 by Maria"``.

    Examples
    --------
    >>> remote_branch_lines(Path("."), "origin/main")  # doctest: +SKIP
    ['origin/old-fix: merged into origin/main']
    """
    refs = run_git(repo, "for-each-ref", "--format=%(refname:short)", "refs/remotes")
    lines = []
    for ref in refs.splitlines():
        if ref in (default, "origin", "origin/HEAD") or ref.endswith("/HEAD"):
            continue
        merged = subprocess.run(
            ["git", "-C", str(repo), "merge-base", "--is-ancestor", ref, default],
            capture_output=True,
            check=False,
        )
        if default and merged.returncode == 0:
            lines.append(f"{ref}: merged into {default}")
        else:
            last = run_git(
                repo, "log", "-1", "--format=%ad by %an", "--date=short", ref
            )
            lines.append(f"{ref}: not merged; last commit {last}")
    return lines


def survey(repo: Path) -> str:
    """The full report for one repository.

    Parameters
    ----------
    repo : Path
        The repository's working directory.

    Returns
    -------
    str
        A multi-line report, or a one-line note if ``repo`` is not a git repository.

    Examples
    --------
    >>> print(survey(Path(".")))  # doctest: +SKIP
    """
    if not run_git(repo, "rev-parse", "--git-dir"):
        return f"=== {repo}: not a git repository"
    remotes = run_git(repo, "remote")
    current = run_git(repo, "branch", "--show-current") or "(detached HEAD)"
    changed = len(run_git(repo, "status", "--porcelain").splitlines())
    report = [
        f"=== {repo.name}",
        f"last fetch: {last_fetch_time(repo)}",
        f"on {current}; {changed} file(s) with uncommitted changes",
    ]
    if not remotes:
        report.append("no remote configured: nothing here is on GitHub")
        return "\n".join(report)
    default = default_branch(repo)
    report.append(f"default branch: {default or 'unknown'}")
    report += ["  " + line for line in branch_lines(repo)]
    report += ["  " + line for line in remote_branch_lines(repo, default)]
    worktrees = run_git(repo, "worktree", "list").splitlines()[1:]
    report += ["  worktree: " + line for line in worktrees]
    return "\n".join(report)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "repos",
        nargs="*",
        type=Path,
        default=[Path(".")],
        help="repository directories; defaults to the current directory",
    )
    args = parser.parse_args()
    print("\n\n".join(survey(repo.expanduser().resolve()) for repo in args.repos))


if __name__ == "__main__":
    main()
