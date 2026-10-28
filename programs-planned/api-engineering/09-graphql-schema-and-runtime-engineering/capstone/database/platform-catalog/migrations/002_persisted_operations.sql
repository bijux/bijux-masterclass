CREATE TABLE graph_persisted_operations (
    operation_sha256 text PRIMARY KEY,
    operation_name text NOT NULL,
    client_name text NOT NULL,
    client_version text NOT NULL,
    document text NOT NULL,
    status text NOT NULL CHECK (status IN ('active', 'deprecated', 'retired')),
    UNIQUE (client_name, client_version, operation_name)
);
