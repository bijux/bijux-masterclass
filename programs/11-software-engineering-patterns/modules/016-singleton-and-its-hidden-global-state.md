---
module_id: SEPAT-016
program: Software Engineering: Patterns
level: 1
module_number: 16
title: Singleton and Its Hidden Global State
status: complete
last_verified: 2026-08-28
---

# Singleton and Its Hidden Global State

## One-Page Review

### Governing question

When is one instance genuinely required, and why should instance cardinality usually be enforced without granting every caller hidden global access?

### Essential definitions

- **Singleton** is the GoF creational pattern that restricts a class to one instance within a declared scope and provides a global access point to it.
- **cardinality** answers how many instances may exist; **access policy** answers who can obtain one and how dependencies are revealed.
- **global state** is state reachable without an explicit value or capability flowing through the caller's interface.
- A **hidden dependency** is a service or state read through global lookup rather than declared in parameters, fields, or an owned composition boundary.
- **scope** is the boundary within which uniqueness is claimed: object graph, request, thread, process, class loader, container, host, cluster, tenant, or domain key.
- **eager initialization** creates the instance before first use; **lazy initialization** creates it on demand.
- **safe publication** guarantees that every observer sees a fully initialized instance according to the language memory model.
- **temporal coupling** occurs when correctness depends on global initialization, reset, or shutdown order.
- A **composition root** constructs one instance deliberately and supplies it to consumers explicitly.
- **distributed uniqueness** is coordination across processes or hosts and cannot be established by a process-local Singleton alone.

### Central model, mechanism, or theorem

Separate cardinality from reachability. For scope (S) and service instances (I_S), a one-instance invariant is

$$
|I_S|=1.
$$

Global access adds a resolver (G:C\times T\to I_S), often available to every caller (C) at time (T). The cardinality equation does not imply that (G) is necessary. A composition root can create one (s\in I_S) and explicitly construct a dependency graph (D) whose required nodes reference (s). Concurrency additionally requires exactly-once initialization and a happens-before relation from completed construction to every published read.

### Critical invariants

- The uniqueness scope and reason are explicit and no broader than necessary.
- Every observer sees a fully initialized instance; initialization failure has defined retry or terminal behavior.
- Consumers declare the dependency instead of performing ambient lookup where practical.
- Mutable state has synchronization, ownership, and invariant protection.
- Startup, reconfiguration, shutdown, and resource release are deterministic.
- Tests can create isolated dependency graphs without shared reset hooks.
- Cardinality, lifetime, access, and immutability are evaluated separately.
- Cluster-wide uniqueness uses an appropriate coordination protocol and fencing, not a local static variable.

### Common failures

Common failures include using Singleton because “there is only one right now,” confusing one instance with global access, unsafe lazy initialization, publishing `this` during construction, assuming one instance across processes or class loaders, adding mutable caches and configuration without synchronization, test suites that depend on order or reset globals, service locators disguised as singleton registries, shutdown after dependencies have already disappeared, and replacing a singleton with a global pointer while preserving every hidden dependency.

### Compact example

An application composition function creates one AuditSink and injects it into Processor and Reporter. Both consumers share the instance within that graph, while a second application graph receives a distinct sink. Cardinality is one per graph, dependency visibility is explicit, and tests need no global reset. If the requirement were one audit leader per cluster, this code would be insufficient.

### Connections

[SEPAT-015](015-prototype.md) distinguishes intentional immutable sharing from global access. [SEPAT-018](../ROADMAP.md) develops explicit creation graphs through Dependency Injection; [SEPAT-019](../ROADMAP.md) analyzes lazy initialization separately. Singleton scope connects to [Operating Systems](../../22-operating-systems/ROADMAP.md), concurrency to [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md), and distributed coordination to [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md).

## Governing Question

What problem requires restricted cardinality, within exactly which boundary, and does solving it require ambient global reachability?

The original Singleton pattern combines two responsibilities: controlling construction and exposing an access point. Modern systems can usually separate them. A composition root creates one service for an application graph; constructor injection makes consumers explicit; a container can own one instance per scope without letting product code query the container.

This distinction makes critique precise. The claim “we need one metrics exporter per process” may be valid. The inference “therefore every class should call `Metrics.instance()`” does not follow.

## Why This Matters

Global mutable state expands the effective input of every function that can reach it. Behavior depends on call order, concurrent mutation, configuration history, and tests that ran earlier. Interfaces understate dependencies, making local reasoning and reuse harder.

Singleton initialization also interacts with language runtime rules. Naive check-then-create races can allocate several instances or expose partial state. Static initialization can be safe in one language version yet have class-loader, module-order, recursion, or shutdown surprises.

At larger scale, Singleton creates false confidence. Ten service processes each have one “singleton” scheduler, producing ten schedulers. Enforcing one active leader requires leases, consensus or an equivalent coordination authority, failure detection, and fencing of stale leaders.

## Prerequisites and Retrieval

You should understand constructors, static/global variables, dependency injection, concurrency, memory visibility, process boundaries, and resource lifecycle. Retrieve these facts:

1. One instance per process is not one instance per host, cluster, tenant, or domain.
2. Construction atomicity and safe publication are separate from reference equality.
3. Immutable global constants differ materially from mutable global services.
4. A dependency can remain single-scoped while being passed explicitly.
5. Test reset is a second mutation API with concurrency and ordering risk.
6. Distributed failover can leave a stale owner alive, so a lock alone may not protect effects.

## Learning Objectives

After completing this module, you should be able to:

- separate cardinality, access, lifecycle, mutability, and scope decisions;
- state a defensible uniqueness boundary and evidence;
- analyze eager and lazy initialization under a language memory model;
- identify hidden dependency, temporal coupling, and test-isolation failures;
- construct one explicit instance per application graph;
- design deterministic startup, reconfiguration, and shutdown;
- distinguish process-local Singleton from distributed leader or uniqueness protocols;
- refactor global access toward explicit dependencies safely.

## Core Exposition

### Start with scope

Ask “one per what?” A formatter may be one per request, a connection pool one per data source per process, a cache one per tenant, a device controller one per physical device, and a coordinator one active lease-holder per cluster.

If the scope is not named, the invariant cannot be verified. Language statics often mean one per class-loader or module instance, which may differ across plugins, test runners, interpreters, or reloads.

### Cardinality is not access

Create one object at the composition root and pass it to every consumer that needs it. This enforces cardinality for the graph while preserving visible dependencies. Tests create a fresh graph.

Global access is sometimes convenient for process primitives or legacy integration, but convenience is a consequence to weigh, not a logical requirement of uniqueness.

### Immutable constants

An immutable mathematical table or build identifier can be globally available safely when initialization and representation are stable. It has no mutable lifecycle and concurrent reads do not race.

Do not wrap every constant in a Singleton class. A module-level immutable value or pure function communicates more directly.

### Safe initialization

Eager initialization can use language/runtime guarantees and fail early. It may allocate unused expensive resources and create cross-module order problems. Lazy initialization delays cost and failure, but needs an exactly-once or idempotent creation protocol and safe publication.

Double-checked locking is correct only under specific memory-model and volatile/atomic rules. Prefer documented language primitives: class initialization, one-time cells, function-local statics, `call_once`, or container scope. Verify failure and recursion semantics.

### Initialization failure

What happens if construction fails? Some runtimes mark static initialization erroneous permanently; others retry on the next call. Infinite implicit retry can storm a dependency; permanent poisoning can make transient recovery impossible.

Expose classified failure at an owned startup or acquisition boundary. Health and readiness should reflect it. Do not let arbitrary domain calls become surprise initialization sites.

### Mutable state and synchronization

One instance can have many concurrent callers. Singleton does not make its fields thread-safe. Protect invariants with immutability, confinement, locks, atomics, actors, or transactions as appropriate.

Avoid a global “manager” that accumulates unrelated mutable maps. It becomes a contention point and broad failure domain.

### Lifecycle and shutdown

Resource-owning singletons need deterministic closure after consumers stop but before dependencies vanish. Runtime finalization or arbitrary static destruction order is rarely sufficient.

The composition root can start components in dependency order and stop them in reverse. It can propagate cancellation and await draining. Hidden lookups obscure that graph.

### Reconfiguration

Changing a global instance in place makes every consumer observe a moving target at different times. Prefer immutable configuration snapshots, explicit reload transactions, or construct-and-swap at a controlled boundary with versioned observations.

If an instance is replaced, define whether in-flight operations retain the old object, how it drains, and when resources close. “Singleton” no longer describes a stable identity automatically.

### Testing

Global singleton tests share history and fail under parallel execution. Reset methods expose otherwise private lifecycle, can race active users, and often leave subordinate caches or threads behind.

Construct a fresh dependency graph per test. Inject fakes or deterministic collaborators. If legacy global access cannot be removed immediately, isolate it behind one adapter and serialize only the smallest migration surface.

### Service Locator confusion

A singleton registry that returns arbitrary services is Service Locator plus global scope. It hides every consumer dependency and allows runtime failure by string/type key. The fact that the locator itself is unique adds no correctness.

Keep containers at the composition root. Inject ready services or narrow factories; do not pass or expose the container to domain code.

### Distributed uniqueness

One local object cannot prevent peers from acting. A cluster leader needs a coordination store or consensus system, lease expiry, monotonic term or fencing token, recovery, and effect-side rejection of stale leaders.

Database uniqueness constraints can enforce one row per domain key, but application replicas still need transaction and conflict handling. Choose the mechanism matching the actual scope.

### Legitimate uses

Some runtimes or hardware APIs impose one process instance; a process-wide signal router or event-loop integration may have genuine cardinality. Encapsulate it behind an explicit interface, minimize mutable state, and inject the handle downstream.

A documented local static for immutable or idempotent infrastructure can be acceptable when runtime semantics, failure, and shutdown are understood. The burden is contextual, not ideological.

### Refactoring away

Inventory every access, initialization side effect, identity assumption, reset, and shutdown dependency. Introduce an interface or concrete parameter at leaf consumers. Temporarily adapt through the old accessor at an outer boundary, then move construction upward.

Once all accesses are explicit, construct one instance at the root, delete reset/global lookup, and test multiple isolated graphs. Preserve cardinality only where still required.

## Definitions and Notation

Let scopes form a relation (belongs(i,S)). The scoped instance set is

$$
I_S=\{i\mid belongs(i,S)\}.
$$

A cardinality requirement may be exact (|I_S|=1), upper-bounded (|I_S|\le1), or keyed:

$$
\forall k\in K:\ |I_{S,k}|\le1.
$$

Let construction events be (create(i)) and reads (read_c(i)). Safe publication requires

$$
complete(create(i))\ hb\ read_c(i)\quad\forall c,
$$

where (hb) is the language-defined happens-before relation. Exactly-once initialization additionally requires only one successful publication for the scope generation.

For explicit dependency graph (D=(V,E)), every consumer requiring service (s) has an edge to the same instance, while consumers not requiring it have no ambient path by contract. This graph property is stronger for dependency visibility than a globally callable resolver.

## Mechanisms, Invariants, or Proof Structure

### State scope and cardinality

Name process, graph, tenant, key, device, or cluster; justify exact-one versus at-most-one and define generations.

### Separate construction and access

Prefer one owned composition boundary and explicit edges. If global access remains, constrain and document every caller and effect.

### Verify publication and lifecycle

Use runtime guarantees or synchronization, test concurrent first use and failure, and own startup/shutdown ordering.

### Demonstrate explicit one-per-graph scope

The executable example shares one sink inside each graph and isolates separate graphs.

<!-- bijux-verify: {"id":"explicit-single-instance-scope","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"shared-within-graph=True\nisolated-between-graphs=True\nevents=processed:7,reported:ready\n","stderr":""}} -->
```python
class AuditSink:
    def __init__(self):
        self.events = []

    def record(self, event):
        self.events.append(event)


class Processor:
    def __init__(self, audit):
        self.audit = audit

    def process(self, item_id):
        self.audit.record(f"processed:{item_id}")


class Reporter:
    def __init__(self, audit):
        self.audit = audit

    def report(self, state):
        self.audit.record(f"reported:{state}")


def make_application():
    audit = AuditSink()
    return audit, Processor(audit), Reporter(audit)


audit_a, processor_a, reporter_a = make_application()
audit_b, processor_b, reporter_b = make_application()
processor_a.process(7)
reporter_a.report("ready")

print(f"shared-within-graph={processor_a.audit is reporter_a.audit is audit_a}")
print(f"isolated-between-graphs={audit_a is not audit_b}")
print(f"events={','.join(audit_a.events)}")
```

The run proves selected identity relations in one thread. It does not prove synchronization, exactly-once runtime initialization, resource lifecycle, or distributed uniqueness.

### Test alternative scopes

Create multiple graphs, keys, tenants, processes, and concurrent callers as applicable. Verify isolation and intended sharing rather than only calling the accessor twice.

### Contract hidden access

Migrate leaves to parameters, move construction outward, remove global resets, and retain only the narrow scoped cardinality mechanism that evidence requires.

## Alternatives and Trade-Offs

**Immutable global constant.** Simple and race-free for stable values. It cannot own mutable lifecycle or context-specific configuration.

**Explicit one-per-graph instance.** Preserves cardinality and dependency visibility with isolated tests. It requires wiring through the graph.

**Container-scoped service.** Automates keyed/request/process scopes and lifecycle. Product code must not query the container.

**Singleton global accessor.** Convenient and protects local construction. It hides dependencies and creates temporal, concurrency, and testing costs.

**Module-level global.** Less ceremony than Singleton but retains global-state problems when mutable.

**Thread-local instance.** Avoids cross-thread sharing but multiplies state, breaks task migration assumptions, and is not one per process.

**Actor or service process.** Serializes state and makes messaging explicit. It adds queues, failure, backpressure, and lifecycle.

**Distributed lease/leader election.** Enforces active ownership across nodes under assumptions. It requires fencing, expiry, recovery, and coordination availability.

## Failure Modes and Misconceptions

1. **One instance implies global accessor.** Explicit injection can preserve cardinality.
2. **Singleton means one everywhere.** Scope may be class loader, process, container, or test runtime.
3. **Private constructor proves exactly once.** Reflection, serialization, reloads, races, and multiple runtimes can differ.
4. **Lazy initialization is a null check.** Safe publication and failure semantics are required.
5. **One object is thread-safe.** Mutable operations still need synchronization.
6. **Reset makes tests isolated.** Resets are global mutation and can miss subordinate state.
7. **Service locator is dependency injection.** Lookup hides requirements; injection supplies them explicitly.
8. **A process Singleton elects a cluster leader.** Every process can instantiate one.
9. **Leaking a singleton avoids destructor problems.** It abandons resource and observability obligations.
10. **Singleton is always wrong.** Genuine runtime cardinality exists, but scope and access still need evidence.

## Worked Examples

### Example 1

**Question:** What does the executable example establish?

**Reasoning:** One composition call creates one AuditSink shared by two declared consumers; another call creates an isolated graph. No global accessor or reset is required.

**Conclusion:** One-per-graph cardinality does not require global state.

### Example 2

**Question:** Should an immutable unit-conversion table be Singleton?

**Reasoning:** If values are compile-time or immutable verified data, a constant/module value or pure function is clearer. There is no managed mutable identity.

**Conclusion:** Immutability can remove the pattern's main forces.

### Example 3

**Question:** How should a database pool be scoped?

**Reasoning:** Usually one per process per data-source/credential/configuration key, not one universal pool. The root owns startup, health, draining, and close; consumers receive a pool or narrow lease factory.

**Conclusion:** Keyed cardinality and lifecycle matter more than the class name.

### Example 4

**Question:** Why can naive lazy initialization fail?

**Reasoning:** Two threads can observe absence and construct twice; weak publication can expose incomplete fields. Use a runtime one-time primitive with documented memory ordering.

**Conclusion:** Creation count and visibility both require proof.

### Example 5

**Question:** Can a test reset a global cache safely?

**Reasoning:** Only if no concurrent user, background task, reference, or subordinate state survives—conditions hard to establish. Fresh cache instances per test graph are safer.

**Conclusion:** Isolation by construction beats cleanup of ambient history.

### Example 6

**Question:** Is a singleton service registry harmless?

**Reasoning:** Every lookup hides a dependency and can fail at runtime. The unique registry becomes a global Service Locator. Keep it at the root and inject resolved services.

**Conclusion:** Uniqueness does not legitimize broad resolution authority.

### Example 7

**Question:** How should reconfiguration work?

**Reasoning:** Build an immutable new configuration/service graph, validate it, atomically route new operations, drain old users, and close in order. Record generation in telemetry.

**Conclusion:** Treat replacement as a lifecycle migration, not field mutation.

### Example 8

**Question:** Does one scheduler object prevent duplicate jobs in a cluster?

**Reasoning:** No; every replica has one. Use a lease or consensus-backed leader with a fencing term checked by the job-effect authority, or make jobs idempotent with transactional uniqueness.

**Conclusion:** Distributed scope requires distributed coordination.

### Example 9

**Question:** When can a process-local instance be justified?

**Reasoning:** A runtime may allow one signal dispatcher or hardware session. Encapsulate construction, expose a narrow injected handle, minimize state, and test lifecycle/concurrency.

**Conclusion:** Valid cardinality need not imply ubiquitous access.

### Example 10

**Question:** How should a legacy Singleton be removed?

**Reasoning:** Inventory accesses, add parameters at leaves, adapt at outer boundaries, move construction toward the root, preserve behavior and scope, then delete accessor/reset and test two graphs.

**Conclusion:** Refactor access separately from cardinality.

## Cross-Program Connections

- **Concurrent Programming:** one-time initialization, safe publication, races, and memory ordering determine correctness.
- **Object-Oriented Programming:** constructors and encapsulation can restrict creation but do not define runtime scope universally.
- **Software Design:** explicit dependencies, information hiding, and composition roots counter global reachability.
- **Testing & Quality Engineering:** parallel tests expose global history, lifecycle, and reset defects.
- **Operating Systems:** processes, threads, dynamic loading, signals, and resource teardown define local scopes.
- **Distributed Systems:** leader election, leases, consensus, and fencing govern cluster ownership.
- **Database Engineering:** uniqueness constraints and transactions enforce keyed invariants across replicas.
- **Security Engineering:** global capabilities broaden authority and complicate revocation/audit.
- **Platform Engineering:** containers, plugins, and reloads create multiple runtime scopes inside one host.
- **Reliability Engineering:** startup, readiness, drain, failover, and shutdown are lifecycle evidence.

## References

1. Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, [*Design Patterns: Elements of Reusable Object-Oriented Software*](https://www.pearson.com/en-us/subject-catalog/p/Gamma-Design-Patterns-Elements-of-Reusable-Object-Oriented-Software/P200000009480/9780321700698), Addison-Wesley, 1994. Canonical Singleton intent, structure, participants, consequences, and implementation discussion.
2. Bjarne Stroustrup and Herb Sutter, editors, [*C++ Core Guidelines*](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines), rules I.2, I.3, and I.22, accessed 2026-08-28. Discusses hidden global dependencies, singleton variants, data races, local static initialization, and global initialization order.
3. Oracle, [*The Java Language Specification*, §12.4.2](https://docs.oracle.com/javase/specs/jls/se20/html/jls-12.html#jls-12.4.2), accessed 2026-08-28. Defines synchronized class/interface initialization, recursion, completion, failure, and memory-order requirements.
4. Oracle, [*The Java Language Specification*, §17.4.5](https://docs.oracle.com/javase/specs/jls/se17/html/jls-17.html#jls-17.4.5), accessed 2026-08-28. Defines happens-before relationships relevant to safe publication and data races.
5. Martin Fowler, [“Inversion of Control Containers and the Dependency Injection Pattern”](https://martinfowler.com/articles/injection.html), 2004, accessed 2026-08-28. Compares injection with singleton Service Locator and emphasizes separating configuration from use.
6. Mark Seemann and Steven van Deursen, *Dependency Injection Principles, Practices, and Patterns*, Manning, 2019, ISBN 978-1-61729-473-0. Develops composition roots, scopes, lifetime, and explicit dependency graphs.
7. Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly, 2017, ISBN 978-1-4493-7332-0. Provides distributed coordination, fencing, leases, and consistency context that bounds process-local uniqueness.

## Exercises

### Exercise 1

For the executable example, formalize scope and identity properties. Extend the design to two tenants, each with one AuditSink, without global lookup.

### Exercise 2

Analyze eager class initialization, synchronized lazy initialization, and unsafe double-checked locking under startup failure, recursion, concurrency, memory visibility, and shutdown.

### Exercise 3

Plan migration of a singleton cache with global reset into explicit keyed per-tenant caches while preserving behavior, metrics, capacity, and rollout safety.

### Exercise 4

Design one active scheduler per cluster using a lease and fencing token. State failure assumptions, stale-leader cases, effect-side checks, observability, and rollback.

### Exercise 5

An unfamiliar railway signaling platform claims a Singleton guarantees one command authority. Produce a graduate-level critique and replacement covering process/host/cluster scopes, failover, fencing, hard real-time boundaries, safety invariants, evidence, and human authorization.

## Answers to the Exercises

### Answer 1

Scope is one call to `make_application`, representing one dependency graph. For each graph (g), exactly one sink (a_g) exists and Processor/Reporter edges both target it. For two distinct graphs (g_1\ne g_2), (a_{g_1}\ne a_{g_2}). The run proves these identities for two graphs and one thread.

For tenants, define `make_tenant(tenant_id)` that creates one sink tagged with that immutable tenant ID and injects it into tenant Processor/Reporter instances. The application root creates a map from authorized tenant IDs to complete tenant graphs. Routing resolves a tenant once at an authenticated boundary and passes the selected graph explicitly; domain consumers never query the map. Tests create two tenants and verify within-tenant sharing, cross-tenant nonidentity, event isolation, authorization, and independent shutdown.

### Answer 2

Eager class initialization uses runtime ordering/publication guarantees and surfaces failure near startup, but can initialize unused services, recurse through other classes, and poison the class after failure according to runtime rules. Shutdown still requires explicit ownership; class initialization guarantees do not define resource drain.

Synchronized lazy initialization serializes first use, publishes after complete construction, and can define retry/poison policy. It moves latency/failure to a caller and must handle recursive initialization without deadlock or partial return. Unsafe double-checked locking can race creation or expose stale/partial state when the reference lacks the required atomic/volatile semantics; correctness is language/version-specific. Prefer a documented one-time primitive or explicit root startup. In every case test concurrent first use, injected failure, recursion, cancellation if applicable, and deterministic reverse-order shutdown.

### Answer 3

Inventory keys, callers, eviction, TTL, loader, metrics, capacity, background tasks, reset behavior, and tenant assumptions. Characterize hit/miss/value/error and concurrency behavior. Introduce `TenantCache` as an explicit dependency and a root-owned map keyed by authenticated tenant. Initially wrap the existing cache behind a compatibility adapter while adding tenant tags to metrics.

Migrate leaf consumers to injected caches, then route tenant at outer boundaries. Partition keys and capacity; prevent cross-tenant reads, noisy-neighbor exhaustion, and metric-label explosion. Roll out by tenant cohorts with hit ratio, latency, load, memory, eviction, and correctness comparison. Create new graph generations for configuration changes, drain loaders/tasks, then close. Once access inventory is zero, remove global accessor/reset and adapter. Fault-test eviction, expiry, loader failure, concurrent miss, tenant deletion, rollout rollback, and two graphs in parallel.

### Answer 4

Candidates acquire a time-bounded lease from a linearizable coordination authority. Each successful acquisition receives monotonically increasing fencing term (t). The scheduler attaches (t) to every job claim and side effect; the database/queue/device authority rejects terms lower than the greatest accepted for that resource. Renew before expiry using bounded clocks/authority semantics; stop scheduling on lost renewal or uncertain ownership.

Test pause beyond expiry, partition, delayed renewal, process restart, duplicated messages, coordination failover, clock behavior under the lease model, and old leader resumption. Idempotency and transactional job keys complement fencing. Observe holder identity, term, lease deadline, renewal latency/failure, rejected stale effects, duplicates, and handoff duration. Rollback changes software version without reusing an old term. Availability during coordination failure follows declared policy; never sacrifice a safety/uniqueness constraint silently.

### Answer 5

A static field supplies at most one object per runtime scope—possibly per process, class loader, container, or plugin. Redundant processes and hosts each create one; paused or partitioned old processes can resume. Therefore it cannot establish one railway command authority across the safety system.

Define authority per controlled interlocking/route domain. Use a safety-certified coordination/allocation protocol appropriate to the railway architecture, with monotonically increasing epoch/fencing token persisted and checked by every command-accepting endpoint. A new authority cannot command until state synchronization and safety preconditions complete; an old epoch is rejected even if its process remains alive. Hard real-time local interlocks independently enforce movement-authority, route-conflict, occupancy, speed, and fail-safe constraints; remote coordination latency must not bypass them. Loss or ambiguity moves to a specified safe state.

Analyze simultaneous startup, partition, pause, delayed packets, replay, clock failure, restart with stale state, epoch-store failure, corrupted messages, endpoint isolation, failover during command, and recovery. Evidence includes formal safety invariants/protocol analysis where tractable, independent hazard analysis, model checking, timing analysis, simulation, hardware-in-the-loop, fault injection, cybersecurity assessment, requirements traceability, and controlled operational validation. Named railway safety, signaling, systems, real-time, security, verification, regulatory, and operations authorities approve the architecture and deployment. Repository validation or process-local identity proves no signaling safety claim.
