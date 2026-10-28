# Patterns in Software Engineering in Python — Deep Dive

## Module 1 — Foundations & Principles

1. SOLID for Python (pragmatic adaptations, duck typing)
2. Cohesion, coupling, and stability metrics in code reviews
3. Value vs object semantics; identity boundaries
4. Interfaces via `Protocol` vs ABCs; when each wins
5. Dependency direction: stable abstractions, volatile details
6. Mutability policy: immutable cores, effectful edges
7. Error semantics: typed domain errors vs operational failures
8. Configuration as data; code vs config boundaries
9. Idempotence and replayability as first-class constraints
10. Evolution rules: semver, deprecation paths, compat shims

## Module 2 — Creational Patterns (Pythonated)

1. Factory Method vs `@classmethod` constructors
2. Abstract Factory for families of components
3. Builder for complex immutable objects
4. Prototype with copy-on-write (dataclasses, `replace`)
5. Object Pool & Flyweight under memory pressure
6. Registry-driven instantiation (name/versioned keys)
7. Smart constructors enforcing invariants (pydantic v2)
8. Resource acquisition patterns (context-bound factories)
9. Policy objects vs boolean flags (strategy injection)
10. Wiring: DI-lite with constructors, not magic containers

## Module 3 — Structural Patterns

1. Adapter (sync/async adapters; capability narrowing)
2. Facade for subsystems (clean edges, stable APIs)
3. Proxy (lazy, remote, memoized, and protective)
4. Decorator (behavior layering; stacking rules)
5. Composite for trees/graphs; uniform traversal APIs
6. Bridge to decouple abstractions from implementations
7. Flyweight revisited for high-cardinality symbols
8. Data Mapper vs Active Record (Python ORMs reality)
9. Repository as anti-leak for persistence concerns
10. Anti-corruption layer between bounded contexts

## Module 4 — Behavioral Patterns

1. Strategy (pure functions vs objects; hot-swapping)
2. Template Method vs hooks (prefer composition)
3. Observer vs Event Bus (sync/async, backpressure)
4. Command objects (undo/redo, audit, retries)
5. State/Typestate machines (pattern matching, enums)
6. Chain of Responsibility (short-circuitable pipelines)
7. Interpreter/mini-DSLs (safe evaluation, spec-as-data)
8. Mediator for chatty subsystems (reduce coupling)
9. Iterator/Generator patterns (lazy flows, `itertools`)
10. Visitor for acyclic structures (double-dispatch alternatives)

## Module 5 — Concurrency & Async Patterns

1. Future/Promise with `concurrent.futures` discipline
2. Task groups / structured concurrency (AnyIO/asyncio)
3. Bounded queues & backpressure (producer–consumer)
4. Bulkhead & concurrency limits per capability
5. Cancellation, timeouts, and shielded sections
6. Async resource pools (HTTP, DB) with context managers
7. Fan-out/fan-in; scatter–gather; map–reduce in Python
8. CPU vs I/O segregation (process vs thread pools)
9. Saga/compensations for multi-step workflows
10. Free-threaded (3.13+) migration playbook & hazards

## Module 6 — Architectural Patterns

1. Layered → Hexagonal → Clean Architecture: trade-offs
2. Ports & Adapters in real services (FastAPI edges)
3. DDD building blocks: entities, value objects, services
4. CQRS basics; read models and projections
5. Event sourcing: append-only state + snapshots
6. Modular monoliths (enforced boundaries, package layout)
7. Microservice cut heuristics (don’t over-slice)
8. Plugin architecture (entry points, registries, sandboxes)
9. Configuration-driven assembly (graphs from specs)
10. Evolution without breakage: feature flags, strangler fig

## Module 7 — Data & Persistence Patterns

1. Schema evolution & compatibility contracts
2. Serialization codecs (JSON, MsgPack, Parquet) + versioning
3. Outbox/inbox for reliable events
4. Idempotent writes; exactly-once illusions vs reality
5. Caching layers (request, object, query, materialized)
6. Unit of Work (transactional consistency, retries)
7. Pagination & streaming reads (lazy iteration)
8. Snapshotting and compaction policies
9. Sharding/partitioning strategies (keys, time, load)
10. Data validation gateways (pydantic, runtime checks)

## Module 8 — Reliability, Resilience & Observability

1. Retries with jitter; timeouts; circuit breakers
2. Rate limiting & token buckets (sync/async)
3. Dead letter queues & quarantine for poison pills
4. Health checks, readiness, liveness (service edges)
5. Structured logging (context, correlation IDs)
6. Metrics: RED/USE + domain KPIs (Prometheus-friendly)
7. Tracing spans across async boundaries
8. Fault injection & chaos drills (property + randomized tests)
9. Bulk data operations with safety rails (temp files, `os.replace`)
10. Incident-driven hardening; postmortem to code patterns

## Module 9 — APIs, Integration & Delivery

1. HTTP API patterns (idempotency keys, pagination, ETags)
2. GraphQL/gRPC vs REST: contract and evolution
3. Validation at edges; error schemas; problem+json
4. CLI/daemon duality; supervisors and lifecycles
5. Safe imports & dynamic loading (isolation, timeouts)
6. Security patterns: least privilege, secrets handling
7. Policy enforcement via linters/AST (forbidden imports, APIs)
8. Feature flags & gradual rollout patterns
9. Packaging, version pins, and reproducible builds
10. Backward/forward compatibility tests in CI

## Module 10 — Testing, Analysis & Performance Patterns

1. Test pyramid for patterns (unit/property/contract)
2. Property-based testing for invariants (Hypothesis)
3. Golden master tests for refactors (snapshots with care)
4. Fake clocks, deterministic schedulers for async
5. Contract tests for ports/adapters
6. Performance budgets; micro/macro benchmarking
7. Memory/GC profiling; object layout (`__slots__`)
8. Regression guards in CI (perf + behavior)
9. Static typing discipline (`mypy --strict` patterns)
10. Governance of patterns: review checklists, docs-as-tests

---
