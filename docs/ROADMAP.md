# NOVA Runtime roadmap

A stage is complete only when its evidence is recorded. Upstream functionality is not automatically a NOVA test result.

## Stage 0 — Repository bootstrap

- [x] Establish the NOVA Runtime identity and scope.
- [x] Record project lineage and GPL-3.0 baseline.
- [x] Document local-only data handling and protection boundaries.
- [x] Record the initial repository state accurately.

## Stage 1 — Engine integration

- [x] Select the active continuation repository, not the older ExCorvus mirror.
- [x] Pin an exact upstream commit.
- [x] Add the engine as `engine/leonida` Git submodule, retaining the original repository and history.
- [x] Record nested submodule requirements and update procedure.
- [ ] Clone the repository recursively in a clean environment and verify every submodule resolves.
- [ ] Run the upstream no-game-data scanner against the pinned engine checkout.
- [ ] Audit dependency, workflow, and build behavior before NOVA-specific engine patches.

## Stage 2 — NOVA developer entry point

- [x] Add the NOVA CLI with `doctor`, `engine-help`, and `build` forwarding.
- [x] Add unit tests for version parsing and toolchain checks.
- [x] Add CI checks for the submodule pin and upstream data scanner.
- [ ] Run CI on GitHub and fix any failures.
- [ ] Reproduce the documented upstream build prerequisites on a clean Windows machine.
- [ ] Record build commands, exact tool versions, hardware, GPU, and driver.

## Stage 3 — NOVA experience

- [x] Define the first NOVA visual identity, wordmark, palette, and usage guide.
- [ ] Create the NOVA setup and first-run experience without changing upstream engine semantics.
- [ ] Add a clearer compatibility report and diagnostics bundle.
- [ ] Add resumable setup guidance and storage planning for separate work/output drives.
- [ ] Add accessible interface design and localization strategy.
- [ ] Add regression tests for every NOVA-owned feature.

## Stage 4 — Engineering changes

- [ ] Identify a narrow, testable upstream improvement and verify it is not already claimed upstream.
- [ ] Keep NOVA patches isolated from upstream code where possible.
- [ ] Add regression tests and measurable evidence for each change.
- [ ] Submit upstream fixes when they are generally useful and compatible with upstream contribution rules.

## Stage 5 — Release readiness

- [ ] Reproduce an end-to-end run on supported hardware.
- [ ] Document known limitations and compatibility by GPU/driver.
- [ ] Verify all license and third-party notices in source archives and releases.
- [ ] Ensure releases contain no proprietary game files, keys, extracted assets, or saves.
- [ ] Publish only claims supported by repeatable tests.

## Release gate

NOVA must not be described as playable or production-ready until an end-to-end run has been reproduced and documented. The currently pinned upstream revision reports reaching the world phase but does not report a verified first world frame or playable story mode.
