BEGIN;

CREATE TABLE IF NOT EXISTS rpc_worker_sessions (
    session_id text PRIMARY KEY,
    worker_id text NOT NULL,
    tenant_id text NOT NULL,
    connected_at timestamptz NOT NULL DEFAULT now(),
    last_seen_at timestamptz NOT NULL DEFAULT now(),
    credential_expires_at timestamptz,
    closed_at timestamptz
);

CREATE TABLE IF NOT EXISTS rpc_work_assignments (
    assignment_id text PRIMARY KEY,
    run_id text NOT NULL,
    worker_id text NOT NULL,
    tenant_id text NOT NULL,
    lease_generation bigint NOT NULL CHECK (lease_generation > 0),
    lease_expires_at timestamptz NOT NULL,
    state text NOT NULL CHECK (
        state IN ('assigned', 'running', 'completed', 'failed', 'expired', 'cancelled')
    ),
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (run_id, lease_generation)
);

CREATE INDEX IF NOT EXISTS rpc_work_assignments_claim_idx
    ON rpc_work_assignments (tenant_id, state, lease_expires_at);

COMMIT;
