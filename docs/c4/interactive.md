# Interactive C4 workspace

## On the shared website (team)

Open:

**https://ayushkumar-rfe.github.io/falconx-architecture-docs/c4-workspace/**

(or nav **Open diagrams**)

### How to use

1. You land on the **hub** with 4 cards — click one to open that diagram.
2. **Scroll / drag** the canvas; use **+ / − / fit** (bottom-left) to zoom.
3. **Hover / click** a box to read its description; arrows are relationships (labelled).
4. Use **Search (⌘K)** to jump to a service by name.
5. **Export** (top-right) to save an image for a PR/chat.
6. Top-left **back** returns to the hub.

| Card | What it answers |
|---|---|
| System context | Who/what talks to FalconX from outside? |
| Containers | What services exist inside FalconX? |
| Money path | How does place-bet → settle flow? |
| Odds & catalogue | How do odds / catalogue get into FrontMarket? |

### How to read icons / AWS runtime

| Look | Means |
|---|---|
| **EKS icon** (or `· EKS` in technology) | App/API/worker on Kubernetes |
| **Lambda icon** (amber box) | AWS Lambda (settlement); LocalStack locally |
| **Aurora / cylinder** | Amazon Aurora PostgreSQL |
| **ElastiCache** | Valkey/Redis cache + pub/sub |
| **MSK / queue** | Amazon MSK (Kafka) |
| **Amber dotted arrow** | Poll / sync loop (not push). Exact interval lives in that service’s config — put e.g. `polls every 2s` on the edge once you confirm it. |

Note: `/c4/` on the docs site is only written help — not the interactive app.

## Local (authors)

```bash
npm install
npm run c4:dev          # live editor while changing model.c4
npm run build           # embeds workspace into the docs site
```

Model source: `c4/model.c4`. CI rebuilds the hosted workspace on merge to `main`.

GitHub Pages needs **hash URLs** (`#/view/...`) so diagram links work — set in `npm run c4:build` via `--use-hash-history`.
