from __future__ import annotations

import argparse

from .evidence import render_study_evidence


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render the course-first study and reentry route.",
    )
    parser.add_argument(
        "--last-trusted-module",
        type=int,
        default=0,
        help="last module whose exit evidence you can still explain, from 0 to 10",
    )
    args = parser.parse_args()
    print(render_study_evidence(last_trusted_module=args.last_trusted_module))


if __name__ == "__main__":
    main()
