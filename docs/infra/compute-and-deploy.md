# Compute & deploy

## Local

- One toolchain + baseline image: `falconx-local-dev:latest`
- Edit → run loop: **`make redeploy`** (Compose Watch removed)
- No application bind mounts (OrbStack inotify gap)

## Cloud

- Workloads on Kubernetes via **Argo CD / Helm** (`rfetech-gitops`)
- Images from CI (`rfetech-github-actions` reusable workflows)
- Settlement **AWS Lambda** (SAM) for BettingEngine settlement path
- VPC details for lambdas via **SSM** (`/rfe/lambda/vpc/*`) — `ssm` required in LocalStack `SERVICES`

## CI shape (per service repo)

`ci-cd-pipeline.yml` should call **only** shared reusable workflows; repo-specific tests live in separate workflow files so a reusable startup failure does not hide checks.
