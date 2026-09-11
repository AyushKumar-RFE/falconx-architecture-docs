# Critical flows

End-to-end paths engineers must understand before changing contracts.

| Flow | Why it matters | Page |
|---|---|---|
| Place bet → settle | Money path; lambdas + Kafka + User balances | [place-and-settle](/flows/place-and-settle) |
| Odds ingest | Latency & correctness of prices to FrontMarket/SSE | [odds-ingest](/flows/odds-ingest) |
| Catalogue sync | Markets exist before betting; gates local stack readiness | [catalogue-sync](/flows/catalogue-sync) |

Complementary C4 views live under [C4](/c4/).
