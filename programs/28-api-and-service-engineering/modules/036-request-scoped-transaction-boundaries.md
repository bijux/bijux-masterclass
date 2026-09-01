---
module_id: API-036
program: API & Service Engineering
level: 1
module_number: 36
title: Request-Scoped Transaction Boundaries
status: complete
last_verified: 2026-09-01
---

# Request-Scoped Transaction Boundaries

## One-Page Review

### Governing question

Where should a service begin, commit, and end a local transaction so one request's authoritative reads, decisions, writes, and durable follow-up intent form one coherent state change without holding scarce locks across remote work or response delivery?

### Essential definitions

- A **database transaction** groups local operations into one commit or rollback under declared isolation.
- A **transaction boundary** is the owned interval between beginning a transaction and its terminal commit or rollback.
- A **unit of work** tracks changes and coordinates their persistence and concurrency handling for one business operation.
- **isolation** constrains which concurrent histories and observations a transaction may experience.
- A **commit point** is the instant after which the local durable effect is authoritative even if the client has not received a response.
- An **outbox record** stores durable publication intent in the same transaction as the business change.
- An **ambiguous outcome** occurs when the caller cannot know from transport success whether the transaction committed.

### Central model, mechanism, or theorem

For one local store, let $R$ be authoritative reads, $D$ domain decisions, $W$ business writes, and $E$ durable outbox/audit intent. A useful request transaction is

$$
B=\operatorname{begin};R;D;W;E;\operatorname{commit}.
$$

Its invariant is all-or-nothing local visibility: a successful commit makes the valid combined state visible; rollback makes none of $W$ or $E$ visible. Parsing, response serialization, unbounded computation, and ordinary remote calls lie outside $B$ unless a specific correctness proof and technology justify otherwise. A database commit cannot atomically include an HTTP response or an unrelated service.

### Critical invariants

The application use case owns the transaction, not generic route middleware. All repositories participating in one local atomic change share the same transaction context. Required invariants are rechecked or enforced inside the boundary. Isolation and conflict behavior are explicit. No response is declared successful before commit. No event describing a rolled-back change is published. External calls are not made while holding local locks unless the design accepts and bounds that risk. Every exit commits exactly once or rolls back, releases the connection, and preserves cancellation and failure evidence. Post-commit response loss is treated as ambiguity, not rollback.

### Common failures

Opening a transaction for the entire HTTP pipeline; allowing each repository to start and commit independently; reading before the transaction then assuming the value is protected; calling payment, email, or policy services while locks are held; publishing before commit; publishing only in an in-memory after-commit callback; returning `200` before commit completes; treating client disconnect as proof of rollback; using a long-lived ORM session across requests; retrying a serialization failure without replay-safe inputs; swallowing a commit error; leaking an aborted connection to the pool; and assuming “transactional” means multiple services committed atomically.

### Compact example

`POST /transfers` validates its representation and authentication before beginning a database transaction. Inside, it loads both accounts with the chosen concurrency control, checks currency and funds, writes both balances, inserts the transfer and an outbox event, then commits. Only afterward does it build the success response; a relay publishes the event. If the response connection breaks after commit, the transfer remains committed and the client reconciles through its operation or idempotency identity. **Conclusion:** the boundary protects one local business effect, not the network conversation.

### Connections

[Transport, Application, and Domain Boundaries](031-transport-application-and-domain-boundaries.md) assigns ownership to the use case, and [Error Translation](035-error-translation.md) maps rollback, conflict, commit, and ambiguity outcomes. [Idempotency Keys](../ROADMAP.md) next makes safe reconciliation and replay concrete; later concurrency and distributed-workflow modules refine isolation and cross-service effects.

## Governing Question

Which data, decisions, locks, isolation level, timeout, retries, outbox records, commit ordering, and response behavior belong to one request-triggered local transaction, and which work must remain outside it?

## Why This Matters

A request can make several local facts true together: reserve inventory, create an order, record a ledger entry, advance a version, and schedule an event. If separate commits expose only part of that change, later requests observe states the domain declared impossible. If an event publishes before the database commit, another service can act on a change that later rolls back. If it publishes only from memory after commit, a crash can hide a committed change forever.

Making the transaction too broad is also dangerous. Database transactions consume connections, retain row versions, and may hold locks. A remote call inside the boundary turns another system's latency and outage into local contention. A streamed response can last minutes. User think time can last hours. Wrapping these in one transaction reduces throughput and raises deadlock, timeout, vacuum/cleanup, and cascading-failure risk.

“One transaction per request” is therefore a design heuristic, not middleware magic. The correct unit is one local business operation with a coherent atomicity requirement. Some read-only requests need no explicit transaction; some commands require one; one request may intentionally initiate several independently observable operations; one business workflow may span many requests and cannot hold a database transaction between them.

The response boundary creates a final subtlety. Commit can succeed and the connection can fail before the client sees success. The database cannot retract a correct commit merely because a socket broke. The API must expose operation identity, idempotency, or reconciliation rather than equating response delivery with transactional outcome.

## Prerequisites and Retrieval

Retrieve ACID properties; transaction begin, commit, rollback, savepoints, and connection pooling; database isolation and anomalies; row/version locking; optimistic concurrency; domain invariants; application/use-case boundaries; deadlines and cancellation; HTTP method and response semantics; idempotency; event delivery; transactional outbox and change data capture; audit; and distributed workflow patterns.

Before designing the boundary, retrieve the authoritative store, aggregate and invariant set, read/write set, legal concurrent histories, database isolation semantics, expected contention, lock order, retryable database errors, request deadline, pool capacity, maximum transaction time, remote dependencies, event/audit requirements, commit acknowledgement behavior, response streaming, idempotency/reconciliation identity, and ownership of post-commit work.

## Learning Objectives

By the end of this module, you should be able to:

1. distinguish an HTTP request, business operation, unit of work, and database transaction;
2. place begin and commit around the smallest complete local invariant boundary;
3. select isolation, locking, deadlines, and retries from correctness needs;
4. coordinate repositories, outbox records, and audit in one local commit;
5. keep remote, streaming, and post-commit work outside scarce transaction scope;
6. reason about cancellation, commit failure, and post-commit response ambiguity; and
7. test transaction ownership, rollback, concurrency, resource release, and recovery.

## Core Exposition

### Separate the four lifetimes

Four lifetimes often overlap but are not identical:

- the **HTTP exchange**, from request arrival through response completion;
- the **application operation**, from accepted command through an owned outcome;
- the **unit of work**, tracking local reads and changes relevant to that operation; and
- the **database transaction**, from begin through commit or rollback on one transactional resource.

Do not make their scopes identical by default. Parsing a large body does not need a row lock. Authentication token verification often needs no database transaction. Response compression and streaming occur after the authoritative state has been chosen. Conversely, a domain operation may be invoked by HTTP, a queue consumer, or a scheduled job and should preserve the same transaction semantics in every adapter.

Put transaction orchestration at the application boundary that knows the complete local effect. Transport supplies a validated command and cancellation/deadline context. The use case begins a unit of work, loads through transaction-aware ports, makes domain decisions, persists changes and durable follow-up intent, commits, and returns an outcome. The HTTP adapter then serializes that outcome.

Generic transaction middleware can work only when every matched route has the same lifecycle and no handler begins streaming or escapes work. Even then, it must commit before success headers/body are irreversibly sent. Application-owned orchestration is easier to review because command semantics determine the boundary.

### Define one atomic local effect

List facts that must become visible together. For an order this might be:

- order row and initial version;
- inventory reservation owned by the same database;
- payment-intent record, but not the external charge;
- idempotency record;
- audit fact required for the mutation; and
- outbox event describing the committed state.

If failure after any subset would violate a local invariant, include that subset in the same supported transaction. If two repositories silently use different connections or stores, no single local commit exists. Make the unit-of-work/transaction handle an explicit dependency or propagate it through a narrowly controlled execution context.

Do not expand “atomic” across resources by naming it so. A database and broker, two independent databases, or a database and payment provider need a distributed protocol or workflow. In many services, local business state plus outbox intent commit together; a relay later publishes at least once, and consumers handle duplicates. This removes the database/broker dual-write gap without pretending publication occurs in the original local commit.

### Begin after cheap boundary work

Perform bounded transport work before acquiring a transaction when it cannot change authoritative state:

- method, media type, content length, and representation parsing;
- structural validation and normalization;
- cryptographic authentication whose evidence is request-contained;
- coarse rate and function checks that need no protected current data; and
- command construction.

Do not move correctness-critical reads outside merely to shorten the transaction. Tenant membership, authorization relationships, current balance, uniqueness, version, or state transition may change concurrently. If the decision must cover the effect, read it inside the appropriate isolation boundary or bind the write to a version/predicate that proves the assumption still holds.

Duplicate cheap validation inside a database constraint when it protects shared state. A preflight uniqueness query improves messages but cannot replace a unique constraint; another request can insert between query and write.

### Share one transaction across repositories

Repositories within one unit of work must not auto-commit independently. A transfer repository, account repository, audit repository, and outbox repository need the same local transaction and connection when their changes are one atomic effect.

Useful designs include:

- an explicit `UnitOfWork` passed to application ports;
- repositories created from a transaction-scoped factory;
- a transaction context accessed through safe structured execution scope; or
- a database session owned by the application operation.

Explicit passing makes dependencies visible but can add plumbing. Ambient context reduces signatures but can disappear across threads/tasks, leak into nested operations, or make tests deceptive. If using ambient context, define propagation and prohibition rules and fail when a repository expected a transaction but has none.

Nested service calls should normally join the existing unit rather than commit independently. True nested database transactions are uncommon; many frameworks implement nesting with savepoints. A savepoint can roll back part of the work, but it does not make that part durable before the outer commit and does not release every kind of resource uniformly. Use it only when partial recovery is a declared operation semantic.

### Choose isolation from the invariant

Atomicity alone does not protect decisions from concurrent transactions. Isolation determines allowed observations and conflicts. Product names and nominal levels are insufficient; database implementations differ.

Under a common `READ COMMITTED` model, two statements in one transaction can observe different committed snapshots. It can be correct for a guarded single-row update but unsafe for a multi-query invariant such as “at most one active assignment across these rows.” Stronger snapshot or serializable isolation can prevent more anomalies, but may abort transactions that must be retried.

Choose one or combine:

- **database constraints** for uniqueness, foreign keys, and checkable invariants;
- **atomic conditional statements** such as decrement only when balance is sufficient;
- **optimistic version checks** that reject stale writes;
- **row or advisory locks** with documented ownership and order;
- **repeatable snapshot** when a stable view is required; and
- **serializable isolation** when accepted histories must correspond to a serial order.

Serializable does not mean “never fails.” Correct implementations can raise serialization failures under contention. Retry the whole transaction from fresh reads, not only the last statement. Bound attempts by deadline and contention budget, and require that everything inside the replayable closure be free of unprotected external side effects.

### Keep the critical section short and bounded

Transaction duration should cover correctness work, not convenience. Long transactions retain locks or old versions, occupy pool connections, increase conflict windows, and amplify failures.

Set and propagate:

- a request/application deadline;
- a shorter transaction budget;
- database statement and lock-wait timeouts;
- maximum retry count/time;
- bounded rows and batch size; and
- metrics for transaction duration, lock waits, aborts, and pool occupancy.

Acquire locks in a consistent order. For transfers, lock accounts by stable account ID rather than debit-then-credit request order, or opposing transfers can deadlock. Deadlock detection resolves a cycle by aborting work; it does not make unordered locking a sound capacity plan.

Do CPU-heavy computation before begin when its inputs can be safely validated later, or compute a proposal and verify its assumptions inside. Never wait for user interaction inside a database transaction. A business “transaction” such as checkout may span minutes and several requests; model it as durable states and compensating transitions.

### Exclude ordinary remote calls

A call to a payment gateway, email provider, authorization graph, or another service can stall while the local transaction holds locks. It may also perform an irreversible effect that local rollback cannot undo.

Prefer one of these shapes:

1. call remotely before the local transaction only when the remote operation is read-only or creates a separately reconcilable intent, then validate assumptions locally;
2. commit local pending state and outbox command, let a worker call remotely, then record the result in a new transaction;
3. use a documented saga/compensation workflow for multiple committed participants; or
4. use a real distributed transaction protocol only when all resources, operations, availability goals, and operators support it.

Do not publish an event before commit. Do not rely solely on `afterCommit(() => publish())`: process death after commit and before callback loses notification. Insert an outbox row atomically, relay committed rows, give each message stable identity and ordering scope, and make relay and consumers idempotent.

Some remote authorization checks must occur before a protected effect. Avoid assuming they are transaction participants. Retrieve a decision with defined freshness or consistency evidence, then guard local policy-relevant state inside the transaction. If authorization itself changes remotely between check and commit, the policy must define acceptable staleness or a coordinated consistency mechanism.

### Commit before success becomes irreversible

The application must observe commit success before returning a success outcome. Commit can fail because of constraint checks deferred until commit, serialization conflict, deadlock victim selection, connection failure, storage failure, or uncertain acknowledgement.

Do not send a `2xx` header or first streaming bytes while a mutation transaction is still open. Once response bytes are on the wire, replacing success with a correct error may be impossible. For a command producing a large export, commit command state first and stream from a separate read strategy, or expose an asynchronous artifact.

Rollback after a failed commit is cleanup, not evidence that nothing committed when the acknowledgement itself was lost. Some database drivers can distinguish a definitive rejection from unknown commit outcome; preserve that classification. An unknown outcome requires idempotency or reconciliation.

Response serialization can fail after commit. Build and validate a bounded response representation before commit if doing so does not disclose or freeze stale state, but send only after commit. Alternatively return a minimal stable operation reference and allow retrieval. Never attempt to reverse a valid local commit merely because JSON encoding or socket delivery failed.

### Handle cancellation by state, not wish

A client disconnect or cancelled request should stop unnecessary work, but cancellation races commit. There are three materially different cases:

- cancellation before commit begins: abort and roll back;
- cancellation while a cancelable statement runs: request database cancellation, then determine transaction state;
- cancellation during or after commit: do not claim rollback without authoritative result.

Always terminate the transaction in `finally`/structured resource cleanup, return or discard the connection according to driver state, and avoid returning an aborted transaction to the pool. A database may mark the transaction failed until rollback after any statement error.

Server shutdown should stop accepting new work, give bounded in-flight commits a chance to resolve, and record unresolved outcomes. Deadline expiry is an outcome, not permission to abandon an open connection.

### Design read-only and streaming paths separately

A simple point lookup may rely on one statement's implicit transaction and snapshot. A report needing a consistent multi-query snapshot may use an explicit read-only transaction. Read-only is not cost-free: a long snapshot can delay cleanup and consume resources.

Do not keep a transaction open while slowly streaming rows to an untrusted client unless the design explicitly bounds duration, backpressure, snapshot retention, disconnect cleanup, and pool impact. Prefer keyset pagination, a materialized/export artifact, a server-side job, or short chunk transactions with documented consistency semantics.

If a streamed representation must reflect one point-in-time snapshot, create a durable snapshot artifact or use database-specific snapshot export only with a carefully bounded operational contract. “Consistent forever while the client pauses” is not a free API property.

### Scope retries around the whole unit

Retryable local errors include selected serialization failures, deadlock victims, and transient connection acquisition failures. Classification is database- and driver-specific. Constraint violations and domain rejections are normally deterministic under the same command and need correction, not immediate retry.

The retry loop must recreate the transaction, repeat authoritative reads, rerun domain decisions, reconstruct writes/outbox records deterministically, and attempt commit. It must not repeat an email, charge, random public identifier, or irreversible clock-dependent decision unless those values are fixed in the command or protected by idempotency.

Generate stable operation IDs outside the retry closure or deterministically from idempotency context. Treat current time and randomness as explicit inputs when their change would alter business meaning. Emit telemetry per logical operation and per attempt without double-counting the business success.

### Observe and test transaction ownership

Record logical operation ID, transaction attempt, isolation, start/commit/rollback outcome, duration, lock wait, rows affected, conflict category, and ambiguous-commit state. Avoid logging SQL values or personal data without policy. Trace spans should show transaction time and remote calls so a remote span nested inside a lock-holding interval is visible.

Test rollback after each write, commit-time failure, repository exceptions, constraint failure, cancellation at each boundary, serialization retry, deadlock, pool exhaustion, nested application calls, and response serialization failure. Assert both database state and outbox/audit state.

Concurrency tests must orchestrate interleavings rather than merely run two fast requests and hope. Verify invariant preservation under conflicting requests, lock order, retry bounds, and correct `409`/`412` or service outcome. Operational tests ensure no idle transactions, leaked connections, unbounded snapshots, or post-commit callbacks are the sole publication path.

The executable model below demonstrates atomic local business/outbox changes and post-commit response ambiguity. It is an in-memory teaching model, not evidence for database isolation, crash durability, or message delivery.

<!-- bijux-verify: {"id":"local-transaction-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"success=balance:70 outbox:1 result:committed\nrollback=balance:100 outbox:0 result:insufficient\nresponse_lost=balance:70 outbox:1 result:ambiguous_to_client\n","stderr":""}} -->
```python
def transfer(initial_balance, amount, response_lost=False):
    committed = {"balance": initial_balance, "outbox": []}
    working = {"balance": committed["balance"], "outbox": list(committed["outbox"])}
    if working["balance"] < amount:
        return committed, "insufficient"
    working["balance"] -= amount
    working["outbox"].append({"type": "transfer_committed", "amount": amount})
    committed = working
    result = "ambiguous_to_client" if response_lost else "committed"
    return committed, result

for name, balance, amount, lost in [
    ("success", 100, 30, False),
    ("rollback", 100, 130, False),
    ("response_lost", 100, 30, True),
]:
    state, result = transfer(balance, amount, lost)
    print(f"{name}=balance:{state['balance']} outbox:{len(state['outbox'])} result:{result}")
```

## Definitions and Notation

Let $B=[t_b,t_c]$ be a local transaction interval from begin time $t_b$ to terminal commit/rollback time $t_c$. Let $R(B)$ and $W(B)$ be its authoritative read and write sets. Let invariant $I(S)$ classify valid committed store states $S$.

For commit transition $S\xrightarrow{B}S'$, correctness requires $I(S)\land \operatorname{valid}(B,S)\Rightarrow I(S')$. Rollback leaves no visible subset of $W(B)$. Isolation constrains which concurrent transaction history supplies reads and whether a conflicting $B$ may commit.

A **logical operation** is the caller-intended business effect; a **transaction attempt** is one execution that may abort and retry. A **definitive abort** establishes no commit. An **ambiguous commit** lacks authoritative acknowledgement of whether commit occurred. A **dual write** independently writes two resources without an atomic protocol. A **transactional outbox** makes business state and publication intent one local write set, while later delivery remains separate and possibly duplicated.

## Mechanisms, Invariants, or Proof Structure

1. Define the complete local invariant and its authoritative store.
2. Parse and perform safe bounded boundary work before acquiring transactional resources.
3. Begin one application-owned unit of work with explicit deadline and isolation.
4. Perform correctness-critical reads and decisions inside or guard their assumptions at write.
5. Share the same transaction across every repository in the atomic effect.
6. Enforce invariants through domain rules, predicates, versions, locks, and constraints.
7. Write business state, required audit, idempotency state, and outbox intent together.
8. Commit before declaring success; classify definitive failure versus ambiguous acknowledgement.
9. Roll back and release resources on every non-commit path.
10. Perform remote delivery, response streaming, and other post-commit work under separate bounded semantics.

The local atomicity property covers only resources enlisted in the database transaction. The observation that selected tests roll back correctly is evidence about those paths, not proof of crash durability, serializability, distributed atomicity, or absence of every connection leak.

## Alternatives and Trade-Offs

Transaction-per-command provides a clear default and simple reasoning. Highly optimized endpoints may use atomic statements or stored procedures without an explicit application transaction, but still need an owned atomic boundary and outcome mapping.

Application-managed units expose intent and support multiple adapters. Middleware-managed transactions reduce repetition but can begin too early, commit after response start, and accidentally wrap streaming or remote work. Use middleware only under a strict route contract with application-visible semantics.

Pessimistic locks prevent selected concurrent changes but increase blocking and deadlock risk. Optimistic versions avoid waiting but shift conflict handling to retries/users. Serializable isolation gives strong history constraints but can abort more work. Choose from invariant, contention, latency, and database semantics.

One large transaction offers a consistent snapshot and atomic batch, but consumes resources and makes conflicts expensive. Smaller transactions scale better but expose partial progress. If partial progress is legitimate, model it with durable item outcomes; do not accidentally create it by chunking an atomic promise.

Remote call before commit avoids holding locks but can create an orphan remote effect if local commit fails. Remote call after commit avoids rollback conflict but can leave pending local state. Outbox/workflow makes the gap explicit and recoverable at the price of eventual completion, duplicates, and more states.

Synchronous success is convenient when local work is fast and bounded. `202` plus operation resource handles long or multi-service workflows more honestly but adds polling, terminal states, expiry, and cancellation contracts.

## Failure Modes and Misconceptions

- **“One HTTP request equals one transaction.”** The correct boundary is one local atomic business effect.
- **“Middleware can infer the boundary.”** Only operation semantics identify reads, writes, streaming, and remote work.
- **“Every repository can commit itself.”** Independent commits break a shared invariant.
- **“I read it earlier in the request.”** Pre-transaction reads can become stale before the write.
- **“A preflight uniqueness check is enough.”** Concurrent writers require a constraint or atomic predicate.
- **“Atomicity prevents races.”** Isolation, locking, versions, and constraints govern concurrent histories.
- **“Serializable never aborts.”** Serialization failures are a normal correctness mechanism.
- **“Retry the failed statement.”** A new transaction must repeat authoritative reads and decisions.
- **“Savepoint means nested commit.”** Savepoint release is not durability before the outer commit.
- **“Hold locks while calling the provider.”** Remote latency and effects are outside local rollback control.
- **“Publish after commit in memory.”** A crash between commit and callback loses the event.
- **“Outbox gives exactly-once effects.”** Relays and consumers still handle duplicate delivery.
- **“Client disconnect rolls back.”** Commit may already be in progress or complete.
- **“Commit succeeded because the driver returned late.”** Lost acknowledgement can leave ambiguity.
- **“Read-only transactions are free.”** Long snapshots and connections have operational cost.

## Worked Examples

### Example 1

**Situation:** A handler begins a transaction before reading a 20 MB body. **Reasoning:** Parsing holds a connection without protecting state. Enforce size, parse, and structurally validate first; begin at the application operation. **Conclusion:** acquire transactional resources only for correctness work.

### Example 2

**Situation:** Order and audit repositories each auto-commit. **Reasoning:** A crash can leave an order with no required audit or audit for no order. Inject one unit of work and commit both writes together. **Conclusion:** repository convenience cannot split one invariant.

### Example 3

**Situation:** Two requests both observe a free username before either insert. **Reasoning:** The preflight read races. Let a unique constraint arbitrate and translate its typed duplicate outcome; optionally use the query only for early feedback. **Conclusion:** shared-state validation belongs at an atomic enforcement point.

### Example 4

**Situation:** Opposing transfers lock source then destination. **Reasoning:** Each can hold one account and wait for the other. Lock both by canonical account ID, keep work short, and retry bounded deadlock victims. **Conclusion:** deterministic lock ordering is part of the boundary.

### Example 5

**Situation:** A transaction charges a payment provider and later fails its database commit. **Reasoning:** Local rollback cannot uncharge the provider. Record pending payment/outbox intent locally, call outside the transaction, and reconcile/compensate through durable workflow. **Conclusion:** remote effects need workflow semantics, not a wider local transaction.

### Example 6

**Situation:** An event publishes, then the order transaction rolls back. **Reasoning:** Consumers observed nonexistent state. Write order and outbox row together; a relay sees only committed rows and publishes with stable identity. **Conclusion:** durable intent closes the database/broker dual-write gap.

### Example 7

**Situation:** Serialization failure occurs after generating a random shipment label and sending email. **Reasoning:** Replaying the whole transaction duplicates external effects and changes identity. Generate stable operation facts outside, keep email in outbox, and retry only the pure local closure. **Conclusion:** replayability constrains transaction contents.

### Example 8

**Situation:** Commit succeeds, but response serialization fails. **Reasoning:** The order is authoritative and cannot be reported as rolled back. Log the occurrence and let the client retrieve by operation/idempotency identity. **Conclusion:** response production is not part of database atomicity.

### Example 9

**Situation:** A client cancels while commit acknowledgement is pending. **Reasoning:** Cancellation cannot establish state. Preserve an ambiguous outcome, resolve the driver/connection state, and reconcile rather than blindly retry. **Conclusion:** cancellation is temporal evidence, not a rollback theorem.

### Example 10

**Situation:** A report streams for 30 minutes from one read-only snapshot. **Reasoning:** It retains a connection and old versions under slow-client control. Prefer a bounded export job/materialized artifact or paginated reads with declared consistency. **Conclusion:** consistent streaming needs an operational design beyond transaction middleware.

## Cross-Program Connections

[Database Engineering](../../18-database-engineering/ROADMAP.md) supplies isolation, locking, constraints, MVCC, and commit mechanics. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies partial failure, outbox delivery, sagas, idempotency, and ambiguous outcomes. [Software Engineering Patterns](../../11-software-engineering-patterns/ROADMAP.md) supplies Unit of Work and application-boundary patterns. [Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies deterministic concurrency, fault injection, and resource-leak testing. This API module places those mechanisms around one request-triggered local business operation.

## References

1. PostgreSQL Global Development Group, [*Transactions*](https://www.postgresql.org/docs/current/tutorial-transactions.html), PostgreSQL current documentation. Checked 2026-09-01.
2. PostgreSQL Global Development Group, [*Transaction Isolation*](https://www.postgresql.org/docs/current/transaction-iso.html) and [*Explicit Locking*](https://www.postgresql.org/docs/current/explicit-locking.html), PostgreSQL current documentation. Checked 2026-09-01.
3. Martin Fowler, [*Unit of Work*](https://martinfowler.com/eaaCatalog/unitOfWork.html), *Patterns of Enterprise Application Architecture*, 2003.
4. Amazon Web Services, [*Transactional Outbox Pattern*](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html), AWS Prescriptive Guidance. Checked 2026-09-01.
5. R. Fielding, M. Nottingham, and J. Reschke, [*RFC 9110: HTTP Semantics*](https://www.rfc-editor.org/rfc/rfc9110.html), June 2022. Checked 2026-09-01.

## Exercises

### Exercise 1

Draw the transaction boundary for creating an order with local inventory, a required audit record, an external payment provider, an email, and an HTTP response. Classify every operation as before, inside, or after the local transaction.

### Exercise 2

Design a transaction for transferring funds between two local accounts under concurrent opposing transfers. Specify invariant, isolation/locking, order, timeout, conflict outcome, retry, audit, and outbox behavior.

### Exercise 3

Diagnose an ORM service with one session per HTTP request, lazy reads during response serialization, repository auto-commit, remote authorization and email calls inside middleware transaction, and an in-memory after-commit publisher.

### Exercise 4

Reason through cancellation at four points: before begin, during a locked update, during commit, and after commit before the response. State what the server knows and what it may safely tell the client.

### Exercise 5

Design verification for a batch command promised to be atomic across 500 items under serialization conflicts, constraint failure, worker shutdown, response loss, and outbox relay duplication.

## Answers to the Exercises

### Answer 1

Before: enforce body limits, parse and structurally validate, authenticate, construct the command, and optionally create a stable operation/idempotency identity. Inside one local transaction: load authoritative inventory and policy-relevant local state, enforce availability and order invariants, insert the order and reservation, write required audit, store payment-request/outbox and email/outbox intents, then commit. After: call or enqueue payment through the workflow, relay committed events/email, and serialize/send the response. If payment must precede order commitment, create a remotely reconcilable authorization then validate and record it locally; define orphan/expiry handling. The response is never sent as success before commit.

### Answer 2

Invariant: conserved ledger amount, nonnegative balances if policy requires, exactly one transfer identity, and debit/credit/audit/outbox atomicity. Begin with a bounded deadline; lock both accounts in ascending stable ID or use guarded versioned updates under a justified isolation level. Verify currency, authorization-bound versions, and funds; insert immutable transfer/ledger entries, update balances, audit, and outbox, then commit. Constraint or domain rejection is not retried unchanged. Deadlock/serialization victims retry the whole pure local closure with the same operation identity and bounded attempts. Commit ambiguity reconciles by transfer/idempotency identity rather than issuing another logical transfer.

### Answer 3

The session lifetime is too broad and permits database access after operation completion; lazy serialization can fail or hold locks after headers. Auto-commit breaks multi-repository atomicity. Remote authorization/email inflate lock time and introduce effects rollback cannot undo. The callback can lose an event after process crash. Move transaction ownership to each application operation, require transaction-aware repositories, eagerly construct authorized response data, bind remote authorization evidence without treating it as a participant, store email/event intent in an outbox, commit before returning success, and close/rollback the session on every path. Add tests that fail on repository access without the expected unit.

### Answer 4

Before begin, cancellation permits ending with no transaction. During a locked update, request statement cancellation, roll back the now-failed transaction, release/discard the connection correctly, and report cancellation only after a definitive abort. During commit, cancellation does not prove outcome; await authoritative driver status within shutdown policy or mark the result ambiguous and reconcile. After commit, the state is durable even if response delivery stops; record the delivery failure and expose retrieval/idempotency recovery. In no case should a client disconnect be logged or translated as proof that a completed commit was undone.

### Answer 5

First question whether 500 items can meet transaction duration, lock, log, and response budgets; reject or redesign if not. For the atomic contract, insert no visible subset on any failure. Build deterministic barriers to create conflicting interleavings, inject failure after each item and at commit, and assert unchanged state plus no outbox rows after rollback. Retry serialization failures from a fresh transaction with stable input and operation identity; prove no external effect occurs inside attempts. Kill the worker before begin, mid-transaction, during commit, and after commit; reconcile ambiguous outcomes by operation record. Lose the response after commit and verify retrieval returns the one result. Run the outbox relay repeatedly and verify stable message IDs, ordered scope, and idempotent consumer effects. Measure transaction duration, lock waits, pool recovery, and absence of idle/aborted leaked sessions.
