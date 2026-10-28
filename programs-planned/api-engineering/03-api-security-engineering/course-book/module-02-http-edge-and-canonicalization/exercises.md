# Exercises — Module 02: HTTP Edge and Canonicalization

## 1. Why must edge policy execute before JWT validation?

## 2. When may `X-Forwarded-Proto` be trusted?

## 3. Why reject duplicate JSON keys instead of choosing last-wins?

## 4. What is the difference between byte limit and nesting limit?

## 5. Why is malformed UTF-8 a security concern?

## 6. What should happen to two Authorization headers?

## 7. Why is `Access-Control-Allow-Origin` not authentication?

## 8. What is a safe host policy?

## 9. Why are request-smuggling proofs environment-specific?

## 10. Where should strict JSON errors map publicly?

## 11. Trace raw HTTP edge evaluation in the primary implementation

Read `capstone/tracks/python-fastapi/src/api_security/edge.py` or `capstone/tracks/typescript-fastify/src/security/edge.ts` in your primary track. Trace one accepted input and one rejected or failed input from the public/application boundary to the authoritative result. Name the focused regression that would fail if the central guard were removed.

## 12. Compare raw HTTP edge evaluation across Python and TypeScript

Compare `capstone/tracks/python-fastapi/src/api_security/edge.py` with `capstone/tracks/typescript-fastify/src/security/edge.ts`. Identify the shared invariant, one deliberate language or library difference, and one source-shape difference that must not become a parity requirement.

## Submission format

Submit Module 02 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
