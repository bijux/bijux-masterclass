# Lab — Module 05: Queries, Stable Pagination, and Authorized Access

## Objective

Implement owner-concealed retrieval and a high-water-bounded cursor traversal that produces no duplicates or omissions among unchanged rows eligible at traversal start, excludes later inserts, rejects cursor/filter reuse, and follows verified index plans.

## Setup conditions

The previous baseline is: **One hundred concurrent identical submissions create one run; stale ETags fail atomically; replay survives restart.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How do list and retrieval operations remain stable, efficient, and non-leaking while data changes?*

## Failure action and investigation

1. **Define result-set identity and total ordering for project, dataset, and run lists.**
2. **Implement normalized filters and shared fingerprint vectors.**
3. **Implement persisted cursor creation, lookup, expiry, and cleanup.**
4. **Implement keyset queries with owner-qualified predicates, a first-page high-water bound, and deliberate projection/mapping boundaries.**
5. **Create tie-heavy and multi-owner fixture data.**
6. **Traverse pages while inserting later rows and separately mutating one filter-relevant field; assert the declared insertion guarantee and mutation limitation.**
7. **Capture representative `EXPLAIN` output and verify intended indexes.**
8. **Plant an offset cursor and preserve the smallest duplicate/omission reproducer before repair.**

### Required planted defect

> Replace one keyset cursor with an encoded offset, insert a row before page two, and capture the duplicate or omission.

Preserve the following evidence:

```text
prediction:
change introduced:
minimal setup:
first failing command:
public symptom:
durable/process state:
root cause:
repair:
regression path:
remaining limitation:
```

## Operational oracle

A cursor issued for one principal/filter cannot be used by another, and rows inserted beyond the captured high-water mark do not enter the traversal.

## Required evidence

- baseline transcript proving the previous checkpoint before **Queries, Stable Pagination, and Authorized Access** changes
- source, fixture, contract, migration, or configuration diff for this module
- focused result for: Bind queries to principal, operation, filters, and order.
- public, durable, security, or operational observation showing: Project, dataset, and run listings are stable, owner-bound, and resistant to cursor tampering.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **stable authorized pagination**
- a limitation statement naming every live database, network, process, telemetry backend, or operated exercise not run

## Cleanup and reset

1. Restore the control changed for **Queries, Stable Pagination, and Authorized Access**.
2. Remove synthetic data, faults, credentials, permits, files, or delivery state created by this lab.
3. Rerun the focused regression and `make module-proof MODULE=05`.
4. Confirm the system again provides this result: Project, dataset, and run listings are stable, owner-bound, and resistant to cursor tampering.

## Completion gate

- total orders documented
- no duplicate/omission for unchanged start-eligible rows
- later inserts excluded by the high-water bound
- mutation limitation documented
- context-bound cursor
- expiry enforced
- authorization in predicate
- explicit projection
- sort allowlist
- plan evidence recorded
