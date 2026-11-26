# Changelog

Changes are recorded by development milestone. This file does not imply a public binary release.

## 0.2.0-dev — 2026-11-26

### Added
- FRAMEZERO LAB identity, original SVG mark, developer documentation, and public issue templates.
- FRAMEZERO CLI commands for version, status, doctor, and recursive repository verification.
- Cross-platform Python CI for Ubuntu and Windows.
- Security policy and pull request checklist.

### Improved
- Diagnostics now report whether the nested engine dependency is initialized and whether the checked-out engine matches the committed Git link.
- Repository verification checks recursive submodule states, including missing, mismatched, or conflicted links.
- Desktop process handles are created before the Stop control is enabled; stop escalation is bounded.
- Desktop activity output is batched and the visible log is capped to prevent unbounded widget growth.
- Old NOVA entry points remain as compatibility shims.

### Not verified
- No end-to-end engine build or first world frame has been reproduced by FRAMEZERO.
- The desktop GUI has not yet been interactively tested on a clean Windows workstation.
- No standalone installer or executable release is produced by this milestone.
