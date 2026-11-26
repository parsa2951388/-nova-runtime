# Third-party notices and project lineage

## Leonida engine

FRAMEZERO references the upstream engine through a Git submodule at engine/leonida:

- Active continuation: https://github.com/ubiquitarianism/leonida
- Pinned commit: https://github.com/ubiquitarianism/leonida/commit/b9320a118d46b24de665e30e577425c131b4a2ee
- Original project: https://github.com/ItsNotRexed/Leonida
- Earlier mirror reviewed during bootstrap: https://github.com/ExCorvus/leonida

The upstream README identifies the project as a continuation of NotRexed's Leonida project. Credit for the original work and the commit history belongs to NotRexed and the upstream contributors. The current continuation is maintained under the ubiquitarianism GitHub account. FRAMEZERO does not claim authorship or maintainership of that engine.

The pinned upstream repository identifies its licence as GNU GPL v3.0. This repository retains the GPL-3.0 baseline and a copy of the licence text. Consult the current upstream licence and notices before redistributing source or binaries.

## Nested dependencies

The upstream engine declares third_party/rpf9-explorer as a nested Git submodule at https://github.com/breadbbbb/rpf9-explorer. Its own licence and notices remain in that repository. Initialize recursive submodules and consult the nested project's current licence before redistribution.

## FRAMEZERO-owned additions

FRAMEZERO's CLI, desktop console, diagnostics, documentation, tests, and brand assets are separate additions, maintained under this repository's GPL-3.0 baseline. Additional third-party notices must be added whenever new dependencies are introduced.

## Trademarks and affiliation

FRAMEZERO LAB is an independent, unofficial research workbench. It is not affiliated with or endorsed by Rockstar Games, Take-Two Interactive, Microsoft, Xbox, NotRexed, or the upstream Leonida maintainers. Product names and trademarks belong to their respective owners.
