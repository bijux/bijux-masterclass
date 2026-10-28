# Reference Answers — Module 09: Failure-Oriented Verification

Read after attempting all twelve Failure-Oriented Verification exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Which layer proves that `evolve()` rejects terminal transitions?

Dependency-light pure domain tests using the exhaustive state matrix.

## 2. Which layer proves `createAnalysisRun` rolls back all rows?

A real PostgreSQL integration test with injected failures and direct durable-state assertions.

## 3. Why is HTTP conformance insufficient for idempotency cardinality?

Several duplicate rows might still produce apparently identical responses. The proof must inspect logical/database counts.

## 4. What is the oracle for the ETag race?

Exactly one update succeeds with the shared validator, one fails 412, version increments once, and final body equals the winner.

## 5. How do you avoid sleep in worker recovery proof?

Observe the leased row/generation through the database or a test hook, kill at that boundary, explicitly advance/wait lease expiry, then start recovery.

## 6. What does a skipped test mean?

Only that it was not executed. It provides no positive evidence and cannot satisfy a required completion gate.

## 7. Why preserve a minimized counterexample?

It makes the root failure fast, deterministic, reviewable, and resistant to being hidden by unrelated setup.

## 8. What should a capability report contain?

Capability name, required tools/topology, executed status, versions, commands, input hashes, result/report path, and limitations.

## 9. Why separate typecheck and runtime tests?

Types prove static relationships in checked code; untrusted JSON and framework behavior still require runtime validation and execution.

## 10. What is wrong with one final end-to-end test only?

It is slow, opaque, incomplete for combinatorial policy, and cannot isolate failures; it also tempts broad mocking or weak assertions.

## 11. Trace failure-sensitive proof architecture in the primary implementation

The relevant entry points are `capstone/tests/runtime/proof_runner.py` and `capstone/tracks/typescript-fastify/test-core/domain.test.mjs`. The required invariant is that a planted defect must cause the smallest relevant oracle to fail before the repair can count as evidence.

## 12. Compare failure-sensitive proof architecture across Python and TypeScript

Both tracks must preserve this invariant: a planted defect must cause the smallest relevant oracle to fail before the repair can count as evidence. The intentional difference is that test runners differ; shared scenarios and durable observations remain provider-neutral.
