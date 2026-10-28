---
module_id: API-020
program: API & Service Engineering
level: 1
module_number: 20
title: Designing an API from Consumer Tasks Rather Than Database Tables
status: complete
last_verified: 2026-09-01
---

# Designing an API from Consumer Tasks Rather Than Database Tables

## One-Page Review

### Governing question

How can an API expose the stable work consumers need to accomplish without copying storage tables, internal joins, and migration history into a long-lived public contract?

### Essential definitions

- A **consumer task** is a goal an authorized consumer attempts under known preconditions, with a recognizable outcome and recovery path.
- A **task contract** states the intent, required inputs, observable result, failure meanings, and retry or correction choices for one task.
- A **domain resource** is an API-visible concept with stable identity, meaning, lifecycle, and relationships; it need not correspond to one table.
- A **command** requests a state transition whose meaning is richer than replacing stored fields.
- **persistence leakage** occurs when storage-specific columns, keys, joins, flags, or transaction boundaries become consumer obligations without domain justification.
- A **consumer-shaped representation** contains the information needed for an interaction, subject to authority and consistency, rather than mirroring one internal row.

### Central model, mechanism, or theorem

Let $T$ be admitted consumer tasks and $O$ public operations. A design is task-complete only if every $t\in T$ has at least one documented operation path that can reach its promised outcome or a defined recoverable failure. It is task-coherent when each operation has one stable purpose and its preconditions, effects, and failures can be explained without referring to private table mechanics. Start with task narratives, derive resource lifecycles and commands, and map those contracts onto storage only behind the boundary.

### Critical invariants

Every operation traces to a named consumer task and authorized actor. Public identifiers express domain identity, not accidental primary-key layout. Writes express valid state transitions rather than arbitrary column mutation. Representations expose only task-relevant authorized data. Failures tell the consumer whether to correct, retry, reconcile, or stop. Internal schema migration does not require a consumer migration unless the domain contract itself changes.

### Common failures

Generating one endpoint per table; exposing join tables as resources without domain meaning; accepting a writable copy of every column; encoding workflow in boolean flags; forcing consumers to reconstruct one task through undocumented call order; returning foreign-key and constraint names; making consumers understand internal transactions; and calling a task-based command “unRESTful” merely because it is not CRUD.

### Compact example

A consumer needs to approve an expense report. `PATCH /expense_rows/481 {"approved": true}` exposes a row flag but omits approver authority, current workflow state, policy findings, audit evidence, duplicate intent, and conflict meaning. `POST /expense-reports/481:approve` accepts the decision context, checks the transition, and returns the approved report or a task-level problem such as `policy-review-required`. **Conclusion:** the API contract names the consumer's decision while storage remains an implementation detail.

### Connections

[Outside-In API Requirements](011-outside-in-api-requirements.md) identifies consumers and outcomes. [Resource Identification](012-resource-identification.md) and [Create, Read, Update, and Delete Semantics](015-create-read-update-and-delete-semantics.md) supply resource and standard-method foundations. [Bulk and Batch Operations](019-bulk-and-batch-operations.md) handles one intent over multiple targets. The successor [API Contracts and Behavioral Guarantees](../ROADMAP.md) turns these task decisions into explicit promises.

## Governing Question

Which public concepts and operations let consumers complete real work with the least necessary coupling, while preserving HTTP semantics, authorization, failure precision, and independent implementation evolution?

## Why This Matters

A database schema answers storage questions: which facts are persisted, normalized, indexed, constrained, or joined. An API answers interaction questions: what an authorized consumer can observe or request, what outcome is promised, and what to do next. The two models overlap, but they have different owners and rates of change.

Table-shaped APIs often look productive at first. Scaffolding can generate list, get, insert, update, and delete endpoints quickly. The cost moves to every consumer. A client may need to join five endpoints, infer which flags encode a lifecycle, send fields it does not own, translate constraint errors, and coordinate a sequence that the service cannot safely make atomic. An internal column rename then becomes an external migration even though the consumer's task did not change.

Task-first design does not reject resources or standard HTTP methods. It asks what the consumer is trying to achieve, identifies stable domain resources and their lifecycles, uses standard methods where their semantics fit, and introduces a clearly named command or operation resource where a meaningful transition does not reduce to ordinary CRUD. Google AIP-121 explicitly notes that a resource-oriented API is not necessarily a database, while AIP-136 permits custom methods when standard methods do not express the intent. These are design guides, not additions to HTTP itself. RFC 9110 remains authoritative for HTTP resource, method, safety, and idempotency semantics. These current documents were checked on 2026-09-01.

## Prerequisites and Retrieval

Retrieve actors, use cases, domain language, resource identity, HTTP methods, status and problem semantics, authorization, validation, idempotency, optimistic concurrency, transactions, long-running operations, and pagination. Recall that a representation is information about a resource state, not a serialized memory object or database row. Recall also that `POST` can process a resource-specific request according to the target's semantics; it is not merely “insert a row.”

## Learning Objectives

By the end of this module, you should be able to:

1. elicit consumer tasks with actors, triggers, outcomes, and recovery paths;
2. distinguish domain resources from tables, rows, views, and join structures;
3. map tasks to standard methods, commands, or operation resources;
4. design task-relevant representations, authorization, errors, and concurrency rules;
5. detect persistence leakage and consumer-side workflow reconstruction; and
6. test whether an API remains stable across internal schema and implementation changes.

## Core Exposition

### Begin with consumer work

A consumer is a person, device, service, job, or operator acting through an API identity. Do not begin with endpoint names. Begin with a concrete narrative:

> When a verified merchant sees a captured payment that qualifies for return, it requests a refund for a stated amount and reason, then needs to know whether the refund was accepted, rejected, or requires later observation.

The narrative exposes more design information than a `refunds` table. It identifies actor qualification, trigger, target payment, amount and reason, eligibility, immediate versus deferred result, and failure recovery. Record for each task:

- actor and authority;
- trigger and desired outcome;
- prerequisite facts and state;
- required inputs and their provenance;
- observable success and acceptable latency;
- correctable, retryable, conflicting, forbidden, and uncertain failures;
- concurrency, duplicate, cancellation, and audit expectations; and
- information needed for the next decision.

Use observed workflows, support cases, integration traces, and consumer interviews as evidence. A requested endpoint is a proposed solution, not automatically the underlying task. “We need access to `invoice_status_code`” may mean “we need to know whether shipment is permitted.” The latter can lead to a stable domain decision rather than a code table consumers must decode.

### Derive resources from identity and lifecycle

A domain resource deserves public identity when consumers need to name it, retrieve or relate its state, hold a reference across interactions, control it independently, or observe its lifecycle. One resource may aggregate many tables. One table may support several resource types. Some computed resources have no dedicated table, and some internal tables have no public meaning.

Ask four questions:

1. What does the concept mean in the consumer's language?
2. What gives it identity across time?
3. Which states and transitions are externally meaningful?
4. Which relationships must consumers navigate or preserve?

An `Order` resource might combine order header, line, address snapshot, pricing, payment summary, and fulfillment projections. A `Membership` might deserve identity even if stored as a join row because consumers enroll, suspend, and terminate it. Conversely, an ORM join entity created only to implement a many-to-many relation may not deserve its own endpoint.

Public identifiers should remain opaque unless their structure is part of a deliberate contract. Composite database keys, shard prefixes, sequence values, and foreign keys can reveal topology and constrain future storage. If consumers need a business key, define its normalization, uniqueness scope, mutability, and lookup behavior separately from the service's stable resource name.

### Prefer standard semantics when they fit

Task-first does not mean verb-heavy URLs. Many tasks map cleanly to standard resource operations:

- “view the current invoice” maps to `GET /invoices/{id}`;
- “create a saved delivery address” maps to `POST /customers/{id}/addresses`;
- “replace this caller-owned preference document” can map to `PUT`;
- “change the notification channel” may map to a constrained `PATCH`; and
- “remove a draft that the caller owns” can map to `DELETE` with defined preconditions.

Preserve method semantics. A task that changes state must not hide behind `GET`. An idempotent replacement should not be made unpredictably non-idempotent. A resource name and method together communicate intent; the URI does not override the method properties defined by HTTP.

Standard methods work best when the consumer can validly express desired resource state and owns the fields being changed. They work poorly when a transition needs domain authorization, evaluates policy, produces side effects, or has a result different from an ordinary representation update.

### Model commands and operation resources deliberately

Use a command when the consumer asks the service to decide or perform a domain transition: approve, capture, suspend, rotate, reconcile, publish, or close. The request should contain intent and evidence, not internal target columns. The service validates the transition against current state, authority, policy, and concurrency.

A resource-bound custom method such as `POST /expense-reports/{id}:approve` makes the target and verb explicit. A command resource such as `POST /refund-requests` is useful when the request itself has identity, lifecycle, cancellation, audit, or asynchronous observation. Both designs can be sound. Choose according to what consumers must name and observe, not by a blanket ban on verbs.

Commands require precise contracts:

- whether submission is idempotent and how duplicates are recognized;
- required state and version of the target;
- authorization evaluated at acceptance and, if delayed, execution;
- committed effects and transaction boundary;
- synchronous result or operation resource;
- conflict, rejection, uncertainty, and retry meanings; and
- resulting links and next permitted actions.

Do not invent custom methods for ordinary retrieval or replacement. Consistency and generic tooling are valuable when standard semantics fit. Microsoft Azure's published API guidance likewise distinguishes resource state operations from action patterns; it is organizational guidance rather than an HTTP standard.

### Design representations around decisions

A consumer-shaped representation answers the next legitimate question with a coherent consistency story. It can combine stored, computed, and linked facts. It must not expose every internal column “in case someone needs it,” nor require one request for each normalized table.

Separate fields by ownership:

- **consumer-supplied intent**, which the caller may set;
- **service-derived state**, which is read-only;
- **policy or authority data**, which may be visible only in summarized form;
- **links and affordances**, which identify related resources or permitted next actions; and
- **operational metadata**, such as versions and timestamps with defined meaning.

Avoid writable representations that deserialize directly into persistence models. Mass assignment can let a caller set tenant, price, role, approval, audit, or lifecycle fields it does not own. Define request schemas per operation. Response schemas may share components, but request authority must remain explicit.

A task view can reduce chattiness, but it is not a license for an unbounded “everything” document. Bound cardinality, paginate collections, link to large related data, and state freshness. If different consumers need materially different decisions, separate projections or query capabilities may be clearer than one unstable union of all fields.

### Make workflows visible without scripting internals

Some tasks require several public interactions. The question is whether each step reflects a real consumer decision or merely compensates for internal decomposition. A checkout consumer may legitimately choose an address, select a payment instrument, review a quote, and confirm an order. It should not need to insert order rows, line rows, tax rows, ledger rows, and outbox rows in an undocumented sequence.

Expose lifecycle states that matter to decisions, not raw flags. `state: "awaiting_review"` with a documented transition model is clearer than `submitted=true`, `approved=false`, `rejected=false`, `locked=true`, whose combinations may be invalid. If the service can own a multi-step invariant, give it one task-level operation. If a human or external authority must decide between steps, expose a durable resource and next-action contract.

Do not promise a transaction larger than the implementation can provide. A task can be accepted synchronously and completed asynchronously through an operation resource. The consumer contract then covers acceptance, observation, terminal states, idempotency, cancellation, and reconciliation rather than pretending one response contains a cross-system commit.

### Specify failures in task language

Storage errors are evidence for the service, not public semantics. `duplicate key value violates uk_8291` does not tell a consumer whether the business identifier already names the same resource, another resource, or an unauthorized resource. Translate failure into a stable problem type and safe detail.

A useful task contract distinguishes:

- **invalid input**: correct the request before retrying;
- **failed precondition**: establish a required condition or choose another task;
- **state conflict**: refresh current state or version and reconsider;
- **forbidden intent**: do not retry without changed authority;
- **rate or capacity limit**: retry only under the supplied policy;
- **accepted and pending**: observe the operation resource; and
- **unknown outcome**: reconcile using request identity before repeating an effect.

Do not expose table names, constraint names, SQL fragments, internal IDs, or whether a hidden record exists. Problem types and fields are part of the API contract and should trace to consumer recovery behavior.

### Treat authorization as part of the task

Authorization is not a filter attached after data access. Define who may request the task, on which target, in which tenant or relationship, under which current state, and which result fields they may observe. A caller allowed to initiate an investigation may not be allowed to view confidential findings. A caller allowed to edit contact details may not set verification status.

Task-based request schemas make authority review tractable because each input has a reason. Table-shaped generic updates make it easy to overpost. Object-level checks still apply even when an operation is named well. For collections, authorize the candidate universe before filtering, counting, and pagination to avoid disclosure.

### Evaluate the design with a task-operation matrix

Create a matrix whose rows are prioritized tasks and whose columns are public operations. Mark which operation starts, advances, observes, cancels, or recovers each task. The matrix exposes missing tasks, duplicate operations, undocumented sequences, and generic endpoints with unrelated responsibilities.

The following bounded model checks only declared coverage and operation purpose. It cannot establish usability, authorization correctness, or production fitness.

<!-- bijux-verify: {"id":"task-operation-coverage","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"approve_expense: approve_expense\ncorrect_expense: revise_expense\nobserve_decision: get_expense\nrefund_payment: request_refund\ncoherent_operations=4\ncovered_tasks=4\nevidence=declared_task_operation_matrix\n","stderr":""}} -->
```python
tasks = {
    "approve_expense": "approved_or_rejected",
    "correct_expense": "revised_draft",
    "observe_decision": "current_expense_state",
    "refund_payment": "refund_request",
}

operations = {
    "approve_expense": {"purpose": "decision", "outcomes": {"approved_or_rejected"}},
    "revise_expense": {"purpose": "correction", "outcomes": {"revised_draft"}},
    "get_expense": {"purpose": "observation", "outcomes": {"current_expense_state"}},
    "request_refund": {"purpose": "compensation", "outcomes": {"refund_request"}},
}

coverage = {}
for task, required_outcome in tasks.items():
    candidates = [
        name for name, contract in operations.items()
        if required_outcome in contract["outcomes"]
    ]
    assert len(candidates) == 1
    coverage[task] = candidates[0]
    print(f"{task}: {candidates[0]}")

assert all(contract["purpose"] for contract in operations.values())
print(f"coherent_operations={len(operations)}")
print(f"covered_tasks={len(coverage)}")
print("evidence=declared_task_operation_matrix")
```

Coverage is necessary but not sufficient. Review task frequency, consequence, complexity, and evidence. Observe completion rate, retries, support contacts, abandoned workflows, authorization failures, and incompatible client workarounds. Metrics reveal friction; they do not decide the correct contract without qualitative investigation.

### Preserve an anti-corruption boundary

Implement adapters that translate public requests into application commands and domain operations, then translate outcomes into public representations and problems. The boundary may join tables, call services, maintain projections, or enqueue work. Consumers should not know which mechanism was used unless it changes an explicit guarantee.

Test the boundary with a schema-change thought experiment. Split one table, merge two tables, replace a relational store with a document projection, or introduce an internal queue. If public fields, call order, or error meanings must change even though consumer tasks and domain rules did not, the contract probably leaks persistence.

The inverse test matters too: a domain change can require an API change even if the table remains stable. If refund eligibility gains a mandatory consent decision, keeping the same columns does not preserve the task contract. API evolution follows public meaning, not migration count.

## Definitions and Notation

Let $C$ be consumer roles, $T$ admitted tasks, $R$ public resources, and $O$ public operations. For task $t\in T$:

- $actor(t)\in C$ identifies the authorized role;
- $pre(t)$ is the declared precondition predicate;
- $goal(t)$ is the observable desired outcome;
- $recover(t)$ is the set of defined recovery choices; and
- $path(t)=(o_1,\ldots,o_k)$ is a documented sequence of public operations.

Task completeness requires:

$$
\forall t\in T,\;path(t)\ne\varnothing
$$

and every terminal result of the path must either establish $goal(t)$ or select a failure with a defined recovery or stop decision. This is a specification obligation, not a proof that an implementation always succeeds.

For operation $o$, let $I_o$ be accepted intent fields, $E_o$ observable effects, $F_o$ failure meanings, and $A_o$ its authorization predicate. Let $D_o$ be internal persistence fields touched by an implementation. Persistence leakage exists when a field in the public contract is justified only by membership in $D_o$, rather than by intent, observation, concurrency, or recovery needs. The sets are review aids; they are not a universal numeric quality score.

A **task card** records actor, trigger, goal, inputs, preconditions, success, failures, recovery, and evidence. A **task-operation matrix** traces tasks to public operations. A **domain resource** has consumer-relevant identity and lifecycle. A **projection** is a read model shaped for a query or decision. An **anti-corruption boundary** translates between public language and internal models. A **command** requests a domain transition. An **affordance** tells a consumer which meaningful interaction is available without granting authority by itself.

## Mechanisms, Invariants, or Proof Structure

1. Identify prioritized consumers and observed tasks rather than collecting endpoint wishes.
2. Write task cards with authority, preconditions, outcomes, failures, and recovery.
3. Derive domain resources from stable identity, meaning, lifecycle, and relationships.
4. Map ordinary state retrieval and manipulation to standard HTTP methods where semantics fit.
5. Introduce commands or operation resources for domain transitions and asynchronous work.
6. Design operation-specific requests and task-relevant authorized representations.
7. Translate storage failures into stable task-level problem meanings.
8. Build the task-operation matrix and remove gaps, overlaps, and undocumented scripts.
9. Test concurrency, duplicates, partial effects, authorization, and schema-change independence.
10. Observe consumer outcomes and evolve the contract by domain meaning.

The **traceability invariant** requires every operation to have a named task and actor. The **authority invariant** requires every accepted input and exposed output to be justified for that actor. The **transition invariant** permits only domain-valid state changes. The **recovery invariant** gives consumers a defined response to every public failure category. The **encapsulation invariant** keeps internal storage changes behind the boundary when public meaning is unchanged.

## Alternatives and Trade-Offs

**Table-first scaffolding versus task-first design.** Scaffolding is fast for private administration or disposable prototypes. Task-first design costs discovery and modeling but reduces consumer coupling and authority ambiguity. A generated internal API can still sit behind a deliberate public boundary.

**Standard method versus custom command.** Standard methods provide familiar, reusable semantics. Commands express transitions that cannot honestly be represented as ordinary state replacement. Prefer the standard method when it fits; prefer a precise command over pretending a policy decision is a field edit.

**Fine-grained resources versus task projection.** Fine-grained resources support reuse and independent caching, but can force client joins and inconsistent snapshots. A projection answers one decision coherently but may duplicate data and need explicit freshness. Often the best design uses stable resources plus bounded task views.

**Orchestration endpoint versus client workflow.** Server orchestration protects invariants and hides internal steps. Client-visible steps are appropriate when the consumer supplies a real decision between them. Do not centralize decisions the consumer owns or externalize steps the service owns.

**One universal representation versus operation-specific schemas.** Reuse reduces schema count, but a universal writable model invites overposting and unstable optional fields. Operation-specific requests clarify authority and validation at the cost of more contract components.

## Failure Modes and Misconceptions

REST does not mean one public resource per table. CRUD is a useful operation family, not a complete requirements method. A noun-shaped URL does not repair an incoherent task. A command is not automatically RPC-style coupling; vague behavior and unstable semantics cause coupling. Hiding every domain state is not encapsulation when consumers need it for decisions. Returning more columns does not create flexibility if consumers become dependent on them. A backend-for-frontend can tailor representations but does not excuse an incoherent underlying domain contract. GraphQL can reduce field over-fetching while still exposing a table-shaped graph. An ORM entity is not evidence of public identity. “The UI can orchestrate it” is not a justification for leaking service-owned workflow.

## Worked Examples

### Example 1

**Situation:** A generated API exposes `PATCH /expense_rows/{id}` with writable `approved`, `approver_id`, and `approved_at`. **Reasoning:** The consumer owns the approval intent, not the approver identity or authoritative time. Model `POST /expense-reports/{id}:approve`, derive actor and time from trusted context, check workflow state, and return the resulting report or task-level problem. **Conclusion:** operation-specific intent prevents mass assignment and expresses the decision.

### Example 2

**Situation:** An order read requires calls to order header, lines, addresses, discount rows, and shipment tables. **Reasoning:** The consumer needs one coherent order decision view. Aggregate stored and computed facts into an order representation, link large shipment history separately, and state snapshot/freshness behavior. **Conclusion:** normalization inside storage does not require consumer-side joins.

### Example 3

**Situation:** A many-to-many `team_user` table has `joined_at`, role, suspension, and invitation state. **Reasoning:** Those fields form a consumer-relevant lifecycle, so a `Membership` resource may be justified even though its implementation began as a join table. **Conclusion:** table correspondence is neither necessary nor sufficient; identity and lifecycle decide.

### Example 4

**Situation:** A client wants to change an email address. **Reasoning:** If the task merely replaces caller-owned contact data, a constrained `PATCH` fits. If change requires challenge delivery and confirmation, create or invoke a verification workflow and expose its status. **Conclusion:** choose the operation from the actual transition, not the field name.

### Example 5

**Situation:** `GET /accounts/{id}/close` closes an account because the path contains a verb. **Reasoning:** HTTP assigns safety semantics to the method, not the spelling of the URI. Crawlers and retries may issue `GET`; the action changes state. Use an unsafe method with explicit preconditions and outcome. **Conclusion:** task-first design still obeys HTTP method semantics.

### Example 6

**Situation:** A unique constraint fails while registering a username. **Reasoning:** The service must avoid disclosing another account and must not expose a constraint name. Return a stable `username-unavailable` problem, or a privacy-preserving validation result, with correction guidance. **Conclusion:** storage errors are translated into safe task recovery.

### Example 7

**Situation:** A mobile client sets `submitted=true`, then separately creates line items and an audit record. **Reasoning:** Submission is one service-owned invariant over a complete draft. A submit command validates required lines, freezes the accepted version, records trusted audit evidence, and returns submitted state atomically within the declared boundary. **Conclusion:** consumers should not script private transaction structure.

### Example 8

**Situation:** A refund may take minutes and cross a payment provider. **Reasoning:** `POST /refund-requests` gives the request identity, deduplicates intent, and returns an operation or refund-request resource whose terminal states include succeeded, rejected, and reconciliation-required. **Conclusion:** a task resource can express durable work that no table-shaped synchronous update can promise.

### Example 9

**Situation:** An internal migration splits `customers` into identity, profile, and preferences tables. **Reasoning:** Public customer identifiers, task requests, representations, and problem types remain stable through an adapter and projection. Only internal queries and transactions change. **Conclusion:** unchanged domain meaning should permit storage evolution without consumer releases.

### Example 10

**Situation:** Support logs show consumers calling five endpoints, caching undocumented codes, and retrying conflicts blindly. **Reasoning:** Map the intended task, add a coherent decision projection, define code meanings or replace them with stable domain values, and return recovery-specific conflicts. Measure whether completion and support burden improve. **Conclusion:** consumer workarounds are evidence for redesign, not features to copy uncritically.

## Cross-Program Connections

[Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) supplies domain language and boundaries. [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) owns system-wide decomposition. [Database Engineering](../../18-database-engineering/ROADMAP.md) owns persistence models and transactions. [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies threat and authorization analysis. [Platform Engineering](../../29-platform-engineering/ROADMAP.md) treats APIs as consumer-facing platform products. This module owns the translation from consumer tasks into externally observable API contracts.

## References

1. R. Fielding, M. Nottingham, and J. Reschke, [*RFC 9110: HTTP Semantics*](https://www.rfc-editor.org/rfc/rfc9110.html), Internet Standard, June 2022, especially Sections 3 and 9. Checked 2026-09-01.
2. Google, [*AIP-121: Resource-Oriented Design*](https://google.aip.dev/121), approved guidance, created 2019-01-26. Current published page checked 2026-09-01.
3. Google, [*AIP-136: Custom Methods*](https://google.aip.dev/136), approved guidance, created 2019-01-25. Current published page checked 2026-09-01.
4. Microsoft, [*Azure REST API Guidelines*](https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md), sections on REST and action patterns. Current `vNext` guidance checked 2026-09-01.
5. Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software*. Addison-Wesley, 2003. Used for durable domain language and anti-corruption-layer foundations.

## Exercises

### Exercise 1

For a library API, distinguish the consumer tasks “view a book description,” “borrow an available copy,” “renew a loan,” and “record a catalog row.” Identify which are genuine public tasks and which phrase leaks implementation.

### Exercise 2

A table-shaped endpoint accepts `PATCH /payments/{id}` with fields `status`, `captured_at`, `failure_code`, and `version`. Redesign capture as a task contract. State actor, inputs, preconditions, success, conflicts, idempotency, and safe failures.

### Exercise 3

Create a task-operation matrix for submitting, correcting, approving, and observing an expense report. Identify one operation that would be incoherent if it attempted to serve several of these tasks.

### Exercise 4

Compare these designs for changing a verified phone number: direct `PATCH`, a bound verification command, and a verification resource. Choose one for a system requiring an expiring challenge and audit history, and justify its HTTP and lifecycle semantics.

### Exercise 5

A logistics API mirrors `shipment`, `shipment_leg`, `carrier_event`, `warehouse_scan`, and `exception_code` tables. Consumers need to answer “Where is this parcel, is action required, and what can I do?” Propose a task-first boundary that can survive a storage redesign. Include representation, commands, authorization, freshness, errors, and migration test.

## Answers to the Exercises

### Answer 1

Viewing a description is a retrieval task over a publicly identifiable catalog resource. Borrowing is a domain transition that checks patron authority, copy availability, limits, and due-date policy; it may create a `Loan` resource. Renewal is a transition on an existing loan with holds and renewal-limit preconditions. “Record a catalog row” names storage rather than a consumer outcome; a catalog maintainer might instead create or revise a bibliographic record under an explicit authority and validation contract. The first three are genuine tasks. The fourth must be reframed before choosing an operation.

### Answer 2

Use a contract such as `POST /payments/{id}:capture` or create a capture request when durable observation is needed. The actor is an authorized merchant principal. Inputs include amount when partial capture is allowed, currency constraint, merchant reference, and an idempotency key; trusted time and final status are not writable inputs. Preconditions include an authorized payment state, remaining capturable amount, target version or equivalent concurrency rule, and merchant ownership. Success returns the captured payment and receipt/reference. Same-intent duplicate submission returns the existing result; key reuse for different intent conflicts. Stable failures distinguish invalid amount, already captured, expired authorization, version conflict, forbidden target, provider rejection, rate limit, and unknown provider outcome requiring reconciliation. Internal failure codes may be logged but are not copied blindly into the public contract.

### Answer 3

Rows are: submit draft, correct rejected/draft report, approve submitted report, and observe current report/decision. Suitable columns are `submit`, constrained `revise` or `PATCH`, `approve`, and `GET report`. Each row has one primary operation, while observation may follow any transition. A generic `PATCH report` that allows arbitrary changes to draft fields, submission state, approval state, approver, timestamps, and findings is incoherent: it combines consumer correction with authority-sensitive decisions and service-derived evidence. Split request schemas and transitions so each operation has one purpose and authorization rule.

### Answer 4

A direct `PATCH` is suitable only if the phone number can become authoritative immediately. A bound command can start verification, but the expiring challenge and audit history have identity and lifecycle that consumers may need to observe. Create `POST /phone-verifications` with target phone and account context, return the verification resource, accept challenge confirmation through a constrained transition, and expose pending, verified, expired, and attempt-limited states. Submission is unsafe and should use `POST`; duplicate intent needs an idempotency policy. The account's verified phone changes only on successful confirmation. The resource design makes expiry, retry, audit, and observation explicit without exposing challenge secrets.

### Answer 5

Expose a stable `Parcel` or `Shipment` resource keyed by an opaque public identifier. Its task view contains current journey state, last meaningful event and observed time, estimated delivery with freshness, action-required summary, safe exception category, and links to bounded history and permitted actions. Commands might include `reschedule-delivery`, `provide-instructions`, or `acknowledge-customs-request`, each with actor, state, idempotency, and conflict rules. Authorize parcel access before returning location or recipient data; restrict carrier and warehouse evidence by role. State event-delay and projection freshness rather than implying live truth. Translate missing scans, invalid transitions, stale versions, and carrier uncertainty into task-level problems. The migration test replaces the five tables with an event stream plus projections while keeping identifiers, representations, commands, and problem meanings unchanged. If consumers must change only because event storage changed, persistence has leaked.
