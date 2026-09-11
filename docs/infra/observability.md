# Observability

| Signal | Local | Cloud |
|---|---|---|
| Errors / traces | GlitchTip via `SENTRY=1` (UI `:8000`) | Sentry org |
| Metrics (KEDA-shaped) | OTel collector via `OTEL=1` → `:8889/metrics` | Groundcover / Prometheus path per gitops |
| Logs | `make logs-local SERVICE=…` | Platform logging |

## Rules of thumb

- Tracing ownership is **Sentry's** in the local OTel overlay (metrics-only collector).
- A **zero** in GlitchTip is not a pass — verify ingest (e.g. CrossSlot) before claiming "no errors".
- Pool saturation metrics are the intended KEDA signal — see data-stores / ADRs.
