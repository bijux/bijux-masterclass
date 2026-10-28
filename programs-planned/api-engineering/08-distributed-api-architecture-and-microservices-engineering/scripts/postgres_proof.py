#!/usr/bin/env python3
"""Apply owner-local Course 8 migrations to isolated PostgreSQL schemas."""
from __future__ import annotations

import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
DATABASE = ROOT / "capstone" / "database"
SERVICES = {
    "analysis-control": ["service_schema_metadata"],
    "artifact-service": ["artifacts", "consumed_artifact_capabilities"],
    "notification-service": [
        "webhook_subscriptions",
        "webhook_deliveries",
        "notification_run_view",
    ],
    "platform-catalog": ["service_catalog"],
}


def run(command: list[str], *, env: dict[str, str] | None = None) -> str:
    merged = os.environ.copy()
    if env:
        merged.update(env)
    completed = subprocess.run(
        command,
        check=True,
        text=True,
        capture_output=True,
        env=merged,
    )
    return completed.stdout.strip()


def identifier(value: str) -> str:
    candidate = "course8_" + value.replace("-", "_")
    if not re.fullmatch(r"[a-z_][a-z0-9_]*", candidate):
        raise ValueError(f"unsafe schema identifier: {candidate}")
    return candidate


def main() -> None:
    psql = shutil.which("psql")
    url = os.environ.get("TEST_DATABASE_URL")
    if not psql or not url:
        raise SystemExit(
            "psql and TEST_DATABASE_URL are required for the live PostgreSQL proof"
        )

    results: dict[str, object] = {}
    created: list[str] = []
    try:
        for service, expected_tables in SERVICES.items():
            schema = identifier(service)
            run([
                psql,
                url,
                "-X",
                "-v",
                "ON_ERROR_STOP=1",
                "-c",
                f'DROP SCHEMA IF EXISTS "{schema}" CASCADE; '
                f'CREATE SCHEMA "{schema}";',
            ])
            created.append(schema)
            env = {"PGOPTIONS": f"-c search_path={schema}"}
            migrations = sorted((DATABASE / service / "migrations").glob("*.sql"))
            if not migrations:
                raise AssertionError(f"no migrations for {service}")
            for migration in migrations:
                run([
                    psql,
                    url,
                    "-X",
                    "-v",
                    "ON_ERROR_STOP=1",
                    "-f",
                    str(migration),
                ], env=env)
            rows = run([
                psql,
                url,
                "-X",
                "-At",
                "-v",
                "ON_ERROR_STOP=1",
                "-c",
                "SELECT tablename FROM pg_catalog.pg_tables "
                f"WHERE schemaname = '{schema}' ORDER BY tablename;",
            ])
            actual = {row for row in rows.splitlines() if row}
            missing = sorted(set(expected_tables) - actual)
            if missing:
                raise AssertionError(f"{service} missing tables: {missing}")
            results[service] = {
                "schema": schema,
                "migrations": [path.name for path in migrations],
                "tables": sorted(actual),
            }
    finally:
        for schema in reversed(created):
            try:
                run([
                    psql,
                    url,
                    "-X",
                    "-v",
                    "ON_ERROR_STOP=1",
                    "-c",
                    f'DROP SCHEMA IF EXISTS "{schema}" CASCADE;',
                ])
            except Exception:
                pass

    print(json.dumps({"status": "pass", "services": results}, indent=2))


if __name__ == "__main__":
    main()
