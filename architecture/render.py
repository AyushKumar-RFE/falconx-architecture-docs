"""Render architecture diagrams into docs/architecture/."""

from pathlib import Path

import accounts
import prod_level1
import prod_network

OUT = Path(__file__).resolve().parents[1] / "docs" / "architecture"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    accounts.render()
    prod_level1.render()
    prod_network.render()
    print(f"rendered diagrams into {OUT}")


if __name__ == "__main__":
    main()
