---
module_id: PLAT-023
program: Platform Engineering
level: 1
module_number: 23
title: Kubernetes Declarative Resources
status: complete
last_verified: 2026-09-02
---

# Kubernetes Declarative Resources

## One-Page Review

### Governing question

How should a platform use Kubernetes resources as durable records of intent and observation while preserving field ownership, concurrency, lifecycle, versioning, and honest evidence across many independent reconcilers?

### Essential definitions

- A **resource type** is an API group, version, and resource with a scope, schema, operations, and behavior; a **kind** names the object representation returned by the API.
- An **object** is one occurrence of a resource type, identified during its lifetime by API group/resource, namespace where applicable, name, and server-assigned UID.
- **spec** is user- or controller-supplied desired state; **status** is controller-supplied observation about current state and progress.
- **reconciliation** is repeated comparison of desired and observed state followed by bounded action and updated evidence.
- **generation** is an API-maintained counter for desired-state changes where the resource semantics define it; **observed generation** states which generation a controller's status reflects.
- **resourceVersion** is an opaque API concurrency token, not a timestamp, sequence shared across clusters, or business version.
- A **field manager** is the identity recorded by server-side apply as asserting ownership of particular fields.
- A **condition** is a structured status observation with type, status, reason, message, transition time, and commonly observed generation.
- A **finalizer** is a qualified key that delays physical deletion until responsible cleanup is complete; it is not executable code.
- An **owner reference** binds a dependent to a particular owner UID for garbage-collection semantics; labels express selectable attributes, not ownership.

### Central model, mechanism, or theorem

Model an object contract as $O=(I,D,V,F,R,L,E,X)$: lifetime identity $I$, desired state $D$, validation/defaulting $V$, field ownership and concurrency $F$, reconciliation/status $R$, lifecycle/relationships $L$, evidence and observability $E$, and extension/version policy $X$. A controller processes a level-based snapshot, computes a bounded plan, performs idempotent operations, and publishes status for the generation it actually observed. Convergence is conditional on satisfiable intent, stable dependencies, fair retries, exclusive or coordinated ownership, and recoverable effects; declarative syntax alone proves none of these.

### Critical invariants

- Object identity uses UID when lifetime matters; name reuse never makes a replacement object the same occurrence.
- `apiVersion` and schema are resolved before mutation; unknown, duplicate, pruned, defaulted, and converted fields are visible in validation and tests.
- Spec writers, status writers, defaulting, admission, and controllers have explicit field boundaries and least-privilege authorization.
- Server-side apply conflicts are investigated; force transfers only intended fields under named authority.
- Status never claims a generation that was not reconciled, and `Ready=True` never substitutes for resource-specific outcome evidence.
- Reconciliation is level-based and idempotent: events prompt work, while current state—not a presumed event history—drives decisions.
- Owner references use valid scope and UID; selectors do not establish deletion ownership.
- Finalizers are added before dependent effects, make deletion resumable, and are removed only after cleanup or an authorized compensating decision.
- Custom resources use structural schemas, status separation, version/conversion policy, compatibility tests, and stored-version migration.
- Configuration promotion identifies exact rendered intent and cluster context without storing plaintext secrets or assuming every cluster is identical.

### Common failures

Treating YAML as an execution script; using names instead of UIDs for ownership; editing status as desired state; reading stale status without observed generation; treating resourceVersion as time; replacing whole objects; mixing apply managers; forcing all conflicts; encoding mutable data in labels; using annotations as an unbounded database; overlapping selectors; cross-namespace owner references; adding finalizers after external creation; deleting finalizers blindly; controllers depending on every event; hot retry loops; unstructured CRDs; changing schemas without conversion; and calling API acceptance successful reconciliation.

### Compact example

A `DatabaseClaim` generation 7 requests class `regional`, capacity `100Gi`, and deletion policy `SnapshotThenDelete`. Admission defaults an allowed backup window and validates capacity. A platform manager owns class and policy fields; the application manager owns capacity. The controller observes generation 7, creates an external database with an idempotency key containing the claim UID, and reports `Provisioned=True`, endpoint evidence, and `Ready=True` with observed generation 7. On deletion, the existing finalizer snapshots and verifies recovery metadata before deleting the external database and removing itself. A recreated claim with the same name receives a new UID and cannot adopt the old database accidentally.

### Connections

Retrieve declarative interface principles from [PLAT-015](015-apis-and-declarative-resources.md), error and lifecycle evidence from [PLAT-018](018-feedback-and-error-diagnostics.md), compatibility from [PLAT-019](019-golden-path-versioning.md), measurement from [PLAT-020](020-measuring-developer-experience-without-vanity-metrics.md), image identity from [PLAT-021](021-container-images-as-platform-artifacts.md), and runtime enforcement from [PLAT-022](022-runtime-isolation-and-resource-controls.md).

## Governing Question

Which desired fields may each actor assert, which controller owns each effect, how is current truth reported for the right generation, and how do creation, conflict, partial failure, deletion, and API evolution remain recoverable?

Kubernetes objects are records of intent. They persist desired configuration and observed status through an API that supplies identity, schemas, concurrency, watch streams, authorization, and lifecycle machinery. Controllers turn those records into effects. This separation enables automation, but also distributes authority: users, apply clients, admission, built-in controllers, custom controllers, and operators may touch one object.

Declarative does not mean side-effect free or automatically convergent. A controller can leak cloud resources, fight another manager, report stale readiness, wedge deletion, or repeat a non-idempotent call. The object contract must make these risks explicit.

## Why This Matters

Platform APIs often use Kubernetes as their control plane because it already offers durable resources, watches, namespaces, RBAC, admission, status, and extension. A service team can request an outcome while a platform controller manages provider details. Git-based review can promote desired state. Other controllers can compose around labels, ownership, and status.

The same leverage magnifies ambiguity. YAML makes a request look complete before defaulting and mutation. `kubectl get` can show an object that no controller can realize. A successful apply reports API persistence, not workload or business success. Two field managers can express incompatible intent. Deletion can remain pending while external infrastructure leaks or cleanup authority disappears.

Durable resource design therefore resembles public API and distributed-systems design. It requires stable identity, schemas, conflict ownership, state machines, idempotency, compatibility, evidence, and recovery.

## Prerequisites and Retrieval

Retrieve HTTP resources, JSON/YAML, schemas, optimistic concurrency, watches, idempotency, retries, distributed reconciliation, state machines, garbage collection, version conversion, access control, admission, Git workflows, secrets, and platform product boundaries.

You should understand Kubernetes API groups and versions, namespaces, labels/selectors, controllers, CRDs, JSON merge behavior, structured status, eventual consistency, partial failure, and external resource lifecycles.

## Learning Objectives

After completing this module, you should be able to:

1. identify Kubernetes resource types and object lifetimes precisely;
2. separate desired spec, defaulted stored representation, controller status, and external truth;
3. use generation, observed generation, UID, resourceVersion, and conditions correctly;
4. choose create, update, patch, or server-side apply with explicit field managers and conflict policy;
5. design labels, annotations, selectors, owner references, finalizers, and deletion behavior;
6. implement level-based idempotent reconciliation with bounded retries and status evidence;
7. define structural CRD schemas, subresources, versions, conversion, compatibility, and storage migration; and
8. promote rendered configuration across clusters with validation, drift ownership, secret safety, and rollback evidence.

## Core Exposition

### Identify a resource and an object

API discovery maps group, version, and resource to supported operations, scope, kinds, and media. `apps/v1` in a manifest combines group `apps` and version `v1`; core `v1` omits a group prefix. The plural resource used in URLs is not always a mechanical lowercase plural of kind.

An object's address includes resource type, namespace if namespaced, and name. Its UID distinguishes one lifetime from a later object that reuses the name. Use UID in external idempotency keys, ownership, audit, and adoption checks. A controller seeing the same name with a different UID must treat it as replacement.

`resourceVersion` represents the version of API state used for concurrency and watch semantics. Treat it as opaque. Send a current token when an update must fail rather than overwrite a concurrent change. Do not sort business events across clusters by it.

### Separate intent, observation, and external truth

Spec expresses what should be true. Status describes what controllers observed and accomplished. External systems retain their own truth. These can disagree temporarily or permanently: the API accepts desired capacity, the provider request is pending, and the database remains smaller.

Use the status subresource so spec writers cannot forge status and status writers do not overwrite spec. Status writes should not increment desired generation. A controller records the generation it reconciled; readers compare `status.observedGeneration` or condition-level equivalents with `metadata.generation` before trusting results.

Define conditions around meaningful questions: accepted, dependencies ready, provisioned, degraded, ready, deletion blocked. Each condition includes stable type, tri-state status where applicable, machine reason, human message, transition time, and observed generation. Do not encode a chronological log in conditions or make reason strings an undocumented API.

`Ready=True` means only what the resource contract defines. A platform claim may also need endpoint reachability, policy compliance, backup evidence, or a consumer task outcome.

### Understand the write pipeline

A request passes authentication, authorization, mutating admission and defaulting in defined API-server behavior, schema and validating admission, storage conversion, persistence, and watch publication. Exact order has nuances by operation and implementation; design tests against supported Kubernetes versions rather than relying on folklore.

Defaulting reduces repetition but changes the stored object. Defaults should be safe, stable, documented, and visible through dry run. A new default can change behavior for clients that omitted a field, so version it as API behavior.

Validation rejects structurally invalid or unsafe intent before a controller sees it. Use OpenAPI/CEL constraints for local invariants and admission for cross-resource or organization policy where necessary. Avoid network-dependent admission when failure policy and latency cannot be made safe.

Server-side field validation detects unknown or duplicate fields under configured strictness. Treat warnings as migration work; silently ignored misspellings turn desired safety controls into absent fields.

### Choose mutation semantics deliberately

Create establishes a new object and fails on an existing name. Replace/update submits a complete representation and uses resourceVersion for optimistic concurrency; careless clients can erase fields they did not preserve. Patch changes selected content, but JSON Patch, JSON Merge Patch, strategic merge, and apply have different list and deletion semantics.

Server-side apply lets a named field manager assert a partial desired configuration. The API records managed fields. If one manager changes a field another manager owns to a different value, apply reports conflict. Conflict is coordination evidence, not an inconvenience to suppress.

Resolve conflict by relinquishing a field, aligning managers on the same value, changing authority, or deliberately forcing ownership of exact reviewed fields. Never use a generic manager name shared by unrelated automation. Do not edit `managedFields` manually.

An update can transfer ownership without producing apply-style conflict, so controllers should update only their owned subresource or narrow fields. Prefer status subresource updates for controllers and apply for cooperative desired configuration when schema supports it.

### Model field ownership

Create a table of actor, field set, mutation method, authority, and conflict response. An application team may own image digest and service capacity. Platform policy may own runtime class and mandatory labels. An autoscaler may own replicas. A controller owns status. Admission may default a field only when absent.

Avoid two continuous reconcilers owning the same desired field. If human and automation alternate, make the mode explicit: autoscaling enabled transfers replicas authority; disabling it returns authority after a handoff. Otherwise each controller “repairs” the other's valid update.

List fields require schema-aware ownership. Associative lists keyed by name can let managers own separate elements; atomic lists make the whole list one field. CRD markers determine this behavior and are compatibility decisions.

### Use metadata by semantic role

Labels are small identifying attributes intended for equality/set selection and organization. Use stable keys such as application, component, owner, environment class, and managed-by. Selector semantics become API contracts: a changed or overlapping selector can adopt unintended objects.

Annotations hold non-identifying metadata such as provenance references, tool hints, or external correlation. They are strings and are included in object size and API traffic. Do not store secrets, unbounded logs, large state, or authoritative external records in annotations.

Names are human and API identity within scope. `generateName` helps create unique occurrences but does not replace a durable owner UID. Namespace is an administrative and naming boundary, not by itself a complete security boundary.

### Design selectors safely

A selector identifies a set at evaluation time; it does not remember why a label was assigned. Make controller selectors immutable where the resource contract requires and ensure peer controllers cannot overlap unexpectedly. Admission can enforce ownership labels and selector disjointness within a platform domain.

Do not use mutable business status as selector identity if reassignment would cause destructive adoption. Separate identity labels from observation annotations/status. A Service may select pods by labels, but garbage collection uses owner references—not the selector.

When migrating labels, support old and new query paths or stage object relabeling before selector change. Test zero-match and overmatch outcomes.

### Reconcile levels, not event stories

Watches and queues tell a controller that something may have changed. Events can be duplicated, delayed, coalesced, or missed across restart. Reconciliation reads the current object and dependencies, computes the desired level, and acts idempotently.

Use a key such as namespace/name to enqueue, then re-fetch and verify UID. Handle not-found as a legitimate deletion outcome. Cache reads can be stale; use API reads or expectations where an immediate decision requires stronger freshness.

The controller loop should be restartable between any two effects. Derive external idempotency keys from object UID and purpose. Discover whether an effect already exists before creating another. Record external identity in durable status only after validating ownership.

Return bounded errors and requeue with backoff. A permanent invalid spec should publish a condition and wait for generation change, not hot-loop. Transient provider failure should retain progress and retry. Successful reconciliation can still requeue for renewal or drift checks.

### Publish honest status

Set status from observations, not intended next steps. Preserve last known good endpoint separately from a condition saying current verification failed. Use concise conditions plus typed fields for stable machine data; keep verbose diagnostics in events/logs with correlation.

The following synthetic classifier prevents stale status from being called current.

<!-- bijux-verify: {"id":"kubernetes-resource-status-classifier","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"objects=6\ncurrent_ready=2\nstale_status=2\ncurrent_not_ready=1\ndeleting=1\nreplacement_uids=2\n","stderr":""}} -->
```python
objects = [
    {"name": "api", "uid": "u1", "generation": 3, "observed": 3, "ready": True, "deleting": False},
    {"name": "worker", "uid": "u2", "generation": 5, "observed": 4, "ready": True, "deleting": False},
    {"name": "cache", "uid": "u3", "generation": 2, "observed": 2, "ready": False, "deleting": False},
    {"name": "report", "uid": "u4", "generation": 7, "observed": 6, "ready": False, "deleting": False},
    {"name": "old", "uid": "u5", "generation": 1, "observed": 1, "ready": True, "deleting": True},
    {"name": "api", "uid": "u6", "generation": 1, "observed": 1, "ready": True, "deleting": False},
]
active = [obj for obj in objects if not obj["deleting"]]
current = [obj for obj in active if obj["generation"] == obj["observed"]]
print(f"objects={len(objects)}")
print(f"current_ready={sum(obj['ready'] for obj in current)}")
print(f"stale_status={sum(obj['generation'] != obj['observed'] for obj in active)}")
print(f"current_not_ready={sum(not obj['ready'] for obj in current)}")
print(f"deleting={sum(obj['deleting'] for obj in objects)}")
print(f"replacement_uids={len({obj['uid'] for obj in objects if obj['name'] == 'api'})}")
```

The fixture treats deletion as a separate lifecycle and namesake UIDs as separate occurrences. It does not model multiple conditions, missing observed generation, API watch consistency, or actual controller success.

### Coordinate ownership and garbage collection

An owner reference contains API version, kind, name, UID, controller flag, and block-owner-deletion behavior. The UID prevents a new namesake from owning an old dependent accidentally. Namespaced dependents can refer to valid owners only under Kubernetes scope rules; invalid cross-namespace relationships are not a portable ownership mechanism.

Set one controlling owner reference for resources a controller exclusively manages. Use labels for queries and additional relationships, not deletion authority. Before adopting an orphan, verify type, UID history, labels, annotations, external identity, and absence of another controller.

Choose foreground, background, or orphan deletion according to consequence. Garbage collection handles API dependents, not external databases, DNS records, cloud roles, or data unless a controller owns those effects.

### Make finalization recoverable

Add the finalizer before creating an external effect so deletion cannot race ahead of cleanup. On deletion, `deletionTimestamp` becomes immutable and the object remains while finalizers exist. Reconciliation enters a deletion branch and stops creating normal resources.

Cleanup must be idempotent and resumable. Treat external not-found as success only after verifying identity and deletion semantics. Record progress and blockers. Do not remove the finalizer until cleanup, transfer, or an explicitly authorized compensating action satisfies the contract.

A dead finalizer can wedge deletion indefinitely. Monitor age, reason, responsible controller health, and external dependency. A break-glass removal procedure must understand and perform or accept the missed cleanup, preserve evidence, and name authority. Blind removal converts a visible problem into an invisible leak.

### Define CRDs as public APIs

A CRD needs a structural OpenAPI schema in `apiextensions.k8s.io/v1`. Declare types, required fields, bounds, enums, list/map semantics, defaults, and CEL validation. Unknown fields are generally pruned unless explicitly preserved, which means schema omissions can destroy intent.

Enable the status subresource so controllers can update status without spec. Enable scale only when replica paths and selector semantics are genuine. Add printer columns for useful discovery, not as a substitute for structured status.

Names, field meaning, defaults, mutability, validation, conditions, and deletion behavior are public contracts. A field called `region` cannot later mean availability zone. Prefer intent-level fields over provider-specific knobs; expose an escape mechanism separately when required.

### Version, convert, and migrate storage

CRD versions declare which representations are served and which one is storage. Conversion must preserve meaning across round trips. A webhook conversion is availability- and security-critical API infrastructure; version, scale, observe, and test it before serving dependent resources.

Adding an optional field can still change defaults or controller behavior. Removing enum values, narrowing bounds, changing list type, making optional required, or changing ownership semantics can break stored objects and apply managers.

Migrate stored objects through the new storage version and confirm `status.storedVersions` no longer lists the old version before removing it. Test old clients, new clients, conversion, defaulting, managed fields, status, backup/restore, and deletion. API-version removal is a lifecycle event, not only a schema edit.

### Compose resources without creating hidden transactions

A platform claim may reconcile Deployments, Services, policies, credentials, DNS, and cloud resources. Kubernetes does not make that graph one transaction. Publish partial progress, ownership, ordering constraints, and rollback/forward recovery.

Prefer one aggregate intent resource with clearly owned dependents when the lifecycle is inseparable. Prefer independent resources when teams need separate authority and lifecycle. Avoid a giant custom resource whose every field triggers unrelated controllers and conflicts.

Cross-controller dependencies should be expressed through stable references and conditions, with cycle detection and timeout. Do not depend on creation order in a YAML file. Apply order is not readiness order.

### Promote configuration safely

Store reviewable source intent in version control, render deterministically, validate against the target API and policy, and record source revision plus rendered digest. Pin image and external artifact identities. Keep plaintext secrets outside Git and manifests; reference a governed secret delivery mechanism.

Overlays should express legitimate environment differences, not copy entire objects. Validate the final rendered object because patches can delete required fields, change selectors, or transfer ownership. Server-side dry run exercises supported defaulting, validation, and admission without persistence, while still depending on target availability and side-effect-safe admission.

Promotion does not mean identical clusters. Record supported API versions, CRDs, admission, runtime classes, storage classes, and policy. Gate or adapt explicitly. Use the same field manager across the same authority, not across unrelated tools.

### Detect and resolve drift

Define drift as a difference between an actor's declared fields and live owned fields, not any live difference. Controllers legitimately update status and dependent objects; admission defaults fields; autoscalers change replicas. A naive textual diff produces noise and unsafe reversions.

Use managed fields, normalized schemas, and ownership rules. Classify drift as expected controller state, defaulting, authorized emergency change, conflicting ownership, unsupported mutation, or stale source. Resolve by updating source, transferring field ownership, removing the mutation, or recording a time-bounded exception.

Never make the Git reconciler force every conflict automatically. A live emergency change can be safety-critical evidence. Freeze, investigate, and reconcile authority before overwriting.

### Observe and test the control plane

Measure API request errors/latency, admission decisions, watch restarts, queue depth, reconciliation duration and result, retry age, generation lag, status freshness, finalizer age, orphan count, conversion failures, apply conflicts, and external side-effect inventory. High reconcile count alone is neither good nor bad.

Test create, no-op repeat, update, conflicting apply, deletion during provisioning, controller restart after each effect, provider timeout with unknown outcome, namesake recreation, stale cache, conversion round trip, old stored objects, invalid/unknown fields, and target-cluster dry run.

Audit records actor, manager, operation, resource identity/UID, old/new intent where permitted, policy decision, and correlation. Protect secrets and sensitive status while retaining enough evidence for incident reconstruction.

## Definitions and Notation

Let resource type $K=(g,v,r,s)$ contain API group $g$, served version $v$, plural resource $r$, and scope $s\in\{\text{namespaced},\text{cluster}\}$. Let object lifetime identity be $I=(g,r,n,x,u)$ for resource group/type, namespace $n$ where applicable, name $x$, and UID $u$.

For object $o$, let desired generation be $G(o)$ and a condition's observed generation be $\widehat{G}_c(o)$. Condition $c$ is current only if $\widehat{G}_c(o)=G(o)$ and its other evidence remains within the resource contract.

Let manager $m$ assert field set $F_m(o)$. An apply conflict exists when manager $m_1$ proposes a different value for field $f\in F_{m_2}(o)$ without shared ownership or authorized transfer. Force is an ownership transfer operation, not a merge strategy.

Let reconcile function $\rho(D_t,A_t)=(P_t,S_t)$ map desired snapshot $D_t$ and observed actual state $A_t$ to bounded plan $P_t$ and status $S_t$. Idempotency requires repeated execution against the resulting level not to duplicate effects; convergence additionally requires environmental assumptions.

## Mechanisms, Invariants, or Proof Structure

The resource path is discovery and version selection $\rightarrow$ authentication/authorization $\rightarrow$ defaulting/admission/validation $\rightarrow$ persisted desired state $\rightarrow$ watch/queue hint $\rightarrow$ level-based reconcile $\rightarrow$ idempotent external effects $\rightarrow$ status for observed generation $\rightarrow$ update, conflict, deletion/finalization, conversion, or retirement.

Forward traceability maps each desired field to owner, validator, controller behavior, dependent effects, status, and deletion. Backward traceability maps each external object to source UID, generation, controller, idempotency key, and policy.

Invariants are lifetime identity, validated representation, narrow field ownership, explicit conflict transfer, generation-honest status, level-based idempotency, UID-valid ownership, finalizer-before-effect, compatible version conversion, deterministic promotion, and classified drift.

No theorem guarantees convergence. Unsatisfiable intent, competing managers, permanent provider failure, lost authority, conversion bugs, and non-idempotent effects can prevent it. Status must expose those conditions.

## Alternatives and Trade-Offs

**Built-in resource versus CRD:** built-ins offer mature semantics; CRDs offer platform intent and Kubernetes integration but create a public API and controller lifecycle.

**Apply versus update:** apply coordinates partial field ownership and conflicts; update is simpler for one exclusive owner but risks replacing unrelated fields. Use status subresources for status.

**Defaulting versus explicit configuration:** defaults reduce burden but hide stored changes and can alter omitted-field behavior. Explicit values improve review at the cost of verbosity. Publish safe defaults and render them in previews.

**Admission versus reconciliation validation:** admission rejects early but adds API-path latency and availability risk. Reconciliation can evaluate external facts asynchronously but accepts an object that may remain unfulfilled. Use each for the guarantee it can sustain.

**Owner references versus finalizers:** ownership garbage-collects API dependents; finalizers coordinate pre-deletion work and external effects. They complement rather than replace each other.

**Aggregate versus composable resources:** aggregates simplify a journey and inseparable lifecycle; composable primitives preserve independent authority. Choose by ownership and failure boundary.

**Git desired state versus direct API:** Git adds review and reproducibility; direct changes support emergencies and interactive workflows. Define field authority and reconciliation rather than denying one exists.

**Conversion webhook versus new type:** conversion preserves one conceptual resource across versions but becomes critical infrastructure. A new type is explicit when semantics truly differ but requires migration and dual lifecycle.

## Failure Modes and Misconceptions

- **“YAML is declarative.”** Declarative behavior comes from API and controller contracts, not serialization syntax.
- **“Created means ready.”** API persistence precedes reconciliation and outcome evidence.
- **“Name identifies the resource forever.”** A recreated namesake has a different UID and lifetime.
- **“resourceVersion is a timestamp.”** It is an opaque concurrency/watch token.
- **“Ready is current.”** Compare observed generation and evidence freshness.
- **“Force apply resolves drift.”** It transfers ownership and can erase another actor's legitimate intent.
- **“Labels own dependents.”** Owner references govern garbage collection; selectors only identify current matches.
- **“Finalizers prevent deletion.”** They delay physical removal after deletion begins; they require a live cleanup controller.
- **“Watch delivers every event once.”** Controllers reconcile current levels and tolerate replay, gaps, and restart.
- **“A schema is documentation.”** It drives validation, pruning, defaulting, apply semantics, and compatibility.
- **“Git is the whole truth.”** Live defaults, status, emergency ownership, secrets, and external state remain.
- **“One apply file is transactional.”** Independent resources and external effects reconcile separately.

## Worked Examples

### Example 1

A controller sees `payments` with UID `u2`; its external database is labeled with old UID `u1`. It refuses adoption and reports an identity conflict instead of attaching a namesake to old data.

### Example 2

An autoscaler and Git manager both own `spec.replicas`. Apply conflicts reveal the design error. Enabling autoscaling removes replicas from Git's asserted fields; disabling it performs an explicit handoff.

### Example 3

Generation 9 status says `Ready=True` but observed generation is 8. The portal shows “reconciling generation 9” and retains the older endpoint as last-known evidence rather than declaring success.

### Example 4

A misspelled `readOnlyRootFilesytem` field yields strict validation failure. Warning-only validation would have stored intent without the safety control; the pipeline treats warnings as failure for promotion.

### Example 5

A controller times out creating a DNS record. On retry it queries by UID-derived idempotency key before creating, avoiding a duplicate after an unknown provider outcome.

### Example 6

A selector change would overlap another controller's pods. Admission rejects it and requires staged labels plus disjoint selector verification.

### Example 7

Deletion starts during external provisioning. Because the finalizer existed first, the controller enters deletion mode, discovers any partially created resource, cleans it idempotently, and then removes the finalizer.

### Example 8

A conversion webhook preserves an old enum but maps a new field lossy on round trip. Compatibility tests block serving the new version until conversion preserves meaning.

### Example 9

An emergency live change transfers one network-policy field to an incident manager. Git reconciliation stops on conflict; after review, source incorporates the change and ownership returns explicitly.

### Example 10

A cluster lacks the required CRD version and runtime class. Server-side dry run and capability inventory block promotion before any partial workload graph is created.

## Cross-Program Connections

API engineering contributes resource identity, versions, schemas, validation, errors, concurrency, idempotency, compatibility, and deprecation. Distributed systems contributes reconciliation, watches, retries, partial failure, eventual consistency, leader election, and convergence assumptions.

Data engineering contributes schema evolution, storage versions, conversion, lineage, migration, and backup/restore. Software engineering contributes state machines, property testing, Git workflows, rendering, and ownership boundaries. Security contributes authentication, RBAC, admission, secrets, audit, and least privilege.

Reliability contributes conditions, retry/backoff, finalizer age, unknown outcomes, recovery, and control-plane objectives. Product engineering contributes intent-level APIs, defaults, user journeys, escape routes, and outcome evidence.

## References

- Kubernetes Project, [*Objects in Kubernetes*](https://kubernetes.io/docs/concepts/overview/working-with-objects/), current documentation retrieved September 2, 2026. Object intent, spec/status, required fields, manifests, server-side validation, and API interaction.
- Kubernetes Project, [*Kubernetes API Concepts*](https://kubernetes.io/docs/reference/using-api/api-concepts/), current documentation retrieved September 2, 2026. Resource types, operations, resourceVersion, concurrency, watches, collections, deletion, dry run, and field validation.
- Kubernetes Project, [*Server-Side Apply*](https://kubernetes.io/docs/reference/using-api/server-side-apply/), current documentation retrieved September 2, 2026. Field managers, managed fields, conflicts, forced transfer, shared ownership, schema merge semantics, and migration.
- Kubernetes Project, [*Object Names and IDs*](https://kubernetes.io/docs/concepts/overview/working-with-objects/names/), current documentation retrieved September 2, 2026. Names, scope, API versions, UIDs, and object-lifetime identity.
- Kubernetes Project, [*Labels and Selectors*](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/), current documentation retrieved September 2, 2026. Label syntax, equality/set selectors, API query use, and non-overlapping controller selectors.
- Kubernetes Project, [*Annotations*](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/), updated June 26, 2026. Non-identifying metadata, key/value syntax, reserved prefixes, arbitrary string values, and size constraints.
- Kubernetes Project, [*Owners and Dependents*](https://kubernetes.io/docs/concepts/overview/working-with-objects/owners-dependents/), current documentation retrieved September 2, 2026. UID owner references, controlling ownership, deletion blocking, scope, and garbage collection.
- Kubernetes Project, [*Finalizers*](https://kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/), updated April 27, 2025. Deletion timestamps, qualified finalizer keys, cleanup, owner interaction, and cautions on manual removal.
- Kubernetes Project, [*Extend the Kubernetes API with CustomResourceDefinitions*](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/), current documentation retrieved September 2, 2026. Structural schemas, pruning, validation, defaults, status/scale subresources, categories, and selectable fields.
- Kubernetes Project, [*Versions in CustomResourceDefinitions*](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definition-versioning/), updated 2026. Served/storage versions, conversion, webhook behavior, storage migration, and `storedVersions` retirement.
- Kubernetes Project, [*Custom Resources*](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/), current documentation retrieved September 2, 2026. CRD versus aggregation choice, API access, storage, discovery, subresources, and declarative API considerations.
- Kubernetes Community, [*API Conventions*](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md), current conventions retrieved September 2, 2026. Spec/status, metadata, conditions, references, lists, naming, compatibility, and declarative API conventions.

## Exercises

### Exercise 1

Design a `CacheClaim` CRD and controller contract. Include identity, spec, defaults, schema, field managers, status/conditions, external idempotency, dependents, finalizer, versions, conversion, storage migration, and evidence.

### Exercise 2

Resolve conflicts among Git, a platform policy manager, an autoscaler, admission, and a controller over image, replicas, runtime class, labels, defaults, and status. Define mutation methods and handoffs.

### Exercise 3

Design reconciliation for an external DNS resource across create timeout, duplicate events, stale cache, controller restart, spec update, provider drift, deletion during creation, and namesake recreation.

### Exercise 4

Plan a CRD migration from `v1alpha1` to `v1` that renames fields, tightens validation, changes a list from atomic to map semantics, adds status, and removes an enum value.

### Exercise 5

Transfer the declarative model to municipal building-permit workflows. Address applicant intent, review status, identity, concurrent authorities, evidence, dependencies, amendments, withdrawal, deletion/retention, versioning, and human authority.

## Answers to the Exercises

### Answer 1

Define `cacheclaims.platform.example` as namespaced with UID-bound external identity. Spec includes intent-level class, capacity, availability, backup, access, and deletion policy; admission defaults only safe documented values and validates bounds and combinations through structural OpenAPI/CEL. Application manager owns capacity/access, platform manager owns class/policy constraints, and controller owns `/status`. Conditions include Accepted, Provisioned, BackupReady, Degraded, and Ready with observed generation; typed status records external ID, endpoint reference, capacity, and last verification. Add the finalizer before provider creation, use claim UID plus purpose as idempotency key, create owned API credentials/policies with owner references, and make create/update/delete restartable. Start with a served/storage version whose semantics can be supported; new versions require round-trip conversion, old/new client and managed-field tests, storage migration, and `storedVersions` verification. Evidence distinguishes API acceptance, provider completion, endpoint tests, backup restore, and consumer task success.

### Answer 2

Git's named server-side manager owns image digest, baseline capacity, and application labels. The platform manager owns runtime class, mandatory security/resource fields, and qualified platform labels through a separate apply identity. Admission defaults absent safe fields but does not continuously own them or overwrite explicit values. The autoscaler owns replicas only while autoscaling mode is enabled; Git omits replicas then. Disabling autoscaling first stops the controller and transfers replicas through an explicit apply. The resource controller writes only `/status` and owned dependents. Apply conflicts stop promotion and identify field managers; force is allowed only for reviewed authority transfer of named fields. Shared labels can share ownership only when values agree. Schema list/map semantics are tested. Status is protected by subresource RBAC, and no desired-state manager uses whole-object update.

### Answer 3

Queue namespace/name on any relevant watch, re-fetch, and verify UID. For creation, add finalizer first, derive a provider idempotency key from UID, and query by that key before create. A timeout yields Unknown/Pending status and retry with backoff, never an immediate second create. After restart or duplicate events, current API and provider levels drive the same plan. If cache freshness is insufficient for adoption/deletion, read directly. Spec updates use generation and update the same UID-owned DNS record only after validating immutable fields. Provider drift is classified: repair controller-owned fields, report provider policy changes, and never adopt an unowned record by name alone. If deletionTimestamp appears during create, stop normal reconciliation, discover any result, delete the exact UID-owned record, verify absence, and remove the finalizer. A namesake with a new UID gets a new key and cannot claim the old record. Status always names observed generation and last verified provider state.

### Answer 4

Inventory every stored object, client, manager, webhook, backup, and controller. Serve alpha and v1 concurrently while retaining alpha storage initially. Define a conversion hub that preserves renamed fields and old enum meaning round trip; do not remove a value until all objects and clients migrate or represent it explicitly. Tightened validation must accept converted existing objects or be preceded by remediation. Changing a list from atomic to map changes server-side apply ownership; define stable map keys, test conflicts, and coordinate manager migration rather than silently transferring fields. Add status subresource and controller RBAC without deriving current status from stale alpha annotations. Test defaulting, unknown-field pruning, conversion failure, backup/restore, deletion, and old/new clients. Switch storage to v1, rewrite all objects through storage migration, verify data and managed fields, confirm the old version disappears from `status.storedVersions`, then stop serving alpha after deprecation and inventory gates.

### Answer 5

Represent a permit application occurrence with immutable system ID rather than address/name, and keep applicant proposal separate from authority-owned review status. Schema validates parcel, work categories, plans, accessibility, safety, and required declarations while retaining signed evidence in governed document storage. Applicant, planning, fire, accessibility, heritage, utility, and payment authorities own distinct fields or decisions; conflicts are visible and no generic force overwrites statutory authority. Conditions record completeness, reviews, dependencies, hearing, decision, appeal, and issuance with the proposal revision observed. Amendments create reviewed generations and preserve prior evidence; a decision never claims a later revision. Dependencies use explicit references, not labels alone. Withdrawal starts a lifecycle process for fees, public records, and outstanding inspections; legal retention may forbid physical deletion even though active processing ends. Version conversion preserves legal meaning and jurisdiction effective dates. Automation routes and checks evidence, but authorized humans make discretionary and legal decisions, record reasons, support appeal, and can exercise documented emergency authority.
