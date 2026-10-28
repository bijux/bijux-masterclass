# Module 54 Solutions — HTTP/1.1 Messages and Connections

## Prediction reasoning

Observed bytes enforce the application limit. A declared length can support early rejection but cannot replace counting. A `HEAD` response carries representation metadata without body bytes. After `response.end()`, local response completion may or may not have reached `'finish'`; immediate socket close can indicate premature termination. Valid JSON with the wrong media type fails the representation contract before parsing. For a known path, 405 with `Allow` is more precise when the product exposes method knowledge; 404 can be a deliberate concealment policy but should not arise accidentally.

## Repair reasoning

The bounded reader increments before retaining each chunk. On overflow, it stops normal parsing and invokes the server's rejection/connection policy. It should not keep consuming an unbounded body merely to be polite.

Layered errors might be:

```text
UNSUPPORTED_MEDIA_TYPE
BODY_REQUIRED
BODY_TOO_LARGE
MALFORMED_JSON
INVALID_REQUEST
DOMAIN_CONFLICT
```

They map to stable problem details. Internal causes remain available to logs.

For `HEAD`, compute metadata through the same application query as GET but tell the renderer not to emit body bytes. If body generation itself is expensive, expose metadata and representation generation separately.

Request IDs need exact syntax and length. Generate when absent or invalid under a documented policy. Never echo control characters or arbitrary large values.

Shutdown must stop admission, then decide whether already admitted partial bodies may finish under grace. Every active request receives one terminal observation. Connections are separate owners and may carry several requests.

## Construction notes

A content-type parser should compare media type case-insensitively and parse parameters. For JSON, permit a documented set such as `application/json` and perhaps `application/*+json`. Do not accept every string ending in “json” without a grammar.

Response serialization can fail on unsupported values or size. Serialize and bound before sending headers. Once headers are committed, error replacement options narrow.

A process-level test should connect, send partial body bytes, then close. Assert that no domain command ran and that active request accounting returns to zero.

## Laboratory evidence

The strict server should test:

- `GET` and `HEAD` parity;
- 405 and `Allow`;
- missing/unsupported media type;
- declared length above bound;
- chunked body above bound;
- malformed JSON;
- valid JSON primitive when object required;
- early client disconnect;
- response completion;
- server shutdown with an active request.

## ServiceWire transfer

The finite adapter calls an interface such as:

```ts
interface ServiceApplication {
  submit(command: SubmitCommand): Promise<SubmitResult>;
  getJob(id: JobId): JobView | undefined;
  stats(): ServiceStats;
  health(): HealthView;
}
```

It must not reach into maps or mutate jobs directly. That boundary allows HTTP/1.1 and HTTP/2 to share one domain authority later.

## Independent transfer

A binary upload route uses a fixed media type, observed byte limit, incremental checksum, and staged storage. Receiving all bytes only establishes candidate completeness. Publication or domain registration is a later commit. Cancellation removes the candidate and returns no success.

## Defense summary

HTTP parsing creates a structured message, not a trusted application command. Correct services preserve every trust transition and delay irreversible domain mutation until method, path, headers, body, syntax, and runtime semantics are valid.

## Trust-transition solution

Duplicate singleton `Content-Type` values are decisive before body decoding. The adapter rejects the ambiguous header policy and does not attempt UTF-8 or JSON parsing. Running later stages would create disagreement about which media type governed the bytes.

When observed body bytes cross the limit, the body reader terminates receipt and returns `BODY_TOO_LARGE`. If headers are not committed, a 413 problem can be sent; if the connection is no longer safe, it is destroyed. The `finally` path decrements active-request accounting regardless of whether the response completes.

A finite helper can preserve causal errors until response construction because it owns a bounded complete body. SSE commits early, so post-commit failures must close the stream or use an in-band event contract. Attempting to replace committed SSE with a JSON problem is not a principled repair.

## Header-policy solution

Singleton application headers such as idempotency key and request ID should reject ambiguous duplicates. `Content-Type` is interpreted under a strict media policy. `Content-Length` belongs primarily to the HTTP parser but conflicting framing evidence must fail. `Accept` can be list-valued. `Set-Cookie` must preserve separate values and order. `If-None-Match` follows its grammar rather than an arbitrary first-string rule. The catalogue turns header access into named protocol decisions instead of a lossy conversion helper.
