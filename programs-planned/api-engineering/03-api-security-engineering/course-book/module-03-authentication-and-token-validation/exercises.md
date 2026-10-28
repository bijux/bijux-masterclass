# Exercises — Module 03: Authentication and Token Validation

## 1. Why is signature validity insufficient?

## 2. Who chooses the accepted JWT algorithm?

## 3. Why validate `typ`?

## 4. How should an unknown `kid` be handled?

## 5. What does audience express?

## 6. Why inject a clock?

## 7. What is the difference between token expiry and revocation?

## 8. Why store API-key digests?

## 9. Why reject bearer plus API key?

## 10. What should a 401 response reveal?

## 11. Trace resource-server credential validation in the primary implementation

Read `capstone/tracks/python-fastapi/src/api_security/tokens.py` or `capstone/tracks/typescript-fastify/src/security/tokens.ts` in your primary track. Trace one accepted input and one rejected or failed input from the public/application boundary to the authoritative result. Name the focused regression that would fail if the central guard were removed.

## 12. Compare resource-server credential validation across Python and TypeScript

Compare `capstone/tracks/python-fastapi/src/api_security/tokens.py` with `capstone/tracks/typescript-fastify/src/security/tokens.ts`. Identify the shared invariant, one deliberate language or library difference, and one source-shape difference that must not become a parity requirement.

## Submission format

Submit Module 03 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
