# Visual map

Skim this page first. Each diagram is one idea. Captions are short on purpose.

**Want the repo-by-repo detail?** [Four repos](/infra/repos/) · [Creating things](/infra/repos/creating)

The three flows to learn first: **[request](#2-a-user-request)** · **[ship](#3-a-code-change)** · **[data / CDC](#7-data-plane)**. Plus **[infra change](#13-an-infrastructure-change)** and the **[cloud tree](#0-cloud-layout)**. Each diagram has a short “when to look” note.

## 0. Cloud layout

**What:** One tree of the AWS account as we actually run it. **When to look:** first hour on the team. **Notice:** perf is a namespace under develop’s cluster, not a third account. WAF/CloudFront certs are us-east-1; the VPC is eu-west-2.

```mermaid
flowchart TB
  subgraph cloud [AWS]
    subgraph net [Network]
      VPC[VPC + subnets]
      SG[security groups]
      NAT[NAT + SSM bastion]
    end
    subgraph k8s [Kubernetes]
      EKS[EKS Auto Mode]
      KP[Karpenter NodePools]
      NS[app namespaces]
      ING[Traefik + HTTPRoute]
      EKS --> KP --> NS
      ING --> NS
    end
    subgraph data [Data]
      AU[(Aurora + aurora-da)]
      VK[(Valkey)]
      MSK[MSK + Debezium]
    end
    subgraph obs [Observability]
      GC[Groundcover]
      SE[Sentry]
      GR[Grafana / Prometheus]
    end
    subgraph ext [Edge + vendors]
      CF[CloudFront + WAF]
      BF[Betfair / feeds]
    end
  end
  CF --> ING
  NS --> AU
  NS --> VK
  NS --> MSK
  NS --> GC
  NS --> SE
  NS -.-> BF
```

Interactive: [C4 workspace](/c4/) · narrative: [Overview](/infra/)

---

## 1. The whole system

**What:** Four Git repos around one region. **When to look:** after the cloud tree, before diving into a single hop.

Four repos. One AWS region (`eu-west-2`). Traffic in from the left, code in from the top.

```mermaid
flowchart TB
  subgraph git [Git]
    Mods[tf-modules<br/>recipes]
    Infra[rfetech-infra<br/>AWS per env]
    Actions[rfetech-github-actions<br/>CI workflows]
    GitOps[rfetech-gitops<br/>cluster desired state]
    Svc[Service repos]
  end

  subgraph edge [Public edge]
    WAF[WAF us-east-1]
    CF[CloudFront]
    S3[S3 images]
  end

  subgraph vpc [VPC private]
    Traefik[Traefik NLB]
    EKS[EKS pods]
    Aurora[(Aurora)]
    Valkey[(Valkey)]
    MSK[MSK Kafka]
    Deb[Debezium]
  end

  Mods --> Infra
  Infra --> vpc
  Svc --> Actions
  Actions --> ECR[ECR]
  Actions --> GitOps
  GitOps --> EKS
  User[User] --> WAF --> CF
  CF --> S3
  CF --> Traefik --> EKS
  EKS --> Aurora
  EKS --> Valkey
  EKS --> MSK
  Aurora --> Deb --> MSK
```

[Overview](/infra/) · [Provisioning](/infra/provisioning) · [Compute & deploy](/infra/compute-and-deploy)

---

## 2. A user request

The browser never talks to a Kubernetes pod. DNS for `bigbash.site` / `bigbash.life` points at **CloudFront**. WAF is attached to that distribution (it must live in **us-east-1**). After WAF, CloudFront either serves a **cached file from S3** or forwards into the VPC.

```mermaid
sequenceDiagram
  actor User
  participant WAF
  participant CloudFront
  participant S3
  participant Traefik
  participant Pod
  participant Aurora
  participant Valkey

  User->>WAF: HTTPS to b2c / admin / gateway host
  WAF->>CloudFront: COUNT or BLOCK
  alt static image
    CloudFront->>S3: /B2C/images or /B2B/images
    S3-->>User: file
  else API or UI
    CloudFront->>Traefik: VPC origin internal NLB
    Traefik->>Pod: HTTPRoute host + path
    Pod->>Aurora: SQL
    Pod->>Valkey: cache
    Pod-->>User: HTML / JSON / SSE
  end
```

```mermaid
flowchart LR
  U[User] --> H1[b2c / admin / gateway host]
  H1 --> CF[CloudFront + WAF]
  CF -->|images| S3[S3]
  CF -->|app| NLB[internal Traefik NLB]
  NLB --> R[HTTPRoute]
  R --> P[service pod]
```

**Hop by hop**

1. **DNS** — Prod: `bigbash.site` (B2C), `admin.bigbash.site` (B2B), `gateway-prod.bigbash.site` (APIs). Develop/perf: same three roles on `bigbash.life` with `-develop` / `-perf`. ExternalDNS keeps Route53 in sync from HTTPRoute hostnames.
2. **WAF** — Rate limits (gateway vs B2C vs B2B, auth vs anonymous, global ceiling), AWS managed rules, optional maintenance kill-switch. **COUNT** = log only (develop/prod today). **BLOCK** = enforce (perf). A 403 here never reached Traefik.
3. **CloudFront** — Terminates TLS. Path `/B2C/images/*` and `/B2B/images/*` go to S3 + OAC. Everything else is a **VPC origin** to an **internal** NLB (not on the public internet).
4. **Traefik CloudFront** — In namespace `traefik-cloudfront`. Gateway API `HTTPRoute` matches **host + path** (example: `gateway-prod.bigbash.site` `/frontmarket` → FrontMarket). A second Traefik (`traefik-external`) is for Grafana and tools, not this public product path.
5. **Pod** — ClusterIP Service. Reads Aurora and/or Valkey. Response goes back the same way. There is no service mesh.

If this hop fails, see [Networking](/infra/networking). Interactive C4: **Infra — Request path**.

---

## 3. A code change

Nobody `kubectl apply`s product apps. The service repo calls **reusable workflows**. Those workflows push an image and **commit a tag in GitOps**. Argo CD is the only thing that talks to the Kubernetes API for that deploy.

```mermaid
sequenceDiagram
  actor Dev
  participant Repo as Service repo
  participant GHA as github-actions
  participant ECR
  participant GitOps as rfetech-gitops
  participant Argo as Argo CD
  participant EKS

  Dev->>Repo: push / release
  Repo->>GHA: thin ci-cd-pipeline.yml
  GHA->>GHA: Sonar + Trivy + quality-gate
  GHA->>ECR: push V{run}-{semver}
  GHA->>GitOps: bump image.tag in fantasy7-env
  Argo->>GitOps: watch
  Argo->>EKS: sync pod
```

```mermaid
flowchart LR
  B1[main] --> D[develop ECR + fantasy7-develop]
  B2[performance] --> P[perf ECR + fantasy7-perf]
  B3[release/vX.Y.Z] --> R[prod ECR + fantasy7-prod]
  D --> NS1[namespace development]
  P --> NS2[namespace performance]
  R --> NS3[namespace production]
```

**Hop by hop**

1. **Push** — `main` → develop, `performance` → perf, `release/vX.Y.Z` → prod. Manual deploys also check branch + `infra-team`.
2. **Qualify** — `sonar.yml` + `trivy-fs-scan.yml` (+ lint). `quality-gate.yml` sets `proceed`. A reusable-workflow crash must not hide other checks — keep extra tests in a **sibling** workflow.
3. **Build** — `extract-version.yml` makes tag **`V{run}-{semver}`** (never `latest`). `build-docker-image.yml` Buildx + image scan; `push-ecr-image.yml` writes `{service}-{develop|perf|prod}` in ECR `eu-west-2`.
4. **GitOps** — `update-helm-charts.yml` sets `deployment.image.tag` in `helm-overrides/fantasy7-<env>/<service>/custom-values.yaml` (rebase retry if two ships collide).
5. **Argo CD** — ApplicationSet already points that folder at chart `helm-templates/1.0.0`. It syncs the Deployment in `development` / `performance` / `production`. Rollback = **revert that GitOps commit**, not `kubectl rollout undo`.

Settlement Lambdas skip this path (`build-lambda.yml` / SAM). C4: **Infra — Ship path**.

[Compute & deploy](/infra/compute-and-deploy) · [Environments](/infra/environments) · [Creating things](/infra/repos/creating)

---

## 4. Where code runs

Perf is **not** a third AWS account. It is a namespace on the develop cluster, plus a few overlay stacks.

```mermaid
flowchart TB
  subgraph laptop [Laptop / CI]
    L[local compose]
    I[isolated compose]
  end

  subgraph a1 [Account 460195068944 · eu-west-2]
    VPC1[rfe-dev-vpc 10.10.0.0/16]
    EKS1[rfe-dev-cluster]
    VPC1 --> EKS1
    EKS1 --> N1[development]
    EKS1 --> N2[performance]
    VPC1 --> Shared[shared Aurora + MSK]
    VPC1 --> R1[dev Valkey]
    VPC1 --> R2[perf Valkey]
  end

  subgraph a2 [Account 389068786427 · eu-west-2]
    VPC2[rfe-prod-vpc 10.30.0.0/16]
    EKS2[rfe-prod-cluster]
    VPC2 --> EKS2 --> N3[production]
    VPC2 --> Own[own Aurora + MSK + Valkey]
  end

  L -.->|same services, not AWS| N1
  I -.->|e2e images| N1
```

```mermaid
flowchart LR
  Local[local] --> Isolated[isolated CI]
  Isolated --> Develop[develop]
  Develop --> Perf[perf]
  Develop --> Prod[prod]
```

[Environments](/infra/environments)

---

## 5. How AWS is built

`tf-modules` = recipe. `rfetech-infra` = this environment's sizes. GitOps = what runs on the cluster after the seed exists.

```mermaid
flowchart LR
  M[tf-modules] -->|source = git ...?ref=tag| I[rfetech-infra]
  I -->|creates| AWS[VPC EKS Aurora MSK Valkey ECR]
  I -->|seeds| Argo[Argo CD]
  G[rfetech-gitops] --> Argo
  Argo --> Apps[add-ons + services]
```

```mermaid
flowchart TB
  VPC[vpc] --> EKS[eks]
  EKS --> IAM[iam]
  EKS --> K8S[k8s seed]
  VPC --> SG[security-groups]
  SG --> AUR[aurora]
  SG --> KFK[kafka]
  KFK --> DEB[debezium]
  KFK --> CFG[config_manager]
  AUR --> CFG
  WAF[waf] --> CF[cloudfront]
```

Develop = many small folders. Perf = overlays only. Prod = one core stack + `k8s/`.

[Provisioning](/infra/provisioning)

---

## 6. Inside the VPC

Public subnet: NAT + SSM bastion only. Data stores have no public IP.

```mermaid
flowchart TB
  subgraph public [Public subnets]
    NAT[NAT Gateway]
    Bastion[SSM bastion]
  end
  subgraph private [Private subnets]
    Pods[EKS pods]
    DB[(Aurora :5432)]
    Cache[(Valkey :6379)]
    Kafka[MSK :909x]
    Connect[MSK Connect]
  end
  Internet1[Internet out] --> NAT --> Pods
  Eng[Engineer] -->|Session Manager| Bastion
  Bastion -.->|port-forward| DB
  Bastion -.->|port-forward| Cache
  Bastion -.->|port-forward| Kafka
  Pods --> DB
  Pods --> Cache
  Pods --> Kafka
  Connect --> DB
  Connect --> Kafka
```

[Networking](/infra/networking) · [Data stores](/infra/data-stores)

---

## 7. Data plane

Synchronous work is SQL + cache. Asynchronous work is **Kafka**. Three services also write an **outbox table in the same Postgres transaction** as the business row. Debezium (MSK Connect) copies those rows to Kafka so consumers like DataAggregator **never poll OLTP**.

```mermaid
flowchart LR
  subgraph services [Pods]
    US[userservice]
    BE[bettingengine]
    CM[casinomanagement]
    DA[dataaggregator]
    Others[other APIs]
  end

  subgraph data [Managed stores]
    OLTP[(aurora main)]
    DADB[(aurora-da)]
    Redis[(Valkey)]
    Bus[EventBridge]
  end

  subgraph async [CDC + messaging]
    Outbox[outbox_events]
    Deb[Debezium]
    Kafka[MSK]
  end

  US --> OLTP
  BE --> OLTP
  CM --> OLTP
  Others --> OLTP
  Others --> Redis
  BE --> Redis
  OLTP --> Outbox --> Deb --> Kafka --> DA
  DA --> DADB
  BE --> Kafka
  BE --> Bus
```

**Hop by hop**

1. **API** — e.g. BettingEngine writes the bet **and** an `outbox_events` row in one transaction on **aurora main** (database/schema per service).
2. **Debezium** — Connector `{env}-{service}-outbox-connector` for **userservice**, **bettingengine**, **casinomanagement**. Plugin ZIP on env S3. Needs `rds.logical_replication=1`.
3. **MSK** — Topics are Terraform, prefix `develop_*` / `perf_*` on shared `rfe-kafka`, `prod_*` on prod. Families include `bet_placed`, `market_settlement`, `user_sync`, plus `failed_*` and `dlq_*` twins. Apps do not auto-create topics.
4. **Consumer** — DataAggregator reads Kafka and writes **aurora-da**. Other consumers subscribe to domain topics BettingEngine produces directly (not only CDC).
5. **Cache / bus** — Valkey is odds, sessions, pub/sub (cluster-mode). EventBridge `bus_{env}` is market-closure style events, not the main bet bus.
6. **Sharing** — Perf **shares** develop Aurora + MSK (different topic prefix + own Debezium + own Valkey). Prod shares nothing.

C4: **Infra — Data plane**. Detail: [Data stores](/infra/data-stores).

---

## 8. GitOps on the cluster

Two roots per environment. Left = platform. Right = BigBash services.

```mermaid
flowchart TB
  subgraph roots [Applied once]
    R1[falcon-apps-system]
    R2[falcon-apps-develop / perf / prod]
  end

  R1 --> A1[applications/env/*.yaml]
  A1 --> P[Traefik Groundcover KEDA Kyverno secrets-store ...]

  R2 --> AS[ApplicationSet]
  AS --> H[helm-templates/1.0.0]
  V[fantasy7-env/service/custom-values.yaml] --> AS
  H --> S[userservice bettingengine frontends ...]
```

[Compute & deploy](/infra/compute-and-deploy)

---

## 9. Secrets

**What:** How pods get DB/Kafka/Valkey settings. **When to look:** CrashLoop on mount, or a new env key. Detail: [IAM & secrets](/infra/iam-and-secrets).

Credentials never live in Helm values. Config Manager builds one Secrets Manager document. CSI mounts it into the pod.

```mermaid
flowchart LR
  Aurora[(Aurora secret)] --> CM[CONFIG_MANAGER]
  MSK[MSK secret] --> CM
  Valkey[Valkey endpoint] --> CM
  CM --> SM[Secrets Manager<br/>config_env_region]
  SM --> CSI[Secrets Store CSI]
  CSI --> Pod[pod volume / K8s Secret]
```

[Compute & deploy](/infra/compute-and-deploy)

---

## 10. Observability

Groundcover is the cloud default. Sentry is errors. Prometheus is HPA CPU/memory. Local is GlitchTip + optional OTel.

```mermaid
flowchart LR
  Pod[pod]
  Node[node]
  Pod -->|OTLP| OTEL[OTEL collector]
  OTEL --> Sensor[Groundcover sensor]
  Node -->|eBPF logs/traces| Sensor
  Sensor --> GC[Groundcover UI]
  Pod -->|SDK| Sentry[Sentry]
  Node --> Prom[Prometheus / Grafana]
  Prom --> HPA[HPA]
```

[Observability](/infra/observability)

---

## 11. Local vs cloud

Same services. Different everything else.

```mermaid
flowchart TB
  subgraph local [Local-dev-setup]
    Img[falconx-local-dev image]
    PG[(Postgres :5432)]
    RD[(Redis :6379)]
    KF[Kafka :9092]
    LS[LocalStack :4566]
    GT[GlitchTip :8000]
    Img --> PG
    Img --> RD
    Img --> KF
    Img --> LS
  end

  subgraph cloud [Develop / prod]
    EKS[EKS + Argo CD]
    AU[(Aurora)]
    VK[(Valkey)]
    MSK[MSK]
    AWS[real AWS]
    EKS --> AU
    EKS --> VK
    EKS --> MSK
    EKS --> AWS
  end
```

```mermaid
flowchart LR
  S[make setup-local] --> ST[make start-local]
  ST --> R[make redeploy]
  R --> L[make logs-local]
  ST --> X[make stop]
```

[Local & isolated stack](/infra/local-stack)

---

## 12. Where to edit

**What:** Decision tree for which GitHub repo owns the change. **When to look:** before you open a PR. Full table: [Where to change](/infra/changes).

```mermaid
flowchart TB
  Q{What are you changing?}
  Q -->|how every VPC/MSK is built| TM[tf-modules then bump ref]
  Q -->|this env's size / topic / CIDR| INF[rfetech-infra]
  Q -->|cluster add-on| AOA[gitops falcon-apps-of-apps]
  Q -->|replicas / route / image / secrets mount| HV[gitops helm-overrides]
  Q -->|build / scan / ship| GHA[rfetech-github-actions]
  Q -->|the story / a decision| DOC[this repo + ADR]
```

---

## 13. An infrastructure change

**What:** How Terraform or GitOps reaches AWS/the cluster. **When to look:** you are not shipping an app image. **Notice:** prod Terraform is the **manual** `github-aws-int.yaml` workflow (`workflow_dispatch`) with **infra-team** approval. Image-only deploys skip this — they are flow 3.

```mermaid
sequenceDiagram
  actor Eng as Engineer
  participant Repo as tf-modules / infra / gitops
  participant CI as validate / plan
  participant Gate as infra-team
  participant Cloud as AWS or Argo CD

  Eng->>Repo: pull request
  Repo->>CI: fmt, validate, plan or helm-lint
  CI->>Gate: prod apply / prod GitOps
  Gate->>Cloud: apply or Argo sync
```

```text
Infra code → PR → review → CI (plan / helm-validate)
  → develop: apply in the leaf folder, or merge GitOps for Argo
  → prod: github-aws-int.yaml (workflow_dispatch: plan → approval → apply) or GitOps + infra-team
  → Cloud / cluster
```

Hop-by-hop: [Changes](/infra/changes). C4: **Infra — Kubernetes compute** (nodes) · **Infra — Ship path** (apps).
