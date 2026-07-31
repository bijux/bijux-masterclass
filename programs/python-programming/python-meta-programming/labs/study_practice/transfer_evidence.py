from __future__ import annotations

import argparse
import json

from .transfer import (
    CAPSTONE_TRANSFERS,
    transfer_for,
    transfer_target_evidence,
)


def build_transfer_evidence(*, module: int | None = None) -> dict[str, object]:
    """Publish one or all course-to-capstone transfer contracts."""

    transfers = (
        list(CAPSTONE_TRANSFERS)
        if module is None
        else [transfer_for(module)]
    )
    return {
        "primary_product": "course website and runnable course material",
        "transfer_rule": "focused course proof precedes observational capstone transfer",
        "constructed": False,
        "executed": False,
        "targets": transfer_target_evidence(),
        "transfers": [transfer.evidence() for transfer in transfers],
    }


def render_transfer_evidence(*, module: int | None = None) -> str:
    """Render stable JSON for learner inspection and documentation checks."""

    return json.dumps(
        build_transfer_evidence(module=module),
        indent=2,
        sort_keys=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render course-to-capstone transfer contracts.",
    )
    parser.add_argument(
        "--module",
        type=int,
        help="substantive module transfer to render, from 1 to 10",
    )
    args = parser.parse_args()
    print(render_transfer_evidence(module=args.module))


if __name__ == "__main__":
    main()
