# NOVA Runtime

**A new identity for an independent PC runtime research project.**

NOVA Runtime is the working brand for a community engineering project exploring a native Windows/Linux PC runtime path for a legally obtained, locally readable Xbox Series game package. Its initial technical reference is the Leonida project.

> [!WARNING]
> **This repository is currently a documentation bootstrap, not a playable port.** The upstream codebase has not yet been imported into this repository. There are no NOVA binaries, installers, launchers, or compatibility claims at this stage.

## Project direction

The aim is to build a clearly branded and maintainable project around the upstream technical foundation, with an independent identity, better onboarding, diagnostics, build orchestration, testing, and eventually a polished desktop experience.

Planned engineering areas:

- Local package validation and reproducible build orchestration.
- RDNA2 shader translation to SPIR-V for Vulkan.
- A PC runtime and console-API compatibility shims.
- Local-only asset processing from the user's own readable files.
- Automated regression tests, GPU diagnostics, and clear compatibility reporting.
- A distinct NOVA setup experience, documentation, and visual identity.

These are project goals, not claims that the features are already implemented here.

## Current status

| Area | Status |
|---|---|
| NOVA project repository | Created |
| Branding and project documentation | Bootstrap in progress |
| Upstream code integration | Not started |
| Reproducible build verification | Not started |
| NOVA runtime executable | Does not exist yet |
| Playable game support | Not available / not claimed |

See [the roadmap](docs/ROADMAP.md) and [architecture notes](docs/ARCHITECTURE.md).

## Technical starting point and attribution

The initial technical reference is [ExCorvus/leonida](https://github.com/ExCorvus/leonida), a continuation/mirror in the Leonida project lineage. The original project is credited to **NotRexed and its contributors**; the continuation is associated with **ubiquitarianism**. The reviewed ExCorvus snapshot is:

- Repository: https://github.com/ExCorvus/leonida
- Reviewed commit: [`8eee35cfdccc`](https://github.com/ExCorvus/leonida/commit/8eee35cfdccc613a1f7a10a5539d5bd3b25038ba)
- License identified by the upstream repository: **GNU GPL v3.0**

No upstream source files have been copied into this bootstrap commit. When upstream code is integrated, its copyright notices, license terms, and third-party notices must be retained. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Non-negotiable data and safety rules

- Use only a game copy and files that the user is legally entitled to access and that are already readable locally.
- Do not provide, download, distribute, or commit game executables, archives, keys, decrypted files, extracted assets, generated game shaders, saves, or other proprietary game data.
- Do not implement key extraction, decryption, DRM circumvention, or protection bypasses. If a required input is protected or encrypted, stop and document the limitation.
- Do not connect to Xbox Live, Rockstar services, or other game services.
- Keep generated assets, build output, logs, and user data on the user's machine.

These rules follow the upstream project's documented contributor constraints and are repeated here so they remain explicit in the NOVA repository.

## License

This repository includes the GNU General Public License v3.0 text as the intended license baseline for the project. Any imported or adapted upstream code remains subject to its applicable notices and license. See [LICENSE](LICENSE).

## Disclaimer

NOVA Runtime is an independent, unofficial community project. It is not affiliated with, endorsed by, or sponsored by Rockstar Games, Take-Two Interactive, Microsoft, or Xbox. All product names and trademarks belong to their respective owners.
