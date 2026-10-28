# Exercises — Module 07: Secrets, Cryptography, and Sensitive Data

For questions 1–10, give a direct decision, governing invariant, smallest counterexample, decisive proof, and evidence limitation.

## 1. Why is an environment variable not a complete secret-management design?


## 2. Why separate keys by purpose?


## 3. What must an algorithm profile name?


## 4. Why is `==` discouraged for authentication tags?


## 5. Why validate lengths before timing-safe comparison?


## 6. What makes redaction structural?


## 7. Why are pseudonyms still sensitive?


## 8. What should an audit record contain?


## 9. What should it not contain?


## 10. What does a local hash chain prove?


## 11. Trace purpose-bound secrets and sensitive-data handling in the primary implementation

Read `capstone/tracks/python-fastapi/src/api_security/secrets.py` or `capstone/tracks/typescript-fastify/src/security/secrets.ts` in your primary track. Trace one accepted input and one rejected or failed input from the public/application boundary to the authoritative result. Name the focused regression that would fail if the central guard were removed.

## 12. Compare purpose-bound secrets and sensitive-data handling across Python and TypeScript

Compare `capstone/tracks/python-fastapi/src/api_security/secrets.py` with `capstone/tracks/typescript-fastify/src/security/secrets.ts`. Identify the shared invariant, one deliberate language or library difference, and one source-shape difference that must not become a parity requirement.

## Submission format

Submit Module 07 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
