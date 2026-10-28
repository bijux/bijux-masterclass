---
module_id: SARCH-039
program: Software Engineering: Software Architecture
level: 1
module_number: 39
title: Microservices Architecture
status: complete
last_verified: 2026-09-06
---

# Microservices Architecture

## One-Page Review

### Governing question

When do independently deployable, capability-aligned services create enough organizational, scaling, release, and fault-isolation value to justify distributed data, reliability, security, testing, and operational cost?

### Essential definitions

- A **microservice** is an independently deployable service with a cohesive capability, an explicit contract, meaningful control of its data and runtime, and accountable ownership. “Micro” describes bounded scope, not a line or process count.
- **Microservices architecture** composes a product from multiple such services that collaborate across process or network boundaries.
- **Independent deployment** means one service can be changed and released without requiring coordinated releases of unaffected services, within supported contracts.
- A **bounded context** is a boundary within which a domain model and its terms have a specific consistent meaning; it is evidence for service boundaries, not an automatic one-to-one rule.
- **Data authority** is responsibility for the meaning, invariants, writes, lifecycle, and access policy of data.
- A **distributed monolith** has separate deployments but retains tightly coupled change, data, release, or failure assumptions.
- A **synchronous dependency** requires a response during the caller's operation; an **asynchronous dependency** communicates through durable messages whose acceptance, delivery, processing, and business outcomes remain distinct.
- **Eventual consistency** means replicas or derived views may temporarily differ and converge under stated assumptions; it does not mean “probably correct later.”
- A **compensating action** is a new domain effect that mitigates a prior committed effect; it is not rollback through time.
- A **platform capability** supplies reusable delivery and operational mechanisms while leaving domain ownership with service teams.

### Central model, mechanism, or theorem

Represent services as a directed graph $D=(S,E)$. An edge $(a,b)$ means service $a$ depends on an observable contract of $b$. Annotate edges with interaction form, criticality, latency budget, data semantics, compatibility, and fallback. A healthy boundary should reduce coordinated change while accepting explicit runtime dependency.

For an observed release window, define

$$
CoordinationRate(s)=\frac{releases\ of\ s\ requiring\ another\ service\ release}{all\ releases\ of\ s}.
$$

The ratio is diagnostic evidence, not a universal threshold. High values can reveal shared schemas, breaking contracts, coupled tests, or inseparable responsibilities. Decomposition succeeds only if contract, data, ownership, release, and failure boundaries become meaningfully independent.

### Critical invariants

- derive boundaries from capabilities, authority, change, workload, and ownership rather than entity or repository counts;
- give each service an accountable team and enough control to build, deploy, operate, secure, and retire it;
- prohibit ungoverned cross-service writes and private-schema dependencies;
- version semantic contracts for mixed deployment and rollback;
- keep local invariants and transactions within one authority where possible;
- model cross-service workflows with identity, durable progress, idempotency, compensation, reconciliation, and unknown outcomes;
- bound synchronous depth, fan-out, retries, deadlines, queues, payloads, concurrency, and resource use;
- design failure containment and graceful degradation rather than assuming process separation isolates effects;
- authenticate services and principals, authorize each operation, minimize data, and rotate credentials safely;
- automate repeatable build, test, artifact, deployment, rollback, telemetry, and ownership controls;
- observe user outcomes, service outcomes, dependencies, saturation, and deployment correlation;
- retain a credible modular-monolith or coarser-service alternative and reverse poor splits when evidence warrants.

### Common failures

Frequent failures include splitting by table or CRUD entity; equating containers with microservices; creating a service per team or developer; sharing one writable database; requiring lockstep releases; using a synchronous call for every former function; putting business logic in gateways or meshes; giving every service a different stack without support; multiplying retries; attempting global ACID transactions by default; confusing event publication with completed work; hiding ownership in a platform team; testing only isolated mocks; centralizing shared domain libraries; ignoring version skew and rollback; and adopting the style before delivery and operational capabilities can sustain it.

### Compact example

Orders and pricing change together in 18 of 20 releases, share tables, and require one end-to-end test environment. Calling them separate microservices does not create autonomy. Either redraw the boundary around the cohesive capability or first separate data, contracts, tests, and release compatibility. If no independent scaling, ownership, security, or lifecycle need exists, a modular monolith is the simpler sound design.

### Connections

[SARCH-032](032-modular-monoliths.md) provides the primary alternative; [SARCH-035](035-event-driven-architecture.md) and [SARCH-036](036-client-server-architecture.md) provide interaction semantics; [SARCH-038](038-service-oriented-architecture.md) supplies the broader service-orientation lineage. [SARCH-040](../ROADMAP.md) next chooses among styles from forces. Distributed Systems and API Engineering own detailed coordination and protocol mechanisms.

## Governing Question

Separating capabilities into independently deployable services can let teams release at different rates, scale unlike workloads, isolate selected failures and privileges, and use technology suited to a bounded problem. These are real benefits when a product, organization, and workload need them.

The separation also converts local calls into distributed interactions, local transactions into workflows, one deployment into many, and one security boundary into a network of identities. It demands mature automation, observability, compatibility, ownership, and incident response. The governing question is therefore not “How many microservices should we have?” but whether particular boundaries buy enough independence to repay their recurring cost.

## Why This Matters

Microservices are easy to imitate superficially. Multiple repositories, containers, HTTP endpoints, and deployment manifests produce the appearance of the style. If services share database writes, release together, depend on private schemas, and fail as one synchronous chain, the result is a distributed monolith: the system pays network and operational cost without gaining meaningful autonomy.

A rigorous architecture connects decomposition to desired outcomes. It identifies which teams need release independence, which workloads need isolated scaling, which failures or privileges need containment, and which domain capabilities have coherent authority. It then supplies the contracts, data boundaries, platform, tests, and operations required to make those outcomes true.

## Prerequisites and Retrieval

Retrieve service, capability, contract, bounded context, aggregate, invariant, authority, transaction, deployment unit, process, partial failure, latency, availability, idempotency, timeout, retry, message, event, queue, compensation, eventual consistency, version skew, observability, service-level objective, least privilege, team ownership, platform, and total cost of ownership.

From SARCH-015 retrieve evolvability tactics; SARCH-024 and SARCH-025 provide runtime and deployment views; SARCH-032 provides modular-monolith boundaries and extraction seams; SARCH-035 provides asynchronous facts and delivery semantics; SARCH-036 provides remote ambiguity and capacity; and SARCH-038 provides service contracts, composition, and governance.

## Learning Objectives

After completing this module, you should be able to:

1. define a microservice using capability, deployment, data, contract, and ownership properties;
2. distinguish microservices from SOA, modular monoliths, nanoservices, and distributed monoliths;
3. identify service candidates from domain, change, workload, security, and organizational evidence;
4. design data ownership and cross-service workflows without hidden shared writes;
5. bound synchronous dependencies, fan-out, retries, latency, and failure propagation;
6. preserve contract compatibility through independent deployment and rollback;
7. define team and platform responsibilities without centralizing domain ownership;
8. design security, observability, testing, delivery, and recovery for many services;
9. plan incremental extraction and recognize when to merge or retain a monolith;
10. evaluate the style from measurable outcomes and lifecycle cost rather than popularity.

## Core Exposition

**Define the style by independence, not size.** Lewis and Fowler characterized microservices through small services running in their own processes, business-capability organization, automated deployment, decentralized control, and evolutionary design [1]. These are related tendencies, not a mechanical checklist. A 500-line service can be too broad in authority; a large service can be cohesive and independently deployable.

Use “micro” as a prompt to keep scope understandable, not as a numeric target. Count responsibilities, reasons to change, authorities, deployments, dependencies, and operational burden. A tiny service that cannot release or operate independently is a nanoservice, not a success.

**Begin from forces and scenarios.** Candidate benefits include independent release cadence, isolated scaling, fault containment, security separation, regulatory boundary, technology fit, acquisition boundary, and team autonomy. State measurable scenarios: “pricing must deploy weekly without rebuilding checkout,” or “image processing must scale independently from account traffic.”

If the only driver is fashion, resume writing requirements. A modular monolith preserves many domain boundaries without distribution. The future possibility of scale is not enough unless evidence shows a likely bottleneck and a partitionable workload.

**Align services with cohesive capabilities.** Business capabilities and bounded contexts often provide evidence because they group language, policy, state, and change. Evans's bounded-context concept recognizes that a model's meaning is local to a boundary [2]. It does not require one service per aggregate or bounded context. A context may be one service, several services under one team, or a module in a monolith.

Validate a candidate with change history, invariant ownership, data access, workload, failure policy, security, and consumer needs. Splitting “customer” into address, phone, and email services by noun creates remote CRUD and scatters customer policy. Splitting image transformation from account management can make sense when workload and failure behavior differ.

**Match architecture and team ownership.** Conway's law observes that system communication structures reflect organizational communication structures [3]. Use this as a design constraint, not a command to mirror every current reporting line. Stable product-aligned teams should own coherent capabilities end to end: semantics, code, data, deployment, on-call, security, cost, and retirement.

A service owned by nobody becomes shared risk. A service owned by a central operations team while domain teams throw code over the wall lacks product accountability. Platform teams can provide delivery and runtime capabilities, but they do not inherit business decisions.

**Make independent deployment real.** A service is independently deployable when its artifact, configuration, data changes, and contract evolution allow a release without simultaneous releases of unaffected consumers or providers. Separate repositories are neither necessary nor sufficient. A monorepo can build and release services independently; many repositories can still share a release train.

Test mixed versions and rollback. Use additive contracts and expand-compatible-contract data changes where appropriate. Avoid shared libraries that embed volatile domain models across every service. Small stable technical libraries can reduce repetition, but each upgrade and vulnerability becomes portfolio work.

**Own data through service contracts.** Each service should own the meaning, invariants, and writes for its data. Other services request capabilities or consume published facts rather than writing its tables. Physical infrastructure may be shared if logical ownership, credentials, schemas, backup, capacity, and failure effects remain controlled; “database per service” describes authority more than a mandatory server count.

Cross-service reads can use service queries, replicated read models, caches, or event-built projections. Each choice declares freshness, provenance, privacy, and failure. A reporting query should not join private production tables from every service and become an undocumented contract.

**Keep local transactions local.** Place invariants that require atomic enforcement within one service boundary. If two facts must always commit together, splitting their authority creates coordination burden and may indicate the boundary is wrong. A service may use a local ACID transaction for its state and an outbox to publish a fact after commit.

Cross-service business processes use durable identities and progress. Orchestration can record steps; choreography can react to facts. Define idempotency, preconditions, retries, timeouts, compensation, reconciliation, and manual states. Compensation is a new action and may be partial or impossible.

**Accept temporary inconsistency deliberately.** Derived views and independent authorities may not update simultaneously. State which values may lag, the convergence trigger, maximum expected delay or objective, conflict policy, and user experience. “Eventually consistent” without these details is an excuse rather than a model.

Some decisions require current authority and must call or colocate with it. Others can use timestamped projections. A checkout may need authoritative stock reservation but can display a slightly stale recommendation count. Match consistency to consequence.

**Choose interaction form per dependency.** Synchronous request-response fits immediate decisions and bounded results. It creates temporal availability coupling: caller progress waits for provider response. Asynchronous messages decouple time and can buffer load, but add duplicates, ordering, lag, storage, and outcome tracking.

Do not replace every local call with HTTP. Redraw operations around meaningful outcomes to avoid chatty sequences. Events should state facts owned by the publisher; commands target an authority. Avoid using a broker as a hidden synchronous RPC mechanism or treating publish acknowledgment as business completion.

**Map the runtime dependency graph.** Static source dependencies do not show service calls, message flows, identity providers, configuration, DNS, gateways, brokers, databases, or telemetry backends. Maintain a runtime view with required and optional edges, deadlines, fallbacks, capacity, and ownership.

Cycles often reveal unclear authority. A needs B for every request while B needs A for authorization can deadlock or recursively fail. Break the cycle by relocating policy, publishing a fact, creating a stable lower-level capability, or reconsidering the boundary.

**Bound synchronous depth and fan-out.** Required sequential calls accumulate latency. Required parallel calls inherit the slowest branch and multiply request volume. If a request fans to $n$ independent dependencies, each available with probability $a$, and all are required, the simplified success probability is $a^n$. At $a=0.999$ and $n=20$, it is about $0.98019$, before considering caller failure or correlation.

This product model is diagnostic, not a guarantee. Dependencies share networks, zones, credentials, and deploys. Reduce hard fan-out using cohesive services, projections, caches, batch operations, optional results, and asynchronous preparation.

**Control retries as load.** Every retry is additional work during a failure. Nested client, gateway, service, and library retries can multiply attempts. Give one layer responsibility, use stable operation identity, retry only safe transient failures, bound attempts and total time, add jitter, honor pushback, and stop when the caller's objective expires.

Circuit breakers can limit repeated calls to a failing dependency but create state, tuning, and recovery behavior. Bulkheads isolate resources but require correct pool sizes. Timeouts stop waiting; they do not cancel committed effects. These patterns support, but do not replace, capacity and correctness design.

**Design graceful degradation.** Classify dependencies as hard, soft, cached, deferred, or optional for each user outcome. If recommendations fail, checkout may continue; if authorization is unknown, payment may require reconciliation. A fallback must be simpler and safe under the same failure, not another equally fragile chain.

Test failure at boundaries: before request receipt, after commit before response, during message publication, while a projection lags, during credential rotation, and while a deployment rolls back. Verify the user-visible and business outcome, not merely a handled exception.

**Create a paved delivery path.** Many services multiply builds, artifacts, dependencies, configurations, deployments, secrets, policies, telemetry, and runbooks. Automate reproducible builds, dependency checks, immutable artifacts, progressive rollout, health checks, rollback, configuration validation, ownership metadata, and observability.

The Twelve-Factor App captured influential practices for deployable service applications, including explicit dependencies, externalized configuration, attached resources, disposability, and environment parity [4]. Treat it as durable historical guidance, not a complete architecture or security standard.

**Keep the platform a product.** A platform should reduce cognitive load through self-service interfaces, safe defaults, diagnostics, and supported runtime patterns. Service teams retain responsibility for domain behavior and production outcomes. A platform that requires tickets for every release recreates central coupling; a platform that exposes raw infrastructure without guardrails transfers complexity rather than reducing it.

Standardize undifferentiated mechanisms—identity bootstrap, artifact provenance, deployment, telemetry, secret delivery, traffic policy—when this improves safety. Allow variation only with ownership and lifecycle. Unbounded polyglot freedom increases patching, on-call, tooling, and hiring cost.

**Design service identity and authorization.** Network location is not authority. Authenticate service workloads and end principals, authorize each operation and resource, constrain delegation, rotate credentials, and preserve tenant context. Gateways or service meshes can establish secure channels and common policy, but business authorization belongs with the service that owns the resource.

Minimize data in requests, messages, logs, traces, and replicated views. Per-service stores do not automatically improve privacy; copies can proliferate through events. Govern purpose, retention, deletion, encryption, and access across every replica.

**Observe end-to-end and locally.** Each service needs health, work rate, errors, latency, saturation, dependency, deployment, and domain-outcome evidence. Correlate a logical operation across attempts without using trace identity as business idempotency. Record version and configuration so incidents can be tied to change.

Distributed tracing samples causal paths and helps locate latency. It does not prove transactions, message delivery, or business completion. Metrics can hide individual tenant failures; logs can leak sensitive context. Use bounded stable dimensions and domain reconciliation for correctness-critical outcomes.

Google's SRE material distinguishes service-level indicators, objectives, and error budgets as tools for reliability management [5]. A service SLO needs measurement scope and consumer relevance. Meeting every local SLO does not guarantee an end-to-end product objective when dependencies compose.

**Test at several boundaries.** Unit tests protect local logic. Component tests exercise one service with controlled dependencies. Contract tests check consumer-provider compatibility. Integration tests verify real infrastructure and protocols. End-to-end tests cover a small set of critical journeys. Production verification observes rollout and outcomes.

Avoid one giant shared test environment as the only release gate; it creates scheduling and data coupling. Consumer-driven contracts can reveal used behavior but may preserve poor designs or miss provider invariants. Provider contract suites and semantic review remain necessary.

**Evolve schemas and messages independently.** Producers and consumers coexist. Add fields with safe defaults, preserve unknown fields where appropriate, and never reuse identifiers for new meaning. Events may remain in logs longer than code versions; consumers can replay old representations. Define retention and upcasting or migration policy.

Database changes need expand, migrate, verify, and contract stages when old and new code overlap. A service must tolerate rollback after new code has written data. “Backward compatible API” is insufficient if storage, policy, or messages cannot roll back.

**Manage deployments as risk.** Small independent releases reduce change size only when artifacts and ownership are truly independent. Canary or progressive rollout can limit exposure, but cross-service behavior and low-volume faults may escape. Feature flags separate activation from deployment but need ownership, safe defaults, observation, and removal.

Do not deploy dozens of services simultaneously and call them independent. Correlate releases with errors and outcomes. Maintain the ability to stop, roll back, or roll forward without leaving contracts and data incoherent.

**Plan incident ownership.** A user failure can cross five teams. Define who leads the end-to-end incident, how dependency owners engage, where authoritative evidence lives, and which service can degrade. Shared dashboards do not replace decision rights.

On-call load is an architectural cost. Each new service adds alerts, patches, certificates, capacity, backup, restore, and failure modes. Include cognitive load and support maturity in decomposition decisions. Team Topologies frames cognitive load and team interaction as design concerns [6].

**Measure whether boundaries work.** Useful evidence includes change failure, lead time, independent release rate, coordinated-release rate, incident propagation, recovery time, SLO attainment, dependency depth, cross-service data access, security scope, cost, and team cognitive load. Metrics need context and cannot mechanically choose boundaries.

For a service with 20 releases, 18 requiring another service to deploy, $CoordinationRate=18/20=0.9$. Investigate: perhaps contracts break, a shared schema changes, tests are coupled, or the capabilities belong together. The ratio does not prove which repair is correct.

**Migrate incrementally.** Strengthen internal module and data boundaries before extraction. Choose a capability with clear ownership and a justified driver. Place a stable seam around it, redirect one interaction, migrate authority carefully, compare outcomes, and retain rollback. The strangler approach replaces bounded behavior gradually rather than rewriting everything at once [7].

Data migration is usually the hardest part. Define source of truth, dual-write avoidance or reconciliation, backfill, cutover, verification, and rollback. Do not run two authorities indefinitely. Publish ownership changes to every consumer.

**Merge when evidence says to.** A poor split is reversible architecture work, not failure of principle. Merge services that always change and deploy together, require synchronous chatty calls for one invariant, share one owner and workload, and gain no material isolation. Preserve internal modules inside the merged deployment.

Conversely, do not merge a service merely because it is operationally difficult if the difficulty reflects an essential security or ownership boundary. Improve the platform or contract when the boundary is justified.

**Compare honestly with SOA and modular monoliths.** Microservices inherit service-orientation principles but emphasize decentralized product-team ownership, independent deployment, automation, and smaller capability scope. Classical SOA often integrates heterogeneous enterprise systems through broader services and shared mediation. Neither label guarantees boundaries.

A modular monolith keeps calls, transactions, deployment, and debugging local while retaining strong module contracts. It is often the best starting and durable architecture. Extract only where distribution buys a named outcome.

## Definitions and Notation

Let services be vertices $S$ and runtime dependencies be directed edges $E$. For edge $e=(a,b)$, annotate interaction type $type(e)$, requiredness $req(e)$, deadline $d(e)$, retry policy $r(e)$, contract version $v(e)$, authority $owner(e)$, and fallback $f(e)$.

For service $s$ over release window $W$, let $R_s$ be all releases and $C_s\subseteq R_s$ those requiring a coordinated release of another service. Then $CoordinationRate(s)=|C_s|/|R_s|$ when $|R_s|>0$. Define the empty-window result as unavailable, not zero.

For $n$ independent equally available required dependencies with per-dependency availability $a$, the simplified series availability is $A=a^n$. For unequal values, $A=\prod_{i=1}^{n}a_i$. Independence and required-series structure are explicit assumptions.

For business operation $o$, attempts $A(o)$ share a stable operation identity where duplicate effects matter. Outcome belongs to $\{not\_received,accepted,committed,rejected,unknown,compensated,manual\}$ under an authoritative observer. Transport timeout is an observation, not one of these authoritative effects.

## Mechanisms, Invariants, or Proof Structure

**Capability invariant.** A service contains a cohesive capability and one authority for its local invariants. Entity count and process count do not define the boundary.

**Deployment invariant.** Supported service changes do not require simultaneous releases of unaffected services. Mixed versions and rollback are part of the contract evidence.

**Data invariant.** Each datum and invariant has one write authority. Replicas and projections carry provenance, freshness, and correction semantics; consumers do not mutate another service's private store.

**Remote-outcome argument.** After send and before authoritative terminal response, not-received and committed executions can produce the same timeout observation. Therefore a new attempt requires stable identity and safe duplicate or inquiry semantics; timeout does not imply rollback.

**Fan-out derivation.** Under independent equal availability $a$ and a requirement that all $n$ dependencies succeed, joint success probability is the product of all probabilities, $a^n$. Relaxing independence, equal availability, or all-required structure changes the model.

**Release-coupling invariant.** Separating deployment artifacts creates value only if contracts, data, tests, and operations permit independent change. Persistent lockstep releases are evidence against realized autonomy.

**Team invariant.** One accountable team owns each service's behavior and operation. Platform and enabling teams supply capabilities without becoming implicit domain owners.

**Resource invariant.** Calls, retries, queues, threads, connections, memory, storage, and telemetry have bounded admission and ownership. Failure cannot create unlimited recovery work.

**Security invariant.** Workload identity, principal identity, authorization, data purpose, and delegation remain explicit across every hop. Internal network placement creates no blanket trust.

**Evidence invariant.** Containers, repositories, passing tests, traces, independent deployments, and local SLOs each establish bounded facts. None alone proves microservice quality or product reliability.

## Alternatives and Trade-Offs

| Choice | Advantages | Costs and risks | Prefer when |
|---|---|---|---|
| Modular monolith | local transactions, low latency, simpler delivery and diagnosis | shared process, deployment, and scaling fate | one ownership group and workload can evolve coherently |
| Coarse service | fewer remote edges, clearer process and data authority | broader release surface; coarser scaling | capability and invariants are strongly cohesive |
| Fine microservice | targeted release, scaling, technology, and failure boundary | more calls, state coordination, security, and operations | independence produces a measured benefit |
| Synchronous request | immediate answer and direct error path | temporal coupling, tail latency, ambiguity, cascading failure | current authoritative decision is required |
| Asynchronous message | temporal decoupling, buffering, fan-out | duplicates, lag, ordering, storage, and progress tracking | delayed processing and explicit convergence are acceptable |
| Orchestrated workflow | visible progress, timeout, compensation, and audit owner | coordinator coupling and availability | one capability owns the composite outcome |
| Choreographed reactions | extensible participants and local autonomy | emergent flow and difficult completion diagnosis | reactions are independent consequences of durable facts |
| Shared database server | efficient infrastructure operation | correlated capacity and failure | logical ownership and credentials remain isolated |
| Shared writable schema | easy joins and local-style transactions | invisible coupling and ambiguous authority | generally avoid across service owners |
| Standardized stack | lower cognitive load and stronger paved path | less local technology freedom | operational scale and staffing favor consistency |
| Polyglot stack | technology fit and experimentation | patch, tooling, on-call, and hiring multiplication | bounded benefit has an accountable owner |
| Extracted service | independent lifecycle and enforcement boundary | migration and recurring distribution cost | a proven driver repays the cost |

## Failure Modes and Misconceptions

1. **“A microservice has fewer than N lines.”** Scope is architectural and operational, not a universal size threshold.
2. **“One container equals one microservice.”** Containers package processes; they do not establish capability, data, or release boundaries.
3. **“One team needs one service.”** A team may own several cohesive services or one modular deployment.
4. **“A bounded context must be a service.”** It is a semantic boundary and may remain a module.
5. **“Database per service requires one database server.”** Logical write authority matters; infrastructure can be shared carefully.
6. **“Shared tables are harmless if calls use APIs.”** Direct writes bypass contracts and preserve hidden coupling.
7. **“Independent repositories give independent deployment.”** Lockstep contracts, tests, data, and release policy can remain.
8. **“HTTP makes a function a service.”** Network transport adds failure without creating coherent capability.
9. **“Events eliminate coupling.”** Meaning, schema, timing, ordering, and consumer assumptions remain dependencies.
10. **“Eventually consistent means no guarantee.”** It needs convergence, freshness, conflict, and failure assumptions.
11. **“Compensation is rollback.”** It is a new effect and may leave irreversible consequences.
12. **“Retries improve reliability.”** Uncoordinated retries amplify failure and can duplicate effects.
13. **“A mesh owns service security.”** It can secure channels; domain authorization and data policy remain with services.
14. **“Distributed tracing proves a workflow completed.”** Traces are sampled observations, not an authoritative ledger.
15. **“More services increase team autonomy.”** Shared data, release trains, and central ticket queues can reduce it.
16. **“Migration must end with microservices.”** A modular monolith or coarser services may be the evidence-backed destination.

## Worked Examples

### Example 1

**Situation.** A six-person team proposes 30 services for 30 database entities.

**Reasoning.** Entity boundaries scatter invariants, create remote CRUD, and give a small team 30 artifacts, deployments, dashboards, credential sets, and recovery paths. No independent team, workload, security, or release need exists. Group the domain into cohesive modules inside one deployable application, enforce data ownership internally, and preserve extraction seams for evidence-backed future needs.

**Conclusion.** Service count must fit capability and operational ownership; entity count is not a decomposition rule.

### Example 2

**Situation.** Image processing consumes 80% of CPU during uploads while account operations remain light and latency-sensitive.

**Reasoning.** The workloads scale differently, image decoders process hostile input, and jobs can complete asynchronously. Extract an image-processing service with bounded input, content validation, isolated workers, job identity, quotas, and result events. Accounts retain user authority. A queue buffers demand, while upload status exposes accepted, processing, completed, rejected, and unknown states.

**Conclusion.** Independent scaling and failure containment justify this boundary when its data and outcome contract are explicit.

### Example 3

**Situation.** Order and pricing services have 20 releases each; 18 order releases require a simultaneous pricing release.

**Reasoning.** $CoordinationRate(order)=18/20=0.9$. Inspect causes rather than declaring a threshold violation. The teams discover a shared domain library, coupled database view, and breaking request changes. Options are stabilize a coarse pricing contract and eliminate shared writes, or merge responsibilities if one capability and team own them. Separate repositories do not fix the coupling.

**Conclusion.** A high coordination rate is evidence to investigate contract or boundary failure, not proof of one remedy.

### Example 4

**Situation.** A product page requires all 20 downstream services, each modeled with independent availability 0.999.

**Reasoning.** Under the deliberately simplified all-required independent model, success is $0.999^{20}\approx0.98019$, about $98.019\%$. This excludes the page service and shared infrastructure and ignores correlation. Redesign by using a product read model, batching coherent data, caching with freshness, and making recommendations or reviews optional rather than synchronously hard dependencies.

**Conclusion.** Large hard fan-out can defeat strong local availability; dependency structure matters more than service count.

### Example 5

**Situation.** Payment times out after an order sends `charge-842`; the order service wants to retry as `charge-843`.

**Reasoning.** The timeout cannot distinguish nonreceipt from committed charge. A new identity risks duplication. Query payment by `charge-842` or retry under the same idempotency scope and request fingerprint. If still unknown, persist reconciliation state and prevent fulfillment from inventing an outcome. A refund, if required after known commit, has its own stable identity and audit history.

**Conclusion.** Independent services require explicit operation identity and unknown-outcome handling.

### Example 6

**Situation.** Inventory publishes `StockChanged`, but a checkout projection may lag by 45 seconds.

**Reasoning.** The projection can support browsing if it shows or internally respects freshness, but it cannot authorize a final reservation. Checkout submits a reservation command with item, quantity, operation identity, and observed version to inventory authority. Inventory atomically accepts or rejects. The user interface handles changed availability rather than promising that event delivery made the view current.

**Conclusion.** Eventual read consistency and authoritative write decisions can coexist when freshness and authority are explicit.

### Example 7

**Situation.** A request passes through a client library, gateway, and three services; each layer retries up to three times.

**Reasoning.** In a worst-case nested sequence, one logical request can generate $3^5=243$ attempts at the deepest dependency if each layer independently exhausts three attempts. Even lower realized amplification can collapse a recovering service. Assign retry ownership at one boundary, propagate one deadline, use backoff and jitter, honor overload signals, and measure logical operations separately from attempts.

**Conclusion.** Retry composition is offered load; bounded coordination is part of reliability.

### Example 8

**Situation.** A shared `customer-model` library is imported by 42 services and changes a postal-address invariant.

**Reasoning.** Upgrading every service requires coordinated releases; not upgrading creates inconsistent meaning. The library has become a distributed domain model. Put address authority behind the responsible capability, publish stable value representations with context, and let other domains translate or store purpose-specific snapshots. Retain shared code only for stable technical types whose semantics and support are intentionally common.

**Conclusion.** Shared domain libraries can create compile-time distributed-monolith coupling.

### Example 9

**Situation.** A team extracts shipping from a monolith and plans two-way writes for a six-month migration.

**Reasoning.** Two authorities can diverge under partial failure. First create a monolith-owned seam and outbox, backfill shipping state with checksums and provenance, run the new service in comparison mode, then choose one write authority at cutover. Route writes through that authority and replicate facts one way. Keep a bounded rollback plan that accounts for data written after cutover; never rely on indefinitely synchronized dual writes.

**Conclusion.** Extraction succeeds when data authority moves explicitly, not when a second copy appears.

### Example 10

**Situation.** A clinical alert service must remain separate for regulatory and privilege reasons, but its team struggles with on-call load.

**Reasoning.** Merging it into a general application would widen access and weaken independent audit and deployment evidence. Keep the justified boundary, simplify its contract and dependency graph, and provide platform capabilities for identity, immutable artifacts, telemetry, safe rollout, backup, and runbooks. Assign a durable product team and test degraded operation. If the alert authority is unavailable, the clinical workflow follows an explicitly approved safe procedure rather than silently suppressing alerts.

**Conclusion.** Operational difficulty does not invalidate an essential safety boundary; architecture and platform must reduce its cost without erasing authority.

## Cross-Program Connections

- **Distributed Systems Engineering:** owns partial failure, time, ordering, replication, consistency, coordination, transactions, and fault-tolerance mechanisms used by services.
- **API and Service Engineering:** owns protocol semantics, contracts, compatibility, security, gateways, resilience, testing, and observability at service interfaces.
- **Software Design and Domain Modeling:** bounded contexts, aggregates, invariants, domain events, and context maps inform capability and data boundaries.
- **Database Engineering:** local transactions, schemas, indexes, migrations, replication, outbox, backup, and recovery support service data authority.
- **Software Delivery and Reliability Engineering:** CI/CD, artifacts, progressive delivery, SLOs, incidents, capacity, and recovery determine release and operational independence.
- **Platform Engineering:** paved paths, self-service, workload identity, deployment, telemetry, and policy reduce repeated operational complexity.
- **Security Engineering:** least privilege, workload identity, delegation, supply-chain assurance, segmentation, audit, and data minimization define trust boundaries.
- **Organizational and systems architecture:** team cognitive load, ownership, interface control, risk, and lifecycle shape the feasible service topology.

## References

1. James Lewis and Martin Fowler, “Microservices: a definition of this new architectural term,” 25 March 2014. <https://martinfowler.com/articles/microservices.html>
2. Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software*, Addison-Wesley, 2003.
3. Melvin E. Conway, “How Do Committees Invent?”, *Datamation* 14(4), 1968. <https://www.melconway.com/Home/Committees_Paper.html>
4. Adam Wiggins, *The Twelve-Factor App*, 2011. <https://12factor.net/>
5. Betsy Beyer, Chris Jones, Jennifer Petoff, and Niall Richard Murphy, eds., *Site Reliability Engineering: How Google Runs Production Systems*, O'Reilly Media, 2016. <https://sre.google/sre-book/table-of-contents/>
6. Matthew Skelton and Manuel Pais, *Team Topologies: Organizing Business and Technology for Fast Flow of Value*, 2nd ed., IT Revolution, 2025. <https://itrevolution.com/product/team-topologies/>
7. Martin Fowler, “Strangler Fig Application,” 29 June 2004. <https://martinfowler.com/bliki/StranglerFigApplication.html>
8. Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2nd ed., O'Reilly Media, 2021. <https://www.oreilly.com/library/view/building-microservices-2nd/9781492034018/>

## Exercises

### Exercise 1

Define microservice, independent deployment, bounded context, data authority, distributed monolith, and platform capability. Explain why a container and a repository establish none of these properties by themselves.

### Exercise 2

A request requires eight independent downstream services with modeled availability 0.997 each. Compute the simplified all-required success probability, show the expression, and give three reasons it is not a production guarantee.

### Exercise 3

Two services release separately but share writable tables, a domain library, and one end-to-end test environment. Diagnose whether they realize microservice autonomy and propose the smallest coherent repair options.

### Exercise 4

Compare synchronous calls, asynchronous messages, and a replicated read model for a checkout that needs price, stock, recommendations, and fraud information. Assign authority, freshness, and failure behavior.

### Exercise 5

A city wants independent services for emergency dispatch, traffic signals, hospital capacity, and public notifications. Design justified boundaries, interaction and data authority, unknown-outcome handling, security, platform support, degraded operation, ownership, and evidence. Identify one proposed split you would reject.

## Answers to the Exercises

### Answer 1

A **microservice** is a cohesive independently deployable service with explicit contract, meaningful data/runtime control, and accountable ownership. **Independent deployment** permits one service to release within supported contracts without simultaneous unaffected-service releases. A **bounded context** is a boundary of consistent domain meaning and is evidence, not a mandatory deployment. **Data authority** owns meaning, invariants, writes, lifecycle, and access. A **distributed monolith** separates processes while retaining coupled change, data, release, or failure. A **platform capability** supplies reusable self-service delivery or runtime mechanisms while domain teams retain outcomes. A container packages and isolates some runtime resources; a repository stores source history. Neither defines capability, authority, compatibility, owner, release policy, or operational independence.

### Answer 2

Under the stated equal, independent, all-required model,

$$
A=0.997^8\approx0.976250494,
$$

or about $97.6251\%$. It is not a guarantee because dependencies may share correlated infrastructure and deployments; measured availability definitions and time windows can differ; callers, networks, and identity systems are omitted; retries, caching, or degradation can change the requirement graph; and workload-dependent saturation violates a constant model. Any three with the correct calculation and assumptions earn full credit.

### Answer 3

They are separate deployment artifacts but not autonomous microservices. Cross-service writes bypass contracts and make data changes coupled; the domain library couples semantics and upgrades; the shared environment serializes release evidence. Two coherent repairs exist. If the responsibilities form one capability and gain no scaling, privilege, or lifecycle value, merge them into strong modules in one deployment. If separation has a proven driver, assign every table one write authority, replace cross-writes with capability operations or facts, shrink the shared library to stable technical code or duplicate/translate domain concepts, add mixed-version contract tests and service-local component environments, and retain only a small end-to-end journey suite. The smallest repair depends on the driver; adding more gateways is not one.

### Answer 4

Price and stock needed for commitment should be obtained from their authorities through bounded synchronous quote and reservation operations with stable identities, deadlines, preconditions, and unknown-outcome inquiry. Recommendations are optional and can come from a timestamped replicated read model; failure omits the panel. Fraud may require a current synchronous decision if regulation or risk demands it, or an asynchronous hold-and-review process when latency and policy permit delayed fulfillment. Price display may use a versioned short-lived projection, but final charge uses the authoritative quote. Inventory events build browsing views but do not authorize reservation. Every cached or replicated value carries freshness and provenance; retries are coordinated; checkout records the composite process and never infers commit from timeout.

### Answer 5

Dispatch owns incident intake, priority, unit assignment, and the composite response record. Traffic owns signal plans and physical safety interlocks. Hospitals own signed timestamped capacity declarations and acceptance decisions. Public notification owns approved messages and channels. Dispatch orchestrates a response using stable operation IDs and authoritative step outcomes; agencies publish durable facts for independent observers. Messages tolerate disconnection with bounded queues, replay protection, expiry, provenance, and reconciliation. A timeout creates an unknown state that is queried or handled by an approved manual procedure, never automatic duplicate dispatch. Workload and operator identities use least privilege; traffic actuation and patient data are separately authorized and minimized. A platform supplies immutable artifacts, identity, deployment, telemetry, regional failover, and audit without taking domain decisions. Each capability has a 24-hour owning team and cross-agency incident lead. Test partitions, stale capacity, duplicate messages, lost responses after commit, compromised credentials, overload, rollback, and manual fallback. Reject a separate service per traffic light: it creates excessive ownership and coordination; traffic control needs cohesive regional safety authority with internally modular device management.
