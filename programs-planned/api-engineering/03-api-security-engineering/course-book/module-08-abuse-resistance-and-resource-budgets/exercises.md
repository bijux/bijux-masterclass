# Exercises — Module 08: Abuse Resistance and Resource Budgets

Work through all twelve problems before opening the answers. In **Abuse Resistance and Resource Budgets**, every response must settle this question: **How can the service resist brute force and resource exhaustion without turning traffic control into false authorization?** Use the cumulative platform, not an invented toy system. Preserve inherited guarantees and make every new assumption explicit and falsifiable.

## 1. Why is request count an incomplete cost metric?


## 2. What does burst capacity represent?


## 3. Why use a monotonic clock?


## 4. Where should an upload permit be acquired?


## 5. What must happen on cancellation?


## 6. How do tenant and global budgets interact?


## 7. Why is in-memory rate limiting not multi-instance proof?


## 8. What should `Retry-After` avoid?


## 9. How does enumeration resistance differ from authorization?


## 10. Why charge rejected malicious input?


## 11. Trace resource budgets and abuse admission in the primary implementation

Read `capstone/tracks/python-fastapi/src/api_security/abuse.py` or `capstone/tracks/typescript-fastify/src/security/abuse.ts` in your primary track. Trace one accepted input and one rejected or failed input from the public/application boundary to the authoritative result. Name the focused regression that would fail if the central guard were removed.

## 12. Compare resource budgets and abuse admission across Python and TypeScript

Compare `capstone/tracks/python-fastapi/src/api_security/abuse.py` with `capstone/tracks/typescript-fastify/src/security/abuse.ts`. Identify the shared invariant, one deliberate language or library difference, and one source-shape difference that must not become a parity requirement.

## Submission format

Submit Module 08 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
