# Architecture diagrams (source)

Python [diagrams](https://diagrams.mingrammer.com/) using [AWS Architecture Icons](https://aws.amazon.com/architecture/icons/).

Rendered files live next to the page: `docs/architecture/*.png` and `*.svg`.

```bash
python3 -m venv architecture/.venv
architecture/.venv/bin/pip install -r architecture/requirements.txt
# requires Graphviz
PATH="/opt/homebrew/bin:$PATH" architecture/.venv/bin/python architecture/render.py
```

| Script | Output | Role |
|---|---|---|
| `prod_level1.py` | `prod-level1` | **Baseline** — design against this |
| `accounts.py` | `accounts` | Both AWS accounts |
| `prod_network.py` | `prod-network` | Level 2 AZs / CIDRs |

The published page is [Architecture baseline](../docs/architecture/index.md).
