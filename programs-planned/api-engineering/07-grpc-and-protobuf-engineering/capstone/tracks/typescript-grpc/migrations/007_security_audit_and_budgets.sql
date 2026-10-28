-- 007_security_audit_and_budgets.sql
CREATE TABLE IF NOT EXISTS security_audit_events (
  sequence_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  occurred_at timestamptz NOT NULL,
  actor_pseudonym text NOT NULL,
  action text NOT NULL,
  target_reference text,
  decision text NOT NULL CHECK (decision IN ('allow','deny','error')),
  reason_code text NOT NULL,
  correlation_id text NOT NULL,
  previous_digest bytea,
  event_digest bytea NOT NULL,
  minimized_context jsonb NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE IF NOT EXISTS abuse_quotas (
  tenant_id text NOT NULL,
  budget_name text NOT NULL,
  period_start timestamptz NOT NULL,
  consumed bigint NOT NULL CHECK (consumed >= 0),
  limit_value bigint NOT NULL CHECK (limit_value > 0),
  version integer NOT NULL DEFAULT 1 CHECK (version > 0),
  PRIMARY KEY (tenant_id, budget_name, period_start)
);

CREATE INDEX IF NOT EXISTS revoked_access_tokens_expiry_idx ON revoked_access_tokens (expires_at);
CREATE INDEX IF NOT EXISTS webhook_replays_expiry_idx ON webhook_replays (expires_at);
CREATE INDEX IF NOT EXISTS security_audit_events_time_idx ON security_audit_events (occurred_at);
