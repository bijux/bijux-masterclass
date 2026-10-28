-- API Performance, Capacity, and Traffic Engineering
-- Revision 009: evidence-backed indexes for critical Course 5 workloads.
--
-- Operational note:
-- CREATE INDEX CONCURRENTLY cannot run inside a transaction block. The course
-- migration runner executes each statement as an explicit non-transactional
-- step, records checksum/status, and verifies index validity before release.
-- The exact index is a hypothesis for the declared DS-RUNS-1M distribution;
-- it is not a universal PostgreSQL recommendation.

CREATE INDEX CONCURRENTLY IF NOT EXISTS
    idx_analysis_runs_owner_status_created_id
ON analysis_runs (owner_id, status, created_at DESC, id DESC)
INCLUDE (project_id, dataset_id, progress, version);

CREATE INDEX CONCURRENTLY IF NOT EXISTS
    idx_run_jobs_available_claim
ON run_jobs (available_at, run_id)
WHERE status = 'queued';

CREATE INDEX CONCURRENTLY IF NOT EXISTS
    idx_webhook_deliveries_available_claim
ON webhook_deliveries (available_at, id)
WHERE status = 'pending';

CREATE INDEX CONCURRENTLY IF NOT EXISTS
    idx_artifacts_owner_run_created
ON artifacts (owner_id, run_id, created_at DESC, id DESC);
