# Module 2 — API objects, change semantics, and ownership

Once several clients and controllers can modify Kubernetes state, correctness depends on more than valid YAML. An API object is a concurrent record with server-assigned identity, optimistic concurrency, field managers, lifecycle ownership, and deletion protocols. A casual “apply this manifest” can overwrite another manager, recreate an object with a new UID, orphan children, or leave deletion stuck indefinitely.

This module treats object changes as a concurrency and ownership problem.

## Object identity is more than a name

Within a namespace and resource type, an object is addressed by name. Its **UID** identifies one lifetime. Delete and recreate `atlas-api` and the name is the same, but the UID changes. Owner references and preconditions can therefore distinguish an old object from a replacement.

Important metadata includes:

- `name` and `namespace`: address in the API;
- `uid`: unique lifetime identity;
- `resourceVersion`: opaque concurrency/watch token;
- `generation`: desired-state revision for resources that implement it;
- `labels`: selectable identity and grouping;
- `annotations`: non-identifying metadata;
- `ownerReferences`: lifecycle graph;
- `finalizers`: deletion barriers;
- `managedFields`: server-side field ownership history;
- `deletionTimestamp`: deletion has begun but is not complete.

Do not parse or numerically compare `resourceVersion`. It is opaque. Use it where the API requires a concurrency or watch position.

## Spec and status are separate responsibilities

The common API convention is:

```text
spec    desired state supplied by users or higher-level controllers
status  observed state supplied by controllers
```

A controller should not rewrite user intent to match the world. If the desired replicas are three and only two are available, status records two; the controller continues trying to reach three or reports why it cannot.

The status subresource can have separate authorization and update semantics. A controller updating status should not accidentally replace spec. A user changing spec should not need to send the latest status.

`generation` usually changes when desired fields change. A controller records `observedGeneration` in status or conditions after processing that generation. Without this link, a `Ready=True` condition might describe an older spec.

## Conditions are a contract, not a log

A condition typically includes:

- type;
- status: `True`, `False`, or `Unknown`;
- reason: stable machine-readable cause;
- message: human explanation;
- last transition time;
- observed generation.

Conditions should describe current aspects of state, not append an unbounded event history. Updating `lastTransitionTime` when only the message changed destroys its meaning. Writing the current timestamp on every reconcile can create an endless update loop.

For AtlasWorkload, useful conditions are:

```text
Accepted
Progressing
Available
Degraded
```

`Available=True` must be tied to the current generation and a defined readiness threshold. It is not synonymous with “some Pod exists.”

## Optimistic concurrency and resource versions

A read-modify-write update should include the resource version that was read. If another actor changed the object, the API rejects the stale update. The client then re-reads, recomputes, and retries.

Blind retry of the same stale object is wrong because it ignores the concurrent change. The retry unit is the **decision**, not the old payload.

For destructive operations, UID/resourceVersion preconditions prevent deleting a replacement that reused the same name.

## Patch styles are not interchangeable

Kubernetes supports several change mechanisms:

- full object replacement with `PUT`;
- JSON merge patch;
- JSON patch;
- strategic merge patch for selected built-ins;
- server-side apply.

Each has different list, omission, and ownership semantics. “Patch” is not a complete description.

Course 4 uses server-side apply for declarative ownership and explicit update/patch operations where the workflow owns a narrow mutation.

## Server-side apply and field managers

Server-side apply records an actor's declared field set. If another manager owns a field and the values conflict, the API rejects the apply unless ownership is deliberately forced.

This makes ownership visible:

```text
atlas-release-manager  owns image digest and Pod security context
atlas-operator         owns generated selectors and status
autoscaler             may own replicas in a later course
human-debugger         should own no durable workload fields
```

Force-conflicts is not a routine repair. It transfers ownership. The operator must know which workflow is being displaced and whether that workflow will immediately set the field back.

Omitting a previously managed field can relinquish ownership and may remove or default the value depending on other managers and schema behavior. Field-set evolution is therefore part of release design.

## Labels are API identity; annotations are commentary

Selectors drive Deployments, Services, scheduling rules, policies, and monitoring. Changing a selector can change ownership and routing. Labels used in selectors require stable governance.

Recommended Atlas labels:

```text
app.kubernetes.io/name
app.kubernetes.io/instance
app.kubernetes.io/component
app.kubernetes.io/part-of
app.kubernetes.io/version
```

The version label is informational; the image digest remains artifact identity.

Annotations can carry release references, evidence digests, or human metadata. They are not automatically trusted and should not contain secrets.

## Owner references and garbage collection

A controller sets owner references on children. When the owner is deleted, garbage collection can remove dependent objects according to propagation policy.

The controlling owner is not simply “the object that created this child.” It is the object whose desired state governs the child's lifecycle. A Deployment controls ReplicaSets; a ReplicaSet controls Pods.

Incorrect ownership causes:

- orphaned children after owner deletion;
- children deleted with the wrong parent;
- two controllers racing to adopt the same child;
- cross-namespace invalid references;
- release cleanup that destroys independently owned state.

PersistentVolumeClaims and external resources often require deliberate retention rather than automatic owner deletion. Course 6 addresses that in depth.

## Finalizers are deletion protocols

When an object with finalizers is deleted, the API sets `deletionTimestamp`; the object remains until controllers remove their finalizer strings.

A finalizer means:

> Before this API object disappears, the named controller must complete or explicitly abandon a cleanup/release obligation.

It does not mean “do cleanup sometime.” The controller must handle retries, missing external state, permission failure, and its own upgrade. A controller that disappears permanently can trap deletion.

For AtlasWorkload, a finalizer might release a reserved external identity. It should not protect ordinary Kubernetes children already handled by owner references.

A safe finalizer flow:

1. observe deletion timestamp;
2. inspect whether cleanup is already complete;
3. perform an idempotent cleanup step;
4. record durable evidence if needed;
5. remove only the controller's own finalizer;
6. tolerate repeated execution.

Never remove another controller's finalizer to “unstick” an object without understanding its obligation.

## Deletion propagation is a decision

Foreground deletion keeps the owner visible until dependents are gone. Background deletion removes the owner and lets garbage collection continue. Orphaning preserves dependents.

The right choice depends on ownership and recovery requirements. A release tool that always uses cascade deletion can destroy diagnostic Pods or state interfaces before evidence is preserved.

## Atlas field-ownership policy

Course 4 records field ownership in `capstone/architecture/field-ownership.yaml`.

Examples:

- Course 3 release manager owns image digests and runtime security defaults.
- Atlas controller owns generated Deployment selectors, child owner references, and AtlasWorkload status.
- workload authors own desired replicas, approved configuration references, and availability class.
- a later autoscaler may own replicas after an explicit contract change.
- Course 7 GitOps owns declared application resources but must not force controller-owned status.

This map prevents later courses from inventing conflicting workflows.

## Worked failure: the permanently terminating workload

An operator deletes AtlasWorkload. `deletionTimestamp` appears, but the object remains. The controller logs an authorization error while attempting external cleanup. A second operator removes the Deployment manually, but the custom resource still cannot disappear.

The correct diagnosis is not “Kubernetes deletion is broken.” The finalizer protocol is incomplete. Evidence should include:

- object metadata and finalizers;
- controller identity and authorization;
- cleanup target state;
- retry condition and reason;
- whether removing the finalizer would leak authority or data.

The repair may be to restore controller permission and let cleanup converge. Manual finalizer removal is a break-glass decision with an explicit residual-risk record.

## Capstone increment

The semantic API store implements UID, resource versions, generation changes, status updates, managed-field conflict detection, owner references, deletion timestamps, and finalizers. The lab creates one field conflict and one deletion deadlock, then repairs them through ownership-aware operations.

## Further reading

- Server-side apply: <https://kubernetes.io/docs/reference/using-api/server-side-apply/>
- API conventions: <https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md>
- Owners and dependents: <https://kubernetes.io/docs/concepts/overview/working-with-objects/owners-dependents/>
- Finalizers: <https://kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/>

## Transition

Object semantics establish how desired state is changed. Module 3 turns the Course 3 runtime contract into the Pod—the atomic scheduling and lifecycle unit on which workload controllers operate.

## Worked investigation — three managers, one replica field

Atlas begins with a Git-managed Deployment declaring three API replicas. A custom controller later writes two replicas because it interprets an `AtlasWorkload.spec.size` field. During an incident, an operator runs `kubectl scale` to five. All three actors appear reasonable in isolation; together they create an unstable ownership model.

The key question is not which value is “latest.” It is which actor is authorized to own `.spec.replicas`.

A sound design selects one of these models:

1. **Git owns replicas.** The custom resource may not also express size, and emergency scaling must change or temporarily transfer field ownership with a recorded process.
2. **AtlasWorkload owns replicas.** Git owns the custom resource, while the controller owns generated Deployment replicas. Humans do not edit the generated Deployment.
3. **An autoscaler owns replicas.** The higher-level object expresses bounds and policy; the autoscaler owns the changing replica field.

The unsound model is “all managers may write, and the last write wins.” That converts reconciliation into a contest.

Server-Side Apply exposes this issue through managed fields. If `atlas-controller` attempts to apply a field owned by `atlas-author`, the conflict is useful evidence. Forcing the conflict is not a normal repair; it is an explicit ownership transfer and should be justified as such.

### Resource version and field ownership solve different problems

`resourceVersion` protects a read-modify-write sequence from replacing an object that changed after it was read. Managed fields protect declarative field ownership. A client can satisfy the resource-version precondition and still overwrite a field it should not own if it uses an inappropriate update method. Conversely, two apply managers can conflict on one field while safely managing disjoint fields of the same object.

Use the mechanism that matches the invariant:

| Invariant | Primary mechanism |
|---|---|
| do not replace a newer object accidentally | resourceVersion precondition |
| preserve declarative ownership of individual fields | Server-Side Apply managed fields |
| prevent two controllers from controlling one child lifecycle | controller owner reference and design |
| preserve API compatibility | structural schema, defaulting, conversion, validation |
| delay deletion until owned external cleanup completes | finalizer |

## Deletion case — finalizers are durable obligations

Suppose an AtlasWorkload reserves an external release name. The controller adds `platform.bijux.dev/release-reservation` before creating the reservation. When deletion begins, the API server records a deletion timestamp but retains the object while the finalizer remains. The controller must:

1. observe deletion intent;
2. locate the exact reservation identity;
3. remove it idempotently or prove it is already absent;
4. record a condition if cleanup is blocked;
5. remove only its own finalizer.

Manual finalizer removal can be appropriate during a reviewed recovery, but it means accepting possible orphaned state. It is not the equivalent of successful cleanup.

## Common false conclusions

- **“Force apply fixes drift.”** It may merely seize another manager’s field.
- **“Generation changes on every update.”** Status-only and some metadata changes do not represent a new desired generation.
- **“Owner references authorize a controller.”** They express lifecycle relationships, not API authorization.
- **“Finalizers execute code.”** They only keep deletion pending; a controller must do the work.
- **“Replacing the whole object is simpler.”** It can erase fields owned by admission, controllers, or other clients.
