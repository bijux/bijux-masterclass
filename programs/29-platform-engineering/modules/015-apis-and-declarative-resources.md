---
module_id: PLAT-015
program: Platform Engineering
level: 1
module_number: 15
title: APIs and Declarative Resources
status: complete
last_verified: 2026-09-02
---

# APIs and Declarative Resources

## One-Page Review

### Governing question

How should a platform expose imperative API operations and declarative resources so consumers can state intent, collaborate safely, observe convergence, recover from partial failure, and understand exactly which system owns each field and lifecycle transition?

### Essential definitions

- An **imperative operation** asks a system to perform a bounded action, such as rotate a credential, preview a change, retry a failed operation, or acknowledge an incident.
- A **declarative resource** records durable desired intent and identity while a controller repeatedly works to make observed state satisfy that intent.
- A **specification** contains consumer-owned desired properties. **Status** contains controller-reported observations, conditions, evidence, and reconciliation progress.
- A **reconciler** is an idempotent control loop that observes desired and actual state, computes a bounded plan, acts, verifies, and publishes status.
- **Convergence** means the resource's declared predicates are satisfied according to fresh evidence; it does not require every underlying system to stop changing.
- **field ownership** identifies which actor or workflow has authority and expectations for a field; it is distinct from identity authorization to write the resource.
- A **condition** is a typed, timestamped, reasoned observation such as `Ready`, `Degraded`, or `Deleting`, scoped to a resource and generation.
- A **finalizer** is a durable lifecycle barrier that prevents resource removal until named cleanup or preservation obligations are satisfied or explicitly resolved.

### Central model, mechanism, or theorem

Model resource $r$ as $R_r=(I,V,S,F,A,O,C,E,L)$: canonical identity $I$, API version $V$, desired spec $S$, field ownership $F$, authorization/policy context $A$, observed external state $O$, conditions/status $C$, evidence $E$, and lifecycle state $L$. Reconciliation applies transition $\rho(S,O,A)\rightarrow(P,O',C',E')$, where $P$ is a bounded plan. A correct loop is level-driven and idempotent: repeating it after the same observations causes no new effect, while new desired or observed state triggers new work.

### Critical invariants

- The resource schema expresses stable platform intent, not raw provider configuration or a serialized form layout.
- Spec is consumer intent; status is controller observation. Consumers do not declare success by writing status.
- Every status and condition identifies the desired generation and freshness to which it applies.
- Authorization to write an object does not imply authority over every field; conflicts are visible rather than silently overwritten.
- Reconciliation is idempotent, retryable, bounded, observable, and safe after process restart.
- API acceptance means intent was recorded, not that external convergence or domain verification occurred.
- Deletion is a stateful, observable workflow with ownership, retention, cleanup, evidence, and a point of irreversibility.
- CLI, portal, Git workflow, SDK, events, and support share canonical resource and operation identities.

### Common failures

Calling YAML declarative while the server executes it once; mirroring a provider schema as a platform API; mixing desired and observed fields; returning success before verification; treating `Ready=true` without generation or freshness as current; allowing two controllers to fight over a field; retrying non-idempotent provider calls without identity; hiding defaults; removing finalizers to clear a stuck deletion without cleanup; using free-form strings instead of typed conditions; and evolving schemas without conversion, defaulting, compatibility, or stored-version plans.

### Compact example

A team applies a `ServiceEnvironment` with profile, region, owner, data class, expiry, and cost boundary. Admission defaults only published non-consequential fields, validates policy, and stores generation 7. The reconciler observes generation 6 status and a provider environment of the wrong size, computes one update with a stable request key, verifies provider and platform evidence, then publishes `observedGeneration: 7` and `Ready=true`. A repeated loop makes no provider call. Deletion sets a deletion timestamp, exposes `Deleting`, exports required evidence, removes dependents, verifies provider cleanup and cost cessation, then releases the finalizer.

### Connections

Retrieve self-service state from [PLAT-005](005-self-service-and-guardrails.md), capability/provider boundaries from [PLAT-007](007-platform-capabilities-versus-tool-catalogs.md) and [PLAT-008](008-internal-platforms-and-external-cloud-services.md), team authority from [PLAT-009](009-platform-team-boundaries.md), journeys and evidence from [PLAT-011](011-developer-journeys.md) and [PLAT-012](012-time-to-first-successful-deployment.md), and channel contracts from [PLAT-013](013-command-line-interfaces.md) and [PLAT-014](014-web-portals.md).

## Governing Question

Which consumer intent deserves a durable resource, which work deserves an explicit operation, and how can the platform preserve authority and truth while continuously reconciling external systems?

An API can expose actions, resources, or both. An imperative call is often clearest for an event-like request with a bounded result. A declarative resource is powerful when intent must survive client exit, controller restart, provider drift, and repeated observation. Neither style is inherently safer. Safety comes from explicit semantics, identity, ownership, evidence, and lifecycle.

The essential design choice is not JSON versus YAML. It is whether the server stores desired intent and operates a durable control loop, or merely interprets a document as a one-time instruction. The interface must tell consumers which model they are using.

## Why This Matters

Platform consumers need durable automation without inheriting provider mechanics. A well-designed resource lets a team declare “a production service environment with these owned constraints” and lets the platform choose, observe, repair, and migrate implementation. A provider-shaped resource instead freezes accidental details into the consumer contract and makes replacement expensive.

Kubernetes provides a mature, current example of records of intent with `spec` and controller-reported `status`. Its controller documentation describes non-terminating loops that move current state toward desired state, including external systems. This is a useful reference pattern, not a requirement to build every platform on Kubernetes or reproduce its entire API machinery.

Current Kubernetes Server-Side Apply makes another subtle requirement visible: declarative collaboration needs field management. A fully specified intent contains fields about which one workflow has an opinion. Conflicts signal that applying it would overwrite another manager's claim. “Last writer wins” is not a sufficient collaboration model for consequential platform fields.

HTTP semantics still matter. RFC 9110 defines safe and idempotent method properties and conditional requests. `PUT` and `DELETE` are defined as idempotent in intended effect, but that alone does not make a downstream provider workflow retry-safe. The platform must persist request identity and reconcile actual outcome across network uncertainty.

Schemas enable validation and tooling. OpenAPI 3.2.0 is the current language-agnostic HTTP interface description, and JSON Schema 2020-12 remains the current published JSON Schema version. A valid schema documents structure, not complete operational semantics. Defaulting, ownership, authorization, reconciliation, status, deletion, and compatibility require additional contracts.

## Prerequisites and Retrieval

Retrieve consumer jobs, cognitive load, product lifecycle, self-service operations, provider composition, team boundaries, value hypotheses, journey states, verified outcomes, CLI process contracts, and portal projection rules from PLAT-001 through PLAT-014.

You should understand HTTP methods and status codes, JSON, schemas, resource identity, optimistic concurrency, idempotency, distributed systems, control loops, eventual consistency, authentication, authorization, policy, events, versioning, migrations, provider APIs, observability, and lifecycle management.

## Learning Objectives

After completing this module, you should be able to:

1. choose between imperative operations, declarative resources, and a deliberate combination;
2. design stable platform resource identity, metadata, spec, status, conditions, and lifecycle;
3. implement a level-driven, idempotent reconciliation loop with bounded plans and durable request identity;
4. preserve field ownership and detect optimistic-concurrency and declarative-apply conflicts;
5. define admission, defaulting, validation, policy, planning, and dry-run boundaries;
6. model deletion, finalization, retention, cascading, orphaning, and stuck cleanup safely;
7. evolve schemas through compatibility, conversion, storage-version, and migration contracts; and
8. expose consistent resources and operations across CLI, portal, Git, SDK, events, and support.

## Core Exposition

### Choose the right interaction model

Use a declarative resource when intent is durable, continuously enforceable, observable, independently owned, and meaningful across provider changes. Examples include service environments, data products, workload identities, deployment policies, and database instances. The resource should have a coherent lifecycle and stable identity.

Use an imperative operation when the request is event-like, time-bound, non-repeatable in meaning, or requires a procedural decision: rotate now, run a diagnostic, acknowledge, approve, promote this verified artifact, restore from this recovery point, or retry a named failure. Persist long-running operation identity even when the initiating call is imperative.

Combine them carefully. A declarative database resource can hold class, region, retention, and lifecycle intent while `restore` is an explicit operation producing a new recovery attempt and evidence. Do not smuggle actions into mutable booleans such as `spec.rotateNow: true`; repeated reconciliation and unclear reset semantics make them fragile.

### Design platform intent, not provider passthrough

Start from consumer decisions and platform promises. A workload profile, durability class, latency boundary, residency constraint, retention policy, or support tier can survive provider change. Provider instance type, proprietary identifier, and control-plane flag often cannot.

Expose provider detail only when it is a genuine consumer decision that the platform cannot responsibly abstract. Label responsibility and portability. An extension field can be an escape hatch, but untyped bags of provider configuration bypass validation, policy, documentation, migration, and support.

Keep each resource cohesive. A giant `PlatformApplication` containing repository, runtime, database, DNS, identity, pipeline, telemetry, and every policy creates an enormous blast radius and ownership conflict. Compose bounded resources with stable references and aggregate higher-level readiness without pretending atomicity across providers.

### Define identity, version, metadata, spec, and status

Model resource $r$ as

$$
R_r=(I,V,S,F,A,O,C,E,L),
$$

where $I$ is canonical identity, $V$ API/schema version, $S$ desired spec, $F$ field ownership, $A$ authorization and policy context, $O$ observed external state, $C$ conditions/status, $E$ evidence and correlation, and $L$ lifecycle.

Identity commonly includes immutable server UID plus human name and scope. Names can be reused after deletion; UIDs prevent accidental adoption of a different object. References should distinguish name, UID, kind, scope, and optional expected version where integrity matters.

Metadata can include creation time, generation, labels for selection, annotations for non-semantic integration data, owners, and finalizers. Do not place large secrets, status, or behavior-changing unvalidated configuration in annotations.

Spec contains desired consumer-owned properties. Status contains controller-owned observation and should be reconstructible from durable intent and external systems, even if reconstruction is expensive. Separate subresources or permissions can protect status from ordinary consumers.

### Build a level-driven reconciliation loop

For desired spec $S$, observation $O$, and authorization/policy context $A$, define one transition as

$$
\rho(S,O,A)\rightarrow(P,O',C',E'),
$$

where $P$ is a bounded plan, $O'$ the new observation after safe action, $C'$ updated conditions, and $E'$ evidence. A production controller schedules future reconciliation rather than recursively running until convergence.

A durable loop performs: fetch latest resource; handle deletion; validate controller prerequisites; observe provider and dependents; compare desired with observed; compute plan; persist request identity; execute at most bounded work; re-observe or schedule; update status; and emit events/metrics. Failures update typed conditions and retry according to class.

Design from levels, not event history. An event says something may have changed; the current resource and provider state determine action. Events can be duplicated, reordered, or lost. After restart, the loop should reconstruct what remains.

The following synthetic loop changes a provider once and makes no change after convergence.

<!-- bijux-verify: {"id":"declarative-reconcile-idempotency","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"generation=4\nobserved_generation=4\nfirst_pass_actions=1\nsecond_pass_actions=0\nready=true\nconverged=true\n","stderr":""}} -->
```python
resource = {
    "generation": 4,
    "spec": {"size": "medium"},
    "status": {"observedGeneration": 2, "ready": False},
}
provider = {"size": "small", "healthy": True}

def reconcile(resource, provider):
    actions = 0
    if provider["size"] != resource["spec"]["size"]:
        provider["size"] = resource["spec"]["size"]
        actions += 1
    resource["status"] = {
        "observedGeneration": resource["generation"],
        "ready": provider["healthy"] and provider["size"] == resource["spec"]["size"],
    }
    return actions

first = reconcile(resource, provider)
second = reconcile(resource, provider)
print(f"generation={resource['generation']}")
print(f"observed_generation={resource['status']['observedGeneration']}")
print(f"first_pass_actions={first}")
print(f"second_pass_actions={second}")
print(f"ready={str(resource['status']['ready']).lower()}")
print(f"converged={str(provider['size'] == resource['spec']['size']).lower()}")
```

The example assumes an atomic in-memory provider update and fresh health. Real controllers need timeouts, request keys, partial-state observation, rate limits, error classification, concurrency, and evidence before publishing readiness.

### Make idempotency survive network uncertainty

Controller restart, queue redelivery, API timeout, or provider response loss can repeat work. Assign stable identity to each desired transition or provider operation. Before retry, observe by that identity or resource correlation. Do not generate a fresh provider request ID on every loop.

Idempotency means repeated intent has the same intended effect, not that every response or log line is identical. A create-or-observe workflow may return an existing provider object. A rotation operation usually needs an operation resource because repeating “rotate” can create a new credential each time.

Classify failures: invalid or denied intent needs consumer action; conflict needs ownership resolution; throttling and transient outage can retry with backoff; unknown outcome needs reconciliation before replay; terminal provider failure needs retained evidence and safe recovery. Infinite retries are not resilience when no progress is possible.

### Preserve concurrency and field ownership

Optimistic concurrency prevents lost updates by requiring an expected resource version or HTTP conditional such as `If-Match`. On conflict, re-read, recompute, and ask the user to resolve consequential changes. Blind retries can overwrite new intent.

Declarative apply adds field-level collaboration. Each manager declares fields about which it has an opinion. Omitting an owned field may relinquish or delete it according to the apply contract. Conflicting assertions should fail with manager, path, current value, desired value, and resolution options.

Forced ownership transfer is a governance decision, not a generic “make it work” flag. Controllers may own derived operational fields; application teams own domain settings; security policy may constrain but should not silently become the owner of unrelated fields. Defaulting must not create phantom consumer ownership.

### Separate admission from reconciliation

Admission handles structural validation, defaulting, authorization, policy, reference syntax, quotas that can be decided immediately, and mutation allowed by contract. It should be deterministic, fast, and free of fragile provider calls. Reject unknown fields where practical rather than ignore typos.

Reconciliation handles asynchronous observation and external change. A region can be syntactically valid yet unavailable later. A provider can accept then fail. Put these outcomes in status rather than blocking the API request indefinitely.

Defaults should be published, stable, and visible in the stored representation or effective-spec view. Consequential choices such as public exposure, data residency, deletion policy, or expensive size should not appear through an invisible default. Distinguish omitted, explicit null, empty, and defaulted values.

### Design status and conditions for decisions

Status answers what the controller observed, for which desired generation, at what time, with what evidence, and what action is safe. Common fields include `observedGeneration`, provider identifiers, operation references, endpoints, last observation time, phase only when useful, and typed conditions.

A condition should have type, boolean or tri-state status, reason code, human message, transition time, observed generation, and evidence/correlation. Use stable reason codes for automation and messages for people. A single phase enum often cannot represent `Ready`, `Degraded`, `PolicyCompliant`, and `Deleting` simultaneously.

`Ready=true` for generation 6 does not prove generation 7 is ready. Unknown is not false. A stale observation should not remain confidently green. Aggregate readiness must state which child predicates it includes and preserve the child evidence.

Events describe notable transitions and diagnostics but are not the durable current state. Logs support operators. Metrics support trends. Status is the consumer-facing observation contract; none should contain secrets.

### Expose preview, dry run, and plans honestly

Schema validation and policy dry run can happen without provider mutation. A plan may also compare desired state with current observation and list proposed actions, replacements, cost effects, and unknowns. Label the guarantees separately.

Plans decay. Bind apply to resource version, provider observation token, policy version, schema version, and a plan digest where high consequence. If assumptions change, reject or re-plan rather than claim the old preview still applies.

Do not promise an exact provider plan when the provider cannot supply one. Mark values known, derived, estimated, sensitive, or unknown. A dry-run response that invokes no external system cannot prove quota, provider acceptance, or eventual convergence.

### Treat deletion as reconciliation

Delete usually records intent first. The resource enters a deleting state with timestamp, propagation policy, retention, and finalizers. Controllers stop ordinary convergence, perform or verify cleanup, preserve required evidence, and remove only the finalizers they own.

Define cascading, orphaning, retention, snapshot, export, credential revocation, cost cessation, and dependent notification. Some child resources may outlive the parent by contract. Canonical UIDs prevent a newly created same-name parent from adopting old children accidentally.

A stuck finalizer is an incident with an owner, reason, retry state, and recovery procedure. Manually removing it can orphan costly, sensitive, or dangerous external state. Provide a break-glass path that records authority and compensating cleanup rather than teaching consumers to edit metadata blindly.

### Evolve schemas and stored resources

Separate API version from product release. Define compatibility for field meaning, defaults, validation, enum expansion, list/map behavior, status, and deletion. Adding an optional field can still break clients that reject unknown members or exhaustively switch on enums.

Support conversion between served versions and choose a canonical storage version. Conversion must preserve round trips for supported fields or clearly define loss. A new version may reinterpret intent only through an explicit migration, never silently during read.

Plan stored-object migration, controller skew, rollback, deprecated fields, admission ordering, and old clients. Record which controller and schema produced status. Test old manifests against new servers and new resources through old supported readers.

OpenAPI can describe paths, operations, parameters, representations, and schemas. JSON Schema can express structural assertions. Neither replaces semantic compatibility tests, reconciliation fixtures, provider simulations, or lifecycle migration rehearsal.

### Keep all channels on one contract

CLI, portal, SDK, Git workflow, and automation should call the same resource and operation APIs. A portal form may render schema hints and journey guidance; it must not create a separate field model. CLI machine output should expose canonical identity and conditions. Support should use the same correlation.

Git is a transport and review workflow, not automatically the source of truth. Define repository intent, branch/merge authority, delivery controller, live API resource, drift policy, emergency changes, and reconciliation direction. Avoid two independent reconcilers repeatedly reverting each other.

Emit watch or event streams with resource version, type, identity, and resumable semantics. Consumers must handle duplicates, relisting, compaction, and authorization changes. An event notification is not proof that the observed object still has that state.

### Operate the control plane as a product

Measure admission latency and rejection, reconciliation queue age, attempts, convergence time, status freshness, conflict, drift, retry, unknown outcomes, finalizer age, provider errors, API availability, watch health, and controller saturation. Pair these with consumer task success, reliability, safety, cost, support, and operator toil.

Set objectives by capability consequence. A slow sandbox reconciler differs from stale credential revocation or stuck production deletion. Rate-limit and prioritize fairly. Backpressure should preserve intent and show delay rather than drop work silently.

Audit desired changes, principal, manager, policy decision, plan, provider operation, status transition, and break-glass action without storing secrets. Make resource ownership and controller ownership discoverable. Reconciliation code is production operations, not background glue.

## Definitions and Notation

$R_r=(I,V,S,F,A,O,C,E,L)$ models resource $r$ through identity, version, desired spec, field ownership, authorization/policy, observed state, conditions/status, evidence, and lifecycle.

$\rho(S,O,A)\rightarrow(P,O',C',E')$ is one bounded reconciliation transition. The prime denotes the next observation/status/evidence after action or re-observation, not guaranteed convergence in one pass.

Let desired generation be $g$ and status observation generation be $\hat g$. A readiness claim applies to current intent only if $\hat g=g$ and its evidence meets the freshness contract. If $\hat g<g$, prior readiness is historical evidence.

For deterministic external state $O$ and desired $S$, idempotent reconciliation has the fixed-point property that after convergence, repeated transition produces empty action plan: $\rho(S,O,A).P=\varnothing$. Real observations can change, so the property is conditional on relevant inputs.

## Mechanisms, Invariants, or Proof Structure

Use a contract-first loop: select durable intent; define resource boundary and identity; assign field authority; define schemas and versions; specify admission; model observations and conditions; design idempotent reconciliation; persist request correlation; define preview and conflicts; model deletion/finalizers; expose channel adapters; test failures and skew; release gradually; operate with objectives; migrate and retire.

The intent invariant separates platform promise from provider mechanics. The spec/status invariant separates desire from observation. The generation invariant prevents stale success. The ownership invariant prevents silent collaboration loss. The fixed-point invariant prevents repeated side effects. The lifecycle invariant prevents deletion from becoming disappearance without cleanup.

Adversarial review includes duplicate queue events; controller restart after provider action; response lost after create; provider object changed manually; two field managers conflict; default changes; old client drops new fields; condition from old generation; status write conflict; clock skew; reference target recreated with same name; finalizer owner unavailable; conversion round-trip loss; provider deletion succeeds but cost continues; and Git/API reconcilers fight.

## Alternatives and Trade-Offs

**Imperative API** makes procedure and immediate errors explicit. Clients must coordinate retries, sequencing, and drift unless operations remain durable.

**Declarative resource** preserves intent and enables repair. It requires controllers, field ownership, status, lifecycle, and eventual-consistency literacy.

**Coarse aggregate resource** simplifies onboarding and transactions. It increases ownership conflict, replacement blast radius, and partial-state ambiguity.

**Fine-grained resources** improve independent lifecycle and reuse. They expose composition and dependency complexity to consumers unless profiles aggregate it well.

**Full replacement with PUT** is conceptually simple. It risks dropping unknown fields and conflicts on unrelated changes.

**Patch** updates narrow fields. Different patch formats have different list, null, precondition, and ownership semantics.

**Field-managed apply** supports multiple declarative managers. It adds managed-field size, conflict UX, schema requirements, and force-transfer governance.

**Git-mediated intent** adds review and history. It adds latency, repository permissions, delivery-controller availability, secrets concerns, and emergency-change reconciliation.

## Failure Modes and Misconceptions

- **“YAML is declarative.”** Serialization does not establish durable intent, observation, or reconciliation.
- **“Accepted means ready.”** It only proves the API accepted or stored a request under its contract.
- **“Status is another input.”** Allowing consumers to declare observed success destroys trust and controller ownership.
- **“Retry the provider call.”** First reconcile using durable request identity; the first call may have succeeded.
- **“Last writer wins is collaboration.”** It silently destroys another manager's asserted intent.
- **“Ready is a boolean.”** Generation, freshness, reason, evidence, and component predicates determine meaning.
- **“Finalizers prevent deletion.”** They delay object removal while named lifecycle obligations are handled; they can also become stuck.
- **“OpenAPI defines behavior.”** It describes interfaces but cannot fully express control-loop and lifecycle semantics.
- **“Git is always truth.”** Authority and reconciliation direction must be explicitly designed.
- **“Controllers are internal.”** Their latency, errors, status, and recovery directly shape the consumer product.

## Worked Examples

### Example 1

A `ServiceEnvironment` exposes profile, region, data class, expiry, and owner. Provider account, network IDs, and instance types remain status/evidence. Migrating providers preserves consumer intent while the controller changes implementation.

### Example 2

A `rotateNow` boolean repeatedly triggers after controller restart because reset failed. The design replaces it with a `CredentialRotation` operation resource with unique identity, target, state, evidence, and terminal outcome.

### Example 3

Two managers assert different retention periods. Apply returns a field conflict naming both managers and values. Security policy can deny an unsafe value, but the platform does not force ownership transfer without explicit authority.

### Example 4

Generation 12 status says ready, but the spec is generation 13 after a region change. The portal displays reconciling and the previous observation rather than green. `observedGeneration` reaches 13 only after new evidence passes.

### Example 5

A provider create succeeds but the response times out. The controller searches by request key and ownership tag, adopts the exact object, and continues. A blind retry would have created a duplicate environment.

### Example 6

A plan knows a database size change requires replacement but cannot know provider capacity. It marks replacement known, capacity unknown, cost estimated, and binds apply to resource/provider versions rather than promising guaranteed convergence.

### Example 7

Deleting a data store sets a timestamp and `Deleting` condition. The finalizer snapshots required data, verifies retention and dependent notification, deletes the provider object, confirms billing cessation, and then releases removal.

### Example 8

A new API version splits `region` into `jurisdiction` and `location`. Conversion preserves the old value, admission requires explicit selection for new high-risk resources, and migration records unresolved ambiguous objects rather than guessing.

### Example 9

A Git controller and emergency API operator both edit replicas. Field ownership and a documented break-glass workflow let the operator temporarily take the field, commit the intended state back, and relinquish ownership without a reconciliation fight.

### Example 10

A list watch is compacted while a client is disconnected. The client relists at a new resource version, rebuilds its projection, and resumes. It does not treat the missing event range as proof that nothing changed.

## Cross-Program Connections

API engineering contributes HTTP semantics, schema description, status codes, conditional requests, compatibility, and client contracts. Distributed systems contributes idempotency, partial failure, retries, ordering, eventual consistency, and uncertainty. Control theory contributes desired/observed state and feedback loops, while software controllers remain discrete, delayed, and policy-laden systems rather than ideal continuous controllers.

Database engineering contributes identity, optimistic concurrency, migrations, materialized views, and event logs. Security contributes authentication, authorization, policy, field authority, secret handling, and audit. Reliability contributes conditions, freshness, objectives, backpressure, degraded behavior, and incident response.

Product and organizational design define durable capability boundaries and owners. Data governance defines retention and deletion evidence. Developer experience connects declarative semantics to CLI, portal, Git, documentation, support, and comprehensible conflict recovery.

## References

- IETF, [RFC 9110: *HTTP Semantics*](https://www.rfc-editor.org/rfc/rfc9110.html), June 2022. Safe and idempotent methods, representation metadata, validators, conditional requests, and HTTP method semantics.
- OpenAPI Initiative, [*OpenAPI Specification 3.2.0*](https://spec.openapis.org/oas/latest.html), September 19, 2025. Current language-agnostic HTTP API description, discovery, tooling, and versioning specification.
- JSON Schema, [*Draft 2020-12*](https://json-schema.org/draft/2020-12), published June 16, 2022 and current as retrieved September 2, 2026. Core, validation, vocabularies, dialect, annotation, and output specifications.
- Kubernetes Project, [*Objects in Kubernetes*](https://kubernetes.io/docs/concepts/overview/working-with-objects/), updated November 24, 2025. Records of intent, desired spec, controller-reported status, identity, validation, and API version fields.
- Kubernetes Project, [*Controllers*](https://kubernetes.io/docs/concepts/architecture/controller/), current documentation retrieved September 2, 2026. Control loops, desired/current state, external systems, and status reporting.
- Kubernetes Project, [*Kubernetes API Concepts*](https://kubernetes.io/docs/reference/using-api/api-concepts/), current documentation retrieved September 2, 2026. Resource operations, versions, watches, updates, patches, conflicts, and Server-Side Apply trade-offs.
- Kubernetes Project, [*Server-Side Apply*](https://kubernetes.io/docs/reference/using-api/server-side-apply/), current documentation retrieved September 2, 2026. Fully specified intent, field managers, ownership conflicts, force transfer, serialization, and access control.
- Kubernetes Project, [*Finalizers*](https://kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/), updated April 27, 2025. Deletion timestamps, accepted deletion, cleanup barriers, owner references, stuck finalizers, and manual-removal risk.
- Kubernetes SIG Architecture, [*API Conventions*](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md), current source retrieved September 2, 2026. Resource, metadata, spec/status, condition, naming, update, and compatibility conventions.
- DORA, [*Platform Engineering*](https://dora.dev/capabilities/platform-engineering/), updated January 12, 2026. Current internal-product, critical-journey, abstraction, feedback, independence, and balanced platform-measurement guidance.

## Exercises

### Exercise 1

Design a declarative `ServiceEnvironment` resource. Specify identity, scope, spec, status, conditions, ownership, admission, reconciliation, evidence, and lifecycle without mirroring one cloud provider.

### Exercise 2

Trace a controller crash after a provider accepted a create request but before status was written. Design request identity, observation, adoption, retry, condition, and operator evidence that prevents duplication.

### Exercise 3

Two workflows manage one resource: a team manages runtime size and a sustainability controller manages a scheduling window. Design field ownership, defaulting, conflicts, forced transfer, optimistic concurrency, and audit behavior.

### Exercise 4

Design deletion and finalization for a regulated database resource. Include dependents, snapshots, retention, access revocation, provider deletion, cost verification, stuck cleanup, break glass, and final evidence.

### Exercise 5

Transfer the declarative-resource model to a hospital laboratory-result routing system. Separate durable routing intent, event-like clinical operations, authoritative result truth, status, field authority, correction, deletion/retention, and safety evidence.

## Answers to the Exercises

### Answer 1

Use immutable UID plus scoped name. Spec contains profile, jurisdiction, availability class, owner reference, data class, expiry, cost boundary, network intent, and deletion policy; provider account, instance type, IDs, endpoints, and observations remain status. Team owns profile/owner/expiry; security constrains exposure and data class; finance constrains cost; platform owns derived implementation. Admission validates schema, references, policy, and visible defaults without calling providers. Reconciliation observes dependencies/provider, plans idempotently, acts with request keys, verifies connectivity, policy, telemetry, ownership, and cost, then publishes observed generation and typed Ready/Degraded conditions. Lifecycle includes create, change, suspend if supported, renew, migrate, and finalizer-governed delete. Evidence names source, freshness, provider correlation, and verification contract.

### Answer 2

Generate and persist an operation/request key before the provider call, derived from resource UID and desired transition identity rather than loop attempt. Tag or otherwise correlate the provider object with resource UID and request key. After restart, read current resource, observe provider by request key and canonical ownership, and classify absent, unique match, ambiguous match, or inaccessible observation. Adopt only the uniquely matching object after verifying immutable attributes. Do not create while outcome is unknown. Status records observed generation, `Reconciling` or `Unknown`, reason, last observation, request correlation, and safe next action. Retry uses the same key when the provider contract supports it. Ambiguity escalates with redacted evidence and performs no duplicate mutation.

### Answer 3

The team manager asserts `spec.runtime.size`; the sustainability manager asserts `spec.schedule.window`. Published defaults are materialized by admission but do not falsely assign either workflow's ownership unless it asserted them. Apply records manager/path claims and rejects attempts to change another manager's differing value. A consumer can relinquish a field by omitting it under the documented apply semantics, adopt the current value for shared ownership, or request an authorized forced transfer that names displaced owner and reason. Whole-resource updates require expected resource version to prevent lost updates and should not drop unknown fields. Audit records principal, workflow manager, old/new value, conflict, policy, force authority, and correlation. Neither manager writes status.

### Answer 4

Delete sets timestamp, policy, and `Deleting` condition while retaining the resource. The controller freezes unsafe ordinary changes, enumerates UID-bound dependents, blocks or coordinates consumers, creates and verifies a required snapshot, records retention and legal hold, revokes application access, drains traffic, deletes the provider instance, verifies absence and billing cessation, retains required audit evidence, then removes only its finalizer. Each obligation has owner, attempt, error class, evidence, and recovery. A stuck finalizer pages the owning team and exposes status. Break glass requires named authority, reason, review, and manual proof that obligations were satisfied or an explicit accepted risk with compensating cleanup; it never means deleting the finalizer just to hide the object.

### Answer 5

A `ResultRoute` resource can declare authorized sending laboratory, receiving organization/system, message profile, jurisdiction, privacy purpose, urgency policy, acknowledgement objective, correction channel, and lifecycle. Laboratory result content and provenance remain authoritative laboratory records, not desired platform spec. Event-like operations include transmit a released result, issue a correction, acknowledge receipt, and invoke downtime reconciliation; each has durable identity and evidence. Platform status reports route readiness, observed generation, connectivity, policy, last test, and degradation, never clinical correctness or interpretation. Laboratories own release/correction truth, privacy authorities own purpose/access/retention constraints, clinical authorities own interpretation and escalation, and platform controllers own technical routing fields. Retention and deletion follow records law and patient safety, with finalizers for acknowledgement, correction linkage, export, and audit. Unknown delivery remains unknown until authoritative reconciliation; duplicates use clinical message identity and idempotent handling.
