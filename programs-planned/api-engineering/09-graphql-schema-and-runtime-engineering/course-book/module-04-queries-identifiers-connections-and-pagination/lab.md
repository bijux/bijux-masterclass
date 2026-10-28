# Lab — Traverse a changing connection

> **Module 04:** Queries, Identifiers, Connections, and Pagination

## Objective

Prove that connection pagination remains stable under concurrent insertion and that cursors cannot cross tenant, filter, sort, or operation boundaries.

## Why this lab matters

This lab turns the module’s governing question—**How can clients navigate lists and relationships without unstable pages, leaked internals, or unbounded work?**—into a falsifiable experiment. A connection contains edges, edge cursors, and PageInfo. The course profile requires first between one and one hundred, stable total ordering, an opaque cursor, and hasNextPage. The cursor binds tenant, normalized filters, current position, and a traversal high-water boundary.

It advances the cumulative Analysis Runs Platform by requiring this result: **Implement global IDs and stable, bound connections**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

Complete Module 3. Seed at least thirty runs with duplicate timestamps and a deterministic tie-breaker. Record tenant and status populations.

## Hypothesis

The clean implementation should satisfy this claim: **the original traversal is stable under insertions above its high-water; a fresh traversal observes the new top row; cursor binding rejects every population or query mismatch; tampering and expiry are rejected; duplicate timestamps do not produce duplicate or missing nodes; authorization filtering occurs before page construction.** When the lab introduces this fault—**The declared profile must prevent duplicates and must exclude rows above the traversal high-water until a new traversal**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

### 1. Start a traversal

Request `analysisRuns(status: RUNNING, first: 10)`. Decode the cursor only with the course inspection tool, never in client code. Record:

- field coordinate;
- tenant and authorization population;
- normalized filter;
- sort tuple;
- current boundary;
- captured high-water position;
- expiry and format version.

### 2. Change the dataset

Insert a newer running run above the captured high-water position and a later older-position row below it. Continue using the original cursor until traversal ends.

The declared profile must prevent duplicates and must exclude rows above the traversal high-water until a new traversal. The exact treatment of the older-position insertion follows the stable-key and snapshot policy; record it explicitly rather than assuming database-snapshot semantics.

### 3. Begin a new traversal

Request the first page without the old cursor. Confirm that the new high-water includes the newly inserted top row.

### 4. Attack cursor binding

Attempt to reuse the cursor with:

- another tenant;
- another principal population;
- status `FAILED`;
- another root field;
- changed sort order;
- an altered payload;
- an expired timestamp.

Every mismatch must fail before a source page is returned.

### 5. Test duplicate sort values

Create several runs with the same timestamp. Traverse all pages and prove no duplicate or missing IDs. This demonstrates why the total order includes a unique tie-breaker.

### Investigation notes

Before editing code, predict the first observable divergence caused by **The declared profile must prevent duplicates and must exclude rows above the traversal high-water until a new traversal**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Prove that connection pagination remains stable under concurrent insertion and that cursors cannot cross tenant, filter, sort, or operation boundaries**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

- the original traversal is stable under insertions above its high-water;
- a fresh traversal observes the new top row;
- cursor binding rejects every population or query mismatch;
- tampering and expiry are rejected;
- duplicate timestamps do not produce duplicate or missing nodes;
- authorization filtering occurs before page construction.

## Required evidence

Create `reports/module-04-connections.json` with the two traversal identities, page ID lists, high-water values, sort tuples, rejection reasons, and source rows examined. Hash sensitive identifiers in the report if necessary.

## Interpretation and defense

1. Which state or effect is authoritative for **Queries, Identifiers, Connections, and Pagination**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **The declared profile must prevent duplicates and must exclude rows above the traversal high-water until a new traversal** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Remove seeded scratch rows and cursor inspection output. Rerun connection vectors in Python and TypeScript and verify that the canonical cursor bytes match.

## Completion gate

All authorized rows appear exactly once in a traversal, new-traversal behavior matches policy, all cross-boundary cursor attacks fail, and both tracks produce identical cursor decisions.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Queries, Identifiers, Connections, and Pagination**. A green command without the negative case and causal explanation does not satisfy this gate.
