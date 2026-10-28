---
module_id: PLAT-077
program: Platform Engineering
level: 2
module_number: 77
title: Admission Control
status: complete
last_verified: 2026-09-02
---

# Admission Control

## One-Page Review

### Governing question

How should a platform validate or mutate API requests before persistence so that policy sees the right identity and final object, covers every intended operation and resource, remains available and recoverable, and cannot be bypassed through controllers, nodes, storage, or mis-scoped exemptions?

### Essential definitions

- **admission control** is request processing after authentication and authorization but before persistence that can validate, reject, annotate, warn about, or mutate API objects.
- A **mutating admission controller** returns changes to the incoming object; a **validating admission controller** accepts or rejects the resulting request without mutation.
- An **AdmissionReview** carries request identity, operation, resource/kind, namespace/name, object, old object, dry-run status, and options to a webhook and returns an AdmissionResponse.
- A **matching rule** defines API groups, versions, resources/subresources, operations, scope, namespace/object selectors, and optional conditions that cause a policy or webhook to run.
- **failure policy** specifies whether an admission error, timeout, or unreachable webhook fails or ignores the request; it does not turn an explicit denial into allowance.
- **timeout** is the API server’s maximum wait for a webhook; every matching webhook consumes request latency and availability budget.
- **side effects** are changes outside the admitted object. Admission should avoid them and must suppress them for dry-run according to its declared contract.
- **reinvocation** allows a mutating webhook/policy to run again after other mutations make its conditions relevant; all mutations must remain idempotent.
- **audit mode** records violations without denial; **warn mode** returns a client warning; **enforce mode** rejects a violating request.
- **background audit** evaluates persisted resources later; it cannot reconstruct every request-only field and does not prevent the original effect.
- **bypass** is a path that changes cluster execution or storage without traversing the intended API admission chain, such as direct etcd, kubelet/runtime, or static-pod access.
- **recovery boundary** is a protected route or configuration that lets operators repair a broken admission system without granting routine bypass.

### Central model, mechanism, or theorem

For request $r$, Kubernetes-like admission can be modeled as

$$
o_0=DecodeDefault(r),\quad o_{i+1}=M_i(r,o_i),\quad
Accept(r,o_f)=\bigwedge_j V_j(r,o_f),
$$

where matching mutators $M_i$ transform the object, possibly under reinvocation, and all matching validators $V_j$ must accept the post-mutation object $o_f$. Safety requires correct request matching, idempotent/non-conflicting mutations, validation of final state, bounded failure behavior, and complete path coverage. A perfect validator cannot protect workloads created outside the API-server admission boundary.

### Critical invariants

- Authentication and authorization succeed before admission; admission never replaces RBAC or workload runtime authorization.
- Matching explicitly covers intended groups, versions, resources, subresources, operations, scopes, and namespaces; exclusions are narrow and tested.
- Validation evaluates the final post-defaulting/post-mutation state and denies every prohibited representation, including init and ephemeral containers or generated objects where relevant.
- Mutations are deterministic, idempotent, minimal, schema-valid, conflict-aware, and never rely on a fixed ordering among webhooks.
- Webhooks accurately declare side effects and suppress them during dry-run; preferred admission logic is side-effect free.
- Failure policy and timeout are chosen per control risk and availability, with fail-open mutation followed by authoritative validation when appropriate.
- Every webhook is highly available, fast, load-tested, TLS-authenticated, minimally privileged, and excluded from circular dependencies needed for its recovery.
- User information is used only where present and authoritative; controllers, background audit, and indirect resource creation do not magically preserve the initiating human.
- Audit/warn/shadow precedes enforcement for impactful changes, with current violations owned and versioned policy pinned where drift matters.
- Exemptions are minimal, explicit, attributable, monitored, expiring, and never broadly applied to controller identities that act for many users.
- Direct etcd, kubelet, runtime socket, node filesystem/static pod, and control-plane configuration access is restricted and separately monitored because admission cannot intercept it.
- A protected recovery path can remove or repair broken admission configuration while normal workloads cannot use it to evade policy.

### Common failures

Wildcard match without exclusions; wrong API group/version/subresource; create checked but update/patch/connect ignored; namespace selector assumed to apply to cluster-scoped objects; object selector trusted when users can set labels; controller identity mistaken for originating user; mutation depends on order; non-idempotent sidecar injection; mutation overwritten later and never validated; `replace` destroys fields; admission webhook performs external writes; dry-run lies about side effects; ten-second defaults multiplied across serial mutators; single-replica webhook; webhook intercepts its own Deployment or dependencies; fail-open validator; fail-closed nonessential mutator; timeout/error confused with explicit deny; audit report assumed complete history; broad Pod Security exemption for a controller; version set to `latest` without upgrade preview; static pods or direct kubelet/etcd bypass ignored; and a webhook blocks updates needed to repair itself.

### Compact example

A platform requires production pods to use digest-pinned images, approved registries, non-root security settings, dedicated service accounts, and owners. CI gives early feedback. A mutating policy adds a harmless owner-derived annotation idempotently and fails open; an in-process validating policy and a highly available validating webhook inspect the final object, all container kinds, operation, old object, tenant namespace, actor/workload, and policy data. Candidate rules run warn/audit and server-side dry-run, then canary enforcement. Webhook timeout is one second, replicas span zones, dependency namespaces are narrowly excluded, and final validation fails closed for production. Pod Security Admission enforces a pinned Restricted version. Direct kubelet/runtime/etcd and static-pod paths are restricted separately.

### Connections

Admission is a concrete enforcement point for the lifecycle designed in [PLAT-076](076-platform-policy-as-code.md), consuming human and workload identities from [PLAT-074](074-identity-federation.md) and [PLAT-075](075-workload-identity.md). It implements tenant and isolation guardrails from [PLAT-071](071-tenant-models.md) and [PLAT-072](072-namespace-account-and-cluster-isolation.md). PLAT-078 uses admission for artifact evidence and PLAT-079 uses request, policy, warning, denial, exemption, and bypass evidence.

## Governing Question

How can a platform place reliable policy gates in the API request path without creating a fragile cluster-wide dependency or assuming that every dangerous effect originates as a simple pod create?

Admission has a powerful location: it can inspect requested and existing object state immediately before persistence. It can reject unsafe configurations and supply carefully designed defaults. That location is also operationally dangerous. A slow, unavailable, recursive, or overbroad webhook can stop deployments or impair incident recovery across a cluster.

Sound design begins with the request sequence, supported in-process controls, exact match semantics, final-state validation, and bypass inventory. Tool installation is secondary.

## Why This Matters

Authorization answers whether a principal may perform a verb on a resource type/name. It does not normally inspect every field of the proposed object. An authorized developer may still request privileged host access, an unapproved image, a public load balancer, cross-tenant reference, or unsafe deletion.

Admission turns platform standards into preventive controls at self-service scale. It also improves feedback when warnings and remediations are returned before a dangerous object exists.

Cluster availability depends on admission. Every matching external webhook sits in the API-server critical path. A webhook may depend on DNS, networking, certificates, its own pods, or storage—all of which may require API updates during an incident. Circular dependency can turn a small outage into control-plane paralysis.

Admission is not a sandbox around the node. Direct access to etcd, kubelet APIs, container runtime sockets, or static-pod manifests can bypass API-server admission. The architecture must protect and audit those paths independently.

## Prerequisites and Retrieval

Retrieve Kubernetes API groups/versions/kinds/resources/subresources, authentication, authorization/RBAC, API request verbs, object schemas/defaulting/conversion/validation, create/update/patch/delete/connect, old object and resourceVersion, controllers and owner references, webhooks/TLS/services/DNS, JSON Patch and Server-Side Apply, CEL, dry-run, audit logging, Pod Security Standards, high availability, latency/error budgets, failure modes, policy as code, exceptions, and node/control-plane security.

Distinguish kind from resource; resource from subresource; user from controller; request object from persisted/final object; `object` from `oldObject`; mutation from defaulting; mutation from validation; explicit denial from transport/evaluation failure; `Ignore` from allow; `audit` from history; namespace selector from request namespace; label selection from trusted identity; dry-run from local client rendering; webhook service availability from policy correctness; API-server boundary from cluster/node boundary; and recovery from routine bypass.

## Learning Objectives

After completing this module, you should be able to:

1. trace a Kubernetes API request through authentication, authorization, mutation, schema/defaulting, validation, persistence, controllers, and audit;
2. define exact admission matching across operations, groups, versions, resources, subresources, scopes, selectors, and conditions;
3. choose built-in admission, ValidatingAdmissionPolicy, MutatingAdmissionPolicy, or webhooks by capability and failure boundary;
4. design deterministic, idempotent, minimal mutations and validate the complete final object;
5. set failure policy, timeout, sideEffects, reinvocation, match policy, and availability deliberately;
6. account for controller identity, indirect object creation, dry-run, old state, deletion, and background audit limitations;
7. roll out admission through offline tests, dry-run, warn/audit, canary, enforce, and fleet reconciliation;
8. protect recovery dependencies and test webhook outage, overload, recursion, certificate failure, and policy rollback;
9. inventory and constrain direct etcd, kubelet, runtime, node/static-pod, aggregated API, and privileged bypass paths; and
10. produce decision, mutation, warning, denial, exemption, latency, revision, and enforcement evidence without leaking objects or credentials.

## Core Exposition

### Place admission in the request lifecycle

The API server authenticates the requester and authorizes the requested verb/resource before admission. Admission can then inspect identity, operation, resource, object, old object, and context. It cannot grant an unauthorized request.

Mutating admission runs before validating admission. Defaulting, conversion, schema validation, and built-in plugins interact with this flow according to API implementation. The safe design assumption is that validation must inspect the final object after mutations, not merely the user’s original YAML.

If accepted, the object is persisted. Controllers may later create secondary objects, usually under controller service accounts. Those secondary requests traverse admission but may not contain the original human identity.

Admission is synchronous prevention at one boundary. Background audit and runtime controllers are complementary detection/reconciliation. Runtime behavior may still diverge from admitted desired state through compromise or bypass.

### Define the protected effect and request matrix

Start from a policy such as “untrusted code cannot obtain host-level privilege.” Enumerate every API object and operation capable of the effect: pods and templates, controllers, ephemeral containers, node/runtime configuration, custom workload APIs, updates, and restore paths.

Build a matrix of API group, version, resource/subresource, scope, operations, source actors, and generated objects. Kubernetes uses plural resource names in match rules, not Kind strings. `pods/ephemeralcontainers` is distinct from `pods`.

Include CREATE, UPDATE, and relevant CONNECT/DELETE operations. PATCH becomes an update after merge. Examine `oldObject` for transitions: making a field privileged, removing ownership/protection, or changing a namespace policy label.

Test discovery against the actual cluster version. New API versions, resources, subresources, and fields can open gaps when a rule assumes yesterday’s schema.

### Understand matching and exclusions

Webhook rules select operations, API groups/versions, resources/subresources, and scope. Namespace and object selectors plus match conditions further reduce invocations. Each filter is part of the security boundary.

Namespace selectors use labels of the request namespace for namespaced resources and have different implications for namespace objects or cluster-scoped resources. Object selectors depend on labels of old/new objects and are unsafe as sole exclusions when untrusted users can set the label.

Use exact exclusions for system dependencies and recovery, not a broad `kube-system` bypass by habit. A namespace contains both critical and ordinary workloads; a controller service account may create pods for any user authorized to create a parent workload.

Avoid matching TokenReview, SubjectAccessReview, and other authentication/authorization virtual resources. Avoid intercepting admission configuration in a way that makes correction impossible unless using a deliberately protected manifest-based recovery model.

### Choose in-process or webhook enforcement

Built-in controllers have low dependency overhead and well-defined cluster-version semantics. Pod Security Admission supplies namespace-selected Privileged, Baseline, and Restricted profiles in enforce, audit, and warn modes.

ValidatingAdmissionPolicy uses CEL in the API server and parameter resources/bindings. It avoids an external network service for expressible validation. MutatingAdmissionPolicy provides declarative in-process CEL mutations in current Kubernetes versions, with bindings and optional parameters.

Webhooks support arbitrary implementation languages, external data, and richer integration but add TLS, service discovery, network, deployment, scaling, certificate, latency, and availability dependencies. Use them only when in-process mechanisms cannot express the required decision safely.

Gatekeeper and Kyverno package broader policy lifecycles around admission and audit. Their controllers/webhooks still require the same scope, availability, version, exception, and recovery analysis.

### Design validation as a total final-state predicate

Validation must return an explicit decision for every matching, schema-valid request. Handle missing/empty values, new enum values, all container lists, object generation, old object absence, deletion, and parameter absence.

Validate the final object regardless of who supplied each field. If mutation injects a sidecar, validation must apply image, resource, security, and identity rules to it too.

Return concise stable reason and actionable message. Avoid reflecting secret fields or entire objects in responses and logs. A denial should name policy, offending safe path/value, and remediation.

If external data is necessary, define authority, cache, freshness, timeout, and fail policy. Prefer local snapshots for hot admission paths. Do not make a remote ticketing or vulnerability service an unbounded synchronous dependency.

### Make mutations deterministic and idempotent

Given the same effective input and parameters, a mutator should produce the same minimal patch. Running it twice must not duplicate sidecars, volumes, finalizers, environment entries, or annotations.

Do not rely on webhook ordering. Other mutators may run before or after and may cause reinvocation. Design the entire set to converge and validate the result after mutation.

Prefer additive, ownership-aware changes. `replace` can overwrite user or controller fields. Treat unordered arrays as sets where appropriate, and respect schema merge semantics. Never mutate immutable mirror/static pod representations expecting the node workload to change.

Mutation should make safe defaults easy, not conceal major behavior. Sidecar injection, identity changes, network interception, or storage modification must be previewable, documented, versioned, and visible in the persisted object.

### Use reinvocation without assuming order

A mutating controller may add a structure another mutator would have processed. Reinvocation can run eligible mutators again when needed, but invocation count and exact relative order should not become business logic.

Idempotence is global: two individually idempotent mutators can oscillate or overwrite each other. Test combined fixed-point behavior with every installed mutating layer and realistic object variants.

Validation is the final guard. If the desired mutation was skipped, overwritten, or conflicted, the validator either accepts a still-safe equivalent or denies with remediation.

Observe patch conflicts, reinvocation count, and unexpected final state. A successful webhook response does not prove its intended field survived later mutation.

### Avoid side effects in admission

Admission may be retried, dry-run, rejected by a later validator, or followed by persistence failure. Creating tickets, allocating IPs, decrementing quota, or writing external state synchronously can leak or duplicate side effects.

Prefer recording intent in the admitted object and let an idempotent controller reconcile external state after persistence. If a webhook necessarily has side effects, declare them accurately, suppress them for dry-run, use idempotency keys, and reconcile orphaned effects.

Kubernetes dry-run executes relevant admission stages but does not persist the object or allow undeclared side effects. It is valuable for preview but generated values can differ from the real request.

Test dry-run through the API server, not only local template rendering. Verify patches, warnings, denials, and side-effect suppression.

### Set failure policy by control role

`failurePolicy` applies when a webhook call or policy evaluation errors, times out, or is misconfigured according to that mechanism. An explicit `allowed: false` response remains a denial.

For an optional/defaulting mutator, `Ignore` may preserve availability if a final validating controller fails closed when the required final property is missing. This decouples convenience mutation from authoritative safety.

For high-impact validation, failing closed is normally necessary. But the webhook must then meet control-plane availability requirements and exclude the minimum dependencies needed to restore it.

Document every fail-open path and compensating enforcement. Alert on ignored webhook calls. “Ignore” is not safe because policy also runs in CI; direct API paths remain.

### Engineer webhook latency and availability

Mutating webhooks are generally called serially; validating webhooks may be called in parallel. Each matched webhook consumes API request budget. Set small timeouts based on measured p99 plus margin, usually far below the maximum.

Run multiple replicas across failure domains behind a stable Service, configure readiness and disruption protection, size for API bursts, and avoid cold-start or remote dependency chains. Secure API-server-to-webhook TLS and rotate serving CA/certificates safely.

Match only necessary requests. Exclude high-volume status/lease/event paths unless genuinely governed. Cache bounded data, precompile policies, and prevent unbounded object or regex work.

Load-test ordinary and adversarial maximum inputs, concurrent cluster recovery, node outage storms, certificate rotation, DNS/network failure, and backend rolling upgrade.

### Prevent dependency loops and self-interception

A webhook deployed inside the cluster depends on its Deployment/Pods, Service, Endpoints, DNS, networking, certificates/secrets, scheduler, nodes, and sometimes storage. If it denies changes to those dependencies while unavailable, recovery deadlocks.

Map the dependency graph. Prefer in-process validation for foundational controls. Narrowly exclude or separately govern bootstrap resources needed to restore the webhook. Do not exclude an entire system namespace without compensating controls.

Prevent a webhook from matching objects it creates for logging or reconciliation. Avoid broad mutation of Events, Leases, endpoint objects, or its own configuration.

Maintain an authenticated, audited recovery procedure that can remove or correct a broken webhook configuration. Test it before an incident and ensure ordinary tenants cannot invoke it.

### Account for controllers and indirect creation

Users often create Deployments, Jobs, operators’ custom resources, or GitOps declarations. Controllers then create pods/resources under their own workload identities. Pod admission sees that controller identity.

Enforce user-level rules on the parent request when the human identity is present. Enforce final workload-state rules on generated objects independent of human identity. Preserve trustworthy provenance through signed or controller-owned fields, not user-forgeable annotations.

Do not exempt general controllers from pod security or validation: that can exempt every user who can create the corresponding parent. Exempt only narrow runtime classes, namespaces, subjects, or objects with separately controlled creation.

Test ownership chains, orphan adoption, resync, rollback, scale, and controller upgrade. A controller may generate a different object shape after version change.

### Use Pod Security Admission deliberately

Pod Security Standards define cumulative Privileged, Baseline, and Restricted profiles. Pod Security Admission applies namespace labels separately for enforce, audit, and warn and can pin the Kubernetes policy version.

Pin versions where cluster upgrades must not silently tighten semantics; preview newer Restricted policy in warn/audit before changing enforce version. Track namespace labels as governed configuration.

Pod templates in workload resources receive warning/audit feedback, while enforce applies to resulting pods. Understand exemptions and update-field behavior from the applicable Kubernetes version.

Avoid exempting controller users. Namespace and runtime-class exemptions are powerful and require owner, rationale, scope, monitoring, and review. Layer custom admission only for organization-specific requirements not covered by the standard.

### Roll out from evidence to enforcement

Test policy and matching offline across API versions and operation matrix. Use server-side dry-run to exercise the installed admission chain. Backtest existing resources and recent sanitized AdmissionReviews where available.

Enable warn/audit/shadow. Inventory violations and evaluation errors, assign owners, validate remediation, and distinguish legacy state from new requests. Canary enforcement in representative namespaces/clusters.

Promote only when latency/error/availability, violation ownership, dependency recovery, match coverage, and bypass tests meet criteria. Maintain rollback or safe roll-forward that does not re-admit a known exploited configuration.

Reconcile existing resources continuously. Admission prevents new/changed objects; it does not automatically repair or remove every object admitted under older policy.

### Observe decisions and mutations safely

Record policy/webhook revision, request UID, operation, group/version/resource/subresource, namespace/name or safe fingerprint, authenticated user/workload, dry-run, match result, decision/reason, patch type/summary, latency, failure type, and enforcement outcome.

Kubernetes audit annotations can capture admission mutation and validation information. Webhook metrics expose request, rejection, fail-open, timeout, and latency behavior. Correlate with API audit outcome.

Do not log full AdmissionReview by default; it may contain Secrets, tokens, environment variables, personal data, or proprietary configuration. Redact and minimize at source.

Alert on fail-open calls, unknown/error decisions, revision drift, timeout/error rate, p99 growth, exemption use, denied recovery dependencies, repeated reinvocation, oversized patches, and direct bypass signals.

### Inventory admission bypasses

Direct etcd writes alter cluster state outside API validation and audit. Limit etcd network access and client certificates to API servers and governed backup/restore tooling; audit and reconcile restores.

Direct kubelet API access can exec or inspect workloads without API-server admission and may evade Kubernetes audit. Restrict node subresources, network access, authentication, and authorization.

Container runtime socket or node-root access can start/alter containers directly. Static pod manifests are consumed by kubelet even if mirror pod admission fails. Restrict node filesystem/runtime access and scan actual node state.

Admission coverage claims must state this boundary. Node hardening, workload identity, runtime detection, network policy, and reconciliation complement API admission.

### Upgrade and retire safely

Cluster upgrades change APIs, defaulting, CEL libraries, built-ins, Pod Security versions, and fields. Test candidate cluster version with current admission configurations and representative requests before control-plane rollout.

Use equivalent match policy/conversion deliberately; validate every served version. New fields should fail or receive defined handling instead of disappearing through decoding.

To replace a webhook with in-process policy, run both in shadow/differential mode, compare results, switch authoritative enforcement, then remove webhook dependencies, certificates, RBAC, Services, and exceptions.

Retain policy and decision provenance for historical explanation. Disaster recovery must not restore retired webhook configurations, expired exemptions, or trust material without reconciliation.

## Definitions and Notation

Let an admission request be

$$
r=(uid,user,groups,op,g,v,res,sub,ns,name,dry,o,old,opts).
$$

A match predicate for controller $c$ is $Match_c(r)$ across rule, scope, selectors, and conditions. A mutator is a partial transformation applied only when matched:

$$
M_c(r,o)=o\oplus patch_c(r,o),
$$

where $\oplus$ follows the declared patch semantics. Idempotence requires

$$
M_c(r,M_c(r,o))=M_c(r,o)
$$

when no other input changes.

For a sequence/reinvocation process reaching final object $o_f$, validation is

$$
Admit(r,o_f)=Schema(o_f)\land BuiltIns(r,o_f)\land
\bigwedge_{c:Match_c(r)} V_c(r,o_f).
$$

Let $L_c$ be latency of controller $c$, $T_c$ its configured timeout, and $F_c\in\{Fail,Ignore\}$ its transport/evaluation failure behavior. End-to-end request latency is affected by serial mutators and parallel validation groups, so the platform measures rather than assumes a simple sum.

For protected effect $z$, admission coverage is bounded by paths crossing the API server:

$$
Covered_{admission}(z)=\forall p\in Paths_{api}(z),\ EffectivePEP(p,z).
$$

Paths outside $Paths_{api}(z)$ require separate controls; admission cannot prove them safe.

## Mechanisms, Invariants, or Proof Structure

### Admission control mechanism

1. Define protected effect and enumerate request/object, API-version, operation, controller-generated, and non-API paths.
2. Trace authentication and authorization before admission and identify which actor/context is present at each request.
3. Select built-in, in-process CEL, or webhook mechanism with exact capability, version, dependency, and failure boundary.
4. Define match matrix for groups, versions, resources/subresources, operations, scopes, selectors, conditions, and narrow exclusions.
5. Implement deterministic idempotent minimal mutations and total validation over the final object, old state, and parameters.
6. Declare failurePolicy, timeout, sideEffects, dry-run, reinvocation, match/conversion, TLS, permissions, and recovery contract.
7. Test syntax/schema, match/no-match, mutation fixed point, all object variants, old/new transitions, errors, timeouts, and adversarial inputs.
8. Backtest, server-side dry-run, audit/warn/shadow, assign violation owners, and canary enforce with measured criteria.
9. Deploy highly available fast components without circular dependencies; validate final state after mutation.
10. Correlate request, decision, patch/warning/denial, policy revision, latency, exception, API audit, and persisted outcome safely.
11. Restrict and monitor etcd, kubelet, runtime, static-pod, node, recovery, and other bypass paths; reconcile actual state.
12. Exercise outage, overload, certificate rotation, cluster upgrade, rollback, migration, retirement, and disaster restore.

### Matching invariant

Every API request capable of the protected effect matches at least one authoritative validator unless it satisfies an explicit governed exclusion; every out-of-scope request avoids unnecessary invocation.

### Mutation invariant

The installed set of mutations converges to a schema-valid fixed point independent of unsupported ordering assumptions, and the final state is revalidated against all safety requirements.

### Failure invariant

Every error, timeout, unreachable service, invalid parameter, and stale dependency produces the risk-approved Fail/Ignore outcome, emits evidence, and cannot be confused with explicit policy allowance.

### Availability invariant

Admission dependencies meet the API path budget and can be restored through a protected route that does not create a reusable tenant bypass.

### Boundary invariant

Claims about admission protection are limited to API-server paths. Direct storage/node/runtime/static-pod paths are separately restricted, detected, and reconciled.

### Proof sketch: idempotence is necessary under reinvocation

Suppose a mutator appends sidecar `agent` on every invocation without first checking whether it exists. On initial invocation it produces one sidecar. Another webhook changes the pod and triggers reinvocation; the mutator appends a second sidecar. Thus identical policy intent yields a different object solely because reinvocation occurred, potentially causing invalid names, resource growth, or repeated patches.

If instead mutation satisfies $M(r,M(r,o))=M(r,o)$, reinvoking it after no relevant external change adds nothing. This does not alone prove the entire webhook set converges—two idempotent mutators can still conflict—but non-idempotence provides an immediate counterexample. Therefore individual and composition-level fixed-point tests are required.

### Executable admission audit

This synthetic classifier checks nine AdmissionReview summaries for scope, operation, final-state image, privilege, owner, and policy availability. It demonstrates decision ordering only; it neither parses Kubernetes objects nor calls an admission API.

<!-- bijux-verify: {"id":"admission-request-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"admitted=4\nscope=1\noperation=1\nimage=1\nprivilege=1\npolicy=1\n"}} -->
```python
requests = [
    ("prod", "CREATE", True, False, True),
    ("prod", "CREATE", True, False, True),
    ("prod", "CREATE", True, False, True),
    ("prod", "CREATE", True, False, True),
    ("excluded", "CREATE", True, False, True),
    ("prod", "CONNECT", True, False, True),
    ("prod", "CREATE", False, False, True),
    ("prod", "CREATE", True, True, True),
    ("prod", "CREATE", True, False, False),
]

counts = {name: 0 for name in ("admitted", "scope", "operation", "image", "privilege", "policy")}
for scope, operation, image_safe, privileged, policy_ready in requests:
    if scope != "prod":
        counts["scope"] += 1
    elif operation not in {"CREATE", "UPDATE"}:
        counts["operation"] += 1
    elif not image_safe:
        counts["image"] += 1
    elif privileged:
        counts["privilege"] += 1
    elif not policy_ready:
        counts["policy"] += 1
    else:
        counts["admitted"] += 1

for name, count in counts.items():
    print(f"{name}={count}")
```

### Verification strategy

Generate a match matrix from discovery and exercise group/version/resource/subresource, create/update/patch/delete/connect, namespace/cluster scope, selectors/conditions, dry-run, old object, parameters, and exclusions.

Test each mutator twice and in installed combinations; compare final object under order/reinvocation changes. Validate every injected container, volume, identity, label, security, and ownership field.

Inject webhook/Service/DNS/network/certificate/policy/data failure, timeout, overload, rolling update, node outage, and dependency loss. Verify explicit denial versus Fail/Ignore and recovery access.

Attempt bypass through parent controllers, old API versions, ephemeral subresources, static pods, kubelet/runtime, etcd restore, node access, and emergency paths. Reconcile API objects with actual workload state.

## Alternatives and Trade-Offs

- **Built-in versus extension.** Built-ins reduce dependencies and track Kubernetes semantics; extensions support organization-specific rules at greater operational cost.
- **In-process CEL versus webhook.** CEL avoids network availability and latency; webhooks support richer logic/data and independent release cadence.
- **Validation versus mutation.** Validation preserves user intent and explanation; mutation improves defaults but creates ordering, ownership, and surprise.
- **Apply-configuration versus JSON Patch mutation.** Apply semantics can manage structured ownership; JSON Patch is explicit but array/index operations are fragile. Test schema behavior.
- **Fail versus Ignore.** Fail preserves enforcement but can block the API; Ignore preserves availability but needs an authoritative compensating guard.
- **Short versus long timeout.** Short timeouts bound API latency and expose unhealthy controls; long timeouts tolerate slowness while amplifying incident impact.
- **Broad versus narrow matching.** Broad matching reduces missed resources but increases latency/recursion; narrow matching needs continuous coverage review.
- **Object selector versus namespace/rule condition.** Object labels are flexible but may be user-controlled; namespace and exact rule/condition boundaries may have stronger governance.
- **Pinned versus latest Pod Security version.** Pinned semantics avoid surprise; latest adopts new protections automatically but can break on upgrade.
- **Warn/audit versus enforce.** Warn/audit reveals impact and enables migration; enforce prevents unsafe new state. Staging needs a deadline.
- **Webhook external lookup versus local snapshot.** Lookup improves currency; snapshot improves latency/reproducibility. Define freshness and failure.
- **One large webhook versus domain webhooks.** One reduces calls but concentrates ownership/blast radius; domain services isolate changes while adding latency/dependencies.
- **Controller exemption versus workload-specific exemption.** Controller exemption is simple but transitively broad; resource/runtime/namespace exceptions can be narrower.
- **User-time versus generated-object enforcement.** Parent admission retains user context; child admission sees final concrete state. Use both without trusting forgeable provenance.
- **Admission versus background controller.** Admission prevents persistence synchronously; controller can reconcile existing state and external dependencies but leaves a window.
- **Server dry-run versus offline test.** Dry-run exercises the real chain; offline tests are fast/deterministic. Generated fields and environment still differ.
- **Automatic rollback versus safe roll-forward.** Rollback restores API availability; it may re-enable exploited state. Preserve emergency denials.
- **API recovery object versus manifest-based recovery.** API configuration is dynamic but can self-lock; protected on-disk configuration can recover the API while expanding node/control-plane governance.
- **Admission-only versus layered node/runtime controls.** Admission handles API desired state; node/runtime controls cover bypass and post-admission compromise.

## Failure Modes and Misconceptions

- “Authorization inspects the whole proposed object” confuses verb/resource permission with field validation.
- “Admission runs before authentication” would lack trustworthy caller identity.
- “The original YAML is the admitted object” ignores defaulting, conversion, patch merge, and mutation.
- “A Kind name belongs in webhook resources” confuses Kind with plural API resource.
- “Matching pods covers ephemeral containers” ignores subresources.
- “CREATE is the only dangerous operation” ignores update, patch, delete, and connect transitions.
- “Namespace selectors work identically for cluster-scoped resources” ignores request scope.
- “A skip label is safe” fails when requesters can set it.
- “Controller username is the original user” loses indirect provenance.
- “Exempting deployment controllers exempts only operators” may exempt all users creating parents.
- “Mutating webhooks have stable order” is unsupported.
- “Individually idempotent means the set converges” ignores interactions.
- “The mutation response proves final state” later mutation can overwrite it.
- “Side effects are safe because request was accepted locally” later validation/persistence can fail.
- “Dry-run is only client-side rendering” server dry-run traverses relevant admission stages.
- “failurePolicy Ignore overrides explicit deny” applies to errors/timeouts, not successful rejection.
- “Fail closed is free” can halt critical API updates.
- “Fail open is safe if CI also checks” direct requests bypass CI.
- “Maximum timeout improves reliability” increases control-plane latency and queues.
- “One replica is enough for a small cluster” makes all matching writes depend on one process.
- “The webhook can govern its dependencies like any workload” risks recovery deadlock.
- “Audit mode provides permanent event history” many reports reflect current state; export audit events.
- “Pod Security Restricted never changes” profile versions evolve.
- “Admission controls static pods” mirror rejection does not stop node execution.
- “Kubelet and etcd access go through admission” they can bypass the API server.
- “Deleting webhook YAML completes retirement” leaves configurations, CA/RBAC, services, exceptions, reports, and restore artifacts.

## Worked Examples

### Example 1

A webhook matches `pods` CREATE but not `pods/ephemeralcontainers` UPDATE. A user with ephemeral-container permission adds a privileged debugger to a running pod.

The request matrix adds the subresource and transition-specific validation; RBAC is narrowed because admission is defense in depth, not a reason to grant broad connect/update rights.

### Example 2

A mutator appends a proxy container on every call. Reinvocation produces duplicates. The corrected mutator detects a stable name/ownership marker, produces no patch when desired state exists, and final validator checks exactly one approved proxy configuration.

Composition tests also detect a second webhook overwriting proxy security context.

### Example 3

An optional mutator adds resource defaults and uses `failurePolicy: Ignore`. A separate in-process validator requires safe minimums in production. During mutator outage, explicitly configured compliant workloads proceed; missing-resource workloads deny.

Convenience failure no longer becomes either cluster outage or safety bypass.

### Example 4

A validating webhook performs live vulnerability queries with five-second p99. Three replicas depend on the same external API. When it slows, all pod creates queue.

The platform moves signed scan/approval summaries into a local bounded snapshot, sets one-second timeout, scales across zones, and measures freshness separately.

### Example 5

Webhook matches its own Deployment and denies certificate-sidecar changes needed during rotation. The service becomes unreachable and fail-closed admission blocks repair.

A tested recovery route narrows exclusion to exact webhook resources/identity, restores it, and adds dependency-graph and certificate-rotation tests. Ordinary namespace workloads remain covered.

### Example 6

Pod Security Admission enforces Baseline v1.36 and warns/audits Restricted v1.37. Reports show teams ready after remediation. The platform pins enforce to Restricted v1.37 rather than `latest` during the next control-plane upgrade.

Namespace exemptions have owners and expiry; controller accounts are not broadly exempted.

### Example 7

An operator custom resource contains a pod template. Human request is validated for tenant permission and permitted configuration. Operator later creates pod as its service account; pod admission validates final security regardless of human identity.

A controller-owned UID/reference links evidence; a user-written `approved=true` annotation does not.

### Example 8

Server-side dry-run returns the fully mutated object and warning without persistence. A webhook that allocates an external address declares side effects incorrectly, and the dry-run leaks allocation.

Allocation moves to a post-persistence reconciler with idempotency and cleanup; webhook declares `None` and only validates intent.

### Example 9

API audit shows no privileged pod creation, yet runtime inventory finds one static pod mounting the host root. Node administrator wrote its manifest directly; mirror-pod admission denial did not stop it.

The platform restricts static manifest directory and node access, inventories actual runtime, and limits its admission coverage claim to API paths.

### Example 10

During cluster upgrade, a new sidecar field appears. A strict webhook decoder drops it and validation never inspects the sidecar. Compatibility tests with the next Kubernetes schema expose the gap.

The webhook uses supported conversion/match semantics, preserves unknown evolution safely, validates all containers, and rolls out before enabling the new API behavior.

## Cross-Program Connections

- **Kubernetes Engineering:** API lifecycle, resources/subresources, controllers, CEL, webhooks, Pod Security, dry-run, and node paths define admission semantics.
- **API and Service Engineering:** request schemas, compatibility, timeouts, TLS, errors, retries, idempotency, and structured denials govern webhook contracts.
- **Security Engineering:** authentication, authorization, least privilege, bypass analysis, fail-safe defaults, exemptions, and recovery bound trust.
- **Distributed Systems:** ordering, fixed points, partial failure, caches, clocks, retry, convergence, and controller reconciliation shape behavior.
- **Reliability Engineering:** API latency/error budgets, dependency loops, failure domains, overload, rollout, and incident repair protect cluster availability.
- **Programming Languages:** CEL/Rego semantics, total predicates, decoding, unknown fields, patch operations, and idempotence affect correctness.
- **Software Testing:** match matrices, property/fuzz/differential tests, dry-run, backtests, load tests, and chaos exercises establish evidence.
- **DevOps and Delivery Engineering:** admission gives GitOps/CI an authoritative runtime counterpart and requires versioned promotion and rollback.
- **Operating Systems:** kubelet, static pods, node files, runtime sockets, and process privileges define non-API bypasses.
- **Governance and Compliance:** policy IDs, warnings, denials, exemptions, audit annotations, control evidence, and retention make enforcement accountable.

## References

1. Kubernetes. [Admission Controllers](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/). Retrieved 2026-09-02.
2. Kubernetes. [Dynamic Admission Control](https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/). Retrieved 2026-09-02.
3. Kubernetes. [Admission Webhook Good Practices](https://kubernetes.io/docs/concepts/cluster-administration/admission-webhooks-good-practices/). Retrieved 2026-09-02.
4. Kubernetes. [Validating Admission Policy](https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/). Retrieved 2026-09-02.
5. Kubernetes. [Mutating Admission Policy](https://kubernetes.io/docs/reference/access-authn-authz/mutating-admission-policy/). Retrieved 2026-09-02.
6. Kubernetes. [Manifest-Based Admission Control](https://kubernetes.io/docs/reference/access-authn-authz/manifest-admission-control/). Retrieved 2026-09-02.
7. Kubernetes. [Kubernetes API Concepts](https://kubernetes.io/docs/reference/using-api/api-concepts/). Retrieved 2026-09-02.
8. Kubernetes. [Authorization](https://kubernetes.io/docs/reference/access-authn-authz/authorization/). Retrieved 2026-09-02.
9. Kubernetes. [Pod Security Admission](https://kubernetes.io/docs/concepts/security/pod-security-admission/). Retrieved 2026-09-02.
10. Kubernetes. [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/). Retrieved 2026-09-02.
11. Kubernetes. [Kubernetes API Server Bypass Risks](https://kubernetes.io/docs/concepts/security/api-server-bypass-risks/). Retrieved 2026-09-02.
12. Kubernetes. [Audit Annotations](https://kubernetes.io/docs/reference/labels-annotations-taints/audit-annotations/). Retrieved 2026-09-02.
13. OPA Gatekeeper. [How to Use Gatekeeper](https://open-policy-agent.github.io/gatekeeper/website/docs/howto/). Retrieved 2026-09-02.
14. Kyverno. [Policy Reports](https://kyverno.io/docs/guides/reports/). Retrieved 2026-09-02.

## Exercises

### Exercise 1

Create an admission request matrix for preventing privileged workload execution. Include parent and child resources, versions, subresources, operations, actors, selectors, and non-API bypasses.

### Exercise 2

Design a sidecar/defaulting mutation and final validation. Specify patch semantics, idempotence, reinvocation, ownership, dry-run, failure policy, timeout, and composition tests.

### Exercise 3

Design a highly available validating webhook for production image and provenance policy. Include dependencies, TLS, data freshness, scaling, match scope, fail behavior, recovery, and observability.

### Exercise 4

Plan migration from a custom pod-security webhook to Pod Security Admission plus a smaller organization-specific policy. Include version pinning, exemptions, audit/warn, differential tests, enforcement, and retirement.

### Exercise 5

Threat-model admission bypass and disaster recovery for etcd, kubelet API, runtime socket, static pods, node root, controllers, and webhook configuration. State which controls and evidence cover each.

## Answers to the Exercises

### Answer 1

Enumerate Pods CREATE/UPDATE and `pods/ephemeralcontainers` UPDATE, plus Deployments, ReplicaSets, StatefulSets, DaemonSets, Jobs, CronJobs, and every installed operator CRD carrying pod templates. Validate parent while human/GitOps context exists and final Pod under controller identity. Cover all served versions/conversion and old-to-new transitions for host namespaces, privileged, capabilities, hostPath, device access, service account, runtime class, and security profiles.

Match exact namespaced resources/operations, with governed namespace selection; never rely on a user-set skip label. Inventory exemptions and who can create parents. Restrict RBAC for exec/ephemeral/update and controller permissions.

Outside admission, constrain static-pod manifest paths, node root, kubelet port and `nodes/proxy`, runtime sockets, direct etcd clients, backup/restore, and alternate/aggregated APIs. Runtime inventory reconciles actual containers with API state and alerts on unmatched workloads.

### Answer 2

Use a declarative apply configuration or minimal JSON Patch to add one named sidecar/default only when absent and compatible. Define ownership marker and reject conflicting user-provided same-name objects rather than overwrite. Applying twice returns the same final object; arrays are treated with schema-aware set/map semantics.

Declare no side effects, support server dry-run, use `IfNeeded` only where later mutations matter, and never assume order. An optional mutator may Ignore failures with a one-second timeout only because a final validator fails closed when the required property is absent or unsafe.

Tests run the mutator twice, permute/reinvoke installed mutators, cover existing/conflicting/partial sidecar, all container types, API versions, malformed/maximum inputs, and ensure final validation catches overwritten image, identity, resources, network, or security context. Persisted object and decision evidence show the mutation survived.

### Answer 3

Normalize every container image/digest and provenance reference locally; use a signed bounded approval snapshot rather than synchronous registry/scanner calls. Match exact workload resources, versions, create/update and relevant subresources; inspect final state and controller-generated pods. Return stable denial reasons without raw provenance secrets.

Run multiple stateless replicas across zones behind ClusterIP Service with readiness, disruption protection, autoscaling/capacity for API bursts, precompiled policy, and one-second timeout. API server authenticates TLS using pinned/rotated CA; webhook has minimal RBAC. Production validator uses Fail, with narrowly protected dependencies/recovery; lower-risk preview is separate.

Monitor request/decision/reason, p50/p95/p99, timeout, rejection, fail-open, snapshot age, active policy/data revision, TLS errors, and API outcome. Load-test node outage storms, DNS/network partitions, cert rotation, data staleness, rolling upgrade, oversized objects, and dependency recovery. Server-side dry-run and canary precede fleet enforcement.

### Answer 4

Inventory current webhook rules, versions, exemptions, denials, mutations, policy-specific extensions, dependencies, and bypasses. Map controls covered by Baseline/Restricted and keep only requirements genuinely outside Pod Security Standards.

Pin the current target Pod Security version. Apply Restricted in audit and warn while existing enforce remains; backtest namespaces and templates, assign violations, and encode only narrow owned exemptions—never general controller exemptions. Differential-test webhook, PSA results, and custom policy across current/next cluster versions and all pod sources/subresources.

Canary PSA enforcement by namespaces/clusters, then move custom checks to in-process CEL when possible. After full coverage and recovery testing, disable old webhook enforcement, observe shadow comparison, remove configuration, Service/Deployment, CA/certs, RBAC, data, dashboards, and old exemptions. Reconcile restore artifacts so webhook cannot return.

### Answer 5

Direct etcd access can change all stored state without admission/audit: restrict network/client CAs to API servers and governed backup tooling, protect keys, log access, validate/reconcile restores. Kubelet API and `nodes/proxy` can exec/read without admission: narrow RBAC, authenticate/authorize kubelet, restrict port, and audit node telemetry.

Runtime socket and node root can start containers or edit static manifests: prohibit host mounts, isolate sockets, restrict administrators/files, integrity-monitor paths, and reconcile runtime inventory. Static mirror admission denial does not stop execution. Controllers cross admission but change actor context: validate parent and generated final state, preserve trusted provenance, and avoid broad controller exemption.

Webhook/admission configuration can disable controls or self-lock: limit RBAC, require policy review, audit every change, protect verification/TLS keys, and maintain tested individual emergency recovery or manifest-based route. Disaster restore compares policies, exemptions, CAs, and registrations with a current retirement ledger before serving requests; expired or revoked controls are not resurrected.
