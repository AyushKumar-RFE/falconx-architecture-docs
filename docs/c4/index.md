# C4 model

The structural model lives in **`/c4/model.c4`** (LikeC4).

## Where to look

| Link | What it is |
|---|---|
| This section (`/c4/…`) | Written guide (overview / views) |
| **[Interactive workspace](https://ayushkumar-rfe.github.io/falconx-architecture-docs/c4-workspace/)** | Clickable LikeC4 diagrams (use this) |
| Nav **Open diagrams** | Same interactive app |

## Views in the model

| View | Purpose |
|---|---|
| System context | FalconX vs customers, operators, Betfair, feeds |
| Containers | Deployable units inside FalconX |
| Money path | B2C → BettingEngine → User / Bets / lambdas |
| Odds & catalogue | Streaming, aggregator, FrontMarket, bookmaker/fancy |

## Edit loop

```bash
npm run c4:dev        # interactive UI with live reload
npm run c4:validate   # CI gate
npm run build         # export into docs site + VitePress
```
