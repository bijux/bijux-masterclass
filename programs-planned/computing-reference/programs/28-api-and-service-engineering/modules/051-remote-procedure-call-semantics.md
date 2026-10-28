---
module_id: API-051
program: API & Service Engineering
level: 2
module_number: 51
title: Remote Procedure Call Semantics
status: complete
last_verified: 2026-09-02
---

# Remote Procedure Call Semantics

## One-Page Review

### Governing question

What can a caller legitimately conclude after invoking an operation across an unreliable network, and which protocol, storage, and application rules make retries safe when the outcome is uncertain?

### Essential definitions

- A **remote procedure call (RPC)** presents a named operation on a remote service through a request/response abstraction.
- A **logical call** is the caller's intended operation; an **attempt** is one transmission/execution opportunity for that call.
- A **call identifier** correlates attempts; an **idempotency key** identifies one intended effect and supports durable result reuse.
- **At-least-once** execution retries until an attempt is accepted, so duplicate executions are possible.
- **At-most-once** execution uses duplicate suppression so a logical call executes no more than once within stated scope and retention assumptions.
- **Exactly-once effect** means one durable domain effect, normally obtained through idempotent state transitions, uniqueness, or transactions—not from the transport alone.
- An **outcome-unknown** result means the caller cannot distinguish “not executed” from “executed but reply lost.”
- A **deadline** bounds caller interest; **cancellation** communicates lost interest but does not roll back effects already committed.
- **application error**, **protocol error**, and **transport failure** are different failure domains and require different caller actions.

### Central model, mechanism, or theorem

For logical call $c$ with attempts $A(c)$ and domain effect count $E(c)$, a transport may deliver zero, one, or many attempts:

$$
|A_{delivered}(c)|\in\{0,1,2,\ldots\}.
$$

If an attempt fails before a trustworthy response, the caller observes uncertainty rather than a fact about execution:

$$
\operatorname{timeout}(a)\not\Rightarrow E(c)=0.
$$

An at-most-once server atomically records a call identity and its terminal outcome with the effect. Repeated attempts return that outcome without re-executing. A stronger domain invariant targets

$$
E(c)=1
$$

for an accepted logical operation, using a stable idempotency key, request fingerprint, atomic commit, and sufficient retention. Even then, liveness and a delivered acknowledgement remain separate properties.

### Critical invariants

The service contract states operation semantics rather than pretending a remote call is local. Every attempt carries a stable logical identity and a distinct attempt identity where retries exist. Request bytes are bounded, validated, and decoded under an explicit schema/version. Authentication and authorization apply to every attempt. A mutating operation defines its idempotency and concurrency behavior. Deduplication lookup, effect, and stored outcome are atomic or reconciled by a declared protocol. Reusing an idempotency key with a different request is rejected. Retention exceeds every legitimate retry/replay horizon. Deadlines propagate as remaining budget; cancellation stops useful work when possible but never promises rollback. Errors distinguish invalid input, failed preconditions, conflicts, permission, resource exhaustion, transient unavailability, deadline, cancellation, internal failure, and outcome unknown. Retries are bounded, back off with jitter, respect server pushback, and consume one end-to-end budget. Observability correlates logical call, attempt, service, method, outcome, latency, retry, and effect without leaking secrets.

### Common failures

Treating RPC as syntax sugar for a local call; assuming timeout means no effect; advertising exactly-once delivery without defining identity, atomicity, retention, and recovery; retrying every error; generating a new idempotency key per attempt; reusing a key for different input; keeping deduplication only in process memory; recording the result after committing the effect in a separate failure window; caching authorization failures beyond policy changes; failing to authenticate retried attempts; retrying non-idempotent operations through multiple layers; resetting the deadline at each hop or attempt; equating cancellation with transaction abort; exposing stack traces as application errors; collapsing every failure into “unavailable”; unbounded payloads or queues; assuming code-generated types guarantee wire compatibility; losing unknown fields; and using high-cardinality or secret request data as metric labels.

### Compact example

A client submits `Transfer(idempotency_key=K, from=A, to=B, amount=20)`. The server atomically checks that $K$ is unused, verifies a request fingerprint, moves the funds, and stores the terminal response under $(principal,K)$. The reply is lost. The caller receives outcome unknown and retries with the same $K$ and request. The server returns the stored response without moving funds again. **Conclusion:** two attempts produced one effect; no transport promise made the response arrive, and a different request under $K$ would be a conflict.

### Connections

[Idempotency Keys](037-idempotency-keys.md) develops operation identity, [Concurrency Control at the API Boundary](038-concurrency-control-at-the-api-boundary.md) protects state transitions, [Implementing a Predictable Service Endpoint](040-implementing-a-predictable-service-endpoint.md) frames caller decisions, and [Designing an API Against Expected Abuse Cases](050-designing-an-api-against-expected-abuse-cases.md) adds adversarial reasoning. [Protocol Buffers and Schema Evolution](../ROADMAP.md) next develops the message contract beneath typed RPC.

## Governing Question

Which observations belong to the caller, client runtime, network, server runtime, handler, and durable domain—and how should an RPC contract compose naming, encoding, execution, retries, failure, and cancellation without promising facts no participant can know?

## Why This Matters

RPC is compelling because generated stubs can make a remote invocation resemble a function call. That resemblance improves ergonomics, but it is not a semantic equivalence. A local call ordinarily shares an address space, failure fate, scheduler, and type/runtime assumptions with its caller. A remote call crosses serialization, queues, connections, load balancers, process lifetimes, independently deployed code, authorization boundaries, and durable state. It is slower by orders of magnitude, can be delayed without a known upper bound, and can leave the caller and server with different conclusions.

The most important ambiguity appears after a server commits a mutation but before the caller receives the response. A reset connection or expired deadline cannot reveal whether the request never arrived, is still running, committed with a lost reply, or failed during recovery. Retrying may be necessary for availability and dangerous for correctness. Suppressing the retry may avoid duplication and leave a required operation incomplete. The interface must therefore define logical operation identity, effect semantics, retryable outcomes, and recovery—not hide them behind generated syntax.

RPC semantics also shape evolvability and operations. An operation name and message schema are a distributed contract. A status is a control signal to client policy, not merely a human message. Deadlines form an end-to-end resource budget. Cancellation is cooperative. Streaming changes the unit of progress and commitment. Load balancing can send attempts to different server instances, making process-local duplicate caches insufficient. Observability must show a logical call and its attempts without multiplying apparent demand or losing the causal chain.

The durable lesson is not that RPC is inherently bad. It is that a useful RPC abstraction preserves the network's boundaries in its contract. Well-designed RPC can provide strong typing, efficient encoding, standardized lifecycle hooks, and excellent interoperability while making uncertainty explicit.

## Prerequisites and Retrieval

Retrieve procedure/function calls, values versus references, serialization and framing, request/response protocols, sockets and connections, DNS/service discovery, authentication and authorization, timeouts/deadlines, cancellation, retries/backoff/jitter, idempotence, transactions, concurrency control, durable uniqueness, partial failure, load balancing, schema evolution, status codes, logging/metrics/tracing, and resource bounds.

Before designing an RPC, retrieve the domain operation and invariant; whether it reads, mutates, streams, or starts asynchronous work; request/response size and sensitivity; caller/service trust boundaries; logical call identity; acceptable duplicate/missing effects; transactional boundary; deadline and latency objective; retry ownership; error taxonomy; deployment/version skew; discovery and balancing; overload behavior; cancellation and cleanup; audit needs; and how a caller resolves an uncertain outcome.

## Learning Objectives

By the end of this module, you should be able to:

1. distinguish a logical call, attempt, transport exchange, handler execution, and domain effect;
2. derive why timeout, cancellation, and connection failure do not establish whether a mutation occurred;
3. compare maybe, at-least-once, at-most-once, and exactly-once-effect claims with their assumptions;
4. design durable deduplication and idempotent state transitions for retryable RPCs;
5. specify operation shape, error, deadline, cancellation, versioning, and resource semantics;
6. place retry policy at one accountable layer and prevent amplification; and
7. verify RPC behavior through failure injection, concurrency tests, traces, and recovery exercises.

## Core Exposition

### Separate the abstraction from the mechanism

An RPC interface names operations and defines typed input/output plus call lifecycle. A client stub validates or encodes an input message, resolves a destination, attaches call context, sends framed bytes, waits or streams, decodes the outcome, and maps it into the caller's language. A server runtime accepts the exchange, authenticates context, decodes the request, dispatches a handler, encodes status/output, and terminates the exchange.

This mechanism can mimic call syntax but cannot inherit local-call guarantees. References cannot be passed as shared memory addresses; arguments are copied or represented by stable remote identifiers. Exceptions do not naturally cross languages, versions, or trust boundaries; they require an explicit status model. A local stack unwinds on cancellation, while a remote handler may already have committed, may not observe cancellation, or may be unreachable. Latency and availability are properties of every dependency in the call path.

Keep these layers distinct:

- the **interface model** defines operations and messages;
- the **wire protocol** defines framing, correlation, status, and metadata;
- the **transport** moves bytes and exposes connection/stream events;
- the **runtime** performs discovery, balancing, serialization, interception, and lifecycle handling;
- the **application handler** validates policy and invokes domain behavior; and
- the **domain/storage layer** owns durable invariants and effects.

A runtime acknowledgement that bytes reached a server process is not a domain commit. A handler return does not guarantee the response reached the caller. A successful client result is evidence of one response, not proof that no duplicate handler execution ever occurred unless the protocol supplies and enforces that invariant.

### Model a call as identities and state transitions

Let $c$ denote one logical call and $a_i$ its $i$th attempt. Useful identities include principal, service/method, logical-call or idempotency key, attempt ID, trace/span context, and server execution ID. They are not interchangeable. A trace ID correlates diagnostics and is not automatically a protected uniqueness key. An attempt ID distinguishes retries and is not stable enough to deduplicate the intended effect.

A simplified attempt evolves through client-created, queued, transmitted, accepted by a server runtime, dispatched, effect committed or rejected, response produced, response observed, and terminal locally. Different participants observe only projections of this state. The client may transition to deadline-exceeded while the server transitions to committed. Neither is lying; their local outcomes differ.

For a read-only call, duplicate execution is often harmless with respect to mutation, though it can still consume resources, leak through audit/side channels, or observe different state. For a mutation, define the semantic unit: “create this order,” “advance job 42 from queued to running,” or “append this exact event.” The method name alone does not define duplicate behavior.

### Derive the unavoidable outcome ambiguity

Assume a client sends a request and receives no valid terminal response before its deadline. Consider three traces:

1. the request was dropped before reaching the server;
2. the handler committed, but the response was dropped; or
3. the handler is still running when the caller stops waiting.

The client's observation is identical in all three: no terminal response. Any algorithm using only that observation cannot distinguish the traces. Therefore a transport failure maps to **outcome unknown** unless additional durable evidence exists. Querying operation status by stable ID, retrying through durable deduplication, or reconciling domain state can produce that evidence later.

This is an indistinguishability argument, not an implementation defect. A protocol can reduce uncertainty through acknowledgements and durable logs, but an acknowledgement can itself be lost. Consensus/transactions can order and atomically commit effects within a defined system; they do not force an unreachable client to learn the result.

### State delivery and execution claims precisely

“At most once,” “at least once,” and “exactly once” are incomplete without scope.

- **Maybe execution**: one attempt is sent, with no retry. It may execute zero or one time; the caller can still face outcome unknown.
- **At-least-once attempt delivery/execution**: retry continues under stated availability assumptions until an attempt reaches the handler. Duplicate deliveries/executions are possible. This is a liveness-oriented property.
- **At-most-once handler execution**: a stable call ID plus duplicate table suppresses repeated executions within an identity scope and retention period. The call may execute zero times. This is a safety property.
- **Exactly-once effect**: an accepted logical operation changes the durable domain exactly once. This generally composes at-least-once attempts with an idempotent/unique atomic effect or at-most-once execution, plus recovery and retention assumptions.

At-least-once plus at-most-once yields one execution only when both properties refer to the same call identity, time horizon, failure model, and durable system. A garbage-collected duplicate record can allow a late retry. A failover that loses the record breaks the claim. A handler can perform an external side effect before the duplicate record commits. Define principal/method/resource scope, retention, crash recovery, regional behavior, and downstream participation.

### Make operations idempotent by domain meaning

Mathematical idempotence means $f(f(x))=f(x)$. A “set account email to X” transition can be idempotent over state; “increment balance by 10” is not. Yet even a state-idempotent call may duplicate notifications, audit entries, provider charges, or version increments. State every relevant effect.

An idempotency-key protocol usually:

1. scopes a caller-supplied stable key to authenticated principal and operation;
2. computes a canonical request fingerprint;
3. atomically reserves a new key or reads an existing record;
4. rejects an existing key with a different fingerprint;
5. commits effect and terminal result with the record, or uses a recoverable state machine/outbox when one transaction cannot cover all effects; and
6. returns the stored result to matching retries.

An in-progress record needs lease/fencing/recovery semantics. Deleting it after a worker crash may allow duplicate effects; retaining it forever as “running” destroys liveness. External effects require provider idempotency keys, a durable outbox/inbox, or reconciliation because a local database transaction cannot atomically include an arbitrary remote provider.

Authentication and authorization are evaluated on every attempt. Do not return a cached sensitive result merely because a key matches if the current caller cannot access it. Conversely, changing authorization after an effect committed raises a policy question: the service might confirm only that an operation exists, return a redacted status, or require a privileged recovery route.

### Assign retry ownership and a finite budget

Retries can occur in application code, generated clients, RPC libraries, proxies, service meshes, gateways, queues, and operators. If three layers each make three attempts, one logical call can create up to $3^3=27$ downstream attempts before fan-out. The design assigns one primary retry owner per boundary and disables or tightly bounds overlapping policies.

Retry only when the operation is semantically safe and the outcome/status is eligible. Invalid input, permission denial, and stable failed preconditions do not become valid through repetition. Transient unavailability may be retryable. A deadline-exceeded mutation may have committed, so a retry requires stable idempotency identity. Resource exhaustion may require server-directed delay rather than immediate retry.

Use a maximum attempt count, exponential backoff, jitter, per-attempt cap, total deadline, and retry throttling/budget. Remaining time decreases across queueing, attempts, backoff, and nested calls. Hedging—starting another attempt before the first fails—can reduce tail latency for safe operations but deliberately creates concurrency and load; it demands deduplication/cancellation and a strict hedge budget.

Some runtimes transparently retry before application commitment. Treat that as part of the documented attempt model and observe it. Never infer that a library's retry configuration changes the domain operation from non-idempotent to idempotent.

### Design errors as machine-actionable semantics

An RPC outcome should distinguish success, application rejection, and infrastructure/protocol failure. A useful taxonomy separates:

- malformed or domain-invalid input;
- unauthenticated caller and unauthorized action;
- missing resource;
- existing resource/duplicate identity;
- state-dependent failed precondition;
- optimistic concurrency abort/conflict;
- quota or resource exhaustion;
- caller cancellation and deadline expiration;
- unimplemented method/version;
- transient unavailability;
- internal invariant failure or data loss; and
- outcome unknown requiring lookup/reconciliation.

Map each to caller action: correct input, authenticate, stop, refresh state, retry safely, back off, query status, compensate, or escalate. Status descriptions are for diagnostics and must not be parsed as a protocol. Structured details need a versioned schema and privacy review. Do not expose stack traces, topology, queries, tokens, or private entity existence.

The server and client can legitimately report different terminal statuses. Current gRPC documentation explicitly notes that a server may complete successfully while the client sees a deadline failure; it also warns that changes made before cancellation are not rolled back. This is a concrete instance of the general RPC model, not a gRPC anomaly.

### Treat deadline and cancellation as lifecycle semantics

A timeout is a duration; a deadline is an absolute end of caller interest. At each hop, propagate remaining duration after subtracting elapsed work rather than granting a fresh full budget. Reserve time for serialization, network, cleanup, and useful fallback. A server should reject work that cannot plausibly finish before the deadline rather than consume resources for a response nobody will use.

Cancellation communicates that a result is no longer wanted. It is cooperative: handlers check context, stop CPU/IO, cancel child calls, release locks/buffers, and avoid starting new effects. It does not reverse a completed transaction. A mutation that crosses its commit point must expose the committed outcome through idempotency/status/reconciliation even if the client cancelled.

Cancellation races with success. Define one local terminal result per participant and make cleanup safe under repeated signals. Background work that intentionally outlives the call must transfer ownership to a durable job and return that job identity; it must not survive merely because a detached thread ignored context.

### Specify naming, binding, and compatibility

An RPC name typically combines package/service/method and is resolved to one of several compatible server instances through discovery and balancing. The service identity used for authorization/TLS is not necessarily the DNS label or backend instance. Bind credentials to the intended service/audience, reject cross-environment names, and make routing metadata authenticated where it changes tenancy or policy.

Interface definition languages generate language bindings, but generated types do not remove compatibility obligations. Define field identity, presence, defaults, unknown-field behavior, numeric ranges, enum evolution, one-of semantics, validation, and size bounds. Additive changes can still alter business semantics. Removing/reusing field identifiers, changing units, narrowing ranges, or reinterpreting defaults breaks deployed clients even when decoding succeeds.

Version negotiation and deployment skew belong in tests. Servers should tolerate supported older clients, clients should handle unknown/new values safely, and rollouts should not require lockstep deployment. API-052 examines Protocol Buffers specifically; the semantic rule here is broader: wire compatibility is necessary but not sufficient for behavioral compatibility.

### Bound resources and expose overload deliberately

Every call consumes connection, stream, message bytes, decode memory, queue space, handler concurrency, downstream calls, storage, and response bandwidth. Declare maximum message sizes, stream duration/message count, metadata size, decompression ratio, queue wait, per-principal concurrency, and fan-out. Validate cheap structural limits before expensive decoding or allocation.

Overload should be visible as a specific signal with pushback where possible. Unlimited retries convert overload into collapse. Admission control rejects work before it consumes scarce capacity; concurrency limits and fair queues prevent one tenant or method from starving others. Deadlines remove obsolete queued work only when all layers observe them.

### Observe logical calls and attempts separately

Metrics need logical-call demand, attempt count, retries/hedges, deduplication hits/conflicts, client/server duration, queue time, status, deadline/cancellation, payload buckets, and committed effects. Counting attempts alone makes retry storms look like new demand; counting only logical calls hides load amplification.

Distributed traces should represent the client/server lifecycle and preserve attempt links without claiming that telemetry is a correctness ledger. OpenTelemetry's current RPC span semantic conventions define client and server spans and say a client span covers the full client-side lifecycle; the document is marked release candidate as of verification, so pin convention versions during instrumentation changes.

Use bounded attributes such as RPC system, service, method, status category, and retry number. Do not use raw request bodies, tokens, arbitrary IDs, or error messages as metric labels. Logs may include protected logical/attempt IDs and decision evidence under retention/access policy. Reconcile telemetry with durable effect records during incidents.

### Verify semantics through hostile traces

Unit tests cover validation, status mapping, and retry classification. Property tests assert stable fingerprinting and key/request conflicts. Integration tests inject drops before dispatch, during handler work, after commit, and during response. Concurrency tests race matching attempts against one key. Crash tests terminate the process between reservation, effect, result persistence, and outbox dispatch. Failover tests move calls across instances/regions. Load tests measure retry amplification and deadline cleanup. Compatibility tests run old/new clients and servers. Security tests alter identities, metadata, sizes, encodings, and authorization between attempts.

The central oracle is the domain invariant plus durable call record—not whether all client calls returned success. A test that loses the response after commit should produce one effect and a recoverable answer. A test that reuses a key with different input should produce no second effect and a conflict. A test that exhausts the deadline should show downstream cancellation and bounded cleanup.

## Definitions and Notation

Let $c$ be one logical call, $A(c)=\{a_1,\ldots,a_n\}$ its attempts, $D(a)$ the event that attempt $a$ reaches application dispatch, $X(a)$ the handler-execution count contributed by $a$, and $E(c)$ the count of durable domain effects attributable to $c$. Let $K(c)$ be its stable idempotency identity, $F(c)$ the canonical request fingerprint, $R(c)$ the durable terminal result, $B_0$ the original time budget, and $B(t)$ the remaining budget.

**Maybe execution** permits $\sum X(a)\in\{0,1\}$. **At-least-once** aims for $\sum X(a)\ge 1$ under declared reachability/retry assumptions. **At-most-once** requires $\sum X(a)\le 1$ within declared identity, durability, and retention assumptions. **Exactly-once effect** requires $E(c)=1$ for an accepted logical operation, which is not equivalent to exactly one network delivery.

An operation is **state-idempotent** when applying the same semantic command twice yields the same relevant state: $f(f(s))=f(s)$. **Outcome unknown** is the caller state in which both $E(c)=0$ and $E(c)\ge1$ remain consistent with its observations. A **commit point** is the boundary after which the declared effect survives the relevant failures. A **retry budget** bounds extra attempts/load across the logical call. **Fencing** rejects work performed by an obsolete lease/owner. **Reconciliation** compares intended calls, call records, and actual effects to repair or escalate disagreement.

## Mechanisms, Invariants, or Proof Structure

The fundamental limitation follows from indistinguishable executions. Let trace $T_0$ drop a request before dispatch and trace $T_1$ commit its effect then drop the response. Before any later durable query, the caller receives the same observation $o=$ no response. A deterministic caller decision based only on $o$ is identical for both traces. “Do not retry” may violate liveness in $T_0$; “retry as new” may duplicate the effect in $T_1$. Therefore correctness requires additional stable identity and server/domain state, an intrinsically idempotent transition, or explicit reconciliation.

For key $k=K(c)$ and fingerprint $f=F(c)$, require:

$$
\forall a_i,a_j\in A(c): K(a_i)=K(a_j)=k\land F(a_i)=F(a_j)=f.
$$

The server enforces a uniqueness invariant on $(principal,method,k)$. The first valid attempt establishes $f$ and an execution record. Any matching attempt observes the same terminal $R(c)$; any differing fingerprint is rejected. If effect and record commit in one serializable transaction, then concurrent matching attempts cannot create two effects in that transaction's domain. This is a bounded safety argument, not a universal exactly-once proof: external effects, lost durability, expired records, incorrect fingerprints, identity collisions, or bypass routes remain assumptions to test.

For nested calls, remaining budget satisfies

$$
B(t)=B_0-(t-t_0)-B_{reserve},\qquad B(t)>0
$$

before useful work begins. Retry delay and every attempt consume $B(t)$; no layer resets it. Cancellation establishes a stop-work obligation, while the effect invariant is determined independently by whether the commit point was crossed.

The following executable model deliberately loses the first response after committing a transfer. Its durable record returns the original outcome on retry and rejects key reuse with different input.

<!-- bijux-verify: {"id":"rpc-deduplication-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"first=outcome_unknown\nretry=committed:20\nbalance_a=80\nbalance_b=20\nconflict=key_conflict\n","stderr":""}} -->
```python
balances = {"A": 100, "B": 0}
records = {}

def transfer(principal, key, source, target, amount, lose_reply=False):
    identity = (principal, "Transfer", key)
    fingerprint = (source, target, amount)
    if identity in records:
        old_fingerprint, result = records[identity]
        if old_fingerprint != fingerprint:
            return "key_conflict"
        return result

    if amount <= 0 or balances[source] < amount:
        return "rejected"

    # This block models one atomic durable transaction.
    balances[source] -= amount
    balances[target] += amount
    result = f"committed:{amount}"
    records[identity] = (fingerprint, result)

    return "outcome_unknown" if lose_reply else result

print("first=" + transfer("user-7", "K", "A", "B", 20, lose_reply=True))
print("retry=" + transfer("user-7", "K", "A", "B", 20))
print("balance_a=" + str(balances["A"]))
print("balance_b=" + str(balances["B"]))
print("conflict=" + transfer("user-7", "K", "A", "B", 21))
```

Production code needs authenticated identity, a database uniqueness constraint/transaction, canonical request encoding, in-progress recovery, bounded retention, authorization on retries, and a transactional outbox or provider idempotency for external effects. The dictionary demonstrates the invariant, not those implementation guarantees.

## Alternatives and Trade-Offs

**RPC versus resource-oriented HTTP.** RPC directly names commands and supports typed unary/streaming interactions; resource APIs expose uniform protocol semantics, caches, and intermediaries more naturally. Either can be idempotent or unsafe. Choose from interaction semantics, ecosystem, evolvability, and operational boundaries rather than URL aesthetics.

**Synchronous RPC versus asynchronous job/message.** Synchronous calls give immediate feedback and simple composition when work fits a bounded latency budget. Durable jobs decouple long-running work and caller availability but add status, cancellation, deduplication, ordering, and retention. Starting a job can itself be an idempotent RPC.

**Natural idempotence versus result deduplication.** Setting desired state is simpler than caching outcomes, but may not cover secondary effects. Deduplication preserves command-shaped APIs and exact response replay, at the cost of storage, fingerprinting, retention, and recovery logic. Combine them for critical effects.

**Client-generated versus server-issued identity.** Client keys survive response loss and retry; they require entropy, scope, and misuse protection. Server IDs are authoritative after receipt but cannot help when the creation response carrying the ID is lost unless the client also supplied correlation. A client operation key plus server resource/job ID is often useful.

**Blocking, callback/future, and streaming APIs.** A blocking stub is simple but can hide resource waiting. Futures integrate concurrency but complicate cancellation/context. Streaming supports incremental data and flow control but introduces partial progress and stream-level commitment. The semantic contract must remain explicit across language bindings.

**Aggressive retries versus fast failure.** Retries mask transient faults but add latency, load, and duplication risk. Fast failure protects capacity and lets callers choose fallback, but can reduce success during brief faults. Budgets, idempotence, backoff, pushback, and admission control make the tradeoff accountable.

**Central deduplication versus domain uniqueness.** A general call ledger can replay exact outcomes across methods. Domain keys/transactions enforce the business invariant close to state. A ledger alone misses bypass paths; domain uniqueness alone may not reproduce the same response. Critical operations often need both aligned.

## Failure Modes and Misconceptions

- **“It looks like a function, so it behaves like one.”** Network, deployment, trust, and failure boundaries remain observable.
- **“A timeout means the server stopped.”** The handler may be queued, running, or committed; deadline is a local observation.
- **“Cancellation rolls back.”** It signals lost interest and should stop future work, but committed effects persist.
- **“At-most-once means the call succeeds.”** It prevents duplicate execution under assumptions; zero execution is permitted.
- **“Exactly-once is a transport option.”** Exactly-once effect needs domain identity, atomicity/idempotence, durability, retention, and recovery.
- **“A trace ID is an idempotency key.”** Diagnostic correlation may be regenerated, propagated broadly, untrusted, or differently scoped.
- **“Any retryable status is safe to retry.”** Safety depends on operation semantics and stable identity, not status alone.
- **“Each layer may retry conservatively.”** Multiplication across libraries, proxies, and services can cause a retry storm.
- **“The same key always returns the cache.”** Different fingerprints must conflict, and current authorization/privacy policy still matters.
- **“An in-memory cache provides at-most-once.”** Restarts, balancing, eviction, and region changes destroy the scope.
- **“Store the dedupe record after the effect.”** A crash between effect and record permits duplicate execution.
- **“Store the record before the effect.”** Without recoverable state, a crash can permanently suppress required work.
- **“Generated schemas guarantee compatibility.”** Wire-decodable changes can still break presence, units, ranges, defaults, or behavior.
- **“Unknown means internal error.”** Outcome unknown has a distinct recovery path; hiding it invites blind retry or abandonment.
- **“More generous deadlines improve reliability.”** They retain obsolete work, inflate queues, and consume failure budgets.
- **“Retries improve availability without cost.”** Every attempt uses capacity and may amplify a dependency outage.
- **“Read-only calls need no limits.”** Reads consume resources and can leak or trigger secondary effects.
- **“Telemetry is the source of truth.”** Traces can sample/drop; durable domain/call records decide effect correctness.

## Worked Examples

### Example 1

**Situation:** A unary `GetProfile` request is dropped before dispatch. The client deadline expires.

**Reasoning:** The operation is read-only, so a bounded retry is usually effect-safe. It is not free: the first attempt might merely be slow and both attempts can consume database capacity. The client reuses logical correlation, creates a distinct attempt, subtracts elapsed time, backs off within the remaining budget, and accepts either valid response. **Conclusion:** read-only semantics permit retry, while budget and load still constrain it.

### Example 2

**Situation:** `IncrementCounter(1)` commits, but its response is lost. The client retries without a stable operation key.

**Reasoning:** Both attempts execute `value := value + 1`; the final state rises by two. The method is non-idempotent because $f(f(x))=x+2\ne x+1$. A timeout did not prove absence of the first effect. **Conclusion:** blind retry violates the intended one-increment invariant.

### Example 3

**Situation:** `SetMode("safe")` is retried twice.

**Reasoning:** The primary state transition is idempotent: setting `safe` again leaves mode unchanged. If the handler also emits a billed notification per execution, the full operation is not effect-idempotent. Move notification through an outbox unique on operation identity or declare it repeatable. **Conclusion:** idempotence must cover all relevant effects, not only the headline row.

### Example 4

**Situation:** Two instances concurrently receive the same `CreateOrder` key and both perform “read missing, then insert.”

**Reasoning:** Both can observe absence before either writes. A process lock cannot coordinate instances. A database unique constraint plus transaction lets one reserve/commit; the loser reads the winner's compatible record. If fingerprints differ, it returns conflict. **Conclusion:** at-most-once requires atomic uniqueness at the shared durability boundary.

### Example 5

**Situation:** A three-service chain gives every hop a new two-second timeout after spending 1.7 seconds upstream.

**Reasoning:** The original caller may abandon at two seconds while downstream continues until 3.7 seconds or longer. Queued obsolete work raises tail latency. Passing the remaining roughly 0.3-second budget—and rejecting work that cannot fit—preserves caller intent. **Conclusion:** reset timeouts break the end-to-end deadline invariant.

### Example 6

**Situation:** A client receives deadline exceeded for `ReserveInventory`, while the server logs success.

**Reasoning:** Local terminal results differ because response delivery missed the deadline. The caller must not map deadline to “unreserved.” It queries `GetOperation(K)` or retries with $K$ through deduplication. The UI can display “confirming outcome” until evidence arrives. **Conclusion:** conflicting local statuses are expected; recovery uses durable operation identity.

### Example 7

**Situation:** An application, client library, and proxy each allow three attempts.

**Reasoning:** In the worst nested policy, one logical call can create $3\times3\times3=27$ attempts, before downstream fan-out. During overload, successful responses slow and retries increase, forming positive feedback. Assign the application/library one bounded policy and disable proxy mutation retries, or share a retry budget/token. **Conclusion:** independent conservative policies compose into aggressive amplification.

### Example 8

**Situation:** A client reuses idempotency key `K` for `Transfer(A,B,20)` and later `Transfer(A,B,200)`.

**Reasoning:** Returning the first cached success for the second request misrepresents intent; executing the second duplicates identity. A canonical fingerprint bound to principal/method/key detects the mismatch and returns a stable conflict without another effect. **Conclusion:** key equality is insufficient; request identity must match.

### Example 9

**Situation:** `GenerateReport` takes minutes and is implemented as one open unary RPC.

**Reasoning:** Load balancers, client mobility, deadlines, and deployment drains make a long connection fragile. Convert the call to idempotently create a durable job and return a job ID; expose status/result and authorized cancellation. Retries of creation reuse the operation key. **Conclusion:** asynchronous ownership is a better semantic fit for work that outlives a bounded call.

### Example 10

**Situation:** An RPC is cancelled after its database transaction commits but before an email provider is called.

**Reasoning:** Rolling back is impossible. Ignoring cancellation and directly calling email risks an untracked partial path. The transaction should persist an outbox event with the domain effect; a worker sends it under a provider idempotency key, records outcome, and reconciliation repairs uncertainty. The RPC may end cancelled while the durable workflow continues by explicit ownership. **Conclusion:** a commit point transfers responsibility; cancellation governs call work, not erasure of durable intent.

## Cross-Program Connections

- **Distributed Systems:** indistinguishability, partial failure, consensus, leases, and failure detectors explain why local observations cannot establish global outcome.
- **Database Systems:** unique constraints, serializable transactions, write-ahead recovery, and outbox/inbox patterns supply durable effect invariants.
- **Programming Languages and Semantics:** generated stubs map one protocol into several type, exception, concurrency, and cancellation models; observational equivalence is limited by the network.
- **Reliability Engineering:** deadlines, retry budgets, admission control, overload, and tail latency determine whether fault handling stabilizes or amplifies failure.
- **Security Engineering:** every attempt crosses an authorization boundary; replay, key scope, message limits, and metadata privacy remain explicit.
- **Observability Engineering:** logical-call and attempt telemetry exposes amplification and ambiguity but does not replace the domain ledger.

## References

1. Andrew D. Birrell and Bruce Jay Nelson, “Implementing Remote Procedure Calls,” *ACM Transactions on Computer Systems*, vol. 2, no. 1, February 1984. [Author publication index and paper](https://birrell.org/andrew/papers/ImplementingRPC.pdf).
2. IETF, RFC 5531, “RPC: Remote Procedure Call Protocol Specification Version 2,” May 2009, updated by RFC 9289. [RFC Editor](https://www.rfc-editor.org/rfc/rfc5531.html).
3. gRPC Authors, “Core concepts, architecture and lifecycle,” current documentation, verified 2026-09-02. [gRPC documentation](https://grpc.io/docs/what-is-grpc/core-concepts/).
4. gRPC Authors, “Status Codes” and “Error handling,” current documentation, verified 2026-09-02. [Status codes](https://grpc.io/docs/guides/status-codes/) and [error handling](https://grpc.io/docs/guides/error/).
5. gRPC Authors, “Retry,” “Deadlines,” and “Cancellation,” current documentation, verified 2026-09-02. [Retry](https://grpc.io/docs/guides/retry/), [deadlines](https://grpc.io/docs/guides/deadlines/), and [cancellation](https://grpc.io/docs/guides/cancellation/).
6. OpenTelemetry Authors, “Semantic conventions for RPC spans,” release-candidate specification as verified 2026-09-02. [OpenTelemetry specification](https://opentelemetry.io/docs/specs/semconv/rpc/rpc-spans/).
7. Maarten van Steen and Andrew S. Tanenbaum, *Distributed Systems*, 4th ed., distributed-systems.net, 2023, chapters on communication and fault tolerance. [Official book site](https://www.distributed-systems.net/index.php/books/ds4/).

## Exercises

### Exercise 1

Define logical call, attempt, outcome unknown, at-least-once, at-most-once, and exactly-once effect. For each of the last three, state whether it is primarily a safety or liveness claim and one required scope assumption.

### Exercise 2

A client sends `CreateInvoice(K, customer=7, amount=90)`. Trace these events: server reserves $K$; transaction commits invoice and stored result; response is lost; client retries on another instance. State the required durable records and the response. Then change the retry amount to 99 and state the result.

### Exercise 3

Diagnose a production incident: an application retries twice, a mesh retries twice, and a downstream library retries three times. Metrics show 12 attempts for some logical calls, deadline-exceeded clients, and duplicate provider charges. Give a bounded repair covering retry ownership, identity, provider effects, deadlines, and telemetry.

### Exercise 4

Compare (a) a synchronous `RenderVideo` RPC held open for 20 minutes, (b) an idempotent `StartRender` RPC returning a job ID with status/cancel methods, and (c) a durable message accepted into a queue. Evaluate outcome discovery, backpressure, cancellation, client complexity, and deployment failure. Recommend one for a public API.

### Exercise 5

Design the RPC semantics for activating a municipal emergency siren. The command is safety critical, must not activate twice for one incident, may arrive during regional partition, and operators must learn the outcome. Specify identity, authorization, concurrency, execution/effect guarantee, deadline/retry, regional behavior, audit/reconciliation, errors, and tests without claiming impossible certainty.

## Answers to the Exercises

### Answer 1

A logical call is one intended operation; an attempt is one concrete transmission/execution opportunity. Outcome unknown means the caller's observations remain compatible with both no effect and one-or-more effects. At-least-once is mainly liveness: under stated reachability, availability, retry-duration, and server-acceptance assumptions, one or more attempts execute; duplicates are allowed. At-most-once is safety: within a named principal/method/key scope, durable duplicate table, failure model, and retention horizon, no more than one handler execution occurs; zero is allowed. Exactly-once effect combines safety and liveness for an accepted domain operation: the declared durable effect occurs once. It requires stable operation identity, atomic/idempotent domain enforcement, durability/recovery, and sufficient retention; external effects require participating idempotency or reconciliation. None guarantees the caller receives the acknowledgement.

### Answer 2

The server stores a record keyed by authenticated principal, `CreateInvoice`, and $K$, containing canonical fingerprint `(customer=7, amount=90)`, execution state, invoice ID, terminal response, and retention metadata. The invoice/effect and terminal call record commit atomically, or a recoverable state machine makes their relationship equivalent. The second instance consults shared durable state, matches the fingerprint, and returns the stored invoice/result without creating another invoice. If the retry says amount 99, its fingerprint differs; the server returns idempotency-key conflict and creates no new invoice. It must not return the old success as if it applied to 99, and it must not overwrite the record.

### Answer 3

The maximum nested policy is $2\times2\times3=12$, matching the metric. Choose one accountable retry owner—normally the generated/application client for that service boundary—and disable mesh retries for mutating calls plus hidden downstream retries unless they share an explicit budget. Use one total deadline with decreasing remaining time, bounded attempts, exponential backoff/jitter, and retry throttling. Classify statuses and retry mutations only with a stable operation key/fingerprint. Carry the same domain/provider idempotency key to the charge provider or dispatch through a transactional outbox; reconcile historical duplicates and compensate/refund under policy. Instrument logical calls separately from attempts, retry owner/reason, provider idempotency outcome, dedupe hit/conflict, deadlines, and committed charges. Load/fault-test loss after commit and overload before rollout.

### Answer 4

The 20-minute unary call gives simple syntax but fragile outcome delivery, consumes connection/runtime state, interacts poorly with client mobility/deployments, and makes cancellation races opaque. `StartRender` makes acceptance a short idempotent mutation, gives a durable job ID for outcome discovery, supports explicit status/result/cancel, and lets workers apply queue/admission policy; the client must poll, subscribe, or receive a callback. Direct durable messaging provides strong buffering and producer/consumer decoupling, but public clients need broker access or an API façade, acknowledgement still means accepted rather than completed, and status/cancel must be designed separately. For a public API, choose idempotent `StartRender` plus job resources; internally it may publish a durable message. Bound queued jobs, authenticate every status/cancel, define cancellation before/after commit, and retain terminal results.

### Answer 5

Use an incident-scoped, authority-issued command ID $K$, authenticated operator/workload identity, two-person or policy-approved authorization, siren/zone target, command kind, validity interval, and canonical fingerprint. A durable regional command ledger enforces uniqueness on `(zone, incident, command kind)` and a state transition such as `armed -> activation_committed`; fencing prevents obsolete controllers. Activation hardware needs a durable command ID and deduplication, or the controller must reconcile hardware state before reissuing. During a partition, do not casually claim both availability and global uniqueness: route each siren/zone to a fenced authoritative region/controller, or fail closed and require an audited local emergency procedure. Use a short deadline for call interest, but persist accepted work under a durable job; retries retain $K$, back off, and query status. Return explicit rejected, conflict, unavailable, deadline/outcome-unknown, accepted, activated, and failed states without exposing sensitive topology. Keep tamper-evident operator/approval/command/controller/hardware acknowledgements and reconcile until every target is confirmed or escalated. Test duplicate/concurrent attempts, lost response after activation, controller crash at each boundary, stale fence, partition/failover, authorization change, deadline/cancellation, hardware acknowledgement loss, audit completeness, and operator drills. The defensible claim is one activation command/effect per incident within named ledger, controller, hardware, retention, and failover assumptions—not perfect knowledge under arbitrary partition.
