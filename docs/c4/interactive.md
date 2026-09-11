# Interactive C4 workspace

## On the shared website (team)

After Pages deploy, open:

**`/c4-workspace/`** on the hosted site  

(or use the nav link **Open diagrams**).

That is the interactive LikeC4 app: zoom, switch **System context / Containers / Money path / Odds** views, click services.

## Local (authors)

```bash
npm install
npm run c4:dev          # live editor UI while changing model.c4
npm run c4:build        # writes docs/public/c4-workspace for the docs site
```

Model source of truth: `c4/model.c4` — change it in a PR; CI rebuilds the hosted workspace.
