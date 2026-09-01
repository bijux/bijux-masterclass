---
module_id: API-031
program: API & Service Engineering
level: 1
module_number: 31
title: Transport, Application, and Domain Boundaries
status: complete
last_verified: 2026-09-01
---

# Transport, Application, and Domain Boundaries

## One-Page Review

### Governing question

How should a service divide HTTP transport mechanics, use-case orchestration, domain decisions, and infrastructure so that public semantics remain correct while frameworks, storage, and delivery mechanisms can change independently?

### Essential definitions

- A **transport adapter** parses and serializes protocol messages, applies protocol rules, and maps them to or from application-owned values.
- The **application layer** coordinates one use case: trusted context, transactions, domain calls, ports, and outcome handling.
- The **domain layer** owns business vocabulary, invariants, state transitions, and decisions independent of HTTP or persistence mechanisms.
- A **port** is an application-owned interface through which an adapter drives the application or the application requests an external capability.
- An **inbound adapter** translates an external stimulus into an application call; an **outbound adapter** implements an application-owned port toward storage or another service.
- A **boundary model** is a value designed for one crossing, such as a request DTO, application command, domain value, persistence record, or response DTO.
- **dependency direction** says source dependencies point toward stable policy rather than from policy toward replaceable mechanisms.

### Central model, mechanism, or theorem

Represent source dependencies by directed graph $G=(V,E)$ with layer rank $r(T)=0$, $r(A)=1$, $r(D)=2$ for transport, application, and domain. Policy-preserving dependencies satisfy $r(u)\le r(v)$ for every edge $u\rightarrow v$ among those layers: transport may depend on application, and application on domain, but domain must not depend on either. Outbound adapters depend on application-owned ports; runtime control may flow outward even while source dependency points inward.

### Critical invariants

Transport code owns HTTP parsing, negotiation, headers, and status serialization—not business truth. The application receives authenticated context separately from untrusted body fields. Domain code neither imports a web framework nor returns HTTP statuses. Persistence records never cross the public boundary. Mapping is explicit and rejects prohibited fields. Transactions surround the use case at an application/infrastructure seam. Domain outcomes remain typed until an adapter translates them. Logs preserve internal cause without exposing it. Every boundary can be tested through owned contracts, including negative and failure behavior.

### Common failures

Controllers containing business rules; domain entities annotated for JSON or ORM and returned directly; application services receiving raw requests; trusting tenant or actor IDs from bodies; repositories returning framework query objects; domain methods throwing HTTP exceptions; one generic model shared across request, domain, database, and response; hidden lazy loads during serialization; adapters deciding business retries; transactions per repository call; broad exception-to-`500` mapping; and abstractions added only to imitate a diagram.

### Compact example

An HTTP adapter parses `If-Match`, a JSON quantity, and authenticated principal, then creates `ChangeQuantity(order_id, quantity, expected_version, actor)`. The application loads through an `Orders` port, asks the aggregate to change, commits once, and returns `Changed(order, version)`. The adapter maps stale version to `412`, forbidden domain decision to the disclosure policy, and success to `200` with `ETag`. **Conclusion:** each boundary translates vocabulary and preserves ownership instead of forwarding framework objects.

### Connections

[Request and Response Modeling](024-request-and-response-modeling.md) defines direction-specific public models. [Reviewing a Contract for Ambiguity and Incompleteness](030-reviewing-a-contract-for-ambiguity-and-incompleteness.md) establishes the semantics adapters must preserve. [Request Parsing and Validation](../ROADMAP.md) next deepens the inbound pipeline, while later modules assign authentication, authorization, error, transaction, and concurrency responsibilities.

## Governing Question

Which responsibilities, types, dependency rules, translations, and tests keep a service endpoint faithful to its API contract without allowing HTTP, framework, or persistence concerns to own application and domain policy?

## Why This Matters

A service endpoint is a semantic crossing, not merely a function with a route annotation. External messages use HTTP concepts, serialized representations, public identifiers, and an adversarial trust model. The application executes a use case with identity, time, transaction, and dependency policy. The domain decides what states and transitions are valid. Storage and downstream services expose yet other failure and consistency models.

Collapsing these worlds can appear efficient. A controller binds JSON into an ORM entity, calls `save`, and returns the entity. Soon public fields mirror columns, authorization depends on client-supplied tenant data, lazy relationships trigger unbounded queries during serialization, database exceptions leak as `500`, and a framework upgrade changes public null behavior. Tests require a server and database even to evaluate a business rule.

Boundaries localize change and make trust visible. They do not require one class per line or a ceremonial architecture. A small service may implement an adapter and use case in two functions. The test is whether public protocol, orchestration, business policy, and mechanism have clear owners and whether dependencies preserve those owners.

## Prerequisites and Retrieval

Retrieve HTTP methods, statuses, headers, representations, negotiation, conditional requests, caching, and error semantics; API requirements and contracts; request/response ownership; parsing and validation; authentication and authorization; domain invariants and state transitions; dependency inversion; ports and adapters; repositories; transaction boundaries; failure classification; and deterministic testing.

Before implementing an endpoint, retrieve the exact contract version, actor and trust model, command/query purpose, public identifiers, domain transition, required consistency, transaction scope, outbound capabilities, failure taxonomy, disclosure policy, and observability requirements.

## Learning Objectives

By the end of this module, you should be able to:

1. assign responsibilities to transport, application, domain, and infrastructure;
2. design inbound and outbound ports around owned use-case semantics;
3. map untrusted requests into trusted commands without mass assignment;
4. preserve domain outcomes while translating protocol and infrastructure failures;
5. place transactions, retries, time, identity, and observability deliberately;
6. enforce dependency direction with code structure and tests; and
7. choose proportionate boundaries without abstraction for its own sake.

## Core Exposition

### Start from four semantic worlds

The transport world contains method, target URI, headers, cookies, media type, encoding, status, and representation bytes. It answers whether a message can be understood and which protocol response communicates the result.

The application world contains a named use case, authenticated actor context, target identity, preconditions, transaction policy, calls to domain behavior, and external capabilities. It answers what sequence constitutes one application operation.

The domain world contains business values, entities, invariants, policies, and state transitions. It answers whether a proposed decision is meaningful and allowed under authoritative business state.

The infrastructure world contains database queries, queues, clocks, identity providers, remote APIs, files, and framework configuration. It answers how required capabilities are realized in one environment.

These are semantic roles, not mandatory directories. Names such as `transport`, `application`, `domain`, and `infrastructure` are useful when the codebase has enough complexity. A tiny handler can preserve the same separation with local functions and explicit value types.

### Put HTTP mechanics in the transport adapter

An inbound HTTP adapter should:

1. select the operation from method and target;
2. negotiate supported request and response media types;
3. parse path, query, header, cookie, and body bytes;
4. perform transport and structural validation;
5. obtain verified principal context from trusted middleware;
6. map public values into an application input;
7. invoke exactly one use case; and
8. map its outcome to status, headers, media type, and response body.

The adapter understands that `If-Match` is an HTTP precondition, `Accept` controls representation selection, and `Location` identifies a created resource. The domain should not. Conversely, the adapter should not decide whether an order may be cancelled after shipment; the domain should.

Protocol semantics are policy at the API boundary, not incidental framework defaults. Explicitly map method safety and idempotency, preconditions, caching, `201` versus `202`, `204` body absence, and Problem Details. A framework response helper is a mechanism used after the public outcome is known.

Keep adapter functions thin in decision depth, not necessarily line count. Parsing multipart input or serializing links can require substantial code while remaining transport responsibility. A five-line handler that calls an ORM and embeds authorization in a query can still collapse several boundaries.

### Design application inputs around use-case intent

Do not pass a raw request, framework context, deserializer model, or arbitrary field map into application policy. Construct a command or query with only the information the use case legitimately receives.

For example, `CancelOrder` might contain:

- public order identifier;
- authenticated actor and tenant context;
- expected version or precondition;
- cancellation reason supplied by the actor;
- request identity for deduplication; and
- trace context in a separate operational envelope.

It should not contain response writers, database sessions, bearer token strings, caller-supplied owner IDs, final status, or cancellation timestamp. The application obtains an authoritative clock and generates derived audit facts.

Commands express requested change. Queries express requested observation. Avoid names such as `OrderData` that do not reveal direction or authority. Values should be immutable after construction so later middleware cannot change the meaning that validation established.

### Treat authenticated context as separate input

Transport parsing yields untrusted claims. Authentication middleware verifies credentials and constructs a principal context according to issuer, audience, signature, expiry, and deployment policy. The adapter passes that trusted context separately from request-controlled content.

If a JSON body repeats `tenantId` or `userId`, do not let it override context. Reject the field when it is prohibited, or compare it under a documented contract when a public target includes it. Silently accepting and ignoring privileged fields can mislead callers and hide attacks.

The application asks authorization policy whether the actor can attempt the use case; domain rules decide whether the transition is valid. Exact placement varies: object-level authorization may require loading domain state. What matters is that authentication, authorization, and domain validity remain distinct reasons with a deliberate public disclosure mapping.

### Let the application orchestrate one use case

An application service typically:

1. validates application-level preconditions not owned by wire format;
2. establishes transaction or unit-of-work scope;
3. loads required authoritative state through ports;
4. invokes authorization and domain decisions;
5. persists resulting state and records effects;
6. coordinates reliable messages or outbox entries;
7. commits or rolls back once; and
8. returns a typed application outcome.

The application layer should not repeat business invariants as procedural `if` statements around an anemic entity. If “a shipped order cannot be cancelled” is domain truth, the aggregate or domain policy owns it. The application decides which aggregate to load and what to do with the decision.

Orchestration is not business meaning. Calling repository, policy, aggregate, outbox, and unit of work in order is orchestration. Calculating whether a cancellation fee applies from contract rules is domain behavior, even if it needs a domain service rather than one entity.

### Keep domain behavior mechanism-free

Domain types should speak the ubiquitous business language and remain executable without a web server, serializer, database, or queue. They may return a changed aggregate, domain event, or typed rejection. They do not return `HTTP 409`, database rows, JSON objects, or framework exceptions.

A domain invariant must hold regardless of entry adapter. The same cancellation rule should apply when driven by HTTP, a scheduled expiration, an administrator tool, or a message consumer. Different actors may have different policies, but the policy input is business capability—not a specific header object.

Avoid leaking persistence annotations or lazy-loading handles into domain behavior. Some projects pragmatically share a domain and persistence shape when the mapping is truly stable and private. They must still prevent serialization and query mechanisms from escaping. Sharing representation is a local trade-off, not permission to surrender ownership.

### Make ports application-owned

An outbound port describes the capability the application needs, using application or domain vocabulary. `Orders.find(OrderId)` and `Orders.save(Order, ExpectedVersion)` are owned needs. `SqlOrderRepository.execute(queryBuilder)` exposes the mechanism and reverses control.

Ports may cover persistence, clocks, ID generation, payment authorization, message publication, feature decisions, or audit recording. Create a port when the capability is a meaningful boundary with alternatives, failure semantics, or test value. Do not wrap every library call reflexively.

Adapters implement ports using PostgreSQL, an HTTP client, a broker, or an in-memory substitute. They translate foreign identifiers, schemas, timeouts, errors, and transactions into the port's outcome algebra. The application must not catch a vendor exception to learn that an order version is stale.

An inbound port is the application use-case interface exposed to driving adapters. It need not be a language interface when one function suffices. Its stability comes from owned semantics, not syntax.

### Understand dependency direction versus control flow

At runtime, control may flow:

$$
\text{HTTP adapter}\rightarrow\text{application}\rightarrow
\text{port}\rightarrow\text{database adapter}.
$$

Source dependencies differ. The HTTP adapter imports the application input and port. The application defines or imports the outbound port. The database adapter imports and implements that port. The application does not import the database adapter; composition at the outer startup boundary supplies it.

This inversion permits application tests with controlled adapters and infrastructure replacement without rewriting policy. It also prevents an ORM query type or HTTP client response from becoming part of the use-case interface.

Dependency direction is not absolute purity. Domain code can use a standard decimal or date library if its semantics fit. The rule targets replaceable mechanisms and foreign policy. Record justified exceptions rather than constructing weak wrappers around stable language primitives.

### Map values explicitly

A safe mapping pipeline is:

$$
W\xrightarrow{p}T\xrightarrow{m}A\xrightarrow{d}D
\xrightarrow{o}A'\xrightarrow{s}T'\xrightarrow{e}W',
$$

where wire bytes $W$ parse to transport value $T$, map to application input $A$, drive domain values $D$, yield application outcome $A'$, serialize response model $T'$, and encode response bytes $W'$.

Each arrow can reject or lose information and therefore needs tests. Parsing checks syntax and encoding. Mapping establishes field ownership and trusted context. Domain construction checks business validity. Output mapping applies field-level visibility. Serialization enforces the media type.

Explicit mapping prevents mass assignment and accidental exposure. It also costs code. Reduce repetition with focused constructors or generated structural adapters only when they preserve allowlists, null/absence semantics, numeric precision, and error locations. Do not use reflection that copies matching names across trust boundaries by default.

### Keep boundary models distinct when meanings differ

A create DTO admits caller-owned inputs. An application command includes trusted actor and preconditions. A domain aggregate contains authoritative state and behavior. A persistence record includes storage keys, version columns, and serialization details. A response DTO contains the authorized public projection.

They may share small immutable value types such as `OrderId` or `Currency` when semantics truly agree. They should not share a giant `Order` shape just to avoid mapping. A field can be required in storage, derived in domain, forbidden in requests, and conditional in responses.

Distinct models also protect evolution. Adding an index column does not alter OpenAPI. Adding a response link does not change the aggregate. Accepting a new create option does not make it writable in updates.

### Place validation by ownership

Validation is layered:

- transport: malformed bytes, unsupported media type, parameter encoding;
- structural contract: required fields, types, ranges, closed properties;
- application: referenced input combination and use-case preconditions;
- authorization: actor capability over target and fields;
- domain: invariant and transition validity;
- infrastructure: uniqueness, concurrency, and availability evidence translated to owned outcomes.

Do not stop after schema validation or repeat the same rule inconsistently. A positive quantity bound may be structural; “quantity does not exceed remaining inventory under reservation policy” is domain. A database constraint can defend an invariant but should not be the only place its meaning exists.

Preserve error locations and causes internally. Public responses reveal only stable, safe classifications. A structural error can name an allowed public field; a storage constraint name should never leak.

### Preserve typed outcomes until the edge

Define an application outcome algebra such as:

$$
O=\{\text{Changed},\text{NotFound},\text{Forbidden},
\text{Stale},\text{Conflict},\text{Unavailable}\}.
$$

The transport adapter maps outcomes under the API's disclosure and HTTP policy. `Stale` can become `412` when tied to `If-Match`; a state conflict can become `409`; concealed `Forbidden` can map to the same public `404` as `NotFound`. Another adapter may map the same domain decision differently while preserving meaning.

Avoid catching every exception at the controller and returning `500`. Infrastructure adapters translate known vendor failures into typed port failures while retaining the cause. Unexpected defects reach a top-level safety boundary, produce a generic public problem, and record a correlated internal error.

Do not make error type names mirror HTTP statuses. `OrderAlreadyShipped` expresses domain reason; status selection belongs to the public contract and operation context.

### Put transactions around the use case

If one use case must load, decide, persist, and enqueue an outbox record atomically, transaction scope surrounds those actions. Repository methods that each commit independently can expose partial effects. Conversely, holding a database transaction across a slow remote payment call increases locks and cannot make the remote action atomic.

The application owns the unit-of-work policy; infrastructure realizes it. For remote effects, choose an explicit consistency pattern such as reservation, outbox, saga, or idempotent reconciliation. The API must report the actual completion point rather than pretending a distributed transaction exists.

Retries belong at the layer that understands safety. A database adapter may retry a serialization failure only when the whole application operation can be repeated correctly. An HTTP adapter must not blindly replay a non-idempotent use case after losing its response. Preserve request identity and effect evidence across boundaries.

### Control time, IDs, and nondeterminism

Authoritative time and generated IDs are application dependencies when they affect business state or observable output. Inject a clock or generator through a narrow port so tests can exercise exact boundaries and retry stability. Do not let controllers, entities, and repositories each call wall clock independently.

Operational trace IDs are transport/observability context and need not become domain values. Business request identity used for idempotency is part of application semantics. Distinguish them even if both are strings.

Randomness used in business selection needs a recorded seed or strategy when reproducibility matters. Cryptographic tokens require a security-owned generator and must never enter logs or ordinary domain display values.

### Make observability cross boundaries without contaminating them

The adapter starts or continues request context and records protocol dimensions such as operation, status, and response size. The application records use-case outcome and dependency timing. Domain code can emit meaningful domain events but should not call a vendor telemetry SDK.

Pass an opaque correlation context where necessary or use scoped infrastructure outside domain signatures. Logs must not contain bearer credentials, sensitive request bodies, or another tenant's data. Metrics use bounded labels; public IDs and raw error messages are usually unsafe high-cardinality dimensions.

Trace context helps correlate, not authorize. Never trust a caller-supplied trace field as actor or tenant identity. Preserve causal chains internally while the public error uses a safe opaque instance identifier.

### Enforce architecture mechanically

Package layout and language visibility can prevent unwanted imports. Add dependency tests that reject domain imports of transport, ORM, or vendor clients; application imports of concrete adapters; and controllers that access persistence directly. Generated code stays at an adapter boundary.

The following executable audit checks a tiny dependency graph. It models source dependencies only, not runtime calls or architectural quality.

<!-- bijux-verify: {"id":"boundary-dependency-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"edges=5\nviolations=[]\ndomain_external_dependencies=[]\npolicy_direction=preserved\n","stderr":""}} -->
```python
rank = {"transport": 0, "application": 1, "domain": 2}
edges = {
    ("transport", "application"),
    ("application", "domain"),
    ("http_adapter", "application"),
    ("database_adapter", "application"),
    ("composition", "database_adapter"),
}
layer_edges = {(left, right) for left, right in edges if left in rank and right in rank}
violations = sorted((left, right) for left, right in layer_edges if rank[left] > rank[right])
domain_external = sorted(right for left, right in edges if left == "domain")
print(f"edges={len(edges)}")
print(f"violations={violations}")
print(f"domain_external_dependencies={domain_external}")
print("policy_direction=preserved")
```

Architecture tests are guardrails, not proof. A controller can call one permitted application function whose implementation still contains every business rule. Review responsibility and vocabulary in addition to imports.

### Test at every owned boundary

Test domain rules as pure decisions across valid, boundary, and rejected states. Test application use cases with controlled ports for not found, unauthorized, stale, dependency failure, and commit failure. Test outbound adapters against real protocol/database contracts. Test HTTP adapters for parsing, trusted-context construction, status, headers, media type, safe errors, and serialization.

Contract tests check that adapter behavior agrees with the published interface. Integration tests check composition and real mechanisms. End-to-end tests exercise a small number of deployed tasks. No single layer substitutes for the others.

Include negative field-ownership tests: actor, tenant, status, totals, internal IDs, and restricted notes cannot be mass-assigned or exposed. Verify transaction rollback and postconditions, not merely method calls.

### Keep boundaries proportionate

Too few boundaries cause mechanism and policy coupling. Too many create translation chains with no independent meaning. Add a boundary when vocabulary, trust, lifecycle, failure model, change cadence, ownership, or test strategy changes.

A pass-through class that renames every repository method adds no policy. A generic `BaseService` or `GenericRepository` often erases use-case and aggregate semantics. Prefer concrete, narrow ports and explicit operations.

Reassess boundaries as the service evolves. A direct in-process call may be correct inside a modular monolith. Splitting it into a network service introduces partial failure, serialization, versioning, and authorization and therefore requires a new public boundary—not merely a remote implementation of the same internal interface.

## Definitions and Notation

Let $T$, $A$, $D$, and $I$ denote transport, application, domain, and infrastructure components. Source dependency $u\rightarrow v$ means $u$ requires a symbol or contract owned by $v$. Among policy layers, rank $r(T)=0$, $r(A)=1$, and $r(D)=2$; permitted inward dependency satisfies $r(u)\le r(v)$.

An inbound transformation $m:T\times C\rightarrow A$ maps parsed transport value and trusted context $C$ to application input. It is partial because invalid or prohibited combinations are rejected. Domain transition $\delta:D\times A\rightharpoonup D\times E$ produces new state and domain events $E$ only where preconditions hold.

An outbound port $P$ is owned by application policy; adapter $J$ realizes $P$ using foreign mechanism $F$. Application code depends on $P$, while composition binds $J$. Runtime call direction does not determine source ownership.

A **composition root** constructs concrete adapters and connects them to ports. An **outcome algebra** is a closed set of meaningful result variants. A **trust boundary** is a crossing where claims require validation before gaining authority. **Mass assignment** is unintended binding of caller fields to internal state. **Mechanism leakage** occurs when foreign framework or vendor types cross into owned policy interfaces.

## Mechanisms, Invariants, or Proof Structure

1. Identify transport, use-case, domain, and infrastructure vocabulary.
2. Define one application input with caller intent and separate trusted context.
3. Parse and structurally validate at the inbound adapter.
4. Map explicitly, rejecting prohibited or ambiguous fields.
5. Orchestrate one use case within an explicit transaction policy.
6. Invoke domain decisions free of transport and persistence mechanisms.
7. Access external capabilities through application-owned ports.
8. Preserve typed outcomes and causes until safe edge translation.
9. Compose adapters outward and enforce source dependency inward.
10. Test each boundary, postcondition, failure, and dependency invariant.

The central reasoning chain is ownership: public protocol determines adapter behavior; application use-case policy determines sequencing; domain truth determines transitions; foreign mechanisms satisfy owned ports. An import graph supports this arrangement but cannot establish it without semantic review.

## Alternatives and Trade-Offs

Direct framework handlers minimize files and suit small, stable CRUD surfaces. Explicit adapters and use cases cost mapping but protect trust, policy, failure, and evolution. Begin simple while keeping untrusted input, policy, and persistence visibly separate; extract when meanings diverge.

Layered architecture organizes by technical role but can encourage every call to descend through generic services. Ports and adapters organize dependencies around application capabilities and allow multiple drivers and mechanisms. They can coexist when layers retain concrete ownership.

Sharing domain and persistence types reduces mapping and may fit a small private service. It couples storage lifecycle and query behavior to business state. Separate them when schemas, lifecycles, confidentiality, or change rates differ.

Exceptions are idiomatic in some languages; result types make expected outcomes visible. Use typed exceptions or values for expected domain and port outcomes, and reserve unexpected exceptions for defects. Whichever style is chosen, prevent HTTP and vendor errors from owning inner semantics.

One transaction per use case gives coherent local effects but may increase lock time. Smaller transactions improve concurrency but require explicit reconciliation. Do not hide the trade-off behind repository defaults.

Generated adapters reduce repetitive parsing and serialization. Handwritten adapters better express unusual protocols and policies. Generated code remains replaceable at the edge and must receive compilation, contract, and negative-field tests.

## Failure Modes and Misconceptions

- **“Thin controllers mean good boundaries.”** A one-line controller can call a service that mixes all responsibilities.
- **“Domain objects should know HTTP for convenience.”** That couples business truth to one delivery mechanism.
- **“The ORM entity is already the model.”** Storage, request, domain, and response ownership commonly differ.
- **“Mapping is wasted code.”** At trust and ownership boundaries, mapping is enforcement and evidence.
- **“Authentication claims in the body are convenient.”** Actor and tenant context must come from verified authority.
- **“Every dependency needs a port.”** Wrap meaningful volatile capabilities, not stable primitives mechanically.
- **“Runtime calls must point inward only.”** Control reaches outbound adapters; source dependencies still point to owned ports.
- **“Repositories should expose flexible query builders.”** Foreign query mechanisms leak infrastructure policy inward.
- **“Domain errors are HTTP errors.”** Domain reasons can serve multiple adapters and need edge-specific disclosure.
- **“A database constraint is the domain rule.”** It is defense and concurrency enforcement, not the only semantic owner.
- **“A transaction per repository method is safe.”** One use case can partially commit across calls.
- **“Retries belong in generic middleware.”** Only a layer that knows operation safety can authorize replay.
- **“Trace context is trusted identity.”** Correlation and authorization are different concerns.
- **“Architecture import tests prove design.”** They detect selected edges, not misplaced logic or weak vocabulary.
- **“More layers are more maintainable.”** Boundaries without semantic change add indirection and failure translation.

## Worked Examples

### Example 1

**Situation:** A controller binds request JSON directly into an ORM `User` with `role` and `tenant_id`. **Reasoning:** Define `RegisterUser(email, display_name)` and attach verified tenant and actor separately; derive role under policy and map to a persistence record. **Conclusion:** explicit input ownership blocks mass assignment.

### Example 2

**Situation:** Domain method `cancel()` returns HTTP status `409`. **Reasoning:** Replace it with `AlreadyShipped` domain outcome; let the HTTP adapter map it to the operation's stable conflict problem, while a batch adapter records a rejected command. **Conclusion:** domain meaning survives multiple transports.

### Example 3

**Situation:** A response serializer traverses a lazy `customer` relationship and emits internal notes. **Reasoning:** Construct an authorized response DTO inside the use case or output mapper with explicit fields and already-loaded data. **Conclusion:** persistence navigation must not define public shape or query cost.

### Example 4

**Situation:** Each repository `save` commits, then outbox insertion fails. **Reasoning:** Put state update and outbox record in one application-owned unit of work and publish after commit through reliable relay. **Conclusion:** transaction scope follows the use-case invariant, not repository convenience.

### Example 5

**Situation:** A database unique violation exposes constraint `orders_external_ref_key`. **Reasoning:** The adapter recognizes the governed constraint, translates it to `DuplicateOrderIdentity`, retains the cause internally, and the HTTP adapter selects the safe public conflict. **Conclusion:** failure translation preserves meaning without leaking mechanism.

### Example 6

**Situation:** Both HTTP and scheduled expiration cancel orders. **Reasoning:** Each inbound adapter constructs the same application intent with distinct actor capability; one domain transition enforces shipment and state rules. **Conclusion:** shared policy belongs behind transport-specific adapters.

### Example 7

**Situation:** A remote inventory call times out while a database transaction holds locks. **Reasoning:** Redesign with reservation before the local transaction or a durable pending workflow; report `202` if completion is genuinely asynchronous. **Conclusion:** boundary placement exposes distributed consistency rather than extending a local transaction fiction.

### Example 8

**Situation:** Middleware retries `POST /payments` after connection loss. **Reasoning:** The adapter cannot know whether the effect occurred. Require application request identity, durable deduplication, and replay outcome; retry only under that contract. **Conclusion:** transport retry is safe only with application effect semantics.

### Example 9

**Situation:** An application service imports a concrete SQL repository to use one optimized query. **Reasoning:** Define the needed `OrderSummaryReader` query port with result semantics, then implement it directly in SQL. **Conclusion:** ports need not force aggregate loading and can preserve optimized reads without mechanism leakage.

### Example 10

**Situation:** A five-endpoint internal service has controllers, services, managers, gateways, facades, and repositories that only forward calls. **Reasoning:** Collapse pass-through types into explicit handler-to-use-case functions, retain one domain policy and one storage port where meanings change, and enforce only real boundaries. **Conclusion:** architecture quality comes from semantic ownership, not layer count.

## Cross-Program Connections

[Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) owns domain language, values, aggregates, and invariants. [Software Engineering Patterns](../../11-software-engineering-patterns/ROADMAP.md) supplies Adapter, Repository, Unit of Work, Data Mapper, and Dependency Injection patterns. [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) owns system-wide styles and boundaries. [Database Engineering](../../18-database-engineering/ROADMAP.md) supplies transaction and persistence mechanisms. This API module owns translation between public service semantics and those internal responsibilities.

## References

1. R. Fielding, M. Nottingham, and J. Reschke, [*RFC 9110: HTTP Semantics*](https://www.rfc-editor.org/rfc/rfc9110.html), especially implementation-independent resource interfaces, Internet Standard, June 2022. Checked 2026-09-01.
2. OpenAPI Initiative, [*OpenAPI Specification 3.2.0*](https://spec.openapis.org/oas/v3.2.0.html), language-agnostic public HTTP interface description, 19 September 2025. Checked 2026-09-01.
3. A. Cockburn, [*Hexagonal Architecture: Ports and Adapters*](https://alistair.cockburn.us/hexagonal-architecture/), HaT Technical Report 2005.02, 4 September 2005. Checked 2026-09-01.
4. E. Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software*, Addison-Wesley, 2003, especially layered architecture, repositories, services, and model isolation.
5. M. Fowler, *Patterns of Enterprise Application Architecture*, Addison-Wesley, 2002, especially Service Layer, Data Mapper, Repository, and Unit of Work.
6. R. C. Martin, *Clean Architecture: A Craftsman's Guide to Software Structure and Design*, Pearson, 2017, especially dependency direction and boundary crossing.

## Exercises

### Exercise 1

Classify these responsibilities: parsing `If-Match`, verifying bearer credentials, checking cancellation policy, opening a unit of work, executing SQL, selecting `412`, and serializing Problem Details.

### Exercise 2

Trace `PATCH /orders/{id}` from wire bytes through transport, trusted context, application command, domain decision, repository port, outcome, and response. Name every possible rejection owner.

### Exercise 3

Diagnose a service whose controller receives an ORM entity, trusts body tenant ID, calls two auto-committing repositories, catches all exceptions, and returns the saved entity. Propose the smallest coherent repair.

### Exercise 4

Compare shared and separate request, domain, persistence, and response models for a small internal service that is likely to add a second transport and field-level authorization.

### Exercise 5

Design boundaries for accepting a payment command that calls a remote provider, persists local state, emits an event, supports idempotent retry, and may complete asynchronously. State transaction, failure, and evidence limits.

## Answers to the Exercises

### Answer 1

The HTTP adapter parses `If-Match`, selects `412`, and serializes Problem Details. Authentication middleware verifies the bearer credential and constructs trusted principal context. Domain policy decides whether cancellation is allowed. The application owns unit-of-work scope. A database adapter executes SQL. Exact authorization may span application policy and loaded domain state, but it remains distinct from authentication and public error disclosure.

### Answer 2

The adapter parses method, path, media type, patch document, and `If-Match`; syntax or negotiation can fail there. Trusted middleware supplies principal or an authentication failure. Mapping rejects prohibited fields and creates an update command. The application loads through a port, evaluates authorization, and invokes domain transition; absence, concealment, stale version, invalid transition, and dependency unavailability remain typed. The database adapter translates concurrency and vendor failures. After commit, the adapter maps outcome to status, `ETag`, content type, and authorized response. Each rejection has one semantic owner even when the edge formats it.

### Answer 3

Introduce an operation-specific request DTO and mapping that excludes tenant and server-owned fields; pass verified tenant separately. Add one application use case and unit of work around both persistence actions. Move business invariant into a domain method or policy. Define narrow repository ports and translate known database failures. Construct an authorized response DTO rather than serializing the entity. Map typed outcomes explicitly and leave unexpected defects to a top-level safe handler. This adds only boundaries where trust, transaction, policy, and representation change.

### Answer 4

Sharing reduces mapping now, but the second transport and field-level authorization make directions and projections diverge. Keep small immutable domain values shared where semantics agree, but separate create/update inputs, aggregate state, storage record, and authorized outputs. The second adapter can reuse application commands without importing HTTP. Separate responses make field visibility explicit; separate persistence prevents new columns and lazy relations from becoming public. The extra mapping is justified by known change and trust differences.

### Answer 5

The inbound adapter parses the command and request identity; the application checks durable deduplication and records a pending payment. A local transaction atomically stores state and outbox intent. A worker calls the remote provider through an outbound port with provider idempotency identity, records the result in another local transaction, and emits completion through an outbox. The API returns final success only if known; otherwise `202` identifies an operation with observation and terminal failure semantics. Retries reconcile by identity rather than replay blindly. Local transactions cannot prove atomicity with the provider; evidence must separately cover deduplication, crash points, provider responses, event publication, and deployed workflow.
