---
module_id: PLAT-071
program: Platform Engineering
level: 2
module_number: 71
title: Tenant Models
status: complete
last_verified: 2026-09-02
---

# Tenant Models

## One-Page Review

### Governing question

How should a platform define tenants and choose what they share or isolate across identity, control plane, compute, network, data, keys, quotas, observability, operations, and recovery so the promised security, fairness, residency, customization, cost, and blast radius are demonstrably true?

### Essential definitions

- A **tenant** is a governed administrative and isolation principal whose users, workloads, data, resources, budgets, policies, and lifecycle share an accountable boundary.
- **tenant identity** is a stable immutable identifier derived from a trusted mapping, distinct from display name, organization name, namespace, account, subscription, cluster, or deployment.
- A **tenant context** binds authenticated actor/workload, tenant ID, entitlements, placement, and request purpose at a trust boundary.
- A **pooled model** shares a resource among tenants and enforces separation logically through identity, policy, keys, partitions, row attributes, and quotas.
- A **silo model** dedicates a resource stack or layer to one tenant, improving some isolation properties while increasing fleet cost and variation risk.
- A **bridge model** mixes pooled and siloed layers, such as shared control plane with tenant-dedicated data stores.
- A **deployment stamp/cell** is an independently deployable scale and failure unit hosting one or more assigned tenants.
- A **placement record** is the authoritative versioned mapping from tenant to region, stamp, isolation tier, data/key domains, and lifecycle state.
- **security isolation** prevents unauthorized cross-tenant access or influence; **performance isolation** constrains noisy-neighbor resource consumption.
- **control-plane isolation** separates configuration, identity, policy, management APIs, and operators; **data-plane isolation** separates runtime execution, traffic, and data.
- A **tenant cohort** groups tenants with compatible region, classification, isolation, version, capacity, and operational requirements.
- **tenant lifecycle** covers request, verification, provisioning, activation, suspension, migration, export, deletion, evidence retention, and identifier tombstoning.

### Central model, mechanism, or theorem

Model tenant $t$ by requirement vector

$$
R_t=(a,c,d,n,k,q,r,o),
$$

covering access/threat, compute, data, network, keys, quota/fairness, residency/recovery, and operations. For each platform layer $\ell$, choose placement/isolation function $I(t,\ell)$ from pooled partition, pooled cell, dedicated layer, or dedicated stack. The choice is valid only when controls and evidence satisfy $R_t$ under failures and administrator actions. Tenant identity is resolved from authenticated routing context to an immutable ID before any data access; every query, cache key, event, job, metric drill-down, backup, and provider resource preserves that ID. A dedicated namespace or account is evidence for only the boundary it actually controls, not a proof of end-to-end tenant isolation.

### Critical invariants

- Tenant ID comes from trusted identity/routing and is never accepted solely from a client-supplied body, query, or mutable name.
- Tenant, user, workload, organization, project, environment, billing account, and infrastructure container identities remain distinct and explicitly related.
- Every shared layer enforces tenant scope server-side and defaults closed when context is absent, ambiguous, suspended, or stale.
- Cache keys, queues, topics, search indexes, files, object paths, logs, traces, backups, exports, and support tools preserve tenant confinement.
- Resource budgets and admission prevent one tenant from exhausting shared compute, memory, storage, connections, API rate, queue, or operator capacity.
- Placement is authoritative, versioned, auditable, and reconciled; request routing and background work cannot guess it from a name.
- Isolation tier is an enforceable contract with tested controls, exclusions, SLOs, cost, and migration behavior—not a marketing label.
- Dedicated resources still use least privilege, tenant context, patching, quotas, and verification; physical separation does not cure control-plane mistakes.
- Cross-tenant analytics, support, administration, migration, and incident response use explicit privileged workflows with purpose, approval, bounds, and audit.
- Tenant suspension blocks new effects without destroying recovery evidence; deletion separately handles live resources, replicas, backups, keys, exports, and legal holds.
- Schema/version rollouts and rollback preserve compatible operation across all tenant cohorts and stamps.
- A tenant ID is not reused after deletion while retained records, tokens, caches, events, or audit references could collide.

### Common failures

Namespace called a tenant; organization display name as key; tenant ID trusted from HTTP body; `WHERE tenant_id` omitted in one code path; cache missing tenant dimension; background job loses context; shared queue leaks payloads; wildcard support role; cross-tenant search suggestions; global unique email assumption; per-tenant database with shared superuser; dedicated cluster with shared secrets; quotas only on CPU; pooled connection exhaustion; noisy migrations; unsanitized tenant metrics labels; backups restored into wrong tenant; tenant-to-stamp mapping cached forever; migration with two writable homes; suspension equated with deletion; encryption key deletion before legal hold; bespoke silo configuration drift; premium isolation without tests; and reused tenant identifiers.

### Compact example

Tenant `tn-82` requires EU residency, customer-managed key, production noisy-neighbor protection, and 24-hour restore. The platform maps it to EU stamp `eu-7`, shared control plane, dedicated database/key, pooled compute namespace with enforced CPU/memory/storage/connection/API quotas, and tenant-specific network egress policy. Gateway derives `tn-82` from an audience-bound identity claim and placement revision, not URL input. APIs bind tenant scope into authorization and query; caches use `(tenant,resource,revision)`; jobs/events carry signed context; telemetry uses bounded cohort labels and protected drill-down. Migration to dedicated compute fences writes, copies/verifies data, switches placement atomically, drains old work, and tests rollback before cleanup.

### Connections

This module builds on component authority from [PLAT-070](070-integrating-platform-components-without-creating-a-portal-monolith.md), policy enforcement from [PLAT-066](066-policy-decision-and-enforcement-points.md), environment/account vending from [PLAT-067](067-environment-and-account-vending.md), platform eventing from [PLAT-069](069-platform-eventing.md), and ownership metadata from [PLAT-064](064-ownership-and-metadata.md). PLAT-072 maps tenant models to namespace/account/cluster isolation; PLAT-073 adds quotas; PLAT-074–075 deepen human and workload identity.

## Governing Question

What exactly does “tenant” mean for this platform, which threats and interference must the boundary resist, and at which layers should resources be pooled, partitioned, stamped, or dedicated?

There is no universal tenant primitive. A tenant may be an internal team, business unit, regulated workload group, customer organization, customer environment, or partner. Kubernetes documentation explicitly notes that multi-tenancy has no single definition and that “hard” and “soft” are a spectrum rather than standardized guarantees.

A platform must state its own definition and threat model. Internal teams that trust a central operator differ from mutually hostile external customers. Production data differs from ephemeral preview workloads. One tenant can require different isolation at different layers.

The goal is not maximum separation everywhere. It is sufficient, verified isolation with sustainable economics and operations, plus a migration path when requirements change.

## Why This Matters

Multi-tenancy concentrates efficiency and risk. Shared systems amortize infrastructure and operations, but one missing tenant predicate, cache-key collision, wildcard credential, or unbounded queue can expose data or impair every tenant.

Siloing is not a free safety proof. Hundreds of dedicated stacks can drift, miss patches, exhaust account limits, and become impossible to recover consistently. Shared fleet automation and tenant-aware authorization remain necessary.

Tenant decisions also harden over time. IDs enter databases, tokens, object paths, metrics, events, invoices, encryption keys, and third-party systems. Placement affects residency, latency, cost, and restore. Treat the model as a first-class platform contract before scale makes change hazardous.

Finally, operations are often the weakest boundary. Support search, bulk export, backup restore, incident tooling, and migrations legitimately cross normal scopes. Without constrained privileged workflows, strong application isolation can be bypassed by routine administration.

## Prerequisites and Retrieval

Retrieve authentication and authorization, threat modeling, data classification, Kubernetes namespaces/RBAC/network policy, cloud accounts/subscriptions/projects, database row-level security and schemas, encryption/key management, quotas and rate limiting, deployment stamps/cells, sharding, routing, eventing, caching, observability, backups, disaster recovery, fleet management, billing, and data lifecycle.

Distinguish tenant from user; tenant from team/organization; tenant from infrastructure container; logical partition from security boundary; pooled from stamped; stamp from region; control plane from data plane; security isolation from performance isolation; authentication claim from trusted resolved context; tenant ID from display name; placement from routing cache; encryption from authorization; quota from capacity; suspension from deletion; deletion from key destruction; migration copy from authority cutover; and per-tenant customization from code fork.

## Learning Objectives

After completing this module, you should be able to:

1. define tenants, hierarchies, memberships, entitlements, and lifecycle for a platform;
2. create a threat- and requirement-based isolation matrix across platform layers;
3. choose pooled, siloed, bridge, cell, and tiered patterns deliberately;
4. derive and propagate trusted tenant context through APIs, events, jobs, data, and telemetry;
5. prevent cross-tenant access in storage, cache, search, messaging, and administrative tools;
6. design performance fairness across every exhaustible shared resource;
7. automate tenant placement, fleet rollout, migration, suspension, export, and deletion;
8. validate isolation with negative, adversarial, restore, and noisy-neighbor tests;
9. measure tenant SLOs without leaking identifiers or creating unbounded telemetry; and
10. evolve isolation tiers and tenant topology without dual authority or identifier collision.

## Core Exposition

### Define the tenant in domain terms

Write a precise statement: “A tenant is the boundary within which these principals share these resources and policy, and across which these access/interference properties are prohibited.” Name the accountable business owner and platform owner.

Do not substitute a deployment primitive. A namespace may host one workload; a team may own many namespaces; one customer may have development and production tenants; one stamp may host hundreds of tenants.

Give every tenant an immutable opaque ID. Mutable name, slug, domain, billing label, and identity-provider organization are attributes/mappings. Preserve old aliases and collision/tombstone records.

Model hierarchy only where semantics require it: enterprise, division, tenant, project, environment. Authorization and billing inheritance must be explicit; tree structure does not automatically grant access.

### Separate identity, membership, and entitlement

Tenant identity answers “which governed boundary?” Membership relates users/workloads/groups to that tenant under role, validity, source, and provenance. Entitlement says which capability, tier, region, quota, or feature the tenant may use.

Do not encode all three in a role string or namespace name. Membership changes frequently; tenant identity and historical audit must remain stable.

Federate users and workloads through trusted issuers and map external organization/group claims to internal tenant IDs. Validate issuer, audience, subject, expiry, and mapping revision. Ambiguity or absent mapping fails closed.

Service accounts and background jobs have workload identity plus explicit tenant scope. A global worker may process many tenants, but each work item re-establishes context and authorization.

### Build an isolation requirement matrix

For each tenant/cohort, record adversaries, trust between tenants, operator trust, data class, residency, encryption/key ownership, availability, noisy-neighbor tolerance, recovery, customization, audit, deletion, scale, and cost.

For each layer—edge/routing, API/control plane, compute, network, database, object storage, cache, search, messaging, secrets/keys, observability, backup, CI/CD, support—record sharing choice, controls, residual risk, owner, and test evidence.

Avoid vague “hard isolation.” State whether tenants can share kernel, node, cluster control plane, cloud account, database server, encryption key, broker, operators, or backup media, and what attacks are in scope.

Review the matrix when classification, tenant trust, product tier, region, or platform capability changes. Isolation is a living contract.

### Choose pooled, silo, bridge, or stamped placement

Pooled infrastructure maximizes utilization and uniform operation. It demands tenant-aware application logic, defense in depth, fairness controls, and strong negative testing.

Silo infrastructure dedicates a layer or stack. It can reduce data/performance blast radius and satisfy customer constraints, but multiplies cost, fleet rollout, monitoring, patching, backup, and quota management.

Bridge models isolate selected layers: dedicated database or key with pooled compute; dedicated account with shared portal/control plane. This often matches real requirements better than all-or-nothing tiers.

Deployment stamps/cells host bounded cohorts. They cap blast radius and scale horizontally. Maintain authoritative tenant-to-stamp placement and automate identical-but-versioned fleet delivery.

### Treat tenant placement as control-plane state

Placement maps tenant to region, stamp, isolation tier, database shard, key domain, version ring, and lifecycle state. It has stable revision, effective time, audit, and reconciliation.

Resolve placement before accessing tenant data. Cache it with bounded freshness and invalidation; sensitive mutations can require current revision. Never infer from tenant name or accept a client-selected database endpoint.

Routers validate authenticated tenant context and select only allowed placement. Downstream services confirm context matches resource ownership. Avoid a trusted router becoming the sole isolation layer.

Placement changes are workflows, not table edits. They coordinate write fencing, copy, verification, cutover, caches, jobs, events, rollback, and cleanup.

### Establish trusted tenant context

At ingress, derive tenant from authenticated identity, selected authorized membership, hostname/route bound by server configuration, or signed token claim. If users can belong to several tenants, require an explicit selection then verify membership.

Represent context as immutable request-scoped data: tenant ID, actor/workload, issuer, audience, scopes/roles, placement revision, correlation, and delegation. Do not use process-global variables.

Every service authenticates the caller and authorizes tenant/action/resource. A plain `X-Tenant-ID` header is not trusted unless a controlled gateway strips client input and signs/derives it under a documented trust contract.

Events and jobs carry tenant ID with producer identity and authorization provenance. Consumers reject missing/unknown/suspended tenants rather than route to a default.

### Enforce data isolation at several layers

Application repositories require tenant context in their interface. Queries bind it; resource IDs are verified under it. Composite keys and uniqueness constraints include tenant where uniqueness is tenant-local.

Use database policies such as row-level security where available as defense in depth, with session context set safely per transaction/connection. Test connection-pool reuse and privileged bypass roles. A shared superuser defeats policy.

Schema-per-tenant and database-per-tenant increase separation but create migration, connection, backup, and fleet problems. Catalog the mapping and automate every operation.

Object paths, file names, warehouse partitions, snapshots, and exports include opaque tenant identity and server-enforced access. User-supplied path fragments never select another tenant.

### Partition caches, search, and derived views

Cache keys contain tenant ID plus resource and relevant policy/version dimensions. Authorization-filtered results must not be shared across users/tenants under a broad key.

Search filters tenant authorization before query, facets, counts, autocomplete, spelling, snippets, and ranking. An index may use physical per-tenant partitions or verified filters, but every query path and administrative browse is tested.

Derived projections preserve source tenant ID and deletion/suspension signals. Reconciliation detects orphan or cross-tenant documents.

When a tenant migrates, invalidate old placement/cache keys without allowing the new location to read another tenant's stale entries.

### Isolate messaging and asynchronous work

Choose shared topic with tenant-aware ACL/filter, per-cohort topic, or per-tenant destination based on confidentiality, rate, retention, and scale. Topic proliferation and wildcard privileges are real costs.

Envelope tenant must be bound to authenticated producer authority. Consumers authorize subscriptions and validate every message. Dead-letter and replay tools preserve the same confinement.

Queue fairness prevents a noisy tenant from starving others. Partitioning by tenant may create hot keys; weighted scheduling or per-cohort queues can protect critical tenants.

Background workers clear context between tasks. Idempotency receipts include logical consumer and tenant so identical resource/event IDs across tenants never collide.

### Design network and compute boundaries

Network policy constrains allowed flows but does not replace application authorization or encryption. Account for ingress, egress, DNS, metadata service, node-local agents, control-plane endpoints, and shared proxies.

Compute isolation options include process, container, pod, namespace, node pool, cluster, VM, dedicated host, account, and physical infrastructure. Each protects different threat/failure surfaces.

Kubernetes namespaces scope names and many policies, but cluster-scoped resources, nodes, control plane, admission, CRDs, webhooks, and privileged workloads remain shared. PLAT-072 treats these boundaries directly.

Schedule hostile or regulated tenants onto stronger boundaries. Test escape assumptions against the actual runtime and provider shared-responsibility model.

### Separate keys and secrets deliberately

Shared provider-managed encryption at rest protects lost media but may not isolate tenants from application/operator access. Tenant-specific envelope keys or customer-managed keys support stronger separation and revocation contracts.

Bind secret paths and key policies to tenant identity and workload. Do not let a portal or global worker enumerate all tenants without justified privilege.

Key rotation, disablement, escrow, restore, and destruction are tenant lifecycle steps. Destroying a key may be irreversible and conflict with legal hold or recovery.

Record which copies remain encrypted under which key: primary, replica, event, cache, export, quarantine, log, and backup.

### Engineer performance fairness

Inventory every exhaustible resource: CPU, memory, ephemeral/storage IO, network, API concurrency/rate, database connections/locks, cache capacity, broker partitions/storage, job workers, external-provider quota, and operator attention.

Set admission, reservation, limit, queue, rate, and burst policy per tenant/cohort. A CPU quota does not prevent connection-pool or queue exhaustion.

Observe utilization and throttling by bounded cohort/tier labels; protected drill-down can resolve tenant. Avoid tenant ID as a high-cardinality public metric label.

Test noisy neighbors and failure amplification. Autoscaling shared capacity without per-tenant fairness can reward an abusive tenant and inflate cost.

### Preserve tenant-aware authorization

Authorization is a relation among actor/workload, tenant, action, resource, environment, policy revision, and context. Verify resource tenant from authoritative data rather than trust an ID pair supplied by the caller.

Platform administrators need separate scoped roles. Support access is time-bound, purpose-bound, approved when required, logged, and visible. “Super-admin” should not be routine support workflow.

Cross-tenant operations—fleet rollout, aggregate billing, abuse detection—use dedicated services and data products with minimum fields, not bypass flags in ordinary endpoints.

Confused-deputy defense ensures a privileged service cannot be induced by tenant A to act on tenant B through an unvalidated resource reference.

### Customize without tenant forks

Represent differences as governed entitlement, policy, configuration, template/class, feature flag, or placement tier. Validate scopes and compatible combinations.

Per-tenant code branches and infrastructure edits cause drift and make security fixes inconsistent. If a capability cannot be supported uniformly, expose it as a product tier with owner and lifecycle.

Deployment rings can roll versions across stamps/cohorts, but security compatibility and rollback remain bounded. Do not leave a tenant permanently on an unpatched fork.

Track configuration provenance, effective version, expiry, and exceptions. Tenant-controlled configuration is untrusted input.

### Design tenant-aware observability

Operators need per-tenant diagnosis without leaking identities or overwhelming telemetry. Use stable service/stamp/tier/cohort labels for aggregate metrics and protected logs/traces for exact tenant.

Propagate tenant context as sensitive baggage only when necessary and trusted. Sanitize error messages and prevent tenant-controlled values from metric names/labels.

SLOs can be measured per tier/stamp and audited for high-value tenants. Global averages hide one tenant consistently harmed by hot placement.

Audit tenant context resolution, privileged access, placement changes, policy decisions, exports, suspensions, migrations, and deletions with actor and evidence.

### Operate a fleet, not snowflakes

Maintain desired configuration for all stamps/silos and reconcile drift. Inventory version, region, capacity, tenants, data/key mappings, health, backup, exceptions, and owner.

Roll changes through tested rings with compatibility and rollback. Dedicated tenants still receive uniform security patches and evidence.

Capacity placement considers headroom, correlated tenant peaks, failure evacuation, provider quotas, and residency. Do not fill every stamp to steady-state maximum.

Test management-plane scalability: provisioning thousands of databases/accounts, rotating credentials, collecting evidence, and restoring one tenant without affecting all.

### Migrate tenants safely

Define source/destination, exact objects/data, consistency boundary, allowed downtime, encryption, version compatibility, event/job behavior, DNS/routing, and rollback point.

For mutable data, establish single write authority through fencing or replication protocol. Two writable homes without conflict semantics corrupt state.

Copy and verify counts, checksums, constraints, permissions, keys, backups, and provider resources. Atomically advance placement revision, invalidate caches, route new work, and drain old queues.

Observe reconciliation and retain rollback only while safe. Cleanup old copies, credentials, routes, events, and backups under deletion/retention policy.

### Model tenant lifecycle explicitly

Request/onboarding verifies owner, identity domain, classification, region, tier, billing, quotas, contacts, and contractual constraints. Provisioning creates placement and controls before activation.

Suspension may block writes/new resources while allowing authorized export, billing, investigation, or recovery. Define effect on tokens, jobs, events, secrets, and provider resources.

Deletion inventories resources, data, replicas, caches, search, events, quarantine, exports, keys, provider systems, backups, legal holds, and audit. Use durable workflows and evidence.

Tombstone tenant ID and aliases after deletion. Never assign them to a new tenant while any retained or external reference could reappear.

### Test the isolation promise

Generate two or more tenants with deliberately colliding local resource IDs/names. For every API/query/mutation/list/search/cache/event/job/export/support path, attempt cross-tenant access and absent/forged context.

Test privileged database roles, connection reuse, cache races, search facets, object traversal, broker wildcard subscriptions, replay/dead letter, logs, backups, and restore into wrong placement.

Load one tenant across each exhaustible resource while measuring others. Exercise stamp loss, placement staleness, migration cutover/rollback, key disablement, suspension, deletion, and identifier reuse attempt.

External penetration/compliance evidence may be required, but internal automated negative tests run continuously. A diagram is not isolation evidence.

## Definitions and Notation

Let tenants be $T$, platform layers $L$, deployment stamps $S$, and isolation modes

$$
M=\{pooled,cell,dedicated\_layer,dedicated\_stack\}.
$$

Tenant requirement vector is

$$
R_t=(a,c,d,n,k,q,r,o),
$$

and placement function $I:T\times L\rightarrow M\times S$ selects mode and stamp for every layer.

For request $x$, trusted resolver returns

$$
C(x)=(t,p,v),
$$

where $t$ is immutable tenant ID, $p$ is authenticated actor/workload/delegation, and $v$ is placement revision. Authorization of resource $r$ requires authoritative ownership $owner(r)=t$ plus policy decision; equality to a client-supplied tenant field is insufficient.

Let $U_{t,j}$ be tenant $t$ consumption of shared resource $j$, reservation $g_{t,j}$, limit $b_{t,j}$, and capacity $K_j$. A feasible allocation maintains

$$
0\le g_{t,j}\le U_{t,j}\le b_{t,j},\qquad \sum_t g_{t,j}\le K_j,
$$

while admission reserves headroom for failure and burst. These inequalities express allocation bounds, not guaranteed application performance.

During migration from placement $s_0$ to $s_1$, single-authority invariant requires at most one writable authority for each object/revision unless an explicit conflict-resolution protocol exists.

## Mechanisms, Invariants, or Proof Structure

### Tenant-model design mechanism

1. Define tenant boundary, hierarchy, owners, threat model, and lifecycle.
2. Assign immutable tenant ID and trusted identity/membership mappings.
3. Capture security, performance, residency, recovery, customization, scale, and cost requirements.
4. Build per-layer isolation matrix and select pooled, cell, dedicated layer, or stack.
5. Create authoritative placement record and route through versioned resolution.
6. Enforce tenant context across API, authorization, data, cache, search, event, job, telemetry, and support.
7. Allocate every shared resource with admission, quota, fairness, and capacity headroom.
8. Automate fleet configuration, patching, backup, evidence, and drift reconciliation.
9. Test negative access, confused deputy, noisy neighbor, restore, migration, and lifecycle boundaries.
10. Migrate through single-write fencing, verification, atomic placement cutover, drain, and cleanup.
11. Suspend and delete through explicit state machines and retained-obligation inventory.
12. Reassess the model as tenant trust, classification, scale, regulation, and economics change.

### Tenant-context invariant

Every operation resolves a trusted tenant ID before access and carries it through each derived artifact. Missing, ambiguous, mismatched, stale-sensitive, or suspended context fails according to explicit closed policy.

### Cross-tenant noninterference invariant

An authorized action by tenant $t_1$ cannot read, mutate, infer, or materially starve protected resources of $t_2$ beyond documented shared-service limits. This requires security and performance controls, not identifier filtering alone.

### Placement invariant

Routing, data authority, keys, background work, and recovery agree on one current placement revision. Migration cannot make both old and new destinations unconstrained writers.

### Lifecycle invariant

Activation follows control provisioning; suspension is reversible policy state; deletion proves disposal or retained obligation; identifiers remain tombstoned through the maximum reappearance horizon.

### Proof sketch: namespace separation is insufficient for end-to-end isolation

Suppose tenants $t_1,t_2$ use different Kubernetes namespaces. They still share a cluster-scoped admission webhook, node kernel, external database credential, cache whose key omits tenant, and support role with wildcard reads.

The namespace can scope names and selected RBAC/network/quota policies, but none of those facts prevents the shared cache collision or database credential from returning $t_2$ data to $t_1$. Therefore distinct namespaces do not imply end-to-end isolation. Each layer needs controls matched to its threat surface. This proof sketch does not claim namespaces lack value; it bounds what their existence proves.

### Executable placement audit

This synthetic audit checks eight tenant placements for required region, dedicated-data/key controls, capacity, and lifecycle. It demonstrates deterministic record classification only; it does not prove runtime isolation or compliance.

<!-- bijux-verify: {"id":"tenant-placement-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"eligible=4\nwrong_region=1\nweak_isolation=1\nover_capacity=1\ninactive=1\n"}} -->
```python
placements = [
    ("active", "eu", "eu", True, True, 60, 100),
    ("active", "us", "us", False, False, 40, 100),
    ("active", "eu", "eu", True, True, 70, 100),
    ("active", "us", "us", True, True, 30, 100),
    ("active", "eu", "us", True, True, 20, 100),
    ("active", "eu", "eu", True, False, 20, 100),
    ("active", "us", "us", True, True, 110, 100),
    ("suspended", "eu", "eu", True, True, 10, 100),
]

counts = {name: 0 for name in ("eligible", "wrong_region", "weak_isolation", "over_capacity", "inactive")}
for state, required, actual, dedicated_data, dedicated_key, used, limit in placements:
    if state != "active":
        counts["inactive"] += 1
    elif required != actual:
        counts["wrong_region"] += 1
    elif dedicated_data and not dedicated_key:
        counts["weak_isolation"] += 1
    elif used > limit:
        counts["over_capacity"] += 1
    else:
        counts["eligible"] += 1

for name, count in counts.items():
    print(f"{name}={count}")
```

### Verification strategy

Validate identity mapping, placement, membership, entitlement, authorization, resource ownership, and lifecycle state under normal and forged requests. Use colliding IDs across tenants.

Exercise pooled data, caches, search, objects, queues, logs, traces, metrics drill-down, support tools, exports, backups, restores, and provider consoles. Include privileged and break-glass roles.

Load CPU, memory, storage, connections, locks, network, broker, APIs, jobs, and operator queues for one tenant. Measure impact on others and enforce budgets.

Exercise stamp loss/evacuation, stale placement, fleet skew, key loss/rotation, suspension, migration fence/cutover/rollback, deletion/legal hold, and attempted ID reuse.

## Alternatives and Trade-Offs

- **Pooled versus siloed.** Pooling improves utilization and uniform operations; siloing improves selected isolation while increasing cost and fleet burden.
- **Single deployment versus stamps.** One deployment is simpler; stamps cap blast radius and scale but require placement/routing/fleet automation.
- **Namespace versus cluster per tenant.** Namespaces are efficient logical scopes; clusters isolate more control/data-plane surfaces at greater cost.
- **Shared database versus database per tenant.** Shared data is economical and easy to aggregate; dedicated databases simplify some separation but multiply migrations/connections/backups.
- **Row filter versus row-level security.** Application filters are portable and explicit; database policy adds defense but requires safe session/role discipline.
- **Shared key versus tenant key.** Shared keys simplify operation; tenant/customer keys strengthen separation/revocation but complicate rotation and recovery.
- **Shared topic versus tenant topic.** Shared topics limit topology; tenant topics improve ACL/retention separation but cause scale and wildcard-management issues.
- **Tenant ID in token versus server lookup.** Signed claims reduce lookup latency; authoritative lookup handles rapid changes. Short-lived claims plus sensitive-operation refresh can combine them.
- **Global workers versus tenant workers.** Global pools use capacity efficiently; tenant pools improve fairness/isolation at fleet cost.
- **Uniform tier versus premium isolation.** Uniformity simplifies proof; tiering matches economics and requirements but creates placement/migration complexity.
- **Physical separation versus logical policy.** Physical boundaries reduce some shared attack surfaces; policy remains necessary for identity, operators, and external services.
- **Per-tenant customization versus product classes.** Customization can meet unique needs; governed classes avoid forks and drift.
- **Aggregate metrics versus tenant drill-down.** Aggregation protects cardinality/privacy; drill-down enables diagnosis under protected access.
- **Immediate deletion versus retention/hold.** Fast disposal minimizes exposure; legal, audit, billing, and recovery duties may require bounded retention.
- **Live migration versus maintenance window.** Live movement reduces downtime but adds dual-system complexity; a fenced window simplifies authority.
- **Build versus managed multitenant services.** Managed services reduce infrastructure work; the platform still owns identity mapping, configuration, evidence, and application isolation.

## Failure Modes and Misconceptions

- “A tenant is a namespace” confuses domain identity with one implementation scope.
- “Internal teams trust each other” ignores mistakes, compromised workloads, and fairness.
- “Hard multi-tenancy has one standard meaning” hides the actual threat model.
- “Dedicated means secure” ignores shared identity, operators, credentials, and drift.
- “Encryption at rest isolates tenants” does not prevent authorized application misuse.
- “Tenant ID in the request is context” trusts attacker-controlled selection.
- “Opaque resource IDs prevent leakage” substitutes obscurity for authorization.
- “Every query remembers the predicate” lacks defense and negative proof.
- “Schema per tenant eliminates fleet concerns” multiplies migrations and restore work.
- “Cache is harmless” ignores keys, authorization, eviction, and stale placement.
- “Search filtering at result rendering is enough” leaks counts, facets, and suggestions.
- “One queue is fair” ignores hot tenants and head-of-line blocking.
- “CPU quotas stop noisy neighbors” ignores every other exhaustible resource.
- “Autoscaling fixes fairness” can scale abuse and cost.
- “Tenant ID belongs in every metric label” creates leakage and cardinality failure.
- “Global support access is operationally necessary” avoids scoped workflows.
- “Customer-managed key means customer controls all copies” ignores derived data/backups.
- “A stamp is a region” confuses failure/scale unit with geography.
- “Placement can be derived from a name” breaks rename and migration.
- “Two writable homes ease migration” creates conflict without protocol.
- “Suspension is deletion” destroys recovery or leaves effects unexpectedly active.
- “Deleting a database deletes the tenant” misses caches, events, backups, and providers.
- “Tenant IDs can be recycled” risks collision with retained artifacts.
- “Silos can be customized manually” creates unpatchable snowflakes.
- “Isolation tests are only penetration tests” misses performance, restore, and lifecycle.
- “A compliant provider makes the application compliant” ignores the platform's own controls.

## Worked Examples

### Example 1

An internal platform defines tenant as a production ownership/budget boundary, not team. One team has three tenants for regulated production, general production, and experimentation. Membership may overlap, but data class, quotas, and support differ.

Namespaces map to workloads beneath those tenants. The tenant ID remains stable when team name and namespace layout change.

### Example 2

An API accepts `/tenants/tn-b/resources/r9` while the user's token selects `tn-a`. It does not switch context from the path. It resolves `r9`, validates ownership under `tn-a`, and returns not-authorized/not-found according to disclosure policy.

A privileged cross-tenant support endpoint is separate, purpose-bound, time-limited, and audited.

### Example 3

A pooled database uses composite `(tenant_id, local_id)` keys, tenant-required repository interfaces, database row policies, restricted roles, and connection-context reset tests. Two tenants both create `project-1` without collision.

A deliberately missing predicate test must fail closed at the database layer rather than return both rows.

### Example 4

A tenant has dedicated database but pooled cache. Cache key uses only resource ID and returns another tenant's record. This disproves the “dedicated data tier” end-to-end claim.

The fix uses tenant-scoped key and authorization-aware versioning, purges contaminated entries, audits access, and adds colliding-ID tests.

### Example 5

Most tenants share EU stamp `eu-4`; a regulated tenant receives dedicated database/key and node pool in the same stamp. Its model is bridge, not wholly siloed.

The contract names remaining shared control plane, cluster, networking components, operators, and backup system rather than advertising absolute isolation.

### Example 6

Tenant `tn-hot` exhausts database connections while staying under CPU quota. Per-tenant connection pools/limits and weighted queueing protect other tenants. Admission reserves capacity for control operations and incident recovery.

Metrics aggregate by stamp/tier, while protected logs allow exact tenant diagnosis without public high-cardinality labels.

### Example 7

A background export worker processes multiple tenants. A process-global tenant variable survives one task and writes the next export to the prior tenant path.

The worker uses immutable per-message context, validates tenant placement/authorization, derives destination server-side, clears connection/session state, and tests alternating colliding job IDs.

### Example 8

A tenant migrates from pooled to dedicated database. The workflow establishes a log boundary, copies and verifies, catches up, fences source writes, atomically changes placement revision, drains old jobs, and monitors.

Rollback is permitted before destination-only writes cross the boundary. Old credentials/data are removed after acceptance and retention policy.

### Example 9

Support needs to inspect two tenants during a shared incident. Rather than global console access, an approved incident workflow issues a short-lived scope for named tenants and read actions, logs queries/exports, redacts secrets, and expires automatically.

Emergency expansion is explicit and reviewed; ordinary application endpoints remain tenant-confined.

### Example 10

Tenant deletion suspends new work, exports requested data, inventories provider resources, drains jobs, removes active data/caches/indexes/events, handles backups/holds, revokes keys/credentials at the correct time, and archives audit.

The ID and external aliases are tombstoned. A new customer with the same display name receives a new ID and cannot inherit stale objects or events.

## Cross-Program Connections

- **Security Engineering:** threat models, authorization, least privilege, confused deputies, encryption, administrator access, and negative testing define security isolation.
- **Cloud Engineering:** accounts, subscriptions, projects, regions, stamps, quotas, managed services, and shared responsibility realize placement choices.
- **Kubernetes Engineering:** namespaces, RBAC, admission, network policy, nodes, clusters, and cluster-scoped resources provide non-equivalent isolation layers.
- **Database Engineering:** keys, row policy, schemas, sharding, connection pools, migrations, backups, and restore protect tenant data.
- **Distributed Systems:** routing, partitioning, caches, queues, consistency, fencing, failure domains, and split-brain govern migration and availability.
- **API and Service Engineering:** audience-bound tenant context, resource authorization, rate limits, errors, idempotency, and versioning protect service boundaries.
- **Data Engineering:** tenant partitions, CDC, analytics, exports, lineage, deletion propagation, and data products govern derived copies.
- **Reliability Engineering:** fairness, capacity headroom, noisy neighbors, cell blast radius, SLOs, fleet rollout, and disaster recovery protect service quality.
- **Observability Engineering:** cardinality, sensitive context, cohort metrics, secure drill-down, trace propagation, and audit make isolation diagnosable.
- **Governance and Compliance:** residency, retention, legal hold, evidence, customer keys, support purpose, and deletion make tenant promises auditable.

## References

1. Kubernetes. [Multi-tenancy](https://kubernetes.io/docs/concepts/security/multi-tenancy/). Retrieved 2026-09-02.
2. Kubernetes. [Namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/). Retrieved 2026-09-02.
3. Kubernetes. [RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/). Retrieved 2026-09-02.
4. Kubernetes. [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/). Retrieved 2026-09-02.
5. AWS. [SaaS Tenant Isolation Strategies](https://docs.aws.amazon.com/whitepapers/latest/saas-tenant-isolation-strategies/saas-tenant-isolation-strategies.html). August 2020. Retrieved 2026-09-02.
6. AWS. [SaaS Architecture Fundamentals: Tenant Isolation](https://docs.aws.amazon.com/whitepapers/latest/saas-architecture-fundamentals/tenant-isolation.html). Retrieved 2026-09-02.
7. Microsoft Azure Architecture Center. [Tenancy Models for a Multitenant Solution](https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/considerations/tenancy-models). Retrieved 2026-09-02.
8. Microsoft Azure Architecture Center. [Architectural Approaches for Multitenant Solutions](https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/approaches/overview). Retrieved 2026-09-02.
9. Microsoft Azure Architecture Center. [Deployment Stamps Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/deployment-stamp). Retrieved 2026-09-02.
10. Microsoft Azure Architecture Center. [Storage and Data in Multitenant Solutions](https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/approaches/storage-data). Retrieved 2026-09-02.
11. Microsoft Azure Architecture Center. [Resource Organization in Multitenant Solutions](https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/approaches/resource-organization). Retrieved 2026-09-02.
12. NIST. [SP 800-144: Guidelines on Security and Privacy in Public Cloud Computing](https://csrc.nist.gov/pubs/sp/800/144/final). December 2011. Retrieved 2026-09-02.
13. IETF. [RFC 8707: Resource Indicators for OAuth 2.0](https://datatracker.ietf.org/doc/html/rfc8707). February 2020. Retrieved 2026-09-02.
14. OWASP. [Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html). Retrieved 2026-09-02.

## Exercises

### Exercise 1

Define tenant for an internal platform serving teams, regulated workloads, sandboxes, and external partners. Model identity, hierarchy, membership, entitlement, and lifecycle without equating tenants to namespaces.

### Exercise 2

Build an isolation matrix for pooled portal/control plane, Kubernetes compute, database, cache, search, broker, keys, telemetry, backups, and support. State controls, residual risks, and tests.

### Exercise 3

Design trusted tenant context from browser through API, workflow, event, worker, provider, and audit. Include multi-membership selection, audience, placement revision, and confused-deputy defense.

### Exercise 4

Design migration of 200 tenants from one saturated stamp into four stamps while preserving residency, ordered work, database authority, keys, caches, events, rollback, and live capacity.

### Exercise 5

Design suspension and deletion for a tenant with active resources, shared and dedicated data, customer key, exports, quarantined events, legal hold, backups, provider SaaS accounts, and reused display name.

## Answers to the Exercises

### Answer 1

Define tenant as governed production/security/budget boundary. Internal team may own several tenants; a sandbox can be a lower-assurance tenant; regulated workloads use a distinct tenant/cohort; external partner receives its own mutually untrusted boundary. Namespace is a placement/resource beneath a tenant.

Use immutable opaque tenant ID, mutable display/slug/aliases, parent organization relation where needed, projects/environments beneath tenant, and explicit non-inheriting/hierarchical policies. Membership relates federated user/workload/group to tenant with role/source/validity. Entitlement defines capabilities, tier, region, quota, and features.

Lifecycle states requested, provisioning, active, suspended, migrating, deleting, retained-hold, deleted/tombstoned. Every transition has authority and evidence; IDs/aliases are not reused while artifacts can reappear.

### Answer 2

For each layer record pooled/cell/dedicated choice. Portal is shared but backend reauthorizes and search filters before facets. Control plane uses tenant-aware APIs and placement. Compute uses namespaces plus RBAC/network/admission/quota, with dedicated nodes/clusters for hostile tiers. Database uses composite keys, required repository context, row policy/restricted roles; regulated tenant may get dedicated DB.

Cache keys include tenant/auth revision; search preserves tenant and deletion; broker binds producer identity to tenant and protects subscribe/replay/quarantine; keys use per-tenant envelope/customer key where required. Telemetry aggregates cohort and protects drill-down. Backups retain mapping/key and support tenant-level restore. Support uses scoped, time/purpose-bound workflows.

Residual risks include shared cluster/control plane, kernel, database server, operators, identity provider, broker, backup service, and application defects. Test forged/missing context, colliding IDs, privileged bypass, cache/search side channels, wildcard subscriptions, noisy neighbors, restore mismatch, key disablement, and support abuse.

### Answer 3

Browser authenticates to portal. User selects among authorized memberships; backend validates selection and exchanges/obtains a token for domain API audience carrying internal tenant ID or resolves it server-side. Domain verifies issuer/audience/subject/delegation/membership, current resource ownership, placement revision where sensitive, and policy.

Workflow persists actor, tenant, request, policy, and placement, then executes as scoped workload. Events carry tenant with authenticated producer source; broker/subscription and consumer validate it. Worker creates fresh immutable per-item context and clears pooled connection state. Provider resources receive immutable tenant metadata but provider identifiers do not replace internal tenant ID.

Audit records actor, workload/delegation, tenant, action/resource, decision/policy, operation, placement, and provider receipt. Resource lookup verifies owner rather than accepting paired IDs. Gateways strip spoofable headers, tokens are audience-bound/short-lived, and absent or conflicting context fails closed.

### Answer 4

Select tenants by residency/cohort and destination capacity with failure headroom. Version placement records and pre-provision four stamps, schemas, keys, policies, quotas, monitoring, backups, and compatible application versions. Protect live and recovery capacity from copy/replay.

For each cohort establish source log/event boundary, copy encrypted data, verify counts/checksums/constraints/ownership/key access, replicate catch-up, and route shadow reads. Pause/fence tenant writes and new jobs, drain or transfer ordered queues with stable identities, atomically advance placement revision, invalidate caches/search routes, then enable destination writes.

Observe API/business reconciliation, events, providers, lag, and SLO. Roll back only before incompatible destination-only effects or reverse through equivalent fenced protocol. Remove old data/credentials/routes/backups after acceptance and retention. Rate-limit cohorts, preserve unaffected tenants, and exercise evacuation of one new stamp.

### Answer 5

Suspension blocks new login/tokens, mutations, provisioning, and scheduled effects according to contract while preserving authorized export, billing, incident access, and recovery. Pause or classify queued jobs/events; revoke active grants without destroying evidence. Record reason, actor, policy, time, and reversibility.

Deletion inventory joins primary/shared/dedicated data, compute/network resources, caches/search, live jobs, events/quarantine, exports, keys/secrets, replicas, backups, SaaS/provider accounts, audit, and holds. Export authorized data, deprovision effects idempotently, delete active copies, and verify provider absence. Legal-held records remain access-restricted with owner/expiry; audit remains per policy.

Do not destroy the customer key until all required encrypted data is disposed or retention/escrow permits it. Remove quarantines and derived copies, propagate tombstones, revoke identities/credentials/routes, and test restored backups cannot reactivate work. Mark tenant ID and aliases tombstoned. A later organization with the same display name receives a new immutable ID.
