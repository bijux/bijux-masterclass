#!/usr/bin/env python3
from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROGRAMS = ROOT / "manifests" / "programs.csv"
MODULES = ROOT / "manifests" / "modules.csv"

BANNED = (
    "overview",
    "advanced topics",
    "miscellaneous",
    "future directions",
    "final synthesis",
    "capstone",
    "comprehensive project",
)

def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)

def main() -> None:
    if not PROGRAMS.is_file() or not MODULES.is_file():
        fail("manifest files are missing")

    with PROGRAMS.open(encoding="utf-8", newline="") as fh:
        programs = list(csv.DictReader(fh))
    with MODULES.open(encoding="utf-8", newline="") as fh:
        modules = list(csv.DictReader(fh))

    if len(programs) != 30:
        fail(f"expected 30 programs, found {len(programs)}")
    if len(modules) != 3000:
        fail(f"expected 3000 modules, found {len(modules)}")

    for field in ("module_id", "module_title", "future_path"):
        values = [row[field].strip() for row in modules]
        if len(values) != len(set(values)):
            dupes = [v for v, count in Counter(values).items() if count > 1]
            fail(f"duplicate {field}: {dupes[:10]}")

    by_program: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in modules:
        by_program[row["program_code"]].append(row)

    if set(by_program) != {p["program_code"] for p in programs}:
        fail("program codes differ between manifests")

    for program in programs:
        code = program["program_code"]
        rows = sorted(by_program[code], key=lambda r: int(r["module_number"]))
        if len(rows) != 100:
            fail(f"{code}: expected 100 modules, found {len(rows)}")

        numbers = [int(r["module_number"]) for r in rows]
        if numbers != list(range(1, 101)):
            fail(f"{code}: numbering is not continuous 001-100")

        levels = Counter(int(r["level"]) for r in rows)
        if levels != Counter({1: 50, 2: 50}):
            fail(f"{code}: expected 50 modules in each level, found {dict(levels)}")

        blocks = Counter(int(r["block_number"]) for r in rows)
        if set(blocks) != set(range(1, 11)) or any(count != 10 for count in blocks.values()):
            fail(f"{code}: expected 10 blocks of 10 modules")

        for row in rows:
            title = row["module_title"].strip()
            lowered = title.casefold()
            for term in BANNED:
                if term in lowered:
                    fail(f'{row["module_id"]}: banned filler phrase "{term}"')
            if not re.fullmatch(r"[A-Z0-9]+-\d{3}", row["module_id"]):
                fail(f'{row["module_id"]}: invalid module ID')
            if row["status"] != "planned":
                fail(f'{row["module_id"]}: blueprint status must be planned')
            if (ROOT / row["future_path"]).exists():
                fail(f'{row["module_id"]}: placeholder module file exists')

        roadmap = ROOT / "programs" / program["slug"] / "ROADMAP.md"
        if not roadmap.is_file():
            fail(f"{code}: ROADMAP.md is missing")
        text = roadmap.read_text(encoding="utf-8")
        for row in rows:
            if row["module_title"] not in text:
                fail(f'{code}: roadmap omits "{row["module_title"]}"')

    print("PASS")
    print(f"Programs: {len(programs)}")
    print(f"Modules: {len(modules)}")
    print("Modules per program: 100")
    print("Level I per program: 50")
    print("Level II per program: 50")
    print("Unique module IDs: 3000")
    print("Unique module titles: 3000")
    print("Unique future paths: 3000")
    print("Placeholder module files: 0")
    print("Banned filler-title findings: 0")

if __name__ == "__main__":
    main()
