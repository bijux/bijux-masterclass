#!/usr/bin/env python3
"""Complete a passing or failing selftest evidence bundle."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from write_bundle_manifest import build_manifest

ROUTE = """Selftest review route:
  1. Read summary.txt for the top-level verdict and stopping boundary.
  2. Read SELFTEST_GUIDE.md for file meanings and review questions.
  3. Read PROOF_GUIDE.md for the wider claim-to-evidence route.
  4. Read settings.env and commands.txt for the execution boundary.
  5. Read schedule-comparison.json for the schedule-equivalence decision.
  6. Compare serial-inventory.json and parallel-inventory.json when it fails.
  7. Read the matching file under logs/ before inspecting workspace/.
"""

BUNDLE_GUIDE = """Bundle surfaces:
  SELFTEST_GUIDE.md          reading order and file meanings
  summary.txt                result, stopping boundary, and per-check status
  settings.env               runtime boundary and guardrail values
  commands.txt               ordered commands executed by the harness
  logs/                      captured output for each proof command
  schedule-comparison.json   semantic schedule-equivalence result
  serial-inventory.json      declared serial artifact inventory
  parallel-inventory.json    declared parallel artifact inventory
  hidden-input.txt           dishonest-input detection result
  workspace/                 preserved sandbox at the stopping boundary
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report-dir", required=True)
    parser.add_argument("--selftest-guide", required=True)
    parser.add_argument("--proof-guide", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report_dir = Path(args.report_dir)
    summary = report_dir / "summary.txt"
    if not summary.is_file():
        raise SystemExit(f"selftest summary is missing: {summary}")

    shutil.copyfile(args.selftest_guide, report_dir / "SELFTEST_GUIDE.md")
    shutil.copyfile(args.proof_guide, report_dir / "PROOF_GUIDE.md")
    (report_dir / "route.txt").write_text(ROUTE, encoding="utf-8")
    (report_dir / "bundle-guide.txt").write_text(BUNDLE_GUIDE, encoding="utf-8")
    manifest_path = report_dir / "manifest.json"
    manifest_path.unlink(missing_ok=True)
    manifest = build_manifest(report_dir)
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
