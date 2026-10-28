---
module_id: API-040
program: API & Service Engineering
level: 1
module_number: 40
title: Implementing a Predictable Service Endpoint
status: complete
last_verified: 2026-09-01
---

# Implementing a Predictable Service Endpoint

## One-Page Review

### Governing question

How can an endpoint compose transport semantics, bounded parsing, verified identity, authorization, admission control, idempotency, concurrency control, domain rules, transactions, durable events, error translation, and observability so that every outcome remains predictable under retries, races, failures, and attack?

### Essential definitions

- A **predictable endpoint** gives each materially distinct request condition one documented outcome and preserves its invariants under repetition and concurrency.
- A **boundary pipeline** is the ordered sequence of checks and effects from receipt through committed response.
- An **authoritative context** contains authenticated, server-derived identity and scope rather than caller assertions.
- An **operation identity** is the server-scoped identity of one logical unsafe operation, commonly tenant, principal, operation, and idempotency key.
- A **request fingerprint** is a canonical digest of the request facts that an idempotency key is allowed to bind.
- A **precondition** is client-supplied state knowledge, such as `If-Match`, that must hold before mutation.
- A **commit point** is the atomic transition after which the service may truthfully report success.
- An **outbox record** is a durable event intent committed with the domain mutation for later publication.

### Central model, mechanism, or theorem

Model the endpoint as an ordered partial function

$$
E:(R,A,S,L)\rightarrow(O,S',L'),
$$

where request $R$, authoritative context $A$, state $S$, and operation ledger $L$ produce public outcome $O$ and new durable state. A successful first execution must make the domain mutation, new version, audit/outbox intent, and completed idempotency outcome atomic. A replay with the same operation identity and fingerprint returns the recorded outcome without another domain effect; a reused key with a different fingerprint is rejected. Authentication and authorization still guard replay observation.

### Critical invariants

The transport adapter does not make domain decisions. Caller-controlled tenant or subject fields never override verified context. Parsing is bounded before expensive work. Authorization is target- and action-specific and does not leak concealed objects. Precise quotas use verified identities; capacity admission happens before the protected resource. An idempotency record never bypasses authorization. The precondition is evaluated in the same consistency boundary as the write. One request owns one explicit transaction, and no success leaves before commit. State, version, outbox, audit, and completed operation outcome agree. Errors use stable HTTP and Problem Details semantics without exposing internals. Logs and metrics use correlation and bounded labels, not secrets or unbounded identifiers.

### Common failures

Putting business rules in the router; trusting a body tenant; authenticating but never authorizing the object; starting the transaction before parsing or remote calls; checking `If-Match` outside the write transaction; treating an idempotency key as globally unique or as permission; storing success before commit; publishing an event before the state commits; returning `200` after a rollback; mapping every rejection to `400` or every failure to `500`; converting overload to `429`; charging a business quota twice on replay; revealing object existence through precondition order; logging tokens or request bodies; and letting framework exceptions define the public contract.

### Compact example

`POST /tenants/acme/orders/ord-7:cancel` carries verified principal `user-4`, `Idempotency-Key: cancel-81`, and `If-Match: "v6"`. The service authenticates, binds the path tenant, admits bounded cost, loads the order, authorizes cancellation, detects no prior operation record, verifies version 6, applies the domain transition, writes version 7 plus audit, outbox, and completed operation outcome in one transaction, commits, then returns `200` with `ETag: "v7"`. An identical retry receives the recorded response and creates no second event. **Conclusion:** predictability is a property of the whole ordered boundary, not of any one handler function.

### Connections

[Transport, Application, and Domain Boundaries](031-transport-application-and-domain-boundaries.md) defines ownership; [Request Parsing and Validation](032-request-parsing-and-validation.md), [Authentication Context Propagation](033-authentication-context-propagation.md), and [Authorization Checks](034-authorization-checks.md) establish trustworthy inputs; [Error Translation](035-error-translation.md), [Request-Scoped Transaction Boundaries](036-request-scoped-transaction-boundaries.md), [Idempotency Keys](037-idempotency-keys.md), [Concurrency Control at the API Boundary](038-concurrency-control-at-the-api-boundary.md), and [Rate Limits and Quotas](039-rate-limits-and-quotas.md) supply the remaining controls. [API Threat Modeling](../ROADMAP.md) next examines this endpoint as an attack surface.

## Governing Question

What exact order of validation, trust establishment, admission, replay handling, authorization, precondition evaluation, domain execution, durable commit, and response construction makes one service endpoint safe and understandable across every documented outcome?

## Why This Matters

Endpoint implementation is where individually correct ideas collide. Validation wants to reject early. Authorization may need a loaded object. Concealment may require returning `404` rather than revealing that authorization failed. Idempotency wants to recognize a retry before repeating work, but its stored response must not become a capability that bypasses current authentication. Optimistic concurrency wants a version check adjacent to the write. Rate admission should precede expensive work, while precise tenant accounting requires verified identity. Transactions should be short, but success must not escape before all durable facts agree.

A handler that is readable only on its success path is not predictable. Clients encounter lost responses, duplicated messages, stale versions, expired credentials, exhausted limits, objects crossing states, dependency failures, and races. Operators encounter the same conditions plus partial telemetry, deployments, and attacks. The endpoint contract must make those paths deliberate.

Predictability does not mean that every request succeeds or that distributed execution becomes exactly once. It means that the service can state which request facts it trusts, where the irreversible boundary lies, what durable evidence survives, and what a client may safely do next. The endpoint then behaves as a small protocol implementation rather than a bag of framework callbacks.

This module constructs one concrete endpoint: cancel an order inside a tenant. Cancellation is a useful synthesis because it is unsafe, state-dependent, object-authorized, retryable after transport loss, and sensitive to concurrent changes. The specific domain is illustrative; the method applies to payments, reservations, workflow approvals, inventory adjustments, and administrative actions.

## Prerequisites and Retrieval

Retrieve HTTP method and status semantics, media types, Problem Details, OpenAPI operations, schema validation, trusted proxy boundaries, authentication and delegation, object-level authorization, tenant isolation, transaction isolation, optimistic concurrency and entity tags, idempotency keys and request fingerprints, rate and concurrency admission, domain aggregates, unit of work, audit trails, transactional outbox, timeouts, cancellation, logs/traces/metrics, and fault injection.

Before coding an endpoint, retrieve its consumer task, method and target resource, request and response schemas, success code, error catalogue, authentication scheme, tenant-binding rule, authorization decision, concealment policy, limit keys and costs, idempotency scope/retention, version representation, transaction owner, domain invariant, outbox/audit requirements, downstream dependencies, deadline policy, data classification, observability fields, and test matrix. Missing entries are contract decisions, not implementation details to improvise in an exception handler.

## Learning Objectives

By the end of this module, you should be able to:

1. turn a service contract into an ordered endpoint pipeline with explicit ownership;
2. place authentication, authorization, admission, idempotency, and preconditions without creating bypasses or disclosure;
3. define the atomic commit set for state, version, audit, outbox, and operation outcome;
4. translate every expected branch into stable HTTP and Problem Details behavior;
5. reason about response loss, concurrent requests, cancellation, and dependency failure;
6. design observability that proves invariants without leaking secrets or exploding cardinality; and
7. verify a real endpoint through contract, state-machine, race, retry, and fault tests.

## Core Exposition

### Start with an operation dossier

Write a one-page operation dossier before choosing framework annotations. For the running example:

- consumer task: cancel an order that has not shipped;
- operation: `POST /tenants/{tenant}/orders/{order}:cancel`;
- successful result: `200 OK` with the current order representation and a strong `ETag`;
- request body: optional bounded cancellation reason with a closed schema;
- authentication: bearer credential verified at the service trust boundary;
- authorization: `order.cancel` on this tenant-scoped order;
- admission: coarse anonymous/edge control, then verified tenant/principal action cost;
- retry identity: verified tenant, effective principal, operation name, and idempotency key;
- concurrency: required strong `If-Match` for the representation version;
- atomic write: order state/version, audit fact, outbox intent, and completed operation record;
- concealment: an absent or non-observable order is `404`;
- domain conflict: an order already shipped cannot be cancelled and yields a stable `409` problem;
- deadline: enough budget must remain before transaction entry; and
- sensitive data: credentials, raw idempotency keys, internal exception details, and private order fields never enter public errors or ordinary logs.

An action-shaped `POST` is justified here because cancellation is a domain command rather than replacement of the order representation. The URI convention is a local API design choice, not a new HTTP method. Document it consistently and do not pretend the colon syntax has universal semantics.

The dossier separates public promises from internal choices. A caller depends on `If-Match`, `Idempotency-Key`, response codes, schemas, and replay behavior. It should not depend on ORM exceptions, table layout, handler class names, or which message broker publishes the outbox.

### Make ownership visible

Use four boundaries even if the codebase implements them with fewer physical objects:

1. **Transport adapter:** method, route, headers, media negotiation, bounded decoding, response encoding, and HTTP error representation.
2. **Application service:** orchestration, authoritative context, policy calls, idempotency, transaction ownership, deadline, and result algebra.
3. **Domain model:** whether this order may transition from its current state to cancelled and which domain facts result.
4. **Infrastructure adapters:** repositories, operation ledger, audit/outbox persistence, limiter, clock, and telemetry.

The transport adapter creates a typed `CancelOrder` command. It does not set `order.status = "cancelled"`. The domain model does not inspect bearer tokens or construct `application/problem+json`. The repository does not decide whether a forbidden object should appear absent. The application service coordinates these responsibilities and returns a closed result type that the transport layer maps.

This separation makes negative paths testable without booting the full server. It also prevents framework exception order from becoming accidental protocol semantics.

### Establish a deliberate pipeline

A useful pipeline is:

1. enforce connection, header, compressed/uncompressed body, and time bounds;
2. match method and route and check supported media types;
3. authenticate credentials into a verified immutable context;
4. bind path tenant to allowed tenant context and delegation constraints;
5. apply authenticated rate, quota, and concurrency admission;
6. decode and schema-validate the bounded body and headers into typed values;
7. canonicalize the operation identity and request fingerprint;
8. ensure enough deadline remains for transactional work;
9. load the tenant-scoped target through a repository that cannot cross scope;
10. authorize the action and apply the concealment policy;
11. inspect an existing operation record; replay only after observation is authorized;
12. begin the short write transaction or enter an equivalent unit of work;
13. re-read/lock as required, evaluate `If-Match`, and apply the domain command;
14. atomically persist state/version, audit, outbox, and completed operation outcome;
15. commit, then construct the public success response; and
16. record bounded telemetry and release permits in every exit path.

This is a design template, not a universal fixed ordering. A service can schema-check a small body before authentication to reduce unauthenticated work elsewhere, or authenticate first to avoid returning detailed validation information to an attacker. The invariant is stronger than either preference: untrusted input is bounded; no expensive or revealing work occurs before its prerequisites; and the public ordering is consistent enough not to create an oracle.

Coarse edge limits may run before authentication. Precise tenant and principal limits must use verified context. Body streaming may interleave bounds with authentication. Authorization might be evaluated from an indexed policy relation before the full aggregate is loaded, but object-level permission must still bind the exact target. Record these choices in the dossier and test them.

### Parse into trusted types, not convenient dictionaries

The command should contain only values that passed syntax and structural validation: tenant identifier from the path, order identifier from the path, bounded normalized reason from the body, parsed entity tag, and an opaque validated idempotency key. Identity is a separate authoritative context produced by the authentication component.

Do not let a request body contain `tenant_id`, `owner_id`, `state`, or `version` merely because those columns exist. If such fields are accepted for a legitimate purpose, compare or authorize them explicitly; never mass-assign them into a domain object. Reject unknown properties when silent acceptance would conceal client mistakes.

Parsing should distinguish malformed representation (`400`), unsupported media type (`415`), unacceptable response type (`406` where the API negotiates it), schema violations (a documented `400` or `422` policy), and missing required precondition (`428`). Pick a consistent validation status policy and use a stable problem type plus field-error extension. Do not expose parser stack traces.

### Treat context as authority, not data

Authentication yields an immutable context such as `{subject, effective_subject, tenant_memberships, client, assurance, token_id_hash, expires_at}`. Only a trusted authenticator may construct it. Gateways may forward signed or mutually authenticated context only across a documented trust boundary; the public service must strip or reject spoofable identity headers.

Bind the path tenant before repository access. A principal authenticated for tenant `north` cannot cause a lookup in tenant `south` by changing the URI. Delegation records both actor and effective subject, and authorization evaluates the effective action under delegation constraints. Audit preserves both.

Authentication answers who presented acceptable evidence. Authorization answers whether that context may cancel this order now. Successful authentication is never implicit object permission.

### Compose admission without confusing it with permission

Admission control protects resources and fairness; it does not grant domain authority. Apply a coarse edge limit before expensive parsing or authentication where possible. After authentication and tenant binding, charge a bounded action cost to verified tenant/principal policies and acquire any scarce concurrency permit before database work.

If the requester exceeds its policy, return `429` with safe retry guidance. If the service is generally unable to accept valid work, return `503`; do not blame an individual caller. If an idempotent replay is served, it may still consume transport and lookup capacity, but it must not repeat the business cancellation unit. Maintain separate accounting dimensions.

All permits release on validation error, denial, domain conflict, timeout, cancellation, commit failure, and success. A leaked permit slowly turns correct traffic into outage. A request with insufficient remaining deadline should be rejected before acquiring scarce transactional resources.

### Scope idempotency as an operation ledger

The raw idempotency key is not globally meaningful. Scope it by verified tenant, effective principal or client as the contract requires, and operation name. Store a keyed digest when raw keys are sensitive. Define maximum length, allowed entropy/format, retention, concurrent duplicate policy, and whether response headers/body are replayed.

The fingerprint covers every semantic input whose change would create another operation: tenant, order, action, normalized reason, and precondition token. It excludes transport trivia such as trace identifier and header order. Version the canonicalization format so deployments do not reinterpret a retained key.

An existing record has three important cases:

- same key and same fingerprint, completed: return the recorded public outcome without another effect;
- same key and different fingerprint: return a stable idempotency-mismatch problem, commonly `409` under a documented contract; and
- same key and same fingerprint, in progress: wait within a small bound, return a documented conflict/retry response, or expose an operation resource.

Do not replay solely from the key table before authentication and authorization. Otherwise possession or guessing of a key can reveal the outcome of an object the current caller cannot observe. Authenticate, bind scope, load or otherwise identify the protected target, authorize observation/action, and only then expose the stored result. Re-evaluating authorization can mean a caller who was once allowed later cannot retrieve a replay; that is usually safer and must be documented.

A completed replay is checked before applying the current version precondition. Suppose the first call changed version 6 to 7 but its response was lost. The identical retry still carries `If-Match: "v6"`. If the service evaluated the current precondition first, it would return `412` and destroy the purpose of idempotency. After scope and authorization, the completed operation record wins for the identical fingerprint. Without a matching record, evaluate the precondition normally.

### Evaluate concurrency at the write boundary

Require `If-Match` for this state-changing command and return `428 Precondition Required` when absent. Parse accepted entity-tag forms according to the endpoint contract; do not compare an opaque wire tag to an integer through ad hoc string slicing scattered across handlers.

For a new operation, compare the expected version with the authoritative current version inside the same transaction and locking/isolation discipline as the write. A check performed before the transaction followed by an unconditional update has a time-of-check/time-of-use race. Prefer a conditional statement equivalent to:

<!-- bijux-verify: {"id":"conditional-order-cancellation","mode":"schematic","language":"sql","toolchain":"none","reason":"This database-specific concurrency pattern depends on transaction isolation, schema constraints, and affected-row interpretation unavailable in the isolated snippet runner."} -->
```sql
UPDATE orders
SET state = 'cancelled', version = version + 1
WHERE tenant_id = :tenant
  AND order_id = :order
  AND version = :expected
  AND state = 'open';
```

The affected-row count alone may conflate absence, stale version, and incompatible state. If the public contract distinguishes them, load under tenant scope and appropriate lock or issue narrowly designed follow-up reads without creating a disclosure. A stale precondition produces `412`; a current version whose domain state prohibits cancellation produces `409`.

Entity tags are opaque validators. The representation and ETag policy must ensure that `"v7"` truly identifies the selected representation or deliberately define a version-based strong validator for that representation. If different representations share a version incorrectly, caches and conditional clients become unsound.

### Keep one atomic commit set

The transaction begins only after bounded input, trustworthy context, admission, target discovery, authorization, and replay checks have eliminated most rejection paths. It owns the short consistency-critical section:

$$
C=\{\text{order state/version},\text{ audit fact},\text{ outbox intent},\text{ completed operation outcome}\}.
$$

Either all members of $C$ commit or none do. The domain transition produces facts; the application service persists them. Store enough canonical outcome data to reconstruct the promised replay without retaining prohibited secrets. The audit fact records actor, effective subject, tenant, object, action, decision/result, timestamp, and correlation identifiers under retention policy. The outbox intent is later published at least once, so consumers still deduplicate by event identity.

Do not call a remote broker, email service, payment processor, or webhook while holding the database transaction. Commit an outbox record and let a separate publisher handle retries. If an unavoidable remote side effect cannot join the transaction, model it as a saga/operation with explicit intermediate states rather than claiming one atomic endpoint.

Only after commit may the service report success. If response serialization can fail, validate/construct the response representation from stable result data before or predictably after commit, but never roll back a committed domain effect merely because the connection vanished. A lost response is exactly why the completed operation record exists.

Cancellation signals deserve care. Before commit, cancel safely and roll back. Once commit begins, the server must learn the final database outcome even if the client disconnects; abandoning the connection is not proof of rollback. After a known commit, finalize telemetry and operation result handling without executing the domain command again.

### Return a closed result algebra

The application service should return or raise only named outcomes that the transport adapter exhaustively maps. For this endpoint:

| Condition | Public response | Retry meaning |
|---|---:|---|
| cancellation committed or identical completed replay | `200` plus representation and `ETag` | complete; do not repeat with a new key |
| malformed syntax or representation | `400` | correct request |
| unauthenticated/invalid credential | `401` plus applicable challenge | obtain valid authentication |
| absent or concealed unauthorized order | `404` | do not infer existence |
| unsupported request media type | `415` | send supported representation |
| stale `If-Match` | `412` | retrieve/reconcile current representation |
| required `If-Match` absent | `428` | retry with current validator |
| order state prohibits cancellation | `409` with domain problem | resolve domain conflict |
| idempotency key reused for another fingerprint | `409` with key-mismatch problem | use original request or a new key for a new operation |
| requester-specific limit | `429` | wait/pacing per safe advice |
| general overload/maintenance | `503` | bounded availability backoff |
| unexpected internal failure before known commit | `500` generic problem | retry only under operation policy with same key |

RFC 9457 Problem Details gives the envelope, not the domain taxonomy. Use stable type URIs such as `https://api.example.test/problems/order-not-cancellable`; keep `title` stable, make `detail` safe, attach a correlation-safe `instance`, and define extensions such as invalid fields. The HTTP status retains generic semantics. Never return database exception text, authorization policy internals, stack frames, bearer credentials, or raw idempotency storage keys.

The mapper should be exhaustive in code and tests. An unknown exception becomes one generic `500` path and an internal diagnostic event, not a new client-visible schema invented from the exception class name.

### Specify the endpoint as contract and code

OpenAPI 3.2.0 can describe the operation, path/header parameters, security requirements, request schema, response representations, and reusable Problem Details schemas. It cannot by itself prove atomicity, authorization completeness, replay safety, or limiter placement. Express those behavioral promises in operation descriptions, extensions only where tooling agrees, executable tests, and implementation invariants.

Keep generated server stubs at the transport boundary. A generated handler can parse a header and body, but it should call a handwritten application port. Do not let regeneration overwrite domain orchestration or make generated nullable types the domain model.

Maintain examples for success, stale precondition, missing precondition, concealed object, domain conflict, key mismatch, and limit response. Validate examples against schemas and run consumer tests against a real implementation, because a schema-valid example can still express the wrong behavior.

### Make observability prove the protocol

Create or propagate one request correlation identifier and one trace context under a strict trust policy. Add spans for authentication, admission, repository load, authorization, operation-ledger decision, transaction, and response mapping. Record outcome class, operation name, status, replay/new indicator, transaction result, and bounded duration.

Do not put tenant IDs, order IDs, idempotency keys, token IDs, or problem details into unbounded metric labels. Use approved hashed/sampled identifiers in logs or traces when operationally necessary and legally permitted. Never log bearer tokens or full bodies by default. Redact cancellation reasons if they may contain personal data.

Useful invariants become alerts or reconciliation queries: every committed cancellation has exactly one order version transition, one audit fact, one operation completion, and one outbox event identity; replay count does not increase domain transitions; no success response corresponds to a rolled-back transaction; in-progress operation records do not remain stranded past their lease; and permit acquisition equals release.

The following executable model is intentionally in-memory and sequential. It demonstrates authorization before replay disclosure, fingerprint binding, replay before current precondition evaluation, one state transition, and one outbox fact. It does not prove database isolation or distributed operation-ledger correctness.

<!-- bijux-verify: {"id":"predictable-cancel-endpoint","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"first=200 cancelled v2 events:1\nreplay=200 cancelled v2 events:1\nmismatch=409 idempotency-key-reused\nstale=412 precondition-failed\nconcealed=404 not-found\nlimited=429 rate-limited\n","stderr":""}} -->
```python
orders = {
    ("acme", "o1"): {"owner": "u1", "state": "open", "version": 1},
    ("acme", "o2"): {"owner": "u1", "state": "open", "version": 3},
}
operations = {}
outbox = []

def cancel(tenant, order_id, principal, expected, key, fingerprint, admitted=True):
    if not admitted:
        return "429 rate-limited"

    order = orders.get((tenant, order_id))
    if order is None or order["owner"] != principal:
        return "404 not-found"

    identity = (tenant, principal, "order.cancel", key)
    prior = operations.get(identity)
    if prior is not None:
        if prior["fingerprint"] != fingerprint:
            return "409 idempotency-key-reused"
        return prior["response"]

    if order["version"] != expected:
        return "412 precondition-failed"
    if order["state"] != "open":
        return "409 order-not-cancellable"

    order["state"] = "cancelled"
    order["version"] += 1
    outbox.append((tenant, order_id, "order.cancelled"))
    response = f"200 cancelled v{order['version']} events:{len(outbox)}"
    operations[identity] = {"fingerprint": fingerprint, "response": response}
    return response

print("first=" + cancel("acme", "o1", "u1", 1, "k1", "cancel:o1:v1"))
print("replay=" + cancel("acme", "o1", "u1", 1, "k1", "cancel:o1:v1"))
print("mismatch=" + cancel("acme", "o1", "u1", 1, "k1", "cancel:o1:changed"))
print("stale=" + cancel("acme", "o2", "u1", 2, "k2", "cancel:o2:v2"))
print("concealed=" + cancel("acme", "o2", "u2", 3, "k3", "cancel:o2:v3"))
print("limited=" + cancel("acme", "o2", "u1", 3, "k4", "cancel:o2:v3", admitted=False))
```

### Verify the outcome matrix, not only the happy path

Build tests from the operation dossier. Contract tests assert method, route, content types, authentication challenge, headers, schema, status, and problem types. Application tests assert the closed result algebra. Repository tests assert tenant scoping and conditional writes. Domain tests assert allowed transitions. Integration tests assert the atomic commit set.

Retry tests inject response loss after commit, then resend the identical request and verify one state transition and one outbox identity. Key-reuse tests vary each fingerprint field. Race tests send two authorized commands with the same version but different keys and prove that at most one wins. Duplicate tests send the same key concurrently and prove one execution. Authorization tests compare absent and concealed paths for indistinguishable public behavior. Fault tests fail audit/outbox/operation writes and prove the domain mutation rolls back.

Test deadlines immediately before transaction entry, during statement execution, and while the response connection disappears. Test limiter-store and database outages separately. Test that secrets and raw identifiers are absent from responses and ordinary telemetry. Test schema examples against the implementation. Finally, load-test the endpoint with realistic contention; a logically correct conditional write can still create a hot-row bottleneck.

## Definitions and Notation

Let $R$ be the bounded parsed request, $A$ the authoritative authentication/delegation context, $P$ the applicable policy decision set, $S$ durable domain state, and $L$ the idempotency operation ledger. Let $k$ be the scoped operation identity, $f(R)$ the versioned canonical request fingerprint, $v_c$ the client precondition version, and $v_s$ the current server version.

For completed record $L[k]=(f,O)$, an authorized request with the same fingerprint returns $O$ without applying the domain transition. If $f(R)\ne f$, it returns key mismatch. If no record exists, mutation requires $v_c=v_s$ and a permitted domain transition. Successful commit creates $S'$, version $v_s+1$, audit $a$, outbox fact $e$, and completed result $L'[k]$ atomically.

A **concealment policy** maps absent and selected unauthorized targets to indistinguishable public outcomes. A **result algebra** is the finite named set of expected application outcomes. A **transactional outbox** stores publication intent with domain state and publishes it later. A **commit uncertainty** is a condition where the caller or application layer has not yet established whether commit occurred; it must be resolved by database outcome or idempotent retry, not guessed.

## Mechanisms, Invariants, or Proof Structure

1. Freeze the consumer task and public operation dossier.
2. Bound transport input before expensive or stateful work.
3. authenticate into immutable authoritative context and bind tenant/delegation scope.
4. Admit cost and concurrency using the correct verified partition keys.
5. Parse all semantic inputs into closed typed commands and a versioned fingerprint.
6. Load through tenant-scoped access and authorize the exact action and object.
7. Resolve a matching completed operation before current precondition evaluation, but only after authorized observation.
8. For a new operation, evaluate the precondition atomically with the domain write.
9. Commit state, version, audit, outbox, and operation completion as one set.
10. Translate the closed result algebra to documented HTTP/Problem Details outcomes.
11. Emit safe evidence, release every permit, and never infer rollback from disconnect.
12. Verify the state machine with retries, races, faults, deadlines, and disclosure tests.

The safety argument depends on verified identity, complete fingerprinting, tenant-scoped storage, correct authorization, database isolation/conditional writes, and atomic persistence. The endpoint cannot provide exactly-once delivery to downstream consumers; the outbox plus stable event identity provides durable at-least-once publication with consumer deduplication.

## Alternatives and Trade-Offs

An action `POST` clearly names a domain command but adds application-specific URI semantics. A `PATCH` can express a state update but may invite clients to set forbidden fields. `DELETE` fits only when cancellation actually has deletion semantics. Choose from the consumer task and document the state machine.

Pessimistic locking simplifies some state decisions but holds locks while work proceeds and can deadlock or reduce throughput. Optimistic `If-Match` scales well for low contention and makes client reconciliation explicit, but clients handle `412`. A single atomic conditional update is efficient; a locked aggregate load can distinguish richer domain conflicts more clearly.

Storing a full replay response provides high fidelity but increases retention, schema evolution, and privacy cost. Storing a canonical result reference is smaller but must reconstruct equivalent public behavior across versions. Choose retention and encryption from risk and retry horizons.

Rechecking authorization on replay prevents a stale grant from becoming permanent, but identical retries can produce a later denial after access revocation. Freezing authorization into the operation record makes retry output stable but can disclose data after revocation. Prefer current authorization for observation and describe the consequence.

Beginning the transaction before target load can make one consistent snapshot easy but holds scarce resources during policy work. Loading before the transaction shortens it but requires a re-read or conditional write to avoid races. Keep the consistency-critical decision inside the transaction regardless.

Synchronous event publication offers immediate feedback but creates dual-write failure. A transactional outbox is durable and atomic with eventual publication, at the cost of lag and duplicates. If the client needs downstream completion, expose an operation resource instead of extending a database transaction across services.

Rich error detail helps consumers but can leak existence, policy, or internal topology. Stable problem types and safe fields strike the balance; detailed diagnostics stay in protected telemetry correlated by instance identifier.

## Failure Modes and Misconceptions

- **“The framework handler is the application service.”** Transport lifecycle and domain orchestration have different ownership and tests.
- **“A valid schema is a valid command.”** Authorization, current state, and domain invariants remain.
- **“The tenant in JSON selects scope.”** Only authoritative context and explicitly bound path scope may do so.
- **“Authenticated means authorized.”** Permission is action-, object-, tenant-, and time-specific.
- **“Check idempotency first.”** A stored outcome must not bypass authentication or authorization.
- **“Check `If-Match` before replay.”** An identical retry after a successful lost response would incorrectly fail against the new version.
- **“Check the version, then update later.”** That creates a race; the check and write share one atomic boundary.
- **“The key makes execution exactly once.”** It controls one service's operation ledger; publication and downstream delivery still need deduplication.
- **“Write the replay record after commit.”** A crash between commits can repeat the domain effect; it belongs in the atomic set.
- **“Publish, then commit.”** Consumers can observe an event for rolled-back state.
- **“Client disconnect means rollback.”** Commit may already have succeeded.
- **“Every rejection is 400.”** Authentication, concealment, precondition, conflict, rate, and availability semantics differ.
- **“Every capacity rejection is 429.”** General service inability is `503`.
- **“OpenAPI proves behavior.”** It describes interfaces but does not prove authorization, atomicity, or races.
- **“Log the whole request for debugging.”** Credentials and private fields make that unsafe.

## Worked Examples

### Example 1

**Situation:** An authorized caller cancels open order version 6 with a fresh key. **Reasoning:** All bounds and policies pass; the transaction writes cancelled version 7, audit, outbox, and completed outcome, then commits. **Conclusion:** return `200` and `ETag: "v7"` only after known commit.

### Example 2

**Situation:** The response to Example 1 is lost and the caller retries the identical request with `If-Match: "v6"`. **Reasoning:** After authentication and authorization, the matching completed record is evaluated before current version 7. **Conclusion:** replay the recorded `200`; do not return `412` or emit another event.

### Example 3

**Situation:** A caller reuses the same key but changes the cancellation reason. **Reasoning:** The versioned fingerprints differ even if the target is identical. **Conclusion:** return the documented `409` idempotency-key-reused problem and perform no transition.

### Example 4

**Situation:** Two different keys concurrently cancel version 6. **Reasoning:** Both may authorize and read version 6, but the conditional write/lock permits only one version transition. **Conclusion:** one commits `200`; the other receives `412` or the documented current-state conflict after reconciliation.

### Example 5

**Situation:** A principal can authenticate in tenant `acme` but cannot observe order `ord-9`. **Reasoning:** The tenant-scoped load and authorization policy conceal protected existence. No idempotency result is disclosed. **Conclusion:** return the same `404` shape and timing budget used for an absent order.

### Example 6

**Situation:** The tenant exceeds its cancellation policy while the service is healthy. **Reasoning:** Verified requester-specific admission denies before database work. **Conclusion:** return `429` with bounded safe advice and do not charge the business cancellation unit.

### Example 7

**Situation:** The database pool is exhausted for all valid callers. **Reasoning:** This is service inability rather than one caller's policy excess. **Conclusion:** shed with `503`, bounded backoff guidance, and an availability signal; do not mislabel it `429`.

### Example 8

**Situation:** The outbox insert fails after the order update statement but before commit. **Reasoning:** Both writes share one transaction. **Conclusion:** roll back state, version, audit, and operation completion; a same-key retry may safely attempt the command again.

### Example 9

**Situation:** The broker is unavailable after the transaction commits. **Reasoning:** The durable outbox remains pending and the HTTP success describes committed service state, not broker delivery. **Conclusion:** retry publication asynchronously with stable event identity; do not re-run cancellation.

### Example 10

**Situation:** The client disconnects while commit is in progress. **Reasoning:** The server waits for the database's definitive outcome or recovers through the operation ledger. Connection state cannot decide transaction state. **Conclusion:** never guess; an identical client retry converges on the recorded outcome when commit succeeded.

## Cross-Program Connections

- **Software Engineering Patterns:** ports/adapters, application services, units of work, repositories, and result types assign ownership without coupling domain rules to HTTP.
- **Distributed Systems:** response loss, duplicate delivery, partial failure, leases, transactional outboxes, and at-least-once publication define the real retry model.
- **Database Systems:** conditional updates, isolation, locking, unique constraints, and atomic commits enforce concurrency invariants.
- **Security Engineering:** trust boundaries, object-level authorization, tenant isolation, concealment, least disclosure, and abuse controls constrain check ordering.
- **Systems Engineering:** the endpoint is a socio-technical control surface whose contract, operations, telemetry, failure modes, and evidence must agree.
- **Testing and Verification:** state-machine, property, contract, race, fault-injection, and load tests provide evidence beyond line coverage.
- **Observability Engineering:** traces connect boundary stages, while reconciliation proves durable cardinality invariants without unsafe metric labels.

## References

1. Fielding, R., Nottingham, M., and Reschke, J. [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html). IETF, June 2022. Checked 2026-09-01.
2. Nottingham, M., Wilde, E., and Dalal, S. [RFC 9457: Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457.html). IETF, July 2023. Checked 2026-09-01.
3. OpenAPI Initiative. [OpenAPI Specification 3.2.0](https://spec.openapis.org/oas/v3.2.0.html). 19 September 2025. Checked 2026-09-01.
4. OWASP Foundation. [OWASP API Security Top 10 — 2023](https://owasp.org/API-Security/editions/2023/en/0x00-header/). Checked 2026-09-01.
5. OWASP Foundation. [API1:2023 Broken Object Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/). Checked 2026-09-01.
6. Fowler, M. [Unit of Work](https://martinfowler.com/eaaCatalog/unitOfWork.html). Catalog of Patterns of Enterprise Application Architecture. Checked 2026-09-01.
7. Richardson, C. [Pattern: Transactional Outbox](https://microservices.io/patterns/data/transactional-outbox.html). Microservices.io. Checked 2026-09-01.

## Exercises

### Exercise 1

Design the operation dossier and ordered pipeline for `POST /tenants/{tenant}/payments/{payment}:refund`. Identify authoritative fields, admission controls, idempotency scope/fingerprint, precondition policy, atomic commit set, and public outcomes.

### Exercise 2

Explain why an identical retry after a lost successful response must consult a completed idempotency record before evaluating the request's now-stale `If-Match`, and why authorization must nevertheless precede replay disclosure.

### Exercise 3

Construct a race test for two cancellation requests with different keys and the same version. State the allowed response pairs and the durable cardinality assertions.

### Exercise 4

The domain row and audit write commit, but the idempotency record and outbox are written in later transactions. Enumerate failure windows and redesign the boundary.

### Exercise 5

Create a verification matrix covering contract, authentication, authorization/concealment, validation, rate/availability denial, replay/key mismatch, concurrency, rollback, response loss, observability, and secret leakage.

## Answers to the Exercises

### Answer 1

The refund dossier binds tenant/payment from the path to verified tenant membership; derives actor/effective subject from authentication; authorizes `payment.refund`; applies coarse edge and verified tenant/principal/refund-value admission; fingerprints target, normalized amount/currency/reason, and precondition; scopes the key by tenant, effective principal/client, and operation; requires a payment version or another explicit concurrency rule; and atomically commits refund state/ledger entry, audit, outbox, and operation outcome. Outcomes distinguish malformed/unsupported input, `401`, concealed `404`, `428`, `412`, domain `409`, key-mismatch `409`, requester `429`, general `503`, generic `500`, and committed/replayed success. Remote payment-rail work should use an operation/saga rather than remain inside a database transaction.

### Answer 2

The first request can commit version 7 while its `200` is lost. Its identical retry still truthfully carries version 6 because that was the logical operation's precondition. Evaluating current state first would yield `412` and make the retry ambiguous. A matching completed record proves the operation outcome and therefore wins after target observation is authorized. Authentication, tenant binding, and authorization come first because the record is protected information, not a bearer capability conferred by knowing a key.

### Answer 3

Start order version 6/open, authorize both calls, synchronize them immediately before the conditional write, then release them concurrently. With two different keys, one may return `200`; the other may return `412` or a documented `409` if the service reconciles the new state. Two `200` responses representing two new executions are forbidden. Assert one version increment, one cancelled state, one cancellation audit fact, one cancellation outbox identity, one completed winning operation record, no completed losing effect, and no leaked permits.

### Answer 4

After the domain/audit commit, a crash before the key record allows a retry to repeat or conflict without the promised replay. A crash before outbox insertion makes committed state invisible to event consumers. A key record committed before outbox can permanently replay success for an event that never exists. Put domain state/version, audit, outbox, and completed operation outcome in one local transaction with uniqueness/conditional constraints. Publish the outbox asynchronously with stable event IDs and consumer deduplication. If one store cannot own the set, model an explicit recoverable workflow and stop promising atomic completion.

### Answer 5

The matrix includes every documented status, content type, required header, and schema; invalid/expired credentials and spoofed context; allowed, denied, absent, cross-tenant, and concealed objects; boundary and unknown fields; `429` versus `503`; identical replay, concurrent duplicate, in-progress record, and changed fingerprints; missing/stale/current preconditions and racing keys; injected failure at each atomic write; disconnect before/during/after commit; one transition/audit/outbox/operation cardinality; permit release; bounded metric labels; correlation; and scans proving credentials, raw keys, private reasons, stack traces, and internal policy details never enter public responses or ordinary telemetry.
