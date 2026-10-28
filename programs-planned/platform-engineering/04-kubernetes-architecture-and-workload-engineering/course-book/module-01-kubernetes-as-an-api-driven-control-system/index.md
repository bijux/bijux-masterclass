# Module 1 — Kubernetes as an API-driven control system

Kubernetes is often introduced through a sequence of commands: create a Deployment, inspect Pods, expose a Service. That sequence hides the central engineering idea. Kubernetes is a distributed control system organized around an API. Clients write desired state. Independent components observe subsets of that state, act on the world, and publish observations. No single component “runs the application” from beginning to end.

The most useful question in this course is therefore not “Which YAML field do I need?” It is:

> Which component owns this transition, which API object records it, and what evidence explains why convergence did or did not occur?

## The API server is the authority boundary

The Kubernetes API server is the front door to persisted cluster state. Authentication, authorization, admission, defaulting, validation, conversion, and persistence occur around this boundary. A client may submit a manifest, but the server-returned object is the authoritative admitted representation. Defaults may have been added. Invalid fields may have been rejected or, depending on the API and schema, pruned. Metadata such as UID and resource version is server-owned.

`kubectl` is one client. A controller, operator, scheduler, kubelet, CI system, or platform API can be another. Treating kubectl as “Kubernetes itself” makes later automation difficult to reason about.

The API is resource-oriented. A Deployment, Pod, Node, Job, and custom resource each have:

- type identity through `apiVersion` and `kind`;
- object identity through namespace, name, and UID;
- desired fields, usually under `spec`;
- observed fields, usually under `status`;
- metadata used for selection, ownership, concurrency, deletion, and field management.

## Persistence does not equal convergence

Suppose the Atlas API Deployment is accepted and persisted with three replicas. Three different facts can now be true:

1. the Deployment object exists;
2. the Deployment controller has created a ReplicaSet;
3. three ready Pods exist on healthy Nodes.

These facts belong to different stages. The API server can be healthy while the Deployment controller is stopped. The Deployment and ReplicaSet can exist while the scheduler cannot place Pods. Pods can be bound while kubelets cannot pull the image. Containers can run while readiness remains false.

This gives a failure ladder:

```text
client intent
→ admitted object
→ controller child object
→ scheduled Pod
→ kubelet sandbox and containers
→ application health
→ endpoint eligibility
```

Good diagnosis starts at the earliest missing transition rather than jumping to application logs.

## Control-plane components and their ownership

### API server

The API server validates and persists API state and mediates all other components. It does not directly create a Linux process on a worker node.

### etcd

etcd stores the API server's durable cluster state. Application code should not bypass the API server and read or mutate etcd. Doing so bypasses validation, version conversion, authorization, admission, and API invariants. Backup and restore of etcd are cluster-operating concerns addressed later; Course 4 needs only the ownership boundary.

### Controller manager

Controller processes run many control loops. The Deployment controller observes Deployments and ReplicaSets. The ReplicaSet controller observes ReplicaSets and Pods. Job, DaemonSet, StatefulSet, namespace, service-account, endpoint, and garbage-collection controllers own other transitions.

A controller is generally **level-triggered**: it compares current state with desired state and acts toward the target. It must not depend on receiving every individual event. Watches can close, events can coalesce, and a process can restart. Re-listing and reconciling the current level must be sufficient.

### Scheduler

The scheduler observes Pods without a node assignment, filters Nodes that cannot satisfy requirements, scores feasible Nodes, and records a binding. It does not start containers. Once a Pod is bound, the kubelet on the selected Node owns local realization.

### Kubelet

The kubelet watches Pods assigned to its Node. It coordinates the container runtime, mounts, projected data, probes, container restarts, and Pod status. A kubelet can continue running existing Pods during a temporary control-plane outage, but new desired state cannot converge normally.

### Cloud and extension controllers

Cloud-controller components, CSI drivers, CNI plugins, admission webhooks, custom schedulers, and operators add transitions. Their presence does not change the analysis method: identify the object, controller, external system, and reported condition.

## Desired state, observed state, and time

Kubernetes does not promise immediate convergence. It promises an architecture in which controllers repeatedly attempt convergence. Between attempts, desired and observed state differ.

That difference is not automatically an incident. It becomes actionable when one of these is true:

- the gap exceeds a declared time budget;
- a controller reports a terminal or stalled condition;
- retries cannot make progress;
- the desired state is impossible under current constraints;
- the world changed outside the controller's authority;
- two managers fight over the same field or child object.

Atlas therefore records both the desired replica count and observed availability. “Deployment applied successfully” is not accepted as workload completion.

## Reconciliation must be idempotent

Controllers are retried. A queue item can be processed more than once. A watch can reconnect. A process can crash after an external effect but before recording status. A correct reconciler computes or enforces a desired level rather than blindly appending another effect.

Bad reconciliation:

```text
on event: create one Pod
```

If the event is repeated, the controller creates another Pod.

Level-based reconciliation:

```text
count owned Pods matching desired template
if fewer than desired: create the missing number
if more than desired: delete selected excess Pods
```

The second form tolerates repeated execution because the decision is derived from current state.

Idempotency is not merely “HTTP PUT is idempotent.” It is the property that reprocessing the same desired state cannot multiply business or infrastructure effects beyond the target.

## Ownership graphs prevent controller fights

Every child object should have a clear controlling owner. Kubernetes owner references support garbage collection and make object graphs visible, but they do not replace design reasoning.

For Atlas:

```text
AtlasWorkload
  ├── Deployment atlas-api
  │     └── ReplicaSet
  │           └── Pods
  ├── Deployment atlas-worker
  │     └── ReplicaSet
  │           └── Pods
  ├── ServiceAccounts
  ├── ConfigMap reference
  └── PodDisruptionBudget
```

A custom controller should not directly create Pods that a Deployment also manages. A GitOps manager, human operator, and custom controller should not all force ownership of the same replica field. The object graph and field-ownership graph are related but distinct: owner references describe lifecycle relationships; managed fields describe which actor owns which object fields.

## Control-plane failure does not have one meaning

“Control plane down” can mean several things:

- API server unavailable: no normal API reads/writes; existing node workloads may continue.
- etcd unavailable: API server cannot persist or consistently serve state.
- scheduler unavailable: existing bound Pods continue; new unscheduled Pods remain Pending.
- controller manager unavailable: existing Pods may continue; replica replacement and rollout stop.
- kubelet unavailable on one Node: control plane eventually marks node/pods unhealthy, but local process state may be unknown.

This distinction matters during incidents. Restarting application Pods cannot repair an unavailable scheduler. Scaling a Deployment cannot help if the controller manager is not reconciling it.

## Atlas cluster contract

Course 4 creates `capstone/architecture/component-ownership.yaml`. It records:

- which component owns each transition;
- which object carries desired state;
- which status or condition carries observation;
- which proof lane can exercise the transition;
- which later course owns network, storage, security, or fleet behavior.

The contract also prevents scope creep. Course 4 may create a ClusterIP Service as a stable object reference, but it does not claim to explain kube-proxy, CNI routing, Gateway API, or cloud load balancers. Those belong to Course 5.

## Debugging by earliest failed transition

When Atlas API is unavailable, inspect in this order:

1. **Deployment object:** desired replicas, generation, conditions.
2. **ReplicaSet:** desired/current/ready counts and owner reference.
3. **Pods:** existence, phase, scheduling condition, container states.
4. **Events:** admission, scheduling, pull, mount, probe, eviction clues.
5. **Node and kubelet evidence:** placement and local realization.
6. **Application evidence:** logs and health endpoints.
7. **Connectivity evidence:** deferred to Course 5, but do not confuse it with Pod health.

Starting with logs can waste time when no Pod was ever scheduled.

## Capstone increment

The semantic API store in `capstone/atlas_kube/api_store.py` records objects with UID, resource version, generation, spec, status, labels, finalizers, and owner references. `controllers.py` reconciles a simplified Atlas workload into Deployments and Pods. The first lab deliberately stops one reconciler: desired state remains durable while convergence stops. Restarting the reconciler must recover without duplicate children.

## Further reading

- Kubernetes components: <https://kubernetes.io/docs/concepts/overview/components/>
- Kubernetes API concepts: <https://kubernetes.io/docs/reference/using-api/api-concepts/>
- Controllers: <https://kubernetes.io/docs/concepts/architecture/controller/>

## Transition

Module 1 establishes that state changes have owners. Module 2 examines how several owners safely modify API objects without lost updates, field fights, orphaned children, or deletion deadlocks.

## Worked investigation — the Deployment exists, but nothing runs

An operator applies the Atlas API Deployment and receives a successful response. Ten minutes later, there are no ready Pods. The phrase “the deployment failed” is too imprecise to guide action. Start by constructing a transition ledger.

| Transition | Owner | Object or evidence | Observation |
|---|---|---|---|
| Request admitted | API server and admission chain | Deployment UID, generation, resourceVersion | succeeded |
| Desired replica controller created children | Deployment controller | ReplicaSet owned by Deployment | succeeded |
| ReplicaSet created Pod objects | ReplicaSet controller | Pods with owner references | succeeded |
| Pods assigned to Nodes | scheduler | `.spec.nodeName`, scheduling condition, events | missing |
| Containers started | kubelet and runtime | container state and Node evidence | not reached |
| Application became eligible | kubelet probes and application | Ready condition | not reached |

The earliest missing transition is scheduling. Application logs cannot explain it because the application never started. The scheduler events show `0/3 nodes are available: 3 Insufficient cpu`. The corrective decision is not to restart the Deployment controller, delete the Pods, or weaken readiness. It is to change declared demand, add feasible capacity, or revise placement policy with explicit consequences.

Now change the incident: there is no ReplicaSet. The same symptom—no ready Pods—has a different earliest missing transition. The operator should inspect Deployment conditions, controller-manager availability, selector validity, and admission. A healthy scheduler is irrelevant because no Pod was created.

This method scales beyond Deployments. For any Kubernetes incident, write:

```text
intent
→ admitted state
→ controller-owned derivative state
→ placement
→ node realization
→ workload health
→ consumer eligibility
```

Then locate the first absent or contradictory fact. This prevents the common error of diagnosing from the most familiar layer rather than the owning layer.

## Design consequence — status is evidence, not a command channel

A controller should not infer new desired state from its own status output. `spec` expresses intent; `status` records observation. If a human writes `status.availableReplicas: 3`, no scheduler or kubelet is obligated to create anything. Similarly, an automation that writes desired configuration into status creates an authority loop with no clear owner.

Atlas therefore uses status only for:

- observed generation;
- conditions with stable reasons and messages;
- observed child identities;
- available and ready populations;
- the latest successful release subject;
- failures that require another actor to change desired state.

The distinction matters during recovery. Restoring etcd restores API state, not external effects that may have drifted. Controllers must re-observe the world and reconcile; they must not assume that a restored status document proves the current world.

## Common false conclusions

- **“The manifest applied, so the workload is deployed.”** Admission proves only that the API accepted state.
- **“A controller saw the event, so it will never need to see it again.”** Controllers must recover by relisting current state.
- **“A running container means the service is available.”** Running, ready, available, and reachable are different populations.
- **“The control plane owns application correctness.”** It owns reconciliation mechanics; the application still owns truthful health and safe shutdown.
- **“More reconciliation is always safer.”** A reconciler with ambiguous ownership can amplify damage repeatedly.
