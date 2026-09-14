# Kubernetes (EKS)

Application containers run on **Amazon EKS** (Elastic Kubernetes Service) version **1.35** in **Auto Mode**. AWS owns more of the data-plane node lifecycle than a classic managed node group. We still declare **Karpenter NodePools** (which instance families, spot vs on-demand, taints).

There is **no service mesh** (no Istio). East-west traffic is ClusterIP plus VPC security groups to Aurora / Valkey / MSK.

## Clusters and namespaces

| | Develop + perf | Prod |
|---|---|---|
| Cluster | `rfe-dev-cluster` | `rfe-prod-cluster` |
| Account | `460195068944` | `389068786427` |
| App namespaces | `development`, `performance` | `production` |
| Seed (Terraform) | `rfetech-infra/.../rfe-dev/eks` + `k8s/` | `rfe-prod/main.tf` + `rfe-prod/k8s/` |
| Desired apps | GitOps ApplicationSet | same, `fantasy7-prod` |

**Kubeconfig (develop):**

```bash
# Uses your IAM role; refreshes credentials for this context
aws eks update-kubeconfig \
  --name rfe-dev-cluster \
  --region eu-west-2 \
  --role-arn arn:aws:iam::460195068944:role/rfe-dev-cluster-admin-role \
  --alias rfe-dev-developer
```

Prod: cluster `rfe-prod-cluster`, admin role in account `389068786427`. Roles: `{cluster}-admin-role`, `-developer-role`, `-poweruser-role` via EKS Access Entries (`rfetech-infra` `iam/`).

## What Terraform installs vs GitOps

Terraform **seeds**: cluster, IAM, Karpenter NodePools, Argo CD, cert-manager identity, storage class, often Traefik/ingress on prod `k8s/`.

GitOps **owns** after Argo exists: Groundcover, Kyverno, KEDA, oauth2-proxy, product Deployments, HTTPRoutes. See [Compute & deploy](/infra/compute-and-deploy).

## Karpenter NodePools

**Karpenter** watches unschedulable pods and launches EC2 nodes that match a NodePool. Develop pools are `kubernetes_manifest` in `rfetech-infra/rfe-infra/rfe-dev/k8s/karpenter.tf`. Prod pools are YAML under `rfe-prod/k8s/files/k8s/`. They use `apiVersion: karpenter.sh/v1` and NodeClass `default` (`eks.amazonaws.com` — Auto Mode).

Pools you will see (names from develop Terraform):

| NodePool | Typical use |
|---|---|
| `on-demand` | amd64 on-demand, tainted `nodetype=on-demand` |
| spot (amd64) | cheaper stateless x86 |
| `spot-perf` | perf-oriented spot |
| `graviton-spot` | arm64 spot |
| `graviton-tainted-workload-on-demand` / `-spot` | label `nodetype=graviton-tainted-workload` — Traefik often schedules here |

Prod YAML (same idea, more files): `on-demand-nodepools.yaml`, `spot-nodepools.yaml`, `graviton-spot-nodepool.yaml`, `tainted-*-nodepool.yaml`, `high-cpu-mem-multiarch-nodepools.yaml` under `rfe-prod/k8s/files/k8s/`.

Disruption: `WhenEmptyOrUnderutilized`, `consolidateAfter` about `1m`, budget ~10% of nodes. `expireAfter` on some pools (e.g. 480h). CPU/memory **limits** cap how large the pool can grow.

Workloads that must not land on the wrong arch/taint set `nodeSelector` / `tolerations` in Helm or add-on values (cert-manager comments: graviton spot).

**Prod** also has `cluster-overprovisioning` (GitOps) so scale-up has spare pods already scheduled.

### What happens when a node is terminated?

1. Karpenter or AWS reclaims the instance (spot interruption, consolidation, expiry).
2. Pods get evicted. **PodDisruptionBudgets** in **prod** Helm limit how many die at once. Develop/perf ApplicationSets **force PDBs off**.
3. Kubernetes reschedules pods. If no matching node exists, Karpenter creates one from the NodePool.
4. Until then, that replica is gone. HPA (prod) may add replicas if CPU/memory rise. Develop replica counts are pinned in the ApplicationSet.

If Traefik pods cannot schedule (wrong taint), **all** public API/UI via CloudFront 502s. That is why ingress is pinned to known NodePools.

## Ingress inside the cluster

Public users do not hit a Kubernetes LoadBalancer that is internet-facing for product traffic. See [Networking](/infra/networking): CloudFront → **internal** NLB in namespace `traefik-cloudfront` → Gateway API HTTPRoute → Service → pod.

Health: **`/livez`** (liveness), **`/readyz`** (readiness).

## If EKS / Karpenter fails

| Failure | User impact | What to check |
|---|---|---|
| API server / control plane | `kubectl` fails; existing pods may still run | AWS EKS console / Groundcover |
| Karpenter cannot launch nodes | Pending pods, 502s as replicas drain | NodePool limits, quotas, taints |
| Wrong nodeSelector | Add-on or app Pending forever | Helm values vs NodePool labels |
| Argo CD down | No new deploys; traffic OK | Argo UI / `argocd` namespace |

[Troubleshooting](/infra/troubleshooting) · [Compute & deploy](/infra/compute-and-deploy)
