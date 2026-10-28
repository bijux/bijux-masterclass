CREATE TABLE IF NOT EXISTS notification_run_view (
  run_id text PRIMARY KEY, tenant_id text NOT NULL, run_version bigint NOT NULL, state text NOT NULL, updated_at timestamptz NOT NULL
);
