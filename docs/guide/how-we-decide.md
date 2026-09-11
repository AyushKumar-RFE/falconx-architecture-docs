# How we decide

This site exists so engineers can change FalconX after launch **without tribal knowledge**.

## Decision loop

```mermaid
flowchart LR
  A[Change idea / incident / request] --> B{Touches boundaries,<br/>data stores, deploy path,<br/>or cross-service contract?}
  B -->|No| C[PR + update catalog/flow if needed]
  B -->|Yes| D[Draft ADR Status: Proposed]
  D --> E[Update C4 model if topology changes]
  E --> F[PR review]
  F --> G{Accept?}
  G -->|Yes| H[ADR → Accepted + merge]
  G -->|No / later| I[ADR → Rejected or Superseded]
```

## What requires an ADR

Write an ADR when the change:

- Adds/removes a **service boundary** or splits/merges ownership of data
- Changes a **cross-service contract** (API, Kafka topic semantics, Redis key shape used by multiple services)
- Changes **deploy path** (new lambda, new env, new dependency on VPN/emulator, etc.)
- Chooses among **durable alternatives** the team might reverse later
- Declares something **legacy / out of rollout** (e.g. BetfairData, OrderStreaming)

Skip an ADR for pure refactors, bugfixes, and docs-only typo fixes — still update catalog/flows if behavior readers rely on changes.

## Roles

| Role | Responsibility |
|---|---|
| Author | Drafts ADR + C4/catalog deltas in one PR |
| Reviewers | Domain owners of affected services |
| Merger | Ensures Status, Consequences, and links are complete |

## Related

- [ADR template](/adr/template)
- [Updating the SSOT](/guide/updating-ssot)
- [How to use](/guide/how-to-use)
