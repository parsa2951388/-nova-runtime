#!/usr/bin/env python3
"""Scan NOVA-owned tracked files using the upstream binary-format detector."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE_SCANNER = ROOT / "engine" / "leonida" / "scripts" / "check_no_game_data.py"


def main() -> int:
    if not ENGINE_SCANNER.is_file():
        print(
            "NOVA data scan: engine submodule is not initialized. "
            "Run: git submodule update --init --recursive",
            file=sys.stderr,
        )
        return 2

    try:
        result = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        )
        tracked = [
            os.fsdecode(path)
            for path in result.stdout.split(b"\0")
            if path
        ]
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"NOVA data scan: cannot list tracked files: {exc}", file=sys.stderr)
        return 2

    absolute_paths = [str(ROOT / Path(path)) for path in tracked]
    try:
        scan = subprocess.run(
            [sys.executable, "-I", str(ENGINE_SCANNER), *absolute_paths],
            cwd=ROOT,
            check=False,
        )
    except OSError as exc:
        print(f"NOVA data scan: could not start detector: {exc}", file=sys.stderr)
        return 2

    if scan.returncode == 0:
        print(f"NOVA data scan passed ({len(tracked)} tracked root entries checked).")
    return scan.returncode


if __name__ == "__main__":
    raise SystemExit(main())
