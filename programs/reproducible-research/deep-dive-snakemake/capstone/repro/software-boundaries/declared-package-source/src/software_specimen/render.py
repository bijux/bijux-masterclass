from __future__ import annotations

import argparse
from pathlib import Path

SOFTWARE_MARKER = "declared-package-source-v1"


def render(source: Path, artifact: Path) -> None:
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text(
        f"{SOFTWARE_MARKER}\n{source.read_text(encoding='utf-8')}",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--artifact", type=Path, required=True)
    args = parser.parse_args()
    render(args.source, args.artifact)


if __name__ == "__main__":
    main()
