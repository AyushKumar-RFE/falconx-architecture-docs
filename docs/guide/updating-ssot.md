# Updating the SSOT

## Same-change rule

If your PR changes behavior that this site describes, update the matching page **in the same PR or wave**:

| Change | Update |
|---|---|
| New / removed service | [Catalog](/catalog/services) + C4 model |
| New decision | New ADR under `docs/adr/` + index row |
| New critical path | [Flows](/flows/) + Mermaid |
| Env / store / deploy | [Infra](/infra/) — link IaC, don't paste secrets |

## Commands

```bash
npm install
npm run docs:dev      # VitePress http://localhost:5173
npm run c4:dev        # LikeC4 interactive UI
npm run c4:validate   # fail CI if model breaks
npm run build         # export C4 into docs/public/c4 + build site
```

See also [How to use](/guide/how-to-use).
