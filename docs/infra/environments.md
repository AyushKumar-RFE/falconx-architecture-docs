# Environments

Five places code runs. Three are cloud. Two are compose.

```mermaid
flowchart LR
  L[local<br/>laptop compose] --> I[isolated<br/>CI e2e]
  I --> D[develop<br/>shared cloud]
  D --> P[perf<br/>same cluster]
  D --> R[prod<br/>own account]
```

| Env | Runs on |
|---|---|
| **local** | Docker Compose (`Local-dev-setup`) |
| **isolated** | Same topology, pre-built images |
| **develop** | Account `460195068944`, cluster `rfe-dev-cluster`, ns `development` |
| **perf** | **Same account + cluster**, ns `performance` |
| **prod** | Account `389068786427`, cluster `rfe-prod-cluster`, ns `production` |

Region: **`eu-west-2`**. WAF + CloudFront certs: **`us-east-1`**.

## Shared vs isolated

Perf is a namespace and a few overlays — not a copy of prod.

```mermaid
flowchart TB
  subgraph acc[Account 460195068944]
    VPC[rfe-dev-vpc]
    EKS[rfe-dev-cluster]
    VPC --> EKS
    EKS --> NS1[ns development]
    EKS --> NS2[ns performance]
    VPC --> SH[shared Aurora + MSK rfe-kafka]
    VPC --> RD[dev Valkey]
    VPC --> RP[perf Valkey]
  end
  subgraph prod[Account 389068786427]
    VPC2[rfe-prod-vpc]
    EKS2[rfe-prod-cluster]
    VPC2 --> EKS2 --> NS3[ns production]
    VPC2 --> OWN[own Aurora + MSK + Valkey]
  end
```

```mermaid
flowchart LR
  subgraph share [Develop + perf share]
    A[AWS account]
    V[VPC + NAT]
    C[EKS + Traefik + Groundcover]
    D[Aurora + MSK cluster]
  end
  subgraph split [Per env]
    N[K8s namespace]
    H[Helm values fantasy7-*]
    T[topic prefix develop_* / perf_*]
    R[Valkey + Debezium + CloudFront + ECR]
  end
```

| | Develop | Perf | Prod |
|---|---|---|---|
| Domain | `*.bigbash.life` | `*.bigbash.life` | `bigbash.site` |
| Hosts | `b2c-develop` `b2b-develop` `gateway-develop` | `*-perf` | `bigbash.site` `admin` `gateway-prod` |
| GitOps | `fantasy7-develop/` | `fantasy7-perf/` | `fantasy7-prod/` |

## Names in git

```mermaid
flowchart LR
  BB[BigBash product] --- FX[FalconX codebase]
  BB --- F7[fantasy7-* Helm folders]
  BB --- RFE[rfe-dev / rfe-prod Terraform]
  D[overlay folder 'dev'] --> DEV[means develop]
```

## Promotion

```mermaid
flowchart LR
  Loc[prove on compose] --> Main[merge to main]
  Main --> DevNS[CI → ECR -develop → Argo ns development]
  Main --> PerfBr[performance branch]
  PerfBr --> PerfNS[ECR -perf → ns performance]
  Main --> Rel[release / Big Bash]
  Rel --> ProdNS[ECR -prod → ns production]
```

Autoscaling is forced **off** in develop and perf ApplicationSets. Prod uses HPA.

[Visual map](/infra/diagrams) · [Compute & deploy](/infra/compute-and-deploy)
