# Exercises — Module 03: Relational Modeling and Migrations

## 1. Why should public IDs and internal ordering positions be separate?

## 2. What invariant does a composite `(project_id, owner_id)` foreign key add?

## 3. When is a database default appropriate?

## 4. Why name constraints?

## 5. What makes a migration idempotent versus immutable?

## 6. Why does `pool.query("BEGIN")` not establish a transaction for later pool queries in node-postgres?

## 7. Design a check for local versus remote dataset source.

## 8. What should an adapter do with a unique violation on project owner/name?

## 9. Why not expose database serial position as `projectId`?

## 10. How do you prove an index helps?

## 11. Trace migration ownership in the primary implementation

Read `capstone/tracks/python-fastapi/src/analysis_service/migrations.py` or `capstone/tracks/typescript-fastify/src/migrations.ts` in your primary track. Trace one accepted input and one rejected or failed input from the public/application boundary to the authoritative result. Name the focused regression that would fail if the central guard were removed.

## 12. Compare migration ownership across Python and TypeScript

Compare `capstone/tracks/python-fastapi/src/analysis_service/migrations.py` with `capstone/tracks/typescript-fastify/src/migrations.ts`. Identify the shared invariant, one deliberate language or library difference, and one source-shape difference that must not become a parity requirement.

## Submission format

Submit Module 03 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
