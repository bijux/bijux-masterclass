# Exercises — Module 10: Security Operations and Incident Response

For questions 1–10, give a direct decision, governing invariant, smallest counterexample, decisive proof, and evidence limitation.

## 1. What is the first goal of triage?


## 2. When revoke a token `jti` versus a subject?


## 3. How does webhook key containment work?


## 4. Why preserve compatibility during a security release?


## 5. What belongs in an incident timeline?


## 6. Why not log the leaked secret as evidence?


## 7. What proves containment?


## 8. What proves recovery?


## 9. How should a vulnerable dependency be handled?


## 10. Why update the threat model?


## 11. Trace security incident containment and recovery in the primary implementation

Read `capstone/tracks/python-fastapi/src/api_security/incident.py` or `capstone/tracks/typescript-fastify/src/security/incident.ts` in your primary track. Trace one accepted input and one rejected or failed input from the public/application boundary to the authoritative result. Name the focused regression that would fail if the central guard were removed.

## 12. Compare security incident containment and recovery across Python and TypeScript

Compare `capstone/tracks/python-fastapi/src/api_security/incident.py` with `capstone/tracks/typescript-fastify/src/security/incident.ts`. Identify the shared invariant, one deliberate language or library difference, and one source-shape difference that must not become a parity requirement.

## Submission format

Submit Module 10 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
