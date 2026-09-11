---
layout: home
hero:
  name: FalconX Architecture
  text: Single source of truth
  tagline: C4 model · ADRs · service catalog · infra · critical flows — versioned in git, readable as a site, fed by Confluence when useful.
  actions:
    - theme: brand
      text: How we decide
      link: /guide/how-we-decide
    - theme: alt
      text: Service catalog
      link: /catalog/services
    - theme: alt
      text: Open C4
      link: /c4/
features:
  - title: C4 as code
    details: LikeC4 model under /c4 — interactive workspace for context, containers, and key components. Diagrams change with PRs.
  - title: ADRs
    details: Architecture Decision Records are how the team decides. Status, context, consequences — searchable and reviewable.
  - title: Catalog + infra
    details: Every active service, library, env, and data store — with links to the real IaC/gitops/compose sources of truth.
  - title: Confluence bridge
    details: Atlassian Rovo MCP pulls existing Confluence pages into draft markdown. Git remains SSOT; Confluence is the hub and inbox.
---

## Start here

| I need to… | Go to |
|---|---|
| Propose or accept a decision | [How we decide](/guide/how-we-decide) + [ADR template](/adr/template) |
| Understand the system shape | [C4 overview](/c4/) → [interactive workspace](/c4/interactive) |
| Find a service | [Service catalog](/catalog/services) |
| Trace money / odds / catalogue | [Critical flows](/flows/) |
| Understand AWS / local / deploy | [Infra](/infra/) |
| Import from Confluence | [Confluence bridge](/confluence/) |

## Non-negotiables

1. **This repo is the SSOT** for architecture narrative, C4, and ADRs.
2. **IaC / Compose / gitops** remain the SSOT for *config* — docs summarize and link, they do not copy YAML wholesale.
3. **Confluence is not SSOT** — use it as a discovery hub and to pull legacy pages via MCP; promote into git via PR.
4. **Topology or boundary changes ship with an ADR** (Proposed → Accepted) in the same change wave when possible.
