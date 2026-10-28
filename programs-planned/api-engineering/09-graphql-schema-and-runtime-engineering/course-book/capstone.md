# Capstone: Analysis Graph

The graph gateway sits over the services extracted in Course 8.

```text
                         Analysis Graph Gateway
                          /        |        \
                         /         |         \
                        v          v          v
                Analysis Control  Artifact  Notification
```

The gateway owns:

- schema and operation admission;
- request-scoped context and loaders;
- graph-specific demand limits;
- composition and partial-response policy;
- graph telemetry and client-operation inventory.

It does not own project, run, artifact, or notification state. Mutations delegate to the owning service. Nested fields call the service that owns the fact. The gateway may cache only under an explicit consistency and authorization policy.

## Principal workflow

A client requests a project and its recent analysis runs. For each run it selects artifacts and delivery status. A naïve resolver produces one analysis call, one artifact call per run, and one notification call per run. The corrected runtime batches artifacts and delivery summaries once per request.

The client starts an analysis through a mutation. The gateway passes the client idempotency key to Analysis Control. It does not create a graph-only duplicate-prevention mechanism that can diverge from the authoritative command.

A completed run is observed through a subscription sourced from Analysis Events API 1.0. Resume begins after a sequence value. Duplicate events are suppressed; a gap stops delivery and requires replay.

## Final result

By Module 10 the capstone contains:

- Analysis Graph API 1.0 SDL;
- ten trusted operation documents;
- Python and TypeScript semantic tracks;
- optional Strawberry and Yoga adapters;
- query budget and persisted-operation registries;
- field ownership, authorization, nullability, and consistency policies;
- a real loopback graph-composition laboratory;
- release compatibility fixtures;
- a sanitized Course 10 platform handoff.
