# Evidence Model

## Claims require the right oracle

The program separates evidence classes because a green check at one layer cannot prove another layer.

| Evidence class | Establishes | Does not establish |
|---|---|---|
| document and schema proof | parseability, references, examples, structural policy | live provider behavior |
| provider-neutral protocol proof | observed request and response behavior | durable database outcomes |
| pure domain proof | deterministic rules and state transitions | transaction or process behavior |
| database and storage proof | committed constraints, locks, bytes, and recovery state | user-perceived availability |
| adversarial security proof | a control rejects or constrains a threat case | absence of all vulnerabilities |
| lifecycle and fault proof | startup, drain, restart, deadline, and recovery behavior | production-scale capacity |
| telemetry proof | emitted diagnostic signals and propagation | authoritative business truth |
| workload and benchmark proof | behavior under a declared comparable workload | unrelated environments or future scale |
| broker and consumer proof | delivery attempts, deduplication, effects, and replay | all broker implementations |
| network and distributed proof | remote-call, partial-failure, and ownership behavior | operated multi-region reliability |
| governance proof | evidence-backed publication and lifecycle decisions | organizational adoption by itself |

## Evidence record

Every serious report should name:

```text
claim
owner
version
input or workload identity
environment identity
oracle
result
known exclusions
retained artifact
```

## Negative evidence

A proof is stronger when a planted defect demonstrates sensitivity. Every course includes defects or incompatible candidates that should fail before a valid candidate passes. A test suite that never rejects anything is not a trustworthy release gate.

## Environment boundary

When a required environment is missing, report `not-executed`. Do not substitute an in-memory simulator for a live transaction claim, a local broker for operated retention, or a laptop benchmark for production capacity.
