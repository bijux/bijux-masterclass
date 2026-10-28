---
module_id: PLAT-061
program: Platform Engineering
level: 2
module_number: 61
title: Platform API Layers
status: complete
last_verified: 2026-09-02
---

# Platform API Layers

## One-Page Review

### Governing question

How should an internal developer platform separate experience, access, domain, policy, workflow/reconciliation, provider, state/event, and observability concerns so each layer can evolve and fail independently without splitting semantics or creating a synchronous distributed monolith?

### Essential definitions

- A **layer** is an architectural responsibility boundary with an explicit contract and allowed dependency direction; it is not necessarily a process, repository, team, or network hop.
- The **experience layer** presents journeys through portal, CLI, IDE, SDK, or Git while projecting the canonical domain contract.
- The **access layer** authenticates, routes, rate-limits, and applies transport concerns; it does not invent domain meaning.
- The **domain API layer** owns resource vocabulary, intent, lifecycle, compatibility, and user-visible status.
- The **policy layer** makes context-specific authorization, admission, quota, and placement decisions with identifiable policy inputs.
- The **workflow/reconciliation layer** turns accepted intent into restart-safe progress and coordinates long-running effects.
- A **provider adapter** translates capability operations and observations to one implementation while containing provider identity, errors, and idempotency.
- The **system of record** is the authority for a fact; a catalog, cache, search index, event stream, and rendered view are not automatically authoritative.
- A **synchronous cut** is the set of components that must respond before a request completes; every member contributes latency and availability coupling.
- **semantic duplication** occurs when multiple layers independently default, validate, authorize, or interpret the same field.

### Central model, mechanism, or theorem

Model layer dependencies as a directed graph $G=(L,E)$ with an edge $a\rightarrow b$ when layer $a$ depends on contract $b$. Keep the control graph acyclic except for explicit asynchronous feedback through versioned state/events. For a synchronous request path $P$, latency is approximately

$$
T_P=\sum_{i\in P}t_i+\sum_{(i,j)\in P}t_{ij},
$$

and, under the simplifying assumption of independent component availability, $A_P=\prod_{i\in P}A_i$. The product is a model, not a guarantee; common dependencies and correlated failures usually make the real result worse. Minimize the synchronous cut: authenticate, authorize, validate stable rules, durably accept intent, return identity/revision, and move provider work to asynchronous reconciliation. Every interface reads the same schema/status semantics, policy decisions carry revision/evidence, adapters preserve operation identity, and derived views rebuild from authoritative state.

### Critical invariants

- Layers are defined by owned decisions and contracts, not fashionable component names or deployment count.
- Portal, CLI, SDK, Git, and direct API clients submit semantically equivalent intent; no UI-only default or policy becomes authoritative.
- Authentication context survives every boundary; authorization is enforced at the domain/effect boundary, not trusted from presentation alone.
- Domain objects and operation records are authoritative; catalogs, caches, search, analytics, and events declare freshness and rebuild paths.
- Admission performs bounded deterministic work; provider calls, long workflows, and volatile feasibility remain asynchronous.
- Policy input/output, class/composition, schema, and adapter contract revisions are identifiable in decisions and status.
- Workflow checkpoints and external idempotency identities survive process restart, duplicate event, timeout, restore, and failover.
- Provider-specific configuration/errors do not leak into the stable domain contract without an explicit expert surface.
- Cross-layer calls have timeout, retry ownership, idempotency, backpressure, error translation, and degraded-mode contracts.
- No central portal backend becomes the only route, policy engine, orchestrator, catalog authority, secret broker, and provider client.

### Common failures

Calling a deployment diagram “layers”; putting business defaults in portal code; trusting gateway authorization for later effects; synchronous portal→orchestrator→policy→catalog→provider chains; one shared database with undocumented ownership; catalog as desired-state authority; event payload as command and record; retries at every layer; leaking provider errors; an adapter that owns domain policy; cyclic callbacks; reading stale cache for destructive action; trace IDs mistaken for operation IDs; one global availability SLO; direct UI-to-provider credentials; plugin code sharing internals; rebuilding state from incomplete events; and splitting services before contracts exist.

### Compact example

A developer submits `DataService` through a portal. The form is generated from the same versioned schema used by CLI and Git. The access layer authenticates and limits traffic; the domain API authorizes the tenant, validates stable transitions, evaluates a local/versioned policy decision, persists intent, and returns UID/generation. A reconciler asynchronously resolves class and dependencies, checkpoints an operation, and calls a PostgreSQL adapter with object UID plus idempotency key. The adapter translates provider state and errors into a capability contract. Status records observed generation, policy/composition revisions, domain conditions, and a secret reference. Catalog and search consume changes as derived views and can be rebuilt. If the portal, search, or one provider is down, direct API access and unrelated capability domains remain available.

### Connections

This module layers the domain contract from [PLAT-060](060-designing-a-domain-specific-platform-api.md) over control/data-plane separation from [PLAT-051](051-control-plane-and-data-plane-separation.md), reconciliation from [PLAT-052](052-desired-state-and-reconciliation.md), dependency/failure reasoning from [PLAT-058](058-cross-resource-dependencies.md) and [PLAT-059](059-control-plane-failure-and-recovery.md). PLAT-062 through PLAT-070 specialize portal, catalog, ownership, workflow, policy, vending, broker, eventing, and integration layers.

## Governing Question

How can a platform provide one coherent product while decomposing its interfaces and control machinery into boundaries that preserve authority, allow independent evolution, and prevent optional experiences or integrations from joining every critical path?

Layering is useful only when it answers who owns a decision, where truth lives, what crosses the boundary, and how failure behaves. A portal plus APIs plus controllers is not automatically layered. If each repeats defaults and policy, the system has multiple contracts. If every request waits for every component, it has one availability domain.

The aim is a coherent semantic plane with replaceable experiences and implementations. Users should see the same resource and status through every interface. Operators should trace a request into durable work and provider effects without treating the trace as authority. Failures should stop at deliberate bulkheads wherever the domain permits.

## Why This Matters

Internal platforms integrate identity, catalogs, policy, source control, workflows, Kubernetes, cloud providers, secrets, cost, and observability. Naive integration creates a dependency web where a search outage blocks provisioning or a provider slowdown exhausts portal threads.

Layers control change. A provider adapter can be replaced without changing `DataService`; a portal can change without migrating stored intent; a policy engine can roll a compatible bundle without recompiling every provider integration. These benefits appear only when contracts prevent internal leakage.

Layers control authority. The browser should not hold provider credentials. A gateway should not be the sole authorization for a long-running controller action. A catalog should not become a writable shadow copy of desired state.

Layers also control cognition. Teams can reason about domain semantics, policy, orchestration, or provider translation separately. Excess fragmentation reverses that benefit, so a logical layer need not become a microservice until scale, security, ownership, or failure isolation justifies it.

## Prerequisites and Retrieval

Retrieve layered architecture, ports and adapters, dependency inversion, bounded contexts, control/data/management planes, platform as product, declarative APIs, API gateways, authentication and authorization, schemas and admission, desired state and reconciliation, durable workflows, idempotency and fencing, policy decision/enforcement points, service catalogs, composition, provider adapters, GitOps, events and outbox/inbox, systems of record, caches and materialized views, consistency and freshness, timeouts/retries/circuit breakers, queues and backpressure, bulkheads, SLOs, tracing/logging/metrics/audit, API versioning, disaster recovery, tenancy, and least privilege.

You should distinguish logical layer from deployment; interface from authority; experience validation from admission; authentication from authorization; policy decision from enforcement; domain API from provider API; workflow from event stream; event notification from system of record; catalog metadata from desired state; cache from durable checkpoint; correlation ID from idempotency key; synchronous acknowledgement from completed outcome; orchestration from reconciliation; composition from coupling; availability model from measured SLO; and independent service from independent failure domain.

## Learning Objectives

After completing this module, you should be able to:

1. partition a platform by responsibilities, authoritative facts, contracts, and allowed dependency direction;
2. design consistent portal, CLI, SDK, Git, and direct-API experiences over one semantic contract;
3. minimize synchronous cuts and calculate latency/availability implications without overstating the model;
4. place authentication, authorization, policy decisions, and effect enforcement at durable trust boundaries;
5. separate domain intent, workflow state, provider translation, catalog views, events, and telemetry;
6. specify cross-layer identity, revision, idempotency, error, timeout, retry, and backpressure contracts;
7. choose logical versus physical separation from security, scale, ownership, and failure evidence;
8. test degradation, restore, version skew, replay, and retirement across the dependency graph; and
9. evolve platform components without creating semantic duplication or a portal monolith.

## Core Exposition

### Layer by responsibility, not product logo

Begin with owned decisions. Experience owns interaction and progressive disclosure. Access owns transport authentication, routing, and limits. Domain API owns vocabulary and lifecycle. Policy owns context-specific decisions. Workflow/reconciliation owns progress. Adapters own provider translation. State/event services own durable records or distribution according to explicit contracts. Observability owns evidence, not control authority.

A commercial tool may implement several logical layers; one logical layer may use several tools. That is acceptable if contracts and authority remain clear. Drawing one box per vendor obscures semantics; drawing one box per process can invent boundaries that do not exist.

For every layer record inputs, outputs, source of truth, allowed callers/dependencies, identity propagation, version, latency budget, availability/degraded mode, ownership, data classification, scale, recovery, and retirement. If two boxes both own a field’s default, status, or policy, the boundary is unresolved.

Keep dependency direction inward toward stable domain contracts and outward through ports to replaceable implementations. Provider SDK types should not appear in domain objects. Experience code may depend on generated domain clients; domain code must not depend on portal widgets.

### Experience is a projection, not a control plane

Portal, CLI, IDE, SDK, ChatOps, and Git serve different journeys. They can tailor discovery, guidance, batching, or review, but must converge on the same canonical API and status. A portal-only workflow creates an untestable second contract and excludes automation.

Generate forms and clients from schema where useful, then add domain explanations and accessibility. Client-side validation improves feedback but server-side admission remains authoritative. Defaults shown in a form must match actual API resolution; never insert invisible values only in one interface.

The experience layer may aggregate read models for speed, but destructive or authoritative actions submit to the domain API with current identity and concurrency preconditions. Stale catalog/search data must be labeled and refreshed before consequential operations.

Provide deep links from an object to status, ownership, policy decision, workflow, dependencies, cost, audit, and diagnostics without making the portal database the authority for them. Direct API access should remain viable during portal outage.

### Keep the access layer thin and explicit

An edge gateway can terminate TLS, authenticate, normalize identity claims, route versions, enforce coarse rate limits, and attach correlation context. It should not silently translate domain versions, choose providers, or contain the only authorization logic.

Identity must be cryptographically verifiable or exchanged for a scoped internal identity at each trust boundary. Forwarded headers are not trustworthy unless the receiver authenticates the forwarding proxy and strips caller-supplied copies.

Gateway authorization can reject obviously forbidden routes, but domain and effect layers reauthorize using current object, tenant, reference, and policy context. Long-running work cannot rely on the fact that a browser request passed a gateway hours earlier.

Rate limits need persona/tenant/fairness semantics. One global limit lets a noisy automation client starve incident repair. Preserve priority for security revocation, deletion obligations, and recovery while bounding expensive preview or bulk operations.

### Make the domain API the semantic center

The domain layer defines resources, intent, transitions, status meanings, error taxonomy, compatibility, and lifecycle. It stores or delegates to one authoritative record. It does not need to perform the external outcome synchronously.

For a create/update, the smallest robust synchronous cut is usually authenticate, authorize, decode/default, validate deterministic rules, enforce known policy/quota, commit intent with concurrency metadata, append reliable work/change evidence, and acknowledge UID/revision. Provider capacity and long effects proceed asynchronously.

Separate spec and status ownership. Store requested and effective policy/composition revisions. Publish actionable domain conditions rather than raw adapter failures. Version semantic changes and keep conversion free of provider side effects.

Resource boundaries follow domain lifecycle, not downstream service boundaries. One API object may compose multiple capabilities, while independently authorized/shared capabilities remain references.

### Place policy decisions and enforcement deliberately

Policy decision points evaluate versioned input: principal, tenant, object old/new state, referenced capabilities, classification, quota, environment, and policy bundle revision. Responses include decision, reason, obligations/defaults where supported, policy identity, and expiry/freshness.

Enforcement points exist at admission, workflow transition, secret delivery, provider effect, and sometimes data-plane request. A create-time allow does not authorize a later destructive change or cross-tenant attachment. Re-evaluate at the boundary where consequence occurs, with stable semantics for revocation.

Keep admission bounded. In-process/schema/CEL-like rules reduce synchronous dependencies. Remote policy services need strict timeouts, caching rules, failure policy, and recovery path; do not use stale allow decisions for destructive effects merely to preserve availability.

Policy should not mutate the same field differently at portal, gateway, admission, and controller. Centralize decision semantics or produce a single effective state with provenance.

### Separate progress from transport requests

Long-running provisioning, migration, restore, and deletion need durable workflow/reconciliation state. HTTP connections, queue delivery attempts, and traces are ephemeral transports. A timeout must not erase accepted work or cause blind duplication.

Controllers repeatedly derive bounded actions from desired and observed state. Workflow resources model ordered irreversible steps, approval, compensation, or terminal operation history. Use each where its semantics fit; do not turn every reconcile into a global workflow or every workflow into mutable desired state.

Persist checkpoints before and after ambiguous effects with stable operation identity. The queue carries a key/hint, not the only copy of intent. Duplicate or out-of-order delivery triggers reread and idempotent evaluation.

Partition queues by capability, tenant, provider, and risk where needed. Backpressure must propagate as domain conditions and admission/priority choices rather than memory growth.

### Isolate provider behavior behind adapters

An adapter accepts a capability-level operation with object/effect identity and returns normalized observation/outcome. It owns authentication to that provider, API pagination/throttling, error classification, idempotency semantics, eventual consistency, and version compatibility.

It does not choose business class, tenant entitlement, or deletion policy. Those decisions arrive in the effective plan. Keeping policy out permits the same adapter to serve several domain products without hidden behavior.

Normalize errors into stable categories: invalid capability request, unauthorized/forbidden, quota/capacity, conflict, throttled, transient unavailable, ambiguous timeout, permanent provider failure, and not found with identity context. Preserve an operator-only diagnostic reference.

Adapters need conformance tests against real or faithful provider environments, including retries, duplicate creates, stale reads, import/adoption, deletion, credential rotation, and API version change. A mock that always responds immediately does not prove isolation.

### Name authoritative and derived state

For each fact identify its system of record. Domain spec/status may live in Kubernetes or a service database. Workflow checkpoints may have their own store. Provider reality remains authoritative for provider existence. Git may be authority for declared configuration in a GitOps path. Catalog metadata often derives from several authorities.

A cache or read model declares source revision, update time, staleness bound, and rebuild procedure. Never perform destructive action from a search index alone. Re-read the authority with concurrency/identity checks.

Avoid a shared database whose tables are edited by many layers. Shared physical storage can be acceptable, but schema/table ownership and transactional boundaries must be explicit; cross-layer joins create release and recovery coupling.

Backups must capture mutually consistent identity and revisions or document reconciliation. Restore can move domain/workflow state backward while providers and events remain ahead.

### Use events for distribution, not magical decoupling

Events notify that a durable fact changed or record a domain fact. Define producer, schema/version, event ID, subject identity, source revision, occurrence/publication time, ordering scope, retention, privacy, and replay.

Use an outbox or equivalent atomic linkage so committed intent/status changes are not lost between database commit and publish. Consumers maintain inbox/idempotency state where effects matter. At-least-once delivery is expected; exactly-once business effects require domain identity and state.

Events can reduce temporal coupling, but schema, semantics, broker, retention, and replay remain dependencies. A consumer must recover from missed or duplicate events by rereading an authority where possible.

Avoid event cycles that cause layers to rewrite each other’s authority. Derived catalog enrichment should not mutate domain intent, which emits another event indefinitely.

### Quantify the synchronous cut

For a serial synchronous path, sum component and network latency. Tail latency matters: five fast medians with one slow p99 still produce poor p99. Parallel calls use the slowest required branch plus coordination rather than a simple sum.

Under independent availability, required components multiply. Five components at 99.9% each yield about $0.999^5\approx0.99501$, before networks and common dependencies. Independence is optimistic: shared identity, DNS, cluster, database, or rollout creates correlated failure.

<!-- bijux-verify: {"id":"platform-layer-path-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"latency_ms=185\navailability=0.995010\nasync_accept_ms=35\n"}} -->
```python
latencies_ms = [8, 12, 15, 40, 110]
availability = 1.0
for component in range(5):
    availability *= 0.999

print(f"latency_ms={sum(latencies_ms)}")
print(f"availability={availability:.6f}")
print(f"async_accept_ms={sum(latencies_ms[:3])}")
```

The synthetic calculation compares a five-hop required path (185 ms modeled latency) with accepting durable intent after three bounded layers (35 ms), then doing policy/provider work asynchronously where contract permits. It is not an SLO forecast.

### Propagate identity, revisions, and operation context

Carry authenticated principal/tenant, request/correlation ID, domain object UID/generation, policy revision, effective-plan digest, workflow/operation ID, adapter/provider effect ID, and recovery epoch where relevant. Not every value belongs in every user response, but cross-layer evidence must join unambiguously.

Correlation IDs connect telemetry; they do not deduplicate effects. Idempotency keys identify a logical operation. Object UID prevents name-reuse collision. Generation ties status to intent. Policy and composition revisions explain resolution. Keep these meanings distinct.

Do not put tokens, secrets, or sensitive full objects in headers, events, logs, or trace attributes. Propagate least information and use secure lookups at authorized boundaries.

Standardize context names and formats across domains so incident tools can join them, while controlling high-cardinality metrics. Per-object identifiers usually belong in logs/traces/audit, not unbounded metric labels.

### Define cross-layer failure contracts

Every call states deadline, retrying owner, safe retry conditions, idempotency, concurrency preconditions, circuit-breaking, error translation, and degraded mode. If each layer retries three times, a single request can create exponential amplification.

Retry where fresh information or progress is possible. Gateways may retry idempotent transport failures before acceptance; reconcilers own outcome retries after durable acceptance; adapters implement provider-specific observation and backoff. A caller must know whether failure occurred before or after acceptance.

Bulkhead by domain and provider so one outage does not consume every worker, connection, or API priority. Shed optional catalog refresh, previews, analytics, and recommendations before lifecycle/security work.

Expose layer-local health and end-to-end journey conditions. A healthy portal with stalled workflows is not a healthy provisioning capability; a failed catalog search need not make existing runtime reconciliation unavailable.

### Choose deployment boundaries from evidence

Start with logical modularity. Split deployment when independent scaling, security isolation, data classification, availability, release cadence, technology, or accountable ownership produces material benefit. Network boundaries add latency, authentication, version skew, retries, observability, and operational cost.

A modular monolith with enforced package boundaries can be better than chatty microservices. Conversely, a provider adapter holding broad cloud credentials may merit isolation even at modest scale.

Test whether a proposed service owns data and a coherent capability. A thin remote wrapper around one function can add failure without autonomy. A giant “platform backend” that owns everything prevents isolation.

Document which logical layers co-deploy and which failure domains they share. Independent replicas in one cluster/database/identity domain are not independent availability.

### Version boundaries in compatible order

Version schemas, domain APIs, policy inputs/results, workflow checkpoints, event schemas, adapter contracts, and read models. Consumers tolerate additive fields and unknown enum behavior according to contract; producers do not assume every consumer upgraded.

Use expand/migrate/contract: deploy consumers that understand both, expand producer/store, migrate state/traffic, observe, then remove old. Avoid coordinated flag days across portal, API, controller, policy, and providers.

Events and durable checkpoints live longer than processes. Keep old decoders/converters until retention, replay, in-flight work, and backups no longer contain old forms.

Provider adapter upgrades require compatibility with existing effects and identifiers. A new client library can change default retry or pagination behavior without changing the domain schema; conformance tests catch it.

### Observe without making telemetry authoritative

Define service/journey metrics by layer: request admission, policy decision, durable acceptance, queue age, reconciliation/action latency, adapter throttling/errors, status convergence, catalog lag, event backlog, and user outcome.

Trace synchronous requests and asynchronous work using durable links rather than assuming one continuous span survives hours. Logs/audit capture decisions and effects; metrics aggregate bounded dimensions; traces diagnose paths. None replaces stored intent or checkpoints.

Monitor dependency graph and synchronous cut. A new portal feature that calls four backends may silently worsen availability. Use contract tests and architectural checks as well as dashboards.

Redact secrets and tenant data. Observability pipelines are additional systems with retention and access policies, not harmless debugging sinks.

### Recover and retire by layer

Restore authorities before derived views: identity/trust, domain schemas/state, policy/class revisions, workflow checkpoints, provider credentials/identities, then catalogs/search/events as their contracts require. Fence old actors and invalidate caches.

Compare restored intent/workflow with current provider reality. Events emitted before rollback may replay; use event IDs, source revisions, object UID, operation identity, and epoch to reject stale effects. Rebuild read models from authority rather than treating incomplete retention as history.

Retire a layer by inventorying callers, data, events, credentials, policies, in-flight work, effects, backups, SLOs, and operational runbooks. Route through a compatible successor, measure zero use, then remove in dependency order.

Do not remove a converter, adapter, event decoder, or workflow implementation while stored/in-flight/backed-up state still requires it. Portal removal is only experience retirement.

## Definitions and Notation

Let $L$ be logical layers and $G=(L,E)$ their dependency graph. Edge $a\rightarrow b$ means $a$ consumes a versioned contract owned by $b$. Let $P\subseteq L$ be the required synchronous path for an operation, $t_i$ component latency, $t_{ij}$ boundary latency, and $A_i$ modeled component availability.

For a serial path,

$$T_P=\sum_{i\in P}t_i+\sum_{(i,j)\in P}t_{ij}.$$

Under an explicit independence approximation,

$$A_P=\prod_{i\in P}A_i.$$

Common-cause dependence invalidates simple multiplication; use measured joint behavior and fault tests for claims. For parallel required branches, completion latency is governed by the slowest branch plus coordination.

Let $u,g$ be object UID and generation; $p$ policy revision; $c$ composition revision; $o$ logical operation ID; $e$ provider effect identity; $x$ event ID; and $h$ recovery epoch. These form a causality/authority tuple, while a request or trace ID $q$ is correlation evidence only.

A fact has authority $S(f)$, source revision $r_f$, observation time $t_f$, and freshness policy $\Delta_f$. A derived view may be used for a decision only if the contract permits it and $now-t_f\leq\Delta_f$; destructive actions normally reread authority.

## Mechanisms, Invariants, or Proof Structure

### Layer-design protocol

1. Inventory user journeys, control paths, data, identities, effects, and existing tools.
2. Assign each decision and fact one owner/system of record.
3. Define logical layers and allowed dependency edges before deployments.
4. Specify contracts: schema, identity, revision, errors, deadlines, retries, idempotency, freshness, security, SLO, recovery, retirement.
5. Draw synchronous cuts for create/read/update/delete/recovery and remove volatile dependencies from acknowledgement paths.
6. Place authorization and policy enforcement at consequence boundaries.
7. Persist desired state and long-running progress; make queues/events replayable hints or facts.
8. Isolate provider semantics behind conformance-tested adapters.
9. Add backpressure, bulkheads, degraded modes, and semantic observability.
10. Test version skew, duplicate/reorder/loss, partial failure, restore, failover, and component removal.

### Single-semantic-owner invariant

Each domain field, default, transition, condition, and policy decision has one authoritative semantic owner. Other layers render, cache, or enforce the result without independently redefining it. This prevents portal/API/controller disagreement.

### Durable-acceptance invariant

Once a client receives accepted identity/revision, intent and sufficient work-discovery evidence survive process failure. Subsequent retries with the same operation semantics do not create duplicate authoritative intent or effects.

### Authority/freshness invariant

Derived views identify source and freshness. Security-sensitive, destructive, ownership-transfer, and adoption decisions reread authoritative identity/revision. Cache speed never silently weakens correctness.

### Retry-ownership invariant

Exactly one layer owns outcome retries for a given stage. Transport retries cease once durable acceptance is known; reconciliation owns progress retries; adapters own provider-specific retry/observation within that attempt contract.

### Dependency-graph argument

An unmediated cycle—portal depends on catalog status, catalog synchronously depends on workflow, workflow callback depends on portal—has no clear recovery/root authority and can deadlock or amplify. Orient writes toward authority and publish changes outward asynchronously. Feedback becomes a new versioned observation consumed by an owner, not a peer rewriting the source. This is an architectural proof sketch, not proof that every acyclic graph is live.

### Synchronous-cut review

For every operation list required components and common dependencies; sum latency budgets; calculate an explicitly qualified availability approximation; inject failures; and verify allowed degraded behavior. Reject a new synchronous dependency unless it is required for correctness at acknowledgement time.

### Layer verification matrix

Cover portal absent, gateway identity failure, policy slow/unavailable/stale, API partial commit, queue unavailable, duplicate/out-of-order event, workflow crash, adapter timeout/throttle/version change, provider partial effect, catalog/search lag, telemetry loss, tenant overload, schema/policy/controller version skew, backup restore, external-ahead effect, old actor reconnect, and retirement of each consumer/provider.

## Alternatives and Trade-Offs

### Logical layers versus microservices

Logical modules give clarity without network cost; microservices add isolation and scaling but create distributed failure/versioning. Split only for evidence-based boundaries.

### Thin gateway versus business gateway

A thin gateway centralizes transport controls and preserves domain ownership. Business logic at the edge can give fast responses but duplicates semantics and couples all APIs to one deployment.

### Synchronous policy versus local/versioned policy

Remote policy centralizes change but joins latency/availability paths. Local bundles improve bounded admission but require secure distribution and revision evidence. Choose by decision freshness and consequence.

### Orchestration versus choreography

Orchestration exposes one workflow and checkpoints complex sequences but centralizes coordination. Events decouple timing but obscure global progress and compensation. Combine explicit workflow for one owned journey with events for notification.

### Shared platform backend versus capability services

One backend simplifies initial operation and shared facilities but accumulates credentials, coupling, and blast radius. Capability-aligned services isolate ownership but require consistent standards. Preserve logical boundaries either way.

### Shared database versus database per service

Shared infrastructure is simpler and can support transactions but tempts cross-owner tables. Separate stores improve autonomy/recovery isolation at operational cost. Schema ownership matters more than slogans.

### Direct provider access versus adapters

Direct calls reduce layers and expose full features but leak credentials/types and repeat failure logic. Adapters normalize capability behavior but can become lowest-common-denominator bottlenecks. Keep expert surfaces explicit.

### Events versus authoritative polling/watch

Events reduce scanning and distribute facts, but delivery/retention/schema complexity remains. Rereading authority repairs gaps; high-scale providers may require event plus periodic inventory.

### Fast cached reads versus authoritative reads

Caches improve experience and protect dependencies but introduce staleness. Use them for discovery and bounded display; revalidate consequences against authority.

### Immediate outcome versus durable asynchronous acceptance

Synchronous completion feels simple but couples clients to long, failure-prone provider work. Durable acceptance needs status/operations but improves resilience and retry clarity.

### One SLO versus layer and journey SLOs

One platform availability number is easy to communicate but hides which journeys work. Layer indicators diagnose; journey SLOs express user outcome. Use both with named scope.

### Universal abstraction versus domain-specific stacks

One universal layer reduces apparent duplication but becomes generic and central. Domain stacks preserve semantics and blast radius but need shared identity/audit/conventions. Standardize cross-cutting contracts, not all domain logic.

## Failure Modes and Misconceptions

1. **“More boxes mean better layering.”** Boundaries require owned decisions and contracts.
2. **“Each layer should be a service.”** Network deployment is a trade-off, not the definition.
3. **“The portal is the platform.”** It is one replaceable experience over domain capabilities.
4. **“Client validation protects the API.”** Direct clients bypass it; admission is authoritative.
5. **“The gateway already authorized it.”** Later effects require current domain context.
6. **“Catalog data is truth.”** It is often a derived view with lag and incomplete ownership.
7. **“Events eliminate coupling.”** Schemas, brokers, retention, ordering, and semantics remain dependencies.
8. **“The queue is the workflow store.”** Delivery state is not complete domain progress.
9. **“At-least-once is nearly exactly-once.”** Business idempotency still needs durable identity.
10. **“A trace ID is an idempotency key.”** Correlation and operation identity have different lifecycles.
11. **“Retries improve reliability everywhere.”** Layered retries amplify load and duplicates.
12. **“Provider errors should pass through.”** Stable domain remediation and operator diagnostics differ.
13. **“Adapters should decide policy.”** That hides semantics and prevents reuse.
14. **“Five 99.9% services produce 99.9%.”** Required independent availabilities multiply; correlation can worsen it.
15. **“Asynchronous means eventually succeeds.”** It means durable progress/failure can be observed.
16. **“Shared storage is always a monolith.”** Undocumented shared ownership is the core problem.
17. **“Microservices isolate failure automatically.”** Shared identity, cluster, database, DNS, and rollout can correlate them.
18. **“Telemetry can reconstruct state.”** sampling, loss, redaction, and retention make it evidence, not authority.
19. **“Version only the public API.”** policies, events, checkpoints, adapters, and backups outlive releases.
20. **“Removing a plugin retires a capability.”** callers, data, effects, work, credentials, and recovery paths remain.

## Worked Examples

### Example 1

**Situation.** Portal code defaults production databases to `critical`, while Git submissions default to `standard`.

**Reasoning.** Move default resolution to the domain/policy contract and expose effective class revision. Both interfaces show the same result.

**Conclusion.** Experience-specific semantics create two APIs.

### Example 2

**Situation.** Creating a service synchronously calls identity, catalog, policy, source control, workflow, Kubernetes, and cloud APIs.

**Reasoning.** Keep authentication, deterministic admission/policy, and durable intent in the acceptance cut; reconcile integrations asynchronously with status and idempotency.

**Conclusion.** Minimize the synchronous cut to correctness-critical work.

### Example 3

**Situation.** Search is stale and shows a deleted owner during resource transfer.

**Reasoning.** The UI refreshes authoritative ownership with revision before submitting transfer; audit binds both identities.

**Conclusion.** Cached discovery cannot authorize consequence.

### Example 4

**Situation.** Gateway retries a timed-out create while the API committed it.

**Reasoning.** Client operation ID and server idempotency return the same UID/revision; reconciliation performs effects once by separate effect identity.

**Conclusion.** Acceptance ambiguity needs protocol identity, not hope.

### Example 5

**Situation.** Policy service is down during a destructive deletion.

**Reasoning.** The domain fails closed for new destructive authorization, continues already authorized reversible cleanup as contracted, and preserves emergency approval evidence.

**Conclusion.** Failure policy is decision- and consequence-specific.

### Example 6

**Situation.** One cloud throttles database operations and fills the global queue.

**Reasoning.** Provider/tenant bulkheads, circuit breaking, fair queues, and domain conditions isolate it while other adapters progress.

**Conclusion.** Adapter separation needs resource isolation too.

### Example 7

**Situation.** A duplicate event asks catalog and workflow consumers to process generation 12 twice.

**Reasoning.** Catalog upserts by source UID/revision; workflow rereads intent/checkpoint and makes no duplicate effect. Event ID supports inbox evidence.

**Conclusion.** Consumers assume duplicate delivery.

### Example 8

**Situation.** After restore, workflow state is old but provider resources are new.

**Reasoning.** Fence old actors, inventory provider effects by UID/operation, classify and adopt matching outcomes, quarantine ambiguity, then rebuild catalog/events.

**Conclusion.** Restore authorities and external reality before derived views.

### Example 9

**Situation.** A platform team proposes splitting every adapter method into a remote service.

**Reasoning.** Credential isolation justifies adapter deployment, but method-level services add no data ownership or scale boundary. Keep methods in one capability adapter service.

**Conclusion.** Deployment boundaries need coherent autonomy.

### Example 10

**Situation.** The portal plugin is removed, yet Git clients and finalizing resources remain.

**Reasoning.** Keep domain API/controller/adapter, migrate callers, finish or transfer effects, measure zero use, then retire schemas and recovery artifacts.

**Conclusion.** An experience lifecycle is not the capability lifecycle.

## Cross-Program Connections

1. **Software Architecture:** dependency inversion, ports/adapters, modularity, cohesion, and coupling define layers.
2. **API & Service Engineering:** gateways, contracts, idempotency, versions, errors, quotas, and asynchronous operations shape boundaries.
3. **Distributed Systems:** partial failure, delivery semantics, causality, retries, fencing, and consistency govern cross-layer behavior.
4. **Security Engineering:** trust boundaries, least privilege, confused deputy, policy enforcement, credentials, and audit govern authority.
5. **Database Systems:** systems of record, transactions, outbox/inbox, materialized views, migration, and restore govern state.
6. **Reliability Engineering:** SLOs, tail latency, availability composition, bulkheads, backpressure, and recovery quantify design.
7. **Product Engineering:** coherent journeys across portal/CLI/Git and capability ownership keep decomposition user-centered.
8. **Data Engineering:** event schemas, replay, checkpoints, lineage, freshness, and derived views parallel platform state flow.
9. **Networking:** proxies, TLS, routing, timeouts, load balancing, and failure domains shape physical boundaries.
10. **Organizational Design:** team ownership and cognitive load influence deployment, escalation, and contract stewardship.

## References

1. CNCF TAG App Delivery. [CNCF Platforms White Paper](https://github.com/cncf/tag-app-delivery/blob/main/platforms-whitepaper/latest/index.md). Retrieved 2026-09-02.
2. Kubernetes. [Kubernetes API Concepts](https://kubernetes.io/docs/reference/using-api/api-concepts/). Retrieved 2026-09-02.
3. Kubernetes. [Extending the Kubernetes API](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/). Retrieved 2026-09-02.
4. Kubernetes. [Kubernetes API Aggregation Layer](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/apiserver-aggregation/). Retrieved 2026-09-02.
5. Kubernetes. [Controllers](https://kubernetes.io/docs/concepts/architecture/controller/). Retrieved 2026-09-02.
6. Kubernetes. [Server-Side Apply](https://kubernetes.io/docs/reference/using-api/server-side-apply/). Retrieved 2026-09-02.
7. Kubernetes. [API Priority and Fairness](https://kubernetes.io/docs/concepts/cluster-administration/flow-control/). Retrieved 2026-09-02.
8. Crossplane. [Composite Resource Definitions](https://docs.crossplane.io/latest/composition/composite-resource-definitions/). Retrieved 2026-09-02.
9. Crossplane. [Compositions](https://docs.crossplane.io/latest/composition/compositions/). Retrieved 2026-09-02.
10. Backstage. [Architecture Overview](https://backstage.io/docs/overview/architecture-overview/). Retrieved 2026-09-02.
11. Backstage. [Backend System Architecture](https://backstage.io/docs/backend-system/architecture/). Retrieved 2026-09-02.
12. Backstage. [Backend Plugins](https://backstage.io/docs/backend-system/architecture/plugins/). Retrieved 2026-09-02.
13. OpenGitOps. [GitOps Principles](https://opengitops.dev/). Retrieved 2026-09-02.
14. OpenTelemetry. [General Semantic Convention Attributes](https://opentelemetry.io/docs/specs/semconv/general/attributes/). Retrieved 2026-09-02.

## Exercises

### Exercise 1

Layer an internal `DataService` platform across portal/CLI/Git, access, domain API, policy, reconciliation/workflow, two providers, catalog/events, and observability. Assign authority, contracts, and allowed edges.

### Exercise 2

Analyze a synchronous create path with component latencies and availability. Redesign it for durable asynchronous acceptance, state assumptions, and define user-visible completion.

### Exercise 3

Design identity, authorization, revision, correlation, operation, event, and provider-effect context propagation without leaking secrets or confusing their purposes.

### Exercise 4

Create a fault and recovery plan for policy outage, duplicate events, provider throttle, stale catalog, control-state restore, and old-worker reconnection. State bulkheads and authoritative rereads.

### Exercise 5

Plan an expand/migrate/contract evolution and eventual retirement spanning portal, API version, policy bundle, workflow checkpoint, event schema, adapter contract, stored objects, effects, and backups.

## Answers to the Exercises

### Answer 1

Treat portal/CLI/Git as experience projections using one generated/documented domain client. The access layer authenticates, routes, limits, and forwards verifiable identity. The `DataService` API owns schema, spec/status, lifecycle, errors, and authoritative desired state. Policy owns tenant entitlement, class, residency, quota, and deletion authorization at identified revisions. Reconciliation owns convergence; separate immutable workflow resources own restore/migration approvals and terminal progress.

PostgreSQL adapters own provider credentials, API translation, throttling, observation, idempotency, and normalized errors. They consume effective capability plans but cannot decide tenant policy. Catalog/search derive resource, owner, and status views with source revisions. An outbox publishes change events; consumers are idempotent and can rebuild. Observability records layer and journey evidence but never replaces state.

Dependencies flow experience→domain contract, domain→policy port/state, reconciler→domain/policy/dependency ports, and reconciler→adapter. Updates return through authoritative status and events, not callbacks that mutate spec. Direct API remains usable without portal/catalog; one provider failure is bulkheaded; catalog can rebuild.

### Answer 2

Suppose gateway, identity, API, policy, workflow, catalog, and provider have modeled serial latencies 8, 12, 15, 40, 35, 25, and 300 ms: the path is 435 ms before network/tail effects. At 99.9% independent availability each, the approximation is $0.999^7\approx0.99302$. This is optimistic if they share cluster, DNS, identity, or database.

Keep gateway/identity/API plus bounded local or highly available deterministic policy in the synchronous cut. Commit intent and reliable work evidence transactionally, return UID/generation and `Accepted` status, then let reconciliation call workflow/provider and publish derived views. If the bounded policy is 40 ms, modeled acknowledgement is 75 ms; moving policy asynchronously is valid only if no forbidden intent can be durably accepted or effects remain safely blocked.

User-visible completion is a current-generation domain condition proving the promised endpoint, identity, recovery class, and dependencies—not queue empty or provider call returned. Status distinguishes accepted, policy blocked, progressing, ready, degraded, and terminal operation outcomes.

### Answer 3

At ingress authenticate principal and tenant; exchange external token for scoped internal identity rather than trusting raw headers. Carry object UID/generation after persistence, policy revision and effective-plan digest after decision, workflow/operation ID for the logical long-running action, event ID/source revision for delivery, provider effect ID for observation/adoption, and recovery epoch after failover.

Use request/trace correlation IDs only for telemetry. Use client operation/idempotency ID for repeated submission, and distinct stable provider operation IDs for effects. Audit joins principal, tenant, object, policy, workflow, adapter/effect, and result. Logs/traces redact tokens, secret values, full sensitive specs, and provider credentials. Metrics use bounded dimensions rather than raw IDs.

Receivers authenticate callers and validate that context matches their authoritative object. Long-running workers reauthorize current consequence rather than replaying stale browser authority. Events contain references and safe facts, not bearer credentials; consumers fetch sensitive data through authorized channels.

### Answer 4

For policy outage, fail closed on new/destructive decisions, use only explicitly freshness-bounded safe cached decisions, reserve recovery access, and keep unrelated reads/reversible work. Duplicate events are deduplicated by event inbox and, more importantly, consumers reread source UID/revision and checkpoints. Provider throttle opens a provider circuit, applies provider/tenant concurrency, delays work with jitter, and leaves other providers progressing.

Stale catalog is marked with source revision/time; creation can continue against domain authority, while destructive ownership actions force authoritative reread. After control-state restore, fence old workers, restore schemas/policy/checkpoints/keys, inventory providers by UID/operation/effect, classify external-ahead state, and adopt or quarantine before mutation. Rebuild catalog/search and republish/replay safe events from authority.

An old worker reconnecting has stale epoch/lease and scoped credentials revoked; provider conditional operations reject it. Fault tests combine these cases, because policy outage during restore or catalog lag during transfer is more revealing. Verify domain outcomes, no duplicate/cross-tenant effects, fair queue drainage, stale-authority denial, and renewed backups.

### Answer 5

Inventory every version and consumer, including Git manifests, portal/CLI/SDK, policy inputs, workflow checkpoints, event retention, adapter effects, stored objects, finalizers, audit, and backups. First deploy readers/consumers that accept old and new forms. Expand stores and API serving, ship converters and dual-compatible policy/workflow/adapter code, then emit the new event schema with versioned consumers.

Migrate objects and in-flight work using UID, generation, operation/effect identity, and checkpoint mapping. Canary policy and adapter revisions, compare semantic outcomes, and retain rollback while effects remain reversible. Provider changes already committed require forward recovery, not merely binary rollback. Measure old API requests, policy inputs, checkpoint versions, event consumers/backlog, adapter calls, stored versions, and effects.

Contract only after observation windows show zero old use, retained events/backups no longer require old decoders or an archived recovery environment preserves them, all finalizers/effects are handled, and restore is tested. To retire the capability, stop new intent, migrate/transfer/delete resources, revoke credentials, drain work/events, remove derived views, then remove controllers/adapters/API/converters and obsolete recovery material in dependency order.
