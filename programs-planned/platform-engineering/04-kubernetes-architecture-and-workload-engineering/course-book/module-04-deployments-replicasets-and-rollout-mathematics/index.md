# Module 4 — Deployments, ReplicaSets, and rollout mathematics

A Deployment is a controller contract for continuously running interchangeable replicas and declarative template replacement. It does not update containers in place. It creates and scales ReplicaSets, which create Pods from immutable templates.

A rollout is therefore a controlled overlap between old and new replica populations. Availability depends on arithmetic, readiness, capacity, and application compatibility—not on the fact that `kubectl apply` returned success.

## The ownership chain

```text
Deployment
  owns ReplicaSets by selector and owner reference
ReplicaSet
  owns Pods matching its template
```

The Deployment selector must match the Pod-template labels and is effectively immutable after creation. A selector change is not a cosmetic rename; it changes which Pods the controller considers its population and can orphan or adopt resources unexpectedly.

Atlas uses stable identity labels for selection and separate informational labels for version. The image digest remains artifact identity.

## Template changes create revisions

The Pod template includes container images, environment, volumes, security context, probes, labels, and scheduling policy. A change to the template produces a new template hash and ReplicaSet.

Changing only Deployment metadata outside the template does not create a new workload revision. This distinction matters when operators expect a rollout after modifying a top-level annotation.

The revision number is useful history, not a substitute for exact template evidence. Preserve the ReplicaSet template and image digest.

## RollingUpdate bounds

A RollingUpdate strategy uses:

- `replicas`: desired steady-state count;
- `maxSurge`: temporary Pods above desired count;
- `maxUnavailable`: desired Pods allowed unavailable during rollout.

For percentages, Kubernetes rounds surge up and unavailable down.

For Atlas API:

```yaml
replicas: 3
maxSurge: 1
maxUnavailable: 0
```

This permits up to four total Pods and requires at least three available desired replicas during normal controlled rollout. It also requires spare schedulable capacity for the surge Pod. If the cluster has capacity for exactly three Pods, the rollout can deadlock even though the arithmetic is valid.

With `maxSurge: 0` and `maxUnavailable: 1`, rollout can proceed without spare capacity but intentionally drops available replicas. The correct policy depends on workload capacity and availability objectives.

## Availability is readiness plus time

A Pod contributes to available replicas only after it is ready for at least `minReadySeconds`. This filters brief readiness flaps. `minReadySeconds` is not a startup deadline; it is a stability interval after readiness.

`progressDeadlineSeconds` bounds how long the Deployment may fail to make progress before reporting `ProgressDeadlineExceeded`. It does not automatically roll back. An external release workflow must decide whether to pause, investigate, or revert.

A good rollout contract defines:

- startup budget;
- readiness meaning;
- minimum ready duration;
- progress deadline;
- surge/unavailability limits;
- application version coexistence rules;
- rollback compatibility.

## Desired, current, updated, ready, and available are different counts

Deployment status exposes several populations:

- desired replicas;
- current replicas;
- updated replicas matching the new template;
- ready replicas currently passing readiness;
- available replicas ready for the minimum duration;
- unavailable replicas.

A rollout can have all updated replicas but zero available if readiness fails. It can have available old replicas while the new revision makes no progress. Reports must state which population they mean.

## Readiness is a rollout gate

The Atlas API readiness endpoint represents ability to serve new requests with required dependencies. New Pods that fail readiness do not become available, so the Deployment should retain old capacity within its strategy bounds.

If liveness also checks a slow dependency, containers may restart repeatedly and never remain ready long enough. The rollout symptom belongs to Deployment status, but the root cause belongs to probe design. Module 8 deepens that interaction.

## Rollback creates another reconciliation target

A Deployment rollback changes the Pod template to a previous revision. It does not reverse external schema, configuration, secret, or data changes automatically.

Course 3 records that Atlas Workload Release 1.0 has no incompatible state-schema change for this exercise. That documented compatibility makes image rollback plausible. In a real release, rollback requires a matrix covering old/new application versions, configuration, database schema, events, and external dependencies.

A previous ReplicaSet can also have been scaled to zero; rollback scales it again. Do not treat the existence of revision history as proof that the old artifact is still retrievable or authorized.

## Pause and resume

Pausing a Deployment stops new rollout actions while allowing inspection and some updates. It can be useful while assembling several template changes or investigating a staged release. It is not a durable release approval mechanism and does not freeze external systems.

## Recreate strategy

`Recreate` scales down old Pods before creating new ones. It may be appropriate when versions cannot coexist or the workload cannot share an exclusive resource. It intentionally creates downtime and should not be used as a shortcut for misunderstood compatibility.

## Rollout failure taxonomy

### Unschedulable new Pods

Symptoms: new ReplicaSet exists; Pods remain Pending; scheduler events show insufficient resources or constraints. The rollout policy may require surge capacity the cluster lacks.

### Image-pull failure

Symptoms: Pods scheduled; containers waiting with pull errors. Artifact reference, registry authorization, platform compatibility, or node connectivity is wrong.

### Startup failure

Symptoms: containers restart or startup probe fails. Application/runtime contract is wrong.

### Readiness failure

Symptoms: containers run; ready remains false; old ReplicaSet may stay. Dependency or readiness semantics are wrong.

### Progress deadline

Symptom: Deployment condition reports no progress within budget. This is a controller observation, not the original cause. Inspect the earliest failed transition.

### Field conflict

A release manager cannot change the template because another field manager owns the image or probe field. Resolve ownership; do not blindly force.

## Atlas rollout calculation

The course provides `atlas_kube/rollout.py`. Given desired replicas and integer/percentage strategy, it calculates:

- rounded surge and unavailable values;
- maximum total Pods;
- minimum available Pods;
- whether progress requires spare capacity;
- whether the configuration is invalid;
- possible old/new population steps.

The model is not a Deployment-controller reimplementation. It makes the safety arithmetic visible and testable.

## Worked failure: green apply, red rollout

A release changes the Atlas API image digest. Apply succeeds. A new ReplicaSet appears and creates one Pod, but the Pod remains unready because the configuration key name changed. With `maxUnavailable: 0`, the controller keeps all old replicas and cannot complete.

A superficial report says “Deployment stuck.” A useful report says:

```text
Desired generation: 8
Observed generation: 8
Updated replicas: 1
Available updated replicas: 0
Old available replicas: 3
Progressing=False / ProgressDeadlineExceeded
Earliest failed transition: readiness of new Pod
Cause: missing configuration key expected by image digest X
Availability impact: old revision remains available
```

The correct repair is a compatible configuration/image change, not increasing `maxUnavailable` to force the broken revision through.

## Capstone increment

Atlas API uses three replicas, `maxSurge: 1`, `maxUnavailable: 0`, `minReadySeconds: 10`, and a bounded progress deadline. Worker uses one replica in Course 4 because its durable filesystem interface has not yet been made multi-writer safe. The lab simulates a permanently unready revision and requires a condition-based diagnosis and compatible rollback.

## Further reading

- Deployments: <https://kubernetes.io/docs/concepts/workloads/controllers/deployment/>
- ReplicaSets: <https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/>

## Transition

Deployments fit continuous interchangeable replicas. Module 5 compares them with finite, scheduled, and node-scoped controllers whose retry and completion semantics are different.

## Worked rollout — compute before you apply

Atlas API has five desired replicas. The rollout policy is `maxSurge: 40%`, `maxUnavailable: 20%`, and `minReadySeconds: 30`.

Kubernetes resolves percentage surge upward and percentage unavailability downward:

```text
maxSurge        = ceil(5 × 0.40)  = 2
maxUnavailable  = floor(5 × 0.20) = 1
maximum Pods    = 5 + 2           = 7
minimum available desired Pods = 5 - 1 = 4
```

These are controller limits, not guarantees of user-visible success. A new Pod must schedule, start, pass readiness, and remain ready for `minReadySeconds` before it contributes to availability.

Now assume all five old Pods occupy the only Nodes that satisfy strict topology constraints, and each Node has no capacity for another Pod. Although two surge Pods are permitted by policy, zero surge Pods are feasible. The controller may remove one old available Pod because `maxUnavailable` permits it, freeing capacity for one new Pod. If the new revision never becomes ready, rollout stops with four old available replicas and one failing new Pod. Raising `maxUnavailable` can accelerate loss without creating evidence that the new revision works.

### The four populations that matter

A useful rollout ledger records:

| Population | Meaning |
|---|---|
| desired | target replicas in the Deployment |
| updated | replicas using the current Pod template |
| ready | current Pods passing readiness |
| available | ready Pods that satisfy minimum ready time |

A rollout can have `updated=5`, `ready=0`, and `available=4` if five new Pods exist but none is ready while four old Pods remain available. “All new Pods created” is not completion.

### Rollback is a compatibility decision

Deployment revision history can restore a prior Pod template. It cannot restore:

- an externally migrated database;
- an old secret value that has been destroyed;
- a removed message schema;
- a revoked image digest;
- an incompatible ConfigMap contract;
- external side effects already produced.

Course 4 therefore records rollback eligibility as an input from release evidence, not as a property inferred from Deployment history.

## Common false conclusions

- **“25% means one quarter of a Pod can be unavailable.”** Controllers operate on resolved integers.
- **“Progress deadline performs rollback.”** It reports stalled progress; release automation decides what follows.
- **“All Pods are updated, so release succeeded.”** Updated is not ready or available.
- **“Deleting a failing new Pod restarts the rollout cleanly.”** The same template is recreated.
- **“More surge always speeds rollout.”** Scheduling, quota, and topology may make surge infeasible.

## Design exercise — capacity-aware strategy selection

Before choosing a strategy, calculate whether the cluster can satisfy it under the same placement rules as the old revision. A critical workload with zero unavailability may need reserved surge capacity in every required failure-domain combination. If that capacity does not exist, the strategy is an aspiration rather than an executable plan.

Course 4 records this as a release precondition. Course 5 measures runtime demand, and Course 9 owns fleet capacity; neither later course can retroactively make an uncomputed Course 4 rollout safe.
