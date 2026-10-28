from __future__ import annotations

import json
import re
from pathlib import Path

CAP = Path(__file__).resolve().parents[1]
HANDOFF = CAP / "handoff"
ARCH = CAP / "architecture"


def load(name: str) -> object:
    return json.loads((HANDOFF / name).read_text(encoding="utf-8"))


def main() -> int:
    requirements = load("cloud-foundation-requirements.json")
    if not isinstance(requirements, dict) or requirements.get("profileVersion") != "1.0":
        raise SystemExit("invalid handoff profile version")
    rows = requirements.get("requirements")
    if not isinstance(rows, list) or len(rows) < 12:
        raise SystemExit("handoff requirement catalogue is incomplete")
    ids: list[str] = []
    for row in rows:
        if not isinstance(row, dict):
            raise SystemExit("requirement is not an object")
        rid = row.get("id")
        if not isinstance(rid, str) or not re.fullmatch(r"PE-CF-\d{3}", rid):
            raise SystemExit(f"invalid requirement id: {rid!r}")
        if not isinstance(row.get("statement"), str) or len(row["statement"].split()) < 6:
            raise SystemExit(f"requirement statement too weak: {rid}")
        acceptance = row.get("acceptance")
        if not isinstance(acceptance, list) or len(acceptance) < 2 or not all(isinstance(v, str) for v in acceptance):
            raise SystemExit(f"requirement acceptance evidence missing: {rid}")
        ids.append(rid)
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate requirement id")

    for name in ["host-profile.json", "network-plan.json", "storage-plan.json", "cloud-provider-map.json", "failure-scenarios.json"]:
        if (ARCH / name).read_bytes() != (HANDOFF / name).read_bytes():
            raise SystemExit(f"handoff copy differs from architecture source: {name}")

    version = load("version-ledger.json")
    if version.get("hostRuntimeProfile") != "1.0" or version.get("handoffProfile") != "1.0":
        raise SystemExit("version ledger does not match released profiles")

    schema = load("handoff-profile.schema.json")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        raise SystemExit("handoff schema dialect is not declared")

    print(f"PASS handoff semantics — {len(rows)} requirements, {len(ids)} unique ids")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
