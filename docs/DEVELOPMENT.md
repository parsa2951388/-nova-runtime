# Development and local setup

## 1. Clone the complete source

The engine and one of its dependencies are Git submodules. Clone recursively:

~~~sh
git clone --recurse-submodules https://github.com/parsa2951388/framezero-lab.git
cd framezero-lab
~~~

For an existing checkout:

~~~sh
git submodule update --init --recursive
python framezero.py verify
~~~

## 2. Prerequisites

The pinned upstream README lists:

- A lawfully accessed local package that is already readable on disk, if using an upstream package workflow.
- Windows 10/11 x64 as the primary runtime build environment.
- Python 3.12+.
- .NET 8 SDK.
- Vulkan SDK with spirv-as and spirv-val.
- LLVM 21+ with the AMDGPU target for llvm-mc.
- Visual Studio 2022 with Desktop development with C++ and Windows SDK 10.0.26100+ for the runtime stage.
- ffmpeg optional for selected audio conversions.

See the upstream documentation for current tool versions and platform-specific instructions. FRAMEZERO does not provide game files, keys, or protection circumvention.

## 3. Check the local environment

~~~sh
python framezero.py doctor
python framezero.py status
python framezero.py verify
~~~

The doctor checks tool availability and version information, engine and nested submodule initialization, the exact root Git link, and free space on the repository volume. It does not inspect game packages.

## 4. Desktop console

~~~sh
python framezero_gui.py
~~~

The console provides overview, diagnostics, package validation, build profiles, output streaming, and stop/force-stop controls. Tkinter is part of the Python standard library where the selected Python distribution includes Tk support.

## 5. Delegate upstream commands

~~~sh
python framezero.py engine-help
python framezero.py build --find
python framezero.py build --check
~~~

The remainder of a build command is forwarded to the pinned upstream make_game.py. The upstream README and help output define every accepted option.

## 6. Storage planning

The pinned upstream documentation estimates approximately 30 GiB for its reduced check/shaders/runtime stages and approximately 400 GiB for the full pipeline. Asset export accounts for a substantial portion of the full estimate. These numbers are not guarantees and may change upstream.

Select work and output directories only after checking the capacity of the actual target volumes. The doctor reports the repository volume only; it cannot predict every upstream intermediate file.

## 7. Tests

~~~sh
python -m compileall -q framezero.py framezero_gui.py nova.py nova_gui.py scripts tests
python -m unittest discover -s tests -v
python scripts/verify_upstream.py
python -I scripts/check_no_game_data.py
~~~

The CI workflow repeats Python tests on Linux and Windows and performs recursive submodule and data-integrity checks on Linux.

## 8. Upstream updates

Do not move the engine pin automatically. Review the upstream repository, release notes, commit history, nested dependencies, licence changes, and current project status first. Then update the Git submodule pointer deliberately and update docs/UPSTREAM.md in the same change.

~~~sh
git -C engine/leonida fetch origin main
git -C engine/leonida log --oneline --decorate -10 origin/main
~~~

After review, check out the selected commit, stage the Git link, and open a focused pull request. Never treat a moving branch as a reproducible engine baseline.
