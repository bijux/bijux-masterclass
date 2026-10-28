# Exercises — Module 05: Hostile Input and File Handling

Work through all twelve problems before opening the answers. In **Hostile Input and File Handling**, every response must settle this question: **How are hostile strings, numbers, paths, filenames, uploads, and serialized structures constrained at the correct boundary?** A useful solution connects semantics to mechanism: who owns the decision, what can go wrong, and which retained artifact proves the claimed outcome.

## 1. Why is OpenAPI validation insufficient for file paths?

## 2. What is the safe role of a client filename?

## 3. Why check actual bytes when `Content-Length` is present?

## 4. How does atomic publication reduce risk?

## 5. Why reject symlinks in uploaded archives?

## 6. When is Unicode normalization unsafe?

## 7. What is an archive expansion budget?

## 8. How do prepared statements help and not help?

## 9. Why reject dangerous JavaScript keys in a cross-language contract?

## 10. What cleanup proof is required?

## 11. Trace semantic input and file confinement in the primary implementation

Read `capstone/tracks/python-fastapi/src/api_security/input_security.py` or `capstone/tracks/typescript-fastify/src/security/input-security.ts` in your primary track. Trace one accepted input and one rejected or failed input from the public/application boundary to the authoritative result. Name the focused regression that would fail if the central guard were removed.

## 12. Compare semantic input and file confinement across Python and TypeScript

Compare `capstone/tracks/python-fastapi/src/api_security/input_security.py` with `capstone/tracks/typescript-fastify/src/security/input-security.ts`. Identify the shared invariant, one deliberate language or library difference, and one source-shape difference that must not become a parity requirement.

## Submission format

Submit Module 05 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
