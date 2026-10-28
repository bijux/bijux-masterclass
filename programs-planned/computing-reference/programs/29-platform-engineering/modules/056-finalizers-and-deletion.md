---
module_id: PLAT-056
program: Platform Engineering
level: 2
module_number: 56
title: Finalizers and Deletion
status: complete
last_verified: 2026-09-02
---

# Finalizers and Deletion

## One-Page Review

### Governing question

How should a controller hold, execute, explain, override, and eventually release deletion so external resources and dependent obligations are neither leaked nor destroyed under ambiguity, concurrency, failure, and operator retirement?

### Essential definitions

- A **deletion request** asks Kubernetes to begin removing an object; it is not proof that cleanup or physical removal has completed.
- A **deletion timestamp** is immutable API metadata marking that deletion has been accepted and finalization may proceed.
- A **finalizer** is a qualified key in `metadata.finalizers` that retains an object until its owning controller removes that key; it is not code or an ordered callback.
- A **cleanup obligation** is one durable responsibility that must be satisfied, explicitly orphaned, waived under policy, or transferred before release.
- **garbage collection** removes Kubernetes dependents using owner references and a propagation policy.
- **foreground**, **background**, and **orphan** propagation govern whether and when owners and dependents are removed; they do not clean arbitrary external systems.
- A **tombstone** is minimal retained identity and disposition evidence after the primary API object disappears.
- **force finalization** removes a blocking constraint without establishing that its obligation succeeded.
- An **orphan policy** intentionally leaves an external or dependent resource under a named owner and support model.
- A **stuck deletion** is a deletion whose progress or evidence violates its service objective; age alone does not identify the safe remedy.

### Central model, mechanism, or theorem

For finalizer owner $c$, let $O_c$ be its required obligation set and $d(o)$ the durable disposition of obligation $o$. The controller may remove its key only when deletion is requested and

$$
\forall o\in O_c,\quad d(o)\in\{\text{Satisfied},\text{AuthorizedOrphan},\text{Transferred}\}.
$$

`Unknown` is not success. Before creating any external responsibility, install the finalizer and confirm the write; after `deletionTimestamp` is set, stop ordinary provisioning and reconcile a repeat-safe cleanup protocol. Use immutable resource UID and external IDs, observe ambiguous effects, checkpoint each obligation, remove only the controller’s own key with optimistic concurrency, and retain tombstone/audit evidence through late-response and recovery horizons. Safety—never release early—does not imply liveness; progress also needs a running compatible controller, permission, reachable dependencies, bounded ambiguity, and an authorized outcome for every obligation.

### Critical invariants

- The finalizer is durably present before the controller creates an external resource or other obligation that Kubernetes garbage collection cannot recover.
- Deletion timestamp permanently switches authority from ordinary desired-state work to the documented deletion policy; the object is never resurrected in place.
- Every cleanup action has stable resource UID, target identity, idempotency, preconditions, checkpoint, and unknown-outcome handling.
- Finalizer owners coordinate through explicit resources or conditions, never list order; finalizers may execute concurrently and be reordered.
- A controller removes only its own qualified finalizer and preserves unrelated keys through resource-version conflicts.
- `NotFound` counts as satisfied only when scope, identity, prior evidence, and provider semantics make absence authoritative.
- Foreground garbage collection covers only discoverable blocking dependents with valid owner references; external inventory is verified separately.
- Orphan, retain, transfer, force, and waive are privileged dispositions with owner, reason, scope, expiry where relevant, and audit.
- Progress age, obligation state, retry/backoff, last error, and safe operator action remain observable while the object exists.
- Controller, webhook, CRD, credentials, and finalizer retirement are sequenced so no live or restorable object retains an unserviceable key.

### Common failures

Adding a finalizer after provisioning; treating finalizer position as order; putting several teams’ work behind one vague key; removing every finalizer to unstick an object; deleting by reusable name; treating timeout or `NotFound` as verified deletion; continuing create/update after deletion begins; relying on foreground propagation for external cloud resources; waiting forever without conditions or alerts; setting a fixed deadline that silently abandons data; granting broad finalizer-patch and provider-delete privileges to incident users; uninstalling a controller or CRD before draining keys; changing finalizer names during upgrade; and claiming a forced API disappearance proves environmental cleanup.

### Compact example

A `Database` with UID `u7` is admitted with finalizer `databases.platform.example/delete`. Before provisioning, the controller confirms that key is stored. Deletion later freezes ordinary plan changes and materializes obligations: disable traffic, take a policy-required verified snapshot, revoke credentials, delete provider database ID `db-41`, publish billing closure, and retain a tombstone. Each action has a stable UID-derived operation key. A lost provider delete response leaves `DeleteDatabase=Unknown`; lookup by immutable provider ID resolves it. Only after every required item is satisfied, transferred, or explicitly orphaned by authorized policy does the controller conditionally remove its own key. A manual force path records unresolved `db-41`, tenant, approver, consequence, and follow-up owner; it does not rewrite history as successful deletion.

### Connections

This module applies reconciliation from [PLAT-052](052-desired-state-and-reconciliation.md), workflow state from [PLAT-054](054-operator-state-machines.md), and repeat-safe effects from [PLAT-055](055-idempotent-reconciliation.md). It also depends on workload ownership from [PLAT-024](024-pods-workloads-and-controllers.md) and upgrade policy from [PLAT-049](049-upgrade-and-deprecation-policies.md). PLAT-057 continues with status and drift, while PLAT-058 develops dependency graphs beyond deletion.

## Governing Question

How can a platform guarantee that deleting an API object initiates the correct domain retirement protocol, preserves enough evidence to recover from partial failure, and eventually releases the object without turning “Terminating” into either an indefinite outage or a destructive shortcut?

Creation adds state; deletion removes the record that explains what state exists. This makes deletion structurally dangerous. If the Kubernetes object disappears before a controller deletes or transfers a cloud database, DNS delegation, encryption key, backup, credential, or billing association, the control plane may lose the identity required to find it. If the object remains forever, namespaces, applications, upgrades, and controller retirement can stall.

Finalizers create a deliberate interval between deletion request and API removal. That interval is valuable only when it is backed by a precise protocol: who owns the key, which obligations it protects, how effects are retried, what evidence releases the key, how progress is observed, and what happens when automatic cleanup is impossible.

## Why This Matters

Deletion is a systems lifecycle, not a CRUD footnote. Data retention law may require preserving a backup while privacy law may require erasing primary data. Network teardown must prevent new traffic before removing endpoints. Identity revocation may need to precede resource handoff. Billing closure should happen once, even if provider deletion takes hours.

Kubernetes gives multiple mechanisms with different boundaries. A deletion timestamp and finalizers retain the API object. Owner references and garbage collection handle Kubernetes dependency relationships. Pod grace periods give processes time to stop. Provider APIs delete external assets. None substitutes automatically for the others.

Failures are inevitable during teardown. The provider may complete a delete while the response is lost. A dependent kind may no longer be discoverable. An admission webhook may be unavailable. Two finalizer owners may wait on each other. Credentials needed for cleanup may be revoked too early. Restoring an old cluster backup can resurrect objects whose external resources were already deleted or reassigned.

Operational pressure makes mistakes more likely. A stuck namespace invites broad finalizer stripping; an uninstall script may delete the controller deployment first; a force-deleted Pod may continue using shared storage on an unreachable node. Good platform design makes consequences visible and supplies narrow, audited repair operations before an incident.

## Prerequisites and Retrieval

Retrieve Kubernetes object metadata, qualified names, names and UIDs, delete options and preconditions, watch/reconcile behavior, owner references, garbage collection, foreground/background/orphan propagation, grace periods, finalizers, resource versions and patch conflicts, namespaces and discovery, admission webhooks, CRDs, RBAC, leader election, idempotency, ambiguous outcomes, desired-state controllers, dependency graphs and topological ordering, state machines, safety and liveness, distributed transactions, tombstones, data retention, backup/restore, credential lifecycle, audit, incident management, service objectives, and decommissioning.

You should distinguish request acceptance from removal; deletion timestamp from deletion completion; finalizer key from cleanup implementation; finalizer set membership from execution order; owner reference from label; garbage collection from external cleanup; graceful process termination from API finalization; `NotFound` from verified absence; orphan from leak; force from success; delete permission from permission to mutate finalizers; one API object from one domain resource; controller shutdown from protocol retirement; and safety from liveness.

## Learning Objectives

After completing this module, you should be able to:

1. explain Kubernetes two-stage deletion and the exact role and limitations of finalizers;
2. acquire finalizer ownership before external effects and branch reconciliation correctly after deletion begins;
3. model deletion as durable, idempotent, observable cleanup obligations with explicit dispositions;
4. choose owner references and foreground, background, or orphan propagation appropriately;
5. order dependent domain teardown without relying on finalizer-list order;
6. recover safely from timeouts, missing resources, conflicts, dead controllers, and invalid ownership;
7. design privileged orphan, transfer, waive, and force procedures with bounded consequences;
8. evolve and retire controllers, finalizer names, webhooks, CRDs, credentials, and restore artifacts safely; and
9. verify deletion with crash, concurrency, dependency, security, and disaster-recovery tests.

## Core Exposition

### Understand the Kubernetes deletion state transition

For an object without blocking finalizers, a successful delete can quickly make the object disappear. When finalizers are present, the API server accepts deletion, sets immutable `metadata.deletionTimestamp`, restricts finalizer changes so new keys cannot be added, and returns HTTP 202. The object remains readable and watchable while keys remain. Removing the last key permits storage removal.

This is not a callback registry. A finalizer string names an ownership claim, and some controller must watch the object and implement the behavior. A misspelled or abandoned key has no executable meaning and can retain the object indefinitely. Custom finalizer names must be publicly qualified, such as `databases.platform.example/delete`.

Deletion cannot be cancelled by clearing the timestamp. Once requested, the object cannot be resurrected; a similar object must be created as a new incarnation with a new UID. Controllers should therefore stop ordinary create/update convergence as soon as they observe deletion and execute only behavior explicitly allowed by the deletion protocol.

The object can still be updated while terminating, subject to API and admission rules, but that mutability is not permission to reinterpret destruction freely. Snapshot deletion policy, target identities, and required obligations before ambiguity. Reject or ignore ordinary spec changes after deletion according to the API contract; support repair inputs through a narrow, authorized operation or status/evidence resource.

### Acquire the finalizer before external responsibility

The most important creation-side ordering rule is: persist the finalizer before creating anything whose lifecycle depends on it. A correct normal reconcile commonly follows this shape:

1. read the current object;
2. if deletion is already requested, never add a new finalizer and enter deletion handling only if the owned key exists;
3. if the owned finalizer is absent, add it with optimistic concurrency and return;
4. on a later reconcile, confirm the stored key and then create external state;
5. record immutable external identity and effect evidence.

If a controller creates a database first and crashes before adding its finalizer, deleting the Kubernetes object can erase the only cleanup anchor. Admission-time finalizer injection can close some gaps but adds webhook availability and upgrade dependencies. Controller-time acquisition is often sufficient if the controller never performs the external effect in the same transaction that first requests the key.

Do not install a finalizer merely because a controller recognizes a kind. Each key should protect concrete obligations. Unnecessary keys increase deletion latency and couple resource availability to another controller. Conversely, a controller that creates responsibility must not depend on a later best-effort key write.

### Give one key one durable owner and contract

Use a qualified, stable name whose organizational owner remains clear. Document the API kinds, external systems, obligation categories, release predicate, status/metrics, escalation, repair interface, compatibility window, and retirement process.

One controller may own several internal obligations behind one key when it can coordinate them coherently. Do not make several independently deployed teams share one generic finalizer: no actor can safely decide that everyone is done. If teams need separate release authority, use separate keys and explicit dependency state.

Finalizers form a set for semantics even though serialized as a list. Kubernetes does not enforce execution order, and authorized actors can reorder the field. Two owners that depend on list position are incorrect. If cleanup A must precede B, encode that relationship in a domain operation resource, condition, lease, or shared orchestrator with one finalizer owner.

Controllers remove only their own key. A merge/JSON Patch or current-object update must preserve all unrelated keys and handle `resourceVersion` conflict by rereading. Never assign an empty list as ordinary error recovery.

### Materialize cleanup obligations

Deletion should be explainable as a finite set or graph of obligations. For a database, possible items are stop admission, drain traffic, take/verify final backup, revoke client credentials, delete read replicas, delete primary, remove DNS, close billing, publish audit, and retain a tombstone.

Persist for each item: stable ID, type, target UID/provider ID, dependency set, policy source/revision, state, operation correlation, attempts, last observation, absolute deadline or escalation time, outcome evidence, and disposition authority. Keep sensitive data out of status; link to protected records when necessary.

Useful states include `Pending`, `InProgress`, `OutcomeUnknown`, `Satisfied`, `Blocked`, `AuthorizedOrphan`, and `Transferred`. `Failed` needs semantics: is it retryable, terminal under unchanged inputs, or awaiting policy? Do not collapse timeout into failure or failure into permission to release.

The release predicate is universal over required obligations. Removing the finalizer after the “main” provider delete while credential revocation or audit publication is unrecorded destroys the coordination record. If an obligation is best effort, declare that policy before deletion and still record its attempted disposition.

### Build repeat-safe cleanup

Every cleanup action can be reconciled repeatedly. Use operation identities derived from resource UID and obligation ID. Target immutable provider IDs, not reusable names. Apply delete preconditions such as expected UID, resource version, ETag, owner tag, account, or tenant where supported.

A successful response should be observed or checkpointed. A timeout produces `OutcomeUnknown`; retry lookup by operation or target identity before another mutation. Repeating a provider delete can be safe when the provider contract makes it idempotent, but downstream snapshots, audit events, billing closure, or deletion of a reused name may not be.

Interpret `NotFound` carefully. It may mean already removed, wrong region, wrong account, stale replica, hidden-by-permission, or never created. It can satisfy an obligation when durable prior identity, correct query scope, authorization, consistency window, and provider contract together make absence authoritative. Otherwise retain ambiguity or escalate.

Checkpoint evidence before removing the key. Finalizer removal is itself a potentially lost response: after conflict or timeout, reread. If the object is gone, the API removal completed; ensure any evidence that must outlive it was written to an audit/tombstone store first.

### Separate grace, finalization, and garbage collection

Pod termination grace gives a workload time to handle signals and stop. It does not execute arbitrary controller obligations, and force deletion can remove the API object before the process is confirmed stopped. For stateful workloads using shared identity or storage, that can permit two incarnations to operate concurrently.

Finalization retains an API object based on controller-owned keys. It can protect external cleanup, accounting, or domain evidence but does not itself terminate processes.

Garbage collection follows owner references between Kubernetes objects. Labels select groups but do not establish ownership. A valid owner reference includes UID and obeys scope rules: namespaced dependents can reference a same-namespace namespaced owner or a cluster-scoped owner; invalid cross-namespace ownership is not a cleanup plan.

Choose the mechanism by boundary. Use owner references for Kubernetes dependents that should share owner lifecycle. Use finalizers for prerequisites to removal, external systems, or evidence. Use workload-specific graceful shutdown for process behavior. Combine them when one resource spans all three.

### Choose propagation policy deliberately

**Background propagation** removes the owner first and lets garbage collection delete dependents afterward. It favors owner disappearance and is commonly the default, but the owner record is unavailable while children remain. Do not choose it when parent evidence is required to clean dependents safely.

**Foreground propagation** retains the owner with the `foregroundDeletion` finalizer while the garbage collector removes known dependents that have `blockOwnerDeletion=true`. Only dependents known to the garbage collector cache can block; unlistable resource types or concurrent creations complicate completeness. Foreground is useful for visible tree teardown, not proof that every external or undiscoverable child is gone.

**Orphan propagation** removes ownership so dependents remain. Orphaning is a lifecycle transfer, not “skip cleanup.” Record who owns the retained objects, how they are discovered, billed, secured, upgraded, and later deleted.

Delete options can include UID and resource-version preconditions. Use them when deleting a specific incarnation to prevent a stale command from affecting a recreated name. Bulk collection deletion lacks an atomic ordered transaction across selected resources; plan for partial completion.

### Order domain dependencies without finalizer order

Let deletion obligations form a directed graph $G=(O,E)$, where edge $(a,b)$ means $a$ must be satisfied before $b$ starts. For example, block new traffic before revoking serving credentials; verify the required snapshot before deleting the primary; delete the database before destroying the encryption key if later verification needs that key.

A directed acyclic graph permits topological execution with independent branches in parallel. Cycles reveal an impossible or underspecified contract. If network deletion waits for database deletion while database deletion waits for network access, introduce a safe intermediate state or retain a cleanup channel.

Multiple finalizer owners may independently build graphs, creating hidden distributed cycles. Establish system-level ownership for cross-controller ordering. Conditions alone should not become unauthenticated commands; bind evidence to resource UID, generation/policy revision, and freshness.

Deletion intent can supersede an ordinary workflow but cannot erase its in-flight effects. First discover whether provisioning, restore, or upgrade operations committed. Adopt and then delete, cancel under provider semantics, or transfer them. Preserve operation IDs until ambiguity is resolved.

### Make retention and orphan policies explicit

`Delete`, `Retain`, `Orphan`, and `Transfer` are product semantics, not controller implementation flags. Define them at admission and restrict changes that would weaken already-created obligations. Crossplane, for example, exposes deletion and management policy that determine whether the external resource is deleted or left behind; provider support and precedence must be checked.

For retained resources, remove controller authority only after durable handoff: new owner identity, credentials, billing, inventory, alerts, backups, support, and future deletion route. If no owner accepts these, the result is a leak even if policy says “orphan.”

Data policy can require selective order. A retained backup may need a different encryption key lifecycle and expiry than the primary. Legal hold can transfer deletion authority to a compliance controller. Destruction certificates should identify exact provider/resource incarnation and method without exposing secrets.

Policy changes during deletion need a state machine. A late switch from `Delete` to `Orphan` cannot restore an already deleted resource; a switch from `Orphan` to `Delete` may require renewed authorization. Record commit points and reject impossible reversals.

### Design progress, deadlines, and service objectives

Deletion latency is user-visible platform reliability. Define time to observe deletion, time to begin each obligation, expected provider duration, alert threshold, maximum automatic retry interval, and manual-response objective. Partition by risk: a namespace blocked on a dead annotation finalizer differs from a database with a deletion still outcome-unknown.

Use bounded exponential backoff with jitter while preserving periodic observation. Store next attempt and escalation times durably. A deadline should change status and escalation; it must not silently remove the finalizer unless a pre-authorized policy explicitly chooses orphan/force and records consequence.

Expose deletion age, finalizer owner, obligation counts/states, last successful observation, stable error reason, next retry, dependency, and runbook/repair entry point. Avoid unbounded raw provider errors or credentials in status. Metrics should show age distributions, stuck count by owner/reason, retry rate, external unknowns, forced releases, and orphan inventory.

Fair scheduling matters. A storm of mass deletions must not starve safety-critical credential revocation or block ordinary reconciles indefinitely. Apply global, provider, tenant, and resource concurrency limits; use priority for obligations whose delay increases harm.

### Diagnose before forcing

When an object is stuck, inspect the exact UID, deletion timestamp, all finalizers and their owners, owner references, events, conditions, controller deployment/version, queue and metrics, RBAC/admission errors, external operation identities, dependency health, and audit history. Determine whether cleanup never began, is progressing, is retrying, is ambiguous, or is complete but uncheckpointed.

Repair the cause when possible: restore the compatible controller, credentials, discovery, network, or webhook; replay observation; migrate the key to a successor; complete cleanup manually and attach evidence; or authorize a real orphan transfer.

Manual finalizer removal is a release of a safety interlock. It should require narrow RBAC, exact UID/resourceVersion preconditions, preview of unresolved obligations, two-person or risk-tier approval where warranted, reason/ticket, immutable audit, tombstone, follow-up owner, and post-action inventory. Never present it as equivalent to cleanup success.

Unsafe storage-level or force deletion has even wider consequences because it may bypass finalizers and preconditions. Use only for the precise failure class and feature contract, after preserving evidence and accepting cluster/domain risk. Namespace force-finalization can leave content in an otherwise absent namespace; broad scripts that clear every finalizer multiply this uncertainty.

### Treat webhooks and discovery as deletion dependencies

Admission webhooks can block patches, deletes, or finalizer removal when unavailable or incompatible. Design failure policies by operation risk, exclude controller-owned repair paths carefully, and ensure certificate/service lifecycle outlives objects requiring admission. Test deletion during webhook outage and upgrade.

Namespace deletion depends on discovery and listing namespaced resources. Removed or broken API services can make the namespace controller unable to prove emptiness. Restore discovery or clean the failing API before forcing finalization. A namespace’s absence is not proof that every namespaced external effect vanished.

Deleting a CRD is a schema and data-lifecycle operation, not routine uninstall. Inventory custom resources and finalizers, drain them with their controllers, preserve required data, and only then remove conversion/admission services and the CRD. Retaining a CRD without a controller can leave objects stuck; removing it too early can remove the API records needed for cleanup.

### Secure deletion authority

Separate permission to request deletion, mutate a finalizer, execute external deletion, authorize orphaning, and force release. They have different blast radii. A tenant may delete its claim but must not remove platform protection keys or delete another tenant’s provider object.

Validate target identity immediately before destructive effects: tenant, account/project, resource UID, provider immutable ID, owner tags, policy revision, and deletion timestamp. Use short-lived scoped credentials when possible, but do not revoke cleanup credentials until all obligations are drained or transferred.

Protect tombstones and audit because they reveal resource topology, identifiers, failure reasons, and retention policy. Make force/orphan actions tamper-evident and queryable. Rate-limit deletion requests and finalizer mutations to contain denial-of-service through mass stuck objects.

### Evolve and retire finalizers safely

Finalizer names and semantics are persisted API contracts. Renaming a controller or package must not abandon the old key. New versions should recognize legacy keys, perform or migrate their obligations, and remove them only under the old contract. Rolling old/new replicas need compatible behavior.

Before uninstalling a controller, inventory all current and restorable objects carrying its keys, active and unknown provider operations, queues/callbacks, webhooks, RBAC, credentials, CRDs, backups, and orphaned resources. Stop new admission/provisioning, drain or transfer every obligation, verify zero keys across all served versions/scopes, update restore artifacts, then remove execution dependencies.

If a successor takes ownership, write an explicit handoff record and ensure it can interpret every checkpoint and provider identity. Do not simply replace old key with new key after deletion timestamp, because Kubernetes forbids adding a new finalizer then and because the new name alone does not migrate evidence.

Retain minimal tombstones through the late provider response, audit, disaster-recovery, and legal horizons. Revoke old credentials and callback routes only after they can no longer create unowned changes; alternatively route callbacks to the successor classifier.

### Verify deletion as a system property

Inject crashes before/after finalizer acquisition, each external call, ambiguous response, obligation checkpoint, tombstone write, and finalizer patch. Race delete with first provisioning, spec update, leader change, policy change, dependent creation, and controller upgrade.

Test multiple finalizers in every ordering and concurrently. Create valid, invalid cross-namespace, multi-owner, and unlistable dependents. Exercise foreground, background, and orphan propagation. Recreate an object name with a new UID and deliver a stale delete. Remove RBAC, webhook service, API discovery, provider access, and encryption keys at each boundary.

Restore an old cluster/control database against newer provider state. Replay late callbacks after API removal. Test manual completion, authorized orphan transfer, and forced release with exact preconditions. Assert domain outcomes: no wrong-incarnation deletion, no lost required backup, no live credential after declared revocation, no unowned retained asset, no finalizer without an executor, and no release with an unresolved required obligation.

## Definitions and Notation

Let $R$ be a resource incarnation with immutable UID $u$, deletion timestamp $t_d\in\{\bot\}\cup T$, and current finalizer set $F$. For controller $c$, $f_c$ is its qualified finalizer and $O_c$ its finite required obligation set.

Each obligation $o\in O_c$ has durable disposition

$$
d(o)\in\{P,I,U,S,B,A,X\},
$$

where $P$ is pending, $I$ in progress, $U$ outcome unknown, $S$ satisfied, $B$ blocked, $A$ authorized orphan/waiver, and $X$ transferred to a durable successor. If waiver and orphan have different risk in a domain, model them as separate states; the compact notation groups only explicitly authorized non-execution outcomes.

Define the release predicate

$$
\operatorname{release}_c(R)\equiv (t_d\ne\bot)\land(f_c\in F)\land
\forall o\in O_c,\ d(o)\in\{S,A,X\}.
$$

The safety property is $f_c$ is never removed by controller $c$ unless `release` holds against fresh authoritative evidence. The liveness property is conditional: if deletion is requested, every obligation eventually reaches $S$, $A$, or $X$, the controller is fairly scheduled and authorized, dependencies eventually respond, and writes eventually succeed, then $f_c$ is eventually removed.

Let deletion dependencies be graph $G=(O,E)$ with $(a,b)\in E$ meaning $a$ must reach an allowed disposition before $b$ begins. A topological ordering exists exactly when $G$ is acyclic. External actions use stable operation identity $K(u,o,v)$, where $v$ is the deletion-policy or protocol revision.

Let $N$ be queued objects, $w$ workers, and $\mu$ mean completed deletion protocols per worker per unit time under a simplified stable service model. Ideal drain time is

$$
T=\frac{N}{w\mu}.
$$

This capacity estimate excludes arrivals, retries, rate limits, long-tail providers, dependency serialization, and manual intervention; it is not a liveness proof.

## Mechanisms, Invariants, or Proof Structure

### Deletion protocol

1. Before any external responsibility, add and confirm the qualified owned finalizer through a conflict-safe write.
2. On every reconcile, read immutable UID, current deletion timestamp, policy revision, finalizers, external identities, and operation checkpoints.
3. If deletion is absent, reconcile ordinary desired state without weakening deletion ownership.
4. If deletion is present, stop unauthorized ordinary effects and materialize the versioned cleanup obligation graph.
5. Resume active/unknown operations by stable identity; use idempotent calls, preconditions, and observation.
6. Execute only obligations whose dependencies have allowed dispositions, with bounded fair concurrency.
7. Persist outcome evidence and expose progress/blocked/unknown status without secrets.
8. For impossible automatic cleanup, require explicit satisfied, authorized orphan/waiver, or transferred disposition; never map error to success.
9. Write required audit and tombstone evidence that must outlive the object.
10. Re-evaluate the release predicate from fresh state and remove only the owned key with optimistic concurrency.
11. After API disappearance, monitor retained resources, callbacks, and tombstone expiry under the named successor owner.

### Invariant argument

Assume the finalizer is installed before responsibility, every cleanup path is mediated by the protocol, $O_c$ contains all obligations owned by $c$, dispositions cannot be forged by unauthorized actors, evidence is fresh and identity-bound, and the finalizer patch is conditional and removes only $f_c$.

Initially, external responsibility implies $f_c\in F$. Once deletion begins, the API retains $R$ while $f_c$ remains. Protocol transitions can advance obligations but cannot remove $f_c$ until all required dispositions are allowed. The final transition persists outliving evidence, rechecks `release`, and removes $f_c$. Therefore the controller never voluntarily discards its Kubernetes coordination record while one of its modeled required obligations is pending, in progress, unknown, or blocked.

This is a proof sketch of the model. It does not cover omitted obligations, administrators stripping keys, direct provider mutations, storage corruption, invalid identity checks, broken admission, or premature CRD removal. It proves no eventual deletion without the stated liveness assumptions.

### Executable obligation inventory

The synthetic inventory below checks ten deletion designs against ten controls. It illustrates review classification only; it does not exercise Kubernetes, a provider, or destructive behavior.

<!-- bijux-verify: {"id":"deletion-obligation-inventory","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"releasable=2\nblocked=5\nhazardous=3\n"}} -->
```python
required = {
    "finalizer_before_effect", "uid_bound", "obligations_explicit",
    "idempotent_cleanup", "unknown_observed", "dependencies_acyclic",
    "own_key_only", "orphan_authorized", "tombstone", "retirement_tested",
}

designs = {
    "database": required,
    "dns": required,
    "late-finalizer": required - {"finalizer_before_effect", "tombstone"},
    "name-delete": required - {"uid_bound"},
    "blind-timeout": required - {"unknown_observed", "idempotent_cleanup"},
    "hidden-cycle": required - {"dependencies_acyclic"},
    "clear-list": required - {"own_key_only", "orphan_authorized"},
    "silent-orphan": required - {"orphan_authorized"},
    "no-tombstone": required - {"tombstone"},
    "dead-controller": required - {"retirement_tested"},
}

counts = {"releasable": 0, "blocked": 0, "hazardous": 0}
for controls in designs.values():
    missing = required - controls
    category = "releasable" if not missing else ("blocked" if len(missing) == 1 else "hazardous")
    counts[category] += 1
for category in ("releasable", "blocked", "hazardous"):
    print(f"{category}={counts[category]}")
```

One missing control is classified `blocked` because release cannot be justified from the inventory. Two missing controls are labeled `hazardous`, not because every pair has equal severity, but to force deeper review. Real evidence requires concurrency, crash, provider, admission, security, restore, and domain-outcome tests.

## Alternatives and Trade-Offs

### Finalizer versus owner reference

Owner references efficiently express Kubernetes ownership and enable garbage collection. They cannot represent arbitrary external resources or policy evidence. A finalizer retains the owner until a controller proves obligations; it adds latency and executor dependency. Use each for its actual boundary, often together.

### Controller-added versus admission-added finalizer

Controller addition avoids webhook coupling and keeps ownership local, but requires strict “add, return, then effect” sequencing. Admission addition closes gaps before storage and can enforce organization policy, but webhook outage, ordering, rollout, and removal become lifecycle dependencies. Do not use both without one authority contract.

### One aggregate key versus multiple owner keys

One key supports an internally coordinated graph and one release decision. It can hide responsibility if several teams share it. Multiple keys preserve independent authority but are unordered and can deadlock through hidden cross-dependencies. Choose ownership boundaries, then represent ordering explicitly.

### Foreground versus background cascade

Foreground retains the owner and makes known blocking dependents visible before removal, at higher latency and garbage-collector dependency. Background removes the owner quickly and cleans later, reducing coordination evidence. Neither covers invalid/unlistable relationships or external systems.

### Delete versus orphan/retain

Delete reduces inventory and future ownership but may destroy data. Orphan/retain protects continuity and supports handoff, but carries cost, security, compliance, and discoverability obligations. Require an identified successor and retained inventory; otherwise “orphan” is a leak label.

### Sequential versus parallel cleanup

Sequential execution simplifies ordering and rate control but increases latency. Parallel execution improves throughput for independent obligations but needs explicit graph edges, per-provider limits, and join semantics. Never parallelize effects whose safety relation is unknown.

### Status fields versus separate deletion-operation resource

Status is colocated and naturally retained by the finalizer, but can grow, expose sensitive data, and disappear at release. A separate operation resource supports detailed history and handoff but has its own ownership, finalizer, retention, and orphan risks. Store compact public progress in status and protected durable evidence where required.

### Automatic deadline orphan versus manual authorization

Automatic orphan after a deadline bounds deletion latency but can silently leak costly or sensitive resources. Manual approval slows liveness but makes consequence explicit. For low-risk best-effort cleanup, admission-time deadline policy may be acceptable; high-risk data or identity should fail closed with escalation.

### Restore controller versus strip finalizer

Restoring a compatible controller preserves protocol meaning and can complete cleanup, but may be slow or impossible if code/credentials are gone. Stripping releases immediately but loses the coordination record. Prefer successor/migration or manual completion; force only after inventory and durable consequence capture.

### Immutable deletion policy versus mutable repair operation

Immutable admitted policy makes consequences predictable and auditable. Incidents still need repair choices. Keep baseline policy immutable for the operation and provide narrow authorized dispositions rather than allowing arbitrary spec mutation during deletion.

### Long tombstone retention versus rapid erasure

Long retention classifies late callbacks, restores, and reused names but consumes storage and can retain sensitive topology. Rapid erasure reduces privacy exposure yet weakens recovery. Minimize tombstone fields, encrypt/access-control them, and size retention from delivery, restore, and legal horizons.

### Dedicated cleanup identity versus controller identity

A dedicated least-privilege identity limits ordinary controller blast radius and can outlive rollout, but adds credential and deployment operations. One broad identity is simpler but couples creation, deletion, force, and incident privileges. Separate destructive authority when domain risk justifies it.

## Failure Modes and Misconceptions

1. **“A finalizer runs cleanup.”** It is only a stored key; a live compatible controller must interpret it.
2. **“Finalizers run top to bottom.”** Kubernetes enforces no order and the shared list can be reordered.
3. **“Add the key after create succeeds.”** A crash or concurrent delete can erase the cleanup anchor.
4. **“Deletion timestamp is just another spec flag.”** It is immutable, changes lifecycle authority, and the object cannot be resurrected.
5. **“Foreground means every child is gone.”** Only eligible, known Kubernetes dependents block; external and undiscoverable resources need separate proof.
6. **“Labels create ownership.”** Owner references, including UID and valid scope, drive Kubernetes garbage collection.
7. **“NotFound always means deleted.”** Scope, permission, stale reads, and reused identity can make that conclusion false.
8. **“DELETE is enough for idempotency.”** Surrounding backups, events, billing, and wrong-incarnation risks remain.
9. **“The first finalizer may wait for the second.”** There is no first; encode dependencies elsewhere or risk deadlock.
10. **“Removing all keys fixes termination.”** It removes every owner’s safety interlock and can leak or corrupt state.
11. **“A deadline authorizes release.”** Time triggers escalation unless policy explicitly pre-authorized a disposition.
12. **“Orphan means harmless.”** Retained resources require owner, security, billing, backup, inventory, and future deletion.
13. **“Force deletion proves the workload stopped.”** API disappearance can precede process termination, especially on unreachable nodes.
14. **“Delete permission implies finalizer authority.”** Request, finalizer mutation, external destruction, and force should be separately authorized.
15. **“One successful provider response completes deletion.”** All required obligations and outliving evidence must reach allowed dispositions.
16. **“Uninstalling the deployment is reversible.”** Live keys immediately lose their executor; restore artifacts may resurrect them later.
17. **“Rename the key with the controller.”** Persisted objects retain the old contract, and new keys cannot be added after deletion begins.
18. **“Deleting the CRD is cleanup.”** It can remove the API records needed to discover and finalize external state.
19. **“A stuck deletion should retry faster.”** Permission, dead executor, dependency cycles, or ambiguous effects require diagnosis, not load.
20. **“Object disappearance is the system outcome.”** Verify external assets, data, credentials, dependents, billing, audit, and retained ownership.

## Worked Examples

### Example 1

**Situation.** A controller provisions a bucket, then adds `storage.platform.example/delete`. A delete races between those calls.

**Reasoning.** Kubernetes can remove the object before the key exists, leaving the bucket without its UID-to-provider identity anchor. Reverse the order: add the qualified finalizer with a resource-version-safe write, return, reread it, then submit the stable bucket create. If deletion won the race before finalizer acquisition, do not add a new key or create the bucket. If the key is present and deletion begins after acquisition, enter cleanup.

**Conclusion.** The finalizer must be confirmed before the first external responsibility, with a reconcile boundary that makes the ordering testable.

### Example 2

**Situation.** One object has finalizers `network.example/delete` and `database.example/delete`. The database controller assumes network cleanup runs second because its key is first.

**Reasoning.** Finalizer list order has no execution semantics. Both controllers may begin concurrently, and authorized updates may reorder keys. If database deletion requires network connectivity, the database owner should expose a `DatabaseRetired` condition/operation that network cleanup consumes, or one deletion orchestrator should own both steps. Each controller removes only its own key.

**Conclusion.** Cross-owner order must be represented as durable domain dependency, never inferred from list position.

### Example 3

**Situation.** A provider delete for immutable ID `db-41` times out. A subsequent lookup returns `NotFound` from a regional endpoint.

**Reasoning.** Verify that `db-41` belongs to the resource UID and that the lookup used the recorded account and region with permission to distinguish absent from forbidden. Check provider consistency and operation-token semantics. If the endpoint is authoritative after the documented window, checkpoint `Satisfied`. If region or authorization is uncertain, preserve `OutcomeUnknown`; do not remove the finalizer or send a delete by display name.

**Conclusion.** `NotFound` is evidence only when identity, scope, authorization, and consistency assumptions are satisfied.

### Example 4

**Situation.** A parent has three Kubernetes dependents. Two have `blockOwnerDeletion=true`; a fourth custom kind cannot be listed because its APIService is broken. The user selects foreground propagation.

**Reasoning.** The owner receives foreground deletion state. Known blocking dependents can retain it until garbage collection deletes them. The unlistable kind may be absent from the garbage collector cache, so foreground completion is not proof about that dependent. Restore API discovery/listing, inventory the kind, and use controller-owned finalization if its lifecycle is critical.

**Conclusion.** Foreground propagation improves visible tree ordering but is bounded by valid ownership and discovery.

### Example 5

**Situation.** Cleanup obligations are `drain traffic`, `snapshot`, `delete primary`, `revoke key`, and `remove DNS`. Snapshot and drain can run together; primary deletion needs both; key revocation needs primary deletion; DNS removal needs drain.

**Reasoning.** Edges are drain→delete, snapshot→delete, delete→revoke, and drain→DNS. A valid schedule begins drain and snapshot in parallel, then DNS after drain, delete after both drain and snapshot, and revoke after delete. Adding revoke→snapshot would create a cycle if snapshot needs the key; the design must preserve a scoped key or change order.

**Conclusion.** An explicit DAG enables safe parallelism and exposes impossible teardown cycles before production.

### Example 6

**Situation.** Twelve thousand resources await deletion. Eight workers each complete 0.4 deletion protocols per second with no arrivals or retries. Estimate ideal drain time.

**Reasoning.** Aggregate service is $w\mu=8\times0.4=3.2$ objects/second. Thus

$$
T=\frac{12{,}000}{3.2}=3{,}750\text{ seconds}=62.5\text{ minutes}.
$$

Real drain will be longer under rate limits, long-tail providers, dependency serialization, ambiguity, retries, and manual blocks. Capacity planning should prioritize high-risk obligations rather than assume uniform work.

**Conclusion.** Worker capacity sets a lower-bound planning estimate, not a deletion-liveness guarantee.

### Example 7

**Situation.** A user asks to orphan a cloud database after deletion has begun because provider deletion is failing.

**Reasoning.** Confirm policy permits a late change and the database is not already partially destroyed. Create a transfer record naming tenant owner, immutable provider ID, credentials, billing, backup, alerts, and future deletion route. Revoke controller authority only after the successor accepts. Mark the obligation `Transferred`, write a tombstone/audit, and then release. If no owner accepts, keep `Blocked` rather than relabel a leak.

**Conclusion.** Safe orphaning is an ownership transfer with evidence, not omission of a delete call.

### Example 8

**Situation.** A finalizer is stuck because its controller deployment was removed and its old image registry no longer exists.

**Reasoning.** Inventory every object with the key and group them by external operation evidence. Deploy a compatible recovery controller or successor that understands the old key and checkpoint schema. Restore scoped credentials, observe external state, complete or transfer obligations, and remove keys individually with conflicts handled. Only objects whose cleanup was manually verified may use a force procedure. Update backups so the abandoned key cannot return.

**Conclusion.** Restore or transfer protocol ownership; global key stripping converts an availability incident into unknown environmental state.

### Example 9

**Situation.** A delayed deletion command targets `cache/blue` after the old UID was removed and a new object reused the name.

**Reasoning.** The old deletion tombstone contains UID `u-old` and provider ID `p-old`. Send or verify deletion only against `p-old` with its owner tag and delete precondition. The new object has UID `u-new` and provider ID `p-new`, so it cannot match. If only the reusable name remains and the provider offers no ownership precondition, quarantine rather than risk destroying the successor.

**Conclusion.** UID-bound external identity and tombstone retention prevent stale deletion from crossing incarnations.

### Example 10

**Situation.** A platform team wants to uninstall an operator, webhook, and CRD while 40 objects are active, 3 terminating, and disaster-recovery backups contain older objects.

**Reasoning.** Stop new claims first. Keep webhook, CRD, controller, permissions, provider credentials, and callback routes alive while active objects are deleted, retained under an accepted owner, or migrated. Resolve the three terminating objects and verify zero old/new finalizer keys across versions and scopes. Update or expire restore artifacts, verify external inventory and tombstones, then remove webhook service/configuration, controller, credentials, and finally the CRD according to the planned API retirement. Test restore cannot reintroduce unserviceable keys.

**Conclusion.** Finalizer executor and API schema are removed after obligation drainage and restore closure, not at the start of uninstall.

## Cross-Program Connections

1. **API & Service Engineering:** asynchronous DELETE, 202 acceptance, preconditions, long-running operations, idempotency, and error semantics determine what clients may infer.
2. **Distributed Systems:** partial failure, stale leaders, ambiguity, durable identity, eventual consistency, and absence of cross-system transactions shape cleanup recovery.
3. **Database Systems:** write-ahead intent, transactions, compare-and-swap, tombstones, retention, and recovery logs preserve obligations across crashes.
4. **Graph Theory:** ownership trees, dependency DAGs, topological order, cycles, and reachability make teardown ordering and deadlocks explicit.
5. **Security Engineering:** destructive privilege, tenant binding, two-person approval, credential sequencing, tamper-evident audit, and force controls bound blast radius.
6. **Reliability Engineering:** deletion SLOs, backoff, queues, fairness, fault injection, runbooks, recovery objectives, and error budgets keep termination operable.
7. **Data Engineering:** tombstones, replay, retention horizons, late events, checkpoint restore, and compaction mirror stream and lakehouse deletion challenges.
8. **Privacy and Governance:** erasure, legal hold, retained backups, destruction evidence, data minimization, and owner transfer constrain technical cleanup order.
9. **Software Architecture:** bounded ownership, explicit contracts, compatibility, dependency inversion, and decommissioning prevent finalizer keys from becoming permanent coupling.
10. **Systems Engineering:** lifecycle disposal, hazard analysis, interlocks, override authority, verification, configuration control, and retirement treat deletion as a complete system mode.

## References

1. Kubernetes. [Finalizers](https://kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/). Retrieved 2026-09-02. Documents deletion timestamps, 202 responses, restrictions after deletion, and qualified custom names.
2. Kubernetes. [Garbage Collection](https://kubernetes.io/docs/concepts/architecture/garbage-collection/). Retrieved 2026-09-02. Documents ownership, foreground/background cascading deletion, cache limitations, and orphaning.
3. Kubernetes. [Owners and Dependents](https://kubernetes.io/docs/concepts/overview/working-with-objects/owners-dependents/). Retrieved 2026-09-02. Documents UID-bearing owner references, scope rules, and `blockOwnerDeletion`.
4. Kubernetes. [Kubernetes API Concepts](https://kubernetes.io/docs/reference/using-api/api-concepts/). Retrieved 2026-09-02. Covers two-stage resource deletion, unordered finalizers, concurrency, and API behavior.
5. Kubernetes. [Object Names and IDs](https://kubernetes.io/docs/concepts/overview/working-with-objects/names/). Retrieved 2026-09-02. Distinguishes reusable names from object-incarnation UIDs.
6. Kubernetes. [kubectl delete](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_delete/). Retrieved 2026-09-02. Documents grace, propagation, force behavior, and stateful-workload cautions.
7. Kubernetes. [Share a Cluster with Namespaces](https://kubernetes.io/docs/tasks/administer-cluster/namespaces/). Retrieved 2026-09-02. Documents asynchronous namespace deletion and stuck nonexistent finalizers.
8. Kubernetes. [Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/). Retrieved 2026-09-02. Documents stable Job tracking finalizers and controller accounting.
9. Kubernetes SIGs. [controller-runtime finalizer package](https://pkg.go.dev/sigs.k8s.io/controller-runtime/pkg/finalizer). Retrieved 2026-09-02. Provides current controller finalizer interfaces.
10. Kubernetes SIGs. [controller-runtime controllerutil package](https://pkg.go.dev/sigs.k8s.io/controller-runtime/pkg/controller/controllerutil). Retrieved 2026-09-02. Documents add, contains, and remove helpers and owner-reference operations.
11. Crossplane. [Managed Resources](https://docs.crossplane.io/latest/managed-resources/managed-resources/). Retrieved 2026-09-02. Documents current external deletion, orphan, management-policy, and finalizer behavior.
12. IETF. [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html). 2022. Defines DELETE and idempotent method semantics at the HTTP boundary.
13. Pat Helland. [Life Beyond Distributed Transactions: An Apostate's Opinion](https://www.cidrdb.org/cidr2007/papers/cidr07p15.pdf). CIDR, 2007. Develops durable identity and workflow reasoning without distributed transactions.
14. Martin Kleppmann. *Designing Data-Intensive Applications*. O'Reilly Media, 2017. See distributed failures, delivery semantics, logs, transactions, and recovery.

## Exercises

### Exercise 1

Explain the state of a Kubernetes object with `deletionTimestamp` set and two finalizers. State what the API server has established, what it has not established, which mutations are restricted, and what makes the object disappear.

### Exercise 2

Design the deletion obligation graph for a tenant database with traffic, credentials, a required verified backup, primary/replicas, DNS, billing, audit, and a retained compliance tombstone. State dependencies and the finalizer release predicate.

### Exercise 3

A controller creates an external queue and then adds its finalizer. Provider deletion by name returns timeout followed by `NotFound`. Diagnose every unsafe assumption and propose a crash-safe create and delete protocol.

### Exercise 4

Compare foreground garbage collection, a controller-owned finalizer, and orphan propagation for a platform resource with Kubernetes Deployments, a cross-namespace consumer, a cloud load balancer, and a customer-selected retain option.

### Exercise 5

Plan retirement of a controller whose finalizer exists on 100,000 objects across API versions and backups. Some objects are terminating, provider operations are ambiguous, the admission webhook injects the key, and the successor uses a different checkpoint schema.

## Answers to the Exercises

### Answer 1

The API server has accepted deletion, recorded an immutable deletion timestamp, and is retaining the object while finalizer keys remain. It has not proved that either cleanup obligation started, completed, or even has a live controller. The object is still readable/watchable and may allow limited updates, but a new finalizer cannot be added after deletion begins and the timestamp cannot be cleared; the object cannot be resurrected in place. Finalizer owners may remove their existing keys after satisfying their contracts, using conflict-safe writes that preserve other keys. Once the finalizer list becomes empty, Kubernetes may remove the object from storage. Its disappearance still proves nothing about external resources unless their cleanup protocol supplied separate evidence.

### Answer 2

One safe graph begins with `block-new-traffic` and `freeze-billing-growth`. After traffic is blocked, `drain-connections` can run. `snapshot-primary` may run in parallel; `verify-snapshot` follows snapshot. Replica deletion requires drain and verified snapshot if replicas contribute recovery. Primary deletion requires drain, verified snapshot, and replica disposition. Credential revocation may begin after drain but must preserve the scoped cleanup credential; customer credentials should be revoked before final release. DNS removal follows traffic block/drain. Billing closure follows verified provider deletion or accepted transfer. Audit publication follows material outcomes, and the protected compliance tombstone is written after all identities/dispositions are known.

Let $O_c$ contain every required item. Release requires deletion timestamp set, the owned key present, and every item in `Satisfied`, `AuthorizedOrphan`, or `Transferred`, with the latter two allowed only by policy and authority. `Pending`, `InProgress`, `OutcomeUnknown`, or `Blocked` prevents release. The tombstone and any outliving audit must be durably written before removing the key.

### Answer 3

Creation has a leak window: the queue can exist while no key retains the Kubernetes object. Name-only deletion can target a reused queue. Timeout does not establish failure, and `NotFound` may reflect wrong scope, permission, or stale observation. The design also lacks a stable operation identity, immutable provider ID, owner validation, and explicit evidence horizon.

On normal reconcile, add the qualified finalizer with optimistic concurrency, return, reread, then derive a UID-bound create key and deterministic/searchable identity. Submit with provider idempotency support, owner tenant/UID tags, and persist operation/external ID. If deletion already began before the key was stored, do not create. On delete, freeze ordinary work, target the immutable queue ID with UID/account preconditions, record the request identity, and observe ambiguous outcomes. Treat `NotFound` as satisfied only from the authoritative account/region with adequate permission and consistency delay; otherwise retain `OutcomeUnknown`. Write the tombstone and remove only the owned finalizer after every obligation is dispositioned.

### Answer 4

Use owner references and a selected propagation policy for same-scope Kubernetes Deployments. Foreground can retain the platform owner while known `blockOwnerDeletion` dependents are removed, which aids ordered visible teardown; background is faster if parent evidence is unnecessary. A cross-namespace consumer cannot be modeled as a namespaced owner-reference dependent of a namespaced owner, so represent it through a domain dependency or independent claim rather than an invalid owner reference.

The cloud load balancer is outside Kubernetes garbage collection and needs a controller finalizer with stable provider identity, idempotent/observable deletion, and unknown handling. For customer retain, orphan propagation alone handles only Kubernetes dependents. The external load balancer also needs explicit transfer: owner, credentials, billing, security, inventory, and later-deletion route. The controller marks `Transferred` only after acceptance, preserves a tombstone, and then removes its key. Foreground does not prove external deletion; finalization does not terminate processes; retain without ownership is a leak.

### Answer 5

First freeze new obligations: change admission so it stops accepting new claims only through a compatible rollout, while preserving deletion/finalizer operations. Inventory all 100,000 objects by served/storage version, namespace, UID, finalizer name, deletion state, checkpoint schema, provider identity, last progress, and restore source. Inventory provider operations, callbacks, credentials, webhook configurations, CRDs, queues, and external orphans.

Deploy the successor with adapters that understand the old key and every old checkpoint, or run old and new executors behind explicit version routing. Do not rename keys on terminating objects; migrate evidence and let the compatible owner remove the legacy key under its original release predicate. Resolve active operations, observe ambiguous provider outcomes, and prioritize terminating/high-risk items with bounded provider concurrency. Transfer obligations through durable records and validate tenant/UID identity. Exercise conflict, crash, old/new leader, webhook outage, and restored-backup traces.

Track key count and age to zero across all live served versions and scopes; separately disposition retained resources and tombstones. Rewrite, expire, or fence disaster-recovery artifacts so restoration cannot resurrect objects with no executor or allow old credentials to act. Keep the admission/conversion webhook, CRDs, RBAC, cleanup credentials, callback routes, and monitoring until drainage and restore verification complete. Then stop callbacks and workers, revoke credentials, remove webhook configurations/services, and remove deprecated APIs/CRDs according to their lifecycle plan. The completion evidence includes zero serviceable legacy keys, no unresolved required obligation, accepted ownership for every retained asset, tested restore, and durable force/orphan audit—not merely an empty current cluster query.
