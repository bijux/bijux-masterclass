-- Event-Driven API Engineering
-- Revision 012: event contract catalogue and consumer compatibility declarations.

CREATE TABLE IF NOT EXISTS event_contract_releases (
    event_type text NOT NULL,
    major_version integer NOT NULL CHECK (major_version > 0),
    schema_uri text NOT NULL,
    schema_sha256 text NOT NULL CHECK (schema_sha256 ~ '^[0-9a-f]{64}$'),
    owner text NOT NULL,
    channel text NOT NULL,
    partition_key_field text NOT NULL,
    classification text NOT NULL
        CHECK (classification IN ('public', 'internal', 'restricted')),
    retention_days integer NOT NULL CHECK (retention_days > 0),
    replay_policy text NOT NULL
        CHECK (replay_policy IN ('projection-safe', 'workflow-review', 'not-replayable')),
    status text NOT NULL
        CHECK (status IN ('candidate', 'active', 'deprecated', 'retired', 'rejected')),
    released_at timestamptz,
    created_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (event_type, major_version),
    UNIQUE (schema_uri, schema_sha256)
);

CREATE TABLE IF NOT EXISTS event_consumer_contracts (
    consumer_name text NOT NULL,
    effect_version text NOT NULL,
    event_type text NOT NULL,
    minimum_major_version integer NOT NULL CHECK (minimum_major_version > 0),
    maximum_major_version integer NOT NULL CHECK (maximum_major_version >= minimum_major_version),
    required_fields text[] NOT NULL DEFAULT '{}',
    accepts_unknown_fields boolean NOT NULL DEFAULT true,
    owner text NOT NULL,
    status text NOT NULL CHECK (status IN ('active', 'deprecated', 'retired')),
    updated_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (consumer_name, effect_version, event_type)
);

CREATE TABLE IF NOT EXISTS event_release_decisions (
    decision_id uuid PRIMARY KEY,
    candidate_id text NOT NULL,
    decision text NOT NULL CHECK (decision IN ('accepted', 'review-required', 'rejected')),
    contract_valid boolean NOT NULL,
    compatibility_status text NOT NULL
        CHECK (compatibility_status IN ('accepted', 'review-required', 'rejected')),
    replay_safe boolean NOT NULL,
    security_valid boolean NOT NULL,
    reliability_ready boolean NOT NULL,
    catalogue_complete boolean NOT NULL,
    reasons jsonb NOT NULL DEFAULT '[]'::jsonb,
    decided_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS event_consumer_contracts_event_idx
    ON event_consumer_contracts (event_type, status, consumer_name);

COMMENT ON TABLE event_contract_releases IS
    'Governed event definitions. Event contract version is independent of public HTTP API version.';
