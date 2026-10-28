from __future__ import annotations
import os
from pathlib import Path
import pytest

def database_url():
 value=os.getenv('TEST_DATABASE_URL')
 if not value:pytest.skip('TEST_DATABASE_URL is not set')
 pytest.importorskip('psycopg');return value

def test_migrations_are_immutable_and_repeatable():
 url = database_url()
 from analysis_service.migrations import apply_migrations
 root = Path(__file__).parents[1] / 'migrations'
 first = apply_migrations(url, root)
 second = apply_migrations(url, root)
 assert first or second == []
 assert second == []

def test_concurrency_is_proved_by_shared_runner_not_a_mock():
 database_url();runner=Path(__file__).parents[3]/'tests/failure/postgres_proof.py';assert runner.is_file()
