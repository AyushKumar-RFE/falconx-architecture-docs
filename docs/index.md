---
layout: home
hero:
  name: Bigbash Architecture
  text: Doc-as-Code
  tagline: Current-state architecture baseline · C4 · ADRs · catalog · infra handbook — versioned in git.
  actions:
    - theme: brand
      text: Architecture baseline
      link: /architecture/
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
      text: Infra handbook
      link: /infra/
    - theme: brand
      text: Feature flags
      link: /feature-flags/
---

## Rules We Follow

1. **The [production architecture diagram](/architecture/) is the baseline** we design against. ADRs that change topology include a before/after of that diagram.
2. **This repo is the SSOT** for architecture narrative. IaC/gitops remain SSOT for configuration.
3. **Every change in infra/arch** updates the baseline diagram when topology changes, then the handbook if needed.
4. **Decision flow:** Update ADR (with diagram before/after) → update the baseline if needed → implement in the owning repo.
5. **Creating or deprecating any feature flag** — update this doc with why it is needed and what it does in the Feature Flag section.
