# Worked Answers — Module 10: Incremental Extraction, Strangler Migration, and Final Architecture Defense

Use these solutions to audit your reasoning for **Incremental Extraction, Strangler Migration, and Final Architecture Defense**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why is Notification Delivery extracted before Artifact Delivery?

It already consumes durable events, has independent retry/retention behavior, and can be shadowed without entering the run-completion critical path.

**Decisive evidence:** extraction sequence ADR

The chapter’s decisive distinction is this: Notification Service consumes completion events and builds its own state, but legacy delivery remains authoritative. External effects are suppressed. Compare subscription selection, payload identity, retry classification, and receiver policy over a representative replay window.

**Evidence.** Require a remote-process fault experiment, ownership/reconciliation evidence, operational responsibility, and a quantified benefit exceeding distribution cost.

## 2. Why is Artifact extraction delayed until capability authorization exists?

Otherwise the service must query Control synchronously or trust identity headers, preserving coupling or creating an authorization hole.

**Decisive evidence:** artifact prerequisites proof

In the cumulative capstone, the rule becomes concrete: GraphQL will add client-shaped graph access. Course 8 exports a boundary brief so that graph resolvers do not read service databases directly or create unbounded fan-out. Safe roots name an authority, staleness policy, batch strategy, and field authorization. Partial data must be explicit.

## 3. What is the authority during shadow mode?

The legacy path. Candidate results are compared and must suppress uncontrolled external effects.

**Decisive evidence:** shadow routing record

A useful way to reason about the boundary is: The final module changes production ownership while preserving every contract built in Courses 1–7. The safe method is incremental: create a candidate behind the existing boundary, compare it, move one authority at a time, and keep a path to stop.

**Evidence.** Execute legacy, shadow, canary, cutover, rollback, and decommission states while checking mixed-version compatibility, divergence, and data ownership.

## 4. Why must canary selection be stable?

Stateful users or resources should not alternate unpredictably between implementations, which can hide or create divergence.

**Decisive evidence:** deterministic canary test

The implementation consequence is: Course 8 includes merge-back criteria. If Notification and Control always release together, one team owns both, event lag creates no value, and on-call cost exceeds isolation benefit, merging Notification back into the modular service may be the correct architecture. The event contract can remain useful even if deployment changes.

## 5. How do you avoid uncontrolled dual writes during artifact extraction?

Backfill historical state, shadow reads, then move new write authority through one controlled path with idempotent import and reconciliation.

**Decisive evidence:** write-authority transition report

The important nuance is: In the primary track, add one failed transition and one rollback case. In the comparative track, review whether static types alone could prevent an unsafe dual writer or side-effecting shadow. They cannot; runtime ownership and proof remain necessary.

**Evidence.** Require a remote-process fault experiment, ownership/reconciliation evidence, operational responsibility, and a quantified benefit exceeding distribution cost.

## 6. What is required before decommission?

Consumer inventory, old writer removal, retention decision, credential and route removal, backup ownership, alert/runbook update, and reconciliation window completion.

**Decisive evidence:** decommission checklist

Under concurrency or failure, the distinction becomes: Notification Service consumes completion events and builds its own state, but legacy delivery remains authoritative. External effects are suppressed. Compare subscription selection, payload identity, retry classification, and receiver policy over a representative replay window.

**Evidence.** Require a remote-process fault experiment, ownership/reconciliation evidence, operational responsibility, and a quantified benefit exceeding distribution cost.

## 7. When can the legacy path be removed?

After cutover remains within correctness and SLO policy for the declared window, rollback evidence is archived, and no hidden consumers remain.

**Decisive evidence:** decommission gate

The design remains honest only if: In the primary track, add one failed transition and one rollback case. In the comparative track, review whether static types alone could prevent an unsafe dual writer or side-effecting shadow. They cannot; runtime ownership and proof remain necessary.

**Evidence.** Require a remote-process fault experiment, ownership/reconciliation evidence, operational responsibility, and a quantified benefit exceeding distribution cost.

## 8. What makes merge-back a valid outcome?

If independent ownership, scaling, and release value fail to materialize while coordination cost remains, merging restores cohesion without erasing contracts.

**Decisive evidence:** merge-back review

The consumer-facing consequence is: Course 8 includes merge-back criteria. If Notification and Control always release together, one team owns both, event lag creates no value, and on-call cost exceeds isolation benefit, merging Notification back into the modular service may be the correct architecture. The event contract can remain useful even if deployment changes.

## 9. Why does the Course 9 handoff forbid direct database joins?

GraphQL must compose through service contracts and batching; database joins would bypass ownership and recreate a distributed monolith at the graph layer.

**Decisive evidence:** GraphQL boundary brief

The operational consequence is: GraphQL will add client-shaped graph access. Course 8 exports a boundary brief so that graph resolvers do not read service databases directly or create unbounded fan-out. Safe roots name an authority, staleness policy, batch strategy, and field authorization. Partial data must be explicit.

## 10. What must a final defense say about Worker Plane?

It is an independently scalable compute deployment; Control remains the authority for leases, attempts, and run completion.

**Decisive evidence:** state ownership defense

The strongest engineering interpretation is: The final module changes production ownership while preserving every contract built in Courses 1–7. The safe method is incremental: create a candidate behind the existing boundary, compare it, move one authority at a time, and keep a path to stop.

**Evidence.** Require a remote-process fault experiment, ownership/reconciliation evidence, operational responsibility, and a quantified benefit exceeding distribution cost.

## 11. How do you prove the extraction did not weaken the public API?

Run the inherited HTTP conformance and user-journey proof against the cutover topology, including partial and failure outcomes.

**Decisive evidence:** public contract regression

The defect-oriented view is: The final module changes production ownership while preserving every contract built in Courses 1–7. The safe method is incremental: create a candidate behind the existing boundary, compare it, move one authority at a time, and keep a path to stop.

**Evidence.** Require a remote-process fault experiment, ownership/reconciliation evidence, operational responsibility, and a quantified benefit exceeding distribution cost.

## 12. What is the strongest sign that Course 8 succeeded?

The team can explain why only two services were extracted, how each owns its data and failures, and how to stop or reverse the decision.

**Decisive evidence:** final architecture defense

Across the Python and TypeScript tracks, the invariant is: Course 8 includes merge-back criteria. If Notification and Control always release together, one team owns both, event lag creates no value, and on-call cost exceeds isolation benefit, merging Notification back into the modular service may be the correct architecture. The event contract can remain useful even if deployment changes.
