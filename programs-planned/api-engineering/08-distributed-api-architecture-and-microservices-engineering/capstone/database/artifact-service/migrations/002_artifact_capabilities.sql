CREATE TABLE IF NOT EXISTS consumed_artifact_capabilities (
  capability_id text PRIMARY KEY, artifact_id text, consumed_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS artifacts_orphan_scan_idx ON artifacts(state, created_at);
