# Exercises — Module 01: HTTP and OpenAPI Foundations

## 1. Write the complete raw request and response for creating a project named `Atlas`. Include the minimum fields that establish the contract.

## 2. Classify each method as safe and/or idempotent: GET, POST, PUT, DELETE.

## 3. Explain why an internal analytics counter does not make a GET operation unsafe.

## 4. Find the structural error when `responses` is aligned with `get` rather than nested under it.

## 5. Why can changing only `operationId` be breaking?

## 6. Give one claim a parser can prove and one it cannot.

## 7. Design a negative test for `/projects/{projectId}`.

## 8. Why is a representation not the same as a resource?

## 9. Choose a stable operation ID for retrieving one project and justify it.

## 10. What evidence would falsify the claim that project creation conforms?

## 11. Practical defect exercise

Inject **State-changing GET**.

- Expected symptom: `GET /projects/{id}/delete` appears convenient but requests deletion.
- Suggested reproducer: Send the GET twice and observe resource disappearance.

Predict the first failing command, run it, preserve the minimized evidence, repair the defect, and add a permanent regression test.

## 12. Cross-language parity exercise

Choose one HTTP and OpenAPI Foundations boundary and write a provider-neutral scenario for both implementations. Separate semantic assertions from generated values that require capture or normalization.

## Submission format

Submit Module 01 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
