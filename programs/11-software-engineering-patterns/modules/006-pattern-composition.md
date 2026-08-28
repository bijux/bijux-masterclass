---
module_id: SEPAT-006
program: Software Engineering: Patterns
level: 1
module_number: 6
title: Pattern Composition
status: complete
last_verified: 2026-08-28
---

# Pattern Composition

## One-Page Review

### Governing question

How can several pattern instances share participants and responsibilities without creating contradictory contracts, hidden control flow, or emergent failure?

### Essential definitions

- **Pattern composition** integrates two or more pattern instances into one design whose roles, collaborations, and consequences interact.
- A **role** is a responsibility and collaboration contract that a participant fulfills in a pattern instance.
- **Role binding** assigns a concrete participant to a pattern role; **role fusion** lets one participant fulfill compatible roles from several patterns.
- **Stringing** connects one pattern's output or boundary to another without merging roles deeply.
- **Overlapping** composes patterns by sharing or fusing participants and responsibilities.
- A **pattern compound** or **composite pattern** is a recurring synergistic composition with its own context, problem, forces, and consequences—not merely several co-located patterns.
- A **composition invariant** is a contract that must hold across all integrated instances.
- **Emergent behavior** arises from interactions among patterns and is not visible when each is analyzed alone.
- **Pattern soup** is a design with many named roles but no coherent force, ownership, or interaction model.

### Central model, mechanism, or theorem

Treat each pattern instance as a contract graph (G_i=(V_i,E_i,C_i)), where nodes are roles, edges are collaborations, and (C_i) contains state, control, time, error, lifecycle, and authority constraints. Composition binds roles through a mapping (\mu) and is valid only when all fused contracts are compatible:

\[
G=G_1\oplus_\mu G_2,
\qquad Compatible(C_1,C_2,\mu).
\]

Composition is generally neither commutative nor freely associative. `Cache(Authorize(Service))` can bypass authorization on a cache hit, whereas `Authorize(Cache(Service))` rechecks authority before every result. Order and boundary placement are part of correctness.

### Critical invariants

- Every pattern remains tied to a distinct force; no participant exists only to display vocabulary.
- Fused roles have compatible identity, state ownership, lifecycle, concurrency, and error contracts.
- Control and data flow are traced end to end, including short-circuit and failure paths.
- Ordering assumptions are explicit where wrappers, handlers, retries, transactions, or events compose.
- Security checks cannot be bypassed by caching, routing, retry, or asynchronous boundaries.
- Local pattern guarantees are not promoted automatically to system guarantees.
- The composition has an owner, verification plan, and removal seams.

### Common failures

Common failures include merging roles because names look similar, composing only class diagrams, hiding wrapper order, giving two patterns ownership of the same state, allowing retries outside deadlines, placing caches outside authorization, mixing transaction and event boundaries without atomicity, assuming “decoupled” patterns cannot interact, and naming an accidental bundle as a composite pattern without recurrence or synergy.

### Compact example

Repository and Unit of Work often compose: Repository offers collection-like access while Unit of Work owns identity, change tracking, and commit. If each creates its own session or identity map, one business operation can hold duplicate objects and split transactions. The valid composition binds repositories to the same unit-of-work scope and makes commit ownership singular.

### Connections

[SEPAT-005](005-trade-offs-and-negative-consequences.md) supplies consequence and interaction analysis. [SEPAT-007](../ROADMAP.md) develops sequences and languages rather than one integrated design. Composition depends on object roles from [OOP-001](../../02-programming-languages-object-oriented-programming/modules/001-objects-as-state-behavior-and-identity.md) and end-to-end concurrency reasoning from [Concurrent & Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md).

## Governing Question

When individually valid patterns meet at one participant or boundary, what must agree so the combined design remains coherent?

Real systems rarely contain isolated pattern specimens. A Strategy may be created by a Factory, an Adapter exposed behind a Facade, a Command recorded by a Memento, or a Repository scoped by a Unit of Work. Resilience designs combine deadlines, retries, circuit breakers, queues, and bulkheads.

Composition is not catalog addition. The patterns can compete for control, state, identity, time, and authority. A cache may prevent a Decorator from executing. A retry wrapper may repeat a transaction. An asynchronous Observer may run after its Unit of Work is closed. The combined contract—not the correctness of each part—is the review unit.

## Why This Matters

Pattern names improve local communication, which can conceal system-level gaps. Each component owner can truthfully say their implementation follows a known pattern while an end-to-end invariant fails. Many production defects live at these seams: duplicate messages after retry, stale authorization after caching, nested transactions with inconsistent commit, callback reentrancy through Observer, or deadlocks between Monitor Objects.

Disciplined composition also prevents overengineering. If a design needs Factory, Strategy, Registry, Adapter, Facade, and Dependency Injection to vary one simple function, the role graph may reveal multiple participants answering the same force. Composition review can collapse them into a smaller coherent design.

## Prerequisites and Retrieval

You should understand pattern form, applicability, consequences, object identity, call order, and failure propagation. Retrieve these facts:

1. A role describes responsibility; one object can fulfill several roles.
2. Static dependency and runtime control flow are different graphs.
3. Wrappers can short-circuit inner behavior.
4. Retry can repeat effects unless the operation contract prevents duplication.
5. Transaction scope, identity scope, and request scope need not coincide.
6. A local guarantee holds only under its stated boundary and assumptions.

## Learning Objectives

After completing this module, you should be able to:

- distinguish stringing, overlapping, role fusion, and composite patterns;
- model each pattern instance as roles, collaborations, and contracts;
- test role compatibility across state, control, time, errors, lifecycle, and authority;
- explain why composition order and boundary placement matter;
- identify emergent behavior and guarantee gaps;
- simplify pattern soup by tracing roles back to forces;
- verify end-to-end invariants rather than isolated instances;
- document a recurring synergistic composition without overstating it as a new pattern.

## Core Exposition

### Compose roles, not names

Pattern diagrams name abstract participants: Subject and Observer, Context and Strategy, Command and Receiver. Concrete software binds objects, functions, modules, services, tables, or processes to those roles. Composition begins by listing responsibilities and collaboration contracts, not by overlaying boxes with similar names.

One participant can legitimately fulfill several roles. A document node can be both Composite child and Visitable element. A service adapter can be both Strategy implementation and Adapter. Fusion is safe only if identity, lifecycle, and behavior agree. Similar labels such as “handler” do not establish compatibility.

### Stringing and overlapping

**Stringing** keeps pattern boundaries mostly distinct. A Factory constructs a Strategy, then the client uses it. The construction output connects the patterns, but Factory does not own algorithm execution.

**Overlapping** shares participants or mechanisms. A Mediator can also be an Observer of colleagues; a Decorator can also serve as Proxy when it mediates access. Overlap reduces objects but increases responsibility density and lifecycle coupling. Document which role owns each decision.

### Contract dimensions

For every binding, compare:

- **type and data:** representation, validation, mutability, and ownership;
- **identity:** whether roles require shared, copied, cached, or unique identity;
- **state:** authoritative owner, consistency, reset, and persistence;
- **control:** caller, callback, short-circuit, reentrancy, and recursion;
- **time:** deadline, ordering, scheduling, retry, and expiration;
- **errors:** translation, propagation, aggregation, suppression, and compensation;
- **lifecycle:** creation, registration, scope, shutdown, and cleanup;
- **authority:** credentials, access checks, trust, and side effects;
- **observation:** logs, metrics, traces, audit, and source correlation.

A mismatch in any dimension can invalidate composition even when interfaces type-check.

### Order is semantic

Wrapper and pipeline order determines which behavior executes and what it observes. Authorization outside caching checks every request before a cached value is returned. Caching outside authorization can return a value without invoking the check. Logging outside Retry records one logical operation; logging inside records each attempt. A transaction outside a Command handler includes all work; inside it may commit before outer behavior finishes.

Write order as an explicit expression or sequence diagram. Test alternative orders and negative paths. Framework defaults are policy choices, not neutral wiring.

### Shared state needs singular authority

Repository, Identity Map, and Unit of Work illustrate state composition. Repository queries should return the same in-scope identity where the model requires it. Unit of Work coordinates changes and commit. If each repository owns an independent session, identity and transaction guarantees fragment.

Declare scope and authority once: one unit of work creates repositories bound to its identity map and transaction; only it commits. Repositories may stage changes but do not secretly begin independent transactions.

### Time and retries compose multiplicatively

Nested retries can multiply attempts. Three client attempts around two SDK attempts can issue six calls. Independent timeouts can exceed the caller deadline. Queued work can start after its usefulness expired. Compose one end-to-end time budget and one attempt budget, then allocate them across layers.

Circuit breakers, bulkheads, and queues observe different signals. Define whether rejection counts as failure, whether probes bypass queues, and whether retries consume reserved capacity. Otherwise feedback loops emerge.

### Asynchrony changes lifetime

Observer or event patterns can move work beyond the publisher's call and transaction. Objects, credentials, trace context, and database sessions valid during publication may be invalid later. Transfer durable values or explicit capabilities, not borrowed state whose lifetime ended.

Also decide delivery semantics, ordering, duplicates, and subscriber failure. “Decoupled” means some dependencies changed form; it does not remove semantic coupling to event meaning.

### Composite patterns require synergy and recurrence

A one-off design using several patterns is a composition. A **composite pattern** claims more: the integrated arrangement recurs, produces a stable synergy, and is best explained as a whole with its own context, forces, solution, and consequences. Model–View–Controller is often analyzed as a composition of observer-like update, strategy-like controller variation, and composite views, but its overall interaction is the reusable subject.

Do not publish “Factory + Strategy” as a new composite pattern merely because the pair appears once. Document the local composition first; mine a pattern only after independent recurrence and stable synergy.

### Composition can justify simplification

Build a force-to-role map. If two abstractions answer the same force, see whether one can own it. If a role has no mapped force, remove it. If several roles always change and live together, fusion may improve cohesion. If one participant carries incompatible lifecycles, split it.

The goal is not the fewest objects or patterns. It is the smallest design whose contracts make the required interactions explicit and verifiable.

## Definitions and Notation

For pattern instance (i), define contract graph

\[
G_i=(V_i,E_i,C_i),
\]

where (V_i) is roles, (E_i) collaborations, and (C_i) constraints. A role-binding map (\mu:V_i\rightharpoonup P) assigns roles to concrete participants (P). Role fusion occurs when

\[
\mu(v_a)=\mu(v_b),\quad v_a\in V_1,\ v_b\in V_2.
\]

Fusion is valid only if the conjunction of role contracts is satisfiable for the participant:

\[
Sat(C(v_a)\land C(v_b)\land C_{interaction}).
\]

This is an engineering obligation; general satisfiability is not claimed to be automated.

Let composition (G_1\oplus_\mu G_2) unify bound roles and add cross-pattern edges. In general,

\[
G_1\oplus G_2\ne G_2\oplus G_1
\]

when composition encodes wrapper or pipeline order. Similarly, regrouping three stateful patterns can change scope and behavior, so associativity must not be assumed.

Define end-to-end invariant (I) over traces (\tau) of the composed system:

\[
\forall \tau\in Traces(G),\ I(\tau).
\]

Unit tests for each (G_i) do not imply this property for (G).

## Mechanisms, Invariants, or Proof Structure

### Inventory instances and forces

Name each pattern instance, the force that justifies it, and the concrete roles. Remove labels whose force is absent. Include the direct design as a baseline.

### Bind roles explicitly

Create a table from abstract roles to participants. Mark fused roles and verify responsibility, state, identity, lifecycle, concurrency, and authority compatibility.

### Trace normal and adverse flows

Walk successful calls, cache hits, retries, short circuits, cancellation, timeout, partial failure, recovery, and shutdown. Record which pattern owns each transition and error.

### Test order as a correctness property

The executable example shows why cache and authorization composition is noncommutative. The cache is intentionally keyed only by resource to make the unsafe contract visible.

<!-- bijux-verify: {"id":"cache-authorization-order","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"unsafe owner: classified:report\nunsafe guest: classified:report\nsafe owner: classified:report\nsafe guest: denied\n","stderr":""}} -->
```python
def load(user, resource):
    return f"classified:{resource}"


def authorize(next_call):
    def wrapped(user, resource):
        if user != "owner":
            return "denied"
        return next_call(user, resource)
    return wrapped


def cache_by_resource(next_call):
    stored = {}

    def wrapped(user, resource):
        if resource not in stored:
            stored[resource] = next_call(user, resource)
        return stored[resource]
    return wrapped


unsafe = cache_by_resource(authorize(load))
safe = authorize(cache_by_resource(load))

print("unsafe owner:", unsafe("owner", "report"))
print("unsafe guest:", unsafe("guest", "report"))
print("safe owner:", safe("owner", "report"))
print("safe guest:", safe("guest", "report"))
```

The safe order is still only a toy. Production caches need tenant-aware keys, invalidation, classification, audit, and protection against side channels.

### Verify cross-pattern invariants

Add integration, property, concurrency, fault, security, and lifecycle tests at the composed boundary. Assert attempt and deadline budgets, transaction/identity scope, access checks, ordering, and cleanup.

### Reassess emerging consequences

Measure combined latency, state, change surface, traceability, and operations. If composition adds more policy than it removes, split or simplify it.

## Alternatives and Trade-Offs

**Keep patterns adjacent.** Stringing preserves independent ownership and testing. It can add conversion boundaries and repeated traversal.

**Fuse roles.** Fewer participants can improve locality and reduce indirection. Responsibility density and lifecycle conflict can increase.

**Introduce an orchestrator.** Central control makes order and failure visible. It can become a mediator bottleneck or oversized workflow object.

**Use declarative composition.** Middleware or pipeline configuration exposes order as data and enables validation. Runtime resolution and hidden defaults can impair debugging.

**Adopt a framework compound.** A mature framework supplies integrated lifecycle and tested variants. It constrains composition policy and creates dependency/upgrade obligations.

**Design one cohesive abstraction.** A purpose-built component can replace several pattern roles. It may lose shared vocabulary and reusable extension points.

**Compose incrementally.** Add one pattern after evidence and measure interactions. This reduces speculation but may require later boundary migration.

## Failure Modes and Misconceptions

1. **Valid patterns compose into a valid system automatically.** Cross-pattern contracts can conflict.
2. **Similar role names should share an object.** Compatibility depends on responsibility and lifecycle, not labels.
3. **Composition is visible in a class diagram.** Order, failure, time, authority, and state require dynamic views.
4. **Wrapper order changes only performance.** It can change authorization, transaction, error, and observation semantics.
5. **More patterns mean more decoupling.** Semantic and temporal coupling can increase with structural indirection.
6. **A framework's default order is correct for every context.** Defaults encode one policy and threat model.
7. **Retries at each layer increase reliability.** They can multiply load and violate deadlines.
8. **Asynchronous events preserve publisher scope.** sessions, transactions, and borrowed capabilities may expire.
9. **Any recurring pair is a composite pattern.** Stable synergy, independent recurrence, and a whole-pattern argument are required.
10. **Pattern soup is cured by better naming.** Remove or fuse roles whose forces and contracts do not justify them.

## Worked Examples

### Example 1

**Question:** How do Factory and Strategy compose?

**Reasoning:** Factory owns construction and configuration; Strategy owns algorithm behavior. Stringing is clean when Factory returns a strategy satisfying the stable contract and has no control over later execution. If Factory caches strategies, state and lifecycle consequences enter the composition.

**Conclusion:** Connect construction output to behavior while keeping ownership boundaries explicit.

### Example 2

**Question:** Can one object be both Adapter and Strategy?

**Reasoning:** Yes, when each provider adapter translates to the local capability and the client selects among providers as strategies. The fused object must satisfy semantic translation, algorithm contract, provider lifecycle, and selection identity. Provider-specific failures cannot be erased.

**Conclusion:** Role fusion is valid when all role contracts remain visible and compatible.

### Example 3

**Question:** How do Composite and Visitor interact?

**Reasoning:** Composite supplies recursive element structure; Visitor externalizes operations over element variants. Each element accepts the visitor, and traversal ownership must be decided. Adding element types burdens visitors; adding operations is localized.

**Conclusion:** The composition trades operation extensibility against element-family extensibility.

### Example 4

**Question:** Why can Observer plus Mediator become opaque?

**Reasoning:** A mediator observing colleagues can reduce direct dependencies, but colleague changes trigger callbacks that cause further mediator updates. Without reentrancy and cycle policy, notification loops or order-dependent state emerge.

**Conclusion:** Combined event and coordination control needs an explicit transition model.

### Example 5

**Question:** How should Repository, Identity Map, and Unit of Work share scope?

**Reasoning:** Repositories within one business operation use the same identity map and transaction owned by one Unit of Work. Reads of one identity return one in-scope object; commit happens once. Independent repository sessions violate both guarantees.

**Conclusion:** Singular identity and commit authority are cross-pattern invariants.

### Example 6

**Question:** What does the cache/authorization program prove?

**Reasoning:** An owner populates the resource-only outer cache with authorized data. A guest cache hit never invokes the inner authorization and receives the data. When authorization is outermost, the guest is denied before cache access.

**Conclusion:** Wrapper composition is noncommutative and security order requires executable negative-path evidence.

### Example 7

**Question:** How do Command and Memento compose for undo?

**Reasoning:** Command represents the action; Memento captures state needed to reverse it without exposing internals. The composition must define capture timing, storage cost, failed-command behavior, and whether external effects are reversible.

**Conclusion:** Undo is not guaranteed by the names; snapshot and effect contracts determine it.

### Example 8

**Question:** What is the risk of Retry around a transaction?

**Reasoning:** If retry repeats a transaction after an ambiguous commit, effects may duplicate. The transaction gives local atomicity but not knowledge of whether the response was lost. Stable operation identity and deduplication or reconciliation are required.

**Conclusion:** Transaction and Retry guarantees leave an outcome-ambiguity gap at their boundary.

### Example 9

**Question:** How do Transactional Outbox and Idempotent Consumer compose?

**Reasoning:** Outbox closes local write/publication atomicity but commonly permits duplicate delivery. The consumer records stable message identity with its effect so replay is harmless under the declared scope. Retention and identity collisions remain shared policy.

**Conclusion:** The two patterns jointly address different halves of reliable delivery; neither alone provides exactly-once execution.

### Example 10

**Question:** When is Factory–Strategy–Registry pattern soup?

**Reasoning:** If two fixed pure functions can be selected by one configuration key, a dictionary of callables may fulfill construction, lookup, and behavior with one explicit structure. Separate classes and registries add no distinct lifecycle or change ownership.

**Conclusion:** Collapse roles when their supposed forces and contracts do not differ.

## Cross-Program Connections

- **Object-Oriented Programming:** roles, identity, delegation, and dynamic dispatch provide common composition mechanisms.
- **Functional Programming:** higher-order function composition makes order explicit but does not remove state, error, or authority interactions.
- **Concurrent Programming:** lock order, task lifetime, queues, callbacks, and cancellation create cross-pattern invariants.
- **Metaprogramming:** annotations and middleware can assemble compositions while hiding the final call graph.
- **Software Architecture:** component and connector contracts scale role composition across deployment boundaries.
- **Testing & Quality Engineering:** unit correctness does not imply integration invariants; composition needs adverse end-to-end tests.
- **Database Engineering:** identity, transaction, cache, and persistence patterns require shared scope and authority.
- **Distributed Systems:** deadlines, retries, duplication, queues, and circuit state form feedback loops.
- **Security Engineering:** authorization order, credential lifetime, isolation, and audit must survive every boundary.
- **Platform Engineering:** frameworks standardize composition order and lifecycle, making their defaults governed policy.

## References

1. Dirk Riehle, [“Composite Design Patterns”](https://www.ubilab.org/publications/print_versions/pdf/rie97e.pdf), *OOPSLA '97*, pp. 218–228, ACM Press, 1997. Primary paper defining composite patterns through role-based composition and emergent synergy.
2. Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, [*Design Patterns: Elements of Reusable Object-Oriented Software*](https://www.pearson.com/en-us/subject-catalog/p/design-patterns-elements-of-reusable-object-oriented-software/P200000009480/9780321700698), Addison-Wesley, 1994. Discusses pattern relationships and compositions, including the pattern interactions in Model–View–Controller.
3. Frank Buschmann, Kevlin Henney, and Douglas C. Schmidt, [*Pattern-Oriented Software Architecture, Volume 5: On Patterns and Pattern Languages*](https://www.oreilly.com/library/view/pattern-oriented-software/9780471486480/30_pattern-concept.html), Wiley, 2007. Distinguishes pattern compounds, sequences, languages, relations, and resulting contexts.
4. Sherif M. Yacoub and Hany H. Ammar, [*Pattern-Oriented Analysis and Design: Composing Patterns to Design Software Systems*](https://www.oreilly.com/library/view/pattern-oriented-analysis-and/0201776405/ch05.html), Addison-Wesley, 2003, ISBN 978-0-201-77640-9. Develops pattern-level composition models, role/type/class views, traceability, and composability.
5. Frank Buschmann, Regine Meunier, Hans Rohnert, Peter Sommerlad, and Michael Stal, *Pattern-Oriented Software Architecture, Volume 1: A System of Patterns*, Wiley, 1996. Connects architectural, design, and idiomatic patterns in systems and explains their relationships.
6. Gregor Hohpe and Bobby Woolf, *Enterprise Integration Patterns*, Addison-Wesley, 2003, ISBN 978-0-321-20068-6. A pattern language whose message-routing, transformation, endpoint, and management patterns demonstrate operational composition.
7. Martin Fowler, *Patterns of Enterprise Application Architecture*, Addison-Wesley, 2002, ISBN 978-0-321-12742-6. Documents collaborations among Repository, Unit of Work, Identity Map, Data Mapper, transaction, and domain patterns.

## Exercises

### Exercise 1

Classify each relation as stringing, overlapping, or potential role fusion: Factory constructs Strategy; Mediator subscribes as Observer; Adapter is one selected Strategy; Facade calls several independent subsystem services.

### Exercise 2

Change the unsafe cache key in the executable example from `resource` to `(user, resource)`. Does that make `Cache(Authorize(Service))` equivalent to `Authorize(Cache(Service))`? Explain the remaining authority, revocation, timing, and side-channel differences.

### Exercise 3

Diagnose a design where every Repository opens its own transaction and Unit of Work calls each repository's `commit`. State violated invariants and propose one role binding.

### Exercise 4

Compare `Logging(Retry(Service))` with `Retry(Logging(Service))`. Define logical-operation and attempt telemetry, error behavior, trace identifiers, and which composition you would choose for production observability.

### Exercise 5

An unfamiliar medical platform composes authorization, cache, retry, circuit breaker, audit, and asynchronous notification around patient-record access. Produce a composition review covering role bindings, order, hard invariants, lifetime, failure paths, tests, and simplifications.

## Answers to the Exercises

### Answer 1

Factory constructing Strategy is stringing: construction output connects otherwise distinct responsibilities. Mediator subscribing as Observer is overlapping and role fusion when the same participant owns coordination and receives change notification. Adapter serving as a selected Strategy is also role fusion: one participant satisfies translation and algorithm/provider-selection roles. Facade calling independent subsystem services is stringing unless the Facade also fuses roles from those services; ordinary delegation alone does not.

### Answer 2

Including user identity prevents the demonstrated cross-user value collision, but the orders are not equivalent. An outer cache can still return a value without executing current authorization, so revoked access, changed roles, tenant policy, or contextual checks may be bypassed until invalidation. It also learns/cache-probes user-resource relationships before authorization and may expose timing side channels. Authorization outermost evaluates current policy before any hit, though the cache key still needs tenant, classification, version, and policy context where relevant.

Therefore user-aware keys mitigate one bug but do not replace explicit authority-order and revocation contracts. Tests must include revocation after fill, tenant separation, policy change, missing audit, and timing observations.

### Answer 3

The design has multiple transaction authorities, no atomic all-repository commit, and likely multiple identity maps. An object loaded through two repositories can have duplicate in-memory identities; one repository can commit while another fails. Unit of Work is merely coordinating commits after ownership has already fragmented.

Bind every repository in one business operation to a single Unit of Work. The unit owns one transaction/session and identity map, creates or supplies repositories using them, tracks changes, and performs one commit or rollback. Repositories query and stage changes but do not commit independently. Integration tests cover cross-repository atomicity, duplicate identity, rollback, nested use, and cleanup.

### Answer 4

`Logging(Retry(Service))` logs one outer logical start and final result; attempt details are invisible unless Retry emits them. `Retry(Logging(Service))` logs every attempt but can make three attempts look like three independent user operations and may omit one final logical outcome.

A production design usually models both explicitly: an outer operation span owns deadline, operation ID, final status, and user-visible latency; each inner attempt gets an attempt number, remaining budget, dependency timing, and error linked to the same trace. Sensitive data and exception policy are consistent. This can be implemented by two deliberate observation layers, not a generic logger stacked accidentally. Choose order from the required telemetry semantics and test retry exhaustion, cancellation, and successful later attempts.

### Answer 5

Bind a request coordinator to patient, tenant, purpose-of-use, deadline, trace, and current authorization context. Place authorization before cache access and again where policy requires use-time enforcement. Cache only explicitly cacheable record views with tenant/patient/version/classification keys and revocation/invalidation policy. Audit every attempted and successful access independently of cache hits; audit failure must follow a declared safety/compliance policy.

Retry only classified transient reads within the caller deadline and stable request identity. Circuit Breaker counts defined dependency outcomes and must not suppress required local authorization or audit. Async notification receives a minimal durable event after the authoritative outcome; it must not retain request sessions, credentials, or mutable patient objects.

Hard invariants include no cross-patient/tenant disclosure, current purpose-based authorization, complete tamper-evident required audit, bounded deadline/attempt/resource use, and no notification before a failed read. Trace cache hit/miss, authorization decision, each attempt, breaker state, final result, and event publication under one correlation identity without leaking protected content.

Test cache fill then revocation, tenant collision, stale version, dependency timeout and ambiguous response, retry exhaustion, breaker open/recovery, audit sink failure, cancellation, notification duplication, shutdown, and privacy redaction. Simplify by avoiding retry around cache hits, keeping one deadline/attempt owner, removing duplicated framework middleware, and using direct notification when only one mandatory ordered consumer exists. No composition ships until the end-to-end security and safety invariants pass, regardless of isolated pattern tests.
