# Exercises — Module 04: References and Multi-Document Architecture

Work through all twelve problems before opening the answers. In **References and Multi-Document Architecture**, every response must settle this question: **How can a multi-document contract remain understandable, relocatable, and deterministically buildable?** For every answer, separate the authoritative boundary from convenient diagnostics, then explain which failing experiment would force you to revise the design.

## 1. Resolve `../components/schemas/Project.yaml` from `spec/paths/projects.yaml`.

## 2. Decode JSON Pointer `/components/schemas/A~1B~0C`.

## 3. When should a one-use schema stay inline?

## 4. Distinguish bundle and dereference.

## 5. Why can a recursive schema be valid while a generator fails?

## 6. Design a relocation test.

## 7. What is the risk of `$id` in a nested schema?

## 8. How do you prove bundling preserved meaning?

## 9. Why is editing a bundle forbidden?

## 10. Name one intentional and one accidental cycle.

## 11. Practical defect exercise

Inject **Working-directory reference**.

- Expected symptom: Resolver joins relative paths to `cwd`.
- Suggested reproducer: Run the same command from another directory.

Predict the first failing command, run it, preserve the minimized evidence, repair the defect, and add a permanent regression test.

## 12. Cross-language parity exercise

Choose one References and Multi-Document Architecture boundary and write a provider-neutral scenario for both implementations. Separate semantic assertions from generated values that require capture or normalization.

## Submission format

Submit Module 04 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
