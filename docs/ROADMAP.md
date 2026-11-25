# NOVA Runtime roadmap

This roadmap is staged. A stage is not complete until its evidence and tests are recorded.

## Stage 0 — Repository bootstrap

- [x] Establish the NOVA Runtime identity and project scope.
- [x] Record the upstream lineage and license baseline.
- [x] Document data-handling and protection boundaries.
- [x] Record the current state honestly: no imported code and no playable build.

## Stage 1 — Source integration

- [ ] Select and pin an exact upstream revision.
- [ ] Import source without losing existing authorship and commit attribution where technically possible.
- [ ] Preserve the upstream license, copyright notices, submodule declarations, and third-party notices.
- [ ] Audit the imported tree for game data, generated assets, binaries, secrets, and unsafe network behavior.
- [ ] Establish a repeatable update procedure for upstream changes.

## Stage 2 — Baseline reproduction

- [ ] Identify prerequisites and supported build environments.
- [ ] Run source-level compile, unit, semantic, and runtime tests that do not require proprietary game data.
- [ ] Record toolchain versions and exact commands.
- [ ] Verify that no game-derived artifacts are present in the repository.
- [ ] Produce a reproducible status report before making functional changes.

## Stage 3 — NOVA-specific engineering

- [ ] Add NOVA branding to project metadata, documentation, setup flow, and user-facing diagnostics.
- [ ] Keep brand/UI changes separated from low-level translation and runtime semantics.
- [ ] Improve setup validation, error messages, resumable builds, and diagnostic bundles.
- [ ] Add a compatibility matrix based on actual test evidence.
- [ ] Add regression tests for every core behavior change.

## Stage 4 — Packaging and release readiness

- [ ] Define a clean build and packaging process.
- [ ] Ensure releases contain only project code and permitted dependencies—not game files, extracted assets, keys, or saves.
- [ ] Verify license and third-party notices in source archives and releases.
- [ ] Run security and dependency checks.
- [ ] Publish only when supported functionality and limitations are accurately documented.

## Release gate

NOVA must not be described as playable or production-ready until an end-to-end run has been independently reproduced and its results, hardware, driver, and known limitations are documented. No release date is promised.
