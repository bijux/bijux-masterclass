---
module_id: SEPAT-051
program: Software Engineering: Patterns
level: 2
module_number: 51
title: Transaction Script
status: complete
last_verified: 2026-08-28
---

# Transaction Script

## One-Page Review

### Governing question

How can one application request be implemented as a clear procedural transaction while preserving business invariants, authorization, isolation, idempotency, error semantics, durable messaging, observability, and an evolution path when domain complexity outgrows scripts?

### Essential definitions

- A **Transaction Script** organizes business logic as a procedure where each procedure handles one request/use case.
- A **business transaction** is the application-level unit of intent such as transfer funds or approve an invoice.
- A **database transaction** is the datastore's atomic/isolation boundary; one business transaction may span one or several such boundaries.
- A **script boundary** defines validated input, authorization, database work, result/error, and effects for one use case.
- **isolation level** constrains which concurrent execution anomalies may be observed; it is not simply “transactions are safe.”
- **idempotency key** identifies one logical request so retry does not apply its effects twice.
- A **serialization failure** means the database could not serialize a concurrent transaction and the whole local transaction may need bounded retry.
- A **transactional outbox** stores state change and message intent atomically in one database transaction for later relay.
- A **Domain Model** distributes behavior/invariants among domain objects; it becomes attractive when repeated complex rules make procedural scripts duplicate or diverge.

### Central model, mechanism, or theorem

For pre-state (S), validated authorized request (r) with idempotency identity (k), and one local transaction (T), script computes

\[
T(S,r,k)\to(S',result,outbox')\quad\text{or}\quad(S,error,\varnothing).
\]

Atomic commit means governed state, idempotency record, and outbox intent become visible together or none do. Correctness additionally depends on isolation/locking, constraint enforcement, retry scope, trusted inputs, and domain invariants; procedural order alone proves none of these.

### Critical invariants

- One script implements one named use case and contains no presentation/transport rendering logic.
- Inputs are parsed, bounded, normalized, authenticated/authorized, tenant-scoped, and assigned trusted idempotency identity before effects.
- All local governed writes, idempotency outcome, and outbox/audit intent commit atomically under an isolation/locking strategy matched to the invariant.
- External network/broker/email/payment effects do not occur inside a retriable database transaction without an explicit idempotent protocol.
- Expected domain conflicts, invalid input, authorization denial, not found, retryable concurrency, dependency failure, and internal error remain distinct.
- Transactions are short, acquire resources in consistent order, propagate cancellation/deadline, and retry only the entire safe local unit with bounds/jitter.
- Repeated rules/calculations have one owner; scripts do not drift through copy/paste or bypass database/domain constraints.
- Tests and monitoring cover actual database concurrency, rollback, duplicate requests, outbox relay, recovery, security, and resource limits—not only a happy-path mock.

### Common failures

Common failures include placing the script in an HTTP controller, trusting client tenant/user/price/status fields, one transaction per SQL statement, long remote calls while locks are held, read-then-write lost updates, assuming read committed prevents write skew, retrying after external charge, idempotency lookup outside the transaction, persisting state then publishing directly to a broker, catch-all 500/error swallowing, duplicate rules across endpoints/jobs, unbounded retry/deadlock loops, huge god scripts, dynamic SQL interpolation, sensitive logs, mocks that simulate impossible isolation, and calling a script simple after its state machine spans many services.

### Compact example

An in-memory transfer script validates amount/accounts/balance, uses a request ID, copies transaction state, moves 300 cents from A to B, and appends one outbox intent atomically. Repeating the same request returns duplicate without changing balances/events; an insufficient-funds request leaves state unchanged.

### Connections

[SEPAT-050](050-diagnosing-behavioral-pattern-misuse.md) supplies evidence-driven simplification; [SEPAT-052](../ROADMAP.md) introduces Domain Model for complex logic. Transaction Script connects to [Database Engineering](../../18-database-engineering/ROADMAP.md), [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md), and [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md).

## Governing Question

Is the business operation simple and cohesive enough to read as one procedure, and what exact transaction, isolation, retry, authority, effect, and recovery boundary makes that procedure correct under real failures and concurrency?

Transaction Script is a legitimate domain-logic organization pattern for straightforward applications and services. It is not a synonym for unlayered code, stored procedures, or controllers issuing arbitrary SQL.

## Why This Matters

Many enterprise operations are naturally procedural: validate request, load a few records, calculate, enforce constraints, update, record an event, return. A script keeps this sequence visible and avoids an object model more elaborate than the rules.

The danger is that sequential source code looks atomic even when storage isolation, external effects, retries, and concurrent workers violate its assumptions. Graduate-level use requires reasoning about the real transaction system, not only the function body.

## Prerequisites and Retrieval

You should understand ACID transactions, SQL constraints, isolation anomalies, locks/MVCC, idempotency, outbox, authentication/authorization, retries, and layered architecture. Retrieve these facts:

1. Atomicity does not imply serializability; isolation levels permit different anomalies.
2. A check followed by update can race unless protected by a constraint, lock, version predicate, or serializable transaction.
3. Deadlocks and serialization conflicts are normal concurrent outcomes requiring whole-transaction handling.
4. A database transaction cannot ordinarily atomically commit an unrelated broker/network effect without a coordination pattern.
5. A retry is safe only if every repeated action is safe or deduplicated at the correct identity scope.
6. HTTP/request success is not the same as database commit, message delivery, or downstream effect completion.

## Learning Objectives

After completing this module, you should be able to:

- determine when Transaction Script fits domain complexity and change patterns;
- define a script's application, database, authorization, and effect boundaries;
- select constraints, optimistic predicates, locks, or serializable isolation for invariants;
- implement atomic idempotency and outbox recording with bounded retries;
- distinguish business errors, concurrency conflicts, dependency failures, and internal defects;
- test actual transaction behavior, concurrency anomalies, crashes, duplicates, and recovery;
- recognize duplication/complexity signals for Domain Model or workflow extraction;
- review financial, medical, safety, or regulated scripts without overstating evidence.

## Core Exposition

### Name one use case

Use `transfer_funds`, `register_shipment`, or `close_invoice`, not `process`, `handle`, or `businessLogic`. Define command/request schema, result/error algebra, actor/tenant/action authority, invariant, and externally observable effect.

Group related scripts in an application service/module if useful. Do not create one class per script unless runtime command identity/scheduling requires it.

### Keep transport outside

The HTTP/RPC/job handler parses transport, authenticates, applies size/rate/deadline controls, calls the script, and maps its typed result. The script must not know status codes, templates, headers, or framework request objects.

The same script can serve API, job, CLI, or message handler only when their authority/idempotency semantics are reconciled explicitly.

### Establish trusted input

Treat client IDs, tenant, ownership, prices, roles, status, timestamps, and calculated totals as untrusted. Derive actor/tenant from authenticated server context and load authoritative values inside the transaction/snapshot.

Validate syntax/shape before the transaction when safe; revalidate state-dependent rules inside it. Bound collection sizes, numeric ranges, text, and query scope before acquiring locks.

### Design the result algebra

Return typed outcomes: applied, duplicate with original compatible result, invalid, denied, not found/non-disclosing, conflict, retry exhausted, dependency unavailable, and internal error. Do not encode them as null/false or parse exception text.

Map to transport only at the edge and follow disclosure policy. A not-found response may intentionally hide unauthorized resource existence.

### Draw the transaction boundary

Start the database transaction immediately before reads that must be consistent with writes and end after governed state, idempotency, and outbox/audit intent are recorded. Keep parsing, slow computation, and remote calls outside when their data consistency permits.

Repository/unit-of-work APIs should make commit/rollback ownership singular. Nested helpers must not silently start/commit independent transactions.

### Encode invariants redundantly where useful

Check business conditions for clear errors, and back them with database constraints/conditional updates when representable. For nonnegative balance, `UPDATE ... WHERE balance >= amount` can atomically claim the condition; inspect affected-row count.

Unique keys protect one-per-tenant identities/idempotency. Foreign/check/exclusion constraints protect structural invariants under every writer. Constraints complement, not replace, domain-readable errors and authorization.

### Choose isolation by anomaly

At read committed, each statement may see a different committed snapshot; read-modify-write checks can lose updates without guarded writes/locks. Repeatable read/snapshot may still permit write-skew-style invariant violations depending on database semantics.

List conflicting transactions and construct a schedule that could violate the invariant. Use atomic SQL, row/advisory/predicate locks, version columns, or serializable isolation based on the actual database. Document portability assumptions.

### Lock deliberately

Acquire rows/resources in stable order to reduce deadlocks. Lock only what protects the invariant and keep the transaction short. `SELECT ... FOR UPDATE` does not automatically protect absent rows, cross-row totals, or arbitrary predicates.

Handle lock timeout/deadlock as typed retryable/failed outcomes. Monitor contention and do not retry forever while amplifying load.

### Implement idempotency atomically

Scope key by tenant/actor/operation as required and bind it to a normalized request digest. In the same transaction, insert/reserve the key, reject reuse with different payload, and store final compatible result/status.

Concurrent duplicate requests must converge through a unique constraint/lock rather than both executing. Define retention, in-progress recovery, privacy, response replay, and what happens after unknown client timeout.

### Retry the whole safe unit

On serialization/deadlock retry, discard the failed transaction/session state, begin anew, reload facts, recompute, and commit. Limit attempts by deadline, use jitter/backoff, instrument conflicts, and stop on non-retryable errors.

Never retry only the final statement after earlier reads. Do not include non-idempotent network effects in the retried lambda.

### Use an outbox for durable messages

Insert a versioned minimal event/message intent with stable ID, aggregate/ordering key, schema, and data/reference in the same database transaction as state/idempotency. A relay later publishes and may duplicate; consumers must be idempotent.

Outbox closes the database-broker dual-write gap. It does not provide universal exactly-once effects, global order, instant delivery, or automatic schema/privacy correctness.

### Keep remote effects outside locks

For payment, email, inventory service, or webhook, choose a workflow: reserve/commit local intent then invoke idempotently, invoke before local transaction with compensation risk, or use saga/orchestration. Record intermediate states and recovery.

Do not hold database locks across an unbounded network call. If a remote authorization quote is needed, bind its signed/versioned/expiry terms and revalidate locally.

### Preserve authorization at the action point

Check authenticated actor/resource/action/tenant and current policy/facts close to mutation. Object lookup alone is not authorization. Recheck security-sensitive state after locks/snapshot establish the acted-upon version.

Use parameterized queries, least-privilege database credentials, row/tenant predicates, and protected audit. Idempotency must not let one actor retrieve another actor's prior result.

### Make helpers cohesive

Extract pure calculations/value validation and narrow data-access operations; keep orchestration readable. Shared business rules need one authoritative module/domain type, not copy/pasted helper snippets.

Avoid a generic base script with hooks/configuration/reflection. Transaction Script's advantage is visible control flow; over-generalization recreates a hidden framework.

### Handle time and money

Capture one authoritative instant/time zone/policy version. Use explicit currency and integer minor units or configured decimal semantics. State rounding stage/mode, rate source/version, and maximum/overflow behavior.

Database/application numeric/time semantics must agree. Test day boundaries, DST where relevant, precision, zero/negative/maximum, and stale quotes.

### Observe without leaking

Record request/correlation/idempotency-safe reference, script name/version, attempt count, outcome/error category, transaction duration, lock/conflict/retry, rows affected, and outbox count/lag. Use bounded labels and redact personal/financial/secret payloads.

Trace commit and relay/consumer as separate stages. A script span ending successfully does not mean an outbox effect was delivered.

### Test with the real database

Unit-test pure calculations and script orchestration with disciplined fakes, but run integration tests against the supported database/version/configuration for constraints, isolation, locks, deadlocks, SQL semantics, transactions, connection failure, and outbox.

Coordinate concurrent schedules with barriers/latches to reproduce lost update/write skew/duplicate races. Fault-inject before/after idempotency insert, state update, outbox insert, commit acknowledgement, relay publish, and consumer effect.

### Know when to evolve

Transaction Script strains when many scripts duplicate rules, behavior depends on rich object state/transitions, invariants span numerous entities, changes touch every procedure, or scripts become long conditional state machines. A Domain Model can centralize behavior; a Service Layer can define application boundary; workflow/saga can own long-running coordination.

Refactor incrementally: extract value objects/pure policies, then aggregates/domain services, keeping script as application coordinator. Do not rewrite all scripts because one domain area became complex.

## Definitions and Notation

Let accounts have balances (b_i\in\mathbb{Z}_{\ge0}) in one currency. A fee-free transfer of (a>0) from (i) to (j) requires (b_i\ge a) and preserves

\[
b'_i=b_i-a,\quad b'_j=b_j+a,\quad \sum_k b'_k=\sum_k b_k.
\]

Let idempotency map (K) bind request key to normalized digest/result. A same-key/same-digest retry returns recorded result without a second state/outbox transition; same-key/different-digest is conflict. These local properties assume atomic isolation and do not establish distributed exactly-once effects.

## Mechanisms, Invariants, or Proof Structure

### Transaction Script design procedure

1. Define one use case, trusted command/context, result algebra, invariants, and effect/durability claims.
2. Separate transport; validate/bound input and authenticate/authorize server-side context.
3. Model competing transactions/anomalies and choose atomic SQL, constraints, versions, locks, or isolation.
4. Bound one local transaction over consistent reads, writes, idempotency, and outbox/audit intent.
5. Keep remote effects outside; define idempotent workflow, recovery, retry, and cancellation.
6. Extract shared pure rules without hiding orchestration or duplicating invariants.
7. Instrument attempts/outcomes/contention/outbox stages with privacy and resource bounds.
8. Test real database concurrency/faults and evolve complex rule clusters toward domain/workflow models.

### Executable finite model

The following in-memory store simulates copy-on-transaction state and atomic replacement on commit. It demonstrates conservation, idempotency, outbox co-commit, and rollback for three serialized calls—not actual isolation, crash durability, authorization, or distributed delivery.

<!-- bijux-verify: {"id":"transaction-script-transfer","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"first=applied A=700 B=800 events=1\nretry=duplicate A=700 B=800 events=1\ndenied=insufficient A=700 B=800 events=1\n","stderr":""}} -->
```python
class Store:
    def __init__(self):
        self.balances = {"A": 1000, "B": 500}
        self.processed = {}
        self.outbox = []

    def begin(self):
        return Transaction(self)


class Transaction:
    def __init__(self, store):
        self.store = store
        self.balances = dict(store.balances)
        self.processed = dict(store.processed)
        self.outbox = list(store.outbox)

    def commit(self):
        self.store.balances = self.balances
        self.store.processed = self.processed
        self.store.outbox = self.outbox


def transfer_funds(store, request_id, source, destination, cents):
    tx = store.begin()
    if request_id in tx.processed:
        return "duplicate"
    if cents <= 0 or source not in tx.balances or destination not in tx.balances:
        return "invalid"
    if tx.balances[source] < cents:
        return "insufficient"
    tx.balances[source] -= cents
    tx.balances[destination] += cents
    tx.processed[request_id] = "applied"
    tx.outbox.append(("funds-transferred", request_id, cents))
    tx.commit()
    return "applied"


store = Store()
first = transfer_funds(store, "R-1", "A", "B", 300)
print("first=" + first + " A=" + str(store.balances["A"]) + " B=" + str(store.balances["B"]) + " events=" + str(len(store.outbox)))
retry = transfer_funds(store, "R-1", "A", "B", 300)
print("retry=" + retry + " A=" + str(store.balances["A"]) + " B=" + str(store.balances["B"]) + " events=" + str(len(store.outbox)))
denied = transfer_funds(store, "R-2", "A", "B", 900)
print("denied=" + denied + " A=" + str(store.balances["A"]) + " B=" + str(store.balances["B"]) + " events=" + str(len(store.outbox)))
```

The model lacks concurrent commit validation: two simultaneous copied transactions could overwrite each other. That deliberate limit illustrates why a dictionary simulation cannot validate database isolation.

## Alternatives and Trade-Offs

- **Domain Model:** centralizes complex stateful behavior/invariants; object-relational and design overhead is higher.
- **Table Module:** organizes logic around all rows of a table/record set; fits record-oriented environments and set operations.
- **Service Layer:** defines application operations/transaction boundary; can contain/delegate to scripts or a Domain Model.
- **Stored procedure:** executes close to data with database transaction semantics; portability, versioning, testing, and ownership trade-offs.
- **Active Record:** row object combines data access and domain behavior; simple but can couple persistence and repeated cross-row rules.
- **Functional core/imperative shell:** pure decisions/calculations inside a procedural coordinator; often complements Transaction Script.
- **Command handler/CQRS:** one write intent per handler and separate reads; does not itself solve transactions/idempotency/distributed effects.
- **Workflow/saga:** owns long-running multi-service state, retries, and compensation; more operational states than one local script.

Choose per bounded domain/use case; one application can legitimately mix scripts and richer models.

## Failure Modes and Misconceptions

- **“Transaction Script means one database transaction.”** Application intent and database boundary must be designed, not assumed.
- **“Sequential code is isolated.”** Concurrent schedules can invalidate read/check/write reasoning.
- **“Serializable means no errors.”** Serialization failures require safe whole-transaction retry.
- **“Idempotency is a cache lookup.”** It needs atomic scope, payload binding, concurrency, result, and retention semantics.
- **“Outbox is exactly once.”** Relay/consumer duplicates and downstream effect identity remain.
- **“A controller is a script.”** Transport concerns obscure reuse, testing, authority, and transaction ownership.
- **“Anemic records make scripts wrong.”** They are appropriate when domain logic is simple and cohesive.
- **“Helpers eliminate duplication.”** Vague utility procedures can spread hidden rules and transactions.
- **“Mocked repositories prove concurrency.”** Database engine isolation/constraints/locks require engine evidence.
- **“Committed means complete.”** External workflows may still be pending, failed, or compensating.

## Worked Examples

### Example 1

Two withdrawals read balance 100 under weak read/check/write and each debit 80. Guarded conditional update allows only one. **Conclusion:** Protect the invariant at the write/serialization boundary.

### Example 2

Two doctors each see another on call and go off call under snapshot isolation. Serializable/predicate locking or a different invariant owner prevents write skew. **Conclusion:** Row conflict is not the only anomaly.

### Example 3

Payment API is called while a database lock is held; timeout causes retry and double charge. A persisted idempotent payment intent moves the effect outside. **Conclusion:** Remote effects and local retries need workflow identity.

### Example 4

Two identical requests race before idempotency insert. A unique key inside the transaction makes one owner and one duplicate result. **Conclusion:** Idempotency must be concurrency-safe.

### Example 5

State commits, then broker publish crashes. An atomic outbox row survives and relay retries. **Conclusion:** Persist message intent with the state.

### Example 6

Scripts trust client `tenant_id` and update another tenant's invoice. Authenticated context and tenant predicate/authorization close the gap. **Conclusion:** Transaction boundaries do not provide authorization.

### Example 7

Deadlocked transactions retry instantly without bound, causing a storm. Stable lock order plus deadline/jitter/attempt cap recovers. **Conclusion:** Retry is a bounded load-control policy.

### Example 8

Twelve scripts copy the same discount thresholds and diverge. Extracted versioned policy centralizes the rule while scripts coordinate. **Conclusion:** Procedural organization still needs one rule owner.

### Example 9

An order lifecycle grows 18 states and cross-entity invariants. Incremental aggregate/state extraction leaves the script as application coordinator. **Conclusion:** Evolve only the complex bounded area.

### Example 10

A medication-dispense script is atomic in tests but dosage source, device timing, overrides, and human workflow are unvalidated. **Conclusion:** Database correctness is not clinical/system safety.

## Cross-Program Connections

- **Software Design and Domain Modeling:** use cases, application services, policies, values, aggregates, and domain models define evolution.
- **Database Engineering:** ACID, MVCC, isolation, locks, constraints, SQL semantics, deadlocks, and recovery ground local correctness.
- **Distributed Systems Engineering:** partial failure, retries, idempotency, outbox, messaging, sagas, and consistency govern external effects.
- **API and Service Engineering:** command schemas, authentication, authorization, errors, deadlines, rate limits, and compatibility expose scripts.
- **Security Engineering:** tenant scope, least privilege, parameterization, current authorization, audit, and disclosure constrain mutations.
- **Concurrency Engineering:** interleavings, atomic guarded writes, versions, lock order, cancellation, and contention constrain execution.
- **Testing and Quality Engineering:** model/concurrency/fault/integration/mutation tests and independent oracles provide evidence.
- **Software Delivery and Reliability Engineering:** rollout, migrations, observability, SLOs, incident recovery, and rollback own operations.
- **Data Architecture Engineering:** ownership, lineage, reference/master data, retention, and event schemas shape transaction facts.
- **Safety and High-Assurance Engineering:** traceability, hazard analysis, independent validation, timing, and human workflow exceed ACID evidence.

## References

1. Martin Fowler, [Transaction Script](https://martinfowler.com/eaaCatalog/transactionScript.html), *Patterns of Enterprise Application Architecture*, 2002/2003. Defines procedures where each handles one presentation request.
2. Martin Fowler et al., *Patterns of Enterprise Application Architecture*, Addison-Wesley, 2002, ISBN 978-0-321-12742-6. Provides Transaction Script, Domain Model, Table Module, Service Layer, gateways, Unit of Work, and concurrency patterns.
3. Jim Gray and Andreas Reuter, *Transaction Processing: Concepts and Techniques*, Morgan Kaufmann, 1992, ISBN 978-1-55860-190-1. Comprehensive transaction, concurrency, recovery, and processing foundation.
4. PostgreSQL Global Development Group, [Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html), PostgreSQL 18 documentation, accessed 2026-08-28. Documents implemented isolation levels and serialization anomalies.
5. Atul Adya, [*Weak Consistency: A Generalized Theory and Optimistic Implementations for Distributed Transactions*](https://pmg.csail.mit.edu/papers/adya-phd.pdf), MIT PhD thesis, 1999. Formalizes transaction histories and weak-consistency anomalies.
6. Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly, 2017, ISBN 978-1-4493-7332-0. Explains isolation, serializability, distributed transactions, time, and failure.
7. Chris Richardson, [Transactional Outbox](https://microservices.io/patterns/data/transactional-outbox.html), accessed 2026-08-28. Describes atomic database update and message-intent persistence without database-broker 2PC.
8. OWASP Foundation, [Transaction Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transaction_Authorization_Cheat_Sheet.html), accessed 2026-08-28. Provides server-side transaction-data integrity, authorization, sequencing, and fail-safe guidance.

## Exercises

### Exercise 1

Trace the executable transfer script and state exactly which transaction, idempotency, conservation, outbox, concurrency, and durability claims it does and does not establish.

### Exercise 2

Design a PostgreSQL Transaction Script for reserving limited inventory under concurrent requests with idempotency and an outbox.

### Exercise 3

Construct anomaly schedules for a cross-row invariant and compare atomic SQL, locks, optimistic versions, and serializable isolation.

### Exercise 4

Plan migration of a growing Transaction Script subsystem toward a Domain Model without changing every use case at once.

### Exercise 5

Review a high-stakes Transaction Script without claiming financial, clinical, safety, security, or regulatory correctness from ACID/test evidence.

## Answers to the Exercises

### Answer 1

First transaction copies A=1000/B=500/empty processed/outbox. R-1 is new, 300 valid, A sufficient; it produces A=700/B=800, records R-1 applied and one event, then atomically replaces store fields. Retry copies committed state, finds R-1 and returns duplicate without commit/change. R-2 requests 900, finds A=700 insufficient, returns without commit; totals remain 1500 and one event.

This proves one serialized in-process finite trace, fee-free conservation, same-key duplicate suppression after commit, outbox/state replacement together in this model, and no mutation on insufficient funds. It does not prove payload binding, authorization/tenant, crash durability, concurrent commit validation, database isolation/constraints, deadlock/retry, integer bounds/currency, commit uncertainty, relay/delivery/idempotent effects, or exactly-once behavior.

### Answer 2

Command contains server-authenticated tenant/actor, SKU/location, positive bounded quantity, request key and normalized digest, deadline. Transaction inserts/reserves `(tenant,operation,key,digest)` under unique constraint; same digest returns stored status/result, different digest conflicts. Use one atomic statement such as decrement `available` where tenant/SKU/location and `available>=quantity`, returning new version; zero affected distinguishes not found/unauthorized according to disclosure versus insufficient/conflict through safe follow-up under the same transaction or a function with explicit result.

Insert reservation with unique business identity, store idempotency outcome, and insert versioned `InventoryReserved` outbox row in the same transaction. Commit; relay publishes with retries, consumer deduplicates by event/effect ID. Acquire multiple SKUs in stable order; retry serialization/deadlock by recreating whole transaction within deadline/jitter cap. Test simultaneous last-unit claims, duplicate same/different payload, transaction/outbox constraint failure, timeout/unknown commit, deadlock, tenant bypass, relay duplicates/order, schema skew, and reconciliation on the actual PostgreSQL version.

### Answer 3

Use “at least one doctor on call.” Initial A=true, B=true. T1 reads both, decides B remains, writes A=false; T2 reads both in the same snapshot, decides A remains, writes B=false. Writes touch different rows, so snapshot/repeatable-read can commit both depending on engine, violating cross-row invariant.

Atomic single-row SQL cannot alone express this cross-row predicate unless representation changes—for example one guarded schedule/version row or count with a constraint/serialized updater. Lock all roster rows or a stable parent/advisory key in canonical order, then re-read/check/write; ensure phantom membership is protected. Optimistic version on one shared roster record makes one commit conflict; per-doctor versions do not. Serializable isolation can detect a dangerous structure and abort one, requiring bounded whole-transaction retry. Test actual engine schedules, membership insert/delete phantoms, lock timeout/deadlock, and starvation; choose based on invariant, contention, portability, and operational evidence.

### Answer 4

Inventory scripts, duplicated rules/co-change, state transitions, cross-entity invariants, data access, effects, and incidents. Choose one bounded high-change concept, not a wholesale rewrite. Lock public script result/error/idempotency/effect contracts with characterization plus authoritative domain tests. Extract pure value types/calculations/policies first, then an aggregate/domain service owning invariants/transitions; repositories map it while the original script remains the application transaction/authorization/outbox coordinator.

Run old/new pure decision differentials over boundary/historical fixtures; shadow plans only, never effects. Migrate one script/cohort at a time with compatible state/schema, backfill/reconciliation, metrics, rollback, and version skew tests. Keep simple CRUD scripts procedural. Remove duplicated legacy rules/adapters after measured convergence. Verify concurrency/isolation, serialization, performance, authorization, outbox, migrations, and operations at each commit; do not call an anemic data object a completed Domain Model.

### Answer 5

Define use case authority, exact invariants, data sources/units/versions, preconditions/outcomes, concurrency/isolation, timing/resource bounds, authorization/separation of duties, idempotency, external effects, failure/degraded/safe states, audit/retention, human override, hazards, and exact claim. Trace transaction and external workflow through success, crash, retry, cancellation, partition, stale data, duplicate, and recovery.

Evidence requires requirements/source traceability, independent domain/numerical recomputation, actual-database constraint/isolation/deadlock/fault tests, end-to-end idempotency/outbox/recovery/reconciliation, security threat/authorization/audit review, worst-case timing/capacity, data quality/lineage, representative workflow/human-factors trials, hazard/risk analysis, controlled rollout/rollback/monitoring/incident records, and applicable quality/regulatory change control. Named financial/clinical/domain, database/concurrency, safety, security/privacy, verification, human-factors, quality/regulatory, and operations reviewers approve. ACID, script execution, and passing tests establish no high-stakes correctness or fitness.
