# Exercises — Module 05: Queries, Stable Pagination, and Authorized Access

## 1. Why must an order be total for cursor pagination?

## 2. How does pure keyset pagination behave when a row appears before the boundary, and what extra rule does the capstone high-water value provide?

## 3. What semantic data belongs in a cursor fingerprint?

## 4. Why store server-side cursor handles instead of signed self-contained tokens?

## 5. How can deletion between pages affect keyset traversal?

## 6. Why is foreign ownership represented as not found?

## 7. What is wrong with `ORDER BY ${sort}`?

## 8. How should an expired cursor differ from a never-valid cursor?

## 9. Why is `SELECT *` dangerous even with response validation?

## 10. Design a pagination invariant.

## 11. Trace stable authorized pagination in the primary implementation

Read `capstone/tracks/python-fastapi/src/analysis_service/postgres.py` or `capstone/tracks/typescript-fastify/src/repository.ts` in your primary track. Trace one accepted input and one rejected or failed input from the public/application boundary to the authoritative result. Name the focused regression that would fail if the central guard were removed.

## 12. Compare stable authorized pagination across Python and TypeScript

Compare `capstone/tracks/python-fastapi/src/analysis_service/postgres.py` with `capstone/tracks/typescript-fastify/src/repository.ts`. Identify the shared invariant, one deliberate language or library difference, and one source-shape difference that must not become a parity requirement.

## Submission format

Submit Module 05 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
