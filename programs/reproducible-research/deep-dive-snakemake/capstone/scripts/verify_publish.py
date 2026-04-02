from __future__ import annotations

import argparse
import json
from pathlib import Path


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
    load_json(publish_dir / "provenance.json")
    discovered = load_json(publish_dir / "discovered_samples.json")
    summary = load_json(publish_dir / "summary.json")

    if int(manifest["schema_version"]) != 2:
        raise ValueError("manifest schema_version must be 2")
    if not manifest["files"]:
        raise ValueError("manifest must list published files")
    if not discovered["samples"]:
        raise ValueError("discovered_samples.json must list at least one sample")
    if not summary["units"]:
        raise ValueError("summary.json must list at least one unit")

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
                        },
                        {
                            "check": "discovery",
                            "sample_count": len(discovered["samples"]),
                        },
                        {
                            "check": "summary",
                            "unit_count": len(summary["units"]),
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
