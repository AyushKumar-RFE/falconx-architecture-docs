# Libraries

| Library | Lang | Role |
|---|---|---|
| **TestingCommon** | Python | Shared test helpers |
| **TransactionManager** | Python | Shared DB/tx + `common_obs` (pool metrics, obs) |
| **cacheking** | Go/Python boundary | Cache helpers used across services |
| **gofair** | Go | Betfair protocol / client primitives |
| **go-datastore** | Go | Shared datastore + `obs` for Go services |

Libraries generally run **lint + trivy + quality-gate** in CI (no SonarCloud project for libraries). Versioning policy lives with the library repos / Local docs (`library-versioning.md` in Local-dev-setup when present).
