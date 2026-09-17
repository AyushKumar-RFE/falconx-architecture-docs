# ADR 0004 — Production AWS diagram is the architecture baseline

**Status:** Proposed  
**Date:** 2026-09-17  
**Deciders:** FalconX engineering / infra-team  
**Related:** [Architecture baseline](/architecture/) · ADR 0002 · ADR 0003

## Context

The infra handbook explains the environment well, but it is a written guide. Reviewers and new joiners have to read several pages to picture how production is laid out. ADRs had no single picture to point at, so decisions were made against prose that can drift.

We need one current-state diagram that is the thing we design against.

## Decision

1. **Level 1 production diagram** (`architecture/prod_level1.py` → [Architecture baseline](/architecture/)) is the **current-state baseline** for infrastructure decisions.
2. Grouping follows AWS Architecture Center: AWS Cloud → Account → Region → VPC → subnet. Icons are AWS Architecture Icons (Python `diagrams` library).
3. **Level 2** drill-downs (network AZs, plus C4 views for EKS, data, CI/CD) explain a slice. They must stay consistent with Level 1.
4. The written [handbook](/infra/) is **supporting detail**, linked from the diagram, not the entry point.
5. Every ADR that changes topology includes a **before / after** of the affected part of this diagram (see [template](/adr/template)).
6. Source and rendered PNG/SVG are reviewed in git like any infra change. If the diagram and Terraform disagree, Terraform wins — then the diagram is updated in the same PR.

## Consequences

- Onboarding and review start from one picture
- ADRs are grounded in a shared baseline
- Diagram PRs are required when VPC/EKS/data/edge topology changes
- LikeC4 remains the interactive drill-down (ADR 0003), not the Level 1 baseline — C4 does not use AWS grouping boxes

## Alternatives considered

| Option | Why not |
|---|---|
| Handbook + Mermaid only | Hard to read as a one-page AWS layout; no official icons |
| LikeC4 as the only baseline | Good for C4 views; weak AWS Cloud→AZ→subnet grouping |
| draw.io only | Weaker diffs; we already have diagrams-as-code |
| Target-state / aspirational diagram | Would mix “now” and “wish”; baseline is **current** |

## Architecture baseline (this ADR)

This ADR **introduces** the baseline. There is no before diagram in git. After: [Level 1 production](/architecture/).
