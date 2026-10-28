CREATE TABLE IF NOT EXISTS artifacts (
  artifact_id text PRIMARY KEY, tenant_id text NOT NULL, run_id text NOT NULL, attempt_id text NOT NULL,
  sha256 text NOT NULL, size_bytes bigint NOT NULL CHECK (size_bytes >= 0), object_key text NOT NULL UNIQUE,
  state text NOT NULL CHECK (state IN ('staged','published','orphaned','expired')), version bigint NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now()
);
CREATE UNIQUE INDEX IF NOT EXISTS artifacts_attempt_checksum_uq ON artifacts(run_id, attempt_id, sha256);
