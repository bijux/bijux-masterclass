from __future__ import annotations

import csv
import json
import shutil
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / "artifacts"


def copy_blueprint() -> tempfile.TemporaryDirectory[str]:
    ARTIFACTS.mkdir(exist_ok=True)
    directory = tempfile.TemporaryDirectory(dir=ARTIFACTS)
    target = Path(directory.name)
    shutil.copytree(ROOT / "manifests", target / "manifests")
    shutil.copytree(ROOT / "programs", target / "programs")
    shutil.copy2(ROOT / "ALL_3000_MODULES.md", target)
    csv_path = target / "manifests" / "modules.csv"
    with csv_path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fields = reader.fieldnames
    if fields is None:
        raise ValueError("copied module CSV has no fields")
    for row in rows:
        row["status"] = "planned"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    jsonl_path = target / "manifests" / "modules.jsonl"
    json_rows = [
        json.loads(line)
        for line in jsonl_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    for row in json_rows:
        row["status"] = "planned"
    jsonl_path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in json_rows),
        encoding="utf-8",
    )
    for modules_directory in target.glob("programs/*/modules"):
        shutil.rmtree(modules_directory)
    return directory
