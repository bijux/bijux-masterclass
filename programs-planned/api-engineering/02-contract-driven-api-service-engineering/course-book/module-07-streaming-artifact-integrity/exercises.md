# Exercises — Module 07: Streaming and Artifact Integrity

Work through all twelve problems before opening the answers. In **Streaming and Artifact Integrity**, every response must settle this question: **How can large uploads, progress streams, and artifacts remain bounded, durable, and integrity-checked?** Each solution must survive delay, duplication, version skew, hostile input, or partial failure where relevant; happy-path intuition alone earns no credit.

## 1. Why is Content-Length insufficient for enforcement?

## 2. Why must staging and final paths share a filesystem?

## 3. What does content-addressed storage buy?

## 4. Why publish before metadata in this course?

## 5. What is the cost of verifying checksum on every download?

## 6. How should interrupted staging be cleaned?

## 7. Why not hold a transaction while streaming run events?

## 8. How does SSE reconnect relate to event positions?

## 9. Can two logical artifacts share content bytes?

## 10. What should happen when bytes are tampered?

## 11. Trace bounded content-addressed artifact publication in the primary implementation

Read `capstone/tracks/python-fastapi/src/analysis_service/artifacts.py` or `capstone/tracks/typescript-fastify/src/artifacts.ts` in your primary track. Trace one accepted input and one rejected or failed input from the public/application boundary to the authoritative result. Name the focused regression that would fail if the central guard were removed.

## 12. Compare bounded content-addressed artifact publication across Python and TypeScript

Compare `capstone/tracks/python-fastapi/src/analysis_service/artifacts.py` with `capstone/tracks/typescript-fastify/src/artifacts.ts`. Identify the shared invariant, one deliberate language or library difference, and one source-shape difference that must not become a parity requirement.

## Submission format

Submit Module 07 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
