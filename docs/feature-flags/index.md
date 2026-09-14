# Feature flags

BigBash does not use a dedicated feature-flag SaaS (LaunchDarkly, Unleash, etc.). Instead:
- Environment variables set in GitOps Helm values (custom-values.yaml) setting the flags directly inside the  container.
- For Frontends (B2B/B2C), We use PostHog remote flags (the env var usually only holds the flag key; on/off is in PostHog), Frontends also have plain env flags (NEXT_PUBLIC_ENABLE_*, NEXT_PUBLIC_DISPLAY_*, etc.) — those are on/off from env alone, not PostHog.


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

### What is this?

Many **read** APIs used to live only on BettingEngine (PnL, bets list, odds, etc.).
FrontMarket can now answer those same reads itself (usually from Redis/cache).

Each `FRONTMARKET_OWNS_<THING>` flag is a simple on/off switch:

- **`"true"`** → FrontMarket handles that read
- **anything else / unset** → treat as off (FrontMarket code checks case-insensitive `"true"` only)

Why so many flags? So we can move **one endpoint at a time** from BettingEngine → FrontMarket, and roll back one endpoint without turning everything off.

### Where do you flip them?

| Env | File in `rfetech-gitops` |
|---|---|
| develop | `helm-charts/helm-overrides/fantasy7-develop/frontmarket/custom-values.yaml` |
| perf | `helm-charts/helm-overrides/fantasy7-perf/frontmarket/custom-values.yaml` |
| prod | `helm-charts/helm-overrides/fantasy7-prod/frontmarket/custom-values.yaml` |

Look under `deployment.envs` in that YAML. Today on **develop**, the ownership flags below are set to `"true"`.

Code that reads them lives mainly in FrontMarket: `pkg/domain/betfair`, `fancy`, `bookmaker` (plus related packages for the non-OWNS flags below).

### Ownership flags (one flag = one capability)

| Flag | FrontMarket owns… |
|---|---|
| `FRONTMARKET_OWNS_PNL_USER` | User PnL |
| `FRONTMARKET_OWNS_PNL_MARKETS` | Event markets PnL |
| `FRONTMARKET_OWNS_PNL_USER_ACCOUNTS` | PnL user-accounts |
| `FRONTMARKET_OWNS_PROMOTED_EVENTS` | Promoted events |
| `FRONTMARKET_OWNS_FAVOURITE_EVENTS` | Favourite events |
| `FRONTMARKET_OWNS_USER_BETS` | User bets (`/betting/bets`) |
| `FRONTMARKET_OWNS_MARKET_RUNNERS_PNL` | Market runners PnL |
| `FRONTMARKET_OWNS_STACK_BUTTONS` | Stack buttons |
| `FRONTMARKET_OWNS_EVENT_LIVE_PNL` | Live PnL |
| `FRONTMARKET_OWNS_BETTICKER` | Betticker |
| `FRONTMARKET_OWNS_BETFAIR_ODDS` | Betfair odds |
| `FRONTMARKET_OWNS_EVENT_SERVICES` | Event services |
| `FRONTMARKET_OWNS_MARKET_CASHOUT_CONFIG` | Market cashout config |
| `FRONTMARKET_OWNS_EVENTS_BY_SPORT` | Events by sport |
| `FRONTMARKET_OWNS_BOOKMAKER_CASHOUT` | Bookmaker cashout admin path |
| `FRONTMARKET_OWNS_EVENTS_BY_IDS` | Events by ids |
| `FRONTMARKET_OWNS_BETS_COUNT` | Bets count |
| `FRONTMARKET_OWNS_BOOKMAKER_RUNNER_ODDS` | Bookmaker runner odds |
| `FRONTMARKET_OWNS_BOOKMAKER_EVENT_MARKETS_ODDS` | Bookmaker event markets odds |
| `FRONTMARKET_OWNS_FANCY_EVENTS_ODDS` | Fancy events/odds |
| `FRONTMARKET_OWNS_FANCY_EVENT_MARKETS` | Fancy event markets |

### Related FrontMarket flags (same YAML, not `OWNS_*`)

These are **also** set on the FrontMarket `custom-values.yaml`, but they are not ownership migrations — they turn features/caches on or off.

| Flag | What it does | Notes |
|---|---|---|
| `COMPETITION_WINNER_MARKET_ENABLED` | Exposes `GET /aggregator/competition/markets` | Off in code until env is `"true"` |
| `SSE_ODDS_ENABLED` | Exposes `GET /stream/odds` (live odds stream) | Soak carefully before promoting |
| `DASHBOARD_BLOB_L1_CACHE_ENABLED` | In-process cache for dashboard blob | |
| `FRONTMARKET_ODDS_CACHE_ENABLED` | Per-market odds cache | **On** by default in code; prod YAML may set `"false"` to kill it |
| `BETTOR_CHILD_ACCOUNTS_USE_GOUSER` | Load bettor downline via GoUser | Also exists on BettingEngine; develop FrontMarket sets `"true"` |

### ManualDataManagement is separate

MDM can call FrontMarket instead of BettingEngine for a few reads. That is a **different** switch, in a **different** YAML:

`helm-charts/helm-overrides/fantasy7-{env}/manualdatamanagement/custom-values.yaml`

| Flag | Meaning |
|---|---|
| `READ_MARKET_RUNNERS_PNL_VIA_FRONTMARKET` | MDM calls FrontMarket for that read |
| `READ_EVENT_DETAILS_VIA_FRONTMARKET` | same |
| `READ_BETS_COUNT_VIA_FRONTMARKET` | same |
| `FRONTMARKET_SERVICE_URL` | Base URL MDM uses when those reads are on |

Even if FrontMarket already “owns” the path (`FRONTMARKET_OWNS_*=true`), MDM still talks to BettingEngine until these `READ_*` flags are `"true"`. On develop they are still **`"false"`**.

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
