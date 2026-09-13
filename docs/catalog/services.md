# Service catalog

Active FalconX services. Ports are **local compose** defaults unless noted.  
Canonical clone list: `Local-dev-setup/stack/config/local-repos.txt`.

| Service | Lang | Local port | Role | Depends on (typical) |
|---|---|---|---|---|
| **User** | Python / FastAPI | 8001 | Identity, wallets, hierarchy | Postgres, Redis |
| **BettingEngine** | Python / FastAPI + SAM lambdas | 8002 | Bet placement, settlement orchestration, Kafka consumers | Postgres, Redis, Kafka, LocalStack/AWS, User, market data |
| **Bets** | Go / Fiber | (compose) | Not in use currently | Postgres, BettingEngine contracts |
| **BookmakerData** | Python / FastAPI | 8003 | Bookmaker odds API (+ worker) | Postgres, Redis; VPN path via Gluetun in VPN stacks |
| **FancyData** | Python / FastAPI | 8004 | Fancy markets API (+ worker) | Postgres, Redis; VPN path via Gluetun |
| **CasinoManagement** | Python / FastAPI | 8005 | Casino management API | Postgres, Redis |
| **LiveScore** | Python / FastAPI | 8006 | Live scores | Postgres / upstream feeds |
| **LiveTV** | Python / FastAPI | 8007 | Live TV metadata / streams | Upstream providers |
| **ManualDataManagement** | Python / FastAPI | 8008 | Operator overrides (odds/suspend); publishes odds-change notices | Redis, Postgres |
| **FrontMarket** | Go | 8010 | Market read path + odds SSE hub | Redis, Markets, upstream APIs |
| **Markets** | Go | 8012 | Market catalogue / market read service | Postgres, Redis |
| **MarketsProxy** | Go | (compose) | Proxy in front of markets path | Markets |
| **BackOffice** | Go | (compose) | Back-office APIs | Postgres, internal services |
| **BetfairStreaming** | Go | via stack / Gluetun on VPN | Live Betfair stream, catalogue-sync, dlq-worker | Kafka, Redis, Postgres, Betfair or emulator |
| **DataAggregator** | Go | (worker) | Kafka consumer → aggregated store / partitions | Kafka, Postgres |
| **emulators** | Go | 8089 REST (local) | Betfair API + stream mock | — |
| **Frontend-B2B** | Next.js | 3000 | Operator / B2B UI | APIs on localhost |
| **Frontend-B2C** | Next.js | 3001 | Customer UI | APIs on localhost |

Health convention fleet-wide: **`/livez`** (liveness) + **`/readyz`** (readiness). 

