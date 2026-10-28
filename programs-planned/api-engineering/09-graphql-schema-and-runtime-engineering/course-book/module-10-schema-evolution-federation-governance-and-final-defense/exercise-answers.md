# Worked answers — Schema Evolution, Federation, Governance, and Final Defense

Compare the decision rule and evidence, not just wording.

## 1. Why is schema diff alone insufficient?

It does not show whether supported clients use a changed coordinate or whether runtime behavior and budgets remain safe.

**Decisive evidence.** Run both structural diff and every supported persisted operation with budget, ownership, and client fixtures. Either layer alone can miss a real consumer or operational break.

## 2. What makes removing a field safe?

All supported operations and clients have stopped using it, deprecation and migration are complete, and release evidence proves no dependency.

**Decisive evidence.** Prove no supported operation, generated client, documented workflow, or retained compatibility window uses the field. Deprecation and telemetry alone are not deletion evidence.

## 3. Why is output non-null to nullable breaking?

Generated clients and application logic may assume a value always exists. The new schema weakens that promise.

**Decisive evidence.** Compile supported clients and inject a source failure. Clients that previously assumed a value must now handle null, so the change weakens an existing output guarantee.

## 4. Why is adding an enum value review-required?

Exhaustive client switches may not handle it even though existing operations validate.

**Decisive evidence.** Execute exhaustive client handling against the new value and inspect persisted operations. Validation may pass while application code still fails, requiring review rather than automatic acceptance.

## 5. Who owns a federated field?

The service publishing and resolving the capability owns its facts; the graph platform owns composition policy and client contract review.

**Decisive evidence.** Compare federation SDL, source service contract, and ownership catalogue. The owning service defines and resolves the fact; composition metadata cannot transfer business authority.

## 6. Does federation eliminate N+1?

No. Entity fetch plans can still fan out. Batching, query planning, and budgets remain required.

**Decisive evidence.** Measure subgraph fetch plans and downstream calls for nested lists. Federation changes composition machinery, not the need for batching, budgets, and bounded fan-out.

## 7. What evidence approves a schema release?

Independent parse/validation, active operation validation, ownership completeness, authorization, budget, old-client execution, and partial-failure tests.

**Decisive evidence.** Require candidate SDL, schema diff, all active-operation validation, old-client execution, ownership completeness, authorization review, budget comparison, resolver tests, and rollback evidence.

## 8. What belongs in the Course 10 handoff?

Public schema, operation registry, field ownership, clients, budgets, versions, releases, and platform boundary—not private credentials or resolver internals.

**Decisive evidence.** Publish released schema, operation and client catalogues, field ownership, budgets, compatibility policy, version ledger, and sanitized evidence—never private data schemas or secrets.

## 9. When should a review-required change be rejected?

When supported clients cannot prove safe handling, source fan-out grows beyond policy, or rollback and observation evidence are missing.

**Decisive evidence.** Reject when a supported client cannot demonstrate tolerant handling, when an owner is missing, when demand increases beyond policy, or when rollout/rollback evidence is incomplete.

## 10. Why is deprecation not permission to delete?

It is only a signal. Actual removal requires consumer inventory and migration evidence.

**Decisive evidence.** Inspect supported-client and usage evidence after the deprecation window. The directive communicates intent; only completed migration and retirement evidence permits removal.

## 11. What is the final architecture defense?

Demonstrate query, mutation, partial failure, authorization denial, demand rejection, subscription resume, and compatible release while naming source authority and oracle.

**Decisive evidence.** Demonstrate one composed query, mutation replay, denial, partial failure, budget rejection, subscription resume, and schema release while naming authority, phase, oracle, and evidence for each.

## 12. How does Course 9 prepare Course 10?

It converts graph contracts and client operations into discoverable, measurable platform products with explicit ownership and lifecycle evidence.

**Decisive evidence.** Verify the outgoing handoff exactly. Course 10 receives governable product metadata and proof surfaces while service teams retain all business facts and decisions.
