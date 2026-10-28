# Module 03 — Relational Modeling and Migrations

> **Program stage:** Course 2 of 6 — Make the promise durable.

> **Central question:** How should relational structure and migrations reinforce rather than merely store application invariants?

## Where this module fits

Design tables, keys, constraints, indexes, repositories, pools, and forward migrations from the domain rules. You arrive from Module 02 with all earlier checkpoints still green. The Course 1 handoff is fixed. This course may change internal architecture and add a compatible API release, but it may not solve an implementation problem by quietly weakening the public contract. The result is the baseline for **Transactions, Concurrency, ETags, and Idempotency**.

## Learning outcomes

- Map relationships and ownership to keys and constraints.
- Use nullability and checks to exclude invalid states.
- Choose indexes from actual query patterns.
- Own migrations explicitly and apply them from an empty database.
- Map rows to domain objects without leaking persistence shape.

## Capstone result

Persist principals, projects, datasets, runs, artifacts, and ownership with constraints and deterministic migrations.

Projects, datasets, runs, jobs, artifacts, idempotency records, and subscriptions survive restart.

## Core model

### Driving question

> How does PostgreSQL reinforce application invariants instead of acting as a passive dictionary?

The relational model is a second line of defense and a durable coordination surface. Keys, constraints, indexes, ownership columns, and migrations must encode facts the application cannot afford to lose.

A useful mental model predicts behavior under a counterexample. For every concept below, distinguish:

- the public behavior inherited from Course 1;
- the application or domain decision owner;
- the durable database, worker, storage, or delivery mechanism;
- the proof that exposes failure after retry, concurrency, or restart.


### 1. Relational identity

Each durable resource has a stable primary key independent of display fields. Relationships use foreign keys, and ownership participates in composite references where it prevents cross-owner linkage. Surrogate position columns support deterministic ordering without exposing database sequence internals as public identity.

**Counterexample.** A dataset row references a project ID but can pair it with another owner because only the project ID is constrained.

**Evidence direction.** Direct SQL attempts to create cross-owner references fail.

### 2. Constraint layering

Transport schemas reject malformed requests, domain policy rejects invalid commands, and PostgreSQL rejects invalid durable facts. The layers may overlap, but their jobs differ: the database protects data against every writer, including migrations, scripts, and future bugs.

**Counterexample.** Relying only on a Pydantic enum while the database column accepts arbitrary text.

**Evidence direction.** Bypass the application and execute invalid inserts in a disposable database.

### 3. Nullability as meaning

`NULL` must mean a specific absence, not “we forgot to decide.” State-specific fields such as `completed_at`, failure detail, and artifact metadata are nullable only when lifecycle semantics require it. Defaults are used only when the database can safely own the value.

**Counterexample.** Making every column nullable to simplify inserts, then interpreting combinations in application code.

**Evidence direction.** Schema review pairs every nullable column with allowed states and tests invalid combinations.

### 4. Ownership in the key space

Owner identity is stored with protected resources and included in queries and selected composite constraints. This makes authorization-aware access natural and blocks accidental cross-tenant association before a later response leaks it.

**Counterexample.** Fetching by `resource_id` first and checking owner in a second query.

**Evidence direction.** Foreign-resource lookups return no row, and cross-owner inserts violate constraints.

### 5. Migration immutability

Applied migrations are append-only history. A migration table records identifier and checksum. New releases add files; they do not rewrite old files. Correcting a bad released migration requires a new compensating migration.

**Counterexample.** Changing `001_base.sql` after it has run because a column name was misspelled.

**Evidence direction.** Migration proof compares checksums and refuses history drift.

### 6. Expand–backfill–contract

A compatible schema change is staged: add structures accepted by old code, deploy code that can handle both forms, backfill existing data, then enforce the new requirement only after old code is gone. The course’s `result_summary` release demonstrates the sequence.

**Counterexample.** Adding a non-null column with no default while old processes are still inserting rows.

**Evidence direction.** Release proof runs old and new application versions across each migration phase.

### 7. Repository mapping

The adapter maps rows to application values and translates database failures into stable application conditions. SQLSTATE and constraint names are more reliable than parsing English exception text.

**Counterexample.** Returning psycopg rows or node-postgres result objects directly to route handlers.

**Evidence direction.** Repository integration tests compare application values and classify named constraint failures.

### 8. Index as query contract support

An index is selected for a real predicate and order, such as `(owner_id, position)` or `(run_id, position)`. Its value is verified with `EXPLAIN`, not assumed from presence. Partial indexes support claim queues by excluding terminal rows.

**Counterexample.** Adding an index on every column while the actual query filters and sorts on a different composite order.

**Evidence direction.** Module 5 query-plan fixtures record intended scans for representative cardinality.

### Design pressure

Choose the principle above most likely to fail in **Relational Modeling and Migrations**. Compare the reference design with one credible alternative and name the counterexample that distinguishes their guarantees.

### Synthesis exercise

Build a four-column table for the capstone increment:

```text
claim | public observation | internal mechanism | falsifying experiment
```

## Architecture and state model

### 1. Schema

Durable facts, relationships, constraints, and access paths independent of one runtime.

**Invariant:** Every table and column has a domain or coordination purpose.

Ordered transformation from one known schema version to the next.

**Invariant:** An applied migration file never changes.

Implements application ports using transactions and parameterized SQL.

**Invariant:** Callers see application values and failures, not driver objects.

Isolated database created, migrated, exercised, and destroyed by tests.

**Invariant:** Tests never depend on developer data or order.

### Boundary diagram

```text
frozen OpenAPI + generated client
                |
                v
       transport/auth adapter
                |
                v
      application use case
        /       |       \
       v        v        v
  PostgreSQL  artifact  outbound HTTP
       ^        store       adapter
       |          \          /
       +----------- worker ---+
```

### Decision record template

```text
Decision:
Context and competing designs:
Chosen guarantee:
Mechanism:
Failure window that remains:
Evidence:
Rollback or migration path:
What this does not prove:
```

Use this template for at least two decisions from today. A course answer that hides remaining failure windows is incomplete.

## Worked service design

### Objective

Turn the module thesis into explicit choices before framework or SQL convenience dictates the design.

### Working method

For each decision, produce three artifacts:

1. a short decision record;
2. a sequence/state/transaction sketch;
3. a falsifying example with expected evidence.

For each decision, record the inherited API behavior, the new durable requirement, one rejected alternative, the first counterexample, and the exact application, adapter, migration, or proof file that owns the choice.

### Decision 1: Derive tables from durable facts, not from route names.

### Decision 2: Choose primary keys, public IDs, and private ordering positions deliberately.

### Decision 3: List every foreign key and whether ownership must participate.

### Decision 4: For every nullable column, write the exact states in which absence is legal.

### Decision 5: Name constraints so adapters can translate violations without parsing messages.

### Decision 6: Define migration checksums and refusal behavior for drift.

### Decision 7: Map expected queries to candidate composite or partial indexes.

### Decision 8: Design disposable-database setup that can run in CI and locally.

### Worked reasoning pattern

Suppose a learner proposes: “The route can check first, then the repository can write.” Ask:

- Can another request change the fact between check and write?
- Which rows or effects must commit atomically?
- What survives a lost response or process restart?
- Which focused test makes the race or partial effect observable?


### Design review

The design review must challenge the module-specific failure named in the lab and identify the durable oracle that distinguishes a real repair from a cosmetic pass.
## Python implementation

### Reading route

Use the implementation under:

```text
capstone/tracks/python-fastapi/src/analysis_service/
```

### Focus points

1. `migrations.py` discovers ordered SQL files, verifies migration checksums, and applies each in a transaction.
2. `PostgresRepository` uses `AsyncConnectionPool`; connection acquisition and transaction scope remain explicit.
3. Use row factories or explicit column mapping rather than positional tuple assumptions throughout the service.
4. Catch narrow psycopg exceptions and inspect SQLSTATE/constraint metadata before translating.
5. Parameterized values are supplied separately from SQL text; identifiers are never interpolated from requests.
6. Integration tests are marked `postgres` and refuse to run against a non-disposable database name.

### Representative pattern

```python
async def create_project(self, owner_id: str, project_id: str, name: str) -> Project:
    query = """
        INSERT INTO projects(public_id, owner_id, name)
        VALUES (%s, %s, %s)
        RETURNING public_id, name, description, created_at, updated_at, version
    """
    async with self.pool.connection() as connection:
        row = (await connection.execute(query, (project_id, owner_id, name))).fetchone()
    return map_project(row)
```

This excerpt is deliberately smaller than the complete implementation. Identify the transaction or decision boundary, one hidden assumption, the cleanup/error path, and the regression that would fail if the guard moved outside that boundary.


## TypeScript implementation

### Reading route

Use the implementation under:

```text
capstone/tracks/typescript-fastify/src/
```

Runtime schemas, TypeScript types, Fastify lifecycle, Node streams, and node-postgres sessions solve different problems. Keep them separate while reading.

### Focus points

1. `db.ts` owns one `pg.Pool`; transactions must hold one checked-out client for their entire lifetime.
2. Never issue `BEGIN` with `pool.query()` followed by unrelated pooled queries; PostgreSQL transactions are session-scoped.
3. Use parameterized `$1` values and explicit mapping from `snake_case` rows to application types.
4. `migrate.ts` and `migrations.ts` apply the same immutable history as the Python track to a separate database.
5. Translate `DatabaseError` fields such as `code` and `constraint`, not localized message text.
6. Close the pool during application shutdown and after integration suites.

### Representative pattern

```typescript
const client = await pool.connect();
try {
  const result = await client.query<ProjectRow>({
    text: `INSERT INTO projects(public_id, owner_id, name)
           VALUES($1, $2, $3)
           RETURNING public_id, name, description, created_at, updated_at, version`,
    values: [projectId, ownerId, name],
  });
  return mapProject(result.rows[0]);
} finally {
  client.release();
}
```

Interrogate the excerpt for cancellation, connection ownership, rollback, retry scope, and any framework convenience that could change the durable guarantee.


### Cross-language comparison

Write no more than one page:

```text
shared public guarantee:
Python mechanism:
TypeScript mechanism:
idiomatic difference:
proof shared by both:
proof that must remain track-specific:
```

## SQL and durable state

### Module data focus

1. Composite ownership foreign keys prevent cross-owner project/dataset and run relationships.
2. Check constraints close status vocabularies, progress bounds, and source-kind combinations.
3. Partial claim indexes include only queued or expired work so workers do not scan terminal history.
4. `schema_migrations` stores migration identity, checksum, and application time.

### Representative SQL

```sql
UNIQUE (public_id, owner_id),
FOREIGN KEY (project_id, owner_id)
  REFERENCES projects(public_id, owner_id),
FOREIGN KEY (dataset_id, project_id, owner_id)
  REFERENCES datasets(public_id, project_id, owner_id)
```

### Reading the statement as a proof obligation

For every SQL fragment, annotate:

```text
input parameters:
rows it may observe:
locks or transaction context:
condition that makes it atomic:
rows it may change:
constraint/index supporting it:
zero-row meaning:
retry behavior:
application failure mapping:
```

### Constraint exercise

Choose one invariant from the mental model and classify it:

Explain the classification rather than adding a trigger reflexively.

## How to verify the guarantee

### Principle

The relational model is a second line of defense and a durable coordination surface. Keys, constraints, indexes, ownership columns, and migrations must encode facts the application cannot afford to lose.

### Required proof matrix

| # | Claim | Required evidence |
|---:|---|---|
| 1 | empty database migrates to latest | Write the narrow command and machine-readable oracle. |
| 2 | migration rerun is idempotent | Write the narrow command and machine-readable oracle. |
| 3 | changed applied migration is rejected | Write the narrow command and machine-readable oracle. |
| 4 | restart preserves resources | Write the narrow command and machine-readable oracle. |
| 5 | cross-owner foreign key fails | Write the narrow command and machine-readable oracle. |
| 6 | unknown state insert fails | Write the narrow command and machine-readable oracle. |
| 7 | repository maps rows explicitly | Write the narrow command and machine-readable oracle. |
| 8 | candidate indexes match query shapes | Write the narrow command and machine-readable oracle. |

### Layer selection

Use the narrowest layer capable of falsification:

```text
pure function/vector
    ↓
application use case with substitutes
    ↓
real PostgreSQL/filesystem/receiver integration
    ↓
HTTP provider conformance
    ↓
concurrent actors
    ↓
process death and restart
    ↓
old/new release coexistence
```

Skipping directly to the bottom produces slow, opaque evidence and still may miss combinatorial policy errors.

### Defect protocol

The planted defect for this module is:

> Remove `owner_id` from one composite foreign key and demonstrate a dataset can reference a project owned by another principal.

Before injecting it, write:

```text
predicted first failing proof:
smallest input/interleaving:
expected durable state:
expected public observation:
what a weaker test would miss:
```

After repair, preserve:

```text
actual first failure:
root cause:
repair boundary:
permanent regression path:
remaining limitation:
```

### Evidence report schema

```json
{
  "claim": "...",
  "status": "passed | failed | not-executed",
  "command": "...",
  "topology": {"postgresql": "18.4", "track": "python | typescript"},
  "inputs": ["fixture/hash"],
  "assertions": ["observable or durable oracle"],
  "report": "capstone/reports/...",
  "limitations": ["what this does not establish"]
}
```

A missing dependency is `not-executed`, never `passed`.

## Failure patterns

### 1. Class-shaped schema

**Observable symptom:** One code refactor requires destructive table changes unrelated to behavior.

**Root cause:** Tables mirrored runtime classes rather than durable facts.

**Repair:** Model identities, relationships, and invariants independently, then map.

**Permanent regression:** Architecture review traces each column to a durable requirement.

### 2. Nullable everything

**Observable symptom:** Rows contain combinations no lifecycle can explain.

**Root cause:** Nullability was used to avoid insert planning.

**Repair:** Tighten columns and state-specific checks through staged migrations.

**Permanent regression:** Direct invalid-row corpus.

### 3. Application-only ownership

**Observable symptom:** A script or buggy code creates a cross-owner relation.

**Root cause:** Foreign keys ignored tenant identity.

**Repair:** Use composite uniqueness and foreign keys or equivalent constrained association.

**Permanent regression:** Direct SQL cross-owner insertion must fail.

### 4. Rewritten history

**Observable symptom:** Fresh environments work while long-lived databases fail or differ.

**Root cause:** An old migration was edited.

**Repair:** Restore original bytes and add a new migration.

**Permanent regression:** Checksum ledger proof.

### 5. Transaction through pool query

**Observable symptom:** Statements expected in one transaction execute on different sessions.

**Root cause:** Node pool convenience calls were mixed with manual `BEGIN`.

**Repair:** Checkout one client, execute all statements, commit/rollback, release.

**Permanent regression:** Forced rollback integration test.

### 6. English error parsing

**Observable symptom:** Driver or locale upgrade breaks conflict classification.

**Root cause:** Adapter searches exception message text.

**Repair:** Use SQLSTATE and named constraints.

**Permanent regression:** Assert translation metadata rather than exact driver prose.

### 7. Index decoration

**Observable symptom:** Many indexes slow writes while queries still sort or scan.

**Root cause:** Indexes were added without predicate/order analysis.

**Repair:** Derive and verify indexes from queries.

**Permanent regression:** Recorded `EXPLAIN` assertions at representative scale.

### 8. Shared test database contamination

**Observable symptom:** Tests pass alone and fail together or delete developer data.

**Root cause:** No disposable database lifecycle.

**Repair:** Create unique databases/schemas, migrate, isolate, and destroy.

**Permanent regression:** Parallel test run with safety-name guard.

### Failure triage template

```text
public symptom:
first incorrect durable fact:
first component that could have prevented it:
why existing proof missed it:
minimal reproducer:
repair:
regression:
claim still not proved:
```

## What you add to the capstone

### Target state

The in-memory dictionaries are replaced by independently owned PostgreSQL schemas while public representations and operation semantics remain unchanged.

### Increment plan

1. Review the relational model and write one justification per table, key, nullable column, and constraint.
2. Start PostgreSQL 18.4 and create a disposable database for the chosen track.
3. Apply migrations 001 and 002 from an empty state; rerun and inspect the ledger.
4. Implement repositories for projects, datasets, runs, artifacts, and subscriptions.
5. Run direct invalid SQL cases for unknown states, broken ownership, duplicate identities, and inconsistent source fields.
6. Restart API and verify previously created resources through generated client calls.

### Files to inspect before editing

```text
predecessor/spec/dist/openapi.bundle.yaml
predecessor/behavioral-scenarios.yaml
predecessor/scope-matrix.yaml
capstone/shared/operation-map.yaml
capstone/shared/state-machine.json
capstone/tracks/python-fastapi/
capstone/tracks/typescript-fastify/
capstone/scripts/course_tool.py
```

### Integration invariant

The increment must preserve the frozen contract, all earlier durable invariants, owner-aware access, bounded resources, restart safety, and equivalent public outcomes in the comparison track.


### Review trace

For one operation affected today, produce:

```text
operationId:
request/credential input:
application use case:
domain rule:
transaction/query:
external/file/process boundary:
response/problem mapping:
proof command:
remaining failure window:
```

## Representative implementation

These are the smallest useful entry points for **Relational Modeling and Migrations**.

### Python — `capstone/tracks/python-fastapi/src/analysis_service/migrations.py`

```python
LOCK_ID = 734_246_110


def migration_files(root: Path, target: str | None = None) -> list[Path]:
    files = sorted(
        path
        for path in root.glob("[0-9][0-9][0-9]_*.sql")
        if path.is_file()
    )
    if not files:
        raise RuntimeError(f"no migrations under {root}")
    versions = [path.name[:3] for path in files]
    if len(versions) != len(set(versions)):
        raise RuntimeError("migration versions must be unique")
    if target is not None:
        if len(target) != 3 or not target.isdigit():
            raise ValueError("migration target must be a three-digit revision")
        files = [path for path in files if path.name[:3] <= target]
    return files


def apply_migrations(
    database_url: str,
    root: Path,
    target: str | None = None,
) -> list[str]:
    applied: list[str] = []
    # Autocommit keeps the session-level advisory lock usable even if one
    # migration transaction fails.  Each migration and its manifest row commit
    # atomically inside an explicit transaction context.
    with psycopg.connect(database_url, autocommit=True) as connection:
        connection.execute(BOOTSTRAP)
        connection.execute("SELECT pg_advisory_lock(%s)", (LOCK_ID,))
        try:
            for path in migration_files(root, target):
                raw = path.read_bytes()
                digest = sha256(raw).hexdigest()
                version = path.name
                existing = connection.execute(
                    """
                    SELECT checksum_sha256
                    FROM schema_migrations
                    WHERE version=%s
                    """,
                    (version,),
                ).fetchone()
                if existing:
                    if existing[0] != digest:
                        raise RuntimeError(
                            f"applied migration changed: {version}"
                        )
                    continue

                with connection.transaction():
                    connection.execute(raw.decode("utf-8"))
```

### TypeScript — `capstone/tracks/typescript-fastify/src/migrations.ts`

```typescript
import pg from "pg";

const { Client } = pg;
const MIGRATION_LOCK = 734_246_110;
const MIGRATION_NAME = /^\d{3}_.+[.]sql$/;

export async function migrationFiles(
  root: string,
  target?: string,
): Promise<string[]> {
  const files = (await readdir(root))
    .filter((name) => MIGRATION_NAME.test(name))
    .sort();
  if (files.length === 0) {
    throw new Error(`no migrations found under ${root}`);
  }

  const versions = files.map((name) => name.slice(0, 3));
  if (new Set(versions).size !== versions.length) {
    throw new Error("migration history contains duplicate numeric versions");
  }
  if (target !== undefined && !/^\d{3}$/.test(target)) {
    throw new Error("migration target must contain exactly three digits");
  }
  return target === undefined
    ? files
    : files.filter((name) => name.slice(0, 3) <= target);
}

/** Apply immutable, ordered SQL migrations while holding one advisory lock. */
export async function applyMigrations(
  url: string,
  root: string,
  target?: string,
): Promise<string[]> {
  const client = new Client({ connectionString: url });
  const applied: string[] = [];
  let lockHeld = false;

  await client.connect();
  try {
    await client.query(`
      CREATE TABLE IF NOT EXISTS schema_migrations (
        version text PRIMARY KEY,
        checksum_sha256 text NOT NULL
          CHECK (checksum_sha256 ~ '^[0-9a-f]{64}$'),
        applied_at timestamptz NOT NULL DEFAULT clock_timestamp()
      )
    `);
    await client.query("SELECT pg_advisory_lock($1)", [MIGRATION_LOCK]);
    lockHeld = true;

    for (const file of await migrationFiles(root, target)) {
      const bytes = await readFile(join(root, file));
      const checksum = createHash("sha256").update(bytes).digest("hex");
```

Compare the two tracks by this invariant: **ordered migration names, one migration history, and atomic application are identical commitments**. The intended implementation difference is: the drivers and advisory-lock APIs differ, but neither provider may invent its own schema history.

## Module synthesis

The module answer to “How does PostgreSQL reinforce the service invariants instead of acting as an unstructured persistence dictionary?” is now executable in the capstone: Projects, datasets, runs, jobs, artifacts, idempotency records, and subscriptions survive restart.

## Next in the story

Module 04, [Transactions, Concurrency, ETags, and Idempotency](../module-04-transactions-concurrency-idempotency/index.md), asks: *How do public guarantees survive simultaneous requests, retries, lost responses, and process restart?* The current checkpoint must remain green while that new responsibility is added.
