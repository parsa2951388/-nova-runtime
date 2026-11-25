# Upstream engine pin

## Selected repository

NOVA uses the active continuation repository:

- URL: https://github.com/ubiquitarianism/leonida
- Submodule path: `engine/leonida`
- Remote branch used as the update source: `main`
- Pinned commit: `b9320a118d46b24de665e30e577425c131b4a2ee`
- Commit date: 2026-11-25 17:36:10 UTC
- Commit message: `Merge pull request #1812 ... tools: harden bcpack-bptc safety`
- GitHub signature verification: verified

The earlier `ExCorvus/leonida` repository was a mirror/fork with an older snapshot. NOVA uses the active continuation so new work is based on the current code and status, not the earlier copy.

## Submodule structure

The root `.gitmodules` maps `engine/leonida` to the repository above and tracks `main` for deliberate future updates. The actual checked-out commit is pinned by the Git gitlink in this repository. The upstream itself contains a nested submodule:

- `engine/leonida/third_party/rpf9-explorer`

Use `git clone --recurse-submodules` or `git submodule update --init --recursive`.

## Upstream status snapshot

The upstream README at the pinned commit reports:

- The game's own executable reaches the world phase after the story load on native Windows and Linux through Proton.
- A first world frame has **not** been verified on a test machine.
- Story mode and playable gameplay are **not** reported as available.
- The local package check for Xbox Series version 1.0.2.1 works.
- 26,503 RDNA2 shaders have been translated to SPIR-V and reported as passing `spirv-val`.
- The D3D12-to-Vulkan implementation and ray-tracing work remain in progress.

This is a snapshot of upstream-reported status, not a result independently reproduced by NOVA. Recheck the upstream README and commit history when updating this file.

## License and attribution

The selected upstream repository identifies its license as **GNU GPL v3.0**. The source remains in its original repository via a Git submodule; its history, authorship, license, and notices must not be removed. See [LICENSE](../LICENSE) and [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md).
