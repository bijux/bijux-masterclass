---
module_id: PLAT-028
program: Platform Engineering
level: 1
module_number: 28
title: Scheduling and Placement
status: complete
last_verified: 2026-09-02
---

# Scheduling and Placement

## One-Page Review

### Governing question

How should a platform place workloads onto nodes so that feasibility, availability, performance, isolation, locality, priority, cost, and recovery remain explicit under changing capacity and failures?

### Essential definitions

- **scheduling** assigns an unscheduled pod to a node; kubelet and other components then attempt admission and startup on that node.
- A **feasible node** satisfies every active hard filter for a pod at the scheduler's evaluated cluster state.
- **scoring** ranks feasible nodes using weighted preferences; it cannot make an infeasible node eligible.
- A **resource request** is declared demand used for scheduling and some runtime/resource-pressure behavior; observed idle usage does not erase that reservation.
- **allocatable** is the node capacity available for pods after system reservations and other constraints.
- `nodeSelector` and required **node affinity** constrain eligible nodes by labels; preferred node affinity influences scoring.
- **inter-pod affinity/anti-affinity** attracts or repels a pod relative to selected existing pods in a topology domain.
- A **topology spread constraint** controls skew of selected pods across eligible labeled domains such as zones or hosts.
- A **taint** marks a node with an effect; a matching **toleration** allows a pod past that repulsion but does not select or reserve the node.
- A **PriorityClass** maps a name to scheduling priority and optionally prevents that class from preempting lower-priority pods.
- **preemption** nominates/removes lower-priority pods so a higher-priority pending pod may fit; **eviction** is pod termination initiated by another control path.
- A **scheduling gate** keeps a newly created pod out of normal scheduling consideration until all declared gates are removed.

### Central model, mechanism, or theorem

Model placement intent as $P=(R,H,T,A,S,Q,F,C,O,L,X)$: resource demand $R$, hard eligibility $H$, taints/tolerations $T$, workload affinity $A$, spread/locality $S$, scoring preferences $Q$, failure-domain model $F$, capacity and priority policy $C$, observations $O$, lifecycle/rebalancing $L$, and declared exceptions $X$. For pod $p$ and node $n$, feasibility is the conjunction $F(p,n)=R\land H\land T\land V\land K\land Z\land G$, including resource fit, labels/affinity, taints, volume reachability, ports/device/plugin constraints, topology, and active scheduler gates/policies. Only after $F(p,n)$ is true may a score choose among nodes. Placement at time $t$ does not prove that constraints remain balanced or that the workload becomes ready.

### Critical invariants

- Requests represent defensible peak or protected demand for every container, init behavior, pod overhead, local ephemeral storage, and extended resource relevant to placement.
- Hard constraints encode true correctness, compliance, hardware, security, and reachability requirements; preferences encode optimization that may yield under scarcity.
- Node labels used for isolation or compliance are set by trusted automation and protected from unauthorized kubelet mutation.
- `nodeName` is not used as ordinary placement policy because it bypasses scheduler feasibility, topology, volume binding, and scoring.
- A toleration is paired with positive affinity when workloads must use a dedicated pool; toleration alone permits spillover to any otherwise feasible node.
- Spread selectors match the incoming workload, topology labels exist on all intended nodes, and `maxSkew`, `minDomains`, eligibility, and unsatisfiable behavior reflect the failure model.
- Replica placement counts independent failure domains and sufficient capacity, not merely distinct pod or node names.
- Priority is scarce policy governed by quota; preemption is not autoscaling, guaranteed admission, disruption safety, or a substitute for capacity.
- Scheduling, kubelet admission, image/volume/network startup, readiness, and application service are observed as distinct stages.
- Placement drift from deletion, failure, autoscaling, or changing labels is detected; rebalancing is intentional and disruption-aware rather than assumed automatic.

### Common failures

Omitting requests; setting requests from averages; using hard constraints for preferences; selecting mutable or spoofable labels; pinning with `nodeName`; assuming toleration attracts; combining broad tolerations with no affinity; using hostname anti-affinity for every replica at large scale; writing spread selectors that do not match the pod; ignoring missing topology labels or scale-to-zero domains; requiring more domains than capacity can provide; treating preferred rules as guarantees; confusing RWO storage with placement; assigning high priority to every service; assuming PDB prevents preemption; expecting preemption to make an impossible pod fit; and debugging Pending pods by adding capacity before reading failed filters.

### Compact example

A four-replica payments API requests measured CPU/memory plus sidecar and pod overhead, requires an attested general-compute pool and a region, tolerates only that pool's taint, and prefers lower-carbon nodes. Hard zone spread uses `maxSkew: 1`, `minDomains: 3`, and a selector matching the Deployment revision; host spread is a soft preference. The storage class delays binding so scheduler and CSI select compatible topology. A governed service-critical priority may preempt lower-tier batch work, but three-zone headroom and autoscaling provide routine capacity. Status separates scheduling queue time, failed filters, nominated node, binding, kubelet admission, volume attach, container start, readiness, and task success. A disruption-aware rebalancer may correct drift after node repair; the scheduler does not move already bound pods automatically.

### Connections

Retrieve resource and runtime controls from [PLAT-022](022-runtime-isolation-and-resource-controls.md), declarative objects from [PLAT-023](023-kubernetes-declarative-resources.md), controller/disruption behavior from [PLAT-024](024-pods-workloads-and-controllers.md), endpoint/locality effects from [PLAT-025](025-services-and-ingress.md), and volume topology/fencing from [PLAT-027](027-storage-and-stateful-workloads.md). Capacity, reliability, distributed-systems, security, performance, and finance programs supply the models behind policy choices.

## Governing Question

Which nodes may run a workload, which nodes should be preferred, what declared resources and failure domains make that placement safe, and how will the platform explain Pending, preempted, evicted, imbalanced, or underperforming outcomes as the cluster changes?

Scheduling is a constrained decision over a snapshot of declared state. It is neither continuous optimization nor proof of runtime success. The scheduler can bind a pod to a feasible node; kubelet can later reject or evict it, a volume can fail to attach, an image can fail to pull, a topology can lose a domain, or the application can remain unready.

Platform engineers therefore design placement as a product contract spanning workload declarations, trusted node facts, scheduler configuration, capacity pools, autoscaling, storage and devices, priority, disruption, observation, and rebalancing.

## Why This Matters

Placement determines which failures take replicas down together, which data paths cross zones, which workloads interfere, which devices and licenses are consumed, and which tenants share hardware. A technically schedulable placement can violate availability, latency, security, sovereignty, or cost goals.

Overconstraint is equally dangerous. One nonexistent label, unavailable zone, contradictory affinity, unbound local volume, or oversized request can keep every replica Pending. Hard anti-affinity can block upgrades because old and new revisions temporarily coexist. Priority can evict useful work yet still fail to admit the preemptor.

A governed platform makes common intent easy—general compute, zonal stateful, accelerators, isolated tenants, latency-sensitive services, interruptible batch—and prevents consumers from assembling fragile combinations of raw fields.

## Prerequisites and Retrieval

Retrieve bin packing, multidimensional capacity, queues, constraints, optimization, graph relationships, labels/selectors, taints, failure domains, replicas, quorum, resource requests/limits, CPU/memory/storage/devices, pods, nodes, controllers, volumes, autoscaling, disruption, preemption, eviction, latency, and cost.

You should distinguish feasibility from preference, scheduler reservation from runtime use, node capacity from allocatable, availability from balance, a toleration from attraction, placement from admission/startup, and preemption from node-pressure eviction or API-initiated disruption.

## Learning Objectives

After completing this module, you should be able to:

1. explain scheduler queueing, filtering, scoring, reservation, permit, binding, and post-binding boundaries;
2. derive honest pod requests and evaluate fit against allocatable resources, pod overhead, volumes, ports, and devices;
3. compose node selectors, required/preferred affinity, inter-pod affinity, anti-affinity, taints, and tolerations;
4. design topology spread constraints with correct selectors, eligible domains, skew, minimum domains, and failure behavior;
5. coordinate scheduler placement with storage topology, extended resources, runtime classes, and autoscaling;
6. govern PriorityClasses, preemption, scheduling gates, and disruption interactions;
7. detect and correct placement drift without unsafe or wasteful churn; and
8. diagnose unschedulable, preempted, evicted, and poorly placed workloads from layered evidence.

## Core Exposition

### Begin with placement intent, not YAML fields

For every workload, record replicas, startup and steady resource demand, scaling range, statefulness, storage/device/network dependencies, failure tolerance, latency/locality, security/isolation, residency, disruption tolerance, priority, cost, and expected queue time.

Classify each rule as correctness or optimization. A confidential workload requiring attested nodes is hard. Keeping ordinary API pods near caches may be soft. Spreading quorum voters across zones is hard if zone loss is in scope; spreading stateless replicas across hosts may be soft when emergency packing preserves service.

Every hard rule consumes placement freedom. Test the intersection against current and scale-to-zero capacity, rollout surge, maintenance, zone loss, and autoscaler capabilities before shipping it.

### Understand the scheduler cycle

The default scheduler watches pods without an assigned node. Queue sorting selects work. Pre-filter and filter plugins eliminate nodes that cannot satisfy the pod. If no feasible node remains, the pod stays Pending/unschedulable and is retried when relevant state changes or backoff expires.

Scoring plugins rank feasible nodes. Scores may reflect resource balance or packing, affinity, topology spread, image locality, volume binding, or configured extensions. Highest combined score wins, with tie handling; a high score never overrides a failed filter.

The scheduling framework exposes extension points including queue sort, pre-filter, filter, post-filter, pre-score, score, normalize, reserve, permit, pre-bind, bind, and post-bind. Reserve/permit operations participate in assumptions and coordination before binding. A bind writes node assignment to the API; kubelet then owns node-side admission and startup.

Custom profiles or schedulers are powerful control-plane code. They can block, misplace, starve, or compromise workloads. Prefer built-in declarative primitives unless a proven requirement cannot be expressed, and version, secure, observe, load-test, and roll back every scheduler change.

### Calculate resource fit from declared requests

For ordinary app containers, pod CPU and memory requests aggregate across containers that may run together. Effective init-container calculation, restartable sidecars, pod overhead from RuntimeClass, local ephemeral storage, huge pages, device/extended resources, host ports, volume attach limits, and node-specific plugins can add constraints.

The scheduler compares declared demand with node allocatable minus requests already assigned, not with momentary utilization. This protects capacity for later peaks but makes underrequested workloads appear cheap and overrequested workloads strand capacity.

For resource $r$ on node $n$, a simplified fit condition is

$$
request_p(r) \le allocatable_n(r)-\sum_{q\in assigned(n)}request_q(r).
$$

Real feasibility also includes pod-count, devices, ports, volumes, topology, policies, and plugin state.

Derive requests from load tests and production distributions under expected concurrency and failure. Include startup, compaction, recovery, sidecars, and failover. Use recommendations and vertical tuning as reviewed inputs, not silent changes that invalidate capacity plans.

### Keep requests, limits, and observed use distinct

CPU request influences scheduling and contention weight; CPU limit throttles. Memory request influences scheduling and node-pressure behavior; memory limit can lead to OOM termination. A pod may use above request when spare capacity exists, so aggregate requested capacity and observed use answer different questions.

No request or a tiny request improves apparent packing while creating interference and eviction risk. Request equal to a rare worst case can make capacity unaffordable. Platform classes should define protected service levels, headroom, overcommit policy, and measurement/adjustment windows.

QoS class, priority, request overage, and node pressure interact during kubelet eviction but are not interchangeable. A pod scheduled successfully can later be evicted because node memory, disk, inodes, or process IDs are scarce.

### Use selectors and node affinity for node facts

`nodeSelector` requires all listed label equalities. Required node affinity supports expressions and multiple terms: expressions inside one term are ANDed; required terms are ORed. If both `nodeSelector` and node affinity exist, both must pass.

Preferred node-affinity terms add weighted scores when they match. They are optimization, not fallback ordering or guarantees. A preferred rule can lose to other scoring plugins or disappear when only nonpreferred feasible nodes exist.

Use stable, qualified label keys owned by platform automation: architecture, operating system, accelerator family, pool, isolation class, topology, regulatory boundary, or attestation status. Avoid pinning to mutable node names, transient health, image presence, or human labels.

Labels used for security/isolation must be protected by Node authorizer/NodeRestriction or equivalent trusted admission and provisioning. A compromised kubelet must not self-label into a protected workload pool.

### Avoid direct node assignment

Setting `spec.nodeName` bypasses ordinary scheduler filtering, scoring, delayed volume binding, taints with `NoSchedule`, and profile policy. Kubelet may still reject or evict the pod, and a nonexistent node can leave it stuck.

Use `nodeSelector` or affinity to constrain without bypassing the scheduler. Direct binding is reserved for specialized trusted control paths that explicitly reproduce feasibility, authorization, storage, and lifecycle guarantees.

Static pods and DaemonSets have separate management purposes; they do not justify ordinary application pinning. Stable workload identity should come from controllers and storage/service abstractions, not a node name.

### Compose taints and tolerations correctly

A node taint has key, optional value, and effect. `NoSchedule` blocks new pods without a matching toleration. `PreferNoSchedule` is a soft repulsion. `NoExecute` also evicts already running pods lacking tolerance; `tolerationSeconds` can allow bounded continued residence after a matching `NoExecute` taint.

Evaluation begins with node taints and ignores those matched by tolerations; remaining effects decide repulsion. A toleration does not say “place me here.” For a dedicated pool, combine its taint with required node affinity or selector so dedicated workloads land there and ordinary workloads stay out.

Broad `Exists` tolerations can admit a workload to hardware, control-plane, unhealthy, or tenant-isolated nodes unintentionally. Platform admission should limit tolerated keys/effects and couple them to approved workload classes.

Automatic taints for node conditions participate in scheduling and eviction. Distinguish operational condition taints from intentional tenancy/capability taints, and test temporary control-plane/network partitions before choosing `NoExecute` tolerance durations.

### Use inter-pod affinity for relationships sparingly

Pod affinity selects topology domains containing matching pods; anti-affinity excludes or disfavors domains containing them. Required rules filter; preferred rules score. Namespace selection and topology key define relationship scope.

Use affinity for a real dependency such as co-locating a helper with a data shard or keeping a cache near consumers. Use anti-affinity for strict separation when a domain failure would violate the contract. For general even distribution, topology spread is clearer and often scales better.

Selectors must describe durable workload identity, not ephemeral readiness or controller-generated accidents. Required self-affinity can deadlock initial placement unless the scheduler's special first-pod behavior applies exactly; avoid designs whose bootstrap depends on an existing selected peer.

Inter-pod rules require examining other pods across topology and can be expensive in large clusters. Bound their namespace/selector scope and load-test high-cardinality or densely connected policies.

### Design topology spread from the failure model

A spread constraint selects pods to count, a node topology label, `maxSkew`, optional `minDomains`, and `whenUnsatisfiable`. Eligible domains depend on node affinity and taint inclusion policy. All constraints on a pod are combined, so a zone rule and host rule must both permit a node.

For eligible domain counts $c_1,\ldots,c_k$ and global minimum $m$, candidate skew is compared with

$$
skew_i=c_i-m.
$$

With hard `DoNotSchedule`, a candidate cannot cause skew beyond `maxSkew`. When eligible domains are fewer than `minDomains`, the global minimum becomes zero under the documented semantics, which can intentionally block unsafe concentration.

`ScheduleAnyway` is a scoring preference to reduce skew, not a maintained invariant. Hard spread protects availability but can block replicas during zone loss or rollout. Choose whether preserving replica count or domain separation wins under degraded capacity, and provide enough headroom for that decision.

The label selector should match the incoming pod. Otherwise “ghost” pods do not count themselves and concentration can grow. Every intended node must carry the topology key. Scale-to-zero node groups may make domains invisible unless the autoscaler has independent topology knowledge.

### Inspect feasibility as a conjunction

The following synthetic inventory shows why free CPU alone does not establish a feasible node.

<!-- bijux-verify: {"id":"placement-feasibility-inventory","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"nodes=8\nresource_fit=6\nlabel_fit=5\ntaint_fit=5\nvolume_fit=4\nfeasible=3\nzones=3\n","stderr":""}} -->
```python
nodes = [
    {"name": "n1", "cpu_free": 6, "label": True,  "tainted": False, "volume": True,  "zone": "a"},
    {"name": "n2", "cpu_free": 5, "label": True,  "tainted": False, "volume": True,  "zone": "b"},
    {"name": "n3", "cpu_free": 8, "label": True,  "tainted": False, "volume": False, "zone": "c"},
    {"name": "n4", "cpu_free": 3, "label": False, "tainted": False, "volume": False, "zone": "a"},
    {"name": "n5", "cpu_free": 10,"label": False, "tainted": True,  "volume": False, "zone": "a"},
    {"name": "n6", "cpu_free": 7, "label": True,  "tainted": True,  "volume": True,  "zone": "b"},
    {"name": "n7", "cpu_free": 4, "label": True,  "tainted": False, "volume": True,  "zone": "c"},
    {"name": "n8", "cpu_free": 2, "label": False, "tainted": True,  "volume": False, "zone": "c"},
]
resource_fit = lambda node: node["cpu_free"] >= 4
label_fit = lambda node: node["label"]
taint_fit = lambda node: not node["tainted"]
volume_fit = lambda node: node["volume"]
feasible = lambda node: resource_fit(node) and label_fit(node) and taint_fit(node) and volume_fit(node)
print(f"nodes={len(nodes)}")
print(f"resource_fit={sum(resource_fit(node) for node in nodes)}")
print(f"label_fit={sum(label_fit(node) for node in nodes)}")
print(f"taint_fit={sum(taint_fit(node) for node in nodes)}")
print(f"volume_fit={sum(volume_fit(node) for node in nodes)}")
print(f"feasible={sum(feasible(node) for node in nodes)}")
print(f"zones={len({node['zone'] for node in nodes})}")
```

The fixture is a design classifier, not evidence of scheduler plugin behavior, real allocatable capacity, volume attachment, topology safety, runtime admission, or application readiness.

### Coordinate storage with scheduling

Topology-constrained volumes add filters for existing PV node affinity, CSI topology, storage capacity, attach limits, and multi-attach rules. A pod with several claims needs one node compatible with all of them.

StorageClasses using `WaitForFirstConsumer` let the scheduler consider the pod's constraints before provisioning/binding. `nodeName` defeats that coordination. Immediate binding can strand a zonal volume away from otherwise required hardware.

Data locality is not merely a score when the volume cannot attach elsewhere. For replicated databases, solve application replica topology and each member's volume topology together. Never resolve a Pending pod by changing claim or node affinity without confirming data identity and fencing.

### Place accelerators and specialized resources

Device plugins advertise extended resources such as GPUs; requests are integer and normally cannot be overcommitted by the core mechanism. Node labels and affinity select model, memory, interconnect, driver, feature, or licensing constraints. RuntimeClass and pod overhead may add node/runtime requirements.

One generic `gpu=true` label is insufficient when device generations, drivers, partitioning, topology, health, and workload compatibility differ. Publish governed accelerator classes with validated images, drivers, resource names, node features, quotas, sharing policy, and failure behavior.

Dynamic Resource Allocation or other evolving APIs can coordinate richer claims and device configuration when supported. Treat feature maturity and driver compatibility as versioned platform contracts rather than portable defaults.

Pack scarce devices to free whole nodes when workload concurrency and interference permit; spread latency-sensitive or fault-tolerant jobs when contention/failure requires. Measure device utilization, memory, topology transfers, queue time, and job outcome—not only allocated count.

### Use priority as an admission and recovery policy

Priority orders queued pods and influences preemption and node-pressure eviction. A higher-priority pod that cannot schedule may trigger removal of lower-priority victims if their removal makes some node feasible. It cannot fix a missing label, incompatible volume, unavailable device, or hard topology contradiction.

PriorityClass is cluster-scoped and can be abused for denial of service. Offer a small semantic ladder tied to business/recovery roles, govern it with admission and ResourceQuota, and keep built-in system-critical classes for actual control-plane components.

Preemption respects PodDisruptionBudget on a best-effort basis when choosing victims; it may violate a PDB if no alternative exists. Victims take termination time, capacity can be claimed by another pod, and the preemptor can remain Pending. Observe nomination, victims, grace, and eventual binding separately.

Non-preempting priority (`preemptionPolicy: Never`) moves urgent work ahead in the queue without killing lower-priority work; it waits for capacity naturally. This suits expensive checkpointless jobs or governance that values queue order but forbids collateral disruption.

### Delay scheduling until dependencies are known

Scheduling gates allow admission or another trusted controller to create a pod in `SchedulingGated` state. Gates can be removed after required placement inputs exist; new gates cannot be added after creation. While gated, the scheduler avoids repeated futile attempts and autoscaler churn.

Gates do not reserve capacity, volumes, devices, or node identity. When the last gate is removed, normal feasibility uses current state. Gate controllers need ownership, timeouts, failure status, garbage collection, and authorization; an abandoned gate can hold pods indefinitely.

Use gates for external resource preparation or cohort coordination only when the workflow truly needs it. Do not hide ordinary missing configuration or capacity behind a gate.

### Coordinate with autoscaling and provisioning

Pending pods are demand signals only if an autoscaler can map constraints to a node group it may create. Unsupported labels, impossible combinations, quotas, maximum pool size, unavailable zones, provider capacity, or daemon/pod overhead can prevent scale-up.

Model the full node template: allocatable after system/DaemonSets, taints, labels, devices, architecture, topology, max pods, volumes, and startup time. A nominal 8-CPU instance does not fit two 4-CPU pods if overhead consumes capacity.

Scale-to-zero removes live nodes and potentially topology domains from scheduler observation. Autoscaler configuration must retain template and domain knowledge. Hard `minDomains` plus unavailable provider zones can intentionally keep pods Pending; surface that cause rather than weakening availability silently.

Autoscaling reacts after demand; critical services need existing headroom for failover, rollout, and node loss. Preemption can bridge short pressure but should not be the normal capacity strategy.

### Detect placement drift and rebalance deliberately

The scheduler selects a node once. It does not continuously move bound pods when better nodes arrive, topology becomes imbalanced, affinity preferences change, or taints/labels drift. Required `IgnoredDuringExecution` affinity normally does not evict a pod after labels change.

Controllers replace failed pods, which can gradually rebalance, but scale-down may remove arbitrary replicas and worsen skew. A descheduler or operator can evict pods that violate current strategy or could be better placed, subject to policy and support.

Rebalancing is disruption. Respect availability, PDBs, stateful leadership, volume movement, cache warmup, termination, surge, priority, and cost. Rate-limit and canary policy changes. Sometimes accepting temporary skew is safer than churn.

Continuously validate trusted node labels, taints, topology completeness, pool capacity, and actual distribution. Placement conformance should include both desired rules and service outcome.

### Design dedicated and isolated pools

Dedicated pools combine trusted labels, taints, workload affinity, admission, identity, runtime isolation, network/storage policy, and capacity ownership. A taint alone prevents ordinary placement but does not provide a security boundary against privileged control-plane actors or compromised nodes.

Separate pools for untrusted build jobs, regulated data, accelerators, latency-sensitive services, or control-plane components when threat, interference, compliance, or lifecycle warrants. Excessive pools fragment capacity and increase cost; use stronger runtime isolation or scheduling profiles where they meet the requirement more efficiently.

Define spill behavior explicitly. Hard isolation may leave work Pending. Soft preference may mix tenants during scarcity. A break-glass exception needs authorization, expiry, observation, and reversal; it must not become a permanent broad toleration.

### Observe placement as a sequence

Measure created-to-queued, gated duration, scheduling attempts, filter failures, scoring/binding latency, nominated node, preemption time, bind-to-kubelet observation, admission, sandbox, volume attach/mount, image pull, container start, readiness, and task success.

Scheduler events summarize reasons such as insufficient resources, affinity mismatch, untolerated taint, topology spread, volume conflict, or port conflict. Events are bounded/aggregated evidence; correlate with scheduler metrics/logs, pod spec, node state, PVCs, priority, autoscaler decisions, and controller revisions.

Report requested versus allocatable capacity by resource, feasible node count per workload class, Pending age/reason, queue fairness, preemption/victims, evictions, spread skew, co-failure exposure, pool fragmentation, device allocation/utilization, cross-zone traffic, and cost.

Do not label every Pending pod a capacity shortage. Classify hard-policy, missing dependency, topology, quota, device, storage, taint, and resource causes separately.

### Diagnose Pending and placement failures systematically

Start with the immutable pod spec actually created, its scheduler name, scheduling gates, condition and events. Separate `SchedulingGated`, unschedulable, nominated/preempting, bound but not admitted, and running but unready states.

For unschedulable pods, enumerate failed filters rather than editing blindly: requests versus allocatable/requested; node selectors and required terms; taints/tolerations; spread selector/domains/skew; pod affinity/anti-affinity; PVC binding/topology/attach limit; host ports; devices; quotas; and scheduler profile/plugin status.

Find the intersection. Ten nodes with CPU, five with the label, four without the taint, and three with volume access may yield zero common nodes. The executable inventory illustrates why independent counts mislead.

If preemption says no victims help, identify the remaining nonresource filter. If autoscaler does not act, compare pod constraints with node-group templates and limits. If bound but startup fails, switch from scheduler evidence to kubelet, runtime, CNI, CSI, image, and application evidence.

Never remove hard security/topology constraints, add wildcard tolerations, lower requests, change a PVC, or grant high priority merely to clear Pending status. Change the contract only with evidence that the requirement was wrong.

### Govern placement as platform products

Publish workload classes that combine default requests policy, RuntimeClass, node pools, trusted labels, taints/tolerations, affinity, topology spread, priority, storage/device support, quotas, autoscaling, disruption, observability, and cost.

Validate combinations at admission and in conformance clusters. Simulate steady state, rollout surge, node drain, zone loss, pool scale-to-zero, provider capacity shortage, device failure, storage topology, and priority pressure. Test scheduler upgrades and profile changes with representative pod populations.

Provide consumer diagnostics that explain which requirement failed and which team owns it. The safest platform API expresses intent such as `availability: zone-redundant` or `compute: gpu-large` and renders reviewed primitives, while still exposing enough status for expert diagnosis.

## Definitions and Notation

Let $N$ be current nodes and $C_p(n)$ be the conjunction of hard constraints for pod $p$ on node $n$. The feasible set is

$$
N_p^*=\{n\in N\mid C_p(n)=\text{true}\}.
$$

If $N_p^*=\varnothing$, scoring weights are irrelevant. Otherwise the scheduler chooses a node approximating

$$
n^*\in\operatorname*{arg\,max}_{n\in N_p^*}\sum_j w_j s_j(p,n),
$$

subject to implementation, sampling, tie, reservation, and concurrent-state behavior.

For resource vector $\mathbf r_p$ and node free-request vector $\mathbf f_n$, componentwise resource fit requires $\mathbf r_p\preceq\mathbf f_n$. It does not imply port, device, volume, label, taint, or topology fit.

For topology domain counts $c_d$ over eligible domains $D$, define observed spread

$$
Skew=\max_{d\in D}c_d-\min_{d\in D}c_d,
$$

while Kubernetes candidate calculations use the configured global-minimum and `minDomains` rules. Observed skew after deletions is not automatically repaired.

## Mechanisms, Invariants, or Proof Structure

The mechanism is a declarative placement pipeline. Workload APIs declare requests and placement rules; trusted node/provider controllers publish capacity, labels, taints, devices, volumes, and topology; admission supplies defaults/policy; the scheduler queues, filters, scores, reserves/permits, and binds; kubelet admits and starts; controllers replace failures; autoscalers change supply/demand; observers and rebalancers handle drift.

The **request invariant** makes declared demand sufficient for protected operation. The **hard-versus-soft invariant** ensures correctness constraints never depend on scoring. The **trust invariant** protects security and compliance labels and scheduler/plugin authority.

The **dedication invariant** requires both repulsion and attraction. The **topology invariant** defines correct selector, eligible domains, independent failures, skew, and degraded behavior. The **stateful locality invariant** aligns member, claim, volume, and fenced writer identity.

The **priority invariant** constrains high priority and accounts for victims, termination, PDB limitations, and remaining filters. The **stage invariant** separates scheduler binding from kubelet admission and application readiness. The **drift invariant** observes and safely rebalances rather than assuming continuous enforcement.

This is an assurance structure, not a proof of optimal placement or availability. Scheduler/plugin implementations, node facts, capacity, autoscaler/provider behavior, failure independence, runtime admission, application replication, and operational policy remain assumptions requiring tests and evidence.

## Alternatives and Trade-Offs

Hard constraints protect correctness but reduce feasible capacity and can block recovery. Preferences preserve flexibility but cannot guarantee isolation, locality, or availability. A platform can combine hard region/security with soft zone/host balance for graceful degradation where acceptable.

Packing increases utilization, frees whole nodes, and reduces cost but concentrates failures and interference. Spreading improves fault tolerance and sometimes latency while increasing cross-zone traffic, fragmented headroom, and cost. Use different scoring profiles or workload classes only with explicit objectives.

Node affinity selects infrastructure facts; pod affinity expresses workload relationships; topology spread expresses distribution. Affinity can model specialized dependencies but costs more and is easier to deadlock. Spread better represents balanced replicas but depends on accurate domains/selectors.

Dedicated pools simplify isolation and performance attribution but fragment capacity. Shared pools improve utilization but need stronger runtime controls and noisy-neighbor management. Taints/tolerations provide repulsion permissions, not isolation by themselves.

Preempting priority reduces time to recover critical services at the cost of victim disruption and wasted work. Non-preempting priority changes queue order without collateral termination but cannot create immediate space. Existing headroom is faster and more reliable but costs money.

Automatic rebalancing improves policy conformance and utilization but creates disruption, data movement, and churn. Eventual replacement is gentler but may leave risk/cost skew for a long time.

## Failure Modes and Misconceptions

- **“The scheduler uses current CPU and memory utilization.”** Core fit uses declared requests against allocatable/requested capacity; runtime metrics guide tuning and other controllers.
- **“A preferred rule will be honored if possible.”** It is one weighted score among others and offers no guarantee.
- **“A toleration sends a pod to the tainted pool.”** It only removes matching repulsion; pair it with positive node selection.
- **“Required affinity keeps enforcing after scheduling.”** `IgnoredDuringExecution` rules generally do not evict a pod when labels change.
- **“Different nodes mean different failure domains.”** Nodes may share rack, zone, power, network, storage, account, or control plane.
- **“Topology spread always stays balanced.”** It affects incoming scheduling; deletion and scale-down can create drift.
- **“Hard anti-affinity is the strongest availability policy.”** It can block rollout/recovery and lacks `minDomains` balance semantics; choose from the actual failure model.
- **“Priority guarantees that a pod runs.”** Nonresource constraints can remain; victims take time; capacity can race; preemption may not help.
- **“PDB prevents preemption.”** Scheduler preemption treats it as best effort, not an absolute guarantee.
- **“Node pressure is a scheduler bug.”** A pod can fit declared requests and later exceed them or encounter disk/PID pressure; kubelet eviction is separate.
- **“Scheduling gates reserve the future node.”** They only postpone consideration and can be abandoned.
- **“Adding nodes fixes Pending pods.”** New nodes must match all labels, taints, topology, devices, volumes, quotas, and profile rules.

## Worked Examples

### Example 1

A pod requests average memory and is repeatedly evicted at peak. The team derives a protected percentile plus failover headroom, validates the limit, and updates pool capacity instead of blaming scoring.

### Example 2

A dedicated GPU workload tolerates the GPU taint but lands on general nodes. Required pool affinity is added; the toleration remains only the permission to enter GPU nodes.

### Example 3

A three-replica API has hard hostname anti-affinity and cannot surge during a three-node rollout. Zone-hard plus host-soft topology spread preserves availability while permitting controlled same-host overlap.

### Example 4

A spread selector omits the incoming revision label, so new pods do not count themselves. Correct selector/match-label behavior restores meaningful skew and conformance tests catch recurrence.

### Example 5

A zonal PVC stays Pending because the pod uses `nodeName`. Removing direct pinning and using affinity lets delayed binding and scheduler topology choose a compatible node/volume.

### Example 6

A high-priority pod preempts two workers but remains Pending because its required accelerator label is absent. Diagnostics separate resource victims from the unchanged hard label failure.

### Example 7

A non-preempting research job moves ahead in the queue but waits for a whole GPU node, avoiding loss of several long-running lower-priority simulations.

### Example 8

A scale-to-zero zone disappears from scheduler domains, making `minDomains` unsatisfiable. Autoscaler templates retain zone knowledge and provider-capacity failure is surfaced rather than weakening spread.

### Example 9

After maintenance, all replicas remain in one zone because bound pods are not moved. A PDB-aware, rate-limited rebalance canaries evictions and observes endpoint capacity during redistribution.

### Example 10

A regulated workload's node label was writable by kubelet credentials. The platform moves it to protected label prefixes, trusted provisioning/admission, attestation, dedicated placement policy, and audit.

## Cross-Program Connections

Operating systems contributes CPU/memory scheduling, cgroups, NUMA, devices, pressure, and eviction. Algorithms contributes multidimensional bin packing, constraints, scoring, queues, and approximation. Distributed systems contributes failure domains, quorum, partitions, locality, and eventual state.

Reliability contributes headroom, degraded modes, disruption, recovery time, capacity and failure testing. Security contributes trusted labels, tenancy, admission, denial-of-service resistance, and isolated pools. Performance contributes interference, tail latency, locality, device utilization, and representative demand.

Storage contributes topology, attach limits, local data, and writer fencing. Networking contributes cross-zone cost and endpoint locality. Finance contributes packing, idle headroom, specialized nodes, transfer, and fragmentation. Platform product engineering turns these into governed workload classes and explainable diagnostics.

## References

- Kubernetes Project, [*Kubernetes Scheduler*](https://kubernetes.io/docs/concepts/scheduling-eviction/kube-scheduler/), current documentation retrieved September 2, 2026. Unscheduled pods, feasible nodes, filtering, scoring, binding, placement factors, profiles, and scheduler boundaries.
- Kubernetes Project, [*Scheduling Framework*](https://kubernetes.io/docs/concepts/scheduling-eviction/scheduling-framework/), current documentation retrieved September 2, 2026. Queue, scheduling and binding cycles; plugin extension points; reserve, permit, and unreserve behavior.
- Kubernetes Project, [*Assigning Pods to Nodes*](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/), current documentation retrieved September 2, 2026. `nodeSelector`, node name, node and pod affinity/anti-affinity, term composition, namespaces, topology keys, and trusted labels.
- Kubernetes Project, [*Taints and Tolerations*](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/), current documentation retrieved September 2, 2026. Matching, `NoSchedule`, `PreferNoSchedule`, `NoExecute`, bounded toleration, dedicated nodes, and condition taints.
- Kubernetes Project, [*Pod Topology Spread Constraints*](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/), current documentation retrieved September 2, 2026. Selectors, topology domains, eligibility, skew, minimum domains, hard/soft behavior, inclusion policies, defaults, and limitations.
- Kubernetes Project, [*Resource Management for Pods and Containers*](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/), current documentation retrieved September 2, 2026. Requests, limits, scheduling fit, cgroup behavior, pod/container aggregation, extended resources, ephemeral storage, and pressure.
- Kubernetes Project, [*Pod Overhead*](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-overhead/), current documentation retrieved September 2, 2026. RuntimeClass overhead admission, scheduler accounting, kubelet/cgroup behavior, and pod resource totals.
- Kubernetes Project, [*Pod Priority and Preemption*](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/), current documentation retrieved September 2, 2026. PriorityClass, queue order, preempting/non-preempting policy, victim selection, PDB interaction, limits, and troubleshooting.
- Kubernetes Project, [*Pod Scheduling Readiness*](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-scheduling-readiness/), current documentation retrieved September 2, 2026. Scheduling gates, creation/removal rules, gated state, mutable directives, and metrics.
- Kubernetes Project, [*Scheduler Configuration*](https://kubernetes.io/docs/reference/scheduling/config/), current documentation retrieved September 2, 2026. Configuration API, profiles, plugin stages, weights, multiple schedulers, and VolumeBinding.
- Kubernetes Project, [*Node-pressure Eviction*](https://kubernetes.io/docs/concepts/scheduling-eviction/node-pressure-eviction/), current documentation retrieved September 2, 2026. Pressure signals, thresholds, node conditions/taints, reclamation, pod selection, QoS, requests, priority, and grace.
- Kubernetes Project, [*Storage Classes*](https://kubernetes.io/docs/concepts/storage/storage-classes/#volume-binding-mode), current documentation retrieved September 2, 2026. Immediate versus delayed volume binding, scheduler participation, topology constraints, `nodeName` caveat, and capacity-aware provisioning.

## Exercises

### Exercise 1

Design placement contracts for a public API, three-voter database, GPU inference service, untrusted build workers, and interruptible batch jobs. Include resources, pools, trusted labels, taints, affinity/spread, storage/devices, priority, autoscaling, disruption, and evidence.

### Exercise 2

Audit a Deployment whose pods have no requests, tolerate every taint, require hostname anti-affinity, use a spread selector that does not match their labels, request a zonal PVC with Immediate binding, and use the highest custom PriorityClass.

### Exercise 3

Given four zones with matching-pod counts $(3,2,2,0)$, a hard zone constraint with `maxSkew: 1` and `minDomains: 4`, evaluate where the next pod may go when all domains are eligible. Then analyze what changes if the fourth zone has no nodes or is excluded by required affinity.

### Exercise 4

Diagnose a high-priority pod that remains Pending after three lower-priority pods are preempted. Events also mention untolerated taint, unbound PVC, and insufficient accelerator. Provide an evidence-first response that avoids further collateral disruption.

### Exercise 5

Transfer the placement model to assigning emergency medical teams and equipment across hospitals during a regional disaster. Address capabilities, hard/soft constraints, geography, failure domains, scarce resources, priority, displacement, travel/setup, changing state, fairness, evidence, and human authority.

## Answers to the Exercises

### Answer 1

The public API requests measured CPU/memory including sidecars/overhead, requires general trusted nodes, spreads hard across available zones and softly across hosts, uses service-critical governed priority, autoscaled pool headroom, PDB/rollout capacity, and task plus scheduling evidence. Database voters use one identity/PVC each, delayed volume binding, hard independent-zone spread with quorum-aware degraded policy, pod/member fencing, controlled disruption, and no generic rebalance. GPU inference selects an approved device/driver class with required node affinity and taint toleration, declares extended resources, prefers packing or spreading according to interference/failure tests, and measures device/queue/task results. Untrusted builds require an isolated tainted/labeled runtime pool, narrow toleration plus affinity, local scratch quotas, low priority, egress/runtime controls, and no protected volumes. Batch jobs use non-preempting or low priority, checkpointing, flexible soft placement, quota, scale-from-zero templates, and bounded queue objectives. Every class records feasible-node counts, failed filters, bind/start/readiness stages, skew, preemption/eviction, and cost.

### Answer 2

Missing requests makes packing and pressure behavior dishonest; derive protected CPU/memory/ephemeral demand from representative execution. Wildcard toleration permits placement onto dedicated, control-plane, unhealthy, or regulated nodes; replace it with exact pool tolerations and positive affinity. Hard hostname anti-affinity can block surge and recovery; use zone-hard/host-soft spread if that matches failure goals and capacity. Correct the spread selector so incoming pods count, validate topology keys, and set `minDomains`/degraded behavior deliberately. Immediate zonal provisioning can bind away from feasible compute; use a supported delayed-binding class and remove any direct node pinning. Highest priority is a denial/disruption risk and does not cure nonresource constraints; assign a quota-governed semantic class based on recovery importance. Test normal, rollout, node/zone loss, pool scale, storage capacity, and preemption before promotion.

### Answer 3

With all four domains eligible, the global minimum is zero. For a hard constraint, the scheduler evaluates the candidate domain's matching count after placement minus that global minimum. Placing in the empty fourth zone produces candidate skew $1-0=1$ and is allowed. Placing in a domain currently holding two or three produces candidate skew at least $3-0=3$ and is rejected. The cluster-wide maximum-minus-minimum after the allowed placement is still two, which illustrates why that descriptive imbalance is not the admission formula. If the fourth zone has no eligible nodes, eligible-domain count falls below `minDomains`; the documented global minimum remains zero, and every remaining domain already has at least two matching pods, so every candidate is unschedulable under `maxSkew: 1`. Required affinity exclusion has the same eligibility effect. Restore eligible capacity or consciously revise the failure contract; do not silently lower `minDomains` merely to clear Pending.

### Answer 4

Stop further preemption and read the complete FailedScheduling events/profile status. Victim removal addresses only resource fit; an untolerated taint, unbound or topology-incompatible PVC, and absent accelerator independently keep the feasible set empty. Confirm the pod's exact tolerations/required pool labels, whether the tainted accelerator pool is intended, device-plugin resource advertisement and allocatable count, PVC class/binding mode/events/topology, node attach limits, and current provider capacity. Compare these with autoscaler node templates and limits. If the workload belongs on that pool, add only the approved exact toleration/affinity through its workload class, restore device/plugin or scale valid nodes, and let delayed storage binding coordinate topology. If requirements are contradictory, correct the owning contract. Restore displaced capacity/workloads according to priority policy and measure termination loss. Do not preempt more pods, add wildcard tolerations, change claim identity, or remove device requirements without evidence.

### Answer 5

Represent each team, clinician, bed, operating room, ambulance, blood product, ventilator, and specialty as time-varying capacity/capability, with location, travel/setup time, shift limit, safety, and compatibility. Hard constraints include required specialty/equipment, patient safety, reachable geography, infection/isolation, and legal scope; soft preferences include proximity, continuity, balanced fatigue, and home-region cost. Spread critical capabilities across hospitals whose power, access, supply, and communications failures are genuinely independent, while preserving enough local teams for existing patients. Emergency priority may displace lower-urgency elective work only through an authorized triage policy that accounts for victims and setup delay; it cannot create a missing specialist or device. Continuously update capacity and transport routes, but treat stale reports as uncertain rather than true. Observe request, candidates rejected and why, assignment, departure, arrival/setup, treatment readiness, outcomes, displaced care, and fairness. Incident commanders and clinical leaders approve exceptions and reassignment; optimization proposes placements but never replaces medical triage or informed human authority.
