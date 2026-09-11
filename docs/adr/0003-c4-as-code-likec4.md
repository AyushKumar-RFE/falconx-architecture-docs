# ADR 0003 — C4 as code with LikeC4

**Status:** Accepted  
**Date:** 2026-09-11  
**Deciders:** FalconX engineering  

## Context

MkDocs/Docusaurus/VitePress host pages but do not provide an interactive C4 model. Hand-maintained HTML/SVG maps polish well but lag service inventory.

## Decision

Maintain a **LikeC4** model under `/c4`. Engineers explore via `npm run c4:dev` or the exported workspace embedded in the docs site. Mermaid remains for sequence diagrams inside flow/ADR pages.

## Consequences

- Topology changes update the model in git
- CI validates the model
- Learning curve for LikeC4 DSL

## Alternatives considered

| Option | Why not |
|---|---|
| Structurizr DSL | Equally valid; LikeC4 chosen for lightweight local UX |
| Mermaid-only C4 | Weak for multi-view estate navigation |
| Excalidraw / draw.io only | Not reviewable as structured model |
