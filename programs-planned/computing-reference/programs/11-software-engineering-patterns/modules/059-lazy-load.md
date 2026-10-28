---
module_id: SEPAT-059
program: Software Engineering: Patterns
level: 2
module_number: 59
title: Lazy Load
status: complete
last_verified: 2026-08-29
---

# Lazy Load

## One-Page Review

### Governing question

When should an object defer acquiring related data until use, and what explicit loading, lifetime, consistency, authorization, query-budget, concurrency, and failure contracts prevent that deferral from becoming invisible and unsafe I/O?

### Essential definitions

- A **Lazy Load** leaves a marker in an object graph and obtains missing data when a client first demands it.
- **Lazy Initialization** tests an unloaded marker in an accessor and initializes the field on first use.
- A **Virtual Proxy** presents the target interface, loads the target on first meaningful operation, then delegates.
- A **Value Holder** wraps a loader and exposes an explicit forcing operation that returns the value.
- A **Ghost** has target identity and type but initially lacks some or all field values; access materializes its state.
- A **lazy collection** defers loading a relationship, page, count, membership, or query result; these are distinct operations unless the contract unifies them.
- An **identity map** ensures one in-memory representative per scoped persistent identity within a context.
- **N+1** is a query shape with one root query followed by up to one additional query for each traversed root or association.
- **select-in/batch loading** fetches relationships for a set of parent keys; **joined loading** fetches root and relationship rows together.
- **strict loading/raise-on-access** rejects an unplanned lazy access, turning hidden I/O into a visible contract failure.
- A **loading context** carries transaction/session, identity map, tenant, authorization, deadline, cancellation, and instrumentation premises.

### Central model, mechanism, or theorem

For a lazy slot with state

\[
q\in\{U,L(v),F(e),C\},
\]

where \(U\) is unloaded, \(L(v)\) loaded with value \(v\), \(F(e)\) failed, and \(C\) unavailable because its context is closed, forcing performs an effect only from an allowed unloaded state:

\[
\operatorname{force}(U,x)=
\begin{cases}
L(v),&\operatorname{load}(x)=v,\\
F(e),&\operatorname{load}(x)=e,\\
C,&x\text{ is closed},
\end{cases}
\qquad
\operatorname{force}(L(v),x)=L(v).
\]

In a serialized, non-invalidating value holder, successful load count is at most one. That theorem does not extend to concurrent forcing, retry, expiration, refresh, or a mutable context without additional synchronization and version rules.

### Critical invariants

- Unloaded is distinct from loaded `null`, empty collection, zero, false, failed, expired, and forbidden.
- Access that can perform I/O is documented or deliberately rejected; ordinary-looking property access is not assumed pure.
- A load uses the intended tenant, authorization, transaction/snapshot, identity map, deadline, and cancellation context.
- A closed or detached context does not silently open a new consistency/security boundary.
- Repeated serialized force of a loaded slot returns the same materialized value without another read until explicit invalidation.
- Concurrent first access has an explicit single-flight, duplicate-read, locking, or thread-confinement policy.
- Failure caching, retry, refresh, and invalidation are distinct and preserve typed outcomes.
- Collection loading defines membership, order, duplicates, filtering, pagination, count, and mutation semantics.
- Query shape is selected per use case and tested against statement, row, byte, memory, and latency budgets.
- Serialization, logging, equality, debugging, templates, and API field traversal cannot accidentally walk an unbounded graph.

### Common failures

Common failures include using `null` for both unloaded and absent, N+1 queries, eager-join row explosion, pagination corruption, access after session close, mixed transaction snapshots, cross-tenant loaders, stale authorization captured in a proxy, duplicate concurrent initialization, cached transient failure, hidden blocking in asynchronous code, cancellation ignored after a caller leaves, partial ghosts marked dirty, identity-map duplication, lazy collections mistaken for ordinary lists, serializers/debuggers triggering graph traversal, sensitive data fetched before field authorization, tests that mock away query behavior, and treating “lazy by default” as architecture.

### Compact example

A tenant-scoped `LoadingContext` and `LazyValue` show three transitions. Before forcing, the slot is unloaded and reads are zero. Two serialized reads return Ada with exactly one context read. A different slot forced after context closure reports closed, performs no read, and remains unloaded.

### Connections

[SEPAT-058](058-active-record.md) exposed association loading beneath a row object; [SEPAT-060](../ROADMAP.md) develops Identity Map. Lazy loading also depends on [Database Engineering](../../18-database-engineering/ROADMAP.md), [Distributed Systems](../../27-distributed-systems-engineering/ROADMAP.md), [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md), and [Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md).

## Governing Question

When does delayed acquisition reduce unnecessary work, and how can a design make the resulting I/O, consistency, lifetime, security, query shape, and failure behavior visible enough to reason about and verify?

Lazy Load is not merely a performance toggle. It moves an effect from an explicit query or constructor into later object use. That temporal relocation changes which transaction, authority, deadline, thread/task, error handler, and telemetry surround the read.

## Why This Matters

Loading a whole reachable object graph wastes work when most branches are never used. Deferral can reduce initial latency, memory, bandwidth, and database work. It can also let callers navigate a familiar object model without predeclaring every relationship.

The same convenience hides cost and failure behind access that looks local. A loop can issue hundreds of queries; a serializer can traverse the world; a detached object can fail far from the use case; data loaded later can come from another snapshot; and a proxy created under one authority can be forced under another.

Production design therefore treats laziness as an execution and consistency policy. It decides what may load, when, under which context, with what cardinality and budget, and what happens when the premise is unavailable.

## Prerequisites and Retrieval

You should understand object identity, interfaces/delegation, database keys and joins, transactions/isolation, Unit of Work, Data Mapper, Active Record, authorization, caching, concurrency, asynchronous I/O, serialization, and query plans. Retrieve these facts:

1. A database relationship can be fetched by separate selects, a join, a subquery, a batched key query, or a purpose-built projection; these shapes are not performance-equivalent.
2. Under common isolation levels, two statements in one use case may observe different committed states unless the transaction supplies a stable snapshot or locks.
3. A session/context usually owns identity and change tracking and is not safely usable after closure or across arbitrary concurrent tasks.
4. Authentication and tenant identity are not data properties that a loader may infer from an object ID.
5. Synchronous property access cannot transparently express `await`, cancellation, or a remote failure in an honest type contract.
6. Loaded empty and not-yet-loaded are different knowledge states.
7. Database query count alone omits returned rows, duplicated columns, bytes, server work, memory, and tail latency.

## Learning Objectives

After completing this module, you should be able to:

- distinguish Lazy Initialization, Virtual Proxy, Value Holder, Ghost, and lazy collection variants;
- model loading states and prove limited at-most-once properties under stated assumptions;
- select lazy, joined, select-in/batch, subquery, projection, or explicit loading per use case;
- calculate N+1 and batching query bounds while also reasoning about row multiplication;
- define context lifetime, identity-map, snapshot/version, retry, refresh, and invalidation semantics;
- preserve tenant/action authorization and avoid confused-deputy loaders;
- design honest synchronous and asynchronous loading APIs with deadlines and cancellation;
- control lazy collections, mutation, dirty tracking, serialization, debugging, and graph traversal;
- instrument and test real query shapes, lifecycle failures, concurrency, security, and representative cardinalities;
- reject lazy loading where predictable performance, offline use, high-stakes completeness, or explicit effects dominate convenience.

## Core Exposition

### Decide from access probability and effect cost

Deferral helps when a value is expensive and often unused. Let initial acquisition cost be \(c\), probability of later access be \(p\), and lazy overhead/failure cost be \(h\). A crude expected-work comparison is eager \(c\) versus lazy \(pc+h\). It ignores batching, correlation, tail latency, cache locality, and consistency, but exposes the real premise: low access probability alone is insufficient if later load is impossible or risky.

Measure by use case, not mapping fashion. The same `Order.customer` may be unnecessary in a write command, mandatory in a detail response, and best represented as a projection in a report.

### Recognize the four classical forms

Lazy Initialization stores an explicit sentinel and checks it on access. It is simple but tangles loading with the entity and must not confuse sentinel with a valid value.

A Virtual Proxy substitutes for a target with the same interface. It preserves navigation but intercepting every operation, identity/equality, final classes, reflection, serialization, and type tests can be difficult.

A Value Holder exposes a wrapper such as `customer_ref.read()`. It makes forcing more visible and centralizes state/failure policy, at the cost of changing the client-facing type.

A Ghost begins as a partially populated target, typically with identity. Field/method interception fills it later. It supports transparent ORM graphs but makes partial-state, dirty tracking, constructors, invariants, and debugging subtle.

Combinations are common. A collection proxy may itself hold ghosts. Name the actual mechanism; “lazy” does not specify the contract.

### Represent knowledge states explicitly

Use a sentinel or sum type for unloaded, loaded value (including `None`/empty), loading, failed, expired, forbidden, and closed as needed. A nullable field cannot encode both “known absent” and “unknown.”

Expose inspection that does not force, such as `is_loaded`, only if callers cannot use it to create timing-dependent business rules. A diagnostic state should not become an authorization bypass or an alternative truth source.

### Treat property access as an effect

Once `invoice.customer.name` may query, ordinary object syntax can block, time out, fail, allocate, acquire locks, or observe newer data. Document this in API types and architectural rules. At boundaries where surprise is costly, prefer explicit `load_customer`, awaited loader, query specification, projection, or strict-loading failure.

Do not perform lazy I/O from equality, hashing, destructors, exception formatting, validation that callers expect to be pure, or lock-protected code without deliberate analysis.

### Bind lifetime deliberately

The loader usually needs an open persistence context. An object escaping that context is detached: forcing should return a typed unavailable result or fail predictably, not silently create a new session. Reattachment/reload is an explicit application operation with new consistency and authority premises.

Keeping a context open through web rendering can make navigation convenient, but it extends connection/transaction lifetime and permits view/serializer code to issue uncontrolled queries. If used, bound it, avoid long transactions, enforce query limits, and test failure behavior. Prefer assembling response models inside the application operation when predictability matters.

### Preserve identity-map semantics

If several lazy references identify `(tenant, Customer, 7)`, forcing them in one context should normally resolve through the same identity map so object identity and tracked changes agree. The loader must consult/populate the map atomically enough for its concurrency model.

Identity scope includes tenant and any partition/generation needed to prevent collisions. A process-wide map creates staleness, memory, authorization, and concurrency hazards; context-bound identity is usually safer.

### Define snapshot and freshness

A root loaded at time \(t_0\) and relationship loaded at \(t_1\) may combine versions that never formed one consistent aggregate. Under a stable database snapshot, both reads can align; under read-committed behavior, later load may see newer membership or values.

Choose and state one: same transaction snapshot, version-compatible load, current-at-access navigation, or explicitly stale cache. For invariants and commands, reload/lock/version-check the required state within one transaction instead of trusting an old lazy graph.

### Carry tenant and authorization context safely

A loader requires trusted tenant/partition and permission to disclose the relationship or field. Do not create `CustomerProxy(id=7)` and later perform a global lookup. Bind a scoped key and enforce actor-resource-action/purpose at the use-case or loader boundary.

Authority can change between proxy creation and force. Caching a prior yes decision is valid only under a defined authorization snapshot/version; otherwise reauthorize. Never treat presence in the identity map as continuing permission to disclose.

### Understand the N+1 cost shape

If one root query returns \(N\) objects and each distinct unloaded association is forced separately, query count can be

\[
Q_{\text{naive}}=1+N.
\]

Identity-map hits may reduce this when roots share targets. Batch size \(b\) gives an upper shape near

\[
Q_{\text{batch}}=1+\lceil N/b\rceil,
\]

subject to parameter limits, composite keys, polymorphism, filters, and cache hits. A joined fetch may use one statement but return repeated root columns and up to the product of to-many cardinalities.

Therefore assert statements and rows/bytes. “One query” can be worse than several bounded queries.

### Select loader strategy per relationship and use case

- **Lazy select** is reasonable for rarely touched to-one relationships inside a valid context.
- **Select-in/batch** often handles collections predictably by fetching child rows for known parent keys.
- **Joined eager loading** can suit bounded to-one relationships, but to-many joins multiply rows and complicate ordering/pagination.
- **Subquery loading** may preserve a root query shape but adds planner/database-specific complexity.
- **Projection** selects exactly response/report fields and avoids pretending the result is a mutable entity graph.
- **Strict/raise-on-access** makes undeclared loads fail and is useful in serializers, async paths, tests, and performance-critical flows.

Loader strategy should not change which root entities qualify. If adding eager loading changes filtering, distinctness, ordering, or page membership, query semantics and loading mechanics have been improperly conflated.

### Page roots before expanding collections

Joining several to-many relationships before limit/offset can page multiplied rows rather than roots. Fetch stable root keys under deterministic unique ordering, then batch-load required relationships, or use a database-specific plan whose root semantics are proven.

Keyset pagination must carry the correct ordering tuple. Concurrent insert/delete behavior remains part of the pagination contract, not something lazy loading repairs.

### Specify lazy collection semantics

`len(collection)`, membership, indexing, iteration, slicing, append, and remove can require different queries or full materialization. A collection that reports database count without loading elements is not necessarily a normal in-memory list, especially with pending Unit of Work changes.

Define filtering, ordering, duplicates, partial pages, orphan/cascade ownership, mutation before load, and whether “loaded” means all members under a snapshot. Avoid exposing a partially loaded page as the complete aggregate collection.

### Make asynchronous I/O honest

A synchronous property cannot suspend transparently. Blocking an event-loop thread harms concurrency; implicit task creation loses structured cancellation and error ownership. In async systems, use `await repository.load_customer(...)`, `await reference.read()`, explicit prefetch, or strict loading.

Propagate deadline and cancellation to driver calls. Decide whether cancellation leaves a slot unloaded, failed, or eligible for retry. A late completion must not publish into a disposed context or leak a value to a cancelled request.

### Control concurrent first access

Two threads/tasks can observe unloaded and issue duplicate reads. Options include context thread confinement, a mutex, atomic state machine, or single-flight future shared by waiters. Define how waiter cancellation affects the shared load and whether failures are shared.

At-most-once initialization does not establish fresh or linearizable data. Locking a proxy may also serialize slow I/O and deadlock if callbacks reenter. Prefer contexts with clear single-owner concurrency rules.

### Distinguish failure, retry, refresh, and invalidation

Caching a deterministic “not found” may be useful under a snapshot; caching a timeout forever poisons the slot. Classify absent, forbidden, conflict, closed, cancelled, deadline, transient infrastructure, and malformed data.

Retry only when operation is safe, within budget, and still uses valid context. Refresh deliberately replaces a loaded value under version policy. Invalidation marks knowledge obsolete; it should not silently discard dirty tracked changes.

### Integrate ghosts with dirty tracking carefully

A partially initialized ghost must not treat fields populated from storage as user modifications. Conversely, assigning an unloaded field requires policy: load-before-write, blind guarded update of selected column, or reject until materialized. Constructors and domain invariants cannot assume every field exists.

Instrumentation/interception may fail for final/private/nonvirtual methods or direct field access. Test the exact runtime enhancement/proxy behavior rather than reasoning from mapping declarations alone.

### Bound graph traversal at external boundaries

Generic serializers, template engines, object inspectors, log formatters, debuggers, schema resolvers, and tracing can invoke getters. Use explicit DTO/projection schemas, depth/cardinality limits, field authorization, batched data loaders, and strict loading.

Logging should record scoped identifiers and loading metadata, not force values or expose sensitive fields. `toString`/representation must be safe for exception paths.

### Observe loading as a first-class operation

Record loader/relationship name, strategy, outcome, duration, statement/row/byte count, batch size, identity-map hit, context state, cancellation, and bounded caller/use-case label. Do not put raw IDs, query text with secrets, or object values in high-cardinality labels.

Trace fan-out and flag lazy queries after transaction/application boundaries. Metrics should distinguish planned batch loads, unexpected individual loads, strict-loading violations, and join explosion.

### Test the real mechanism

Unit-test the finite state machine: loaded empty, success, typed failure, retry policy, closed context, invalidation, and serialized repeated force. Add coordinated concurrency tests for the actual context guarantee.

Integration-test the real ORM/driver/database for query shape, identity map, detach/close, transaction isolation, rollback, versions, lazy collections, dirty tracking, inheritance/proxies, pagination, authorization, and async behavior. Assert statements plus rows/bytes at representative cardinality and data skew. Fault-inject timeout/cancellation/connection loss and inspect slot/context recovery.

### Know when not to use Lazy Load

Prefer eager/projection/explicit loading when data is almost always needed, a response must be complete, offline/detached operation is required, async effects must be explicit, consistency spans a fixed aggregate, query latency is tightly bounded, or a high-stakes decision cannot tolerate unknown fields.

Lazy loading is an optimization technique with semantic consequences, not a substitute for designing application queries.

### Executable model: serialized value holder and context closure

The model distinguishes unloaded from loaded values. It demonstrates one successful context read across two serialized forces and no read after closure. It does not model threads, async cancellation, databases, transactions, identity maps beyond one slot, authorization policy, invalidation, or retry.

<!-- bijux-verify: {"id":"lazy-load-value-holder","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"before=unloaded reads=0\nfirst=Ada second=Ada reads=1 state=loaded\nclosed_status=closed reads=1 state=unloaded\n","stderr":""}} -->
```python
class LoadingContext:
    def __init__(self, tenant_id, rows):
        self.tenant_id = tenant_id
        self.rows = rows
        self.reads = 0
        self.open = True

    def close(self):
        self.open = False

    def read_customer(self, customer_id):
        if not self.open:
            return ("closed", None)
        self.reads += 1
        key = (self.tenant_id, customer_id)
        return ("loaded", self.rows[key])


class LazyValue:
    def __init__(self, loader):
        self.loader = loader
        self.state = "unloaded"
        self.value = None

    def read(self):
        if self.state == "loaded":
            return ("loaded", self.value)
        status, candidate = self.loader()
        if status == "loaded":
            self.value = candidate
            self.state = "loaded"
        return (status, candidate)


rows = {("T1", "C-7"): "Ada", ("T1", "C-8"): "Grace"}
context = LoadingContext("T1", rows)
customer = LazyValue(lambda: context.read_customer("C-7"))
print(f"before={customer.state} reads={context.reads}")
first = customer.read()[1]
second = customer.read()[1]
print(f"first={first} second={second} reads={context.reads} state={customer.state}")
other = LazyValue(lambda: context.read_customer("C-8"))
context.close()
status = other.read()[0]
print(f"closed_status={status} reads={context.reads} state={other.state}")
```

### Finite invariant argument

**Initial state.** `customer.state` is unloaded and the context read count is zero.

**First force.** The loaded-state guard fails, so the loader runs. The open tenant-scoped context increments reads to one and returns Ada. The holder stores Ada and transitions to loaded.

**Second force.** The loaded-state guard returns the stored value before invoking the loader. Reads remains one and the result remains Ada.

**Closed force.** `other` is unloaded, but its context is already closed. The context returns closed before incrementing reads. Because the holder caches only loaded results, `other` remains unloaded and reads remains one.

For this finite serialized trace, a loaded holder performs exactly one successful read, repeated force is stable, and closure prevents a read. The argument assumes one caller at a time, an immutable loader/context association, no invalidation, and no exception between read and state assignment. Real concurrency requires synchronization/single-flight; a database implementation also requires transaction, identity, authorization, timeout, and error rules.

### Evidence classification

The snippet report is empirical evidence for the stated interpreter execution and output. The state/read-count argument is independently recomputable for this finite program. Neither proves general ORM correctness, database snapshot consistency, security, thread safety, async cancellation, query performance, or framework proxy behavior.

## Definitions and Notation

Let a lazy reference be \(R=(k,x,q)\), where \(k\) is a scoped persistent key, \(x\) is its loading context, and \(q\) is its local knowledge state. A scoped key includes tenant or partition as well as entity kind and identifier; an unscoped integer is insufficient identity.

The minimal state set is \(q\in\{U,L(v),F(e),C\}\): unloaded, loaded value, failed outcome, and unavailable through a closed context. Rich implementations may add \(I(f)\) for an in-flight shared future, \(E(r)\) for expired knowledge with reason/version, and distinct absent/forbidden outcomes. Loaded \(v\) includes legitimate null, false, zero, and empty values.

`force(R)` requests materialization. **Force** is not necessarily a database select: it can hit an identity map, batch result, cache, or remote service. **Load** names the actual acquisition effect. **Refresh** deliberately obtains a newer representation; **invalidation** marks prior knowledge unusable; **retry** repeats a failed acquisition under an explicit safety/budget policy.

For \(N\) roots and batch size \(b\), \(Q\) denotes database statement count, while \(R_q\), \(B_q\), \(M_q\), and \(T_q\) denote rows, bytes, application memory, and latency attributable to loading. Query efficiency is a vector, not the scalar \(Q\).

An **authorization snapshot** is a versioned/stated premise under which a prior disclosure decision may be reused. A **data snapshot** is the database consistency view. They are different: stable data does not imply continuing permission, and continuing permission does not make two reads one data snapshot.

## Mechanisms, Invariants, or Proof Structure

The mechanism has five collaborating responsibilities: a reference/proxy holds scoped identity and state; the loading context owns session/transaction, identity map, authority, deadline, and instrumentation; a strategy chooses select/join/batch/projection behavior; the Unit of Work reconciles materialization and dirty state; and the application boundary decides which effects are permitted before serialization or detachment.

For a serialized, non-invalidating reference, establish the at-most-one property by induction over forces. Initially \(q=U\) and successful-load count \(s=0\). The first successful force transitions to \(L(v)\) and \(s=1\). Every subsequent force from \(L(v)\) returns before the loader, preserving \(s=1\). A closed or failed force does not establish this result for later retry. With concurrent callers, the induction fails because both can observe \(U\); a synchronized `U -> I(f)` transition or thread confinement restores a single acquisition owner.

Correct implementations preserve these invariants:

1. **Knowledge separation:** \(U\neq L(\varnothing)\neq F(e)\neq C\).
2. **Scoped identity:** every acquisition predicate includes the trusted partition/entity key, and resolution uses the intended context identity map.
3. **Context validity:** load begins and publishes only while transaction/session, deadline, cancellation, and ownership rules permit it.
4. **Authority validity:** disclosure is authorized for current actor/resource/action/purpose or a documented authorization snapshot.
5. **Stable serialized replay:** without refresh/invalidation, force from \(L(v)\) performs no acquisition and returns the stored value.
6. **Snapshot honesty:** later-loaded values are labeled/used according to same-snapshot, version-compatible, current-at-access, or stale-cache policy.
7. **Collection completeness:** loaded collection state identifies its filter, order, page/completeness, and pending Unit of Work mutations.
8. **Boundary closure:** external serialization/logging/debugging cannot force undeclared or unbounded relationships.
9. **Failure distinction:** absent, forbidden, conflict, deadline, cancellation, closed, and transient infrastructure outcomes remain distinguishable.
10. **Budget accountability:** each allowed force contributes to an observable and tested statement/row/byte/memory/latency budget.

Verification separates proof and evidence. Static review checks state distinctions, scoped keys, effect-bearing APIs, and boundary rules. The finite program supports a narrow trace and induction. Real integration tests recompute query counts and exercise context closure, isolation, proxy interception, dirty tracking, async cancellation, and authorization with the chosen framework/database. Load and fault tests provide empirical bounds only for stated environments and data distributions; named domain/security reviewers remain necessary for high-stakes completeness and disclosure rules.

## Alternatives and Trade-Offs

| Strategy | I/O visibility | Useful fit | Principal risk |
|---|---|---|---|
| Lazy select | Hidden or wrapper-mediated at access | Rarely used bounded relation | N+1/lifetime failure |
| Select-in/batch | Explicit/planned secondary query | Many parents, bounded children | Parameter/batch limits |
| Joined eager | Root query includes relationship | Bounded to-one/read shape | Row multiplication/pagination |
| Subquery eager | Planned secondary query from root shape | ORM/database-specific cases | Complex plans/order constraints |
| Projection/DTO | Fully explicit selected fields | API/report/read model | Separate shape/evolution |
| Explicit loader | Visible method or `await` | Async, remote, controlled consistency | More orchestration |
| Strict/raise loading | Rejects undeclared access | Performance/security boundaries | Up-front query specification |
| Whole aggregate eager load | Complete known graph | Small invariant boundary | Over-fetch/large aggregates |

Use multiple strategies by operation. Mapping defaults are fallbacks, not substitutes for query plans at application boundaries.

## Failure Modes and Misconceptions

- **“Lazy means no cost unless used.”** It adds markers, branches, proxies, context lifetime, later latency, and failure complexity even when some reads are avoided.
- **“A property is still local.”** It may perform I/O, block, fail, or observe a newer snapshot.
- **“`null` means unloaded.”** `null` may be the valid loaded answer; use an explicit state.
- **“One query is always fastest.”** A join can multiply rows/bytes and corrupt root pagination.
- **“Eager loading always solves N+1.”** Wrong joins, nested collections, polymorphism, and serializers can create different explosions.
- **“An open session fixes detachment.”** It extends resource/error boundaries and enables uncontrolled view-layer queries.
- **“A proxy can open a new session.”** That silently changes transaction, identity, authorization, and failure semantics.
- **“Identity map is authorization.”** It prevents duplicate representatives; it does not grant disclosure.
- **“Loaded once means consistent.”** Root and later relationship may come from different versions/snapshots.
- **“At-most-once initialization is automatic.”** Concurrent first access can duplicate reads without confinement/synchronization.
- **“Cache every failure.”** A transient timeout then poisons future access; classify retryability.
- **“Async ORM can hide await in a getter.”** Synchronous access cannot honestly suspend or propagate structured cancellation.
- **“A lazy collection is a list.”** Count, iteration, membership, paging, and mutation may have separate database semantics.
- **“Serialization is read-only.”** Getter traversal can issue queries and disclose/allocate unbounded graphs.
- **“Mocks prove the mapping.”** They omit driver, SQL, identity, detach, dirty tracking, isolation, and proxy behavior.

## Worked Examples

### Example 1

**Situation.** A profile includes a 2 MB audit attachment opened by 2% of overview requests.

**Reasoning.** Deferring the attachment can save frequent bandwidth/memory, but a generic property should not open storage. Return attachment metadata and an authorized, explicit download operation with deadline and audit.

**Conclusion.** Low access probability supports deferral; an explicit boundary may be better than a transparent proxy.

### Example 2

**Situation.** One query returns 200 posts; rendering calls each distinct `post.author` and executes 201 statements.

**Reasoning.** This is N+1. Select-in loading authors may use a small bounded number of queries and identity-map shared authors. Assert statement, row, byte, and latency budgets.

**Conclusion.** Plan relationship loading for the collection use case.

### Example 3

**Situation.** A page joins 50 orders to lines and tags, averaging 20 lines and 10 tags.

**Reasoning.** Joining both to-many relationships can yield roughly 10,000 combined rows before deduplication and repeat order/line data. Page roots, then batch-load required collections or project the response.

**Conclusion.** Replacing N+1 with Cartesian amplification is not a win.

### Example 4

**Situation.** `customer.middle_name is None` is used both before loading and for a loaded customer without a middle name.

**Reasoning.** The accessor cannot distinguish unknown from known absent and may repeatedly query or falsely claim absence. Use an unloaded sentinel/sum state separate from loaded `None`.

**Conclusion.** Knowledge state is part of correctness.

### Example 5

**Situation.** A controller returns a mapped order after closing its session; response serialization later touches `order.lines`.

**Reasoning.** The loader no longer has a valid context. Reopening silently changes snapshot and authority. Assemble an authorized response projection before closure or reject unexpected load through strict loading.

**Conclusion.** Object lifetime must not exceed an undeclared loader lifetime.

### Example 6

**Situation.** An order header is loaded, another transaction changes line membership, then lazy lines are loaded under read committed isolation.

**Reasoning.** Header and lines may not describe one historical aggregate. A command must load required state under a stable transaction/version rule and guarded write; a current-at-access read model may accept and label the semantics.

**Conclusion.** Laziness chooses an observation time unless a snapshot constrains it.

### Example 7

**Situation.** A proxy stores customer ID 7, then a background task under tenant B forces it using a global lookup.

**Reasoning.** Unscoped identity creates cross-tenant disclosure. Scoped key, trusted context, current purpose/action authorization, and task-safe context propagation are mandatory.

**Conclusion.** Loaders are security principals' deputies, not neutral convenience functions.

### Example 8

**Situation.** An async request handler reads `order.customer.name`; the property blocks a thread or raises because implicit I/O is forbidden.

**Reasoning.** Prefetch with the request query or expose `await customer_ref.read(deadline)`. Propagate cancellation and prevent late completion from mutating a disposed context.

**Conclusion.** Async boundaries favor explicit loading or strict access.

### Example 9

**Situation.** Error logging prints an entity whose representation walks parent, children, and back-references.

**Reasoning.** Logging during failure triggers queries, recursion, latency, and sensitive-data exposure. Represent only bounded type/scoped identity/loading states without forcing.

**Conclusion.** Diagnostic paths must be load-free and privacy-safe.

### Example 10

**Situation.** A clinical decision screen treats an unloaded allergy collection as empty because the loading context timed out.

**Reasoning.** Unknown, unavailable, and confirmed empty have radically different safety meanings. The decision must fail closed or enter an explicitly reviewed degraded workflow, with authoritative retrieval, freshness, provenance, audit, and clinical/human review.

**Conclusion.** High-stakes completeness cannot be represented by transparent best-effort laziness.

## Cross-Program Connections

- [Database Engineering](../../18-database-engineering/ROADMAP.md) supplies joins, indexes, isolation, plans, cursors, and transaction behavior beneath loaders.
- [Distributed Systems](../../27-distributed-systems-engineering/ROADMAP.md) develops caching, retries, deadlines, consistency, and partial-failure limits for remote loading.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) favors explicit response projections, batching, field selection, and bounded application operations.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies tenant/action authorization, purpose limitation, disclosure control, and audit.
- [Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) provides integration, concurrency, fault, performance, and security evidence.
- [SEPAT-058](058-active-record.md) places lazy relationships on row objects; [SEPAT-060](../ROADMAP.md) develops the Identity Map that loaders commonly consult.

## References

1. Martin Fowler, [“Lazy Load”](https://martinfowler.com/eaaCatalog/lazyLoad.html), *Patterns of Enterprise Application Architecture* catalog, 2003. Definition and four principal variants.
2. Martin Fowler, *Patterns of Enterprise Application Architecture*, Addison-Wesley, 2002. Lazy Load, Identity Map, Unit of Work, and data-source patterns.
3. SQLAlchemy, [“Relationship Loading Techniques”](https://docs.sqlalchemy.org/en/21/orm/queryguide/relationships.html), 2.1 documentation accessed 2026-08-29. Lazy, raise, joined, select-in, and subquery strategies.
4. Hibernate ORM, [“Hibernate ORM User Guide”](https://docs.hibernate.org/orm/current/userguide/html_single/), current guide accessed 2026-08-29. Proxies, fetching, persistence context, and lazy initialization behavior.
5. Ruby on Rails, [“Active Record Query Interface”](https://guides.rubyonrails.org/active_record_querying.html), current guide accessed 2026-08-29. Eager loading, strict loading, joins, and query behavior.
6. Martin Kleppmann, *Designing Data-Intensive Applications*, O’Reilly, 2017. Transactions, snapshots, caching, and distributed-system failure semantics.
7. Jim Gray and Andreas Reuter, *Transaction Processing: Concepts and Techniques*, Morgan Kaufmann, 1992. Transaction and concurrency foundations.
8. Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software*, Addison-Wesley, 2004. Aggregate boundaries, repositories, and explicit application operations.
9. OWASP Foundation, [“Authorization Cheat Sheet”](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html), accessed 2026-08-29. Per-request authorization, least privilege, and object-level access principles.
10. Brian Goetz et al., *Java Concurrency in Practice*, Addison-Wesley, 2006. Safe publication, lazy initialization, synchronization, and concurrent state reasoning.

## Exercises

### Exercise 1

Extend the finite state model on paper with loading, failed, expired, and closed states. Define transitions for two concurrent callers, cancellation, retryable timeout, not found, refresh, and context closure. State which properties need synchronization.

### Exercise 2

A query returns 100 orders, each with one distinct customer and a lazy line collection. Calculate worst-case statement counts when both associations are traversed naïvely, then for customer batch size 25 and lines batch size 20. Explain why query count does not settle performance.

### Exercise 3

Design loading for an order-detail API and an order-list API. Specify projection/entity choice, strategy per relationship, transaction/snapshot, identity, authorization, pagination, async interface, budgets, serialization, and tests.

### Exercise 4

Diagnose a service that keeps a session open through JSON serialization, shows intermittent detached errors in jobs, and has both N+1 alerts and oversized eager joins. Produce an incremental correction plan with evidence gates.

### Exercise 5

Review lazy loading for a clinical medication-allergy decision. Define known-empty versus unavailable states, authority/freshness/provenance, transaction/consistency, degraded behavior, UI/accessibility, privacy/audit, tests, operations, and required named human review.

## Answers to the Exercises

### Answer 1

Use `U` unloaded, `I(f)` in-flight future, `L(v,version)` loaded, `F(e,retryability)` failed, `E(version)` expired, and `C` closed. From `U`, one synchronized compare-and-set installs `I`; the winner starts the load and other callers await the same future. Success publishes `L`; deterministic absent may publish a loaded option/typed absence; retryable timeout/cancellation returns to `U` or a time-bounded `F` according to policy. A single waiter's cancellation should normally detach that waiter, not cancel shared work, unless all waiters cancel and the driver safely supports cancellation.

Refresh moves `L/E` to a new `I` only after resolving dirty-state policy; invalidation moves clean `L` to `E`. Closure atomically prevents new loads, cancels/awaits in-flight work per ownership policy, and prevents late publication into the context. Synchronization protects state/future publication, waiter accounting, value visibility, invalidation/refresh races, and close versus completion. Database/version/authorization rules remain outside this local state proof.

### Answer 2

The root costs 1. Traversing 100 distinct customers adds 100 and 100 distinct line collections adds 100, so worst case is 201 statements. With customer batches of 25, `ceil(100/25)=4`; line batches of 20 add 5; including root gives 10 statements, assuming all keys can be grouped, no cache hits, and one query per batch.

Ten statements can still lose if each line batch returns enormous collections, parameters/plans are poor, rows are wide, network round trips are distant, or skew creates memory/tail-latency spikes. Conversely 201 indexed local reads might appear tolerable in a tiny test while collapsing under concurrency. Measure returned rows/bytes, database time, application allocation, connection occupancy, p95/p99 latency, representative skew, and correctness of root membership/order/snapshot.

### Answer 3

For order detail, load one authorized tenant-scoped order under the intended read snapshot and project required header, customer summary, bounded ordered lines, totals, and version. Use joined loading only for bounded to-one values; select-in or a direct projection for lines. Exclude optional histories/attachments behind explicit authorized endpoints. Do not serialize mapped objects. The async repository returns an awaited DTO/result with deadline/cancellation and typed not-found/denied/unavailable outcomes.

For order list, keyset-page stable root keys under authorized filters/order, select a compact row projection, then batch-load only bounded fields actually shown; often customer display names can be one join while lines become aggregate counts rather than collections. Scope identity by tenant, bind authorization at query construction and field disclosure, and state current-at-read versus stable snapshot semantics.

Tests use the real database/ORM and assert root membership/order, no cross-tenant fields, statement/row/byte budgets, page boundaries, empty/large/skewed associations, detachment/strict-loading violations, concurrent updates, timeout/cancellation, serialization depth, and explain plans. Telemetry distinguishes use case and strategy without sensitive/high-cardinality values.

### Answer 4

First inventory query traces by endpoint/job, relationship, cardinality, context lifetime, and serializer access. Add strict-loading in selected tests and query/row/byte budgets; reproduce detached paths and join multiplication with realistic data. Create explicit response projections assembled inside application operations, starting with the highest-fan-out endpoint. Page roots before batch-loading selected relationships and remove generic entity serialization.

Jobs receive scoped IDs/commands and open their own bounded transaction/context; they do not receive mapped objects from request contexts. Replace implicit async loads with awaited repositories/prefetch. Close contexts before rendering once each endpoint projection is complete. For remaining mapped internal flows, define detach behavior and use strict/raise access at boundaries.

Migrate endpoint by endpoint with parity/security tests, latency/database-load canaries, plan review, connection occupancy, fault injection, and rollback switches. Do not globally switch every association eager or lazy: choose each use-case shape. Evidence gates include zero undeclared loads, bounded rows/bytes/statements, stable page semantics, tenant/field authorization, no job detachment failures, and acceptable p95/p99 under representative concurrency.

### Answer 5

Model allergy evidence as `confirmed_empty(source, observed_at, version)`, `present(records,...)`, `unavailable(reason, last_known...)`, `stale`, or `conflicted`; never map timeout/unloaded to empty. The decision operation authenticates and authorizes actor-patient-purpose, retrieves medications and allergy data from authoritative scoped sources within an approved consistency/version window, records provenance and policy version, and fails closed or enters a separately approved override/escalation workflow when completeness is unavailable.

Use explicit awaited loading with deadline/cancellation, no view-layer lazy I/O, privacy-minimized projections, immutable audit, and guarded versions. The UI visibly distinguishes loading, verified empty, present, stale, and unavailable; supports keyboard/screen reader/color-independent cues; prevents premature action; and explains override/escalation. Operations monitor source freshness, timeout, mismatch, override, and reconciliation without exposing patient data in telemetry.

Tests cover every knowledge state, source disagreement, staleness boundary, race/version change, tenant/patient/purpose matrix, guessed IDs, cancellation/late completion, outage/recovery, audit integrity, UI/accessibility, and fail-closed behavior. Named clinicians/pharmacists, patient-safety, clinical informatics, privacy/legal/regulatory, security, accessibility/human-factors, database/distributed-systems, SRE, and incident-response owners must review real policies and workflow. Passing code cannot establish clinical safety or regulatory compliance.
