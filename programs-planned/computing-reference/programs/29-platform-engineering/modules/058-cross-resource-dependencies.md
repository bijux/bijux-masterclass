---
module_id: PLAT-058
program: Platform Engineering
level: 2
module_number: 58
title: Cross-Resource Dependencies
status: complete
last_verified: 2026-09-02
---

# Cross-Resource Dependencies

## One-Page Review

### Governing question

How should a platform represent, authorize, evaluate, schedule, evolve, delete, and explain dependencies among independently reconciled resources without relying on file order, stale readiness, hidden cycles, or one giant orchestration transaction?

### Essential definitions

- A **dependency** is a predicate that a consumer requires another resource or capability to satisfy; it is more precise than “create A before B.”
- A **reference** identifies a target; it does not prove target existence, authorization, readiness, compatibility, or freshness.
- A **dependency graph** $G=(V,E)$ has resources/capabilities as vertices and prerequisite relations as directed edges.
- A **hard dependency** blocks progress when unsatisfied; a **soft dependency** changes quality or policy but permits a documented degraded path.
- **readiness** is current evidence that a target supplies its promised capability; **compatibility** additionally binds the version or contract a consumer needs.
- **fan-in** aggregates several prerequisites for one consumer; **fan-out** exposes one dependency to many consumers.
- A **cycle** is a directed path returning to its start; a strict prerequisite cycle has no initially enabled member.
- A **strongly connected component** is a maximal subgraph in which every vertex reaches every other; a nontrivial component localizes a cycle.
- A **wave** is a set of currently eligible independent work; it is scheduling structure, not proof of domain readiness.
- A **ReferenceGrant-style handshake** lets the target namespace/owner authorize a cross-boundary reference without surrendering ownership.

### Central model, mechanism, or theorem

For consumer $v$ at desired generation $g_v$, each incoming edge $e=(u,v)$ defines predicate $P_e(S_u,g_v,t)$ over trusted, freshness-bounded dependency evidence $S_u$. The consumer is eligible only when its hard-edge aggregation policy holds; for ordinary conjunction, every hard predicate must be current and true. A finite strict dependency graph admits a topological order exactly when it is acyclic. In a weighted DAG, unlimited-parallelism critical-path time follows

$$
EF(v)=w(v)+\max_{(u,v)\in E}EF(u),
$$

with zero for no predecessors. This lower bound does not include worker/provider limits. Controllers repeatedly resolve references, authorize scope, evaluate version-correlated predicates, reconcile eligible bounded work, and resync. Cycles are rejected or replaced by a deliberately coordinated joint protocol, never “fixed” with retries.

### Critical invariants

- Each edge states consumer, target identity, required capability/version, hard/soft policy, authorization, freshness, and deletion behavior.
- Reference resolution binds immutable UID where lifecycle safety matters; reusable name alone never authorizes destructive or security-sensitive action.
- Target existence is not target readiness, and readiness without matching contract/generation is not compatibility.
- Missing, stale, unauthorized, or ambiguous hard-dependency evidence blocks as `Unknown` or `False` according to contract; it never becomes optimistic success.
- Strict prerequisite graphs are cycle-checked on admission and after dynamic membership/policy changes.
- Independent vertices may run concurrently, subject to provider, tenant, failure-domain, and global fairness limits.
- One failing high-fan-out dependency is reported once as a shared cause while dependents retain their individual desired state and retry budgets.
- Cross-namespace/tenant references require target-side consent and do not leak target existence before authorization.
- Update and deletion use explicit graphs; deletion is not blindly reverse creation order when retention, traffic, backup, or shared ownership differs.
- Graph schema, readiness semantics, edge identities, and in-flight checkpoints remain compatible across upgrade, restore, and controller retirement.

### Common failures

Depending on YAML/file name order; equating object creation with usability; reading `Ready=True` without observed generation or freshness; using labels as security authorization; allowing name-only cross-namespace references; adding broad `dependsOn` edges that serialize unrelated changes; hiding a cycle behind retries; making optional telemetry block the service; copying thousands of child conditions into one parent; retrying every dependent during a shared outage; letting deletion remove a shared provider before consumers detach; assuming destroy order is always the graph reverse; using one global `Ready`; and uninstalling a dependency controller while consumers still rely on its condition contract.

### Compact example

An application requires database schema `orders/v4`, identity audience `orders-api`, and network route policy revision 18; telemetry is soft. Each reference carries namespace/name plus observed UID, and the cross-namespace database reference is permitted by a target-owned grant. The application does not start because the database object merely exists: it waits for a trusted fresh `Ready=True`, `observedGeneration` current, and `providedSchema=v4`. Identity and network may reconcile in parallel. When the shared identity provider becomes unknown, a dependency index enqueues affected applications once with jitter rather than hot-looping all tenants. On deletion, traffic drains before application credentials are revoked; the shared database is retained because application ownership never implied lifecycle ownership.

### Connections

This module combines reconciliation from [PLAT-052](052-desired-state-and-reconciliation.md), operator workflows from [PLAT-054](054-operator-state-machines.md), finalization from [PLAT-056](056-finalizers-and-deletion.md), and generation/freshness conditions from [PLAT-057](057-status-conditions-and-drift.md). It builds on workload ownership from [PLAT-024](024-pods-workloads-and-controllers.md). PLAT-059 applies the graph to control-plane failure and recovery.

## Governing Question

How can independently owned resources converge as a coherent system when one resource needs capabilities, outputs, or lifecycle facts from others, those facts arrive asynchronously, and no controller has an atomic view or transaction over the whole graph?

Platform APIs compose networks, identities, data stores, workloads, policies, secrets, DNS, and external services. Their relationships are rarely just construction order. An application needs a compatible database endpoint; a route needs an authorized backend; a backup needs a source incarnation and key; a deletion needs consumers detached before credentials disappear.

A durable dependency model turns these assumptions into explicit edges and predicates. It permits parallelism where safe, stops on cycles or unknown evidence, propagates shared failure without retry storms, and preserves resource-level reconciliation rather than turning the platform into one fragile imperative installer.

## Why This Matters

Hidden dependencies fail far from their cause. A Deployment can exist before its CRD controller, a Pod can start before a schema migration, a secret reference can cross a tenant boundary, or a network can be deleted while a database still needs it for final backup. “Apply again” may mask ordering during success and collapse during recovery.

Over-modeling is also harmful. A broad dependency on an entire platform stack can block an application because an unrelated dashboard is degraded. Excess edges reduce parallelism, expand failure domains, and make every update conservatively unknown.

Dependency evidence is distributed and stale. Each controller owns different status fields and observes different systems. Consumers need generation, version, source, and freshness correlation rather than a Boolean copied through several parents.

Lifecycle changes reverse or transform relationships. Creation may require network before database before application. Deletion may drain application traffic, snapshot database, retain data, then remove network. Upgrade may require lockstep compatibility rather than either direction alone.

## Prerequisites and Retrieval

Retrieve directed graphs, paths, reachability, topological sorting, strongly connected components, critical paths, partial orders, queues and scheduling, fan-in/fan-out, desired-state reconciliation, conditions and observed generation, freshness, owner references and garbage collection, finalizers, resource identity and references, optimistic concurrency, field ownership, admission, cross-namespace authorization, RBAC, capabilities and version negotiation, readiness and health, circuit breaking, bulkheads, backoff/jitter, caches/indexes, eventual consistency, transactions and sagas, upgrade compatibility, backup/restore, and decommissioning.

You should distinguish reference from ownership; existence from readiness; readiness from compatibility; hard from soft dependency; data flow from lifecycle ownership; graph edge from event subscription; orchestration order from continuous reconciliation; cycle from temporary wait; aggregate false from unknown; fan-out from duplication; topological order from one unique order; create graph from delete graph; target name from target UID; target authorization from source permission; and critical-path lower bound from production completion time.

## Learning Objectives

After completing this module, you should be able to:

1. specify dependency edges as identity-, capability-, version-, authorization-, freshness-, and lifecycle-aware predicates;
2. build and validate directed dependency graphs, topological waves, strongly connected components, and critical paths;
3. aggregate hard, soft, optional, quorum, and conditional dependencies with explicit three-valued semantics;
4. resolve references safely across namespaces, tenants, clusters, and external systems;
5. schedule incremental fan-in/fan-out reconciliation without polling storms or unfair serialization;
6. propagate shared failure and recovery while preserving local resource ownership and diagnosis;
7. design distinct create, update, migration, failover, and deletion dependency protocols;
8. evolve and retire graph/readiness contracts across rolling upgrade and restore; and
9. verify cycles, races, staleness, scale, authorization, deletion, and recovery with domain outcomes.

## Core Exposition

### Model a dependency as a predicate

“B depends on A” is incomplete. State what B needs: A must exist, be admitted, publish an endpoint, be ready for generation 7, expose schema version at least 4, retain a backup, grant access, or remain alive until B drains.

Define edge fields: consumer UID and generation; target group/kind/namespace/name and resolved UID; capability and contract range; hard/soft/optional policy; readiness predicate and producer; freshness bound; authorization/grant; failure behavior; event/index mapping; and create/update/delete semantics.

Keep data flow separate. Referencing an endpoint value creates an information dependency, but may not mean the producer owns the consumer or must be garbage-collected with it. Conversely, a hidden behavioral dependency can exist without a copied field; make it explicit when it changes safety or scheduling.

Prefer narrow capability edges over broad resource edges. “Needs database write endpoint compatible with schema v4” permits unrelated backup-condition changes without blocking the application. “Depends on database object” makes every database update conservatively relevant.

### Resolve identity and authority before state

A typed reference should constrain allowed group, kind, namespace, and sometimes API version. Resolve it to immutable UID before relying on status or performing destructive lifecycle work. If a target with the same name is recreated, the old edge becomes stale and must be reauthorized/rebound according to policy.

Same-namespace references often inherit a useful authorization boundary, but source-side read permission alone does not prove the target owner consented. Cross-namespace and cross-tenant references need a target-side handshake. Gateway API `ReferenceGrant` exemplifies an additive target-namespace grant and explicitly avoids revealing whether a target exists before a grant authorizes the reference.

Avoid selector references across trust boundaries unless selection authority and cardinality are constrained. A tenant able to change labels could capture consumers or secrets. Record resolution revision and reject ambiguous multiple matches.

External references need provider account/project, tenant, immutable ID, and credential authority. DNS name or URL reachability is not ownership proof.

### Distinguish existence, readiness, and compatibility

Existence means the API object can be retrieved. Admission means its desired form was accepted. Reconciled means a controller evaluated a generation. Ready means a documented capability is currently supplied. Compatible means that capability matches the consumer’s contract. These are separate predicates.

A CRD can exist before its conversion webhook/controller is serving. A database can be `Ready=True` for schema v3 while an application requires v4. A secret can exist but contain an expired certificate. A network can be ready in a different region.

Use conditions with unique producers, observed generation, stable reasons, and freshness as established in PLAT-057. Bind extra outputs such as endpoint revision, schema/API version, identity audience, region, or policy digest. Missing or stale hard evidence is unknown, not success.

Do not require “perfect health” when the consumer needs a narrower capability. A database may be degraded due to a failed replica while its quorum write service remains ready. Conversely, a green generic health condition may omit the exact compatibility property.

### Build and validate the graph

Choose edge direction consistently: $(u,v)$ means prerequisite $u$ must satisfy its predicate before dependent $v$ may perform the gated action. Derive edges from typed references where possible; use explicit dependency fields only for behavioral prerequisites not visible in data flow.

At admission or planning, validate reference shape, scope/grant, self-edge, duplicate edge, allowed target kind, and obvious cycles. Dynamic targets and cross-object updates require continuous cycle detection, not only schema validation.

A finite DAG has at least one vertex of indegree zero and admits a topological order. Kahn’s algorithm repeatedly removes zero-indegree vertices; if vertices remain, they lie in or behind a cycle. Depth-first search or strongly connected component algorithms localize cycles. Report the actual cycle path or component, not “dependency not ready.”

Several topological orders can be valid. Do not bake arbitrary lexical/file ordering into semantics. The scheduler can run each current zero-indegree/ready wave concurrently under limits.

### Reject or deliberately redesign cycles

A strict cycle A waits for B, B waits for C, C waits for A has no enabled initial action. Backoff does not resolve it. Identify whether an edge is truly hard, whether one capability has a bootstrap mode, or whether the resources are one joint protocol.

Break a legitimate bootstrap cycle with explicit staged predicates: identity service can start with local bootstrap credentials, then database connects, then identity rotates to database-backed state. Each stage needs safety and recovery evidence. Do not weaken every edge to optional.

If two resources require atomic coordination, introduce an owning composition/workflow resource that drives guarded steps while children remain independently observable. This converts an accidental distributed cycle into one explicit state machine.

Runtime cycles can appear through policy or selector changes. Freeze hazardous new actions, preserve serving state, identify the strongly connected component, and require corrected intent or a versioned migration protocol.

### Evaluate three-valued and conditional edges

Each predicate produces `True`, `False`, or `Unknown`. For all-required hard edges, any current false blocks with known unmet dependency; all current true enables; otherwise unknown blocks without asserting failure. Soft false or unknown may enable a documented degraded path and set a condition.

Optional means absence is accepted, not that a present unhealthy dependency is automatically ignored. Define both cases. Quorum dependencies specify count, eligibility, freshness, failure-domain diversity, and version compatibility. Conditional edges state when they apply—backup dependency may become hard only for deletion, or GPU capacity only for one workload class.

Aggregate against a consistent membership revision. If dependencies change during evaluation, retry or report unknown; do not combine half of old graph with half of new. Preserve bounded references to blockers and counts rather than copying full child status.

### Reconcile resources, not an imperative installation script

Events from a dependency enqueue affected consumers through an index. Each consumer rereads current intent, resolved target, authorization, and status; it does not replay the event as a command. Periodic resync repairs missed events and external changes.

The dependency controller or consumer computes eligibility, performs one bounded action, checkpoints, and returns. It should not hold a worker waiting for every predecessor. This preserves fairness and restart safety.

Tools expose different mechanisms. Flux Kustomization `dependsOn` can gate reconciliation on readiness and a custom expression, while warning that circular dependencies never apply. Argo CD phases/waves order one sync and wait on health; higher waves are pruned first. Terraform derives reference edges, supports explicit hidden dependencies, validates cycles, and walks ready graph nodes in parallel. These illustrate mechanisms, not interchangeable end-to-end guarantees.

Continuous platforms must re-evaluate after initial success. A dependency can degrade, revoke a grant, change version, or be deleted. Define whether the consumer stops traffic, freezes changes, fails over, continues with last-known data, or becomes unknown.

### Index fan-out without producing storms

Scanning every consumer on every target change is expensive. Maintain a reverse index from resolved target UID/capability to consumer keys. Rebuild it from authoritative objects after restart; an in-memory index is an optimization, not the only record.

Coalesce duplicate consumer keys and add jitter. When one shared identity service fails, do not let 100,000 dependents issue identical active probes. Cache only appropriately scoped observations, rate-limit per dependency/tenant/provider, and use circuit breaking while preserving eventual resync.

Prioritize lifecycle risk. Consumers needing credential revocation or traffic drain may outrank ordinary rollout. Use fair queues so one high-fan-out dependency cannot starve independent graphs.

Record shared cause on the dependency and bounded propagated context on consumers. Cardinality-safe metrics can count blocked consumers by stable dependency class/reason; raw UID lists belong in indexed queries or artifacts.

### Preserve independent ownership and status

The producer owns its desired state and condition contract. The consumer owns its decision about whether the producer evidence satisfies its edge. A parent must not write a child `Ready` condition, and a child must not mutate consumer spec to clear a dependency.

An aggregator can publish `DependenciesReady` for the consumer, with its observed generation, graph revision, counts, and bounded blockers. `Ready` then combines this with the consumer’s own capability under documented logic. Do not let several controllers overwrite one global condition.

Status distinguishes `ReferenceResolved`, `ReferenceAuthorized`, `DependencyReady`, `DependencyCompatible`, `Progressing`, and `Blocked` when consumers need those facts. Avoid condition explosion: one condition plus structured bounded summaries can represent repeated homogeneous edges.

Failure reason should point to the causal boundary without leaking cross-tenant target existence. Before authorization, report `ReferenceNotPermitted`, not “secret payroll-prod missing.”

### Propagate failure by policy, not contagion

A dependency false/unknown does not always mean tear down a working consumer. Define behavior by capability and duration: prevent new rollout, keep serving last-known configuration, shed optional features, fail closed, fail open within bounded lease, switch provider, or enter manual hold.

Avoid destructive cascades from transient status. Require fresh identity-bound evidence, hysteresis or duration where appropriate, and a guarded failover protocol. Security revocation may deliberately fail closed without delay.

Retry at the layer that can make progress. If the database is unavailable, application controllers should not all retry database creation. The database owner reconciles it; consumers wait with low-rate observation and respond locally.

Expose root-cause topology for incidents: dependency UID, capability, current reason, affected count, graph revision, and first-failure time. Do not erase individual consumer conditions because the shared cause recovers; each consumer must re-evaluate its own current generation.

### Model version and upgrade dependencies

Compatibility is often a relation $C(v_u,v_v)$, not equality. An application v5 may accept database schema 4–6. Store provided and required contract versions, not only product release labels.

For lockstep upgrade, require dependency ready at the intended version and consumer generation compatible. Flux `readyExpr` demonstrates matching version metadata in a dependency gate, but expressions must also check readiness and generation according to the configured semantics.

Plan expand/migrate/contract protocols: producer first expands compatibility, consumers migrate, then producer contracts old behavior. A single hard edge reversed halfway is insufficient; persist stages and evidence.

During controller rollout, old and new binaries must interpret edge and condition schemas compatibly. Unknown predicates or graph revisions fail safe. Conversion must preserve resolved UID, capability, policy, and lifecycle behavior.

### Use a distinct deletion graph

Creation edges often suggest reverse deletion, but domain constraints can differ. Terraform retains dependency information and models destroy actions separately because removed configuration otherwise loses ordering. Controllers likewise need durable delete dependencies before the source object disappears.

If application uses database, deletion may drain application before database. But a retained/shared database should not be deleted at all. A final backup may require network and encryption key to outlive database deletion. DNS might be removed before workloads to block new traffic, not after.

Express deletion obligations and edges explicitly, using finalizers and stable identities from PLAT-056. Owner references express Kubernetes lifecycle ownership only; a reference does not imply garbage collection. Multiple consumers require reference counts or owner-managed policy, not “last observer deletes.”

Race dependency deletion with new consumers. Admission/grants should stop new binding, existing consumers should detach or transfer, and target finalization should wait only for obligations it owns. Prevent hidden cycles between consumer and provider finalizers through one deletion orchestrator or acyclic contracts.

### Secure dependency resolution

Treat a reference as a request for authority. Validate source identity, namespace/tenant, allowed target kinds, grant, capability, and least-privilege data projection. Target-side consent should be revocable and continuously re-evaluated.

Avoid confused deputy behavior: a privileged controller must not fetch a secret for an unprivileged source merely because the source named it. Do not expose target existence, status, messages, or UID across a boundary before authorization. Gateway API’s grant model explicitly incorporates this information-control requirement.

Selector and wildcard grants broaden blast radius. Prefer exact kinds/namespaces and narrow projected outputs. Audit grant creation/revocation, binding/rebinding, cross-tenant resolution, compatibility override, cycle override, and forced deletion.

Dependency outputs can contain endpoints or credentials. Publish secrets through protected references and rotate/revoke them on consumer/target lifecycle changes; do not copy sensitive values into general status.

### Plan capacity and critical paths honestly

For weighted DAG work duration $w(v)$, earliest finish under unlimited workers is the node duration plus maximum predecessor earliest finish. The maximum $EF$ is the critical-path lower bound. Parallel branches off the critical path have slack.

Real systems add worker pools, provider quotas, tenant limits, batching, retries, observation delay, and unavailable dependencies. A wide wave can overload one API even when graph theory permits concurrency. Apply resource-constrained scheduling and per-provider semaphores.

Graph validation/traversal is $O(|V|+|E|)$ for adjacency-list topological/SCC algorithms, but resolving distributed status and authorization can dominate. Bound fan-out, pagination, and status size. Incremental indexes reduce work but require rebuild/reconciliation.

Measure graph vertices/edges, depth, width, cycles, unresolved/unauthorized references, blocker age, critical-path estimate, wave queue age, fan-out, shared outage amplification, and deletion blocks. Avoid high-cardinality labels.

### Recover and retire dependency protocols

After restore, resource names may resolve to new UIDs and status may be stale. Rebuild the graph from desired references, grants, and immutable identities; mark evidence unknown until producers re-observe. Fence old controllers and callbacks.

Handle missing dependency kinds/controllers explicitly. Installing the CRD without its reconciler gives existence without capability. A dependency condition whose producer is gone must expire by freshness rather than remain green forever.

Before retiring a capability, inventory incoming edges across live objects, clusters, tenants, versions, and backups. Migrate consumers, revoke new grants/admission, preserve compatibility while edges drain, update deletion graphs, and test restore cannot resurrect unsupported references.

Remove indexes, RBAC, CRDs, grants, secrets, and producer controllers only after zero supported incoming edges and obligations remain. Retain bounded audit/tombstone evidence for late events and incident reconstruction.

### Verify graph and domain behavior

Generate DAGs, self-edges, two-node and long cycles, dense fan-in/fan-out, dynamic edge changes, and strongly connected components. Compare detected paths/components with the model. Randomize object/file/list order and verify identical eligibility.

Inject absent, false, unknown, stale, wrong-generation, incompatible, unauthorized, and recreated-UID dependencies. Drop watch events, rebuild indexes, partition one provider, and recover high-fan-out targets without storms.

Race upgrades, grant revocation, consumer creation, dependency deletion, finalizers, and restore. Test hard, soft, optional, conditional, and quorum policies. Assert domain outcomes: no unauthorized secret read, no consumer starts on incompatible schema, independent branches progress, shared outages stay bounded, cycles never masquerade as transient waits, and deletion preserves required backup/ownership.

## Definitions and Notation

Let $G=(V,E)$ be a directed dependency graph. Edge $(u,v)$ means consumer $v$ requires predicate $P_{uv}$ over evidence from prerequisite $u$ before a named action. Each vertex has immutable identity $I(v)$, desired generation $g_v$, and trusted status projection $S_v(t)$.

Define edge evaluation

$$
q_{uv}(t)=P_{uv}(S_u(t),g_v,\kappa_{uv})\in\{T,F,U\},
$$

where $\kappa_{uv}$ contains required capability/version, freshness, authorization, hardness, and lifecycle mode. For hard incoming edges $H(v)$, ordinary conjunctive eligibility is false if any $q=F$, true if all are $T$, and unknown otherwise.

A **path** is a sequence of directed adjacent vertices. A **cycle** begins and ends at the same vertex. A **DAG** is acyclic. A **topological order** places every $u$ before $v$ for $(u,v)\in E$. A **strongly connected component** contains mutual reachability; size greater than one, or a self-loop, identifies a cycle.

For duration $w(v)\ge0$ and DAG predecessors $pred(v)$,

$$
EF(v)=w(v)+\begin{cases}0,&pred(v)=\varnothing;\\\max_{u\in pred(v)}EF(u),&\text{otherwise}.
\end{cases}
$$

The critical-path lower bound is $T_{cp}=\max_v EF(v)$ with unlimited capacity and exact durations. Resource constraints can only keep or increase completion time.

Creation graph $G_c$, update/migration graph $G_m$, and deletion graph $G_d$ may differ. Ownership/lifecycle edge $L(u,v)$ is distinct from readiness edge $E(u,v)$ and data reference $R(u,v)$.

## Mechanisms, Invariants, or Proof Structure

### Dependency protocol

1. Parse typed references and capability requirements from admitted desired state.
2. Authorize scope and target-side grants before revealing or consuming target information.
3. Resolve names/selectors to unambiguous immutable UIDs and record graph revision.
4. Build create/update/delete edge sets with hard/soft/optional/conditional/quorum semantics.
5. Validate self-edges, duplicates, target kinds, grants, and cycles; report concrete components.
6. Observe producer-owned conditions/outputs with generation, version, source, and freshness.
7. Evaluate edge predicates and aggregate against one membership/graph revision.
8. Enqueue eligible bounded work through reverse indexes, fair limits, coalescing, and jitter.
9. Publish bounded dependency status and shared root cause without cross-tenant leakage.
10. Re-evaluate continuously on desired, target, grant, policy, deletion, timer, and resync events.
11. Migrate and retire edges, producers, grants, indexes, and restore artifacts only after dependency inventories close.

### Topological-order theorem and limits

In any finite DAG, some vertex has indegree zero; otherwise following predecessors indefinitely in a finite set repeats a vertex and forms a cycle. Remove a zero-indegree vertex and its outgoing edges. The remaining graph is a DAG, so induction produces a topological order. Conversely, a directed cycle cannot have a topological order because each member would need to precede the next and the last precede the first.

This theorem establishes structural schedulability of strict edges. It does not prove predicate truth, worker fairness, provider availability, safe effects, adequate capacity, or liveness under changing graphs. A DAG can wait forever on a false external predicate.

### Executable dependency inventory

The following synthetic classifier checks ten designs against ten dependency controls. It neither creates resources nor proves a production graph safe.

<!-- bijux-verify: {"id":"dependency-contract-inventory","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"schedulable=2\nblocked=6\nunsafe=2\n"}} -->
```python
required = {
    "uid_resolved", "target_authorized", "capability_specific",
    "generation_fresh", "cycle_checked", "failure_policy",
    "reverse_index", "bounded_fanout", "delete_graph", "restore_tested",
}

designs = {
    "application": required,
    "database": required,
    "name-only": required - {"uid_resolved"},
    "cross-tenant": required - {"target_authorized", "uid_resolved"},
    "exists-only": required - {"capability_specific"},
    "stale-ready": required - {"generation_fresh"},
    "hidden-cycle": required - {"cycle_checked"},
    "retry-storm": required - {"failure_policy", "bounded_fanout"},
    "scan-only": required - {"reverse_index"},
    "reverse-delete": required - {"delete_graph"},
}

counts = {"schedulable": 0, "blocked": 0, "unsafe": 0}
for controls in designs.values():
    missing = required - controls
    category = "schedulable" if not missing else ("blocked" if len(missing) == 1 else "unsafe")
    counts[category] += 1
for category in ("schedulable", "blocked", "unsafe"):
    print(f"{category}={counts[category]}")
```

The labels force review; they are not severity measurements. The two complete rows still need live authorization, observation, concurrency, provider, upgrade, deletion, and restore evidence.

## Alternatives and Trade-Offs

### Inferred references versus explicit dependencies

Typed data references reveal precise relationships and changes. Hidden behavioral prerequisites need explicit edges. Broad explicit dependencies are easy but serialize unrelated work and expand unknown values. Infer when semantics are clear; declare what cannot be inferred.

### Direct observation versus copied aggregate

Direct target observation preserves freshest evidence and detail but increases coupling and permissions. A copied aggregate narrows the interface and scales access but adds staleness and trust hops. Bind aggregates to target UID/version/time and use the narrowest sufficient capability API.

### Hard versus soft edge

Hard gates protect correctness but expand availability coupling. Soft edges preserve service with reduced quality but require an honest degraded contract. Risk and consumer capability decide; “soft” must not weaken safety prerequisites.

### Static DAG versus dynamic graph

Static graphs are easy to validate, visualize, and schedule. Dynamic selection supports fleets and policy but can introduce runtime cycles, ambiguity, and authorization changes. Constrain selectors and continuously validate resolved graph revisions.

### Central orchestrator versus distributed controllers

A central owner gives coherent multi-step decisions and cycle resolution but becomes a large coupling/failure boundary. Distributed controllers preserve autonomy and scalability but need explicit conditions, identity, and failure policy. Use joint workflow resources for true coordination, not every reference.

### Polling versus reverse-indexed events

Polling is simple and repairs lost events but costs latency and load. Reverse indexes enable prompt targeted enqueue but must be rebuilt and can be stale. Combine event indexing with periodic authoritative resync.

### Fail closed versus bounded last-known operation

Fail closed protects security and consistency but can amplify dependency outage. A bounded lease on last-known data preserves availability but risks stale behavior. Classify by capability, duration, revocation semantics, and audit.

### One global readiness versus capability conditions

One Boolean is easy for users but over-couples unrelated health. Capability-specific conditions allow precise gates at API complexity cost. Provide a documented summary while retaining exact edge predicates.

### Creation-order reuse versus separate deletion graph

Reverse creation order is a useful default for pure ownership trees. Retention, shared resources, traffic, backups, and cleanup channels change edges. Derive and persist deletion obligations explicitly.

### Wide parallel waves versus conservative sequencing

Wide waves reduce critical path but can overwhelm providers and failure domains. Conservative sequencing reduces load but wastes independence. Use graph eligibility plus resource/tenant/provider concurrency controls.

### Cross-namespace grant versus cluster-wide privilege

Target-side grants preserve tenant consent and information boundaries at operational/schema cost. Cluster-wide controller privilege is simpler but creates confused-deputy risk. Prefer explicit grants for tenant-authored references.

### Version equality versus compatibility range

Equality is simple for lockstep rollout but causes unnecessary coupling. Compatibility ranges allow gradual migration but require durable contract tests and expand/contract discipline. Model the actual compatibility relation.

## Failure Modes and Misconceptions

1. **“File order is dependency order.”** Declarative APIs and controllers may process objects independently.
2. **“A reference means ownership.”** Data use does not authorize garbage collection or mutation.
3. **“Exists means ready.”** Admission, reconciliation, health, and capability can still be absent.
4. **“Ready means compatible.”** The consumer may require another schema, region, audience, or revision.
5. **“True stays true.”** Conditions need generation, source, and freshness.
6. **“Missing dependencies should be retried quickly.”** Shared outages turn fan-out into retry storms.
7. **“Backoff resolves cycles.”** A strict prerequisite cycle has no enabled vertex.
8. **“There is one topological order.”** Independent vertices permit many correct orders and parallelism.
9. **“A DAG eventually completes.”** External predicates can remain false and workers/providers can fail.
10. **“Every dependency should be hard.”** Optional capabilities can create needless availability coupling.
11. **“Soft means ignore failure.”** It requires a specified degraded behavior and status.
12. **“Labels securely select dependencies.”** Mutable selectors can cross ownership boundaries or become ambiguous.
13. **“Source permission authorizes cross-tenant reads.”** Target owner consent and non-disclosure are separate.
14. **“One parent should copy all child status.”** This creates unbounded, stale, conflict-prone objects.
15. **“Consumers should repair providers.”** Reconcile at the owning layer; consumers apply local failure policy.
16. **“Server readiness is enough for migration.”** Lockstep/expand-contract needs version compatibility and stage evidence.
17. **“Deletion is reverse creation.”** Shared ownership, retention, backup, traffic, and cleanup channels alter order.
18. **“Owner references work cross-namespace.”** Kubernetes scope rules disallow that ownership pattern.
19. **“A wave is a transaction.”** Partial effects and later drift remain independently reconciled.
20. **“Stopping a producer removes dependencies.”** Stored green status and restore artifacts remain until freshness and retirement close them.

## Worked Examples

### Example 1

**Situation.** An application references a database object that exists and is `Ready=True` for generation 4, while the database spec is generation 5 and provided schema is v3; the application requires v4.

**Reasoning.** Resolution proves only object identity. Readiness is stale relative to target generation, and the provided capability is incompatible. The edge evaluates unknown/false according to contract and blocks rollout while preserving any previously safe serving version. It reports required v4, observed v3, dependency UID, and stale generation without starting the new application.

**Conclusion.** Gate on current compatible capability, not object existence or an unqualified green condition.

### Example 2

**Situation.** A Route in namespace `shop` references a Service in `payments`, but no target-owned grant permits it.

**Reasoning.** The privileged controller must not reveal whether the Service exists. It reports `ReferenceNotPermitted` and identifies the missing authorization class, not target details. The payments owner may add a narrow grant for Routes from `shop` to Services. The controller watches grant changes and then resolves/binds UID.

**Conclusion.** Cross-namespace resolution is an authorization handshake with non-disclosure, not a privileged lookup convenience.

### Example 3

**Situation.** A→B, B→C, and C→A are hard readiness edges.

**Reasoning.** Every vertex has indegree one, so Kahn’s algorithm finds no initial zero-indegree vertex. An SCC algorithm returns `{A,B,C}`. Retries cannot create readiness. The platform must reject the graph, make one edge a safe staged bootstrap predicate, or place the joint transition behind an explicit workflow owner.

**Conclusion.** Report the concrete cycle and redesign it; do not classify it as transient unready state.

### Example 4

**Situation.** Service requires database and identity; telemetry is optional. Database is true, identity unknown, telemetry false.

**Reasoning.** Hard conjunction is unknown because identity evidence is inadequate. Telemetry absence/false follows its documented optional policy and produces `TelemetryDegraded=True` but does not decide core readiness. If identity becomes current false, core dependency status becomes false. If it becomes true, the service may proceed degraded.

**Conclusion.** Hard and optional edges require separate aggregation and honest degraded status.

### Example 5

**Situation.** One identity provider with 100,000 consumers becomes unknown.

**Reasoning.** A reverse UID/capability index identifies consumers. Queue keys coalesce; per-provider and tenant limits plus jitter prevent active-probe storms. The identity controller owns recovery. Consumers apply bounded last-known or fail-closed policy locally and update only semantic status. Metrics aggregate affected count; status samples blockers rather than listing all consumers.

**Conclusion.** Indexing, shared-cause reporting, and rate/failure policy contain fan-out amplification.

### Example 6

**Situation.** DAG durations are network 3, identity 4, database 8 after network, application 5 after database and identity, and route 2 after application.

**Reasoning.** $EF(network)=3$, $EF(identity)=4$, $EF(database)=8+3=11$. Application waits for max(11,4), so $EF(application)=5+11=16$. Route finishes at $2+16=18$. The network→database→application→route path is critical at 18 units under unlimited capacity; identity has slack.

**Conclusion.** Critical path identifies the structural lower bound and optimization target, not provider/worker-constrained completion.

### Example 7

**Situation.** A selector intended to choose one production database matches two after a label change.

**Reasoning.** Arbitrarily choosing the first makes serialization order into authority and can leak/corrupt tenants. Resolution becomes `AmbiguousReference`; the consumer freezes new effects while preserving a safe serving state. Admission should constrain selector/cardinality, and binding should persist UID so later label drift cannot silently rebind.

**Conclusion.** Ambiguous dynamic reference is a blocked configuration, never a nondeterministic choice.

### Example 8

**Situation.** Application v5 supports database schemas 4–6; database plans migration 4→5→7.

**Reasoning.** Compatibility $C(5,s)$ holds for 4,5,6 but not 7. Database may expand to 5 while app runs. Before contract to 7, consumers must upgrade to versions supporting 7 and report current compatible readiness. The migration workflow inventories all incoming edges, gates contraction, and retains rollback data until the commit point.

**Conclusion.** Encode compatibility relation and expand/migrate/contract stages rather than raw version equality or producer-first updates.

### Example 9

**Situation.** Creation order is network→database→application. Database is retained on application deletion and needs network for final backups.

**Reasoning.** Blind reverse order deletes application, then database, then network—violating retain. The deletion graph drains application traffic, revokes application credentials, transfers/retains database ownership, verifies its network requirement, and removes only application-specific network bindings. Shared network deletion belongs to its owner after all consumers detach.

**Conclusion.** Model deletion ownership and prerequisites separately from creation readiness.

### Example 10

**Situation.** A cluster is restored from yesterday. Dependency names exist, some UIDs changed, and old `Ready=True` conditions remain.

**Reasoning.** Rebuild reference graph and target-side grants from authoritative desired state. Compare recorded UIDs; changed incarnations require rebind policy and authorization. Expire old observations, wait for compatible producers to publish current generation/freshness, and fence pre-restore controllers. Do not launch consumers from restored green status.

**Conclusion.** Restore reconstructs identity, authorization, graph revision, and fresh evidence before enabling dependency actions.

## Cross-Program Connections

1. **Algorithms and Data Structures:** adjacency lists, topological sort, SCCs, reachability, critical paths, and incremental indexes implement dependency planning.
2. **Distributed Systems:** partial observation, eventual consistency, failure detection, fan-out amplification, and lack of atomic snapshots bound evidence.
3. **API & Service Engineering:** typed references, capability/version negotiation, conditions, pagination, authorization errors, and compatibility are public contracts.
4. **Security Engineering:** target-side grants, confused deputy prevention, non-disclosure, selector control, tenant binding, and credential projection protect references.
5. **Reliability Engineering:** bulkheads, circuit breakers, backoff, jitter, fairness, root-cause propagation, and recovery objectives bound shared failure.
6. **Database Systems:** foreign keys, materialized indexes, transactions, referential integrity, MVCC snapshots, and cascading actions offer useful analogies and contrasts.
7. **Control Theory:** coupled loops, delays, oscillation, hierarchy, and stability explain why peer controllers need ownership and bounded feedback.
8. **Software Architecture:** dependency inversion, interfaces/capabilities, bounded contexts, compatibility, and lifecycle ownership keep graphs evolvable.
9. **Data Engineering:** DAG schedulers, task retries, data freshness, lineage, fan-in joins, and backfill resemble resource dependency reconciliation.
10. **Systems Engineering:** interface control, hazard chains, modes, critical paths, verification, lifecycle disposal, and configuration baselines frame end-to-end safety.

## References

1. Kubernetes. [Owners and Dependents](https://kubernetes.io/docs/concepts/overview/working-with-objects/owners-dependents/). Retrieved 2026-09-02.
2. Kubernetes. [Garbage Collection](https://kubernetes.io/docs/concepts/architecture/garbage-collection/). Retrieved 2026-09-02.
3. Kubernetes SIG Architecture. [API Conventions](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md). Retrieved 2026-09-02.
4. Kubernetes. [Kubernetes API Concepts](https://kubernetes.io/docs/reference/using-api/api-concepts/). Retrieved 2026-09-02.
5. Kubernetes Gateway API. [ReferenceGrant](https://gateway-api.sigs.k8s.io/reference/api-types/referencegrant/). Retrieved 2026-09-02.
6. Kubernetes Gateway API. [Security Model](https://gateway-api.sigs.k8s.io/docs/concepts/security/). Retrieved 2026-09-02.
7. Flux. [Kustomization dependencies](https://fluxcd.io/flux/components/kustomize/kustomizations/). Retrieved 2026-09-02.
8. Argo CD. [Sync Phases and Waves](https://argo-cd.readthedocs.io/en/stable/user-guide/sync-waves/). Retrieved 2026-09-02.
9. HashiCorp. [Terraform Dependency Graph](https://developer.hashicorp.com/terraform/internals/graph). Retrieved 2026-09-02.
10. HashiCorp. [`depends_on` reference](https://developer.hashicorp.com/terraform/language/meta-arguments/depends_on). Retrieved 2026-09-02.
11. Crossplane. [Compositions](https://docs.crossplane.io/latest/composition/compositions/). Retrieved 2026-09-02.
12. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. *Introduction to Algorithms*, 4th ed. MIT Press, 2022. See graph traversal, topological sorting, and strongly connected components.
13. Leslie Lamport. “Time, Clocks, and the Ordering of Events in a Distributed System.” *Communications of the ACM* 21(7), 1978.
14. Martin Kleppmann. *Designing Data-Intensive Applications*. O'Reilly Media, 2017. See partial order, replication, streams, and distributed-system faults.

## Exercises

### Exercise 1

Specify a dependency edge from an application to a database, including identity, capability, compatibility, readiness, generation, freshness, authorization, hard/soft behavior, events, and deletion semantics.

### Exercise 2

For edges A→C, B→C, C→D, B→E, and E→F with durations A=2, B=4, C=5, D=3, E=6, F=1, produce topological waves and compute earliest finishes and critical-path time.

### Exercise 3

A graph contains A→B, B→C, C→A, C→D, and E→F. Diagnose schedulability, identify the relevant SCC, and propose two safe redesigns rather than retries.

### Exercise 4

Design fan-out failure handling for one shared certificate authority serving 250,000 resources across tenants. Include indexing, authorization, freshness, retry control, status, prioritization, recovery, and observability.

### Exercise 5

Design a rolling upgrade and later deletion for application, database, identity, network, backup, and DNS resources with cross-namespace references, shared ownership, compatibility ranges, restored backups, and a controller being retired.

## Answers to the Exercises

### Answer 1

Use source application UID/generation and a typed target reference constrained to the database API/kind, namespace/name, then persist resolved database UID. Require target-side grant for cross-namespace/tenant use. The capability is a write endpoint plus schema/API range, region, encryption/policy digest, and credential audience—not generic existence. Predicate requires trusted database-produced readiness, matching database observed generation, provided contract within application-supported range, and observation age within the action’s freshness bound.

Mark core database access hard; define whether an already serving application may continue on last-known evidence for a bounded lease while new rollout blocks. Index database UID/capability to application key and resync periodically. Status records graph revision, resolved/authorized/compatible states, bounded reason, and no credential. On application deletion, drain and revoke only its access; a shared/retained database is not garbage-collected. On database deletion, block new grants, detach/transfer consumers, preserve final-backup/network obligations, and never infer lifecycle ownership from the reference.

### Answer 2

Initial zero-indegree vertices are A and B, so wave 1 is `{A,B}`. After both, C and E are eligible, giving wave 2 `{C,E}`. D follows C and F follows E, so wave 3 is `{D,F}`. Other topological orders interleaving independent branches are valid.

$EF(A)=2$ and $EF(B)=4$. $C$ waits for both, so $EF(C)=5+\max(2,4)=9$. $D=3+9=12$. $E=6+4=10$, and $F=1+10=11$. Critical-path lower bound is 12 on B→C→D. It assumes exact durations and unlimited workers/provider capacity; constrained scheduling can take longer.

### Answer 3

The graph is not a DAG because `{A,B,C}` is a strongly connected component with cycle A→B→C→A. D is downstream of the cycle and cannot become eligible under strict prerequisites. E→F is independent and should progress; a global stop would unnecessarily expand the failure domain.

One redesign identifies a false hard edge and replaces it with an explicit bootstrap capability—for example A can start in restricted mode without C, then B and C initialize, then A transitions to full mode with guards and credential rotation. Another introduces one joint workflow/composition resource owning A/B/C stages and effects, exposing children as observations; this makes commit/recovery explicit. Simply making all edges soft, choosing file order, or retrying does not prove safety.

### Answer 4

Resolve each consumer to immutable CA/capability UID under tenant/grant policy and maintain a rebuildable reverse index. CA status publishes current signing/validation capability, contract/key epoch, observed generation, source, and freshness. Consumers distinguish issuing new certificates from validating existing ones; new issuance may fail closed while existing certificates remain usable until a bounded expiry/revocation rule.

On shared failure, enqueue consumer keys with coalescing and tenant/provider rate limits, jitter, circuit breaking, and fair priority. The CA controller owns repair; consumers do not all probe or recreate it. Prioritize imminent expiry, revocation, and security-critical rotation over routine rollout. Report one root cause with affected counts and bounded samples; each resource reports its own current generation and policy without copying the fleet. Metrics cover fan-out, age, expiry risk, queue fairness, retry suppression, and recovery waves without UID labels.

Recovery requires fresh CA epoch/status and each consumer re-evaluating current intent; do not bulk-stamp readiness. Test dropped events/index rebuild, cross-tenant non-disclosure, stale green status, key epoch mismatch, 250,000 simultaneous timers, controller failover, and restore against newer CA state.

### Answer 5

Define typed, UID-bound, target-authorized edges: application needs identity audience, database schema range, network route, and DNS publication; database needs network and backup/key capabilities; cross-namespace uses narrow target-owned grants. Publish capability versions and fresh generation-correlated conditions. Build a DAG per lifecycle and reject cycles.

Upgrade with expand/migrate/contract: database and identity first expand compatibility, application versions migrate in bounded waves only when matching capabilities are ready, then providers contract old schema/audience after every incoming edge reports migration. Network/DNS rollout gates traffic separately from object creation. Shared dependencies use reverse indexes, provider/tenant limits, and root-cause suppression.

Deletion gets a separate graph: block new grants/traffic, drain application, preserve network/key for required backup, revoke application credentials, detach DNS, then delete or transfer application-owned resources. Shared database/identity/network are retained under their owners; reference does not authorize deletion. Finalizers persist obligations and immutable IDs.

After restore, rebuild grants and graph, compare UIDs, expire status, and re-observe providers before enabling work. To retire a controller, stop new edges, inventory live and backup references across versions, deploy a compatible successor/adapters, drain or migrate checkpoints and conditions, test restore, then remove grants/indexes/RBAC/CRDs/credentials only after zero supported incoming edges and deletion obligations remain.
