# FRAMEZERO LAB roadmap

A milestone is complete only when there is repeatable evidence. An upstream capability is not automatically a FRAMEZERO result.

## Stage 0 — Project foundation

- [x] Establish FRAMEZERO identity, scope, and project boundaries.
- [x] Preserve GPL-3.0 baseline and upstream provenance.
- [x] Record the exact external engine pin and nested dependency.
- [x] Add a local-first project and data policy.

## Stage 1 — Reproducible integration

- [x] Pin the external engine as a Git submodule.
- [x] Preserve upstream history and attribution.
- [x] Add recursive submodule verification.
- [x] Distinguish upstream status from FRAMEZERO-tested status.

## Stage 2 — Developer tooling

- [x] Add the FRAMEZERO CLI and compatibility aliases for existing NOVA shortcuts.
- [x] Add toolchain and storage diagnostics.
- [x] Check the nested engine dependency and exact committed engine pin.
- [x] Add status and verification commands.
- [x] Add desktop diagnostics, package validation, build profiles, and output streaming.
- [x] Fix process-handle initialization and safe stop escalation in the desktop console.
- [x] Add unit tests and Linux/Windows CI.
- [ ] Test the console interactively on a clean Windows installation.
- [ ] Add exportable diagnostics that omit private paths and proprietary content by default.

## Stage 3 — Independent research prototypes

- [ ] Build a clean-room x86-64 test harness using original synthetic programs.
- [ ] Add a minimal loader test suite for owned test binaries.
- [ ] Add a Vulkan graphics test application with original assets and test shaders.
- [ ] Add input-device and controller compatibility tests.
- [ ] Publish reproducible benchmarks and GPU/driver test matrices.
- [ ] Add crash-report minimization using synthetic fixtures only.

## Stage 4 — Research quality

- [ ] Add deterministic regression fixtures and CI artifact summaries.
- [ ] Add structured compatibility reports with explicit evidence labels.
- [ ] Document performance and correctness limits by GPU and driver.
- [ ] Submit generally useful upstream fixes through the maintainers' contribution process where appropriate.

## Stage 5 — Release readiness

- [ ] Reproduce an end-to-end research prototype on supported hardware.
- [ ] Validate source archives, licences, and third-party notices.
- [ ] Ensure releases contain no proprietary game data, keys, or generated assets.
- [ ] Publish binaries only after clean-machine testing and a documented bill of materials.
- [ ] Publish claims only when supported by repeatable tests.

## Release gate

FRAMEZERO must not be described as a playable game or production-ready console-to-PC port until a lawful, independently reproducible end-to-end result exists. The current upstream snapshot does not report playable gameplay or a verified first world frame.
