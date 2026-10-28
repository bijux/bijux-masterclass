# Exercises — Module 09: Adversarial Verification and Supply-Chain Assurance

Work through all twelve problems before opening the answers. In **Adversarial Verification and Supply-Chain Assurance**, every response must settle this question: **How do adversarial tests and supply-chain evidence show that controls fail closed and that the proof is sensitive?** The strongest answer distinguishes specification, implementation, and operational evidence, then demonstrates where a plausible shortcut would fail.

## 1. What makes a negative test security-relevant?


## 2. Why plant defects?


## 3. What is a good fuzz oracle for strict JSON?


## 4. Why preserve minimized counterexamples?


## 5. What does an SBOM prove?


## 6. Why require lockfiles?


## 7. What is a false positive disposition?


## 8. What is a false negative risk?


## 9. Why separate core and full proofs?


## 10. What should secret scanning include?


## 11. Trace adversarial and supply-chain verification in the primary implementation

Read `capstone/tracks/python-fastapi/tests_security/test_gateway.py` or `capstone/tracks/typescript-fastify/test-security-core/gateway.test.mjs` in your primary track. Trace one accepted input and one rejected or failed input from the public/application boundary to the authoritative result. Name the focused regression that would fail if the central guard were removed.

## 12. Compare adversarial and supply-chain verification across Python and TypeScript

Compare `capstone/tracks/python-fastapi/tests_security/test_gateway.py` with `capstone/tracks/typescript-fastify/test-security-core/gateway.test.mjs`. Identify the shared invariant, one deliberate language or library difference, and one source-shape difference that must not become a parity requirement.

## Submission format

Submit Module 09 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
