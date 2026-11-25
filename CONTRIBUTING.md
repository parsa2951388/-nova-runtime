# Contributing to NOVA Runtime

## Scope

NOVA-owned code and documentation live in this repository. The original engine lives in the pinned `engine/leonida` Git submodule. Keep the boundary explicit:

- NOVA CLI, setup experience, documentation, tests, and project automation are NOVA-owned.
- Engine translation, package parsing, runtime loading, and graphics compatibility remain upstream responsibilities unless a separately reviewed patch is proposed.
- Do not silently edit the engine and then represent the result as an ordinary NOVA-only change.

## Safety and data rules

- Never commit game packages, executables, keys, extracted assets, generated shaders, textures, audio, models, videos, saves, logs that quote game data, or other proprietary game content.
- Never add key extraction, decryption, DRM circumvention, or protection-bypass logic.
- Work only with files already readable locally and a package the user is legally entitled to access.
- Do not connect to Xbox Live, Rockstar services, or other game services.
- Keep build outputs, logs, and generated assets outside version control.
- Run both data scans before proposing a change:
  - `python -I scripts/check_no_game_data.py` for NOVA-owned tracked files.
  - `python -I scripts/check_no_game_data.py` from `engine/leonida` for the pinned engine checkout.

## Change process

1. Keep each pull request focused on one change.
2. Update tests and documentation with behavior changes.
3. Run `python -m unittest discover -s tests -v
python -m compileall -q nova.py nova_gui.py scripts tests`.
4. Run `python scripts/verify_upstream.py` after submodule changes.
5. For an upstream pin update, review the intervening commits, source status, nested dependencies, and licenses before moving the gitlink.
6. Record exactly what was tested. Do not label upstream-reported behavior as NOVA-tested.
7. Preserve GPL-3.0 and all upstream/third-party copyright and attribution notices.

## Upstream contributions

The engine submodule is pinned to an external repository. Do not attempt to push directly to that upstream unless the relevant maintainer has explicitly granted access. Engine changes should be developed against an authorized fork or submitted through the upstream project's contribution process, with source authorship preserved.
