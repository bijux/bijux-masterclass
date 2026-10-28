# Worked Answers — Module 05: Production HTTP API Design

Use these solutions to audit your reasoning for **Production HTTP API Design**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why is 202 different from 201?

201 says a resource was created as the result and normally identifies it; 202 says processing is accepted but incomplete. The capstone may create a run resource while its analysis remains incomplete, so 202 communicates the operation state.

The chapter’s decisive distinction is this: 202 Accepted says the request was accepted for processing but processing is not complete. A useful response identifies how the client can observe status—here, a run resource in Location plus a current run representation and Retry-After guidance.

## 2. Specify idempotency behavior for same key/same body and same key/different body.

Same principal/key/body returns the same run with replay evidence. Same principal/key/different body returns 409 and creates nothing.

In the cumulative capstone, the rule becomes concrete: POST can be made safely retryable through an application-level idempotency key. The server scopes the key to a principal, binds it to a canonical request-body fingerprint, stores the logical result, and replays it for the same request. A changed body under the key is a conflict.

## 3. Why scope idempotency keys by principal?

Unrelated clients may choose the same key. Global scope would leak or collide across tenants.

A useful way to reason about the boundary is: The common fields—type, title, status, detail, instance—give generic clients a stable structure. The API still chooses stable problem type identifiers and defines when to use 404, 409, 412, 413, 415, 422, or 428. Validation extends the shape with structured issues.

**Evidence.** Resolve the effective security requirement per operation and run missing, invalid, insufficient, foreign-owner, and successful credential scenarios against both providers.

## 4. What does an ETag mean to a client?

An opaque validator for a selected representation. The client must return it unchanged, not parse the encoded training version.

The implementation consequence is: An entity tag identifies a selected representation version. The client sends If-Match with the tag it observed. If the current tag differs, the server returns 412 Precondition Failed rather than overwriting another update. If the contract requires a precondition and none is supplied, 428 Precondition Required makes that policy explicit.

## 5. Distinguish 409 and 412 in this API.

409 is a domain/request conflict such as invalid state or idempotency mismatch. 412 means a supplied HTTP precondition evaluated false.

The important nuance is: Queued and running runs can be canceled; completed, failed, and canceled runs are terminal. Artifacts are unavailable before completion. These rules determine legal responses and conflict branches, so they belong in the contract narrative, examples, and tests—not only the store implementation.

**Evidence.** Capture the raw HTTP exchange and compare its method, parameters, media type, status, headers, and schema with the resolved operation contract and both providers.

## 6. Why use 428?

It states that this server requires a precondition, rather than treating a missing If-Match as an arbitrary validation field.

Under concurrency or failure, the distinction becomes: A client might retry transient server failures, honor Retry-After, correct validation input, refresh authentication, or abandon a conflict. The status code alone is not a universal retry algorithm, but careless status selection removes useful signals.

**Evidence.** Capture the raw HTTP exchange and compare its method, parameters, media type, status, headers, and schema with the resolved operation contract and both providers.

## 7. Design a cursor-page boundary test.

Create more items than the limit, request a bounded page, follow nextCursor, assert no duplicates/omissions, and assert null at the end.

The design remains honest only if: Offset pagination is easy to understand but unstable under insertions and deletions. Cursor pagination can encode a stable continuation position but makes random access harder. The capstone uses a simple numeric cursor for deterministic teaching and bounds page size to 50.

**Evidence.** Capture the raw HTTP exchange and compare its method, parameters, media type, status, headers, and schema with the resolved operation contract and both providers.

## 8. Can a client blindly retry every 5xx?

No. Method/idempotency, whether the server may have committed, retry limits, and server guidance matter. An idempotency key can make POST recovery safer.

The consumer-facing consequence is: POST can be made safely retryable through an application-level idempotency key. The server scopes the key to a principal, binds it to a canonical request-body fingerprint, stores the logical result, and replays it for the same request. A changed body under the key is a conflict.

## 9. Why is an empty artifact page misleading before completion?

It conflates “no artifacts will exist” with “artifacts are not available yet.” A conflict communicates lifecycle state.

The operational consequence is: Returning 202 and then losing the job is still possible; HTTP does not guarantee execution. The contract must describe observable lifecycle states and failures. The deterministic training provider advances on polling so protocol behavior is testable without a queue.

**Evidence.** Capture the raw HTTP exchange and compare its method, parameters, media type, status, headers, and schema with the resolved operation contract and both providers.

## 10. What fields should never be the machine discriminator of a problem?

Human title/detail text and stack traces. Use status, stable type URI, and documented extension codes.

The strongest engineering interpretation is: The common fields—type, title, status, detail, instance—give generic clients a stable structure. The API still chooses stable problem type identifiers and defines when to use 404, 409, 412, 413, 415, 422, or 428. Validation extends the shape with structured issues.

**Evidence.** Capture the raw HTTP exchange and compare its method, parameters, media type, status, headers, and schema with the resolved operation contract and both providers.

## 11. Practical defect exercise

For **202 without monitor**, a valid solution must first reproduce: the response says accepted but provides no status URI or current representation. The smallest useful starting case is: disconnect after the response and determine how the client can continue. The repair is: return a `Location` header or link and model a status resource.

The defect-oriented view is: 202 Accepted says the request was accepted for processing but processing is not complete. A useful response identifies how the client can observe status—here, a run resource in Location plus a current run representation and Retry-After guidance.

## 12. Cross-language parity exercise

The Production HTTP API Design parity scenario must be data-driven by base URL and credentials. Assert observable status, media type, stable headers, schema properties, lifecycle, or authorization—not internal classes. Validate and capture generated identifiers or timestamps instead of comparing fresh literal values.

Across the Python and TypeScript tracks, the invariant is: This Production HTTP API Design increment is a vertical slice: contract source, provider behavior, consumer impact, tests, and evidence move together. A large YAML diff with no executable observation is not progress.
