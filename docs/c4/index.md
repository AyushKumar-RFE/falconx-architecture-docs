# C4 model

### C4 stands for Context, Containers, Components, and Code.

## **[Link](https://ayushkumar-rfe.github.io/falconx-architecture-docs/c4-workspace/)** | LikeC4 diagrams (use this) |

## Views in the model

| View | Purpose |
|---|---|
| System context | The highest level of view. software system as a single box in the center, surrounded by the people who use it and the other external systems it talks to.|
| Containers | A zoom-in on your software system. separately deployable applications that make up the system such as server-side API, or a database. |
| Component | A zoom-in on one specific container. B2C → BettingEngine → User / Bets / lambdas, For each componete you can see Inbound and OutBound services (i.e Relationships), Structure, Properties, Deployment Info|
| Code | We are not implementing it since maintaing it will be very hard. |

## For Editing this digram, Clone repo and run this.

```bash
npm run c4:dev        # interactive UI with live reload
npm run c4:validate   # CI gate
npm run build         # export into docs site + VitePress
```
