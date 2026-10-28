# Reference Answers — Module 02: Operations, Parameters, and Messages

Read after attempting all twelve Operations, Parameters, and Messages exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Place each value: project identifier, page limit, idempotency key, project patch, session token.

Project ID belongs in the path, limit in query, idempotency key in a header, patch in request content, and a session token may be a cookie only when that authentication design is intentional.

## 2. Write the wire form for a form/explode query array named `tag` with values `a` and `b`.

`?tag=a&tag=b`. With `explode: false`, form style would commonly serialize `?tag=a,b`; the contract must choose.

## 3. Distinguish `requestBody.required` from a schema `required` list.

The first says content must be present. The second says named properties must appear in an object instance when that schema is evaluated.

## 4. Why must a 204 response omit a schema/content map?

HTTP 204 indicates no content. Describing or sending a JSON payload creates contradictory expectations and can confuse clients.

## 5. Choose between 400, 404, 409, 412, 415, and 422 for: unknown resource, stale ETag, unsupported media type, invalid field, lifecycle conflict.

Unknown resource 404; stale ETag 412; unsupported media type 415; schema/field validation 422 in this contract; lifecycle conflict 409. 400 remains for malformed requests not better classified.

## 6. What does `Content-Type` describe when a body is absent?

It has no useful representation to describe and generally should be omitted. A field alone does not create content.

## 7. Why can a default response be insufficient?

Consumers may need exact branches for retry, authentication, correction, or generated result unions. Known statuses deserve explicit schemas.

## 8. Write one invalid cursor case and expected result.

`cursor=abc` violates the digits-only grammar and should return the public 422 validation problem.

## 9. How can examples drift even when schemas remain valid?

An example can retain old semantics, status references, or resource relationships while still satisfying shape. Behavioral review complements schema validation.

## 10. What should a parity test compare for dataset creation?

Method/path, status 201, Location, content type, response fields, invalid-body status/media type, and ownership/security behavior.

## 11. Practical defect exercise

For **Optional path parameter**, a valid solution must first reproduce: a template variable is marked optional or omitted. The smallest useful starting case is: call the route without the segment and compare routing behavior. The repair is: Path parameters are always required; use a different path for a different target.

## 12. Cross-language parity exercise

The Operations, Parameters, and HTTP Messages parity scenario must be data-driven by base URL and credentials. Assert observable status, media type, stable headers, schema properties, lifecycle, or authorization—not internal classes. Validate and capture generated identifiers or timestamps instead of comparing fresh literal values.
