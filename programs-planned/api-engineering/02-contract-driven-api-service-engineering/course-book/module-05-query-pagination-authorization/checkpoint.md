# Checkpoint — Module 05: Queries, Stable Pagination, and Authorized Access

## Required result

Implement owner-bound, filter-bound, high-water keyset traversal and evidence-backed query plans.

## Demonstrate

- Bind queries to principal, operation, filters, and order.
- Use opaque server-side cursor handles.
- Prevent duplicates and omissions during a traversal.
- Conceal foreign-resource existence where policy requires it.
- Read query plans and index use.

## Commands

```bash
make predecessor-proof
make operation-proof
make module-proof MODULE=05 TRACK=python
make module-proof MODULE=05 TRACK=typescript
make core-proof
```

## Evidence to retain

- baseline transcript proving the previous checkpoint before **Queries, Stable Pagination, and Authorized Access** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Queries, Stable Pagination, and Authorized Access**
- focused result for: Bind queries to principal, operation, filters, and order.
- public, durable, security, or operational observation showing: Project, dataset, and run listings are stable, owner-bound, and resistant to cursor tampering.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **stable authorized pagination**
- a limitation statement naming every live dependency required to support the strongest **Queries, Stable Pagination, and Authorized Access** claim but not exercised

## Defend the design

1. Answer the central question: **How do list and retrieval operations remain stable, efficient, and non-leaking while data changes?**
2. Demonstrate this capstone result: Project, dataset, and run listings are stable, owner-bound, and resistant to cursor tampering.
3. Show the **Queries, Stable Pagination, and Authorized Access** defect, the first failing oracle, and the exact regression retained after repair.
4. Explain why this invariant is shared across languages: cursor state is bound to principal, operation, normalized filters, boundary, high-water position, and expiry.
5. State which environment-backed **Queries, Stable Pagination, and Authorized Access** route was not run and how that limits the claim.

## Continue only when

Continue when the system again provides this module result—Project, dataset, and run listings are stable, owner-bound, and resistant to cursor tampering.—all focused checks pass, the **Queries, Stable Pagination, and Authorized Access** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
