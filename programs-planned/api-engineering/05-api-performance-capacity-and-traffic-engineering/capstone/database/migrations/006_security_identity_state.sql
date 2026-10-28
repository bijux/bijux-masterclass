-- 006_security_identity_state.sql
CREATE TABLE IF NOT EXISTS revoked_access_tokens (
  issuer text NOT NULL,
  token_id text NOT NULL,
  subject_id text,
  revoked_at timestamptz NOT NULL,
  expires_at timestamptz NOT NULL,
  reason text NOT NULL,
  PRIMARY KEY (issuer, token_id)
);

CREATE TABLE IF NOT EXISTS api_keys (
  key_id text PRIMARY KEY,
  owner_id text NOT NULL,
  tenant_id text NOT NULL,
  digest bytea NOT NULL,
  scopes text[] NOT NULL,
  created_at timestamptz NOT NULL,
  expires_at timestamptz,
  revoked_at timestamptz,
  version integer NOT NULL DEFAULT 1 CHECK (version > 0)
);

CREATE TABLE IF NOT EXISTS webhook_replays (
  key_id text NOT NULL,
  delivery_id text NOT NULL,
  accepted_at timestamptz NOT NULL,
  expires_at timestamptz NOT NULL,
  PRIMARY KEY (key_id, delivery_id)
);
