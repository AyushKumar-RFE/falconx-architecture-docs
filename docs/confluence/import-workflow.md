# Import workflow (Confluence → git)

Goal: harvest useful Confluence content into this SSOT without leaving two competing truths.

```mermaid
flowchart LR
  A[Find page via MCP search] --> B[Fetch page body]
  B --> C[Draft Markdown in a branch]
  C --> D{Fits where?}
  D -->|Decision| E[New ADR]
  D -->|Service fact| F[Catalog / flow / infra page]
  D -->|Noise| G[Discard / link only]
  E --> H[PR review]
  F --> H
  H --> I[Merge — git wins]
  I --> J[Optional: Confluence page becomes link hub]
```

## Agent prompts (examples)

After MCP is connected:

- “Search Confluence for FalconX architecture and list page titles + IDs”
- “Fetch Confluence page `<id>` and draft an ADR stub under `docs/adr/`”
- “Extract the service list from page `<id>` and diff against `docs/catalog/services.md`”

## Rules

- Never commit API tokens.
- Prefer summarizing over pasting entire Confluence HTML.
- If Confluence and git disagree after import, **fix git** or open an ADR — don't silently keep both.
