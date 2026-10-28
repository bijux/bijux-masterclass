# Exercises — Module 06: Outbound HTTP, SSRF, and Webhook Integrity

For questions 1–10, give a direct decision, governing invariant, smallest counterexample, decisive proof, and evidence limitation.

## 1. Why is `https://` alone insufficient SSRF defense?


## 2. Why reject mixed public and private DNS answers?


## 3. What does peer verification prove?


## 4. How should redirects be handled?


## 5. Why sign exact bytes?


## 6. What belongs in webhook signed metadata?


## 7. Why use both freshness and replay state?


## 8. What if the receiver commits business state and crashes before replay state?


## 9. Why revalidate at delivery instead of registration only?


## 10. What does egress firewalling add?


## 11. Trace SSRF-safe delivery and webhook integrity in the primary implementation

Read `capstone/tracks/python-fastapi/src/api_security/ssrf.py` or `capstone/tracks/typescript-fastify/src/security/ssrf.ts` in your primary track. Trace one accepted input and one rejected or failed input from the public/application boundary to the authoritative result. Name the focused regression that would fail if the central guard were removed.

## 12. Compare SSRF-safe delivery and webhook integrity across Python and TypeScript

Compare `capstone/tracks/python-fastapi/src/api_security/ssrf.py` with `capstone/tracks/typescript-fastify/src/security/ssrf.ts`. Identify the shared invariant, one deliberate language or library difference, and one source-shape difference that must not become a parity requirement.

## Submission format

Submit Module 06 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
