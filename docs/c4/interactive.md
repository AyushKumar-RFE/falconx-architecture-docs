# Interactive C4 workspace

## Local (best)

```bash
npm install
npm run c4:dev
```

LikeC4 opens a browser UI: zoom, filter, and navigate context → containers → focused views.

## Embedded export (docs site)

After `npm run c4:build`, static assets land in `docs/public/c4/`.

After export, open the built workspace at [`/c4/`](/c4/) (served from `docs/public/c4` when using `npm run docs:dev`).

If that link 404s, run `npm run c4:build` then `npm run docs:dev` again.
