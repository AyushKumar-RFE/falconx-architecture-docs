# Data stores

| Store | Local | Cloud (typical) | Notes |
|---|---|---|---|
| **Postgres** | `:5432` (admin/admin) | Aurora PG | Schema per service; BettingEngine owns bets schema used by Bets |
| **Postgres replica** | `:5433` when `REPLICA=1` | Read replica | Not always-on in base local stack |
| **Redis / Valkey** | `:6379` | ElastiCache Valkey | Base local Redis is **cluster-enabled** (single node, all slots) — CROSSSLOT surfaces early |
| **Kafka** | `:9092` | MSK | Local pinned intentionally (listener constraints) — see Local CLAUDE/DECISIONS |
| **LocalStack** | `:4566` | Real AWS | Lambdas, SQS, EventBridge, SSM, etc. for local/isolated |

## Pool / saturation

Fleet DB/Redis pools are a shared budget. Pool metrics contract (`db_pool_*` / `redis_pool_*`) is implemented in shared obs libs — see historical ADR material in Local-dev-setup (`docs/adr-003-…`) and promote a copy into this repo's ADR series when you formally adopt it here.

## GlitchTip / Sentry Redis

Local GlitchTip must use **its own** Redis — not the cluster-enabled app Redis (cross-slot ingest failures).
