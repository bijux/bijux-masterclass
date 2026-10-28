# Module 54 — HTTP/1.1: Messages, Methods, Headers, Bodies, and Connections

**Progress: 54/100**

## The governing question

> How do you turn Node's low-level HTTP request and response objects into a strict application message boundary without confusing transport completion, HTTP syntax, method semantics, body framing, and domain validation?

## Why this module comes now

Modules 51–53 separated service identity, transport framing, and correlation. HTTP adds a standardized request/response protocol above transport. Node's HTTP implementation parses message syntax and framing, but it intentionally remains low-level. It does not validate your media type, route grammar, JSON shape, idempotency policy, or domain state.

This module establishes the finite HTTP boundary. The next module adds typed routing and application semantics. Keeping those steps separate matters: the server adapter should own HTTP mechanics, while the application owns job semantics.

## Observable outcomes

By the end of the module, you can:

- identify request method, target, version, headers, raw header evidence, and body as separate inputs;
- define supported methods and precise `HEAD` behavior;
- enforce request-body limits incrementally;
- distinguish message syntax, media-type, JSON syntax, schema, and domain failures;
- understand response status, headers, body, completion callback, and connection close as separate facts;
- configure request, headers, keep-alive, and connection limits deliberately;
- prevent request smuggling assumptions from leaking into application code;
- track active requests and connections through graceful shutdown.

## The HTTP message ledger

| Surface | Authority |
|---|---|
| request line | Node HTTP parser |
| normalized headers | Node's header object |
| raw header pairs | `rawHeaders` evidence |
| body chunks | request readable stream |
| body limit | application adapter |
| media-type policy | application protocol |
| JSON syntax | JSON parser |
| runtime shape | validator |
| route semantics | router/application |
| response status and headers | adapter from application result |
| response body | application representation |
| response completion | response owner |
| connection reuse | HTTP server/client policy |

## Node's HTTP layer is intentionally low-level

Node parses HTTP messages and exposes streams. It does not buffer complete bodies automatically, and it does not interpret application content. This is a strength: the service can enforce its own bounds and stream policies. It also means “I received an `IncomingMessage`” is only the beginning of validation.

A request can be divided conceptually:

```text
transport accepted
    ↓
HTTP headers parsed
    ↓
route and method recognized
    ↓
body admitted and bounded
    ↓
media type accepted
    ↓
body syntax parsed
    ↓
runtime schema validated
    ↓
domain command committed
```

Each transition can fail independently.

## Methods are protocol semantics, not route decorations

A route table should decide which methods are legal. Returning the same generic 404 for every wrong method hides useful protocol information. Depending on product policy, a known path with an unsupported method can return 405 and an `Allow` header.

`HEAD` is not “GET but ignore whatever happens.” The response should carry the same representation metadata a corresponding GET would produce, while omitting the response body. Avoid performing expensive body generation only to discard it if metadata can be computed separately.

`OPTIONS` and CORS are not automatically required. Add them only when the public protocol includes them.

## Header surfaces

Node provides normalized headers, typically with lowercase names, and `rawHeaders`, which preserves raw alternating name/value entries. Application code normally uses normalized headers. Security diagnostics or strict protocol tests may inspect raw evidence.

Headers can appear more than once. Different fields have different combination rules. Do not join arbitrary duplicates with commas under a universal policy.

Bound and validate application-relevant header values:

- authorization credentials;
- content type;
- content length;
- idempotency key;
- conditional request headers;
- request/correlation ID.

Node's parser and server limits handle parts of header parsing, but the application still defines allowed lengths and syntax for its own fields.

## Body admission before retention

A common helper collects a body into memory. It must enforce a limit while reading:

```ts
import type { IncomingMessage } from 'node:http';

export async function readBoundedBody(
  request: IncomingMessage,
  maxBytes: number,
): Promise<Buffer> {
  const chunks: Buffer[] = [];
  let total = 0;

  for await (const chunk of request) {
    const bytes = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
    total += bytes.byteLength;
    if (total > maxBytes) {
      throw new Error('request body exceeds limit');
    }
    chunks.push(bytes);
  }

  return Buffer.concat(chunks, total);
}
```

The product needs more than this minimal example:

- validate `maxBytes`;
- reject early using a trustworthy `Content-Length` only as an optimization, never as sole evidence;
- stop reading and close or drain according to server policy after rejection;
- distinguish cancellation, socket error, and limit violation;
- avoid retaining chunks after terminal failure.

A declared content length can be missing or misleading. The observed byte count remains authoritative for the application limit.

## Content type is a contract

For a JSON endpoint, require a supported media type such as `application/json`. Parse parameters deliberately. A client sending JSON text with `text/plain` has violated the protocol even if `JSON.parse()` would accept it.

Media type failure occurs before JSON syntax. JSON syntax failure occurs before runtime schema validation. This order gives stable errors and prevents validators from receiving values from unsupported representations.

Do not treat an absent `Content-Type` as JSON merely because the body begins with `{` unless the product explicitly defines content sniffing.

## Empty bodies and zero-length representations

An empty body is not universally invalid. `GET` commonly has no request body. `POST /v1/jobs` requires one. The route contract decides.

Distinguish:

- no bytes;
- JSON text `null`;
- empty object `{}`;
- empty string JSON `""`.

Those are different representations and values.

## Response construction

A response owner must establish:

- status code;
- headers;
- body representation;
- whether a body is permitted;
- body length or streaming semantics;
- terminal completion or failure.

For finite bodies, compute bytes before sending headers when practical:

```ts
const bytes = Buffer.from(JSON.stringify(value), 'utf8');
response.writeHead(200, {
  'content-type': 'application/json; charset=utf-8',
  'content-length': String(bytes.byteLength),
});
response.end(bytes);
```

For `HEAD`, send the metadata including the length the GET representation would have, but omit the bytes.

`response.end()` begins or completes the local response write path. The `'finish'` event indicates the response was handed off to the operating system, not that the client processed it. A connection `'close'` can occur before or after successful response completion. Preserve both facts when they matter.

## Stable error responses

ServiceWire uses `application/problem+json` with:

- bounded stable `code`;
- HTTP `status`;
- short `title`;
- bounded `detail`;
- request ID when available;
- no stack trace;
- no raw secret headers;
- no unbounded body excerpt.

The error renderer must itself be reliable. If headers have already been sent, it may be too late to replace the response with a clean problem body. Design validation so likely failures occur before response commitment.

## Keep-alive and per-connection fairness

HTTP/1.1 can reuse a connection for several requests. A connection idle timeout and a per-request body deadline solve different problems. One client should not monopolize resources with slow headers, slow bodies, or indefinite keep-alive.

Relevant server settings and policies include:

- maximum connections;
- request timeout;
- headers timeout;
- keep-alive timeout;
- maximum requests per connection;
- application request-admission limit;
- body deadline;
- shutdown behavior for idle and active connections.

Do not rely on defaults without documenting the pinned Node baseline and product requirements.

## Request IDs

A request ID supports correlation and diagnostics. It is not an idempotency key.

Policy:

- accept a valid bounded client request ID if the protocol permits;
- otherwise generate one;
- include it in logs and error responses;
- never use it to decide semantic replay;
- ensure it contains no control characters and has a strict length.

## HTTP parser security boundaries

Node owns parsing of the request line, headers, transfer coding, and message framing. Application code should not reimplement these from raw socket bytes unless building a dedicated parser course or product.

However, the service still needs to avoid contradictory assumptions:

- do not trust `Content-Length` alone for body limits;
- do not forward ambiguous or unvalidated hop-by-hop headers blindly;
- do not construct proxy behavior without understanding message framing;
- reject malformed application headers;
- keep dependencies and Node version current.

This course builds an origin service, not a reverse proxy. Proxy-specific normalization and smuggling defenses require a separate boundary analysis.

## Worked case — strict job submission

Request:

```http
POST /v1/jobs HTTP/1.1
Host: 127.0.0.1:39117
Content-Type: application/json
Idempotency-Key: 0f7b...
Content-Length: 48

{"operation":"uppercase","payload":"hello"}
```

The finite adapter should:

1. validate method/path shape;
2. require and validate media type;
3. validate idempotency header syntax at the application boundary;
4. reject declared length above the limit;
5. read and count observed bytes;
6. decode UTF-8 under policy;
7. parse JSON into `unknown`;
8. pass `unknown` to the route validator;
9. receive a typed application result;
10. serialize a bounded response;
11. send status and headers;
12. observe response finish or early close.

The adapter must not create a job before body and semantic validation complete.

## Common wrong models

### “Node parsed HTTP, so the request is valid”

Node established HTTP syntax, not your media type or domain contract.

### “Content-Length enforces the body limit”

It is useful evidence but the observed stream must still be counted.

### “404 is enough for every mismatch”

It may hide known-path method errors, media failures, and structured client mistakes.

### “Response end means the client committed”

It establishes local write completion semantics, not remote application behavior.

### “Request ID prevents duplicates”

It identifies an attempt; idempotency needs semantic identity and server-side records.

## Decision procedure

For every finite route, write:

1. legal methods;
2. path grammar;
3. required headers and bounds;
4. request media type;
5. maximum body bytes;
6. empty-body policy;
7. syntax parser;
8. runtime validator;
9. domain command;
10. success status and representation;
11. stable error set;
12. `HEAD` and conditional behavior;
13. timeout and cancellation ownership.

## ServiceWire increment

Implement the HTTP/1.1 adapter for finite endpoints:

- bounded body reader;
- request ID policy;
- content-type validation;
- problem details;
- `GET`, `HEAD`, and `POST` semantics;
- connection registry and timeout configuration;
- active request accounting;
- graceful listener close.

The SSE endpoint remains for Module 59.

## Deep reasoning — HTTP is a sequence of trust transitions

An HTTP request reaches application code in several representations:

```text
socket bytes
  → Node parser output
  → method, target, and raw headers
  → bounded body bytes
  → decoded text
  → unknown JSON value
  → validated command
  → domain transition
```

Each arrow has a distinct failure vocabulary. Collapsing the chain into one `try/catch` produces vague 400 responses and makes it impossible to state which limit was enforced.

Consider `POST /v1/jobs` with a JSON body. Before parsing JSON, the adapter should decide:

1. Is this route and method combination supported?
2. Is a body allowed and required?
3. Is the media type acceptable?
4. Does the announced or observed body exceed the configured byte bound?
5. Did the connection terminate before the body completed?
6. Are the bytes valid UTF-8 under the chosen policy?
7. Is the JSON syntax valid?
8. Does the resulting unknown value satisfy the command schema?
9. Can the domain accept the command under current capacity and state?

These are not cosmetic distinctions. They affect status codes, retry behavior, observability, and whether the server may safely keep the connection alive.

### Commit points on the response side

`response.writeHead()` or the first body write commits response headers. After that point, replacing the response with a problem document may be impossible. If an error occurs while a streaming response is already committed, the remaining choices may be to terminate the body, destroy the connection, or encode an in-band stream error if the protocol defines one.

Finite ServiceWire responses are deliberately constructed in memory before headers are sent. The response is bounded, so this is an acceptable trade-off. The adapter can know status, headers, content length, and body before committing. Long-lived SSE uses a different contract and is handled later.

### Header normalization is not header simplification

Node exposes header values as strings, arrays, or `undefined`. A helper that always takes the first value may be correct for one header and wrong for another. Some headers are singleton by protocol policy; others are list-valued; repeated `set-cookie` values must remain distinct. Application code should request a header through a policy-aware function rather than a generic “stringify everything” conversion.

ServiceWire defines singleton handling for `Content-Type`, `Idempotency-Key`, `If-None-Match`, and request ID. Duplicate singleton values are rejected or normalized deliberately. This prevents an attacker from depending on disagreement between a proxy, Node, and application code about which value wins.

### Method semantics influence retry and caching

`GET` and `HEAD` are not merely routes with no JSON body. Their semantics affect intermediaries and clients. `HEAD` should return the metadata a corresponding `GET` would return while omitting body bytes. A `POST` that creates work is not automatically safe to retry; ServiceWire requires an idempotency key to make ambiguous transport outcomes reconcilable.

### A finite-response checklist

Before accepting a finite endpoint, verify:

- route and method table is exhaustive;
- allowed methods are returned on 405;
- body limit is enforced while reading, not after concatenation;
- bodyless and required-body cases are separate;
- UTF-8 and JSON failures are distinct;
- unknown JSON is validated before domain use;
- peer-visible problem text is bounded;
- `HEAD` metadata agrees with `GET`;
- request ID is stable through the response;
- active-request accounting decrements on every terminal path.

This checklist is the bridge between raw Node HTTP APIs and the typed application layer in Module 55.

## Ready to continue

You are ready for Module 55 when you can trace an HTTP request through every trust transition without letting the adapter perform domain mutation prematurely.

## Primary Node.js references

- [HTTP](https://nodejs.org/docs/latest-v24.x/api/http.html)
- [HTTPS](https://nodejs.org/docs/latest-v24.x/api/https.html)
- [Stream](https://nodejs.org/docs/latest-v24.x/api/stream.html)

## Continue

- [Workbook](workbook.md)
- [Reasoned solutions](solutions.md)
- [Laboratory brief](../../labs/module-54-strict-http-message-server/README.md)
- [ServiceWire engineering guide](../capstone.md)
