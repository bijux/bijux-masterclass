# Lab 04 — Traverse a changing connection

## Purpose

Prove that connection pagination remains stable under concurrent insertion and that cursors cannot cross tenant, filter, sort, or operation boundaries.

## Prerequisites

Complete Module 3. Seed at least thirty runs with duplicate timestamps and a deterministic tie-breaker. Record tenant and status populations.

## Procedure

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

## Correctness oracle

- the original traversal is stable under insertions above its high-water;
- a fresh traversal observes the new top row;
- cursor binding rejects every population or query mismatch;
- tampering and expiry are rejected;
- duplicate timestamps do not produce duplicate or missing nodes;
- authorization filtering occurs before page construction.

## Required evidence

Create `reports/module-04-connections.json` with the two traversal identities, page ID lists, high-water values, sort tuples, rejection reasons, and source rows examined. Hash sensitive identifiers in the report if necessary.

## Interpretation questions

- Which consistency guarantee is actually provided, and which is not?
- Why is a cursor not an authorization credential?
- How would post-filtering unauthorized rows corrupt `hasNextPage`?
- What client behavior is required when a cursor expires?

## Cleanup

Remove seeded scratch rows and cursor inspection output. Rerun connection vectors in Python and TypeScript and verify that the canonical cursor bytes match.

## Completion gate

All authorized rows appear exactly once in a traversal, new-traversal behavior matches policy, all cross-boundary cursor attacks fail, and both tracks produce identical cursor decisions.
