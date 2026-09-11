# Legacy / excluded

These repos may still be cloned but are **not** part of rollout, waves, or e2e by default.

| Repo | Status | Notes |
|---|---|---|
| **BetfairData** | LEGACY / UNUSED | Not in compose. **Not** the same as **BetfairStreaming** (live Go ingestion). |
| **OrderStreaming** | LEGACY | Expected reimplementation. CI historically stuck in startup_failure — do not spend time greening unless product revives it. |

Manifest exclusion: comment `LEGACY` / `DEPRECATED` / `UNUSED` above the entry in `local-repos.txt` so `wave.sh` skips them.
