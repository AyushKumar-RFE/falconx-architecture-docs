# Dependencies

What BigBash talks to **outside** a single service process. Internal service list: [catalog](/catalog/services). Live prod deploy list: GitOps ApplicationSet (see [rfetech-gitops](/infra/repos/rfetech-gitops)).

## AWS (in-VPC)

| Dependency | Used for | If it fails |
|---|---|---|
| Aurora `aurora-*` | OLTP, one database/schema per service | Writes/reads fail |
| Aurora `aurora-da-*` | Data Aggregator / partitions | Backoffice/DA lag; OLTP may still work |
| Valkey | Odds cache, sessions, pub/sub | Stale odds, session issues |
| MSK | Domain events + CDC topics | Async lag; placement may still hit SQL |
| MSK Connect / Debezium | Outbox → Kafka | Consumers starve; outbox table grows |
| S3 | CDN images, MFA QR, plugins, partitions | Images 404; MFA/plugins break |
| EventBridge `bus_{env}` | Market-closure style events | Those flows stall |
| SQS | Referenced by `livetv` Helm (`AWS_SQS_BASE_URL`) | LiveTV features degrade |
| ECR | Pull images | New pods cannot start |
| Secrets Manager | Config blob | CrashLoop / 500s |
| Lambda + EventBridge/SQS | BettingEngine **settlement** (SAM, not GitOps) | Bets may place; settlement stalls |

How a pod reaches data stores: private subnets + security groups from the VPC CIDR. No public RDS. [Networking](/infra/networking).

## Third-party (prod inventory)

Evidence from GitOps Helm env keys / architecture inventory — not guessed:

| System | Used by | Notes |
|---|---|---|
| **Betfair** | `betfairstreaming`, BettingEngine Betfair jobs | Stream + catalogue; local **emulators** replace this |
| **data.datafeed365.com** | `bookmakerdata`, `fancydata` | `THIRD_PARTY_SERVICE_URL` |
| **scoremaster.123scard.com** | `livescore` | `THIRDPARTY_SERVICE_URL` |
| **oddsdata.org** | `livetv`, frontends | Player / TV metadata |
| **Casino operators** | `casinomanagement` | Per-operator credentials in Secrets Manager |
| **skorekard.123scard.com** | Frontends | Scorecard UI |
| **Groundcover** | Cluster sensors | APM UI (vendor backend) |
| **Sentry** | App SDKs | Errors / traces |
| **GitHub** | All CI + GitOps | Actions, Argo repo |
| **Google Chat** | Trivy / ship notifications; Alertmanager *config* exists | Alertmanager is **disabled** in the kube-prometheus-stack base values we inspected — do not assume Chat is the live pager |

Local VPN compose: bookmaker/fancy/betfair paths egress via Gluetun. [Networking](/infra/networking).

## In-cluster platform

Traefik, ExternalDNS, cert-manager, Kyverno, KEDA, metrics-server, oauth2-proxy, Groundcover sensor, OTEL collector, kube-prometheus-stack. [rfetech-gitops](/infra/repos/rfetech-gitops).

## Service → data (prod, evidenced)

| Service | Ingress path (gateway) | Primary deps |
|---|---|---|
| `frontend-b2c` | `bigbash.site` | Gateway APIs, OTEL browser |
| `frontend-b2b` | `admin.bigbash.site` | Gateway, MDM websocket |
| `userservice` | `/userservice` | Aurora, Valkey, MSK `*_user_sync`, S3 MFA |
| `bettingengine` | `/bettingengine` | Aurora, Valkey, MSK, EventBridge, Fancy/BM/MDM/Casino |
| `betfairstreaming` | none (worker) | Betfair, Valkey, MSK DLQ, EventBridge |
| `bookmakerdata` | `/bookmakerdata` | DB, Valkey, markets, datafeed365 |
| `fancydata` | `/fancydata` | DB, Valkey, markets, datafeed365 |
| `markets` | `/markets` | DB, Valkey |
| `manualdatamanagement` | `/manualdatamanagement` | DB, Valkey, BE/Fancy/BM |
| `casinomanagement` | `/casinomanagement` | DB, Valkey, MSK, BE, userservice |
| `livescore` | `/livescore` | DB, Valkey, scoremaster |
| `livetv` | `/livetv` | DB, Valkey, oddsdata, SQS |
| `frontmarket` | `/frontmarket` | BE+BM DBs, Valkey |
| `backoffice` | `/backoffice` | DA DB + userservice DB, Valkey |
| `dataaggregator` | none | MSK, aurora-da, Valkey |

Gateway host prod: `gateway-prod.bigbash.site`. Exact HTTP edges: `rfetech-gitops` Helm `httpRoutes` (source of truth).

## Settlement Lambdas

C4 and the catalog describe BettingEngine triggering **AWS Lambda** on a settlement path (EventBridge → SQS → Lambda). Images/stacks ship with `build-lambda.yml` (SAM), **not** Argo. LocalStack needs `ssm` for `/rfe/lambda/vpc/*`. This repo does not contain the SAM templates — they live in the BettingEngine (or lambda) service repo.
