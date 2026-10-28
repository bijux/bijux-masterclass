# Worked Answers — Module 03: Relational Modeling and Migrations

Use these solutions to audit your reasoning for **Relational Modeling and Migrations**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why should public IDs and internal ordering positions be separate?

Public IDs are stable opaque identity; internal positions support deterministic pagination and may reflect insertion order. Exposing sequence mechanics couples clients to storage and complicates migration.

The chapter’s decisive distinction is this: Each durable resource has a stable primary key independent of display fields. Relationships use foreign keys, and ownership participates in composite references where it prevents cross-owner linkage. Surrogate position columns support deterministic ordering without exposing database sequence internals as public identity.

## 2. What invariant does a composite `(project_id, owner_id)` foreign key add?

It proves the dataset’s owner agrees with the referenced project owner, preventing cross-owner association even if application checks are bypassed.

In the cumulative capstone, the rule becomes concrete: The Relational Modeling and Migrations increment must preserve the frozen API and every earlier durability invariant while delivering this result: Persist principals, projects, datasets, runs, artifacts, and ownership with constraints and deterministic migrations The comparison track must expose the same public outcomes even when internal libraries and control flow differ.

## 3. When is a database default appropriate?

When the database can authoritatively and consistently assign the value for all writers, such as a creation timestamp or sequence. It is inappropriate when application policy must choose the value.

A useful way to reason about the boundary is: NULL must mean a specific absence, not “we forgot to decide.” State-specific fields such as completed at, failure detail, and artifact metadata are nullable only when lifecycle semantics require it. Defaults are used only when the database can safely own the value.

## 4. Why name constraints?

Adapters can translate a stable constraint identifier into a specific application conflict; generated or message-only identification is brittle.

The implementation consequence is: Transport schemas reject malformed requests, domain policy rejects invalid commands, and PostgreSQL rejects invalid durable facts. The layers may overlap, but their jobs differ: the database protects data against every writer, including migrations, scripts, and future bugs.

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 5. What makes a migration idempotent versus immutable?

Idempotent means rerunning safely has no additional effect; immutable means released bytes never change. Both matter but are different properties.

The important nuance is: Applied migrations are append-only history. A migration table records identifier and checksum. New releases add files; they do not rewrite old files. Correcting a bad released migration requires a new compensating migration.

**Evidence.** Force competing requests against one database transaction boundary and inspect public responses, uniqueness/version rows, and rollback state after restart.

## 6. Why does `pool.query("BEGIN")` not establish a transaction for later pool queries in node-postgres?

Each pool query may use a different connection, while a PostgreSQL transaction belongs to one session. A checked-out client must be retained.

Under concurrency or failure, the distinction becomes: An index is selected for a real predicate and order, such as (owner id, position) or (run id, position). Its value is verified with EXPLAIN, not assumed from presence. Partial indexes support claim queues by excluding terminal rows.

**Evidence.** Force competing requests against one database transaction boundary and inspect public responses, uniqueness/version rows, and rollback state after restart.

## 7. Design a check for local versus remote dataset source.

Use a closed `source_kind` plus checks that local-only columns are present only for local and remote URI fields only for remote; application validation remains authoritative for richer rules.

The design remains honest only if: For Relational Modeling and Migrations , record the inherited API behavior, the new durable rule, one rejected alternative, the first counterexample, and the exact application, adapter, migration, or proof artifact that owns the choice.

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 8. What should an adapter do with a unique violation on project owner/name?

Translate the named constraint and SQLSTATE into the documented application conflict, then roll back the transaction.

The consumer-facing consequence is: The excerpt for Relational Modeling and Migrations isolates one mechanism from the full service. Before copying it, locate the decision or transaction boundary, state the assumption it makes, trace cleanup on failure, and name the regression that would expose moving the guard elsewhere.

**Evidence.** Traverse multiple pages while inserting rows and changing principal or filters; assert stable high-water results and concealed foreign resources.

## 9. Why not expose database serial position as `projectId`?

It reveals volume/order, is hard to preserve across import, and confuses public identity with an access-path implementation.

The operational consequence is: Claim Required evidence ---: --- --- 1 empty database migrates to latest Write the narrow command and machine-readable oracle. 2 migration rerun is idempotent Write the narrow command and machine-readable oracle. 3 changed applied migration is rejected Write the narrow command and machine-readable oracle. 4 restart preserves resources Write the narrow command and machine-readable oracle. 5 cross-owner foreign key fails Write the narrow command and machine-readable oracle.

## 10. How do you prove an index helps?

Populate representative data, run `EXPLAIN (ANALYZE, BUFFERS)` in a controlled environment, inspect predicate/order compatibility, and compare measured plan behavior.

The strongest engineering interpretation is: A compatible schema change is staged: add structures accepted by old code, deploy code that can handle both forms, backfill existing data, then enforce the new requirement only after old code is gone. The course’s result summary release demonstrates the sequence.

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 11. Trace migration ownership in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/analysis_service/migrations.py` and `capstone/tracks/typescript-fastify/src/migrations.ts`. The required invariant is that ordered migration names, one migration history, and atomic application are identical commitments.

The defect-oriented view is: Applied migrations are append-only history. A migration table records identifier and checksum. New releases add files; they do not rewrite old files. Correcting a bad released migration requires a new compensating migration.

## 12. Compare migration ownership across Python and TypeScript

Both tracks must preserve this invariant: ordered migration names, one migration history, and atomic application are identical commitments. The intentional difference is that the drivers and advisory-lock APIs differ, but neither provider may invent its own schema history.

Across the Python and TypeScript tracks, the invariant is: The Relational Modeling and Migrations increment must preserve the frozen API and every earlier durability invariant while delivering this result: Persist principals, projects, datasets, runs, artifacts, and ownership with constraints and deterministic migrations The comparison track must expose the same public outcomes even when internal libraries and control flow differ.
