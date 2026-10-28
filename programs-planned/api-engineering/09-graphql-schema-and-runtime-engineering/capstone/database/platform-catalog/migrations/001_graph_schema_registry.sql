CREATE TABLE graph_schema_releases (
    schema_version text PRIMARY KEY,
    schema_sha256 text NOT NULL UNIQUE,
    published_at timestamptz NOT NULL,
    status text NOT NULL CHECK (status IN ('candidate', 'active', 'retired'))
);
