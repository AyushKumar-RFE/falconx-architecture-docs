---
layout: home
hero:
  name: Bigbash Architecture
  text: Doc-as-Code
  tagline: C4 model · ADRs · service/Li catalog · infra — versioned in git and readable as a local site.
  actions:
    - theme: brand
      text: Open C4
      link: /c4/
    - theme: brand
      text: Service catalog
      link: /services/
    - theme: brand
      text: ADRs
      link: /adr/
    - theme: brand
      text: Infra
      link: /infra/
features:
  - title: C4 as code
    details: LikeC4 model under /c4 — interactive workspace for context, containers, and key components. Diagrams change with PRs.
  - title: ADRs
    details: Architecture Decision Records are how the team decides. Status, context, consequences — searchable and reviewable.
  - title: Catalog + infra
    details: Every active service, library, env, and data store — with links to the real IaC/gitops/compose sources of truth.
---



## Non-negotiables

1. **This repo is the SSOT** for architecture narrative, C4, Infra and ADRs.
2. **IaC / Compose / gitops** remain the SSOT for *config* — docs summarize and link, they do not copy YAML wholesale.
3. **Topology or boundary changes ship with an ADR** (Proposed → Accepted) in the same change wave when possible.
