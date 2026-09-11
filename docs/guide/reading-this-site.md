# Reading this site

## Layers (C4)

| Level | What you get | Where |
|---|---|---|
| Context | FalconX vs external systems (Betfair, clients, ops) | [C4](/c4/) + interactive workspace |
| Containers | Deployable services / data stores | Catalog + C4 container views |
| Components | Important internals (only where it matters) | Selected C4 views + flow pages |
| Code | Implementation | Service repos — not duplicated here |

## Where truth lives

| Kind of truth | Location |
|---|---|
| Architecture narrative & decisions | **This repo** |
| Which repos exist locally / in waves | `Local-dev-setup` → `stack/config/local-repos.txt` |
| What runs in compose | `Local-dev-setup` compose files |
| What runs in AWS | `rfetech-infra` (Terraform), `rfetech-gitops` (Helm/Argo) |
| Per-service ops notes for agents | `Local-dev-setup` → `.claude/context/.../CLAUDE.md` |

## Interactive diagrams

1. Run `npm run c4:dev` for the live LikeC4 UI, or
2. Open [Interactive workspace](/c4/interactive) after `npm run c4:build` (embeds exported site).

Sequence diagrams on flow pages use **Mermaid** and render in VitePress and on GitHub.
