# Worked Answers — Module 02: HTTP Edge and Canonicalization

Use these solutions to audit your reasoning for **HTTP Edge and Canonicalization**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why must edge policy execute before JWT validation?

The credential channel and external origin may be ambiguous; validating a token does not resolve which Authorization value or host interpretation is authoritative.

The chapter’s decisive distinction is this: Critical singleton fields deserve special treatment. Two Authorization fields, two Host fields, or conflicting Content-Length values are not a request the application should repair. Reject ambiguity before authentication or body parsing. Some HTTP request-smuggling classes depend on disagreement between intermediaries and cannot be solved solely in application code; the course control establishes a strict application boundary while requiring edge-server and proxy configuration to agree on malformed-message handling.

## 2. When may `X-Forwarded-Proto` be trusted?

Only when the immediate peer is configured as a trusted proxy and the chain interpretation is explicit.

In the cumulative capstone, the rule becomes concrete: For each deployment topology, write a trust rule. A direct client connection may use the socket peer, request target, and Host field. A proxied deployment may trust one exact proxy network to replace those values with a specified forwarding convention. The application must ignore forwarding fields from every other peer.

## 3. Why reject duplicate JSON keys instead of choosing last-wins?

Different components may choose differently, enabling a security decision over one value and business action over another.

A useful way to reason about the boundary is: Register a Fastify content-type parser for JSON that receives text or bytes, applies the same duplicate/depth/number profile, and returns a parsed value. Use an onRequest hook for raw headers and proxy policy before authentication. Avoid relying on plain JSON.parse for duplicate-member detection.

## 4. What is the difference between byte limit and nesting limit?

A small body can still be deeply nested; bytes bound memory transfer while depth bounds parser recursion/complexity.

The implementation consequence is: Body limits must be enforced while bytes are read. Checking Content-Length alone trusts a client assertion and misses chunked transfer. Reading the complete body and then comparing length has already paid the memory cost. The decisive test sends a stream that crosses the limit and observes bounded allocation and an early documented response.

## 5. Why is malformed UTF-8 a security concern?

Replacement or divergent decoding can make validators and downstream systems see different text.

The important nuance is: Strict JSON illustrates the point. JSON object member names are not required to be unique by every parser behavior in practice. If one layer keeps the first role and another keeps the last, the message has no single meaning. The course parsers reject duplicate members, malformed UTF-8, non-finite numeric forms, excessive depth, and an over-budget body before Pydantic or TypeBox constructs application models.

## 6. What should happen to two Authorization headers?

Reject the request as ambiguous; do not concatenate or choose silently.

Under concurrency or failure, the distinction becomes: Implement an ASGI middleware that reads bounded raw bytes, rejects ambiguous critical headers, invokes a strict JSON decoder with object pairs hook, and replays the validated body to FastAPI. Do not modify Starlette private request attributes. Put verified edge context in scope["state"].

**Evidence.** Exercise missing scope, correct scope/wrong owner, wrong tenant, stale support context, field restrictions, and successful ownership while checking that denied requests perform no protected source I/O.

## 7. Why is `Access-Control-Allow-Origin` not authentication?

It is enforced by browsers for response visibility; arbitrary HTTP clients are unaffected.

The design remains honest only if: Framework request objects are already interpretations. Headers may have been merged, case-normalized, decoded, or discarded; a proxy may have rewritten the host, scheme, and client address. Security decisions that depend on those values must therefore define which component owns the canonical interpretation and which raw evidence remains available.

**Evidence.** Remove the central guard in a planted variant and require the negative security suite to detect the exact unauthorized or leaked outcome.

## 8. What is a safe host policy?

An explicit normalized allowlist including expected port semantics, applied after trusted proxy reconstruction.

The consumer-facing consequence is: At the end of this module, one raw inbound message must have one accepted interpretation or one rejection. The Python ASGI middleware and Fastify content-type/parser hooks may be shaped differently, but they must agree on critical duplicates, proxy trust, host/scheme, media type, byte budget, and strict JSON outcomes.

**Evidence.** Exercise missing scope, correct scope/wrong owner, wrong tenant, stale support context, field restrictions, and successful ownership while checking that denied requests perform no protected source I/O.

## 9. Why are request-smuggling proofs environment-specific?

They depend on the exact front proxy, server, protocol version, and parsing chain; application unit tests cannot prove the full path.

The operational consequence is: Security validation commonly fails because decoding and checking occur in the wrong sequence. Preserve raw input for diagnostics, then apply the one protocol-defined parse, then validate the parsed result, then normalize only where the application has defined an equivalence relation. Repeated percent decoding, opportunistic Unicode folding, or trimming values that the protocol treats as significant can create a second language understood only by part of the stack.

## 10. Where should strict JSON errors map publicly?

To the frozen client-error/problem vocabulary without exposing parser internals or reflected hostile content.

The strongest engineering interpretation is: At the end of this module, one raw inbound message must have one accepted interpretation or one rejection. The Python ASGI middleware and Fastify content-type/parser hooks may be shaped differently, but they must agree on critical duplicates, proxy trust, host/scheme, media type, byte budget, and strict JSON outcomes.

**Evidence.** Run the shared hostile-input corpus through raw edge parsing and both implementations, asserting rejection, bounded resource use, cleanup, and non-leaking problem responses.

## 11. Trace raw HTTP edge evaluation in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/api_security/edge.py` and `capstone/tracks/typescript-fastify/src/security/edge.ts`. The required invariant is that critical singleton headers, trusted proxy assertions, media type, body size, and strict JSON are decided before model construction.

The defect-oriented view is: Implement an ASGI middleware that reads bounded raw bytes, rejects ambiguous critical headers, invokes a strict JSON decoder with object pairs hook, and replays the validated body to FastAPI. Do not modify Starlette private request attributes. Put verified edge context in scope["state"].

## 12. Compare raw HTTP edge evaluation across Python and TypeScript

Both tracks must preserve this invariant: critical singleton headers, trusted proxy assertions, media type, body size, and strict JSON are decided before model construction. The intentional difference is that ASGI and Fastify hooks differ; ambiguous raw messages must be rejected identically.

Across the Python and TypeScript tracks, the invariant is: Register a Fastify content-type parser for JSON that receives text or bytes, applies the same duplicate/depth/number profile, and returns a parsed value. Use an onRequest hook for raw headers and proxy policy before authentication. Avoid relying on plain JSON.parse for duplicate-member detection.
