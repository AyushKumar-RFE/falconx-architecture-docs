# Interactive C4 workspace

## On the shared website (team)

**Important:** `/c4/` is only the *explanation* pages. The interactive model is here:

**https://ayushkumar-rfe.github.io/falconx-architecture-docs/c4-workspace/**

Or use the site nav **Open diagrams**.

There you can zoom, switch **System context / Containers / Money path / Odds** views, and click services.

## Local (authors)

```bash
npm install
npm run c4:dev          # live editor UI while changing model.c4
npm run build           # embeds workspace into the docs site under /c4-workspace/
```

Model source of truth: `c4/model.c4` — change it in a PR; CI rebuilds the hosted workspace.
