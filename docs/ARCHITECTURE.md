# FRAMEZERO LAB architecture

## Purpose

FRAMEZERO is a developer workbench for local runtime and graphics-compatibility research. It owns diagnostics, orchestration, a desktop setup experience, tests, documentation, and repository-integrity checks. It does not claim to be an independent implementation of the upstream game engine.

## Repository boundaries

- FRAMEZERO-owned files: **framezero.py**, **framezero_gui.py**, **scripts/**, **tests/**, **docs/**, assets, and repository automation.
- External engine dependency: **engine/leonida/**, pinned as a Git submodule at the exact commit recorded in the root Git tree.
- Nested dependency: **engine/leonida/third_party/rpf9-explorer**, also initialized recursively through Git.

The submodule preserves the upstream repository's commit history, licence, authorship, and notices. Do not copy the engine into another source tree or represent upstream implementation as FRAMEZERO-authored work.

## FRAMEZERO command path

1. **status** reports the local project identity, committed engine pin, and initialization state.
2. **doctor** checks local tools, versions, submodules, and repository-volume capacity.
3. **verify** validates the engine Git link, expected remotes, and every recursive submodule state.
4. **engine-help** and **build** invoke the pinned upstream make_game.py through the current Python interpreter in isolated mode.
5. The desktop console calls the same CLI; it does not duplicate engine behavior.

The command wrapper must not reimplement package parsing, shader translation, runtime loading, or graphics compatibility. Those are external-engine responsibilities unless a separately reviewed, lawful, and technically justified implementation is developed.

## Desktop process model

The Tk main thread owns widget state and the child-process handle. It creates the process before enabling the Stop control, preventing a race where the user could request cancellation before the process handle existed. A worker thread reads stdout and sends events through a thread-safe queue. The Tk event loop alone updates widgets. Stop sends a normal termination request and schedules a bounded forced-stop check.

No GUI worker thread may mutate Tk widgets directly.

## Upstream pipeline context

The pinned engine describes the following broad responsibilities:

1. Local package identification and validation.
2. RDNA2 shader disassembly and SPIR-V translation/validation.
3. Local processing of models, textures, and audio.
4. Executable loading and import shims.
5. Console-facing graphics compatibility through Vulkan.
6. Runtime, shader, and GPU-specific testing.

The list describes upstream architecture, not independently verified FRAMEZERO capabilities.

## Data boundary

- User-owned game packages and generated outputs remain local.
- Never commit or distribute game archives, executables, keys, extracted assets, generated shaders, textures, models, audio, video, saves, or proprietary logs.
- Never implement key extraction, decryption, protection bypass, or DRM circumvention.
- Do not connect to Xbox Live, Rockstar services, or any game service.
- If a required input is protected or unavailable through lawful means, document the limitation and stop.

## Evidence labels

All reports and status pages must distinguish:

- **FRAMEZERO-tested** — reproduced by this repository's tests or documented local run.
- **Upstream-reported** — stated by the external engine maintainers.
- **Unverified** — not yet measured.

Never reword an upstream claim as a FRAMEZERO test result.
