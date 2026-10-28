---
module_id: PLAT-070
program: Platform Engineering
level: 2
module_number: 70
title: Integrating Platform Components Without Creating a Portal Monolith
status: complete
last_verified: 2026-09-02
---

# Integrating Platform Components Without Creating a Portal Monolith

## One-Page Review

### Governing question

How should a platform compose portal experiences, domain APIs, catalogs, workflows, policy, vendors, brokers, and events so users receive one coherent product while components retain independent authority, data ownership, security enforcement, deployment, scaling, and recovery?

### Essential definitions

- A **portal shell** provides navigation, layout, identity session, discovery, shared presentation primitives, and extension composition; it does not own every platform domain.
- A **domain component** owns one bounded platform capability, its contract, state, rules, operations, evidence, SLO, and lifecycle.
- A **frontend plugin** is a separately owned user-experience extension consuming published interfaces rather than private code or databases.
- A **backend plugin** or **domain backend** exposes server-side capability through an authenticated API/event contract and can be isolated or deployed independently when risk requires.
- A **backend for frontend (BFF)** adapts and aggregates domain APIs for a specific user experience without becoming the domain authority or universal integration hub.
- An **integration contract** specifies identity, request/event schema, version, authorization context, failure behavior, timeout, idempotency, observability, and lifecycle.
- A **composition root** selects and wires implementations, routes, extensions, and policy; it should contain integration configuration, not domain behavior.
- A **dependency graph** has components as vertices and runtime/build/data dependencies as directed edges; cycles and high fan-in identify coordination and blast-radius risks.
- **independent deployability** means a component can be released and rolled back within its compatibility window without synchronized release of unrelated components.
- **authority leakage** occurs when a shell, BFF, workflow, or shared library starts deciding or storing facts owned by another domain.
- A **distributed monolith** has multiple processes but still requires coordinated changes, shared state, synchronous availability, or lockstep deployment.
- **graceful partial failure** preserves safe unaffected journeys and makes missing/stale capability explicit rather than presenting false success.

### Central model, mechanism, or theorem

Model the platform as directed graph $G=(V,E)$, where an edge $a\rightarrow b$ is labeled by contract, criticality, interaction mode, timeout, identity, compatibility window, and fallback. Let $A(r)$ be the authoritative component for resource/fact $r$. For every mutation of $r$, the request reaches $A(r)$ with end-user or workload provenance, and every terminal claim is derived from $A(r)$ evidence. The portal may compose views and initiate operations, but it neither bypasses $A(r)$ nor commits its private state. A component is independently deployable only if every adjacent contract tolerates its supported version interval and unavailable behavior. Reducing process size without reducing semantic, data, and release coupling does not reduce monolith risk.

### Critical invariants

- Each domain fact, mutation, workflow, policy enforcement, and SLO has one accountable authority.
- Portal/frontend authorization improves experience but every backend reauthorizes the concrete action and resource.
- Components exchange versioned APIs, events, routes, and narrow library contracts; they do not query or mutate another component's private database.
- User identity, actor, delegation chain, audience, tenant, and correlation are preserved and independently validated at every trust boundary.
- The portal never holds provider credentials or secrets needed only by domain backends.
- Aggregation has bounded fan-out, deadlines, concurrency, response sizes, and explicit partial-result semantics.
- Long-running work is handed to durable workflows and observed by stable operation identity; browser/process lifetime is not the lifecycle.
- Plugin absence, timeout, incompatible version, or rollback cannot corrupt unrelated domains or falsely report success.
- Shared libraries contain stable cross-cutting primitives, not mutable domain models or hidden network calls.
- Events communicate authoritative facts; commands reach named owners; neither becomes an undocumented substitute for domain APIs.
- Deployments, data stores, queues, quotas, credentials, and failure domains can be split along ownership/criticality boundaries.
- Dependency inventory, compatibility evidence, and consumer usage govern evolution and retirement.

### Common failures

Portal database as master inventory; frontend calling cloud providers; hiding authorization only in buttons; one backend endpoint proxying everything; BFF implementing policy and workflow state; shared library exporting every domain model; plugins importing private packages; direct cross-plugin database joins; synchronous fan-out to twenty systems; unbounded home-page widgets; browser polling as orchestration; identity token forwarded to the wrong audience; service credentials erasing the human actor; portal routes as the only API; events emitted by scraping UI state; one release train; all plugins in one blast radius; micro-frontends with lockstep builds; duplicate search indexes treated as truth; silent stale data; generic error pages; compatibility tested only at head; and removing a plugin before API/event/subscription consumers are drained.

### Compact example

A developer opens environment `env-82`. The shell resolves route and session; catalog plugin fetches ownership from catalog API; environment plugin fetches authoritative status from environment API; cost widget queries a bounded cost BFF; policy badge displays a signed decision explanation. One optional cost timeout yields “cost unavailable, observed 09:41,” while environment actions remain usable. `Suspend` sends a user-delegated, audience-bound request with stable idempotency key to the environment authority, which reauthorizes, starts workflow `op-91`, and returns an operation link. The portal owns no provider token, workflow state, or environment row. Each plugin and backend can roll forward within tested contract intervals.

### Connections

This capstone composes domain APIs from [PLAT-060](060-designing-a-domain-specific-platform-api.md), API layering from [PLAT-061](061-platform-api-layers.md), portal architecture from [PLAT-062](062-developer-portal-architecture.md), catalogs and ownership from [PLAT-063](063-software-catalogs.md)–[PLAT-064](064-ownership-and-metadata.md), workflows and policy from [PLAT-065](065-workflow-and-orchestration-layers.md)–[PLAT-066](066-policy-decision-and-enforcement-points.md), vending/brokering from [PLAT-067](067-environment-and-account-vending.md)–[PLAT-068](068-service-broker-and-marketplace-models.md), and events from [PLAT-069](069-platform-eventing.md). PLAT-071 begins multi-tenant architecture.

## Governing Question

How can many platform capabilities appear as one product without the portal becoming their codebase, database, workflow engine, authorization boundary, credential vault, synchronous bottleneck, and release coordinator?

Coherence and centralization are not synonyms. Users benefit from consistent navigation, terminology, identity, ownership context, status patterns, and support. They do not benefit when every capability must be implemented or deployed inside one portal.

The portal is a valuable integration surface because it understands human journeys. It is a dangerous integration authority because user interfaces change quickly, execute in an untrusted browser, and tend to accumulate expedient adapters.

The architectural goal is a modular platform with explicit authorities and contracts. Deployment may begin in one process for operational simplicity. The design remains healthy only when boundaries permit selective isolation without rewriting domain semantics.

## Why This Matters

A successful portal attracts requests: add cluster data, deployment actions, cost, vulnerabilities, database provisioning, incidents, documentation, and approvals. Without explicit boundaries, every team edits the same backend and database. The portal becomes a critical shared service whose release, outage, and compromise affect every platform capability.

Superficial decomposition does not help. Twenty plugins in one repository can be modular; twenty services sharing a database and release train can be a distributed monolith. The meaningful questions are who owns state and decisions, how contracts evolve, which failures propagate, and whether changes require coordination.

Security is equally important. The portal sees many users and resources. If it holds broad cloud credentials or forwards bearer tokens without audience control, compromise becomes organization-wide privilege. Backends must preserve actor provenance while enforcing their own resource decisions.

Healthy composition also improves product development. Domain teams can own outcomes end to end, while a portal team owns shell quality and integration standards. Users receive coherent journeys; teams retain autonomy where it creates reliability and speed.

## Prerequisites and Retrieval

Retrieve bounded contexts, modular monoliths and microservices, API/event contracts, frontend plugin systems, BFFs, service discovery, distributed workflows, idempotency, OAuth/OIDC and token exchange, policy decision/enforcement, multi-tenancy, data ownership, observability, SLOs, dependency graphs, contract testing, deployment strategies, and disaster recovery.

You should distinguish cohesive experience from shared implementation; portal shell from domain backend; plugin from arbitrary code injection; BFF from domain service; aggregation from orchestration; route from authority; UI permission from backend authorization; user token from delegated service token; correlation from identity; catalog projection from provider/domain truth; build dependency from runtime dependency; physical process from semantic boundary; modular monolith from distributed monolith; graceful degradation from silent failure; and independent deployment from independent repository.

## Learning Objectives

After completing this module, you should be able to:

1. map platform domains, authorities, contracts, data, journeys, and dependencies;
2. design a thin portal shell and independently owned frontend/backend plugins;
3. choose direct API, BFF, workflow, event, and catalog integration deliberately;
4. preserve end-user identity and least-privilege service delegation across components;
5. bound aggregation latency, fan-out, partial failure, caching, and staleness;
6. prevent shared code, shared data, and shared infrastructure from erasing ownership;
7. define compatibility windows and tests that enable independent deployment;
8. isolate critical, privileged, noisy, and optional components by risk;
9. measure coupling, user-journey reliability, ownership, and release coordination; and
10. migrate and retire components without losing routes, data, operations, events, or recovery obligations.

## Core Exposition

### Map domains before selecting plugin boundaries

Start with platform capabilities and user journeys: discover software, create a service, vend an environment, request a database, observe a deployment, rotate a binding, inspect cost, or resolve policy failure. Identify the domain authority, state, decision, workflow, and outcome for each.

Do not make one plugin per page by default. One journey may compose several domains, and one domain may support portal, CLI, API, automation, and event consumers. The durable boundary follows authority and ownership, not today's screen layout.

Create a context map. Record upstream/downstream relationship, API/event contract, data classification, identity, criticality, latency, failure mode, team, and change cadence. Mark translation/anti-corruption layers where models differ.

Use the map to detect an integration domain that has no owner, a portal table that became authoritative, cyclic commands, or two components both claiming the same status.

### Keep the portal shell thin

The shell owns application composition: navigation, layout, route binding, extension discovery, user session initiation, accessibility baseline, design system, localization, common error patterns, and telemetry bootstrap.

It may present a cross-domain home page or search entry point. Those are projections with freshness and completeness, not new domain authorities.

Avoid business-specific conditionals in shell code. If navigation visibility depends on a declared capability or permission, consume a stable extension/permission contract. If it depends on environment state, ask the environment authority.

Keep the shell replaceable. Domain APIs, workflows, and events must serve non-portal clients. Losing the portal should impair human convenience, not erase platform state or make automation impossible.

### Make plugins vertical and owned

A frontend plugin owns a coherent user slice and its client adapter, routes, screens, accessibility, states, and tests. A backend plugin/domain backend owns corresponding server-side adapters or capability when appropriate.

Backstage's architecture distinguishes a composition app, frontend extensions/plugins, backend plugins, and databases; its current backend rules emphasize plugin isolation and network communication. Adopt the underlying boundary principles without assuming a framework creates them automatically.

Give each plugin a stable ID, owner, lifecycle, compatibility range, permissions, routes, dependencies, data classification, support, SLO contribution, and rollback behavior. A plugin package is code distribution, not proof of independent authority.

Third-party plugins are supply-chain and privilege decisions. Pin provenance, inspect permissions/network/data access, isolate credentials, scan artifacts, test upgrades, and maintain removal capability.

### Separate composition from domain behavior

The composition root chooses installed plugins, route bindings, implementations of shared interfaces, configuration, and deployment grouping. It should not implement environment placement, cost rules, approval, or broker lifecycle.

Dependency injection can make cross-cutting implementations replaceable: logging, discovery, authentication client, feature flags, and storage factories. Do not use it to conceal arbitrary cross-domain calls.

Extensions may contribute cards, pages, actions, search result renderers, or processors under a declared extension point. The host validates type, version, permission, placement, resource bounds, and failure behavior.

An extension point is public API. Its owner must version it, test consumers, document ordering/conflict, and deprecate it. Unlimited hooks create an ungovernable shared runtime.

### Preserve domain APIs as the primary contract

Every material capability exposes an authenticated, versioned API and/or event contract independent of the portal. CLI, automation, other components, and tests use the same authority.

The portal adapter should not scrape HTML, import server internals, query the domain database, or call a provider directly. It consumes supported contracts and maps domain results to UI states.

Use resource and operation links rather than reconstructing provider URLs. Keep stable domain IDs across portal routes, APIs, workflows, events, and audit.

When a portal-specific view needs joined data, consider bounded aggregation or a derived read model. Do not change ownership merely to make one screen query convenient.

### Use a BFF as an adapter, not a new authority

A BFF can tailor payloads, batch calls, resolve routes, translate presentation formats, and combine read-only domain views for one client. It may reduce browser round trips and hide internal network topology.

It must not become the only place where a business rule, approval, workflow, or resource status exists. Mutations should be passed to the owning domain under explicit contract; long operations return stable operation identity.

Define BFF cache policy per field/source, propagate provenance and observed time, and preserve partial results. A cached compliance badge must not silently become authorization evidence.

Avoid a universal BFF used by portal, CLI, automation, and services. That is an integration monolith with presentation naming. Give domain APIs first-class clients and use experience-specific aggregation narrowly.

### Choose an interaction pattern by semantics

Use direct synchronous APIs for current state, validation, or immediate decisions from one authority. Use durable workflows for multi-step, long-running, compensating, or approval-heavy mutations. Use events for authoritative facts needed by independently paced consumers.

Use catalog/search projections for discovery. Use links for navigation. Use a BFF for bounded view aggregation. Use a notification to invalidate/fetch when copying data would create risk.

Do not broadcast a command because the target is inconvenient to name. Do not use a workflow engine as a data query layer. Do not use an event stream to answer strongly current authorization.

Record the choice and failure semantics in the dependency edge. An unlabeled “calls” arrow hides the most consequential design information.

### Bound synchronous fan-out

If a page makes serial calls with latencies $l_1,\dots,l_n$, critical-path latency approaches their sum plus overhead. Parallel calls approach the slowest dependency, but still amplify connection, quota, and failure load.

Give every call a deadline shorter than the user-journey budget. Bound concurrency, retries, response size, pagination, and circuit behavior. Never permit nested unbounded fan-out.

Classify dependencies as required, conditionally required, or optional for the journey. Required failure stops the action safely; optional failure produces a labeled partial result with last observation.

Aggregate data only when the semantics of a partial answer are defined. “3 of 4 sources responded” may be usable for recommendations and unacceptable for destructive authorization.

### Design graceful partial failure

Render each plugin/card/page state explicitly: loading, fresh, stale, empty-authoritative, unauthorized, unavailable, incompatible, and failed. Empty is not a generic substitute for any of them.

Keep safe unaffected actions available. If cost is unavailable, environment deletion might still be possible; if policy authorization is unavailable and fail-closed is required, a mutation is not possible.

Show source and observation time when freshness matters. Avoid green aggregate health if one required authority was skipped or stale.

Failures must be accessible and actionable: concise user message, correlation reference, retry when safe, support owner, and protected operator detail. Do not expose raw stack, token, provider payload, or tenant data.

### Carry identity and delegation correctly

The browser authenticates the user to the portal. Each backend must receive a token intended for its audience or an exchanged/delegated token, not an ambient bearer token valid everywhere.

Preserve actor, authorized intermediary, tenant, audience, scopes, delegation chain, and request/operation identity. The backend independently validates issuer, signature, audience, expiry, subject, tenant, and authorization for the concrete resource/action.

Service-to-service credentials prove the calling workload, not the end user. When acting on behalf of a user, carry both identities under a protocol such as OAuth token exchange and constrain delegation. When running background work, record the originating actor and use workflow identity with narrowly scoped authority.

Never trust identity or permission claims supplied as arbitrary headers by the browser. A trusted gateway may derive headers only after validation and must prevent spoofing.

### Enforce policy at owning backends

Frontend permission checks improve usability by hiding or disabling unavailable actions. They are not enforcement because users can call endpoints directly or modify browser code.

The policy decision service evaluates governed policy, while each domain backend is the policy enforcement point for its resources. Conditional decisions may be translated to owner-native filters rather than exporting all resources to a central policy process.

Authorize every step that crosses authority: initial request, secret access, provider action, callback, status detail, cancellation, replay, and administrative recovery. Long workflows re-check time-sensitive policy where required.

Do not centralize domain resource schemas inside generic authorization code. Define stable attributes and let the owning service resolve conditions against current state.

### Protect credentials and sensitive data

Frontend code is delivered to the user and cannot safely hold platform or provider credentials. Browser-visible configuration, source maps, storage, and network requests are inspectable.

Use domain backends to hold scoped workload credentials and integrate with secret authorities. Prefer short-lived, audience-bound tokens. Prevent a general portal proxy from becoming an SSRF tunnel or confused deputy.

Minimize cross-domain payloads. BFF caches, search indexes, logs, traces, and client state create new data copies. Apply classification, tenant filtering, retention, and redaction at each boundary.

Sanitize third-party and catalog content. Plugin HTML/Markdown, external links, images, and error payloads are untrusted inputs to a privileged interface.

### Keep data ownership explicit

Each domain component owns its write model and schema. Other components access it through contracts, events, or explicitly governed exports. Separate schemas in one physical database can be an initial operational choice, but credentials and migrations must preserve ownership.

Cross-domain dashboards use read models or query federation with known freshness. They do not gain authority to mutate source tables. Every field carries source and reconciliation behavior.

Avoid shared tables such as `resources`, `requests`, or `statuses` into which every plugin writes. Their apparently generic model becomes semantic coupling and a migration bottleneck.

Backups and restores respect ownership. Restoring one component must not silently rewind shared rows owned by another. Cross-component recovery requires version/position reconciliation.

### Use shared libraries sparingly

Good shared libraries provide stable primitives: authentication client, tracing bootstrap, error envelope, pagination, design tokens, accessibility components, or contract-generated types.

Bad shared libraries export every domain entity, repository abstraction, database client, workflow helper, and mutable configuration. A change then forces coordinated upgrades across the platform.

Keep dependency direction clear. Domain packages should not depend on portal application packages. Plugins must not import another plugin's private implementation. Network clients and public extension contracts live in intentionally public packages.

Track version skew. A library can support multiple installed versions if its wire contracts remain compatible; runtime singleton assumptions and global registries often defeat that independence.

### Make events complement APIs and workflows

Events notify other components of authoritative facts without synchronizing their availability. They are useful for catalog projection, evidence, notification, analytics, or cache invalidation.

Commands still target an owner, and user-facing operation status still comes from a workflow/domain authority. Do not infer completion from seeing a request event.

Events have schema, identity, tenant, ordering, retention, and replay contracts from PLAT-069. A portal plugin normally consumes a projection/API rather than connecting a browser directly to privileged event infrastructure.

Avoid cyclic choreography in which components wait for each other's events to decide one business transaction. Use an owning workflow when sequencing and compensation require one accountable coordinator.

### Design search and home views as projections

Unified search and home dashboards are valuable composition surfaces. They index or aggregate domain documents under explicit freshness and authorization contracts.

Filter restricted data before indexing and before query response. Search counts, suggestions, facets, snippets, and deep links can leak hidden entities.

Preserve stable entity/resource identity and source. A search result links to the domain plugin, whose backend reauthorizes the detail. Search relevance never grants permission.

When an index is stale, show observation or omit unsafe actions. Reconciliation monitors source coverage, deleted documents, authorization-policy change, and orphaned results.

### Align deployment topology with risk

Semantic boundaries do not require one process each. A modular deployment can colocate low-risk plugins while retaining separate schemas, APIs, credentials, and code ownership.

Split when scaling, availability, privilege, data classification, noisy-neighbor behavior, dependency set, release cadence, or recovery objectives differ. A high-privilege vending backend should not share every portal plugin's runtime simply for convenience.

Deployment grouping is reversible only if components communicate through supported interfaces. In-process private imports and shared transactions make later extraction expensive.

Record failure domains: process, node, zone, cluster, database, identity, network, broker, and upstream provider. Multiple deployments sharing one saturated database are not isolated.

### Enable independent deployment with compatibility windows

For edge $a\rightarrow b$, define producer/client and provider/server versions that interoperate. Test current, previous, and rollout-skew combinations required by the deployment strategy.

Use additive changes, tolerant readers, explicit defaults, feature negotiation where needed, and deprecation telemetry. Avoid synchronized flag activation that creates an implicit release train.

Database expand/migrate/contract patterns allow old and new application versions during rollout. Event dual-read/write requires clear occurrence mapping and retirement. Frontend/plugin packages need host API compatibility and rollback tests.

Independent deployment is disproved if a routine component release requires rebuilding, redeploying, or data-migrating unrelated components. Track coordinated releases as architectural evidence.

### Test contracts and composition

Provider contract tests establish that an implementation meets the published API/event/extension contract. Consumer tests show which behavior is actually relied upon. Schema checks alone do not cover authorization, error semantics, timing, or meaning.

Test plugins against supported shell and backend versions, missing optional extensions, stale caches, malformed data, denied permissions, timeouts, and partial results. Test routes and deep links independently of navigation.

Run journey tests across composition boundaries for a small number of critical paths. Do not replace component tests with a brittle all-platform suite.

Exercise rollback and mixed versions. Inject dependency latency, 401/403, 404/410, 409, 429, 5xx, invalid schemas, token audience mismatch, and event duplication.

### Observe components and user journeys

Give every service stable name/namespace and instance identity, and propagate bounded trace context across synchronous and asynchronous edges. Preserve user/operation correlation without placing sensitive IDs in metric labels.

Measure each component's availability, latency, saturation, error classes, version, dependency calls, queue lag, and data freshness. Measure journey outcomes separately: create environment lead time, successful catalog discovery, or binding rotation completion.

Build a live dependency inventory from declared contracts, traces, gateway logs, broker subscriptions, and build metadata. Observed calls do not by themselves establish ownership, but expose undeclared coupling.

Allocate user-journey budgets across required dependencies. Optional widgets cannot consume the entire page latency or error budget.

### Measure and reduce coupling

For graph $G$, inspect fan-in, fan-out, cycles, strongly connected components, path length, shared data, shared release count, and change failure propagation. Edge count alone is not quality; a platform necessarily integrates.

Weight edges by criticality, synchrony, compatibility burden, privilege, and failure propagation. A stable asynchronous notification is less constraining than a synchronous mutation into a private schema.

Track percentage of releases requiring coordination, incompatible-change incidents, dependency-caused outages, ownership gaps, plugin upgrade lag, and time to isolate a failing component.

Refactor high-risk cycles by assigning authority, replacing cross-writes with APIs, introducing durable workflows, deriving projections from events, or merging components that are truly one bounded context.

### Operate composition as a product

Set standards for plugin registration, ownership, documentation, security review, API/event compatibility, permissions, telemetry, accessibility, performance budgets, dependency declarations, and lifecycle.

Provide paved-road scaffolds and test harnesses, not a central team that implements every integration. Domain teams own vertical capability; portal maintainers own shell contracts and quality.

Use an architecture review proportional to risk: privileged mutation, sensitive data, new shared dependency, unbounded fan-out, or new runtime code needs deeper evidence than a static link.

Maintain a kill switch or removal route for optional plugins. Safe disablement includes route behavior, background jobs, subscriptions, credentials, and cached data—not just hiding navigation.

### Migrate a portal monolith incrementally

Inventory routes, handlers, tables, credentials, jobs, events, owners, consumers, and workflows. Identify seams by authority and change cadence rather than by source directory size.

Choose one bounded capability. Define its domain contract and stable IDs, move write authority/data, build an adapter behind the old route, and compare behavior. Preserve user URLs where valuable through route indirection.

Strangle old reads after projections or APIs are verified. Revoke direct table and provider access so the boundary cannot regress. Move deployment only when semantic separation is real.

Repeat by risk/value. Avoid a whole-portal rewrite: it freezes product learning and often reproduces the same ownership mistakes in more services.

### Recover and retire components safely

Back up domain data, contract/configuration, plugin registry, routes, permission definitions, workflow state, event subscriptions, secrets references, and dependency inventory according to ownership.

During recovery, do not restore a portal snapshot as authority over newer domain services. Rebuild projections and reconcile versions, event positions, routes, and user-visible operation status.

To retire a component, stop new use, enumerate routes/clients/events/jobs/data/credentials, migrate consumers, drain work, archive required evidence, remove permissions, and verify no observed or declared dependencies remain.

Removing the UI first can orphan automation and live operations. Removing the backend first can turn the UI into false success. Retirement is a graph change with contract and data obligations.

## Definitions and Notation

Let the platform dependency graph be

$$
G=(V,E), \qquad e=(a,b,k,c,q,f),
$$

where vertex $v\in V$ is a component and edge $e$ connects consumer $a$ to provider $b$. Label $k$ is interaction kind (API, event, workflow, extension, library, or data export), $c$ is versioned contract, $q$ is criticality/quality budget, and $f$ is failure/fallback behavior.

Let $A(r)$ be the unique authoritative component for domain resource or fact $r$. For a mutation $m(r)$, correctness requires

$$
route(m(r))=A(r)
$$

and terminal state displayed by any component $v$ must cite evidence derived from $A(r)$ rather than local inference.

Let journey $J$ have required dependency set $R_J$ and optional set $O_J$. For serial required dependencies, a rough latency bound is

$$
T_J \ge \sum_{e\in path(J)} T_e,
$$

while parallel fan-out satisfies $T_J\ge\max T_e$ plus coordination overhead. In both cases every edge needs a deadline inside the journey budget.

Define release coordination indicator $z_{uv}=1$ when routine change in $u$ requires simultaneous release of $v$. A strongly coupled cluster has large

$$
C(S)=\sum_{u,v\in S,u\ne v} z_{uv}.
$$

The measure is diagnostic, not a universal threshold: security emergencies and intentional atomic changes can require coordination.

For contract $c$, let supported provider versions be interval/set $P_c$ and consumer versions $D_c$. Independent rollout requires tested compatibility for every pair that can coexist during deployment and rollback, not merely latest/latest.

## Mechanisms, Invariants, or Proof Structure

### Integration design mechanism

1. Map user journey, domain facts, mutations, workflows, and current authorities.
2. Assign one owner and source of truth for every resource/status/decision.
3. Choose domain API, workflow, event, projection, route, or extension by semantics.
4. Specify contract, version range, identity/delegation, authorization, idempotency, timeout, and error behavior.
5. Classify dependency as required/optional and bound fan-out, latency, retry, cache, and fallback.
6. Keep shell/BFF presentation state separate from domain state and provider credentials.
7. Define deployment, data, queue, credential, quota, and failure isolation by risk.
8. Test provider/consumer contracts and all rollout/rollback version pairs.
9. Observe component health, journey outcome, source freshness, and declared/actual dependency edges.
10. Exercise partial failure, incompatible versions, identity faults, recovery, disablement, and retirement.
11. Reduce high-risk cycles, private imports, cross-writes, and coordinated releases.
12. Govern additions and removals through ownership and lifecycle evidence.

### Authority invariant

For each $r$, $A(r)$ alone accepts mutation and asserts terminal domain state. Shell, BFF, search, catalog, and event consumers may cache or project, but expose source and staleness and cannot silently override it.

### Enforcement invariant

Every externally reachable backend enforces authorization for its owned action/resource. UI visibility, gateway routing, or upstream policy checks are defense and experience layers, not substitutes.

### Identity invariant

Each hop validates workload and delegated actor under the intended audience and tenant. It does not convert arbitrary browser headers or trace context into identity, and records provenance for durable work.

### Data-ownership invariant

Only owner-controlled migrations mutate a domain schema. Cross-domain reads occur through supported contracts or governed projections. Restore and retention remain owner-specific.

### Failure-containment invariant

Optional component failure cannot corrupt required domain state or falsely report success. Required dependency failure follows explicit safe behavior. Every call and fan-out is bounded.

### Deployability invariant

All versions that coexist during forward rollout and rollback satisfy their edge contracts. A routine component deployment does not require simultaneous unrelated release.

### Proof sketch: process decomposition is insufficient for independent deployability

Suppose monolith modules $x$ and $y$ are placed in separate processes, but $x$ still reads $y$'s private tables and both must adopt every schema change simultaneously. Any incompatible $y$ migration requires coordinated $x$ release or causes failure.

The number of processes changed, but compatibility and release constraint $z_{yx}=1$ remains. If they also share transaction assumptions and synchronous availability, failure coupling remains. Therefore process separation alone does not establish independent deployability. A supported contract and coexistence window—or recognition that $x,y$ are one intentional boundary—is required. This is a proof sketch about the given dependency, not an argument that every shared deployment is a monolith.

### Executable dependency audit

The following synthetic audit finds directed cycles and high-risk private-data edges in a platform graph. It demonstrates static classification only; it does not prove runtime independence, correct authority, security, or user-journey reliability.

<!-- bijux-verify: {"id":"platform-coupling-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"components=6\nedges=8\ncycles=1\nprivate_data_edges=1\nhigh_fan_out=1\n"}} -->
```python
from collections import defaultdict

edges = [
    ("portal", "catalog", "api"),
    ("portal", "environment", "api"),
    ("portal", "cost", "api"),
    ("portal", "policy", "api"),
    ("environment", "workflow", "api"),
    ("workflow", "environment", "event"),
    ("cost", "catalog", "event"),
    ("policy", "catalog", "private-data"),
]

graph = defaultdict(set)
for source, target, _ in edges:
    graph[source].add(target)

def reachable(start, target):
    pending, seen = [start], set()
    while pending:
        node = pending.pop()
        if node == target:
            return True
        if node not in seen:
            seen.add(node)
            pending.extend(graph[node] - seen)
    return False

cycle_pairs = {
    tuple(sorted((source, target)))
    for source, target, _ in edges
    if reachable(target, source)
}
components = {node for edge in edges for node in edge[:2]}
private_edges = sum(kind == "private-data" for _, _, kind in edges)
high_fan_out = sum(len(targets) >= 4 for targets in graph.values())

print(f"components={len(components)}")
print(f"edges={len(edges)}")
print(f"cycles={len(cycle_pairs)}")
print(f"private_data_edges={private_edges}")
print(f"high_fan_out={high_fan_out}")
```

### Verification strategy

Validate every edge against declared owner, authority, schema, authentication, audience, authorization, tenant, idempotency, timeout, retry, partial-result, compatibility, and retirement contract.

Run plugin and backend tests against current/previous shell and API versions. Exercise forward and rollback skew, absent plugins, duplicate packages, route rebinding, stale projections, denied conditions, malformed content, and dependency failure.

Inject latency, saturation, 401/403, version mismatch, token audience confusion, provider timeout, workflow crash, event duplication, database restore, and component disablement. Verify unaffected journeys remain safe and false success is impossible.

Compare declared graph with build imports, database grants, traces, gateway calls, broker subscriptions, credentials, and deployment changes. Investigate undeclared edges and routine coordinated releases.

## Alternatives and Trade-Offs

- **Modular monolith versus services.** One deployment is simpler; separate deployments improve selective scaling/isolation. Semantic boundaries and contracts matter in both.
- **Single portal versus several experiences.** One portal improves discovery/coherence; specialized surfaces may better serve distinct users and risk domains.
- **Direct browser API versus BFF.** Direct calls reduce aggregation code; a BFF protects topology and reduces round trips but can become an authority or bottleneck.
- **Client-side versus server-side composition.** Client composition isolates UI areas and parallelizes; server composition centralizes rendering and can govern payload/security more consistently.
- **Frontend plugin versus link-out.** Plugins create a seamless journey; links preserve product autonomy and reduce supply-chain/runtime coupling.
- **Shared backend process versus isolated backends.** Colocation reduces operational overhead; isolation limits privilege, scaling, and failure coupling.
- **Shared database versus database per domain.** Shared infrastructure is economical; separate ownership credentials/schemas or instances improve migration and recovery independence.
- **Synchronous API versus event.** APIs provide immediate authoritative answers; events decouple pace but add staleness and replay obligations.
- **Choreography versus workflow orchestration.** Choreography reduces central sequencing; explicit workflows improve accountability for long multi-step mutation.
- **Live aggregation versus projection.** Live reads improve currency but amplify failures; projections improve latency/resilience but are stale and require reconciliation.
- **Shared library versus wire contract.** Libraries improve consistency and type reuse; wire contracts permit language/version independence and make failure explicit.
- **Central policy versus domain-local rules.** Central policy gives organization-wide consistency; owner-local evaluation preserves resource semantics. Decision/enforcement separation can combine them.
- **End-user token forwarding versus token exchange.** Forwarding is simple but risks audience/privilege spread; exchange constrains delegation but adds identity infrastructure.
- **Lockstep compatibility versus coexistence window.** Lockstep simplifies code assumptions but creates release trains; coexistence costs compatibility work and enables autonomy.
- **Framework-native plugin versus remote component.** Native plugins integrate deeply; remote boundaries can isolate release and technology but add runtime/network complexity.
- **Rewrite versus strangler migration.** Rewrite promises uniformity but freezes learning and concentrates risk; strangling yields incremental evidence while carrying temporary adapters.

## Failure Modes and Misconceptions

- “A single portal requires a single backend” confuses experience with authority.
- “Plugins guarantee modularity” ignores private imports, shared tables, and lockstep releases.
- “Microservices guarantee independence” ignores data, semantic, and synchronous coupling.
- “One repository is a monolith” confuses source organization with runtime and domain boundaries.
- “One process is always wrong” ignores the value of a well-structured modular deployment.
- “The portal database is a convenient source of truth” creates competing authority.
- “Hiding the button enforces permission” ignores direct requests.
- “A gateway authorized it, so the domain need not” loses resource-specific enforcement.
- “Service identity is the user” erases actor and delegation provenance.
- “Forward the same token everywhere” creates audience confusion and privilege spread.
- “Trace ID carries identity” turns untrusted telemetry into security state.
- “A BFF can own any cross-domain rule” creates a presentation-layer domain monolith.
- “Aggregation must be complete” makes optional widgets destroy core availability.
- “Empty means unavailable” lies about authoritative absence and stale failure.
- “Retrying fan-out improves reliability” can amplify overload and duplicate mutations.
- “A shared model library prevents drift” often forces every domain to change together.
- “Shared database joins are harmless reads” bind schema evolution, access, and restore.
- “Events eliminate APIs” ignores current queries and directed mutation results.
- “Choreography removes orchestration” can hide cycles and ownership.
- “Search knows the resource” confuses projection and relevance with authority.
- “Independent repo means independent deployment” ignores compatibility and release practice.
- “Latest/latest contract tests are enough” misses rollout and rollback skew.
- “Splitting deployment removes blast radius” ignores shared identity, database, and provider quotas.
- “Optional plugin failure can be silent” produces false completeness.
- “Disabling navigation disables the component” leaves jobs, APIs, credentials, and subscriptions.
- “No observed calls means safe retirement” misses offline and recovery consumers.

## Worked Examples

### Example 1

An environment page combines catalog ownership, environment status, cost, and policy. Each card calls its owning backend under a bounded budget. Cost is optional and can show stale/unavailable; status and authorization are required for mutation. The portal never joins their databases.

`Delete` reaches the environment API, which checks policy and starts a durable workflow. The portal follows an operation link. Closing the browser has no effect on execution.

### Example 2

A team proposes a portal plugin that calls AWS directly using a shared credential. Review identifies frontend credential exposure, duplicated placement policy, absent idempotency, and no non-portal API.

The durable design adds an account-vending domain backend. The plugin sends a delegated request; the backend authorizes, plans, workflows, reconciles, and emits status. Provider credential is scoped and never reaches portal runtime.

### Example 3

A home page requests 18 widgets serially and misses its latency SLO whenever any provider is slow. The team classifies four required summary sources and fourteen optional widgets, parallelizes under concurrency/deadline limits, and caches safe projections with source time.

Optional failures render individually. Required authorization failure blocks only affected actions. The shell does not retry every request after global timeout.

### Example 4

Policy plugin reads catalog tables to evaluate owner conditions. A catalog migration breaks it, and restore ordering becomes coupled. The team defines stable owner attributes and conditional-decision contract. Catalog backend translates the condition to its native query and remains enforcement-data authority.

Database grants are revoked after contract rollout. The dependency graph loses a private-data edge and supports version coexistence.

### Example 5

A BFF aggregates environment and cost views, then begins storing “approved” and invoking providers. Those behaviors lack an owner outside the UI. The team moves approval/effective policy to the environment domain and provider work to durable orchestration.

The BFF retains presentation aggregation and short caches. It reports provenance and cannot manufacture a terminal environment state.

### Example 6

Portal backend plugins run in one process initially. Vending has broad cloud privileges and bursty workflows, while TechDocs is untrusted-content heavy. Because contracts and data are isolated, the team moves them into separate deployments without changing domain semantics.

The shell resolves routes through discovery. Separate identities, quotas, databases, and SLOs make the deployment split materially reduce blast radius.

### Example 7

Frontend plugin version 8 uses a field removed by backend version 10. Latest/latest tests pass, but rollback to frontend 8 fails during backend rollout. The team restores an additive compatibility field through the rollback window and adds a matrix for frontend 8–10 against backend 9–10.

Deprecation telemetry identifies remaining version 8 calls. Field removal waits until no supported coexistence pair needs it.

### Example 8

An optional security widget returns an empty list on 503. Users interpret this as zero vulnerabilities. The corrected contract distinguishes `fresh-empty`, `stale`, `unauthorized`, and `unavailable`, carries observed time, and prevents compliance export from accepting partial data.

The main catalog page remains available, but sensitive mutation fail-closed behavior is unchanged.

### Example 9

Workflow and environment services form a cycle: each synchronously calls the other before committing. A transient failure leaves both waiting and requires coordinated release. The team assigns environment as domain authority and workflow as execution authority under an operation contract.

Environment persists intent, workflow advances steps idempotently, and events communicate observations. Neither waits synchronously for the other's callback while holding state locks.

### Example 10

The platform retires an old database plugin. Navigation traffic is zero, but CLI calls its API, a nightly job uses its service credential, two workflow instances remain, and a replay projection consumes its events.

Retirement migrates API clients, drains workflows, moves event consumers, archives required data, revokes credential/permissions, removes routes and deployment, and tests recovery documentation. UI removal is last-mile presentation, not proof of completion.

## Cross-Program Connections

- **Software Engineering Patterns:** bounded contexts, ports/adapters, dependency inversion, modular monoliths, anti-corruption layers, and strangler migration shape component boundaries.
- **API and Service Engineering:** versioning, audience, idempotency, errors, pagination, deadlines, contract tests, and deprecation enable independent clients/providers.
- **Distributed Systems:** partial failure, retry, fan-out, clocks, queues, consistency, and recovery explain why composition cannot pretend to be local procedure calls.
- **Security Engineering:** token exchange, least privilege, audience restriction, confused-deputy defense, secret containment, and server-side enforcement preserve trust.
- **Systems Engineering:** dependency graphs, interfaces, emergent risk, failure propagation, and lifecycle evidence govern the platform as a system of systems.
- **Reliability Engineering:** criticality, SLO budgets, bulkheads, graceful degradation, saturation, rollback, and disaster recovery bound user journeys.
- **Observability Engineering:** stable service identity, traces, logs, metrics, dependency inventory, and business outcomes make coupling and partial failure visible.
- **Data and Database Engineering:** ownership, projections, CDC, migration, consistency, backups, and reconciliation prevent portal convenience from corrupting truth.
- **Product Management:** user journeys, cognitive load, capability ownership, adoption, support, and outcome measures keep integration grounded in user value.
- **Governance and Compliance:** classification, authorization, audit provenance, retention, third-party review, and separation of duties apply across every plugin edge.

## References

1. CNCF TAG App Delivery. [CNCF Platforms White Paper](https://github.com/cncf/tag-app-delivery/blob/main/platforms-whitepaper/latest/index.md). Retrieved 2026-09-02.
2. Backstage. [Architecture Overview](https://backstage.io/docs/overview/architecture-overview/). Retrieved 2026-09-02.
3. Backstage. [Frontend Plugins](https://backstage.io/docs/frontend-system/architecture/plugins/). Retrieved 2026-09-02.
4. Backstage. [Backend System Architecture](https://backstage.io/docs/backend-system/architecture/index/). Retrieved 2026-09-02.
5. Backstage. [Backend Plugins](https://backstage.io/docs/backend-system/architecture/plugins/). Retrieved 2026-09-02.
6. Backstage. [Permission Framework Overview](https://backstage.io/docs/permissions/overview/). Retrieved 2026-09-02.
7. Backstage. [Permission Concepts](https://backstage.io/docs/permissions/concepts/). Retrieved 2026-09-02.
8. Kubernetes. [Extending the Kubernetes API](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/). Retrieved 2026-09-02.
9. Kubernetes. [API Aggregation Layer](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/apiserver-aggregation/). Retrieved 2026-09-02.
10. IETF. [RFC 8693: OAuth 2.0 Token Exchange](https://datatracker.ietf.org/doc/html/rfc8693). January 2020. Retrieved 2026-09-02.
11. W3C. [Trace Context Recommendation](https://www.w3.org/TR/trace-context/). November 2021. Retrieved 2026-09-02.
12. OpenTelemetry. [Service Entity Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/registry/entities/service/). Retrieved 2026-09-02.
13. Jackson, Cam. [Micro Frontends](https://martinfowler.com/articles/micro-frontends.html). June 2019. Retrieved 2026-09-02.
14. Newman, Sam. [Building Microservices, Second Edition](https://www.oreilly.com/library/view/building-microservices-2nd/9781492034018/). O'Reilly Media, 2021.

## Exercises

### Exercise 1

Draw the component/authority graph for a portal that provides catalog, environment vending, database marketplace, deployments, cost, policy, and documentation. Label every edge with contract, identity, criticality, timeout, and fallback. Identify three risky edges.

### Exercise 2

Design a resource page that combines five domains while remaining useful during partial failure. Specify required/optional sources, provenance, freshness, authorization, latency budget, and prohibited false-success states.

### Exercise 3

Design user-to-portal-to-workflow-to-cloud identity for an account-vending request. Explain audience, service identity, actor delegation, policy enforcement, durable provenance, callback authentication, and secret boundaries.

### Exercise 4

Migrate a portal monolith whose handlers, provider calls, workflow state, search, and 40 plugin tables share one database. Choose the first seam and give contract, data, rollout, rollback, and verification steps.

### Exercise 5

Create a release and retirement policy for 60 plugins owned by 14 teams, with mixed frontend/backend versions, third-party packages, offline API clients, event consumers, and three deployment failure domains.

## Answers to the Exercises

### Answer 1

Create vertices for shell, catalog, environment, service marketplace/broker, deployment authority, cost, policy decision service, documentation, workflow engine, event broker, identity, search projection, secret authority, and providers. Mark catalog/environment/broker/deployment/cost as owners of their respective facts; policy decides while each domain enforces; workflow owns execution state but not resource truth; shell owns only composition/session UX.

Edges include shell-to-plugin extension contracts; plugin/BFF-to-domain APIs; domain-to-policy decisions; domain-to-workflow commands/operation status; workflow-to-provider APIs; domain/outbox-to-event broker; consumers-to-events; search-to-governed projections; services-to-identity/token exchange and secret authority. Label audience/delegation, tenant, schema/version, timeout, retry/idempotency, required/optional, and fallback.

Three likely risks are portal direct provider calls with broad credential, policy reading catalog private tables, and synchronous home-page fan-out to every domain. Other candidates are cyclic environment/workflow calls, shared generic status tables, or wildcard event subscriptions.

### Answer 2

Treat identity/session and resource authority as required for the page; ownership, cost, vulnerabilities, documentation, and recent deployment may be independently optional depending on the action. Run bounded parallel reads with per-source deadlines inside a page budget and no automatic mutation retry. Limit concurrency/size and protect each backend with bulkheads.

Every panel distinguishes loading, fresh-empty, fresh-data, stale with observation time, unauthorized, unavailable, and incompatible. Show source links and correlation reference. Cost outage does not erase environment status; vulnerability outage cannot render “secure”; stale policy evidence cannot authorize a destructive operation.

The owning backend reauthorizes each mutation. UI permission only guides. If policy decision is required and unavailable, fail closed. A BFF may aggregate read shapes and cache by field/source policy, but it cannot synthesize domain terminal state. Compliance/export journeys require all mandated sources or return explicitly incomplete, never a green partial report.

### Answer 3

User authenticates to portal under portal audience. For environment/account API, portal backend exchanges or obtains an audience-bound delegated token containing constrained actor/delegation and tenant context. Account backend validates issuer, signature, audience, expiry, authorized intermediary, subject, tenant, and concrete request permission; it does not accept browser-supplied identity headers.

The backend persists request ID/idempotency key, actor, delegating service, policy revision/decision reference, tenant, requested class, and time. It starts durable workflow under a scoped workflow workload identity. The workflow uses a separate short-lived provider credential from secret authority and carries originating provenance without impersonating the user's raw token.

Callbacks authenticate provider/workflow identity, bind to operation/nonce/audience, authorize transition, and reject replay. Portal never receives provider credential, secret value, or workflow service token. Status reads are resource-authorized. Later privileged steps reauthorize when policy freshness demands it, and audit connects actor, delegation, service, operation, provider receipt, and terminal evidence.

### Answer 4

Inventory routes, tables, queries, provider credentials, jobs, owners, API clients, events, workflows, and restore dependencies. Choose a high-value bounded domain with clear authority—environment vending—rather than extracting generic utilities. Define stable Environment and Operation APIs/events, IDs, authorization attributes, error semantics, compatibility window, and ownership.

Create owner-controlled schemas/credentials, migrate/copy data with checksums and reconciliation, and write new mutations through the environment authority. Put an adapter behind old portal routes so the current UI remains compatible. Move provider calls and durable workflow state behind that authority with idempotency and provider reconciliation. Shadow reads compare old/new status and authorization.

Roll out by cohorts with mixed-version contract tests, telemetry, abort thresholds, and rollback that preserves new writes. Once verified, switch reads, rebuild search from governed events/export, revoke portal table/provider grants, then optionally split deployment. Test backup/restore and in-flight operations. Repeat by domain; do not extract the shared `resources` table as a new universal service.

### Answer 5

Require each plugin to register stable ID, owner/support, routes, extension/API/event contracts, host/backend compatibility, permissions/data classification, dependencies, third-party provenance, deployment group, SLO contribution, kill behavior, and retirement plan. Test every version pair that can coexist during rollout/rollback, not only latest/latest. Publish deprecation windows and collect version/consumer telemetry.

Group deployments by privilege, criticality, scaling, and failure tolerance. Preserve separate identities, quotas, schemas, and credentials even when plugins colocate. Release one owned capability through canary/cohort with contract, journey, partial-failure, and rollback evidence. Coordinated releases require an explicit exception and become coupling metrics.

Third-party updates need provenance, vulnerability/license review, permission/network diff, sandbox/isolation decision, and removal test. Offline API clients and event consumers register support/replay horizons; observed usage supplements declarations. For retirement, stop new installs/use, announce replacement, migrate clients and data, drain operations/subscriptions, retain decoders through replay obligations, revoke permissions/credentials, remove routes/jobs/deployments, dispose data, update catalog, and test recovery documents across all three failure domains.
