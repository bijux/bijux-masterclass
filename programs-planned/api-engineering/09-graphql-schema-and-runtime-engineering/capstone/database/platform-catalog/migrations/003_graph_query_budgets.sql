CREATE TABLE graph_client_budgets (
    client_name text PRIMARY KEY,
    maximum_cost integer NOT NULL CHECK (maximum_cost > 0),
    maximum_fanout integer NOT NULL CHECK (maximum_fanout > 0),
    maximum_concurrent_operations integer NOT NULL CHECK (maximum_concurrent_operations > 0)
);
