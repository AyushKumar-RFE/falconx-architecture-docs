# Changes — where to edit, how it lands

An engineer should not grep the whole company to change one thing.

## If I need to change X

| Change | Repository | Path / mechanism |
|---|---|---|
| VPC CIDR, NAT, flow logs | `rfetech-infra` | `rfe-dev/vpc` or prod `main.tf` |
| How *every* VPC is built | `tf-modules` | `modules/VPC`, then bump `ref=` in infra |
| EKS version / Auto Mode | `rfetech-infra` | `eks/` or prod `main.tf` (`tf-modules/EKS`) |
| Karpenter NodePool | `rfetech-infra` | `rfe-dev/k8s/karpenter.tf` or `rfe-prod/k8s/files/k8s/*nodepool*` |
| Kafka topic | `rfetech-infra` | `rfe-dev/kafka/terraform.tfvars` `topic_names` **and** prod `main.tf` |
| Debezium connector | `rfetech-infra` | `rfe-dev/debezium`, `rfe-perf/debezium`, prod `main.tf` |
| Aurora / Valkey size | `rfetech-infra` | env `aurora/` `elasticache/` or prod `main.tf` |
| CloudFront aliases / WAF mode | `rfetech-infra` | `cloudfront/`, `waf/` |
| ECR repository | `rfetech-infra` | `ecr/terraform.tfvars` |
| Config secret keys (module-owned) | `tf-modules` `CONFIG_MANAGER` + infra `config_manager` | then apps read new fields |
| Ad-hoc Secrets Manager key | `rfetech-github-actions` | `update-secrets-manager.yml` |
| Traefik / Groundcover / Kyverno / KEDA | `rfetech-gitops` | `falcon-apps-of-apps/apps/<addon>/` |
| HTTPRoute, replicas, resources, secretProvider | `rfetech-gitops` | `helm-overrides/fantasy7-<env>/<service>/custom-values.yaml` |
| Which services exist in an env | `rfetech-gitops` | `app-services/<env>/application-set-*.yaml` |
| Image tag | CI | `update-helm-charts.yml` writes the values file |
| Lint / scan / Docker build | `rfetech-github-actions` | `.github/workflows/` |
| Connection pool numbers | `rfetech-gitops` | `.github/connection-budget/<env>.yaml` + sync workflow — **never** promote from develop |
| Heat-event Aurora/MSK scale | `rfetech-gitops` | `.github/scale-data-plane/` + `scale-data-plane.yml` |
| Architecture story / ADR | **this repo** | `docs/infra/`, `docs/adr/` |
| Laptop compose | `Local-dev-setup` | not this repo |

Cookbook (new service, new module): [Creating things](/infra/repos/creating).

## Infrastructure change flow (Terraform)

```text
Branch tf-modules and/or rfetech-infra
  → Pull request (infra-team CODEOWNERS)
  → terraform fmt / validate / plan (folder state)
  → Merge
  → Apply:
       develop: engineer or pipeline in that stack folder
       prod: github-aws-int.yaml  (workflow_dispatch: plan → infra-team approval → apply core, then k8s/)
  → AWS resources change
  → If Config Manager: pods see new secret on next mount/rotation
```

Rules: **one folder = one state**. Plan in the leaf. Pin module `?ref=` tags. SSH to GitHub for `terraform init`.

## Cluster change flow (GitOps)

```text
PR on rfetech-gitops
  → helm-validate-pr.yml (lint / connection-budget gate)
  → prod PRs: check-production-access.yml (infra-team)
  → Merge to main
  → Argo CD (prune + selfHeal) syncs
  → Pods / HTTPRoutes / add-ons update
```

Image-only deploys skip the Helm PR: CI commits the tag directly (Deployment Bot). Rollback: revert that commit (`rollback.yml`).

## Application deploy flow

```text
Developer pushes service repo
  → validate-branch / infra-team (manual)
  → Sonar + Trivy + quality-gate
  → build + push ECR  ({service}-{env}:V{run}-{semver})
  → update-helm-charts → fantasy7-{env}/…/custom-values.yaml
  → Argo CD syncs namespace development | performance | production
```

Lambdas: `build-lambda.yml` SAM → CloudFormation. Not Argo.

## Promote develop values → prod

GitOps `promote-to-prod.yml` copies *some* Helm keys. **Never** auto-promotes image tags, resources, replica counts, or `DB_POOL_*` / Redis pool env vars. Those are env-specific. [rfetech-gitops](/infra/repos/rfetech-gitops).
