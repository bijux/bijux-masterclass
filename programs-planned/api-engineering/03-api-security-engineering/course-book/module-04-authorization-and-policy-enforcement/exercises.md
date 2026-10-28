# Exercises — Module 04: Authorization and Policy Enforcement

## 1. Why is a scope not object authorization?

## 2. Where should tenant filtering occur?

## 3. What does default deny mean for a new endpoint?

## 4. When use 403 versus concealed 404?

## 5. Why is authorization after lookup risky?

## 6. What is an obligation?

## 7. How should support impersonation be modeled?

## 8. Why protect output fields?

## 9. How does ETag mutation interact with authorization?

## 10. What proves list isolation?

## 11. Trace default-deny resource authorization in the primary implementation

Read `capstone/tracks/python-fastapi/src/api_security/authorization.py` or `capstone/tracks/typescript-fastify/src/security/authorization.ts` in your primary track. Trace one accepted input and one rejected or failed input from the public/application boundary to the authoritative result. Name the focused regression that would fail if the central guard were removed.

## 12. Compare default-deny resource authorization across Python and TypeScript

Compare `capstone/tracks/python-fastapi/src/api_security/authorization.py` with `capstone/tracks/typescript-fastify/src/security/authorization.ts`. Identify the shared invariant, one deliberate language or library difference, and one source-shape difference that must not become a parity requirement.

## Submission format

Submit Module 04 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
