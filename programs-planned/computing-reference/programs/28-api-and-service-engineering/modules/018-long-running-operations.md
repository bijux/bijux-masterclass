---
module_id: API-018
program: API & Service Engineering
level: 1
module_number: 18
title: Long-Running Operations
status: complete
last_verified: 2026-09-01
---

# Long-Running Operations

## One-Page Review

### Governing question

How should an API accept work that cannot be completed during one request while making its identity, progress, result, failure, cancellation, retention, and retry behavior precise?

### Essential definitions

- A **long-running operation** (LRO) is a server-accepted unit of work whose outcome is retrieved later.
- An **operation resource** is the API representation that names and reports that unit of work.
- **Acceptance** means the server has taken responsibility under a stated durability policy; it does not mean success.
- A **terminal state** has a final outcome: succeeded, failed, cancelled, or expired under the contract.
- An **idempotency key** associates repeated client submission attempts with one logical requested effect.
- A **compensation** is a separate corrective action; it is not a magic rollback of irreversible effects.

### Central model, mechanism, or theorem

Model an operation as a state machine $S=\{accepted,running,succeeded,failed,cancelled,expired\}$. A submission creates a durable operation identifier $o$. State transitions are monotone toward a terminal state, except that observable progress may increase while the operation is nonterminal. The operation representation is the source of truth for its outcome; a `202 Accepted` response is only an acknowledgement of later processing.

### Critical invariants

An operation has one stable identity, an explicit requester/authorization scope, bounded retention, and a defined deduplication key scope. Success exposes a result or result link; failure exposes a safe problem representation; cancellation is a request with a documented race. Polling is bounded and backs off. Events, callbacks, and polling are alternative observations of the same state, not independent state machines.

### Common failures

Holding an HTTP request open for minutes; interpreting `202` as eventual success; returning a transient worker identifier as public identity; accepting duplicate charges on retry; reporting a percentage with no denominator; deleting the result before the client can retrieve it; allowing anyone who guesses an ID to poll; treating cancellation as guaranteed rollback; and emitting progress events that disagree with `GET`.

### Compact example

`POST /exports` validates a request and returns `202 Accepted`, `Location: /operations/op_7f`, and a representation with `state: "accepted"`. `GET /operations/op_7f` later reports `running`, then `succeeded` and links `result` to a retained export. Repeating the original request with the same idempotency key returns the same operation rather than starting another export.

### Connections

[Create, Read, Update, and Delete Semantics](015-create-read-update-and-delete-semantics.md) defines request effects; [Partial Updates](016-partial-updates.md) supplies conditional state changes; [Filtering, Sorting, and Pagination](017-filtering-sorting-and-pagination.md) supplies bounded observation of operation collections. Distributed systems adds durable queues, leases, retries, and exactly-once limits.

## Governing Question

What public operation resource and lifecycle let a client safely submit, observe, retry, cancel, and retrieve expensive work when networks, workers, and client processes can all fail independently?

## Why This Matters

A request-response exchange is a poor container for an export, model build, migration, media transformation, or fan-out workflow that might outlive a connection, gateway timeout, deployment, or client process. Keeping the connection open hides the failure boundary: the client cannot tell whether a timeout happened before acceptance, during work, or after a side effect.

HTTP defines `202 Accepted` as a response whose processing has not been completed and notes that it is intentionally noncommittal about eventual action. It therefore cannot by itself answer “did it succeed?” An API needs a named resource that can answer later. `Location` identifies a URI for a response-related resource, while Web Linking provides typed relationships for results and controls. These standards supply protocol vocabulary, not a universal job schema. [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html) and [RFC 8288](https://www.rfc-editor.org/rfc/rfc8288.html) were checked on 2026-09-01.

The design is consequential: an ambiguous retry can duplicate money movement or provisioning; a misleading progress meter can trigger unsafe manual intervention; and an unprotected operation identifier can disclose another tenant’s activity. Treat the LRO as a real API resource, not as a background implementation detail.

## Prerequisites and Retrieval

Retrieve HTTP request/response semantics, `POST`, `GET`, `DELETE`, status classes, resource identity, authorization, cache controls, idempotence, optimistic concurrency, queues, transactions, leases, backoff, failure domains, and the difference between a durable record and an in-memory task. Recall that transport acknowledgement and business completion are distinct events.

## Learning Objectives

By the end of this module, you should be able to:

1. distinguish acceptance, execution, and final business outcome;
2. specify an operation resource, state machine, and terminal representations;
3. select polling, event, callback, or result-delivery observation mechanisms;
4. design idempotent submission and safe retry behavior;
5. state cancellation, compensation, timeout, and retention semantics;
6. prevent operation enumeration and cross-tenant disclosure; and
7. test crashes, duplicate delivery, stale observers, and terminal-state races.

## Core Exposition

### Separate submission from completion

An API submits an intent; a worker or workflow eventually attempts it. At least four moments may differ: the server receives bytes, validates and durably accepts intent, begins execution, and reaches a business outcome. A lost response after durable acceptance is the classic ambiguity: retrying might be essential, but naive resubmission might duplicate work.

Use synchronous completion only when the operation fits the advertised latency and failure envelope. Otherwise create an operation resource durably enough that, after acceptance is reported, an authorized client can retrieve its status through a restart or worker failover. A queue message alone may not be adequate public evidence if it can disappear or lacks a stable public identifier.

`202 Accepted` is appropriate when acceptance occurred but completion is pending. A service may instead return `201 Created` when it has created the operation resource and wants that creation semantics to be explicit. The important contract is not a fashionable status code: it is the documented meaning of acknowledgment, identifier, and later representation.

### Design the operation representation

Expose stable fields that clients need to make decisions: operation `id`, state, creation and update times, request identity/correlation identifier, optional bounded progress, terminal outcome, and links to result or problem. Do not expose worker hostnames, broker offsets, raw SQL, stack traces, or transient queue handles as public protocol.

Represent progress only if it is meaningful. A percentage must state its denominator and whether it can pause, regress, or be revised. For a discovery crawl with unknown frontier size, phase plus counters may be more honest than `73%`. Progress is observational evidence, not a delivery guarantee; the terminal state wins if an old event and a later `GET` disagree.

Define legal state transitions. One useful model is `accepted -> running -> {succeeded, failed, cancelled}` and `accepted -> cancelled`; `expired` is a retention outcome that can occur after a terminal record's retention period. Avoid state names that encode implementation stages unless those stages are durable client commitments. Make unknown future states safely ignorable or explicitly fail clients according to a versioning policy.

### Make the lifecycle durable and observable

The operation record needs a durability boundary. For a database-backed service, an outbox or equivalent coordinated handoff can record the operation and the command to execute without claiming an atomic transaction across unrelated systems. A worker lease prevents concurrent ownership but does not by itself prevent duplicate external effects after a crash.

Use retries inside execution only where effects are idempotent or protected by a downstream idempotency key. Persist enough attempt and outcome evidence to distinguish “not started,” “attempt uncertain,” and “known failed.” An API cannot generally promise exactly-once execution across client, service, queue, and external side effect; it can provide an operation identity, deduplicate submission, and design effects for safe repetition.

`GET /operations/{id}` is the simplest observation interface. Supply a bounded polling recommendation in documentation or representation; `Retry-After` has standardized semantics for 3xx and 503 responses, but using it on an operation response is an application convention that must be documented rather than represented as an HTTP-wide guarantee. Clients should apply jitter and upper bounds and stop when their own deadline expires.

For lower latency, events, server-sent streams, webhooks, or callbacks can notify clients. They require reconnect/replay rules, ordering semantics, acknowledgement policy, authentication, signature verification, delivery retry, and a polling fallback. Notification means “recheck the operation”; it must not be the sole evidence of success.

### Define completion, result, and failure

Success can inline a small immutable result, link to a resource created by the operation, or link to a result artifact. State which result is authoritative and how long it remains available. For an export, the operation might succeed even if a later signed-download URL expires; the durable result resource should make that distinction visible.

Failure needs a stable machine-readable category, a safe human explanation, retryability, and correlation data. RFC 9457 defines the `application/problem+json` format for HTTP API problem details; an LRO can use the same shape inside its terminal representation, but it must not leak internal secrets or confuse a failed operation with an HTTP error returned by the polling endpoint. A `GET` that successfully reports `state=failed` can still be `200 OK` because retrieval succeeded.

Set both execution deadline and retention deadline. A timed-out execution must say whether work was stopped, whether outcome is uncertain, and which reconciliation path exists. Retention expiry should be distinguishable from “never existed” only where disclosure policy permits. Preserve audit metadata as required without keeping sensitive results indefinitely.

### Submission retries and idempotency

An idempotency key has a scope: principal or tenant, endpoint/operation type, canonicalized request identity, and retention window. On the first accepted submission, store key, request fingerprint, operation ID, and initial response. A repeat with the same key and same fingerprint returns the original operation. A repeat with the same key but a different semantic request is a conflict, not a new operation.

Do not define idempotency only as “the client retries quickly.” Network paths can duplicate a request later, and retries can cross deployments. Define maximum key length, entropy expectation, expiration, whether keys are secret, and behavior after expiry. A key prevents duplicate *submission* under its contract; it does not automatically deduplicate a worker's downstream external effect.

For naturally idempotent target-state operations, a client-selected resource identifier or conditional write may be a better identity mechanism. For non-idempotent commands such as “charge” or “send,” operation identity plus downstream deduplication is usually necessary.

### Cancellation is a race, not an undo button

Expose cancellation as an explicit operation-specific action, often `POST /operations/{id}:cancel`, rather than pretending that deleting a status record necessarily stops work. A cancellation request can race completion. Define outcomes: accepted cancellation, already terminal, cancellation unavailable, or cancellation requested but not guaranteed until the state becomes terminal.

Some work is interruptible before commit; some has crossed an irreversible boundary. If effects may remain, report them and provide a separate compensation action with its own operation and authorization. Never label compensation “rollback” unless atomic rollback is actually guaranteed across every affected effect.

Guard cancellation against stale clients with ownership/authorization checks and, where useful, an operation version or conditional request. Do not permit cancellation merely because the caller knows an identifier.

### Security, privacy, and resource governance

Authorize creation, observation, result retrieval, and cancellation independently. An operation can change ownership through delegated work, and result access can require stronger permission than status. Use unguessable IDs as defense in depth, but authorization remains mandatory. Error behavior should not turn `404` versus `403` into a tenant enumeration oracle without an explicit policy.

Bound request body, requested workload, queued items per principal, execution duration, result size, polling rate, callback targets, and retained artifacts. Callback URLs are particularly dangerous: validate allowed destinations, prevent internal-network requests, require signatures, and limit redirects. Record correlation IDs and auditable actor data without putting credentials or personal payloads in status text.

Avoid caching personalized operation status in shared caches. If caching is permitted, declare validators and `Vary` dimensions so a response cannot cross authorization contexts. Clients must be able to tolerate stale progress but must not act on it as an irreversible authorization decision.

### Test the contract at failure boundaries

Test lost response after durable acceptance, duplicate submissions, queue redelivery, worker crash before and after external side effects, result-write failure, authorization revocation, cancellation races, expired records, event reordering, and stale cache reads. Assert a client-visible outcome for each case, not merely an internal log message.

Measure acceptance latency, queue delay, execution duration, terminal failure category, duplicate-key hit rate, retry attempts, cancellation latency, polling load, notification delivery lag, and age of nonterminal operations. Alerts should distinguish a healthy long operation from a stuck one by contract-specific deadlines and progress evidence.

## Definitions and Notation

Let $o$ be an operation identifier and $s(o,t)$ its observed state at time $t$. Let $T=\{succeeded,failed,cancelled,expired\}$ be terminal states. A lifecycle is valid when $s(o,t)\in T$ implies no later state changes the completed business outcome. Let $k$ be an idempotency key and $h(r)$ a canonical semantic request fingerprint. The submission invariant is $k\mapsto(h(r),o)$ within its scope and retention interval: a repeat with equal fingerprint returns $o$; unequal fingerprints are rejected.

**Acceptance** is a policy commitment to retain enough state for later observation, not a guarantee of success. **Polling** repeatedly retrieves the operation representation. **Lease** is time-bounded worker authority and requires fencing or idempotent effects to resist stale workers. **Compensation** creates a new effect intended to counter a previous one. **Retention** defines how long status, result, and audit evidence persist.

## Mechanisms, Invariants, or Proof Structure

1. Validate authorization, input bounds, and semantic request identity before acceptance.
2. Persist operation identity and idempotency mapping at the stated acceptance boundary.
3. Return a representation or location that authorized clients can later retrieve.
4. Dispatch work with a durable handoff and lease/attempt policy.
5. Make externally visible effects idempotent, conditional, or reconcilable.
6. Publish monotone lifecycle transitions and treat the operation resource as authoritative.
7. Bind result, problem, cancellation, and retention policies to that identity.
8. Offer bounded polling and optional notifications with replay/fallback semantics.
9. Authorize every lifecycle action and govern resources throughout retention.
10. Exercise crash, duplicate, race, expiry, and disclosure cases.

The **identity invariant** gives one public name to one logical request. The **durable-acceptance invariant** prevents an acknowledged operation from vanishing after restart. The **terminal-outcome invariant** prevents success becoming failure because a later observer retries. The **idempotency invariant** prevents same-key same-intent resubmission from creating a second operation. The **observation invariant** makes notifications subordinate to retrievable state.

## Alternatives and Trade-Offs

**Synchronous wait versus operation resource.** Waiting minimizes client steps for short bounded work but couples the outcome to connection and gateway lifetimes. An LRO introduces polling and retention but makes failure and recovery observable.

**Inline result versus result link.** Inline results are simple and can be immutable; links handle large, delayed, or separately authorized artifacts. A link requires explicit retention and authorization semantics.

**Self-contained operation token versus server record.** A signed token can carry small immutable context, but mutable status still needs state. A server record supports cancellation, audit, and retention at the cost of storage and cleanup.

**Polling versus callback/event.** Polling is robust and client-controlled but creates repeated load. Push reduces apparent latency but adds delivery and replay failures. Mature APIs commonly provide polling as the correctness path and push as acceleration.

**Cancellation versus compensation.** Cancellation conserves work when interruption is possible. Compensation acknowledges that some effects cannot be undone atomically and must be repaired through a new deliberate workflow.

## Failure Modes and Misconceptions

`202` does not promise success. A job queue is not automatically an API resource. HTTP request idempotence and application command deduplication are different. An operation ID is not authorization. A percentage is not evidence of completion. A worker lease is not exactly-once effect delivery. A cancellation endpoint cannot guarantee undo after an irreversible step. A webhook delivery is not the final truth. A `200` response to `GET` can correctly contain a failed operation, because status retrieval itself succeeded.

## Worked Examples

### Example 1

A video export takes five minutes, but the load balancer times out at sixty seconds. `POST /exports` durably creates `op_41`, returns `202`, and supplies its location. The export later either links a file or records failure. **Conclusion:** an operation resource separates acceptance from a connection lifetime.

### Example 2

The server writes an operation record, enqueues work, then its response is lost. The client retries with idempotency key `k9`; lookup finds the same request fingerprint and returns `op_41`. **Conclusion:** retry safety requires a durable submission identity before acknowledgement.

### Example 3

A client reuses `k9` for a different export filter. The stored fingerprint differs, so the API returns a conflict describing key reuse rather than attaching the new request to `op_41`. **Conclusion:** an idempotency key must bind to request semantics, not just a string.

### Example 4

A migration reports 80% after copying 800 of 1,000 known rows. A new source partition is discovered, raising total work to 1,200. The representation changes phase and explains that percentage is recalculated. **Conclusion:** progress needs denominator and revision semantics.

### Example 5

A worker calls a payment provider, the provider succeeds, and the worker crashes before storing success. Redelivery runs again. The worker sends the operation ID as the provider idempotency key; the provider returns the original charge outcome. **Conclusion:** queue redelivery needs downstream effect deduplication.

### Example 6

Client A receives an event saying `succeeded`, but a delayed cache shows `running`. The event carries `op_41`; client A rechecks an authorized uncached status endpoint and obtains the terminal representation. **Conclusion:** notifications accelerate observation but do not replace authoritative retrieval.

### Example 7

An administrator cancels an import just as its final database transaction commits. The cancellation action returns “request received”; the operation then becomes `succeeded` and explains that the commit preceded cancellation. **Conclusion:** cancellation is a race with documented terminal resolution.

### Example 8

An export succeeds and creates a 2 GB artifact. The temporary download URL expires after fifteen minutes, while the result resource remains for seven days and can mint a new authorized URL. **Conclusion:** operation success, result retention, and delivery-link lifetime are separate contracts.

### Example 9

Tenant B guesses `op_41`. The service evaluates tenant and actor policy before returning a representation and uses its chosen non-disclosure error policy. **Conclusion:** unguessable identifiers complement, never replace, authorization.

### Example 10

A webhook receiver is offline for three hours. The API retries signed notifications with bounded backoff, but the client eventually polls `op_41` and obtains the final result. **Conclusion:** a durable pull path makes notification loss recoverable.

## Cross-Program Connections

[Create, Read, Update, and Delete Semantics](015-create-read-update-and-delete-semantics.md) distinguishes command acceptance from resource state. [Partial Updates](016-partial-updates.md) informs conditional lifecycle writes, and [Filtering, Sorting, and Pagination](017-filtering-sorting-and-pagination.md) supports operation-history traversal. Systems engineering owns queues, leases, and crash recovery mechanisms; API engineering owns the public lifecycle contract. Security engineering owns callback and authorization threat models; data engineering owns durable execution and result retention mechanisms.

## References

1. R. Fielding et al., *RFC 9110: HTTP Semantics*, Standards Track, June 2022, Sections 10.2.2, 10.2.3, and 15.3.3. Checked 2026-09-01. https://www.rfc-editor.org/rfc/rfc9110.html
2. M. Nottingham, *RFC 8288: Web Linking*, Standards Track, October 2017. Checked 2026-09-01. https://www.rfc-editor.org/rfc/rfc8288.html
3. E. Wilde et al., *RFC 9457: Problem Details for HTTP APIs*, Standards Track, July 2023. Checked 2026-09-01. https://www.rfc-editor.org/rfc/rfc9457.html
4. M. Kleppmann, *Designing Data-Intensive Applications*, 1st ed., O'Reilly Media, 2017, Chapters 8–9. Used for durable messaging, idempotence, and distributed-failure calibration.

## Exercises

### Exercise 1

For an image-render request, distinguish the event that justifies `202 Accepted` from the event that justifies `state=succeeded`. State one thing that must survive a process restart after acceptance.

### Exercise 2

An operation has states `accepted`, `running`, `succeeded`, `failed`, and `cancelled`. List the legal transitions and explain why `succeeded -> running` is invalid even if a later notification was delayed.

### Exercise 3

A client times out after submitting an invoice-generation request. Specify an idempotency-key record and response behavior that avoids creating two invoices when it retries.

### Exercise 4

Compare polling and signed webhooks for a regulated export service. Give a design that retains correctness when webhook delivery is duplicated, delayed, or absent.

### Exercise 5

Design cancellation and retention semantics for a bulk account-deactivation operation that may already have deactivated some accounts when cancellation arrives. Include client-visible terminal outcomes and a reconciliation path.

## Answers to the Exercises

### Answer 1

`202` is justified after validation and the service's stated durable acceptance boundary: it has recorded an operation ID and enough request state to answer later. `succeeded` is justified only after rendering completed and the authoritative result is committed or linked under the contract. The operation record and requester scope must survive restart; otherwise acceptance was misleading.

### Answer 2

Legal transitions are `accepted -> running`, `accepted -> cancelled`, and `running -> succeeded|failed|cancelled`. Terminal states have no transition that changes the business outcome. A delayed old `running` notification cannot reopen a succeeded operation because the authoritative record's terminal-outcome invariant dominates observation delivery order.

### Answer 3

Store `(tenant, endpoint, key) -> (canonical request fingerprint, operation ID, original acceptance response, expiry)`. The first durable acceptance creates that mapping and `op_88`. A same-key, same-fingerprint retry returns `op_88`; a same-key, different-fingerprint retry returns a conflict. The invoice worker must also deduplicate its own external effects, because submission deduplication alone cannot repair worker redelivery.

### Answer 4

Polling is simpler, client-controlled, and is the durable correctness path; webhooks reduce latency but require delivery infrastructure. Return an operation URI on submission, retain terminal state, and make `GET` authorized and reliable. Send signed webhook notifications that contain the operation identifier and event identifier; receivers deduplicate event IDs and re-fetch the operation. Retry notification delivery with bounds, but absence or reordering changes no operation outcome.

### Answer 5

Cancellation may be accepted while the operation is nonterminal, but it races each deactivation. The terminal record should report `cancelled` with completed account IDs/counts and remaining work, or `succeeded` if commit completed first; `failed` must state safe category and reconciliation ID. Already deactivated accounts are not silently reactivated. Provide a separately authorized reactivation/reconciliation operation, retain the status for a stated period, and audit both operations. Evaluation requires clear race semantics, partial-effect reporting, and a new compensating workflow rather than a false atomic rollback claim.
