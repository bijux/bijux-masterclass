---
module_id: PLAT-060
program: Platform Engineering
level: 2
module_number: 60
title: Designing a Domain-Specific Platform API
status: complete
last_verified: 2026-09-02
---

# Designing a Domain-Specific Platform API

## One-Page Review

### Governing question

How should a platform turn recurring user outcomes into a small, durable, secure, evolvable API that hides provider mechanics without hiding consequential choices, and whose controller can reconcile, explain, recover, and retire every accepted state?

### Essential definitions

- A **domain-specific platform API** exposes concepts and outcomes meaningful to its users—such as a service environment, data capability, or delivery policy—rather than mirroring provider resources.
- A **capability** is a supported outcome with an owner, service contract, policy boundary, lifecycle, and evidence of fulfillment.
- **intent** states what the consumer owns; **implementation** states how the platform and providers realize it.
- An **abstraction budget** is the complexity the platform deliberately accepts to remove recurring cognitive load without erasing important cost, risk, or lifecycle decisions.
- A **pit of success** makes the common safe path easy and the dangerous or exceptional path explicit, reviewable, and observable.
- A **class** is a named, versioned service policy such as `standard` or `regulated`; it is not an undocumented alias for one provider SKU.
- An **escape hatch** is a bounded, owned extension point whose compatibility, security, portability, and support consequences are explicit.
- **semantic compatibility** preserves promised meaning and outcomes, not merely the ability to decode old YAML.
- A **composition revision** identifies the implementation plan used to realize an API object so rollout and rollback can be controlled.
- **effective state** is the resolved combination of user intent, defaults, class/policy decisions, and implementation selection that actually governs reconciliation.

### Central model, mechanism, or theorem

Let user journey $j$ occur at rate $f_j$, impose unmanaged cognitive/coordination cost $c_j$, and receive fractional reduction $r_j$ from an API. Let platform build and lifecycle cost be $B+M$. A candidate abstraction has modeled net value

$$
V=\sum_j f_j c_j r_j-(B+M),
$$

subject to safety, support, and ownership constraints; frequency alone does not justify encoding a hazardous workflow. The API contract maps valid intent $I$ plus policy/context $P$ to an effective plan $E=R(I,P)$, then a reconciler converges implementation state toward $E$ and reports generation-correlated evidence. Design proceeds through discovery, domain boundaries, resource/state/lifecycle modeling, schema and policy, authorization, composition, status, failure/recovery, versioning, testing, release, measurement, and retirement. Portal, CLI, Git, and SDK experiences are projections over one contract—not separate sources of truth.

### Critical invariants

- Every resource corresponds to a researched user job and a platform-owned capability, not a vendor object or organizational handoff.
- The API exposes consequential choices about availability, recovery, data disposition, geography, security, and cost while hiding replaceable mechanics.
- Each accepted spec has defined admission, authorization, ownership, reconciliation, status, update, deletion, recovery, and support behavior.
- Defaults and classes are deterministic or their resolved values and provenance are recorded; silent policy drift never changes existing outcomes accidentally.
- References use durable identity and target-side authorization where boundaries cross; secrets are referenced, not copied into status or ordinary spec.
- Composition and controllers are replaceable behind the contract, but implementation revisions, effect identities, and rollback limits remain observable.
- Status reports user-relevant capability, observed generation, dependencies, policy resolution, and actionable failure without leaking sensitive internals.
- API evolution preserves representation and semantic compatibility or uses a new version/kind plus measured migration and conversion.
- Escape hatches are typed, bounded, least-privilege, ownership-scoped, measured, and designed for promotion or removal.
- Success is measured by user outcomes, adoption, support burden, safety, lead time, and abandonment—not object count or portal clicks alone.

### Common failures

Mirroring cloud APIs; designing from available controllers instead of user journeys; one giant `Application` object; one resource per ticketing team; free-form provider blobs; hiding region, recovery, or deletion policy; magical mutable defaults; mixing workflow commands into desired state; equating schema validity with deliverability; accepting references the caller is not authorized to use; copying secrets into outputs; returning a provider error without a user remedy; changing a class beneath existing objects; exposing every advanced knob; promising portability while leaking one backend; treating a portal form as the API; using templates as ongoing reconciliation; versioning YAML but changing semantics; measuring creation rather than successful use; and deleting the controller before effects and consumers are retired.

### Compact example

A platform studies repeated requests for production PostgreSQL and publishes namespaced `DataService` rather than a wrapped cloud database. Users choose `serviceClass`, capacity band, region policy, recovery tier, maintenance window, deletion policy, and an authorized consumer identity reference. A class resolves to a versioned plan; status records `observedGeneration`, class/composition revision, endpoint and secret references, cost band, recovery evidence, and capability conditions. CEL rejects impossible transitions such as reducing retention below a regulated minimum; admission checks reference grants and budget policy; the controller uses UID-derived provider operation identities. A new provider is rolled out by composition revision to opt-in canaries, not by silently redefining existing objects. Portal, CLI, and Git all submit the same resource. If users repeatedly need read replicas, the team researches and promotes that bounded outcome into the API instead of distributing an untyped provider override.

### Connections

This module synthesizes declarative platform APIs from [PLAT-015](015-apis-and-declarative-resources.md), CRD contracts from [PLAT-053](053-custom-resource-definitions.md), state machines and idempotency from [PLAT-054](054-operator-state-machines.md) and [PLAT-055](055-idempotent-reconciliation.md), deletion and evidence from [PLAT-056](056-finalizers-and-deletion.md) and [PLAT-057](057-status-conditions-and-drift.md), dependency graphs from [PLAT-058](058-cross-resource-dependencies.md), and recovery from [PLAT-059](059-control-plane-failure-and-recovery.md). PLAT-061 separates this contract into platform API layers.

## Governing Question

How can a platform encode a real organizational domain into an interface that makes common user outcomes safer and easier while preserving the choices, evidence, and lifecycle controls that users and operators must still understand?

The hard part is not writing a CRD or endpoint. It is deciding which promises the platform owns. An API that mirrors a provider transfers cognitive load. An API that hides every decision creates surprises in cost, resilience, deletion, and compliance. An API that accepts more states than the platform can operate creates a queue of latent incidents.

A domain-specific API is a product contract and a control contract. It shapes user language, authorization, stored intent, controller effects, support expectations, migrations, backups, and eventual retirement. The design must remain useful even when the portal changes, the controller is rewritten, or the backing provider is replaced.

## Why This Matters

Internal platforms multiply decisions. A good field default or lifecycle rule can make thousands of environments safer; a vague field or hidden mutation can produce the same mistake everywhere. The leverage demands product discovery and API rigor together.

Users need stable concepts. They should request a recoverable data service or compliant runtime, not assemble subnet IDs, IAM policies, backup jobs, encryption options, and provider SKUs anew. Yet they must still choose outcomes that materially affect their system and obligations.

Providers and organizational policies change faster than application intent. A durable platform contract lets implementations evolve behind a controlled boundary, but only if the abstraction is not secretly coupled to one provider and class changes are revisioned.

Self-service without lifecycle ownership is merely faster provisioning. Updates, incidents, migrations, deletion, cost attribution, data retention, controller retirement, and recovery are part of the same service. The API must carry enough identity and policy to manage them safely.

Different interfaces otherwise fragment intent. A portal can validate one way, a Git template another, and an SDK a third. A canonical machine contract lets every experience share admission, authorization, status, audit, and reconciliation behavior.

## Prerequisites and Retrieval

Retrieve platform as product, user research and jobs-to-be-done, cognitive load, domain-driven design, bounded contexts, ubiquitous language, capabilities and service catalogs, declarative resources, REST and Kubernetes API conventions, metadata/spec/status, reconciliation, state machines, structural OpenAPI schemas, CEL and admission, API groups/versions, conversion and deprecation, optimistic concurrency and Server-Side Apply, identity and references, RBAC and tenancy, finalizers and deletion policy, dependency DAGs, idempotency and external operation IDs, composition, templates and portals, GitOps, SLOs, quotas and cost attribution, audit, disaster recovery, migration, and decommissioning.

You should distinguish user outcome from provider object; domain resource from portal form; capability from implementation; abstraction from concealment; class from SKU; desired state from command; schema validity from policy eligibility and operational feasibility; default from policy resolution; reference from secret value; namespace from complete tenant isolation; status from logs; API version from product release; representation compatibility from semantic compatibility; composition revision from resource generation; template execution from continuous reconciliation; exception from escape hatch; adoption from value; and provisioning completion from lifecycle success.

## Learning Objectives

After completing this module, you should be able to:

1. discover and rank candidate platform capabilities from recurring user journeys and operational evidence;
2. define bounded domain resources, identities, ownership, state, relationships, and lifecycle promises;
3. choose the correct abstraction level and expose outcome-oriented fields without hiding consequential trade-offs;
4. design schemas, defaults, classes, admission, authorization, and references that form one coherent contract;
5. map intent to revisioned compositions and idempotent reconciliation without leaking provider mechanics;
6. design user-relevant status, errors, observability, cost, support, and recovery evidence;
7. control escape hatches, multi-tenancy, quotas, policy, and sensitive outputs;
8. evolve, migrate, test, release, measure, and retire the API as a product; and
9. evaluate a complete domain API against safety, operability, compatibility, and user-outcome invariants.

## Core Exposition

### Begin with user journeys, not resource kinds

Observe how teams currently obtain and operate a capability. Follow the full journey: discover an offering, compare choices, request it, wait, connect, change capacity, diagnose failure, recover, transfer ownership, and delete. Ticket history, incident reviews, abandoned templates, shadow automation, support chats, and provider spend provide evidence beyond interviews.

Write the job in domain language: “run an HTTP service with a defined exposure and recovery objective,” not “create a Deployment, Service, Ingress, and database.” Identify the user, trigger, desired outcome, decision points, latency tolerance, failure consequences, and evidence of success.

Rank candidates by recurrence, cognitive load, safety leverage, reuse, platform competence, and lifecycle ownership. A rare but catastrophic key-rotation workflow may still deserve a guarded capability; a common one-line namespace creation may not justify a new abstraction.

Use the value model $V=\sum_j f_jc_jr_j-(B+M)$ as a reasoning aid, not accounting truth. Include maintenance, support, versioning, migration, recovery, and retirement in $M$. Add hard constraints: the team must own or coordinate the whole promise, and risks must fit its operational model.

Start with a small cohort and concrete journeys. “All developers” is too broad for discovering field semantics. A regulated data team and an ephemeral preview-environment team may require different capabilities or classes rather than one incoherent mega-resource.

### Establish the bounded context and ubiquitous language

Name concepts as users and domain owners understand them. If “environment” means a deployable application boundary to one group and a cloud account to another, resolve the ambiguity before encoding `Environment`. API names institutionalize language through manifests, clients, policy, audit, and support.

Draw boundaries around responsibilities. A `DataService` can own provisioning, backup policy, endpoint publication, maintenance, and deletion disposition while a `Workload` owns executable artifact and traffic. Avoid a resource whose controller must own every team’s domain.

Map upstream and downstream contracts: identity, network, cost center, policy set, data classification, delivery source, runtime, telemetry, and consumers. Decide which are fields, typed references, separate resources, or derived context. References preserve independent ownership; embedding implies stronger lifecycle coupling.

Choose aggregate boundaries around invariants and lifecycle. Fields that must change atomically and are owned together may belong in one spec. Independently authorized or long-lived concepts deserve separate resources. Do not copy the organizational chart: ticket handoffs are not necessarily domain boundaries.

Maintain a glossary with accepted and rejected meanings, examples, and counterexamples. Review it with users, operators, security, finance, and provider owners. This is API design work, not cosmetic documentation.

### Define the capability contract before the representation

For each capability, state supported outcomes, eligibility, service level, ownership, data/security classification, cost model, geography, dependencies, maintenance, recovery, update behavior, deletion disposition, support channel, and exclusions. An API schema cannot repair an undefined promise.

Define the platform’s control span. If another team owns the database provider, the platform can promise only what its dependency contract supports. A `Ready=True` outcome needs a source, freshness, and escalation path across that boundary.

Separate stable promise from replaceable implementation. “Encrypted at rest with regional failover and seven-day point-in-time recovery” can survive a provider replacement; “enable provider flag X on instance class Y” cannot. Do not claim portability beyond tested implementations and semantics.

State degraded modes. Can an existing service keep running when the control plane is unavailable? Can users update labels but not capacity during a provider incident? Which operations fail closed? A capability contract includes failure behavior, not just the success catalog.

Publish support tiers and lifecycle. Experimental capabilities can have narrower guarantees, but instability must be visible in version, documentation, conditions, and migration expectations. “Beta” is not permission to abandon stored effects.

### Choose resources and boundaries deliberately

Model nouns with durable identity and lifecycle as resources. A request to maintain a data service fits desired state. A one-time restore may be a separate immutable `Restore` work resource with terminal status because repeated mutation of `spec.restoreNow: true` is ambiguous.

Avoid one giant `Application` whose spec embeds database, network, pipeline, runtime, DNS, policy, and monitoring. It couples independent ownership, authorization, update cadence, failure, and deletion. A composition resource may coordinate a coherent aggregate, but children and dependencies should remain inspectable.

Avoid microscopic resources that expose every internal component. If users must understand the provider graph, the abstraction has not removed much cognitive load. Expose child references for diagnosis without requiring users to orchestrate them.

Choose scope from identity, authorization, policy, quota, and lifecycle. Namespaced resources are often safer for team-owned capabilities, but namespace boundaries do not prevent every confused-deputy or cross-reference risk. Cluster-scoped APIs require strong justification and careful RBAC.

Define name, UID incarnation, owner, transfer, adoption, import, and duplication behavior. External effects should carry stable platform object identity and operation identity so restore or recreation does not collide with an old instance that shares a name.

### Expose outcomes and consequential choices

Each spec field should represent a decision the consumer owns and the platform can honor. Useful fields include service class, availability/recovery tier, capacity band, region policy, exposure, data classification, maintenance constraint, dependency reference, deletion policy, and budget owner.

Hide replaceable mechanics: cloud subnet IDs, chart values, IAM JSON, controller retry counts, provider SKU names, or raw Terraform modules. If an implementation detail affects user responsibility or interoperability, expose the outcome it represents rather than pretending it does not exist.

Do not hide irreversible consequences. Data retention, destructive replacement, cross-region replication, public exposure, and material cost deserve explicit intent or a clearly documented class promise. Convenience is not informed consent.

Keep the common path small. Required fields should correspond to information the platform cannot safely infer. Optional fields need a real use case; every field increases documentation, testing, compatibility, policy, support, and migration cost.

For each field record meaning, owner, allowed values, default/resolution, mutability, interactions, effect, status evidence, failure behavior, security/cost implication, and deprecation plan. A field without these answers is not ready for the contract.

### Design classes as stable policy products

A class packages decisions that users should select together: for example `standard`, `critical`, or `regulated`. Define each in terms of outcome—availability target, backup/recovery, security, maintenance, cost band, and support—not current implementation.

Version class resolution. If `standard` changes from single-zone to multi-zone, existing resources must not silently acquire cost and topology changes unless the contract explicitly uses continuous policy and provides preview/approval. Record resolved class version and composition revision in status.

Decide binding semantics: snapshot class at creation, follow compatible revisions automatically, or require explicit upgrade. High-consequence capabilities often need controlled opt-in or maintenance windows. Automatic movement can be safe for narrow patches with tested invariants.

Do not encode tenant-specific exceptions into global class names such as `standard-team-a`. Put entitlement and policy in owned policy resources or admission data. Let the domain API remain comprehensible.

Retire classes through usage inventory, successor compatibility, migration preview, opt-in/forced schedules, and proof that no objects depend on the old resolution. Removing a catalog tile does nothing to stored intent.

### Specify schema, defaulting, and validation together

Use structural schemas with types, required fields, bounds, list/map topology, formats, and descriptions. Validation should reject representations the system cannot interpret, while domain policy rejects contexts the caller is not eligible to request.

Defaults are contract behavior. Static safe defaults may live in schema. Tenant, geography, budget, or policy-dependent choices should be resolved by admission or reconciliation and recorded with provenance. A controller-only invisible default makes preview and audit unreliable.

Use CEL or equivalent side-effect-free validation for cross-field and transition invariants: production exposure requires an owner, a regulated class cannot reduce retention below its minimum, and an immutable region policy cannot change after data exists. Bound collections so validation cost is predictable.

Keep schema validation, admission policy, and feasibility distinct. A request can be syntactically valid and authorized yet temporarily infeasible because quota or provider capacity is unavailable. Admission should reject permanent/known violations; reconciliation should report transient conditions without turning admission into a fragile provider call.

Validate old and new object state for hazardous transitions. Creation rules alone do not prevent a later unsafe downgrade. Yet overly strict immutability can block incident recovery; define authorized migration or break-glass protocols rather than ad hoc field edits.

### Make authorization part of the resource model

Define verbs by persona and lifecycle: who may create, read, update which fields, approve exceptional class, invoke restore, see cost, rotate credentials, transfer ownership, or delete retained data. Ordinary RBAC is often resource/verb scoped; sensitive actions may require subresources or separate work resources.

Use namespace-level grants where possible and avoid wildcard permissions. Controllers need only their watched resources, status/finalizer updates, specific child types, and provider credentials. Separate platform administration from tenant consumption.

References cross authority boundaries. The caller’s ability to name a secret, network, identity, or data source does not prove permission to consume it. Require target-side grants or a trusted broker, bind immutable target identity, and avoid leaking whether unauthorized targets exist.

Treat controller service accounts as confused-deputy risks. Admission and reconciliation must preserve the requesting tenant/owner context instead of using controller power to attach any target the caller can guess.

Audit spec changes, policy/class resolution, approvals, forced ownership, external effects, secret publication, adoption, deletion, and break glass. Audit should link principal, object UID/generation, policy revision, composition revision, and operation identity.

### Separate contract, policy, and implementation

The domain contract describes intent and user-visible evidence. Policy decides whether and how that intent is permitted in context. Implementation composes provider resources and performs effects. Keeping them separate permits policy and provider changes without forcing every consumer to learn them.

Resolution can be modeled as $E=R(I,P)$, where $I$ is admitted user intent, $P$ is an identified policy/class revision, and $E$ is an effective plan. Record a digest or structured summary of $E$ so operators can explain why a provider choice occurred.

Make resolution deterministic for the same relevant inputs, or explicitly model time/capacity selection and freeze the result. “Pick any cheapest region on every reconcile” causes oscillation. Stable selection, hysteresis, and migration protocols turn dynamic optimization into controlled behavior.

Composition may use controller code, Crossplane Composition functions, templates, workflow resources, or another engine. This is an internal choice until its limitations change the public promise. Crossplane demonstrates schema-defined composite APIs with separately revisioned compositions; its mechanics do not eliminate domain design.

Templates and portals help users author intent and bootstrap code. They do not replace continuous reconciliation, state, ownership, or lifecycle. A generated repository can drift; the domain API remains the canonical service contract.

### Build a previewable effective plan

Before expensive or destructive effects, let users and reviewers inspect resolved class, provider family, region, availability/recovery properties, estimated cost band, dependencies, policy decisions, replacements, and warnings. Preview must use the same resolver and revisions as execution.

Mark uncertainty. Cost is often an estimate, provider capacity can change, and some identities are allocated later. Do not present false precision. State estimate time, inputs, excluded usage, and expiry.

Bind approved preview to intent generation and policy/composition revision. If any consequential input changes, require a new preview or explicit policy. A screenshot of an old portal page is not an execution authorization.

Avoid exposing the full provider manifest as the primary preview; that recreates cognitive load and may leak secrets. Offer a domain summary first and controlled low-level diagnostics for operators.

Preview itself needs authorization and scale controls. It can reveal provider topology, policies, names, capacity, or price. Cache only safe revision-bound results and rate-limit expensive provider lookups.

### Reconcile through revisioned, idempotent plans

The controller observes current intent, policy, dependencies, owned children, and external reality; resolves one effective plan; performs one bounded safe action; records durable identity/checkpoint; updates status; and requeues. It never assumes create order alone proves readiness.

Use object UID, generation, composition revision, and stable operation IDs for effects. Before retrying an ambiguous external call, observe by identity. Adopt only effects whose ownership and plan digest match; quarantine collisions.

Revision compositions. Roll a new plan to canaries, opt-in objects, tenants, or cohorts. Define whether an existing object stays pinned, accepts compatible updates, or requires migration. Rollback can stop future use, but it may not undo destructive schema/data/provider changes.

Preserve field ownership. User, policy resolver, controller, and integrations should have disjoint spec/status responsibilities. Kubernetes Server-Side Apply can detect field conflicts, but good API boundaries still determine which manager may own each field.

Bound concurrency per tenant/provider/failure domain and use backoff, jitter, circuit breaking, and dependency indexes. A popular domain API can amplify one spec change into many provider calls; fairness and recovery behavior belong in the design.

### Design status for the user’s decision

Status answers whether the promised capability exists for the current generation, what blocks it, what changed, and what the user can do. Include observed generation, stable conditions/reasons, resolved class/policy/composition revision, user-relevant endpoint references, and bounded dependency or cost summaries.

Do not copy secret values. Publish a reference to a separately authorized Secret or brokered credential. Do not dump child resources or raw provider errors into status; provide stable domain reasons plus a trace or diagnostic reference.

Separate progress, readiness, degradation, policy, and lifecycle. A resource can remain `Ready=True` for serving while `Progressing=True` during a safe rollout; a failed optional telemetry child should not falsely mark the core data service unavailable.

Make errors actionable: rejected field, violated rule/policy identity, current condition, retryability, owner, and remedy. “Provisioning failed” creates tickets. Avoid promising exact completion time unless backed by data and a service objective.

Expose effective state because users otherwise cannot distinguish explicit intent from defaults and policy. Keep it bounded and stable; massive rendered manifests belong in controlled artifacts, not watch-hot status.

### Model dependencies and composition boundaries

Use typed references for independently owned capabilities. Each reference needs identity, scope, authorization, required capability/version, readiness/freshness predicate, and deletion behavior. An object’s existence is not a usable dependency.

Composition children are implementation details but still need independent identities, conditions, ownership, finalizers, and operator visibility. Do not flatten every child failure into one generic parent error or let children independently rewrite the parent’s desired state.

Reject strict dependency cycles or redesign them as explicit staged protocols. A platform API that composes identity, network, data, and runtime must have a bootstrap DAG that also works during disaster recovery.

Distinguish lifecycle ownership from reference. A workload may consume a shared database without owning its deletion. Owner references are not authorization or business retention policy.

Index fan-out and propagate shared cause without causing retry storms. A class, network, or identity service used by thousands of objects should recover through bounded waves and report affected counts without copying thousands of condition entries.

### Treat deletion as a first-class product journey

Specify deletion policy at creation when data or cost persists: delete, retain, snapshot-then-delete, transfer, or require approval. Make dangerous defaults conservative and visible. Policy may narrow user choices but should not silently reinterpret them later.

Use finalizers for real external obligations and expose stage, owner, retry, and deadline. A finalizer is not a permanent lock. Provide audited force paths with explicit residual effects and legal/security constraints.

Deletion order differs from creation. Drain traffic, revoke new access, preserve required backup/network/key dependencies, delete or retain effects, verify provider absence/transfer, then remove finalizer. Shared resources must not be deleted because one consumer disappears.

Handle controller absence. Before retiring or reinstalling the API, inventory finalizers and effects; provide a compatible cleanup/migration controller or documented adoption path. Deleting a CRD can remove records while cloud resources remain.

Test name recreation during deletion. Old effects and callbacks must be bound to UID and epoch so a new object with the same name cannot inherit or delete them accidentally.

### Govern escape hatches as evidence

An escape hatch is appropriate when the platform has a real boundary and informed users need a bounded option before it becomes a standard capability. It is not `providerConfig: {}` with unknown fields.

Prefer typed extensions scoped to a provider family or capability, with size limits, allowlists, ownership, validation, authorization, compatibility level, and support statement. Show how the extension affects portability, upgrades, policy, cost, and recovery.

Record and measure use. Repeated similar overrides indicate missing product capability; promote a stable outcome field after research. One-off risky use may remain an approved exception with expiry and accountable owner.

Prevent overrides from disabling platform invariants such as encryption, identity tagging, deletion evidence, network isolation, or audit. If an exception can violate them, model a separate privileged workflow with explicit approval.

Define retirement: migration target, usage query, deadline, and behavior after removal. An unowned extension becomes a permanent compatibility trap.

### Design for multi-tenancy, quotas, and cost

Tenant identity must be unambiguous across namespace, organization, project, account, and provider. Namespace is a useful boundary but not a complete economic or security tenancy model. Bind every object and effect to accountable ownership.

Enforce quotas at meaningful levels: object count, capacity, expensive class, regions, previews, concurrent operations, and provider limits. Reject known hard limit violations early; report temporary provider scarcity through status and fair queues.

Expose cost responsibility without false precision. A class can publish a cost band and major drivers; preview can estimate; status can link actual allocation. Tag effects with tenant, owner, object UID, class, and cost center while protecting sensitive metadata.

Prevent noisy-neighbor behavior in API requests, watches, validation, conversion, controller queues, and providers. Rate limits alone are insufficient; use fair scheduling and per-tenant/provider concurrency.

Test cross-tenant enumeration, reference probing, status leakage, shared dependency failure, quota races, name collisions, and deletion/adoption. The controller’s broad provider credentials make these boundary tests essential.

### Evolve representations and semantics safely

Classify changes: additive optional field, validation tightening, default/policy change, condition change, behavior change, required field, enum removal, identity/scope change, or resource replacement. A syntactically additive change can still be semantically breaking if it changes cost or deletion.

Preserve round trips between served versions and migrate storage explicitly. Use conversion for representation, not provider calls or business migration. Keep converters deterministic, side-effect-free, batch-safe, and available on the API path.

Track clients and field usage through audit/metrics before deprecation. Publish warnings, successor version, semantic differences, migration tooling, and dates. A portal upgrade does not migrate GitOps repositories, SDKs, automation, stored objects, or policy matches.

For incompatible domain change, prefer a new version or kind plus explicit migration resource over contorting old fields. Preserve source UID, ownership, external operation identity, deletion obligations, and rollback boundary.

Version documentation, schemas, examples, SDKs, policies, compositions, and conformance fixtures together. Product release numbers and API versions are related but not identical; one release may serve several versions.

### Test the contract as a state space

Build a matrix across API version, class/policy revision, composition revision, controller version, provider, tenant, lifecycle state, and failure mode. Pairwise selection helps breadth, but high-risk combinations require explicit scenarios.

Test schema boundaries and property-based invariants: absence/null/zero, min/max, enum, list uniqueness/topology, old/new transition, unknown fields, oversized objects, and hostile strings. Test admission authorization and error messages, not only accepted examples.

Use golden fixtures for conversion and effective-plan resolution. For every stored historical shape, round-trip supported versions and verify semantic intent. Recompute plan digests and ensure nondeterministic map order or live provider data does not cause drift.

Exercise controller crashes before/after external calls, stale caches, duplicate events, dependency loss, quota race, provider timeout/throttle, partial composition, deletion, restore from backup, lost status, old callbacks, and leader changes. Prove no duplicate or cross-tenant effects.

Run user-journey tests through YAML/API, CLI, portal, and Git. All should reach the same admitted object and status semantics. Accessibility and documentation tests matter, but the portal must not become the only usable contract oracle.

### Release through evidence and reversible cohorts

Begin with design partners whose journeys shaped the API. Set explicit alpha hypotheses, support arrangements, data/effect disposition, and compatibility expectations. Experimental does not mean unowned.

Gate promotion on more than usage: successful lifecycle journeys, understandable fields/errors, low manual intervention, controller reliability, policy/security review, recovery exercise, migration evidence, support capacity, and stable ownership.

Roll schema, admission, controller, composition, policy, portal, docs, and SDK changes in a compatible sequence. Mixed versions exist during deployment and recovery. Avoid admission rules that reject objects the old controller still writes.

Canary composition/controller revisions by risk-bounded cohort and observe domain outcomes. Have abort criteria and a forward recovery plan; rollback may not reverse provider changes already committed.

Publish change logs in user language: what outcome changes, who is affected, required action, dates, and rollback/support. Internal implementation diffs are insufficient.

### Measure value without gaming adoption

Measure journey outcomes: time and active effort to first usable capability, successful-change rate, time to diagnose/recover, policy violations prevented, support contacts, manual interventions, deletion completion, migration burden, and user satisfaction.

Segment by class, tenant maturity, interface, provider, and journey. A median can hide one regulated cohort that cannot use the API. Compare with the prior path and account for selection bias.

Track API health: admission latency/rejections, reconcile latency, queue age, condition reasons, dependency failure, effect duplication/orphans, conversion traffic/errors, deprecated-version calls, escape-hatch use, and controller resource cost.

Adoption is ambiguous. High object count might mean value, forced mandate, leaked resources, or one automation loop. Low adoption can expose poor discovery, missing capability, risky migration, or a narrow but valuable user group.

Close the product loop. Combine telemetry with interviews, incident/support evidence, abandoned requests, and extension usage. Remove fields and capabilities only through compatible lifecycle; do not accumulate every request into a universal API.

### Recover and retire the domain API

Back up schemas, stored objects, policy/class/composition revisions, controller checkpoints, external identities, credentials/keys under proper custody, and audit evidence. A restored object without the implementation revision that interprets it is incomplete.

After restore, external resources may be newer. Inventory by immutable identity, reconstruct accepted intent, pin compatible controller/composition revisions, invalidate caches, and stage reconciliation from observation to reversible then destructive action.

Retirement begins by stopping new consumers, publishing successor and dates, migrating clients and objects, resolving effects/finalizers, disabling old compositions, measuring zero use, and preserving audit/retention evidence. Removing a portal tile or repository is not retirement.

Decide disposition for retained resources, backups, credentials, DNS, cost ownership, and legal holds. Transfer must update both platform and provider authority; orphaning is not a migration strategy.

Only remove served versions, conversion, controller, CRD/API endpoint, policy, and recovery artifacts after their dependencies are gone in the right order. Validate restore/failback documentation against the remaining system.

## Definitions and Notation

Let:

- $J$ be the set of researched user journeys;
- $f_j$ be the expected frequency of journey $j$ in a fixed period;
- $c_j$ be its current cognitive, coordination, and operational cost;
- $r_j\in[0,1]$ be the fraction of that cost the proposed capability credibly removes;
- $B$ and $M$ be build and lifecycle-maintenance cost in compatible units;
- $V=\sum_{j\in J}f_jc_jr_j-(B+M)$ be a prioritization estimate;
- $I$ be an admitted intent object at UID $u$ and generation $g$;
- $P_k$ be the identified policy/class context revision $k$;
- $R$ be the effective-plan resolver;
- $E_{g,k}=R(I_g,P_k)$ be the resolved plan for that generation and context;
- $d(E)$ be a stable digest of the consequential effective plan;
- $C_r$ be composition/controller implementation revision $r$;
- $O$ be observed internal and external state;
- $A(E,O)$ be the next bounded reconciliation action;
- $S$ be status evidence correlated to $u,g,k,r$; and
- $X$ be the set of accepted escape-hatch usages with owner and expiry.

The value equation is a comparative model. Its inputs are estimates and cannot override safety, regulatory, or ownership constraints. Costs must share a period and unit; otherwise the arithmetic is decorative.

The resolver should be stable: for unchanged relevant $I_g$ and $P_k$, $R$ produces semantically equivalent $E_{g,k}$. If live capacity or price participates, the selection and its expiry become explicit state rather than invisible nondeterminism.

A readiness claim for current intent requires status correlation such as $S.\mathrm{observedGeneration}=g$, compatible policy and composition revisions, fresh dependency evidence, and the documented capability predicate. Object existence or child count is insufficient.

An API change is representation-compatible if supported objects can be decoded and round-tripped as promised. It is semantically compatible only if user-visible meaning, ownership, effects, security, cost class, and lifecycle guarantees remain within the published contract.

## Mechanisms, Invariants, or Proof Structure

### End-to-end design mechanism

1. **Discover journeys.** Observe creation, operation, incident, migration, and deletion; identify repeated decisions and failure costs.
2. **Define capability ownership.** State user, provider, platform, security, finance, and support responsibilities and exclusions.
3. **Bound the domain.** Establish vocabulary, aggregate/resource boundaries, identity, references, and lifecycle.
4. **Choose abstraction.** Expose outcomes and consequential choices; hide replaceable mechanics; budget complexity explicitly.
5. **Specify the contract.** Define fields, classes, defaults, validation, transition rules, authorization, status, errors, and support.
6. **Resolve effective state.** Version policy/class input and produce a previewable, stable effective plan with provenance.
7. **Compose and reconcile.** Pin or control implementation revisions; use idempotent effects, dependencies, bounded work, and finalizers.
8. **Verify failure and recovery.** Exercise provider ambiguity, controller restart, cross-tenant boundaries, restore, and deletion.
9. **Release by cohort.** Use design partners, canaries, abort thresholds, compatibility sequencing, and documented migration.
10. **Measure and learn.** Combine journey outcomes, control-plane health, support evidence, and extension use.
11. **Evolve or retire.** Preserve semantic contracts, migrate stored/effect state, measure zero use, and remove in dependency order.

### Contract-closure invariant

For every admitted state and transition, the platform must define an authorized owner, a reconciliation behavior, observable evidence, failure/retry semantics, and a lifecycle disposition. If one is missing, admission accepts a state the service cannot fully own.

This does not mean every request succeeds. Quota, provider failure, or dependency unavailability may prevent realization. It means the platform can classify the state, preserve safety, provide a remedy/escalation, and eventually reconcile or terminate it according to contract.

### Abstraction-sufficiency test

For each hidden implementation decision, ask whether changing it can alter user-visible availability, recovery, security, geography, interoperability, cost responsibility, or deletion. If yes, the API must expose the outcome, class promise, preview, or controlled migration that governs that consequence.

For each exposed field, ask whether the user owns the decision and can understand its stable meaning independently of one provider. If no, move it behind policy/composition or into a bounded expert extension.

### Resolver stability argument

Suppose unchanged relevant intent $I_g$ and policy revision $P_k$ can resolve alternately to incompatible plans $E_1$ and $E_2$. Reconciliation may perpetually replace or mutate effects despite no desired change. Therefore deterministic resolution, or persisted selection with explicit renewal/migration, is necessary for convergence. This is a proof sketch of a stability condition, not proof that the controller or provider converges.

### Ownership invariant

The user owns documented intent fields; policy owners own identified policy resources; the controller owns status and explicitly controller-managed metadata/finalizers; provider effects are bound to object UID and operation identity. No actor silently steals another’s field ownership. Forced override is exceptional, authorized, and audited.

### Semantic-version invariant

While a version remains served, its fields and documented meanings remain supported. Conversion preserves representable information. A default, class, or composition change that materially alters promised outcomes is rolled through a compatible revision or explicit migration rather than hidden behind unchanged YAML.

### Security-boundary invariant

Admission and reconciliation authorize both the source action and referenced target use, preserve tenant context despite controller privilege, avoid secret disclosure, and constrain provider effects to the object’s owned scope. Status/errors do not reveal unauthorized target existence.

### Lifecycle invariant

Creation establishes identity, ownership, resolved policy, and deletion disposition before external effects. Updates preserve or migrate those bindings. Restore reconciles external-ahead state by identity. Deletion/retirement discharges or transfers effects, credentials, retention, cost, and audit obligations before records/controllers disappear.

### Executable API-quality inventory

The following synthetic inventory checks whether ten proposed field patterns express user outcome and maintain bounded ownership. It does not validate a CRD, cluster, provider, policy, or production usability.

<!-- bijux-verify: {"id":"domain-api-field-inventory","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"contract=5\nexception=2\nleak=3\n"}} -->
```python
fields = [
    {"name": "serviceClass", "outcome": True, "bounded": True, "typed": True},
    {"name": "recoveryTier", "outcome": True, "bounded": True, "typed": True},
    {"name": "regionPolicy", "outcome": True, "bounded": True, "typed": True},
    {"name": "deletionPolicy", "outcome": True, "bounded": True, "typed": True},
    {"name": "consumerIdentityRef", "outcome": True, "bounded": True, "typed": True},
    {"name": "providerTuning", "outcome": False, "bounded": True, "typed": True},
    {"name": "approvedExtension", "outcome": False, "bounded": True, "typed": True},
    {"name": "terraformModule", "outcome": False, "bounded": False, "typed": False},
    {"name": "rawIamJson", "outcome": False, "bounded": False, "typed": False},
    {"name": "cloudSku", "outcome": False, "bounded": False, "typed": True},
]

counts = {"contract": 0, "exception": 0, "leak": 0}
for field in fields:
    if field["outcome"] and field["bounded"] and field["typed"]:
        counts["contract"] += 1
    elif field["bounded"] and field["typed"]:
        counts["exception"] += 1
    else:
        counts["leak"] += 1

for category in ("contract", "exception", "leak"):
    print(f"{category}={counts[category]}")
```

The classifier is deliberately conservative. `providerTuning` and `approvedExtension` may be governed exceptions, but their non-outcome semantics keep them out of the core contract. A typed `cloudSku` still leaks a provider concept; typing alone does not create a durable abstraction.

### Verification matrix

Verify at least: representative and hostile schemas; all field transitions; persona/tenant authorization; reference grants; policy/class resolution determinism; preview/execution revision binding; composition canary and rollback; field ownership conflicts; idempotency after ambiguous effects; dependency loss and recovery; status freshness and secrecy; quotas and fairness; conversion round trips; old clients/controllers; snapshot restore with external-ahead effects; deletion/force paths; class/API deprecation; and full retirement.

Evidence should include user-journey observations, reviewed capability contract, schema/admission tests, threat model, resolver golden fixtures, controller fault tests, provider inventories, SLO/queue metrics, recovery exercise, conversion/migration reports, deprecated-client telemetry, escape-hatch inventory, support outcomes, and retirement disposition.

## Alternatives and Trade-Offs

### Domain API versus provider API passthrough

A domain API reduces recurring cognitive load and permits backend replacement, but the platform owns semantics, migrations, support, and edge cases. Passthrough exposes provider power quickly but couples users to one implementation and transfers expertise. Offer passthrough only as an explicit expert surface, not a falsely portable core.

### Coarse aggregate versus composable resources

A coarse resource simplifies the main journey and can enforce end-to-end invariants, but couples lifecycles and permissions. Smaller resources preserve ownership and reuse but expose dependency design. Use aggregates around coherent user outcomes and typed references across independent domains.

### Few opinionated fields versus broad configurability

Few fields create a strong pit of success and manageable compatibility surface, but may exclude legitimate workloads. Broad configuration improves reach while increasing cognitive load, testing, security, and provider leakage. Research exceptions and promote stable outcomes rather than accumulating knobs.

### Static default versus context-resolved policy

Static defaults are predictable and schema-visible but cannot reflect tenant/regulatory context. Policy resolution supports context but can surprise users and drift. Identify the policy revision, preview and record effective state, and define whether existing objects follow changes.

### Pinned composition versus automatic revision

Pinning makes outcomes reproducible and rollback boundaries clear but leaves upgrade work. Automatic revisions accelerate patches and consistency but can mutate thousands of effects. Use compatibility classification and risk-bounded rollout rather than one global rule.

### Admission rejection versus asynchronous condition

Admission gives immediate feedback for deterministic, known violations but becomes fragile if it calls providers or depends on volatile capacity. Asynchronous reconciliation tolerates external uncertainty but accepts pending objects. Reject permanent invalidity early; represent transient feasibility in status.

### Kubernetes CRD versus standalone API

A CRD gains discovery, watch, metadata, RBAC, admission, and controller patterns but shares control-plane/storage constraints and Kubernetes semantics. A standalone API supports custom transactions, high-volume data, or non-resource workflows but requires its own machinery. Choose from domain fit, not team habit.

### Resource desired state versus immutable work resource

Desired state suits continuously maintained capabilities. Immutable work resources preserve one-time operation intent and terminal history but can proliferate. Use them for restore, migration, or approval actions whose identity matters; do not encode edge-triggered commands in mutable booleans.

### Portal-first versus contract-first delivery

A portal improves discoverability and guided input but can hide automation gaps or fork validation. Contract-first supports Git/CLI/SDK and stable automation; it still needs good user experience. Build portal forms as projections over the same schema and policy.

### Strict portability versus optimized provider classes

Strict common-denominator APIs ease backend movement but may discard valuable features. Provider-optimized classes offer capability and cost advantages but reduce portability. State the portability unit honestly and make migrations/class differences explicit.

### No escape hatch versus governed extension

No extension protects simplicity and support but can force shadow platforms. A governed extension captures legitimate needs but creates compatibility and security debt. Bound, measure, review, and expire it; never promise full support implicitly.

### Automatic deletion versus retained effects

Automatic deletion reduces leaks and cost but risks irreversible data loss. Retention protects data but leaves cost and ownership obligations. Make disposition explicit, policy-constrained, and verified at the provider boundary.

## Failure Modes and Misconceptions

1. **“A CRD is a platform API.”** A CRD supplies machinery; it does not define a researched capability or service promise.
2. **“Users asked for every field.”** Requests often mirror current workarounds; research the underlying outcome before freezing mechanics.
3. **“Provider-neutral names make it portable.”** Hidden semantics and effects can remain provider-specific despite renamed fields.
4. **“One `Application` gives a simple experience.”** It can centralize unrelated ownership, failure, permission, and deletion into one blast radius.
5. **“More optional fields are backward-compatible.”** They expand semantic, testing, support, policy, and future migration obligations.
6. **“A class can evolve invisibly.”** Silent resolution changes can alter availability, cost, geography, or data movement.
7. **“Defaults are implementation details.”** They determine stored/effective meaning and user outcomes.
8. **“Schema-valid means provisionable.”** Authorization, policy, dependency, quota, provider capacity, and lifecycle feasibility remain.
9. **“Admission should verify the provider.”** Synchronous external checks add availability and stale-observation failure to the write path.
10. **“Namespace makes references safe.”** Cross-boundary target consent and confused-deputy controls can still be required.
11. **“The controller may use its permissions for the user.”** That can turn guessed references into unauthorized provider effects.
12. **“Status should show everything operators know.”** It is watch-hot and user-readable; secrets and unbounded diagnostics belong elsewhere.
13. **“A provider error is actionable.”** Users need a stable domain reason, retryability, owner, and remedy.
14. **“Templates reconcile infrastructure.”** They render or execute once; ongoing drift and lifecycle require authoritative state and controllers.
15. **“Portal users do not need an API contract.”** Forms, Git, CLI, SDKs, audit, and automation must share semantics.
16. **“Server-Side Apply solves ownership design.”** It detects field conflicts only after the API defines meaningful ownership boundaries.
17. **“Rollback restores the old world.”** External schema, data, identity, or provider changes may require forward recovery.
18. **“Escape-hatch demand proves flexibility.”** It can instead reveal a missing capability or an abstraction at the wrong level.
19. **“Object count proves adoption.”** Mandates, automation, leaks, or unused resources can inflate it without value.
20. **“Stopping new creates retires the API.”** Clients, stored versions, effects, finalizers, credentials, backups, and policies remain.

## Worked Examples

### Example 1

**Situation.** Teams request an API that exposes every managed PostgreSQL setting because tickets currently ask for those settings.

**Reasoning.** Interviews reveal recurring outcomes: recovery tier, maintenance constraint, capacity band, geographic policy, consumer identity, and deletion disposition. The platform exposes those fields and maps them to provider configuration. Rare expert tuning becomes a typed, approved extension with expiry.

**Conclusion.** Model the job beneath the workaround, not the ticket vocabulary verbatim.

### Example 2

**Situation.** `standard` currently resolves to a single-zone database; the platform wants multi-zone by default.

**Reasoning.** The change affects cost, topology, maintenance, and possibly replacement. Existing objects record `classRevision: standard-3` and remain pinned. New objects use revision 4; owners receive previewed migration options. A security-only non-effect patch could use a different automatic compatibility policy.

**Conclusion.** A stable class name does not justify silent semantic migration.

### Example 3

**Situation.** A portal proposes a production service with a public endpoint, no owner, and cheapest-region selection.

**Reasoning.** The underlying API rejects missing ownership and requires a defined exposure policy. Dynamic region selection is resolved once, recorded with policy revision and cost estimate, and changes only through migration. The portal explains the same rules; it does not carry unique validation.

**Conclusion.** Guided UX projects the contract; it cannot substitute for it.

### Example 4

**Situation.** A workload references a database in another namespace, and the platform controller can read both.

**Reasoning.** Controller permission does not grant the workload owner use of the database. Admission requires a target-owned grant for the source namespace, kind, and capability; reconciliation binds database UID and reports `ReferenceNotPermitted` without revealing unauthorized details.

**Conclusion.** Preserve caller authority across privileged control-plane execution.

### Example 5

**Situation.** A provider create times out, and the resource has no status because the controller crashed.

**Reasoning.** The controller searches using object UID and stable operation identity before retry. A matching resource with the expected plan digest is adopted; a collision is quarantined. Reissuing a blind create could duplicate cost or data endpoints.

**Conclusion.** API design includes durable effect identity and ambiguous-outcome recovery.

### Example 6

**Situation.** Product teams repeatedly use an extension to request read replicas.

**Reasoning.** Usage shows a coherent latency/availability job. The platform researches topology, failover, consistency, cost, monitoring, and deletion, then adds a bounded `readScale` outcome in a new compatible API revision. Existing opaque extension values migrate with fixtures and preview.

**Conclusion.** Extension telemetry is product-discovery evidence, not permission for permanent blobs.

### Example 7

**Situation.** A new composition changes three child resources and sometimes replaces the database.

**Reasoning.** The resolver previews replacements and consequence. Existing objects are pinned; canary objects opt in by composition revision. Abort stops expansion, but replaced data needs forward recovery from backups rather than a controller binary rollback.

**Conclusion.** Revision and rollout policy must match effect reversibility.

### Example 8

**Situation.** Restoring yesterday’s control-plane snapshot finds a newer provider database absent from restored status.

**Reasoning.** Operators inventory effects by UID, policy/composition digest, operation ID, tenant, and audit trail. Matching accepted intent is reconstructed and adopted; ambiguity is quarantined. The controller remains observation-only until classifications are approved.

**Conclusion.** Recovery reconciles restored intent with external-ahead reality; it never treats absence as delete authority.

### Example 9

**Situation.** A retained data service is deleted, but the namespace and team are also being removed.

**Reasoning.** Retention requires a new owner and cost center, provider authority transfer, credential rotation, backup/legal policy, and a recorded platform disposition. Without an accepted transferee, deletion blocks with an actionable condition or follows an authorized destructive policy.

**Conclusion.** `Retain` is an ownership workflow, not “leave the cloud object somewhere.”

### Example 10

**Situation.** Metrics show 20,000 objects, but users still open tickets for connection and incident diagnosis.

**Reasoning.** Object count came from mandated automation. Journey data shows long time to usable credentials, confusing status, and repeated manual repair. The platform changes credential delivery and domain reasons, measures completion/support outcomes, and does not celebrate raw adoption.

**Conclusion.** Measure the value stream and lifecycle experience, not interface activity alone.

## Cross-Program Connections

1. **Domain-Driven Design:** bounded contexts, ubiquitous language, aggregates, and context maps shape resource boundaries and ownership.
2. **API & Service Engineering:** schemas, compatibility, error semantics, idempotency, authorization, quotas, and deprecation define the public contract.
3. **Product Management:** user research, jobs, hypotheses, design partners, adoption, and outcome metrics determine what the platform should expose.
4. **Distributed Systems:** partial failure, retries, stale observations, leases, identity, and eventual convergence govern controller behavior.
5. **Database Systems:** durable state, schema evolution, migration, backup, retention, and external-ahead recovery constrain lifecycle.
6. **Security Engineering:** least privilege, reference grants, confused deputy, secret handling, audit, tenancy, and break glass protect self-service.
7. **Reliability Engineering:** service contracts, SLOs, degraded modes, fault injection, recovery, and error budgets make promises operable.
8. **Software Architecture:** abstraction, information hiding, coupling, modularity, stable interfaces, and replacement boundaries determine longevity.
9. **Economics and FinOps:** cost bands, attribution, quotas, externalities, and value models connect API choices to accountable consumption.
10. **Human-Computer Interaction:** cognitive load, progressive disclosure, actionable errors, accessibility, and consistent interfaces determine usability.

## References

1. CNCF TAG App Delivery. [CNCF Platforms White Paper](https://github.com/cncf/tag-app-delivery/blob/main/platforms-whitepaper/latest/index.md). Retrieved 2026-09-02.
2. Kubernetes SIG Architecture. [API Conventions](https://github.com/kubernetes/community/blob/main/contributors/devel/sig-architecture/api-conventions.md). Retrieved 2026-09-02.
3. Kubernetes. [Custom Resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/). Retrieved 2026-09-02.
4. Kubernetes. [Extend the Kubernetes API with CustomResourceDefinitions](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/). Retrieved 2026-09-02.
5. Kubernetes. [Common Expression Language in Kubernetes](https://kubernetes.io/docs/reference/using-api/cel/). Retrieved 2026-09-02.
6. Kubernetes. [Versions in CustomResourceDefinitions](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definition-versioning/). Retrieved 2026-09-02.
7. Kubernetes. [Kubernetes Deprecation Policy](https://kubernetes.io/docs/reference/using-api/deprecation-policy/). Retrieved 2026-09-02.
8. Kubernetes. [Server-Side Apply](https://kubernetes.io/docs/reference/using-api/server-side-apply/). Retrieved 2026-09-02.
9. Kubernetes. [Kubernetes API Concepts](https://kubernetes.io/docs/reference/using-api/api-concepts/). Retrieved 2026-09-02.
10. Kubernetes. [Role Based Access Control Good Practices](https://kubernetes.io/docs/concepts/security/rbac-good-practices/). Retrieved 2026-09-02.
11. Kubernetes. [Validating Admission Policy](https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/). Retrieved 2026-09-02.
12. Crossplane. [Composite Resource Definitions](https://docs.crossplane.io/latest/composition/composite-resource-definitions/). Retrieved 2026-09-02.
13. Crossplane. [Compositions](https://docs.crossplane.io/latest/composition/compositions/). Retrieved 2026-09-02.
14. Backstage. [Software Templates](https://backstage.io/docs/features/software-templates/). Retrieved 2026-09-02.

## Exercises

### Exercise 1

Research and design a domain API for an internal PostgreSQL capability. Define users, journeys, capability contract, resource boundary, core fields, classes, status, authorization, deletion, and explicit non-goals.

### Exercise 2

Design effective-plan resolution for two classes, three tenants, two providers, and changing policy. Specify deterministic inputs, preview, revision binding, rollout, rollback boundary, and evidence that prevents silent semantic drift.

### Exercise 3

Threat-model cross-namespace identity, network, secret, and data references for a privileged platform controller. Define admission, target consent, status/error disclosure, audit, and adversarial tests.

### Exercise 4

Plan an incompatible evolution from `DatabaseClaim/v1beta1` to `DataService/v1` while objects, providers, Git clients, portal users, policies, finalizers, and backups remain active. Include rollback and retirement gates.

### Exercise 5

Design the verification and product-measurement program for a multi-tenant domain API. Cover schema/state space, controller failure, provider ambiguity, recovery, fairness, user journeys, extension evidence, promotion, and retirement.

## Answers to the Exercises

### Answer 1

Start with design partners from product teams, database operations, security, finance, and incident support. Observe request, access, resize, maintenance, restore, ownership transfer, and deletion. The capability promise includes an available PostgreSQL endpoint, encryption, backup/recovery tier, maintenance constraints, cost attribution, support, and provider-independent identity; it excludes arbitrary extensions, application schema administration, and synchronous creation guarantees.

Use namespaced `DataService` for the maintained aggregate and immutable `DataRestore` for each restore operation. Core spec fields are `serviceClass`, capacity band, engine compatibility, region policy, recovery tier, maintenance window, consumer identity reference, cost center reference, and deletion policy. Do not expose subnet IDs, provider SKU, raw IAM, parameter groups, or Terraform modules.

Define `standard` and `critical` by availability, recovery, security, maintenance, and cost band, each at an identified class revision. Status includes observed generation, capability conditions, resolved class/policy/composition, provider-neutral endpoint and secret references, recovery evidence, cost band, and actionable reasons. Namespaced roles allow teams to create/read/update ordinary intent; exceptional class, restore, ownership transfer, and destructive deletion use separate authorization. Cross-namespace references require target grants and UID binding.

Deletion drains consumers as contracted, snapshots where required, revokes access, deletes/transfers/retains provider effects, verifies disposition, and then clears finalizer. Non-goals include high-volume application data, SQL migration, arbitrary provider configuration, cross-object transactions, and an availability promise unsupported by the database owner. Validate the contract with real full-lifecycle journeys before GA.

### Answer 2

Let admitted intent $I_g$ include class and outcome constraints. Let $P_k$ contain tenant entitlement, residency, budget, provider allowlist, and class definition at revision $k$. Resolution $R(I_g,P_k)$ chooses provider family, region, topology, recovery configuration, and composition revision using only identified inputs. Persist `policyRevision`, `classRevision`, selection, plan digest, and expiry if any live quote/capacity influenced the choice.

For three tenants, policy can allow both providers for ordinary tenant A, require provider 1 and one jurisdiction for regulated tenant B, and cap tenant C at `standard`. Policy violations reject at admission when deterministic. Temporary provider capacity becomes a pending condition. The preview shows effective outcomes, provider family where permitted, replacements, cost band, uncertainty, and policy rationale; approval binds generation and revisions.

New policy does not silently mutate existing plans. Classify changes as no-effect, compatible in-place, or migration/replacement. Roll compatible revisions by tenant/cohort with health gates; require explicit migration for consequential changes. Rollback stops new selection and restores the prior resolver/composition for untouched objects. Already completed destructive/provider changes use a forward recovery plan. Golden fixtures prove the same inputs yield the same semantic plan and that every recorded historical revision remains interpretable.

### Answer 3

Assets include target existence, secret data, provider authority, tenant resources, controller credentials, and status/audit. Threats include reference guessing, label capture, name recreation, confused-deputy attachment, status enumeration, stolen controller identity, grant race, and cross-tenant deletion.

Use typed references with group/kind/namespace/name and bind resolved UID. Require target-owned consent describing allowed source namespace/kind and capability for identity, network, and data. Secret references permit a broker/controller to publish a separately scoped credential, never copy the secret into ordinary status. Admission checks structural scope and grants without provider calls; reconciliation rechecks grant and UID before every material effect. Revocation behavior is capability-specific and observable.

Before authorization, errors say `ReferenceNotPermitted` rather than missing/existing details. Controller provider roles are partitioned by tenant/account where feasible and effects carry tenant plus object UID. Audit links requester, grant, target UID, object generation, controller principal, plan, and operation ID.

Tests attempt unauthorized existing/nonexisting names, grant create/revoke races, target name recreation, mutable selector capture, namespace transfer, stale cache, forged status, controller credential misuse, cross-tenant list/watch, and deletion of a target with consumers. Passing requires identical nondisclosing errors, no unauthorized effect, eventual revocation behavior, and durable audit evidence.

### Answer 4

Inventory beta API calls, manifests, field managers, stored objects, class/composition revisions, policy matches, finalizers, provider effects, backups, and controller checkpoints. Define semantic mapping to `DataService`: field transformations, changed defaults, unsupported states, identity/ownership, status, deletion, and effect adoption. Do not pretend a kind/group rename is conversion alone.

Ship `DataService/v1`, policies, controller, portal, SDK, docs, and migration tooling while beta remains served and operated. Create a migration work resource per source UID. It freezes hazardous beta changes, previews mapping/replacement, obtains required approval, creates the v1 object with source/effect identity, adopts or migrates provider resources idempotently, transfers consumers and finalizer obligations, validates outcomes, and marks beta retired. Backups include both schemas and mapping revisions.

Canary low-risk objects and every historical fixture. Rollback before effect transfer removes the candidate. After irreversible data/provider migration, forward recovery restores the target or re-adopts effects; deleting v1 is not rollback. Track Git repositories, SDK clients, policies, portal submissions, audit traffic, stored versions, and effects separately.

Stop new beta creation, warn clients, publish dates, and provide reports. Remove beta only after zero requests for the observation window, all objects/effects/finalizers migrated or explicitly disposed, restores tested, old policies/templates removed, and support sign-off. Then retire controller paths, served/storage versions, conversion/migration components, and obsolete recovery artifacts in dependency order.

### Answer 5

Build a matrix over API/class/policy/composition/controller/provider/tenant/lifecycle/failure. Test schema bounds, absent/null/zero, transition rules, field ownership, admission messages, entitlements, target grants, quotas, and conversion fixtures. Verify plan determinism and preview binding. Fault tests crash around provider calls, duplicate events, lose dependencies, throttle providers, change leaders, restore snapshots, remove status, replay callbacks, and race delete/recreate. Check UID/operation identity, no cross-tenant effect, fair progress, bounded queues, and complete deletion disposition.

Run isolated recovery from backed-up objects, schemas, policy/class/composition revisions, keys, and operation stores. Inventory external-ahead resources, adopt matching effects, quarantine ambiguity, and release reconciliation in waves. Validate domain endpoints, security, recovery tier, cost ownership, stale-authority denial, and renewed backup—not merely API/controller health.

Measure time and active effort to discover/request/connect/change/recover/delete; success and abandonment by cohort; support/manual work; policy violations; duplicate/orphan effects; reconcile latency; queue fairness; admission/conversion errors; deprecated clients; and extension usage. Combine telemetry with interviews and incident reviews.

Alpha promotion requires successful full lifecycle, stable semantics, threat review, recovery drill, support ownership, migration path, and evidence that users understand fields/errors. Extension clusters feed research. Retirement requires successor adoption, zero client and stored use, effect/finalizer/credential disposition, restore evidence, and removal in dependency order. Raw object count or portal clicks satisfy none of these gates.
