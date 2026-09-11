# C4 model

The structural model lives in **`/c4/model.c4`** (LikeC4). This section explains how to read and change it.

## Views defined

| View | Purpose |
|---|---|
| System context | FalconX vs customers, operators, Betfair, feeds |
| Containers | Deployable units inside FalconX |
| Money path | B2C → BettingEngine → User / Bets / lambdas |
| Odds & catalogue | Streaming, aggregator, FrontMarket, bookmaker/fancy |

See [Views](./views) and [Interactive workspace](./interactive).

## Edit loop

```bash
npm run c4:dev        # interactive UI with live reload
npm run c4:validate   # CI gate
npm run c4:build      # export into docs/public/c4 for the docs site
```
