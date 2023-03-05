#!/usr/bin/env python3
"""Compare two versions of ruff against a corpus of open-source code.

Example usage:

    scripts/check_ecosystem.py <path/to/ruff1> <path/to/ruff2>
"""

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
    from collections.abc import AsyncIterator, Iterator


class Repository(NamedTuple):
    """A GitHub repository at a specific ref."""

    org: str
    repo: str
    ref: str

    @asynccontextmanager
    async def clone(self: Self) -> "AsyncIterator[Path]":
        """Shallow clone a repository at a specific ref."""
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


async def check(*, ruff: Path, path: Path) -> "Iterator[str]":
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

    return sorted([
        line for line in result.decode("utf8").splitlines()
        if not SUMMARY_LINE_RE.match(line)
    ])


async def compare(*, ruff1: Path, ruff2: Path, name: str) -> bool:
    """Check a specific repository against two versions of ruff."""
    repo = REPOSITORIES[name]

    async with repo.clone() as path:
        async with asyncio.TaskGroup() as tg:
            check1 = tg.create_task(check(ruff=ruff1, path=path))
            check2 = tg.create_task(check(ruff=ruff2, path=path))

        for line in difflib.ndiff(check1.result(), check2.result()):
            if line.startswith(('- ', '+ ')):
                print(line)

    return True


async def main(*, ruff1: Path, ruff2: Path) -> None:
    """Compare two versions of ruff against a corpus of open-source code."""
    tasks = []

    async with asyncio.TaskGroup() as tg:
        tasks.append(tg.create_task(compare(ruff1=ruff1, ruff2=ruff2, name="zulip")))

    print(tasks[0].result())


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
