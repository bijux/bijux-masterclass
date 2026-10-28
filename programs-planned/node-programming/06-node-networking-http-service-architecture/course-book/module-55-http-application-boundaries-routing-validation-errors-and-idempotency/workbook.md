# Module 55 Workbook — Routing, Validation, Errors, and Idempotency

## 1. Predict

1. Two POST bodies differ only in JSON property order. Should a semantic idempotency fingerprint differ?
2. A same-key retry arrives while the first request is in progress. Which state must already exist?
3. A matching `If-None-Match` arrives for a current job representation. What status and body are returned?
4. An idempotency record is full and only in-progress records remain. Should one be evicted?
5. A response is lost after job creation. Is the operation committed?

## 2. Diagnose and repair

- Replace raw-path string slicing with typed route parsing.
- Replace a cast from JSON to `SubmitCommand` with exact validation.
- Separate request ID from idempotency key.
- Canonicalize semantic request fingerprinting.
- Add same-key/different-request conflict.
- Prevent eviction of in-progress records.
- Move event publication into the state transition authority.
- Implement quoted ETags and conditional GET.

## 3. Focused construction

1. Define route and problem unions.
2. Implement strict path and identifier parsing.
3. Validate job submissions from `unknown`.
4. Implement bounded idempotency records.
5. Create monotonic job revisions.
6. Generate and compare ETags.
7. Implement stable problem rendering.
8. Test response loss followed by retry.
9. Test two interleaved same-key requests.
10. Test capacity without partial commit.

## 4. Independent laboratory

Build the [Typed HTTP Router](../../labs/module-55-typed-http-router/README.md).

## 5. ServiceWire transfer

Complete the process-local application authority and connect it to the finite HTTP adapter without passing Node request/response objects into domain code.

## 6. Independent transfer

Design idempotent order submission. Explain what the fingerprint includes, when the order commits, what terminal response is replayed, how conflicts are detected, and which guarantees would require durable storage.

## 7. Closed-book defense

1. What is the semantic commit point?
2. Why must in-progress identity exist before suspension?
3. Why is raw JSON not the right fingerprint input?
4. What does an ETag identify?
5. What remains process-local in this course?

## 8. Ambiguous submission timeline

Write the full timeline for a job that commits on the server but whose 202 response is lost. Include the client’s knowledge after each event. Then show the retry path with the same key and with the same key plus a changed payload.

Your answer must identify the semantic commit point, response-observation point, conflict point, and the bounded record that permits reconciliation.

## 9. Compatibility thought experiment

A future release adds an optional `priority` field. Decide whether priority enters the idempotency fingerprint and explain the compatibility consequence of each choice. Specify how old clients, new clients, stored in-progress records, and replayed representations behave during a rolling upgrade.

## 10. Problem-contract review

Design three problem documents: malformed JSON, idempotency conflict, and overload. Keep stable code, bounded detail, request ID, and status. Decide which internal facts must not cross the boundary. Then specify how a client distinguishes a retryable overload from a permanent validation failure without parsing human prose.
