# Module 04 exercises — PostgreSQL Query and Persistence Performance

Solve these without opening the answer file. Show assumptions, units, populations, and the decisive oracle. A numerical result without its interpretation is incomplete.

## 1. Propose an index for owner, status, descending created_at/id pagination.

Provide a defensible engineering answer and name the evidence needed to verify it.

## 2. Why can an index-only scan still read heap pages?

Provide a defensible engineering answer and name the evidence needed to verify it.

## 3. Actual rows are 100,000 while estimated rows are 100. What does that suggest?

Provide a defensible engineering answer and name the evidence needed to verify it.

## 4. A query executes in 8 ms but request span shows 240 ms database time. What next?

Provide a defensible engineering answer and name the evidence needed to verify it.

## 5. Why is `EXPLAIN ANALYZE DELETE ...` dangerous?

Provide a defensible engineering answer and name the evidence needed to verify it.

## 6. For 8 API instances with pool max 20, 4 workers with pool max 5, and reserve 10, calculate possible connections.

Provide a defensible engineering answer and name the evidence needed to verify it.

## 7. Why may status be a poor leading index column?

Provide a defensible engineering answer and name the evidence needed to verify it.

## 8. What does a sort spill indicate?

Provide a defensible engineering answer and name the evidence needed to verify it.

## 9. How does high-water pagination affect the index query?

Provide a defensible engineering answer and name the evidence needed to verify it.

## 10. Why should exact planner cost not be a cross-version gate?

Provide a defensible engineering answer and name the evidence needed to verify it.

## 11. When is a partial index appropriate?

Provide a defensible engineering answer and name the evidence needed to verify it.

## 12. Design a read/write index decision.

Provide a defensible engineering answer and name the evidence needed to verify it.

## Submission format

Submit Module 04 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
