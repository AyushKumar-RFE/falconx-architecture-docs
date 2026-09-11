# ADR 0001 — Record architecture decisions

**Status:** Accepted  
**Date:** 2026-09-11  
**Deciders:** FalconX engineering  

## Context

Post-launch we will change boundaries, contracts, and infra often. Tribal knowledge and chat threads do not scale across ~20 service repos.

## Decision

All significant architecture choices are recorded as ADRs in this repository, reviewed in PRs, and indexed on the ADR page.

## Consequences

- Decisions are searchable and dated
- Superseding is explicit
- Slight process overhead on large changes

## Alternatives considered

| Option | Why not |
|---|---|
| Confluence-only pages | Drift from code; weak review |
| Slide decks | Not diffable; rot quickly |
