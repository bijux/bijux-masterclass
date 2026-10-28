# Reference Answers — Module 05: Worked answers — Module 05 — Schema Evolution, Compatibility, Replay, and Historical Truth

Read after attempting all twelve Schema Evolution, Compatibility, Replay, and Historical Truth exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Classify an optional addition

Structurally it is usually additive if old consumers ignore unknown fields and old records may omit it. Semantically define what absence means and ensure no consumer assumes presence. Historical events remain valid without the field. The release can be accepted or review-required according to the course’s strict-consumer policy.

## 2. Reject a required addition

Retained v1 events do not contain `region`, so current validators or consumers would reject history. The producer cannot retroactively change those facts. Keep the field optional in v1 with absence semantics, derive it in a projection when defensible, or introduce a new major event type.

## 3. Review an enum expansion

Output widening can break generated exhaustive unions, default-throw switches, metrics labels, or database constraints. Run known-consumer fixtures with an unknown value and require a safe fallback. If consumers cannot tolerate it, introduce a new version or coordinated migration.

## 4. Choose v2 or upcasting

A rename plus meaning change is not a representation-only transformation. An upcaster cannot know execution time from old wall-clock duration. Introduce v2 or add a new optional field whose absence remains unknown for old records. Do not copy the old number into a semantically different field.

## 5. Model unknown history

Use nullable/optional unknown or a tagged value rather than zero. Zero asserts that no artifacts existed, which may be false. A later enrichment projection may consult an immutable historical source, but the original event remains unchanged and the enrichment provenance is explicit.

## 6. Design a correction

Publish a versioned `AnalysisRunCompletionCorrected` fact referencing the original event ID and subject, containing corrected fields, reason code, correction time, and authority. Projections apply latest correction policy. The original remains for audit; security/privacy policies still govern retention.

## 7. Bound a replay

Include replay ID, owner, consumer/effect version, allowed event types, tenant/date or offset range, maximum events, source checkpoint, isolated target, concurrency, dry-run/apply mode, side-effects disabled, abort thresholds, comparison oracle, and approval.

## 8. Disable side effects

Pass replay mode explicitly into handlers, route projection-only effects to an isolated target, deny outbound adapters by capability, use a replay-specific consumer identity, and test that no outbound outbox rows are created. Environment naming alone is insufficient.

## 9. Handle live catch-up

Record a source high-water checkpoint, replay history into a new target through that point, consume post-checkpoint events into the same target using inbox dedupe, reconcile with source truth, then atomically switch readers. Keep v1 for rollback until confidence and retention windows close.

## 10. Version inbox identity

Use keys such as `(analytics-completion:v1, eventId)` and `(analytics-completion:v2, eventId)`. Each version has its own projection target and can process the same fact once. Do not delete or reuse v1 inbox rows.

## 11. Reject nondeterminism

Current rates make historical results depend on replay date and network state. Capture the applicable rate/version as an event fact, use a versioned immutable rate table keyed by event time, or separate the enrichment into a new dated projection. Replay must use the same inputs.

## 12. Evaluate a release

Reject or hold the release. Structural compatibility is only one gate. An unregistered event lacks owner/retention/security governance, and absent replay fixtures leave historical readability unproven. The evaluator should name both reasons rather than returning a generic schema failure.
