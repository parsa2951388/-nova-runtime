# Development and local setup

## 1. Clone the complete source

The engine and one of its dependencies are Git submodules. Use a recursive clone:

```sh
git clone --recurse-submodules https://github.com/parsa2951388/-nova-runtime.git
cd -nova-runtime
```

For an existing checkout:

```sh
git submodule update --init --recursive
```

Confirm the pinned engine revision:

```sh
python scripts/verify_upstream.py
```

## 2. Prerequisites documented by upstream

The upstream README currently documents:

- Your own Xbox Series package, version 1.0.2.1, with files already readable on disk.
- Windows 10/11 x64 as the primary build environment.
- Python 3.12 or newer.
- .NET 8 SDK.
- Vulkan SDK, including `spirv-as` and `spirv-val`.
- LLVM 21 or newer with the AMDGPU target for `llvm-mc`. The official Windows LLVM build does not include this target; upstream documents a build helper, a conda-forge package, or a WSL installation.
- Visual Studio 2022 with the Desktop development with C++ workload and Windows SDK 10.0.26100 or newer for the runtime stage.
- `ffmpeg` is optional for ordinary audio export, but required for the optional WAV conversion.

The upstream reports that some tools and diagnostics also work on Linux and macOS; that is not equivalent to full native runtime support. Follow the platform-specific upstream documentation.

## 3. Check the machine

```sh
python nova.py doctor
```

The doctor is a local toolchain check. It does not locate, open, inspect, or modify game files.

## 4. Use the engine through NOVA

```sh
python nova.py engine-help
python nova.py build --find
python nova.py build --pick
python nova.py build --check
```

To pass a full explicit build command, the remainder of the command is forwarded unchanged:

```powershell
python nova.py build --game "D:\path\to\your\package" --out "D:\Games\NOVA" --work "E:\nova-work"
```

All supported flags and stage behavior are defined by the pinned upstream `make_game.py` and README. NOVA does not override them.

## 5. Storage planning

The upstream estimates approximately:

- **400 GiB** of work space for the full build.
- **30 GiB** for the reduced `check,shaders,runtime` stages.
- Around **370 GiB** for the optional asset-export stage.

The `--work` and `--out` paths can be placed on drives separate from the package. Check the upstream README for its current storage layout before starting; the space estimate is an upstream measurement, not a guarantee for every machine.

## 6. Tests

NOVA-owned tests:

```sh
python -m unittest discover -s tests -v
python scripts/verify_upstream.py
```

The upstream documents its own test commands in `engine/leonida/AGENTS.md` and `engine/leonida/CONTRIBUTING.md`. Run those from the upstream submodule directory. Do not commit game data or files generated from a local game package.

## 7. Upstream updates

The submodule is pinned to a specific commit. To review a newer upstream main revision:

```sh
git -C engine/leonida fetch origin main
git -C engine/leonida log --oneline --decorate -10 origin/main
```

After reviewing the changes and verifying compatibility, update the submodule pointer deliberately:

```sh
git -C engine/leonida checkout <reviewed-commit>
git add engine/leonida
git commit -m "build: update pinned Leonida engine"
```

Update [UPSTREAM.md](UPSTREAM.md) with the new commit and status snapshot in the same change. Never use an unreviewed moving branch as the project's reproducible engine baseline.
