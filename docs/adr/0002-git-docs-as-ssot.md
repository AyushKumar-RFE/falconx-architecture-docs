# ADR 0002 — Git docs site as architecture SSOT

**Status:** Accepted  
**Date:** 2026-09-11  
**Deciders:** FalconX engineering  

## Context

We need a single source of truth engineers trust when making follow-on decisions. Docs that live only in chat or slide decks drift from multi-repo reality.

## Decision

1. **This git repo** (VitePress Markdown + LikeC4 + ADRs) is the architecture SSOT.
2. **IaC / compose / gitops** remain SSOT for configuration — this site summarizes and links.

## Consequences

- PRs review architecture with code
- Team must update docs in the same change wave

## Alternatives considered

| Option | Why not |
|---|---|
| Wiki-only docs | Weak review; drifts from code |
| Only Local-dev-setup/docs | Couples orchestration repo to long-form product architecture |
