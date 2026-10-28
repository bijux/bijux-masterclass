# Module 04 — Transactions, Concurrency, ETags, and Idempotency

> **Program stage:** Course 2 of 6 — Make the promise durable.

> **Central question:** How do idempotency and conditional updates remain atomic under concurrent requests and process restarts?

## Where this module fits

Use atomic predicates, unique constraints, transaction boundaries, and durable replay records. You arrive from Module 03 with all earlier checkpoints still green. The Course 1 handoff is fixed. This course may change internal architecture and add a compatible API release, but it may not solve an implementation problem by quietly weakening the public contract. The result is the baseline for **Queries, Stable Pagination, and Authorized Access**.

## Learning outcomes

- Draw the transaction boundary for each use case.
- Implement compare-and-swap for `If-Match`.
- Persist idempotency scope, fingerprint, and response.
- Handle simultaneous duplicate requests with one logical winner.
- Prove rollback leaves no partial state.

## Capstone result

Implement persistent request fingerprints, replayed outcomes, version columns, ETags, and transaction rollback.

One hundred concurrent identical submissions create one run; stale ETags fail atomically; replay survives restart.

## Core model

### Driving question

> How do public guarantees survive simultaneous requests, retries, and process restarts?

Correctness under concurrency comes from atomic predicates, unique constraints, transaction boundaries, and durable replay records—not from checking state before writing it.

A useful mental model predicts behavior under a counterexample. For every concept below, distinguish:

- the public behavior inherited from Course 1;
- the application or domain decision owner;
- the durable database, worker, storage, or delivery mechanism;
- the proof that exposes failure after retry, concurrency, or restart.


### 1. Atomic decision

The condition and mutation must be evaluated as one database action or one serializable transaction. Application locks protect only one process and are insufficient across workers or replicas.

**Counterexample.** Read project version 4, compare in Python, then update by ID without version predicate.

**Evidence direction.** Barrier-started concurrent PATCH requests yield exactly one success for the same ETag.

### 2. Transaction boundary by outcome

A transaction encloses all durable changes that define one externally visible outcome. Analysis submission includes idempotency reservation, run creation, initial event, and job creation. If any part fails, none may remain.

**Counterexample.** Commit the run, then insert the job in a second transaction.

**Evidence direction.** Injected failure after each statement leaves zero partial records.

### 3. Scoped idempotency identity

The key is scoped by principal and operation so independent callers and endpoints may reuse the same string. The request fingerprint additionally binds canonical request content.

**Counterexample.** A global key namespace leaks another user’s stored response.

**Evidence direction.** Same key for two principals creates independent runs; same principal/operation/key with changed body conflicts.

### 4. Reservation and replay

Concurrent first attempts race to insert one unique idempotency record. The winner performs the transaction; losers observe the record and replay when complete. An incomplete reservation requires explicit recovery policy rather than indefinite waiting.

**Counterexample.** Each request checks for a record, sees none, creates a run, then tries to insert the key.

**Evidence direction.** High-concurrency proof asserts one run, one job, one idempotency row, and identical response identity.

### 5. Stored response boundary

Replay preserves status, selected stable headers, and response body as originally committed. Volatile headers such as `Date` or request correlation ID need not be identical. The course names the stored header set.

**Counterexample.** Recomputing the response from current resource state, which may have advanced from queued to completed.

**Evidence direction.** Replay after the run changes still returns the original accepted representation and replay marker.

### 6. Compare-and-swap ETag

The representation version becomes an HTTP validator. Parsing establishes that the tag belongs to the target resource; the conditional update proves it is still current. Zero updated rows are resolved into concealed not-found versus stale precondition without leaking ownership.

**Counterexample.** Accept any quoted integer as the version for any project.

**Evidence direction.** Malformed, wrong-resource, stale, foreign, and current validators each have distinct expected behavior.

### 7. Isolation and retry

PostgreSQL may abort transactions for deadlock or serialization conflicts. Only the transaction closure may be retried, with bounded attempts and only when its external effects have not escaped. Outbound HTTP never occurs inside the retried transaction.

**Counterexample.** Retry the whole HTTP handler after it has already written a file or sent a webhook.

**Evidence direction.** Injected retryable database failure repeats only pure/durable database work and produces one outcome.

### 8. Deadlock discipline

Consistent lock ordering and narrow transactions reduce deadlocks. Deadlocks are still possible and must be classified. Holding transactions open while waiting for network or user input is prohibited.

**Counterexample.** Update project then dataset in one path, dataset then project in another.

**Evidence direction.** Concurrency tests exercise opposing operations and verify bounded retry or explicit failure.

### Design pressure

Choose the principle above most likely to fail in **Transactions, Concurrency, ETags, and Idempotency**. Compare the reference design with one credible alternative and name the counterexample that distinguishes their guarantees.

### Synthesis exercise

Build a four-column table for the capstone increment:

```text
claim | public observation | internal mechanism | falsifying experiment
```

## Architecture and state model

### 1. Idempotency record

Scoped key, request fingerprint, completion state, stored status, selected headers, body, and timestamps.

**Invariant:** One completed record denotes one logical operation outcome.

Single SQL statement whose predicate includes owner, identity, and expected version.

**Invariant:** At most one concurrent caller using the same version succeeds.

All database statements and pure computation eligible for bounded retry.

**Invariant:** No irreversible external effect occurs before commit.

Barrier-synchronized workload plus database count assertions.

**Invariant:** The test distinguishes logical outcomes from merely successful HTTP responses.

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

### Decision 1: List every row created by `createAnalysisRun` and place them in one transaction.

### Decision 2: Define canonical request fingerprinting independent of JSON object key order.

### Decision 3: Define idempotency scope and stored response fields.

### Decision 4: Decide behavior for an abandoned incomplete reservation.

### Decision 5: Implement ETag parse, resource binding, and conditional update separately.

### Decision 6: Name retryable SQLSTATEs and maximum retries.

### Decision 7: Keep transaction closures free of filesystem and network effects.

### Decision 8: Design barrier-based proofs and database cardinality assertions.

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

1. Use `canonical_json()` and `request_fingerprint()` from the pure core.
2. Acquire one pool connection and transaction context for submission; do not nest hidden commits in repository helpers.
3. Use `INSERT ... ON CONFLICT` or unique-violation handling to arbitrate first idempotency ownership.
4. Persist JSON response data and selected headers in the idempotency row.
5. For PATCH, perform conditional SQL update and inspect `RETURNING` rather than comparing before update.
6. Bound retry logic around the transaction function and preserve cancellation semantics.

### Representative pattern

```python
async def update_project(
    connection: AsyncConnection,
    *, owner_id: str, project_id: str, expected_version: int, patch: ProjectPatch,
) -> Project:
    row = await connection.execute(
        """
        UPDATE projects
           SET name = COALESCE(%s, name),
               description = CASE WHEN %s THEN %s ELSE description END,
               version = version + 1,
               updated_at = clock_timestamp()
         WHERE owner_id = %s AND public_id = %s AND version = %s
        RETURNING public_id, name, description, created_at, updated_at, version
        """,
        (patch.name, patch.has_description, patch.description,
         owner_id, project_id, expected_version),
    )
    updated = row.fetchone()
    if updated is None:
        raise StaleOrMissingProject(project_id)
    return map_project(updated)
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

1. Checkout one `PoolClient` and pass it through all statements in the transaction.
2. Use deterministic canonical JSON before SHA-256 fingerprinting; ordinary `JSON.stringify` insertion order is not a contract by itself.
3. Handle PostgreSQL unique and serialization codes by stable `code` fields.
4. Do not retain a client across request idle time or stream lifetime.
5. Use `UPDATE ... RETURNING` for compare-and-swap and release the client in `finally`.
6. Run `Promise.all` only for independent work; statements inside one transaction remain deliberately ordered.

### Representative pattern

```typescript
const client = await pool.connect();
try {
  await client.query("BEGIN");
  const outcome = await submitAnalysisTransaction(client, command);
  await client.query("COMMIT");
  return outcome;
} catch (error) {
  await client.query("ROLLBACK");
  throw translateDatabaseError(error);
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

1. `PRIMARY KEY(owner_id, operation_id, idempotency_key)` is the concurrency arbiter.
2. Idempotency rows store fingerprint, response status, headers, and body.
3. Project update predicates include `version`; successful updates increment it atomically.
4. Run, initial event, job, and idempotency completion commit together.

### Representative SQL

```sql
UPDATE projects
   SET name = $1, version = version + 1, updated_at = clock_timestamp()
 WHERE owner_id = $2
   AND public_id = $3
   AND version = $4
RETURNING public_id, name, description, version, updated_at;
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

Correctness under concurrency comes from atomic predicates, unique constraints, transaction boundaries, and durable replay records—not from checking state before writing it.

### Required proof matrix

| # | Claim | Required evidence |
|---:|---|---|
| 1 | 100 identical requests one run | Write the narrow command and machine-readable oracle. |
| 2 | changed-body reuse conflicts | Write the narrow command and machine-readable oracle. |
| 3 | different principal same key independent | Write the narrow command and machine-readable oracle. |
| 4 | replay survives restart | Write the narrow command and machine-readable oracle. |
| 5 | replay returns original accepted snapshot | Write the narrow command and machine-readable oracle. |
| 6 | same ETag only one update | Write the narrow command and machine-readable oracle. |
| 7 | rollback leaves no partial rows | Write the narrow command and machine-readable oracle. |
| 8 | retry excludes outbound effects | Write the narrow command and machine-readable oracle. |

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

> Replace the conditional update with `SELECT version` followed by `UPDATE ... WHERE id`. The two-request barrier must demonstrate double success.

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

### 1. Check-then-insert idempotency

**Observable symptom:** Concurrent duplicates create multiple runs.

**Root cause:** Existence check and creation are separate atomic units.

**Repair:** Use unique insertion/reservation inside the outcome transaction.

**Permanent regression:** Barrier-started 100-request test plus row counts.

### 2. Key without body binding

**Observable symptom:** A caller reuses a key for another dataset and receives unrelated success.

**Root cause:** Only key identity was persisted.

**Repair:** Store canonical request fingerprint and conflict on mismatch.

**Permanent regression:** Same key, semantically different body.

### 3. Recomputed replay

**Observable symptom:** Retry returns completed while original response was queued.

**Root cause:** Current resource state is fetched instead of stored response.

**Repair:** Persist and replay the original response boundary.

**Permanent regression:** Advance run before retry and compare.

### 4. Non-atomic ETag check

**Observable symptom:** Two PATCH requests both succeed with the same validator.

**Root cause:** Version was checked before an unconditional update.

**Repair:** Put expected version in the update predicate.

**Permanent regression:** Barrier race with exactly one 200 and one 412.

### 5. Wrong-resource ETag

**Observable symptom:** An ETag from project A updates project B when versions coincide.

**Root cause:** Validator encodes only a number and parser ignores resource binding.

**Repair:** Bind opaque tag generation/parsing to resource identity.

**Permanent regression:** Cross-resource validator test.

### 6. External effect inside retry

**Observable symptom:** A serialization retry sends duplicate webhooks or publishes duplicate files.

**Root cause:** Transaction closure includes irreversible I/O.

**Repair:** Commit intent/outbox, then perform external effect after commit.

**Permanent regression:** Inject one retryable abort and count external calls.

### 7. Inconsistent lock order

**Observable symptom:** Load produces recurring deadlocks.

**Root cause:** Paths acquire rows in different order.

**Repair:** Define stable ordering and keep transactions narrow.

**Permanent regression:** Opposing concurrent operations with bounded retry evidence.

### 8. Leaked open transaction

**Observable symptom:** Pool exhaustion and long-held locks after exceptions.

**Root cause:** Commit/rollback/release is not structured.

**Repair:** Use context managers or `try/catch/finally` around one checked-out connection.

**Permanent regression:** Injected exception followed by pool health and lock check.

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

The predecessor’s idempotency and ETag promises become durable coordination protocols that remain correct across concurrency and restart.

### Increment plan

1. Write transaction diagrams for analysis submission and project conditional update.
2. Implement scoped idempotency reservation, fingerprint binding, and stored response in the primary repository.
3. Implement atomic ETag update with resource-bound parsing.
4. Inject failure after each statement of submission and prove rollback.
5. Run sequential replay, changed-body conflict, cross-principal reuse, and restart replay.
6. Run 100 barrier-synchronized duplicate submissions and assert one run/job/idempotency record.

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

These are the smallest useful entry points for **Transactions, Concurrency, ETags, and Idempotency**.

### Python — `capstone/tracks/python-fastapi/src/analysis_service/postgres.py`

```python
Row = dict[str, Any]


class PostgresRepository:
    def __init__(
        self,
        database_url: str,
        encryption_key: str,
        callback_signing_secret: str,
        service_release: str = "1.0",
    ) -> None:
        if service_release not in {"1.0", "1.1"}:
            raise ValueError("service_release must be 1.0 or 1.1")
        self.pool = ConnectionPool(
            database_url,
            min_size=1,
            max_size=16,
            open=False,
        )
        self.encryption_key = encryption_key
        self.callback_signing_secret = callback_signing_secret
        self.service_release = service_release

    @property
    def exposes_api_1_2(self) -> bool:
        return self.service_release == "1.1"

    def open(self) -> None:
        self.pool.open(wait=True)

    def close(self) -> None:
        self.pool.close()

    @contextmanager
    def connection(self) -> Iterator[Connection[Row]]:
        with self.pool.connection() as connection:
            connection.row_factory = dict_row
            yield connection

    def health(self) -> None:
        with self.connection() as connection:
            connection.execute("SELECT 1").fetchone()

    # ------------------------------------------------------------------
    # Row mapping and visibility
    # ------------------------------------------------------------------
    @staticmethod
    def _visible(
        principal: Principal,
        alias: str = "",
    ) -> tuple[str, list[Any]]:
        prefix = f"{alias}." if alias else ""
        if principal.admin:
            return "TRUE", []
        return f"{prefix}owner_id=%s", [principal.subject]
```

### TypeScript — `capstone/tracks/typescript-fastify/src/repository.ts`

```typescript
  WebhookSubscriptionCreate,
} from "./types.js";

export type StoredResponse = Readonly<{
  status: number;
  headers: Record<string, string>;
  body: RunRepresentation;
  replay: boolean;
}>;

type CursorWindow = Readonly<{
  // node-postgres returns PostgreSQL bigint values as strings. Keep them as
  // strings so a long-lived service never crosses JavaScript's 53-bit limit.
  boundary: string;
  snapshot: string;
}>;

type Page<T> = Readonly<{
  items: T[];
  nextCursor: string | null;
}>;

function iso(value: unknown): string {
  if (value instanceof Date) return value.toISOString();
  return String(value);
}

function notFound(resource: string): ApiProblem {
  return new ApiProblem(
    404,
    "Resource not found",
    `The requested ${resource} does not exist.`,
    "not-found",
  );
}

/**
 * PostgreSQL adapter for application and worker use cases.
 *
 * One adapter intentionally owns transactions that cross runs, jobs,
 * artifacts, events, and outbox rows. Splitting those operations into one
 * repository per table would conceal the atomicity boundary this course is
 * teaching.
 */
export class PostgresRepository {
  public constructor(
    private readonly database: Database,
    private readonly encryptionKey: string,
    private readonly callbackSecret: string,
    private readonly serviceRelease: "1.0" | "1.1",
  ) {}

  public get exposesApi12(): boolean {
    return this.serviceRelease === "1.1";
  }
```

Compare the two tracks by this invariant: **one key and fingerprint produce one durable outcome, while a stale version fails atomically**. The intended implementation difference is: context-manager transactions and promise-scoped clients differ without changing the commit boundary.

## Module synthesis

The module answer to “How do public guarantees survive simultaneous requests, retries, lost responses, and process restart?” is now executable in the capstone: One hundred concurrent identical submissions create one run; stale ETags fail atomically; replay survives restart.

## Next in the story

Module 05, [Queries, Stable Pagination, and Authorized Access](../module-05-query-pagination-authorization/index.md), asks: *How do list and retrieval operations remain stable, efficient, and non-leaking while data changes?* The current checkpoint must remain green while that new responsibility is added.
