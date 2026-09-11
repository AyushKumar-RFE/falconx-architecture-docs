# How to use this site

This repo is the **architecture SSOT**. You read it two ways: the **docs site** (pages) and the **C4 workspace** (interactive diagrams).

## 1. One-time setup

```bash
cd falconx-architecture-docs   # or: git clone https://github.com/AyushKumar-RFE/falconx-architecture-docs.git
npm install
```

Needs **Node.js 20+**.

## 2. Read the docs (pages + Mermaid diagrams)

```bash
npm run docs:dev
```

Open **`http://localhost:5173`** in your browser.

| Area | What you get |
|---|---|
| **Catalog** | Every service / library |
| **Flows** | Sequence diagrams (Mermaid) for bet → settle, odds, catalogue |
| **Infra** | Envs, stores, deploy, local stack |
| **ADRs** | Decisions the team must follow |
| **Guide** | How we decide and update docs |

Use the **search** box in the site header to find a service or topic.

On GitHub you can also read the same Markdown under `docs/` — Mermaid renders in GitHub’s UI for many pages.

## 3. Explore C4 diagrams (interactive)

```bash
npm run c4:dev
```

LikeC4 opens a browser UI. There you can:

- Open **System context** (FalconX vs Betfair / feeds / users)
- Zoom into **Containers** (all services)
- Switch to **Money path** or **Odds & catalogue** views
- Click elements to see relationships

Model source of truth: `c4/model.c4` (edit in a PR when topology changes).

More detail: [Interactive workspace](/c4/interactive).

## 4. When you change the product

| You changed… | You update… |
|---|---|
| A service / dependency | [Catalog](/catalog/services) + `c4/model.c4` |
| A critical path | [Flows](/flows/) |
| Env / store / deploy story | [Infra](/infra/) |
| A real architecture choice | New [ADR](/adr/template) (Proposed → Accepted) |

Full process: [How we decide](/guide/how-we-decide).

## 5. Build check (before PR)

```bash
npm run c4:validate   # model must be valid
npm run build         # C4 export + static docs site
```

CI runs the same checks on PRs.

## Mental model

```text
  npm run docs:dev  →  read / search / Mermaid flows
  npm run c4:dev    →  interactive C4 diagrams
  docs/adr/         →  team decisions (SSOT for “why”)
  c4/model.c4       →  SSOT for “what exists and how it connects”
```
