# FalconX Architecture Docs (SSOT)

Git-hosted **single source of truth** for FalconX architecture:

- **C4 as code** (LikeC4) — interactive diagrams  
- **ADRs** — how the team decides after launch  
- **Service catalog, critical flows, infra** — engineer-facing  

## How to use (quick)

```bash
git clone https://github.com/AyushKumar-RFE/falconx-architecture-docs.git
cd falconx-architecture-docs
npm install
npm run docs:dev    # docs site  → http://localhost:5173
npm run c4:dev      # interactive C4 diagrams
```

Full walkthrough: [docs/guide/how-to-use.md](docs/guide/how-to-use.md)

```bash
npm run build       # validate + static site
```

## Layout

```
c4/model.c4                 # LikeC4 model (diagram SSOT)
docs/                       # VitePress content
  guide/                    # how to use / decide / update
  c4/                       # how to read the model
  catalog/                  # services, libs, legacy
  flows/                    # place-settle, odds, catalogue
  infra/                    # envs, stores, deploy, local stack
  adr/                      # decisions
.github/workflows/docs.yml  # validate + build
```

## Relationship to Local-dev-setup

| Concern | Where |
|---|---|
| Run the stack | `Local-dev-setup` |
| Agent/ops micro-context | `Local-dev-setup/.claude/context/...` |
| **Product architecture SSOT** | **This repo** |
| AWS/K8s config | `rfetech-infra` / `rfetech-gitops` |

## License

Internal — RFE Technology.
