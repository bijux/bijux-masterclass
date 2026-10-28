# Exercises — Module 06: Contract-First and Code-First Runtimes

## 1. When is code-first a defensible choice?

## 2. Why not require text-identical generated documents?

## 3. Name four semantic differences that may never be broadly allowlisted.

## 4. What does response serialization prove that request validation does not?

## 5. Why is an imported TestClient insufficient as the only parity proof?

## 6. How should nondeterministic identifiers be compared?

## 7. What is the risk of exposing framework validation paths?

## 8. Design a handler-map negative test.

## 9. Why are TypeScript static types not a boundary validator?

## 10. What belongs in a drift report?

## 11. Practical defect exercise

Inject **Generated document promoted to canonical**.

- Expected symptom: One provider’s annotations silently redefine the API.
- Suggested reproducer: Change a FastAPI default and observe the published diff.

Predict the first failing command, run it, preserve the minimized evidence, repair the defect, and add a permanent regression test.

## 12. Cross-language parity exercise

Choose one Contract-First and Code-First Runtimes boundary and write a provider-neutral scenario for both implementations. Separate semantic assertions from generated values that require capture or normalization.

## Submission format

Submit Module 06 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
