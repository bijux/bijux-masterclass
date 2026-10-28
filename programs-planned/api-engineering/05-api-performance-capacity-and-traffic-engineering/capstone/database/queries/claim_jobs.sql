-- Claim only a bounded batch of currently available jobs.
WITH candidates AS (
    SELECT run_id
    FROM run_jobs
    WHERE status = 'queued'
      AND available_at <= clock_timestamp()
    ORDER BY available_at, run_id
    FOR UPDATE SKIP LOCKED
    LIMIT %(claim_batch)s
)
UPDATE run_jobs AS jobs
SET
    status = 'leased',
    lease_owner = %(worker_id)s,
    lease_expires_at = clock_timestamp() + %(lease_interval)s,
    lease_generation = jobs.lease_generation + 1,
    attempts = jobs.attempts + 1,
    updated_at = clock_timestamp()
FROM candidates
WHERE jobs.run_id = candidates.run_id
RETURNING jobs.*;
