# Exercises — Module 08: Security in the Public Contract

Work through all twelve problems before opening the answers. In **Security in the Public Contract**, every response must settle this question: **What can the public contract say about authentication and authorization, and what remains a runtime responsibility?** Use the cumulative platform, not an invented toy system. Preserve inherited guarantees and make every new assumption explicit and falsifiable.

## 1. Translate `security: [{ bearerAuth: [], mtls: [] }, { apiKeyAuth: [] }]`.

## 2. What does `security: []` mean on an operation?

## 3. Why is an OAuth2 scheme not an OAuth server?

## 4. When is 404 preferable to 403?

## 5. Why must scope and owner tests be separate?

## 6. Design a minimum-scope test for `createAnalysisRun`.

## 7. Why is `format: uri` insufficient for webhook safety?

## 8. What should a 401 bearer response normally include?

## 9. How does `additionalProperties: false` help security?

## 10. Name evidence that the contract and runtime security agree.

## 11. Practical defect exercise

Inject **Declaration without enforcement**.

- Expected symptom: Docs show a scope but runtime ignores it.
- Suggested reproducer: Call write operation with read-only token.

Predict the first failing command, run it, preserve the minimized evidence, repair the defect, and add a permanent regression test.

## 12. Cross-language parity exercise

Choose one Security Contracts and Runtime Enforcement boundary and write a provider-neutral scenario for both implementations. Separate semantic assertions from generated values that require capture or normalization.

## Submission format

Submit Module 08 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
