# Reference Answers — Module 03: Relational Modeling and Migrations

Read after attempting all twelve Relational Modeling and Migrations exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Why should public IDs and internal ordering positions be separate?

Public IDs are stable opaque identity; internal positions support deterministic pagination and may reflect insertion order. Exposing sequence mechanics couples clients to storage and complicates migration.

## 2. What invariant does a composite `(project_id, owner_id)` foreign key add?

It proves the dataset’s owner agrees with the referenced project owner, preventing cross-owner association even if application checks are bypassed.

## 3. When is a database default appropriate?

When the database can authoritatively and consistently assign the value for all writers, such as a creation timestamp or sequence. It is inappropriate when application policy must choose the value.

## 4. Why name constraints?

Adapters can translate a stable constraint identifier into a specific application conflict; generated or message-only identification is brittle.

## 5. What makes a migration idempotent versus immutable?

Idempotent means rerunning safely has no additional effect; immutable means released bytes never change. Both matter but are different properties.

## 6. Why does `pool.query("BEGIN")` not establish a transaction for later pool queries in node-postgres?

Each pool query may use a different connection, while a PostgreSQL transaction belongs to one session. A checked-out client must be retained.

## 7. Design a check for local versus remote dataset source.

Use a closed `source_kind` plus checks that local-only columns are present only for local and remote URI fields only for remote; application validation remains authoritative for richer rules.

## 8. What should an adapter do with a unique violation on project owner/name?

Translate the named constraint and SQLSTATE into the documented application conflict, then roll back the transaction.

## 9. Why not expose database serial position as `projectId`?

It reveals volume/order, is hard to preserve across import, and confuses public identity with an access-path implementation.

## 10. How do you prove an index helps?

Populate representative data, run `EXPLAIN (ANALYZE, BUFFERS)` in a controlled environment, inspect predicate/order compatibility, and compare measured plan behavior.

## 11. Trace migration ownership in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/analysis_service/migrations.py` and `capstone/tracks/typescript-fastify/src/migrations.ts`. The required invariant is that ordered migration names, one migration history, and atomic application are identical commitments.

## 12. Compare migration ownership across Python and TypeScript

Both tracks must preserve this invariant: ordered migration names, one migration history, and atomic application are identical commitments. The intentional difference is that the drivers and advisory-lock APIs differ, but neither provider may invent its own schema history.
