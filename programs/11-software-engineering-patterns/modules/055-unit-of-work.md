---
module_id: SEPAT-055
program: Software Engineering: Patterns
level: 2
module_number: 55
title: Unit of Work
status: complete
last_verified: 2026-08-28
---

# Unit of Work

## One-Page Review

### Governing question

How can an application track every persistent object changed by one local business operation, preserve one in-scope identity representation, order and batch writes, detect concurrency conflicts, and commit or roll back coherently without confusing flush, commit, user conversation, or distributed workflow?

### Essential definitions

- A **Unit of Work (UoW)** tracks objects affected by a business operation and coordinates writing changes plus resolving concurrency problems.
- A **persistence context** is the scoped set of managed object identities, states, snapshots, and pending persistence actions.
- An **identity map** ensures at most one managed object representation for each persistence identity within the scope.
- An object may be **transient/new**, **managed/clean**, **dirty**, **deleted/removed**, or **detached** relative to a Unit of Work.
- **dirty checking** detects differences between a managed object's current and original persistent state; explicit registration records mutation intent directly.
- **flush** synchronizes pending changes into the database transaction; it is not necessarily transaction commit or durable success.
- **commit** asks the transaction to make its writes durable/visible under the datastore contract.
- **rollback** aborts database transaction effects; it does not automatically restore arbitrary in-memory objects or external effects.
- An **optimistic version** is an expected state token included in a guarded update/delete to detect stale writes.
- A **dependency graph** orders inserts/updates/deletes so keys and constraints can be satisfied.

### Central model, mechanism, or theorem

For identity map \(M\), original snapshots \(B\), and disjoint pending sets new \(N\), dirty \(D\), deleted \(X\), Unit of Work computes an ordered write plan \(W=\tau(N,D,X)\). Commit succeeds only if one database transaction applies every guarded action:

\[
\mathrm{commit}(M,B,N,D,X)=
\begin{cases}
(B',\varnothing,\mathrm{committed}),&\text{all constraints/versions hold},\\
(B,\varnothing,\mathrm{conflict/failure}),&\text{transaction aborts}.
\end{cases}
\]

Atomic database rollback prevents partial durable writes under its assumptions. It does not rewind object graphs, files, network calls, sequences, logs, or another resource; post-failure in-memory state must be expired, discarded, refreshed, or repaired explicitly.

### Critical invariants

- One Unit of Work belongs to one bounded local operation, one execution context, and one explicit transaction owner; it is not shared concurrently.
- Within it, persistence identity maps to at most one managed object; duplicate representations cannot be merged silently.
- New, dirty, and deleted classifications are coherent/disjoint, and transitions are validated (for example, deleted objects cannot also be inserted).
- Original version/snapshot and current intent remain available until guarded flush succeeds or the scope is abandoned.
- Flush orders writes by declared key/constraint dependencies and executes inside the intended transaction/isolation level.
- Every update/delete that needs stale-write protection includes an expected version or equivalent predicate and interprets affected-row count.
- Commit or rollback is singular; repositories join the scope and never independently finalize it.
- Failure invalidates or reconciles managed state; callers cannot assume rollback restored object fields.
- Bulk/native SQL, triggers, generated values, and alternate writers explicitly synchronize, expire, refresh, or bypass tracked objects under a documented rule.
- Local commit plus outbox can be atomic; remote effects and multi-datastore work require separate coordination and recovery claims.

### Common failures

Common failures include one global session/UoW, sharing it across threads/tasks, request-scoped scope that accidentally spans streaming/background work, transaction per repository, commit inside `save`, flushing mistaken for commit, autoflush surprises before queries, user think time inside transactions, duplicate object instances, mutable keys, dirty checking over mutable aliases, registering the same object new and deleted, wrong insert/delete order, cascades that delete too much, stale overwrite without versions, bulk SQL leaving cached objects stale, retrying the same poisoned context, rollback followed by reuse of mutated objects, hidden lazy loads after close, huge identity maps, callbacks with external effects during flush, and assuming a local UoW coordinates broker or second database atomically.

### Compact example

One finite UoW loads accounts A and B twice but returns the same managed A instance, tracks two dirty identities, preflights expected versions, and commits balances 700 and 800 with versions 4 and 9 as one copied-state replacement. A second stale UoW detects version mismatch and applies no balance write.

### Connections

[SEPAT-054](054-service-layer.md) owns the application transaction scope; [SEPAT-056](../ROADMAP.md) develops Identity Map. Unit of Work connects to [Database Engineering](../../18-database-engineering/ROADMAP.md), [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md), and [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md).

## Governing Question

What exact scope and protocol make a set of in-memory object changes become one coherent local database outcome, including identity, change detection, ordering, conflicts, failure cleanup, and evidence—without promising more than the transaction manager actually provides?

A Unit of Work is both a bookkeeping pattern and a transaction coordination boundary. Mature ORMs often implement it as a session/persistence context, but the pattern can be explicit and need not use an ORM.

## Why This Matters

Writing every object immediately causes excessive calls, awkward dependency ordering, and partial operations. Deferring writes without tracking them risks lost changes, duplicate instances, constraint failures, and stale overwrites. Unit of Work gathers intent, sees the whole local change set, and chooses an ordered transactional write plan.

Its apparent convenience hides semantics. An ORM may flush before a query, retain mutated objects after rollback, execute writes in dependency order rather than source order, or bypass tracking during bulk updates. Production correctness depends on knowing those rules and the database beneath them.

Unit of Work is not a substitute for a long-running workflow. A local transaction should be short; a business conversation across requests or services needs versions, states, idempotency, messages, and compensation rather than an open session/transaction.

## Prerequisites and Retrieval

You should understand object identity/equality, repositories, Data Mapper, transactions/ACID, isolation/locking, constraints/keys, optimistic concurrency, dependency graphs, outbox, and partial failure. Retrieve these facts:

1. Database atomicity applies to governed database writes, not arbitrary memory or external effects.
2. Two objects with the same database key can diverge unless the scope enforces identity uniqueness.
3. An update based on stale data needs a version/lock/isolation mechanism; later write does not imply correctness.
4. Foreign keys impose ordering constraints on inserts and deletes unless deferred or otherwise handled.
5. A query issued after pending changes may need flush for read-your-writes semantics.
6. A database-generated key/version/default is not known accurately in memory until returned/refreshed.
7. A failed transaction/session may require rollback and disposal before further use.

## Learning Objectives

After completing this module, you should be able to:

- define Unit of Work scope and distinguish it from repository, identity map, transaction, session, and business workflow;
- model transient, managed, clean, dirty, removed, and detached state transitions;
- compare caller registration, object registration, snapshot dirty checking, and instrumentation;
- derive an ordered/batched write plan from dependency and constraint semantics;
- distinguish flush, commit, durable acknowledgment, rollback, close, detach, expire, and refresh;
- implement optimistic version predicates and classify zero affected rows correctly;
- handle nested operations, savepoints, retries, cancellation, and post-failure in-memory state;
- integrate generated values, cascades, bulk SQL, triggers, soft deletion, outbox, and audit safely;
- test real mapping/transaction/isolation/failure behavior and observe UoW cost;
- recognize overscoped contexts, hidden commits, stale identity maps, and distributed overclaims.

## Core Exposition

### Scope one local operation

Create a Unit of Work per application operation or explicit local transaction. The Service Layer owns begin/commit/rollback/close, and repositories participate. Scope propagation may be explicit parameter/dependency injection or carefully managed context, but ownership must be visible.

Do not use a process-global UoW. Most sessions are not safe to share across threads or concurrent async tasks, and a long-lived identity map returns stale objects and grows without bound. A request can be a convenient lifetime only if streaming, callbacks, background tasks, and nested calls do not escape it.

### Model object states

A transient object has no persistent representation in this UoW. Registering new schedules insert. Loading/attaching yields managed clean state with identity and original snapshot/version. Mutation makes it dirty explicitly or by detection. Marking removed schedules delete/soft-delete. Closing/clearing detaches it.

Define legal transitions. New then deleted before flush may cancel insertion; deleted then modified is normally invalid; detached instances require reload/merge with version policy. Never infer domain lifecycle merely from persistence state: “removed from session” and “business account closed” are different concepts.

### Enforce one representation per identity

The identity map key includes mapped type/context plus persistent key and, where necessary, tenant/shard. Every repository load first checks the map; materialization populates or reconciles the existing managed instance rather than creating a second one.

Identity uniqueness supports consistent changes and relationship wiring, but is scoped only to the UoW. It is not a global cache and does not prevent another transaction/process from loading/updating the same row. Optimistic/pessimistic concurrency remains necessary.

### Choose change tracking deliberately

**Caller registration** explicitly calls `register_dirty`; simple and transparent but easy to omit. **Object registration** has entity methods notify the UoW; reliable but couples domain objects to persistence. **Snapshot comparison** stores original mapped values and diffs at flush; persistence-ignorant but costs memory/scan and must understand mutable values. **Instrumentation/proxies** intercept writes; efficient but add runtime/tooling semantics.

Many systems mix methods. State which properties/collections are tracked, how value equality works, whether in-place mutation is noticed, and how direct SQL or reflection affects snapshots.

### Keep original and current state distinct

Original snapshot/version supports dirty detection, minimal updates, audit, and optimistic predicates. Current object state expresses intended post-state. Do not overwrite the original snapshot before a successful flush/refresh.

Mutable collection/value aliases can corrupt snapshots if both point to the same object. Copy structurally or use immutable values. Sensitive originals in memory/logs require protection and lifetime bounds.

### Build a dependency graph

Insert parents before children when generated keys/references require it; delete children before parents; update foreign keys/null relationships at defined points. Model nodes as persistence actions and edges as “must precede.” Topologically sort when acyclic.

Cycles require assigned keys, nullable two-stage updates, deferrable constraints supported by the engine, association tables, or model redesign. Do not disable constraints and hope. Cascades must be explicit about ownership and deletion breadth.

### Batch without changing semantics

Group compatible statements/prepared plans while preserving dependencies and per-row optimistic outcomes. Batch size balances round trips against parameter/memory/lock/log limits. Generated keys and mixed statement shapes can constrain batching.

Bulk speed is not evidence of correctness. Record affected counts and map each guarded action/result; a batch failure may report limited detail depending on driver. Test actual driver/engine behavior.

### Understand flush

Flush translates pending state to database operations in the current transaction. It may occur explicitly, before commit, or automatically before a query whose result depends on pending changes. Flush can allocate keys, run constraints/triggers, and fail.

Flush is not necessarily commit. Other transactions may not see changes; rollback can still abort them. Conversely, an engine/framework may issue early inserts for key generation. Know the concrete mode rather than assuming “writes happen at commit.”

### Understand commit and acknowledgment

Commit first flushes as required, then asks the transaction manager to commit. Success moves snapshots/versions to the committed state or expires objects under framework policy. A connection loss during commit can leave the caller uncertain whether the database committed.

Use operation/idempotency identity and recovery queries for unknown outcomes. Do not retry the same mutation blindly. Commit acknowledgment still does not imply replicas, broker consumers, or external effects completed.

### Handle rollback and failed state

Rollback undoes database transaction changes, subject to engine/resource semantics. It does not reverse mutations already made to objects, emails sent, files written, sequence numbers consumed, or logs emitted. After failure, expire/refresh/discard the UoW; safest is often close and retry the whole operation with a fresh context.

Do not catch a flush exception and continue using a failed transaction. Define cleanup for newly assigned generated IDs, domain events, cached calculations, and references returned to callers.

### Apply optimistic concurrency

Store original version \(v\). Flush an update using identity and version predicate, set \(v'=v+1\), and require exactly one affected row. Zero means stale/not-found/unauthorized depending on prior scoped lookup and disclosure; classify carefully. More than one violates key assumptions.

On conflict, rollback/discard and return a typed conflict or reload/re-run the entire safe operation. Automatic field merge is valid only for explicitly commutative independent changes, not arbitrary domain transitions.

### Use pessimistic locks and isolation where needed

Optimistic versions protect rows represented by the token, not predicate invariants or new matching rows. For allocation, uniqueness, or cross-row rules, use constraints, conditional statements, locks, or serializable isolation matched to the anomaly.

Acquire locks in stable order, keep scope short, propagate deadline, and handle deadlock/timeout. An identity map cannot substitute for a database lock.

### Define repository participation

Repositories load/register through the current UoW and never commit. `add` means register new; `get` consults identity map; `discard` can mark removal; queries materialize managed or explicit read-only/detached projections. Do not let each repository create its own session.

Queries used only for reporting may bypass tracking for performance. Mark results read-only and do not later assume mutations persist.

### Treat generated values and triggers as state changes

Keys, versions, timestamps, computed columns, and trigger changes may be returned by statements or require refresh. Decide which layer is authoritative. After flush/commit, synchronize values before exposing results or events that depend on them.

Hidden trigger changes can make managed objects stale inside the same transaction. Prefer explicit behavior for important domain rules; when triggers are necessary, document refresh and testing.

### Control cascades and orphan behavior

Persistence cascade is a storage graph policy, not automatically a domain ownership rule. Specify cascade for insert/update/delete/merge/detach and orphan removal narrowly. A root delete should not traverse shared references and erase unrelated data.

Review generated action counts and database `ON DELETE` behavior together. Duplicate application/database cascades can produce surprises.

### Integrate an outbox

Collect domain events/facts during behavior, but persist outbox records as part of the same UoW transaction after identities/versions needed by the event are known. Clear/publish pending events only according to durable semantics.

A relay publishes later and may duplicate. Do not perform network publication in flush callbacks; retries/rollback can duplicate or publish facts that never commit.

### Handle bulk/native writes

Set-based SQL may bypass identity map, dirty checking, versions, callbacks, and cascades. Before use, define whether the UoW is empty, whether affected managed instances will be expired/refreshed, how versions increment, and how events/audit are generated.

Never mix a bulk update with stale managed objects and then flush them blindly. Separate scopes or clear/expire after bulk work. Test engine-specific affected-row semantics.

### Define nested scopes

When operation A calls B, default to one shared UoW owned by the outer application operation. A nested helper must not commit. A savepoint can partially roll back database statements but does not automatically rewind objects, events, or external effects.

An intentionally independent transaction requires a named semantic boundary and consequences if outer work fails. Avoid “requires new” hidden inside repositories or audit helpers; it creates outcomes reviewers cannot infer from call structure.

### Avoid conversation-long transactions

Do not keep UoW/database transactions open while a user edits a form, waits for approval, or a remote system responds. Persist a versioned draft/workflow state, detach/close, and later start a fresh UoW with expected versions and authorization.

An extended persistence context without an open DB transaction still accumulates stale/detached merge complexity. Prefer explicit conversation state.

### Observe Unit of Work behavior

Record UoW/operation identity, duration, managed/new/dirty/deleted counts, flush count/time, statement/batch count, rows, lock wait, deadlock/serialization/version conflict, rollback cause, identity-map size, lazy queries, outbox count, and commit uncertainty. Bound labels and avoid entity payload leakage.

Detect huge scopes, query-per-entity, repeated autoflush, unexpected delete cascade, dirty-with-no-effective-change, and contexts used after failure.

### Test with real persistence

Unit-test explicit state transitions and ordering planner, but integration-test mappings and the supported database/driver/ORM version: identity uniqueness, dirty mutable values, cascades, constraints, generated fields, flush timing, query autoflush, rollback object policy, version races, nested/savepoint behavior, bulk bypass, connection loss, and outbox.

Coordinate concurrent transactions deterministically. Fault-inject before/during/after flush and commit acknowledgment. Inspect SQL/action plans and assert no partial durable state after rollback.

## Definitions and Notation

Let identity map \(M:K\rightharpoonup O\) be a partial function from persistence key \(K\) to managed object instance \(O\). Thus

\[
M(k)=o_1\land M(k)=o_2\Rightarrow o_1=o_2.
\]

Let disjoint pending identity sets be \(N,D,X\subseteq K\), with \(N\cap D=N\cap X=D\cap X=\varnothing\) after normalization. A write plan \(W=\tau(N,D,X,G)\) is a topological order over dependency graph \(G=(V,E)\); an order exists if the required action graph is acyclic or cycles are resolved by the persistence strategy.

For dirty object key \(k\), original version \(v_k\), and current persistent projection \(p(o_k)\), guarded update is conceptually

\[
\mathrm{UPDATE}(k,v_k,p(o_k))\Rightarrow
\begin{cases}
1\text{ row},&v_k\text{ still current},\\
0\text{ rows},&\text{stale/missing under scope}.
\end{cases}
\]

## Mechanisms, Invariants, or Proof Structure

### Unit of Work procedure

1. Begin one short scope/transaction for a canonical application operation; make ownership and deadline explicit.
2. Route all tracked loads through one tenant-aware identity map and capture original snapshots/versions.
3. Register/detect new, dirty, and deleted state with coherent transitions and no duplicate representations.
4. Normalize changes, validate domain/persistence premises, and build a constraint/dependency write graph.
5. Flush guarded, parameterized, ordered/batched actions; interpret every affected-row/constraint result.
6. Persist generated values, audit, idempotency, and outbox facts in the same local transaction as required.
7. Commit once; on conflict/failure/uncertainty, rollback and expire/discard/recover rather than reuse poisoned state.
8. Keep remote effects and long conversations outside; model workflows and outcome recovery explicitly.
9. Synchronize or separate bulk/native/trigger changes from managed state.
10. Measure scope/action behavior and test real mapping, engine, concurrency, and fault boundaries.

### Executable finite model

The finite model implements an identity map, original versions, explicit dirty registration, preflight optimistic checks, and copied-state atomic replacement. It demonstrates one successful two-object transfer and one stale conflict with no balance write. It is serialized memory—not a database, dependency planner, rollback-capable object graph, thread-safe session, or distributed coordinator.

<!-- bijux-verify: {"id":"unit-of-work-accounts","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"same_A=True dirty=2\ncommit=committed A=700@4 B=800@9 writes=2\nconflict=conflict A=700@5 writes=0\n","stderr":""}} -->
```python
class Account:
    def __init__(self, account_id, balance_cents, version):
        self.account_id = account_id
        self.balance_cents = balance_cents
        self.version = version

    def debit(self, amount_cents):
        if amount_cents <= 0 or self.balance_cents < amount_cents:
            return False
        self.balance_cents -= amount_cents
        return True

    def credit(self, amount_cents):
        self.balance_cents += amount_cents


class UnitOfWork:
    def __init__(self, store):
        self.store = store
        self.identity_map = {}
        self.original_versions = {}
        self.dirty = {}
        self.writes = 0

    def get(self, account_id):
        if account_id not in self.identity_map:
            row = self.store[account_id]
            account = Account(account_id, row["balance"], row["version"])
            self.identity_map[account_id] = account
            self.original_versions[account_id] = row["version"]
        return self.identity_map[account_id]

    def register_dirty(self, account):
        self.dirty[account.account_id] = account

    def commit(self):
        for account_id in self.dirty:
            expected = self.original_versions[account_id]
            if self.store[account_id]["version"] != expected:
                self.writes = 0
                return "conflict"
        replacement = {key: dict(row) for key, row in self.store.items()}
        for account_id, account in self.dirty.items():
            replacement[account_id] = {
                "balance": account.balance_cents,
                "version": account.version + 1,
            }
        self.writes = len(self.dirty)
        self.store.clear()
        self.store.update(replacement)
        return "committed"


store = {
    "A": {"balance": 1000, "version": 3},
    "B": {"balance": 500, "version": 8},
}
work = UnitOfWork(store)
source = work.get("A")
same_source = work.get("A")
target = work.get("B")
source.debit(300)
target.credit(300)
work.register_dirty(source)
work.register_dirty(target)
print(f"same_A={source is same_source} dirty={len(work.dirty)}")
result = work.commit()
print(f"commit={result} A={store['A']['balance']}@{store['A']['version']} B={store['B']['balance']}@{store['B']['version']} writes={work.writes}")

stale = UnitOfWork(store)
stale_source = stale.get("A")
stale_source.debit(50)
stale.register_dirty(stale_source)
store["A"]["version"] = 5
result = stale.commit()
print(f"conflict={result} A={store['A']['balance']}@{store['A']['version']} writes={stale.writes}")
```

### Finite invariant argument

**Identity.** `get("A")` inserts one `Account` under key A; the second call returns that exact object, so the scoped identity property holds.

**Successful transfer.** Both original versions match. Replacement is built separately; A becomes 700/version 4 and B 800/version 9, then replaces the store. Nonnegativity and total 1500 are preserved, with two writes.

**Conflict.** The stale UoW captured A version 4; external state advances to 5. Preflight detects mismatch before replacement construction/application, returns conflict, and reports zero writes; balance remains 700.

The proof covers this finite serialized implementation only. Real multi-statement preflight can race after checking; production must place guarded updates inside one transaction and roll back if any affects zero rows. The public mutable objects/store, `clear`/`update` replacement, lack of new/delete/dependencies, and lack of failure injection are explicit limitations.

### Evidence classification

The snippet report is empirical evidence for this trace. Identity, arithmetic, version progression, and case behavior can be independently recomputed. The argument is not evidence for real atomicity, isolation, durability, mapping, driver errors, thread safety, or external correctness.

## Alternatives and Trade-Offs

| Approach | Change timing | Strength | Main risk |
|---|---|---|---|
| Immediate write | Each repository/entity call | Simple explicit persistence | Chatty I/O and partial operation |
| Explicit UoW registration | Deferred registered actions | Visible intent and batching | Omitted registration |
| Snapshot dirty checking | Diff at flush | Persistence-ignorant domain | Memory/scan and mutable-alias complexity |
| Instrumented tracking | Intercept changes | Efficient change detection | Runtime/tool coupling |
| Immutable command/set update | Explicit SQL transformation | Clear set behavior/no managed graph | Rich object collaboration absent |
| Event sourcing | Append facts | History/replay | Ordering/schema/privacy/operational cost |
| Distributed transaction | Multiple transactional resources | Atomicity under supported protocol | Availability, blocking, operational coupling |
| Saga/workflow | Multiple local transactions | Long-running recovery | Intermediate states and compensation |

Unit of Work composes with Domain Model, Data Mapper, Repository, Identity Map, and Service Layer. It is not mandatory for simple single-statement scripts or set operations whose database statement already is the complete change set.

## Failure Modes and Misconceptions

- **“Unit of Work is the database transaction.”** It tracks/co-ordinates objects; the database transaction supplies actual atomic/isolation behavior.
- **“Session per application is efficient.”** Long-lived contexts leak memory and return stale state; most are not concurrency-safe.
- **“Flush means committed.”** Flush writes within a transaction and may be rolled back.
- **“Rollback restores objects.”** Database state may revert while object fields/events remain mutated.
- **“One object per key globally.”** Identity uniqueness is scoped; other transactions have other representations.
- **“Dirty checking sees every mutation.”** Mutable aliases, custom types, native SQL, and instrumentation gaps can escape it.
- **“Source mutation order equals SQL order.”** Dependency planners often reorder actions.
- **“Cascade is aggregate ownership.”** Persistence graph policy can over-delete shared data.
- **“Optimistic locking merges changes.”** It detects a conflict; semantic resolution is separate.
- **“Preflight version select prevents races.”** The guarded write/transaction must enforce the version at mutation.
- **“Savepoint rewinds the object graph.”** It only governs database transaction state unless memory is reconciled.
- **“Bulk ORM update behaves like managed changes.”** It may bypass identity maps, events, versions, and callbacks.
- **“Retry the same failed session.”** Failed contexts can be poisoned/stale; use rollback/disposal and fresh state.
- **“Open a transaction across the approval UI.”** User think time requires versioned conversation/workflow state.
- **“One UoW commits two services atomically.”** Local object tracking cannot erase distributed partial failure.

## Worked Examples

### Example 1

**Situation.** Two repositories load customer key 7 into separate objects; one changes address, the other credit state.

**Reasoning.** Independent instances can overwrite each other or violate invariants. Both repositories must consult the same tenant/type/key identity map and return one managed instance; concurrent external transactions still require versioning.

**Conclusion.** Identity Map coherence is necessary inside a UoW but insufficient across transactions.

### Example 2

**Situation.** An in-place list element changes, but snapshot and object share the same list reference.

**Reasoning.** Both appear equal after mutation, so dirty checking misses it. Use immutable value collections, structural snapshot copies, collection instrumentation, or explicit registration; test custom value equality.

**Conclusion.** Dirty checking depends on snapshot and mutation semantics, not magic observation.

### Example 3

**Situation.** A new order and lines flush with child inserts before the database-generated order key exists.

**Reasoning.** Dependency graph requires parent insert/key return before children, or assigned keys. Build/topologically order actions; preserve batching where compatible. A cycle needs a declared persistence strategy.

**Conclusion.** UoW write order follows constraints, not object mutation sequence.

### Example 4

**Situation.** A query unexpectedly causes a unique-constraint error before explicit commit.

**Reasoning.** Autoflush synchronized pending insert so the query could see consistent state. The constraint fires during flush. Control scope/mode carefully, but do not disable flush globally and accept inconsistent reads.

**Conclusion.** Flush timing is observable correctness behavior and must be understood/tested.

### Example 5

**Situation.** Flush succeeds, an email is sent, then commit fails.

**Reasoning.** Flush was not durable completion; email cannot roll back. Store an outbox intent in the transaction, commit, then relay idempotently. A commit-ack loss is recovered by operation identity.

**Conclusion.** External effects must not be triggered from precommit/flush success.

### Example 6

**Situation.** Two UoWs load product version 12 and change price; both flush unconditional updates.

**Reasoning.** Last writer silently wins. Use `WHERE id=? AND version=12`, increment version, require one row. Loser rolls back/discards and returns conflict or re-runs with fresh business decision.

**Conclusion.** Original versions turn stale overwrite into explicit conflict.

### Example 7

**Situation.** Database rollback occurs after a domain object appended an event and changed status.

**Reasoning.** The object remains mutated even though rows did not commit. Discard/expire the UoW and its pending events; do not return the object as committed. Retry with a fresh context if safe.

**Conclusion.** Rollback requires an explicit post-failure in-memory policy.

### Example 8

**Situation.** Native SQL closes 1000 accounts while 20 are managed in the identity map.

**Reasoning.** Managed instances remain open and may overwrite changes on later flush. Execute bulk work in a separate empty scope, or expire/refresh affected identities and increment/check versions/events deliberately.

**Conclusion.** Bulk/native paths must synchronize or isolate from tracked state.

### Example 9

**Situation.** A nested audit repository commits independently so audit survives even when the business operation fails.

**Reasoning.** This may record an action that never committed and hides a second boundary. If attempted-action audit must survive, give it a named independent security protocol with correlation and semantics; otherwise join the main UoW/outbox.

**Conclusion.** Independent transactions require explicit durable meaning, not helper convenience.

### Example 10

**Situation.** A clinical edit session keeps one persistence context open for hours until a physician signs.

**Reasoning.** State/authorization/evidence become stale and locks/resources are unsafe. Persist a versioned draft, close, then on signing use a fresh UoW, reload current facts, reauthorize significant data, check expected versions, and retain auditable conflict/override paths.

**Conclusion.** Long conversations need explicit workflow/versioning, not a long-lived Unit of Work.

## Cross-Program Connections

- [Database Engineering](../../18-database-engineering/ROADMAP.md) develops transactions, isolation, locks, constraints, recovery, and query execution.
- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) supplies transaction ownership and persistence-boundary design.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) explains why local commit cannot coordinate remote effects and how workflows recover.
- [Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) provides integration, concurrency, model-based, and fault-injection evidence.
- [SEPAT-054](054-service-layer.md) owns UoW lifetime; [SEPAT-056](../ROADMAP.md) isolates the identity uniqueness mechanism used inside it.

## References

1. Martin Fowler, [“Unit of Work”](https://martinfowler.com/eaaCatalog/unitOfWork.html), *Patterns of Enterprise Application Architecture* catalog, 2003.
2. Martin Fowler, *Patterns of Enterprise Application Architecture*, Addison-Wesley, 2002. Unit of Work, Identity Map, Data Mapper, Repository, and related patterns.
3. Martin Fowler, [“Identity Map”](https://martinfowler.com/eaaCatalog/identityMap.html), 2003.
4. Jim Gray and Andreas Reuter, *Transaction Processing: Concepts and Techniques*, Morgan Kaufmann, 1992.
5. Martin Kleppmann, *Designing Data-Intensive Applications*, O’Reilly, 2017. Transactions, concurrency, logs, and distributed limits.
6. SQLAlchemy Project, [“Using the Session”](https://docs.sqlalchemy.org/en/21/orm/session.html), SQLAlchemy 2.1 documentation, accessed 2026-08-28. Concrete session/UoW, flush, identity, rollback, and lifecycle semantics.
7. Hibernate ORM, [*Hibernate ORM User Guide*](https://docs.jboss.org/hibernate/orm/current/userguide/html_single/Hibernate_User_Guide.html), current documentation accessed 2026-08-28. Persistence contexts, dirty checking, flushing, action ordering, and optimistic versions.
8. PostgreSQL Global Development Group, [“Concurrency Control”](https://www.postgresql.org/docs/current/mvcc.html), current documentation accessed 2026-08-28. Concrete isolation/locking behavior; other engines differ.
9. Phillip A. Bernstein, Vassos Hadzilacos, and Nathan Goodman, *Concurrency Control and Recovery in Database Systems*, Addison-Wesley, 1987.
10. Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software*, Addison-Wesley, 2004. Aggregates, repositories, and transaction boundary guidance.

## Exercises

### Exercise 1

Trace the executable UoW if the first transfer attempts 1100 cents, then A and B are still registered dirty and commit is called. State the result/state and identify the missing application/domain safeguard.

### Exercise 2

Define a state-transition table for transient, managed-clean, dirty, removed, and detached objects. Include new-then-removed, dirty-then-rollback, detach/reattach, generated identity, and illegal transitions.

### Exercise 3

Given new `Order`, two `Line` children, existing `Customer`, and deletion of an old `Line`, construct a persistence action dependency graph and write order. Explain generated versus assigned keys, batching, cycles, versions, and failure behavior.

### Exercise 4

Diagnose a web application using one global ORM session, repository commits, autoflush, native bulk updates, and retries after exceptions. Propose an incremental remediation and verification plan.

### Exercise 5

Design a high-stakes UoW boundary for approving and publishing a regulated laboratory result. Include identity, versions, authorization, generated/audit values, outbox, commit uncertainty, rollback object policy, long conversation, retries, bulk correction, tests, and human review.

## Answers to the Exercises

### Answer 1

`source.debit(1100)` returns `False` and leaves A=1000; the sample caller ignores that boolean, credits B by 1100, registers both dirty, and commits because versions match. Store becomes A=1000/version 4 and B=1600/version 9, total 2600: persistence atomicity faithfully commits a domain-invalid change.

The application service must stop on debit rejection and not credit/register/commit; better, a domain transfer policy/coordinator should return one typed transition result so partial intent cannot be assembled incorrectly. UoW guarantees coherent persistence of the supplied change set, not correctness of that set. Add invariant/property tests for conservation and rejection with zero dirty writes.

### Answer 2

Transient may become managed-new through `add`, or disappear without persistence. Managed-new becomes managed-clean after successful insert/flush/commit with generated identity/version; new then removed before flush normalizes to no action (unless external references/events require rejection). Loaded managed-clean becomes dirty on tracked persistent change, removed on explicit deletion, or detached on close/clear.

Dirty becomes clean after successful flush plus committed snapshot policy, removed if deletion supersedes update, or remains mutated but invalid/expired after rollback; do not call it restored. Removed becomes detached after committed delete/close; modification or re-add is illegal unless a named restore workflow exists. Detached may be reloaded and changes reapplied, or merged under identity/version/conflict rules; directly attaching a second representation when the key is already managed is illegal. Generated identity is provisional until returned and must be cleared/treated carefully after failure. Every failed flush transitions the UoW to rollback-required/closed, not normal managed state.

### Answer 3

Actions: insert `Order` (O), insert lines L1/L2 referencing O, update/validate existing Customer if actually changed (C), and delete old line L0. Edges O→L1 and O→L2 when O's generated key is required; L0 delete must precede Order delete only if the order were deleted, which it is not. Customer need not be updated merely because referenced; any order customer FK requires existing C, already satisfied. A valid order is O, then batch L1/L2, with L0 delete positioned anywhere constraints/triggers permit; deterministic planners may group deletes/updates/inserts differently.

Assigned UUID/key removes the key-generation dependency but FK existence still matters. Generated keys may require return before child binding and reduce batch options. A bidirectional non-null cycle requires assigned IDs, association indirection, deferrable constraints, two-stage nullable update, or redesign. Existing dirty records use guarded versions; any zero-row conflict or constraint failure aborts the entire transaction and the UoW is discarded. Test exact supported engine/ORM ordering rather than relying on source call order.

### Answer 4

The global session is stale, unbounded, and concurrency-unsafe; repository commits fragment operations; autoflush exposes unintended early errors; native updates desynchronize objects; retrying failed sessions reuses poisoned state. First instrument session identity/lifetime, commit callers, flush/query counts, identity-map size, native paths, exceptions, and transactions; characterize critical behavior with integration tests.

Introduce one fresh UoW per canonical application operation, owned by Service Layer. Change repositories to join it and remove commits one use case at a time. Make transaction scopes explicit and understand/locally control autoflush without globally disabling correctness. Move bulk SQL to separate scopes or add version increment plus expire/refresh. On any flush/commit error, roll back, close/discard, and retry only the entire safe operation with fresh state and bounded policy.

Add optimistic versions/constraints, outbox, and typed conflicts. Test two concurrent writers, duplicate identity, rollback object behavior, native/bulk then managed access, nested calls, generated values, constraint order, commit-ack loss, and no partial durable writes. Use staged routing/telemetry and remove the global access path after all callers migrate.

### Answer 5

The edit conversation stores a versioned draft and closes; it never holds a transaction while clinicians deliberate. At approval, a fresh UoW has tenant/patient/result-aware identity keys and one managed result representation. Trusted context binds authenticated reviewer, significant result/patient data, action, policy, authoritative time, expected version, and authorization expiry. Domain behavior validates verified/corrected/withheld states and review policy.

One transaction conditionally updates expected result/version, obtains database-generated recorded time/version, appends immutable protected audit/correction lineage, stores idempotency outcome, and inserts privacy-minimized outbox intent. Refresh returned/generated values before forming response/event. Commit-ack loss is resolved by operation identity; conflicts/retryable database failures discard the UoW and re-run only after reloading/re-authorizing. Rollback discards/expirs mutated objects/events—never returns them as released.

Notification/publishing is an outbox-driven idempotent workflow with delay/duplicate/unknown outcome, access-controlled payload, escalation, and reconciliation. Bulk corrections run in isolated bounded scopes with versions, captured membership, audit/events, pause/recovery, and managed-context expiry. Tests cover identity duplication, stale versions, authorization matrix, corrected/withheld/critical results, generated fields, flush/commit faults, rollback memory policy, outbox atomicity, duplicate relay, bulk races, and privacy. Named laboratory medicine, clinical safety, privacy/legal/regulatory, security, human-factors/accessibility, database/SRE, and operations reviewers approve real rules and workflow; automated evidence alone is insufficient.
