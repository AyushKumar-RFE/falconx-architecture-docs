# Tooling

| Job | Tool | Notes |
|---|---|---|
| Docs site | **VitePress** | Markdown → searchable static site (`npm run docs:dev`) |
| Interactive C4 | **LikeC4** | Model in `/c4`; `npm run c4:dev` / `c4:build` |
| Sequences in flows/ADRs | **Mermaid** | Renders in VitePress; also on GitHub |
| Decisions | **ADRs** (Markdown) | See [template](/adr/template) |

## Why VitePress + LikeC4?

VitePress hosts the narrative. LikeC4 runs the interactive C4 model. Mermaid covers sequence diagrams inside flow pages.

## CI

`.github/workflows/docs.yml` validates the LikeC4 model and builds the site on every PR.
