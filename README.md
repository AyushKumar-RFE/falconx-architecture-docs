# FalconX Architecture Docs (SSOT)

Git-hosted **single source of truth** for FalconX architecture, published as a **team website** (docs + interactive C4).

- **C4 as code** (LikeC4)  
- **ADRs** — how the team decides after launch  
- **Service catalog, critical flows, infra**

## For the team (read / discuss)

1. Open the GitHub Pages URL (after enable — see [how to use](docs/guide/how-to-use.md)):
   - Docs: `https://ayushkumar-rfe.github.io/falconx-architecture-docs/`
   - Diagrams: `https://ayushkumar-rfe.github.io/falconx-architecture-docs/c4-workspace/`
2. Discuss via **PRs**, **ADRs**, and optional **GitHub Discussions**.
3. Change architecture by editing this repo and merging to `main` — the site redeploys automatically.

## For authors (local)

```bash
git clone https://github.com/AyushKumar-RFE/falconx-architecture-docs.git
cd falconx-architecture-docs
npm install
DOCS_BASE=/ npm run docs:dev
npm run c4:dev
```

```bash
npm run build    # same output CI publishes to Pages
```

## Enable hosting (once)

Repo **Settings → Pages → Source: GitHub Actions**, then push to `main`. Details: [docs/guide/how-to-use.md](docs/guide/how-to-use.md).

## Layout

```
c4/model.c4                      # LikeC4 model
docs/                            # VitePress pages
docs/public/c4-workspace/        # built interactive diagrams (CI)
.github/workflows/docs.yml       # build + GitHub Pages deploy
```

## License

Internal — RFE Technology.
