---
module_id: SEPAT-024
program: Software Engineering: Patterns
level: 1
module_number: 24
title: Decorator
status: complete
last_verified: 2026-08-28
---

# Decorator

## One-Page Review

### Governing question

How can responsibilities be attached to one object dynamically while preserving a usable contract, and how must order, multiplicity, identity, failure, context, concurrency, and lifecycle be controlled when wrappers compose?

### Essential definitions

- **Decorator** wraps a component, implements the same component contract, and adds behavior before, after, or around delegation.
- The **component** is the common client-facing contract; the **concrete component** provides base behavior.
- A **concrete decorator** owns one responsibility and delegates through a component reference.
- A **decoration chain** is an ordered composition of wrappers around a base component.
- **around behavior** can validate, transform input/output, observe, cache, retry, authorize, meter, or manage a resource scope.
- **order sensitivity** means two decorators produce different observable behavior when swapped.
- **multiplicity policy** states whether a decorator is allowed zero, one, or several times in one effective chain.
- **behavioral transparency** means clients relying on the base contract remain valid; not every decorator is transparent for every observation.
- **context propagation** carries deadline, cancellation, trace, identity, transaction, and other operation-scoped data across wrappers.
- A **language-level decorator/annotation** is syntax or metadata and is not necessarily the GoF object Decorator pattern.

### Central model, mechanism, or theorem

Treat a component behavior as \(B:X\to Outcome(Y,E)\). A decorator is a higher-order transformation \(d:B\to B'\), and a chain is ordered composition

\[
B'=d_n\circ\cdots\circ d_2\circ d_1(B).
\]

In general \(d_i\circ d_j\ne d_j\circ d_i\): authorization before caching differs from caching before authorization; retry outside metrics counts logical calls while metrics inside retry counts attempts. Correct composition requires declared pre/post behavior, allowed order constraints, multiplicity, shared deadline/cancellation, and one owner for effects such as retry, transaction, close, or telemetry.

### Critical invariants

- Every decorator delegates exactly according to its advertised success, failure, short-circuit, and multiplicity policy.
- The effective chain order is explicit, validated, observable, and tested.
- Required context—identity, authorization, deadline, cancellation, trace, transaction, idempotency—survives every wrapper.
- Input/output transformations preserve the component's domain invariants and type/error contract.
- Retry, caching, transactions, and side effects have one authoritative layer and do not amplify each other.
- Resource acquisition is paired with release on success, error, timeout, and cancellation; close ownership is unambiguous.
- Metadata, equality, identity, introspection, and unwrapping behavior are defined where clients depend on them.
- Optional decoration adds bounded overhead and bounded-cardinality telemetry supported by measurement.

### Common failures

Common failures include believing wrapper order is cosmetic, applying authentication after cache lookup, double retrying, counting logical calls and attempts in one metric, swallowing or replacing domain errors, losing cancellation or trace context, opening spans/locks without `finally`-equivalent cleanup, closing a shared inner component multiple times, caching tenant-specific results without tenant keys, adding the same decorator twice through two configuration systems, breaking reflection/signature metadata, unbounded chain depth, and calling every middleware/interceptor a correct Decorator without contract analysis.

### Compact example

A base quote is 10,000 minor units. A ten-percent discount and fixed 500-unit fee implement the same quote interface. Discount-then-fee yields 9,500; fee-then-discount yields 9,450, proving order matters. An audit wrapper records one logical call. The arithmetic is illustrative, not a pricing policy.

### Connections

[SEPAT-023](023-composite.md) nests components as part–whole children; Decorator forms a usually linear wrapper chain. [SEPAT-025](../ROADMAP.md) provides a simplified subsystem entry, and [SEPAT-027](../ROADMAP.md) controls access while preserving an interface. Decorator connects to [Concurrent Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md), [Security Engineering](../../25-security-engineering/ROADMAP.md), and [Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md).

## Governing Question

What single responsibility should surround the component, which observations may it change, and where must it appear relative to every other wrapper for the system contract to remain true?

Decorator trades subclass combinations for runtime composition. It is valuable when responsibilities are independently optional and share a stable contract. It becomes opaque middleware when chain assembly, order, and ownership are implicit.

## Why This Matters

Logging, tracing, metrics, authorization, caching, retries, transactions, validation, compression, encryption, and buffering are frequently layered. Their order changes security, cost, failure, and what is observed. A cache outside authorization can leak data; compression and encryption are not interchangeable; retry placement changes side-effect count.

Production design therefore treats the chain as an executable protocol. It validates constraints, exposes a safe description, tests interactions, and avoids duplicating responsibilities already supplied by frameworks or lower layers.

## Prerequisites and Retrieval

You should understand interfaces, delegation, higher-order functions, exceptions/results, async context, deadlines, idempotency, caching, retries, and resource ownership. Retrieve these facts:

1. Function composition is ordered unless commutativity is proved for the relevant observations.
2. Short-circuiting means inner decorators and the base may not execute.
3. A retry decorator can invoke its inner component multiple times for one outer call.
4. Cancellation and deadlines are data/authority, not implicit magic across threads or tasks.
5. A wrapper is a distinct object even when it presents the same service identity.
6. Cross-cutting instrumentation can duplicate telemetry already produced below.

## Learning Objectives

After completing this module, you should be able to:

- derive one-responsibility decorators from a stable contract;
- model chain order and prove or test order constraints;
- specify logical-call versus attempt semantics;
- preserve context, errors, identity, and resource lifecycle;
- prevent duplicate decoration and unbounded composition;
- distinguish Decorator from Proxy, Adapter, Chain of Responsibility, and language syntax;
- test wrappers alone and in representative interaction chains;
- contract chains when native/platform mechanisms replace them.

## Core Exposition

### Keep one stable component contract

The decorator and base must be usable through the same client-facing interface. Include complete async, streaming, cancellation, and close semantics—not only the happy-path method.

If a wrapper changes return type or requires clients to downcast for normal use, it is likely an Adapter or a different service abstraction.

### Give each decorator one responsibility

Authorization decides permission; retry decides repeated attempts; metrics observes; cache stores; transaction manages commit scope. Combining all in one “interceptor” makes order and testing harder.

One responsibility may still require before/after/error/finally behavior. Keep its policy coherent and named by durable intent.

### Order is architecture

Write chain order from outermost to innermost and translate it into a call trace. For `Metrics(Retry(Client))`, metrics sees one logical call and retry sees attempts. For `Retry(Metrics(Client))`, metrics sees each attempt.

Authorization generally precedes access to tenant/user-specific caches; validation may precede idempotency lookup only if invalid requests must never hit stored results; transaction placement relative to retry determines whether attempts share a transaction.

### Declare constraints

Express `before`, `after`, `requires`, `conflicts`, and maximum multiplicity in chain assembly. Topologically sort only if a unique or explicitly accepted order results; reject cycles and ambiguity that matters.

Do not let framework auto-registration and manual wrapping both add the same concern. Give each decorator a stable ID and inspect the realized chain at startup.

### Short-circuit semantics

Authorization denial, cache hit, circuit open, rate-limit rejection, or validation failure may return without delegation. Outer decorators still observe the outcome; inner ones do not.

Define whether audit must surround all short circuits. Security audit is often outer to authorization so denials are recorded, while sensitive payload capture remains after authorization/redaction.

### Input and output transformation

Compression, encryption, normalization, and pricing transformations change values. Specify domains, exact order, reversibility, loss, and error behavior. Preserve invariants and do not mutate caller-owned data unexpectedly.

For streams, `read`, `skip`, `mark/reset`, close, partial buffers, and end-of-stream must remain coherent. A filter that overrides only one convenience method can violate the full contract.

### Errors

Decorators may add context but must preserve actionable error class and cause unless mapping is their explicit role. Cleanup errors should not silently replace the primary error; report both according to platform conventions.

Retries classify errors and indeterminate outcomes. Metrics and tracing record errors without changing application behavior; instrumentation failure should follow a declared isolation policy.

### Deadline and cancellation

Pass one operation deadline inward. Each wrapper computes remaining budget rather than resetting a full timeout. A retry reserves time for attempts/backoff; a cache loader shares or separates cancellation by policy.

Capture explicit context before crossing task/thread boundaries. Always restore prior thread-local/ambient context after delegation.

### Identity and introspection

Wrapper object identity differs from service/resource identity. Equality based on wrapper addresses can break registries; unwrapping can bypass policy. Expose stable service identity separately and restrict raw-inner access.

Language callable decorators should preserve name, documentation, annotations, and wrapped-function metadata when tools rely on them. Metadata preservation does not prove behavioral transparency.

### Lifecycle

Decide whether closing the outermost wrapper cascades inward and exactly once, or whether a composition root owns the shared base separately. Shared inners make cascading close unsafe unless reference ownership is explicit.

Decorators acquiring locks, spans, transactions, buffers, or permits release them in a guaranteed cleanup path. Cancellation and callback reentrancy need tests.

### Concurrency

A stateless decorator can be thread-safe only if its inner is safe and context is not stored in shared mutable fields. Counters need atomic/synchronized updates; caches need stampede and key policy; rate limiters need scoped ownership.

Do not reuse one decorator instance for request-specific state. Keep per-call state on the stack/context.

### Performance and telemetry

Measure chain overhead, allocation, context capture, serialization, lock contention, cache behavior, and emitted telemetry. A dozen tiny wrappers can create substantial tail cost.

Avoid double instrumentation. OpenTelemetry guidance distinguishes logical library operations from underlying network attempts and recommends checking interactions with auto-instrumentation.

### Testing

Unit-test each decorator with a recording/failing inner: delegation count, input/output, short circuit, error preservation, and cleanup. Use permutation tests for order-sensitive pairs and property tests for decorators claimed idempotent or commutative.

Run integration tests on realized production chains, including framework-added layers. Fault-inject timeout, cancellation, exception, telemetry failure, duplicate config, and shutdown.

### Contraction

Remove wrappers whose responsibility moves into a platform, whose evidence no longer justifies cost, or whose policy becomes mandatory core behavior. Collapse adjacent transformations only when order, observability, and ownership remain explicit.

Keep a chain inventory and reject unknown decorator IDs so obsolete or malicious layers cannot persist invisibly.

## Definitions and Notation

Let base behavior \(B:X\to Outcome(Y,E)\). Decorator \(d_i\) transforms behavior while retaining the component interface. Effective chain

\[
B_D=(d_n\circ\cdots\circ d_1)(B).
\]

Let \(calls_i(x)\) be number of inner invocations. A pure observation decorator normally requires \(calls_i(x)=1\); cache/authorization may allow zero; retry may allow \(0\le calls_i(x)\le k\). Let order relation \(d_i\prec d_j\) mean \(d_i\) must be outer/before \(d_j\) under the documented convention. Let multiplicity \(m_i\) be bounded by policy.

## Mechanisms, Invariants, or Proof Structure

### Contract refinement

For a transparent decorator, every input accepted by the base contract yields an outcome allowed by that contract, with any added observation invisible to functional clients. Transforming decorators require an enriched advertised contract and cannot claim transparency for values they intentionally change.

### Order analysis

For each pair, compare traces of \(d_i(d_j(B))(x)\) and \(d_j(d_i(B))(x)\) across success, failure, short circuit, cancellation, and side effects. Declare commutativity only if all relevant observations agree.

### Chain validation

At composition, enforce unique IDs/multiplicity, required/conflicting layers, ordering DAG, contract versions, and lifecycle ownership. Emit a redacted outer-to-inner description and digest for deployment evidence.

### Executable order example

<!-- bijux-verify: {"id":"decorator-order-and-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"base=10000\ndiscount-then-fee=9500\nfee-then-discount=9450\naudit-events=1\n","stderr":""}} -->
```python
class BaseQuote:
    def quote(self, subtotal):
        return subtotal


class TenPercentDiscount:
    def __init__(self, inner):
        self.inner = inner

    def quote(self, subtotal):
        return self.inner.quote(subtotal) * 90 // 100


class FixedFee:
    def __init__(self, inner, fee):
        self.inner = inner
        self.fee = fee

    def quote(self, subtotal):
        return self.inner.quote(subtotal) + self.fee


class AuditQuote:
    def __init__(self, inner, events):
        self.inner = inner
        self.events = events

    def quote(self, subtotal):
        result = self.inner.quote(subtotal)
        self.events.append(f"quoted:{subtotal}->{result}")
        return result


base = BaseQuote()
discount_then_fee = FixedFee(TenPercentDiscount(base), 500)
fee_then_discount = TenPercentDiscount(FixedFee(base, 500))
events = []
audited = AuditQuote(discount_then_fee, events)

print(f"base={base.quote(10000)}")
print(f"discount-then-fee={audited.quote(10000)}")
print(f"fee-then-discount={fee_then_discount.quote(10000)}")
print(f"audit-events={len(events)}")
```

The run proves integer arithmetic, noncommuting fee/discount order, and one audit event for one finite sequential call. It does not establish a lawful commercial pricing policy, tax behavior, concurrency, failure cleanup, metadata preservation, or authorization.

## Alternatives and Trade-Offs

**Subclassing** attaches behavior statically but creates combinations and cannot vary per instance easily.

**Higher-order function/middleware** is a functional realization of around behavior; it still needs the same order and context analysis.

**Proxy** usually controls access/location/lifecycle while preserving an interface; Decorator emphasizes optional added responsibility. One wrapper may need one clearly named role.

**Chain of Responsibility** gives multiple handlers an opportunity to handle/pass a request; Decorator normally surrounds one inner component and combines behavior.

**Adapter** changes the interface; Decorator retains it. Transformation within the same contract is not interface adaptation.

**Aspect/interceptor framework** centralizes cross-cutting weaving but can hide join points, order, and duplicate instrumentation.

**Explicit pipeline** may be clearer when each stage has different input/output types rather than one common component interface.

## Failure Modes and Misconceptions

- **“Order does not matter because interfaces match.”** Interfaces omit effect traces and transformation algebra.
- **“Logging is always transparent.”** It can fail, leak secrets, block, duplicate, and alter timing.
- **“Retry is just another wrapper.”** It changes invocation count and needs idempotency/deadline policy.
- **“Close can always cascade.”** Shared inner resources may be closed prematurely or twice.
- **“A cache hit behaves like delegation.”** Inner authorization, metrics, and freshness checks may be skipped.
- **“Context propagates automatically.”** Async/thread boundaries frequently break ambient state.
- **“Same interface means same identity.”** Wrapper and service/resource identities differ.
- **“Two registrations are harmless.”** Duplicate auth, retry, encryption, or telemetry can be damaging.
- **“Decorators commute if outputs match once.”** Failure and side-effect traces may still differ.
- **“Language @decorator means GoF Decorator.”** Syntax does not establish object-contract composition.

## Worked Examples

### Example 1

Buffered, digesting, and decrypting input filters share a stream contract. Close and partial-read semantics are tested across each order. **Conclusion:** The full interface, not only `read`, must compose.

### Example 2

Authorization wraps a tenant cache so unauthorized callers never observe cached existence or data. Tenant and policy generation are part of the key. **Conclusion:** Security order constrains caching.

### Example 3

Metrics outside retry records one logical latency and outcome; attempt metrics inside retry record each attempt. Names distinguish them. **Conclusion:** Placement defines the measured population.

### Example 4

Compression before encryption reduces size; encryption before compression produces little benefit and can change security analysis. **Conclusion:** Transformations need domain-specific order evidence.

### Example 5

A transaction decorator outside retry would retry within one potentially aborted transaction. Policy instead creates a fresh transaction per safe attempt under one idempotency key. **Conclusion:** Lifecycle scope and retry interact.

### Example 6

A tracing decorator captures context, creates a span, records errors, and ends it in cleanup while leaving application exceptions unchanged. Auto-instrumented network spans remain separate. **Conclusion:** Observability should not duplicate or alter behavior.

### Example 7

Two configuration systems add the same rate limiter. Stable decorator IDs and maximum multiplicity one cause startup rejection. **Conclusion:** Realized-chain validation prevents invisible duplication.

### Example 8

A callable decorator preserves signature metadata for a framework router but still changes timeout behavior. Behavioral tests remain necessary. **Conclusion:** Introspection transparency is only one dimension.

### Example 9

A chain of fifteen wrappers dominates tail latency. Native platform authentication and telemetry replace six; adjacent validation becomes core policy. **Conclusion:** Decorator chains need performance budgets and contraction.

### Example 10

A medical command service proposes decorators for dose limits, authorization, logging, retries, and device transport. Automatic retry of an indeterminate command is rejected, and independent device safety enforcement remains mandatory. **Conclusion:** Wrapper composition cannot manufacture clinical safety.

## Cross-Program Connections

- **Object-Oriented Programming:** delegation, substitutability, identity, and interface completeness govern wrappers.
- **Functional Programming:** higher-order functions, effects, composition, and algebra illuminate order.
- **Concurrent Programming:** context propagation, atomic counters, caches, locks, and cancellation affect safety.
- **Security Engineering:** authentication, authorization, redaction, encryption, and audit have strict order/authority.
- **Distributed Systems:** retries, deadlines, idempotency, indeterminate outcomes, and circuit state interact.
- **API Engineering:** middleware chains, error mapping, request context, and streaming contracts are decorator-like.
- **Observability Engineering:** logical versus physical spans, duplicate telemetry, cardinality, and failure isolation matter.
- **Testing and Quality:** recording inners, permutations, properties, fault injection, and production-chain tests differ.
- **Performance Engineering:** chain depth, allocation, batching, cache, sampling, and tail cost need measurement.
- **Systems Engineering:** safety constraints and physical side effects limit transparent composition.

## References

1. Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, [*Design Patterns: Elements of Reusable Object-Oriented Software*](https://www.pearson.com/en-us/subject-catalog/p/Gamma-Design-Patterns-Elements-of-Reusable-Object-Oriented-Software/P200000009480/9780321700698), Addison-Wesley, 1994. Canonical Decorator intent, participants, structure, and consequences.
2. Oracle, [`java.io.FilterInputStream`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/io/FilterInputStream.html), Java SE 25 API, accessed 2026-08-28. Documents a stream wrapper that delegates all operations while subclasses transform or add functionality.
3. Python Software Foundation, [`functools.wraps` and `update_wrapper`](https://docs.python.org/3/library/functools.html#functools.wraps), Python 3.14 documentation, accessed 2026-08-28. Documents preservation of callable metadata and wrapped-function access.
4. OpenTelemetry, [“Libraries” instrumentation guidance](https://opentelemetry.io/docs/concepts/instrumentation/libraries/), accessed 2026-08-28. Covers logical versus underlying operations, context propagation, duplicate instrumentation, errors, performance, and testing.
5. Michael Nygard, *Release It!*, second edition, Pragmatic Bookshelf, 2018, ISBN 978-1-68050-239-8. Provides timeout, retry, circuit, bulkhead, and stability interactions.
6. Mark Seemann and Steven van Deursen, *Dependency Injection Principles, Practices, and Patterns*, Manning, 2019, ISBN 978-1-61729-473-0. Provides composition-root and decorator registration/order context.
7. Robert C. Martin, *Agile Software Development: Principles, Patterns, and Practices*, Prentice Hall, 2002, ISBN 978-0-13-597444-5. Provides substitutability and dependency principles for wrapper contracts.

## Exercises

### Exercise 1

Formalize the executable chains and recompute both results. List observations under which fee and discount fail to commute, and design exact rounding/overflow rules.

### Exercise 2

Design and validate a chain containing audit, authorization, tenant cache, metrics, retry, transaction, and transport. State outer-to-inner order, short circuits, invocation counts, deadlines, and error ownership.

### Exercise 3

Specify a chain-assembly validator with IDs, multiplicity, before/after constraints, conflicts, capability requirements, lifecycle ownership, cycle detection, and a safe deployment digest.

### Exercise 4

Design tests for an async tracing decorator around a streaming component under normal completion, early cancellation, exception, callback reentrancy, context switch, telemetry failure, and duplicate instrumentation.

### Exercise 5

An unfamiliar infusion-device command path proposes authorization, dose validation, audit, retry, and transport decorators. Produce a graduate-level order and safety review without claiming clinical suitability.

## Answers to the Exercises

### Answer 1

Let base \(B(x)=x\), discount \(D(B)(x)=\lfloor0.9B(x)\rfloor\) under the toy integer rule, and fee \(F(B)(x)=B(x)+500\). `F(D(B))(10000)=9000+500=9500`; `D(F(B))(10000)=10500*90//100=9450`. They differ by 50, so do not commute for this input.

They can differ in value, rounding, taxable/discountable base, reporting, audit trace, error order, and which transformation observes limits. Define money currency and minor-unit range, checked intermediate multiplication, whether fee is discountable, exact percentage rational, rounding mode and stage, negative/refund handling, maximum/minimum price, and overflow rejection. The example is not tax or pricing evidence. Property-test boundaries and compare the declared business formula independently.

### Answer 2

One defensible outer-to-inner chain is audit → authentication/authorization → tenant-aware cache → logical metrics → retry coordinator → per-attempt transaction → attempt metrics/trace → transport, but exact placement depends on contracts. Audit surrounds denials/cache hits with redaction. Authorization occurs before cache disclosure. Cache key includes tenant, subject-relevant policy generation, request, and data generation; hits short-circuit everything inside. Logical metrics count one outer miss operation. Retry owns one overall deadline and idempotency key; each safe attempt gets remaining budget and a fresh transaction. Attempt telemetry records physical attempts. Transport never adds an independent retry.

Authorization denial and cache hit call inner zero times. Cache miss without retry calls transport once. Retry calls at most \(k\) times only for classified safe outcomes. An indeterminate side effect is reconciled, not blindly retried. Authentication owns identity error, authorization owns denial, cache owns stale/load errors, retry owns exhaustion, transaction owns commit/rollback/indeterminate state, and transport owns protocol failure; outer mapping preserves causes. Audit/metrics/trace cleanup cannot replace the primary error.

### Answer 3

Represent each decorator descriptor with stable ID/version, contract version, multiplicity range, `before`, `after`, `requires`, `conflicts`, provided/required capabilities, lifecycle mode, and owner. Merge configuration sources with provenance, reject unknown IDs and duplicates beyond maximum, validate versions and capabilities, and reject conflict pairs.

Build a directed ordering graph from constraints, detect cycles, and reject materially ambiguous orders unless a canonical order is explicitly part of policy. Validate exactly one close/retry/transaction authority where required and shared-inner ownership. Construct only after validation; inspect framework-added layers too. Emit outer-to-inner IDs/versions and a cryptographic digest over canonical redacted descriptors, never secrets. Tests cover every constraint edge, cycles, missing requirements, duplicates, ambiguous order, deterministic digest, and configuration-source overlap.

### Answer 4

Use a recording async stream and test span/context state before call, during every callback/item, and after termination. Normal completion creates one logical span, propagates explicit context, records outcome, and ends once. Early cancellation propagates cancellation per contract, stops/abandons inner work as documented, closes the span once, and restores prior context. Exception records but rethrows the same application failure; telemetry failure follows isolation policy and never masks it.

Reentrant callbacks see the correct explicit stream context without corrupting the caller's ambient context. Task/thread switches receive captured context, not whatever ambient value exists later. A fake telemetry exporter throws/blocks to test isolation and budget. Enable auto-instrumentation simultaneously and assert one logical wrapper span plus expected underlying spans, no duplicate logical span. Test multiple subscriptions, partial consumption, backpressure, concurrent streams, nested decorators, sampling/no-op behavior, and sensitive-attribute redaction. Retain trace evidence with bounded identifiers.

### Answer 5

Do not treat all responsibilities as freely swappable wrappers. Authenticate and authorize clinician/system/device context before exposing command state. Validate patient, order, drug, concentration, units, route, pump identity, calibration/configuration generation, dose/rate/volume limits, timing, and independent clinical rules before transport. Audit surrounds decision outcomes but captures only approved redacted data and must not block or alter the command result without an explicit safe policy.

Automatic retry is prohibited for an indeterminate actuation unless the device protocol provides an authenticated idempotency/sequence command and queryable reconciliation semantics reviewed for that device. One deadline covers the operation; no layer resets it. Transport and device return explicit accepted, rejected, completed, and indeterminate states. Independent hardware/firmware limits, interlocks, alarms, and safe-state behavior remain outside and below application decorators. Duplicate validation/audit/retry layers are startup defects.

Evidence includes clinical requirements/hazard traceability, dimensional and dose recomputation by an independent method, formal/state/protocol analysis where tractable, worst-case timing, authorization/threat modeling, static analysis and independent review, simulator and hardware-in-the-loop testing, replay/duplicate/loss/delay/partition/restart/indeterminate fault injection, audit integrity, alarm/human-factors validation, and controlled regulatory-quality release. Named clinicians, pharmacists, biomedical/device engineers, controls/real-time, functional-safety, cybersecurity, human-factors, quality, regulatory, operations, and independent verification authorities must approve. This chapter and arithmetic establish no clinical correctness or deployment suitability.
