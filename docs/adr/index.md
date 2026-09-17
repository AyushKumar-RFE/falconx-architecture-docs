# Architecture Decision Records

| ID | Title | Status |
|---|---|---|
| [0001](./0001-record-architecture-decisions) | Record architecture decisions | Accepted |
| [0002](./0002-git-docs-as-ssot) | Git Markdown site as architecture SSOT | Accepted |
| [0003](./0003-c4-as-code-likec4) | C4 as code with LikeC4 | Accepted |
| [0004](./0004-production-architecture-baseline) | Production AWS diagram is the architecture baseline | Proposed |

## Process

1. Copy [template](./template) — include **before/after** of the [architecture baseline](/architecture/) if topology changes
2. Number sequentially (`0005-…`)
3. Open PR with Status **Proposed**
4. Merge as **Accepted** / **Rejected** / later **Superseded** by a newer ADR

Promote important historical ADRs from `Local-dev-setup/docs/adr-*` into this series when the team wants them discoverable here (keep a link back; don't fork conflicting truths).
