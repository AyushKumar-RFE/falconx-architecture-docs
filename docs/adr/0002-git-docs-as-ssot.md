# ADR 0002 — Git docs site as architecture SSOT

**Status:** Accepted  
**Date:** 2026-09-11  
**Deciders:** FalconX engineering  

## Context

We need a single source of truth engineers trust when making follow-on decisions. Google Docs / Confluence are familiar but drift from multi-repo reality.

## Decision

1. **This git repo** (VitePress Markdown + LikeC4 + ADRs) is the architecture SSOT.
2. **Confluence** is a hub + inbox: link here; import legacy pages via Atlassian MCP into PRs; do not treat Confluence as authoritative after import.
3. **IaC / compose / gitops** remain SSOT for configuration.

## Consequences

- PRs review architecture with code
- Non-engineers may need a short Confluence landing page
- Team must update docs in the same change wave

## Alternatives considered

| Option | Why not |
|---|---|
| Confluence as SSOT | Proven drift in multi-repo estates |
| Only Local-dev-setup/docs | Couples orchestration repo to long-form product architecture; harder as a standalone publishable site |
