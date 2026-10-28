# Exercises — Module 02: Operations, Parameters, and Messages

Work through all twelve problems before opening the answers. In **Operations, Parameters, and Messages**, every response must settle this question: **How are parameters, request bodies, media types, status codes, and headers modeled without ambiguity?** Treat each problem as a design review: state the rule, construct the smallest counterexample, and select an oracle capable of rejecting your own answer.

## 1. Place each value: project identifier, page limit, idempotency key, project patch, session token.

## 2. Write the wire form for a form/explode query array named `tag` with values `a` and `b`.

## 3. Distinguish `requestBody.required` from a schema `required` list.

## 4. Why must a 204 response omit a schema/content map?

## 5. Choose between 400, 404, 409, 412, 415, and 422 for: unknown resource, stale ETag, unsupported media type, invalid field, lifecycle conflict.

## 6. What does `Content-Type` describe when a body is absent?

## 7. Why can a default response be insufficient?

## 8. Write one invalid cursor case and expected result.

## 9. How can examples drift even when schemas remain valid?

## 10. What should a parity test compare for dataset creation?

## 11. Practical defect exercise

Inject **Optional path parameter**.

- Expected symptom: A template variable is marked optional or omitted.
- Suggested reproducer: Call the route without the segment and compare routing behavior.

Predict the first failing command, run it, preserve the minimized evidence, repair the defect, and add a permanent regression test.

## 12. Cross-language parity exercise

Choose one Operations, Parameters, and HTTP Messages boundary and write a provider-neutral scenario for both implementations. Separate semantic assertions from generated values that require capture or normalization.

## Submission format

Submit Module 02 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
