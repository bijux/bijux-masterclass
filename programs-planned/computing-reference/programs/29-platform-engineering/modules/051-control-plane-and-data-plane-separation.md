---
module_id: PLAT-051
program: Platform Engineering
level: 2
module_number: 51
title: Control-Plane and Data-Plane Separation
status: complete
last_verified: 2026-09-02
---

# Control-Plane and Data-Plane Separation

## One-Page Review

### Governing question

How should a platform separate intent, policy, planning, reconciliation, and configuration distribution from workload request/effect execution so each plane has explicit authority, performance, consistency, security, failure, recovery, and lifecycle contracts?

### Essential definitions

- A **control plane** accepts authorized intent, validates policy, stores or derives desired state, decides placement/configuration, reconciles resources, and reports status.
- A **data plane** performs the primary workload operation—serving requests, forwarding traffic, executing jobs, processing events, or reading/writing data—under admitted configuration.
- A **management plane** supports administration, lifecycle, policy, observability, audit, and operator workflows; it may configure the control plane but is not synonymous with it.
- A **northbound interface** exposes intent/status to consumers or higher-level controllers; a **southbound interface** distributes decisions and observations between controllers and controlled resources.
- **desired revision** identifies admitted intent; **applied revision** identifies the configuration a data-plane instance has actually accepted.
- **fail-static continuity** means a data-plane instance continues using the last valid configuration during temporary control-plane loss.
- A **staleness budget** bounds how long or under which conditions an old configuration remains acceptable.
- A **fencing token** is a monotonically ordered authority value used to reject effects from an obsolete controller/lease holder.
- **blast-radius isolation** prevents one tenant, controller, workload, or request class from exhausting or corrupting unrelated control/data paths.
- **bootstrap dependency** is a service, identity, network, name, secret, policy, or state prerequisite needed to start or restore a plane.

### Central model, mechanism, or theorem

For resource $r$, let desired revision be $d_r$, control-plane admitted revision $c_r$, and data-plane applied revision $a_{r,i}$ at instance $i$. Convergence claims require evidence about $d_r=c_r=a_{r,i}$ for the intended population, not one green controller condition. If $N$ agents poll at rate $\lambda$ each, aggregate request rate is $N\lambda$ before retries and watch amplification. If a control plane is placed synchronously on every data operation, end-to-end availability is $P(C\cap D)\leq\min(P(C),P(D))$; multiplying availabilities additionally assumes independence. Separation preserves the option for data work to continue under a bounded last-known-good policy.

### Critical invariants

- Planes are classified by authority, responsibility, timescale, and critical path; process or network placement alone does not define them.
- User intent is authenticated, authorized, validated, versioned, idempotent/reconcilable, and durably correlated before side effects.
- Data-plane execution never trusts unauthenticated configuration and never silently accepts an older or wrong-scoped revision.
- Control-plane loss has an operation-specific policy: continue last valid state, expire/restrict, drain, or stop; “fail open/closed” is not universal.
- Every staleness decision names affected threat, safety, correctness, availability, and revocation bounds.
- Control-plane overload is isolated by tenant/request class, bounded queues, fairness/priority, backoff, watch/list efficiency, and admission limits.
- Data-plane traffic and bulk telemetry cannot starve heartbeats, lease renewal, reconciliation, revocation, or emergency recovery.
- Desired, admitted, distributed, accepted, active, observed, and terminal outcome revisions remain distinguishable and queryable.
- Leader election coordinates active reconcilers but does not by itself make external effects exactly once; fencing/idempotency/reconciliation remain necessary.
- Bootstrap and disaster recovery work when normal DNS, identity, admission, telemetry, or the managed plane is partially unavailable.
- Plane identities, permissions, secrets, networks, audit, and administrative access are separated by least privilege and tenant scope.
- Upgrades test old/new controllers, agents, schemas, stored state, snapshots, rollback/forward recovery, and complete retirement.

### Common failures

Calling any central API a control plane; putting control and data in separate clusters while sharing one identity/database/failure domain; invoking the control plane synchronously for every user request; letting every agent poll and list the full fleet; retrying control requests without jitter or bounds; serving forever from stale configuration; expiring all routes during a brief controller outage; accepting snapshot rollback after revocation; conflating desired with applied state; treating leader election as exactly-once execution; granting controllers broad cloud administrator rights; letting admission webhooks recursively call the saturated API; making recovery depend on the failed identity or policy plane; monitoring the control plane only through itself; upgrading all controllers and agents together; and deleting a controller while finalizers, credentials, external resources, snapshots, or data-plane configuration remain.

### Compact example

A regional traffic platform exposes desired routes through an authenticated API. Admission validates ownership, targets, policy, schema, and revision, then stores intent. Reconcilers produce a signed, tenant-scoped snapshot with monotonically increasing version; agents subscribe with backoff and acknowledge accepted/rejected versions. Proxies serve traffic locally from the last valid snapshot. During a 12-minute controller outage, existing routes continue, while a revoked high-risk credential has a shorter policy TTL and causes only affected traffic to drain. Per-tenant flow control preserves lease, revocation, and recovery operations. Status separates desired, compiled, distributed, accepted, active, and synthetic-journey evidence. Recovery uses independently reachable identity and stored snapshots. Mixed-version tests and staged rollout precede upgrades; retirement removes routes, agents, credentials, snapshots, policies, finalizers, and retained evidence.

### Connections

This module builds on Kubernetes architecture, desired-state resources, platform APIs, capability reconciliation, workload standards, telemetry/security contracts, and upgrades from [PLAT-015](015-apis-and-declarative-resources.md), [PLAT-023](023-kubernetes-declarative-resources.md), [PLAT-040](040-designing-a-coherent-minimum-viable-platform.md), and [PLAT-041](041-workload-archetypes.md) through [PLAT-050](050-designing-a-golden-path-that-remains-optional-but-attractive.md). PLAT-052 deepens reconciliation; later modules cover custom resources, operators, finalizers, multi-tenancy, and fleet control.

## Governing Question

Which decisions belong in a control plane, which operations must remain in the data plane, and what interface/failure contract lets each keep doing the safest useful work when the other is slow, partitioned, overloaded, stale, compromised, or upgrading?

The words “control plane” and “data plane” are often used as architecture decoration. A central web service gets called a control plane; application Pods become “the data plane”; the diagram implies separation. That says little about whether product traffic depends synchronously on the central service, whether credentials and storage share a failure domain, whether stale policy remains safe, or whether recovery can start.

Useful separation begins with responsibility. A controller interprets intent and changes configuration or resources. A data component executes the workload outcome under accepted decisions. A management surface lets people and automation govern lifecycle. These responsibilities can be collocated for a small system or distributed across regions. Physical separation can improve isolation, but semantic contracts decide behavior.

Separation is not disconnection. The planes exchange desired state, observations, acknowledgments, heartbeats, leases, revocations, and status. The interface must handle partial failure, duplicates, reordering, version skew, and overload without turning central unavailability into fleet failure.

## Why This Matters

Control planes concentrate privilege and fan-out. One request may create cloud resources, configure thousands of agents, rotate trust, or delete data. A bug or compromised controller can scale harm faster than a manual operator.

Data planes carry product load and latency. If every request synchronously consults a central platform API, that API joins the product availability and latency path. A regional network partition then stops otherwise healthy local work.

Stale control is ambiguous. Continuing last-known-good configuration preserves availability, yet can retain revoked access, obsolete routes, unsafe capacity, or deleted resources. Expiring immediately can cause a fleet-wide outage. The correct choice depends on the operation and threat, so it must be designed before failure.

Scale reverses apparently cheap patterns. Ten agents polling each minute are harmless; 100,000 agents polling, retrying together, or relisting after reconnect can overwhelm storage and API servers. Watch fan-out, cache synchronization, status writes, and telemetry need capacity and fairness models.

Recovery is where hidden coupling appears. If the control plane needs the managed cluster’s DNS, admission webhook, secret controller, telemetry, or identity to restore that same cluster, an outage becomes a bootstrap deadlock.

## Prerequisites and Retrieval

Retrieve distributed-system failure models, availability, latency, partial failure, partitions, consistency, linearizability/eventual consistency, leases, fencing, idempotency, retries/backoff/jitter, queues/fairness, pub-sub/watch, snapshots/deltas, authentication/authorization, PKI and workload identity, desired state, declarative resources, controllers, scheduling, APIs and long-running operations, health/telemetry, multi-tenancy, security, SLOs, incident response, backup/restore, progressive delivery, compatibility/skew, and decommissioning.

You should distinguish control from management; decision from execution; intent from configuration; desired from admitted/applied/active/observed state; logical from physical separation; control-plane availability from data-plane continuity; last-known-good from permanently valid; leader from fenced authority; acknowledgement from workload outcome; watch from reliable event log; cache from source of truth; authentication from authorization; fail-open from fail-static; and rollback of controller binary from rollback of externally changed state.

## Learning Objectives

After completing this module, you should be able to:

1. classify control, data, management, application, and operational responsibilities without relying on deployment topology;
2. specify northbound and southbound contracts for intent, revision, distribution, acknowledgement, observation, and error;
3. model desired/admitted/applied state, convergence, staleness, and last-known-good continuity;
4. size polling/watch/status/fan-out traffic and design overload isolation, priority, fairness, and retry behavior;
5. secure plane identity, authorization, snapshots, agents, administrative access, tenants, and revocation;
6. design leader election, fencing, idempotency, and external-effect reconciliation;
7. remove bootstrap loops and build independent recovery, backup, telemetry, and emergency paths;
8. test partial failure, stale control, reconnect storms, mixed versions, rollback/forward recovery, and regional/federated operation; and
9. retire control/data resources, authority, state, finalizers, snapshots, and evidence completely.

## Core Exposition

### Classify responsibilities before components

List actions and their authority. Consumer declarations, policy decisions, placement, desired-state persistence, configuration compilation, reconciliation, rollout, and lifecycle scheduling are control/management concerns. Request forwarding, query execution, event handling, job computation, storage read/write, and local enforcement are data-plane concerns.

Management plane responsibilities include operator policy, fleet lifecycle, access administration, audit/evidence, cost, incident actions, and control-plane configuration. Some architectures merge management and control. Keep the conceptual distinction because human-scale change and fast automatic control have different interfaces, privileges, and failure budgets.

Operational plane describes local component condition and resources: process health, ports, queues, memory, disks, or device state. Observations inform control but are not decisions themselves.

Classify each dependency by whether it is synchronous on a product operation, asynchronously updates configuration, supplies observation, or supports administration. A feature-flag lookup on every request behaves as a data-path dependency even when branded a control-plane SDK.

### Draw logical and physical boundaries separately

Logical separation identifies contracts and authority. Physical separation identifies processes, hosts, clusters, regions, accounts, networks, storage systems, and operator groups. Either can exist without the other.

Two services on separate clusters still share a failure domain if they require one database, identity issuer, DNS zone, cloud account quota, deployment pipeline, root credential, or operator action. Conversely, a small controller and worker in one process can preserve clear interfaces and later separation, though they share availability/security fate.

Map correlated dependencies: power/region/provider, network, identity, PKI, naming, time, storage, policy/admission, telemetry, software supply chain, management access, and staffing. “Highly available” replicas in one correlated domain do not create independent availability.

Choose physical separation according to risk, scale, latency, tenancy, recovery, and economics. More networks/clusters can add isolation but also credentials, updates, data replication, and failure modes.

### Specify the northbound intent contract

Accept meaningful desired outcomes, not imperative provider steps, where reconciliation is intended. Define resource identity, schema/version, owner/tenant, desired revision, preconditions, idempotency key, authorization, policy, deadlines, dry-run/diff, operation identity, status, cancellation/deletion, and lifecycle.

Validate syntax, semantics, references, quotas, security, and conflicts before side effects when possible. Admission success means intent is accepted, not that the outcome exists.

Persist accepted intent and operation correlation durably. If persistence succeeds but response is lost, a retry with the same idempotency identity returns/reconciles the original operation rather than creating another resource.

Expose desired and observed state separately. Status belongs to a controller-owned subresource or equivalent boundary so consumers do not accidentally overwrite observation while editing intent.

### Specify the southbound configuration contract

Configuration delivered to an agent needs resource/tenant scope, schema/type, immutable version, generation timestamp, source/controller identity, content digest, dependencies, validity/expiry semantics, rollout cohort, and signature/authentication where appropriate.

Agents authenticate the source, authorize scope, validate schema and local invariants, stage configuration, apply atomically or with declared partial semantics, and acknowledge accepted or rejected revision with reason. A transport-level receipt is not an apply acknowledgement; apply acknowledgement is not a workload outcome.

Use full snapshots when atomic whole-state reasoning and recovery simplicity dominate. Use deltas when state/fan-out size makes snapshots expensive. Delta systems need base-version knowledge, ordering/gap recovery, deletion/tombstone semantics, and resynchronization.

Reject configuration downgrade unless an authorized rollback explicitly identifies the target and its security/data implications. Monotonic revision alone is insufficient across restore or authority change; epoch/fencing identity can separate histories.

### Model revision state precisely

For resource $r$, define desired $d_r$, admitted/compiled $c_r$, distributed $s_r$, instance-applied $a_{r,i}$, and observed effect $o_r$. These may legitimately differ during rollout.

Status should expose population counts and identities: target instances, connected, sent revision, accepted, rejected, active, stale, unknown, draining, and absent. “Ready” must not hide a split fleet.

Convergence condition depends on the operation. It might require every required instance at $a_{r,i}=c_r$, a quorum, all instances serving a route, or a canary percentage plus SLO evidence. Define exclusions and deadline.

Status observations can be stale or lost. Record observation time/source and use unknown after freshness expires. Do not infer an agent applied a snapshot merely because the controller sent it.

### Choose fail-static, expiry, drain, or stop per operation

During control loss, a data plane may continue last-known-good state. This avoids adding control availability to every data operation and reduces correlated outage. It also delays desired change and revocation.

Define staleness budget by configuration class. Stable routing to healthy local endpoints may remain safe for hours; an authorization revocation, compromised credential, price/risk limit, or safety interlock may require rapid expiry or locally verifiable revocation.

Options include: continue indefinitely for immutable low-risk configuration; continue for TTL then restrict; preserve reads while disabling writes; drain new work but finish admitted work; use cached signed policy plus local limits; shift to a safe static fallback; or stop the affected operation.

Fail-open permits operation without required decision; fail-closed denies it. Fail-static continues an already validated decision. Treat them separately. The safest behavior may vary across authentication, routing, rate limiting, feature rollout, and emergency shutdown.

Test clock uncertainty and offline duration. TTL depending on unsynchronized clocks can expire early/late. Include monotonic timers where local duration is enough and authoritative epochs for revocation histories.

### Keep control work off the hot path deliberately

If product operation succeeds only when both control $C$ and data execution $D$ are available, availability is $P(C\cap D)$, no greater than the smaller marginal availability. Under independence it is $P(C)P(D)$, but common dependencies often make independence false.

Distribute validated configuration asynchronously so local data-plane decisions serve common traffic. Keep control interaction for changes, leases, observations, or bounded cache misses. If central authorization is required per operation, classify it honestly as part of the data request path and engineer its latency/availability accordingly.

Avoid control-plane calls from admission or policy callbacks that recursively depend on the same saturated API. Recursive flow control can produce priority inversion or deadlock.

Separate bulk analytics and configuration discovery from urgent revoke, lease, health, and recovery actions.

### Engineer polling, watch, and fan-out capacity

If $N$ agents poll at rate $\lambda$, base request rate is $N\lambda$. At $N=100{,}000$ and one poll per minute, average is about 1,667 requests/second before retries, authentication, list cost, and synchronized bursts.

Prefer watches/subscriptions for change delivery when the source can sustain connections and replay/resync. A watch is not automatically a durable log: disconnection, compaction, authorization change, missed versions, and relist must be handled.

Use shared caches/fan-out tiers carefully to reduce central load. Cache identity, tenant isolation, revision integrity, freshness, and failure behavior become part of the trust model.

Clients use exponential backoff with jitter, bounded retries, server hints, and circuit/load shedding. On reconnect, spread resubscription, resume from valid revision where supported, and rate-limit full resync.

For average arrival $\lambda_a$ and mean time in a stable queue/system $W$, Little’s Law gives mean in-flight work $L=\lambda_a W$. It does not size burst buffers or prove stability; tail latency, service capacity, class isolation, and overload policy remain necessary.

### Isolate overload and noisy controllers

Classify API work by tenant, actor, verb/resource, cost, and criticality. Reserve capacity for heartbeats, leader election, revocation, built-in reconciliation, and emergency recovery. Bound nonessential list, status, and bulk operations.

Kubernetes API Priority and Fairness illustrates request classification, priority levels, concurrency isolation, limited queuing, fair queuing, and flow distinction. Its recursive-server cautions show why admission/API aggregation must avoid circular resource waits.

Rate-limit at admission and at expensive downstream effects. One small API request may fan out to thousands of cloud or agent operations. Cost weights should reflect work, not only request count.

Expose rejected, queued, waiting, executing, timed-out, retried, and throttled counts/latency by bounded class. A 429 is a control response; clients must not immediately retry in lockstep.

### Design controller reconciliation safely

Controllers compare desired and observed state, calculate a bounded action, perform/reconcile it, record status, and repeat. They should be level-based—driven by current state—rather than assuming every event arrives exactly once.

Events and watches are prompts to reconcile, not complete truth. Relist/resync and ownership references recover from missed notifications. Idempotency keys, conditional writes, compare-and-swap/resource versions, and provider query prevent duplicate effects.

Leader election ensures one recognized active participant for a lease interval but messages and external effects from an old leader can outlive the lease. Use fencing tokens accepted by the effect target, or make effects idempotent/reconcilable with authoritative state.

Limit action per loop and use per-resource backoff so one failing object does not create hot-loop starvation. Separate permanent invalid intent from transient provider failure and unknown outcomes.

### Secure the plane boundary

Give consumers, controllers, agents, reconcilers, compilers, status writers, operators, and break-glass responders distinct identities. Scope each to tenant/resource/action. A controller with fleet-wide cloud administrator credentials is a high-consequence target.

Authenticate and encrypt northbound, southbound, east-west, and administrative channels. Authorize intent and configuration separately. Bind configuration signature/issuer, audience/tenant, revision, digest, and validity.

Protect desired/state storage, snapshot stores, signing keys, queues, caches, audit, and backups. An attacker who can publish an old signed snapshot can restore revoked access unless epochs and anti-rollback policy exist.

Segment control endpoints from public workload traffic and restrict agent egress to required services. Network separation supplements identity; it is not identity.

Audit who changed intent/policy, which controller revision compiled it, which agents accepted it, and what external effects occurred—without recording secrets or unbounded sensitive payloads.

### Separate tenants and failure domains

Tenant identity must flow through resource ownership, authorization, quotas, queues, caches, snapshots, agent subscriptions, status, telemetry, and deletion. Never rely only on names supplied by clients.

Apply per-tenant and global bounds. A tenant creating millions of resources, rapidly changing desired state, or causing persistent provider failure must not starve system reconciliation.

Consider sharding by tenant, region, resource type, or cell. Shards reduce blast radius and fan-out but create placement, rebalancing, cross-shard operation, fleet visibility, and disaster-recovery complexity.

High-risk tenants may need separate control/storage roots and data-plane cells. Shared dashboards or update pipelines can reintroduce common-cause failure.

### Remove bootstrap and recovery loops

Draw a dependency graph for API startup, storage, identity, certificates, DNS, network, admission/policy, schedulers/controllers, secret delivery, telemetry, backups, and management access. Identify cycles.

Keep minimal recovery identity, naming/network, policy, and credentials independently reachable and strongly protected. A cluster admission webhook should not be the only mechanism allowed to restore itself if its absence blocks all writes.

Store tested last-known-good configuration and control-state backups outside the failed plane’s sole authority. Protect integrity, confidentiality, version compatibility, and restore credentials.

Define degraded management: inspect state, freeze mutations, restore control, rotate trust, reconcile effects, and validate data-plane state. Break-glass access is short-lived, narrow, alerted, audited, and reviewed.

Monitor critical control components through a reduced-dependency path. If telemetry depends entirely on the failed control plane, silence cannot distinguish health from blindness.

### Design regional and hierarchical control

A global control plane may define policy, identity, placement, and fleet intent; regional controllers compile/localize and distribute; agents execute. Each layer is both data plane to the layer above and control plane to the layer below, so plane labels are relational.

Define authority during partition. Can regions accept new intent, allocate resources, rotate secrets, or only serve existing configuration? How are conflicting changes reconciled? Which operations require global consensus?

Use epochs/ownership to prevent two regions from controlling the same exclusive resource. For multi-writer intent, define merge/conflict semantics rather than last-writer-wins by accident.

Replicate only required state and respect residency/privacy. Global visibility can use aggregates without centralizing sensitive workload data.

### Observe both planes and their interface

Control-plane SLIs include intent admission correctness/latency, durable operation status, reconciliation lag, queue age, provider error, snapshot compilation/distribution, connected agents, rejection, skew, stale/unknown population, and recovery.

Data-plane SLIs measure workload outcomes: request success/latency, event settlement/age, job terminal result, storage correctness/availability, and policy enforcement. Do not declare product health from control convergence alone.

Interface telemetry correlates resource, tenant, desired/admitted/distributed/applied revisions, controller/agent versions, operation IDs, and bounded error classes. Avoid high-cardinality raw identities in metrics; use queryable logs/traces/status under access policy.

Use independent synthetic journeys that submit intent, observe reconciliation, and verify a harmless data-plane outcome. Label them synthetic and monitor their identity/scheduler.

### Upgrade and roll back across the boundary

Publish compatibility for API schemas, stored desired/status state, controllers, snapshot formats, agent/data-plane versions, and providers. Test oldest supported agent with newest controller and the reverse when promised.

Roll control instances progressively while data planes continue from last valid state. Canary snapshots/configuration by cell/cohort, observe accept/reject and workload outcomes, then expand.

An agent rejecting an unknown field should preserve last valid state and report reason rather than partially applying. A controller must not assume new defaults exist until applied-version evidence confirms them.

Rollback of controller code is safe only if it reads current stored state, snapshot epochs, and status schemas and does not resurrect revoked configuration. Otherwise roll forward or restore a compatible control environment.

### Test adversarial failure and scale

Test control API/storage loss, region partition, slow storage, identity/PKI/DNS failure, clock skew, leader churn, stale lease, old-controller messages, provider timeout/unknown outcome, partial snapshot, signature failure, downgrade, agent rejection, reconnect storm, watch compaction, cache corruption, and telemetry loss.

Load-test tenant fairness, expensive operations, status storms, list/watch fan-out, snapshot size, change burst, and retry amplification. Validate critical traffic under overload, not only peak throughput in healthy state.

Exercise data continuity with control absent beyond each staleness boundary. Verify which operations continue, restrict, drain, or stop, and ensure revoked/high-risk state does not persist beyond policy.

Run restore from independent backups/credentials and reconcile all external/data-plane effects. A control database restore can regress desired revision while the world remains newer.

### Retire plane resources and authority

Deletion is a distributed workflow. Stop new intent, mark desired deletion, drain or migrate data-plane work/state, remove routes/subscriptions, reconcile external resources, and then remove finalizers/tombstones according to contract.

Never abandon unreachable external effects by deleting the controller’s record. Surface deletion blocked/unknown and give an explicit force/orphan policy with consequence and authority.

Retirement removes APIs, controllers, agents, webhooks, queues/topics, state/snapshot stores, caches, identities/roles, credentials/certificates/signing roots, network paths, policies, providers, telemetry/alerts, backups/retained data, docs, and break-glass paths.

Preserve required audit/provenance without leaving executable authority. Verify no agent accepts the retired issuer/epoch and no restore procedure resurrects the plane.

### Use an executable boundary inventory

The following synthetic inventory counts minimum properties across ten plane interactions. It does not prove architecture, security, availability, scale, recovery, or production convergence.

<!-- bijux-verify: {"id":"control-data-plane-boundary-inventory","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"interactions 10\nauthority_scoped 10\nrevision_correlated 9\ndata_continuity 8\nstaleness_bounded 8\noverload_isolated 8\nidentity_separated 9\nbootstrap_tested 8\nmixed_versions_tested 8\noutcome_observed 9\n","stderr":""}} -->
```python
interactions = [
    ("intent-admission", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("resource-reconcile", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("route-distribution", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("policy-revocation", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("agent-heartbeat", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("provider-effect", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("regional-failover", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("control-restore", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("legacy-agent", 1, 1, 0, 0, 0, 1, 0, 0, 1),
    ("emergency-admin", 1, 0, 0, 0, 0, 0, 0, 0, 0),
]
fields = [
    "authority_scoped", "revision_correlated", "data_continuity",
    "staleness_bounded", "overload_isolated", "identity_separated",
    "bootstrap_tested", "mixed_versions_tested", "outcome_observed",
]
print("interactions", len(interactions))
for index, field in enumerate(fields, start=1):
    print(field, sum(interaction[index] for interaction in interactions))
```

Incomplete legacy and emergency records stay visible. Emergency authority still needs independent identity, bootstrap, observation, and retirement even when it intentionally bypasses ordinary reconciliation.

## Definitions and Notation

- $r$: governed resource or desired outcome.
- $i$: data-plane/agent instance in the intended target population.
- $d_r$: consumer-desired revision for $r$.
- $c_r$: control-plane admitted/compiled revision.
- $s_r$: revision distributed by the control plane.
- $a_{r,i}$: revision accepted/applied by instance $i$.
- $o_r$: observed workload-effect evidence associated with the revision.
- $N$: number of polling/subscribing agents.
- $\lambda$: per-agent poll request rate; $N\lambda$ is base aggregate rate before amplification.
- $\lambda_a$: average admitted work arrival rate for Little’s Law.
- $W$: mean time in the stable system/queue under the defined population.
- $L=\lambda_aW$: mean work in the system under Little’s Law assumptions.
- $C,D$: events that required control and data dependencies are available for a synchronous operation.
- **epoch**: authority generation separating revision histories across leadership or restore.
- **staleness budget**: maximum age/condition under which last valid configuration may continue for a named operation.
- **unknown**: state where freshness, delivery, application, effect, or authority cannot be established.

## Mechanisms, Invariants, or Proof Structure

1. Enumerate consumer intent, control decisions, data operations, management actions, observations, and external effects.
2. Classify logical planes by authority/responsibility/timescale, then map physical failure and trust domains.
3. Specify northbound intent/status and southbound snapshot/delta/acknowledgement contracts with immutable revisions.
4. Define desired, admitted, distributed, applied, active, observed, stale, rejected, and unknown state.
5. Select per-operation last-known-good, TTL/restriction, drain, or stop behavior from threat/correctness/availability analysis.
6. Size fan-out, watch, status, and retries; isolate tenants/classes with queues, priority, fairness, backoff, and shedding.
7. Reconcile level-based current state using idempotency, conditional updates, leader election plus fencing, and bounded actions.
8. Separate plane identities/permissions/storage/networks and secure configuration integrity, audience, epoch, and anti-rollback.
9. Break bootstrap cycles and test independent inspection, restore, trust rotation, and telemetry under partial failure.
10. Qualify regional/hierarchical authority, mixed versions, canaries, rollback/forward recovery, and data-plane outcomes.
11. Delete through reconciled workflow and retire all remaining authority, state, agents, integrations, evidence, and restore paths.

The synchronous availability bound follows because $C\cap D$ is a subset of both $C$ and $D$, hence $P(C\cap D)\leq\min(P(C),P(D))$. Equality/product calculations require additional dependence assumptions. This set relation motivates—but does not prove the safety of—asynchronous separation.

Polling fan-out $N\lambda$ is arithmetic under equal per-agent average rate. It omits authentication/storage cost, status writes, bursts, reconnects, retries, and shared caches. Capacity tests must include those effects.

## Alternatives and Trade-Offs

- **Logical separation versus physical isolation:** logical contracts improve reasoning/evolution; physical boundaries add fault/security isolation but operational complexity.
- **Central versus regional control:** central control simplifies global policy; regional control lowers latency/partition blast radius but adds authority/conflict state.
- **Push/watch versus polling:** push/watch reduces repeated reads and latency; polling is simpler and naturally repairs missed notifications but scales poorly and can synchronize.
- **Full snapshots versus deltas:** snapshots simplify atomic reasoning/recovery; deltas reduce transfer but need ordering, base, deletion, and gap repair.
- **Fail-static versus expire:** last-known-good preserves service; expiry bounds stale security/correctness but can create fleet outage.
- **Online central decision versus local policy:** central decisions see current global state; local policy reduces latency/dependency but may be stale and needs secure distribution.
- **Single leader versus active-active:** a leader simplifies ordering; active-active improves locality/availability but needs partition/conflict authority.
- **Shared control plane versus tenant cells:** sharing is efficient and consistent; cells isolate scale/security failure but multiply operations and fleet coordination.
- **Strong consistency versus eventual convergence:** strong ordering simplifies invariants but costs latency/availability; eventual control tolerates partition but exposes skew/conflict.
- **Status writes per event versus aggregation:** detailed status aids diagnosis; high-rate writes can overload the control store.
- **Broad controller authority versus brokered effects:** broad roles simplify integrations; narrow brokers reduce blast radius but add APIs and dependencies.
- **Long configuration TTL versus short TTL:** long TTL improves partition continuity; short TTL improves revocation/freshness at outage risk.
- **In-band management versus independent recovery:** in-band is cheaper and coherent; independence avoids bootstrap deadlock but requires protected duplicate paths.
- **Binary rollback versus forward recovery:** rollback is quick for compatible state; forward recovery respects new schemas/effects/epochs when reversal is unsafe.

## Failure Modes and Misconceptions

- **“Separate clusters mean separate planes.”** shared identity, storage, DNS, quota, pipeline, or operators can preserve one failure domain.
- **“Central means control plane.”** a central service on every request is part of the data path for that outcome.
- **“Data plane has no policy.”** it often performs local enforcement from admitted policy/configuration.
- **“Control outage should always fail closed.”** denial can amplify availability/safety harm; choose per operation and threat.
- **“Continuing last-known-good is fail open.”** fail-static continues an already authorized decision but still needs staleness/revocation bounds.
- **“Sent means applied.”** transport delivery, local acceptance, activation, and outcome are separate.
- **“Desired equals actual.”** admission, queues, providers, agents, and workload behavior can diverge.
- **“A watch is an event log.”** compaction, disconnect, missed versions, and relist semantics require reconciliation.
- **“Polling is cheap.”** fleet multiplication, retries, list size, authentication, and synchronized reconnect create load.
- **“Replicas make the control plane independent.”** correlated region/storage/identity/upgrade failures remain.
- **“Leader election gives exactly once.”** old effects and messages survive lease loss; use fencing/idempotency/reconciliation.
- **“Monotonic version prevents rollback.”** restore/new authority histories need epochs and anti-rollback policy.
- **“Authentication authorizes configuration.”** source identity, audience, tenant, resource, action, and policy all matter.
- **“Network isolation is identity.”** addresses/segments do not prove workload/controller authority.
- **“Fair queues guarantee recovery.”** wrong classification, recursive calls, exhausted downstreams, or exempt floods can still fail.
- **“Control health means service health.”** only data-plane/domain outcomes establish user service behavior.
- **“Stale telemetry means stable state.”** missing evidence becomes unknown after freshness bounds.
- **“Rollback is redeploying the controller.”** stored schemas, snapshots, agents, providers, trust, and effects may be newer.
- **“Backup restores the control plane.”** credentials, compatibility, external reconciliation, and data-plane divergence must be tested.
- **“Deleting the API retires the plane.”** agents, snapshots, external resources, finalizers, identities, policies, and restore paths remain.

## Worked Examples

### Example 1

A feature service is queried synchronously on every checkout. A regional feature-control outage stops checkout despite cached stable rules. Stable flags move into signed local snapshots, while high-risk kill switches keep short freshness. Conclusion: naming a service control plane does not keep it off the data path.

### Example 2

At 100,000 agents polling once per minute, base mean load is $100{,}000/60\approx1{,}667$ requests per second before retries. Watch subscriptions, sharded caches, jitter, and bounded resync replace full polling. Conclusion: per-agent cheap work becomes fleet load.

### Example 3

The controller reports revision 42 sent; 80 proxies run 42, 15 reject it, and five are disconnected. Status shows each population and keeps outcome incomplete. Conclusion: distribution is not convergence.

### Example 4

Routing configuration may remain for one hour during control loss, but a compromised-client revocation expires within five minutes and drains affected sessions. Conclusion: staleness budgets belong to configuration classes and threats.

### Example 5

An old leader loses its lease after creating a cloud volume, then retries after a new leader has acted. The provider accepts fencing epoch 18 only, and reconciliation finds the existing operation. Conclusion: election without fencing/idempotency does not prevent duplicate external effects.

### Example 6

Tenants share an API queue. One controller lists every object continuously and starves node heartbeats. Per-class concurrency, fair flows, pagination/watch caching, and backoff preserve critical work. Conclusion: overload isolation is part of control-plane correctness.

### Example 7

Admission for the management cluster depends on a webhook hosted in that cluster, while deployment of the webhook itself requires admission. A protected bootstrap policy and independently reachable recovery identity break the cycle. Conclusion: normal self-hosting needs an exceptional restoration path.

### Example 8

A global controller and isolated region both accept writes during partition, assigning one exclusive IP twice. The design changes to globally fenced allocation while regions may serve existing routes and create only region-owned resources. Conclusion: partition authority must be operation-specific.

### Example 9

New snapshots contain a field old agents ignore, causing policy to default permissive. Compatibility tests require explicit rejection; the controller keeps those agents on the old schema until migration. Conclusion: syntactic forward compatibility can violate semantics/security.

### Example 10

A platform deletes a resource record despite provider timeout. The cloud database and agent subscription remain, billing and serving traffic. Deletion instead stays `Unknown/Blocked`, reconciles by external identity, then removes credentials/snapshots. Conclusion: losing the control record abandons the effect rather than retiring it.

## Cross-Program Connections

- **Distributed systems:** partitions, consistency, leases, fencing, idempotency, clocks, retries, caches, and convergence define plane behavior.
- **Control theory:** desired state, observation, error, actuation, delay, stability, saturation, and feedback frame reconciliation.
- **Networking:** SDN forwarding/control/management planes, routes, subscriptions, locality, and failure domains provide the original vocabulary.
- **Operating systems:** process/device state, isolation, scheduling, queues, signals, and resource control ground local agents/data paths.
- **API engineering:** intent, idempotency, long-running operations, versions, status, errors, auth, and deprecation define northbound contracts.
- **Security engineering:** least privilege, trusted configuration, anti-rollback, revocation, tenancy, audit, and break glass protect concentrated authority.
- **Reliability engineering:** critical paths, SLOs, overload, blast radius, graceful degradation, recovery, and canaries connect planes to outcomes.
- **Data engineering:** snapshots/deltas, CDC-like streams, schema evolution, state stores, compaction, lineage, and reconciliation apply to configuration.
- **Systems engineering:** functional allocation, interfaces, modes, verification, common-cause failure, lifecycle, and disposal prevent topology-only separation.
- **Organizational design:** infrastructure provider, cluster/platform operator, application owner, security, and incident roles align with authority boundaries.

## References

1. Kubernetes Authors, “Kubernetes Components,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/overview/components/
2. Kubernetes Authors, “Controllers,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/architecture/controller/
3. Kubernetes Authors, “Communication Between Nodes and the Control Plane,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/architecture/control-plane-node-communication/
4. Kubernetes Authors, “API Priority and Fairness,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/cluster-administration/flow-control/
5. Kubernetes Authors, “Leases,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/architecture/leases/
6. Kubernetes Authors, “Kubernetes API Concepts,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/reference/using-api/api-concepts/
7. Kubernetes Gateway API Authors, “Roles and Personas,” current documentation, retrieved 2026-09-02. https://gateway-api.sigs.k8s.io/docs/concepts/roles-and-personas/
8. Envoy Authors, “xDS REST and gRPC Protocol,” current documentation, retrieved 2026-09-02. https://www.envoyproxy.io/docs/envoy/latest/api-docs/xds_protocol.html
9. IRTF Software-Defined Networking Research Group, “Software-Defined Networking: Layers and Architecture Terminology,” RFC 7426, January 2015. https://www.rfc-editor.org/rfc/rfc7426
10. Seth Gilbert and Nancy Lynch, “Brewer’s Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services,” SIGACT News 33(2), 2002. https://doi.org/10.1145/564585.564601
11. Betsy Beyer et al., “Handling Overload,” Site Reliability Engineering, Google, 2016. https://sre.google/sre-book/handling-overload/
12. Betsy Beyer et al., “Addressing Cascading Failures,” Site Reliability Engineering, Google, 2016. https://sre.google/sre-book/addressing-cascading-failures/
13. National Institute of Standards and Technology, “Zero Trust Architecture,” SP 800-207, August 2020. https://doi.org/10.6028/NIST.SP.800-207
14. CNCF Platforms Working Group, “Platforms White Paper,” April 2023. https://tag-app-delivery.cncf.io/whitepapers/platforms/

## Exercises

### Exercise 1

Classify the control, data, management, operational, and application responsibilities for an internal traffic-routing platform. Draw northbound/southbound contracts, identities, state, and failure domains.

### Exercise 2

A fleet has 240,000 agents polling every two minutes, with a retry multiplier of 1.25 during mild failure and mean server time 80 ms. Compute base and amplified request rates and use Little’s Law to estimate mean in-flight requests; state why this is not capacity proof.

### Exercise 3

Design staleness behavior for ordinary routes, authentication trust, authorization revocation, rate limits, feature configuration, and emergency shutdown during a 30-minute control partition. Address clocks, local evidence, scope, recovery, and outcomes.

### Exercise 4

Design a controller that provisions external databases using leader election. Specify desired/status state, operation identity, conditional updates, fencing/idempotency, unknown outcomes, retries, deletion/finalizers, and disaster recovery.

### Exercise 5

Plan a mixed-version upgrade of a global controller, regional compilers, snapshot schema, and 20,000 agents without making product traffic depend on control-plane availability. Include compatibility, cohorts, rejection, telemetry, rollback/forward recovery, and retirement.

## Answers to the Exercises

### Answer 1

Application owners declare host/path/backend, exposure, policy, owner, and SLO through the northbound API; platform operators manage tenancy, policy, versions, support, and lifecycle; the control plane authenticates/admit/stores intent, allocates routes, compiles snapshots, reconciles gateways, and reports revision status; proxies are data plane, matching/forwarding locally; process/port/queue condition is operational state. Southbound snapshots carry tenant/resource, schema, epoch/revision, digest, validity, signature, and dependencies; acknowledgements distinguish received, accepted, active, rejected, and observed route outcome. Separate consumer, compiler, distributor, agent, status, and emergency identities. Map shared database, PKI, DNS, region, provider, network, deployment, and operator dependencies rather than assuming process separation. During control loss proxies serve bounded last-known-good routes; risky revocation has a shorter rule. Management and synthetic outcome evidence remain reduced-dependency.

### Answer 2

Per-agent rate is $1/120$ requests per second, so base aggregate is $240{,}000/120=2{,}000$ requests per second. With multiplier 1.25, arrival is 2,500 requests per second. With mean system time $W=0.08$ seconds, Little’s Law estimates $L=2{,}500\times0.08=200$ mean in-flight requests if the measured system is stable and definitions align. This does not size capacity: it omits burst synchronization, tail latency, authentication/storage CPU, payload/list size, connections, status writes, failure slowdown, class fairness, queue limits, downstream fan-out, and severe retry storms. Use watch/sharded cache, jitter/backoff, load tests, service-time distributions, critical priority, shedding, and reconnect tests.

### Answer 3

Ordinary stable routes may serve the last signed/accepted snapshot for 30 minutes or longer if endpoints remain locally healthy; prevent new global allocations. Authentication trust can use cached trust bundles with validity/clock bounds and independently delivered emergency distrust. Authorization revocation should use short-lived credentials/local revocation epochs or drain the affected scope after a short TTL; do not expire unrelated traffic. Rate limits may retain conservative local token buckets and stop global quota reallocation. Feature configuration keeps stable low-risk values but expires high-risk experiments or write-enabling flags. Emergency shutdown needs an independently authenticated/fenced path or pre-distributed local rule and must not depend solely on the partitioned controller. Use monotonic elapsed timers plus bounded wall-clock uncertainty, record stale age/reason, test reconnection/downgrade, reconcile changes, and verify domain outcomes/security rather than control connectivity alone.

### Answer 4

Desired state includes database identity, owner/tenant, class/region, policy, deletion intent, and generation. Status carries provider operation/resource identity, observed generation, conditions, endpoint reference, last observation, and deletion progress without credentials. Admission creates a durable operation/idempotency identity before provider effects. The active reconciler conditionally claims the resource using current version and lease epoch; the provider broker accepts a fencing token or idempotency key. On timeout, query operation/resource identity before retry. Use bounded per-resource backoff and classify invalid/transient/unknown. Leader change re-lists current state; election alone is not exactly once. Deletion finalizer blocks record removal until sessions/data disposition, provider deletion or explicit orphan authority, credentials/network, and evidence are reconciled. DR restores desired/control data, advances epoch, inventories provider reality, rejects stale leaders, and reconciles before re-enabling mutations.

### Answer 5

Publish supported tuple/skew matrix for old/new global, regional, snapshot, and agents. Make new components read old stored state; make regional compilers accept both global versions; introduce an additive snapshot schema that old agents either safely interpret or explicitly reject. Upgrade standby/global then canary global instances, a regional compiler, and representative agent cohorts/cells. Proxies retain last valid snapshots during control rollout. Status records sent/accepted/rejected/active populations and data-plane SLO/synthetic outcomes; pause on rejection, skew, policy, latency, or error thresholds. Do not assume new semantics until applied evidence covers the intended population. Preserve old snapshot production until rollback window closes; if new desired state or epochs cannot be read by old control, use forward repair. Progress 20,000 agents with jittered reconnect/resync and priority protection. Finally stop old-schema production, prove no old agents/snapshots/recovery readers, then retire binaries, schemas, caches, signing trust, credentials, dashboards, and restore artifacts.
