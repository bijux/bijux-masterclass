#!/usr/bin/env python3
"""Environment-backed migration and plan proof.

Requires TEST_DATABASE_URL and psycopg. It is intentionally absent from the
core proof so missing infrastructure never becomes a false pass.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

try:
    import psycopg
except ImportError as exc:
    raise SystemExit("psycopg is required; run make setup") from exc

url = os.environ.get("TEST_DATABASE_URL")
if not url:
    raise SystemExit("TEST_DATABASE_URL is required")

root = Path(__file__).resolve().parents[1]
query = (root / "database/queries/list_runs.sql").read_text()
output = root / "reports/live-run-list-plan.json"

with psycopg.connect(url) as connection:
    with connection.cursor() as cursor:
        cursor.execute("SELECT current_setting('server_version')")
        version = cursor.fetchone()[0]
        cursor.execute("EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) " + query, {
            "owner_id": "00000000-0000-0000-0000-000000000001",
            "status": "completed",
            "high_water_created_at": "9999-12-31T23:59:59Z",
            "high_water_id": "ffffffff-ffff-ffff-ffff-ffffffffffff",
            "boundary_created_at": "9999-12-31T23:59:59Z",
            "boundary_id": "ffffffff-ffff-ffff-ffff-ffffffffffff",
            "limit": 50,
        })
        plan = cursor.fetchone()[0]
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps({"postgresqlVersion": version, "plan": plan}, indent=2) + "\n")
print(output)
