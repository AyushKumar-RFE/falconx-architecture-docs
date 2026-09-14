# Local & isolated stack

**Local-dev-setup** runs compose. This docs repo does not. Same *services* as cloud, not the same *AWS*.

```mermaid
flowchart LR
  subgraph local [Laptop]
    IMG[falconx-local-dev]
    PG[(Postgres)]
    RD[(Redis)]
    KF[Kafka]
    LS[LocalStack]
    IMG --> PG
    IMG --> RD
    IMG --> KF
    IMG --> LS
  end
  subgraph cloud [Develop / prod]
    EKS[EKS + Argo]
    AU[(Aurora)]
    VK[(Valkey)]
    MSK[MSK]
  end
  local -.->|not this| cloud
```

```mermaid
flowchart LR
  S[make setup-local] --> ST[make start-local]
  ST --> E[make start-local-emulator]
  ST --> R[make redeploy SERVICE=]
  ST --> LOG[make logs-local]
  ST --> X[make stop]
```

No Argo, CloudFront, or Groundcover sensor on a laptop. Flags: `SENTRY=1` `OTEL=1` `REPLICA=1`, plus VPN / fullstack. VPN path: [Networking](/infra/networking).

```mermaid
flowchart LR
  CS[catalogue-sync] --> DM[debezium-migration]
  DM --> APIs[APIs start]
```

`depends_on` is real — no sleep barriers. Isolated CI (`make start-isolated*`) is the same topology with pre-built images.

Deep compose rules live in Local-dev-setup, not here.

[Visual map](/infra/diagrams) · [Environments](/infra/environments)
