# Reference Answers — Module 05: Production HTTP API Design

Read after attempting all twelve Production HTTP API Design exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Why is 202 different from 201?

201 says a resource was created as the result and normally identifies it; 202 says processing is accepted but incomplete. The capstone may create a run resource while its analysis remains incomplete, so 202 communicates the operation state.

## 2. Specify idempotency behavior for same key/same body and same key/different body.

Same principal/key/body returns the same run with replay evidence. Same principal/key/different body returns 409 and creates nothing.

## 3. Why scope idempotency keys by principal?

Unrelated clients may choose the same key. Global scope would leak or collide across tenants.

## 4. What does an ETag mean to a client?

An opaque validator for a selected representation. The client must return it unchanged, not parse the encoded training version.

## 5. Distinguish 409 and 412 in this API.

409 is a domain/request conflict such as invalid state or idempotency mismatch. 412 means a supplied HTTP precondition evaluated false.

## 6. Why use 428?

It states that this server requires a precondition, rather than treating a missing If-Match as an arbitrary validation field.

## 7. Design a cursor-page boundary test.

Create more items than the limit, request a bounded page, follow nextCursor, assert no duplicates/omissions, and assert null at the end.

## 8. Can a client blindly retry every 5xx?

No. Method/idempotency, whether the server may have committed, retry limits, and server guidance matter. An idempotency key can make POST recovery safer.

## 9. Why is an empty artifact page misleading before completion?

It conflates “no artifacts will exist” with “artifacts are not available yet.” A conflict communicates lifecycle state.

## 10. What fields should never be the machine discriminator of a problem?

Human title/detail text and stack traces. Use status, stable type URI, and documented extension codes.

## 11. Practical defect exercise

For **202 without monitor**, a valid solution must first reproduce: the response says accepted but provides no status URI or current representation. The smallest useful starting case is: disconnect after the response and determine how the client can continue. The repair is: return a `Location` header or link and model a status resource.

## 12. Cross-language parity exercise

The Production HTTP API Design parity scenario must be data-driven by base URL and credentials. Assert observable status, media type, stable headers, schema properties, lifecycle, or authorization—not internal classes. Validate and capture generated identifiers or timestamps instead of comparing fresh literal values.
