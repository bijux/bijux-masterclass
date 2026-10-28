# Checkpoint — Module 05: Queries, Stable Pagination, and Authorized Access

## Required result

Project, dataset, and run listings are stable, owner-bound, and resistant to cursor tampering.

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

## Defend the design

1. Answer the central question: **How do list and retrieval operations remain stable, efficient, and non-leaking while data changes?**
2. Demonstrate this capstone result: Project, dataset, and run listings are stable, owner-bound, and resistant to cursor tampering.
3. Show the planted defect, the first failing oracle, and the retained regression.
4. Explain why this invariant is shared across languages: cursor state is bound to principal, operation, normalized filters, boundary, high-water position, and expiry.
5. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—Project, dataset, and run listings are stable, owner-bound, and resistant to cursor tampering.—all focused checks pass, the **Queries, Stable Pagination, and Authorized Access** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
