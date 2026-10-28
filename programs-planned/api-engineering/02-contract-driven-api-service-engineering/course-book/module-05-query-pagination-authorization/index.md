# Module 05 — Queries, Stable Pagination, and Authorized Access

> **Program stage:** Course 2 of 6 — Make the promise durable.

> **Central question:** How do filters, stable cursors, and authorization-aware queries remain correct while data changes?

## Where this module fits

Implement owner-aware queries and server-bound cursors using a stable total order and traversal high-water mark. You arrive from Module 04 with all earlier checkpoints still green. The Course 1 handoff is fixed. This course may change internal architecture and add a compatible API release, but it may not solve an implementation problem by quietly weakening the public contract. The result is the baseline for **Durable Workers and Recovery**.

## Learning outcomes

- Bind queries to principal, operation, filters, and order.
- Use opaque server-side cursor handles.
- Prevent duplicates and omissions during a traversal.
- Conceal foreign-resource existence where policy requires it.
- Read query plans and index use.

## Capstone result

Implement owner-bound, filter-bound, high-water keyset traversal and evidence-backed query plans.

Project, dataset, and run listings are stable, owner-bound, and resistant to cursor tampering.

## Core model

### Driving question

> How do list and retrieval operations remain correct as data changes and multiple principals share the service?

A query contract includes authorization, ordering, filter semantics, cursor binding, and projection. Pagination is not `LIMIT` plus an encoded offset; it is a continuation protocol over a defined result set.

A useful mental model predicts behavior under a counterexample. For every concept below, distinguish:

- the public behavior inherited from Course 1;
- the application or domain decision owner;
- the durable database, worker, storage, or delivery mechanism;
- the proof that exposes failure after retry, concurrency, or restart.


### 1. Result-set identity

A page belongs to one operation, principal, normalized filter set, sort specification, and continuation-consistency rule. The cursor must not silently continue a different set. The course fingerprints normalized filters and stores that identity with the continuation handle.

**Counterexample.** Use a cursor from `status=queued` with `status=completed` and accept it because it decodes to an integer offset.

**Evidence direction.** Cursor replay under another owner, operation, or filter returns the documented invalid-cursor problem.

### 2. Stable total order

A continuation boundary is meaningful only under an order that can compare every pair of rows. Non-unique sort keys need a deterministic tie-breaker. The capstone’s durable position provides a simple append order; name sorting pairs normalized name with position.

**Counterexample.** `ORDER BY lower(name)` with ten equal names and no second key.

**Evidence direction.** Tie-heavy fixture pages contain every expected ID exactly once.

### 3. Keyset continuation

Keyset pagination asks for rows after the last observed ordering key instead of skipping N rows. It avoids offset drift and often scales better. The course wraps the boundary in an opaque server-side handle so public tokens do not reveal SQL structure.

**Counterexample.** `OFFSET 20` after new rows are inserted before the previous page, causing duplicates or skips.

**Evidence direction.** Capture the first-page high-water position, insert later rows, and prove that the traversal returns each unchanged row from the original eligible set once while excluding positions above the captured high-water value.

### 4. Cursor binding and expiry

A handle stores owner, operation, filter fingerprint, boundary, and expiry. This prevents token transfer and unbounded cursor-table growth. Expiry is a contract policy and must produce a stable error rather than a database miss with ambiguous meaning.

**Counterexample.** Any authenticated user can use another user’s cursor because it is only a base64 offset.

**Evidence direction.** Cross-owner and expired-handle tests inspect both HTTP response and no leaked data.

### 5. Authorization-aware query

Ownership and scope requirements shape the SQL predicate and selected projection. A protected lookup should not fetch foreign data into application memory. This reduces accidental disclosure and aligns not-found concealment with one query.

**Counterexample.** `SELECT * WHERE id=$1`, log the row, then compare `owner_id`.

**Evidence direction.** SQL integration test proves foreign ID returns no row and telemetry contains no foreign fields.

### 6. Filter normalization

Equivalent client forms must produce one semantic filter fingerprint. Defaults, case policy, list ordering, absent versus empty values, and whitespace are normalized before cursor creation. Unsupported sort fields are rejected through an allowlist, never interpolated.

**Counterexample.** Fingerprint raw query-string order so `status=queued&sort=name` differs from the reverse order.

**Evidence direction.** Equivalent normalized requests accept the same continuation; semantic changes reject it.

### 7. Projection boundary

Queries select only fields required by the application result. Projection prevents persistence-only or secret columns from reaching serializers and can reduce I/O. It should be explicit rather than `SELECT *` across evolving tables.

**Counterexample.** A new encrypted webhook-secret column appears in a generic row-to-JSON mapper.

**Evidence direction.** Code review identifies every wide internal row read, public query paths use deliberate mapping/projection boundaries, and response tests inspect exact properties. A source grep is supporting evidence, not proof that secrets cannot escape.

### 8. Plan evidence

Indexes are validated against representative predicates and order using PostgreSQL plans. The course does not freeze exact cost numbers, which vary, but records expected index/scan properties and detects obvious sequential-sort regressions.

**Counterexample.** An index exists, so the learner assumes the query uses it.

**Evidence direction.** Plan fixtures with representative cardinality show the intended composite or partial index and no unexpected sort.

### Design pressure

Choose the principle above most likely to fail in **Queries, Stable Pagination, and Authorized Access**. Compare the reference design with one credible alternative and name the counterexample that distinguishes their guarantees.

### Synthesis exercise

Build a four-column table for the capstone increment:

```text
claim | public observation | internal mechanism | falsifying experiment
```

## Architecture and state model

### 1. Normalized query

Principal, operation, filters, sort, limit, and defaults in canonical form.

**Invariant:** Semantically equivalent requests produce the same filter fingerprint.

Opaque public handle mapped to owner, operation, filter fingerprint, boundary, and expiry.

**Invariant:** A handle continues only the result set that created it.

Comparison after the last ordering tuple.

**Invariant:** Every returned row is strictly after the prior boundary.

SQL predicate and selected columns embody caller visibility.

**Invariant:** Foreign data never enters application memory.

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

### Decision 1: Define normalized filters and supported sorts for each list operation.

### Decision 2: Choose a stable total order and tie-breaker for every sort.

### Decision 3: Define cursor record fields, expiry, and cleanup.

### Decision 4: Decide continuation behavior when rows are inserted or removed between pages.

### Decision 5: Bind principal and operation into cursor identity.

### Decision 6: Push ownership into retrieval and list predicates.

### Decision 7: Choose explicit response projections and forbid dynamic column interpolation.

### Decision 8: Create representative datasets and plan assertions.

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

1. Use `filter_fingerprint()` after normalizing default and optional query values.
2. Create cursor records transactionally with the page boundary when a next page exists.
3. Keep the capstone's public order fixed as `position ASC`; an API that later exposes sort choices must select complete SQL fragments from a closed allowlist rather than interpolate request text.
4. Map a missing/foreign row to the same application not-found condition.
5. Use explicit row mapping and avoid loading secret or coordination columns.
6. Run plan inspection through a dedicated integration helper, not production logging.

### Representative pattern

```python
def normalize_run_query(*, status: str | None, limit: int | None) -> dict[str, object]:
    return {
        "status": status or "all",
        "limit": min(max(limit or 20, 1), 100),
        "order": "position:asc",  # fixed by this public operation
    }

# Cursor lookup verifies operation, owner, and filter fingerprint before
# the repository applies `position > last_position` and
# `position <= first_page_high_water`.
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

1. Parse query strings with runtime schemas, then build a normalized immutable query object.
2. The capstone exposes one fixed order, `position ASC`. A later sort extension must select a complete SQL fragment from a compile-time allowlist; it must never interpolate request text.
3. Use the same cursor/filter vectors as Python to prove semantic parity.
4. Convert PostgreSQL `bigint` positions carefully; keep values within safe representation or use string/bigint internally.
5. Keep cursor lookup and list query on one checked-out client when consistency requires it.
6. Project row fields explicitly before constructing response objects.

### Representative pattern

```typescript
const values: unknown[] = [principal.admin, principal.subject];
const predicates = ["($1 OR owner_id = $2)"];

if (name !== undefined) {
  values.push(`%${name}%`);
  predicates.push(`lower(name) LIKE lower($${values.length})`);
}

const sql = `
  SELECT *
  FROM projects
  WHERE ${predicates.join(" AND ")}
    AND position > $${values.length + 1}
    AND position <= $${values.length + 2}
  ORDER BY position
  LIMIT $${values.length + 3}
`;

// Filter values remain parameters. ORDER BY is fixed by the operation.
```

Interrogate the excerpt for cancellation, connection ownership, rollback, retry scope, and any framework convenience that could change the durable guarantee.


- Is `name` validated at runtime or only typed?
- Which `PoolClient` owns the transaction?
- What happens on rejection or abort?
- Is a promise awaited before the resource is released?
- Does a generated type accidentally stand in for a durable invariant?

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

1. List predicates begin with `owner_id` and stable keyset boundary columns.
2. Cursor table stores operation ID, owner, filter fingerprint, last position, and expiry.
3. Composite indexes align equality predicates before ordering keys.
4. Partial indexes are used only where the query includes the matching predicate.

### Representative SQL

```sql
SELECT public_id, name, description, created_at, updated_at, version
  FROM projects
 WHERE owner_id = $1
   AND position > $2
 ORDER BY position ASC
 LIMIT $3;
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

A query contract includes authorization, ordering, filter semantics, cursor binding, and projection. Pagination is not `LIMIT` plus an encoded offset; it is a continuation protocol over a defined result set.

### Required proof matrix

| # | Claim | Required evidence |
|---:|---|---|
| 1 | tie-heavy pages complete | Write the narrow command and machine-readable oracle. |
| 2 | rows inserted after page one remain above the captured high-water value and do not enter the traversal | Real PostgreSQL traversal report with returned IDs, positions, and cursor record |
| 3 | cursor bound to owner | Write the narrow command and machine-readable oracle. |
| 4 | cursor bound to operation | Write the narrow command and machine-readable oracle. |
| 5 | cursor bound to filters | Write the narrow command and machine-readable oracle. |
| 6 | expired cursor stable error | Write the narrow command and machine-readable oracle. |
| 7 | foreign resource concealed in SQL | Write the narrow command and machine-readable oracle. |
| 8 | plan uses intended access path | Write the narrow command and machine-readable oracle. |

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

> Replace one keyset cursor with an encoded offset, insert a row before page two, and capture the duplicate or omission.

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

### 1. Offset disguised as cursor

**Observable symptom:** Rows repeat or disappear when inserts occur between pages.

**Root cause:** The token encodes only an offset into a moving set.

**Repair:** Use keyset boundary or an explicit snapshot strategy.

**Permanent regression:** Insert before and between page boundaries.

### 2. Non-total ordering

**Observable symptom:** Equal sort keys appear on multiple pages or are skipped.

**Root cause:** No deterministic tie-breaker.

**Repair:** Append a unique/stable ordering component.

**Permanent regression:** Large equal-key corpus.

### 3. Unbound token

**Observable symptom:** A cursor is reusable by another owner or filter.

**Root cause:** Continuation state contains only position.

**Repair:** Bind operation, owner, and normalized filter fingerprint.

**Permanent regression:** Cross-context token matrix.

### 4. Post-fetch authorization

**Observable symptom:** Foreign rows appear in logs or timing paths before denial.

**Root cause:** Lookup by ID precedes owner check.

**Repair:** Put owner in the SQL predicate and project only visible columns.

**Permanent regression:** Foreign lookup with query/log inspection.

### 5. Raw query fingerprint

**Observable symptom:** Equivalent requests reject cursors due to parameter order or defaults.

**Root cause:** Hashing raw URL text instead of semantics.

**Repair:** Normalize typed filter object before fingerprinting.

**Permanent regression:** Permutation/equivalence vectors.

### 6. Dynamic ORDER BY injection

**Observable symptom:** Sort parameter changes SQL syntax or exposes unapproved columns.

**Root cause:** Client string interpolated into SQL.

**Repair:** Allowlist complete SQL fragments selected by code.

**Permanent regression:** Malicious and unknown sort values.

### 7. SELECT star leakage

**Observable symptom:** New internal columns unexpectedly reach response mapping.

**Root cause:** Broad projection and generic serialization.

**Repair:** Select and map exact public/application fields.

**Permanent regression:** Schema-change test plus source check.

### 8. Plan-free index claim

**Observable symptom:** Query sorts or scans despite a nominal index.

**Root cause:** Index column order or predicate does not match the query.

**Repair:** Inspect representative plans and redesign query/index together.

**Permanent regression:** Plan property assertion.

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

All list and retrieval operations become principal-bound database queries with deterministic continuation and evidence-backed access paths.

### Increment plan

1. Define result-set identity and total ordering for project, dataset, and run lists.
2. Implement normalized filters and shared fingerprint vectors.
3. Implement persisted cursor creation, lookup, expiry, and cleanup.
4. Implement keyset queries with owner-qualified predicates and explicit projections.
5. Create tie-heavy and multi-owner fixture data.
6. Traverse pages while inserting rows before and after boundaries; assert the declared semantics.

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

These are the smallest useful entry points for **Queries, Stable Pagination, and Authorized Access**.

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

Compare the two tracks by this invariant: **cursor state is bound to principal, operation, normalized filters, boundary, high-water position, and expiry**. The intended implementation difference is: Python may parse database integers directly; TypeScript preserves bigint cursor handles as strings until validated.

## Module synthesis

The module answer to “How do list and retrieval operations remain stable, efficient, and non-leaking while data changes?” is now executable in the capstone: Project, dataset, and run listings are stable, owner-bound, and resistant to cursor tampering.

## Next in the story

Module 06, [Durable Workers and Recovery](../module-06-durable-workers-recovery/index.md), asks: *What internal machinery makes `202 Accepted` honest after API or worker processes die?* The current checkpoint must remain green while that new responsibility is added.
