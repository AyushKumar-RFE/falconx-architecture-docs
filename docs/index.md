---
layout: home
hero:
  name: FalconX Architecture
  text: Single source of truth
  tagline: C4 model · ADRs · service catalog · infra — versioned in git and readable as a local site.
  actions:
    - theme: brand
      text: Open C4
      link: /c4/
    - theme: alt
      text: Service catalog
      link: /catalog/services
    - theme: alt
      text: ADRs
      link: /adr/
features:
  - title: C4 as code
    details: LikeC4 model under /c4 — interactive workspace for context, containers, and key components. Diagrams change with PRs.
  - title: ADRs
    details: Architecture Decision Records are how the team decides. Status, context, consequences — searchable and reviewable.
  - title: Catalog + infra
    details: Every active service, library, env, and data store — with links to the real IaC/gitops/compose sources of truth.
---

## Start here

| I need to… | Go to |
|---|---|
| Understand the system shape | [C4 overview](/c4/) → [interactive workspace](/c4/interactive) |
| Find a service | [Service catalog](/catalog/services) |
| Propose or accept a decision | [ADR template](/adr/template) |
| Understand AWS / local / deploy | [Infra](/infra/) |

## Non-negotiables

1. **This repo is the SSOT** for architecture narrative, C4, and ADRs.
2. **IaC / Compose / gitops** remain the SSOT for *config* — docs summarize and link, they do not copy YAML wholesale.
3. **Topology or boundary changes ship with an ADR** (Proposed → Accepted) in the same change wave when possible.
