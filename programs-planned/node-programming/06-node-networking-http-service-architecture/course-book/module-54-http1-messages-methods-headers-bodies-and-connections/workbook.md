# Module 54 Workbook — HTTP/1.1 Messages and Connections

## 1. Predict

1. A request declares `Content-Length: 10` but sends 20 bytes. Which count enforces the product limit?
2. A `HEAD` request targets a valid GET route. Should the server generate and send the representation body?
3. `response.end()` returns and the socket closes immediately. Which facts are known?
4. A client sends valid JSON with `text/plain`. Which validation layer rejects it?
5. A known route receives an unsupported method. Compare 404 and 405 behavior.

## 2. Diagnose and repair

- Replace whole-body unbounded collection with incremental counting.
- Separate media-type, JSON syntax, schema, and domain errors.
- Correct a `HEAD` implementation that sends bytes.
- Add bounded request IDs.
- Prevent stack traces and raw authorization values from entering problem details.
- Track active requests separately from accepted connections.
- Define what happens when shutdown starts after headers but before body completion.

## 3. Focused construction

1. Parse and validate media types.
2. Implement bounded body reading.
3. Render stable problem details.
4. Implement finite JSON responses and correct `HEAD`.
5. Add 405 plus `Allow`.
6. Set and echo a request ID.
7. Test slow/partial body cancellation.
8. Test early connection close before response finish.

## 4. Independent laboratory

Build the [Strict HTTP Message Server](../../labs/module-54-strict-http-message-server/README.md).

## 5. ServiceWire transfer

Add finite endpoints for health, stats, job submission, and job lookup, but keep domain logic behind a typed application interface.

## 6. Independent transfer

Design a binary-upload endpoint. State method, media type, maximum bytes, checksum policy, cancellation behavior, response statuses, and the distinction between receiving all bytes and committing the upload.

## 7. Closed-book defense

1. Which HTTP work does Node perform?
2. Which application work remains?
3. Why is `Content-Length` not the sole body-limit authority?
4. What does response `'finish'` prove?
5. Why are request IDs and idempotency keys separate?

## 8. Request trust-transition worksheet

Trace a `POST /v1/jobs` request containing duplicate `Content-Type` values, a valid `Content-Length`, malformed UTF-8, and an otherwise plausible JSON prefix. Decide the earliest decisive failure and justify why later parsing stages must not run.

Repeat with a request whose body exceeds the configured limit one chunk before EOF. Record which resource is destroyed, whether a response can still be sent, and how active-request accounting reaches zero.

## 9. Response commitment exercise

Design a finite-response helper that constructs status, headers, content length, and body before committing. Then contrast it with an SSE response that commits immediately and remains open. List the errors each model can still represent after headers are sent.

## 10. Header-policy catalogue

Create a table for `Content-Type`, `Content-Length`, `Idempotency-Key`, `If-None-Match`, `Accept`, `Set-Cookie`, and `X-Request-ID`. For each, specify whether multiple values are allowed, whether order matters, how the application obtains one value, and what malformed cardinality produces. This exercise should make clear why one generic `getHeaderString()` helper is not a complete protocol policy.
