# Exercises — Module 03: JSON Schema Contract Modeling

Work through all twelve problems before opening the answers. In **JSON Schema Contract Modeling**, every response must settle this question: **How do schemas reject invalid states while remaining usable for providers, clients, and future evolution?** Do not stop at terminology. Show how the decision changes a request, durable state, consumer, operator action, or release result, and state how that consequence is tested.

## 1. List the four distinct instances for a `description` property: missing, null, empty, non-empty.

## 2. Design required-but-nullable `completedAt`.

## 3. Why does `default: normal` not guarantee the provider receives `priority`?

## 4. Create an instance that would expose overlapping local/remote source branches.

## 5. When is `additionalProperties` a schema rather than `false`?

## 6. Explain `anyOf` versus `oneOf` with set language.

## 7. Why separate `ProjectCreate` and `Project`?

## 8. Write a boundary fixture for `maxLength: 80`.

## 9. What can a generated TypeScript type fail to enforce?

## 10. How do you prove validator agreement?

## 11. Practical defect exercise

Inject **Optional confused with nullable**.

- Expected symptom: A property is omitted from `required` when the intent was required-but-nullable.
- Suggested reproducer: Compare `{}` with `{"completedAt": null}`.

Predict the first failing command, run it, preserve the minimized evidence, repair the defect, and add a permanent regression test.

## 12. Cross-language parity exercise

Choose one JSON Schema 2020-12 Contract Modeling boundary and write a provider-neutral scenario for both implementations. Separate semantic assertions from generated values that require capture or normalization.

## Submission format

Submit Module 03 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
