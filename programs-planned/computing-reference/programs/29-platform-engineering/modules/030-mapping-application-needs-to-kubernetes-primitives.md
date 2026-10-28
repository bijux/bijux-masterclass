---
module_id: PLAT-030
program: Platform Engineering
level: 1
module_number: 30
title: Mapping Application Needs to Kubernetes Primitives
status: complete
last_verified: 2026-09-02
---

# Mapping Application Needs to Kubernetes Primitives

## One-Page Review

### Governing question

How should a platform translate application execution, identity, state, traffic, configuration, security, placement, lifecycle, scaling, and recovery requirements into a minimal coherent set of Kubernetes primitives without attributing guarantees those primitives do not provide?

### Essential definitions

- A **requirement** states a needed outcome, constraint, failure behavior, or evidence independent of implementation.
- A **primitive** is a Kubernetes resource or mechanism with a bounded reconciliation responsibility, such as Deployment, Service, PVC, NetworkPolicy, or probe.
- A **composition** is a set of primitives plus application and infrastructure protocols that jointly satisfy one workload contract.
- A **Deployment** manages interchangeable continuously running pods and rolling replacement through ReplicaSets.
- A **StatefulSet** manages pods with stable ordinal/network/storage identities; it does not supply application replication or quorum.
- A **DaemonSet** maintains a pod on every or selected eligible node for node-local capability.
- A **Job** manages finite work toward completion; a **CronJob** creates Jobs according to a schedule and requires idempotent time/task semantics.
- A **Service** supplies stable discovery and L4 reachability to changing endpoints; Gateway API supplies role-oriented protocol-aware external or shared routing.
- A **platform capability** is a supported product contract that renders and governs multiple low-level primitives for a recurring application need.
- A **decision record** links requirements and failure assumptions to chosen/rejected primitives, ownership, lifecycle, evidence, and exceptions.

### Central model, mechanism, or theorem

Model an application contract as $A=(E,I,S,N,C,R,P,H,Q,G,O,L,X)$: execution semantics $E$, identity $I$, state $S$, networking $N$, configuration/credentials $C$, resource/runtime $R$, placement $P$, health/lifecycle $H$, security/policy $Q$, scaling/recovery $G$, observations $O$, ownership/lifecycle $L$, and declared exceptions $X$. A mapping $M(A)$ is adequate only when every requirement has an owning mechanism, evidence, and failure behavior, and every selected primitive has a requirement that justifies its cost and authority. Kubernetes reconciliation proves desired resource state only at its boundary; application correctness, transactionality, identity authorization, backup, and user outcome remain separate obligations.

### Critical invariants

- Requirements are written before resources and include steady state, startup, rollout, scale, dependency failure, node/zone loss, deletion, and recovery.
- Controller choice follows interchangeability, stable member identity, node locality, or finite completion; resource familiarity never decides it.
- Pod is the scheduling/fate/security unit: containers share network and volume context only when they require joint placement and lifecycle.
- A Service selector, route, PVC, Secret, HPA, probe, PDB, or NetworkPolicy has one explicit purpose and cannot substitute for application identity, correctness, replication, or recovery.
- StatefulSet is chosen only for stable member identity; every data workload separately defines writer fencing, replication, backup, restore, retention, and scale semantics.
- Scaling signals lead saturation, correlate with capacity, and account for startup/readiness, dependency limits, work ownership, and safe scale-down.
- Security spans service account/RBAC, Pod Security, runtime, secrets, network policy, images, admission, node/storage/provider authority, and application authorization.
- Availability is derived from replicas, independent failure domains, capacity, readiness, disruption, dependency/data protocols, and tested recovery—not a replica number.
- Every composition has ownership, status interpretation, version compatibility, deletion order, cost, and conformance tests.
- Prefer the smallest supported composition that satisfies the contract; reject speculative sidecars, controllers, CRDs, public routes, persistent volumes, and privileges.

### Common failures

Starting from a copied manifest; using StatefulSet for any database; using Deployment for identity-bound members; running node agents as Deployments; using CronJob for exactly-once business time; placing unrelated processes in one pod; adding Services to workers with no inbound consumers; using headless discovery with naive clients; embedding configuration in images; importing all Secrets; assigning PVCs to reproducible caches; treating HPA as capacity planning; scaling on CPU for I/O queues; using PDB as availability; relying on NetworkPolicy as application authorization; creating an operator for simple reconciliation; and mapping “production-ready” to a checklist without failure evidence.

### Compact example

A document-processing product decomposes into a public stateless API, durable queue, elastic workers, scheduled retention Job, and externally managed object/database services. The API and workers use separate Deployments because they scale and fail differently; only the API has a ClusterIP Service and HTTPRoute. Workers consume queue leases and scale from queue age/backlog per effective worker, with checkpoint-aware scale-down. A CronJob creates idempotent retention Jobs but authoritative retention state lives in the data service. Both images use explicit immutable configuration and workload identity; neither owns a PVC. Zone spread, requests, probes, grace, PDB, policies, telemetry, and task-level SLOs differ by component. The decision record rejects a shared pod, StatefulSet workers, public worker Service, static credentials, and CPU-only scaling because each conflicts with a stated requirement.

### Connections

This module synthesizes container artifacts and runtime from [PLAT-021](021-container-images-as-platform-artifacts.md) and [PLAT-022](022-runtime-isolation-and-resource-controls.md), declarative resources from [PLAT-023](023-kubernetes-declarative-resources.md), workload controllers from [PLAT-024](024-pods-workloads-and-controllers.md), networking from [PLAT-025](025-services-and-ingress.md), configuration/credentials from [PLAT-026](026-configuration-and-secrets.md), state from [PLAT-027](027-storage-and-stateful-workloads.md), placement from [PLAT-028](028-scheduling-and-placement.md), and lifecycle from [PLAT-029](029-health-readiness-and-lifecycle.md).

## Governing Question

Given an application and its real operational obligations, what is the smallest supported Kubernetes composition that satisfies them, which guarantees still belong to the application or external services, and what evidence would disprove the mapping before production?

Kubernetes APIs are composable control loops, not an architecture generator. Each resource reconciles a bounded desired state. Adding resources can improve automation, but it also adds controllers, permissions, state transitions, version dependencies, and failure modes.

The disciplined sequence is requirement → failure model → primitive responsibility → composition → evidence → lifecycle. Starting from YAML reverses the causality and makes accidental fields look like requirements.

## Why This Matters

Primitive selection hardens into platform architecture. An unnecessary PVC constrains scheduling and deletion. An unnecessary Service expands discovery and policy. A broad sidecar couples resources and lifecycle. A wrong controller changes identity, rollout, and recovery. These choices become difficult to remove once telemetry, automation, and runbooks depend on them.

Under-modeling is equally costly. A Deployment cannot preserve database member identity by intention alone. A Service cannot authenticate callers. A Secret is not a complete credential system. A PDB cannot protect direct deletion or node loss. An HPA cannot scale a dependency or create provider capacity.

A requirements-first mapping creates explainable systems and reusable platform products. Reviewers can ask whether a primitive has a justified responsibility and whether any requirement lacks an owner.

## Prerequisites and Retrieval

Retrieve containers, pods, controllers, Services, EndpointSlices, Gateway API, DNS, TLS, configuration, credentials, volumes, workload identity, RBAC, admission, resource requests, scheduling, topology, probes, signals, disruption, autoscaling, metrics, queues, transactions, idempotency, backup, and failure domains.

You should distinguish process, container, pod, workload controller, service endpoint, application identity, data identity, and user-visible service; desired from observed state; orchestration from domain correctness; horizontal scale from concurrency; and availability from recoverability.

## Learning Objectives

After completing this module, you should be able to:

1. elicit a complete workload contract before choosing Kubernetes resources;
2. select Deployment, StatefulSet, DaemonSet, Job, or CronJob from execution/identity/completion semantics;
3. decide pod boundaries, discovery, routing, configuration, credentials, storage, resource, and placement mechanisms;
4. map security, lifecycle, disruption, scaling, and recovery requirements without category errors;
5. compose common stateless, worker, scheduled, stateful, node-agent, and accelerator patterns;
6. reject unnecessary primitives and record alternatives/trade-offs;
7. validate mappings through failure, lifecycle, capacity, security, and outcome tests; and
8. turn recurring compositions into versioned, governed platform capabilities.

## Core Exposition

### Start with a workload contract canvas

Interview the application owner using concrete scenarios, not resource names. What processes run continuously or finish? Are replicas interchangeable? Does each member need stable identity? Must one instance run per node? What work is accepted, acknowledged, retried, or checkpointed?

List inbound/outbound consumers, protocols, identities, latency, connection duration, public/private boundary, and degraded behavior. Classify all data and configuration. Record consistency, writer model, durability, RPO/RTO, retention, and deletion.

Quantify startup, steady, peak, failover, batch, storage, device, and network demand. Identify hardware/runtime/topology constraints. State security principals and authorities. Define readiness, local restart, drain, disruption, scale, and recovery.

Finish with evidence: user task, service level, queue age, data position, successful restore, access denial, cost, and lifecycle status. If a requirement cannot be observed or tested, its mapping cannot be validated.

### Choose the primary controller from identity and completion

Use a **Deployment** when pods are continuously running, interchangeable, independently replaceable, and horizontally scalable. It supplies ReplicaSet reconciliation and rolling replacement. It does not make sessions stateless or data shared; applications must externalize or safely distribute state.

Use a **StatefulSet** when stable ordinal, network name, or per-member storage identity is part of the application protocol. It supplies ordered/parallel lifecycle and stable bindings. The application/operator still owns membership, quorum, replication, fencing, backup, and migration.

Use a **DaemonSet** when capability is node-scoped: networking, storage plugin, telemetry agent, security sensor, or local cache on every/selected node. It follows eligible nodes. It is not a convenient way to get many replicas or bypass ordinary scheduling.

Use a **Job** when the desired state is successful completion of finite, restartable/idempotent work. Parallelism and completions must match task partitioning. Use a **CronJob** to create Jobs on a schedule, acknowledging delayed/missed/duplicate scheduling and concurrency policy; business exactly-once belongs in durable task identity.

Bare Pods are diagnostic or exceptional low-level objects. Without a controller they are not recreated after terminal failure. Static pods are cluster/bootstrap mechanisms, not application deployment primitives.

### Decide whether processes belong in one pod

Containers share a pod only when they require the same node, network namespace, volume context, security/fate boundary, and near-identical scale/lifecycle. Examples include an application plus essential protocol proxy or content adapter that cannot function independently.

Split components when they scale differently, deploy independently, need different privileges, expose separate ownership, compete for resources, or should fail without restarting each other. A queue worker and API usually belong in different Deployments even if one repository builds both.

Sidecars add startup, readiness, resource, security, signal, drain, and version coupling. Prefer a library, node-level DaemonSet, or external service when joint fate is not required. Native sidecar ordering reduces some lifecycle ambiguity but does not erase shared-pod risk.

### Map inbound networking from real consumers

No inbound consumer means no Service. Queue workers, one-shot Jobs, and outbound processors often need only egress policy, identity, DNS, and dependency clients.

Use ClusterIP Service for stable in-cluster L4 discovery of changing interchangeable endpoints. Use a headless Service only when clients deliberately consume multiple member addresses and own balancing/failure, commonly with StatefulSet identity. Use provider LoadBalancer for a supported L4 exposure profile.

Use Gateway API/HTTPRoute for shared or public protocol-aware routing where the installed implementation and conformance meet requirements. Name Gateway/listener/route/backend/certificate owners and cross-namespace consent. Use frozen Ingress only within a supported legacy profile.

Discovery is not authentication. Add workload/client identity, TLS, application authorization, rate/abuse controls, and NetworkPolicy. Define every TLS hop and observe route/endpoint/data-plane/user outcome separately.

### Map outbound dependencies and degraded modes

Inventory each dependency by protocol, identity, timeout, retry/idempotency, connection pool, quota, locality, and failure behavior. NetworkPolicy egress allows paths; it does not make a dependency reliable or authorize its API.

Decide whether dependency failure makes the component unready, feature-degraded, queueing, fail-fast, or still useful. Avoid liveness restarts for shared outages. Bound retries and concurrency so one failing dependency does not exhaust the pod or downstream.

External managed services may be the correct primitive replacement. Kubernetes does not require databases, queues, object stores, or identity systems to run as pods. Model their endpoints, credentials, failover, observability, and recovery as external capabilities.

### Map configuration and credentials independently

Put safe defaults and schema in the image. Put small nonconfidential environment settings in ConfigMaps; use immutable versioned rollout configuration unless the application has a proven reload contract. Use Secrets or external stores only for confidential material under encryption, least privilege, rotation, and non-disclosure controls.

Choose environment injection for startup snapshots and files for structured/reloadable data. Explicitly select keys and containers. Environment and `subPath` projections do not update in place; projected files still require reopen/reload.

Prefer short-lived workload identity over static shared credentials. A source rotation is incomplete until each process loads new material and the relying system accepts it, then old material is revoked.

Do not use ConfigMap as database, coordination log, feature-experiment service, or high-frequency control plane. Select a purpose-built authority when update rate, transactionality, size, audience, or policy exceeds the object.

### Map state by data semantics, not “stateful” label

Use ephemeral writable layer or `emptyDir` for bounded discardable scratch/cache. Use PVC when a pod/workload needs filesystem/block data beyond one pod lifetime and the platform class meets topology, performance, durability, encryption, snapshot, and lifecycle requirements.

PersistentVolume means lifecycle independence, not replication or backup. Define writer fencing, access mode, volume mode, StorageClass, delayed binding, expansion, reclaim, snapshot consistency, independent backup, restore, retention, and erasure.

Many applications should store authoritative data in database/object/queue capabilities and keep pods replaceable. Adding a PVC to an otherwise interchangeable Deployment can serialize rollout and bind one replica to hidden local state.

StatefulSet plus PVC is appropriate only when stable member-to-data identity is meaningful. Scaling and ordinal reuse become data operations, not generic replica changes.

### Map resources, runtime, and placement

Declare CPU, memory, ephemeral storage, devices, init/sidecar behavior, and pod overhead from representative startup/peak/failover measurements. Limits and requests have different runtime semantics. Account for provider/node allocatable and saturation.

Choose RuntimeClass/isolation from threat and compatibility. Use non-root, least capabilities, read-only filesystem where possible, seccomp, namespace controls, and approved images. Privilege is not an application convenience.

Encode correctness/compliance/hardware requirements as trusted hard node affinity and exact taint tolerations plus positive pool affinity. Encode cost/locality preferences as soft scores. Use topology spread from the failure model, with matching selectors and sufficient independent-domain capacity.

Coordinate PVC topology and specialized devices through scheduler-supported mechanisms. Avoid `nodeName`. Define degraded placement: whether replicas remain Pending or may pack when a domain/pool is unavailable.

### Map health and lifecycle by action

Startup probe protects measured initialization. Liveness only detects local unrecoverable state where restart helps. Readiness answers safe admission of new work. Custom readiness gates represent externally observed prerequisites with authoritative writers.

The process handles PID-1 signals and idempotent bounded hooks. On termination it stops new work, drains/completes/checkpoints or hands off accepted work, flushes state, releases/fences ownership, and exits within measured grace. Abrupt node loss must remain safe without hooks.

Define probe mechanism, timing, thresholds, endpoint exposure, sidecar order, endpoint/load-balancer propagation, connection/stream lifetime, and forced-kill behavior. Test rollout, scale-down, eviction, preemption, crash, OOM, and node loss separately.

### Map availability and disruption as a system property

Replica count is only an input. Place replicas across independent failure domains, reserve failover/rollout capacity, make readiness meaningful, avoid shared dependencies, and define state quorum/failover.

Deployment `maxSurge`/`maxUnavailable`, StatefulSet ordering/partition, DaemonSet rollout, Job retry, and PDB each govern different transitions. PDB mediates cooperating voluntary evictions and cannot stop direct deletion, rollout, or involuntary failure.

For every planned disruption, state minimum useful capacity, startup/repair time, drain time, topology, data health, and controller status. For abrupt failure, state detection and replacement delay, accepted-work/data safety, and degraded user behavior.

Recovery includes configuration/image rollback, traffic rollback, data restore, credential recovery, and provider/cluster failure. A resource recreation is not necessarily application recovery.

### Map elasticity from a causal demand model

Horizontal Pod Autoscaler changes desired replicas from resource, pod, object, or external metrics for scalable targets such as Deployment or StatefulSet. It does not apply to DaemonSet and does not create node/provider/dependency capacity.

For a single metric, the controller's basic proportional model resembles

$$
desiredReplicas=\left\lceil currentReplicas\times\frac{currentMetric}{desiredMetric}\right\rceil,
$$

with tolerance, missing/not-ready metrics, multiple metrics, stabilization, and behavior policies affecting actual decisions.

Choose a leading workload metric: queue age/backlog per effective worker, concurrency, in-flight requests, or utilization when it correlates with demand and capacity. CPU is wrong for an I/O-bound queue that can be saturated while CPU is low.

Include startup/readiness delay, metric latency, capacity provisioning, downstream quotas, work partitioning, maximum safe concurrency, and graceful scale-down. Set min replicas for availability/cold start and max for dependency/cost safety. Load test the entire loop and failure behavior.

### Inspect an application portfolio systematically

The following synthetic inventory keeps controller, route, state, and autoscaling choices tied to application needs.

<!-- bijux-verify: {"id":"application-primitive-inventory","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"applications=8\ndeployments=3\nstatefulsets=2\ndaemonsets=1\njobs=1\ncronjobs=1\npublic_routes=1\npersistent_storage=3\nautoscaled=3\n","stderr":""}} -->
```python
applications = [
    {"name": "api",       "controller": "Deployment",  "public": True,  "persistent": False, "autoscaled": True},
    {"name": "database",  "controller": "StatefulSet", "public": False, "persistent": True,  "autoscaled": False},
    {"name": "node-agent","controller": "DaemonSet",   "public": False, "persistent": False, "autoscaled": False},
    {"name": "migration", "controller": "Job",         "public": False, "persistent": False, "autoscaled": False},
    {"name": "report",    "controller": "CronJob",     "public": False, "persistent": False, "autoscaled": False},
    {"name": "worker",    "controller": "Deployment",  "public": False, "persistent": False, "autoscaled": True},
    {"name": "cache",     "controller": "StatefulSet", "public": False, "persistent": True,  "autoscaled": False},
    {"name": "media",     "controller": "Deployment",  "public": False, "persistent": True,  "autoscaled": True},
]
print(f"applications={len(applications)}")
for controller in ("Deployment", "StatefulSet", "DaemonSet", "Job", "CronJob"):
    print(f"{controller.lower()}s={sum(item['controller'] == controller for item in applications)}")
print(f"public_routes={sum(item['public'] for item in applications)}")
print(f"persistent_storage={sum(item['persistent'] for item in applications)}")
print(f"autoscaled={sum(item['autoscaled'] for item in applications)}")
```

The fixture is a classification exercise, not evidence that these fictional mappings satisfy application identity, state, traffic, scaling, security, lifecycle, recovery, or platform support requirements.

### Map security by principal, authority, and data flow

Give each workload a dedicated service account when identity or API access differs. Disable automatic tokens when unnecessary. RBAC grants only required resources/verbs/namespaces and includes indirect workload/secret authority.

Apply Pod Security standards/admission, runtime controls, image provenance, read-only mounts, secret scope, trusted scheduling, NetworkPolicy ingress/egress, and provider/storage policies. Map every connection's authentication, authorization, TLS, credential lifecycle, timeout, and audit.

NetworkPolicy is additive L3/L4 allow policy implemented by the network plugin; it does not authorize an API user or protect unsupported paths automatically. Service DNS/IP is location, not identity.

Admission policies and operators have cluster authority. Add them only for enforceable recurring contracts, with failure policy, availability, versioning, metrics, audit, and break-glass behavior.

### Map observation to decisions and user outcomes

Each primitive supplies partial status: controller replicas/revisions, pod conditions, EndpointSlices, route conditions, PVC/VolumeAttachment, HPA current/desired, PDB disruptions, policy denials, events. Interpret observed generation and controller ownership.

Application telemetry covers accepted/completed/error work, latency, saturation, queue age, data position, dependency result, and business task. Infrastructure covers node/network/storage/provider realization. Correlate by workload revision, pod UID, request/task, and safe resource identity.

Do not create one “healthy” dashboard. Expose desired, reconciled, data-plane, process-effective, and user-outcome states. Define actionable ownership: application, platform capability, cluster, network, storage, provider, or dependency.

Autoscaling, rollout, and alert automation should consume signals designed for that action, not whichever metric exists. Control signals need bounded cardinality, freshness, availability, and resistance to feedback loops.

### Compose recurring workload patterns

**Stateless API:** Deployment, Service, optional Gateway route, immutable config, workload identity, requests/limits, zone spread, startup/liveness/readiness, drain, PDB, HPA, policies, and task SLOs. “Stateless” means any local loss is safe; sessions/idempotency/data still need external design.

**Queue worker:** Deployment or Job depending continuous versus finite ownership; no Service unless inbound control exists; queue identity, lease/idempotency, readiness for acquisition, drain/checkpoint, backlog/age scaling, dependency/concurrency cap, and outcome evidence.

**Scheduled task:** CronJob creates idempotent Jobs with concurrency/deadline/history/cleanup; durable task key prevents duplicate business effect; alerts distinguish missed trigger, failed Job, and wrong result.

**Stateful member:** StatefulSet, headless/member discovery where required, one governed PVC per identity, delayed topology binding, application replication/quorum/fencing, safe readiness/termination, controlled disruption, backup/restore, and no generic HPA without protocol support.

**Node capability:** DaemonSet with exact eligible-node affinity/toleration, least privilege/host access, resource reservations, priority appropriate to node function, rollout safety, and per-node health. Consumers tolerate temporary node-local capability absence.

**Accelerator service:** Deployment/Job, device resource and trusted node class, image/driver compatibility, queueing/batching, device-aware health, autoscaling plus node provisioning, quota, packing/spread policy, and utilization/task latency evidence.

### Record rejected primitives and exceptions

A decision record should state requirement/failure model, chosen composition, responsibility table, rejected alternatives, unsupported assumptions, owners, versions, validation, rollback/deletion, cost, and exceptions with expiry.

Rejection is positive architecture. “No PVC because outputs are durable in object storage,” “no Service because workers have no inbound clients,” and “no sidecar because a shared node agent satisfies telemetry” prevent later accidental complexity.

Exceptions identify the missing platform capability and risk. A privileged host agent, static credential, implementation-specific route, or singleton may be necessary, but its containment and removal path must be concrete.

Update decisions when application semantics or platform implementations change. A valid mapping for one driver/controller/version is not automatically portable.

### Validate the composition before production

Static validation checks schemas, selectors, ownership, resource fields, policy, images, references, class support, and incompatible combinations. Server-side/admission validation checks actual cluster policy. Controller dry runs do not prove external realization.

Conformance exercises start, update, roll back, scale up/down, lose dependency, exhaust resources, rotate config/credential, drain, preempt, kill node/zone, restore data, revoke access, and delete/clean up. Observe both resource state and representative user/task outcomes.

Capacity tests include rollout surge, failover, startup tails, dependency quotas, HPA metric lag, node provisioning, volume attach, and drain. Security tests attempt unauthorized API, network, secret, volume, node, and route access.

Deletion tests are mandatory: routes/DNS/load balancers, claims/volumes/snapshots, Secrets, identities, provider resources, backups, logs, and legal retention follow explicit order and owners.

### Turn mappings into platform capabilities

When a composition recurs, expose a versioned capability such as `web-service`, `queue-worker`, `scheduled-task`, `stateful-member`, or `node-agent`. The capability accepts intent, renders governed resources, reports conditions, and documents escape hatches.

Keep the API smaller than raw Kubernetes but not misleading. Consumers should state public/private, availability, data, scaling, security, and lifecycle intent. The platform validates implementation-specific constraints and supplies defaults with evidence.

Version capability behavior, generated labels/selectors, controller implementations, policies, and migrations. Preview changes against real applications; preserve ownership and rollback. Measure adoption, lead time, failure, support burden, and user outcome rather than resource count.

## Definitions and Notation

Let requirements be $R=\{r_1,\ldots,r_m\}$ and selected mechanisms be $K=\{k_1,\ldots,k_n\}$. Define a responsibility relation $k_j\models r_i$ only when mechanism $k_j$ has declared ownership, failure behavior, and evidence for requirement $r_i$.

Coverage requires

$$
\forall r_i\in R,\ \exists k_j\in K: k_j\models r_i,
$$

while minimal justification requires

$$
\forall k_j\in K,\ \exists r_i\in R: k_j\models r_i.
$$

These conditions do not prove adequacy: several mechanisms may need to compose, and a false guarantee can satisfy the relation only on paper. Let $B$ be boundary assumptions belonging to application/provider behavior; validation must test $K\cup B$ against scenarios $F$.

For an autoscaled component, let $c$ be useful capacity per ready replica and $d(t)$ incoming demand. A necessary but insufficient capacity condition is

$$
readyReplicas(t)\times c\ge d(t),
$$

with queueing, latency, dependency, topology, and failure constraints adding obligations.

## Mechanisms, Invariants, or Proof Structure

The mechanism is a traceable mapping workflow: elicit application contract; declare failures and evidence; select the primary controller; choose pod boundary; add networking, configuration, state, resources, placement, lifecycle, security, scaling, recovery, and observations only where required; record rejected alternatives; validate composition; productize recurrence.

The **controller invariant** ties interchangeability, identity, node scope, or completion to exactly one primary ownership model. The **boundary invariant** keeps application protocols—authorization, transactionality, quorum, fencing, idempotency, backup correctness—outside false Kubernetes guarantees.

The **minimality invariant** rejects primitives without a requirement. The **coverage invariant** gives every requirement an owner and evidence. The **composition invariant** verifies cross-resource selectors, references, identities, topology, lifecycle, and deletion rather than validating resources independently.

The **elasticity invariant** binds metrics to useful capacity and safe scale-down. The **security invariant** follows principals/data across API, runtime, network, storage, provider, and application. The **availability invariant** combines failure independence, capacity, readiness, disruption, data/dependency protocols, and recovery.

This is an assurance structure, not a proof that a composition meets its objectives. Implementations, versions, provider behavior, application code, demand, failure independence, and operations remain assumptions requiring conformance and production evidence.

## Alternatives and Trade-Offs

Raw manifests offer full Kubernetes control and low abstraction latency but expose every team to implementation drift and unsafe combinations. Platform capabilities improve consistency and support at the cost of API design, versioning, and escape-hatch governance.

One multi-purpose Deployment is simple initially but couples scale, rollout, privilege, failure, and resource policy. Separate components increase resources and coordination while preserving independent ownership and elasticity.

Self-managed stateful workloads provide control and portability but transfer protocol upgrades, backup, failover, and recovery to the team. Managed data services reduce some operational burden while adding network, provider, cost, residency, and portability constraints.

Sidecars provide per-pod context and fate; node agents reduce duplication; libraries reduce processes; external services centralize policy. Select from trust, language, scale, lifecycle, and failure rather than fashion.

HPA reacts to demand and improves efficiency but adds feedback delay and scale-down risk. Fixed capacity is predictable and supports instant failover at higher cost. Scheduled/predictive capacity can complement reactive scaling when demand is known.

Strict hard policy protects invariants but can leave workloads unavailable during capacity loss. Explicit degraded modes preserve selected functions without silently violating security, data, or identity constraints.

## Failure Modes and Misconceptions

- **“Kubernetes primitive selection is a best-practice checklist.”** It is a trace from workload semantics and failures to bounded controller responsibilities.
- **“Deployment means stateless.”** It expects interchangeable pods; the application must make local replacement safe.
- **“StatefulSet makes a database highly available.”** It supplies identity and ordered lifecycle, not replication, quorum, fencing, or backup.
- **“Every workload needs a Service.”** Only inbound discovery/reachability justifies one.
- **“One pod is the application boundary.”** It is the joint scheduling/fate unit; independently scaling components should usually split.
- **“PVC makes data safe.”** It persists beyond a pod under class/reclaim behavior; durability and recovery need separate protocols/evidence.
- **“NetworkPolicy secures the API.”** It constrains supported network paths; identity and application authorization remain.
- **“HPA solves overload.”** It may react too late and cannot exceed node, dependency, partition, or concurrency constraints.
- **“Readiness means user success.”** It is one traffic-eligibility signal; route, data plane, dependencies, and application result remain.
- **“PDB protects rollouts and outages.”** It governs cooperating eviction; workload update and involuntary failures have other controls.
- **“An operator is always more mature.”** A custom controller adds authority and lifecycle; use it only for recurring domain reconciliation that simpler APIs cannot express.
- **“More primitives mean more production readiness.”** Unjustified primitives add failure modes, cost, and deletion obligations.

## Worked Examples

### Example 1

A stateless API stores sessions in memory and loses them on rollout. The mapping was false: replicas were not interchangeable. Sessions move to signed/client or durable shared state before Deployment semantics are claimed.

### Example 2

A worker Deployment has a public LoadBalancer but accepts only queue work. Removing the route/Service reduces exposure and cost; egress identity, lease, drain, and queue-age scaling remain.

### Example 3

A database runs in StatefulSet with three PVCs in one zone. Stable identity works, but availability does not. Application replication, fencing, independent-zone placement, backup/export, and restore tests complete the contract.

### Example 4

A log agent runs as a 50-replica Deployment and misses new nodes. DaemonSet expresses one eligible-node instance, with host privileges narrowed and node rollout tested.

### Example 5

A CronJob sends invoices twice after controller delay/retry. A durable billing-period key and transactional outbox make the business effect idempotent; schedule time was never exactly-once.

### Example 6

An I/O-bound worker scales on CPU and backlog grows. Queue age plus effective ready-worker capacity becomes the signal, bounded by database concurrency and checkpoint-safe scale-down.

### Example 7

A sidecar image scanner doubles every pod's CPU and blocks startup though it can scan registry artifacts centrally. The platform moves it to the artifact admission pipeline and removes per-pod coupling.

### Example 8

A mutable ConfigMap reload changes all replicas simultaneously. Immutable digest-bound configuration and canary rollout restore version identity and rollback.

### Example 9

A PDB allows one disruption, but a two-replica service loses both to one zone. Topology, failover headroom, readiness, and dependency redundancy—not a stricter PDB alone—repair availability.

### Example 10

A custom operator only creates a Deployment, Service, and ConfigMap. A versioned platform template/capability supplies the recurring composition without a new privileged reconciliation controller.

## Cross-Program Connections

Software architecture contributes boundaries, coupling, cohesion, interfaces, and decision records. Distributed systems contributes identity, replication, quorum, leases, retries, idempotency, and partial failure. Security contributes principals, threat boundaries, least privilege, supply chain, and authorization.

Reliability contributes objectives, capacity, overload, disruption, rollback, recovery, and failure testing. Data engineering contributes authoritative state, retention, lineage, backup, and restore. API engineering contributes protocols, routing, versioning, timeouts, and client behavior.

Product management contributes user/job outcomes and capability APIs. Finance contributes resource, provider, transfer, idle headroom, and operational cost. Platform engineering integrates these into paved paths while keeping responsibility and evidence visible.

## References

- Kubernetes Project, [*Workload Management*](https://kubernetes.io/docs/concepts/workloads/controllers/), current documentation retrieved September 2, 2026. Controller overview and Deployment, StatefulSet, DaemonSet, Job, and CronJob fit.
- Kubernetes Project, [*Deployments*](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/), current documentation retrieved September 2, 2026. ReplicaSets, desired replicas, rolling update, surge/unavailable, progress, pause, revision, and rollback.
- Kubernetes Project, [*StatefulSets*](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/), current documentation retrieved September 2, 2026. Stable ordinal/network/storage identity, governing Service, claim templates, ordered/parallel management, updates, and retention.
- Kubernetes Project, [*DaemonSet*](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/), current documentation retrieved September 2, 2026. Eligible-node pods, node-local uses, scheduling, updates, priority, and alternatives.
- Kubernetes Project, [*Jobs*](https://kubernetes.io/docs/concepts/workloads/controllers/job/), current documentation retrieved September 2, 2026. Completion, parallelism, indexed work, retry/backoff, failure policy, deadlines, tracking, and cleanup.
- Kubernetes Project, [*CronJob*](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/), current documentation retrieved September 2, 2026. Scheduled Job creation, concurrency, deadlines, suspension, time zones, history, and approximate scheduling semantics.
- Kubernetes Project, [*Service*](https://kubernetes.io/docs/concepts/services-networking/service/), current documentation retrieved September 2, 2026. Stable discovery, selectors, ports, headless Services, types, EndpointSlices, and external exposure.
- Kubernetes Project, [*Gateway API*](https://kubernetes.io/docs/concepts/services-networking/gateway/), current documentation retrieved September 2, 2026. Add-on API family, role-oriented ownership, infrastructure provisioning, listeners/routes, and advanced traffic routing.
- Kubernetes Project, [*ConfigMaps*](https://kubernetes.io/docs/concepts/configuration/configmap/), current documentation retrieved September 2, 2026. Nonconfidential configuration, data forms, delivery, namespace/size, immutable objects, and update behavior.
- Kubernetes Project, [*Persistent Volumes*](https://kubernetes.io/docs/concepts/storage/persistent-volumes/), current documentation retrieved September 2, 2026. PV/PVC lifecycle, binding, modes, class/topology, reclaim, expansion, snapshot, clone, and data sources.
- Kubernetes Project, [*Horizontal Pod Autoscaling*](https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/), current documentation retrieved September 2, 2026. Scaling targets, metrics, proportional algorithm, missing/not-ready behavior, multiple metrics, stabilization, and policies.
- Kubernetes Project, [*Application Security Checklist*](https://kubernetes.io/docs/concepts/security/application-security-checklist/), current documentation retrieved September 2, 2026. Workload security context, ServiceAccounts/RBAC, Secrets, NetworkPolicy, images, dependencies, runtime classes, and application controls.

## Exercises

### Exercise 1

Map an online marketplace containing public web/API, payment worker, catalog database, image processor, node log agent, nightly settlement, and schema migration. State controllers, pod boundaries, networking, configuration, state, security, placement, lifecycle, scaling, recovery, evidence, and rejected primitives.

### Exercise 2

Audit a “production template” that always generates Deployment, ClusterIP Service, public Ingress, PVC, ConfigMap, Secret, HPA on CPU, PDB, broad NetworkPolicy, and telemetry sidecar for every component.

### Exercise 3

An HPA target has 6 ready replicas, current queue-age metric 90 seconds, desired 30 seconds, and a proportional decision with no other constraints. Compute the basic desired replica count. Then explain at least six reasons the actual safe decision may differ.

### Exercise 4

Diagnose a stateful API that cannot roll out: it uses a one-replica Deployment, RWO PVC, hard hostname anti-affinity, `maxUnavailable: 0`, no surge capacity, PDB `minAvailable: 1`, 10-minute startup, and a public route. Decide whether to repair the composition or application architecture.

### Exercise 5

Transfer the mapping method to a university research laboratory automating experiments with instruments, scheduled calibration, streaming sensors, analysis jobs, protected datasets, and human safety review. Identify orchestration primitives, domain protocols, evidence, and boundaries automation must not cross.

## Answers to the Exercises

### Answer 1

Public web/API uses separate Deployments if scale/resource/release differs, ClusterIP Services, Gateway routes, workload identity, zone spread, probes/drain/PDB, HPA on concurrency/latency, and user-task evidence. Payment workers use a Deployment with no inbound Service, queue leases/idempotency, exact egress/identity, backlog-age scaling, checkpoint drain, and downstream concurrency cap. Catalog database uses a managed capability or mature operator/StatefulSet only with member identity, per-member storage, quorum/fencing, backup/restore, topology, and controlled updates. Image processors use queue workers or Jobs depending finite ownership, object storage rather than local PVC, device/resource classes, and task evidence. Node log agents use a least-privileged DaemonSet with bounded host access and per-node rollout. Nightly settlement uses CronJob-to-idempotent Job with durable period key, concurrency/deadline, and business reconciliation. Schema migration uses a separately authorized idempotent Job coordinated with compatible application versions, never an app-container PostStart. Reject public routes for workers/agents/jobs, PVCs for object-backed processors, one shared pod, static shared credentials, and universal CPU scaling.

### Answer 2

The template confuses resource presence with readiness. Deployment fits only interchangeable continuous pods; finite, node-local, or identity-bound work needs other controllers. A Service requires inbound consumers, public routing requires an owned exposure/security contract, and PVC requires authoritative filesystem/block lifetime. ConfigMap/Secret are separate classifications and may be unnecessary or externally sourced. CPU HPA requires correlation with useful demand/capacity and safe scale-down; some targets cannot or should not scale horizontally. PDB needs real replicas/readiness/topology and only governs eviction. “Broad” NetworkPolicy may expose too much or block nothing if unsupported; derive exact ingress/egress plus application auth. A telemetry sidecar is justified only by joint fate/context; library, node agent, or platform pipeline may be safer. Replace universal generation with workload-class intent, minimal resources, explicit exceptions, and conformance/deletion tests.

### Answer 3

The basic formula gives $\lceil6\times90/30\rceil=18$ replicas. Actual safe behavior can differ because tolerance may suppress small changes; multiple metrics choose another recommendation; missing/not-ready metrics adjust direction; scale-up policies cap rate; stabilization uses prior recommendations; max replicas caps result; only ready/effective workers should define capacity; metric age/aggregation may lag; queue age may reflect one poisoned item; startup and node provisioning delay response; database/queue quotas may make 18 unsafe; work partitions may cap useful concurrency; zone/device/storage capacity may not exist; and scale-down/checkpoint policy affects later behavior. Load-test the closed loop and expose constrained reasons rather than treating 18 as guaranteed capacity.

### Answer 4

The composition contains contradictions. A one-replica Deployment with an RWO claim is not truly interchangeable; hard hostname anti-affinity is irrelevant with one current replica but blocks surge co-location, while no surge and `maxUnavailable: 0` permit no replacement step. PDB `minAvailable: 1` blocks cooperating eviction and cannot create capacity. Ten-minute startup extends any transition; the public route preserves user impact. First decide data/session semantics. If local state can move to a managed/shared durable service, make pods interchangeable, remove the PVC, add at least two zone-spread replicas/capacity, meaningful readiness, surge, drain, PDB, and rollback. If stable identity is real, use StatefulSet/operator or external managed service with per-member storage, replication/quorum/fencing, controlled member update, backup/restore, and possibly a read/write routing model. Do not merely force delete, weaken PDB, or switch RWO access to clear rollout.

### Answer 5

Continuously running interchangeable gateways/stream processors map to Deployments and internal Services; node/instrument-local adapters may map to carefully privileged DaemonSets or edge agents; finite analyses use Jobs; calibration schedules create idempotent Jobs; identity-bound local collectors may need StatefulSet-like stable storage only if platform connectivity and recovery justify it. Durable experiment/session IDs, instrument locks/fencing, calibration lineage, sample custody, schema, checksums, protected object/database storage, retention, and reproducible analysis are domain protocols—not controller guarantees. Configuration and credentials are signed/versioned and scoped; safety interlocks remain hardware/local and fail-safe. Placement respects instrument location, hazardous zones, devices, and data residency. Evidence links proposal approval, instrument/calibration version, raw data, commands, operator, analysis artifact, failures, and deletion. Automation may schedule approved operations and stop safely, but cannot waive ethics, biosafety, radiation/chemical controls, equipment limits, consent, or a human emergency stop; designated researchers and safety officers retain authority under audit.
