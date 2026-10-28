---
module_id: API-037
program: API & Service Engineering
level: 1
module_number: 37
title: Idempotency Keys
status: complete
last_verified: 2026-09-01
---

# Idempotency Keys

## One-Page Review

### Governing question

How should a client and service bind repeated non-idempotent requests to one durable logical operation so transport retries neither duplicate effects nor silently attach different intent to an old result?

### Essential definitions

- **idempotent semantics** means repeating the same intended request has the same intended effect as applying it once, although responses may differ.
- An **idempotency key** is a client-supplied opaque value used to recognize retries of one logical operation.
- A **key scope** is the tuple—such as tenant, principal, operation, and API generation—within which a key must be unique.
- A **request fingerprint** is a server-derived digest or canonical comparison value for the request semantics bound to a key.
- An **idempotency record** durably stores scope, key, fingerprint, lifecycle state, outcome identity, and expiry.
- An **in-progress owner** is the one execution permitted to advance an absent key toward a terminal outcome.
- A **replay** returns or reconstructs the authoritative outcome of the original logical operation without repeating its protected effect.

### Central model, mechanism, or theorem

Let

$$
K=(\text{tenant},\text{principal},\text{operation},\text{key})
$$

identify a record $M(K)=(f,s,o,t_e)$ containing semantic fingerprint $f$, lifecycle state $s$, outcome $o$, and expiry $t_e$. Atomic first-writer enforcement allows exactly one owner to move an absent live key to `pending`. A request with the same $K$ and $f$ observes the existing state or outcome; the same $K$ with a different $f$ is rejected. This can provide at-most-one logical execution within the documented retention and consistency boundary. It does not prove global exactly-once delivery or effects outside that boundary.

### Critical invariants

Keys are high-entropy, opaque, bounded, and scoped by verified identity and operation. One live key binds to one semantic request fingerprint. Reservation occurs before the protected effect. Reservation, authoritative effect, and recoverable outcome identity commit atomically or through a workflow that can reconcile every state. Concurrent duplicates do not execute in parallel. Completed outcomes replay consistently. Pending, terminal failure, ambiguous effect, expiry, and abandoned ownership have explicit policies. Key storage and lookup use strong enough consistency for the guarantee. Retention exceeds the supported retry horizon. Logs and metrics do not expose raw keys or secret payloads.

### Common failures

Keeping keys only in process memory; scoping globally and causing cross-tenant collisions; scoping only by key and letting one endpoint replay another; accepting a reused key with different input; hashing raw JSON while claiming semantic equality; reserving after the effect; saving the response after the business commit in a separate write; deleting `pending` records on timeout without reconciling; returning a second execution while the first is active; replaying transient headers or expired signed URLs blindly; caching every validation error forever; using an idempotency key as authentication; expiring records sooner than client retries; and promising exactly once across services.

### Compact example

A mobile client sends `POST /payments` with key `k7`, loses the response, and retries. The service scopes `k7` to tenant, payer, and `payment.create`; a unique claim and payment/outcome record commit together. The retry has the same fingerprint and returns the stored payment identity and terminal result. If the body changes from 40 to 60 euros, the service rejects key reuse. **Conclusion:** the key identifies one logical payment intent, not a permission to cache arbitrary requests.

### Connections

[Request-Scoped Transaction Boundaries](036-request-scoped-transaction-boundaries.md) supplies the local atomic commit that binds key, effect, and outcome; [Error Translation](035-error-translation.md) distinguishes replay, in-progress, mismatch, expiry, and ambiguity. [Concurrency Control at the API Boundary](../ROADMAP.md) next generalizes competing writers and preconditions.

## Governing Question

Which operations accept keys, how are keys generated and scoped, what request semantics are fingerprinted, how is first ownership claimed, which outcomes are persisted and replayed, and when can a retained record safely expire?

## Why This Matters

Networks do not deliver knowledge atomically with effects. A server can commit a payment, order, or message and lose the response before the client reads it. The client then sees the same symptom as a request that never reached the server. Retrying a non-idempotent operation may duplicate a charge; refusing to retry may abandon an operation that never happened.

HTTP already defines some methods as idempotent by semantics. RFC 9110 explains that idempotent methods can be repeated after communication failure because the same intended effect is expected, though responses may differ. `POST` commonly creates a new effect on every accepted request, so a service-specific mechanism is needed when automated retry must be safe.

An idempotency key is that mechanism only when backed by durable protocol and state. A header accepted by middleware but recorded in a local cache cannot protect failover. A uniqueness row written after the charge leaves a crash gap. A stored body without request comparison lets an accidental key reuse return the result of unrelated intent. A completed record pruned before an offline client retries makes an old operation new again.

Good design turns transport uncertainty into a lookup of one logical operation. It also defines the boundary honestly: retention is finite, multi-region consistency has a cost, downstream effects need their own identities, and a key does not authorize the caller or guarantee that arbitrary distributed work happens exactly once.

## Prerequisites and Retrieval

Retrieve HTTP safe and idempotent method semantics; request parsing and canonicalization; authentication and tenant context; local transactions, unique constraints, and isolation; optimistic concurrency; deadlines, retries, and backoff; asynchronous operation resources; transactional outbox; distributed consistency; privacy and secret handling; API versioning; and error translation.

Before enabling keys, retrieve the exact unsafe operation, logical effect identity, verified scope, maximum key length and syntax, client generation guidance, canonical semantic input, excluded volatile fields, validation order, local effect transaction, downstream effect IDs, concurrent duplicate behavior, retry horizon, retention and tombstone period, regional routing/consistency, replay representation policy, failure taxonomy, storage encryption, abuse limits, and operational reconciliation process.

## Learning Objectives

By the end of this module, you should be able to:

1. distinguish HTTP method idempotence from key-mediated logical-operation deduplication;
2. define key syntax, entropy, scope, lifetime, and client responsibilities;
3. bind one live key to one canonical semantic fingerprint;
4. design an atomic absent-to-pending-to-terminal state machine;
5. classify validation, concurrent, transient, terminal, and ambiguous outcomes;
6. replay outcomes safely across versions, regions, and response-time data; and
7. test crash windows, concurrency, expiry, security, and recovery.

## Core Exposition

### Start with operation semantics

Do not add keys indiscriminately to every route. First ask whether repeating the method already has idempotent intended effect. A correctly implemented `PUT` of a complete representation and `DELETE` have idempotent semantics under HTTP, although audit entries, timestamps, rate counters, and responses need not be identical. A `GET` should not require a key to compensate for hidden mutation; make the method safe.

Keys are most useful for unsafe commands such as create payment, place order, submit message, allocate resource, or begin a job. They can also protect a `PATCH` whose repeated application would increment or append rather than set a value. Document whether the key is required, optional, or unsupported per operation.

Do not confuse business uniqueness with retry identity. “Only one active subscription per customer” is a domain invariant; two deliberately submitted requests may conflict even with different keys. An idempotency key says these transmissions represent one logical request. Both mechanisms can apply.

### Define client responsibilities

The client creates one new unpredictable key for one logical operation and retains it across transport retries. It must not create a new key merely because a response timed out; that defeats deduplication. It must not reuse a key for a new intent after success or failure.

Specify a bounded syntax and length before reading into memory or logs. High-entropy random values such as a securely generated UUID-like identifier are common. The server should treat the value as opaque, not derive authority or domain fields from it, and reject multiple conflicting header occurrences.

The IETF HTTPAPI working-group draft for `Idempotency-Key` describes an HTTP request field, uniqueness, expiry, fingerprinting, and responsibilities. As of the review date, revision 07 is an expired Internet-Draft submitted toward publication, not an RFC; an API can adopt a documented field contract but must not represent the draft as a final standard.

Clients need the server's retention horizon. If a mobile device may retry for seven days, a 24-hour record cannot guarantee deduplication. After the advertised horizon, the client should reconcile through resource/operation identity rather than replay an old key.

### Scope keys by verified context

Never use a bare key as the global lookup identity unless the contract intentionally guarantees global uniqueness and prevents cross-principal observation. A useful scope includes:

- tenant or account from verified context;
- effective principal/client where policy requires separation;
- operation identity, not only path text;
- target resource for commands on an existing object;
- API contract generation when semantics differ; and
- the opaque key.

Do not trust tenant or principal scope from an unverified body field. Two tenants may safely use the same random key when storage partitions by verified tenant. Conversely, retries by a delegated workload may need to resolve to the original effective actor and operation even if a refreshed token has different incidental claims.

Authorization is always reevaluated according to policy. Returning a stored result can itself disclose a resource. Decide whether replay uses current authorization, the original authorization snapshot, or a safe operation receipt. Usually the caller must still authenticate and be authorized to observe the outcome; the key is not a bearer capability.

### Bind a semantic request fingerprint

When a live scoped key exists, compare the retry with the original logical request. If semantics differ, reject reuse with a stable problem type instead of returning the wrong outcome or executing new work.

Fingerprint inputs can include method/operation, normalized target identity, canonical body semantics, relevant query parameters, content profile, conditional headers, and invariant actor/tenant scope. Exclude transport noise such as trace ID, connection details, retry count, date, and refreshed authentication token when they do not alter intent.

Raw bytes are simple but can treat insignificant JSON member order or whitespace as different. Parse then canonicalize a typed command to compare semantics. Beware numbers, Unicode normalization, omitted versus explicit defaults, duplicate JSON members, unordered sets versus ordered lists, time zones, file streams, and schema evolution. The same canonicalizer must not reinterpret an old request after a deployment.

Store a versioned fingerprint algorithm or enough protected canonical input to compare under the original rules. A plain hash is a comparison tool, not proof of semantic equality if canonicalization is wrong. For low-entropy sensitive payloads, a leaked hash enables guessing; use access controls and possibly keyed hashing, and avoid logging it broadly.

### Claim first ownership atomically

The critical race is two copies of an absent key arriving together. Both cannot check absence then execute. Use a strongly consistent conditional insert or unique constraint on the complete scope to create exactly one `pending` record. Only the successful claimant may begin the protected effect.

A record can contain:

- scoped key or protected derivative;
- fingerprint and algorithm version;
- state such as `pending`, `succeeded`, `rejected`, `ambiguous`, or `expired`;
- owner/lease generation and timestamps;
- logical operation and resource identity;
- safe replay outcome or a pointer to it;
- original contract/media-type version; and
- expiry and retention policy.

Do not rely on a read-through cache as the authority. Caches may accelerate completed lookups, but a unique durable claim arbitrates ownership. In a partitioned or multi-region system, either route a scope to one home, use a globally consistent conditional write, or weaken and document the guarantee. Two independent regional caches cannot supply at-most-one execution.

### Make pending behavior explicit

A second same-fingerprint request can arrive while the owner still runs. Choices include:

- return a stable `idempotency-in-progress` problem with bounded retry advice;
- wait only within the duplicate request's deadline and then return the current state;
- return an asynchronous operation reference; or
- subscribe to completion through internal coordination while treating the database record as authority.

Never let the duplicate execute in parallel. Do not hold an HTTP connection indefinitely. If the original owner crashes, a `pending` row must not block forever or be stolen blindly.

Use a lease generation and heartbeat only if operations can safely be resumed or reconciled. Lease expiry proves that the owner stopped renewing, not that its external effect did not occur. Before takeover, inspect local commit state and query downstream by the stable logical operation ID. Mark unresolved work ambiguous and route it to reconciliation rather than creating a second payment.

### Couple key state to the protected effect

For a local database effect, insert/claim the key and commit business change, outcome identity, required audit, and outbox intent in one transaction. A terminal replay can then derive from authoritative committed state.

There are two common shapes:

1. claim and finish within one short transaction when the operation is entirely local; or
2. commit a `pending` operation and outbox command, perform remote workflow outside, then update terminal state in a later transaction.

The second is not one transaction, but every durable state has recovery meaning. A worker uses the operation ID as the downstream idempotency key where supported, records attempts, and reconciles timeouts. The API returns the same operation resource for retries.

Never perform the effect, commit, and then insert the idempotency record separately. A crash between those steps duplicates on retry. Likewise, recording “succeeded” before the business commit can replay success for a rolled-back effect.

### Decide which outcomes become terminal

Not every response should be stored the same way. Classify by whether protected execution began and whether the result is stable.

- **Boundary rejection before claim:** malformed syntax, oversized key, failed authentication, or missing required key can return without a record because no operation began.
- **Semantic validation before effect:** an API may avoid claiming so a corrected request with the same key can run, but then the fingerprint/key contract must say correction is permitted. A stricter API can retain the rejection and require a new key.
- **Key mismatch:** retain the original record and reject; never overwrite it.
- **Concurrent duplicate:** expose pending state; it is not a second terminal result.
- **Stable domain rejection:** insufficient funds or forbidden transition may be stored and replayed so retries cannot observe a different decision accidentally, depending on business semantics.
- **Definitive transient failure before effect:** release/delete the claim or mark retryable under a generation so the same key can try again safely.
- **Committed success:** store terminal outcome atomically with the effect.
- **Unexpected error after execution began:** do not assume no effect. Preserve pending/ambiguous state until reconciliation establishes an outcome.

Stripe's documented API provides one concrete deployed policy: it saves the first execution result for a key, compares later parameters, and documents pruning after at least 24 hours. That is evidence of one provider contract, not a universal rule. Your API must state its own validation, error, and retention policy.

### Replay meaning, not accidental bytes

Some systems store exact status and body; others store resource/outcome identity and reconstruct a current representation. Exact replay is simple and preserves what the first caller would have received, but stored bodies consume space, can retain sensitive data, and may contain expired links, obsolete localization, dates, rate headers, request IDs, or signatures.

Reconstruction reduces storage and can apply current presentation/auth rules, but the body may differ from the original and the referenced resource may have changed or been deleted. HTTP idempotence concerns intended effect, not byte-identical responses. Document which fields are stable.

A balanced record stores semantic terminal status, created resource or operation identity, original contract version, and necessary immutable result facts. Generate a new response occurrence/request ID on replay while exposing a safe replay indicator if useful. Do not replay `Set-Cookie`, hop-by-hop fields, stale `Retry-After`, expired signed URLs, or another request's trace headers.

Reevaluate authorization before exposing the result. If a caller no longer may view the created resource, return the current safe authorization outcome without executing again. Keep internal evidence that the key is terminal so later authorization restoration still does not duplicate the effect.

### Define retention and expiry as semantics

Idempotency is bounded in time. Set retention from maximum client retry/backoff, offline duration, queue redelivery, downstream reconciliation, legal/audit needs, and storage capacity. Publish the minimum guarantee; operating longer is safe but not a substitute for a contract.

Do not recycle keys immediately after terminal response. A delayed packet or queued retry can arrive much later. Tombstones can retain scope, fingerprint, operation identity, and expiry with less data after detailed response retention ends.

Expiry transitions need race-safe deletion. A cleanup worker must not delete a record while a lookup or pending owner still depends on it. Never expire unresolved `pending` or `ambiguous` operations solely by age; move them to reconciliation or terminal manual status.

After final expiry, reuse may be treated as a new operation, rejected as too old when a durable operation identity is present, or routed to reconciliation. Random keys make deliberate reuse unlikely, but the behavior still belongs in the contract.

### Protect the idempotency service

Key endpoints can be abused to consume durable storage, pin pending work, probe whether another request occurred, or hot-spot a partition. Authenticate and authorize before creating records where possible; rate-limit claims; cap key/body/fingerprint size; limit outstanding operations per scope; and partition by a stable safe hash.

Use constant-time comparison only when secret-dependent timing is material; more importantly, prevent cross-scope lookup and enumeration. A predictable key is not sufficient authorization. Error responses must not reveal whether a key belongs to another tenant or operation.

Encrypt sensitive stored outcomes, minimize retention, and restrict support tooling. Log a keyed/redacted derivative plus scope and operation rather than the raw key. Metrics should count new, replay, mismatch, pending, ambiguous, expired, and reconciled states without unbounded key labels.

### Test every crash window

Test two simultaneous first requests, same key/same fingerprint, same key/different fingerprint, same key/different tenant, endpoint, actor, and API version. Assert exactly one protected local effect and one outcome identity.

Inject process death after claim, after each business write, before commit, during ambiguous commit acknowledgement, after business commit before response, during remote effect, before terminal update, and during replay. Restart on another node/region and verify the same authority is consulted.

Test canonicalization with reordered JSON, numeric forms, defaults, Unicode, arrays, duplicate members, content profiles, and schema versions. Test retention boundaries with a controllable clock, cleanup races, tombstones, delayed queues, and unresolved pending records. Security tests cover oversized/high-cardinality keys, cross-tenant guessing, log exposure, stored response privacy, and denial-of-service budgets.

The executable model below illustrates scoping, fingerprint binding, pending exclusion, replay, and expiry. It does not model database atomicity, crashes, multi-region consistency, or remote effects.

<!-- bijux-verify: {"id":"idempotency-state-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"created=201 stored\nreplay=201 replay\nmismatch=409 key-reused\nconcurrent=409 in-progress\nother_scope=201 stored\nafter_expiry=201 stored\n","stderr":""}} -->
```python
records = {}

def request(scope, key, fingerprint):
    identity = (scope, key)
    record = records.get(identity)
    if record is None:
        records[identity] = {"fingerprint": fingerprint, "state": "done", "status": 201}
        return "201 stored"
    if record["fingerprint"] != fingerprint:
        return "409 key-reused"
    if record["state"] == "pending":
        return "409 in-progress"
    return f"{record['status']} replay"

print("created=" + request("tenant-a:create-order", "k7", "order=40"))
print("replay=" + request("tenant-a:create-order", "k7", "order=40"))
print("mismatch=" + request("tenant-a:create-order", "k7", "order=60"))
records[("tenant-a:create-order", "k8")] = {"fingerprint": "order=20", "state": "pending"}
print("concurrent=" + request("tenant-a:create-order", "k8", "order=20"))
print("other_scope=" + request("tenant-b:create-order", "k7", "order=40"))
del records[("tenant-a:create-order", "k7")]
print("after_expiry=" + request("tenant-a:create-order", "k7", "order=40"))
```

## Definitions and Notation

Let logical request $q$ have verified scope $\sigma(q)$, client key $k(q)$, and versioned semantic fingerprint $f(q)$. Its lookup identity is $K(q)=(\sigma(q),k(q))$. The live mapping $M(K)=(f,s,o,t_e)$ stores fingerprint $f$, lifecycle state $s$, outcome identity $o$, and expiry $t_e$.

For live record $M(K)$, safety requires that no request with fingerprint $f'\ne f$ executes under $K$, and at most one owner may advance protected execution. A replay is a later observation of $o$, not a second application of the effect. The **deduplication horizon** is the documented interval in which $M(K)$ remains authoritative.

An **owner generation** distinguishes attempts to resume recoverable pending work. A **tombstone** retains enough identity to prevent delayed duplicate execution after detailed outcome data is removed. **Semantic canonicalization** maps equivalent typed requests to one comparison form; it is versioned contract logic, not mere byte hashing.

## Mechanisms, Invariants, or Proof Structure

1. Select unsafe operations whose logical effects need retry protection.
2. Define client key syntax, entropy, reuse rules, and supported retry horizon.
3. Derive scope only from verified tenant, actor/client, operation, target, and contract context.
4. Parse and canonicalize the semantic request under a versioned fingerprint algorithm.
5. Atomically claim an absent scoped key before any protected effect.
6. Reject mismatched fingerprints and prevent concurrent duplicate execution.
7. Couple effect, outcome identity, audit, and outbox to durable key state.
8. Classify pre-execution, stable rejection, transient, committed, and ambiguous outcomes.
9. Replay a safe authoritative outcome under current observation authorization.
10. Retain, expire, reconcile, observe, and test records under the published boundary.

The safety claim is at-most-one logical execution only within the chosen scope, consistency domain, implementation paths, and retention interval. Neither a key nor a successful finite test establishes exactly-once distributed effects.

## Alternatives and Trade-Offs

Client-generated keys preserve one logical intent across retries without a preliminary round trip. Server-issued operation IDs can guarantee syntax/scope and simplify lookup but require the client to obtain or receive the ID before uncertainty. Some APIs combine both.

Exact response storage gives deterministic replay and simple clients but retains more sensitive/versioned data. Outcome pointers reduce storage and apply current presentation policy but can yield different bodies. Store the minimum immutable facts needed for the promised contract.

One transaction for key and local effect gives strong atomicity and simple recovery. Long remote work cannot stay in that transaction; a durable pending workflow adds states and reconciliation but avoids locks and crash gaps.

Waiting for an in-progress owner can reduce client polling but consumes connections and couples deadlines. Immediate `in-progress` response or operation resource scales better but makes clients handle a state machine.

Long retention protects offline and delayed retries but costs storage and privacy exposure. Short retention is cheaper but narrows the guarantee. Tombstones, compact outcome facts, and operation-specific horizons balance these concerns.

Global consistency enables cross-region deduplication but adds latency and availability trade-offs. Home-region routing is simpler but needs failover semantics. Eventual replication alone permits two first owners; document weaker behavior or add an authoritative claim service.

## Failure Modes and Misconceptions

- **“The method is idempotent because it has a key.”** The API's enforcement supplies the retry property; the HTTP method semantics do not change automatically.
- **“The key is globally unique.”** Define and enforce its verified scope.
- **“A key authenticates the request.”** It is an opaque retry identifier, not authority.
- **“Hashing the body proves sameness.”** Canonicalization, actor, target, headers, defaults, and version affect semantics.
- **“Check then insert is safe.”** Concurrent first requests require an atomic claim.
- **“Memory cache is enough.”** Failover and restart bypass it.
- **“Record after success.”** A crash after effect and before record leaves duplication.
- **“Pending lease expired, so nothing happened.”** Lease expiry says nothing definitive about external effects.
- **“Replay every byte.”** Volatile, sensitive, expired, and request-specific fields require policy.
- **“Store only successes.”** Stable failures and ambiguity need explicit semantics.
- **“Delete failed rows.”** Some failures may hide a committed or remote effect.
- **“Use the same key after editing the body.”** A live key is bound to one fingerprint.
- **“Keep records for a day.”** Retention must match the documented client retry horizon.
- **“One key gives exactly once.”** Scope, expiry, partitions, and downstream systems bound the claim.
- **“The IETF draft is an RFC.”** It remained an expired work in progress on the review date.

## Worked Examples

### Example 1

**Situation:** A client times out after creating an order and retries with a new key. **Reasoning:** The service sees a new logical operation and may create a duplicate. The client must retain the original key across uncertainty. **Conclusion:** key lifecycle belongs partly to the client.

### Example 2

**Situation:** Two tenants independently generate `k7`. **Reasoning:** A global bare-key index creates collision or disclosure. Scope by verified tenant and operation, while still requiring enough entropy to prevent abuse. **Conclusion:** uniqueness is contextual.

### Example 3

**Situation:** Retry reorders JSON members but preserves typed values. **Reasoning:** Raw-byte hashing falsely reports mismatch. Parse under the same schema and compare a versioned canonical command. **Conclusion:** fingerprint logical semantics, not incidental encoding.

### Example 4

**Situation:** Retry uses the same key but changes payment from 40 to 60 euros. **Reasoning:** The live fingerprint differs. Return `key-reused-with-different-request` and preserve the original record; never overwrite or charge again. **Conclusion:** one key binds to one intent.

### Example 5

**Situation:** Two identical requests arrive simultaneously on different nodes. **Reasoning:** Both cache misses are irrelevant; one strongly consistent conditional claim wins, and the other observes `pending`. **Conclusion:** first ownership needs durable arbitration.

### Example 6

**Situation:** Process dies after local order commit but before storing an idempotency result. **Reasoning:** Separate writes leave no replay evidence. Commit key, order identity, and outbox/outcome in one transaction. **Conclusion:** result recoverability is part of atomic effect design.

### Example 7

**Situation:** Payment provider times out while the operation is `pending`. **Reasoning:** Removing the row and retrying may charge twice. Query the provider with the stable operation ID, retain ambiguity, and allow takeover only after reconciliation. **Conclusion:** timeout is not evidence of no effect.

### Example 8

**Situation:** A stored response contains a signed download URL that expired. **Reasoning:** Byte replay returns unusable data. Store the immutable artifact identity and generate a new authorized URL, documenting that representation bytes can differ. **Conclusion:** replay stable meaning, not every transient field.

### Example 9

**Situation:** Access is revoked after a successful create, then the key is retried. **Reasoning:** Executing again is forbidden, but returning the old body can leak. Keep the terminal record, reevaluate observation authorization, and return a concealed/current denial without repeating the effect. **Conclusion:** keys do not bypass authorization.

### Example 10

**Situation:** A retry arrives one minute after the published seven-day retention expires. **Reasoning:** The key may no longer protect against duplication. Route the client to operation/resource reconciliation or explicitly treat it as new under the contract; do not imply an infinite guarantee. **Conclusion:** expiry is API semantics, not housekeeping detail.

## Cross-Program Connections

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies retry, partial-failure, consistency, lease, and exactly-once skepticism. [Database Engineering](../../18-database-engineering/ROADMAP.md) supplies unique claims, transactions, isolation, and retention storage. [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies tenant isolation, entropy, disclosure, abuse controls, and protected logging. [Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies deterministic concurrency, crash injection, model-based state testing, and time control. This API module turns them into a public retry contract for unsafe operations.

## References

1. R. Fielding, M. Nottingham, and J. Reschke, [*RFC 9110: HTTP Semantics*](https://www.rfc-editor.org/rfc/rfc9110.html), especially Section 9.2.2, June 2022. Checked 2026-09-01.
2. J. Jena and S. Dalal, [*The Idempotency-Key HTTP Header Field, draft-ietf-httpapi-idempotency-key-header-07*](https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-idempotency-key-header-07), expired Internet-Draft, October 2025; work in progress, not an RFC. Status checked 2026-09-01.
3. Stripe, [*Idempotent Requests*](https://docs.stripe.com/api/idempotent_requests), API documentation. Checked 2026-09-01.
4. Amazon Web Services, [*Making Retries Safe with Idempotent APIs*](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/), Amazon Builders' Library. Checked 2026-09-01.
5. Amazon Web Services, [*Transactional Outbox Pattern*](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html), AWS Prescriptive Guidance. Checked 2026-09-01.

## Exercises

### Exercise 1

Define an idempotency contract for `POST /tenants/{tenant}/payments`: key syntax, verified scope, fingerprint, requiredness, pending response, terminal outcomes, retention, replay fields, and authorization.

### Exercise 2

Design the absent, pending, succeeded, rejected, ambiguous, expired, and reconciled state transitions for a command that calls a remote shipping provider.

### Exercise 3

Diagnose a service that hashes raw bodies, stores keys in a five-minute node-local cache, charges before inserting the cache entry, deletes entries on timeout, and returns stored responses without authentication.

### Exercise 4

Compare exact response replay with outcome-pointer reconstruction for an export API whose response includes localized text, a request ID, rate headers, and a ten-minute signed URL.

### Exercise 5

Design a verification campaign for multi-region order creation under simultaneous duplicates, network partitions, schema deployment, process crashes, cleanup, delayed queue redelivery, and cross-tenant key guessing.

## Answers to the Exercises

### Answer 1

Require one opaque, high-entropy, bounded key per logical payment; reject duplicate header fields. Scope by verified tenant, effective payer/client, `payment.create`, API generation, and key—not body tenant alone. Fingerprint typed amount/currency/destination and relevant target/conditional semantics under a versioned canonicalizer, excluding trace and refreshed-token noise. Atomically claim before effect. Same fingerprint while pending returns an operation reference or stable in-progress problem; mismatch returns key-reuse conflict. Commit payment/outcome/outbox/key together locally or use a recoverable remote-payment workflow. Retain beyond the documented retry/offline horizon, tombstone delayed replays, and never expire ambiguity silently. Replay stable payment/operation facts, regenerating volatile headers. Reauthenticate and authorize every observation.

### Answer 2

`absent -> pending` requires one conditional owner. Local validation can yield `rejected` if the contract retains stable rejections. Pending emits an outbox shipping command with the same logical operation ID. Provider success becomes `succeeded`; definitive business refusal becomes `rejected`; timeout or lost acknowledgement becomes `ambiguous`, never absent. Reconciliation queries the provider by operation ID and moves ambiguous to succeeded/rejected, or to a named manual terminal state. A lease generation may transfer work only after reconciliation proves safe. Completed records eventually compact to tombstones then expire after the retry horizon; unresolved pending/ambiguous records do not expire through ordinary cleanup. Every transition is monotone or generation-guarded and auditable.

### Answer 3

Raw hashing rejects semantically equivalent JSON and ignores scope/version meaning. A five-minute local cache loses state on restart/failover and permits another node to execute. Charging before claim creates a direct duplicate window. Timeout deletion mistakes uncertainty for absence. Unauthenticated replay leaks outcomes and treats the key as a bearer secret. Replace it with verified scoped identity, typed versioned canonicalization, strongly consistent atomic claim, stable downstream operation ID, durable pending/terminal records, effect/outcome atomicity or workflow reconciliation, retention matched to clients, current authorization on observation, protected outcome storage, and deterministic crash/concurrency tests.

### Answer 4

Exact storage would freeze the original language and request ID, replay stale rate metadata, and return an expired signed URL; it also retains a larger sensitive body. Outcome-pointer reconstruction stores artifact ID, immutable export parameters, terminal status, contract generation, and original operation timing. On authorized replay it returns the same artifact/logical outcome, localizes current human text, creates a new response request ID, calculates current rate headers, and signs a fresh short-lived URL. If byte identity is required for evidentiary reasons, store the immutable artifact separately and still regenerate delivery metadata. Document that effect identity is stable while response bytes and volatile fields may differ.

### Answer 5

Use deterministic barriers to submit identical and mismatched duplicates to multiple regions. Under normal and partitioned routing, assert the claimed guarantee: one global owner through a consistent store/home region, or detect and document weakened availability. Crash after claim, local writes, commit, outbox, remote acknowledgement, and terminal update; restart elsewhere and reconcile one outcome. Deploy old/new canonicalizers simultaneously with stored algorithm version and test reordered/defaulted payloads. Advance a controllable clock through detailed retention, tombstone, and final expiry while delayed queue messages arrive. Flood unique oversized keys and pending records to verify limits. Guess keys across tenants/operations and assert no existence disclosure. Audit logs and metrics for raw keys, secret payloads, unbounded labels, and duplicate business effects.
