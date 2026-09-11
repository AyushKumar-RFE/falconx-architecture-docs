# Networking

## Local VPN path

When using `make start-local-vpn` (etc.):

- `bookmakerdata`, `fancydata`, workers, `betfairstreaming`, catalogue-sync use `network_mode: service:gluetun`
- Consumers reach them at `http://gluetun:8003` / `:8004`
- Host ports publish on Gluetun
- Colliding health ports on shared netns: e.g. fancy worker `HEALTH_PORT=8081`

## Frontends

Fullstack targets: B2B/B2C use **`network_mode: host`** so browser and SSR share `localhost` URLs.

## Cloud

Document VPC/mesh details by linking the Terraform module paths in `rfetech-infra` (do not duplicate CIDRs here unless needed for an ADR).
