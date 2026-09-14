# Feature flags

Kill-switches and staged rollouts. **No LaunchDarkly / Unleash** — flags live as env vars (GitOps) or PostHog (frontends).

## How they work

| Mechanism | Where | How to flip |
|---|---|---|
| **GitOps env** | Most services | `others/rfetech-gitops/helm-charts/helm-overrides/fantasy7-{develop,perf,prod}/…/custom-values.yaml` → `envs:` |
| **PostHog** | Frontend-B2B / B2C | Env holds the **flag key**; on/off (+ payload) is in the PostHog UI |
| **Code default** | Service `Settings` / `os.Getenv` | Usually **OFF** until GitOps sets `"true"` |

Local compose uses each service’s `.env` / `env.local`. Prod values in gitops are the SSOT for what is actually on.

**Update this page** when you create or deprecate a product flag (why + what it does).

---

## FrontMarket ownership (`FRONTMARKET_OWNS_*`)

Pattern: FrontMarket serves a BettingEngine (or sibling) **read path**. Flag = case-insensitive `"true"` only.

| Family | What it does | Notes |
|---|---|---|
| `FRONTMARKET_OWNS_*` (PnL, bets, odds, fancy, bookmaker, stack-buttons, …) | FrontMarket owns that route/cache path | Paired MDM clients: `READ_*_VIA_FRONTMARKET` (still mostly **off** — FM owns the path; MDM URL swap is separate) |
| `COMPETITION_WINNER_MARKET_ENABLED` | Registers `GET /aggregator/competition/markets` | Default off |
| `SSE_ODDS_ENABLED` | Registers `GET /stream/odds` | Soak; do not promote lightly |
| `DASHBOARD_BLOB_L1_CACHE_ENABLED` | In-process L1 for dashboard blob | |
| `FRONTMARKET_ODDS_CACHE_ENABLED` | Per-market odds cache | Code default **on**; prod may kill-switch **off** |
| `BETTOR_CHILD_ACCOUNTS_USE_GOUSER` | Bettor downline via GoUser / go-datastore | Also on BettingEngine |

Canonical checks: `FrontMarket` domain packages (`betfair`, `fancy`, `bookmaker`, `stream`, `aggregator`).

---

## Frontend — env (B2B)

`next-runtime-env`. Most require exact `"true"` (settlement also accepts `"1"`).

| Flag | What it does |
|---|---|
| `NEXT_PUBLIC_ENABLE_MARKET_SETTLEMENT` | Market settlement UI |
| `NEXT_PUBLIC_DISPLAY_MANUAL_MARKETS` | Manual Markets nav / routes |
| `NEXT_PUBLIC_DISPLAY_BETFAIR_SUSPEND_ICON` | Betfair suspend icon (Sports Hierarchy) |
| `NEXT_PUBLIC_ENABLE_INCIDENT_REPORTING` | Manager incident reporting |
| `NEXT_PUBLIC_DISPLAY_THIRD_PARTY_LIVE_SCORE` | Third-party live score / Live TV on live markets |
| `NEXT_PUBLIC_FANCY_PER_ROW_SPREADS` | Per-row spreads in fancy override panel |
| `NEXT_PUBLIC_CASINO_LIVE_BETS_DISABLED` | `"true"` → legacy casino bets tabs |

---

## Frontend — PostHog

| Env key | Service | What the remote flag does |
|---|---|---|
| `NEXT_PUBLIC_BET_PLACEMENT_FEATURE_FLAG_KEY` | B2C | When PostHog flag is on → place-bet via **Bets**; else legacy BettingEngine |
| `NEXT_PUBLIC_DATA_AGGREGATION_POSTHOG_KEY` | B2B | Payload: which B2B APIs use data-aggregation (per-key booleans) |
| `NEXT_PUBLIC_POSTHOG_DISABLED` / `NEXT_PUBLIC_ENABLE_POSTHOG` | B2B + B2C | Master kill for PostHog (and thus remote FFs) |

---

## Backend rollouts

Defaults below are **code defaults** (usually off). Env/GitOps overrides per environment.

### Placement & profit

| Flag | Service(s) | What it does |
|---|---|---|
| `ENFORCE_MARKET_MAX_PROFIT` | BettingEngine | Enforce market max-profit on place (default **on**) |
| `ENFORCE_MAX_PROFIT_SINGLE_ODD` | BettingEngine, FancyData, BookmakerData, MDM | Single-odd max profit |
| `ENFORCE_PLACE_BET_SIDE_RULES` | BettingEngine | Side / market_type validation on place (default **on**) |
| `ENABLE_FANCY_BETS_MARKET_LOOKUP` | BettingEngine | Fancy selection string via FancyData lookup |

### SSE / notices (FrontMarket consumers)

| Flag | Service(s) | What it does |
|---|---|---|
| `ODDS_CHANGE_NOTICES_ENABLED` | FancyData, BookmakerData, BetfairStreaming, MDM | Redis odds-change notices for FM SSE |
| `ACCOUNT_CHANGE_NOTICES_ENABLED` | BettingEngine | Redis account notices for FM account SSE |
| `FANCY_MARKET_CLOSURE_SYNC_ENABLED` | FancyData | Force Redis closure sync on market close |

### Reads, routing, access

| Flag | Service(s) | What it does |
|---|---|---|
| `MARKET_SETTLEMENT_APPROVAL_ENABLED` | MDM | Settlement approval workflow |
| `READ_*_VIA_FRONTMARKET` | MDM | Point that read at FrontMarket base URL |
| `INTERNAL_UNAUTH_ROUTES_ENABLED` | BE, FancyData, BookmakerData, MDM | Prefer `/internal/` unauth S2S (default **on**) |
| `UPLINE_ACCOUNTS_USE_BACKOFFICE` | BettingEngine | Upline accounts via BackOffice |
| `BETTOR_CHILD_ACCOUNTS_USE_GOUSER` | BettingEngine | Bettor children via GoUser |
| `EVENT_MARKETS_PNL_READ_REPLICA_ENABLED` | BettingEngine | Event markets PnL on read replica |
| `DA_ROOT_ID_READ_ENABLED` | BackOffice (+ DA) | `root_id`-scoped market reads |
| `DA_ROOT_ID_PARTITION_ENABLED` | DataAggregator | HASH(root_id, market_id) partitions |
| `KAFKA_SA_MARKET_PARTITION_ENABLED` | BettingEngine, DataAggregator | SA:market Kafka keys / dedupe |
| `DOWNLINE_ACCOUNTS_ACCESS_CHECK_ENABLED` | BE, BackOffice | Downline-accounts access guard |
| `ACCOUNT_STATEMENTS_DOWNLINE_ACCESS_CHECK_ENABLED` | BettingEngine | Statements downline guard |
| `USER_ACTIVITY_LOG_ACCESS_CHECK_ENABLED` | User | Activity-log hierarchy checks |
| `CLIENT_ROLE_DIRECT_PARENT_EDIT_CHECK_ENABLED` | User | Client-admin edits only direct children |
| `ENABLE_USER_SYNC_UPLINE_TRIM` | User | Trim company roles from `upline_users` |

### Other product toggles

| Flag | Service(s) | What it does |
|---|---|---|
| `ADD_EVENT_USE_ACTIVE_FANCY` | FancyData | Add-event validates via active-fancy |
| `BOOKMAKER_FEED_GAP_SKIP_OVERRIDDEN_ENABLED` | BookmakerData | Skip feed-gap suspend under MDM override (default **on**) |
| `STALE_OVERRIDE_RECONCILE_ENABLED` | MDM | Stale BM/Fancy override reconcile (default **on**) |
| `DATA_INTEGRITY_AUTO_CORRECTION_ENABLED` | BE, BackOffice | Async data-integrity auto-correct |
| `BANKING_PARITY_ENABLED` | BettingEngine | Banking parity checks |
| `LIVE_MARKETS_BETTORS_COUNT_ENABLED` | BE, BackOffice | Open-bettor counts on live markets |
| `GATEWAY_TRUST_ENABLED` | BackOffice | Gateway trust (`"0"` = off in develop) |

---

## Not listed here

Infra / ops toggles (`KAFKA_ENABLED`, `SENTRY_*`, `LEADER_ELECTION_*`, `PYROSCOPE_*`, `AWS_MSK_*`, pool sizes) are **not** product feature flags — leave them in service config / gitops only.
