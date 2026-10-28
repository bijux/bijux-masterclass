# Exercises — Module 09: Fault Injection, Troubleshooting, and Game Days

Work through all twelve problems before opening the answers. In **Fault Injection, Troubleshooting, and Game Days**, every response must settle this question: **How can fault injection and game days produce falsifiable evidence without creating uncontrolled damage?** The strongest answer distinguishes specification, implementation, and operational evidence, then demonstrates where a plausible shortcut would fail.

## 1. What makes a fault experiment scientific enough for this course?

## 2. Why test latency separately from failure?

## 3. What is a safe blast radius?

## 4. When should an experiment abort?

## 5. Why use an unaffected journey as a control?

## 6. What is the first troubleshooting question?

## 7. Should operators trust the first correlated metric?

## 8. What cleanup evidence is required after a worker-kill test?

## 9. How should a discovered failure be retained?

## 10. When are compound faults appropriate?

## 11. Trace bounded fault injection and diagnosis in the primary implementation

Read `capstone/tracks/python-fastapi/src/api_reliability/faults.py` or `capstone/tracks/typescript-fastify/src/reliability/faults.ts` in your primary track. Trace one accepted input and one rejected or failed input from the public/application boundary to the authoritative result. Name the focused regression that would fail if the central guard were removed.

## 12. Compare bounded fault injection and diagnosis across Python and TypeScript

Compare `capstone/tracks/python-fastapi/src/api_reliability/faults.py` with `capstone/tracks/typescript-fastify/src/reliability/faults.ts`. Identify the shared invariant, one deliberate language or library difference, and one source-shape difference that must not become a parity requirement.

## Submission format

Submit Module 09 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
