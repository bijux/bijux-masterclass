# Module 10 — Custom resources, controllers, and workload release

Kubernetes can be extended with new resource types and controllers. This power is often abused. A CustomResourceDefinition can turn an organization’s platform contract into a declarative API, but it can also create a second, poorly designed orchestration language with unclear ownership and irreversible lifecycle bugs.

The final question of Course 4 is:

> Does Atlas need a new API, and can its controller reconcile that API safely enough to become a platform capability?

## Start by trying not to create a custom resource

Use a built-in API when it expresses the invariant. Use a ConfigMap for passive configuration. Use a Job for finite work. Use a Deployment for interchangeable replicas. Use a policy engine for policy.

A custom resource is justified when:

- users need a stable domain-oriented declarative API;
- several lower-level objects must be composed consistently;
- status must summarize the domain capability;
- reconciliation requires domain knowledge;
- lifecycle and ownership are clear;
- the API can be versioned and supported.

It is not justified merely to shorten YAML or hide all Kubernetes concepts.

## AtlasWorkload is deliberately small

`platform.bijux.dev/v1alpha1, Kind=AtlasWorkload` expresses:

- released image references for API and worker;
- approved replica counts;
- configuration reference;
- resource profile;
- availability class;
- storage-interface reference;
- release identity.

It does not contain secret values, arbitrary Pod fragments, Gateway configuration, database administration, or GitOps workflow state.

The controller renders/owns:

- Deployments;
- ServiceAccounts;
- PodDisruptionBudget;
- a minimal Service contract for Course 5;
- status and conditions.

The user retains ownership of the AtlasWorkload spec. The controller owns generated child fields and status.

## CRD schema is an API contract

An `apiextensions.k8s.io/v1` CRD uses an OpenAPI v3 structural schema. The schema should define types, required fields, formats, list/map semantics, defaults where safe, and validation.

Unknown-field pruning prevents accidental storage of unsupported intent. Preserve-unknown-fields should be narrowly justified. Loose schemas move errors into controllers and make clients unreliable.

Atlas validates:

- image strings contain an immutable digest;
- replicas are within bounded ranges;
- release ID is non-empty;
- configuration reference has a valid name;
- availability values are internally consistent.

CEL validation rules can express cross-field invariants without a webhook. They should remain deterministic and comprehensible.

## Versioning: served and storage versions

A CRD can serve several versions but stores one version. Changing a storage version requires conversion and migration planning. Fields cannot simply be renamed without preserving old clients and stored objects.

Course 4 releases only `v1alpha1` as a course API and labels it non-production. The handoff records that Course 10 may redesign the platform API after Courses 5–9 establish connectivity, storage, delivery, security, and fleet requirements.

## Status and conditions

AtlasWorkload status includes:

```text
observedGeneration
apiReplicas
workerReplicas
availableApiReplicas
conditions: Accepted, Progressing, Available, Degraded
```

The controller updates status only when semantic content changes. Conditions use stable reasons. `Available=True` requires the current generation and the declared availability threshold.

A controller should not copy every child status field into the custom resource. Status is a domain summary, not a duplicate object database.

## Reconciliation algorithm

A safe reconciliation loop:

1. fetch the AtlasWorkload by key;
2. if absent, forget the key;
3. validate current desired state;
4. if deleting, run finalizer protocol;
5. calculate desired child objects from the spec and predecessor contract;
6. read current children;
7. apply only controller-owned fields;
8. observe child status;
9. calculate semantic AtlasWorkload status/conditions;
10. update status only if changed;
11. requeue only for known transient/time-based reasons.

The controller must survive duplicate queue items and process restart. It must not rely on a complete event sequence.

## Watch and work queue

A real controller lists resources, establishes a watch, and places keys into a rate-limited work queue. Watch events are hints to reconcile current state. The queue collapses repeated work and applies backoff after failure.

The included Go controller uses the Kubernetes HTTP API directly to keep the boundary visible. Production controllers commonly use client-go/controller-runtime, but framework details are not the conceptual spine.

## Child identity and ownership

Generated child names are stable:

```text
<atlasworkload-name>-api
<atlasworkload-name>-worker
```

The controller sets owner references and stable labels. It does not delete/recreate children on every reconcile. It uses server-side apply with one field manager for its owned fields.

The controller does not own external configuration objects or persistent claims supplied by reference. Deleting AtlasWorkload must not automatically delete independently owned data.

## Finalizer scope

AtlasWorkload uses a finalizer only for a small external release reservation in the semantic lab. Kubernetes child cleanup uses owner references. The finalizer is idempotent and can treat “already absent” as success.

A finalizer should never wait forever for a child that garbage collection already owns. It should report a stable Degraded reason when cleanup cannot progress.

## Avoid reconciliation loops caused by status

A common defect:

```text
reconcile
→ write current timestamp to status
→ status event
→ reconcile
→ write new timestamp
→ repeat forever
```

The fix is semantic equality and stable transition times. The controller computes desired status, compares it with current status, and writes only meaningful change.

Another loop occurs when two managers continuously overwrite the same child field. Managed-field ownership and release governance must resolve it; retry backoff only slows the fight.

## Controller permissions

The controller ServiceAccount needs:

- get/list/watch AtlasWorkloads;
- update status and finalizers as appropriate;
- get/list/watch/apply owned Deployments, ServiceAccounts, Services, and PDBs;
- events or leases if used.

It does not need cluster-admin. The RBAC scope should match namespaced ownership. Course 8 performs a full threat and policy review.

## Leader election and replicas

Multiple controller replicas improve availability only when they coordinate leadership or safely process the same queue. Leader election typically uses Lease objects. Course 4 includes the conceptual contract and a single-replica local controller; Course 9 owns operated high availability.

## Operator pattern and its limits

An operator combines custom resources and controllers to encode operational knowledge. The term does not guarantee quality. Review:

- API stability;
- reconciliation idempotency;
- upgrade/version skew;
- backup and restore;
- permissions;
- finalizers;
- status quality;
- support and incident behavior.

A controller that shells out to imperative scripts and stores all progress in logs is not made declarative by a CRD.

## API aggregation versus CRDs

The aggregation layer can add an extension API server with custom storage and behavior. It is justified when CRD/schema/controller capabilities are insufficient. It is operationally heavier. AtlasWorkload fits a CRD and controller; aggregation would be needless complexity.

## Workload release gate

Atlas Kubernetes Workload 1.0 is accepted only if:

1. predecessor digests and runtime guarantees match exactly;
2. manifests use supported stable APIs;
3. selectors and ownership graphs are valid;
4. no mutable image tag is used as deployment identity;
5. probes, resources, security context, and termination are explicit;
6. scheduling constraints are satisfiable under the declared profile;
7. worker durable paths remain a PVC interface, not emptyDir;
8. controller reconciliation is idempotent;
9. status observes the current generation;
10. Course 5 handoff is complete and no networking claim exceeds evidence.

## Rejected release examples

The course includes candidates rejected for:

- mutable image tag;
- root runtime;
- selector mismatch;
- liveness depending on a remote service;
- impossible topology spread;
- emptyDir substituted for durable worker state;
- controller force-owning user replicas;
- finalizer without cleanup evidence;
- status timestamp churn;
- networking marked production-ready without CNI/Gateway evidence.

## Course 5 handoff

The accepted release exports:

- namespace and workload object identities;
- stable labels and selectors;
- named container/Service ports;
- readiness and endpoint-eligibility contract;
- expected in-cluster DNS names;
- external HTTPS exposure requirement;
- worker egress dependencies;
- topology/failure-domain assumptions;
- unresolved CNI, DNS, NetworkPolicy, Gateway, TLS, cloud LB, egress, and mesh evidence;
- exact version ledger.

Course 5 can now engineer connectivity without reverse-engineering workload intent.

## Final defense

The learner must defend one complete path:

```text
AtlasWorkload generation
→ admitted CR
→ controller desired children
→ Deployment/ReplicaSet/Pod ownership
→ scheduler placement
→ kubelet lifecycle
→ readiness/availability status
→ Course 5 endpoint contract
```

For every arrow, name the owner, object, retry behavior, evidence, and unresolved environment dependency.

## Capstone completion

`capstone/controller-go/` compiles a small direct-API controller core. `atlas_kube/controller.py` provides a deterministic semantic reconciler. The release corpus includes accepted, rejected, review-required, and not-executed candidates. The handoff manifest verifies exact Course 5 inputs.

## Further reading

- Custom resources: <https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/>
- CRD task guide: <https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/>
- Operator pattern: <https://kubernetes.io/docs/concepts/extend-kubernetes/operator/>
- API conventions: <https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md>

## Course conclusion

Course 3 produced trusted workload artifacts. Course 4 made their desired runtime state declarative and continuously reconciled. Course 5 can now focus on how ready Pods become reachable services and how traffic crosses cluster, tenant, and external boundaries.

## Worked controller review — useful abstraction or hidden platform?

The `AtlasWorkload` custom resource accepts image digests, replica intent, availability class, configuration references, and storage requirements. Its controller renders Deployments, ServiceAccounts, a ConfigMap reference, and a PodDisruptionBudget.

This can reduce repeated policy decisions, but only if the abstraction has a narrow authority boundary. Review it through four tests.

### 1. Does it encode a stable domain of platform intent?

“Run an Atlas workload with this release identity and availability class” is more stable than “create these seven Kubernetes objects.” The API should expose outcomes developers understand and keep implementation fields out unless users truly need them.

### 2. Can its controller own the generated fields without conflict?

The controller owns child templates, selectors, security context, and status. The user owns the custom resource fields. It must not seize fields in independently managed objects. Generated children should be clearly labelled and controller-owned.

### 3. Can the API evolve safely?

A CRD is a long-lived API. Structural schemas, defaulting, pruning, conversion, and version storage matter. `v1alpha1` signals instability; it does not excuse destructive changes. Stored objects can outlive controller binaries. A release must test old objects against new controllers and, before conversion webhooks are introduced, define the supported upgrade path explicitly.

### 4. Can operators diagnose and recover it?

Conditions must distinguish invalid input, blocked dependency, degraded child, and ready state. Status writes should occur only when semantic observation changes. Finalizers must have bounded, idempotent cleanup. Metrics, events, logs, and runbooks should identify the owning controller and failed transition.

## Status design

Atlas conditions use:

- stable `type` values such as `Ready`, `Progressing`, and `Degraded`;
- boolean status;
- machine-readable reason;
- concise human message;
- observed generation;
- transition time changed only when condition status changes.

Writing the current timestamp on every reconcile creates an infinite write/watch loop. Comparing semantic status before update is therefore a correctness property, not merely a performance optimization.

## Final release boundary

Course 4 release approval proves:

- exact Course 3 image subjects remain pinned;
- workload objects satisfy the Course 4 static and semantic policy;
- controller convergence is idempotent in the dependency-light proof;
- optional local-cluster evidence is correctly classified;
- network and storage assumptions are exported rather than silently claimed;
- Course 5 receives exact service, port, endpoint, identity, topology, and deferred-evidence contracts.

It does not prove production networking, persistent-volume durability, managed-cluster behavior, or fleet operation.

## Common false conclusions

- **“A CRD makes Kubernetes understand the domain.”** Only the controller and surrounding policy give the API meaning.
- **“More fields make the abstraction flexible.”** They often leak implementation and freeze accidental design.
- **“Finalizer means cleanup is guaranteed.”** It guarantees deletion remains blocked until someone removes the finalizer.
- **“Controller writes prove progress.”** Repeated no-op writes can indicate a broken control loop.
- **“An operator should own every resource.”** Native controllers and simple manifests remain preferable when they express the invariant clearly.
