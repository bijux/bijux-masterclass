CREATE TABLE graph_subscription_checkpoints (
    subscriber_id text NOT NULL,
    operation_sha256 text NOT NULL,
    subject_id text NOT NULL,
    last_sequence bigint NOT NULL CHECK (last_sequence >= 0),
    updated_at timestamptz NOT NULL,
    PRIMARY KEY (subscriber_id, operation_sha256, subject_id)
);
