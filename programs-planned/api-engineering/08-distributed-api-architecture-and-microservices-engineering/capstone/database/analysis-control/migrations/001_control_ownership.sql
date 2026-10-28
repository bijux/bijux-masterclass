-- Analysis Control retains authoritative project, dataset metadata, run, idempotency, lease, and outbox state.
CREATE TABLE IF NOT EXISTS service_schema_metadata (service_name text PRIMARY KEY, schema_version integer NOT NULL);
INSERT INTO service_schema_metadata(service_name, schema_version) VALUES ('analysis-control', 1) ON CONFLICT (service_name) DO UPDATE SET schema_version = EXCLUDED.schema_version;
