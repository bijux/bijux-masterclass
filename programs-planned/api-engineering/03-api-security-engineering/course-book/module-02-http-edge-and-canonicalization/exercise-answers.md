# Reference Answers — Module 02: HTTP Edge and Canonicalization

Read after attempting all twelve HTTP Edge and Canonicalization exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Why must edge policy execute before JWT validation?

**Answer.** The credential channel and external origin may be ambiguous; validating a token does not resolve which Authorization value or host interpretation is authoritative.

## 2. When may `X-Forwarded-Proto` be trusted?

**Answer.** Only when the immediate peer is configured as a trusted proxy and the chain interpretation is explicit.

## 3. Why reject duplicate JSON keys instead of choosing last-wins?

**Answer.** Different components may choose differently, enabling a security decision over one value and business action over another.

## 4. What is the difference between byte limit and nesting limit?

**Answer.** A small body can still be deeply nested; bytes bound memory transfer while depth bounds parser recursion/complexity.

## 5. Why is malformed UTF-8 a security concern?

**Answer.** Replacement or divergent decoding can make validators and downstream systems see different text.

## 6. What should happen to two Authorization headers?

**Answer.** Reject the request as ambiguous; do not concatenate or choose silently.

## 7. Why is `Access-Control-Allow-Origin` not authentication?

**Answer.** It is enforced by browsers for response visibility; arbitrary HTTP clients are unaffected.

## 8. What is a safe host policy?

**Answer.** An explicit normalized allowlist including expected port semantics, applied after trusted proxy reconstruction.

## 9. Why are request-smuggling proofs environment-specific?

**Answer.** They depend on the exact front proxy, server, protocol version, and parsing chain; application unit tests cannot prove the full path.

## 10. Where should strict JSON errors map publicly?

**Answer.** To the frozen client-error/problem vocabulary without exposing parser internals or reflected hostile content.

## 11. Trace raw HTTP edge evaluation in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/api_security/edge.py` and `capstone/tracks/typescript-fastify/src/security/edge.ts`. The required invariant is that critical singleton headers, trusted proxy assertions, media type, body size, and strict JSON are decided before model construction.

## 12. Compare raw HTTP edge evaluation across Python and TypeScript

Both tracks must preserve this invariant: critical singleton headers, trusted proxy assertions, media type, body size, and strict JSON are decided before model construction. The intentional difference is that ASGI and Fastify hooks differ; ambiguous raw messages must be rejected identically.
