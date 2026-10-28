CREATE TABLE platform_product_events (
    event_id UUID PRIMARY KEY,
    event_type TEXT NOT NULL,
    occurred_at TIMESTAMPTZ NOT NULL,
    consumer_id TEXT,
    api_ref TEXT,
    version TEXT,
    properties JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX platform_product_events_api_time_idx
    ON platform_product_events (api_ref, occurred_at DESC);

CREATE TABLE platform_support_cases (
    case_id TEXT PRIMARY KEY,
    category TEXT NOT NULL,
    entity_ref TEXT,
    accountable_owner_ref TEXT NOT NULL,
    opened_at TIMESTAMPTZ NOT NULL,
    first_response_at TIMESTAMPTZ,
    resolved_at TIMESTAMPTZ,
    status TEXT NOT NULL CHECK (status IN ('open','acknowledged','resolved','closed'))
);
