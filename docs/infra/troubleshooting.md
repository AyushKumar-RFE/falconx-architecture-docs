# Troubleshooting

Safe commands only. They **read** cluster or AWS state. They do not delete production data.

Decide: **user cannot enter** (edge) vs **enter but 5xx** (app/data) vs **deploys stuck** (GitOps/CI) vs **async stale** (Kafka/CDC).

## Where to look first

| Symptom | Look |
|---|---|
| Browser TLS / 403 / maintenance page | CloudFront + WAF ([Networking](/infra/networking)) |
| 502 / 504 after CloudFront | Traefik pods, NodePools, HTTPRoute |
| 5xx JSON from an API | Groundcover + Sentry; pod logs; Aurora |
| Stale odds / SSE | Valkey; FrontMarket; feed workers |
| Bet placed, settlement missing | Lambda / EventBridge / SQS (not Argo) |
| New version not live | Argo OutOfSync; GitOps `image.tag`; ECR |
| Pending pods | Karpenter, taints, quotas ([Kubernetes](/infra/kubernetes)) |
| Laptop “no errors” | GlitchTip ingest / CrossSlot Redis |

Groundcover UI cluster: **Development** (includes perf namespace traffic) or **Production**. Grafana: `grafana.bigbash.life` / `grafana.bigbash.site` (oauth2-proxy). Sentry for user-facing errors.

## Useful read-only commands

```bash
# Context — you must already have kubeconfig from IAM role
kubectl config current-context
kubectl get nodes
kubectl get pods -n development          # or performance / production
kubectl describe pod -n production <pod> # events: pull/schedule/mount
kubectl logs -n production <pod> --tail=100
kubectl get httproute -A
kubectl get applications -n argocd
```

Do not `kubectl apply -f` product YAML. Do not `kubectl delete node` unless you own that incident.

Bastion (DB/Redis/Kafka): SSM port-forward scripts in `rfetech-infra` bastion folders — treat as break-glass.

## Playbooks

### 1. CloudFront 5xx / blank site

1. Does DNS still point at the distribution? (Route53 / ExternalDNS)
2. WAF: COUNT vs BLOCK. Perf BLOCK can 403 legitimate load tests.
3. Origin: internal NLB healthy? `kubectl -n traefik-cloudfront get pods,svc`
4. HTTPRoute hostname/path match the URL? Helm `httpRoutes` in `fantasy7-<env>/<service>/`
5. App `/readyz` failing → pod not in Service

Edge vs app: if S3 images load but API fails, origin/app. If nothing loads, WAF/CloudFront/DNS.

### 2. Image tag did not move

1. Did CI `quality-gate` `proceed`? Sonar/Trivy.
2. ECR: `{service}-{develop|perf|prod}` tag `V{run}-{semver}`
3. GitOps file `deployment.image.tag` on `main` (Deployment Bot commit)
4. Argo Application `<service>-<env>` Healthy/Synced
5. ImagePullBackOff → wrong account ECR / tag / node cannot pull

Rollback: `rollback.yml` or revert the GitOps commit — not `kubectl rollout undo` as process.

### 3. Pending pods / 502 after node loss

1. `kubectl get nodes` / `kubectl get pods -A | grep Pending`
2. `describe` pod: taint vs NodePool `nodetype`
3. NodePool CPU/memory **limits** hit in Karpenter
4. Spot interruption: expected; prod PDBs + overprovisioning should absorb. Develop has PDBs off.

### 4. Cannot connect to Postgres / Redis

1. From **inside** a pod, not your laptop, unless bastion port-forward
2. SecretProviderClass / CSI logs — wrong `config_{env}_{region}`
3. Aurora failover / RDS Proxy (prod) connection budget — fleet pools in GitOps connection-budget
4. Security group: only VPC CIDR should reach 5432/6379

### 5. Kafka / CDC lag

1. MSK connector `{env}-{service}-outbox-connector` running (MSK Connect console)
2. Topic exists in Terraform (`develop_*` / `perf_*` / `prod_*`) — apps do not auto-create
3. Consumer group lag (Groundcover / Kafka tooling)
4. Outbox table growing → Debezium down; OLTP still accepts writes

### 6. “Quiet” GlitchTip / Sentry locally

Zero errors is not a pass. Local GlitchTip must use **its own** Redis, not cluster-mode app Redis (CROSSSLOT).

## Application vs infrastructure

| Clue | Likely |
|---|---|
| One service 5xx, others OK | That app / its DB schema / its HTTPRoute |
| All gateway paths 502 | Traefik / NLB / nodes |
| All users 403 | WAF |
| Only perf namespace | perf Valkey/Debezium/Helm; shared Aurora **can** still be the cause |
| Only after a Terraform apply | Infra change — check that stack’s plan |

## Escalate when

You need prod `IAC_Role` apply, account-wide IAM, MSK broker replacement, or vendor Groundcover IAM. **infra-team** owns Terraform and prod GitOps. This page does not document a named on-call roster — that is not in these repos.

## What these repos do not say

- Named on-call / Slack escalation
- Numeric SLOs
- Live Alertmanager (chart has it **off**)
- Contents of service-repo `ci-cd-pipeline.yml` files (they only *call* reusable workflows)
- Local-dev-setup compose internals (separate repo)

## Related

[Observability](/infra/observability) · [Kubernetes](/infra/kubernetes) · [IAM & secrets](/infra/iam-and-secrets)
