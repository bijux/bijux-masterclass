# Module 05 — Schema Evolution, Compatibility, Replay, and Historical Truth

> **Program stage:** Course 6 of 6 — Extend the promise across asynchronous time.

> **Central question:** How do event schemas evolve while retained historical events remain immutable and replay remains intelligible?

## Where this module fits

Synchronous APIs can often retire old representations after clients migrate. Event systems retain facts for
days, months, or years, and consumers may process them long after publication. A schema change therefore has
two audiences: future producers and historical records. A change that looks additive in today’s source code
can still break an old consumer, invalidate a replay, or reinterpret past truth.

Compatibility is directional. Producers write messages and consumers read them. Making a field required
rejects old records. Removing a field can break consumers. Narrowing an enum can invalidate retained
history. Adding an enum value may be structurally additive but still break an exhaustive switch. Renaming a
field without an upcaster is a new contract, not a refactor.

Replay introduces another risk: a consumer built for current events may call external services, use current
time, or overwrite live state when given historical data. A safe replay is planned, bounded, observable,
side-effect controlled, versioned, and reversible. This module treats retained events as immutable public
data, not as disposable queue items.

## Capstone result

Classify compatibility, add upcasters, preserve source bytes, define retention, and run bounded dry-run replay.

Define event compatibility policy, accepted and rejected schema releases, an upcaster chain, and a bounded
replay workflow. Rebuild an analytics projection from retained events while preventing notifications and
other external side effects.

```text
capstone/event-case/compatibility-policy.yaml
capstone/releases/
capstone/replay/replay-policy.yaml
capstone/replay/example-plan.yaml
capstone/tracks/*/src/event-engineering/evolution.*
capstone/tracks/*/src/event-engineering/replay.*
```

## Learning outcomes

- evaluate event-schema changes from producer, current-consumer, and historical-record perspectives
- distinguish structural compatibility from semantic compatibility
- choose between additive evolution, new major event type, and upcasting
- keep immutable historical events separate from corrected projections
- design deterministic upcaster chains with explicit source and target versions
- plan replay with event bounds, consumer/effect version, checkpoints, and side-effect policy
- build new projections alongside old ones and verify before cutover
- gate releases on contract validity, compatibility, catalogue completeness, and replay safety

## Core event model

### 1. Event compatibility is a reader/writer relationship

A producer release changes what new messages may contain. A consumer release changes what messages can be
read. Retained history fixes a third population: messages already written. The release review must
examine all three.

Adding an optional payload field generally lets old consumers continue reading if they ignore unknown
properties. That assumption must be part of the consumer policy; a strict closed schema may reject the
addition. Making an optional field required breaks historical events. Removing a field breaks consumers
that rely on it.

The course policy classifies changes as accepted, review-required, or rejected rather than pretending
every addition is safe.

### 2. Structural and semantic compatibility are different

JSON Schema can detect required-field, type, range, enum, and object-shape changes. It cannot detect that
`durationMs` changed from execution time to wall-clock elapsed time while remaining an integer. It cannot
know that a tenant ID changed normalization rules or a status value acquired a different business
meaning.

Every schema release therefore includes semantic notes and invariant review. Unit changes require a new
field or major event version even when the encoded type remains the same. A comment edit is not enough
to protect independently developed consumers.

Shared examples and consumer fixtures provide additional evidence but do not prove all semantic uses.

### 3. Major event versions coexist instead of rewriting history

A breaking semantic change creates a new type such as
`org.bijux.analysis.run.completed.v2`. The v1 records remain v1 forever. During migration, the owner may
dual-publish v1 and v2 from one committed fact or provide a translation boundary, but must prevent two
logical facts from being counted twice.

Consumers migrate explicitly and record which type/version they accept. A catch-all subscription that
silently routes v2 into a v1 handler defeats versioning.

Old versions need deprecation, last-publish, retention, and retirement policy. Removing code before the
final retained v1 record expires makes replay impossible.

### 4. Upcasters translate representation, not history

An upcaster converts an old event representation into the input shape expected by a newer consumer. It
must be deterministic, side-effect-free, and explicit about source and target versions. It cannot invent
facts that were not present historically unless a documented deterministic rule or lookup supplies them.

Upcasting `artifactCount` from a missing field to `0` is only correct if absence historically meant zero.
If absence meant unknown, the target model must preserve unknown rather than fabricate certainty.

Chains should be short and tested with stored fixtures. A long chain of ad hoc mutations becomes an
undocumented alternate history.

### 5. Corrections are new facts, not edits to old events

An immutable event may contain a fact later discovered to be wrong. Deleting or rewriting the old record
destroys the audit trail and can leave consumers with inconsistent histories. Publish a correction or
superseding event whose semantics identify the original event and the corrected value.

Projections apply correction policy and may expose only current truth, while the event log preserves how
understanding changed. Security or legal deletion requirements are separate exceptional procedures with
explicit tombstone/redaction design; immutability is not an excuse to retain prohibited data.

The course’s public payloads minimize sensitive data partly because retained events are expensive to
erase safely.

### 6. Replay is a controlled deployment

A replay selects a source range, event types, tenant scope, consumer/effect version, target store,
maximum event count, concurrency, start mode, and side-effect policy. It has an owner, approval, dry run,
abort conditions, progress checkpoints, and reconciliation oracle.

Replaying directly into a live projection can mix old and current writes. Prefer a new isolated target,
process history to a checkpoint, catch up with live events, compare, then switch readers. This is similar
to an expand-and-contract database release.

A replay command without a bound is an operational hazard. `maximum_events` and allowed types are
mandatory in the capstone.

### 7. Event time and processing time affect replay results

A consumer that calls `now()` during handling will produce different results during replay. Durable
calculations should use event time or explicit policy input. Random IDs, unordered map iteration, remote
lookups, and mutable configuration can also make replay non-deterministic.

External side effects are disabled in dry-run and projection-rebuild modes. When a replay intentionally
reissues an effect, it uses a new approved effect version and idempotency namespace.

The replay report distinguishes selected, would-apply, applied, and skipped counts so no-op deduplication
is visible.

### 8. Release gates combine several proofs

A schema release is not accepted because the JSON files parse. The AsyncAPI document must remain valid;
examples must pass; compatibility policy must accept or flag changes; the catalogue must cover new
types; replay must remain safe; security classification and retention must be reviewed.

The capstone includes an additive candidate, a structurally breaking candidate, and a replay-unsafe
candidate. The release evaluator returns accepted, review-required, or rejected with reasons.

A manual override, when policy permits one, is recorded as a risk acceptance with owner and expiry—not
hidden by changing the proof.

## Engineering requirements

| Rule | Required behavior | Failure if omitted | Decisive evidence |
|---|---|---|---|
| Historical readability | Current consumers or an approved upcaster can read every retained event in scope. | Replay fails after a deployment. | Fixture corpus and upcaster tests |
| Directional comparison | Requiredness, properties, types, enums, and bounds are reviewed from writer/reader perspectives. | A syntactically small change breaks old records or consumers. | Compatibility report |
| Semantic review | Meaning, units, normalization, and invariants are reviewed beyond JSON Schema. | Same shape acquires incompatible meaning. | Release notes and consumer review |
| Immutable history | Published records are not rewritten for ordinary corrections. | Consumers observe divergent histories. | Correction policy and audit trail |
| Bounded replay | Replay declares scope, target, maximum count, mode, and side-effect policy. | A command reprocesses an unbounded stream into live state. | Replay plan validation |
| Deterministic handling | Projection logic depends on event facts and versioned policy, not current time or random state. | Rebuild differs from original processing. | Replay parity test |
| Release gate | Contract, compatibility, catalogue, security, and replay checks all contribute. | Schema parsing alone approves an unsafe release. | Release decision report |

## Worked failures

### Case 1 — optional became required

A producer begins requiring `durationMs` in the completed schema. New records satisfy it, but historical
v1 events lack the field. The candidate is rejected for in-place evolution. Keep it optional with defined
absence semantics or introduce v2 with migration/upcasting.

### Case 2 — enum addition broke an exhaustive consumer

`completionKind` gains `partial`. JSON Schema regards the addition as wider output, but a TypeScript
consumer throws in its default branch. Classify the change as review-required, run consumer fixtures,
and version the event if old consumers cannot safely ignore unknown values.

### Case 3 — replay resent every email

Notification code treats replay as ordinary delivery and calls the provider. Thousands of historical
completion emails are resent. Replay policy must disable external effects by default; a projection
rebuild and an effect reissue are separate operations with separate approvals.

### Case 4 — old events were rewritten

A cleanup job updates retained payloads to the latest schema. Event IDs stay the same but signatures,
original meaning, and consumer audit trails change. Restore immutable history and use deterministic
upcasters or a new versioned projection.

## Python implementation

`compare_object_schemas()` reports required fields, removed properties, type changes, enum changes, and
object closure differences. `UpcasterChain` registers deterministic adjacent transformations.

```text
capstone/tracks/python-fastapi/src/event_engineering/evolution.py
capstone/tracks/python-fastapi/src/event_engineering/replay.py
capstone/tracks/python-fastapi/tests_event/test_evolution_replay.py
```

A replay plan is immutable:

```python
plan = ReplayPlan(
    replay_id="replay-analytics-v2-001",
    consumer="analytics-completion:v2",
    mode="dry-run",
    allowed_types=frozenset({"org.bijux.analysis.run.completed.v1"}),
    maximum_events=100_000,
    side_effects="disabled",
)
```

The handler receives an explicit dry-run flag. It cannot infer replay from a global environment variable.

## TypeScript implementation

TypeScript uses explicit schema objects and deterministic transformation functions.

```text
capstone/tracks/typescript-fastify/src/event-engineering/evolution.ts
capstone/tracks/typescript-fastify/src/event-engineering/replay.ts
capstone/tracks/typescript-fastify/test-event-core/evolution-stream.test.mjs
```

Exhaustive switches are useful internally but must include an unknown-value strategy at public evolution
boundaries. A compile-time union generated from today’s schema does not make tomorrow’s new enum value safe.

Replay counters that may exceed safe integers are serialized as decimal strings or checked before conversion.

## Cross-language invariant

Both tracks must classify the same schema changes, produce the same upcasted canonical payload for fixture
history, select the same replay events, and report identical applied/skipped/would-apply counts. If one
runtime treats absent as `null` and the other as missing, the shared vector must expose the difference.

## Design review

Review evolution in this order: retained records, current consumers, new producers, semantic meaning,
replay determinism, and retirement. Do not begin with a version number. For every new field, document
absence semantics. For every removed or narrowed value, identify which historical record becomes invalid.

A replay review must include external side effects, target isolation, live-event catch-up, comparison oracle,
abort threshold, and rollback.

## End-to-end worked example

Analytics v2 adds a `successfulArtifactBytes` aggregate. The existing completion event does not contain byte
totals, and reconstructing them from current artifact tables would reinterpret history. The team chooses a
new additive `ArtifactPublished` consumer combined with completed events rather than pretending old
completion payloads contained the fact.

It creates `analytics:v2` in a new projection store. A dry run replays retained completion and artifact
events with external effects disabled. Event time drives windows. After reconciliation against source
artifacts and v1 totals, the replay catches up to a recorded checkpoint and readers switch. V1 remains
available for rollback.

## Failure patterns

- **Schema-only compatibility.** A unit or semantic change passes because encoded types remain equal.
- **Required-field addition.** New producer expectations invalidate retained history.
- **Enum optimism.** New output values break exhaustive consumers.
- **History rewrite.** Old payloads are edited to resemble current schemas.
- **Unbounded replay.** A consumer reprocesses all retained data with no maximum or abort condition.
- **Side-effect replay.** Emails, webhooks, or billing calls run during a projection rebuild.
- **Current-time dependence.** Replayed results differ because handlers call `now()` or remote mutable services.
- **Inbox deletion.** Deduplication history is removed to force a rebuild, repeating unrelated effects.

## Module synthesis

Classify compatibility, add upcasters, preserve source bytes, define retention, and run bounded dry-run replay. The central distinction is this: how do event schemas evolve while retained historical events remain immutable and replay remains intelligible? The checkpoint is complete only when the mechanism, failure, oracle, and evidence limitation can all be explained together.

## Next in the story

Safe evolution lets consumers live for years, but it does not tell us how to structure those consumers or
coordinate multi-step asynchronous outcomes. Module 06 designs consumer applications, process managers,
projections, commands, compensations, timeouts, and the boundary between orchestration and choreography.
