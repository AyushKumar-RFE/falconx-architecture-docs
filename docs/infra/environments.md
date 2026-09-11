# Environments

| Env | Purpose | How it runs |
|---|---|---|
| **local** | Dev laptop | `make start-local*` — single image `falconx-local-dev`, source baked |
| **isolated** | CI / e2e | Pre-built service images + compose without local overlay |
| **develop** | Shared cloud | gitops `fantasy7-develop` (names evolve — check gitops) |
| **perf** | Performance | gitops perf target + stress baselines |
| **prod** | Production | gitops prod; promotions via controlled process |

Additive local flags (compose overlays): `SENTRY=1`, `OTEL=1`, `REPLICA=1`, plus emulator/VPN/fullstack target variants.

## Rule

Promoting an architecture change: ADR Accepted here → implement in service/infra/gitops PRs → wave merge order as required by `Local-dev-setup` `wave.sh`.
