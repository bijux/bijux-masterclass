# Python Patterns in Software Engineering Deep Dive

**Module 01: Foundations & Typing Discipline**

1. Pattern shape in Python: context → problem → forces → solution → consequences; applicability/contraindications.
2. Composition over inheritance: Pythonic adaptations of GoF (what to keep, what to drop); when not to use OO patterns.
3. Typing rigor: Protocol, TypeVar, ParamSpec, Self, overload, Concatenate; variance pitfalls.
4. Construction invariants: dataclass smart constructors; Pydantic v2 for runtime guarantees (warn: not for domain equality/ordering).
5. Error taxonomy: domain vs operational; Result/Option intro (deep dive in M5); vs exceptions; when to prefer exceptions.
6. Configuration-as-data: partial application, functional wiring, no boolean flags; applicability for pluggable behavior.
7. Factories over singletons: configuration-driven factories; testable injection; contraindications for simple cases.
8. Builder (when justified): immutable build targets; fluent APIs without footguns; skip for trivial objects.
9. Compatibility rules: versioned public API, deprecation lanes, adapters; type evolution policy (Final, Literal, NewType).
10. Non-goals/anti-patterns: Singleton, Service Locator, global registries; inheritance-heavy designs.

**Module 02: Creational Patterns (Pythonated)**

1. Smart constructors & “make_*” functions: invariant before instance; kw_only/frozen/slots=True dataclasses.
2. Factory families: abstract factory + builders for config graphs; functools.partial + config schemas.
3. Prototype safely: copy-on-write; dataclasses.replace; custom __deepcopy__ hooks; when not to clone (immutables).
4. Object pools (narrow): limit to I/O handles; forbid general object pooling; require lifetime tests and leak detectors.
5. Lazy init: properties + descriptors; thread-safe first-use; contraindications for hot paths.
6. __new__ and __init_subclass__: allocation control; subclass policy hooks; applicability for policy enforcement.
7. Minimal metaclasses: policy enforcement without magic; skip unless subclass hooks insufficient.
8. Flyweight: share immutable symbols; memoization with weakrefs; measure object churn reduction.
9. Process-wide cache with explicit init/reset (rare): when global state unavoidable; hazards (test isolation).
10. Demotions: why DI frameworks and metaclass singletons hurt tests; prefer constructor injection.

**Module 03: Structural Patterns & Access**

1. Adapter via Protocol: narrow capabilities; capability-based design; when not to adapt (direct protocol conformance).
2. Bridge: separate abstraction from implementation; swap backends cheaply; contraindications for tight couplings.
3. Composite: uniform tree/graph APIs; safe traversal; measure depth limits to avoid stack overflows.
4. Decorator (functions & objects): stacking rules, wraps, typed signatures (ParamSpec, Concatenate); error wrapping.
5. Facade: stable boundary for messy subsystems; error normalization; applicability for legacy wrappers.
6. Proxy: virtual, remote, protective; access control via descriptors; pitfalls (reentrancy, shadowing).
7. Value objects: immutability, ordering, hashing, serialization; plain frozen dataclasses over Pydantic in domain.
8. Descriptors: validated get/set; conversion; binding; invariant enforcement; bypass prevention, recursion traps.
9. __slots__: memory/layout for hot paths; weakrefs and 3.13 safety; __setattr__ ordering hazards.
10. Package boundaries: __all__, import policy, public vs internal; import lints in CI.

**Module 04: Behavioral Patterns I (Core)**

1. Strategy: algorithm families; partials for configuration; when not to use (simple if/else sufficient).
2. Template method (composition-first): hooks without inheritance entanglement; prefer composition; sealed inheritance only.
3. Chain of responsibility: short-circuiting handlers; typed results; contraindications for long chains (observability loss).
4. Command: immutable commands; undo/redo; auditability; command audit trail schema.
5. Observer/Event bus: weakrefs, backpressure awareness; applicability for decoupled notifications.
6. State/typestate: pattern matching (3.10+), explicit transitions; when not to FSM (simple flags).
7. Iterators/generators: lazy pipelines with itertools; measure memory for large streams.
8. Policy objects: kill boolean flag explosions; applicability for configurable rules.
9. Memento: safe snapshotting & serialization boundaries; capped history or ring buffer; snapshot size/latency risks.
10. Mediator: decouple chatty subsystems; keep flows observable; contraindications for small systems.

**Module 05: Behavioral Patterns II (Advanced)**

1. Visitor vs pattern matching: when visitor still wins; decision table + micro-bench of both.
2. Specification: composable predicates; error accumulation; short-circuit rules; applicability for validation.
3. Result/Option pipelines: exception-free flows; adapters at edges; deep dive (intro in M1).
4. Null object: explicit sentinels; do not hide errors; limit to non-errorable paths.
5. Interpreter/mini-DSLs: tiny ASTs; safe eval; sandbox; when not to DSL (overkill for configs).
6. Balking/guarded actions: reject when invariants fail; contraindications for lenient paths.
7. Command bus vs event bus: sync vs async contracts; observability requirements.
8. Reactor as asyncio/AnyIO: event loop patterns, not raw selectors; applicability for I/O heavy.
9. Scheduling: executors, priority queues, fairness, backpressure; measure queue sizing.
10. Anti-patterns: marker interfaces; inheritance-heavy hierarchies; temporal coupling.

**Module 06: Architecture & Boundaries**

1. Ports & Adapters (Hexagonal): pure domain, effectful edges; applicability for evolvable systems.
2. Modular monolith: bounded contexts, enforced internal APIs; contraindications for microservices hype.
3. Plugin system: entry points/registries, versioned namespacing; sandbox, resource quotas, loader timeouts, import allowlists.
4. CQRS: commands vs queries; read models & projections; when not to split (simple CRUD).
5. Layered architecture done right: minimal crossing rules; API error schema (problem+json) + versioning contract.
6. Pipes & filters: streaming data flows; composition of stages; measure throughput.
7. Strangler fig: compatibility-first migrations; feature flags & strangler routing artifacts.
8. DDD-lite: entities, value objects, aggregates, domain services; applicability for complex domains.
9. Microkernel: core + pluggable capabilities; compat adapters.
10. Web boundaries: FastAPI adapters; error schemas (problem+json); contraindications for non-HTTP.

**Module 07: Data, Serialization & Persistence**

1. Repository with Protocol: persistence independence; applicability for swappable storage.
2. Unit of Work: transactional batches; retry semantics; contraindications for non-transactional data.
3. Data Mapper vs Active Record: clear stance (prefer Mapper); mapping layer patterns; migration path.
4. Identity map: dedup instances per UoW; forbid global caches; scope creep risks.
5. Lazy load: proxies with explicit boundaries; N+1 detection and batching patterns.
6. Optimistic locking: versions; conflict handling policy; when not to use (high contention).
7. Schema evolution: versioned codecs (JSON/MsgPack/Parquet); migrations; compat tests; versioned codec trait.
8. Idempotency keys: safe retries; at-least/at-most once; big-object policy (blobs out of DB).
9. Outbox/inbox: reliable events across services; applicability for distributed consistency.
10. Caching: cache-aside, invalidation, TTLs; lru_cache with care; measure hit rates.

**Module 08: Concurrency & Async Discipline**

1. Structured concurrency: task groups (AnyIO/Trio/asyncio); applicability for clean lifetimes.
2. Pools: threads vs processes (concurrent.futures); CPU vs I/O split; contraindications for low parallelism.
3. Synchronization: Lock, Condition, invariants you actually maintain; per-object locks.
4. Producer–consumer: bounded queues; backpressure; queue sizing measurements.
5. Futures/promises: cancellation, shielding, timeouts; unhandled cancellation risks.
6. Async generators/streams: timeouts, cancellation, cleanup; deterministic testing (fake clocks).
7. Mixing sync/async: to_thread, adapters, blocking audits; mandate timeouts everywhere.
8. Free-threaded Python (3.13+): migration risks; thread-safe descriptors/slots/weakrefs; audit checklist (C-ext, refcounts).
9. Readers–writers: demoted; alternatives (simple locks); use only in rare high-read contention.
10. Active object (Python version): async queue + worker tasks; applicability for decoupling.

**Module 09: Reliability, Security & Observability**

1. Retries with jitter; budgeted attempts; classify retriable vs fatal; error budgets for attempts.
2. Circuit breaker: half-open probes; metrics integration; percentiles/error budgets for transitions.
3. Bulkheads: per-capability limits; overload protection; applicability for isolation.
4. Throttling & load shedding: token buckets; priority drop; measure rates.
5. Structured logging: correlation IDs; domain events as data; log/event schemas; propagation discipline.
6. Metrics: RED/USE; domain KPIs; Prometheus-friendly; sampling strategy.
7. Tracing: spans across async hops; sampling strategy; contraindications for low-traffic.
8. Security policies: secrets (env/KMS), least privilege, audit hooks; supply chain (hash-pinned, SBOM, pip-tools/PEP 665, secret scanning, dependency review).
9. Fault injection: boundary chaos; timeouts, partial reads, DNS failures; constrained (no prod blast radius).
10. Governance: AST/lint guards, import policies, CI gates; stability levels, deprecation SLOs, compat matrices.

**Module 10: Testing, Performance & Refactoring**

1. Test doubles: fakes > mocks; unittest.mock with discipline; contract tests over mocks by default.
2. Property-based tests (Hypothesis): invariants & generators; state machines; ≥ N examples.
3. Contract tests: ports/adapters; API compat tests; mypy --strict baseline zero ignores.
4. Profiling: cProfile, py-spy, tracemalloc; trace hot paths; perf regression gates in CI (threshold + variance).
5. Object layout: __slots__, fewer objects, vectorization where it matters; memory ceilings via tracemalloc.
6. Refactors: Extract Method, Introduce Policy Object, Dependency Inversion; compatibility refactors.
7. Anti-patterns: God Object, Singleton, Service Locator, Flag Explosion, Temporal Coupling; Anemic Domain Model.
8. Compatibility refactors: strangler routes, adapters, deprecation layers, feature flags; end dates.
9. Mutation testing: targeted on core logic; cost control; otherwise CI unusable.
10. Review governance: checklists, ADRs, perf gates, flake8/mypy rulesets; governance artifacts (stability notes).
