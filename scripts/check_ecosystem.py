#!/usr/bin/env python3
"""Compare two versions of ruff against a corpus of open-source code.

Example usage:

    scripts/check_ecosystem.py <path/to/ruff1> <path/to/ruff2>
"""

# ruff: noqa: T201

import argparse
import asyncio
import difflib
import re
import tempfile
from asyncio.subprocess import PIPE, create_subprocess_exec
from contextlib import asynccontextmanager
from pathlib import Path
from typing import TYPE_CHECKING, NamedTuple, Self

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Sequence


class Repository(NamedTuple):
    """A GitHub repository at a specific ref."""

    org: str
    repo: str
    ref: str

    @asynccontextmanager
    async def clone(self: Self) -> "AsyncIterator[Path]":
        """Shallow clone this repository to a temporary directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            process = await create_subprocess_exec(
                "git",
                "clone",
                "--quiet",
                "--depth",
                "1",
                "--no-tags",
                "--branch",
                self.ref,
                f"https://github.com/{self.org}/{self.repo}",
                tmpdir,
            )

            await process.wait()

            yield Path(tmpdir)


REPOSITORIES = {
    "zulip": Repository("zulip", "zulip", "main"),
}

SUMMARY_LINE_RE = re.compile(r"^Found \d+ error.*$")


async def check(*, ruff: Path, path: Path) -> "Sequence[str]":
    """Run the given ruff binary against the specified path."""
    proc = await create_subprocess_exec(
        ruff.absolute(),
        "check",
        "--no-cache",
        ".",
        stdout=PIPE,
        stderr=PIPE,
        cwd=path,
    )

    result, err = await proc.communicate()

    lines = [
        line
        for line in result.decode("utf8").splitlines()
        if not SUMMARY_LINE_RE.match(line)
    ]

    return sorted(lines)


class Diff(NamedTuple):
    """A diff between two runs of ruff."""

    removed: list[str]
    added: list[str]

    def __bool__(self: Self) -> bool:
        """Return true if this diff is non-empty."""
        return bool(self.removed or self.added)


async def compare(ruff1: Path, ruff2: Path, repo: Repository) -> Diff:
    """Check a specific repository against two versions of ruff."""
    removed, added = [], []

    async with repo.clone() as path:
        async with asyncio.TaskGroup() as tg:
            check1 = tg.create_task(check(ruff=ruff1, path=path))
            check2 = tg.create_task(check(ruff=ruff2, path=path))

        for line in difflib.ndiff(check1.result(), check2.result()):
            if line.startswith("- "):
                removed.append(line[2:])
            elif line.startswith("+ "):
                added.append(line[2:])

    return Diff(removed, added)


async def main(*, ruff1: Path, ruff2: Path) -> None:
    """Compare two versions of ruff against a corpus of open-source code."""
    tasks = {}

    async with asyncio.TaskGroup() as tg:
        for name, repo in REPOSITORIES.items():
            tasks[name] = tg.create_task(compare(ruff1, ruff2, repo))

    total_removed = total_added = 0

    for task in tasks.values():
        diff = task.result()
        total_removed += len(diff.removed)
        total_added += len(diff.added)

    if total_removed == 0 and total_added == 0:
        print("\u2705 ecosystem check detected no changes.")
    else:
        changes = f"(+{total_added}, -{total_removed})"

        print(f"\u2139\ufe0f ecosystem check **detected changes**. {changes}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compare two versions of ruff against a corpus of open-source code.",
        epilog="scripts/check_ecosystem.py <path/to/ruff1> <path/to/ruff2>",
    )

    parser.add_argument(
        "ruff1",
        type=Path,
    )
    parser.add_argument(
        "ruff2",
        type=Path,
    )

    args = parser.parse_args()

    asyncio.run(main(ruff1=args.ruff1, ruff2=args.ruff2))
