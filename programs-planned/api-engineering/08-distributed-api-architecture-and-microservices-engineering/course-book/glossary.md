# Glossary

**Anti-corruption layer** — mapping that protects one service’s model from another service’s language and representation.

**Authoritative fact** — business state whose meaning and writes are controlled by exactly one service.

**Bounded context** — boundary within which terms, rules, and models have one coherent meaning. It may remain an internal module.

**Bulkhead** — limit that isolates resource exhaustion between workloads or dependencies.

**Capability token** — narrow, audience-bound authority to perform a specific action on a specific resource for a short period.

**Choreography** — workflow coordination through independently consumed events without one central process manager.

**Compensation** — a new forward business action that addresses a previously completed step; not historical erasure.

**Context map** — description of contexts and the translation or dependency relationships between them.

**Data ownership** — exclusive authority to write the canonical form of a business fact and govern its lifecycle.

**Dependency budget** — portion of a caller’s absolute deadline and attempt budget allocated to one downstream interaction.

**Distributed monolith** — separately deployed components that remain change-, data-, release-, and failure-coupled.

**Effect identity** — stable identifier for one intended business effect across retries and duplicate delivery.

**Fencing token** — monotonic generation used by an owner to reject stale actors after lease or leadership changes.

**Fitness function** — executable or reviewable rule that protects an architecture property over time.

**Gateway** — edge component responsible for protocol termination, routing, and bounded composition; not a default business authority.

**High-water mark** — captured upper boundary that stabilizes traversal or migration population.

**Orchestration** — workflow coordination by an explicit process manager that tracks steps, timeouts, and outcomes.

**Process manager** — durable application component that owns progress toward one cross-service business outcome.

**Projection** — local derived view built from another service’s authoritative contract.

**Reconciliation** — deterministic comparison of durable states to find missing, duplicate, orphaned, or inconsistent effects.

**Saga** — durable sequence of owner-local transactions and compensating actions for a cross-service business workflow.

**Semantic lock** — business representation of reserved intent or current authority, such as a lease generation, rather than a long database lock.

**Service** — independently owned capability with explicit interfaces, data or a declared non-data role, release responsibility, and operations.

**Service instance** — one running copy of a service implementation.

**Shadow traffic** — candidate execution whose result is compared but is not authoritative and must suppress real side effects.

**Strangler migration** — incremental transfer through shadowing, comparison, one-writer cutover, rollback, and decommission.

**Temporal coupling** — requirement that two components be available at the same time for progress.

**Version skew** — period during which callers and providers run different supported versions.

**Workload identity** — authenticated identity of a deployed service or process, distinct from end-user authority.
