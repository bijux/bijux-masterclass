# Two-Week Study Plan — gRPC and Protobuf Engineering

## Rhythm

Course 7 uses ten teaching days over two weeks. Orientation freezes the incoming boundary before Day 1; each day moves from the engineer typed internal invocation and streaming model to transfer problems, a controlled experiment, and an evidence defense. The middle weekend is for repairing failed checkpoints, not adding features.

| Day | Module | Required result |
|---:|---|---|
| 1 | [RPC Boundaries, Service Ownership, and Interaction Choice](module-01-rpc-boundaries-and-service-ownership/index.md) | Publish an interaction decision record, service-ownership map, and minimal Analysis RPC surface without splitting the platform prematurely. |
| 2 | [Protobuf Modeling, Presence, and Semantic Types](module-02-protobuf-modeling-presence-and-semantic-types/index.md) | Complete the Analysis RPC 1.0 message model, publish cross-language presence and integer vectors, and document every field whose absence changes behavior. |
| 3 | [Wire Format, Unknown Fields, and Compatibility Discipline](module-03-wire-format-unknown-fields-and-compatibility/index.md) | Publish Analysis RPC compatibility policy 1.0, golden wire fixtures, and a release report that accepts one additive candidate while rejecting unsafe tag, enum, and method-shape changes. |
| 4 | [Unary RPCs, Metadata, Status, and Rich Errors](module-04-unary-rpcs-metadata-status-and-rich-errors/index.md) | Implement `CreateRun`, `GetRun`, and `CancelRun` with shared status vectors, safe metadata policy, and equivalent Python and TypeScript client behavior. |
| 5 | [Deadlines, Cancellation, Retries, and Idempotent Calls](module-05-deadlines-cancellation-retries-and-idempotent-calls/index.md) | Implement deadline-aware CreateRun and GetRun clients, persistent retry semantics, deterministic retry vectors, and fault-injection evidence for failures before invocation, before commit, after commit, and during response delivery. |
| 6 | [Streaming RPCs, Flow Control, and Backpressure](module-06-streaming-rpcs-flow-control-and-backpressure/index.md) | Implement `WatchRun`, `UploadDataset`, `DownloadArtifact`, and the worker `Work` stream with shared schedule vectors, bounded buffers, resumable observation, and stale-attempt fencing. |
| 7 | [Identity, Authorization, mTLS, and Tenant Isolation](module-07-identity-authorization-mtls-and-tenant-isolation/index.md) | Implement RPC security profile 1.0 with method policy, workload and user identity binding, tenant-isolation vectors, mTLS-ready configuration, and secure worker-stream authorization. |
| 8 | [Channels, Health, Discovery, Load Balancing, and Lifecycle](module-08-channels-health-discovery-load-balancing-and-lifecycle/index.md) | Implement channel and server lifecycle state machines, standard health semantics, bounded reconnect behavior, two-instance routing evidence, graceful drain, and an operational service configuration. |
| 9 | [Generation, Testing, Reflection, and Schema Governance](module-09-generation-testing-reflection-and-schema-governance/index.md) | Publish a reproducible generation pipeline, checked descriptor inventory, generated-client build matrix, runtime catalogue comparison, and Course 7 RPC release gate. |
| 10 | [HTTP, Events, and gRPC in One Architecture: Release and Final Defense](module-10-http-events-and-grpc-release-and-final-defense/index.md) | Release Analysis RPC API 1.0 behind the unchanged public HTTP API and Event API, execute the final defense, and publish a sanitized service-boundary dossier rather than prematurely splitting the system. |

## Suggested day

```text
08:30  retrieval practice and checkpoint repair
09:00  chapter reading and diagram reconstruction
11:00  worked examples and standards review
13:00  primary-track implementation reading
15:00  exercises before answers
17:00  controlled lab
19:30  evidence package and checkpoint defense
```

The two-week schedule is subordinate to evidence. If the engineer typed internal invocation and streaming argument becomes unclear, stop at the last green checkpoint, reduce the counterexample, and resume only after the owning mechanism is understood.

## Weekend synthesis

At the Week 1 boundary, reconstruct how Modules 1–5 change the platform while preserving this incoming state: The Course 6 HTTP API 1.2 and Analysis Events API 1.0 handoff with profiles and migrations through 012. Rerun those checkpoints and postpone every feature that does not serve the Course 7 responsibility.

## Recovery route

When a checkpoint fails:

1. isolate the first broken invariant;
2. restore the predecessor baseline if necessary;
3. reduce the failing case;
4. repair the owning mechanism;
5. retain the case as a regression;
6. update your explanation before continuing.
