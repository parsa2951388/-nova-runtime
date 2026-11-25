# Third-party notices and project lineage

## Leonida engine

NOVA Runtime currently includes the upstream engine as a Git submodule at `engine/leonida`:

- Active continuation: https://github.com/ubiquitarianism/leonida
- Pinned commit: https://github.com/ubiquitarianism/leonida/commit/b9320a118d46b24de665e30e577425c131b4a2ee
- Original project: https://github.com/ItsNotRexed/Leonida
- Earlier mirror reviewed during bootstrap: https://github.com/ExCorvus/leonida

The original project is credited to **NotRexed and its contributors**. The active continuation is maintained under the **ubiquitarianism** GitHub account. The upstream README describes the work as a continuation of the original Leonida project.

The pinned engine repository reports the **GNU General Public License v3.0**. The full license text is included in this repository as `LICENSE`. The submodule retains its own source history, copyright notices, and third-party files. NOVA does not claim authorship of upstream code.

## Nested dependencies

The upstream engine declares `third_party/rpf9-explorer` as a nested Git submodule. Its own license and notices are maintained in that repository. Initialize submodules recursively and consult the nested project's license before redistributing a combined source archive or binary.

## NOVA-owned additions

The NOVA CLI, documentation, tests, and future user-facing layer are separate additions. They are maintained within the repository's GPL-3.0 license baseline. More dependency notices will be added as additional components are introduced.
