# Capstone — Atlas Kubernetes Runtime 1.0

The capstone is not a collection of unrelated examples. It is one workload release progressively translated into Kubernetes authority and evidence.

```text
Course 3 Atlas Workload Release 1.0
        |
        | exact image subjects and runtime contract
        v
AtlasWorkload custom resource
        |
        | atlas-controller owns generated workload fields
        +--------------------+
        |                    |
        v                    v
API Deployment          Worker Deployment
3 replaceable replicas  1 replaceable consumer
        |                    |
        v                    v
ReplicaSets and Pods    ReplicaSet and Pod
        |                    |
        +---------+----------+
                  |
                  v
conditions, scheduling, lifecycle, disruption, and release evidence
                  |
                  v
exact Course 5 connectivity handoff
```

## Why the API and worker differ

The API has three replicas, rolling update with one surge and zero controlled unavailability, minimum-ready time, and a PDB requiring two available replicas. This is a workload-controller policy, not proof of multi-zone or network availability.

The worker remains one replica. Its spool and results paths are declared through PVC interfaces because Course 3 requires durability. Course 4 does not know whether concurrent workers can safely claim work or publish results against a future storage system. Scaling before Course 6 would convert an unknown into a race. The capstone records the limit instead of hiding it.

## Native objects and custom abstraction

The course first teaches native objects directly. Only Module 10 introduces `AtlasWorkload`. The custom resource exposes stable platform intent:

- API and worker release subjects;
- replica intent within proven bounds;
- configuration reference;
- availability class.

The controller renders native Deployments and status. It does not recreate Kubernetes scheduling, rollout, or Pod lifecycle logic. Native controllers retain those responsibilities.

## Implementation lanes

### Python semantic control plane

`capstone/atlas_kube/` contains deterministic models for:

- API persistence, resource versions, generations, watch records;
- Server-Side Apply conflicts and ownership transfer;
- finalizers and garbage-collection relationships;
- Deployment, ReplicaSet, and Pod population;
- rollout bounds;
- Jobs and effect identity;
- configuration projection;
- scheduling predicates;
- probes, shutdown, PDB calculations;
- StatefulSet identity;
- AtlasWorkload reconciliation.

### Go controller

`capstone/controller-go/` contains a standard-library reconciliation core and an in-cluster HTTPS adapter using ServiceAccount identity, Server-Side Apply, finalizers, and the status subresource. It compiles and tests without external Go dependencies.

It is intentionally not described as a production controller manager. Leader election, informer caches, work queues, rate limiting, metrics, admission webhooks, and operated SLOs remain unexecuted capabilities.

### Kubernetes manifests

`capstone/manifests/base/` is production-intent desired state. It preserves exact image digests and runtime security. The PVCs reference a Course 6 StorageClass interface and may remain Pending in Course 4.

`capstone/manifests/labs/` contains controller-choice teaching resources. `capstone/manifests/controller/` contains the CRD, RBAC, controller Deployment contract, and sample custom resource.

### kind observation lane

The optional lane uses a digest-pinned kind node image but a separate observation workload. It proves local Kubernetes mechanics only. The manifest is labelled `local-observation-only` so it cannot be confused with the release candidate.

## Completion conditions

Atlas Kubernetes Runtime 1.0 is accepted only when:

- predecessor images and runtime constraints are unchanged;
- selectors and ownership graphs are unambiguous;
- reconciliation reaches steady state with zero writes;
- finalizer cleanup is idempotent and visible when blocked;
- rollout integers and scheduling predicates are recorded;
- probe and shutdown contracts match their repair actions;
- worker durable paths are not backed by `emptyDir` in the release lane;
- every networking and storage claim is exported to the owning later course;
- Course 5 handoff files match their exact manifest.

Run `make capstone-tour` to exercise the cumulative dependency-light path.
