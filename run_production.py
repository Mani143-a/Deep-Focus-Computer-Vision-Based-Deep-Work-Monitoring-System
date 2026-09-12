from __future__ import annotations

"""
DeepFocus Production Launcher
==============================

Thin executable wrapper around the production deployment manager.

Usage
-----

    python run_production.py --preflight

    python run_production.py --preflight --json

    python run_production.py --run

    python run_production.py --run --require-ml
"""

import sys

from app.deployment import production_main


def main(
    argv: list[str] | None = None,
) -> int:
    """
    Run the DeepFocus production CLI.
    """

    return production_main(
        argv
    )


if __name__ == "__main__":
    raise SystemExit(
        main(
            sys.argv[1:]
        )
    )