# Worked Answers — Module 05: Schema Evolution, Compatibility, Replay, and Historical Truth

Use these solutions to audit your reasoning for **Schema Evolution, Compatibility, Replay, and Historical Truth**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Classify an optional addition

Structurally it is usually additive if old consumers ignore unknown fields and old records may omit it. Semantically define what absence means and ensure no consumer assumes presence. Historical events remain valid without the field. The release can be accepted or review-required according to the course’s strict-consumer policy.

The chapter’s decisive distinction is this: Adding an optional payload field generally lets old consumers continue reading if they ignore unknown properties. That assumption must be part of the consumer policy; a strict closed schema may reject the addition. Making an optional field required breaks historical events. Removing a field breaks consumers that rely on it.

## 2. Reject a required addition

Retained v1 events do not contain `region`, so current validators or consumers would reject history. The producer cannot retroactively change those facts. Keep the field optional in v1 with absence semantics, derive it in a projection when defensible, or introduce a new major event type.

In the cumulative capstone, the rule becomes concrete: A producer begins requiring durationMs in the completed schema. New records satisfy it, but historical v1 events lack the field. The candidate is rejected for in-place evolution. Keep it optional with defined absence semantics or introduce v2 with migration/upcasting.

## 3. Review an enum expansion

Output widening can break generated exhaustive unions, default-throw switches, metrics labels, or database constraints. Run known-consumer fixtures with an unknown value and require a safe fallback. If consumers cannot tolerate it, introduce a new version or coordinated migration.

A useful way to reason about the boundary is: completionKind gains partial. JSON Schema regards the addition as wider output, but a TypeScript consumer throws in its default branch. Classify the change as review-required, run consumer fixtures, and version the event if old consumers cannot safely ignore unknown values.

## 4. Choose v2 or upcasting

A rename plus meaning change is not a representation-only transformation. An upcaster cannot know execution time from old wall-clock duration. Introduce v2 or add a new optional field whose absence remains unknown for old records. Do not copy the old number into a semantically different field.

The implementation consequence is: JSON Schema can detect required-field, type, range, enum, and object-shape changes. It cannot detect that durationMs changed from execution time to wall-clock elapsed time while remaining an integer. It cannot know that a tenant ID changed normalization rules or a status value acquired a different business meaning.

## 5. Model unknown history

Use nullable/optional unknown or a tagged value rather than zero. Zero asserts that no artifacts existed, which may be false. A later enrichment projection may consult an immutable historical source, but the original event remains unchanged and the enrichment provenance is explicit.

The important nuance is: An immutable event may contain a fact later discovered to be wrong. Deleting or rewriting the old record destroys the audit trail and can leave consumers with inconsistent histories. Publish a correction or superseding event whose semantics identify the original event and the corrected value.

## 6. Design a correction

Publish a versioned `AnalysisRunCompletionCorrected` fact referencing the original event ID and subject, containing corrected fields, reason code, correction time, and authority. Projections apply latest correction policy. The original remains for audit; security/privacy policies still govern retention.

Under concurrency or failure, the distinction becomes: Projections apply correction policy and may expose only current truth, while the event log preserves how understanding changed. Security or legal deletion requirements are separate exceptional procedures with explicit tombstone/redaction design; immutability is not an excuse to retain prohibited data.

## 7. Bound a replay

Include replay ID, owner, consumer/effect version, allowed event types, tenant/date or offset range, maximum events, source checkpoint, isolated target, concurrency, dry-run/apply mode, side-effects disabled, abort thresholds, comparison oracle, and approval.

The design remains honest only if: A replay selects a source range, event types, tenant scope, consumer/effect version, target store, maximum event count, concurrency, start mode, and side-effect policy. It has an owner, approval, dry run, abort conditions, progress checkpoints, and reconciliation oracle.

## 8. Disable side effects

Pass replay mode explicitly into handlers, route projection-only effects to an isolated target, deny outbound adapters by capability, use a replay-specific consumer identity, and test that no outbound outbox rows are created. Environment naming alone is insufficient.

The consumer-facing consequence is: Notification code treats replay as ordinary delivery and calls the provider. Thousands of historical completion emails are resent. Replay policy must disable external effects by default; a projection rebuild and an effect reissue are separate operations with separate approvals.

## 9. Handle live catch-up

Record a source high-water checkpoint, replay history into a new target through that point, consume post-checkpoint events into the same target using inbox dedupe, reconcile with source truth, then atomically switch readers. Keep v1 for rollback until confidence and retention windows close.

The operational consequence is: Replaying directly into a live projection can mix old and current writes. Prefer a new isolated target, process history to a checkpoint, catch up with live events, compare, then switch readers. This is similar to an expand-and-contract database release.

## 10. Version inbox identity

Use keys such as `(analytics-completion:v1, eventId)` and `(analytics-completion:v2, eventId)`. Each version has its own projection target and can process the same fact once. Do not delete or reuse v1 inbox rows.

The strongest engineering interpretation is: It creates analytics:v2 in a new projection store. A dry run replays retained completion and artifact events with external effects disabled. Event time drives windows. After reconciliation against source artifacts and v1 totals, the replay catches up to a recorded checkpoint and readers switch. V1 remains available for rollback.

## 11. Reject nondeterminism

Current rates make historical results depend on replay date and network state. Capture the applicable rate/version as an event fact, use a versioned immutable rate table keyed by event time, or separate the enrichment into a new dated projection. Replay must use the same inputs.

The defect-oriented view is: A consumer that calls now() during handling will produce different results during replay. Durable calculations should use event time or explicit policy input. Random IDs, unordered map iteration, remote lookups, and mutable configuration can also make replay non-deterministic.

## 12. Evaluate a release

Reject or hold the release. Structural compatibility is only one gate. An unregistered event lacks owner/retention/security governance, and absent replay fixtures leave historical readability unproven. The evaluator should name both reasons rather than returning a generic schema failure.

Across the Python and TypeScript tracks, the invariant is: A producer release changes what new messages may contain. A consumer release changes what messages can be read. Retained history fixes a third population: messages already written. The release review must examine all three.
