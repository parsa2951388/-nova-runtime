# Architecture notes

> This document records the architecture described by the reviewed Leonida upstream. It is a design reference only: the NOVA repository does not yet contain the runtime implementation.

## End-to-end model

The upstream project describes a local build pipeline that takes an already-readable Xbox Series package supplied by the user and creates PC-side runtime components. The broad flow is:

1. **Local package check** — identify the expected package/version and verify the files available on the user's machine. This stage must not obtain keys, decrypt protected content, or bypass access controls.
2. **Shader pipeline** — carve and disassemble the console's RDNA2 shader programs, translate them to SPIR-V, and validate the generated SPIR-V.
3. **Local asset pipeline** — process models, textures, and audio from the user's package into local working/output directories. Generated assets are user data and must never be committed or distributed by NOVA.
4. **Runtime loader** — load the executable image and resolve the required imports through compatibility shims.
5. **Graphics compatibility layer** — map the console-facing D3D12-style interface to Vulkan-backed operations.
6. **Validation and diagnostics** — run semantic tests, runtime tests, shader/pipeline checks, and GPU-specific diagnostics; report unsupported behavior rather than hiding it.

## Upstream components observed

| Upstream area | Role described by upstream | NOVA status |
|---|---|---|
| `make_game.py` | Build orchestration and local package discovery/checks | Not imported |
| `tools/` | Shader and asset tooling | Not imported |
| `runtime/` | Loader, compatibility shims, Vulkan diagnostics | Not imported |
| `tests/` and `scripts/` | Regression tests and validation runners | Not imported |
| `viewer/` | Local viewer for exported world data | Not imported |
| `third_party/` | External dependencies and submodules | Not imported |

## Platform direction

The upstream README describes Windows as the primary runtime environment, Linux support for several tools and Vulkan diagnostics, and macOS support for selected tools and testing paths. These statements describe the upstream project, not a tested NOVA build.

## Engineering rules

- Keep the runtime and build pipeline deterministic where possible.
- Keep all game-derived data local to the user's machine.
- Never put proprietary game data in tests, fixtures, logs, issues, pull requests, or releases.
- When a format is encrypted or protected, stop; do not add a decryption or circumvention path.
- Preserve upstream author credits, license files, and third-party notices when source is integrated.
- Add tests for behavior changes before changing core translation or runtime semantics.
- Clearly distinguish measured behavior, tested behavior, and hypotheses in documentation.

## Baseline source

- Repository: https://github.com/ExCorvus/leonida
- Reviewed snapshot: `8eee35cfdccc613a1f7a10a5539d5bd3b25038ba`
- License reported by upstream repository: GNU GPL v3.0
