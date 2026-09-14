# Compute & deploy

Workloads run on **EKS**. Delivery is **GitOps**: CI pushes an image and a git tag; Argo CD makes the cluster match.

```mermaid
flowchart LR
  Repo[service repo] --> CI[github-actions]
  CI --> ECR[ECR]
  CI --> Git[gitops image.tag]
  Git --> Argo[Argo CD]
  Argo --> NS[namespace]
```

| | Develop + perf | Prod |
|---|---|---|
| Cluster | `rfe-dev-cluster` | `rfe-prod-cluster` |
| Version / mode | 1.35 Auto Mode | 1.35 Auto Mode |
| App ns | `development` / `performance` | `production` |

```bash
aws eks update-kubeconfig --name rfe-dev-cluster --region eu-west-2 \
  --role-arn arn:aws:iam::460195068944:role/rfe-dev-cluster-admin-role \
  --alias rfe-dev-developer
```

## Two layers

```mermaid
flowchart TB
  R1[root falcon-apps-system] --> ADD[applications/env]
  ADD --> P[Traefik Groundcover KEDA Kyverno CSI ...]
  R2[root falcon-apps-env] --> AS[ApplicationSet]
  VAL[fantasy7-env/service/custom-values.yaml] --> AS
  AS --> CH[helm-templates/1.0.0]
  CH --> SVC[service Deployment + HTTPRoute]
```

**Platform:** develop gets the full add-on set (plus Kubecost / Chaos / k6). Prod is the production subset. Perf does **not** reinstall Traefik/Groundcover — they already run on the shared cluster.

**Services:** one Application per name in the ApplicationSet. Chart `1.0.0`. Health: `/livez` `/readyz`.

Prod list: `userservice` `bettingengine` `betfairstreaming` `bookmakerdata` `fancydata` `casinomanagement` `livescore` `livetv` `manualdatamanagement` `frontmarket` `backoffice` `bets` `frontend-b2b` `frontend-b2c` `dataaggregator` `markets`.

```mermaid
flowchart LR
  DevAS[develop/perf ApplicationSet] -->|forces| Off[HPA KEDA PDB off]
  ProdAS[prod] --> HPA[HPA CPU + memory]
```

## Commit → pod

```mermaid
sequenceDiagram
  participant S as service repo
  participant Q as sonar / trivy / gate
  participant B as build + push ECR
  participant G as update-helm-charts
  participant A as Argo CD
  participant E as EKS

  S->>Q: thin ci-cd-pipeline.yml
  Q->>B: proceed
  B->>G: tag V{run}-{semver}
  G->>A: fantasy7-env custom-values.yaml
  A->>E: sync
```

| Branch | ECR | GitOps folder |
|---|---|---|
| `main` | `{service}-develop` | `fantasy7-develop/` |
| `performance` | `{service}-perf` | `fantasy7-perf/` |
| `release/vX.Y.Z` | `{service}-prod` | `fantasy7-prod/` |

Never tag `latest`. Rollback = revert the GitOps commit (`rollback.yml`), not `kubectl rollout undo`.

**Walk the ship path:** Service `ci-cd-pipeline.yml` only *calls* `rfetech-github-actions`. After the quality gate, CI pushes `{service}-{env}:V{run}-{semver}` and commits `deployment.image.tag` under `fantasy7-<env>`. Argo’s ApplicationSet already renders chart `1.0.0` into the env namespace. Lambdas are SAM, not this path. Hop-by-hop: [Visual map § code change](/infra/diagrams#3-a-code-change).

Coordinated releases: “The Big Bash” / “The Patch” / `ship-release.yml`.

## Secrets

```mermaid
flowchart LR
  SM[Secrets Manager] --> CSI[CSI driver]
  CSI --> Vol[pod volume]
  Helm[custom-values.yaml] -.->|secretProvider class only| CSI
```

No credentials in Helm values. PreSync jobs wait until SecretProviderClass exists.

**Not GitOps:** settlement Lambdas (`build-lambda.yml`). Heat-event scale: `scale-data-plane.yml`.

Local: `falconx-local-dev:latest` + `make redeploy`. No Argo on a laptop.

[Visual map](/infra/diagrams)
