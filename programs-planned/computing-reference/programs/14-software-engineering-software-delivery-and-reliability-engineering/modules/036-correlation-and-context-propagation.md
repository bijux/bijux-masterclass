---
module_id: SDRE-036
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 36
title: Correlation and Context Propagation
status: complete
last_verified: 2026-09-06
---

# Correlation and Context Propagation

## One-Page Review

### Governing question

How can a system carry the minimum correct execution and diagnostic context across functions, tasks, processes, protocols, and trust boundaries without leaking state, confusing correlation with authority, or coupling every component to one vendor?

### Essential definitions

- **context** is immutable execution-scoped state associated with one logical unit of work;
- a **context key** identifies one cross-cutting concern's in-process value;
- **current context** is the context associated with the caller's execution unit;
- **attach** makes a derived context current and returns a restoration token; **detach** restores the previous context;
- a **propagator** serializes selected context into a carrier and reconstructs selected context from it;
- a **carrier** is the protocol-specific container, such as HTTP headers or message properties;
- **inject** writes propagation fields; **extract** reads and validates them;
- **trace context** carries trace identity and flags; **baggage** carries application-defined correlation properties;
- a **correlation identifier** joins evidence but does not establish causality, identity, authenticity, or authorization;
- **security context** represents authenticated and authorized claims under a trust model and is not diagnostic baggage;
- **context leak** lets values outlive their intended scope; **context break** loses them too early;
- a **trust-boundary policy** decides which fields are accepted, replaced, filtered, or dropped.

### Central model, mechanism, or theorem

Represent an immutable context as a finite map $C:K\rightharpoonup V$. Updating key $k$ produces a new map

$$
C'=C[k\mapsto v]
$$

without mutating $C$. In implicit-scope systems, attach operations form a stack: attaching $C_1$ over $C_0$ yields token $\tau_1$, and detaching $\tau_1$ must restore $C_0$. LIFO restoration is a correctness invariant, not cleanup style.

For concern-specific serializer $I$ and parser $X$, propagation through carrier $H$ is

$$
H'=I(C,H),\qquad C'=X(C_{base},H').
$$

Only allowlisted, valid fields cross the boundary. $C'$ is derived evidence, not a trusted copy of every sender value.

### Critical invariants

- contexts are immutable or behave as immutable values;
- attach/detach pairs are balanced and restored in LIFO order;
- task creation captures the intended context, not a later mutable global;
- extract occurs before handling and inject occurs from the intended outbound context;
- parsing failure preserves a safe base context and never crashes the request path;
- trace, baggage, request, idempotency, and security identities remain distinct;
- carrier names, formats, limits, and duplicate-field behavior follow the transport contract;
- baggage is allowlisted, bounded, purpose-limited, and free of secrets and personal data;
- remote sampling, tenant, role, and debug claims never grant authority;
- propagation success, rejection, stripping, conflict, and breakage are observable.

### Common failures

Failures include storing request context in a process global, inheriting it into detached work, failing to restore after nested scope, attaching in one thread and detaching in another, injecting the inbound parent rather than the new client span, copying every header, accepting multiple conflicting formats silently, treating a trace ID as user identity, placing credentials in baggage, turning baggage into metric labels, forwarding hop-by-hop fields, relying on thread-local storage across asynchronous scheduling, and assuming a present header means the downstream telemetry record exists.

### Compact example

A server extracts W3C trace fields into a safe base context, validates an internal tenant hint against authenticated state, and drops all other inbound baggage. It attaches the derived context for the handler and restores it in `finally`. Each child task receives an explicit immutable snapshot. An outbound client span derives a new context; a composite propagator injects only approved trace and baggage fields into the request carrier. At an external boundary, baggage is cleared while a fresh trace may be linked according to policy. Counters record invalid, stripped, conflicting, and oversized fields.

### Connections

[SDRE-032](032-structured-logging.md) consumes correlation fields, [SDRE-034](034-distributed-tracing.md) gives trace context its graph meaning, and [SDRE-035](035-events-and-change-annotations.md) correlates changes. [API-033](../../28-api-and-service-engineering/modules/033-authentication-context-propagation.md) owns authentication context.

## Governing Question

Cross-cutting concerns need state wherever an operation travels. A tracer needs the current span, a logger needs correlation identity, a deadline mechanism needs remaining time, and a feature evaluator may need a stable cohort. Passing every value through every business function creates coupling; hiding values in globals creates contamination. Context provides an explicit or language-integrated execution-scoped carrier.

Distributed propagation adds serialization and trust. In-process state may include objects and capabilities that must never cross a process boundary. A network carrier contains attacker-controlled bytes. A protocol may combine, reorder, normalize, or remove fields. Correct design chooses which concern is serialized, validates its representation, derives local state, and applies boundary policy.

The governing question is not “how do we forward a correlation ID?” It is which context belongs to this work, which parts may cross this particular boundary, what semantics survive translation, how scope ends, and what evidence reveals a break or leak.

## Why This Matters

Broken context fragments traces, loses log correlation, misattributes change exposure, and makes one user operation appear as unrelated records. Leaked context is worse: one request's tenant, trace, deadline, or experiment state can contaminate another. Under concurrency, a global variable may appear correct in tests and fail nondeterministically in production.

OpenTelemetry Specification 1.60.0 defines stable immutable context semantics and balanced attach/detach operations [1]. Its stable Propagators API separates concern state from carrier access and defines extract and inject behavior, including safe parse failure and composite propagators [2]. This division is durable: context is in-process scope; propagation is boundary-specific serialization.

The stable OpenTelemetry Baggage API describes application-defined properties associated with a distributed request and explicitly supports clearing baggage before an untrusted process [3]. W3C Baggage standardizes an HTTP field but assigns no application semantics to its values [5]. Therefore syntactic interoperability does not establish that `tenant=premium` is true, authorized, safe, or useful.

W3C Trace Context standardizes `traceparent` and `tracestate`, their validation and mutation, and privacy/security constraints [4]. Current OpenTelemetry guidance recommends avoiding credentials, API keys, and personal information in baggage [8]. RFC 9110 supplies the surrounding HTTP field and intermediary semantics [6]. Non-OTLP log compatibility guidance defines how trace and span identifiers can be represented for correlation without turning a log record into a span [7].

## Prerequisites and Retrieval

Retrieve immutable value, finite map, stack, dynamic scope, lexical scope, thread, asynchronous task, callback, process, request, message, header field, serializer, parser, carrier, interceptor, trace ID, span ID, baggage, authentication, authorization, tenant, deadline, trust boundary, allowlist, size limit, duplicate, and idempotency.

From SDRE-032 retrieve typed log records and trace correlation fields. From SDRE-034 retrieve root, parent, span context, sampling flag, asynchronous links, and trust-boundary restart. From SDRE-035 retrieve change identity and event provenance. From API-033 retrieve independently validated security identity.

## Learning Objectives

After completing this module, you should be able to:

1. model immutable execution context and nested restoration;
2. distinguish explicit, implicit, thread-local, and task-local propagation;
3. implement extract–derive–attach–handle–detach safely;
4. implement derive–inject–send for outbound calls;
5. separate trace, baggage, request, idempotency, deadline, and security context;
6. choose propagation formats and resolve coexistence during migration;
7. apply validation, size, privacy, and trust-boundary policies;
8. preserve context across queues, fan-out, callbacks, and detached work;
9. diagnose context breaks, leaks, conflicts, and stale capture;
10. test propagation under concurrency and failure.

## Core Exposition

**Begin with immutable execution scope.** Treat context as a persistent map: setting a value returns a derived context while the parent remains unchanged. Two sibling tasks can derive different values without racing over a shared object. Immutability does not make contained values safe if those values themselves are mutable; store stable handles or values with clear ownership.

Context keys belong to concerns, not arbitrary string conventions. Opaque keys prevent unrelated libraries from colliding merely because both choose `request_id`. Higher-level APIs should mediate access so business code does not depend on tracing internals [1]. Context is not a general dependency container; database clients, configuration services, and large domain objects need explicit ownership.

An explicit-context API passes $C$ as a parameter. This is visible and testable but can dominate signatures. An implicit API associates current context with the execution unit. It reduces plumbing but requires exact scope restoration and runtime support. Whichever style is used, make lifetime and task transfer observable in tests.

Attach returns a token representing the previous state. Always detach in a guaranteed cleanup path. If code attaches $C_1$, then $C_2$, detaching the token for $C_1$ first corrupts nesting. A runtime may warn, but an application must not rely on warnings to repair scope.

Thread-local storage is sufficient only when logical work never migrates or interleaves on a thread. Event loops routinely run many requests on one thread; thread pools move continuations; callbacks outlive lexical callers. Use runtime task-local/context mechanisms or explicit capture. Capture at task creation when inheritance is intended. Detached background work should usually receive a deliberately reduced context and new lifecycle.

**Separate concerns.** Trace context contains correlation identity and sampling-related vendor state. Baggage contains application-defined correlation values. A request ID may be an application or gateway identifier useful when tracing is absent. An idempotency key names a replay domain. A deadline constrains remaining time. Security context contains authenticated claims and authorization decisions. Similar strings do not make these interchangeable.

Never authorize from `traceparent`, baggage, or a request ID. An attacker can send syntactically valid values. Validate authentication through the security mechanism and, if useful, derive a bounded telemetry attribute such as authenticated subject class from trusted local state. Do not propagate bearer tokens through diagnostic APIs.

Do not copy baggage automatically into every span, log, or metric. That creates disclosure and cardinality. Define an allowlist with owner, type, maximum encoded size, destination boundaries, retention, and signal mapping. A cohort might be safe as a bounded span attribute; an account number is not. The same field can be acceptable inside one domain and forbidden externally.

**Extract before creating local work.** An inbound interceptor starts from a safe base context, invokes configured propagators against the carrier, validates the result, applies boundary policy, then creates the local operation. OpenTelemetry requires parse failure not to throw and not to overwrite an existing valid value [2]. Record invalid input safely without echoing arbitrary bytes.

Header names and duplicate behavior belong to the transport adapter. HTTP field combination is not equivalent to message metadata or a binary RPC map. Use the official getter/setter for the library. Do not lowercase values, comma-join fields blindly, or treat response propagation as automatically safe. RFC 9110 distinguishes end-to-end fields from connection-specific behavior [6].

A composite propagator runs concerns in configured order. During migration, accepting W3C and a legacy format can yield two valid but conflicting parents. Specify precedence, record conflict, and inject one canonical format or a documented dual-write. Silent last-writer-wins creates topology that depends on library order.

**Derive before injecting outbound work.** For a traced client call, create the client span from current context and inject the resulting child context, not the unchanged inbound context. Otherwise the remote server becomes a sibling of the client operation and the client duration disappears from ancestry. Injection writes to a fresh or safely mutable outbound carrier; stale fields from retries or pooled objects must be cleared.

One retry is a new attempt and should derive its own span context while preserving operation-level request or idempotency semantics. Do not reuse a mutable carrier across concurrent attempts. A redirect crosses a new destination and therefore re-evaluates which baggage and credentials may be forwarded.

**Model messages and fan-out.** A producer captures context at send time into message properties. A broker may reject, transform, or strip properties; test the actual protocol path. A consumer extracts from the delivered message, not from process current state left by another delivery. Redelivery carries the original producer context but begins a new consumer attempt.

When one message causes one operation, remote parenting can express continuity. A batch with many inputs needs links or a batch context rather than one arbitrary parent. When a scheduler accepts work now and executes it days later, continuing the original trace may exceed retention and distort lifecycle. Record a durable correlation ID, start a new trace, and link if supported.

Fan-out tasks should receive the same immutable parent snapshot and derive their own children. If a child mutates shared baggage, siblings must not observe the change. Fan-in needs explicit result association; whichever task finishes last does not become the causal parent by accident.

**Budget carrier cost.** If encoded fields have sizes $b_1,\ldots,b_n$ and framing overhead $h$, propagated size is

$$
B=h+\sum_{i=1}^{n}b_i.
$$

It must remain below the strictest relevant application, proxy, broker, and protocol limit. A limit is not a target. Added bytes consume network, parsing, queue, and log capacity on every hop. Enforce per-entry and total budgets before injection and after extraction.

If a request fans out to $m$ downstream calls, one added baggage byte can be transmitted at least $m$ times at that layer, before retries and deeper fan-out. Cost and disclosure multiply through topology. Prefer locally derived resource attributes when downstream services can determine the value independently.

**Respect standards without confusing syntax and semantics.** W3C Trace Context gives interoperable trace identity. Its sampled flag is advice, not authorization or guaranteed storage. `tracestate` is bounded vendor state and cannot contain personal data [4]. W3C Baggage gives a list-member format and limits, not a universal vocabulary [5].

OpenTelemetry Baggage uses one value per key even though the wire standard can represent duplicates [3]. Conflict and duplicate behavior must be tested at translation. Percent encoding, whitespace, case sensitivity, and metadata need standard parsers rather than handwritten splitting.

At a public ingress, accept valid trace context when correlation value outweighs abuse risk, or restart it by policy. Strip baggage unless explicitly allowlisted. At egress to an external party, clear internal tenant, routing, experiment, and topology hints. A trace restart breaks continuity, so record a safe internal link or boundary event when policy permits; security takes priority over convenience.

**Correlate evidence honestly.** Inject trace and span identifiers into logs through supported integration. A matching trace ID makes records candidates for the same trace; collection loss and forged input remain possible. Change IDs, release versions, and resource identities can connect changes to requests when their source semantics agree.

Correlation does not prove causality. A request ID copied into two logs shows an asserted join. The relationship may be wrong because of reuse, truncation, stale context, or attacker input. Validate controlled histories and preserve provenance.

The deterministic model below demonstrates immutable derivation, allowlisted injection, and LIFO restoration. It is not a production propagator or security mechanism.

<!-- bijux-verify: {"id":"immutable-context-scope","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"base tenant: trusted-a\nchild tenant: trusted-b\ninjected keys: cohort,traceparent\nrestored tenant: trusted-a\n","stderr":""}} -->
```python
def derive(context, key, value):
    return context + ((key, value),)

def lookup(context, key):
    values = [value for name, value in context if name == key]
    return values[-1] if values else None

base = (("tenant", "trusted-a"), ("traceparent", "00-valid-model"))
child = derive(base, "tenant", "trusted-b")
child = derive(child, "cohort", "control")

stack = [base]
token = len(stack)
stack.append(child)
allowlist = {"traceparent", "cohort"}
carrier = {
    key: lookup(stack[-1], key)
    for key in sorted(allowlist)
    if lookup(stack[-1], key) is not None
}
assert len(stack) == token + 1
stack.pop()

print("base tenant:", lookup(base, "tenant"))
print("child tenant:", lookup(child, "tenant"))
print("injected keys:", ",".join(sorted(carrier)))
print("restored tenant:", lookup(stack[-1], "tenant"))
```

**Observe and test the mechanism.** Count extraction attempts, valid/invalid/oversized fields, format conflicts, baggage entries stripped, injections, missing downstream parents, context attach/detach mismatch, and carrier bytes. Avoid labels containing raw IDs. Sample safe diagnostic details when counts indicate trouble.

Test nested scope, exceptions, cancellation, async suspension, thread-pool hops, fan-out, fan-in, callbacks, detached work, queue delay, redelivery, retry, redirects, proxy rewriting, duplicate headers, invalid encoding, multiple formats, and boundary stripping. Use concurrent controlled requests with distinct sentinel values and assert zero cross-request contamination.

Context correctness is end-to-end. A unit test of inject/extract does not show that the framework interceptor runs in the right order, the broker preserves fields, or logs read context before detachment. Run a known path and compare expected context at every boundary.

## Definitions and Notation

Let $C:K\rightharpoonup V$ be a finite partial map. `set` returns $C'=C[k\mapsto v]$ and leaves $C$ unchanged. Let scope stack be $S=(C_0,\ldots,C_n)$ with current context $C_n$. Attach pushes a context and returns a token identifying the prior stack state; valid detach restores that exact state.

Let $I_q(C,H)$ inject concern $q$ into carrier $H$ and $X_q(C,H)$ extract it into a context derived from safe base $C$. Let allowlist $A_q$ select permitted fields. A safe extractor validates syntax, size, multiplicity, and boundary policy before adding values.

For encoded entry sizes $b_i\ge0$ and framing $h\ge0$, carrier contribution is $B=h+\sum_i b_i$. If a layer fans out to $m$ calls without retries, transmitted contribution is at least $mB$ at that layer; actual cost includes protocol compression, framing, retries, and deeper topology.

For a controlled set of $N>0$ operations, contamination rate is $r=x/N$, where $x$ operations observed another operation's sentinel context. Passing requires $x=0$ for the tested schedule, which is evidence for that schedule rather than proof over all interleavings.

## Mechanisms, Invariants, or Proof Structure

**Immutability argument.** Because derive returns a new map and leaves $C$ unchanged, sibling derivations from $C$ cannot overwrite each other's bindings through the context map. Mutable referenced values or unsafe globals can still race, so immutability is necessary but not sufficient.

**Stack-restoration argument.** Nested scopes have last-attached as current. Only detaching the corresponding top token restores the immediately prior context. Out-of-order detach skips or resurrects state and violates dynamic scope.

**Parse-failure safety.** If extraction failure returns the unchanged safe base and does not throw, malformed remote data cannot create a new concern value or directly abort handling through the propagator. Resource exhaustion and unsafe logging require separate bounds.

**Authority separation.** The same carrier is attacker writable at an external boundary. Therefore possession of a syntactically valid correlation field cannot entail an authenticated principal or permission. Authorization needs an independently verified security mechanism.

**Fan-out cost.** Every injected carrier copy includes $B$ bytes. Creating $m$ copies transmits at least $mB$ before lower-layer overhead. This linear bound explains why small baggage grows expensive across wide and deep graphs.

**Correlation limitation.** Equal identifiers can arise from correct propagation, collision, reuse, stale scope, copying, or forgery. Since these mechanisms produce the same equality observation, equality alone cannot identify causal or authentic relationship.

## Alternatives and Trade-Offs

1. **Explicit versus implicit context.** Explicit values improve visibility; implicit scope improves ergonomics but raises leak risk.
2. **Thread-local versus task-local.** Thread-local is simple for synchronous ownership; task-local follows asynchronous work but depends on runtime integration.
3. **Automatic versus manual propagation.** Interceptors provide coverage; manual control handles unusual boundaries but drifts.
4. **One versus composite format.** One canonical format avoids conflict; composite extraction enables migrations with precedence complexity.
5. **Continue versus restart traces.** Continuation preserves correlation; restart reduces cross-boundary tracking and abuse.
6. **Baggage versus local derivation.** Baggage transports decisions; local derivation reduces disclosure and cost.
7. **Parent versus link.** Parent models one primary cause; links preserve fan-in without false ancestry.
8. **Request ID versus trace ID.** A request ID can survive without tracing; a trace ID integrates span topology. Mapping must be explicit.
9. **Fail-open versus fail-closed diagnostics.** Invalid diagnostic context usually falls back safely; security context follows its own authorization policy.

## Failure Modes and Misconceptions

1. **“Context is a global dictionary.”** Scope and immutable derivation are essential.
2. **“Thread-local means request-local.”** Event loops interleave requests on one thread.
3. **“Attach cleanup is optional.”** Missing detach contaminates later work.
4. **“Children can mutate inherited baggage.”** Siblings then race over meaning.
5. **“Copy every inbound header.”** Carriers contain unrelated and untrusted fields.
6. **“A valid trace ID is trusted.”** Syntax is not authenticity.
7. **“Baggage is authorization context.”** It has no such guarantee.
8. **“Baggage belongs on every metric.”** Raw values can explode cardinality and disclosure.
9. **“Injection uses the incoming parent.”** Outbound work needs the derived client context.
10. **“One carrier object can serve concurrent retries.”** Mutation causes cross-attempt races.
11. **“Multiple propagation formats always agree.”** Migrations can produce conflicting parents.
12. **“Message redelivery continues one consumer attempt.”** It is a new attempt over original message context.
13. **“Detached jobs should inherit everything.”** Their lifetime and trust boundary differ.
14. **“Header presence proves trace storage.”** sampling and export can remove evidence.
15. **“Standards define baggage meaning.”** They define representation, not domain truth.
16. **“Unit tests prove propagation.”** Framework and transport integration can still break.

## Worked Examples

### Example 1

**Nested restoration.** Handler attaches $C_1$ over $C_0$, library attaches $C_2$, then library detaches its token before handler detaches. The sequence restores $C_1$ then $C_0$. **Conclusion:** LIFO tokens preserve dynamic scope.

### Example 2

**Out-of-order detach.** If the handler detaches $C_1$ while $C_2$ is current, it can erase or later resurrect library state. A token check should reject or signal the order error. **Conclusion:** balanced counts alone do not prove correct nesting.

### Example 3

**Async contamination.** Two requests interleave on one event-loop thread while a thread-local stores tenant. Request B overwrites A before A resumes. Task-local snapshots keep values separate. **Conclusion:** execution units, not threads alone, define scope.

### Example 4

**Outbound parent.** A server span `s` creates client span `c`. Injecting `s` makes the remote server a sibling of `c`; injecting `c` makes it the child of the attempt. **Conclusion:** derive before inject preserves topology.

### Example 5

**Malformed input.** An inbound `traceparent` has invalid length and an oversized `baggage`. Extraction retains the safe base, records bounded rejection counters, and handles the request without echoing values. **Conclusion:** diagnostics fail safely without trusting malformed state.

### Example 6

**Format conflict.** W3C and legacy headers contain different trace IDs. Policy accepts W3C, logs a conflict class, and emits only W3C downstream during migration. **Conclusion:** composite propagation needs deterministic precedence.

### Example 7

**Carrier budget.** Four encoded entries of 40, 30, 20, and 10 bytes plus 16 bytes framing yield $B=116$ bytes. Fan-out to 25 calls transmits at least 2,900 bytes at that layer. **Conclusion:** baggage cost multiplies with topology.

### Example 8

**Security separation.** External baggage says `role=admin`; a validated access token says `role=viewer`. Authorization uses the token-derived viewer role, and telemetry may record a bounded mismatch event. **Conclusion:** diagnostic propagation cannot override authenticated security context.

### Example 9

**Batch fan-in.** Ten messages have ten producer contexts. The batch consumer starts one operational span with links and derives a new batch context rather than selecting the last extracted message as current. **Conclusion:** fan-in requires explicit many-cause semantics.

### Example 10

**Detached work.** A request schedules a report for tomorrow. The scheduler stores a durable job ID and safe provenance, clears request baggage, and the worker starts a new trace linked to the scheduling evidence. **Conclusion:** long-lived work gets an intentional lifecycle rather than stale request scope.

## Cross-Program Connections

1. [API-010](../../28-api-and-service-engineering/modules/010-tracing-a-request-through-client-proxy-and-service.md) defines the HTTP path that carries trace fields.
2. [API-033](../../28-api-and-service-engineering/modules/033-authentication-context-propagation.md) owns authenticated context and prevents diagnostic authority confusion.
3. [API-037](../../28-api-and-service-engineering/modules/037-idempotency-keys.md) distinguishes replay identity from trace identity.
4. [API-061](../../28-api-and-service-engineering/modules/061-commands-events-and-messages.md) supplies asynchronous message roles.
5. [SDRE-032](032-structured-logging.md) consumes safe trace and span correlation fields.
6. [SDRE-034](034-distributed-tracing.md) interprets propagated parent and link relationships.
7. [SDRE-035](035-events-and-change-annotations.md) adds change identities derived from authoritative sources.
8. Security Engineering owns authentication, authorization, trust, and privacy controls.
9. Concurrent Programming owns task-local state and interleaving mechanisms.
10. Platform Engineering owns shared interceptor and propagator products while services own domain baggage semantics.

## References

1. OpenTelemetry, “Context,” OpenTelemetry Specification 1.60.0, Stable, retrieved 2026-09-06. https://opentelemetry.io/docs/specs/otel/context/
2. OpenTelemetry, “Propagators API,” OpenTelemetry Specification 1.60.0, Stable except where noted, retrieved 2026-09-06. https://opentelemetry.io/docs/specs/otel/context/api-propagators/
3. OpenTelemetry, “Baggage API,” OpenTelemetry Specification 1.60.0, Stable, retrieved 2026-09-06. https://opentelemetry.io/docs/specs/otel/baggage/api/
4. W3C, *Trace Context*, Recommendation, 23 November 2021, retrieved 2026-09-06. https://www.w3.org/TR/trace-context/
5. W3C, *Propagation Format for Distributed Context: Baggage*, current specification retrieved 2026-09-06. https://www.w3.org/TR/baggage/
6. IETF, RFC 9110, *HTTP Semantics*, June 2022. https://www.rfc-editor.org/rfc/rfc9110
7. OpenTelemetry, “Trace Context in non-OTLP Log Formats,” Specification 1.60.0, retrieved 2026-09-06. https://opentelemetry.io/docs/specs/otel/compatibility/logging_trace_context/
8. OpenTelemetry, “Context Propagation,” current concepts documentation, retrieved 2026-09-06. https://opentelemetry.io/docs/concepts/context-propagation/

## Exercises

### Exercise 1

Distinguish context, propagator, carrier, trace context, baggage, request ID, idempotency key, and security context. Give one unsafe substitution.

### Exercise 2

Entries encode to 48, 32, 24, and 16 bytes with 20 bytes framing. Calculate $B$ and the minimum bytes copied across fan-out of 40 calls. State two omitted real costs.

### Exercise 3

Two asynchronous requests occasionally exchange tenant and trace values. Design a focused diagnosis across scope capture, attach/detach, pooled carriers, and logging.

### Exercise 4

Design a migration from legacy and W3C trace propagation across five services. Specify extraction precedence, injection, conflict evidence, rollout, and rollback.

### Exercise 5

A scientific workflow fans out 1,000 tasks, combines results, and runs for a month across organizations. Design correlation and context boundaries without one enormous trace or cross-organization data leakage.

## Answers to the Exercises

### Answer 1

Context stores execution-scoped values; a propagator serializes selected concern state; a carrier holds protocol fields. Trace context carries trace identity and flags. Baggage carries application-defined correlation properties. Request ID identifies an application request, idempotency key identifies a replay domain, and security context contains independently authenticated and authorized claims. Using baggage `role=admin` as authorization is unsafe because remote baggage is not authenticated authority.

### Answer 2

$B=20+48+32+24+16=140$ bytes. Forty copies transmit at least $40\times140=5{,}600$ bytes at that layer. The bound omits protocol framing/compression, retries, deeper fan-out, parsing and allocation, queue/storage cost, and possible logging or indexing. Any two of these with explanation satisfy the second part.

### Answer 3

Run concurrent requests with unique safe sentinels and forced suspension points. Verify task-local rather than process/thread-global storage, capture time at task creation, and LIFO token restoration in exception and cancellation paths. Inspect whether a pooled outbound carrier retains old fields and whether retries mutate one carrier concurrently. Ensure logging reads current context inside scope rather than in a later callback. Count contamination and require zero in the controlled schedule; then stress varied interleavings. Instrument scope mismatch without logging raw tenants.

### Answer 4

Configure a composite extractor that prefers valid W3C, falls back to legacy only when W3C is absent or invalid under documented rules, and records bounded presence/conflict classes. Initially inject both formats derived from one canonical local span context. Roll out readers before writers, compare parent continuity and conflicts, then switch writers to W3C-only service by service. Keep a rollback switch for dual injection. Never merge conflicting IDs silently or use format fields for authority. Completion requires all supported paths—including retries, proxies, and queues—to pass controlled continuity tests before legacy extraction is removed.

### Answer 5

Give the workflow a durable domain ID and safe provenance record. Start bounded traces per stage, organization, or time window, and link each stage root to the workflow and selected predecessor contexts. Each of 1,000 tasks derives from a stage snapshot and gets its own child or trace segment; fan-in uses links or durable manifests rather than an arbitrary last parent. At organization boundaries, restart traces, clear baggage, and propagate only agreed opaque workflow/stage IDs with purpose, size, retention, and access policy. Keep authentication separate. Metrics summarize all tasks; sampled traces diagnose examples; durable workflow records preserve membership. A strong alternative segmentation is acceptable if it bounds graph size and retention, preserves navigable provenance, and prevents cross-domain sensitive propagation.
