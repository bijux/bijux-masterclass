#!/usr/bin/env python3
"""Live PostgreSQL proof for migrations and operational repair evidence.

This route is intentionally environment-gated. It requires TEST_DATABASE_URL
and never silently substitutes SQLite or mocks for PostgreSQL behavior.
"""

from __future__ import annotations

import os
from pathlib import Path
from uuid import uuid4


def main() -> None:
    database_url = os.environ.get("TEST_DATABASE_URL")
    if not database_url:
        raise SystemExit("TEST_DATABASE_URL is required for the live PostgreSQL proof")
    try:
        import psycopg
        from psycopg.errors import UniqueViolation
    except ImportError as exc:
        raise SystemExit("psycopg is required for the live PostgreSQL proof") from exc

    from analysis_service.migrations import apply_migrations

    course = Path(__file__).resolve().parents[3]
    migration_root = course / "capstone" / "tracks" / "python-fastapi" / "migrations"
    first = apply_migrations(database_url, migration_root)
    second = apply_migrations(database_url, migration_root)
    if second:
        raise SystemExit(f"migration replay was not idempotent: {second}")

    reconciliation_id = f"recon-{uuid4()}"
    repair_key = f"repair-{uuid4()}"
    with psycopg.connect(database_url, autocommit=True) as connection:
        versions = [
            row[0][:3]
            for row in connection.execute(
                "SELECT version FROM schema_migrations ORDER BY version"
            ).fetchall()
        ]
        if versions[-8:] != [f"{value:03d}" for value in range(1, 9)]:
            raise SystemExit(f"unexpected migration history: {versions}")

        tables = {
            row[0]
            for row in connection.execute(
                """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                """
            ).fetchall()
        }
        required = {
            "operational_reconciliation_runs",
            "operational_repair_actions",
        }
        if not required.issubset(tables):
            raise SystemExit(f"migration 008 tables missing: {sorted(required - tables)}")

        connection.execute(
            """
            INSERT INTO operational_reconciliation_runs(id, kind, status, summary)
            VALUES (%s, 'live-proof', 'completed', %s::jsonb)
            """,
            (reconciliation_id, '{"findings":1}'),
        )
        connection.execute(
            """
            INSERT INTO operational_repair_actions(
                repair_key, reconciliation_id, target_type, target_id,
                action, before_state, after_state, status
            )
            VALUES (%s, %s, 'analysis-run', 'run-proof', 'no-op-proof',
                    '{}'::jsonb, '{}'::jsonb, 'skipped')
            """,
            (repair_key, reconciliation_id),
        )
        duplicate_rejected = False
        try:
            connection.execute(
                """
                INSERT INTO operational_repair_actions(
                    repair_key, reconciliation_id, target_type, target_id,
                    action, before_state, status
                )
                VALUES (%s, %s, 'analysis-run', 'run-proof', 'duplicate',
                        '{}'::jsonb, 'planned')
                """,
                (repair_key, reconciliation_id),
            )
        except UniqueViolation:
            duplicate_rejected = True
        if not duplicate_rejected:
            raise SystemExit("duplicate repair key was not rejected")

        row = connection.execute(
            """
            SELECT status, before_state, after_state
            FROM operational_repair_actions
            WHERE repair_key=%s
            """,
            (repair_key,),
        ).fetchone()
        if row is None or row[0] != "skipped":
            raise SystemExit("repair evidence was not durable")

        connection.execute(
            "DELETE FROM operational_repair_actions WHERE repair_key=%s",
            (repair_key,),
        )
        connection.execute(
            "DELETE FROM operational_reconciliation_runs WHERE id=%s",
            (reconciliation_id,),
        )

    print(
        "PASS live PostgreSQL proof — migrations 001-008, idempotent replay, "
        "durable reconciliation evidence, unique repair key"
    )
    if first:
        print(f"NOTE migrations applied during this run: {', '.join(first)}")


if __name__ == "__main__":
    main()
