from __future__ import annotations

import os
from pathlib import Path
import unittest


class PostgreSQLMigrationTests(unittest.TestCase):
    @unittest.skipUnless(os.environ.get("TEST_DATABASE_URL"), "TEST_DATABASE_URL is not set")
    def test_event_tables_exist_after_migration(self) -> None:
        try:
            import psycopg
        except ImportError as exc:  # pragma: no cover - environment gate
            self.skipTest(f"psycopg unavailable: {exc}")
        with psycopg.connect(os.environ["TEST_DATABASE_URL"]) as connection:
            names = {
                row[0]
                for row in connection.execute(
                    """
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                      AND table_name LIKE 'event_%'
                    """
                )
            }
        required = {
            "event_outbox",
            "event_inbox",
            "event_replay_runs",
            "event_replay_checkpoints",
            "event_dead_letters",
            "event_contract_releases",
            "event_consumer_contracts",
            "event_release_decisions",
        }
        self.assertTrue(required.issubset(names))

    @unittest.skipUnless(os.environ.get("TEST_DATABASE_URL"), "TEST_DATABASE_URL is not set")
    def test_event_inbox_identity_is_composite(self) -> None:
        try:
            import psycopg
        except ImportError as exc:  # pragma: no cover - environment gate
            self.skipTest(f"psycopg unavailable: {exc}")
        with psycopg.connect(os.environ["TEST_DATABASE_URL"]) as connection:
            columns = [
                row[0]
                for row in connection.execute(
                    """
                    SELECT a.attname
                    FROM pg_index i
                    JOIN pg_attribute a
                      ON a.attrelid = i.indrelid
                     AND a.attnum = ANY(i.indkey)
                    WHERE i.indrelid = 'event_inbox'::regclass
                      AND i.indisprimary
                    ORDER BY array_position(i.indkey, a.attnum)
                    """
                )
            ]
        self.assertEqual(columns, ["tenant_id", "consumer_name", "effect_version", "event_id"])


if __name__ == "__main__":
    unittest.main()
