# C4 views

## System context

Actors (Customer, Operator) and external systems (Betfair, bookmaker/fancy feeds) around the FalconX software system.

## Containers

All major deployables: frontends, money-path services, odds/catalogue services, supporting product APIs, and data stores.

## Money path

Focused view for place-bet and settlement. Pair with [Place bet → settle](/flows/place-and-settle).

## Odds & catalogue

BetfairStreaming, DataAggregator, FrontMarket, Bookmaker/Fancy/MDM, stores. Pair with [Odds ingest](/flows/odds-ingest) and [Catalogue sync](/flows/catalogue-sync).

Open the [interactive workspace](./interactive) to click through relationships.
