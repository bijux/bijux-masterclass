BEGIN;

CREATE TABLE IF NOT EXISTS rpc_request_outcomes (
    method_path text NOT NULL,
    principal_id text NOT NULL,
    request_id text NOT NULL,
    request_fingerprint text NOT NULL,
    outcome_status text,
    outcome_message bytea,
    committed_at timestamptz,
    created_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (method_path, principal_id, request_id)
);

CREATE TABLE IF NOT EXISTS run_observation_events (
    run_id text NOT NULL,
    sequence bigint NOT NULL CHECK (sequence > 0),
    event_type text NOT NULL,
    snapshot jsonb NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (run_id, sequence)
);

CREATE INDEX IF NOT EXISTS run_observation_events_created_idx
    ON run_observation_events (run_id, created_at);

COMMIT;
