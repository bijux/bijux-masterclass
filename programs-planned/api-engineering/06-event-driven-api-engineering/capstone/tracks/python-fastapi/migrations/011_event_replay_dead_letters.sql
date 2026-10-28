-- Event-Driven API Engineering
-- Revision 011: bounded replay evidence, durable checkpoints, and dead-letter custody.

CREATE TABLE IF NOT EXISTS event_replay_runs (
    replay_id uuid PRIMARY KEY,
    requested_by text NOT NULL,
    consumer_name text NOT NULL,
    effect_version text NOT NULL,
    mode text NOT NULL CHECK (mode IN ('dry-run', 'apply')),
    tenant_id text,
    event_types text[] NOT NULL,
    from_time timestamptz,
    to_time timestamptz,
    maximum_events bigint NOT NULL CHECK (maximum_events > 0),
    side_effects text NOT NULL DEFAULT 'disabled'
        CHECK (side_effects = 'disabled'),
    status text NOT NULL DEFAULT 'planned'
        CHECK (status IN ('planned', 'running', 'completed', 'aborted', 'failed')),
    selected_count bigint NOT NULL DEFAULT 0 CHECK (selected_count >= 0),
    applied_count bigint NOT NULL DEFAULT 0 CHECK (applied_count >= 0),
    skipped_count bigint NOT NULL DEFAULT 0 CHECK (skipped_count >= 0),
    started_at timestamptz,
    completed_at timestamptz,
    created_at timestamptz NOT NULL DEFAULT now(),
    CHECK (from_time IS NULL OR to_time IS NULL OR from_time <= to_time)
);

CREATE TABLE IF NOT EXISTS event_replay_checkpoints (
    replay_id uuid NOT NULL REFERENCES event_replay_runs(replay_id) ON DELETE CASCADE,
    channel text NOT NULL,
    broker_partition integer NOT NULL CHECK (broker_partition >= 0),
    next_offset text NOT NULL,
    updated_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (replay_id, channel, broker_partition)
);

CREATE TABLE IF NOT EXISTS event_dead_letters (
    dead_letter_id uuid PRIMARY KEY,
    tenant_id text NOT NULL,
    consumer_name text NOT NULL,
    effect_version text NOT NULL,
    event_id uuid NOT NULL,
    event_type text NOT NULL,
    channel text NOT NULL,
    broker_partition integer NOT NULL CHECK (broker_partition >= 0),
    broker_offset text NOT NULL,
    attempt_count integer NOT NULL CHECK (attempt_count > 0),
    failure_class text NOT NULL
        CHECK (failure_class IN ('permanent', 'exhausted-transient', 'policy')),
    failure_code text NOT NULL,
    safe_detail text NOT NULL,
    envelope jsonb NOT NULL,
    envelope_sha256 text NOT NULL CHECK (envelope_sha256 ~ '^[0-9a-f]{64}$'),
    status text NOT NULL DEFAULT 'open'
        CHECK (status IN ('open', 'quarantined', 'replayed', 'discarded')),
    replay_id uuid REFERENCES event_replay_runs(replay_id),
    created_at timestamptz NOT NULL DEFAULT now(),
    resolved_at timestamptz,
    UNIQUE (consumer_name, effect_version, channel, broker_partition, broker_offset)
);

CREATE INDEX IF NOT EXISTS event_dead_letters_open_idx
    ON event_dead_letters (consumer_name, created_at, dead_letter_id)
    WHERE status IN ('open', 'quarantined');

COMMENT ON TABLE event_replay_runs IS
    'Audited, bounded replay intent. External side effects are disabled by profile.';
COMMENT ON TABLE event_dead_letters IS
    'Custody record for messages that require an explicit operator decision.';
