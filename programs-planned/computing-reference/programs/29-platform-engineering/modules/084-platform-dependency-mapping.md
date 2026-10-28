---
module_id: PLAT-084
program: Platform Engineering
level: 2
module_number: 84
title: Platform Dependency Mapping
status: complete
last_verified: 2026-09-02
---

# Platform Dependency Mapping

## One-Page Review

### Governing question

How should a platform represent, discover, validate, and use dependencies across user journeys, services, control planes, data, identity, artifacts, networks, teams, and recovery paths so architecture, incidents, upgrades, capacity, security, and disaster recovery decisions are based on typed, directional, time-bounded evidence rather than a stale diagram?

### Essential definitions

- A **dependency** is a directional relation in which the behavior or lifecycle of a consumer can be affected by a provider, resource, contract, authority, or condition.
- A **node** is a stable identified entity such as journey, service, API, queue, data store, cluster, identity issuer, artifact, policy, team, or external provider.
- An **edge** is a typed dependency statement with consumer, provider, scope, mode, criticality, contract, evidence, owner, validity interval, and failure semantics.
- A **runtime dependency** is exercised while serving or completing a journey; a **control dependency** changes desired state, authorization, configuration, or lifecycle.
- A **build/deploy dependency** affects production artifacts or releases but may not appear in steady-state traces.
- A **recovery dependency** is required to diagnose, restore, fail over, roll back, or revoke during an incident.
- A **hard dependency** must work for the protected outcome; an **optional dependency** may fail under a tested degradation contract.
- A **transitive dependency** is reachable through one or more intermediate edges; reachability alone does not determine impact.
- A **strongly connected component** is a set of nodes mutually reachable, revealing cycles that can create startup or recovery deadlocks.
- A **cut set** is a set of nodes/edges whose simultaneous failure disconnects a source journey from required outcomes.
- **provenance** records which source asserted or observed an edge and how it was transformed; **freshness** bounds how long that evidence remains usable.
- A **latent dependency** is exercised only under rare conditions such as cache miss, failover, certificate rotation, scale-out, restore, or administrative recovery.

### Central model, mechanism, or theorem

Represent the map as a temporal typed multigraph $G_t=(V,E_t)$. Each edge

$$
e=(u,v,type,mode,scope,criticality,contract,owner,evidence,confidence,[t_0,t_1))
$$

states that consumer $u$ depends on provider $v$ under a context and interval. A journey impact query traverses only edges whose failure semantics and context propagate the selected fault. Static declarations, runtime traces, network observations, configuration, audit, and exercises contribute evidence but none alone proves completeness. Decisions must show source, freshness, unknowns, and counterevidence.

### Critical invariants

- Nodes use stable scoped identity and lifecycle state; reused names cannot merge unrelated histories.
- Every consequential edge is directional, typed, contextual, versioned, owned, evidence-backed, and freshness-bounded.
- API, runtime, control, data, identity, build, deploy, observability, organizational, provider, and recovery edges remain distinguishable.
- Criticality is defined from a named journey and failure mode, not inherited globally from the provider’s reputation.
- Optional/degraded edges have tested timeout, fallback, stale-data, capacity, correctness, and recovery behavior.
- Discovery preserves source provenance, observation interval, sampling/coverage, confidence, and contradictions; inferred edges are not silently promoted to facts.
- Absence of observed traffic means no dependency was observed under stated coverage, not that none exists.
- Mapping includes asynchronous queues, cached/conditional paths, controllers, policy/identity, human approvals, shared infrastructure, and recovery-only dependencies.
- Transitive impact analysis respects edge semantics, topology, correlation, capacity, and failure domain; raw reachability is a candidate set.
- Owners validate and retire dependencies as contracts change; dangling, orphaned, stale, and ownerless edges are actionable states.
- Map access is partitioned because topology, trust, data movement, vulnerabilities, and provider relationships are sensitive.
- Incident, rollout, upgrade, restore, and retirement workflows record discovered edge changes back into the governed graph.

### Common failures

One untyped `dependsOn`; confusing provider→consumer direction; catalog names as identity; only synchronous HTTP traces; ignoring queues, DNS, identity, policy, data, control and recovery; infrastructure-as-code treated as runtime truth; network flow treated as semantic use; sampled traces treated as complete; shared libraries mixed with running services; cache hides cold dependency; fallback never tested; status page itself depends on failed identity; ownership copied from repository but operations differ; diagrams without effective dates; all reachable nodes called critical; cycles ignored; blast radius based only on direct edges; external SaaS hidden behind egress; shadow/manual approval absent; and deleting an entity while dependent records remain.

### Compact example

The “production deploy” journey depends synchronously on platform API, identity, policy and workflow; asynchronously on queue and controllers; at build/deploy time on source, CI, registry, signing and admission; for final effect on cluster API, DNS and workload health; and for recovery on audit, status, rollback artifacts and break-glass identity. Runtime traces reveal only part. Catalog declarations, workflow/audit events, Kubernetes owner references, cloud configuration, DNS/network observations, artifact attestations, and failover exercises supply typed evidence. Each edge names owner, version, region/tenant scope, timeout/fallback, source and freshness. An identity outage analysis follows required edges and also checks whether emergency access shares that issuer.

### Connections

Dependency mapping connects the catalog/API/event architecture from PLAT-061–070 with identity, policy, supply-chain and audit evidence from PLAT-071–080. It gives SLO, capacity and fleet management from PLAT-081–083 their actual topology. It becomes the planning substrate for upgrades, backup/restore, overload, incidents, disaster recovery, cost and scaling in PLAT-085–090.

## Governing Question

Which relationships can cause a platform journey to fail, become unsafe, lose data, exceed its deadline, or become unrecoverable—and how confidently do we know them now?

A dependency map is not one graph for every question. Incident impact, change compatibility, security trust, data residency, capacity amplification, cost allocation, and ownership escalation traverse different edge types and conditions.

The goal is an evidence-backed graph service whose uncertainty is visible. It helps humans ask precise questions and prioritize validation; it does not promise a perfectly complete digital twin.

## Why This Matters

Platform capabilities hide complexity for ordinary use. That abstraction is valuable until a shared identity issuer, DNS zone, registry, webhook, workflow database, policy bundle, or provider quota fails. Without typed dependencies, operators cannot predict blast radius or find a recovery route independent of the outage.

Change safety depends on consumers. A seemingly internal API or schema removal may affect controllers, build pipelines, dormant disaster tooling, and acquired workloads absent from source-code search. Static and runtime discovery catch different parts.

Unmodeled dependencies distort SLO and capacity reasoning. A service can meet its component objective while its user journey relies on a weaker provider. Retries, fan-out, caches, and fallback change both reliability and load propagation.

Maps decay. Owners, endpoints, versions, regions, and deployment topology change continuously. A stale comprehensive-looking diagram is more dangerous than a smaller graph with explicit freshness and unknowns.

## Prerequisites and Retrieval

Retrieve graph theory: directed multigraphs, reachability, strongly connected components, dominators, centrality, cut sets and hyperedges; distributed tracing/context propagation; logs, metrics, audit and network flow; service catalogs and ownership; APIs/schemas/events/queues; DNS/service discovery and load balancing; infrastructure as code, Kubernetes resources/owner references, cloud inventory; SBOM/provenance; identity, authorization, policy and secrets; data lineage; SLOs, error budgets, capacity and retries; threat modeling and attack paths; incident response; progressive delivery; backup/restore and disaster recovery; data classification; and temporal/versioned data modeling.

Distinguish dependency from communication; declaration from observation; absence from nonexistence; consumer→provider from request direction; logical API from endpoint; component from instance; runtime from build/deploy/control/recovery; direct from transitive; reachable from impacted; provider criticality from journey-specific necessity; optional from untested; cache from independence; redundancy from failure-domain independence; correlation from causation; ownership from authorship; current graph from historical graph; and visualization from authoritative data/query.

## Learning Objectives

After completing this module, you should be able to:

1. define a stable node and typed temporal edge schema for platform dependencies;
2. model synchronous, asynchronous, control, data, identity, build, deploy, observability, organizational, provider, and recovery relations;
3. merge declared, configured, observed, inferred, and tested evidence without erasing provenance or contradictions;
4. discover dependencies from catalogs, APIs, infrastructure, orchestration, telemetry, network/DNS, audit, artifacts, data lineage, and exercises;
5. compute candidate blast radius, reverse dependencies, cycles, cut sets, ownership paths, and change impact with semantic constraints;
6. model timeout, retry, cache, fallback, degradation, quorum, capacity and failure-correlation behavior;
7. govern freshness, confidence, access, owner attestation, retirement, and history;
8. integrate graph checks into design, deployment, upgrades, incidents, recovery and decommissioning;
9. verify high-consequence edges through fault injection and restore exercises; and
10. migrate static diagrams into an operational dependency knowledge system incrementally.

## Core Exposition

### Start from decisions and journeys

List questions: Who is affected if this API changes? Can production deploy if corporate identity is down? Which services use a revoked artifact? What must recover before DNS? Which tenants share this provider quota? Who approves a database retirement?

Choose a journey and failure mode. “Deploy production artifact during regional identity outage” yields different relevant edges than “serve cached user traffic during registry outage.” This prevents an indiscriminate hairball graph.

Name the consumer outcome, deadline, correctness, data and recovery needs. Traverse backward from that outcome and validate each required edge with owners and evidence.

Document decisions the map will support and the consequences of error. High-consequence automated placement or deletion requires stronger evidence than an exploratory visualization.

### Design stable node identity

Use typed, scoped IDs: organization/domain/system/component/API/resource/cluster/account/dataset/artifact/policy/team/provider. Keep display name, endpoint, repository, and deployment instance as attributes or related nodes.

Represent logical service separately from regional deployment, replica, endpoint and API version. This permits questions at appropriate granularity without merging failure domains.

Lifecycle states include proposed, active, deprecated, retiring and retired. Preserve tombstones and aliases so historical incident or audit queries do not resolve to a newly reused name.

Bind ownership to an accountable group and operational escalation, with effective interval. A CODEOWNERS author, platform provider and 24-hour on-call can differ.

### Define a typed edge vocabulary

Common types include `calls`, `publishesTo`, `consumesFrom`, `reads`, `writes`, `replicatesTo`, `authenticatesWith`, `authorizedBy`, `configuredBy`, `deployedBy`, `builtBy`, `signedBy`, `scheduledOn`, `routesThrough`, `resolvesThrough`, `observedBy`, `backedUpTo`, `restoredFrom`, `ownedBy`, `operatedBy`, and `approvedBy`.

Direction is consumer to provider for impact queries, even if network packets or data flow in both directions. Store inverse views as derived relations, not independently drifting facts.

Each edge includes scope (environment, region, tenant, operation), modality (sync/async/batch/control), necessity, deadline/timeout, retry, consistency, volume/fan-out, fallback/cache, failure mode, contract/schema/version, data/trust class, owner, source evidence, confidence and valid interval.

Allow parallel edges between the same nodes. A service can both read and write a database, use identity at login, and depend on an emergency issuer only during recovery.

### Model conditional and latent edges

Attach predicates: cache miss, primary region unavailable, token expired, certificate rotation, scale above threshold, feature flag, tenant tier, disaster mode, or specific API version.

Cold-path edges rarely appear in traces. Exercise them with synthetic requests, failover, key rotation, cache flush, restore, and scale tests. Record last successful validation and next due time.

Fallback is itself a dependency plus a switching mechanism. Model detection, decision, routing, capacity, state consistency, and fallback provider. Untested fallback is not redundancy.

Recovery maps include the tools used to reach consoles, fetch runbooks, obtain break-glass identity, restore secrets, resolve DNS, download artifacts, communicate, and access evidence. They often share dependencies with the failed path.

### Use catalogs for declared intent

A software catalog can model components, APIs, resources, systems, domains, ownership and relations. It captures human architectural intent and supports discovery.

Declarations should live near owned source when practical and be processed into authoritative derived relations. Validate entity references, owners, API/resource existence, environment scope and lifecycle.

Catalogs are not exhaustive runtime inventories. Backstage documentation explicitly frames its graph around human mental models rather than every possible thing. Preserve this boundary instead of calling missing low-level edges nonexistent.

Require owners to declare high-consequence and non-observable dependencies: external contracts, manual approvals, data residency, build services, recovery tools and feature-flagged integrations.

### Extract configuration and orchestration edges

Infrastructure code, Kubernetes manifests/owner references, Helm/Kustomize, service discovery, DNS, ingress, network policy, IAM, secret references, pipelines, workflows and controllers reveal intended bindings.

Resolve references with the environment and version that actually rendered/applied them. A template reference is not proof every deployment uses it. Preserve repository/commit, renderer, parameters, artifact digest and apply status.

Controller ownership reveals lifecycle but not necessarily runtime necessity. A Deployment owns ReplicaSets/Pods; the application may depend on a database found elsewhere. Keep lifecycle/control edges distinct.

Cloud inventory exposes resources and wiring created outside source. Reconcile provider IDs to catalog nodes without relying on tags alone; record ambiguous and orphan resources.

### Observe runtime execution

Distributed traces show causal paths for sampled instrumented requests. Normalize service/resource identity, operation, environment and peer. Preserve trace sampling and instrumentation coverage.

Metrics reveal dependency error/latency/load patterns but often lack per-request causality. Logs and audit show decisions and control changes. Queue/broker metadata captures async producer/consumer relationships when trace context is missing.

Network flows and DNS reveal connections, including uninstrumented systems, but connection does not prove semantic dependency. Sidecars, proxies, telemetry and security scans can create communication not required by the application.

Observe over representative time and workload conditions. A one-hour trace window misses monthly billing, certificate rotation, backup, cleanup, failover and dormant recovery paths.

### Map data dependencies and lineage

Represent datasets, stores, schemas, topics, tables, object prefixes, models and derived products at useful granularity. Edges include read/write, publish/consume, replicate, transform, train from, govern, back up and restore.

Record consistency, freshness, retention, residency, classification, ownership, schema/version and quality contract. A service may be available but incorrect because a data edge is stale.

Async event dependencies include topic identity, schema, partition/key/order, delivery semantics, retry/dead-letter, replay and consumer lag. The broker is a runtime resource; the event contract is a logical interface.

Data lineage tools capture transformations but may omit serving/control dependencies. Link rather than flatten their graph into one ambiguous `dependsOn` edge.

### Include build and supply-chain edges

Source repositories depend on CI workflows, actions/tools, runners, package registries, dependencies, base images, artifact registries, signing/provenance, scanners and promotion policy.

SBOMs describe component relationships; provenance describes builder/material relations. Bind both to exact artifact digest. A library edge affects build/runtime risk differently from a service API dependency.

Map which production workload revision runs each digest and which platform components build/admit/deploy it. This supports compromised dependency, signer, builder or registry impact.

Do not infer runtime reachability from component presence alone. Keep `contains`, `buildDependsOn` and verified runtime call/reachability as separate claims.

### Include identity and policy edges

Model authentication issuer, certificate authority, token exchange, workload identity, authorization data, policy bundle, admission, secret/key service and revocation channel.

Identity often forms a hidden universal dependency. Distinguish credential issuance/rotation from offline verification of an already issued credential. Outage effects differ by cache and expiry.

Policy engines depend on policy/data distribution and may serve locally during manager outage. Record last-known-good and freshness/failure behavior.

Map administrative and emergency access separately. If break-glass relies on the same identity, DNS or device posture service as ordinary access, it may fail during the incident it is intended to recover.

### Merge sources without laundering certainty

Store assertions as provenance-bearing observations, then derive current edges. Multiple sources can support or contradict one edge.

An owner declaration may be high semantic confidence but stale. A recent trace is strong execution evidence for its sampled path but weak completeness evidence. An IaC reference shows intended configuration, not successful runtime use.

Define source authority per field/type and confidence rules. Never turn “seen in network flow” into “hard runtime dependency” without semantics. Preserve raw source identifiers and transformation version.

Contradictions are valuable: declared optional but every request fails without provider; desired provider differs from runtime endpoint; retired resource receives traffic. Alert owners rather than silently selecting the convenient source.

### Govern freshness and history

Freshness depends on edge type. Runtime calls may expire quickly; contractual provider dependency changes slowly; recovery validation expires according to drill cadence. Store observation and validity intervals.

Keep bitemporal history where decisions matter: when the dependency was true and when the mapping system learned it. Late evidence can then reconstruct incident-time knowledge without rewriting reports.

Edges transition active, stale, contradicted, deprecated and retired. Stale is not deleted or assumed false; it triggers validation and limits automated decisions.

Version schemas and derivation. A graph result should identify data snapshot, query revision, filters and unknown coverage, as PLAT-079 requires for evidence.

### Analyze direct and transitive impact

Reverse adjacency finds declared consumers of a provider. Traverse only edges compatible with the selected failure: read outage, write outage, latency, stale data, credential issuance, revocation, region, capacity or compromise.

Reachability creates a candidate set. Evaluate timeout/retry, cache, fallback, redundancy, capacity, consistency, user-journey position and correlated failure. A transitive node may be insulated; a non-network shared dependency may be missing.

Bound traversal by environment, tenant, region, version and time. Historical incident impact uses the graph valid then, not today’s topology.

Produce explanation paths with edge evidence and uncertainty. Operators need “deploy→workflow→identity, required for token exchange, observed/validated at time” rather than a red node cloud.

### Find cycles, cut sets and concentration

Strongly connected components reveal cycles. Not every cycle is wrong, but startup, authentication, observability and recovery cycles deserve tests: service needs DNS to start while DNS add-on needs service-hosted storage.

Dominators and cut sets identify candidates whose failure blocks all known paths. Account for conditional fallback and correlated failure domains. An apparent redundant pair in one region/provider/network is one practical fault domain.

Concentration metrics count critical journeys, tenants and recovery paths depending on a node. Weight by consequence and evidence quality; high degree alone is not risk.

Use findings to add isolation, caching, fallback, independent emergency paths, capacity, SLOs, or ownership—not merely to color dashboards.

### Model failure propagation

For each critical edge, document provider failures (error, latency, blackhole, stale/wrong response, overload, compromise), consumer timeout/deadline, retry/hedging, circuit/load shedding, cache, fallback, and degradation.

Retries create reverse load propagation: a weak provider causes consumers to send more attempts. Queue backlogs and reconnects persist after recovery. Map amplification factors and capacity assumptions.

A noncritical dependency that blackholes can exhaust consumer threads before timeout. Test absence, slowness and corruption, not only explicit error.

Security propagation differs: a compromised identity issuer or artifact builder can make dependents unsafe while all availability metrics stay green. Typed trust edges enable that analysis.

### Integrate change and upgrade planning

Change proposals query direct/transitive consumers of API/schema/version/config/policy/provider. Owners attest compatibility or tests prove it. Unknown/stale edges increase rollout caution.

Use observed usage plus declared cold/recovery edges before deprecation. A deprecated API with no seven-day traffic may still be a quarterly restore dependency.

Rollout rings should diversify shared dependencies. If canary and production rely on different providers, success has weak predictive value. Dependency maps select representative cohorts.

Record new/removed/changed edges after rollout. A release that unexpectedly adds public egress, identity dependency or fan-out becomes a review event.

### Support incident response

At incident start, freeze a graph snapshot and query affected journeys, consumers, regions/tenants, owners, recent edge/config changes, capacity and recovery dependencies. Treat output as hypotheses with evidence.

Overlay live health and SLOs without overwriting topology. Distinguish provider root symptoms from consumer cascades. Find ways to shed optional edges or break cycles.

During mitigation, record temporary routing, disabled dependency, cache mode, manual approval or break-glass edge with expiry. Otherwise the post-incident graph omits the actual recovery topology.

Afterward, validate missing/incorrect edges against traces, audit and operator reports. Updating the map is a remediation only if ownership, discovery or test prevents recurrence.

### Support recovery and retirement

Construct recovery dependency maps from clean-room assumptions: primary region, corporate identity, source control, chat, portal or DNS may be unavailable. Ensure runbooks, credentials, artifacts, backups and communication have appropriate independent paths.

Restore exercises validate edges and order. Record prerequisite, result, time, artifact/profile and evidence. A diagrammed recovery edge with no test is a hypothesis.

Before retiring any node, query current, stale and historical consumers across runtime, build, data, control and recovery. Contact owners and use a deny/tombstone or traffic monitor period.

Retain entity tombstone and historical edges. Verify no new calls, config, artifact, data job or recovery test references the retired node before destructive disposal.

### Secure the dependency map

The graph reveals high-value targets, trust relationships, administrative paths, data classes, vendors and failure cut sets. Partition access by tenant, environment, purpose and edge sensitivity.

Authenticate ingestion sources and writers. Prevent a compromised service from self-declaring ownership or hiding critical edges. Audit queries, exports, changes and automated decisions.

Minimize payloads: edge metadata rarely needs request bodies, credentials, secrets or personal data. Pseudonymize sensitive identities where analysis permits.

Keep a constrained emergency export or recovery view available independently of the primary graph service, with freshness and sensitivity clearly marked.

### Measure map quality

Track active-node ownership, edge owner/freshness/type/contract coverage, dangling/orphan references, contradiction age, source coverage, high-risk edge validation age, unknown regions/tenants, change-impact acknowledgements, incident discoveries and retirement residue.

Precision and recall need sampled ground truth. Review random services and important journeys manually; inject synthetic known edges; compare runtime/config/catalog; fault-test declared hard/optional paths.

Do not maximize edge count. Noisy auto-discovery can make queries unusable. Measure decision usefulness: incidents scoped faster, unsafe changes stopped, recovery paths validated, and stale claims corrected.

Publish limitations by source and time. A graph at 95 percent owner coverage may still miss the one unauthenticated recovery dependency that matters.

### Migrate from diagrams incrementally

Select one critical journey. Create stable nodes and minimal edge vocabulary. Import catalog declarations with owners and add runtime/config/audit evidence while preserving source distinctions.

Answer one operational query and exercise it in a game day. Fix identity, semantics and freshness before expanding. Avoid a universal ontology project detached from decisions.

Add ingestion contracts to paved roads and lifecycle workflows so new services, APIs, data, clusters and dependencies register automatically. Keep manual declarations for semantic/cold paths.

Retire static diagrams only when views can be generated from governed graph snapshots; diagrams remain useful projections, not competing truth stores.

## Definitions and Notation

Let $G_T=(V,E_T)$ be the dependency multigraph valid at time $T$. Node $v$ has stable identity, kind, scope, lifecycle and owners. Edge $e=(u,v)$ has:

- $\tau_e$: dependency type;
- $M_e$: mode/context predicate;
- $N_e$: necessity/failure-propagation predicate for a named journey;
- $C_e$: contract including deadline, retry, cache, fallback, consistency and capacity;
- $P_e$: provenance sources and transformation;
- $q_e\in[0,1]$: calibrated confidence, not truth probability unless a statistical model justifies it;
- $[t_s,t_e)$: validity interval;
- $f_e$: evidence age/freshness state.

For fault model $z$ and journey node $j$, candidate impact is semantic reachability in the reverse graph:

$$
Impact(j,z,T)=\{u:\exists\ path\ u\leadsto j\land
\bigwedge_{e\in path}Propagates(e,z,T)\}.
$$

The result is bounded by graph coverage and edge correctness. Let $SCC(G)$ denote strongly connected components. A cut set $K$ disconnects a required journey source from outcome when removing $K$ eliminates every admissible path under its mode/contract.

## Mechanisms, Invariants, or Proof Structure

### Dependency knowledge mechanism

1. Select a user journey and decision such as incident impact, upgrade, recovery or retirement.
2. Assign stable typed nodes, lifecycle, scoped ownership, aliases and historical identity.
3. Define directional typed edge contracts with mode, necessity, failure semantics, scope, version and time.
4. Ingest declared catalog and non-observable semantic dependencies with accountable owners.
5. Extract effective configuration, orchestration, infrastructure, identity, data and supply-chain relationships.
6. Observe runtime traces, metrics, logs, queues, network/DNS and audit over representative conditions.
7. Preserve each assertion’s source, coverage, sampling, time, confidence, transformation and contradictions.
8. Derive current/historical edges using field/type authority and freshness rules; never erase unknowns.
9. Analyze semantic reverse reachability, cycles, cut sets, concentration, failure amplification and recovery order.
10. Integrate evidence-backed queries into design, rollout, upgrade, incident, restore and retirement gates.
11. Validate critical and latent edges through fault, failover, cache-flush, rotation and restore exercises.
12. Measure owner/freshness/contract/source quality, feed discoveries back, and evolve the vocabulary narrowly.

### Identity invariant

Node and edge history binds to stable scoped identities and effective intervals. Endpoint, display name or owner changes cannot merge entities or rewrite incident-time topology.

### Semantic invariant

Every decision-relevant edge states direction, type, context, necessity, failure behavior and contract. Untyped reachability cannot be used as proof of impact.

### Evidence invariant

Every edge claim preserves provenance, observation/validity time, coverage, confidence and contradictions. Inference never silently becomes direct observation or owner attestation.

### Recovery invariant

Every critical journey has a validated recovery subgraph whose identity, access, communication, artifacts, data and observability do not all depend on the primary failed cut set.

### Lifecycle invariant

New and changed dependencies enter review; stale/ownerless/dangling edges remain visible; retirement checks current, latent and historical consumers before destructive removal.

### Proof sketch: absence from runtime traces cannot prove independence

Let observation interval $I$ contain no trace edge from consumer $A$ to provider $B$. Construct world $W_0$ where no such dependency exists and world $W_1$ where $A$ calls $B$ only on cache miss, failover, monthly settlement, certificate rotation, or disaster restore—none exercised during $I$—or where the path is unsampled/uninstrumented. The observed trace dataset is identical.

Therefore absence in runtime traces establishes only non-observation under instrumentation, sampling, traffic and interval coverage. Stronger confidence combines declared/configured evidence, longer representative observation, active condition exercises and owner validation. Even these bound rather than prove universal future independence because code, configuration and conditions change.

### Executable edge-quality audit

The synthetic audit classifies ten dependency edges by their first knowledge-contract gap. It demonstrates validation logic, not a complete real dependency graph.

<!-- bijux-verify: {"id":"dependency-edge-quality-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"usable=5\nmissing_owner=1\nstale=1\nuntyped=1\nuntested_fallback=1\ncontradicted=1\n"}} -->
```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Edge:
    name: str
    owner: str
    age_days: int
    edge_type: str
    fallback_tested: bool
    contradicted: bool


edges = [
    Edge("deploy-workflow", "platform", 1, "calls", True, False),
    Edge("workflow-queue", "platform", 2, "publishesTo", True, False),
    Edge("queue-controller", "platform", 3, "consumedBy", True, False),
    Edge("controller-cluster", "fleet", 1, "configures", True, False),
    Edge("cluster-identity", "identity", 4, "authenticatesWith", True, False),
    Edge("unknown-owner", "", 1, "calls", True, False),
    Edge("old-observation", "network", 45, "routesThrough", True, False),
    Edge("generic-link", "catalog", 2, "", True, False),
    Edge("cold-failover", "reliability", 3, "failsOverTo", False, False),
    Edge("declared-optional", "service", 2, "calls", True, True),
]

counts = {
    "usable": 0,
    "missing_owner": 0,
    "stale": 0,
    "untyped": 0,
    "untested_fallback": 0,
    "contradicted": 0,
}

for edge in edges:
    if not edge.owner:
        counts["missing_owner"] += 1
    elif edge.age_days > 30:
        counts["stale"] += 1
    elif not edge.edge_type:
        counts["untyped"] += 1
    elif "fail" in edge.edge_type.lower() and not edge.fallback_tested:
        counts["untested_fallback"] += 1
    elif edge.contradicted:
        counts["contradicted"] += 1
    else:
        counts["usable"] += 1

for name, count in counts.items():
    print(f"{name}={count}")
```

### Verification strategy

Seed known synthetic nodes/edges across catalog, configuration, trace, queue, DNS/network, audit, artifact and data sources. Verify identity resolution, direction, typing, scope, time, provenance, sampling and contradictions. Test reused names, stale owners, dangling refs and schema changes.

For critical journeys, compare graph predictions with controlled provider error, latency/blackhole, identity outage, cache miss, queue stall, fallback, region loss, rotation and restore. Measure predicted/actual affected set, missed/false edges, recovery order, amplification and freshness.

Use incident and change retrospectives as held-out evidence: snapshot the map before outcome, record predictions, then compare without rewriting history. Audit sensitive queries and automated actions. Restore the graph, source links, schemas, history and emergency view independently.

## Alternatives and Trade-Offs

1. **Catalog declaration versus auto-discovery:** declarations carry semantics; discovery finds reality but can be noisy/incomplete.
2. **One universal graph versus linked domain graphs:** one graph simplifies traversal; linked graphs preserve data, trust and ownership semantics.
3. **Logical service versus instance nodes:** logical nodes reduce scale; instances expose failure locality and rollout detail.
4. **Untyped relation versus rich edge contract:** simple edges ease adoption; rich semantics enable valid impact decisions.
5. **Runtime traces versus network flows:** traces show causal semantics when instrumented; flows cover more systems but not intent.
6. **IaC parsing versus cloud observation:** code shows desired state; provider inventory shows actual resources but may miss rationale.
7. **High recall versus high precision:** broad discovery finds candidates; noise can overwhelm owners and incident analysis.
8. **Current graph versus temporal graph:** current state is easier; history is required for incident, audit and change reconstruction.
9. **Central ownership versus federated assertions:** central rules improve consistency; domain owners know semantics and latent paths.
10. **Automatic criticality versus owner attestation:** algorithms scale; journey owners understand acceptable degradation but can be stale.
11. **Reachability versus fault-semantic traversal:** reachability is fast; semantic traversal avoids many false impacts.
12. **Exact topology versus probabilistic confidence:** exact claims are clear but unrealistic; confidence exposes evidence quality but needs calibration.
13. **Online query versus precomputed emergency export:** live data is fresh; an independent snapshot survives graph-service failure.
14. **Fine-grained resources versus aggregation:** detail supports precise action; aggregation controls scale and cognitive load.
15. **Active probes versus passive evidence:** probes validate rare paths; they add load/risk and cover only designed scenarios.
16. **Automatic enforcement versus advisory impact:** enforcement prevents unsafe change; uncertain maps can block valid work.
17. **Long retention versus topology sensitivity:** history supports learning/audit; it exposes valuable attack and vendor information.
18. **Build in-house versus catalog/observability products:** products accelerate ingestion/UI; durable semantics and governance remain organization-specific.

## Failure Modes and Misconceptions

- **“A diagram is the dependency map.”** It is one projection without necessarily governed data, evidence or freshness.
- **“Any communication is dependency.”** Telemetry, probes, scans or opportunistic calls may not affect outcomes.
- **“No traffic means independent.”** Conditional, sampled, uninstrumented and recovery paths may be dormant.
- **“Trace data is complete.”** Sampling, propagation, instrumentation and time coverage bound it.
- **“Network flows reveal semantics.”** A connection does not identify logical contract, necessity or correct direction.
- **“IaC is actual state.”** It describes intended configuration for some resources and revisions.
- **“Catalog is runtime inventory.”** Catalogs often model human concepts and declared relationships.
- **“One `dependsOn` type is enough.”** Failure, change, security, data and recovery analysis need different semantics.
- **“Request direction is dependency direction.”** Define consumer→provider consistently, regardless of callbacks/data flow.
- **“Provider criticality is global.”** It is specific to journey, context, deadline and fallback.
- **“Optional means safe to lose.”** Degradation, capacity and correctness must be tested.
- **“Cache removes dependency.”** It changes timing and outage behavior and adds freshness/capacity constraints.
- **“Two providers mean redundancy.”** They may share identity, region, network, data or control plane.
- **“Fallback is a line on a diagram.”** Detection, switch, capacity, state and restore must work.
- **“All reachable consumers are impacted.”** Edge semantics and fault type determine propagation.
- **“Only direct dependencies matter.”** Shared transitive providers and cycles create systemic risk.
- **“High degree means root cause.”** Centrality is a prioritization hint, not causal evidence.
- **“Cycles are always bugs.”** Some are intentional, but startup and recovery behavior must be designed.
- **“Owner is repository author.”** Product, platform, provider and operations ownership may differ.
- **“Static owner is timeless.”** Ownership and escalation need effective intervals and validation.
- **“SBOM proves runtime reachability.”** Presence and execution are distinct claims.
- **“Traces show build dependencies.”** CI, registries, signers and scanners often disappear after deployment.
- **“Runtime map covers recovery.”** Emergency identity, runbooks, backups and communication are cold paths.
- **“Identity outage is one edge.”** Issuance, verification, revocation and break-glass have different dependencies.
- **“Stale means false.”** It means current truth is unknown and needs validation.
- **“Conflicting sources should be merged away.”** Contradictions expose drift, semantic error or incident state.
- **“More edges means better quality.”** Noise reduces decision utility and can hide critical paths.
- **“The map can safely enforce deletion.”** High-consequence automation requires strong coverage, owner validation and staged tombstones.
- **“Topology is harmless metadata.”** It reveals attack paths, cut sets, sensitive data and vendors.
- **“Once built, the graph stays useful.”** It must integrate with continuous lifecycle and operational feedback.

## Worked Examples

### Example 1

A production deployment uses identity, policy, workflow, queue, controller, cluster API, admission, registry and DNS. Traces cover API/workflow but not artifact signing or recovery access. Catalog, provenance, audit, Kubernetes and game-day evidence add typed edges. An outage query now finds both serving path and rollback prerequisites.

### Example 2

Network flows show service A connecting to telemetry collector B. Auto-discovery labels B a hard runtime dependency. Fault testing shows A continues normally when B blackholes because export is bounded and dropped; B is an observability dependency with a loss contract, not a serving dependency. The typed correction removes false blast radius without deleting the edge.

### Example 3

A service declares cache as optional and database as fallback. A cache outage sends tenfold reads to the database, which saturates and fails. Edges gain cache-capacity and retry/fan-out semantics; dependency analysis flags correlated overload. Load tests establish degradation and a circuit/load-shedding response.

### Example 4

No trace referenced an old object store for 60 days, so retirement begins. A quarterly restore job fails because its manifest lives there. Recovery/build declarations and exercise evidence would have found the latent edge. The retirement gate now queries stale/cold dependencies and performs a deny-monitor period before deletion.

### Example 5

Two regional providers appear redundant but both authenticate through one global issuer and resolve through one DNS control plane. Cut-set analysis identifies the shared pair. The team creates locally verifiable credentials with bounded expiry, independent emergency access and a secondary DNS recovery route, then tests them.

### Example 6

A sampled trace sees only 5 percent of calls and misses a low-volume regulated tenant. The graph preserves sampling and cohort coverage rather than declaring no edge. Configuration plus audit confirms the tenant path; a targeted synthetic validates it. Automated residency checks require this stronger source combination.

### Example 7

An API version removal query finds direct consumers, but a build pipeline generates clients only during releases. Source and build provenance adds the generator/tool edge. The deprecation gate scans artifacts and runs a representative build, preventing a change that runtime-only observation would approve.

### Example 8

During an incident, the portal and graph UI are down because they share identity. An independently stored, encrypted, freshness-marked emergency dependency export contains recovery identities, owners, critical cut sets and runbooks. Access is audited. The next graph revision records this shared failure and separates recovery dependencies.

### Example 9

A new release unexpectedly adds calls to a public SaaS API. Egress/DNS observation contradicts the declared graph and artifact/config diff. Policy pauses rollout; owners document purpose, data class, timeout, region, provider SLO, cost, fallback and approval—or remove it. The edge is not normalized into invisibility.

### Example 10

A platform migrates from architecture drawings. It models one deploy journey with stable catalog nodes, typed declared edges, trace/config/audit sources and a temporal snapshot. A game day tests identity and queue outages. Only after impact queries help incident response does it add build, data and recovery graphs. Diagrams become generated views.

## Cross-Program Connections

1. **Graph theory:** directed multigraphs, reachability, SCCs, cuts, dominators and temporal graphs formalize topology questions.
2. **Distributed systems:** retries, caches, queues, fallbacks, partial failure and correlated dependencies govern propagation.
3. **Observability engineering:** traces, context, metrics, logs, flows and audit provide differently bounded evidence.
4. **Software architecture:** APIs, bounded contexts, coupling, component/resource models and change compatibility define logical edges.
5. **Data engineering:** lineage, schema, freshness, provenance, streaming and bitemporal history support dependency knowledge.
6. **Security engineering:** trust, identity, policy, attack paths, data movement, least privilege and map confidentiality shape analysis.
7. **Site reliability engineering:** SLO allocation, cascading failure, capacity, incident impact and recovery validation consume the graph.
8. **Supply-chain engineering:** source, builder, package, artifact, signer, scanner and deployment edges extend beyond runtime.
9. **Organizational design:** ownership, escalation, team APIs and cognitive load determine whether dependency contracts stay maintained.
10. **Systems engineering:** interface assurance, failure propagation, common-mode risk and lifecycle evidence make mapping decision-oriented.

## References

1. OpenTelemetry. [Traces](https://opentelemetry.io/docs/concepts/signals/traces/). Retrieved 2026-09-02.
2. OpenTelemetry. [Context Propagation](https://opentelemetry.io/docs/concepts/context-propagation/). Retrieved 2026-09-02.
3. OpenTelemetry. [Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/). Retrieved 2026-09-02.
4. Backstage. [Software Catalog System Model](https://backstage.io/docs/features/software-catalog/system-model/). Retrieved 2026-09-02.
5. Backstage. [Creating the Catalog Graph](https://backstage.io/docs/features/software-catalog/creating-the-catalog-graph/). Retrieved 2026-09-02.
6. Backstage. [Descriptor Format and Relations](https://backstage.io/docs/features/software-catalog/descriptor-format/). Retrieved 2026-09-02.
7. Google. [Site Reliability Engineering: Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/). Retrieved 2026-09-02.
8. Google. [Site Reliability Engineering: Managing Critical State](https://sre.google/sre-book/managing-critical-state/). Retrieved 2026-09-02.
9. CycloneDX. [Specification Overview](https://cyclonedx.org/specification/overview/). Retrieved 2026-09-02.
10. in-toto. [Attestation Framework](https://github.com/in-toto/attestation/tree/main/spec). Retrieved 2026-09-02.
11. Kubernetes. [Owners and Dependents](https://kubernetes.io/docs/concepts/overview/working-with-objects/owners-dependents/). Retrieved 2026-09-02.
12. Kubernetes. [Auditing](https://kubernetes.io/docs/tasks/debug/debug-cluster/audit/). Retrieved 2026-09-02.
13. W3C. [Trace Context](https://www.w3.org/TR/trace-context/). Retrieved 2026-09-02.
14. OpenLineage. [OpenLineage Specification](https://openlineage.io/docs/spec/). Retrieved 2026-09-02.

## Exercises

### Exercise 1

Define a dependency node/edge schema for a production deploy journey, including runtime, control, build, identity, data, organizational and recovery edges.

### Exercise 2

Design a multi-source discovery and confidence process that combines catalog, IaC, traces, queues, network/DNS, audit, SBOM/provenance and owner declarations.

### Exercise 3

Analyze an identity-provider outage for a platform with cached tokens, workload identity, admission, portal login and break-glass access. Produce semantic impact paths and recovery gaps.

### Exercise 4

Create dependency-aware gates for removing an API version and retiring its backing service when runtime traffic is sparse.

### Exercise 5

Plan migration from manually maintained diagrams to an operational temporal graph without launching an unbounded ontology program.

## Answers to the Exercises

### Answer 1

Use stable scoped nodes for journey, portal/API, identity issuer/token exchange, policy bundle/engine, workflow/queue/controller, cluster/API/admission, source/CI/builder/artifact/signing/registry, DNS/network, data/status/audit, team/on-call and break-glass/recovery artifacts. Separate logical services, APIs, deployments, resources and versions.

Each consumer→provider edge records type, mode, environment/region/tenant/operation, hard/optional necessity for named outcome, deadline, retry, cache/fallback, consistency, fan-out/capacity, contract/schema/version, data/trust class, owner, evidence/provenance, confidence, observation and validity interval. Parallel edges preserve distinct semantics.

Define accepted and completed deploy states so control edges do not imply runtime dependency. Include owner/approval and recovery-only relations. Historical identity/tombstones ensure later incident queries resolve exact entities.

### Answer 2

Treat every source as an assertion. Catalog/owner declarations provide semantic intent and cold paths; IaC/render/apply provides configured intent; provider/Kubernetes inventory provides observed resources; traces provide sampled causal execution; queue metadata covers async; flow/DNS finds uninstrumented communication; audit captures control decisions; SBOM/provenance provides build/artifact relations.

Store source ID/revision, producer, scope, environment, time interval, sampling/instrumentation coverage, transformation and confidence. Define authority by edge field/type. Derive current edges without deleting source assertions. Preserve contradictions and stale/unknown state.

Validate high-consequence edges using active faults, cache flush, failover, rotation, scale and restore plus owner attestation. Measure precision/recall on sampled journeys and incident predictions. Never promote non-observation to absence or network communication to hard semantic dependence automatically.

### Answer 3

Split identity edges: human login/portal, token issuance, token verification, workload credential issuance, policy/admission external data, revocation and emergency access. For each, record offline verification/cache expiry, timeout, fail policy, region, issuer/CA/DNS/network, and owner.

Traverse the issuer-unavailable fault. Existing short-lived tokens may verify locally until expiry; new human sessions and workload credentials fail; portal may be unavailable while already authenticated API sessions work; admission may fail open/closed according to control; controllers with cached credentials progress temporarily. Do not treat these as one global edge.

Check break-glass issuer, DNS, device posture, secrets, console and communication. If they share the failed cut set, create an independently protected bounded recovery path. Exercise expiry, revocation, failover and issuer compromise, then record actual impact, deadlines and evidence freshness.

### Answer 4

Model API logical/version nodes, direct consumers, generated clients, build tools, controllers, scripts, queued messages, stored objects, restore jobs and recovery tooling. Combine declarations, source/IaC search, runtime/audit over representative seasonal window, artifact/provenance inventory, stored-version scans and owner attestation.

Mark stale or unknown consumers and create a deny/warn/tombstone period. Publish replacement/schema compatibility and run representative builds, restores, failovers and dormant jobs. Roll out removal through low-risk/representative cohorts with SLO and error gates; retain rollback only if data/schema downgrade is valid.

Retire backing service after zero supported references, no new traffic/control/build/recovery use during the observation gate, owner approvals, data disposition, credential/DNS/network removal and residue search. Preserve historical entity/edges and document coverage limits.

### Answer 5

Choose one consequential journey and decision, such as deploy incident impact. Define minimal stable entity kinds and edge types; import diagram/catalog declarations with owners and effective time. Add only sources needed to validate that journey: traces, workflow/audit and effective configuration.

Produce a versioned snapshot and one reverse-impact query with explanations, freshness and unknowns. Game-day a provider failure and compare predicted/actual effects. Fix identity and semantics from discrepancies before adding scope.

Integrate node/edge registration into service, API, resource, artifact and cluster paved roads; require manual declarations for external and recovery paths. Add domain graphs incrementally for data, build and trust using links rather than flattening. Measure incident usefulness, stale/owner coverage and validation—not edge count. Generate diagrams as views and retire competing manual truth only after users can reproduce needed projections.
