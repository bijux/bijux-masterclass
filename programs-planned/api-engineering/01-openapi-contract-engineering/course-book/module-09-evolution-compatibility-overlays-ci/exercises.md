# Exercises — Module 09: Evolution, Compatibility, and Audience Views

## 1. Why can adding a response enum value be breaking?

## 2. Is removing a maximum from a request string compatible?

## 3. Is adding a required response property breaking?

## 4. Why is changing operationId risky without wire change?

## 5. What belongs in a deprecation record?

## 6. Why archive a bundle rather than only modular source?

## 7. What must an Overlay output test assert?

## 8. Design a breaking-gate self-test.

## 9. When may a suppression be defensible?

## 10. Why is semantic versioning alone insufficient?

## 11. Practical defect exercise

Inject **All additions called safe**.

- Expected symptom: New enum/status/field breaks a strict consumer.
- Suggested reproducer: Regenerate or run an exhaustive consumer fixture.

Predict the first failing command, run it, preserve the minimized evidence, repair the defect, and add a permanent regression test.

## 12. Cross-language parity exercise

Choose one Compatibility, Releases, Overlay, and CI boundary and write a provider-neutral scenario for both implementations. Separate semantic assertions from generated values that require capture or normalization.

## Submission format

Submit Module 09 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
