# Lab 05 — Lose a mutation response safely

## Purpose

Prove that graph mutations preserve source-service idempotency, optimistic concurrency, and typed domain outcomes when responses are lost or commands race.

## Prerequisites

Complete Module 4. Reset the in-memory or test service state and call logs. Use a stable principal, tenant, dataset, and client-selected idempotency key.

## Procedure

### 1. Commit and discard the response

Execute `StartAnalysis`. Allow Analysis Control to commit, but discard the graph response before the client observes it. Confirm that the source owns a run and replay record even though the client has no response.

### 2. Retry the exact command

Repeat the same persisted mutation with the same principal, key, and semantic input. The graph forwards them unchanged. Expect the same run, one logical creation, and `replayed: true`.

### 3. Reuse the key incorrectly

Change `algorithm` or dataset while keeping the key. Expect a typed `MutationProblem` with `CONFLICT`. No second run may appear.

### 4. Test optimistic cancellation

Read the run version, advance the run through another action, then call `CancelAnalysis` with the stale version. Expect `PRECONDITION_FAILED`. Repeat with the current version in a legal state and expect success. Repeat after a terminal state and expect `CONFLICT`.

### 5. Demonstrate non-transactional sibling mutations

In a scratch document, execute two top-level mutations where the first succeeds and the second returns a domain problem. Record that the first effect remains. Explain whether the correct product design is two commands, one owner-local atomic command, or an asynchronous workflow.

## Correctness oracle

- one key and one semantic input create one logical run;
- lost response does not lose committed authority;
- exact retry returns the original outcome;
- changed input under a key conflicts;
- stale version and illegal state are distinct outcomes;
- the gateway owns no replay table or business transaction;
- top-level serial execution does not imply rollback.

## Required evidence

Create `reports/module-05-mutations.json` with hashed command key, semantic input digest, source-call outcome, run identity, replay flag, version transitions, result union member, and gateway persistence inspection. Do not store the raw key.

## Interpretation questions

- Which network failures make a retry reasonable?
- Why is `clientMutationId` not the idempotency authority?
- When should a conflict be data rather than a GraphQL execution error?
- Which service must repeat authorization inside the transaction?

## Cleanup

Remove scratch mutation documents and reset state. Re-run mutation and release proofs. Confirm the graph gateway database contains only graph metadata tables.

## Completion gate

The retry creates no duplicate, changed input conflicts, stale cancellation is atomic, sibling mutation behavior is explained correctly, and both tracks return the same result discriminants.
