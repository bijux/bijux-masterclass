from __future__ import annotations

import argparse
import json
from pathlib import Path

EXPECTED_PUBLISHED_PATHS = [
    "discovered_samples.json",
    "provenance.json",
    "report/index.html",
    "summary.json",
    "summary.tsv",
]


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--publish", type=Path, required=True)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    publish_dir = args.publish
    required_files = [
        publish_dir / "manifest.json",
        publish_dir / "provenance.json",
        publish_dir / "discovered_samples.json",
        publish_dir / "summary.json",
        publish_dir / "summary.tsv",
        publish_dir / "report" / "index.html",
    ]

    for path in required_files:
        if not path.is_file():
            raise FileNotFoundError(f"missing published artifact: {path}")
        if path.stat().st_size == 0:
            raise ValueError(f"published artifact is empty: {path}")

    manifest = load_json(publish_dir / "manifest.json")
    provenance = load_json(publish_dir / "provenance.json")
    discovered = load_json(publish_dir / "discovered_samples.json")
    summary = load_json(publish_dir / "summary.json")

    if int(manifest["schema_version"]) != 2:
        raise ValueError("manifest schema_version must be 2")
    if int(provenance["schema_version"]) != 2:
        raise ValueError("provenance schema_version must be 2")
    if int(discovered["schema_version"]) != 2:
        raise ValueError("discovered_samples.json schema_version must be 2")
    if int(summary["schema_version"]) != 2:
        raise ValueError("summary.json schema_version must be 2")
    if not manifest["files"]:
        raise ValueError("manifest must list published files")
    if not discovered["samples"]:
        raise ValueError("discovered_samples.json must list at least one sample")
    if not summary["units"]:
        raise ValueError("summary.json must list at least one unit")
    if "timestamp_utc" not in provenance or "config" not in provenance:
        raise ValueError("provenance.json must record timestamp_utc and config")

    manifest_paths = [entry["path"] for entry in manifest["files"]]
    if manifest_paths != EXPECTED_PUBLISHED_PATHS:
        raise ValueError(f"manifest paths must equal {EXPECTED_PUBLISHED_PATHS}, got {manifest_paths}")

    discovered_samples = sorted(discovered["samples"])
    summary_units = sorted(summary["units"])
    if discovered_samples != summary_units:
        raise ValueError(
            "summary.json units must match discovered_samples.json sample keys "
            f"(got units={summary_units}, samples={discovered_samples})"
        )

    report_html = (publish_dir / "report" / "index.html").read_text(encoding="utf-8")
    if "<html" not in report_html.lower():
        raise ValueError("report/index.html does not look like HTML")

    if args.report is not None:
        required_paths = [path.relative_to(publish_dir).as_posix() for path in required_files]
        args.report.write_text(
            json.dumps(
                {
                    "publish_dir": publish_dir.resolve().as_posix(),
                    "checks": [
                        {
                            "check": "required_files",
                            "files": required_paths,
                        },
                        {
                            "check": "manifest",
                            "schema_version": int(manifest["schema_version"]),
                            "file_count": len(manifest["files"]),
                            "paths": manifest_paths,
                        },
                        {
                            "check": "discovery",
                            "sample_count": len(discovered["samples"]),
                            "schema_version": int(discovered["schema_version"]),
                        },
                        {
                            "check": "summary",
                            "unit_count": len(summary["units"]),
                            "schema_version": int(summary["schema_version"]),
                            "units_match_discovery": discovered_samples == summary_units,
                        },
                        {
                            "check": "provenance",
                            "schema_version": int(provenance["schema_version"]),
                            "snakemake_version": provenance.get("snakemake_version"),
                        },
                        {
                            "check": "report",
                            "contains_html_tag": True,
                        },
                    ],
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )

    print("PASS: publish artifacts look sane")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
