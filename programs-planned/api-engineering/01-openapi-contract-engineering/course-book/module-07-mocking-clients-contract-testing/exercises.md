# Exercises — Module 07: Mocks, Clients, and Contract Testing

Work through all twelve problems before opening the answers. In **Mocks, Clients, and Contract Testing**, every response must settle this question: **How do mocks, generated clients, examples, property tests, and stateful tests provide different evidence?** Each solution must survive delay, duplication, version skew, hostile input, or partial failure where relevant; happy-path intuition alone earns no credit.

## 1. What does a successful bundle prove?

## 2. When should a custom lint rule block CI?

## 3. Why retain examples when property generation exists?

## 4. What should happen when a generator omits callbacks?

## 5. How do you test that rejection caused no mutation?

## 6. What data belongs in a minimized failure report?

## 7. Why can a schema mock generate an impossible domain state?

## 8. Design one stateful invariant for cancellation.

## 9. What is the client risk of renaming an operationId?

## 10. Distinguish supported, transformed, and partially supported.

## 11. Practical defect exercise

Inject **Lint equals correctness**.

- Expected symptom: A perfectly styled contract is assumed to match runtime.
- Suggested reproducer: Change provider status while lint remains green.

Predict the first failing command, run it, preserve the minimized evidence, repair the defect, and add a permanent regression test.

## 12. Cross-language parity exercise

Choose one Linting, Mocking, Clients, and Contract Testing boundary and write a provider-neutral scenario for both implementations. Separate semantic assertions from generated values that require capture or normalization.

## Submission format

Submit Module 07 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
