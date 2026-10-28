-- Event-Driven API Engineering
-- Revision 010: durable publication intent and exactly-once consumer effects.
--
-- `event_outbox` is written in the same transaction as the domain mutation.
-- A relay may publish a row more than once if it crashes after broker acceptance;
-- consumers therefore deduplicate by tenant, consumer, effect version, and event id.

CREATE TABLE IF NOT EXISTS event_outbox (
    event_id uuid PRIMARY KEY,
    tenant_id text NOT NULL,
    aggregate_type text NOT NULL,
    aggregate_id text NOT NULL,
    channel text NOT NULL,
    partition_key text NOT NULL,
    event_type text NOT NULL,
    source_uri text NOT NULL,
    schema_uri text NOT NULL,
    envelope jsonb NOT NULL,
    envelope_sha256 text NOT NULL CHECK (envelope_sha256 ~ '^[0-9a-f]{64}$'),
    state text NOT NULL DEFAULT 'pending'
        CHECK (state IN ('pending', 'leased', 'published', 'failed')),
    attempts integer NOT NULL DEFAULT 0 CHECK (attempts >= 0),
    next_attempt_at timestamptz NOT NULL DEFAULT now(),
    lease_owner text,
    lease_generation bigint NOT NULL DEFAULT 0 CHECK (lease_generation >= 0),
    lease_expires_at timestamptz,
    published_at timestamptz,
    broker_partition integer CHECK (broker_partition IS NULL OR broker_partition >= 0),
    broker_offset text,
    failure_code text,
    created_at timestamptz NOT NULL DEFAULT now(),
    CHECK (
        (state = 'leased' AND lease_owner IS NOT NULL AND lease_expires_at IS NOT NULL)
        OR state <> 'leased'
    )
);

CREATE INDEX IF NOT EXISTS event_outbox_claim_idx
    ON event_outbox (next_attempt_at, created_at, event_id)
    WHERE state IN ('pending', 'failed');

CREATE INDEX IF NOT EXISTS event_outbox_aggregate_idx
    ON event_outbox (tenant_id, aggregate_type, aggregate_id, created_at, event_id);

CREATE TABLE IF NOT EXISTS event_inbox (
    tenant_id text NOT NULL,
    consumer_name text NOT NULL,
    effect_version text NOT NULL,
    event_id uuid NOT NULL,
    event_type text NOT NULL,
    channel text NOT NULL,
    broker_partition integer NOT NULL CHECK (broker_partition >= 0),
    broker_offset text NOT NULL,
    processed_at timestamptz NOT NULL DEFAULT now(),
    outcome jsonb NOT NULL DEFAULT '{}'::jsonb,
    PRIMARY KEY (tenant_id, consumer_name, effect_version, event_id)
);

CREATE INDEX IF NOT EXISTS event_inbox_event_idx
    ON event_inbox (event_id, consumer_name, effect_version);

COMMENT ON TABLE event_outbox IS
    'Transactional publication intent. Broker acknowledgement is not atomic with this row.';
COMMENT ON TABLE event_inbox IS
    'Consumer deduplication identity. The protected unit is an effect version, not merely an event id.';
