---
module_id: SEPAT-031
program: Software Engineering: Patterns
level: 1
module_number: 31
title: Chain of Responsibility
status: complete
last_verified: 2026-08-28
---

# Chain of Responsibility

## One-Page Review

### Governing question

How can a sender offer a request to an ordered set of potential handlers without knowing which will act, while making handling completeness, short-circuiting, continuation, failure, context, order, concurrency, and operational evidence explicit?

### Essential definitions

- A **chain of responsibility** is an ordered sequence or linked structure of handlers that may handle a request or pass it onward.
- A **handler** evaluates one request under a shared contract and returns an explicit disposition.
- **pass** means this handler declines and permits the next handler to consider the request.
- **handled** means a handler produced the terminal successful result.
- **rejected** means a handler intentionally stops processing with a domain/policy denial.
- **failed** means processing could not complete because a required mechanism failed.
- A **terminal handler** supplies a final result when earlier handlers pass.
- **short-circuiting** stops traversal before later handlers execute.
- **fall-through** occurs when no handler claims a request; it must be an explicit outcome or be prevented by a completeness rule.
- **around-chain behavior** runs before and after downstream handling; it resembles middleware/Decorator and has different control flow from simple first-match handling.

### Central model, mechanism, or theorem

Let ordered handlers be $H=(h_1,\ldots,h_n)$, where

$$
h_i:C\times X\to Pass\mid Handled(Y)\mid Rejected(R)\mid Failed(E).
$$

Dispatch finds the least index (j) whose result is not `Pass` and returns that result; if none exists it returns `Unhandled` unless a total terminal handler is guaranteed. Thus order is semantic. Completeness requires

$$
\forall(c,x)\in D,\ \exists i:\ h_i(c,x)\ne Pass
$$

for the declared input domain (D), or an explicit `Unhandled` contract.

### Critical invariants

- Handler dispositions are explicit; `None`, exceptions, and partial mutation do not ambiguously mean pass.
- Realized order, eligibility predicates, terminal behavior, and multiplicity are deterministic and inspectable.
- Exactly the declared handlers run before and after the terminal disposition; skipped handlers have no hidden required effect.
- Authentication/authorization/validation cannot be bypassed by an earlier unsafe terminal handler.
- Deadline, cancellation, trace, tenant, locale, idempotency, and request identity propagate across every continuation.
- Mutable handler state is safely scoped for concurrent, reentrant, and asynchronous requests.
- Failure, rejection, unhandled, cancellation, and timeout remain distinct outcomes.
- Chain length, per-handler cost, buffers, telemetry cardinality, and dynamic reconfiguration are bounded.

### Common failures

Common failures include implicit `None` pass semantics, assuming some handler will act, putting a cache/static route before authorization, allowing multiple handlers to mutate before passing, registering duplicates, relying on container order accidentally, building cyclic linked handlers, catching failure and continuing unsafely, invoking next twice, forgetting post-processing after exceptions, storing request state in shared handlers, losing async context/cancellation, changing a live chain mid-request, unbounded plugin handlers, and emitting one high-cardinality metric/span per handler.

### Compact example

A request crosses a size guard, then a health-route handler, then a terminal not-found handler. `/health` is handled after two visits; an oversized request is rejected by the first handler; an unknown small path reaches the explicit terminal result. No outcome depends on implicit fall-through.

### Connections

[SEPAT-030](030-combining-structural-patterns-without-indirection-explosion.md) validates structural pipelines; Chain of Responsibility focuses on behavioral handler selection. [SEPAT-032](../ROADMAP.md) encapsulates requests as commands, and [SEPAT-035](../ROADMAP.md) centralizes peer coordination. It connects to [Concurrent Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md), [Security Engineering](../../25-security-engineering/ROADMAP.md), and [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md).

## Governing Question

Which handler is allowed to stop, pass, reject, or fail for each request, and what invariant proves that order and fall-through cannot bypass required policy or silently lose work?

The pattern decouples sender from receiver selection. It does not remove the need to specify who must handle, what handlers may change, or how ordering is governed.

## Why This Matters

Routing, validation, policy evaluation, support escalation, logging, compiler passes, event processing, and web middleware often use chains. New handlers can be added without changing senders, and specialized receivers can decline unfamiliar work.

Flexibility can hide control flow. A handler may disappear, run twice, short-circuit security, or pass after partial effects. Production chains require explicit result algebra, validated configuration, and end-to-end tests.

## Prerequisites and Retrieval

You should understand interfaces, discriminated outcomes, predicates, ordering, exceptions, async context, cancellation, middleware, and authorization. Retrieve these facts:

1. First-match selection makes order part of externally visible behavior.
2. A handler that passes after mutation can leave effects even when a later handler fails.
3. “No result” may mean absent, unhandled, failed, cancelled, or programming defect; these differ.
4. Around middleware unwinds in reverse after downstream returns; simple chains need not.
5. Shared handler instances may process requests concurrently.
6. Dynamic configuration must be validated and snapshotted before use.

## Learning Objectives

After completing this module, you should be able to:

- define an explicit handler-disposition algebra;
- derive and test order and completeness requirements;
- distinguish selection chains from middleware, pipelines, events, and rule engines;
- control mutation, failure, cancellation, and asynchronous continuation;
- validate dynamic registrations, cycles, duplicates, and terminal coverage;
- secure chains against short-circuit and bypass errors;
- instrument logical outcomes without unbounded per-handler noise;
- contract or replace chains when selection rules become clearer as data.

## Core Exposition

### Choose the chain semantics first

Classical Chain of Responsibility often stops at the first handler that accepts. Other systems let every handler observe, transform, or run around downstream work. These are different protocols.

Declare whether zero, exactly one, at most one, or many handlers act. Do not combine selection, broadcast, transformation, and around behavior behind one ambiguous `handle` contract.

### Use explicit dispositions

Return a closed outcome such as `Pass`, `Handled(value)`, `Rejected(reason)`, or `Failed(error)`. Add `Deferred(token)` only if ownership and resumption are specified.

Exceptions represent exceptional mechanism/program failures according to language policy; they should not double as normal “not mine” control flow. Preserve causes and never convert rejection into system failure casually.

### Make completeness a policy

Some chains legitimately return `Unhandled`, such as extensible media decoders. Others require a terminal handler, such as HTTP routing that returns not found. State the domain and coverage rule.

For finite predicate domains, property or model tests can check coverage and overlap. For open domains, a total fallback or explicit unhandled result is more honest than an unverifiable assumption.

### Treat order as configuration with semantics

Attach stable IDs, priorities or before/after constraints, required capabilities, conflicts, and multiplicity. Validate duplicates, cycles, missing prerequisites, ambiguous material orders, and unreachable handlers before publishing a chain.

Snapshot an immutable realized order per request/configuration generation. Live mutation during traversal creates nondeterministic coverage and lifecycle hazards.

### Keep pass side-effect-light

Ideally a handler that passes performs only bounded observation. If it mutates request/context, reserves resources, or emits durable effects before passing, declare composition and rollback/cleanup semantics.

Do not let multiple handlers partially own one business operation accidentally. Use a pipeline/workflow or transaction protocol when multiple sequential effects are required.

### Protect security ordering

Authentication establishes trusted identity; authorization checks a current action/resource. A public/health/static handler may intentionally precede authentication only for explicitly public paths. A cache or fallback must not disclose protected data before authorization.

Test the realized routing table against protected-path policy. One unsafe terminal route is enough to bypass later security handlers.

### Preserve context and budgets

Pass one request context containing identity, tenant, trace, absolute deadline, cancellation, locale, and idempotency where applicable. Each handler consumes bounded time and passes remaining budget.

A handler that launches asynchronous work captures explicit context and owns cancellation/cleanup. Never store per-request context on a singleton handler field.

### Define failure propagation

If a handler fails while deciding whether it can handle, continuing may be unsafe: a policy-store outage should not pass to a permissive fallback. Define fail-closed/fail-open per responsibility with threat and availability analysis.

For around chains, ensure post-processing/finally logic runs exactly once on success, rejection, failure, timeout, and cancellation. Preserve the primary failure if cleanup also fails.

### Control async and streaming chains

An async handler can return a future/promise of disposition or transfer ownership through a durable token. Exactly one continuation may resume, and late completion after cancellation must not invoke the remainder twice.

Streaming handlers preserve ordering, terminal signals, demand/backpressure, cancellation, and bounded buffers. A per-item chain and a per-stream chain have different state/lifecycle.

### Manage concurrency and lifecycle

Prefer stateless immutable handlers. Shared counters need synchronization; mutable caches and rate limiters need scoped ownership; handler removal waits for in-flight users or uses versioned snapshots.

Initialization and shutdown order follow dependencies. A chain should not close the same shared handler twice through aliases.

### Observe the chain usefully

Record chain/configuration digest, terminal handler ID, outcome category, visited count, latency, and bounded failure reason. Sample detailed per-handler timings where needed rather than emitting unbounded labels.

Distinguish one logical request from downstream attempts. Audit policy denials without logging secrets or attacker-controlled unbounded values.

### Test and simplify

Unit-test each handler with recording continuations. Test pairwise order-sensitive combinations, full realized chains, duplicate/cycle/missing terminal configuration, concurrency, cancellation, failure, and reconfiguration.

If handlers are pure predicates mapping to static outcomes, a decision table, pattern match, or rule engine may be clearer. If every handler always calls next, it is a middleware/decorator pipeline rather than selection.

## Definitions and Notation

For domain $D\subseteq C\times X$, define eligibility predicate (q_i(c,x)). In first-match semantics, selected handler is

$$
j(c,x)=\min\{i\mid q_i(c,x)\},
$$

when the set is nonempty. Overlap $q_i\land q_k$ makes order observable; a gap $\neg\bigvee_i q_i$ produces `Unhandled` absent a terminal handler.

Let visited prefix $V(c,x)=\{1,\ldots,j\}$, or all handlers if unhandled. Total sequential decision cost is $T=\sum_{i\in V}t_i$ under the stated simple model. Expected cost depends on request distribution and predicate/handler costs; cheapest-first order is valid only when semantics permit reordering.

For configuration generation (g), request traversal uses immutable chain (H_g). Reconfiguration publishes (H_{g+1}) atomically for new requests while (H_g) remains alive until its in-flight count reaches zero.

## Mechanisms, Invariants, or Proof Structure

### Chain design procedure

1. Declare selection, broadcast, transformation, or around semantics.
2. Define explicit dispositions and complete request/context contract.
3. Specify handler predicates, effects, ordering, and terminal coverage.
4. Validate configuration and publish immutable generations.
5. Define failure, deadline, cancellation, async, and lifecycle behavior.
6. Protect security and other mandatory handlers from bypass.
7. Add unit, interaction, property, configuration, concurrency, and fault tests.
8. Instrument terminal outcome and contract chains when data is clearer.

### Executable mechanism

This deterministic first-terminal chain distinguishes rejection, handling, and explicit fallback while recording only visited handlers.

<!-- bijux-verify: {"id":"chain-explicit-dispositions","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"health=handled:ok visited=size,health\nlarge=rejected:too-large visited=size\nmissing=handled:not-found visited=size,health,fallback\n","stderr":""}} -->
```python
class SizeGuard:
    identifier = "size"

    def handle(self, request):
        if request[1] > 1024:
            return ("rejected", "too-large")
        return ("pass", "")


class HealthHandler:
    identifier = "health"

    def handle(self, request):
        if request[0] == "/health":
            return ("handled", "ok")
        return ("pass", "")


class NotFoundHandler:
    identifier = "fallback"

    def handle(self, request):
        return ("handled", "not-found")


def dispatch(handlers, request):
    visited = []
    for handler in handlers:
        visited.append(handler.identifier)
        outcome = handler.handle(request)
        if outcome[0] != "pass":
            return (outcome[0], outcome[1], visited)
    return ("unhandled", "", visited)


chain = [SizeGuard(), HealthHandler(), NotFoundHandler()]
for label, request in [("health", ("/health", 20)), ("large", ("/health", 2048)), ("missing", ("/other", 20))]:
    kind, value, visited = dispatch(chain, request)
    print(label + "=" + kind + ":" + value + " visited=" + ",".join(visited))
```

A production chain would validate descriptors, freeze configuration generations, propagate trusted context/deadline/cancellation, bound costs, and distinguish domain from transport outcomes.

### Proof obligations

For finite domains, show coverage and intended overlap/order. For open domains, prove the fallback is total or expose unhandled. For mandatory policy, prove every relevant path visits equivalent enforcement before a terminal disclosure/effect.

The snippet proves only three sequential paths. It does not prove complete routing, security, concurrency, async continuation, or deployed configuration.

## Alternatives and Trade-Offs

| Approach | Selection/control | Best fit | Main risk |
|---|---|---|---|
| Chain of Responsibility | handlers may pass or stop | extensible receiver selection | gaps/order opacity |
| Middleware/Decorator | around downstream call | cross-cutting request behavior | order and next-call errors |
| Pipeline | every stage transforms/processes | required sequential processing | partial effects/backpressure |
| Event subscribers | zero or many receivers | notification/broadcast | delivery/ordering complexity |
| Strategy | one selected algorithm | interchangeable policy | selector coupling |
| Decision table/pattern match | explicit data/code selection | finite stable predicates | table growth |
| Rule engine | declarative many-rule evaluation | complex evolving policy | conflict/explainability cost |

Use the protocol whose multiplicity and outcomes match the domain; do not force all into one handler interface.

## Failure Modes and Misconceptions

### “A request will eventually be handled”

Classic chains may fall through. Add a total terminal handler or make unhandled explicit and tested.

### “Handlers are order-independent”

Overlapping predicates, mutations, security checks, and short circuits make order observable unless independence is proved.

### “Pass means nothing happened”

Only if the contract enforces side-effect-light pass. Audit, mutation, allocation, and resource acquisition can remain.

### “Exceptions should try the next handler”

Failure to decide may require fail-closed behavior. Continuing is a policy choice, not a generic recovery rule.

### “Middleware is just Chain of Responsibility”

Middleware often invokes next and resumes on unwind; first-match chains usually relinquish control after passing. Test the actual continuation contract.

### “Priority numbers solve order”

They can collide and hide semantic constraints. Prefer named before/after requirements plus ambiguity validation.

### “Dynamic plugins can be added immediately”

Unvalidated live mutation can change in-flight semantics. Build, validate, then atomically publish a versioned snapshot.

## Worked Examples

### Example 1

Three support handlers accept issues by severity and specialty. A low-severity security issue overlaps two predicates; explicit security-before-general order resolves it. **Conclusion:** Predicate overlap makes order part of policy.

### Example 2

A file decoder chain has no handler for a new format and returns `Unhandled(format)`. The caller can install a plugin or reject cleanly. **Conclusion:** Explicit fall-through supports extensibility.

### Example 3

A rate-limit handler decrements quota and then passes; a later handler rejects validation. Moving quota consumption to the terminal accepted path avoids lost quota. **Conclusion:** Passing after mutation requires deliberate semantics.

### Example 4

A static-file handler precedes authorization for all paths and serves a protected export. Restricting it to a proven public namespace and testing route coverage closes the bypass. **Conclusion:** Early terminals can defeat later security.

### Example 5

Two configuration sources register the same retry handler. Startup multiplicity validation rejects the chain. **Conclusion:** Realized configuration must be inspected, not inferred from source.

### Example 6

An asynchronous fraud handler times out, then completes and resumes the chain after the request was cancelled. A single-owner continuation token rejects late completion. **Conclusion:** Async chains need exactly-once resumption.

### Example 7

A singleton handler stores the current user in a field. Concurrent requests leak identities. Moving request state into immutable context fixes it. **Conclusion:** Handler reuse requires state isolation.

### Example 8

A stream filter requests unlimited input before a slow downstream handler. Bounded demand and cancellation propagation restore backpressure. **Conclusion:** Streaming chains must preserve protocol signals.

### Example 9

One hundred pure exact-match handlers scan linearly. A map-based dispatcher preserves the same outcome and reduces cost/ambiguity. **Conclusion:** Stable selection data may deserve a table, not a chain.

### Example 10

An emergency-command chain has authorization, operating-mode, interlock, and device handlers. Software fall-through never bypasses independent device safety, and indeterminate actuation is not retried blindly. **Conclusion:** Behavioral chaining cannot establish physical safety.

## Cross-Program Connections

- **Programming Languages and Semantics:** sum types, effects, exceptions, continuations, and pattern matching define dispositions.
- **Object-Oriented Programming:** polymorphic handlers, delegation, state isolation, and substitutability implement chains.
- **Functional Programming:** folds, partial functions, parser combinators, and explicit result types clarify semantics.
- **Concurrent Programming:** immutable snapshots, reentrancy, async continuation, cancellation, and backpressure govern execution.
- **Software Architecture:** plugin boundaries, configuration provenance, middleware, and deployment inspection shape realized chains.
- **Testing and Quality:** predicate properties, route matrices, interaction traces, race tests, and fault injection provide evidence.
- **Security Engineering:** complete mediation, fail-closed behavior, trusted context, and route coverage constrain order.
- **Distributed Systems:** deadlines, retries, delayed completion, duplication, and indeterminate effects affect handlers.
- **API and Service Engineering:** routing, filters, protocol errors, and middleware are common applications.
- **Systems Engineering:** authority chains, interlocks, physical effects, and safe-state controls limit abstractions.

## References

1. Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, [*Design Patterns: Elements of Reusable Object-Oriented Software*](https://www.pearson.com/en-us/subject-catalog/p/Gamma-Design-Patterns-Elements-of-Reusable-Object-Oriented-Software/P200000009480/9780321700698), Addison-Wesley, 1994. Canonical Chain of Responsibility intent, participants, applicability, and consequences.
2. Eclipse Foundation, [Jakarta Servlet Specification 6.1, Chapter 6](https://jakarta.ee/specifications/servlet/6.1/jakarta-servlet-spec-6.1), final release, 2024. Specifies ordered filters, passing to the next entity, blocking, response unwind, lifecycle, and failure.
3. Microsoft, [ASP.NET Core Middleware](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/middleware/), ASP.NET Core 10 documentation, accessed 2026-08-28. Documents request order, reverse response order, next invocation, and terminal short-circuit behavior.
4. OWASP Foundation, [Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html), accessed 2026-08-28. Provides deny-by-default, per-request authorization, enforcement-placement, and testing guidance.
5. Reactive Streams Contributors, [Reactive Streams JVM Specification](https://github.com/reactive-streams/reactive-streams-jvm), version 1.0.4, accessed 2026-08-28. Specifies asynchronous stream signaling, cancellation, and non-blocking backpressure.
6. OpenTelemetry, [“Libraries” instrumentation guidance](https://opentelemetry.io/docs/concepts/instrumentation/libraries/), accessed 2026-08-28. Covers explicit context propagation, nested instrumentation, error handling, performance, and tests.
7. Michael Nygard, *Release It!*, second edition, Pragmatic Bookshelf, 2018, ISBN 978-1-68050-239-8. Provides timeout, stability, resource, and failure-propagation principles for production request paths.

## Exercises

### Exercise 1

Trace all executable paths and state which completeness and ordering properties are established or absent.

### Exercise 2

Given predicates (q_1=x<0), $q_2=x\bmod2=0$, and (q_3=true), derive selected handlers for (-2,-1,0,3), overlaps, and the result of swapping the first two.

### Exercise 3

Design a validated dynamic handler registry with constraints, immutable generations, in-flight lifetime, and safe rollback.

### Exercise 4

Design an async authorization/routing chain with deadline, cancellation, cache, retry, telemetry, and explicit failure outcomes.

### Exercise 5

Review a chain for unfamiliar high-stakes industrial commands without claiming functional safety or deployment suitability.

## Answers to the Exercises

### Answer 1

`/health,20` passes size, is handled by health, and visits two. `/health,2048` is rejected by size and visits one. `/other,20` passes size and health, then is handled by the total fallback and visits all three. Thus the three demonstrated requests have one terminal disposition, size precedes routing, and fallback covers all tuples reaching it.

The traces do not prove coverage for a different chain/configuration, authenticated route policy, side-effect freedom, duplicates/cycles, concurrency, context propagation, deadlines, async continuation, or production order. Even here, fallback returns not-found as `handled`; a richer transport/domain model might use a distinct `not_found` outcome.

### Answer 2

In order (q_1,q_2,q_3): (-2) matches both (q_1) and (q_2) but selects 1; (-1) selects 1; (0) selects 2; (3) selects 3. The fallback makes coverage total. Overlap sets include all negative even values for $q_1\land q_2$, all values with (q_3), and negative values with $q_1\land q_3$.

After swapping even before negative: (-2) selects even handler 2-now-first, (-1) selects negative, (0) still selects even, and (3) selects fallback. The changed result for negative evens proves order observability. Reordering by cost is invalid unless overlapping handlers have equivalent outcomes or priority policy allows the change.

### Answer 3

Descriptors contain stable ID/version, predicate/capability, before/after, requires, conflicts, multiplicity, terminal status, effect class, lifecycle owner, and compatibility range. Build a candidate graph from one configuration snapshot with provenance. Reject unknown handlers, duplicate IDs beyond policy, missing capabilities, conflicts, cycles, materially ambiguous orders, security-order violations, and missing terminal coverage. Construct handlers only after structural validation, then run health/contract tests.

Publish an immutable generation atomically for new requests. Existing requests retain the old generation and its handlers until reference/in-flight count reaches zero; close each owned handler once. Store redacted descriptor digest and rollback pointer. Canary a new generation, compare terminal outcomes/latency/errors, and roll back new traffic without mutating old requests. Audit who changed configuration and never expose secrets in descriptors.

### Answer 4

Use explicit `Pass|Handled|Rejected|Failed|Cancelled|DeadlineExceeded|Indeterminate` outcomes. Derive trusted identity/tenant and one absolute deadline at entry. Authorization runs before protected cache disclosure and fails closed if its required policy source is unavailable. Cache keys include tenant, resource, representation, policy generation, and data generation; authorization is re-evaluated according to revocation contract.

Routing handlers receive immutable context and cannot resume more than once. One retry owner retries only safe/idempotent downstream work with remaining budget and one payload-bound key; timeout after an effect may be indeterminate and triggers reconciliation. Cancellation propagates to policy/cache/remote work but does not erase committed effects. One logical span surrounds selection; bounded events or sampled child spans record handler ID, visited count, cache outcome, attempt, and terminal category. Tests cover every route/policy pair, revocation, cache miss/hit/stale, late async completion, double callback, failure/cancellation races, deadline, retries, malformed config, telemetry failure, and production-added middleware.

### Answer 5

Define authenticated actor/role, asset/topology/configuration version, operating mode, command, preconditions, authority, timing, and explicit accepted/confirmed/rejected/indeterminate outcomes. Mandatory validation, authorization, interlock, sequencing, and audit handlers cannot be skipped by plugin order or early terminals. Freeze and sign/review configuration generations where required. Do not treat a software handler chain as the only enforcement layer; retain independent controller/hardware limits, interlocks, alarms, and safe-state behavior.

Do not retry indeterminate actuation unless the validated protocol provides authenticated idempotency/sequence and state reconciliation. Evidence requires requirements/hazard and common-cause traceability, formal/state/timing analysis where tractable, order/coverage/multiplicity proofs for the complete configuration, static analysis, independent code/protocol review, simulator and hardware-in-the-loop testing, loss/duplicate/reorder/delay/partition/restart/power/resource fault injection, threat testing, operator/human-factors exercises, and controlled deployment/recovery. Named domain, controls/real-time, functional-safety, hardware, cybersecurity, human-factors, quality, regulatory, operations, and independent verification authorities approve. This chapter establishes no system safety or deployment fitness.
