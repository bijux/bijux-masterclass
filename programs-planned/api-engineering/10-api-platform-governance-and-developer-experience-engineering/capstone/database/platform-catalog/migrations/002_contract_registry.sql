-- Immutable contract-release registry. A version may be inserted once; its digest is not updated.
CREATE TABLE api_contract_releases (
    api_ref TEXT NOT NULL REFERENCES platform_entities(entity_ref) ON DELETE RESTRICT,
    version TEXT NOT NULL,
    protocol TEXT NOT NULL,
    sha256 CHAR(64) NOT NULL CHECK (sha256 ~ '^[0-9a-f]{64}$'),
    source_path TEXT NOT NULL,
    compatibility_evidence_path TEXT NOT NULL,
    lifecycle TEXT NOT NULL,
    published_at TIMESTAMPTZ NOT NULL,
    published_by TEXT NOT NULL,
    PRIMARY KEY (api_ref, version)
);

CREATE TABLE api_consumers (
    consumer_id TEXT NOT NULL,
    api_ref TEXT NOT NULL REFERENCES platform_entities(entity_ref) ON DELETE RESTRICT,
    version TEXT NOT NULL,
    owner_ref TEXT NOT NULL,
    criticality TEXT NOT NULL CHECK (criticality IN ('low','medium','high','critical')),
    environment TEXT NOT NULL,
    last_seen_at TIMESTAMPTZ,
    migration_status TEXT,
    PRIMARY KEY (consumer_id, api_ref, version)
);
