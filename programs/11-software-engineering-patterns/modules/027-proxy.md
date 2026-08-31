---
module_id: SEPAT-027
program: Software Engineering: Patterns
level: 1
module_number: 27
title: Proxy
status: complete
last_verified: 2026-08-28
---

# Proxy

## One-Page Review

### Governing question

How can a surrogate control access to a subject while preserving the subject contract, and which differences in authority, identity, latency, failure, caching, concurrency, and lifecycle must remain visible rather than being disguised as transparency?

### Essential definitions

- A **proxy** is a surrogate or placeholder that controls access to a real subject through a compatible client-facing contract.
- The **subject** is the contract shared by proxy and real subject; the **real subject** performs the underlying work.
- A **virtual proxy** delays or avoids expensive creation.
- A **protection proxy** enforces authorization or capability policy before delegation.
- A **remote proxy** represents a subject across a process or network boundary.
- A **cache proxy** may serve a valid stored result without invoking the subject.
- A **smart reference** adds reference-related behavior such as leasing, pinning, or usage accounting.
- **observational transparency** means selected client observations cannot distinguish proxy from real subject; it is always relative to a declared observation set.
- A **policy decision point** decides access; a **policy enforcement point** mediates the attempted access.
- An **indeterminate outcome** means the caller cannot know from the response whether the subject applied an effect.

### Central model, mechanism, or theorem

Let subject behavior be (S:C\times X\to Outcome(Y,E)), with operation context (C). A proxy is

$$
P(S)(c,x)=pre(c,x);\ choose\{short\ circuit,\ delegate\};\ post(outcome).
$$

For declared observation set (O), transparency requires (P(S)\approx_O S). A protection proxy intentionally differs for unauthorized contexts; a cache proxy may differ in freshness and subject-call count; a remote proxy necessarily adds delay and distributed failure. Correctness therefore comes from an explicit proxy contract, not the slogan “same interface.”

### Critical invariants

- Every protected operation is mediated or equivalent enforcement exists at every bypass path.
- Authorization is evaluated from trusted subject, resource, action, environment, and current policy; denial is the default.
- The proxy never grants stronger authority, freshness, atomicity, delivery, or failure guarantees than its mechanisms provide.
- Deadline, cancellation, trace, tenant, locale, idempotency, and authentication context propagate without widening or reset.
- Cached results are partitioned and invalidated by every semantic dimension that affects visibility or value.
- Retry occurs at one authoritative layer and only when repetition is safe or the original was not applied.
- Proxy and subject identity, equality, serialization, and lifecycle ownership are explicit.
- Added resource cost, queuing, concurrency limits, telemetry, and failure isolation are bounded and measured.

### Common failures

Common failures include treating a remote call like a local call, authorizing only cache misses, trusting caller-supplied tenant or role, permitting direct subject bypass, caching denials forever, serving one principal's result to another, resetting deadlines, double retrying, hiding partial/indeterminate effects, swallowing causes, loading lazily without synchronization, holding a global lock during remote work, closing a shared subject twice, breaking equality/reflection, unbounded buffering, proxy loops, duplicate telemetry, and claiming transparent interception where protocol semantics changed.

### Compact example

A document proxy checks current authorization before consulting its cache. An unauthorized read never reaches the subject. Two authorized reads reuse one cached immutable result, so the subject loads once. After permission revocation, the same principal is denied despite the cached value.

### Connections

[SEPAT-026](026-flyweight.md) shares immutable representation; Proxy controls access to a subject. [SEPAT-028](../ROADMAP.md) stabilizes package/module entry points, and [SEPAT-030](../ROADMAP.md) evaluates structural combinations. Proxy connects to [Network Engineering](../../24-network-engineering/ROADMAP.md), [Security Engineering](../../25-security-engineering/ROADMAP.md), and [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md).

## Governing Question

What control must mediate access to the subject, which observations may the surrogate change, and what evidence proves that no bypass, stale decision, or distributed failure invalidates the promise?

Proxy is a structural pattern, not a guarantee of invisibility. Its value is a controlled access point. Its risk is concentrating policy in a layer that clients can bypass or whose semantics they misunderstand.

## Why This Matters

Lazy loading, authorization, remote clients, caching, rate limits, leases, and instrumentation are often expressed as proxies. They can reduce cost and centralize enforcement while preserving a familiar client contract.

Yet a proxy is a new execution boundary. It may introduce latency, partial failure, stale data, identity changes, queueing, or common-mode outage. Production design must state these effects and align them with subject ownership.

## Prerequisites and Retrieval

You should understand interfaces, delegation, authorization, caching, concurrency, RPC, deadlines, retries, idempotency, and resource ownership. Retrieve these facts:

1. Authentication establishes identity evidence; authorization decides a requested action on a resource.
2. A cache hit is still a resource access and may require a current authorization decision.
3. Network success and application success can be observed differently by caller and server.
4. Cancellation is cooperative and does not necessarily undo an effect already accepted.
5. Equality, reference identity, and stable resource identity are distinct.
6. An interface signature does not encode latency, locality, failure, or consistency.

## Learning Objectives

After completing this module, you should be able to:

- derive a proxy from one controlled-access responsibility;
- state transparency relative to explicit observations;
- design secure protection and cache-proxy order;
- model virtual-proxy initialization and lifecycle under concurrency;
- expose remote deadlines, cancellation, retry, and uncertainty honestly;
- distinguish Proxy from Decorator, Adapter, Facade, Gateway, and interceptor;
- test bypass, revocation, cache isolation, races, failure, and protocol conformance;
- decide when direct references, capabilities, or platform enforcement are preferable.

## Core Exposition

### Begin with the control objective

Name the subject and the single access responsibility: defer construction, enforce authorization, cross an address space, cache reads, or manage a lease. Multiple responsibilities may be composed, but order and ownership must be visible.

A proxy that merely forwards without a control objective adds indirection. A proxy that owns many unrelated policies becomes an opaque middleware boundary.

### Define the subject contract completely

Include success values, errors, side effects, streaming, cancellation, deadlines, thread safety, resource ownership, and identity—not only method names. State whether clients may detect locality or caching.

If the surrogate changes value shape, it is also adapting. If it offers a simpler multi-component task, it is also a facade. Multiple patterns may coexist, but each responsibility needs a testable contract.

### Treat transparency as relative

For pure immutable reads, a fresh cache proxy may be value-transparent while differing in timing, telemetry, identity, and subject-call count. A protection proxy deliberately changes the unauthorized outcome. A remote proxy changes the failure domain.

List the observations clients may rely on. Do not promise Liskov-style substitutability for observations the proxy intentionally changes.

### Enforce authorization on every access

Obtain principal and tenant from trusted authentication context, not request fields. Decide using current resource, action, attributes, relationship, environment, and policy version. Deny when policy is missing or unavailable unless an explicitly reviewed fail-open case exists.

Authorize before cache disclosure. Cache decisions only with bounded validity and complete policy/resource generations. The subject should retain defense-in-depth checks when other paths exist or the proxy is not the sole enforceable boundary.

### Make bypass impossible or governed

If the proxy is a security enforcement point, ordinary clients must not obtain raw subject references, credentials, sockets, repositories, or alternate endpoints. Use package/module visibility, capability references, dependency rules, and deployment/network controls.

Administrative bypasses require narrower capabilities, separate authentication, logging, monitoring, expiry, and tests. “Everyone agrees to use the proxy” is not enforcement.

### Design virtual initialization as a state machine

Useful states include `uninitialized`, `initializing`, `ready`, `failed`, and `closed`. Decide whether failures are memoized, retried, or reset; whether concurrent callers wait, share failure, or cancel independently; and whether close races with initialization.

Publish a completely initialized subject once. Never hold a coarse lock while executing arbitrary initialization if reentrancy or long blocking can deadlock the system.

### Preserve remote semantics

Remote invocation requires serialization, compatibility, authentication, transport security, backpressure, deadline, cancellation, and error mapping. A timeout can occur after the server commits, producing an indeterminate client outcome.

Pass remaining deadline rather than resetting it. Propagate cancellation, but document that application work must cooperate and already-committed effects remain. Use idempotency or reconciliation before retrying effects.

### Cache only with a consistency contract

Define key dimensions, authorization partitioning, freshness, validation tokens/version, negative caching, invalidation, stampede control, and failure behavior. A proxy may serve stale data only when the boundary explicitly permits it.

Do not let cache availability override revocation. Separate cached data from cached policy decisions and give each its own validity conditions.

### Preserve errors and uncertainty

Map transport/framework errors into stable boundary outcomes while retaining causes internally. Distinguish unauthenticated, forbidden, absent, conflict, unavailable, deadline, cancelled, partial, and indeterminate where clients act differently.

Instrumentation or cleanup failure must not mask the primary result. Redact error details at trust boundaries without destroying operator evidence.

### Define identity and lifecycle

Proxy object identity is not necessarily subject or resource identity. Equality that unwraps may bypass policy; equality based on proxy address can duplicate registries. Expose stable resource identity explicitly.

State whether closing the proxy closes the subject, releases one lease, or only detaches the caller. Shared subjects require reference ownership that prevents premature or repeated close.

### Bound resource and concurrency behavior

Remote and cache proxies need request, queue, concurrency, buffer, and response-size limits. Streaming proxies preserve flow control and cancellation rather than buffering unbounded content.

Measure proxy overhead, hit/miss latency, policy latency, queue wait, subject attempts, rejection, stale serves, and saturation with bounded labels. Avoid duplicate logical spans when lower layers already instrument transport.

### Test the realized access graph

Unit-test proxy behavior with recording, slow, failing, and cancellable subjects. Test authorization matrices, revocation, tenant separation, cache hits/misses, initialization races, close, deadlines, duplicate requests, partial response, and malformed input.

Use architecture and deployment tests to find bypass paths. Protocol-conformance and fault-injection tests are essential for network proxies; a mock-only test cannot prove intermediary correctness.

## Definitions and Notation

Let decision (A(p,r,a,e,v)\in\{allow,deny\}) depend on principal (p), resource (r), action (a), environment (e), and policy/resource version (v). Secure disclosure requires (A=allow) at the time and scope promised by policy, including cache hits.

Let client deadline be (D), current time at proxy step (i) be (t_i), and remaining budget (b_i=\max(0,D-t_i)). The proxy passes at most (b_i) downstream.

For observation set (O), (P(S)\approx_O S) iff every experiment limited to (O) yields equivalent outcomes. Timing, locality, identity, telemetry, call count, and freshness belong to (O) only when the contract exposes them.

A remote effect can yield knowledge states `not_sent`, `rejected`, `applied`, or `indeterminate`. `deadline_exceeded` alone does not determine which effect state occurred.

## Mechanisms, Invariants, or Proof Structure

### Design procedure

1. Identify subject, clients, controlled operation, and threat/failure boundary.
2. Specify the full subject and proxy observation contracts.
3. Assign authority, context source, bypass policy, and fail behavior.
4. Model initialization, cache, remote, retry, and lifecycle states.
5. Define order relative to authorization, caching, retries, and telemetry.
6. Bound queues, buffers, keys, time, concurrency, and error disclosure.
7. Test implementation plus realized import/network access graph.
8. Measure overhead and retain direct/platform alternatives.

### Executable mechanism

This in-memory protection/cache proxy rechecks authorization before every cache access. Its record is immutable by convention; it does not model concurrency, durable policy, or distributed invalidation.

<!-- bijux-verify: {"id":"proxy-authorize-before-cache","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"guest=denied loads=0\nalice-1=design loads=1\nalice-2=design loads=1\nrevoked=denied loads=1\n","stderr":""}} -->
```python
class RecordSubject:
    def __init__(self):
        self.loads = 0
        self.records = {"doc-7": "design"}

    def read(self, document_id):
        self.loads += 1
        return self.records[document_id]


class Policy:
    def __init__(self):
        self.permissions = {("alice", "doc-7"): True}

    def authorize(self, principal, document_id):
        return self.permissions.get((principal, document_id), False)

    def revoke(self, principal, document_id):
        self.permissions[(principal, document_id)] = False


class RecordProxy:
    def __init__(self, subject, policy):
        self.subject = subject
        self.policy = policy
        self.cache = {}

    def read(self, principal, document_id):
        if not self.policy.authorize(principal, document_id):
            return "denied"
        cached = self.cache.get(document_id)
        if cached is None:
            cached = self.subject.read(document_id)
            self.cache[document_id] = cached
        return cached


subject = RecordSubject()
policy = Policy()
proxy = RecordProxy(subject, policy)

print("guest=" + proxy.read("guest", "doc-7") + " loads=" + str(subject.loads))
print("alice-1=" + proxy.read("alice", "doc-7") + " loads=" + str(subject.loads))
print("alice-2=" + proxy.read("alice", "doc-7") + " loads=" + str(subject.loads))
policy.revoke("alice", "doc-7")
print("revoked=" + proxy.read("alice", "doc-7") + " loads=" + str(subject.loads))
```

Production code would use trusted authenticated context, resource/action attributes, versioned invalidation, immutable boundary values, race-safe stampede control, and defense-in-depth at the subject.

### Proof obligations

For protection, enumerate every access path and show mediation or equivalent enforcement. For caching, prove key completeness and freshness only within the specified consistency model. For remote effects, do not collapse timeout into non-application without participant evidence.

The executable trace proves four sequential outputs only. It does not prove authorization completeness, concurrent cache safety, mutation isolation, availability, or network semantics.

## Alternatives and Trade-Offs

| Approach | Primary intent | Key difference |
|---|---|---|
| Proxy | control access through compatible subject contract | surrogate stands in for subject |
| Decorator | add composable responsibility | emphasizes behavior layering |
| Adapter | translate incompatible contract | client interface intentionally differs |
| Facade | simplify a subsystem for a task | may coordinate multiple subjects |
| Gateway | encapsulate an external system | client-side integration boundary |
| Interceptor/middleware | hook a call pipeline | often framework/protocol scoped |
| Capability reference | possession grants narrow authority | avoids ambient lookup and may replace protection proxy |
| Direct reference | no surrogate | simplest when no control is needed |

Names overlap in real systems. Classify by durable responsibility and document combined roles explicitly.

## Failure Modes and Misconceptions

### “A proxy is transparent”

Only declared observations can be equivalent. Protection, caching, remote failure, lazy creation, and timing deliberately or inevitably differ.

### “Authorization at the proxy is enough”

Only if every access path is mediated and the proxy receives trustworthy current context. Otherwise retain enforcement at the resource boundary.

### “A cache hit needs no authorization”

Disclosure is access. Check authorization before revealing cached data and account for revocation and policy version.

### “Timeout means nothing happened”

The server may have committed before the response was lost or late. Use idempotency/reconciliation and represent uncertainty.

### “Cancellation rolls back work”

Cancellation signals loss of interest. Handlers must cooperate; committed or physical effects need separate recovery semantics.

### “Lazy initialization is one null check”

Concurrency, failure, reentrancy, cancellation, and close turn initialization into a state machine.

### “Dynamic proxies enforce security automatically”

Invocation machinery supplies interception, not correct policy, complete coverage, trustworthy context, or bypass prevention.

## Worked Examples

### Example 1

A virtual image proxy exposes dimensions from metadata and loads pixels only for rendering. Concurrent render calls share one initialization; close during load transitions safely. **Conclusion:** Virtual access requires lifecycle states, not just delay.

### Example 2

A protection proxy authorizes a document cache miss but skips checks on hits. A revoked user reads cached content. Moving current authorization before cache disclosure fixes the order. **Conclusion:** Cache hits remain protected accesses.

### Example 3

An internal package exports both proxy and raw repository. Architecture tests reveal ordinary callers importing the repository. Visibility and dependency rules remove bypass. **Conclusion:** Policy convention is not a security boundary.

### Example 4

An RPC times out after the server charges a card. Automatic retry without an idempotency key charges twice. Query/reconciliation or payload-bound idempotency handles uncertainty. **Conclusion:** Remote proxies must expose indeterminate effects.

### Example 5

A proxy gives each retry a fresh two-second timeout under one two-second client budget. Passing remaining deadline stops budget amplification. **Conclusion:** Proxies preserve one end-to-end deadline.

### Example 6

A tenant cache key includes record ID but not tenant and returns identical-looking IDs across tenants. Tenant/resource generation enters the key, with authorization before access. **Conclusion:** Cache equivalence includes visibility context.

### Example 7

A streaming proxy buffers an entire unbounded response to inspect it. Memory exhausts under slow clients. Incremental bounded inspection with backpressure and cancellation restores limits. **Conclusion:** Interface compatibility includes flow control.

### Example 8

Two proxies each retry and instrument one call, creating nine subject attempts and duplicate spans. One retry owner and logical-versus-attempt telemetry restore interpretable behavior. **Conclusion:** Proxy stacks require explicit multiplicity.

### Example 9

Proxy equality unwraps its subject, allowing a caller to recover and invoke the protected object. Stable resource IDs replace unwrapping equality. **Conclusion:** Identity conveniences can bypass control.

### Example 10

A medical-image transforming proxy recompresses data protected by integrity signatures. The system disables transformation and validates end-to-end integrity with named clinical review. **Conclusion:** Intermediary transformations can invalidate high-stakes evidence.

## Cross-Program Connections

- **Object-Oriented Programming:** substitutability, delegation, identity, reflection, and lifecycle define in-process proxies.
- **Concurrent Programming:** initialization, publication, cache stampedes, cancellation, and close require protocols.
- **Software Architecture:** module boundaries and dependency rules determine whether interception is bypassable.
- **Testing and Quality:** authorization matrices, protocol conformance, fault injection, and architecture tests provide evidence.
- **Network Engineering:** intermediaries, forwarding, loops, hop-by-hop state, TLS, and flow control shape network proxies.
- **Security Engineering:** trusted context, deny-by-default, least privilege, revocation, and enforcement placement are central.
- **Distributed Systems Engineering:** partial failure, deadlines, retries, duplicate effects, and reconciliation limit transparency.
- **API and Service Engineering:** error models, compatibility, pagination, streaming, and client generation affect remote proxies.
- **Platform Engineering:** sidecars and gateways centralize controls but add common-mode and operability risk.
- **Systems Engineering:** transformations and remote actuation require integrity, hazard, and independent-control analysis.

## References

1. Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, [*Design Patterns: Elements of Reusable Object-Oriented Software*](https://www.pearson.com/en-us/subject-catalog/p/Gamma-Design-Patterns-Elements-of-Reusable-Object-Oriented-Software/P200000009480/9780321700698), Addison-Wesley, 1994. Canonical Proxy intent, participants, variants, and consequences.
2. Oracle, [`java.lang.reflect.Proxy`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/reflect/Proxy.html), Java SE 25 API, accessed 2026-08-28. Documents runtime objects that implement interfaces through customized invocation handling.
3. R. Fielding, M. Nottingham, and J. Reschke, [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html), IETF Standards Track, June 2022. Defines HTTP proxies, gateways, tunnels, forwarding, loops, and transforming-intermediary constraints.
4. Scott Rose et al., [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final), August 2020. Defines policy decision/enforcement concepts and resource-access assumptions.
5. Ramaswamy Chandramouli and Zack Butcher, [NIST SP 800-207A](https://csrc.nist.gov/pubs/sp/800/207/a/final), September 2023. Applies identity-tier policy enforcement to cloud-native gateways and sidecar proxies.
6. gRPC Authors, [“Deadlines”](https://grpc.io/docs/guides/deadlines/) and [“Cancellation”](https://grpc.io/docs/guides/cancellation/), updated 2025 and 2024, accessed 2026-08-28. Documents remaining-time propagation and cooperative cancellation behavior.
7. OWASP Foundation, [Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html), accessed 2026-08-28. Recommends least privilege, deny-by-default, per-request permission validation, and access-control testing.

## Exercises

### Exercise 1

Trace the executable protection/cache proxy and state exactly which authorization, caching, and concurrency claims it does and does not establish.

### Exercise 2

Design a virtual proxy state machine for a large immutable model under concurrent load, initialization failure, cancellation, retry, and close.

### Exercise 3

Specify a tenant-aware remote cache proxy for document reads, including keys, policy checks, freshness, deadlines, errors, telemetry, and bypass tests.

### Exercise 4

Diagnose a chain containing client retry, sidecar retry, cache, authorization, tracing, and a remote subject after duplicate writes and telemetry appear.

### Exercise 5

Review an unfamiliar proxy proposed between a clinical imaging system and diagnostic workstations without claiming medical suitability.

## Answers to the Exercises

### Answer 1

Guest authorization returns false before cache lookup or subject call, so loads stays zero. Alice is authorized, misses cache, loads `design`, and increments loads to one. The second Alice request reauthorizes, hits cache, and leaves loads one. After revocation, authorization fails before cache disclosure and loads remains one.

This proves only that one sequential implementation checks its mutable policy before its cache in four traces. It does not prove that identity is authenticated, every operation/path is mediated, policy is current/durable, records cannot mutate, cache invalidation is correct, concurrent requests load once, denial/error timing is safe, or distributed revocation works. Production evidence must cover the full access graph and mechanisms.

### Answer 2

Use `uninitialized`, `initializing(generation)`, `ready(subject,generation)`, `failed(error,retry_at,generation)`, and `closed`. An atomic transition from uninitialized to initializing is the construction linearization point; one initializer works outside a global lock while same-generation callers wait with independent cancellation. Publish only a fully initialized immutable subject. Constructor failure records a sanitized cause and retry policy; cancellation of one waiter does not cancel shared construction unless ownership policy says no interested waiters remain.

Close atomically prevents new calls, wakes waiters, cancels initialization if supported, and closes a published subject exactly once by its owner. A late initializer must observe closed and dispose its result rather than publish it. Tests cover same/different calls, reentrancy, failure/backoff/reset, waiter cancellation, initializer cancellation, close at every transition, slow construction, visibility, exactly-once close, and resource leakage. If multiple equal subjects are acceptable, document the weaker identity and use a simpler protocol.

### Answer 3

Derive tenant/principal from authenticated context and authorize `(principal, tenant, document, read, policy_version, environment)` before every disclosure. Cache immutable representations by tenant, document, representation/version, locale/encoding, and data generation; keep policy-decision caching separate with short bounded validity and revocation generation. Use validators or event-driven invalidation plus a documented stale bound; never serve cross-tenant or stale-forbidden entries.

Pass one remaining deadline and cooperative cancellation downstream. Return stable absent/forbidden/conflict/unavailable/deadline/cancelled/indeterminate categories without leaking resource existence beyond policy. Reads may retry within one owner when protocol semantics permit; cap attempts and stampedes. Trace one logical read and separate policy/cache/subject attempts; record bounded outcome, age, policy/data generation, queue wait, and correlation. Static/import, credential, routing, and network-policy tests prove ordinary callers cannot reach the subject; integration tests cover revocation, tenant collisions, stale events, partitions, corrupt entries, malformed content, duplicate instrumentation, load, and shutdown.

### Answer 4

Reconstruct the realized outer-to-inner chain and count multiplicity. Client retry times sidecar retry can multiply attempts; if the write is non-idempotent or the key is not propagated unchanged, duplicates follow. Cache must not short-circuit write semantics unless explicitly designed. Authorization precedes any protected cached disclosure and remains enforced at the resource boundary. One logical trace may legitimately contain attempt spans, but two layers must not each emit the same logical span.

Choose one retry authority closest to the layer that understands operation idempotency and transport outcome; disable the other. Bind one idempotency key to caller, operation, and payload digest, persist result/progress at the subject, propagate one deadline/cancellation, and reconcile indeterminate writes. Define logical metrics outside retry and per-attempt metrics inside. Validate deployed sidecar/client settings, not only source. Fault-inject loss before send, after accept, before/after response, deadline, restart, cache state, and telemetry exporter failure; assert bounded attempts, one logical effect, and interpretable traces.

### Answer 5

Identify whether the proxy forwards, caches, transforms, authorizes, routes, or terminates transport; each role changes the safety/security case. Preserve original pixel data, metadata, modality, patient/study identity, ordering, color/bit depth, calibration, and integrity evidence. Do not transform diagnostically significant content unless the clinical specification and validation explicitly permit it. Authenticate endpoints, authorize each study access, maintain tenant/patient isolation, encrypt transport, minimize/redact logs, and make cache retention/revocation auditable.

Model malformed studies, stale/wrong patient, partial series, duplicate/reordered instances, compression/transcoding, signature failure, proxy bypass, policy outage, network partition, timeout after transfer, disk exhaustion, failover, clock error, and workstation incompatibility. Evidence requires standards conformance, golden-image and pixel/metadata comparisons, integrity and threat analysis, performance/load/soak tests, loss/corruption/restart fault injection, privacy/audit validation, usability/workflow testing, and controlled rollout/recovery. Named radiologists, imaging physicists, clinical engineers, security/privacy, interoperability, quality, regulatory, operations, and independent verification authorities must approve. This chapter establishes no diagnostic accuracy, patient safety, privacy compliance, or regulatory suitability.
