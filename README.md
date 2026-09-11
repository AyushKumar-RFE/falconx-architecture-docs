# FalconX Architecture Docs (SSOT)

Git-hosted **single source of truth** for FalconX architecture:

- **C4 as code** (LikeC4) — interactive diagrams  
- **ADRs** — how the team decides post-launch  
- **Service catalog, critical flows, infra** — engineer-facing  
- **Confluence bridge** — Atlassian Rovo MCP to *pull* existing pages; Confluence is not SSOT  

This is a **standalone repo** (sibling to `Local-dev-setup`), ready to push to GitHub.

## Quick start

```bash
cd falconx-architecture-docs
npm install
npm run docs:dev    # site → http://localhost:5173
npm run c4:dev      # interactive C4 UI
```

Full build (C4 export + site):

```bash
npm run build
```

## Connect Confluence MCP

Config is already in [`.cursor/mcp.json`](.cursor/mcp.json):

```json
{
  "mcpServers": {
    "Atlassian-MCP-Server": {
      "url": "https://mcp.atlassian.com/v1/mcp/authv2"
    }
  }
}
```

1. Open **this folder** in Cursor  
2. Settings → MCP → enable Atlassian server → OAuth in browser  
3. Follow [docs/confluence/connect-mcp.md](docs/confluence/connect-mcp.md)  

Then ask the agent to search/fetch Confluence and draft imports into `docs/`.

## Layout

```
c4/model.c4                 # LikeC4 model (diagram SSOT)
docs/                       # VitePress content
  guide/                    # how we decide / update
  c4/                       # how to read interactive model
  catalog/                  # services, libs, legacy
  flows/                    # place-settle, odds, catalogue
  infra/                    # envs, stores, deploy, local stack
  adr/                      # decisions
  confluence/               # MCP + import + hub template
.cursor/mcp.json            # Atlassian Rovo MCP
.github/workflows/docs.yml  # validate + build
```

## Relationship to Local-dev-setup

| Concern | Where |
|---|---|
| Run the stack | `Local-dev-setup` |
| Agent/ops micro-context | `Local-dev-setup/.claude/context/...` |
| **Product architecture SSOT** | **This repo** |
| AWS/K8s config | `rfetech-infra` / `rfetech-gitops` |

## Push as a new GitHub repo

```bash
cd /Users/ayushkumar/Work/falconx-architecture-docs
git init
git add .
git commit -m "Initial FalconX architecture SSOT (C4, ADRs, VitePress, Confluence MCP)"
gh repo create rfetechnology/falconx-architecture-docs --private --source=. --remote=origin --push
```

Adjust org/visibility as needed. Update `editLink` in `docs/.vitepress/config.mts` if the GitHub path differs.

## License

Internal — RFE Technology.
