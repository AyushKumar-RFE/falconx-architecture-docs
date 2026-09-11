# How to use this site

This repo is the **architecture SSOT**. The team reads it on a **shared website**; you change it with **git pull requests**.

## Shared site (what everyone uses)

After GitHub Pages is enabled (see below), open:

| What | URL |
|---|---|
| **Docs site** (catalog, flows, ADRs, infra) | `https://ayushkumar-rfe.github.io/falconx-architecture-docs/` |
| **Interactive C4 diagrams** | `https://ayushkumar-rfe.github.io/falconx-architecture-docs/c4-workspace/` |

(Exact URL appears under repo **Settings → Pages** after the first deploy.)

Also use the site nav button **Open diagrams**.

### What you can do on the hosted site

- Browse catalog / flows / infra / ADRs
- Search from the header
- Open interactive C4 (zoom, switch views, click services)
- Click **Edit this page** → GitHub → open a PR

### How the team discusses

| Activity | Where |
|---|---|
| Read architecture | Hosted docs + C4 workspace |
| Propose a change | Pull request (update Markdown and/or `c4/model.c4`) |
| Debate a decision | PR comments + new **ADR** (`Proposed`) |
| Async questions | GitHub **Discussions** (enable on the repo) or your team chat with a link to the page |

Git remains the source of truth — the website is the **published view**.

---

## Enable GitHub Pages (once, repo admin)

1. Push these workflow changes to `main`.
2. Repo **Settings → Pages**:
   - **Source:** GitHub Actions
3. Open **Actions** → wait for **docs** workflow → green.
4. Open the Pages URL and share it with the team.

### Private repo note

- **Public** repo → Pages URL is public.
- **Private** repo → Pages for private sites needs GitHub **Pro/Team** (or move the repo under an org that has it).  
  If Pages is blocked, use **Cloudflare Pages** / **Netlify** free private deploy from the same `npm run build` output (ask and we can add that workflow).

---

## Local preview (optional, for authors)

```bash
git clone https://github.com/AyushKumar-RFE/falconx-architecture-docs.git
cd falconx-architecture-docs
npm install
npm run build && npm run docs:preview   # preview the same site CI publishes
# or while editing:
DOCS_BASE=/ npm run docs:dev            # local root path
npm run c4:dev                          # live LikeC4 editor UI
```

Needs **Node.js 20+**.

| Area | What you get |
|---|---|
| **Catalog** | Every service / library |
| **Flows** | Sequence diagrams (Mermaid) |
| **Infra** | Envs, stores, deploy, local stack |
| **ADRs** | Decisions the team must follow |
| **C4 workspace** | Interactive architecture diagrams |

---

## When you change the product

| You changed… | You update… |
|---|---|
| A service / dependency | [Catalog](/catalog/services) + `c4/model.c4` |
| A critical path | [Flows](/flows/) |
| Env / store / deploy story | [Infra](/infra/) |
| A real architecture choice | New [ADR](/adr/template) (Proposed → Accepted) |

Open a PR → CI builds → merge to `main` → **Pages auto-updates** for everyone.

Full process: [How we decide](/guide/how-we-decide).

## Mental model

```text
  Hosted docs URL     → team reads pages + Mermaid
  …/c4-workspace/     → team explores interactive C4
  Pull requests       → team discusses & changes the SSOT
  docs/adr/           → durable decisions
  c4/model.c4         → what exists and how it connects
```
