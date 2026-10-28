# Exercises — Module 01: Threat Modeling and Security Requirements

Work through all twelve problems before opening the answers. In **Threat Modeling and Security Requirements**, every response must settle this question: **Which assets, actors, trust boundaries, abuse cases, and assumptions define the real security problem?** A complete response identifies the contract owner, predicts one observable failure, and names the evidence that decides the case; a definition by itself is incomplete.

## 1. Rewrite “attackers may steal data” as a concrete threat.

## 2. Distinguish an asset from a security property.

## 3. Why is a private JWKS signing key in a fixture directory an assumption and an asset?

## 4. What makes a requirement falsifiable?

## 5. Why can one threat map to several requirements?

## 6. Why can one requirement answer several threats?

## 7. Give one trust boundary inside a single process.

## 8. What is wrong with “all dependencies are trusted”?

## 9. When should a threat be accepted rather than mitigated?

## 10. What proof detects an orphan requirement?

## 11. Trace threat-to-control traceability in the primary implementation

Read `capstone/tracks/python-fastapi/src/api_security/models.py` or `capstone/tracks/typescript-fastify/src/security/models.ts` in your primary track. Trace one accepted input and one rejected or failed input from the public/application boundary to the authoritative result. Name the focused regression that would fail if the central guard were removed.

## 12. Compare threat-to-control traceability across Python and TypeScript

Compare `capstone/tracks/python-fastapi/src/api_security/models.py` with `capstone/tracks/typescript-fastify/src/security/models.ts`. Identify the shared invariant, one deliberate language or library difference, and one source-shape difference that must not become a parity requirement.

## Submission format

Submit Module 01 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
