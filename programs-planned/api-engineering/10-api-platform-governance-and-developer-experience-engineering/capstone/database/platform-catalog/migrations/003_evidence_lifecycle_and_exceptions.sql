CREATE TABLE platform_evidence (
    evidence_id TEXT PRIMARY KEY,
    entity_ref TEXT NOT NULL REFERENCES platform_entities(entity_ref) ON DELETE CASCADE,
    kind TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('pass','review','fail','not-executed')),
    source_path TEXT NOT NULL,
    collected_at TIMESTAMPTZ NOT NULL,
    expires_at TIMESTAMPTZ,
    payload_sha256 CHAR(64)
);

CREATE TABLE policy_exceptions (
    exception_id TEXT PRIMARY KEY,
    entity_ref TEXT NOT NULL REFERENCES platform_entities(entity_ref) ON DELETE CASCADE,
    rule_id TEXT NOT NULL,
    owner_ref TEXT NOT NULL,
    approved_by_ref TEXT NOT NULL,
    reason TEXT NOT NULL,
    compensating_control TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active','expired','revoked','closed')),
    CHECK (expires_at > created_at)
);

CREATE TABLE lifecycle_transitions (
    transition_id UUID PRIMARY KEY,
    api_ref TEXT NOT NULL REFERENCES platform_entities(entity_ref) ON DELETE RESTRICT,
    version TEXT NOT NULL,
    from_state TEXT NOT NULL,
    to_state TEXT NOT NULL,
    requested_by_ref TEXT NOT NULL,
    requested_at TIMESTAMPTZ NOT NULL,
    decision TEXT NOT NULL CHECK (decision IN ('allowed','blocked','review')),
    evidence JSONB NOT NULL
);
