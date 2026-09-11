# Tooling

| Job | Tool | Notes |
|---|---|---|
| Docs site | **VitePress** | Markdown → searchable static site |
| Interactive C4 | **LikeC4** | Model in `/c4`; `npm run c4:dev` / `c4:build` |
| Sequences in flows/ADRs | **Mermaid** | Native in VitePress via plugin; also renders on GitHub |
| Decisions | **ADRs** (Markdown) | See [template](/adr/template) |
| Confluence / Jira context | **Atlassian Rovo MCP** | OAuth; pull into drafts — git stays SSOT |
| AI assist | Cursor / Claude | Draft catalog rows & ADR stubs; humans Accept ADRs |

## Why not MkDocs/Docusaurus alone for C4?

MkDocs and Docusaurus **host pages**; they do not execute a C4 model. Interactive drill-down comes from LikeC4/Structurizr. This repo uses VitePress for narrative + LikeC4 for the model, then embeds/links the export.

## CI

`.github/workflows/docs.yml` validates the LikeC4 model and builds the site on every PR.
