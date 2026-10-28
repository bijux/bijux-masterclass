# Exercises — Module 05: Production HTTP API Design

Work through all twelve problems before opening the answers. In **Production HTTP API Design**, every response must settle this question: **How should an HTTP API express asynchronous work, retries, conflicts, conditional updates, and machine-readable failures?** A useful solution connects semantics to mechanism: who owns the decision, what can go wrong, and which retained artifact proves the claimed outcome.

## 1. Why is 202 different from 201?

## 2. Specify idempotency behavior for same key/same body and same key/different body.

## 3. Why scope idempotency keys by principal?

## 4. What does an ETag mean to a client?

## 5. Distinguish 409 and 412 in this API.

## 6. Why use 428?

## 7. Design a cursor-page boundary test.

## 8. Can a client blindly retry every 5xx?

## 9. Why is an empty artifact page misleading before completion?

## 10. What fields should never be the machine discriminator of a problem?

## 11. Practical defect exercise

Inject **202 without monitor**.

- Expected symptom: Response says accepted but gives no status URI or representation.
- Suggested reproducer: Disconnect after the response and ask how a client continues.

Predict the first failing command, run it, preserve the minimized evidence, repair the defect, and add a permanent regression test.

## 12. Cross-language parity exercise

Choose one Production HTTP API Design boundary and write a provider-neutral scenario for both implementations. Separate semantic assertions from generated values that require capture or normalization.

## Submission format

Submit Module 05 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
