# Infrastructure

Docs here **explain** environments, stores, and deploy paths.  
**Config truth** stays in:

| Concern | Source repos |
|---|---|
| AWS accounts / Terraform | `rfetech-infra`, `tf-modules` |
| Kubernetes / Helm / Argo | `rfetech-gitops` |
| Local & CI compose | `Local-dev-setup` |
| Reusable CI workflows | `rfetech-github-actions` |

Never paste secrets, DSNs with credentials, or full values files into this repo.

## Sections

- [Environments](/infra/environments)
- [Data stores](/infra/data-stores)
- [Compute & deploy](/infra/compute-and-deploy)
- [Networking](/infra/networking)
- [Observability](/infra/observability)
- [Local & isolated stack](/infra/local-stack)
