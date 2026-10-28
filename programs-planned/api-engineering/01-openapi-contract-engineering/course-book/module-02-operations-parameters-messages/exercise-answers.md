# Worked Answers — Module 02: Operations, Parameters, and Messages

Use these solutions to audit your reasoning for **Operations, Parameters, and Messages**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Place each value: project identifier, page limit, idempotency key, project patch, session token.

Project ID belongs in the path, limit in query, idempotency key in a header, patch in request content, and a session token may be a cookie only when that authentication design is intentional.

The chapter’s decisive distinction is this: Parameter Objects cover path, query, header, and cookie locations. Structured message content belongs under requestBody, with a content map keyed by media type. requestBody.required controls whether content must exist; schema required controls which object properties must exist once an object is present.

## 2. Write the wire form for a form/explode query array named `tag` with values `a` and `b`.

`?tag=a&tag=b`. With `explode: false`, form style would commonly serialize `?tag=a,b`; the contract must choose.

In the cumulative capstone, the rule becomes concrete: A response is not only a JSON schema. 201 communicates creation, 204 forbids message content, 404 communicates target absence, and 415 says the submitted content format is unsupported. Location, ETag, and request-correlation fields can be required consumer inputs.

**Evidence.** Capture the raw HTTP exchange and compare its method, parameters, media type, status, headers, and schema with the resolved operation contract and both providers.

## 3. Distinguish `requestBody.required` from a schema `required` list.

The first says content must be present. The second says named properties must appear in an object instance when that schema is evaluated.

A useful way to reason about the boundary is: Content-Type describes content that is present. Accept expresses response preferences. A provider can reject unsupported request content with 415, and can choose or reject a response representation based on Accept. OpenAPI content maps enumerate supported media types; they do not by themselves implement negotiation.

## 4. Why must a 204 response omit a schema/content map?

HTTP 204 indicates no content. Describing or sending a JSON payload creates contradictory expectations and can confuse clients.

The implementation consequence is: For Operations, Parameters, and HTTP Messages, requirements may come from OpenAPI, JSON Schema, HTTP semantics, an observed tool boundary, or the capstone architecture. Keep those sources separate: do not present a local preference as an OpenAPI MUST or soften a normative rule into style.

**Evidence.** Add valid and invalid instances to the shared schema fixture corpus and verify independent schema validation plus request and response behavior in both providers.

## 5. Choose between 400, 404, 409, 412, 415, and 422 for: unknown resource, stale ETag, unsupported media type, invalid field, lifecycle conflict.

Unknown resource 404; stale ETag 412; unsupported media type 415; schema/field validation 422 in this contract; lifecycle conflict 409. 400 remains for malformed requests not better classified.

The important nuance is: An example attached to a media type or schema is part of the published understanding of the operation. It must satisfy required fields, patterns, formats, union selection, and closure rules. A beautifully rendered invalid example trains consumers to send requests the schema rejects.

## 6. What does `Content-Type` describe when a body is absent?

It has no useful representation to describe and generally should be omitted. A field alone does not create content.

Under concurrency or failure, the distinction becomes: Choose location from semantics before choosing framework syntax. A filter does not become a path segment because a router makes it easy. A concurrency precondition does not belong in the JSON patch because intermediaries and generic HTTP tooling understand the field-line semantics.

**Evidence.** Capture the raw HTTP exchange and compare its method, parameters, media type, status, headers, and schema with the resolved operation contract and both providers.

## 7. Why can a default response be insufficient?

Consumers may need exact branches for retry, authentication, correction, or generated result unions. Known statuses deserve explicit schemas.

The design remains honest only if: Always pair a parameter schema with at least one literal URI or field-line example. For cursor pagination, cursor=20 is simple. For arrays or objects, write the exact encoding and test the provider parser against it.

**Evidence.** Capture the raw HTTP exchange and compare its method, parameters, media type, status, headers, and schema with the resolved operation contract and both providers.

## 8. Write one invalid cursor case and expected result.

`cursor=abc` violates the digits-only grammar and should return the public 422 validation problem.

The consumer-facing consequence is: An OpenAPI Parameter Object describes more than a schema. style, explode, and allowReserved determine how arrays and objects become characters in a path, query string, header, or cookie. Two clients can agree that a value is string[] and still send incompatible wire forms.

**Evidence.** Capture the raw HTTP exchange and compare its method, parameters, media type, status, headers, and schema with the resolved operation contract and both providers.

## 9. How can examples drift even when schemas remain valid?

An example can retain old semantics, status references, or resource relationships while still satisfying shape. Behavioral review complements schema validation.

The operational consequence is: For every Operations, Parameters, and HTTP Messages claim above, add one citation in personal notes and one counterexample. Mark the cheapest route that can falsify it—parse, examples, provider tests, live conformance, compatibility diff, or manual review—and combine routes where the claim crosses layers.

**Evidence.** Add valid and invalid instances to the shared schema fixture corpus and verify independent schema validation plus request and response behavior in both providers.

## 10. What should a parity test compare for dataset creation?

Method/path, status 201, Location, content type, response fields, invalid-body status/media type, and ownership/security behavior.

The strongest engineering interpretation is: A response is not only a JSON schema. 201 communicates creation, 204 forbids message content, 404 communicates target absence, and 415 says the submitted content format is unsupported. Location, ETag, and request-correlation fields can be required consumer inputs.

**Evidence.** Capture the raw HTTP exchange and compare its method, parameters, media type, status, headers, and schema with the resolved operation contract and both providers.

## 11. Practical defect exercise

For **Optional path parameter**, a valid solution must first reproduce: a template variable is marked optional or omitted. The smallest useful starting case is: call the route without the segment and compare routing behavior. The repair is: Path parameters are always required; use a different path for a different target.

The defect-oriented view is: For Operations, Parameters, and HTTP Messages, correct-looking YAML and green happy paths remain weak evidence. Start from falsification: every listed defect has an observable symptom, a minimal reproducer, and a bounded repair.

## 12. Cross-language parity exercise

The Operations, Parameters, and HTTP Messages parity scenario must be data-driven by base URL and credentials. Assert observable status, media type, stable headers, schema properties, lifecycle, or authorization—not internal classes. Validate and capture generated identifiers or timestamps instead of comparing fresh literal values.

Across the Python and TypeScript tracks, the invariant is: This Operations, Parameters, and HTTP Messages increment is a vertical slice: contract source, provider behavior, consumer impact, tests, and evidence move together. A large YAML diff with no executable observation is not progress.
