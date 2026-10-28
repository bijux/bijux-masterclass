# Worked Answers — Module 10: Schema Evolution, Federation, Governance, and Final Defense

Use these solutions to audit your reasoning for **Schema Evolution, Federation, Governance, and Final Defense**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why is schema diff alone insufficient?

It does not show whether supported clients use a changed coordinate or whether runtime behavior and budgets remain safe.

**Decisive evidence.** Run both structural diff and every supported persisted operation with budget, ownership, and client fixtures. Either layer alone can miss a real consumer or operational break.

The chapter’s decisive distinction is this: A schema diff tells what changed; active-operation validation tells who is affected. Removing an unused field may be safe after proving no supported operation selects it. Adding a required argument breaks existing documents. Changing output from non-null to nullable breaks generated client assumptions. Adding enum or union members requires review because exhaustive clients may fail.

## 2. What makes removing a field safe?

All supported operations and clients have stopped using it, deprecation and migration are complete, and release evidence proves no dependency.

**Decisive evidence.** Prove no supported operation, generated client, documented workflow, or retained compatibility window uses the field. Deprecation and telemetry alone are not deletion evidence.

In the cumulative capstone, the rule becomes concrete: A candidate adds RunStatus.PAUSED. Existing documents still validate, but generated clients may use exhaustive switches. The release is review-required until supported clients prove safe handling. Removing AnalysisRun.status is rejected immediately because active operations select it.

## 3. Why is output non-null to nullable breaking?

Generated clients and application logic may assume a value always exists. The new schema weakens that promise.

**Decisive evidence.** Compile supported clients and inject a source failure. Clients that previously assumed a value must now handle null, so the change weakens an existing output guarantee.

A useful way to reason about the boundary is: Removing a field or changing an output type is clearly breaking. Making an input field required breaks callers that omit it. Changing a nullable output to non-null may look stricter but can increase null-bubbling blast radius and break error handling. Adding an output enum value is review-required because generated clients may use exhaustive switches. Changing cost or authorization policy can break operations even when SDL is identical.

## 4. Why is adding an enum value review-required?

Exhaustive client switches may not handle it even though existing operations validate.

**Decisive evidence.** Execute exhaustive client handling against the new value and inspect persisted operations. Validation may pass while application code still fails, requiring review rather than automatic acceptance.

The implementation consequence is: A candidate release passes only when the schema parses in an independent implementation, all active operations validate, field ownership is complete, cost budgets do not regress, authorization tests pass, old clients execute, and partial-response semantics remain truthful. Review-required changes pause for consumer evidence.

## 5. Who owns a federated field?

The service publishing and resolving the capability owns its facts; the graph platform owns composition policy and client contract review.

**Decisive evidence.** Compare federation SDL, source service contract, and ownership catalogue. The owning service defines and resolves the fact; composition metadata cannot transfer business authority.

The important nuance is: The capstone includes optional subgraph sketches to compare ownership-aligned federation with one centrally authored gateway schema. The baseline remains executable without federation tooling. A service should not become a subgraph merely because it exists.

## 6. Does federation eliminate N+1?

No. Entity fetch plans can still fan out. Batching, query planning, and budgets remain required.

**Decisive evidence.** Measure subgraph fetch plans and downstream calls for nested lists. Federation changes composition machinery, not the need for batching, budgets, and bounded fan-out.

Under concurrency or failure, the distinction becomes: The course includes a frontier federation sketch, not a claim that federation is required. Analysis Graph API 1.0 can be implemented by one gateway over independently owned services. Course 10 can decide whether platform scale justifies subgraph publication.

## 7. What evidence approves a schema release?

Independent parse/validation, active operation validation, ownership completeness, authorization, budget, old-client execution, and partial-failure tests.

**Decisive evidence.** Require candidate SDL, schema diff, all active-operation validation, old-client execution, ownership completeness, authorization review, budget comparison, resolver tests, and rollback evidence.

The design remains honest only if: The capstone registry stores schema release, operation documents, ownership coordinates, cost profile, client declarations, and release decisions. It is a governance system only if ownership and review are real. A folder of SDL files with no release policy is not a registry.

## 8. What belongs in the Course 10 handoff?

Public schema, operation registry, field ownership, clients, budgets, versions, releases, and platform boundary—not private credentials or resolver internals.

**Decisive evidence.** Publish released schema, operation and client catalogues, field ownership, budgets, compatibility policy, version ledger, and sanitized evidence—never private data schemas or secrets.

The consumer-facing consequence is: The final handoff contains the schema, persisted operations, field ownership, client catalogue, query budget, release evidence, and platform boundary. These are the inputs for API discovery, scorecards, lifecycle governance, SDK generation, and developer onboarding.

## 9. When should a review-required change be rejected?

When supported clients cannot prove safe handling, source fan-out grows beyond policy, or rollback and observation evidence are missing.

**Decisive evidence.** Reject when a supported client cannot demonstrate tolerant handling, when an owner is missing, when demand increases beyond policy, or when rollout/rollback evidence is incomplete.

The operational consequence is: Every field has a source authority and a graph owner responsible for naming, nullability, cost, and client behavior. Service teams review fields backed by their capabilities; the graph team reviews composition and global consistency. No central committee rewrites domain rules without the owner.

## 10. Why is deprecation not permission to delete?

It is only a signal. Actual removal requires consumer inventory and migration evidence.

**Decisive evidence.** Inspect supported-client and usage evidence after the deprecation window. The directive communicates intent; only completed migration and retirement evidence permits removal.

The strongest engineering interpretation is: Do not deprecate without a replacement when the capability remains necessary. Do not remove based only on low aggregate traffic; a low-volume critical client may still depend on it. Persisted-operation ownership gives a better decision basis than anonymous field counts.

## 11. What is the final architecture defense?

Demonstrate query, mutation, partial failure, authorization denial, demand rejection, subscription resume, and compatible release while naming source authority and oracle.

**Decisive evidence.** Demonstrate one composed query, mutation replay, denial, partial failure, budget rejection, subscription resume, and schema release while naming authority, phase, oracle, and evidence for each.

The defect-oriented view is: If a new field requires a source-service release, deploy the source capability before activating operations that select it. If old and new gateway versions overlap, persisted registry and schema routing must support that skew or the rollout must be coordinated explicitly.

## 12. How does Course 9 prepare Course 10?

It converts graph contracts and client operations into discoverable, measurable platform products with explicit ownership and lifecycle evidence.

**Decisive evidence.** Verify the outgoing handoff exactly. Course 10 receives governable product metadata and proof surfaces while service teams retain all business facts and decisions.

Across the Python and TypeScript tracks, the invariant is: The handoff makes clear that a developer portal or API platform may publish, discover, generate, score, and govern the graph, but it may not become the source of project, run, artifact, or delivery facts.
