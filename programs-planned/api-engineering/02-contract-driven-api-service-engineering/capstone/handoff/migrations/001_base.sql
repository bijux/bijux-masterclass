-- Contract-Driven API Service Engineering
-- Baseline durable schema. PostgreSQL owns durable facts; application code owns intent.
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS schema_migrations (
    version text PRIMARY KEY,
    checksum_sha256 text NOT NULL CHECK (checksum_sha256 ~ '^[a-f0-9]{64}$'),
    applied_at timestamptz NOT NULL DEFAULT clock_timestamp()
);

CREATE SEQUENCE project_position_seq;
CREATE SEQUENCE dataset_position_seq;
CREATE SEQUENCE run_position_seq;
CREATE SEQUENCE artifact_position_seq;
CREATE SEQUENCE subscription_position_seq;
CREATE SEQUENCE event_position_seq;
CREATE SEQUENCE delivery_position_seq;
CREATE SEQUENCE cursor_handle_seq;

CREATE TABLE projects (
    position bigint PRIMARY KEY DEFAULT nextval('project_position_seq') CHECK (position BETWEEN 1 AND 999999999999999999),
    id text GENERATED ALWAYS AS ('prj_' || lpad(position::text,4,'0')) STORED UNIQUE,
    owner_id text NOT NULL CHECK (owner_id ~ '^[a-z][a-z0-9-]{2,31}$'),
    name text NOT NULL CHECK (char_length(name) BETWEEN 1 AND 80 AND name=btrim(name)),
    description text CHECK (description IS NULL OR char_length(description)<=500),
    version integer NOT NULL DEFAULT 1 CHECK (version>=1),
    created_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    updated_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    UNIQUE(id,owner_id), CHECK(updated_at>=created_at)
);

CREATE TABLE datasets (
    position bigint PRIMARY KEY DEFAULT nextval('dataset_position_seq') CHECK (position BETWEEN 1 AND 999999999999999999),
    id text GENERATED ALWAYS AS ('dts_' || lpad(position::text,4,'0')) STORED UNIQUE,
    project_id text NOT NULL,
    owner_id text NOT NULL CHECK (owner_id ~ '^[a-z][a-z0-9-]{2,31}$'),
    name text NOT NULL CHECK (char_length(name) BETWEEN 1 AND 100 AND name=btrim(name)),
    source_kind text NOT NULL CHECK (source_kind IN ('local-file','remote-object')),
    source jsonb NOT NULL CHECK (jsonb_typeof(source)='object'),
    status text NOT NULL CHECK (status IN ('awaiting-upload','ready','deleted')),
    content_path text,
    content_length bigint CHECK (content_length IS NULL OR content_length BETWEEN 1 AND 1048576),
    checksum_sha256 text CHECK (checksum_sha256 IS NULL OR checksum_sha256 ~ '^[a-f0-9]{64}$'),
    created_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    updated_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    deleted_at timestamptz,
    FOREIGN KEY(project_id,owner_id) REFERENCES projects(id,owner_id),
    UNIQUE(id,owner_id), UNIQUE(id,project_id,owner_id),
    CHECK(updated_at>=created_at),
    CHECK((source_kind='local-file' AND source->>'kind'='local-file') OR (source_kind='remote-object' AND source->>'kind'='remote-object')),
    CHECK(
      (status='awaiting-upload' AND source_kind='local-file' AND content_path IS NULL AND content_length IS NULL AND deleted_at IS NULL) OR
      (status='ready' AND source_kind='local-file' AND content_path IS NOT NULL AND content_length IS NOT NULL AND checksum_sha256 IS NOT NULL AND deleted_at IS NULL) OR
      (status='ready' AND source_kind='remote-object' AND content_path IS NULL AND deleted_at IS NULL) OR
      (status='deleted' AND deleted_at IS NOT NULL)
    )
);

CREATE TABLE analysis_runs (
    position bigint PRIMARY KEY DEFAULT nextval('run_position_seq') CHECK (position BETWEEN 1 AND 999999999999999999),
    id text GENERATED ALWAYS AS ('run_' || lpad(position::text,4,'0')) STORED UNIQUE,
    project_id text NOT NULL,
    dataset_id text NOT NULL,
    owner_id text NOT NULL CHECK (owner_id ~ '^[a-z][a-z0-9-]{2,31}$'),
    status text NOT NULL CHECK (status IN ('queued','running','completed','failed','canceled')),
    parameters jsonb NOT NULL CHECK (jsonb_typeof(parameters)='object'),
    callback_url text CHECK (callback_url IS NULL OR callback_url ~ '^https://hooks[.]example[.]test(?:/[^#[:space:]]*)?$'),
    progress integer NOT NULL DEFAULT 0 CHECK (progress BETWEEN 0 AND 100),
    cancellation_requested_at timestamptz,
    failure_code text,
    failure_detail text,
    created_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    updated_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    completed_at timestamptz,
    FOREIGN KEY(project_id,owner_id) REFERENCES projects(id,owner_id),
    FOREIGN KEY(dataset_id,project_id,owner_id) REFERENCES datasets(id,project_id,owner_id),
    UNIQUE(id,owner_id), CHECK(updated_at>=created_at),
    CHECK(
      (status='queued' AND progress=0 AND completed_at IS NULL) OR
      (status='running' AND progress BETWEEN 1 AND 99 AND completed_at IS NULL) OR
      (status='completed' AND progress=100 AND completed_at IS NOT NULL) OR
      (status IN ('failed','canceled') AND completed_at IS NOT NULL)
    ),
    CHECK(cancellation_requested_at IS NULL OR status IN ('queued','running','canceled'))
);

CREATE TABLE idempotency_records (
    owner_id text NOT NULL CHECK (owner_id ~ '^[a-z][a-z0-9-]{2,31}$'),
    operation_id text NOT NULL CHECK (operation_id ~ '^[A-Za-z][A-Za-z0-9]+$'),
    idempotency_key text NOT NULL CHECK (char_length(idempotency_key) BETWEEN 16 AND 64),
    request_fingerprint text NOT NULL CHECK (request_fingerprint ~ '^[a-f0-9]{64}$'),
    state text NOT NULL CHECK (state IN ('processing','completed')),
    resource_id text,
    response_status integer,
    response_headers jsonb,
    response_body jsonb,
    created_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    completed_at timestamptz,
    PRIMARY KEY(owner_id,operation_id,idempotency_key),
    CHECK((state='processing' AND response_status IS NULL AND completed_at IS NULL) OR
          (state='completed' AND response_status BETWEEN 200 AND 599 AND response_headers IS NOT NULL AND response_body IS NOT NULL AND completed_at IS NOT NULL))
);

CREATE TABLE pagination_cursors (
    handle bigint PRIMARY KEY DEFAULT nextval('cursor_handle_seq') CHECK (handle > 0),
    owner_id text NOT NULL,
    operation_id text NOT NULL,
    filter_fingerprint text NOT NULL CHECK (filter_fingerprint ~ '^[a-f0-9]{64}$'),
    boundary_position bigint NOT NULL CHECK (boundary_position>0),
    snapshot_position bigint NOT NULL CHECK (snapshot_position>=boundary_position),
    created_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    expires_at timestamptz NOT NULL DEFAULT clock_timestamp()+interval '30 minutes',
    CHECK(expires_at>created_at)
);

CREATE TABLE run_jobs (
    run_id text PRIMARY KEY REFERENCES analysis_runs(id) ON DELETE CASCADE,
    status text NOT NULL CHECK (status IN ('queued','leased','completed','canceled','dead')),
    available_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    lease_owner text,
    lease_expires_at timestamptz,
    lease_generation bigint NOT NULL DEFAULT 0 CHECK (lease_generation>=0),
    attempts integer NOT NULL DEFAULT 0 CHECK (attempts>=0),
    max_attempts integer NOT NULL DEFAULT 5 CHECK (max_attempts BETWEEN 1 AND 20),
    last_error text,
    created_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    updated_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    CHECK((status='leased' AND lease_owner IS NOT NULL AND lease_expires_at IS NOT NULL) OR
          (status<>'leased' AND lease_owner IS NULL AND lease_expires_at IS NULL))
);

CREATE TABLE run_events (
    position bigint PRIMARY KEY DEFAULT nextval('event_position_seq') CHECK (position BETWEEN 1 AND 999999999999999999),
    event_id text GENERATED ALWAYS AS ('evt_' || lpad(position::text,4,'0')) STORED UNIQUE,
    run_id text NOT NULL REFERENCES analysis_runs(id) ON DELETE CASCADE,
    owner_id text NOT NULL,
    status text NOT NULL CHECK (status IN ('queued','running','completed','failed','canceled')),
    progress integer NOT NULL CHECK (progress BETWEEN 0 AND 100),
    occurred_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    FOREIGN KEY(run_id,owner_id) REFERENCES analysis_runs(id,owner_id)
);

CREATE TABLE artifacts (
    position bigint PRIMARY KEY DEFAULT nextval('artifact_position_seq') CHECK (position BETWEEN 1 AND 999999999999999999),
    id text GENERATED ALWAYS AS ('art_' || lpad(position::text,4,'0')) STORED UNIQUE,
    run_id text NOT NULL REFERENCES analysis_runs(id), owner_id text NOT NULL,
    name text NOT NULL CHECK (char_length(name) BETWEEN 1 AND 120),
    media_type text NOT NULL CHECK (media_type IN ('application/json','text/plain')),
    size bigint NOT NULL CHECK (size>=1),
    checksum_sha256 text NOT NULL CHECK (checksum_sha256 ~ '^[a-f0-9]{64}$'),
    storage_key text NOT NULL UNIQUE,
    created_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    FOREIGN KEY(run_id,owner_id) REFERENCES analysis_runs(id,owner_id),
    UNIQUE(run_id,name)
);

CREATE TABLE webhook_subscriptions (
    position bigint PRIMARY KEY DEFAULT nextval('subscription_position_seq') CHECK (position BETWEEN 1 AND 999999999999999999),
    id text GENERATED ALWAYS AS ('whs_' || lpad(position::text,4,'0')) STORED UNIQUE,
    owner_id text NOT NULL CHECK (owner_id ~ '^[a-z][a-z0-9-]{2,31}$'),
    target_url text NOT NULL CHECK (target_url ~ '^https://hooks[.]example[.]test(?:/[^#[:space:]]*)?$'),
    event_types text[] NOT NULL CHECK (cardinality(event_types) BETWEEN 1 AND 2),
    secret_ciphertext bytea NOT NULL,
    secret_hint text NOT NULL CHECK (secret_hint ~ '^\*{4}.{4}$'),
    enabled boolean NOT NULL DEFAULT true,
    created_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    UNIQUE(id,owner_id),
    CHECK(event_types <@ ARRAY['analysis.completed','analysis.failed']::text[]),
    CHECK(cardinality(event_types) = 1 OR event_types[1] IS DISTINCT FROM event_types[2])
);

CREATE TABLE outbox_events (
    position bigint PRIMARY KEY DEFAULT nextval('event_position_seq') CHECK (position BETWEEN 1 AND 999999999999999999),
    event_id text GENERATED ALWAYS AS ('evt_' || lpad(position::text,4,'0')) STORED UNIQUE,
    event_type text NOT NULL CHECK (event_type IN ('analysis.completed','analysis.failed')),
    run_id text NOT NULL REFERENCES analysis_runs(id), owner_id text NOT NULL,
    payload jsonb NOT NULL CHECK (jsonb_typeof(payload)='object'),
    occurred_at timestamptz NOT NULL DEFAULT clock_timestamp(), expanded_at timestamptz,
    FOREIGN KEY(run_id,owner_id) REFERENCES analysis_runs(id,owner_id)
);

CREATE TABLE webhook_deliveries (
    position bigint PRIMARY KEY DEFAULT nextval('delivery_position_seq') CHECK (position BETWEEN 1 AND 999999999999999999),
    id text GENERATED ALWAYS AS ('dlv_' || lpad(position::text,6,'0')) STORED UNIQUE,
    event_id text NOT NULL REFERENCES outbox_events(event_id) ON DELETE CASCADE,
    subscription_id text REFERENCES webhook_subscriptions(id),
    delivery_kind text NOT NULL CHECK (delivery_kind IN ('subscription','callback')),
    target_url text NOT NULL CHECK (target_url ~ '^https://hooks[.]example[.]test(?:/[^#[:space:]]*)?$'),
    status text NOT NULL CHECK (status IN ('pending','leased','delivered','dead')),
    attempts integer NOT NULL DEFAULT 0 CHECK (attempts>=0), max_attempts integer NOT NULL DEFAULT 8 CHECK (max_attempts BETWEEN 1 AND 20),
    available_at timestamptz NOT NULL DEFAULT clock_timestamp(), lease_owner text, lease_expires_at timestamptz,
    lease_generation bigint NOT NULL DEFAULT 0 CHECK (lease_generation>=0),
    delivered_at timestamptz, response_status integer, last_error text,
    created_at timestamptz NOT NULL DEFAULT clock_timestamp(), updated_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    UNIQUE(event_id,delivery_kind,target_url),
    CHECK((status='leased' AND lease_owner IS NOT NULL AND lease_expires_at IS NOT NULL) OR
          (status<>'leased' AND lease_owner IS NULL AND lease_expires_at IS NULL)),
    CHECK((delivery_kind='subscription' AND subscription_id IS NOT NULL) OR
          (delivery_kind='callback' AND subscription_id IS NULL))
);
