# NOVA Runtime architecture

## Repository boundary

NOVA keeps its own user-facing layer at the repository root and pins the upstream implementation at:

- Path: `engine/leonida/`
- Remote: https://github.com/ubiquitarianism/leonida.git
- Pinned commit: `b9320a118d46b24de665e30e577425c131b4a2ee`
- Branch used for future upstream updates: `main`

The submodule preserves the upstream repository's own commit history and attribution. Do not copy the engine into a second source tree or change its pinned revision without updating [UPSTREAM.md](UPSTREAM.md), the submodule pointer, and the roadmap.

## NOVA-owned layer

`nova.py` is a deliberately thin Python front end:

1. `doctor` reports whether the local tools, engine checkout, and disk budget meet the documented prerequisites.
2. `engine-help` shows the pinned engine's own help.
3. `build` forwards the supplied arguments to `engine/leonida/make_game.py` using the current Python interpreter and isolated mode.

The wrapper must not reimplement shader translation, package parsing, runtime loading, or graphics compatibility. Those remain upstream engine responsibilities unless a separately reviewed NOVA patch is introduced.

## Upstream engine pipeline

As documented by the pinned upstream revision, the broad pipeline is:

1. **Local package check** — identify and validate the expected package/version already readable on the user's machine.
2. **Shader pipeline** — carve and disassemble RDNA2 programs, translate them to SPIR-V, and validate the result.
3. **Local asset processing** — process models, textures, and audio from the local package into working/output folders.
4. **Runtime loader** — load the executable image and resolve imports through compatibility shims.
5. **Graphics compatibility** — map the console-facing D3D12-style interface to Vulkan-backed operations.
6. **Testing and diagnostics** — semantic regression tests, runtime tests, shader/pipeline checks, and GPU-specific diagnostics.

These are upstream architectural responsibilities. Their presence in the submodule is not evidence that NOVA has reproduced or validated the complete pipeline.

## External dependency

The upstream repository declares `third_party/rpf9-explorer` as a nested Git submodule. Always use recursive submodule initialization:

```sh
git submodule update --init --recursive
```

## Data boundary

- Game packages and all files generated from them stay on the user's machine.
- No game archives, executable, keys, shader binaries, textures, models, audio, videos, saves, or reports quoting game data may enter commits, issues, pull requests, tests, or releases.
- If a required format is encrypted or protected, document that limitation and stop.
- No connection to Xbox Live, Rockstar services, or other game services is part of this project.

## Evidence standard

NOVA documentation must label each result as one of:

- **Upstream-reported** — stated by the pinned upstream project.
- **NOVA-tested** — reproduced from a documented NOVA checkout and toolchain.
- **Hypothesis** — not yet measured or verified.

Never turn an upstream claim into a NOVA test result by rewording it.
