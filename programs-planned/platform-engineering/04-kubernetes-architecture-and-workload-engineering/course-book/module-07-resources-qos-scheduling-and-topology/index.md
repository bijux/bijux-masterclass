# Module 7 — Resources, QoS, scheduling, and topology

The scheduler does not place Pods where CPU happens to look idle. It evaluates declared resource requests and placement constraints against Node information, filters impossible Nodes, scores feasible Nodes, and records a binding. Kubelet then enforces resource policy locally and may evict Pods under pressure.

A Pod can be valid, healthy in isolation, and permanently Pending because its combined constraints describe no real Node.

## Requests and limits answer different questions

A **request** is the resource quantity used for scheduling and much of resource accounting. A **limit** constrains runtime use through cgroup mechanisms and runtime policy.

For CPU:

- request influences placement and CPU shares;
- limit can throttle CPU over time;
- CPU saturation usually slows work rather than killing the process.

For memory:

- request influences placement and QoS;
- limit can lead to OOM termination when exceeded;
- memory is not safely throttled like CPU.

The scheduler generally does not use current application memory/CPU usage to decide placement. It uses declared requests. Under-requesting can overpack Nodes and produce pressure; over-requesting can make capacity appear unavailable.

Course 3's 100m/64Mi request and 500m/128Mi limit are hypotheses, not production capacity evidence. Course 5/9 will measure and revise them.

## Pod resource total

Scheduling considers the effective Pod request, including regular containers, relevant init-container maxima, and Pod overhead where configured. A large init step can prevent scheduling even if the long-running application is small.

Sidecars run with the workload and contribute continuously. Ephemeral containers are primarily diagnostic and have different resource declaration constraints; their use can still affect a pressured Node.

## Quality of Service classes

Kubernetes classifies Pods:

- **Guaranteed:** every container has CPU and memory request and limit, and each request equals its limit;
- **Burstable:** at least one request or limit exists, but Guaranteed requirements are not met;
- **BestEffort:** no container has CPU or memory requests or limits.

QoS influences eviction and OOM scoring, but it is not a priority or availability guarantee. A Guaranteed Pod can still be evicted or fail if the Node disappears.

Atlas is Burstable in Course 4 because it reserves a baseline and permits bounded CPU/memory burst. The decision is explicit; “Guaranteed is always best” would waste capacity and can increase scheduling difficulty.

## Scheduling pipeline

A simplified scheduler cycle:

1. observe an unscheduled Pod;
2. determine scheduling readiness;
3. filter Nodes by resources and hard constraints;
4. score feasible Nodes by preferences and policy;
5. reserve/permit if plugins require it;
6. bind the Pod to the selected Node.

After binding, kubelet admission can still fail due to node-local reality. Scheduling success is not runtime success.

## Node selectors and node affinity

`nodeSelector` expresses exact label matches. Node affinity supports required and preferred expressions.

Required affinity is a hard filter. Preferred affinity influences scoring only. Labels used for security or compliance placement need a trustworthy source; a compromised kubelet should not be able to self-label into a privileged pool. Course 8 addresses label authority.

Atlas uses required OS/architecture compatibility only when the multi-platform image index cannot supply all cluster architectures. Because Course 3 provides amd64 and arm64, the base avoids unnecessary architecture pinning.

## Taints and tolerations

Taints repel Pods. Tolerations allow a matching taint but do not attract the Pod or guarantee placement.

A toleration without an accompanying placement rule can let Atlas run on both ordinary and special Nodes. If the intent is “only on dedicated nodes,” use both a toleration and required affinity/selector.

Atlas application workloads do not tolerate control-plane or privileged-node taints. The lab DaemonSet has a narrowly justified toleration for its eligible nodes.

## Pod affinity and anti-affinity

Pod affinity places a Pod near matching Pods. Anti-affinity separates it from matching Pods. Hard inter-Pod affinity/anti-affinity can be expensive at scale and depends on consistent topology labels.

For Atlas API, hard anti-affinity by hostname can make a three-replica Deployment unschedulable in a two-node lab. Topology spread constraints often express distribution more flexibly.

## Topology spread constraints

A topology spread constraint tries to balance matching Pods across domains such as hostname or zone. Key fields include:

- `maxSkew`;
- `topologyKey`;
- `whenUnsatisfiable`;
- label selector;
- optional minimum domains and policies.

`DoNotSchedule` is a hard placement rule. `ScheduleAnyway` is a preference. A declared zone spread cannot produce resilience if all Nodes have the same or missing zone label.

Atlas API uses:

- hard spread across hostnames with max skew one in the local model;
- preferred spread across zones in environments where zone labels and capacity exist;
- explicit evidence that the kind topology is not multi-zone.

## Priority and preemption

PriorityClasses rank Pods. If a high-priority Pod cannot schedule, the scheduler may nominate lower-priority Pods for preemption. Priority is not a substitute for capacity or correct requests. Excessive priority can starve other workloads and create cascading disruption.

Atlas uses platform-defined, non-system priority classes only in scenarios that justify them. Application teams should not create arbitrary highest priority classes. ResourceQuota can restrict priority use.

## Unschedulable is a reasoned state

The Pod scheduling condition and events can report reasons such as:

- insufficient CPU or memory;
- node-selector/affinity mismatch;
- untolerated taint;
- topology spread impossible;
- volume topology conflict;
- host port conflict;
- node unschedulable.

Do not “fix” by deleting the Pod. The controller creates another with the same impossible template. Change the constraint or the available world.

## Preemption is not always helpful

If no Node matches a required label or toleration, evicting lower-priority Pods cannot help. Scheduler messages often state that preemption is not helpful. This is evidence that the hard constraint, not capacity occupancy, is the blocker.

## Node pressure and eviction

Kubelet monitors memory, filesystem space, inodes, and other signals. Under pressure it may reclaim resources and evict Pods. Node-pressure eviction is not governed by PodDisruptionBudget and can use little or no grace under hard thresholds.

QoS, priority, and usage relative to request influence victim selection. Under-requested Pods can be more vulnerable because their use exceeds requests.

Course 8 explores availability consequences; Course 9 addresses fleet capacity and node operation.

## Dynamic resources are a later specialization

Kubernetes 1.36 includes stable Dynamic Resource Allocation foundations for devices. This course names DRA as the modern device-allocation model but does not turn the core workload course into a GPU/device-driver course. The same method still applies: claims, classes, scheduling, node access, and lifecycle ownership.

## Atlas scheduling profile

The base Atlas API template declares:

- CPU 100m request / 500m limit;
- memory 64Mi request / 128Mi limit;
- Burstable QoS;
- preferred zone spread;
- required hostname spread where replica/node count permits;
- no broad tolerations;
- no direct `nodeName` assignment;
- no host ports.

The worker has one replica and a durable-volume interface. Course 6 will add storage topology; Course 4 records that scheduler decisions can later be constrained by volume binding.

## Worked failure: individually reasonable, collectively impossible

A Pod requires:

- label `nodepool=general`;
- zone `a` or `b`;
- hard anti-affinity from Atlas API on hostname;
- a toleration for `dedicated=batch` but no affinity to that pool;
- 2 CPU;
- spread across three hostname domains.

The cluster has two general Nodes with 1.5 CPU free each and one dedicated Node with 4 CPU. The Pod cannot use the dedicated Node because required `nodepool=general` excludes it; toleration only permits the taint. General Nodes lack CPU, and three-domain spread cannot be met.

The safe repair depends on intent. Removing all constraints is not engineering. Options include adjusting the request after measurement, adding general capacity, changing the dedicated placement contract, or relaxing domain count with documented availability consequences.

## Capstone increment

`atlas_kube/scheduler.py` evaluates requests, labels, taints, hard affinity, anti-affinity, and topology spread and returns per-Node reasons. The lab constructs an impossible Pod and requires the learner to identify the minimum safe relaxation while preserving the intended failure-domain policy.

## Further reading

- Scheduling and eviction: <https://kubernetes.io/docs/concepts/scheduling-eviction/>
- Resource management: <https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/>
- Taints and tolerations: <https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/>
- Topology spread: <https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/>

## Transition

Scheduling places Pods, but availability depends on what happens after placement and during maintenance. Module 8 combines probes, termination, readiness, eviction, disruption budgets, and rollout behavior into one availability model.

## Worked scheduling proof — capacity is necessary but not sufficient

Three Nodes exist:

| Node | Allocatable CPU | Zone | Pool | Taint |
|---|---:|---|---|---|
| n1 | 2000m | a | general | none |
| n2 | 2000m | b | general | none |
| n3 | 4000m | a | batch | `dedicated=batch:NoSchedule` |

An Atlas API Pod requests 1500m CPU, requires `pool=general`, requires one Pod per hostname through hard anti-affinity, and has a topology-spread rule across zones with `maxSkew: 1` and `DoNotSchedule`. Existing API replicas occupy n1 and n2.

Raw cluster capacity is 8000m. The Pod still has no feasible Node:

- n1 fails hard anti-affinity;
- n2 fails hard anti-affinity;
- n3 fails required pool affinity and lacks a toleration.

Adding the batch toleration alone does not help because required affinity still rejects n3. Changing affinity alone may permit n3 but violate workload-isolation policy. Deleting the Pending Pod simply asks the scheduler the same impossible question again.

A scheduler explanation should preserve per-Node reasons. Aggregated events are useful, but they can hide combinations. The minimum safe repair depends on declared intent: add a general Node in a third zone, relax anti-affinity to preferred, or change replica/capacity design. The “smallest YAML edit” is not necessarily the smallest risk.

### Requests are scheduling truth; limits are runtime ceilings

CPU and memory requests influence placement. CPU limits become throttling budgets. Memory limits can produce termination when exceeded. A Pod with a low request and high observed usage may overcommit a Node even before reaching its limit. A Pod with a tight CPU limit may remain ready while latency deteriorates from throttling.

QoS class is derived from request/limit structure, but eviction selection also considers actual usage, priority, and pressure. `Guaranteed` is not “cannot be evicted,” and high priority is not extra capacity.

### Topology is a label contract

A topology spread constraint assumes topology labels are accurate and sufficiently represented. If every Node reports the same zone, a zone spread rule has no resilience value. If a required domain disappears, `minDomains` and unsatisfiable behavior affect placement. Labels are operational inputs and must be governed like configuration.

## Common false conclusions

- **“The cluster has enough CPU, so scheduling should succeed.”** All hard predicates must pass on one Node.
- **“Toleration attracts a Pod.”** It only permits a tainted Node; affinity and scoring decide more.
- **“Priority creates capacity.”** It may preempt lower-priority work but cannot create resources.
- **“Limits are reservations.”** Requests are the primary scheduling reservation.
- **“Topology spread guarantees multi-zone availability.”** It relies on truthful labels, feasible capacity, and later network/storage behavior.
