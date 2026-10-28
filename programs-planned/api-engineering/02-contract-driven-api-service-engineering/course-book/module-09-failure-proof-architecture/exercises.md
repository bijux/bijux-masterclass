# Exercises — Module 09: Failure-Oriented Verification

Work through all twelve problems before opening the answers. In **Failure-Oriented Verification**, every response must settle this question: **How do tests prove transactions, concurrency, restart, storage, and delivery guarantees rather than only happy paths?** The strongest answer distinguishes specification, implementation, and operational evidence, then demonstrates where a plausible shortcut would fail.

## 1. Which layer proves that `evolve()` rejects terminal transitions?

## 2. Which layer proves `createAnalysisRun` rolls back all rows?

## 3. Why is HTTP conformance insufficient for idempotency cardinality?

## 4. What is the oracle for the ETag race?

## 5. How do you avoid sleep in worker recovery proof?

## 6. What does a skipped test mean?

## 7. Why preserve a minimized counterexample?

## 8. What should a capability report contain?

## 9. Why separate typecheck and runtime tests?

## 10. What is wrong with one final end-to-end test only?

## 11. Trace failure-sensitive proof architecture in the primary implementation

Read `capstone/tests/runtime/proof_runner.py` or `capstone/tracks/typescript-fastify/test-core/domain.test.mjs` in your primary track. Trace one accepted input and one rejected or failed input from the public/application boundary to the authoritative result. Name the focused regression that would fail if the central guard were removed.

## 12. Compare failure-sensitive proof architecture across Python and TypeScript

Compare `capstone/tests/runtime/proof_runner.py` with `capstone/tracks/typescript-fastify/test-core/domain.test.mjs`. Identify the shared invariant, one deliberate language or library difference, and one source-shape difference that must not become a parity requirement.

## Submission format

Submit Module 09 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
