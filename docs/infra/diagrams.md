# Visual map

Skim this page first. Each diagram is one idea. Captions are short on purpose.

**Want the repo-by-repo detail** (every Terraform stack, Argo add-on, CI workflow)? Start at [Four repos](/infra/repos/).

## 1. The whole system

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

Browser never talks to a pod. CloudFront is the front door. Static images stop at S3.

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

  User->>WAF: HTTPS
  WAF->>CloudFront: allow / count
  alt static image
    CloudFront->>S3: /B2C/images or /B2B/images
    S3-->>User: file
  else API or UI
    CloudFront->>Traefik: VPC origin internal NLB
    Traefik->>Pod: HTTPRoute host + path
    Pod->>Aurora: SQL
    Pod->>Valkey: cache
    Pod-->>User: response
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

Prod hosts: `bigbash.site` (B2C), `admin.bigbash.site` (B2B), `gateway-prod.bigbash.site` (APIs). Develop/perf use the same roles on `bigbash.life`.

[Networking](/infra/networking)

---

## 3. A code change

No `kubectl apply`. CI writes git. Argo CD copies git onto the cluster.

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

[Compute & deploy](/infra/compute-and-deploy) · [Environments](/infra/environments)

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

One Aurora for OLTP (database per service). Second Aurora for Data Aggregator. Kafka for async. Debezium copies outbox rows so consumers never poll OLTP.

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

Connectors: userservice, bettingengine, casinomanagement. Topic prefixes: `develop_*` / `perf_*` on the **same** MSK cluster; `prod_*` on prod MSK.

[Data stores](/infra/data-stores)

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
