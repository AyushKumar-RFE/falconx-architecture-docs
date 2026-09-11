# Place bet → settle

## Intent

Customer places a bet; system validates stakes/markets; eventual settlement updates balances via the settlement pipeline.

## Happy path (logical)

```mermaid
sequenceDiagram
  participant UI as Frontend-B2C
  participant BE as BettingEngine
  participant User as User
  participant Bets as Bets
  participant Bus as EventBridge/SQS
  participant L as Settlement lambdas
  participant Kafka as Kafka consumers

  UI->>BE: Place bet
  BE->>User: Auth / balance / limits
  BE->>Bets: Persist bet (schema owned by BE)
  BE-->>UI: Accepted
  Note over Bus,L: Market result / settle trigger
  Bus->>L: Settle message
  L->>User: Balance mutations
  L->>Kafka: Downstream events as designed
```

## Design notes (keep current)

- **In-play vs off-play** stake routing is market-state driven; match-interruption restriction flags were removed (do not reintroduce without ADR).
- Settlement lambdas read **secrets at runtime** — never reintroduce CloudFormation Secrets Manager dynamic refs (`resolve:secretsmanager`) that bake values at deploy time.
- Local/isolated lambdas deploy via **samconfig namespaces** only (`SAM_CONFIG_ENV`), not ad-hoc CLI parameter overrides.

## When you change this flow

Update this page + open an ADR if the bus, lambda set, or balance ownership changes.
