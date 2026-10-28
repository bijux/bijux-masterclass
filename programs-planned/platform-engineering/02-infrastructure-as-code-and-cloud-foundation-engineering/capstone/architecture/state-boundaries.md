# State Boundaries

```text
bootstrap state
    S3 state bucket and state KMS key

foundation state
    network, identity, audit, backup bucket

workload-dev state
    Atlas host, data volume, target and edge
```

A state boundary is an authority and lifecycle boundary, not merely a way to
make plans shorter. Bootstrap recovery is independent because the state store
cannot safely depend on itself. Foundation changes are less frequent and have
a larger blast radius than workload replacement. Production uses a separate
state and apply role rather than a workspace in the development root.
