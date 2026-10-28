# Module 01 — Event Thinking, Ownership, and Message Taxonomy

> **Program stage:** Course 6 of 10 — Extend the promise across asynchronous time.

> **Central question:** Which interactions are commands, immutable facts, queries, notifications, or private domain events, and who owns each public fact?

## Where this module fits

Course 6 begins from this incoming boundary: **The Course 5 API 1.2 service with Security, Reliability, and Performance Profiles 1.0 and migrations 001–009.**

This module establishes the course’s first new responsibility by asking: **Which interactions are commands, immutable facts, queries, notifications, or private domain events, and who owns each public fact?** Its capstone increment is **Create the minimal message taxonomy, publication decision record, owner catalogue, and synchronous/asynchronous boundary**. That result is required before **AsyncAPI, CloudEvents, and Contract Architecture** can be studied honestly.

## Learning outcomes

- Separate commands, events, queries, notifications, domain events, and integration events.
- Name events as immutable facts rather than implementation instructions.
- Assign one authoritative producer to every event type.
- Decide whether an asynchronous boundary creates useful temporal or ownership separation.
- Design event granularity without leaking database rows or private implementation models.
- Use subject, correlation, causation, and process identity for distinct purposes.
- Reject event-driven designs that merely replace an ordinary function call with a queue.

## Capstone increment

Create the minimal message taxonomy, publication decision record, owner catalogue, and synchronous/asynchronous boundary.

## Core event model

### 1. Asynchrony is a semantic decision, not a transport setting

A synchronous interaction couples the caller to an immediate outcome. The caller knows whether the
request was accepted, rejected, or completed before it continues. An asynchronous interaction accepts
that producer and consumer may be separated in time. The producer records a fact or request and does
not depend on every downstream reaction completing during the original call.

Temporal decoupling is useful when reactions have different availability, scaling, ownership, or
latency requirements. It is not automatically useful when the caller needs an immediate authoritative
answer. Authentication, authorization decisions, uniqueness checks, and commands whose result changes
what the caller may safely do next often remain synchronous.

Replacing `notification_service.send()` with `publish("notification")` is not sufficient evidence of a
good boundary. The event must have stable meaning beyond the current implementation, and the producer
must be able to commit that fact without pretending that consumers have already acted.

### 2. Commands describe intent; events describe facts

`StartAnalysis` is a command. It asks the Analysis control plane to attempt a state transition. It may
be denied because the run is already terminal, the dataset is unavailable, or the caller lacks
authority. `AnalysisRunStarted` is an event. It states that the owning service accepted the transition
and committed it.

Commands normally have one logical handler. Events may have zero, one, or many consumers. A command can
be rejected; an event should not be “rejected” as though the recorded fact became false. A consumer may
reject a malformed or unauthorized message, but that is a delivery decision, not a reversal of history.

The course uses imperative names for commands and past-tense names for facts. Naming is not cosmetic.
It prevents consumers from treating an intention as if it were an authoritative outcome.

### 3. Domain events and integration events have different audiences

A domain event helps one application model its own state transition. It may contain rich internal
objects, transaction-local details, or implementation-specific types. An integration event is a
deliberately designed public message for independently deployed consumers. Publishing every domain
event verbatim makes private models part of the external contract.

The Analysis service may internally record `RunStateTransitioned(previous, next, reason, aggregate)`.
The public event `org.bijux.analysis.run.completed.v1` includes stable identifiers, duration, artifact
count, and completion time. It does not serialize the aggregate, ORM row, exception, or worker object.

A domain event can be transformed into one or more integration events inside the same transaction
boundary that persists the state change. The transformation is where privacy, ownership, semantic
stability, and consumer needs are enforced.

### 4. One fact has one authoritative owner

Multiple systems may observe or project a fact, but only one boundary should declare it authoritative.
The Analysis control plane owns run lifecycle events. The artifact component owns `ArtifactPublished`.
An analytics consumer may calculate that a run appears complete, but it must not emit a competing
`AnalysisRunCompleted` fact.

Ownership answers practical questions: Who may publish this type? Who approves schema changes? Which
durable state proves the fact? Who handles corrections? Which team responds when the event stream
contradicts the source of truth?

The catalogue records owner, source URI, channel, schema URI, partition key, classification, retention,
and replay policy. An event without an owner is an orphaned API.

### 5. Event granularity follows business meaning, not table mutations

Row-level change events are useful for change data capture, replication, and infrastructure pipelines,
but they are usually poor business contracts. `analysis_runs.updated` forces consumers to infer what
changed and why. It also exposes storage shape and produces ambiguous semantics when one transaction
updates several rows.

A useful integration event answers: what fact became true, for which subject, because of which accepted
cause, and what stable data do legitimate consumers need? `AnalysisRunCompleted` is more durable than
`analysis_runs.row_changed`. It lets consumers react without reconstructing domain meaning from
before/after columns.

Granularity must also avoid the opposite error: one enormous “RunLifecycleChanged” union that contains
every possible state. Separate facts make compatibility, authorization, retention, and consumer
interest explicit.

### 6. Correlation, causation, subject, and partition identity are not synonyms

The event `id` identifies one immutable occurrence. `subject` identifies the domain resource the fact
concerns, such as `analysis-runs/run-123`. `correlationid` groups a wider user or business journey.
`causationid` identifies the command or event that directly caused this event. `partitionkey` determines
the ordering domain used by the transport.

These values often contain related identifiers, but they solve different problems. Reusing one UUID for
all of them hides the process graph and can create accidental hot partitions. Conversely, inventing new
random values at every hop destroys traceability.

The capstone partitions run-lifecycle messages by run ID because state transitions for one run require
order. Correlation can span project creation, upload, run submission, artifact publication, and
notification delivery without forcing all those events into one partition.

### 7. A rigorous test decides whether to publish

Before creating an event, answer five questions. First, which durable fact already exists? Second, who
owns it? Third, which independent consumer needs it without a synchronous dependency? Fourth, which
delivery anomalies must be tolerated? Fifth, how long must the meaning remain intelligible?

If the “fact” does not exist until a consumer performs work, the message may be a command. If the
consumer must answer before the producer can commit, the interaction may need to remain synchronous.
If no independent consumer exists, an internal function, job, or domain event may be sufficient.

This test restrains event sprawl. The goal is not the largest possible event catalogue. It is the
smallest catalogue that creates valuable, explicit asynchronous boundaries.

## Engineering requirements

| Rule | Required behavior | Failure if omitted | Decisive evidence |
|---|---|---|---|
| Taxonomy explicit | Every message is classified as command, integration event, internal domain event, query, or notification. | Consumers treat intentions as facts or facts as instructions. | Message taxonomy and worked workflow map |
| Authoritative owner | Each integration event has exactly one producer boundary and durable source of truth. | Conflicting publishers create irreconcilable history. | Event catalogue owner and source fields |
| Fact-oriented name | Event type uses a stable past-tense business fact and a major version. | Implementation commands or row mutations become public contracts. | Type naming review and catalogue |
| Consumer independence | At least one legitimate reaction can occur later without changing the fact. | A queue replaces a function call without useful decoupling. | Consumer catalogue and dependency analysis |
| Minimal stable payload | Payload contains consumer-relevant facts, not private aggregates or database rows. | Storage shape and sensitive fields leak into the event API. | Schema review and data-classification field |
| Distinct identities | Event, subject, correlation, causation, and partition identities are defined separately. | Ordering, deduplication, and process diagnosis become ambiguous. | Envelope profile and shared vectors |
| Synchronous boundary retained | Immediate authoritative decisions remain request/response where appropriate. | Eventual answers are introduced where the caller requires certainty. | Interaction decision record |

## Worked failures

### Case 1 — `UpdateAnalysis` was published as an event

The name is imperative and does not state what became true. Three consumers interpret it differently:
one starts work, one updates a dashboard, and one sends a notification. A retry can therefore repeat a
command-like side effect.

Reclassify it as `StartAnalysis` with one handler if it expresses intent. Publish
`AnalysisRunStarted` only after the owner commits the accepted transition. The dashboard and
notification consumers subscribe to the fact, not to the request.

### Case 2 — every database update became `RowChanged`

Consumers inspect changed columns to infer completion. A migration renames `finished_at`, silently
breaking analytics. The event was a storage leak, not an API.

Replace the public message with `AnalysisRunCompleted`, emitted from the application transaction that
knows why the state changed. Keep row-level CDC, if needed, on a private infrastructure channel with a
separate owner and compatibility policy.

### Case 3 — two services publish completion

The worker emits `AnalysisRunCompleted` when computation ends; the API emits another after persisting
the result. Consumers see two event IDs and cannot tell which is authoritative.

The worker should report a completion result to the control plane. The control plane owns the run state,
commits the transition and artifact references, then writes one integration event to the outbox. Other
observations may use different event types but cannot claim the same fact.

### Case 4 — an event replaced a required authorization answer

A client publishes `ArtifactAccessRequested` and immediately attempts the download, assuming a later
consumer will deny unauthorized requests. The security boundary is now eventually consistent.

Keep authorization in the synchronous artifact request. An audit event may record the decision after
the fact. Asynchrony may extend consequences, but it cannot replace an immediate policy decision that
protects the current operation.

## Python implementation

The Python workshop uses the envelope and catalogue as executable design constraints.

Relevant paths:

```text
capstone/tracks/python-fastapi/src/event_engineering/envelope.py
capstone/tracks/python-fastapi/src/event_engineering/catalog.py
capstone/tracks/python-fastapi/src/event_engineering/partitioning.py
capstone/tracks/python-fastapi/tests_event/test_envelope_contracts.py
```

Build a fact with an injected clock and ID source:

```python
from datetime import datetime, timezone
from event_engineering.envelope import build_event

event = build_event(
    source="urn:bijux:analysis-control",
    event_type="org.bijux.analysis.run.completed.v1",
    subject="analysis-runs/run-123",
    dataschema="https://schemas.bijux.test/analysis-run-completed/v1",
    tenant_id="tenant-a",
    correlation_id="97b6ecb9-9884-4b0e-9cd2-cf60c56c4ac1",
    partition_key="run-123",
    data={
        "runId": "run-123",
        "durationMs": 8421,
        "artifactCount": 2,
        "occurredAt": "2026-08-07T08:00:00Z",
    },
    event_id_factory=lambda: "8e850ed1-08bb-4ca0-9b36-b2ffef21445d",
    clock=lambda: datetime(2026, 8, 7, 8, 0, tzinfo=timezone.utc),
)
```

The constructor validates identity, source, type profile, content type, schema URI, tenant, partition key,
timestamp, trace context, and canonical JSON compatibility. Event profile 1.0 permits integers only within
the JavaScript safe range; decimal quantities use a scaled integer with a declared unit or a decimal string.
Rejecting binary floating-point values avoids Python/JavaScript byte drift in signatures and identities. The
constructor does not decide that the event is semantically justified; the taxonomy and catalogue perform that
review.

Then register the type in `EventCatalog`. An unregistered type must fail before publication. The exercise is
to make ownership executable rather than leave it in a diagram.

## TypeScript implementation

The TypeScript track uses the same envelope profile without imitating Python class structure.

Relevant paths:

```text
capstone/tracks/typescript-fastify/src/event-engineering/envelope.ts
capstone/tracks/typescript-fastify/src/event-engineering/partitioning.ts
capstone/tracks/typescript-fastify/test-event-core/core.test.mjs
```

The builder accepts explicit time and ID inputs in tests and returns an immutable plain object. Validation
rejects unsafe integer values before canonicalization because JavaScript `number` cannot preserve every
integer used by databases or offsets.

```typescript
const event = buildEvent({
  source: "urn:bijux:analysis-control",
  eventType: "org.bijux.analysis.run.completed.v1",
  subject: "analysis-runs/run-123",
  dataSchema: "https://schemas.bijux.test/analysis-run-completed/v1",
  tenantId: "tenant-a",
  correlationId: "97b6ecb9-9884-4b0e-9cd2-cf60c56c4ac1",
  partitionKey: "run-123",
  data: {
    runId: "run-123",
    durationMs: 8421,
    artifactCount: 2,
    occurredAt: "2026-08-07T08:00:00Z",
  },
  eventId: "8e850ed1-08bb-4ca0-9b36-b2ffef21445d",
  time: new Date("2026-08-07T08:00:00Z"),
});
```

The learning objective is not identical syntax. Both tracks must emit the same canonical envelope for the
same semantic input and reject the same ambiguous identities.

## Cross-language invariant

Given the same semantic fields, Python and TypeScript must produce byte-identical canonical JSON, the same
partition for a declared partition count, and the same catalogue decision. A language-specific default
timestamp, randomized hash, property order, or unsafe-number coercion cannot change event identity.

Shared vectors in `capstone/shared/vectors/envelope.json` and `partitioning.json` are the governing evidence.

## Design review

Review every proposed message with this sequence:

1. State the fact or intent in one sentence without transport vocabulary.
2. Name the authoritative owner and durable record.
3. Identify independent consumers and why they may react later.
4. Decide whether the message is a command, event, query, or notification.
5. Define event, subject, correlation, causation, and partition identities.
6. Remove internal model fields and sensitive data.
7. Record the synchronous alternative and explain why it is weaker.
8. Reject the message if no stable semantic boundary remains.

A review that starts with partitions or retention before it establishes meaning is in the wrong order.

## End-to-end worked example

A client submits `POST /analysis-runs` with an idempotency key. The HTTP operation remains synchronous until
the control plane validates authorization, dataset ownership, request shape, and uniqueness, then commits
a queued run. That public response is still governed by API 1.2.

Inside the same application boundary, the committed transition creates
`org.bijux.analysis.run.requested.v1`. The event subject is the run, correlation ID is inherited from the
user journey, causation ID is the accepted command identifier, and partition key is the run ID. The event
tells consumers that a run is durably queued; it does not claim that computation has started.

The worker plane consumes a command to start eligible work. When it obtains a valid lease and changes the
authoritative run state, the control plane emits `AnalysisRunStarted`. Later completion and artifact
publication are distinct facts with their own owners. Notification and analytics consumers react to those
facts without becoming part of the original HTTP transaction.

## Failure patterns

- **Broker-first architecture.** A transport is selected before the fact, owner, consumer, or failure window is known.
- **Imperative event names.** A command such as `UpdateRun` is broadcast and retried as though it were an immutable fact.
- **Database-shaped payload.** Consumers depend on columns, ORM objects, or private enum values rather than stable domain meaning.
- **Competing ownership.** Several producers emit the same event type without one authoritative source of truth.
- **Identity collapse.** Event ID, correlation ID, subject, causation ID, and partition key are treated as interchangeable.
- **Event sprawl.** Every internal transition becomes public even when no independent consumer or long-lived contract exists.

## Module synthesis

You are ready to leave this module when you can **separate commands, events, queries, notifications, domain events, and integration events, name events as immutable facts rather than implementation instructions, and assign one authoritative producer to every event type** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Plant two deliberately bad candidates: one imperative “event” and one row-change message** and requiring the following oracle: **The final catalogue contains only facts with one owner and at least one defensible independent consumer. Commands have one logical handler and remain distinguishable from facts. No public payload contains a database row, ORM object, lease token, stack trace, access token, or raw dataset content. The proposed partition key matches the smallest domain requiring order.**

The cumulative platform now includes **Create the minimal message taxonomy, publication decision record, owner catalogue, and synchronous/asynchronous boundary**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [AsyncAPI, CloudEvents, and Contract Architecture](../module-02-asyncapi-and-contract-architecture/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
