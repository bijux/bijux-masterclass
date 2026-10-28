-- Analysis API Platform catalog authority.
CREATE TABLE platform_entities (
    entity_ref TEXT PRIMARY KEY,
    kind TEXT NOT NULL,
    namespace TEXT NOT NULL,
    name TEXT NOT NULL,
    title TEXT NOT NULL,
    owner_ref TEXT,
    system_ref TEXT,
    lifecycle TEXT NOT NULL CHECK (lifecycle IN ('proposed','experimental','active','deprecated','retired')),
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    revision BIGINT NOT NULL DEFAULT 1,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (kind, namespace, name)
);

CREATE TABLE platform_relations (
    source_ref TEXT NOT NULL REFERENCES platform_entities(entity_ref) ON DELETE CASCADE,
    relation TEXT NOT NULL,
    target_ref TEXT NOT NULL REFERENCES platform_entities(entity_ref) ON DELETE RESTRICT,
    PRIMARY KEY (source_ref, relation, target_ref)
);

CREATE INDEX platform_relations_target_idx
    ON platform_relations (target_ref, relation, source_ref);
