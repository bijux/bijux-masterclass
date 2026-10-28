# Lab — Lose a mutation response safely

> **Module 05:** Mutations, Idempotency, Concurrency, and Domain Results

## Objective

Prove that graph mutations preserve source-service idempotency, optimistic concurrency, and typed domain outcomes when responses are lost or commands race.

## Why this lab matters

This lab turns the module’s governing question—**How do graph mutations preserve the durable command guarantees of the owning service?**—into a falsifiable experiment. clientMutationId is an echo for client correlation. It is not the idempotency key. An idempotency key is bound to authenticated principal, operation, and normalized semantic input at the source service. Reusing a key with different input is a conflict. Generating a new key in the graph gateway on each attempt destroys retry safety.

It advances the cumulative Analysis Runs Platform by requiring this result: **Expose idempotent create/start/cancel mutations over owning services**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

Complete Module 4. Reset the in-memory or test service state and call logs. Use a stable principal, tenant, dataset, and client-selected idempotency key.

## Hypothesis

The clean implementation should satisfy this claim: **one key and one semantic input create one logical run; lost response does not lose committed authority; exact retry returns the original outcome; changed input under a key conflicts; stale version and illegal state are distinct outcomes; the gateway owns no replay table or business transaction; top-level serial execution does not imply rollback.** When the lab introduces this fault—**Allow Analysis Control to commit, but discard the graph response before the client observes it**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

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

### Investigation notes

Before editing code, predict the first observable divergence caused by **Allow Analysis Control to commit, but discard the graph response before the client observes it**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Prove that graph mutations preserve source-service idempotency, optimistic concurrency, and typed domain outcomes when responses are lost or commands race**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

- one key and one semantic input create one logical run;
- lost response does not lose committed authority;
- exact retry returns the original outcome;
- changed input under a key conflicts;
- stale version and illegal state are distinct outcomes;
- the gateway owns no replay table or business transaction;
- top-level serial execution does not imply rollback.

## Required evidence

Create `reports/module-05-mutations.json` with hashed command key, semantic input digest, source-call outcome, run identity, replay flag, version transitions, result union member, and gateway persistence inspection. Do not store the raw key.

## Interpretation and defense

1. Which state or effect is authoritative for **Mutations, Idempotency, Concurrency, and Domain Results**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Allow Analysis Control to commit, but discard the graph response before the client observes it** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Remove scratch mutation documents and reset state. Re-run mutation and release proofs. Confirm the graph gateway database contains only graph metadata tables.

## Completion gate

The retry creates no duplicate, changed input conflicts, stale cancellation is atomic, sibling mutation behavior is explained correctly, and both tracks return the same result discriminants.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Mutations, Idempotency, Concurrency, and Domain Results**. A green command without the negative case and causal explanation does not satisfy this gate.
