# Catalogue sync

## Intent

Ensure market catalogue in FalconX matches Betfair (or emulator) so APIs and betting see real markets.

## Happy path (logical)

```mermaid
sequenceDiagram
  participant Src as Betfair API / emulators
  participant Sync as betfairstreaming-catalogue-sync
  participant DB as Postgres
  participant Gate as Stack readiness

  Src->>Sync: List / reconcile markets
  Sync->>DB: Upsert catalogue
  Note over Gate: Local stack: debezium-migration waits on catalogue-sync<br/>so APIs/workers gate on that edge
  Sync-->>Gate: service_started / completed per compose
```

## Design notes (keep current)

- Emulator mode: `BETFAIR_URL=http://emulators:8080`, catalogue-sync often runs with `--loop`.
- Distroless Go images: healthchecks must use the binary's own `healthcheck` subcommand — no `CMD-SHELL` / `curl`.

## When you change this flow

Update infra local-stack notes and any compose dependency edges; ADR if catalogue ownership moves off BetfairStreaming.
