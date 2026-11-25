# NOVA Runtime

**An independent identity and developer experience for a PC runtime research project.**

NOVA Runtime is being built around the open-source Leonida engine lineage. NOVA keeps its own documentation, command-line entry point, engineering roadmap, and future user experience separate from the upstream engine.

> [!WARNING]
> **NOVA is not a playable game or finished port.** The engine is pinned as a Git submodule. NOVA has not yet produced or verified its own end-to-end build.

## Repository layout

- `engine/leonida/` — canonical upstream engine, pinned as a Git submodule.
- `nova.py` — NOVA command-line front end. It checks the local toolchain and delegates engine operations without silently modifying upstream behavior.
- `docs/` — NOVA architecture, development instructions, roadmap, and upstream pin.
- `tests/` — tests for NOVA-owned tooling.
- `THIRD_PARTY_NOTICES.md` and `LICENSE` — provenance and license information.

Clone with submodules so the engine is present:

```sh
git clone --recurse-submodules https://github.com/parsa2951388/-nova-runtime.git
cd -nova-runtime
python nova.py doctor
```

If the repository was cloned without submodules:

```sh
git submodule update --init --recursive
```

## First commands

```sh
python nova.py doctor          # inspect local prerequisites and available disk space
python nova.py engine-help     # show the pinned engine's command-line help
python nova.py build --find    # ask the engine to look for a local game package
python nova.py build --check   # validate a package; do not build
```

The `build` command forwards its remaining arguments to the pinned upstream `make_game.py`. The engine's own documentation remains authoritative for all build flags.

## Verified upstream baseline

NOVA currently pins [ubiquitarianism/leonida](https://github.com/ubiquitarianism/leonida) at commit [`b9320a118d46`](https://github.com/ubiquitarianism/leonida/commit/b9320a118d46b24de665e30e577425c131b4a2ee), dated **25 November 2026**. This is the active continuation; the previously reviewed `ExCorvus/leonida` repository is an older mirror and is not the pinned source.

The upstream README at that commit reports that the game reaches the world phase after the story load on native Windows and Linux/Proton, but **a first world frame has not been verified**. Story mode is not reported as playable. This is upstream-reported status, not a NOVA test result. See [UPSTREAM.md](docs/UPSTREAM.md).

## Build prerequisites and storage

The upstream currently documents Windows 10/11 x64 as its primary build environment, Python 3.12+, .NET 8 SDK, Vulkan SDK tools (`spirv-as` and `spirv-val`), LLVM 21+ with the AMDGPU target for `llvm-mc`, and Visual Studio 2022 with Desktop C++ tools and Windows SDK 10.0.26100 or newer.

The upstream estimates about **400 GiB** of work space for a full build. Its reduced `check,shaders,runtime` path is estimated at about **30 GiB**; the asset-export stage accounts for roughly another **370 GiB**. Work and output directories can be placed on separate drives. Review [DEVELOPMENT.md](docs/DEVELOPMENT.md) and the upstream README before starting a build.

## Project rules

- Use only a game package the user is legally entitled to access and that is already readable locally.
- Never commit or distribute game executables, archives, keys, extracted assets, generated shaders, saves, or other proprietary game data.
- Do not implement key extraction, decryption, DRM circumvention, or protection bypasses. Stop and document the limitation if a required input is protected.
- Keep local build products, logs, and generated assets outside version control.
- Preserve upstream attribution, GPL notices, submodule provenance, and third-party licenses.
- Distinguish upstream-reported functionality from functionality NOVA has actually built and tested.

## License and attribution

The upstream engine is distributed under **GNU GPL v3.0**. The license text and project lineage are preserved here. NOVA's own additions are developed within that license baseline; upstream authorship is not claimed as NOVA authorship. See [LICENSE](LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

NOVA is an independent, unofficial community project. It is not affiliated with or endorsed by Rockstar Games, Take-Two Interactive, Microsoft, or Xbox. Product names and trademarks belong to their respective owners.
