# FalconX Architecture Docs (SSOT)

Git-hosted architecture SSOT, published on **GitHub Pages**.

- Docs: https://ayushkumar-rfe.github.io/falconx-architecture-docs/
- **Architecture baseline (start here):** https://ayushkumar-rfe.github.io/falconx-architecture-docs/architecture/
- **Interactive C4:** https://ayushkumar-rfe.github.io/falconx-architecture-docs/c4-workspace/

## Start here

1. **[Production architecture diagram](https://ayushkumar-rfe.github.io/falconx-architecture-docs/architecture/)** — the current-state baseline we design against.
2. Handbook (why, failure modes, which file): `/infra/`
3. ADRs that change topology must include a before/after of that diagram.

## Local

```bash
npm install
npm run docs:dev
npm run c4:dev
```

Regenerate AWS diagrams (needs Graphviz):

```bash
python3 -m venv architecture/.venv
architecture/.venv/bin/pip install -r architecture/requirements.txt
PATH="/opt/homebrew/bin:$PATH" architecture/.venv/bin/python architecture/render.py
```

## License

Internal — RFE Technology.
