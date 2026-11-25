# NOVA visual identity

## Brand idea

**NOVA Runtime** is presented as a precise engineering tool: restrained, high-contrast, technical, and readable. The identity uses an orbital mark with an angular N, suggesting a system core, a stable orbit, and a point of ignition. It is an original NOVA mark and does not use game, publisher, or console logos.

## Primary palette

| Token | Hex | Use |
|---|---|---|
| Midnight | `#0B1020` | Main application background |
| Carbon | `#141C2E` | Panels and surfaces |
| Ion Cyan | `#45D6FF` | Primary action, active state, technical highlight |
| Plasma Violet | `#8B7CFF` | Secondary accent, data visualization |
| Solar Amber | `#FFCA78` | Caution, important status, limited accent |
| Ice White | `#F2F6FF` | Primary text on dark surfaces |
| Slate | `#9AA8BE` | Secondary text and metadata |

Use Ice White for body text and Ion Cyan for active controls. Do not use cyan or violet for long paragraphs. Reserve Solar Amber for meaningful warnings rather than decoration.

## Typography

Use system fonts; do not bundle fonts:

- Windows: Segoe UI
- macOS: SF Pro / system sans-serif
- Linux: system sans-serif / Inter when installed
- Android: Roboto

Use tabular numerals for timers, measurements, versions, and diagnostic output.

## Logo use

- Use `assets/nova-mark.svg` on dark or transparent backgrounds.
- Preserve its aspect ratio and clear space.
- Do not recolor individual pieces or add glow, bevel, or 3D effects.
- On light backgrounds, place the mark on a dark surface rather than changing the wordmark to an untested color.
- The mark is a brand asset, not an indication of product readiness or official affiliation.

## Interface principles

1. **Evidence first:** every compatibility or readiness status must explain what was checked.
2. **Readable diagnostics:** show the missing tool, detected version, requirement, and next action.
3. **No false green states:** distinguish detected, tested, upstream-reported, and unsupported.
4. **Progressive disclosure:** keep common setup actions visible and advanced build flags accessible without overwhelming the first screen.
5. **Local-first:** package paths, logs, generated assets, and saves remain on the user's device.

## Prohibited presentation

Do not imply endorsement by Rockstar Games, Take-Two Interactive, Microsoft, or Xbox. Do not reuse Leonida branding as if it were NOVA's own work. Upstream attribution must remain visible wherever upstream code is bundled or referenced.
