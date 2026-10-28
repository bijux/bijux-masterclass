# Lab — Module 05: Queries, Stable Pagination, and Authorized Access

> **Module 05:** Queries, Stable Pagination, and Authorized Access

## Objective

Implement owner-concealed retrieval and a high-water-bounded cursor traversal that produces no duplicates or omissions among unchanged rows eligible at traversal start, excludes later inserts, rejects cursor/filter reuse, and follows verified index plans.

## Why this lab matters

This lab turns the module’s governing question—**How do filters, stable cursors, and authorization-aware queries remain correct while data changes?**—into a falsifiable experiment. The Queries, Stable Pagination, and Authorized Access increment must preserve the frozen API and every earlier durability invariant while delivering this result: Implement owner-bound, filter-bound, high-water keyset traversal and evidence-backed query plans The comparison track must expose the same public outcomes even when internal libraries and control flow differ.

It advances the cumulative Analysis Runs Platform by requiring this result: **Implement owner-bound, filter-bound, high-water keyset traversal and evidence-backed query plans**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

The previous baseline is: **One hundred concurrent identical submissions create one run; stale ETags fail atomically; replay survives restart.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How do list and retrieval operations remain stable, efficient, and non-leaking while data changes?*

## Hypothesis

The clean implementation should satisfy this claim: **A cursor issued for one principal/filter cannot be used by another, and rows inserted beyond the captured high-water mark do not enter the traversal.** When the lab introduces this fault—**Plant an offset cursor and preserve the smallest duplicate/omission reproducer before repair**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

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

### Investigation notes

Before editing code, predict the first observable divergence caused by **Plant an offset cursor and preserve the smallest duplicate/omission reproducer before repair**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Implement owner-concealed retrieval and a high-water-bounded cursor traversal that produces no duplicates or omissions among unchanged rows eligible at traversal start, excludes later inserts, rejects cursor/filter reuse, and follows verified index plans**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

A cursor issued for one principal/filter cannot be used by another, and rows inserted beyond the captured high-water mark do not enter the traversal.

## Required evidence

- baseline transcript proving the previous checkpoint before **Queries, Stable Pagination, and Authorized Access** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Queries, Stable Pagination, and Authorized Access**
- focused result for: Bind queries to principal, operation, filters, and order.
- public, durable, security, or operational observation showing: Project, dataset, and run listings are stable, owner-bound, and resistant to cursor tampering.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **stable authorized pagination**
- a limitation statement naming every live dependency required to support the strongest **Queries, Stable Pagination, and Authorized Access** claim but not exercised

## Interpretation and defense

1. Which state or effect is authoritative for **Queries, Stable Pagination, and Authorized Access**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Plant an offset cursor and preserve the smallest duplicate/omission reproducer before repair** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

1. Restore the control changed for **Queries, Stable Pagination, and Authorized Access**.
2. Remove the temporary data, faults, credentials, permits, files, or delivery state created by the **Queries, Stable Pagination, and Authorized Access** experiment.
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

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Queries, Stable Pagination, and Authorized Access**. A green command without the negative case and causal explanation does not satisfy this gate.
