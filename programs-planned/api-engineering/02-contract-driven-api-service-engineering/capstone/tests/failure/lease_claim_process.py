#!/usr/bin/env python3
"""Claim one job durably, report the lease, then remain alive for a kill test."""
from __future__ import annotations
import argparse
import json
import time


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database-url", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--lease-seconds", type=int, default=5)
    args = parser.parse_args()
    try:
        import psycopg
        from psycopg.rows import dict_row
    except Exception as exc:
        raise SystemExit(f"psycopg is required: {exc}")

    worker = "proof-crashed-worker"
    with psycopg.connect(args.database_url, row_factory=dict_row) as connection:
        with connection.transaction():
            row = connection.execute(
                """WITH candidate AS (
                     SELECT run_id FROM run_jobs
                     WHERE run_id=%s AND status='queued' AND available_at<=clock_timestamp()
                     FOR UPDATE SKIP LOCKED
                   )
                   UPDATE run_jobs j
                   SET status='leased', lease_owner=%s,
                       lease_expires_at=clock_timestamp()+(%s||' seconds')::interval,
                       lease_generation=lease_generation+1,
                       attempts=attempts+1, updated_at=clock_timestamp()
                   FROM candidate c
                   WHERE j.run_id=c.run_id
                   RETURNING j.run_id,j.lease_generation,j.lease_expires_at,j.attempts""",
                (args.run_id, worker, args.lease_seconds),
            ).fetchone()
            if row is None:
                raise SystemExit("job was not available for controlled claim")
            connection.execute(
                """UPDATE analysis_runs SET status='running',progress=1,updated_at=clock_timestamp()
                   WHERE id=%s AND status='queued'""",
                (args.run_id,),
            )
            owner = connection.execute(
                "SELECT owner_id FROM analysis_runs WHERE id=%s", (args.run_id,)
            ).fetchone()["owner_id"]
            connection.execute(
                "INSERT INTO run_events(run_id,owner_id,status,progress) VALUES(%s,%s,'running',1)",
                (args.run_id, owner),
            )
    print(
        json.dumps(
            {
                "runId": row["run_id"],
                "generation": row["lease_generation"],
                "attempts": row["attempts"],
                "leaseExpiresAt": row["lease_expires_at"].isoformat(),
            }
        ),
        flush=True,
    )
    while True:
        time.sleep(60)


if __name__ == "__main__":
    main()
