---
module_id: SEPAT-052
program: Software Engineering: Patterns
level: 2
module_number: 52
title: Domain Model
status: complete
last_verified: 2026-08-28
---

# Domain Model

## One-Page Review

### Governing question

When does business complexity justify a behaviorally rich Domain Model, and how can its language, identity, values, aggregate boundaries, invariants, persistence, concurrency, events, and evolution remain correct under real operational constraints?

### Essential definitions

- A **Domain Model** is an object model of domain concepts that incorporates both behavior and data.
- A **domain** is the activity and knowledge area the software serves; a **model** is a deliberately selective system of concepts and rules used to reason about it.
- A **bounded context** is a boundary within which model terms and rules have a particular, consistent meaning.
- An **entity** is distinguished by continuity of identity, even while its attributes change.
- A **value object** is defined by its attributes, is compared by value, and is preferably immutable.
- An **aggregate** is a consistency boundary containing entities and values; its **aggregate root** is the sole external mutation gateway.
- An **invariant** is a proposition that must hold for every externally observable valid aggregate state.
- A **domain service** owns a stateless domain operation that does not naturally belong to one entity or value.
- A **repository** presents aggregate persistence through a collection-like domain interface while hiding storage mechanics.
- A **domain event** records a domain-significant fact that has occurred; it is not the same as a transport message.

### Central model, mechanism, or theorem

For valid aggregate state $a$, command $c$, and explicit decision context $x$, a root implements a partial transition

$$
\delta:A_{\mathrm{valid}}\times C\times X
\rightarrow (A_{\mathrm{valid}}\times E^*)\;\cup\;R,
$$

where $E^*$ is a finite sequence of domain events and $R$ is a typed rejection. If invariant $I(a)$ holds before every public transition, construction admits only valid states, and each successful transition preserves $I$, then all states reachable through that boundary satisfy $I$. This is a conditional inductive argument, not proof that requirements, persistence mappings, concurrency control, or distributed effects are correct.

### Critical invariants

- Code terms, scenarios, rules, and team language agree within the named bounded context.
- Entity identity and value equality are explicit; mutable attributes do not accidentally redefine identity.
- Only the root exposes aggregate mutation, and the boundary contains exactly the rules requiring immediate consistency.
- Factories, reconstitution, and every successful command preserve aggregate invariants; failed commands expose no partial mutation.
- Decisions use explicit, captured time, policy, exchange-rate, authorization, and other external facts rather than hidden ambient state.
- Repositories and mappers preserve identity/version and cannot silently bypass validation or publish half-formed objects.
- Concurrent writes use transaction isolation, locks, or an expected-version predicate matched to the invariant.
- Cross-aggregate processes use explicit workflow, idempotency, events/outbox, and compensation; in-memory references do not create a global transaction.
- Persistence, API serialization, migration, observability, and testing do not leak infrastructure concerns into domain rules or expose unrestricted setters.

### Common failures

Common failures include modeling tables instead of language, anemic data bags plus giant services, putting network/database calls in entities, aggregates equal to entire object graphs, aggregates too small to protect a rule, public setters or ORM rehydration that bypass invariants, identity based on mutable fields, primitive obsession, hidden wall-clock or global configuration, one transaction across many aggregates, stale reads without version checks, publishing events before commit, treating eventual consistency as no consistency, exposing entities directly as API schemas, lazy-load surprises, equality/hash mutation, universal base entities, and assuming unit tests prove stakeholder or distributed-system correctness.

### Compact example

An `Order` root accepts positive lines only while draft, requires a nonempty order before confirmation, and checks the caller's expected version. Adding a two-unit line changes the total to 3000 cents and version to 1; confirmation emits `order-confirmed:O-7:3000` and advances version to 2; a later line addition is rejected without mutation.

### Connections

[SEPAT-051](051-transaction-script.md) is the simpler procedural alternative; [SEPAT-053](../ROADMAP.md) introduces Table Module. Domain Model connects to [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md), [Database Engineering](../../18-database-engineering/ROADMAP.md), and [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md).

## Governing Question

When does a domain contain enough interacting rules, state transitions, and conceptual depth to justify a Domain Model, and what boundaries and evidence make such a model trustworthy rather than merely elaborate?

A Domain Model is neither a diagram of database nouns nor a folder named `domain`. It is executable domain reasoning: concepts carry the behavior that keeps their states meaningful, while application and infrastructure layers coordinate use cases and technical effects around them.

## Why This Matters

Straightforward data entry can be expressed clearly by Transaction Scripts. As rules accumulate, however, scripts often repeat eligibility checks, pricing calculations, lifecycle transitions, and identity assumptions. Their copies diverge across API handlers, jobs, imports, and administrative tools. A Domain Model gives those rules named owners and composes them through explicit concepts.

That benefit has costs. Object-relational mapping becomes less direct; aggregate boundaries constrain transactions; sophisticated abstractions can hide simple workflows; and a model can encode a persuasive misunderstanding of the real domain. The pattern is therefore an economic and epistemic choice, not a default badge of architectural maturity.

In consequential systems, the distinction matters more. A clinically elegant dosage model with the wrong units is dangerous. A financially correct aggregate running on inadequate isolation can still lose money. Correct source-level transitions are only one layer of evidence among domain validation, persistence, concurrency, security, operations, and human review.

## Prerequisites and Retrieval

You should understand objects and encapsulation, identity and equality, application/service layering, transactions and optimistic concurrency, event delivery, and basic logic. Retrieve these facts:

1. An abstraction suppresses detail to support a purpose; no model represents the entire domain.
2. Encapsulation protects a protocol of valid state transitions, not merely private fields.
3. Database atomicity and source-level method execution are different boundaries.
4. Equality by stable identity differs from equality by all constituent values.
5. A successful local commit does not imply a broker publish or downstream effect succeeded exactly once.
6. A test establishes behavior only over its assumptions, cases, environment, and oracle.
7. Authorization answers whether a particular actor may perform a particular action on a particular resource in the current context.

## Learning Objectives

After completing this module, you should be able to:

- decide whether Domain Model or Transaction Script better fits a problem's complexity and change pattern;
- develop model language from scenarios, rules, contradictions, and domain-expert feedback;
- distinguish entities, value objects, aggregates, roots, domain services, repositories, factories, and events;
- define aggregate boundaries from true immediate-consistency invariants rather than navigation convenience;
- specify transitions and prove invariant preservation under explicit assumptions;
- integrate persistence without allowing mappers, ORMs, serializers, or migrations to bypass model validity;
- design versioning, transaction, event, and workflow semantics for concurrent and distributed execution;
- test examples, properties, histories, mappings, races, and operational recovery with appropriate evidence;
- evolve a model incrementally and detect semantic drift, over-modeling, and anemic designs;
- review high-stakes models without confusing code validation with external domain approval.

## Core Exposition

### Model a purpose, not reality in full

A domain is richer than any software representation. A shipping system may model parcel weight and destination but not cardboard chemistry. A clinical system may distinguish prescribed, dispensed, and administered medication because collapsing them would make safety questions unanswerable.

State the model's purpose, stakeholders, decisions, jurisdiction, time horizon, and excluded concerns. The same real-world thing can have different models in sales, fulfillment, accounting, and support. Trying to impose one enterprise-wide class meaning usually produces vague fields and conditionals rather than shared understanding.

### Establish a bounded language

Collect concrete scenarios: commands, policies, exceptional cases, timelines, documents, reports, and disagreements. Replace generic technical verbs such as `process` with domain verbs such as `reserve`, `authorize`, `dispense`, or `settle`. Ask what each term means, when it becomes true, who may assert it, and what would falsify it.

Within a bounded context, source names, tests, telemetry, events, and conversations should reinforce the same distinctions. Across contexts, translate deliberately. A sales `Customer`, billing `Account`, and support `Contact` may share identifiers without being one model object.

### Choose the pattern by rule complexity

Domain Model earns its cost when behavior is rich, interacting, reused across use cases, and expected to evolve: eligibility plus lifecycle plus calculation plus policy, for example. It is less compelling for stable CRUD, simple data transformation, or a few independent operations. In those cases, Transaction Script or Table Module may remain clearer.

Do not decide by table count, team prestige, or framework fashion. Compare expected change: if a rule changes, how many use cases must change together? Can one concept own the rule? Does object collaboration clarify a state machine, or merely scatter a five-line procedure?

### Give entities stable identity

An entity remains the same conceptual individual across attribute changes. Its identity must be stable within the bounded context and scoped explicitly: tenant plus local identifier may be required. Database surrogate keys can implement identity, but database row identity and domain identity are not automatically identical.

Define equality and hash behavior deliberately. Hashing a mutable email or display name can make an entity unfindable in a set after mutation. Two loaded instances representing the same identity must not create conflicting changes silently; identity maps or unit-of-work tracking can help, but concurrency still requires storage-level control.

### Use value objects to make invalid combinations difficult

A value object expresses a descriptive concept such as `Money(1500, "SEK")`, date interval, geographic coordinate, dosage, or policy version. Its equality uses all semantically relevant attributes. Prefer immutability: transformation produces a new value, so aliases cannot mutate each other's meaning.

Values remove primitive ambiguity and centralize units, ranges, rounding, normalization, and operations. They must still state precision and context. `Money` cannot add different currencies without a conversion policy; a `LocalDateTime` without zone/offset may be insufficient for an instant.

### Place behavior with the concept that knows the rule

An entity should expose intention-revealing operations, not unrestricted setters: `order.confirm(quote, actor)` rather than `order.status = "confirmed"`. The operation checks its preconditions, computes changes, and records facts as one semantic transition.

This does not mean every calculation belongs on an entity. A pure value may own arithmetic; a policy object may own replaceable strategy; a domain service may express a stateless operation spanning concepts. The test is conceptual ownership, not a rule that all code be methods.

### Keep the application layer thin but real

An application service authenticates/authorizes context, controls transaction and repository usage, obtains external facts, calls domain behavior, persists results, and arranges durable publication. It owns use-case coordination and technical policy, not the business rule itself.

“Thin” does not mean trivial. Deadlines, idempotency, retries, locks, outbox insertion, result mapping, and workflow coordination are substantial responsibilities. They should remain explicit so domain objects do not call brokers, clocks, HTTP clients, or database sessions.

### Define an aggregate from a consistency rule

An aggregate is not every object reachable from a root. Start with an invariant that must be true immediately after a command. Put only the entities and values required to decide and enforce that invariant inside one boundary. Permit external mutation only through the root.

For an order, line quantities and order total may require immediate consistency. Customer credit, warehouse stock, and carrier capacity may be separate aggregates or services with reservations and workflows. Refer to other aggregates by identity unless a read model is being used; a language-level object reference does not grant atomic consistency.

Large aggregates create contention, load too much state, and couple unrelated lifecycles. Tiny aggregates cannot protect multi-object invariants. Boundary selection is empirical modeling work: state the invariant and competing commands, then test the proposed transaction boundary.

### Preserve invariants by construction and transition

Factories should create only valid initial states. Every public successful method must leave a valid state; rejected operations should not leak partial mutation. Collections exposed from the root should be immutable views or copies, and child entities should not be independently saved or modified from outside.

The familiar induction argument is conditional. A valid base state plus preservation by every transition implies reachable validity only if every state enters through those paths. ORM materialization, reflection, deserialization, database repair, migration, and direct SQL can violate the premise. Govern those paths and validate at boundaries.

### Make decision context explicit

Domain decisions often depend on time, actor authority, jurisdiction, policy version, exchange rate, laboratory result, or inventory promise. Hidden calls to a global clock or configuration make a transition irreproducible and can evaluate different parts of one decision against different facts.

Capture authoritative context once, validate provenance and expiry, and pass a value into the transition. Record the versions needed to explain or replay the decision. Do not confuse deterministic replay with current validity: a past policy decision may be reproducible yet no longer allowed today.

### Use domain services narrowly

A domain service is appropriate when an operation is genuinely a domain verb but no single entity or value owns it—for example, calculating a route between locations or converting money under a supplied rate. It should usually be stateless and expressed in domain terms.

A service named `OrderService` with every order rule and mutable entities underneath is often an anemic model. Conversely, forcing an external credit-network lookup into `Order` harms boundaries. Obtain external evidence in an application/infrastructure service, represent its result as a domain value, then let the model decide.

### Use factories and repositories at lifecycle boundaries

A factory encapsulates valid creation when construction spans rules or several objects. It returns a valid aggregate or typed rejection. Reconstitution from storage is distinct: it reconstructs a previously valid state and must detect corrupt or incompatible records rather than silently normalizing history.

A repository provides operations such as obtain root by identity and save under an expected version. It should not expose unrestricted query language or child-table persistence as domain operations. Complex reporting belongs in dedicated read models; forcing all queries through aggregates causes needless loading and distorted models.

### Map persistence without surrendering the model

Persistence ignorance means domain rules do not depend on database APIs; it does not mean ignoring storage semantics. A mapper must preserve identity, value precision, ordering where semantic, version, optionality, and event state. Database constraints should back critical representable invariants because other writers and operational tools may bypass object code.

ORM conveniences create hazards: public no-argument construction, mutable setters, proxy subclasses, lazy loading, cascade writes, and equality before identifier assignment. Configure mappings explicitly, keep domain APIs restrictive, test the real mapper, and inspect generated queries. Persistence models and domain objects may be separate when their shapes or lifecycles diverge materially.

### Control concurrent transitions

Two individually valid transitions can combine incorrectly if both decide from stale state. Store an aggregate version and update with a predicate such as `WHERE id = ? AND version = ?`; zero affected rows is a typed conflict. Reload and reconsider rather than blindly reapplying a now-invalid decision.

Optimistic concurrency suits low-conflict aggregates. Pessimistic locks or stronger isolation may suit hot resources, but lock scope and deadlocks require design. A version check protects one aggregate row/version; it does not automatically protect uniqueness, predicates, or invariants spanning multiple roots. Use database constraints, locks, or serializable transactions for the actual anomaly.

### Record events after successful decisions

A domain event is an immutable past-tense fact such as `OrderConfirmed`, with stable identity, aggregate identity/version, occurred time, schema/version, and domain-relevant data. It communicates that a transition happened and can drive local reactions or cross-boundary workflows.

Do not publish directly from an entity. Collect pending events, commit aggregate state and an outbox record atomically, then relay. Consumers must tolerate duplicates, delayed delivery, reordering according to the declared key, schema evolution, and poison messages. The event is not proof every downstream effect occurred.

### Coordinate across aggregates explicitly

Rules within one aggregate are usually enforced synchronously. Cross-aggregate business processes require a workflow/saga, reservations, idempotency, timeouts, compensation, and observable intermediate states. “Eventually consistent” must name the convergence rule, maximum acceptable delay, conflict policy, and operational recovery.

If the domain truly requires immediate atomic consistency between two concepts, reconsider their boundary or use a transaction mechanism that can enforce the invariant. Do not pretend asynchronous messaging satisfies a rule that forbids any observable inconsistency.

### Separate write model, read model, and API contract

An aggregate is optimized to protect writes, not to answer every screen or analytic query. Projection/read models can join and denormalize data with stated freshness. Their lag must be visible where users could act on stale information.

Do not serialize domain entities directly as public API resources. That leaks internal structure, allows over-posting, couples versioning, triggers lazy loads, and exposes fields without disclosure policy. Map commands and results through explicit transport schemas.

### Treat authorization as an action invariant

Authentication context is external, but authorization may depend on domain state: only an assigned clinician may sign this order before a cutoff, for example. The application establishes trusted actor/context; a domain policy or aggregate evaluates the action-specific rule against the governed state.

Recheck security-sensitive facts under the same concurrency boundary as mutation when necessary. Tenant identity must constrain repository queries and identifiers. Domain encapsulation is not a security boundary if another code path or database credential can write around it.

### Model time and history deliberately

Distinguish effective time (when a fact is true in the domain), recording time (when the system learned it), and processing time. A mutable “current status” may be insufficient for audits, retroactive corrections, temporal rules, or disputed facts.

Choose snapshots, append-only events, temporal tables, or explicit history entities based on queries and evidence needs. Event sourcing is a different persistence model, not a prerequisite for Domain Model; it adds replay, schema, ordering, privacy, and operational burdens.

### Test claims at several boundaries

Use example tests for named scenarios, property-based tests for algebraic laws and invariants, model-based tests for transition sequences, and mutation tests to challenge the test oracle. Test equality, boundaries, units, time, rejected commands, and event content.

Use integration tests for mappings, constraints, transaction isolation, version conflicts, and outbox atomicity; contract tests for external evidence; concurrency tests with controlled interleavings; and operational tests for crash/retry/rebuild. Have domain experts review scenarios and terminology. No automated suite proves the model matches the world universally.

### Evolve through discovery

Models change as teams learn. Treat disagreement, awkward naming, repeated conditionals, large transactions, and hard-to-express rules as evidence. Refactor one conceptual boundary at a time, preserve external behavior where intended, migrate data explicitly, version contracts/events, and use characterization tests before risky changes.

Avoid a “big DDD rewrite.” Extract a value object or aggregate from the most costly duplicated rule, leaving Transaction Scripts as application coordinators. Keep useful seams; delete abstractions that no longer express domain distinctions.

## Definitions and Notation

Let an aggregate state space be $A$, commands $C$, explicit contexts $X$, events $E$, and typed rejections $R$. Let predicate $I:A\to\{\mathrm{true},\mathrm{false}\}$ define validity, so

$$
A_{\mathrm{valid}}=\{a\in A\mid I(a)\}.
$$

A command transition is partial because not every command is permitted in every state:

$$
\delta(a,c,x)=
\begin{cases}
(a',\langle e_1,\ldots,e_n\rangle),&\text{if preconditions hold and }I(a'),\\
r\in R,&\text{otherwise.}
\end{cases}
$$

Let $v\in\mathbb{N}$ be aggregate version. A successful persisted transition requires expected version $\hat v=v$, writes $v'=v+1$, and atomically stores its event intents. A mismatch is conflict, not permission to overwrite.

For an order with line quantities $q_i\in\mathbb{Z}_{>0}$ and unit prices $p_i\in\mathbb{Z}_{\ge0}$, subtotal in one currency is

$$
T=\sum_{i=1}^{n}q_i p_i.
$$

An illustrative invariant is: every line has positive quantity and nonnegative price; draft orders may change; confirmed orders have $n>0$; version never decreases. Real pricing also needs currency, discounts, tax jurisdiction, rounding, and policy versions.

## Mechanisms, Invariants, or Proof Structure

### Domain Model design procedure

1. Name the bounded context, decisions, stakeholders, and model exclusions.
2. Gather concrete scenarios and contradictions; establish precise domain terms and verbs.
3. Identify entity identities, immutable values, lifecycle transitions, rules, and external facts.
4. Express invariants and competing commands before drawing aggregate boundaries.
5. Assign behavior to entities, values, policies, or narrow domain services by conceptual ownership.
6. Define factories, repositories, expected versions, database constraints, and reconstitution validation.
7. Separate application coordination, infrastructure effects, read projections, and transport schemas.
8. Define event/outbox, cross-aggregate workflow, idempotency, timeout, compensation, and recovery semantics.
9. Test transition properties, mappings, concurrency schedules, crash points, terminology, and real stakeholder cases.
10. Revisit the model when language, rules, performance, or operational evidence contradicts it.

### Executable finite model

The executable model demonstrates a single serialized `Order` aggregate. It checks positive line inputs, draft-only changes, nonempty confirmation, and expected versions; emits one fact after confirmation; and rejects a later change without mutation. It does not implement persistence, parallel threads, money/currency policy, authorization, outbox durability, or external domain validation.

<!-- bijux-verify: {"id":"domain-model-order","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"add=added total=3000 version=1\nconfirm=order-confirmed:O-7:3000 status=confirmed version=2\nlate_change=not-draft total=3000 version=2\n","stderr":""}} -->
```python
class Order:
    def __init__(self, order_id):
        if not order_id:
            raise ValueError("order-id-required")
        self.order_id = order_id
        self.status = "draft"
        self.lines = []
        self.version = 0
        self.events = []

    def total_cents(self):
        return sum(quantity * price for _, quantity, price in self.lines)

    def add_line(self, sku, quantity, unit_price_cents, expected_version):
        if expected_version != self.version:
            return "version-conflict"
        if self.status != "draft":
            return "not-draft"
        if not sku or quantity <= 0 or unit_price_cents < 0:
            return "invalid-line"
        self.lines.append((sku, quantity, unit_price_cents))
        self.version += 1
        return "added"

    def confirm(self, expected_version):
        if expected_version != self.version:
            return "version-conflict"
        if self.status != "draft":
            return "not-draft"
        if not self.lines:
            return "empty-order"
        self.status = "confirmed"
        self.version += 1
        event = f"order-confirmed:{self.order_id}:{self.total_cents()}"
        self.events.append(event)
        return event


order = Order("O-7")
result = order.add_line("book", 2, 1500, 0)
print(f"add={result} total={order.total_cents()} version={order.version}")
event = order.confirm(1)
print(f"confirm={event} status={order.status} version={order.version}")
result = order.add_line("pen", 1, 200, 2)
print(f"late_change={result} total={order.total_cents()} version={order.version}")
```

### Invariant argument

This is a finite proof for transitions reachable through the shown API.

**Base case.** Construction yields draft status, empty lines, version zero, and no events. Every line predicate is vacuously true; version is nonnegative; confirmation constraints do not yet apply.

**Add-line case.** A successful addition requires matching version, draft status, nonempty SKU, $q>0$, and $p\ge0$. Existing valid lines remain unchanged, the new line satisfies the line predicate, status remains draft, and version increases by one. Rejection mutates nothing.

**Confirm case.** Success requires matching version, draft status, and at least one valid line. Lines remain unchanged, status becomes confirmed, version increases by one, and the event total equals the post-state total. Rejection mutates nothing.

**Closure.** By induction over finite successful call sequences, the stated invariant holds for every reachable state. The proof assumes no mutation of public fields/lists, no mapper bypass, no integer overflow, serialized calls, and faithful Python execution. Those assumptions fail in a production design with public mutable fields, so encapsulation and persistence/concurrency mechanisms remain required.

### Evidence classification

The verifier's execution is empirical evidence for one implementation trace. Arithmetic and transition claims can be independently recomputed; the closure argument can be reviewed line by line; boundary cases require adversarial analysis. None of these establishes that “order,” confirmation policy, price meaning, or aggregate boundary matches a real organization without named domain review.

## Alternatives and Trade-Offs

| Approach | Best fit | Strength | Principal cost or risk |
|---|---|---|---|
| Transaction Script | Few simple use cases | Visible procedural flow | Rules duplicate as interactions grow |
| Table Module | Logic organized around record sets/table data | Efficient set-oriented operations | Weaker expression of individual lifecycles |
| Domain Model | Rich interacting rules and state | Concepts own behavior and invariants | Mapping, learning, and boundary complexity |
| Functional core | Pure transformations over explicit values | Determinism and compositional tests | Identity/lifecycle orchestration remains external |
| Active Record | Domain object closely aligned to one row | Low ceremony for CRUD | Persistence coupling and weak aggregate fit |
| Event-sourced model | History/replay is a first-class requirement | Explicit event history and temporal reconstruction | Schema evolution, ordering, privacy, and operations |
| Rules/decision engine | Large externally managed decision tables | Auditable configurable decisions | Split model ownership and difficult interaction/state |

These approaches compose. An application can use Transaction Scripts for administrative CRUD, a Domain Model for pricing and fulfillment, SQL projections for reads, and a workflow for cross-service processes. Uniform architecture is less important than explicit boundaries and consistent guarantees.

## Failure Modes and Misconceptions

- **“Classes named after nouns are a Domain Model.”** Without owned behavior and meaningful transitions, they are data structures.
- **“All services are anemic.”** Application and infrastructure services are necessary; the smell is domain rules evacuated into generic services.
- **“Every rule belongs in an entity.”** Values, policies, domain services, constraints, and workflows may be better owners.
- **“Aggregate means composition.”** Lifecycle ownership and navigation do not by themselves determine immediate consistency.
- **“Load the whole graph and commit once.”** This enlarges contention and does not create distributed atomicity.
- **“One aggregate per table.”** Tables are storage design; aggregates are invariant/transaction boundaries.
- **“Private fields guarantee invariants.”** Deserializers, ORMs, reflection, migrations, direct SQL, leaked collections, and concurrency can bypass methods.
- **“Optimistic locking solves concurrency.”** It detects version conflicts only at its governed boundary; predicate and cross-root anomalies need more.
- **“Persistence ignorance means storage does not matter.”** Isolation, precision, constraints, query shape, and mapping fidelity remain correctness concerns.
- **“Events make everything eventually consistent.”** A system needs convergence, ordering, duplicate, timeout, compensation, and recovery policy.
- **“A domain event is a broker message.”** One is a modeled fact; the other is a delivery representation with operational contracts.
- **“Repositories should support arbitrary queries.”** Aggregate repositories protect lifecycle; reporting projections serve flexible reads.
- **“Expose entities through the API to avoid mapping.”** This couples contracts, enables over-posting, and leaks internal structure/security decisions.
- **“Event sourcing is required for DDD.”** It is one persistence option with substantial additional obligations.
- **“More abstractions mean a richer model.”** Richness is explanatory and behavioral power, not class count.
- **“Passing tests proves the model.”** Tests can support code claims; stakeholder, legal, clinical, or scientific claims require independent evidence and named review.

## Worked Examples

### Example 1

**Situation.** A checkout model represents prices as decimal numbers and adds `10 SEK` to `5 EUR`.

**Reasoning.** Numeric addition is executable but semantically invalid because currency is part of the value. Define immutable `Money(amount_minor, currency)`; addition requires equal currency, while conversion requires a supplied rate, rate source/version, time, and rounding policy. `Money(1500, "SEK")` equals another value with the same attributes, not one with a different currency.

**Conclusion.** A value object prevents invalid primitive combinations and makes external policy explicit.

### Example 2

**Situation.** A user changes email, and a set keyed by the user's hash can no longer find the object.

**Reasoning.** Email was used as entity identity/hash even though it is mutable. If the context recognizes a stable user ID, equality and hashing should use that tenant-scoped identity. Email may be a separately validated value with a uniqueness constraint; changing it does not create a different user.

**Conclusion.** Entity identity must follow conceptual continuity and remain stable under attribute change.

### Example 3

**Situation.** A `Customer` aggregate contains every order ever placed so code can navigate `customer.orders`.

**Reasoning.** Confirming one order now loads or versions an unbounded graph and conflicts with unrelated orders. The immediate invariant likely belongs to one `Order`; customer eligibility can be supplied as versioned evidence or coordinated by workflow. Reference orders/customer by identity and query a projection for history.

**Conclusion.** Navigation convenience produced an oversized aggregate; invariant scope should determine the boundary.

### Example 4

**Situation.** `OrderLine` rows are saved independently, while `Order.total` must always equal their sum.

**Reasoning.** Two writers can change lines and total separately, exposing mismatch. If that equality is an immediate business invariant, lines and computed total belong under an `Order` root; external code requests `change_quantity`, and total is derived/recomputed inside the transition. Mapping and transaction commit the governed state together.

**Conclusion.** An undersized boundary cannot enforce a multi-object invariant.

### Example 5

**Situation.** `Order` exposes getters/setters; `OrderService`, `AdminOrderService`, and an import job each implement confirmation differently.

**Reasoning.** The model pays object/mapping costs while rules live in procedural copies. Move the state transition and stable invariant to `Order.confirm(context)`. Keep authentication, repository, transaction, and outbox coordination in application services. Characterization tests reveal behavior differences that require stakeholder resolution, not blind consolidation.

**Conclusion.** Behavioral ownership removes anemia, but migration must reconcile contradictory rules explicitly.

### Example 6

**Situation.** An invoice in SEK must evaluate a EUR credit limit using a market quote.

**Reasoning.** The entity should not call a rate API. The application obtains and validates a `RateQuote(pair, rate, observed_at, expires_at, source, version)`. A pure domain service converts under declared rounding; the aggregate evaluates the resulting credit evidence and records the quote version needed for audit.

**Conclusion.** External fact acquisition stays outside while domain decision semantics remain explicit and reproducible.

### Example 7

**Situation.** An ORM creates an order with status `confirmed` and zero lines by setting fields after a no-argument constructor.

**Reasoning.** The persistence path bypassed the constructor and public transition. Configure a mapper/reconstitution path that requires all fields, validates schema and invariant, preserves version, and fails/quarantines corrupt records. Add database constraints where representable and migration validation for historical data.

**Conclusion.** Source encapsulation is conditional on every construction and persistence path preserving validity.

### Example 8

**Situation.** Two workers load order version 7; one cancels it while another confirms it. Both local method calls succeed.

**Reasoning.** Saving with `WHERE id = O AND version = 7` permits only one update to version 8. The loser receives conflict, reloads, and reevaluates; it must not overwrite or blindly retry the stale decision. If a predicate outside the order controls the action, versioning this root alone may be insufficient.

**Conclusion.** In-memory invariant preservation needs a storage concurrency mechanism aligned with the decision boundary.

### Example 9

**Situation.** Order confirmation must reserve inventory and authorize payment in separate services.

**Reasoning.** Putting remote calls inside `Order.confirm` hides latency/failure and cannot make three systems atomic. A workflow records intent, requests idempotent reservations, handles duplicate/delayed responses, times out, compensates releases, and confirms only under the declared policy. An outbox atomically connects each local state transition to message intent.

**Conclusion.** Cross-aggregate/service consistency belongs to an explicit workflow, not an oversized in-memory model.

### Example 10

**Situation.** A medication model allows a dose when `daily_total + dose <= limit`.

**Reasoning.** Code review confirms arithmetic only after defining units, route, patient mass, overlapping time window, administered versus prescribed doses, renal adjustment, source authority, clock, late-arriving records, and concurrent administrations. Unit/property/integration tests cover boundaries and races; clinicians and safety reviewers must approve domain assumptions with named records. Denial, override authority, reason, and audit are modeled outcomes.

**Conclusion.** High-stakes Domain Model correctness requires multidisciplinary evidence; an elegant invariant is unsafe when its terms omit reality.

## Cross-Program Connections

- [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) develops modeling language, modularity, and bounded-context practice in greater depth.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) supplies constraints, mapping, indexing, isolation, locking, and temporal-storage mechanisms behind aggregate guarantees.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) explains partial failure, ordering, idempotency, consensus limits, sagas, and eventual convergence.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) treats explicit command/result contracts, versioning, authorization, and transport boundaries.
- [Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) provides property, model-based, mutation, integration, and concurrency evidence for transitions and invariants.
- [SEPAT-051](051-transaction-script.md) provides the simpler procedural baseline; [SEPAT-053](../ROADMAP.md) considers Table Module for business logic organized around tabular data.

## References

1. Martin Fowler, [“Domain Model”](https://martinfowler.com/eaaCatalog/domainModel.html), *Patterns of Enterprise Application Architecture* catalog, 2003. Defines the pattern as an object model incorporating behavior and data.
2. Martin Fowler, *Patterns of Enterprise Application Architecture*, Addison-Wesley, 2002. See the domain-logic, data-mapping, repository, unit-of-work, identity-map, and service-layer patterns.
3. Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software*, Addison-Wesley, 2004. Foundational treatment of model-driven design, language, entities, values, services, aggregates, factories, and repositories.
4. Eric Evans, [*Domain-Driven Design Reference*](https://www.domainlanguage.com/ddd/reference/), 2015 reference edition. Concise licensed summaries of DDD definitions and patterns.
5. Martin Fowler, [“Anemic Domain Model”](https://martinfowler.com/bliki/AnemicDomainModel.html), 2003. Explains why data-only domain objects retain mapping cost while losing behavioral benefit.
6. Vaughn Vernon, [“Effective Aggregate Design”](https://www.dddcommunity.org/library/vernon_2011/), three-part series, 2011–2012. Develops aggregate boundaries around consistency constraints and discusses large-cluster pitfalls.
7. David L. Parnas, [“On the Criteria To Be Used in Decomposing Systems into Modules”](https://doi.org/10.1145/361598.361623), *Communications of the ACM* 15(12), 1972. Primary foundation for information-hiding decomposition.
8. Barbara Liskov and Jeannette M. Wing, [“A Behavioral Notion of Subtyping”](https://doi.org/10.1145/197320.197383), *ACM TOPLAS* 16(6), 1994. Formal basis for reasoning about behavioral contracts and substitutability.
9. Martin Kleppmann, *Designing Data-Intensive Applications*, O’Reilly, 2017. Durable treatment of transactions, isolation, replication, streams, and distributed consistency limitations.
10. PostgreSQL Global Development Group, [“Transaction Isolation”](https://www.postgresql.org/docs/current/transaction-iso.html), current documentation accessed 2026-08-28. Concrete official semantics and anomalies for a production relational system; other databases differ.

## Exercises

### Exercise 1

For the executable `Order`, trace these calls from a fresh instance: `confirm(0)`, `add_line("x", 0, 100, 0)`, `add_line("x", 2, 100, 0)`, `confirm(0)`, and `confirm(1)`. Give each result and final state, and identify which invariant each rejection protects.

### Exercise 2

Design an aggregate for a lending system where a loan contains copies, a member borrows one copy, no copy can have two active loans, and a member's maximum-active-loan policy can change. State identities, values, immediate invariants, aggregate boundary, command transition, external context, concurrency mechanism, and events. Do not assume the whole member history belongs in one aggregate.

### Exercise 3

A service has five short Transaction Scripts over invoices. Two share tax calculation; one handles approval; requirements change twice per year. Diagnose whether to retain Transaction Script, introduce values/policies, or adopt a full invoice Domain Model. State the evidence that would change your decision and an incremental implementation plan.

### Exercise 4

An anemic `Shipment` entity is exposed through a REST API, an ORM supplies public setters, and three services implement dispatch rules. Propose a migration that preserves availability and data compatibility while establishing behavioral ownership, restrictive APIs, mapping validation, version conflicts, outbox publication, and rollback/observability.

### Exercise 5

Transfer the pattern to a high-stakes infusion system. Propose a model for starting an infusion under prescription, patient, pump, time, and authorization constraints. Distinguish what can be proved or tested automatically from what requires clinical, regulatory, security, human-factors, and operational review. Include stale evidence, concurrent commands, override, audit, and fail-safe behavior.

## Answers to the Exercises

### Answer 1

`confirm(0)` returns `empty-order`; state remains draft, empty, version 0. The nonempty-confirmation invariant is protected. `add_line("x", 0, 100, 0)` returns `invalid-line`; positive quantity is protected and state remains unchanged. `add_line("x", 2, 100, 0)` returns `added`; total becomes 200 and version 1. `confirm(0)` returns `version-conflict`; stale-decision protection preserves state. `confirm(1)` returns `order-confirmed:<id>:200`; status becomes confirmed, version 2, lines remain one valid line, and one event is recorded. Version changed only for successful transitions.

### Answer 2

Use stable `CopyId`, `MemberId`, and `LoanId`; values include `LoanPeriod` and a versioned `EligibilityDecision` or policy evidence. A practical immediate boundary is one `CopyLoan` aggregate (or copy aggregate) whose invariant is at most one active loan for that copy. `borrow(member_id, period, eligibility, expected_version)` requires available state, unexpired trusted eligibility for the same member, and valid period, then creates active loan and emits `CopyBorrowed`. Saving uses an expected-version update plus a storage uniqueness/exclusion constraint on active copy loans.

The member maximum is a cross-copy predicate. A separate member eligibility/reservation aggregate or serialized lending-limit service must atomically claim capacity; a mere earlier count query is unsafe. A workflow coordinates capacity reservation with copy borrowing and compensates on failure. This keeps unbounded history outside the copy root while naming the true cross-aggregate invariant. `CopyReturned` and reservation released/expired events complete the process. Tests must exercise two simultaneous borrow attempts for one copy and for the last member slot.

### Answer 3

Retain scripts as application coordinators initially. Extract immutable `Money`, `TaxJurisdiction`, and a pure versioned `TaxPolicy` because shared tax semantics already have one conceptual owner. Model approval as an `Invoice` transition only if it has meaningful lifecycle rules or repeated use across scripts. Five short scripts and infrequent change alone do not justify a full collaborating object graph.

Collect evidence: duplication/defect history, rule interactions, conditional growth, stakeholders' language, concurrency needs, and expected variants. Characterize current results, introduce values/policy behind one script, migrate the other caller, compare readability and change locality, then extract an aggregate if approval/tax/payment state invariants cohere. Retain simple reporting/CRUD scripts. A rapid increase in interacting lifecycle rules favors the Domain Model; stable independent procedures favor the hybrid.

### Answer 4

First freeze and characterize each dispatch path, including contradictory behavior and actual data anomalies. Introduce explicit API command/result schemas so clients no longer bind directly to `Shipment`. Add a restrictive `Shipment.dispatch(context, expected_version)` transition and route one application service through it while old endpoints adapt to the same command. Reconcile rule differences with product/domain owners rather than choosing silently.

Configure a mapper/reconstitution constructor that reads existing schema, validates or quarantines invalid records, preserves stable identity/version, and stops exposing setters. Add conditional version updates and appropriate database constraints. In the same local transaction, persist state and an idempotent outbox event; relay afterward. Migrate callers one at a time with metrics for old/new path, outcome, conflict, invalid legacy state, and outbox lag. Use compatible reads/writes or an explicit data migration, feature-controlled routing, and a tested rollback that does not discard new-version writes. Remove direct entity serialization and setters only after all consumers and operational tools migrate.

### Answer 5

Model `InfusionOrder`/`InfusionSession` boundaries from explicit safety invariants, not device ownership. Inputs are versioned prescription, patient identity/weight/allergies/labs, medication concentration and units, pump capability/calibration, current authoritative time, assigned clinician authority, and policy version. `start(evidence, actor, expected_version)` either emits a typed denial/override-required outcome or transitions a prepared session to starting with an immutable decision record. Stale/discordant evidence fails closed according to approved policy; concurrent starts use version/constraint protection; device communication is a separate acknowledged workflow with timeout and safe cancellation. Overrides require scoped authority, reason, second review where policy requires, prominent feedback, and immutable audit.

Automated checks can verify units/ranges, state-transition closure under stated assumptions, version conflicts, duplicate commands, mapping fidelity, signatures/expiry, event/outbox atomicity, simulated device timeout, and selected hazard cases. They cannot establish appropriate clinical limits, complete contraindications, usability under alarm load, regulatory conformity, cybersecurity posture, pump physical behavior, or workflow safety. Those require named pharmacists/clinicians, safety and human-factors engineers, security specialists, regulatory review, device integration evidence, hazard analysis, usability studies, and operational drills. The system must distinguish “software rejected safely” from “therapy safely stopped”; a fail-safe design uses approved pump behavior and escalation rather than assuming a message changes the physical device.
