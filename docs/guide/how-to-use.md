# How to use this site

This repo is the **architecture SSOT**. The team reads it on a **shared website**; you change it with **git pull requests**.

## Shared site (what everyone uses)

| What | URL |
|---|---|
| **Docs site** | https://ayushkumar-rfe.github.io/falconx-architecture-docs/ |
| **Interactive C4 diagrams** | https://ayushkumar-rfe.github.io/falconx-architecture-docs/c4-workspace/ |

Note: `/c4/` is documentation *about* C4. The interactive diagrams are **`/c4-workspace/`** (also **Open diagrams** in the nav).

### What you can do on the hosted site

- Browse catalog / flows / infra / ADRs
- Search from the header
- Open interactive C4 (zoom, switch views, click services)
- Click **Edit this page** → GitHub → open a PR

### How the team discusses

| Activity | Where |
|---|---|
| Read architecture | Hosted docs + C4 workspace |
| Propose a change | Pull request (Markdown and/or `c4/model.c4`) |
| Debate a decision | PR comments + new **ADR** (`Proposed`) |
| Async questions | GitHub **Discussions** or team chat + link to the page |

Git remains the source of truth — the website is the **published view**.

---

## Hosting notes

This site is on **GitHub Pages** (public repo). CI builds with:

- `DOCS_BASE=/falconx-architecture-docs/`
- `C4_BASE=/falconx-architecture-docs/c4-workspace/` (so LikeC4 assets resolve correctly)

Push to `main` → Actions → **docs** workflow redeploys.

---

## Local preview (optional, for authors)

```bash
git clone https://github.com/AyushKumar-RFE/falconx-architecture-docs.git
cd falconx-architecture-docs
npm install
DOCS_BASE=/ C4_BASE=/c4-workspace/ npm run build && npm run docs:preview
# or while editing:
DOCS_BASE=/ npm run docs:dev
npm run c4:dev
```

Needs **Node.js 22+**.

---

## When you change the product

| You changed… | You update… |
|---|---|
| A service / dependency | [Catalog](/catalog/services) + `c4/model.c4` |
| A critical path | [Flows](/flows/) |
| Env / store / deploy story | [Infra](/infra/) |
| A real architecture choice | New [ADR](/adr/template) (Proposed → Accepted) |

Open a PR → CI builds → merge `main` → **Pages updates** for everyone.

Full process: [How we decide](/guide/how-we-decide).

## Mental model

```text
  …/falconx-architecture-docs/              → docs pages
  …/falconx-architecture-docs/c4-workspace/ → interactive C4 (not /c4/)
  Pull requests                             → discuss & change the SSOT
```
