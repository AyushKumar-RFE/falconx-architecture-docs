# Provisioning

Terraform builds AWS. Two layers: **library** then **this environment**.

```mermaid
flowchart LR
  T[tf-modules<br/>recipe] -->|source = git?ref=tag| I[rfetech-infra<br/>sizes for this env]
  I --> AWS[VPC EKS Aurora MSK Valkey ECR CloudFront]
  I --> Seed[Argo CD seed]
  G[rfetech-gitops] --> Seed
  Seed --> Running[add-ons + app pods]
```

```hcl
source = "git@github.com:rfetechnology/tf-modules.git//modules/AURORA?ref=<tag>"
```

Pin a **tag**. State lives in S3 on the infra stacks, not in `tf-modules`.

## Who owns what

```mermaid
flowchart TB
  TF[Terraform] --> Seed2[cluster, IAM, data plane, Argo CD, Traefik seed]
  GO[GitOps] --> Rest[Groundcover, Kyverno, KEDA, HTTPRoutes, replicas, image tags]
  SAM[SAM / github-actions] --> L[settlement Lambdas]
```

## Layout

```mermaid
flowchart TB
  ROOT[rfetech-infra/rfe-infra]
  ROOT --> DEV[rfe-dev<br/>many small stacks]
  ROOT --> PERF[rfe-perf<br/>overlays only]
  ROOT --> PROD[rfe-prod<br/>monolith + k8s/]
  ROOT --> GC[groundcover<br/>IAM role only]
```

| | Develop | Perf | Prod |
|---|---|---|---|
| Shape | one folder = one state | no VPC/EKS/MSK | `main.tf` + `k8s/` |
| State bucket | `rfe-terraform-state` | same | `rfe-infra-terraform-state` |

Ignore `Unwanted/`. No Terraform workspaces.

## Apply order (develop)

```mermaid
flowchart LR
  VPC[vpc] --> EKS[eks]
  EKS --> IAM[iam]
  EKS --> K8S[k8s]
  VPC --> ECR[ecr]
  VPC --> SG[security-groups]
  SG --> AUR[aurora]
  SG --> KFK[kafka]
  KFK --> DEB[debezium]
  KFK --> CFG[config_manager]
  AUR --> CFG
  WAF[waf] --> CF[cloudfront]
```

Plan in the **leaf**. If a plan wants to create a VPC, you are in the wrong folder.

**Modules by job:** network `VPC` `CLOUDFRONT` `WAF` · compute `EKS` `BASTION-SSM` · data `AURORA` `ELASTICACHE` `KAFKA` `MSK_CONNECT` `S3` · glue `ECR` `CONFIG_MANAGER`.

No ECS / DynamoDB module. The Traefik NLB is created by Kubernetes and passed into CloudFront.

## Change a module

```mermaid
flowchart LR
  B[branch tf-modules] --> L[optional local path in infra]
  L --> R[point infra at ?ref=branch]
  R --> M[merge + tag]
  M --> P[bump ref= in rfetech-infra PR]
```

Prod apply is the **manual** `github-aws-int.yaml` workflow (`workflow_dispatch`, infra-team approval), not a casual laptop apply and not apply-on-merge.

Step-by-step “which file, which PR”: [Changes](/infra/changes). New module/stack: [Creating things](/infra/repos/creating).

[Visual map](/infra/diagrams)
