from __future__ import annotations

import argparse
from pathlib import Path

from incident_escalation_capstone.common import read_json, sha256_file


def verify_manifest(publish_dir: Path) -> None:
    manifest = read_json(publish_dir / "manifest.json")
    artifacts = manifest["artifacts"]
    if not artifacts:
        raise ValueError("publish manifest must list at least one artifact")

    for entry in artifacts:
        target = publish_dir / entry["path"]
        if not target.exists():
            raise FileNotFoundError(f"manifest target missing: {entry['path']}")
        digest = sha256_file(target)
        if digest != entry["sha256"]:
            raise ValueError(f"sha256 mismatch for {entry['path']}: {digest} != {entry['sha256']}")


def verify_metrics(publish_dir: Path) -> None:
    metrics = read_json(publish_dir / "metrics.json")
    for field in ("accuracy", "precision", "recall", "f1"):
        value = float(metrics[field])
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"{field} must be between 0 and 1, got {value}")
    if int(metrics["eval_rows"]) < 3:
        raise ValueError("eval_rows must be at least 3 for this capstone")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--publish", type=Path, required=True)
    args = parser.parse_args()

    verify_manifest(args.publish)
    verify_metrics(args.publish)


if __name__ == "__main__":
    main()
