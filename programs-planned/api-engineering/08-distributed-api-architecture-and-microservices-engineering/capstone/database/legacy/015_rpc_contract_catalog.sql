BEGIN;

CREATE TABLE IF NOT EXISTS rpc_contract_releases (
    rpc_api_version text PRIMARY KEY,
    protobuf_profile text NOT NULL,
    descriptor_sha256 text NOT NULL,
    catalogue_sha256 text NOT NULL,
    released_at timestamptz,
    evidence jsonb NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE IF NOT EXISTS rpc_method_ownership (
    method_path text PRIMARY KEY,
    capability_owner text NOT NULL,
    state_owner text NOT NULL,
    deadline_owner text NOT NULL,
    retry_profile text NOT NULL,
    security_profile text NOT NULL,
    updated_at timestamptz NOT NULL DEFAULT now()
);

COMMIT;
