# Analysis Graph capstone

The capstone adds one graph interface over the distributed platform established in Course 8.

```text
GraphQL client
      |
      v
Analysis Graph Gateway
   /       |        \
  v        v         v
Analysis  Artifact  Notification
Control   Service   Service
```

The gateway owns GraphQL schema, operation admission, request-scoped batching, composition, and graph-specific telemetry. It owns no project, run, artifact, or delivery business fact.

The dependency-light runtime executes a governed set of persisted operations. Optional Strawberry and GraphQL Yoga adapters show how the same policies attach to complete GraphQL implementations.
