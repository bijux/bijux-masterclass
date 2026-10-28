-- Course 4 adds durable evidence for state reconciliation and repair.
-- Telemetry remains outside the transactional application database.
CREATE TABLE IF NOT EXISTS operational_reconciliation_runs (
    id text PRIMARY KEY,
    kind text NOT NULL,
    started_at timestamptz NOT NULL DEFAULT now(),
    completed_at timestamptz,
    status text NOT NULL CHECK (status IN ('running', 'completed', 'failed')),
    summary jsonb NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE IF NOT EXISTS operational_repair_actions (
    repair_key text PRIMARY KEY,
    reconciliation_id text NOT NULL REFERENCES operational_reconciliation_runs(id),
    target_type text NOT NULL,
    target_id text NOT NULL,
    action text NOT NULL,
    before_state jsonb NOT NULL,
    after_state jsonb,
    status text NOT NULL CHECK (status IN ('planned', 'applied', 'skipped', 'failed')),
    created_at timestamptz NOT NULL DEFAULT now(),
    applied_at timestamptz
);

CREATE INDEX IF NOT EXISTS operational_repair_actions_target_idx
    ON operational_repair_actions (target_type, target_id);
