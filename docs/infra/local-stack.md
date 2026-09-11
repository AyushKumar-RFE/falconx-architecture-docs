# Local & isolated stack

Orchestration repo: **Local-dev-setup** (this architecture docs repo does not run the stack).

## Everyday commands

```bash
make setup-local          # clone + build falconx-local-dev
make start-local          # APIs/workers
make start-local-emulator # + Betfair emulator
make redeploy [SERVICE=]  # rebuild image + recreate
make stop                 # teardown any variant
```

## Ordering (no nop barriers)

Real containers express `depends_on`. `debezium-migration` waits on catalogue-sync and acts as the last setup edge many APIs gate on.

## Isolated

CI uses pre-built images (`make start-isolated*`) — same topology ideas, different image source.

Keep this page short; deep compose rules live in Local-dev-setup `CLAUDE.md` / falconx-local-dev skill.
