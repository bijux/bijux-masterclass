# Worked Answers — Module 09: Failure-Oriented Verification

Use these solutions to audit your reasoning for **Failure-Oriented Verification**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Which layer proves that `evolve()` rejects terminal transitions?

Dependency-light pure domain tests using the exhaustive state matrix.

The chapter’s decisive distinction is this: Each claim requires evidence at the narrowest layer that can falsify it, then selected cross-layer proofs. A good proof architecture separates contract, pure policy, database, concurrency, process, storage, network, and release failures instead of hiding them behind one green command.

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 2. Which layer proves `createAnalysisRun` rolls back all rows?

A real PostgreSQL integration test with injected failures and direct durable-state assertions.

In the cumulative capstone, the rule becomes concrete: The Failure-Oriented Verification increment must preserve the frozen API and every earlier durability invariant while delivering this result: Assemble pure, integration, concurrent, process-kill, conformance, and planted-defect proofs The comparison track must expose the same public outcomes even when internal libraries and control flow differ.

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 3. Why is HTTP conformance insufficient for idempotency cardinality?

Several duplicate rows might still produce apparently identical responses. The proof must inspect logical/database counts.

A useful way to reason about the boundary is: A concurrency test needs a logical oracle: expected row counts, unique identities, accepted/rejected outcomes, final version, or lease generation. Merely completing without exception is weak. Barriers and controlled hooks position actors near the critical section.

**Evidence.** Force competing requests against one database transaction boundary and inspect public responses, uniqueness/version rows, and rollback state after restart.

## 4. What is the oracle for the ETag race?

Exactly one update succeeds with the shared validator, one fails 412, version increments once, and final body equals the winner.

The implementation consequence is: Claim Required evidence ---: --- --- 1 claim matrix complete Write the narrow command and machine-readable oracle. 2 core proof deterministic Write the narrow command and machine-readable oracle. 3 real PostgreSQL proof Write the narrow command and machine-readable oracle. 4 barrier concurrency oracles Write the narrow command and machine-readable oracle. 5 named process kill boundaries Write the narrow command and machine-readable oracle.

## 5. How do you avoid sleep in worker recovery proof?

Observe the leased row/generation through the database or a test hook, kill at that boundary, explicitly advance/wait lease expiry, then start recovery.

The important nuance is: The process is killed at a named durable boundary, not at arbitrary sleep. Test hooks or database observation identify claim, publication, or commit state. Restart behavior is then checked from external evidence.

**Evidence.** Kill a worker after claim or partial work, expire the lease, start a replacement, and prove one final effect plus rejection of the stale generation.

## 6. What does a skipped test mean?

Only that it was not executed. It provides no positive evidence and cannot satisfy a required completion gate.

Under concurrency or failure, the distinction becomes: Proof commands distinguish passed, failed, skipped by explicit user choice, and not executed because a dependency is unavailable. Tool absence must be visible in a capability report and cannot yield a green final proof.

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 7. Why preserve a minimized counterexample?

It makes the root failure fast, deterministic, reviewable, and resistant to being hidden by unrelated setup.

The design remains honest only if: The excerpt for Failure-Oriented Verification isolates one mechanism from the full service. Before copying it, locate the decision or transaction boundary, state the assumption it makes, trace cleanup on failure, and name the regression that would expose moving the guard elsewhere.

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 8. What should a capability report contain?

Capability name, required tools/topology, executed status, versions, commands, input hashes, result/report path, and limitations.

The consumer-facing consequence is: Proof commands distinguish passed, failed, skipped by explicit user choice, and not executed because a dependency is unavailable. Tool absence must be visible in a capability report and cannot yield a green final proof.

**Counterexample.** The service passes in one process but loses the invariant after restart, concurrency, or a partial dependency failure.

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 9. Why separate typecheck and runtime tests?

Types prove static relationships in checked code; untrusted JSON and framework behavior still require runtime validation and execution.

The operational consequence is: For Failure-Oriented Verification , record the inherited API behavior, the new durable rule, one rejected alternative, the first counterexample, and the exact application, adapter, migration, or proof artifact that owns the choice.

**Counterexample.** The service passes in one process but loses the invariant after restart, concurrency, or a partial dependency failure.

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 10. What is wrong with one final end-to-end test only?

It is slow, opaque, incomplete for combinatorial policy, and cannot isolate failures; it also tempts broad mocking or weak assertions.

The strongest engineering interpretation is: Each claim requires evidence at the narrowest layer that can falsify it, then selected cross-layer proofs. A good proof architecture separates contract, pure policy, database, concurrency, process, storage, network, and release failures instead of hiding them behind one green command.

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 11. Trace failure-sensitive proof architecture in the primary implementation

The relevant entry points are `capstone/tests/runtime/proof_runner.py` and `capstone/tracks/typescript-fastify/test-core/domain.test.mjs`. The required invariant is that a planted defect must cause the smallest relevant oracle to fail before the repair can count as evidence.

The defect-oriented view is: A defect exercise predicts the first failing gate, captures the smallest counterexample, repairs the root cause, and retains a regression. The learner may not merely broaden expected behavior or delete the test.

## 12. Compare failure-sensitive proof architecture across Python and TypeScript

Both tracks must preserve this invariant: a planted defect must cause the smallest relevant oracle to fail before the repair can count as evidence. The intentional difference is that test runners differ; shared scenarios and durable observations remain provider-neutral.

Across the Python and TypeScript tracks, the invariant is: A defect exercise predicts the first failing gate, captures the smallest counterexample, repairs the root cause, and retains a regression. The learner may not merely broaden expected behavior or delete the test.
