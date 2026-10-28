# Worked Answers — Module 08: Deployment Independence, Version Skew, and Release Choreography

Use these solutions to audit your reasoning for **Deployment Independence, Version Skew, and Release Choreography**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why is a separate deployment pipeline not proof of independent deployment?

If callers, databases, or private models must change simultaneously, the pipeline only automates a coordinated release train.

**Decisive evidence:** mixed-version release matrix

The chapter’s decisive distinction is this: A service is not independently deployable merely because it has its own pipeline. Independence exists when a new version can be released, observed, and rolled back without requiring simultaneous changes to callers, databases, or other services.

**Evidence.** Require a remote-process fault experiment, ownership/reconciliation evidence, operational responsibility, and a quantified benefit exceeding distribution cost.

## 2. What does provider 1.1 need to preserve for consumer 1.0?

Existing request, response, event, and error semantics. Additive features must be optional or ignored safely.

**Decisive evidence:** old-consumer/new-provider contract test

In the cumulative capstone, the rule becomes concrete: A new Artifact Service may support a new retention attribute. Old Control callers ignore it. New Control callers must continue operating when routed to an old Artifact instance, perhaps with the feature disabled. If the new caller assumes the field always exists, the rollout is not safe.

## 3. How can consumer 1.1 work with provider 1.0?

Disable the new feature or use a fallback when the provider capability is absent. Requiring it immediately breaks rolling rollout.

**Decisive evidence:** new-consumer/old-provider test

A useful way to reason about the boundary is: Independent services coordinate through contracts and supported skew, not a mandatory all-service release train. However, some cross-service changes still require choreography. Independence means the choreography is explicit and bounded—not that coordination disappears.

**Evidence.** Require a remote-process fault experiment, ownership/reconciliation evidence, operational responsibility, and a quantified benefit exceeding distribution cost.

## 4. Why must event consumers understand retained historical versions?

Replay can deliver events produced long before the current deployment. Silent history rewrite breaks audit and compatibility.

**Decisive evidence:** replay compatibility proof

The implementation consequence is: A new Artifact Service may support a new retention attribute. Old Control callers ignore it. New Control callers must continue operating when routed to an old Artifact instance, perhaps with the feature disabled. If the new caller assumes the field always exists, the rollout is not safe.

## 5. What is the service-owned expand-and-contract sequence?

Expand owner schema, deploy compatible code, migrate/backfill, remove old writers, observe, then contract. Other services must not write the schema.

**Decisive evidence:** migration choreography report

The important nuance is: Independent services coordinate through contracts and supported skew, not a mandatory all-service release train. However, some cross-service changes still require choreography. Independence means the choreography is explicit and bounded—not that coordination disappears.

**Evidence.** Apply the boundary scorecard and ownership catalogue, then reject duplicate writers, shared private data, cyclic dependencies, and capabilities lacking reversal criteria.

## 6. Why can rollback fail after a successful code deployment?

New data, events, or external effects may not be readable or reversible by old code. Rollback boundaries must include data and contracts.

**Decisive evidence:** rollback rehearsal

Under concurrency or failure, the distinction becomes: A service is not independently deployable merely because it has its own pipeline. Independence exists when a new version can be released, observed, and rolled back without requiring simultaneous changes to callers, databases, or other services.

**Evidence.** Execute legacy, shadow, canary, cutover, rollback, and decommission states while checking mixed-version compatibility, divergence, and data ownership.

## 7. What does shadow comparison need beyond response equality?

Authorization, side-effect suppression, error classification, latency/resource bounds, and version identifiers.

**Decisive evidence:** shadow evidence report

The design remains honest only if: A service is not independently deployable merely because it has its own pipeline. Independence exists when a new version can be released, observed, and rolled back without requiring simultaneous changes to callers, databases, or other services.

**Evidence.** Execute legacy, shadow, canary, cutover, rollback, and decommission states while checking mixed-version compatibility, divergence, and data ownership.

## 8. Why is permanent support for every version harmful?

It multiplies code paths, tests, security surface, and ambiguity. Version skew should be bounded and retired deliberately.

**Decisive evidence:** version retirement policy

The consumer-facing consequence is: Independent services coordinate through contracts and supported skew, not a mandatory all-service release train. However, some cross-service changes still require choreography. Independence means the choreography is explicit and bounded—not that coordination disappears.

**Evidence.** Require a remote-process fault experiment, ownership/reconciliation evidence, operational responsibility, and a quantified benefit exceeding distribution cost.

## 9. How can Notification Service release independently?

Its event input remains compatible, its owned database migrates independently, its delivery behavior stays within contract, and rollback/replay do not require Control deployment.

**Decisive evidence:** notification release proof

The operational consequence is: A new Artifact Service may support a new retention attribute. Old Control callers ignore it. New Control callers must continue operating when routed to an old Artifact instance, perhaps with the feature disabled. If the new caller assumes the field always exists, the rollout is not safe.

## 10. What makes Artifact Service rollback harder than Notification rollback?

Artifact Service owns durable bytes and write authority; rollback may need old readers to understand new objects and must reconcile already stored effects.

**Decisive evidence:** artifact rollback sequence

The strongest engineering interpretation is: A new Artifact Service may support a new retention attribute. Old Control callers ignore it. New Control callers must continue operating when routed to an old Artifact instance, perhaps with the feature disabled. If the new caller assumes the field always exists, the rollout is not safe.

## 11. Why should a platform catalogue record but not centrally execute all migrations?

Visibility is useful, but central execution recreates a shared release train and weakens owner responsibility.

**Decisive evidence:** migration owner audit

The defect-oriented view is: Independent services coordinate through contracts and supported skew, not a mandatory all-service release train. However, some cross-service changes still require choreography. Independence means the choreography is explicit and bounded—not that coordination disappears.

**Evidence.** Require a remote-process fault experiment, ownership/reconciliation evidence, operational responsibility, and a quantified benefit exceeding distribution cost.

## 12. When is a breaking service release acceptable?

Only under an explicit major transition with consumer inventory, migration path, bounded coexistence, rollback, and approval. It cannot masquerade as an internal change.

**Decisive evidence:** breaking-release governance

Across the Python and TypeScript tracks, the invariant is: A service is not independently deployable merely because it has its own pipeline. Independence exists when a new version can be released, observed, and rolled back without requiring simultaneous changes to callers, databases, or other services.
