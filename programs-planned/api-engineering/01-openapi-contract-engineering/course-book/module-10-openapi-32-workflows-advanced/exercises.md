# Exercises — Module 10: OpenAPI 3.2, Streaming, Webhooks, and Workflows

## 1. Why keep 3.1.2 and 3.2.0 artifacts?

## 2. What must “supports 3.2” specify?

## 3. When is `in: querystring` appropriate?

## 4. What does `itemSchema` not describe?

## 5. Distinguish callback, webhook, and link.

## 6. What could make a runtime expression fragile?

## 7. What must an Arazzo source description reference provide?

## 8. How do you test enhanced tag hierarchy?

## 9. What capability state applies when npm cannot be installed?

## 10. Give a safe and unsafe degradation example.

## 11. Practical defect exercise

Inject **Version bump only**.

- Expected symptom: Document says 3.2 but no new feature is understood or tested.
- Suggested reproducer: Insert malformed enhanced tag or QUERY structure.

Predict the first failing command, run it, preserve the minimized evidence, repair the defect, and add a permanent regression test.

## 12. Cross-language parity exercise

Choose one OpenAPI 3.2, Streaming, and Arazzo Workflows boundary and write a provider-neutral scenario for both implementations. Separate semantic assertions from generated values that require capture or normalization.

## Submission format

Submit Module 10 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
