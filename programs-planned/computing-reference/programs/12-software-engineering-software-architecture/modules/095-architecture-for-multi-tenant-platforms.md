---
module_id: SARCH-095
program: Software Engineering: Software Architecture
level: 2
module_number: 95
title: Architecture for Multi-Tenant Platforms
status: complete
last_verified: 2026-09-06
---

# Architecture for Multi-Tenant Platforms

## One-Page Review

### Governing question

How should architects let multiple mutually independent customers or organizations share a product platform while preserving tenant identity, authorization, data and execution isolation, fair service, configurability, lifecycle control, forensic evidence, and an honest boundary for every shared resource?

### Essential definitions

- a **tenant** is a customer or organizational security, data, configuration, billing, and service boundary, not merely a user group or database column;
- **tenant context** is server-verified identity and authorization information that scopes an operation to one tenant and actor;
- **control plane** provisions tenants, policy, placement, versions, keys, quotas, and lifecycle; the **data plane** serves tenant work;
- **isolation** is a property against a named interference or disclosure mechanism at a named layer;
- a **pooled model** shares an instance or data structure across tenants; a **siloed model** assigns dedicated instances; a **bridge model** combines shared and dedicated boundaries;
- a **noisy neighbor** consumes a shared constrained resource enough to harm other tenants;
- **resource fairness** is a declared allocation policy across competing tenants and resource dimensions;
- a **whale tenant** has workload, data, risk, customization, or criticality that invalidates ordinary cohort assumptions;
- **tenant-aware telemetry** attributes service and security evidence without unnecessarily exposing tenant data;
- **tenant lifecycle** covers prospect, provisioning, activation, suspension, migration, export, retention, deletion, and identifier retirement;
- **residual shared fate** is the failure or compromise exposure that remains across supposedly isolated tenants;
- a **support impersonation path** is a tightly governed mechanism for authorized personnel to act within or inspect tenant context, with purpose, scope, consent where required, expiry, and audit.

### Central model, mechanism, or theorem

Represent a multi-tenant platform as

$$
P=(T,C,I,R,D,E,O,L),
$$

where $T$ defines tenant identity and relationships, $C$ tenant context and authorization, $I$ isolation across application, data, runtime, network, cryptographic, operational, and forensic dimensions, $R$ resource allocation and fairness, $D$ data placement and lifecycle, $E$ extension and configuration, $O$ observability and operations, and $L$ onboarding, migration, incident, export, and offboarding. For each shared mechanism, state what is shared, the interference paths, enforcement point, evidence, and residual fate.

### Critical invariants

- client-supplied tenant identifiers select context but never authorize it;
- tenant context is established once from authenticated identity and revalidated at every privileged boundary;
- every tenant-owned object carries or inherits unambiguous tenant ownership;
- data queries, caches, files, search indexes, queues, events, logs, metrics, backups, and derived views preserve tenant scope;
- privileged maintenance and support paths cannot silently become ordinary request paths;
- isolation claims name application, data, runtime, network, key, administrator, supplier, and recovery boundaries;
- one tenant cannot exhaust another tenant's protected capacity or operator attention beyond declared policy;
- configuration and extensions cannot bypass authorization, resource, data, or upgrade boundaries;
- tenant moves preserve authority, residency, keys, histories, jobs, webhooks, and deletion semantics;
- offboarding covers active, derived, cached, replicated, exported, backup, and legally retained data;
- fleet-wide evidence cannot hide a persistently failed or harmed tenant cohort;
- every cross-tenant operation has explicit authority, aggregation, privacy, and audit semantics.

### Common failures

Common failures include trusting an `X-Tenant-ID` header; filtering only top-level queries; reusing a pooled database session with stale tenant state; omitting tenant from cache or idempotency keys; placing every tenant in one queue; using global rate limits; treating namespaces as security boundaries without enforcement; serving requests through a database superuser; letting plugins run with platform authority; offering per-tenant forks; logging secrets with tenant tags; restoring an entire shared database to recover one tenant; deleting active rows but not indexes, exports, or backups; and reporting a global SLO while one small tenant remains unavailable.

### Compact example

A document platform serves 4,000 organizations from shared application and database tiers. The authenticated principal selects organization `A`, but membership and role are verified by an authorization service and bound into immutable request context. Every document row, object key, search entry, cache key, event, job, and audit record derives scope from that context. Ordinary request roles cannot bypass database row policy; support access uses a separate time-limited path. Per-tenant admission protects CPU, connections, queues, storage, and expensive search. Large regulated tenants can move to dedicated data and key boundaries behind the same contracts. Restore, export, and deletion are tenant-granular even when physical storage is pooled.

### Connections

[SARCH-056](056-cell-based-architecture.md) owns repeatable failure-isolation units, [SARCH-068](068-threat-modeling-at-architecture-scale.md) owns architectural threat analysis, and [SARCH-093](093-architecture-for-extreme-read-or-write-scale.md) owns extreme capacity mechanisms. This module composes them around tenant semantics. [SARCH-096](../ROADMAP.md) next examines offline and intermittent operation.

## Governing Question

Multi-tenancy is a promise that sharing will not erase organizational boundaries. The promise spans more than confidentiality: one tenant should not change another's data, impersonate its actors, monopolize service, corrupt its evidence, determine its upgrade, or prevent its recovery beyond the declared product contract. Isolation is therefore a vector of properties, not a boolean architecture label.

Sharing can improve resource utilization, consistent upgrades, security response, and product learning. It also connects failure domains. Stronger physical isolation can reduce some shared mechanisms but increases fleet complexity, drift, cost, and operational exceptions. The architect must select boundaries by threat, consequence, workload, jurisdiction, recovery, and business obligations rather than by slogans such as “database per tenant” or “namespace isolation.”

## Why This Matters

Saltzer and Schroeder's protection principles include complete mediation, least privilege, separation of privilege, and economy of mechanism [1]. These remain durable foundations: tenant isolation fails when one path skips authorization or privileged machinery becomes routine. Lampson's access-control model separates subjects, objects, and rights and exposes why naming an object does not grant access [2]. Modern implementations add distributed identity, caches, asynchronous work, data derivation, infrastructure, suppliers, and support operators, but the fundamental mediation question remains.

Current official Kubernetes guidance, checked 2026-09-06, explicitly treats multi-tenancy as a spectrum and distinguishes control-plane from data-plane isolation; it warns that a namespace needs additional enforcement and that shared components retain exposure [5]. OWASP's current multi-tenant security guidance likewise covers verified tenant context, database, cache, session, API, asynchronous work, files, lifecycle, and audit [6]. These sources supply implementation prompts, not certification of a particular platform.

## Prerequisites and Retrieval

Retrieve tenant, principal, subject, object, authentication, authorization, least privilege, complete mediation, confused deputy, context, policy, control plane, data plane, namespace, process, container, virtual machine, hypervisor, cell, partition, schema, row-level security, cache, queue, quota, reservation, admission, fairness, noisy neighbor, encryption key, residency, backup, restore, retention, deletion, support access, and forensic readiness.

SARCH-041 through SARCH-060 provide interface, data, deployment, observability, partial-failure, partition, control-plane, and cell boundaries. SARCH-061 through SARCH-070 provide scenario, risk, capacity, reliability, threat, cost, and evidence methods. SARCH-081 through SARCH-094 provide ownership, governance, high-change, scale, and ML product judgment. This chapter does not replace detailed identity, database, virtualization, privacy, forensics, or platform implementation disciplines.

## Learning Objectives

After completing this module, you should be able to:

1. define a tenant and its trust, data, workload, jurisdiction, and lifecycle boundaries;
2. propagate server-verified tenant context without trusting selectors;
3. evaluate pooled, siloed, and bridge deployment and data models;
4. enforce isolation across synchronous, asynchronous, derived, administrative, and recovery paths;
5. design multidimensional quotas, fairness, admission, and whale handling;
6. scope keys, secrets, configuration, extensions, observability, and support access;
7. migrate tenants without split authority or residency violations;
8. design tenant-granular backup, restore, export, deletion, and forensic evidence;
9. test negative isolation, noisy-neighbor, failure, lifecycle, and fleet scenarios; and
10. state residual shared fate honestly rather than claim absolute isolation.

## Core Exposition

**Define the tenant model.** A tenant may be a company, household, government body, project, reseller, or nested organization. State whether a person can belong to several tenants, whether tenants can delegate to subtenants, who owns resources, and how cross-tenant collaboration works. Separate stable internal tenant identity from domain name, subscription, region, database, or deployment location; those can change. Define the authority that creates, merges, splits, suspends, and retires a tenant.

**Model trust and consequence.** Ask whether tenant code runs, whether tenants distrust each other, whether administrators may inspect content, whether regulated data exists, and what a breach, slowdown, corruption, or misconfiguration would mean. “Hard” and “soft” tenancy are too vague for assurance. State isolation dimensions and adversaries: another user, tenant administrator, workload, compromised runtime, support engineer, fleet operator, supplier, or failed control plane.

**Establish context from identity.** Authenticate a human or workload, resolve current memberships and delegations, verify the selected tenant and role, then create an immutable server-side context containing tenant, actor, purpose, policy epoch, and request or operation identity. Downstream services accept signed or mutually authenticated context from trusted intermediaries, not arbitrary headers. Reauthorize high-value operations and changes in membership. Do not infer tenant from a resource ID before authorization.

**Mediate every object path.** Put tenant ownership in relational rows, document partitions, object prefixes or metadata, search documents, vectors, cache keys, sessions, files, jobs, events, idempotency records, rate-limit buckets, feature data, and audit events. Ownership can be inherited from a securely resolved parent, but ambiguity fails closed. Test read, create, update, delete, list, export, bulk, relationship load, indirect reference, error, and timing paths. Parameterized SQL prevents injection, not cross-tenant access.

**Use defense in depth for data.** Shared tables maximize pooling and easy fleet changes but depend on pervasive scoping and database policy. Separate schemas add namespaces and grants while sharing an engine and privileged operators. Separate databases create credential, backup, failure, and performance boundaries at greater fleet cost. Dedicated accounts, clusters, or hardware may address stronger risk or jurisdiction needs but still share code, build systems, support, identity, or vendors. A bridge model assigns tenants to isolation classes behind stable logical contracts.

**Constrain database privilege.** Ordinary tenant requests use a role that cannot bypass tenant policy. Bind transaction-local context before queries and clear it by ending the transaction; session pools can otherwise leak prior tenant state. Migration, analytics, support, and repair use separate identities, explicit tenant sets, purpose, approval, query limits, and audit. Row-level policy is one enforcement layer, not permission to omit application authorization and negative-path tests.

**Scope derived and cached state.** A cache key must include every authorization and semantic dimension affecting the answer, or the result must be independently safe to share. Negative cache entries and errors can also leak existence. Search indexes and vector stores retain source tenant, access policy, derivation version, and deletion lineage. Aggregate analytics needs an approved cross-tenant purpose, minimum groups where relevant, privacy controls, and protection against tenant reidentification. Rebuild must preserve scope.

**Make asynchronous work tenant-native.** Events carry verified tenant and operation identity from the authoritative commit. Consumers do not replace context with a payload field from an untrusted producer. Partition, queue, and retry policy must prevent one tenant from blocking all others. Dead-letter records retain tenant scope, access, and replay authority. Webhooks use tenant-scoped credentials, destinations, signatures, egress controls, retry budgets, and deletion. A global worker superuser is a wide blast radius requiring stronger mediation.

**Allocate multiple resources.** CPU-only limits do not protect memory, storage IOPS, connections, queue slots, egress, third-party calls, model tokens, or operator attention. For tenant $t$ and resource $r$, define dominant share

$$
s_t=\max_r\frac{a_{t,r}}{C_r},
$$

where $a_{t,r}$ is allocation and $C_r$ available capacity in the same window. Dominant Resource Fairness generalizes fair sharing across heterogeneous resources under its model [7]. Production policy may combine reservations, weights, priorities, burst credits, deadlines, and hard safety bounds. Fairness theory does not decide contractual tiers or social legitimacy.

**Control noisy neighbors end to end.** Apply admission before scarce work, per-tenant concurrency, queue and storage budgets, query cost limits, timeouts, circuit breaking, egress and provider quotas, and protected control-plane capacity. Observe usage by tenant and operation without exposing identifiers broadly. Retries consume the same tenant budget unless a deliberate policy says otherwise. Shed optional work before accepted durable operations violate promises.

**Handle whales explicitly.** A tenant with 30% of writes, a unique jurisdiction, untrusted code, or strict recovery may need a dedicated database, cell, region, key hierarchy, worker pool, or support team. Do not create a one-off fork. Keep the platform contract and automation common while parameterizing placement and isolation class. Exercise the uncommon recovery path. A large tenant can sometimes subdivide by a domain key; only do so if authority and invariants remain coherent.

**Separate configuration from code.** Per-tenant settings need schema, types, defaults, validation, compatibility, provenance, owner, change audit, rollout, and retirement. Avoid thousands of arbitrary flags whose interactions are untestable. Extension points expose least-privileged capabilities, bounded compute and I/O, versioned APIs, resource budgets, and termination. Untrusted extensions may require process, virtual-machine, sandbox, or separate service boundaries; a language sandbox label is not proof.

**Scope cryptography carefully.** Per-tenant data-encryption keys can improve revocation, blast radius, and evidence, but key-encryption keys, key services, operators, backups, and application plaintext paths may remain shared. Bind ciphertext and key requests to tenant and object context. Rotate and revoke without orphaning legal retention or recovery. Do not promise cryptographic deletion where copies, logs, exports, or plaintext derivatives remain.

**Design control-plane failure.** Provisioning establishes identity, isolation class, placement, policy, keys, quotas, version, and initial administrator through an idempotent state machine. Existing tenants may continue from authenticated cached configuration during bounded control-plane loss; new tenants, privilege grants, moves, and deletion stop if authority is unavailable. Control updates carry epochs and signatures where warranted. Compromise of provisioning can cross every tenant, so separation of privilege and progressive rollout matter.

**Keep release compatibility across tenant diversity.** Tenant data size, old configuration, enabled features, integrations, language, region, and isolation class create a combinatorial fleet. Define supported variation, migrate schemas and settings compatibly, and canary representative cohorts including whales and uncommon tiers. Do not let customer-specific forks make security updates optional. A tenant may control feature release within bounds, not platform vulnerability remediation or invariant changes.

**Move tenants as authority migrations.** Provision eligible target capacity and keys; record placement epoch; copy a bounded snapshot; capture later changes; rebuild derived state; verify counts, hashes, domain invariants, residency, jobs, webhooks, audit, and restore; fence old writes; switch directory authority; drain stale routes; reconcile; then retire old state. Do not run two silent authoritative homes. A DNS change moves traffic, not data authority.

**Design backup and restore for one tenant.** Whole-database backup can protect pooled physical state while making single-tenant recovery difficult. Preserve logical tenant export or point-in-time reconstruction with operation identity, schema version, dependencies, and encryption. Restore into an isolated verification area, select the requested tenant and time, check invariants and authorization, then merge or replace under a governed plan. Test that another tenant's data cannot enter the result.

**Make support access exceptional.** Support impersonation states customer request or incident purpose, approved scope, actor, tenant, allowed operations, expiry, recording, and notification where required. Prefer read-only or action-specific tooling over broad database access. Separate approval and execution for high-risk actions. Emergency access expires automatically and receives independent review. Never reuse a tenant's credential or make audit indistinguishable from the customer.

**Observe tenant and platform outcomes.** Measure tenant-specific correct requests, latency, queue age, quota decisions, storage, error, dependency, version, migration, support access, security events, and business capability. Use pseudonymous identifiers and restrict high-cardinality telemetry appropriately. Global percentiles can hide total failure for a small tenant. Conversely, tenant telemetry must not become an ungoverned replica of customer data.

**Plan incidents and forensics.** Be able to determine which tenants, objects, actors, versions, keys, nodes, and operations may be affected without reading every tenant indiscriminately. Preserve trustworthy time, identity, authorization, configuration, and administrative evidence. NIST SP 800-201 provides a current cloud forensic reference-architecture methodology [10]; it informs readiness but does not establish evidentiary sufficiency for a jurisdiction.

**Complete offboarding.** Suspend new authority, revoke human and workload access, stop jobs and webhooks, settle billing and contractual holds, export where authorized, then delete or restrict data by a versioned schedule across primary, replicas, caches, search, derived analytics, files, logs, backups, support systems, and suppliers. Record exceptions and expiry. Prevent immediate identifier reuse from binding old messages or object paths to a new tenant.

## Definitions and Notation

Let tenant $t\in T$, actor $u$, operation identity $o$, resource $x$, action $a$, purpose $p$, and policy epoch $e$. Authorization is a decision

$$
Authorize(u,t,a,x,p,e)\in\{allow,deny,inconclusive\}.
$$

Failure or missing context must not silently become `allow`. Let the isolation vector be $I=(I_a,I_d,I_r,I_n,I_k,I_o,I_f)$ for application, data, runtime, network, key, operational, and forensic boundaries. Each element records mechanism, threat, evidence, and residual shared fate; it is not a numeric score.

## Mechanisms, Invariants, or Proof Structure

### Context-binding invariant

Every tenant-owned operation binds authenticated actor, authorized tenant, purpose, policy epoch, and stable operation identity before resolving or mutating the target object.

### No-cross-tenant-effect invariant

For ordinary tenant authority, a tenant-scoped operation cannot read, infer beyond the accepted leakage model, mutate, delay beyond policy, or grant authority over another tenant's state.

### Privilege-separation invariant

Ordinary serving identities cannot invoke migration, bypass data policy, impersonate support, change isolation class, or perform unrestricted cross-tenant aggregation.

### Lifecycle-closure invariant

Provision, move, suspend, export, restore, delete, and identifier retirement include every authoritative and derived state class or explicitly governed exception.

### Executable placement illustration

<!-- bijux-verify: {"id":"tenant-placement","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"ordinary: shared-pool\nregulated data: isolated-data\nuntrusted code: dedicated-runtime\nwhale: dedicated-capacity\nmandated boundary: dedicated-cell\ninvalid: reject\n","stderr":""}} -->
```python
def placement(*, valid_tenant, dedicated_required, untrusted_code,
              isolated_data_required, whale):
    if not valid_tenant:
        return "reject"
    if dedicated_required:
        return "dedicated-cell"
    if untrusted_code:
        return "dedicated-runtime"
    if isolated_data_required:
        return "isolated-data"
    if whale:
        return "dedicated-capacity"
    return "shared-pool"

cases = {
    "ordinary": (True, False, False, False, False),
    "regulated data": (True, False, False, True, False),
    "untrusted code": (True, False, True, False, False),
    "whale": (True, False, False, False, True),
    "mandated boundary": (True, True, False, False, False),
    "invalid": (False, False, False, False, False),
}
for name, facts in cases.items():
    print(f"{name}: {placement(valid_tenant=facts[0], dedicated_required=facts[1], untrusted_code=facts[2], isolated_data_required=facts[3], whale=facts[4])}")
```

The finite rule demonstrates explicit precedence, not an isolation assessment. Real placement needs threat, data, residency, workload, supplier, recovery, cost, and legitimate policy evidence. “Regulated” does not universally imply one physical topology.

### Proposition: tenant filtering does not imply tenant authorization

Suppose a request chooses tenant `B`, and every SQL query correctly filters `tenant_id='B'`, but the authenticated actor belongs only to tenant `A`. Filtering prevents rows from other than `B`; it does not establish the actor's right to `B`. Therefore correct tenant filtering does not imply tenant authorization.

### Proposition: dedicated compute does not imply tenant isolation

Suppose each tenant has dedicated compute but all processes use one privileged database credential, one global cache namespace, and one support role. A credential error or cache collision crosses compute boundaries. Therefore dedicated compute alone does not imply tenant isolation.

## Alternatives and Trade-Offs

**Shared tables versus schemas versus databases.** Pooling reduces fleet cost and eases aggregate changes; stronger namespaces and credentials reduce some error and compromise paths while increasing migration, connection, backup, and fleet complexity.

**Shared runtime versus sandbox versus dedicated cell.** Sharing improves utilization. Stronger runtime boundaries address untrusted code and noisy neighbors at cost and still share control, supply chain, operators, or hardware.

**Global fairness versus contractual classes.** Equal shares are legible but may ignore tenant size, public importance, or paid reservations. Weighted and priority policies need transparent limits so one class does not starve another.

**Common product versus customization.** Configuration preserves one product when bounded and typed. Plugins add power and attack surface. Forks maximize local freedom while fragmenting security, compatibility, and operations.

**Per-tenant keys versus shared key hierarchy.** Tenant keys narrow some compromise and deletion paths but increase lifecycle and availability dependencies. Both require authorization and plaintext-path controls.

**Central analytics versus federated summaries.** Centralization simplifies global insight but enlarges privacy and breach scope. Federated or minimized aggregates reduce collection while complicating quality, correction, and reproducibility.

## Failure Modes and Misconceptions

1. **“A tenant ID in every row is isolation.”** Enforcement and every non-row path still matter.
2. **“The header says the tenant.”** A selector is not membership or authority.
3. **“Parameterized queries prevent tenant leakage.”** They prevent an injection class, not missing authorization predicates.
4. **“Namespaces are security boundaries.”** Their guarantees depend on the platform and configured enforcement.
5. **“Database per tenant is complete isolation.”** Code, operators, control planes, build, network, and suppliers remain shared.
6. **“Encryption prevents administrators from reading data.”** Applications and key-authorized paths may expose plaintext.
7. **“Per-tenant keys guarantee deletion.”** Copies, logs, exports, backups, and derivatives may remain.
8. **“One global rate limit is fair.”** One tenant can consume it and deny others.
9. **“CPU quotas stop noisy neighbors.”** Memory, I/O, connections, queues, egress, and attention can bind.
10. **“Retries should bypass quota.”** They can amplify the same scarce resource.
11. **“A whale is only a bigger subscription.”** It may invalidate placement, failure, migration, and support assumptions.
12. **“Plugins are configuration.”** Executable extensions create code, privilege, resource, and compatibility risks.
13. **“Support needs production superuser access.”** Purpose-built, scoped, expiring paths reduce blast radius.
14. **“Cross-tenant analytics is anonymous.”** Sparse groups and linkable attributes can reidentify tenants or people.
15. **“A global SLO proves tenant availability.”** Small cohorts can fail completely beneath aggregate success.
16. **“A backup guarantees one-tenant restore.”** Extraction, dependencies, authorization, and merge semantics need testing.
17. **“Deleting the main row completes offboarding.”** Derived, cached, replicated, exported, and supplier data remain.
18. **“Dedicated tiers can use different code.”** Forks accumulate security and operational drift.
19. **“The control plane is not on the request path, so it is low risk.”** Its compromise can change every tenant's authority.
20. **“Absolute isolation is achievable by label.”** Every mechanism has scope, assumptions, and residual shared fate.

## Worked Examples

### Example 1

**Situation.** An API authenticates Alice, then trusts `X-Tenant-ID: B` and filters every query for tenant B.

**Reasoning.** SQL scoping is internally consistent, but Alice belongs only to A. Resolve Alice's current membership and permitted role for B before creating context. Bind verified tenant and policy epoch into an internal credential or trusted request object; downstream code cannot replace it with the original header. Log the denied selector without leaking whether sensitive B objects exist. Test altered header, object ID, nested loads, bulk actions, and stale membership.

**Conclusion.** Tenant selection and tenant authorization are distinct gates.

### Example 2

**Situation.** A connection pool uses `SET tenant='A'`; the next request for B inherits the session.

**Reasoning.** Session state outlives a transaction and can leak A's context. Begin a transaction, set a transaction-local tenant value from verified context, execute through a non-bypass role, then commit or roll back before returning the connection. Missing context fails closed. Independently scope application authorization and test pooled reuse, errors, cancellation, nested transactions, migration roles, and replicas.

**Conclusion.** Tenant context lifetime must be no broader than the authorized unit of work.

### Example 3

**Situation.** A product must host 3,000 ordinary tenants and twelve healthcare tenants with distinct residency and restore requirements.

**Reasoning.** Use a bridge model: ordinary tenants share row-policy-enforced databases partitioned into cells; healthcare tenants receive eligible dedicated databases and tenant key hierarchies. Both use the same logical APIs, schema migration stream, control-plane state machine, telemetry contract, and security release. Placement policy records the actual required boundary rather than assuming healthcare always means physical hardware. Exercise each tier's backup, move, failover, support, and deletion.

**Conclusion.** Isolation classes can vary physical boundaries without forking product semantics.

### Example 4

**Situation.** The cache key is `document:42`, though document 42 exists independently in tenants A and B.

**Reasoning.** A warms the cache, then B receives A's document. Use a key derived from verified tenant, object, authorization-relevant variant, representation version, and locale where these affect content. Do not trust tenant from the URL. Negative results and errors also need scope. Invalidate from an identified tenant-owned source event. Test same object IDs, membership revocation, public/private transitions, cache stampede, failover, and stale replicas.

**Conclusion.** Cache identity is part of the tenant security model.

### Example 5

**Situation.** Tenant A submits 90% of jobs to one FIFO queue; tenant B's urgent jobs wait two hours.

**Reasoning.** A shared queue couples backlog and worker slots. Partition logical admission by tenant and class, reserve minimum capacity, apply weighted fair scheduling within deadline and safety constraints, and cap retries and expensive jobs. Track queue age and goodput per tenant. Spare capacity may be borrowed but must be reclaimable without killing committed work. Dead-letter and replay preserve tenant authority. A global emergency class needs abuse-resistant authorization.

**Conclusion.** Queue durability does not provide service fairness; allocation policy and admission do.

### Example 6

**Situation.** One tenant uses 35% of write IOPS, 55% of support effort, and a unique region.

**Reasoning.** Tenant count-based placement is invalid. Model IOPS, CPU, storage, connections, egress, incident and support load, recovery, and region eligibility. Give the tenant dedicated capacity and perhaps data placement while retaining standard APIs and automation. If its domain permits subdivision, split by stable subordinate authority rather than arbitrary file. Price is a business input, not evidence that healthy tenants may be starved. Rehearse the uncommon failover.

**Conclusion.** Whale handling is an architectural isolation class, not a manual exception.

### Example 7

**Situation.** Customers upload scripts that transform invoices, and scripts execute in the application process.

**Reasoning.** A loop, memory allocation, network call, or escape can affect every tenant. Replace ambient application authority with a versioned extension API, validated inputs/outputs, tenant-scoped capability tokens, bounded CPU/memory/time/output, isolated filesystem and network, and per-tenant concurrency. Select a runtime boundary from the adversary and consequence model. Scan and record extension versions, provide deterministic test fixtures, and define behavior when an extension fails during upgrade or billing.

**Conclusion.** Executable customization requires an explicit runtime, capability, and resource boundary.

### Example 8

**Situation.** Tenant C asks to restore its project to yesterday, but all tenants share one database backup.

**Reasoning.** Restoring the database in place would rewind everyone. Restore the physical backup into an isolated environment with narrowly authorized operators. Reconstruct C's rows and dependencies at the requested timestamp, including ownership, events, files, search sources, and keys; verify no other tenant enters the export. Compare against current C state, identify later operations and external effects, then merge, replace, or create a recovered copy under an approved plan. Rebuild derived views and audit the action.

**Conclusion.** Backup protects bytes; tenant recovery requires logical selection and reconciliation semantics.

### Example 9

**Situation.** A tenant cancels and policy requires active deletion in 30 days while financial records remain restricted for seven years.

**Reasoning.** Freeze new writes, revoke actors and workloads, stop jobs, integrations, and webhooks, and provide authorized export. Classify primary content, derived search, caches, analytics, logs, support copies, object versions, replicas, backups, supplier copies, and financial records. Delete each eligible class on its schedule; isolate retained financial records from ordinary product access with legal basis, owner, expiry, and audit. Propagate tombstones through replay and prevent tenant-ID reuse.

**Conclusion.** Offboarding is a data-and-authority workflow with explicit retained exceptions, not one delete statement.

### Example 10

**Situation.** A national education platform hosts schools that share curriculum but must isolate student records, accessibility plans, staff roles, regional policy, exams, and incident evidence.

**Reasoning.** Model ministry, region, school, class, guardian, learner, and service-provider relationships without treating every hierarchy edge as authority. Verify tenant and role at each action; use scoped collaboration for transfers. Separate public curriculum from protected learner records. Choose data and key classes by jurisdiction and sensitivity; protect exam authoring, release, and grading with separation of privilege. Bound uploads, video, analytics, and AI features per school. Provide accessible degraded service and fair capacity during exams.

Record cross-school aggregate purpose and privacy; small cohorts cannot be exposed through dashboards. Support access is time-limited and visible. Test compromised school admin, wrong transfer, cache collision, queue saturation, region loss, exam surge, backup restore, legal hold, and school closure. Preserve student continuity during tenant merge or split. Education, child-safety, privacy, accessibility, security, labor, regional, and community authorities decide real policy.

**Conclusion.** Complex tenancy requires explicit relationships, data classes, authority, fairness, lifecycle, and legitimate public governance.

## Cross-Program Connections

- [Database Engineering](../../18-database-engineering/ROADMAP.md) owns row security, schemas, transactions, indexes, backup, restore, and engine privilege.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) owns tenant data authority, lineage, aggregation, residency, retention, and deletion.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns identity, authorization, isolation testing, cryptography, sandboxing, incident, and forensic security depth.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) owns partition, replication, ordering, fencing, and distributed protocol mechanics.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns reusable tenant provisioning, policy, runtime, data, observability, and lifecycle capabilities as internal products.
- [Cloud & Infrastructure Engineering](../../30-cloud-and-infrastructure-engineering/ROADMAP.md) owns cloud account, network, compute, managed-service, and provider implementation choices.

## References

1. Jerome H. Saltzer and Michael D. Schroeder, [“The Protection of Information in Computer Systems”](https://doi.org/10.1109/PROC.1975.9939), *Proceedings of the IEEE* 63(9), 1975, pp. 1278–1308.
2. Butler W. Lampson, [“Protection”](https://doi.org/10.1145/362759.362773), *Proceedings of the Fifth Princeton Symposium on Information Sciences and Systems*, 1971; reprinted in *ACM Operating Systems Review* 8(1), 1974.
3. Ramaswamy Chandramouli and Zack Butcher, [*A Zero Trust Architecture Model for Access Control in Cloud-Native Applications in Multi-Cloud Environments*](https://doi.org/10.6028/NIST.SP.800-207A), NIST SP 800-207A, September 2023; final status checked 2026-09-06.
4. Ramaswamy Chandramouli, [*Security Recommendations for Server-based Hypervisor Platforms*](https://doi.org/10.6028/NIST.SP.800-125Ar1), NIST SP 800-125A Rev. 1, 2018.
5. Kubernetes, [“Multi-tenancy”](https://kubernetes.io/docs/concepts/security/multi-tenancy/), current official documentation checked 2026-09-06.
6. OWASP Foundation, [“Multi-Tenant Security Cheat Sheet”](https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html), current maintained guidance checked 2026-09-06.
7. Ali Ghodsi et al., [“Dominant Resource Fairness: Fair Allocation of Multiple Resource Types”](https://www.usenix.org/conference/nsdi11/dominant-resource-fairness-fair-allocation-multiple-resource-types), NSDI 2011.
8. Martin Kleppmann and Chris Riccomini, [*Designing Data-Intensive Applications*](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/), 2nd ed., O'Reilly, February 2026.
9. Jim Gray and Andreas Reuter, *Transaction Processing: Concepts and Techniques*, Morgan Kaufmann, 1992. Authority, concurrency, recovery, and transaction processing.
10. Martin Herman et al., [*NIST Cloud Computing Forensic Reference Architecture*](https://doi.org/10.6028/NIST.SP.800-201), NIST SP 800-201, July 2024; final status checked 2026-09-06.
11. Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software*, Addison-Wesley, 2003. Identity, boundaries, and domain models.
12. ISO/IEC, [ISO/IEC 27018:2025, *Guidelines for Protection of Personally Identifiable Information in Public Clouds Acting as PII Processors*](https://www.iso.org/standard/27018), 3rd ed., August 2025; official published status checked 2026-09-06.

## Exercises

### Exercise 1

Define tenant, tenant context, control plane, data plane, isolation, pooled, siloed, bridge, noisy neighbor, resource fairness, whale tenant, residual shared fate, and support impersonation. Explain why multi-tenancy is not a boolean database property.

### Exercise 2

A platform has 100 CPU units and 200 GiB memory. Tenant A receives 40 CPU and 20 GiB; B receives 15 CPU and 90 GiB; C receives 25 CPU and 40 GiB. Compute each tenant's dominant share. State at least six reasons equal dominant shares would not by themselves define a correct production allocation.

### Exercise 3

Trace and repair this design: the browser supplies a tenant header; an API filters primary rows; relationship loads use a global ORM path; cache and idempotency keys omit tenant; events carry a mutable tenant field; workers use a database superuser; and support copies query results into tickets.

### Exercise 4

Compare shared tables, separate schemas, separate databases, dedicated cells, and a bridge model for 5,000 ordinary tenants, 20 whales, and 10 jurisdictionally restricted tenants. Cover security, fairness, cost, migrations, release, backup/restore, analytics, support, and deletion.

### Exercise 5

A disaster-relief coordination platform serves governments, international organizations, local nonprofits, clinics, suppliers, and affected households during intermittent connectivity and extreme surges. Design tenant and collaboration boundaries, fair service, data protection, support, incident evidence, organizational handover, and offboarding without assuming every participant trusts every other participant.

## Answers to the Exercises

### Answer 1

A tenant is a customer or organizational security, data, configuration, billing, service, and lifecycle boundary. Tenant context is server-verified identity and authorization scoping an operation. The control plane provisions identity, policy, placement, versions, keys, and lifecycle; the data plane serves work. Isolation is protection against a named mechanism at a named layer. Pooled models share instances; siloed models dedicate them; bridge models combine classes. A noisy neighbor harms others through shared consumption. Resource fairness is the declared allocation rule. A whale invalidates ordinary workload or risk assumptions. Residual shared fate is exposure remaining through shared mechanisms. Support impersonation is governed, scoped, expiring action in tenant context. Different data, runtime, network, resource, operator, backup, and supplier mechanisms have different guarantees, so one database choice cannot make tenancy globally true or false.

### Answer 2

A's CPU share is $40/100=0.40$ and memory share $20/200=0.10$, so $s_A=0.40$. B's shares are $0.15$ and $0.45$, so $s_B=0.45$. C's shares are $0.25$ and $0.20$, so $s_C=0.25$. Equalizing these may omit actual demand; reservations and contracts; operation priority and deadlines; workload efficiency; storage, IOPS, network, connection, and third-party limits; failure and maintenance reserve; tenant criticality; abuse; regional eligibility; historical burst credits; and public or safety obligations. DRF's properties apply under its model. Production fairness requires an authorized multidimensional policy and outcome evidence, not one allocation scalar.

### Answer 3

Authenticate the actor, verify membership and role for the selected tenant, and create immutable server context; the header remains only a selector. Require every owned entity and relationship load to inherit tenant scope, using centralized ORM policy plus database enforcement and negative tests. Include verified tenant and authorization-relevant dimensions in cache keys and tenant plus stable operation identity in idempotency keys. Emit tenant context from the authoritative commit into authenticated immutable event metadata; consumers reject conflicting payload fields.

Workers use least-privileged roles with explicit tenant sets and transaction-local context; no ordinary job runs as a bypass user. Separate cross-tenant maintenance identities and audit. Support tickets contain references and minimized redacted evidence rather than unrestricted query copies; access is purpose-bound, approved, expiring, and logged. Test altered selectors, indirect objects, lazy/eager relationships, cache collisions, replay, dead letters, support search, cancellation, session reuse, and missing context. Trace any historical exposure and follow incident obligations.

### Answer 4

Shared tables offer best pooling and simplest fleet-wide schema but require complete row/object scoping, non-bypass roles, tenant-aware cache/queue/search, and tested single-tenant restore. Schemas add grants and namespaces but share engines, administrators, capacity, backups, and schema fleet. Databases add credential, performance, backup, and movement boundaries while multiplying connections, migrations, monitoring, and restore operations. Dedicated cells add runtime and failure isolation at still greater fixed cost and retain shared identity, control, code, suppliers, and operators.

Use a bridge: cohort ordinary tenants in shared-table databases inside bounded cells; place whales in dedicated capacity or databases based on measured limiting dimensions; place restricted tenants in eligible database, key, region, and perhaps cell boundaries derived from actual rules. Keep one logical product, migration compatibility, control-plane state machine, tenant context, telemetry contract, and security release. Cross-tenant analytics uses approved minimized derivation. Support tooling works across classes through the same scoped authority. Each class has tested tenant-granular restore, export, move, deletion, failover, and cost evidence. Reevaluate placement as workload, threat, jurisdiction, and recovery needs change.

### Answer 5

Model each government, organization, clinic, supplier, and household program as a separate authority where appropriate; do not force legal and operationally distinct actors into one tenant. Represent explicit time-bounded collaborations, delegations, case transfers, and shared incidents as resources with their own membership, purpose, data classes, and audit. Authenticate people and field devices, verify tenant and collaboration role, and carry signed operation identity through store-and-forward queues. One participant cannot select another's tenant by header or reuse a stale delegation after handover.

Separate public advisories, logistics aggregates, protected clinical data, household identity, safeguarding reports, supplier bids, and payment records. Keep sensitive classes in eligible regions and key scopes; minimize cross-organization data and provide offline encrypted stores with revocation, expiry, conflict, and loss procedures. Allocate queue, bandwidth, storage, translation, and support by transparent priority, reservation, and abuse controls so a large actor cannot starve a small clinic. Emergency priority requires authenticated purpose and retrospective review.

During disconnection, local authorities act only within bounded delegated rights and expose staleness. Reconnection deduplicates stable operations, rejects expired epochs, reconciles conflicts through the owning authority, and prioritizes life-safety work. Support access is scoped, time-limited, multilingual and accessible; it does not copy unrestricted case data. Evidence retains source, tenant, collaboration, purpose, event time, authority epoch, transfer, and correction while protecting affected people.

Test compromised devices, malicious participants, false organizations, traffic surge, one-region loss, queue starvation, duplicate aid, clinic privacy, supplier collusion signals, inaccessible workflows, transfer during partition, emergency access, tenant split/merge, and restoration. When an organization exits, transfer active cases under explicit consent or legal authority, revoke identities and integrations, export permitted records, retain required evidence narrowly, delete eligible derivatives and suppliers' copies, and prevent identifier reuse. Humanitarian, government, clinical, safeguarding, privacy, accessibility, security, financial, logistics, and affected-community authorities must approve real boundaries and residual risks.
