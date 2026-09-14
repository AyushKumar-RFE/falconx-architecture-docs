---
layout: home
hero:
  name: Bigbash Architecture
  text: Doc-as-Code
  tagline: C4 model · ADRs · service/library catalog · infra · feature flags — versioned in git and the SSOT for BigBash architecture.
  actions:
    - theme: brand
      text: Open C4
      link: /c4/
    - theme: brand
      text: Service catalog
      link: /catalog/services
    - theme: brand
      text: ADRs
      link: /adr/
    - theme: brand
      text: Infra
      link: /infra/
    - theme: brand
      text: Feature flags
      link: /feature-flags/
---

## Rules We Follow

1. **This repo is the SSOT** for architecture and infra narrative.
2. **Every change in infra/arch** syncs this doc.
3. **Decision flow:** Update ADR in this repo → update other docs if needed → develop the respective component.
4. **Creating or deprecating any feature flag** — update this doc with why it is needed and what it does in the Feature Flag section.
