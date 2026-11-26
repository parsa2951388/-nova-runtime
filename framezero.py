#!/usr/bin/env python3
"""FRAMEZERO LAB command-line front end.

This project owns diagnostics and orchestration only. Engine implementation remains
in the separately licensed and attributed upstream submodule.
"""
from __future__ import annotations

import json
import os
import platform
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
ENGINE = ROOT / "engine" / "leonida"
ENGINE_SCRIPT = ENGINE / "make_game.py"
NESTED_ENGINE = ENGINE / "third_party" / "rpf9-explorer"
EXPECTED_ENGINE_URL = "https://github.com/ubiquitarianism/leonida.git"
MIN_PYTHON = (3, 12)
FULL_BUILD_GIB = 400
RUNTIME_BUILD_GIB = 30
APP_NAME = "FRAMEZERO LAB"
APP_VERSION = "0.2.0-dev"


def parse_version(value: str | None) -> tuple[int, int, int] | None:
    """Extract a numeric major.minor.patch tuple from a tool version string."""
    if not value:
        return None
    match = re.search(r"(?<!\d)(\d+)\.(\d+)(?:\.(\d+))?", value)
    if not match:
        return None
    return tuple(int(part or 0) for part in match.groups())


def version_at_least(value: str | None, minimum: tuple[int, int, int]) -> bool:
    """Return whether a version string meets a minimum version."""
    parsed = parse_version(value)
    return parsed is not None and parsed >= minimum


def _run(
    command: list[str],
    timeout: int = 10,
    cwd: Path = ROOT,
) -> subprocess.CompletedProcess[str] | None:
    """Run a local diagnostic command without invoking a shell."""
    try:
        return subprocess.run(
            command,
            cwd=cwd,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None


def _git_text(arguments: list[str], cwd: Path = ROOT) -> str | None:
    result = _run(["git", *arguments], cwd=cwd)
    if result is None or result.returncode != 0:
        return None
    return result.stdout.strip()


def _version_check(
    label: str,
    command: list[str],
    minimum: tuple[int, int, int] | None = None,
    target_text: str | None = None,
) -> dict[str, str]:
    result = _run(command + ["--version"])
    if result is None or result.returncode != 0:
        return {
            "name": label,
            "status": "missing",
            "detail": f"Could not run: {' '.join(command)}",
        }
    output = (result.stdout or "") + "\n" + (result.stderr or "")
    version = parse_version(output)
    if minimum and (version is None or version < minimum):
        return {
            "name": label,
            "status": "missing",
            "detail": f"Found {version or 'unknown version'}; requires {minimum[0]}.{minimum[1]} or newer.",
        }
    if target_text and target_text.lower() not in output.lower():
        return {
            "name": label,
            "status": "missing",
            "detail": f"Found a version, but its output does not list the required {target_text} target.",
        }
    first_line = next((line.strip() for line in output.splitlines() if line.strip()), "Available")
    return {"name": label, "status": "ready", "detail": first_line}


def _engine_checkout_check() -> dict[str, str]:
    if not ENGINE_SCRIPT.is_file():
        return {
            "name": "Engine submodule",
            "status": "missing",
            "detail": "Not initialized. Run: git submodule update --init --recursive",
        }

    committed = _git_text(["ls-tree", "HEAD", "engine/leonida"])
    checked_out = _git_text(["rev-parse", "HEAD"], cwd=ENGINE)
    if not committed or not checked_out:
        return {
            "name": "Engine pin",
            "status": "warning",
            "detail": "Could not compare the root Git link with the checked-out engine commit.",
        }

    parts = committed.split()
    if len(parts) < 3 or parts[0] != "160000" or parts[1] != "commit":
        return {
            "name": "Engine pin",
            "status": "warning",
            "detail": "engine/leonida is not recorded as the expected Git submodule.",
        }
    if parts[2] != checked_out:
        return {
            "name": "Engine pin",
            "status": "warning",
            "detail": f"Checkout {checked_out[:12]} differs from committed pin {parts[2][:12]}.",
        }
    return {
        "name": "Engine pin",
        "status": "ready",
        "detail": f"Exact committed revision {checked_out[:12]} is checked out.",
    }


def collect_checks() -> list[dict[str, str]]:
    """Collect local setup checks without opening or modifying game files."""
    checks: list[dict[str, str]] = []

    checks.append({
        "name": "Engine submodule",
        "status": "ready" if ENGINE_SCRIPT.is_file() else "missing",
        "detail": str(ENGINE_SCRIPT) if ENGINE_SCRIPT.is_file()
        else "Not initialized. Run: git submodule update --init --recursive",
    })
    checks.append(_engine_checkout_check())

    nested_ready = NESTED_ENGINE.is_dir() and any(NESTED_ENGINE.iterdir())
    checks.append({
        "name": "Nested engine dependency",
        "status": "ready" if nested_ready else "missing",
        "detail": str(NESTED_ENGINE) if nested_ready
        else "rpf9-explorer is not initialized. Run: git submodule update --init --recursive",
    })

    current_python = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    checks.append({
        "name": "Python",
        "status": "ready" if sys.version_info[:2] >= MIN_PYTHON else "missing",
        "detail": f"{current_python}; requires Python 3.12+",
    })

    git = shutil.which("git")
    checks.append({
        "name": "Git",
        "status": "ready" if git else "missing",
        "detail": git or "Install Git and ensure it is on PATH.",
    })

    dotnet = shutil.which("dotnet")
    checks.append(_version_check(".NET SDK", [dotnet] if dotnet else ["__missing_dotnet__"], (8, 0, 0)))

    spirv_as = shutil.which("spirv-as")
    spirv_val = shutil.which("spirv-val")
    checks.append({
        "name": "Vulkan SPIR-V tools",
        "status": "ready" if spirv_as and spirv_val else "missing",
        "detail": "spirv-as and spirv-val found" if spirv_as and spirv_val
        else "Install the Vulkan SDK and make spirv-as and spirv-val available on PATH.",
    })

    llvm_command = shlex.split(os.environ.get("LLVM_MC", "llvm-mc"))
    llvm_executable = llvm_command[0] if llvm_command else "llvm-mc"
    if shutil.which(llvm_executable) or Path(llvm_executable).is_file():
        checks.append(_version_check("LLVM llvm-mc (AMDGPU)", llvm_command, (21, 0, 0), "amdgcn"))
    else:
        checks.append({
            "name": "LLVM llvm-mc (AMDGPU)",
            "status": "missing",
            "detail": "Install LLVM 21+ with the AMDGPU target; set LLVM_MC if it is not on PATH.",
        })

    system = platform.system()
    if system == "Windows":
        msvc = shutil.which("cl.exe")
        checks.append({
            "name": "MSVC C++ toolchain",
            "status": "ready" if msvc else "missing",
            "detail": msvc or "Use a Visual Studio 2022 Developer Command Prompt with Desktop C++ and Windows SDK 10.0.26100+.",
        })
    else:
        checks.append({
            "name": "MSVC C++ toolchain",
            "status": "info",
            "detail": "The upstream runtime build targets Windows; non-Windows support is partial and platform-specific.",
        })

    ffmpeg = shutil.which("ffmpeg")
    checks.append({
        "name": "ffmpeg (optional)",
        "status": "optional" if ffmpeg else "info",
        "detail": ffmpeg or "Not installed; only needed for optional audio decoding / WAV conversion.",
    })

    cmake = shutil.which("cmake")
    checks.append({
        "name": "CMake (optional diagnostics)",
        "status": "optional" if cmake else "info",
        "detail": cmake or "Not installed; useful for selected runtime diagnostic/test builds.",
    })

    try:
        free_gib = shutil.disk_usage(ROOT).free / (1024 ** 3)
        if free_gib >= FULL_BUILD_GIB:
            disk_status = "ready"
            disk_detail = f"{free_gib:.1f} GiB free on the repository volume; enough for the upstream full-build estimate."
        elif free_gib >= RUNTIME_BUILD_GIB:
            disk_status = "warning"
            disk_detail = (
                f"{free_gib:.1f} GiB free on the repository volume. Upstream estimates ~30 GiB for "
                "check/shaders/runtime and ~400 GiB for a full build. Select --work and --out on suitable volumes."
            )
        else:
            disk_status = "missing"
            disk_detail = (
                f"{free_gib:.1f} GiB free on the repository volume; less than the upstream ~30 GiB reduced-build "
                "estimate. --work and --out can use other drives."
            )
    except OSError as exc:
        disk_status = "warning"
        disk_detail = f"Could not inspect free space: {exc}"
    checks.append({"name": "Repository volume space", "status": disk_status, "detail": disk_detail})

    checks.append({
        "name": "Platform",
        "status": "info",
        "detail": f"{system} {platform.release()} / {platform.machine()}; see upstream platform notes.",
    })
    return checks


def doctor(json_output: bool = False) -> int:
    checks = collect_checks()
    if json_output:
        print(json.dumps(checks, indent=2, ensure_ascii=False))
    else:
        print(f"{APP_NAME} — local environment diagnostics")
        print("Checks tools and repository state only; it does not open or modify game files.\n")
        for item in checks:
            print(f"[{item['status'].upper():7}] {item['name']}: {item['detail']}")
        missing = sum(item["status"] == "missing" for item in checks)
        warnings = sum(item["status"] == "warning" for item in checks)
        print(f"\n{missing} missing requirement(s), {warnings} warning(s).")
    return 1 if any(item["status"] == "missing" for item in checks) else 0


def status() -> int:
    """Print identity and reproducible upstream metadata."""
    pin = _git_text(["ls-tree", "HEAD", "engine/leonida"])
    parts = pin.split() if pin else []
    revision = parts[2] if len(parts) >= 3 and parts[0] == "160000" else "unknown"
    print(f"{APP_NAME} {APP_VERSION}")
    print(f"Project root: {ROOT}")
    print(f"Engine source: {EXPECTED_ENGINE_URL}")
    print(f"Committed engine pin: {revision}")
    print(f"Engine checkout: {'present' if ENGINE_SCRIPT.is_file() else 'missing'}")
    print(f"Nested dependency: {'present' if NESTED_ENGINE.is_dir() and any(NESTED_ENGINE.iterdir()) else 'missing'}")
    print("Readiness: diagnostics only; no playable game or end-to-end runtime is claimed.")
    return 0 if revision != "unknown" else 1


def verify() -> int:
    script = ROOT / "scripts" / "verify_upstream.py"
    if not script.is_file():
        print("FRAMEZERO: verification script is missing.", file=sys.stderr)
        return 2
    try:
        return subprocess.run([sys.executable, "-I", str(script)], cwd=ROOT, check=False).returncode
    except OSError as exc:
        print(f"FRAMEZERO: could not start repository verification: {exc}", file=sys.stderr)
        return 2


def run_engine(arguments: list[str]) -> int:
    if not ENGINE_SCRIPT.is_file():
        print(
            "FRAMEZERO: engine submodule is missing. Run: git submodule update --init --recursive",
            file=sys.stderr,
        )
        return 2
    if not NESTED_ENGINE.is_dir() or not any(NESTED_ENGINE.iterdir()):
        print(
            "FRAMEZERO: nested engine dependency is missing. Run: git submodule update --init --recursive",
            file=sys.stderr,
        )
        return 2
    command = [sys.executable, "-I", str(ENGINE_SCRIPT), *arguments]
    try:
        return subprocess.run(command, cwd=ENGINE, check=False).returncode
    except OSError as exc:
        print(f"FRAMEZERO: could not start the upstream engine: {exc}", file=sys.stderr)
        return 2


def print_help() -> None:
    print(
        f"{APP_NAME} {APP_VERSION}\n\n"
        "Usage:\n"
        "  python framezero.py doctor [--json]\n"
        "  python framezero.py status\n"
        "  python framezero.py verify\n"
        "  python framezero.py engine-help\n"
        "  python framezero.py build <upstream make_game.py arguments...>\n\n"
        "Examples:\n"
        "  python framezero.py doctor\n"
        "  python framezero.py doctor --json\n"
        "  python framezero.py status\n"
        "  python framezero.py verify\n"
        "  python framezero.py engine-help\n"
        "  python framezero.py build --find\n"
        "  python framezero.py build --check\n\n"
        "The build command forwards its remaining arguments to the pinned upstream engine."
    )


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in {"-h", "--help", "help"}:
        print_help()
        return 0
    if args[0] in {"-V", "--version", "version"}:
        print(f"{APP_NAME} {APP_VERSION}")
        return 0

    command, *remaining = args
    if command == "doctor":
        return doctor(json_output="--json" in remaining)
    if command == "status":
        return status()
    if command == "verify":
        return verify()
    if command == "engine-help":
        return run_engine(["--help"])
    if command == "build":
        return run_engine(remaining)
    print(f"FRAMEZERO: unknown command '{command}'.\n", file=sys.stderr)
    print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
