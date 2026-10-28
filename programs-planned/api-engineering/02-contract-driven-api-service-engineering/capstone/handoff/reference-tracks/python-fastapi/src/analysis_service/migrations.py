"""Immutable, advisory-locked PostgreSQL migration runner."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path

import psycopg


BOOTSTRAP = """
CREATE TABLE IF NOT EXISTS schema_migrations (
    version text PRIMARY KEY,
    checksum_sha256 text NOT NULL
        CHECK (checksum_sha256 ~ '^[a-f0-9]{64}$'),
    applied_at timestamptz NOT NULL DEFAULT clock_timestamp()
)
"""
LOCK_ID = 734_246_110


def migration_files(root: Path, target: str | None = None) -> list[Path]:
    files = sorted(
        path
        for path in root.glob("[0-9][0-9][0-9]_*.sql")
        if path.is_file()
    )
    if not files:
        raise RuntimeError(f"no migrations under {root}")
    versions = [path.name[:3] for path in files]
    if len(versions) != len(set(versions)):
        raise RuntimeError("migration versions must be unique")
    if target is not None:
        if len(target) != 3 or not target.isdigit():
            raise ValueError("migration target must be a three-digit revision")
        files = [path for path in files if path.name[:3] <= target]
    return files


def apply_migrations(
    database_url: str,
    root: Path,
    target: str | None = None,
) -> list[str]:
    applied: list[str] = []
    # Autocommit keeps the session-level advisory lock usable even if one
    # migration transaction fails.  Each migration and its manifest row commit
    # atomically inside an explicit transaction context.
    with psycopg.connect(database_url, autocommit=True) as connection:
        connection.execute(BOOTSTRAP)
        connection.execute("SELECT pg_advisory_lock(%s)", (LOCK_ID,))
        try:
            for path in migration_files(root, target):
                raw = path.read_bytes()
                digest = sha256(raw).hexdigest()
                version = path.name
                existing = connection.execute(
                    """
                    SELECT checksum_sha256
                    FROM schema_migrations
                    WHERE version=%s
                    """,
                    (version,),
                ).fetchone()
                if existing:
                    if existing[0] != digest:
                        raise RuntimeError(
                            f"applied migration changed: {version}"
                        )
                    continue

                with connection.transaction():
                    connection.execute(raw.decode("utf-8"))
                    connection.execute(
                        """
                        INSERT INTO schema_migrations(
                            version,
                            checksum_sha256
                        )
                        VALUES (%s, %s)
                        """,
                        (version, digest),
                    )
                applied.append(version)
        finally:
            connection.execute("SELECT pg_advisory_unlock(%s)", (LOCK_ID,))
    return applied
