---
module_id: SEPAT-054
program: Software Engineering: Patterns
level: 2
module_number: 54
title: Service Layer
status: complete
last_verified: 2026-08-28
---

# Service Layer

## One-Page Review

### Governing question

How can an application expose one stable set of use-case operations to HTTP, jobs, messages, CLI, and integrations while keeping transport, domain rules, transaction control, authorization, idempotency, retries, effects, and distributed workflow in their correct boundaries?

### Essential definitions

- A **Service Layer** defines an application's boundary through available operations and coordinates its response to each operation.
- An **application service** implements one or several use cases by coordinating domain and infrastructure components.
- A **domain service** owns a stateless domain operation that does not naturally belong to an entity or value; it is inside the domain model, not the application boundary.
- A **transport adapter** maps HTTP/RPC/message/CLI input and output; it does not own the use case.
- A **command** is an explicit request to attempt a state-changing use case; a **query** asks for information without domain mutation.
- A **result algebra** is the closed set of typed success and failure outcomes exposed by an operation.
- A **transaction boundary** determines which local state changes commit or roll back atomically.
- An **idempotency identity** names one logical command so retries can converge on its recorded outcome.
- An **outbox** atomically records message intent with local state for later at-least-once relay.
- An **orchestrator/workflow** owns a long-running process across transaction or service boundaries, including intermediate states, timeouts, and compensation.

### Central model, mechanism, or theorem

For trusted operation context $x$, command $c$, local state $S$, and idempotency map $K$, an application operation denotes

$$
L(S,K,c,x)\to(S',K',r,O')
\quad\text{or}\quad(S,K,e,O),
$$

where $r$ is typed success, $e$ typed failure, and $O'$ outbox intent. The layer validates/binds identity and authority, establishes the local transaction, loads governed state, delegates domain decisions, persists state plus idempotency/outbox, and maps the result. Local atomicity is conditional on the real transaction system; it does not make remote calls atomic or prove the domain rule correct.

### Critical invariants

- Every public operation names a business use case and has one canonical command/query/result contract independent of transport.
- Actor, tenant, authority, time, policy, correlation, deadline, and idempotency context are trusted, scoped, and explicit.
- Authorization is action/resource/state specific, deny-by-default, and rechecked at the mutation boundary when concurrency matters.
- One owner controls transaction begin/commit/rollback; domain and repository helpers cannot commit independently.
- Domain rules remain in entities, values, policies, domain services, Table Modules, or Transaction Scripts as appropriate; the layer coordinates them.
- Idempotency record, governed local state, audit, and outbox intent commit together where the claim requires it.
- External effects are outside retriable local transactions and use explicit idempotency, workflow, timeout, and recovery.
- Errors retain distinctions among invalid, denied/non-disclosing, not found, conflict, duplicate, dependency failure, timeout/cancel, retry exhausted, and defect.
- All adapters receive equivalent semantics; no privileged bypass appears in jobs, imports, admin tools, or message consumers.
- Telemetry is bounded and privacy-aware, and tests cover real transactions, concurrency, recovery, and authorization—not only mocked orchestration.

### Common failures

Common failures include a service per entity with generic CRUD, controllers owning transactions, domain rules duplicated across services, a “domain service” that is actually application orchestration, passing framework requests into the layer, trusting client actor/tenant/status/price, role-only authorization, one giant god service, repositories committing, nested implicit transactions, remote calls while locks are held, retrying non-idempotent effects, idempotency outside the transaction, state-then-broker dual write, catch-all exceptions, leaking ORM entities, inconsistent API/job semantics, service-to-service call chains mistaken for atomic workflows, thread-local hidden context, unbounded fan-out, and mocks that cannot expose isolation or crash defects.

### Compact example

A `TransferService` checks actor/action and request identity, opens one in-memory work unit, loads two `Account` objects, asks the source to debit and target to credit, records the result and one outbox fact, then commits. A repeat returns `duplicate`; a different actor returns `denied`; neither changes balances or events.

### Connections

[SEPAT-053](053-table-module.md) supplies a table-centered domain-logic component; [SEPAT-055](../ROADMAP.md) develops Unit of Work. Service Layer connects to [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md), [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md), and [Security Engineering](../../25-security-engineering/ROADMAP.md).

## Governing Question

What stable application boundary lets every delivery mechanism invoke the same use-case semantics, while making transaction, authority, retry, effect, and error ownership reviewable and preventing the boundary from absorbing the domain itself?

Service Layer is an architectural boundary, not a deployment topology. It may be an in-process module in a monolith or the internal application boundary of a network service. Calling remote endpoints “services” does not implement this pattern.

## Why This Matters

Applications rarely have only one interface. A purchase may originate from HTTP, a scheduled renewal, a message, an administrative tool, or an import. If each adapter implements validation, authorization, transaction handling, business sequencing, and event publication, semantics diverge and bypasses appear.

A Service Layer makes the supported operations explicit. It centralizes application coordination while leaving domain knowledge in the right model. This creates a useful seam for transactions, security, observability, tests, and evolution.

The boundary can also become a dumping ground. “Service” is vague; generic manager classes accumulate unrelated methods, conceal remote failure, and drain behavior from domain objects. The pattern succeeds only when use-case contracts and ownership are precise.

## Prerequisites and Retrieval

You should understand layering, ports/adapters, Domain Model, Transaction Script, Table Module, repositories, transactions/isolation, authentication/authorization, idempotency, outbox, retries, and distributed failure. Retrieve these facts:

1. Authentication establishes an identity; authorization decides whether that identity may perform this action on this resource in this context.
2. A database transaction cannot ordinarily atomically commit an unrelated broker or remote service effect.
3. Retrying after an unknown outcome can duplicate effects unless the operation has the correct idempotency protocol.
4. Local method call, database commit, response delivery, message delivery, and downstream effect are distinct milestones.
5. Domain validity and application coordination are different responsibilities.
6. Cancellation/deadline propagation does not guarantee that already committed or remote work was undone.
7. A stable API is a semantic contract, not just a function signature.

## Learning Objectives

After completing this module, you should be able to:

- distinguish application services, domain services, transport adapters, repositories, and distributed services;
- define cohesive use-case commands, queries, contexts, and typed results;
- assign transaction and Unit of Work ownership without nested-commit ambiguity;
- bind authentication, action authorization, tenant scope, and transaction authorization to execution;
- implement atomic idempotency, audit, state, and outbox coordination for local operations;
- select retry, timeout, cancellation, and dependency policies from failure semantics;
- move long-running cross-system behavior into explicit workflows/sagas;
- maintain equivalent semantics across synchronous, asynchronous, batch, CLI, and administrative adapters;
- test orchestration, domain delegation, actual storage concurrency, crash points, security, and observability;
- detect anemic models, god services, generic CRUD boundaries, and inappropriate service granularity.

## Core Exposition

### Define the application boundary from use cases

List externally meaningful operations: `place_order`, `approve_claim`, `transfer_funds`, `rebuild_projection`. Define who may request each, its inputs, success/failure meanings, state/effects, consistency, and resource bounds. These are capabilities, not table CRUD.

Avoid `EntityService.create/update/delete` as the default. It exposes storage shape, encourages mass assignment, and rarely captures lifecycle transitions or action-specific authority. A coarse boundary should mean cohesive use cases, not one class containing the application.

### Distinguish the roles called service

An application service coordinates a use case. A domain service calculates or decides in domain language without technical orchestration. An infrastructure service implements a port to a clock, payment network, email provider, or storage system. A network service is a deployment/API boundary.

Name by responsibility: `TransferApplication`, `ExchangePolicy`, `PaymentGateway`, not four indistinguishable `PaymentService` classes. Dependencies should point so the domain is not coupled to transport or infrastructure.

### Make commands explicit and immutable

A command contains normalized domain-relevant input and a versioned schema; trusted context is supplied separately. Avoid passing HTTP requests, ORM sessions, headers, globals, or arbitrary maps. Validate shape and bounds at the adapter, then enforce domain/state-dependent constraints inside the operation/model.

Commands should state units, optionality, identity scope, expected version, and policy/evidence references. Treat client-computed prices, tenant IDs, roles, ownership, and timestamps as untrusted unless cryptographically/procedurally established.

### Design a result algebra

Return typed outcomes such as applied, accepted with operation ID, duplicate with compatible prior outcome, invalid field/rule, denied/non-disclosing, not found, state/version conflict, dependency unavailable, deadline/cancelled, retry exhausted, and internal defect. Do not use null/boolean or parse exception messages.

Transport adapters map results to HTTP/RPC/message acknowledgment/CLI exit semantics. The application contract remains stable even when protocols differ. Error payloads obey disclosure and privacy policy.

### Establish trusted operation context

Context may include actor/subject, tenant, authenticated strength, action authorization evidence, correlation/causation IDs, idempotency key, authoritative time, deadline/cancellation, locale only where domain-relevant, and policy versions. Build it server-side and keep it immutable.

Avoid ambient thread-local context in reusable or asynchronous code: it can disappear across tasks, leak between requests, and hide test premises. Pass the minimum explicit context each operation needs.

### Bind authorization to the actual action

Authenticate at the edge, but authorize the precise actor-resource-action under current state. Load tenant-scoped resources without disclosing others; use deny by default and least privilege. Sensitive transaction authorization should bind the user-approved significant data to the executed command and expire/reject replay.

If resource state can change after an early check, re-evaluate authority/preconditions under the lock/snapshot/version used for mutation. A route annotation or generic `is_admin` check is not sufficient evidence for object/action authority.

### Own one local transaction boundary

The application service typically begins a Unit of Work immediately before consistent reads and ends after domain state, idempotency, audit, and outbox intent are durable. Parsing and slow external calls stay outside where semantics allow. One component owns commit/rollback.

Repositories join the current Unit of Work; they do not commit independently. Domain objects do not access the transaction. Nested calls either participate explicitly, use a documented savepoint, or are separate operations—never silently open autonomous commits.

### Delegate domain decisions

The layer loads aggregates or table state, supplies explicit evidence/context, invokes intention-revealing behavior, and persists results. It should not duplicate `if status == ...` rules that the model owns. With Transaction Script, the script itself may be the service operation; do not add a pass-through class merely for symmetry.

Thin does not mean line-count minimal. Transaction, idempotency, authorization, retry, deadline, and outbox coordination are legitimate application logic. Business calculations and lifecycle invariants are not.

### Implement idempotency at the command boundary

Scope an idempotency key by tenant/actor/operation as required and bind it to a canonical request digest. Reserve/check it in the same transaction as state changes. Same key plus same digest returns a compatible recorded result; same key plus different digest is conflict.

Define concurrent duplicates, in-progress ownership/expiry, unknown response after commit, result retention, privacy, and replay of authorization. Idempotency of the application operation does not automatically make remote effects idempotent.

### Coordinate durable messages with an outbox

Domain behavior may record facts; the application persists aggregate/table changes and outbox records atomically. A relay publishes after commit and can duplicate. Consumers deduplicate by stable identity and honor ordering scope/schema/privacy contracts.

Do not publish before commit or in an “after commit” callback without durable recovery. A successful outbox insert means intent is durable, not that a consumer acted.

### Keep remote calls outside retriable locks

Fetching a read-only quote before the transaction can be reasonable if its signed/versioned/expiry evidence is revalidated. Performing an irreversible charge while a retriable database transaction is open is dangerous: retry can charge twice and locks remain held through uncertain latency.

Use provider idempotency keys and a workflow state machine for multi-step effects. Record intended/in-progress/succeeded/failed/unknown states, timeouts, reconciliation, and compensation. Never claim rollback undoes the network.

### Move long-running processes to workflows

A Service Layer operation may initiate or advance a workflow, but should not hide a multi-hour saga in one synchronous call stack. A workflow owns state across transactions: step, attempts, deadlines, correlation, received facts, compensation, manual intervention, and terminal outcome.

Across services, define consistency and convergence explicitly. Chained remote calls do not become one transaction because an application service coordinates them.

### Select retry from semantics

Retry whole local transactions on specific deadlock/serialization outcomes only when all repeated work is safe; reload and recompute under a deadline with bounded attempts/backoff/jitter. Do not retry invalid, denied, or stable domain conflicts.

Dependency retry depends on idempotency and outcome knowledge. Circuit breakers/load shedding can protect capacity but change observable availability. Return accepted/unknown/retry-exhausted honestly rather than fabricating success.

### Propagate deadline and cancellation

Derive a budget for database, dependency, and queue work. Check cancellation before expensive stages and use driver/provider timeouts. Once local commit succeeds, client cancellation does not reverse it; return/recover through operation identity.

Avoid letting every nested layer invent timeouts independently. Reserve time for cleanup, commit, and response. Observe where deadline expired.

### Support multiple adapters consistently

HTTP handler, message consumer, job, CLI, and admin UI should construct the same canonical command/context and call the same operation or an intentionally distinct privileged operation. Their delivery semantics differ: message acknowledgment happens only after the appropriate durable milestone; CLI exit codes map typed results; async APIs may return operation IDs.

Test equivalence. Administrative and migration paths are common authorization/invariant bypasses; give them named capabilities, audit, rate/blast-radius controls, and domain validation.

### Separate queries without overbuilding

Query services may return purpose-built immutable projections with authorization, tenant scope, pagination, freshness, and disclosure rules. They usually need not load aggregates. State-changing commands must not depend blindly on a stale projection.

CQRS can mean only distinct command/query models; it does not require event sourcing, two databases, or messaging. Adopt complexity only when read/write needs justify it.

### Define dependency ports

The application depends on narrow ports stated in its language: repository, Unit of Work factory, authorization decision, quote provider, outbox, clock. Ports return typed outcomes and expose capabilities such as idempotency/deadline, rather than leaking a vendor SDK.

Keep dependency direction stable, but do not create interfaces for every class by ritual. A port is useful at an ownership/technology/test boundary with meaningful alternatives or controlled effects.

### Observe without exposing secrets

Record operation name/version, correlation/causation/idempotency-safe IDs, actor/tenant-safe references, outcome category, duration by stage, transaction attempts/conflicts, repository counts, dependency status/latency, outbox count/lag, and workflow state. Bound labels and redact commands, tokens, personal, health, and financial data.

Trace does not prove success: distinguish service return, local commit, outbox relay, consumer application, and physical effect. Audit logs require integrity, access, retention, and disclosure controls.

### Test at the correct boundaries

Unit-test orchestration with strict fakes: expected call order only where semantic, typed failures, no commit on rejection, and no external effect inside retry. Test domain rules in their owner. Contract-test ports/adapters.

Integration-test the real database/transaction manager for isolation, constraints, versions, rollback, nested behavior, idempotency races, outbox atomicity, commit uncertainty, timeout, and cancellation. Fault-inject every durable boundary. Security tests enumerate actors/resources/actions/tenants/states, including every adapter and non-disclosure.

### Choose granularity by cohesion and change

Group operations by bounded context/capability, not necessarily one class per entity or endpoint. A service with dozens of unrelated dependencies and methods signals missing boundaries; many one-method pass-through services signal ceremony. Track change coupling and authority/transaction differences.

Split when operations have different domain language, security ownership, transaction resources, scaling, release cadence, or team ownership. Do not split merely to create network services; distribution adds partial failure and compatibility obligations.

### Evolve safely

Extract a canonical operation from duplicated controllers/jobs one use case at a time. Characterize current semantics, reconcile contradictions with owners, introduce commands/results and a transaction boundary, route adapters, then remove bypasses. Preserve idempotency and external contract compatibility.

When an application service accumulates domain conditionals, move rules into a model/policy. When it accumulates long-running state, extract a workflow. When it is pure pass-through, remove it unless the boundary itself provides durable value.

## Definitions and Notation

Let local state be $S$, idempotency registry $K$, command $c$, trusted context $x$, result set $R$, error set $E$, and outbox multiset $O$. One operation is a partial function

$$
L:S\times K\times C\times X
\rightarrow (S\times K\times R\times O)\cup E.
$$

Let identity $k=\kappa(c,x)$ and canonical request digest $h=H(c)$. Required idempotency behavior is

$$
K[k]=(h,r)\Rightarrow
\begin{cases}
r,&H(c)=h,\\
\mathrm{key\_conflict},&H(c)\ne h.
\end{cases}
$$

For transfer amount $a>0$ between same-currency balances $b_s\ge a$ and $b_t\ge0$, the domain transition gives $b'_s=b_s-a$, $b'_t=b_t+a$, preserving $b'_s+b'_t=b_s+b_t$. The Service Layer establishes identity, authority, transaction, persistence, and outbox premises around that domain operation.

## Mechanisms, Invariants, or Proof Structure

### Service Layer design procedure

1. Inventory use cases and every adapter; define canonical commands, queries, trusted contexts, and result algebras.
2. Assign domain rules to aggregates/values/policies/services/scripts/tables and application coordination to the Service Layer.
3. Specify actor-resource-action authority, tenant scope, transaction authorization, and non-disclosure.
4. Draw local transaction ownership, repository/Unit of Work participation, isolation/concurrency, and commit milestone.
5. Define idempotency scope/digest/concurrency/retention and atomically store outcome with state/audit/outbox.
6. Keep remote effects outside retriable transactions; define dependency deadlines, idempotency, reconciliation, and workflow states.
7. Map typed results consistently across HTTP, message, job, CLI, and administrative adapters.
8. Instrument bounded stage/outcome telemetry and protected audit without sensitive payload leakage.
9. Test domain delegation, real transactions/concurrency, authorization matrix, crash points, retries, cancellation, and adapter equivalence.
10. Split god services, remove pass-through ceremony, and extract domain rules or workflows when evidence indicates wrong ownership.

### Executable finite model

The example uses one application service, an in-memory Unit of Work copy, two domain accounts, one idempotency registry, and one outbox list. It demonstrates authorized coordination, conservation, atomic replacement in serialized memory, duplicate response, and denial. It does not implement authentication, request digests, real transactions/isolation, parallel calls, crash durability, broker delivery, currencies, or external review.

<!-- bijux-verify: {"id":"service-layer-transfer","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"first=applied A=700 B=800 events=1\nretry=duplicate A=700 B=800 events=1\ndenied=denied A=700 B=800 events=1\n","stderr":""}} -->
```python
class Account:
    def __init__(self, account_id, balance_cents):
        self.account_id = account_id
        self.balance_cents = balance_cents

    def debit(self, amount_cents):
        if amount_cents <= 0:
            return "invalid-amount"
        if self.balance_cents < amount_cents:
            return "insufficient"
        self.balance_cents -= amount_cents
        return "debited"

    def credit(self, amount_cents):
        self.balance_cents += amount_cents


class Store:
    def __init__(self):
        self.accounts = {"A": Account("A", 1000), "B": Account("B", 500)}
        self.receipts = {}
        self.outbox = []

    def begin(self):
        return Work(self)


class Work:
    def __init__(self, store):
        self.store = store
        self.accounts = {
            key: Account(value.account_id, value.balance_cents)
            for key, value in store.accounts.items()
        }
        self.receipts = dict(store.receipts)
        self.outbox = list(store.outbox)

    def commit(self):
        self.store.accounts = self.accounts
        self.store.receipts = self.receipts
        self.store.outbox = self.outbox


class TransferService:
    def __init__(self, store):
        self.store = store

    def transfer(self, actor, request_id, source_id, target_id, amount_cents):
        if actor != "operator-7":
            return "denied"
        work = self.store.begin()
        if request_id in work.receipts:
            return "duplicate"
        source = work.accounts[source_id]
        target = work.accounts[target_id]
        result = source.debit(amount_cents)
        if result != "debited":
            return result
        target.credit(amount_cents)
        work.receipts[request_id] = "applied"
        work.outbox.append(f"funds-transferred:{request_id}")
        work.commit()
        return "applied"


store = Store()
service = TransferService(store)
result = service.transfer("operator-7", "R-1", "A", "B", 300)
print(f"first={result} A={store.accounts['A'].balance_cents} B={store.accounts['B'].balance_cents} events={len(store.outbox)}")
result = service.transfer("operator-7", "R-1", "A", "B", 300)
print(f"retry={result} A={store.accounts['A'].balance_cents} B={store.accounts['B'].balance_cents} events={len(store.outbox)}")
result = service.transfer("intruder", "R-2", "A", "B", 100)
print(f"denied={result} A={store.accounts['A'].balance_cents} B={store.accounts['B'].balance_cents} events={len(store.outbox)}")
```

### Finite invariant argument

**Base.** Balances are nonnegative; total is 1500; receipt/outbox are empty.

**Authorized first call.** The service opens a private copy, the source domain object checks $300>0$ and $1000\ge300$, debit/credit yield 700 and 800, receipt and one event are added, then all copied state replaces store state. Total remains 1500.

**Duplicate.** A copied registry already contains `R-1`, so the operation returns before domain mutation/commit; state remains unchanged.

**Denied.** Authority fails before beginning a work unit; state remains unchanged.

By case analysis over these three calls, nonnegative balances, conservation, at-most-one recorded application for `R-1`, and no denied effect hold. This is not a concurrency proof: two simultaneous copies could both miss the receipt and overwrite. Real uniqueness, isolation/versioning, durable commit, request-digest binding, and secure authorization are additional premises.

### Evidence classification

Execution is empirical evidence for one serialized trace. Arithmetic and case results can be independently recomputed; the finite case argument can be reviewed line by line. It provides no evidence for real database isolation, authentication, distributed messaging, financial policy, or operational safety.

## Alternatives and Trade-Offs

| Approach | Boundary | Best fit | Main risk |
|---|---|---|---|
| Direct adapter-to-domain | Protocol endpoint | Tiny single-interface application | Duplicated semantics as interfaces grow |
| Transaction Script | One procedural use case | Simple domain logic | Rules duplicate across scripts |
| Service Layer + Domain Model | Application capability over rich model | Multiple adapters and complex rules | Anemia or excess ceremony |
| Service Layer + Table Module | Application operation over set logic | Set-oriented enterprise work | Storage semantics leak upward |
| Command bus/mediator | Uniform dispatch pipeline | Cross-cutting policies and many commands | Hidden control flow/generic indirection |
| Workflow/saga | Durable multi-transaction process | Long-running cross-system work | State/compensation complexity |
| Network API gateway | Cross-service edge | Routing and edge policy | Mistaken for application semantics |

Service Layer may be implemented as functions, classes, command handlers, or modules. The pattern is the semantic boundary and coordination responsibility, not a framework shape.

## Failure Modes and Misconceptions

- **“Every class named service belongs in Service Layer.”** Domain, infrastructure, and network services have different ownership.
- **“One service per entity is clean.”** CRUD grouping often exposes storage rather than capabilities.
- **“Thin means no logic.”** Application coordination is logic; domain rules should remain elsewhere.
- **“Service Layer requires Domain Model.”** It can coordinate scripts or Table Modules, and may be unnecessary for one simple interface.
- **“Controllers can start transactions because they call the service.”** This couples transport to application consistency and creates adapter divergence.
- **“Repositories should commit their own changes.”** Independent commits destroy one operation's atomic boundary.
- **“Authentication implies authorization.”** Authority is action/resource/context specific and must be bound to execution.
- **“An idempotency key alone prevents duplicates.”** Scope, digest binding, unique atomic storage, outcome recovery, and effect idempotency are required.
- **“Retry any exception.”** Permanent domain/security failures and unknown external effects must not be blindly repeated.
- **“One application method can make remote services atomic.”** Distribution introduces partial failure and needs workflow semantics.
- **“Cancellation rolls back everything.”** Work may already be committed or remotely accepted.
- **“Domain events can publish themselves.”** Domain objects cannot own durable transaction-to-broker coordination.
- **“All adapters are equivalent automatically.”** Admin, job, message, and import paths often bypass checks unless tested.
- **“A command bus makes boundaries explicit.”** Generic dispatch can hide ownership, transactions, and call graphs without disciplined contracts.
- **“Mock orchestration proves production correctness.”** Real isolation, constraints, commit uncertainty, timeouts, and authorization integration need stronger evidence.

## Worked Examples

### Example 1

**Situation.** HTTP and nightly job each implement invoice closing with different tax and authorization checks.

**Reasoning.** Define one `close_invoice` command/result and trusted context. Both adapters validate transport then invoke the same application operation. The operation authorizes current action, opens one transaction, delegates invoice transition, persists/outboxes, and returns typed result.

**Conclusion.** Service Layer removes interface-specific semantic duplication while retaining adapter differences.

### Example 2

**Situation.** `OrderService.calculate_total` contains pricing arithmetic while `Order` is a data bag.

**Reasoning.** This is an anemic Domain Model: application coordination and domain calculation are conflated. Move arithmetic/rounding to values/policy/order as conceptual ownership dictates; leave `place_order` coordination in the application service.

**Conclusion.** A Service Layer should orchestrate a rich domain, not drain it of behavior.

### Example 3

**Situation.** `CustomerService.update(id, fields)` accepts a client map including `tenant_id`, `credit_limit`, and `status`.

**Reasoning.** Generic mass assignment bypasses use-case authority and invariants. Replace it with `change_contact`, `approve_credit_limit`, and `suspend_customer`, each with allowlisted input, distinct authority, expected version, audit, and typed result.

**Conclusion.** Capability-named operations make security and rules reviewable.

### Example 4

**Situation.** A repository saves an order and commits; the service then inserts an outbox record in another transaction.

**Reasoning.** A crash between commits loses the message. Repository should join the service-owned Unit of Work; aggregate state, idempotency, and outbox intent commit atomically. Relay occurs afterward.

**Conclusion.** Transaction ownership must be singular and include every local fact in the completion claim.

### Example 5

**Situation.** Two same-key requests race and both see no idempotency row.

**Reasoning.** A pre-transaction lookup is insufficient. Insert/reserve a tenant-operation-scoped key with a unique constraint inside the transaction, bind canonical digest, serialize the winner, and return compatible prior result or different-digest conflict.

**Conclusion.** Idempotency is a transactional protocol, not a cache lookup.

### Example 6

**Situation.** A service charges a card inside a transaction that retries after serialization failure.

**Reasoning.** The charge may succeed before the database aborts; retry can charge twice. Use provider idempotency plus a durable payment workflow, or persist intent/outbox then perform and reconcile the effect. Keep locks short.

**Conclusion.** Retriable local work must exclude unsafe external effects.

### Example 7

**Situation.** A request times out after commit but before the response reaches the client.

**Reasoning.** Returning “failed” is wrong; outcome is unknown to the caller. A retry with the same identity retrieves the recorded result. Expose operation lookup where needed and distinguish local commit from response delivery in telemetry.

**Conclusion.** Idempotency and outcome recovery resolve commit-acknowledgment uncertainty.

### Example 8

**Situation.** A message consumer acknowledges before the application transaction commits.

**Reasoning.** Crash loses the message and work. Call the canonical operation, commit durable state/idempotency/outbox, then acknowledge according to broker semantics. Duplicate delivery must return duplicate without effects.

**Conclusion.** Adapter acknowledgment belongs after the operation's required durability milestone.

### Example 9

**Situation.** One service method calls inventory, payment, shipping, and email synchronously and calls the sequence atomic.

**Reasoning.** Each system can fail independently; timeout leaves unknown outcomes and no common rollback. Initiate a persisted workflow with reservations, stable IDs, deadlines, compensation, reconciliation, and terminal/manual states.

**Conclusion.** Cross-service orchestration needs a workflow, not an oversized synchronous method.

### Example 10

**Situation.** A clinician-facing operation signs a medication order after a session-role check.

**Reasoning.** Bind authorized clinician, patient/order, significant dose/route data, policy, evidence versions, expected state/version, and expiry at execution. Revalidate under the transaction, preserve non-disclosing denials and immutable audit, and require named clinical/security/human-factors review of the real workflow.

**Conclusion.** High-stakes Service Layers need transaction-bound authorization and multidisciplinary evidence beyond unit tests.

## Cross-Program Connections

- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) develops boundaries, ports/adapters, dependency direction, and deployment trade-offs.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) covers protocol contracts, versioning, idempotency, deadlines, and service operations.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) develops authentication, action authorization, tenant isolation, audit, and threat modeling.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) supplies transaction, isolation, locking, constraint, and commit semantics.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies partial failure, messaging, ordering, sagas, and convergence.
- [SEPAT-053](053-table-module.md) provides a set-oriented component behind the boundary; [SEPAT-055](../ROADMAP.md) formalizes object-change tracking and commit coordination.

## References

1. Randy Stafford, [“Service Layer”](https://martinfowler.com/eaaCatalog/serviceLayer.html), in Martin Fowler's *Patterns of Enterprise Application Architecture* catalog, 2003.
2. Martin Fowler, *Patterns of Enterprise Application Architecture*, Addison-Wesley, 2002. Service Layer and related domain/data-source patterns.
3. Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software*, Addison-Wesley, 2004. Application/domain layer and service distinctions.
4. Alistair Cockburn, [“Hexagonal Architecture”](https://alistair.cockburn.us/hexagonal-architecture/), 2005. Ports/adapters boundary model.
5. Martin Fowler, [“Unit of Work”](https://martinfowler.com/eaaCatalog/unitOfWork.html), 2003. Change tracking, business transaction, and concurrency coordination.
6. OWASP Foundation, [“Authorization Cheat Sheet”](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html), accessed 2026-08-28.
7. OWASP Foundation, [“Transaction Authorization Cheat Sheet”](https://cheatsheetseries.owasp.org/cheatsheets/Transaction_Authorization_Cheat_Sheet.html), accessed 2026-08-28.
8. Jim Gray and Andreas Reuter, *Transaction Processing: Concepts and Techniques*, Morgan Kaufmann, 1992.
9. Martin Kleppmann, *Designing Data-Intensive Applications*, O’Reilly, 2017. Transactions, replication, streams, and distributed-failure limits.
10. PostgreSQL Global Development Group, [“Concurrency Control”](https://www.postgresql.org/docs/current/mvcc.html), current documentation accessed 2026-08-28. Concrete engine semantics; other systems differ.

## Exercises

### Exercise 1

Trace the executable service for `transfer("operator-7", "R-2", "A", "B", 900)` after the three shown calls, followed by the same request ID with amount 100. State results/state and identify a limitation in the model's idempotency behavior.

### Exercise 2

Design the command, trusted context, result algebra, transaction boundary, domain delegation, idempotency, outbox, and adapter mappings for `approve_expense`. Include expected version, tenant, manager authority, approval limit, and a duplicate message delivery.

### Exercise 3

Diagnose a `CustomerService` with 38 methods, 16 repositories, HTTP types, pricing rules, email calls, and its own thread-local actor. Propose durable boundaries and a safe incremental migration with evidence.

### Exercise 4

Compare a direct controller, Transaction Script, Service Layer plus Domain Model, command bus, and durable workflow for a subscription renewal that charges a payment provider and provisions access. Select and justify a composition.

### Exercise 5

Design and review a high-stakes service operation that releases a laboratory result to a patient. Cover identity, authorization and significant-data binding, result corrections, timing, transaction/outbox, notification workflow, retries, privacy, audit, adapter equivalence, tests, and required human review.

## Answers to the Exercises

### Answer 1

After the shown calls, A=700, B=800, `R-1` recorded, and one event exists. A request for 900 passes actor/idempotency lookup but `Account.debit` returns `insufficient`; the private work is not committed, so state remains unchanged and `R-2` is not recorded. Reusing `R-2` for 100 then succeeds: A=600, B=900, `R-2` recorded, two events.

This exposes a policy choice and a missing feature. The model records only successful results, so a key can be reused after a domain rejection; production may instead record stable rejections. More critically, it stores no canonical request digest: after a committed success, the same key with a different amount would return `duplicate` rather than `key-conflict`. Add scoped unique key, digest, status, compatible stored result, and concurrent in-progress recovery atomically.

### Answer 2

Use immutable `ApproveExpense(expense_id, expected_version, decision_note, idempotency_key)`; trusted context contains authenticated manager ID/strength, tenant, action, authoritative time, deadline, correlation, and policy version. Results include approved with expense/version, duplicate, invalid, denied/non-disclosing, not found, already terminal, version conflict, limit exceeded, retry exhausted, and internal error.

The application authorizes manager-resource-action/tenant and binds any transaction challenge to expense, amount, currency, and decision. Begin one Unit of Work; load tenant-scoped expense and approval-limit evidence consistently; recheck version/authority; call `expense.approve(manager, policy)` for domain lifecycle/limit rules; persist aggregate, idempotency digest/result, protected audit, and `ExpenseApproved` outbox intent; commit once. No repository commits.

HTTP maps typed outcomes without leaking another tenant. A duplicate message constructs the same command/context, calls the operation, commits/returns duplicate, then acknowledges; no second event appears. CLI/admin uses the same operation unless a separately named override capability—with stronger authority/reason/audit—is required. Integration tests race two approvals, stale versions, same/different digest, commit uncertainty, outbox, and every adapter.

### Answer 3

The class combines application capabilities, domain pricing, transport, infrastructure effects, and hidden security context; repository count suggests several bounded contexts. Inventory methods by use case, actor/authority, transaction resources, domain language, dependencies, and change coupling. Cluster durable capabilities such as customer profile, credit decision, pricing, and communications; do not split merely by method count.

First characterize HTTP/job/admin behavior and authorization with contract/integration tests. Introduce explicit commands/results and server-built context for one high-value operation. Move HTTP mapping to adapter, pricing to values/policy/domain model, email behind an outbox-driven notification workflow, and transaction ownership into the application operation. Replace thread-local actor with explicit minimal context. Route one adapter, observe semantic diffs, then migrate remaining callers and remove bypasses.

Use a small repository/Unit of Work set per capability; query projections handle reads. Preserve compatibility/idempotency during routing and reconcile contradictory old behavior with owners. Evidence includes authorization matrix, real transaction/race/outbox tests, fault injection, telemetry comparison, and rollback plan. Split deployment only if ownership/scaling/security evidence justifies distributed failure cost.

### Answer 4

A direct controller is inadequate because renewal has multiple adapters/retries and remote effects. A pure Transaction Script can coordinate a simple local renewal but should not hold a transaction around payment/provisioning. A Service Layer defines `request_renewal`, validates/authorizes/idempotently creates a renewal workflow, and returns accepted/current result. A Domain Model owns subscription eligibility, terms, and lifecycle if rules are rich; otherwise a script/policy can suffice.

Use a durable workflow for payment and provisioning: stable renewal/payment keys, persisted states, outbox commands, deadlines, duplicate responses, unknown-outcome reconciliation, compensation/refund or manual intervention, and final notification. A command bus is optional dispatch plumbing for cross-cutting context and handlers; it adds no atomicity and should be omitted if it hides flow without benefit. HTTP/job/message adapters call the canonical Service Layer operation and map their delivery semantics.

### Answer 5

Define `ReleaseLabResult(result_id, expected_version, idempotency_key)` and trusted clinician/system actor, patient/tenant, authorization strength, authoritative time, deadline, policy/correction version, and correlation. Bind transaction authorization to significant result/patient identity where required. The domain model distinguishes preliminary, verified, corrected, withheld, and released states; it validates reviewer role, critical-result policy, effective/recorded time, correction chain, and whether immediate clinician contact is required.

In one transaction, recheck current result/version and action authority, transition release state, record idempotency/audit, and insert privacy-minimized outbox intent. Notification is a workflow after commit with patient channel consent, redaction, stable IDs, retry, delivery uncertainty, escalation, and no sensitive result in unsafe channels. A correction never overwrites history; it creates a linked version and may initiate revised release/notification under policy.

All portal, clinician UI, batch, message, and administrative adapters use the canonical operation or a separately authorized emergency capability. Tests cover actor-resource-action matrix, cross-patient/tenant guessing, stale version, corrected/withheld/critical states, same/different key, races, rollback/outbox, commit-ack loss, notification duplicates/timeouts, audit privacy, and accessibility. Named laboratory medicine, treating-clinician, privacy/legal, security, patient-safety, human-factors/accessibility, and operations reviewers must approve assumptions and workflow; automated tests do not establish clinical appropriateness or regulatory compliance.
