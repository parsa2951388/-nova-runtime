#!/usr/bin/env python3
"""Verify that the checked-out engine matches NOVA's committed Git submodule pin."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine" / "leonida"
EXPECTED_URL = "https://github.com/ubiquitarianism/leonida.git"


def run_git(arguments: list[str], cwd: Path = ROOT) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode:
        message = result.stderr.strip() or f"git {' '.join(arguments)} failed"
        raise RuntimeError(message)
    return result.stdout.strip()


def main() -> int:
    try:
        url = run_git(["config", "--file", ".gitmodules", "--get", "submodule.engine/leonida.url"])
        if url != EXPECTED_URL:
            raise RuntimeError(f"Unexpected engine submodule URL: {url}")

        tree_entry = run_git(["ls-tree", "HEAD", "engine/leonida"])
        parts = tree_entry.split()
        if len(parts) < 3 or parts[0] != "160000" or parts[1] != "commit":
            raise RuntimeError("HEAD does not contain engine/leonida as a Git submodule.")
        pinned_sha = parts[2]

        if not (ENGINE / "make_game.py").is_file():
            raise RuntimeError("Engine is not initialized. Run: git submodule update --init --recursive")

        checked_out_sha = run_git(["rev-parse", "HEAD"], cwd=ENGINE)
        if checked_out_sha != pinned_sha:
            raise RuntimeError(
                f"Submodule checkout mismatch: expected {pinned_sha}, found {checked_out_sha}"
            )

        nested = run_git(
            ["config", "--file", ".gitmodules", "--get", "submodule.third_party/rpf9-explorer.url"],
            cwd=ENGINE,
        )
        print(f"Engine URL: {url}")
        print(f"Engine pin: {pinned_sha}")
        print(f"Nested dependency: {nested}")
        print("Upstream pin verification passed.")
        return 0
    except (OSError, RuntimeError) as exc:
        print(f"Upstream pin verification failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
