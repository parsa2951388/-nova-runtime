# Contributing to FRAMEZERO LAB

## Scope

FRAMEZERO-owned code includes the CLI, desktop console, diagnostics, tests, documentation, and repository automation. The engine remains in the external engine/leonida Git submodule. Preserve that boundary.

## Safety and data rules

- Do not commit game packages, executables, keys, extracted assets, generated shaders, textures, audio, models, videos, saves, proprietary logs, or other game content.
- Do not add key extraction, decryption, DRM circumvention, or protection-bypass logic.
- Use only files that the user is legally entitled to access and that are already readable locally.
- Do not connect to Xbox Live, Rockstar services, or game services.
- Keep local build products and generated assets outside version control.
- Preserve GPL-3.0 and all upstream and third-party notices.

## Change process

1. Keep pull requests focused and explain the engineering reason.
2. Add or update tests for behavioral changes.
3. Run compile checks and the unit-test suite.
4. Run python scripts/verify_upstream.py after submodule changes.
5. Run the root and upstream data-integrity scans.
6. Record exactly what was tested. Do not label upstream-reported behavior as FRAMEZERO-tested.
7. Do not move the upstream pin without reviewing commits, nested dependencies, licences, and status.

## Upstream contributions

Do not push directly to the upstream repository without explicit maintainer authorization. Develop against an authorized fork or submit generally useful fixes through the upstream contribution process, retaining source authorship and notices.
