# Orientation — Lock the distributed boundary

Course 9 starts from the exact Course 8 handoff. The graph layer may compose capabilities, but it may not erase the ownership, security, consistency, and failure boundaries already established. Orientation is therefore a proof exercise rather than an installation checklist.

## Outcomes

By the end of orientation you can:

- verify the predecessor handoff byte-for-byte;
- name the owner of project, run, artifact, delivery, worker, and gateway facts;
- distinguish a graph field from a service boundary;
- identify which capabilities belong in GraphQL and which remain HTTP, event, or gRPC interfaces;
- select one primary implementation track and use the other for semantic comparison;
- classify dependency-light, framework-backed, and environment-backed evidence.

## Step 1 — Verify the handoff

Run:

```bash
make doctor
make predecessor-proof
```

Inspect `capstone/predecessor/handoff/`. Its manifest is the authority. Do not repair a mismatch by editing the predecessor copy; replace it from the Course 8 release and rerun the proof.

The boundary documents establish:

- Analysis Control owns projects, datasets, runs, idempotency, and legal state transitions;
- Artifact Service owns artifact metadata and content delivery;
- Notification Service owns delivery attempts and summaries;
- the Worker Plane executes leased computation but does not own run truth;
- the Gateway owns edge routing and composition but no business state.

## Step 2 — Write the field-source map

For each proposed root, complete this table before opening the SDL:

| Root | Client task | Source authority | Consistency | Failure behavior |
|---|---|---|---|---|
| `project` | inspect one project and its related work | Analysis Control | authoritative | nullable root plus execution error |
| `analysisRun` | inspect one run | Analysis Control | authoritative | nullable root plus execution error |
| `artifact` | inspect artifact metadata | Artifact Service | authoritative | nullable root plus execution error |
| `deliverySummary` | inspect notification progress | Notification Service | projection with age | explicit staleness and nullable failure |
| `search` | discover supported objects | governed composition/projection | declared per result | bounded partial behavior |

Then name one forbidden implementation for each root. “Direct SQL join across private service databases” is forbidden even when it appears faster in a local benchmark.

## Step 3 — Decide interface placement

Classify each capability:

- typed client composition → GraphQL candidate;
- large byte transfer and conditional/range semantics → HTTP;
- durable state-change notification and replay → AsyncAPI/CloudEvents;
- internal typed invocation or streaming control → gRPC;
- business state ownership → source service, never the graph gateway.

`Artifact.downloadUrl` belongs in the graph; artifact bytes do not. `analysisRunUpdated` can be exposed as a GraphQL subscription, but its durable source remains Analysis Events API 1.0.

## Step 4 — Select a language track

Choose TypeScript when your primary goal is GraphQL.js ecosystem engineering and Python when your primary goal is scientific/data platform integration. Both semantic cores are complete. You implement and debug one track deeply and use shared vectors to review the other. You are not required to mirror framework syntax.

Record the choice in your learning log with one reason and one risk. A language choice is not evidence that the graph behavior is correct.

## Step 5 — Run the initial tours

```bash
make capstone-tour
make network-lab-proof
```

The dependency-light tour proves operation identity, admission, batching, mutation replay, partial data, subscription sequence handling, and release classification. The loopback network lab proves that composition crosses real process boundaries and that one source failure becomes explicit partial data.

These routes do not prove complete GraphQL standards conformance, production capacity, or operated multi-region behavior. The evidence ledger distinguishes:

- **dependency-light** — deterministic semantic mechanisms;
- **framework-backed** — complete GraphQL parser/executor adapters when dependencies are installed;
- **environment-backed** — external services, TLS, telemetry, and representative load.

## Orientation checkpoint

You may begin Module 1 only when you can explain, without reading notes:

1. why a graph edge is not permission to join databases;
2. why a resolver may compose facts but may not own them;
3. why artifact bytes remain outside GraphQL;
4. why a subscription is not the durable event source;
5. which evidence class each available proof route provides.

Run:

```bash
make orientation-proof
```
