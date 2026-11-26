# Upstream engine pin and status

## Selected repository

FRAMEZERO currently references the active continuation as a Git submodule:

- Repository: https://github.com/ubiquitarianism/leonida
- Path: engine/leonida
- Remote branch used as the deliberate update source: main
- Pinned commit: b9320a118d46b24de665e30e577425c131b4a2ee
- Commit date: 25 November 2026
- Nested dependency: https://github.com/breadbbbb/rpf9-explorer at third_party/rpf9-explorer

The actual engine source revision is recorded by the Git submodule link, not by a mutable branch reference. Do not advance it without review.

## Project lineage and attribution

The upstream README describes the repository as a continuation of NotRexed's Leonida project, with development continued by the current maintainers. Original authorship and contributions remain credited to NotRexed and the contributors in the upstream history. FRAMEZERO is not the upstream maintainer and is not an official continuation.

The submodule preserves the upstream repository and commit history rather than copying that implementation into FRAMEZERO-owned files.

## Upstream status snapshot

At the selected commit, the upstream README reports:

- The game's own executable reaches the world phase after the story load on native Windows and Linux through Proton.
- A first world frame has not been verified on a test machine.
- Story mode and playable gameplay are not reported as available.
- Local package checking for the documented Xbox Series version is reported as working.
- 26,503 RDNA2 shaders are reported as translated to SPIR-V and passing spirv-val.
- The D3D12-to-Vulkan implementation and ray-tracing work remain in progress.

These are upstream-reported claims. FRAMEZERO has not independently reproduced an end-to-end build or verified a first world frame. Recheck the upstream README and history before quoting these figures publicly.

## Nested submodule

The upstream declares third_party/rpf9-explorer in its own .gitmodules. Recursive initialization is required for verification and for workflows that need this dependency:

~~~sh
git submodule update --init --recursive
python framezero.py verify
~~~

## Licence and third-party notices

The selected upstream repository identifies its licence as GNU GPL v3.0. Preserve the upstream licence, notices, source history, and nested dependency licences. Read each current notice before redistributing a combined source archive or binary. See [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md).
