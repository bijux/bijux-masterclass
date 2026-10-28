CREATE TABLE IF NOT EXISTS service_catalog (
  service_name text PRIMARY KEY, owner text NOT NULL, data_owner boolean NOT NULL, contract_versions jsonb NOT NULL, lifecycle_state text NOT NULL
);
