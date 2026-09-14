# C4 model

C4 is **Context, Containers, Components, and Code**. We maintain a [LikeC4](https://likec4.dev) model under `/c4` (ADR 0003). Mermaid stays on the [infra](/infra/) pages for sequences; LikeC4 is the navigable topology.

## **[Open interactive diagrams](/c4-workspace/)** (use this)

```bash
npm run c4:dev        # interactive UI with live reload
npm run c4:validate   # CI gate
npm run build         # export into docs site + VitePress
```

## Views

### Product (apps)

| View | Question |
|---|---|
| System context | Who uses FalconX? What is outside (Betfair, bookmaker feeds)? |
| Containers (apps) | Which EKS services, Lambda, Aurora, Valkey, MSK exist and how they talk |
| Money path | Place-bet → User / Bets / settlement Lambda |
| Odds & catalogue | Stream vs poll into FrontMarket / Markets |

### Infrastructure (platform)

| View | Question |
|---|---|
| Infra — System context | Users, GitHub, Groundcover, Sentry around FalconX |
| Infra — Request path | WAF → CloudFront → Traefik HTTPRoute → pod |
| Infra — Data plane | Aurora + DA, Valkey, MSK, Debezium outbox, Secrets Manager |
| Infra — Ship path | GitHub Actions → ECR → Argo CD → pods |
| Infra — Observability | Sensor → Groundcover; SDK → Sentry |
| Infra — AWS accounts | Develop+perf account vs prod account |
| Infra — Develop + perf | Shared VPC/EKS, two namespaces |
| Infra — Production | Dedicated VPC, cluster, data plane |

Source files: `c4/model.c4` (product) and `c4/infra.c4` (platform, deployment).

We do **not** model the Code level — it would rot immediately.

Written walkthrough of the same platform: [Infra](/infra/) · [Visual map](/infra/diagrams) · [Repos](/infra/repos/).
