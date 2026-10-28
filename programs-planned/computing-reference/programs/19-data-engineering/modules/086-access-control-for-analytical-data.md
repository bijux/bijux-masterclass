---
module_id: DE-086
program: Data Engineering
level: 2
module_number: 86
title: Access Control for Analytical Data
status: complete
last_verified: 2026-09-03
---

# Access Control for Analytical Data

## One-Page Review

### Governing question

How can a data organization authorize people and workloads to discover, query, transform, administer, and export exact analytical resources for approved purposes, with row-, column-, and result-level constraints that remain effective across warehouses, lake engines, semantic layers, notebooks, caches, and derived artifacts, without mistaking authentication, a broad role, a masked view, or an approval ticket for durable least privilege?

### Essential definitions

- **Authentication** establishes evidence about an identity; **authorization** decides whether that identity may perform an action on a resource in context.
- A **principal** is the human, workload, service, group, or delegated identity evaluated by policy; actor and effective subject remain distinct during delegation.
- An **entitlement** is a versioned grant or derived permission binding principal, action, resource, constraints, valid time, source, and authority.
- **RBAC** assigns permissions through organizational roles; **ABAC** evaluates subject, object, action, and environmental attributes against policy.
- A **policy decision point (PDP)** evaluates policy; a **policy enforcement point (PEP)** prevents the operation unless the decision permits it; a **policy information point (PIP)** supplies trusted attributes.
- **Coarse-grained control** governs platforms, projects, catalogs, schemas, tables, stages, or functions; **fine-grained control** governs rows, columns, cells, joins, groups, or query shapes.
- A **row filter** limits which records are visible; a **column policy** denies, masks, or transforms fields according to context.
- A **purpose constraint** limits authority to a declared and governed use rather than treating membership as permission for every use.
- **Just-in-time access** activates bounded authority for a short interval after policy checks or approval; it is not a permanent role with a short-lived session.
- A **decision receipt** records the evaluated identity, action, resource/version, relevant attributes, policy revision, outcome, reason, constraints, enforcement point, and time.
- **Derived-data propagation** computes handling and entitlement implications for query results, extracts, caches, models, and downstream datasets from their inputs and transformations.
- **Break-glass access** is exceptional, predeclared, time-bounded authority with strong authentication, justification, alerting, review, and automatic revocation.
- **Inference control** limits disclosure from small groups, repeated queries, joins, differences, or auxiliary data that ordinary row/column checks do not prevent.
- **Access review** tests whether effective authority is still necessary, correct, used, owned, and enforceable; a list of direct grants alone is not an effective-access review.

### Central model, mechanism, or theorem

For policy revision $P$, principal $s$, action $a$, exact resource $o$, context $c$, and time $t$:

$$
D_P(s,a,o,c,t)\in\{permit,deny,indeterminate\}.
$$

Permit requires valid identity and delegation, an active authorized entitlement, satisfied resource/action/purpose/environment predicates, complete sufficiently fresh attributes, and no applicable overriding deny. For a table generation $T_g$, the readable relation and projection are therefore:

$$
Rows_{s,c}=\{r\in T_g\mid D_P(s,read,r,c,t)=permit\},
$$

$$
View_{s,c}=Project_{AllowedColumns(s,c)}(Transform_{policy}(Rows_{s,c})).
$$

This is necessary but not sufficient for safe analytics: query shape, joins, group size, repetition, output classification, export destination, and artifact lifetime may impose additional constraints. Every observation or effect must pass a PEP using the same scoped decision semantics.

### Critical invariants

- Deny by default; missing identity, resource, classification, ownership, purpose, policy, or required attribute is indeterminate and cannot silently permit.
- Human actor, effective/delegated subject, client, and executing workload are authenticated and audited separately.
- Actions distinguish discover, read metadata, query values, unmask, join, create derivative, export, share, administer policy, and approve access.
- Resources use stable IDs plus catalog/schema/table/view/field/generation, tenant/domain, environment, and classification; a mutable name is insufficient.
- RBAC supplies stable coarse responsibility; attributes, relationships, purpose, state, and explicit denies narrow authority without uncontrolled role explosion.
- Group nesting, role hierarchy, inherited grants, ownership, public links, service delegation, and platform bypass roles are included in effective-access computation.
- Row predicates constrain rows before aggregation and pagination; column controls cover explicit selection, wildcard expansion, expressions, nested fields, and indirect use.
- Masking changes representation, not necessarily authorization or classification; permission to see a mask is not permission to unmask or export the source.
- Base tables remain protected even when views or semantic layers enforce additional policy; alternate engines, direct storage paths, replicas, and recovery tools cannot bypass controls.
- The PEP binds the current decision to the exact query, result, mutation, policy version, and execution identity; policy-engine error is not permission.
- Query results, downloads, temporary tables, notebooks, caches, dashboards, logs, model features, and extracts receive owner, classification, access, expiry, and lineage.
- JIT grants and exceptions have exact scope, approver authority, justification, start/end, revocation, monitoring, and renewal rules.
- Break-glass use cannot disable its own audit, has independently protected receipts, triggers notification, and is reviewed after use.
- Access-control administration is separated from data use and independent review for high-risk resources.
- Decision logs minimize or redact sensitive inputs while preserving policy revision, reason, outcome, and traceability.
- Reviews reconcile desired, configured, inherited, cached, and observed access; inactivity alone is evidence for review, not automatic proof that authority is unnecessary.
- Revocation covers sessions, role activation, credentials, tokens, cached decisions, shares, extracts, scheduled jobs, and downstream artifacts within declared bounds.
- Tests cover positive access and adversarial denials, alternate paths, stale attributes, policy rollout/rollback, outage behavior, and derived data.

### Common failures

Common failures include granting one analyst role across a warehouse; trusting network location or successful login; confusing OAuth scope with row authority; authorizing a dashboard but leaving its warehouse identity broad; filtering rows in a view while the base table remains readable; masking output while predicates, joins, errors, or exports leak values; using the invoker's submitted purpose; applying policy after aggregation; ignoring nested columns and wildcard projections; letting table owners bypass policy; copying data into an uncontrolled scratch schema; running every notebook as one service account; retaining grants after team transfer; approving access without expiry; losing policy tags during copy/replace; failing open during PDP or attribute outage; logging sensitive policy inputs; reviewing only direct grants; and revoking the user while scheduled jobs, tokens, shares, caches, or extracts remain active.

### Compact example

An analyst role permits `query` on a customer product, but policy also requires region membership, purpose `churn_analysis`, an active training record, row restriction to the analyst's region, masked contact fields, no raw export, and a seven-day grant. A request with the same role and wrong purpose is denied; an unavailable training attribute is indeterminate and denied; a permitted query receives row and column constraints plus a decision ID. Its materialized result inherits sensitive classification, the requesting team as owner, the same export prohibition, and seven-day expiry. The role is only one input to authority.

### Connections

[DE-066](066-time-travel-and-reproducible-reads.md) binds exact generations, [DE-076](076-data-contracts.md) declares allowed uses, [DE-077](077-producer-and-consumer-responsibilities.md) separates duties, [DE-078](078-data-incident-detection-and-triage.md) handles unauthorized access, [DE-081](081-technical-operational-and-business-metadata.md) supplies policy attributes, [DE-082](082-dataset-and-column-lineage.md) traces derivatives, [DE-083](083-data-catalogs.md) exposes governed request paths, [DE-084](084-ownership-and-stewardship.md) assigns approval authority, and [DE-085](085-classification-and-sensitive-data.md) supplies handling evidence. [DE-087](../ROADMAP.md) next examines protective transformations. [API-034](../../28-api-and-service-engineering/modules/034-authorization-checks.md) and [API-046](../../28-api-and-service-engineering/modules/046-object-level-authorization.md) develop request-level enforcement.

## Governing Question

Analytical access is broader than opening a table. A principal may discover metadata, preview values, execute a query, use a protected field in a predicate, see an aggregate, unmask a value, join two products, create a derivative, schedule a workload, export a result, publish a dashboard, administer grants, or accept an exception. Treating these actions as one `read` privilege either exposes too much or blocks legitimate work.

The resource is equally multidimensional. Catalog, project, schema, table, view, column, row, tenant, partition, snapshot, semantic metric, model feature, file, share, and query result can each be a policy boundary. Names and locations change; classification, ownership, contract, jurisdiction, and lifecycle state can change without a rename. The decision must bind stable identity and exact versioned scope.

Analytics also creates new information. A user denied direct access to salary may infer it through a small aggregate, repeated differences, an error, a join, or a feature. A permitted result can become a durable extract outside the original PEP. Fine-grained row and column controls are valuable but do not solve composition, inference, export, or lifecycle by themselves.

The governing requirement is therefore end-to-end authorization: trustworthy identities and attributes, explicit actions and resources, least-privilege policy, enforcement on every path, constrained query evaluation, governed result creation, auditable receipts, bounded grants, effective revocation, and adversarial testing.

## Why This Matters

Analytical platforms centralize high-value data and powerful computation. A single broad grant can expose millions of records, join domains that were separately tolerable, or create portable files faster than a human reviewer can respond. Conversely, slow manual approval and coarse denials drive screenshots, shared accounts, local copies, and shadow pipelines.

Access decisions affect correctness as well as confidentiality. Row filtering can silently change denominators; masking can change join behavior; a dashboard seen by two regions can calculate different totals. Consumers must know that policy-shaped results are context-dependent without learning the hidden data. Reproducibility requires the policy revision and relevant identity context, not just SQL and table snapshot.

Modern data estates have multiple planes. Catalogs advertise products; orchestration runs service identities; warehouses evaluate SQL; lake engines read object storage; BI tools cache extracts; notebooks hold credentials; reverse ETL sends records outward. A control that exists only in one interface is an invitation to route around it.

Finally, governance claims require evidence. An approval ticket proves that someone approved something, not that the correct policy reached every PEP or that revocation removed effective access. Decision receipts, configuration reconciliation, path tests, access simulations, and artifact inventories connect policy intent to actual behavior.

## Prerequisites and Retrieval

Retrieve identity foundations: authoritative human/workload/service identities, authentication assurance, groups, role hierarchy, employment/vendor status, team/domain, tenant, device/session context, delegation, impersonation, token audience, credential/session lifetime, and offboarding events.

Retrieve resources: stable product/distribution/dataset/table/view/field/generation IDs; catalogs, schemas, storage locations and replicas; tenant/region/jurisdiction; classification; contracts; owner/steward; lineage; lifecycle; query engines; semantic models; BI assets; notebooks; extracts; shares; caches; exports; and recovery paths.

Retrieve actions: discover metadata, preview/sample, query, use in filter/join/group, project, unmask, insert/update/delete, create derivative, schedule, export/download, share/publish, manage grants/policy/tags, inspect audit, and invoke emergency authority.

Retrieve policy inputs: role and relationship assignments; subject/object/environment attributes with source, version, freshness and confidence; purpose and lawful/contractual constraints as determined by qualified authorities; row/column rules; explicit denies; separation of duties; grant/exception records; time/location/network/device conditions; query limits; and output obligations.

Retrieve enforcement: entry points, PEP/PDP/PIP topology, policy bundles/revisions, rollout state, fail behavior, caches and invalidation, base-storage ACLs, warehouse privileges, row policies, masks, authorized views, semantic policies, query firewall, export gateway, object-store permissions, notebook/runtime identity, and downstream transfer controls.

Retrieve evidence: request/approval/rejection, decision IDs, policy inputs minimized for audit, query/access history, rows/bytes/result classification, exports and destinations, denied attempts, break-glass use, configuration snapshots, drift findings, grant utilization, review decisions, revocation latency, test results, incidents, and remediation.

Distinguish authentication from authorization; identity from account; actor from effective subject; role from entitlement; desired from effective access; direct from inherited grant; discover from read; use in a predicate from project; row filter from separate storage; mask from declassification; query permission from export permission; source authorization from derivative authorization; ticket approval from PEP behavior; decision from enforcement; denial from indeterminate; and legal/purpose assessment from a self-asserted string.

Create an access-policy record:

| Concern | Required evidence and decision |
|---|---|
| Subject | Actor, effective subject, workload/client, tenant, assurance and delegation |
| Action | Stable semantic action, fields/query shape, effect and risk class |
| Resource | Stable IDs, exact generation/scope, owner, classification and location |
| Context | Purpose, environment, jurisdiction, time and authoritative attributes |
| Entitlement | Role/relationship/grant source, authority, start/end and constraints |
| Decision | Permit/deny/indeterminate, rule/reason, policy revision and attribute versions |
| Enforcement | PEP, constrained rows/columns/query/export and protected effect |
| Derivative | Output lineage, classification, owner, audience, destination and expiry |
| Governance | Request, approval, separation, exception, review, appeal and revocation |
| Evidence | Decision receipt, configuration, observed use, tests, drift and incident route |

Write a falsifiable claim: “Human H17 acting through notebook workload W9 may query generation G42 of product P under policy Y12 for approved purpose U3 until 2026-09-10; role R supplies coarse query authority, region attribute A8 restricts rows, classification C6 denies two columns and masks one, join policy J2 forbids identity-table combination, export policy E4 denies raw downloads, PDP revision B19 returns constraints and decision ID D7, warehouse and storage PEP tests agree, derivative artifacts inherit owner/classification/expiry, and revocation exercise X5 invalidates roles, sessions, cached decisions and scheduled jobs within ten minutes.”

## Learning Objectives

After completing this module, you should be able to:

1. distinguish identity, authentication, authorization, entitlement, approval, enforcement, and audit for humans and workloads;
2. model analytical decisions over explicit principal, action, resource, context, time, policy, and indeterminate states;
3. combine RBAC, ABAC, relationships, purpose, explicit denies, and temporal grants without uncontrolled role explosion;
4. design row-, column-, semantic-, query-, join-, aggregation-, and export-level enforcement across multiple engines;
5. protect base data and alternate paths while governing views, dashboards, notebooks, service accounts, caches, and shares;
6. propagate classification, ownership, access constraints, retention, and expiry to analytical derivatives;
7. govern access requests, approvals, JIT activation, exceptions, break-glass use, reviews, transfer, and revocation;
8. preserve reproducibility and audit with versioned decision receipts while minimizing sensitive telemetry;
9. measure effective-access coverage, policy drift, unused privilege, decision/enforcement failures, revocation latency, and harmful outcomes; and
10. test authorization with policy units, effective-access simulation, differential identities, alternate paths, mutations, outages, and incident exercises.

## Core Exposition

### Begin with identities and sessions, not email strings

Represent people, workloads, services, groups, and external partners with issuer-scoped stable identifiers. Email addresses, display names, and team labels are mutable attributes, not durable principal identity. Preserve the authentication assurance, client, credential type, session start, token audience, and identity-provider evidence relevant to the decision.

A query commonly involves more than one identity. A person uses a notebook; the notebook invokes a query service; the query engine reads object storage; a scheduler later refreshes the result. Record the initiating actor, effective/delegated subject, client, and executing workload at each hop. Do not collapse them into the powerful warehouse service account or blindly propagate a human bearer token.

Attributes need provenance and freshness. `department=oncology`, `training=current`, and `region=eu` should come from governed systems with versions, timestamps, lifecycle rules, and unavailable behavior. A caller-submitted `purpose=research` is a request, not authoritative approval. If a required attribute is absent or stale beyond policy, the decision is indeterminate and fails safely.

Sessions activate only required authority. A person eligible for several roles need not activate all simultaneously. High-risk unmask/export/admin actions may require fresh authentication, managed devices, explicit elevation, or separation from ordinary analysis.

### Name resources and actions at analytical grain

Use a stable resource hierarchy: organization, platform/account, catalog/database, schema/domain, product/distribution, table/view, column/field, row/cohort, snapshot/generation, and artifact. Inheritance can reduce administration, but the inherited result must be inspectable. A grant at a parent is not safe merely because the child was created later.

Actions must describe semantic effects. `discover` may reveal only approved metadata. `query` may use allowed rows and fields. `project_sensitive` exposes a field; `filter_sensitive` or `join_sensitive` uses it without projection but can still leak information. `unmask`, `create_derivative`, `schedule`, `export`, `share`, `grant`, `alter_policy`, and `view_audit` deserve separate authority.

Bind policy to immutable generation or an explicit moving product scope. A grant to “current certified distribution” behaves differently from a grant to snapshot G42. Record which meaning applies. Schema additions should not automatically become readable through wildcard privileges without classification and policy evaluation.

### Compose RBAC, attributes, relationships, and constraints

RBAC captures stable job functions and permission assignment. It supports review and separation of duties better than thousands of individual grants, but roles should not encode every region, project, field, and temporary exception. Otherwise `analyst_eu_project7_masked_2026` proliferates and becomes unintelligible.

ABAC evaluates governed subject, object, action, and environment attributes. It expresses policies such as “trained clinical analysts may query pseudonymized study fields for protocol U3 from an approved environment.” Its correctness depends on taxonomy, attribute authority, freshness, and predictable missing-value semantics.

Relationships capture ownership, assignment, membership, delegation, and product-consumer contracts. Explicit denies protect legal hold, investigation, conflict-of-interest, or prohibited-use cases. Declare precedence: a broad allow must not accidentally override a narrow deny. Constraints can return permitted rows, columns, transformations, query shapes, rate/budget limits, destination rules, and expiry rather than only a Boolean.

Keep policy understandable. Normalize action/resource vocabularies, lint unreachable or contradictory rules, require owners and tests, version changes, simulate effective-access deltas, canary deployment, and retain rollback. Complexity that no reviewer can explain is a control weakness.

### Separate control plane, decision, information, and enforcement

The control plane manages identity mappings, grants, attributes, classifications, policies, approval workflows, bundles, and rollout. A PDP evaluates a request. PIPs provide trusted identity, relationship, classification, and environment facts. PEPs intercept the actual discovery, query, unmask, export, or administrative effect.

Central policy improves consistency; distributed enforcement improves latency and availability. A practical architecture distributes signed/versioned policy bundles close to engines, reports activation state, and emits protected decision receipts. Central intent does not guarantee every engine loaded the same revision. Treat lag, failed compilation, unsupported rules, and unregistered PEPs as visible states.

Fail behavior is action-specific but fail-safe. If a PDP is unavailable, a bounded cached permit might continue for low-risk reads only when policy explicitly defines freshness and revocation bounds. High-risk unmask/export/admin operations may require a current decision. A cache miss, parse error, missing attribute, or unknown resource never becomes an implicit allow.

Decision logs can contain identities, resource names, purposes, query fragments, and sensitive attributes. Minimize, tokenize, redact, encrypt, restrict, retain, and monitor them. Preserve decision ID, policy revision, outcome, reason code, enforcement point, timestamps, and attribute-version references needed for audit and replay.

### Enforce coarse boundaries and fine-grained rows and columns

Platform/account, catalog, schema, and table privileges form the first boundary. Base tables and storage locations remain least-privileged; authorized views or semantic models should not coexist with broad direct access that bypasses them. Inventory owner, administrator, support, recovery, replication, and system roles whose capabilities exceed ordinary policy.

Row policy should restrict input rows before projection, grouping, windowing, aggregation, pagination, and result counts. Its predicate may use tenant, region, assignment, subject relationship, consent/purpose, or cohort. Test nulls, new enum values, missing mappings, owner bypass, copy/replace behavior, and optimizer interactions. Separate physical datasets can provide stronger isolation for certain tenants or partners at greater operational cost.

Column policy distinguishes denial, transformed/masked observation, and unmasked observation. It must cover wildcard selection, nested/repeated structures, functions, user-defined functions, error paths, previews, metadata statistics, search indexes, materialized views, and result caches. Using a hidden column in filters, joins, ordering, or groups can reveal it even if it is not projected.

Policy-shaped results can differ by principal. Dashboards and caches must key on relevant authorization context or apply policy after retrieval at an authoritative layer. Never populate a shared cache with one privileged principal and serve it to everyone.

### Govern query shape, joins, aggregation, and inference

Row and column decisions answer which atomic records and values may participate. They do not guarantee that arbitrary computation is safe. A permitted user can isolate one person with `COUNT`, compare two overlapping groups, repeatedly vary predicates, join quasi-identifiers to identity data, or train a model that memorizes sensitive examples.

For high-risk domains add query controls: approved semantic measures, join allowlists, minimum group size, suppression, contribution limits, bounded history, rate/privacy budgets where appropriate, prohibited functions, output scanning, or reviewed clean-room protocols. These controls have assumptions and residual risks. A minimum group size alone fails against repeated differences and correlated auxiliary data.

Purpose matters at the query and output, not only request time. The system cannot infer human intent perfectly from a string. Combine approved project membership, declared purpose, contract, training, query patterns, destination, review, and monitoring. Do not claim that technical policy alone determines legal permissibility.

Explain policy-shaped semantics to consumers. A metric computed after row filtering is a metric over an authorized subset. Reproducibility records dataset generation, SQL/model version, semantic definition, policy revision, relevant attribute snapshot or pseudonymous context, and output constraints.

### Treat derived results as governed data

Query results create new resources. Register durable tables, extracts, files, notebook outputs, model features, dashboard caches, and shares with lineage, owner, classification, audience, location, purpose, retention, and expiry. Ephemeral results still need bounded storage and cleanup.

Conservative propagation starts from input classifications and policies, then considers transformation. An aggregate may reduce some row-level risk but can retain confidential business meaning or inference risk. A tokenized identifier can preserve linkability. A joined result can be more sensitive than either input. Declassification requires the evidence process developed in DE-085 and transformation analysis developed next in DE-087.

Source permission does not automatically grant export or onward sharing. Exports cross enforcement boundaries and may change jurisdiction, retention, incident response, deletion, and contract behavior. Gate destination, format, fields, row volume, encryption, recipient, expiry, watermarking or other applicable controls, and create a receipt.

On revocation, find already materialized artifacts and scheduled jobs. Prevent new access immediately within policy bounds, invalidate sessions and caches, disable future refreshes, and remediate existing copies according to contract, retention, and incident policy.

### Design request, approval, JIT, and exceptional access

Self-service begins with a discoverable product, clear eligibility, intended uses, data classification, required training, available access profiles, and accountable approvers. Request the minimum product/action/fields/rows/purpose/environment/time. Suggesting a standard least-privilege profile is safer and faster than asking users to compose raw grants.

Automate approval for low-risk, policy-complete requests. Route higher-risk cases to the roles authorized in DE-084, preserving separation between requester, risk approver, grant executor, and reviewer where needed. A ticket state is an input to provisioning, not proof that provisioning or enforcement succeeded.

JIT access creates or activates a narrowly scoped entitlement with automatic expiry. Approval, grant, propagation, first use, extension, revocation, and cleanup are separate observable states. Reauthentication or ticket presence without entitlement expiry is not JIT.

Break-glass is for declared emergencies, not a convenience role. Require strong authentication, exact reason/case, short duration, least privilege, alerting to independent responders, immutable audit, post-use review, and credential/session revocation. Test it before emergencies without exposing production data unnecessarily.

### Reconcile desired, configured, effective, and observed access

Desired access is what policy and approvals intend. Configured access is what systems store. Effective access includes direct/inherited grants, nested groups, role activation, ownership, impersonation, public/share links, service delegation, administrator bypasses, cached decisions, and alternate paths. Observed access is what logs show. These sets differ.

Build effective-access graphs and answer “why can principal S perform action A on resource O?” Include grant chain, attribute/relationship sources, policy revision, exception, and expiry. Review high-risk access more frequently and on trigger events such as team transfer, contract end, classification increase, product retirement, incident, dormant service account, or owner change.

Usage evidence helps right-size privilege but is incomplete: absence may mean rare emergency duty or missing telemetry, while use may be unauthorized. Review business need, authority, scope, compatibility, conflicts, service identity ownership, expiry, and derivative holdings. Require reviewer decisions and verify resulting enforcement changes.

Measure eligible resources with enforced policy, unregistered paths, policy-revision lag, overbroad/inherited grants, orphaned accounts, unused high-risk privileges, JIT duration, approval latency, denied/indeterminate rates, decision errors, export volume, review completion, revocation latency, escaped access, and recurrence. Avoid optimizing approval speed or denial count without outcome context.

## Definitions and Notation

Let $S$ be principals, $A$ actions, $O$ resources or exact generations, $C$ contexts, $T$ times, and $P_v$ policy revision $v$. Let $Attr_S(s)$ and $Attr_O(o)$ be versioned subject and object attributes from authoritative PIPs. Let $Ent(s,a,o,t)$ mean an active entitlement, possibly derived through roles or relationships.

Define authorization:

$$
D_{P_v}(s,a,o,c,t)=
\begin{cases}
permit & \text{if } Valid(s,c,t)\land Ent(s,a,o,t)\land Pred_{P_v}(s,a,o,c,t)\land \neg Deny_{P_v}(s,a,o,c,t),\\
deny & \text{if a valid applicable deny holds or the complete policy proves no permit},\\
indeterminate & \text{if required identity, attribute, policy, or evaluation evidence is unavailable.}
\end{cases}
$$

An obligation-bearing permit is $\langle permit,K,e,v,d\rangle$, where $K$ contains row, column, query, mask, destination, logging, or rate constraints; $e$ is expiry; $v$ is policy revision; and $d$ is the decision ID. The PEP must enforce $K$ and reject use after $e$ or outside the bound request.

For query $q$ over inputs $I(q)$, define the authorized input relation $R^P_{s,c}$ by row predicates and allowed operations. The output is:

$$
Y=q(R^P_{s,c}) \quad \text{only if } ShapeAllowed(q,s,c,P_v).
$$

Then derive governance assertions:

$$
Govern(Y)=Propagate(\{Govern(x):x\in I(q)\},q,c,P_v).
$$

`Propagate` is policy- and transformation-aware; it is not always the maximum scalar label. An **effective-access graph** is a proof path from principal through group/role/relationship/grant and policy predicates to action/resource. A **bypass path** reaches an observation/effect without the intended PEP. **Revocation latency** is elapsed time from authoritative revocation event to loss of effective authority across every relevant path and cached artifact.

## Mechanisms, Invariants, or Proof Structure

### A complete decision and enforcement sequence

1. Authenticate the human and/or workload, validate issuer/audience/credential/session, and preserve actor, effective subject, client, tenant, and delegation.
2. Map the requested operation to a canonical action and stable resource/generation; reject unknown action/resource shapes.
3. Retrieve authoritative roles, relationships, classifications, ownership, purpose approval, environment, and attribute versions with freshness rules.
4. Resolve direct, inherited, temporal, exceptional, and explicit-deny entitlements; enforce separation and conflict constraints.
5. Evaluate one policy revision and return permit, deny, or indeterminate plus reason, constraints, expiry, decision ID, and relevant version references.
6. At the PEP, constrain base resources, rows, columns, query shape, joins, aggregations, output, and destination before any observation or effect.
7. Bind the decision to the executing identity and exact query/effect; re-evaluate when policy-relevant facts or bounded validity change.
8. Register durable derivatives and propagate classification, owner, audience, purpose, location, retention, expiry, and lineage.
9. Emit a minimized protected receipt and operational metrics; distinguish policy denial, missing evidence, evaluation failure, and enforcement failure.
10. Reconcile rollout/configuration, test alternative paths, review effective access, and revoke sessions, grants, jobs, caches, shares, and artifacts when authority ends.

### Enforcement theorem and assumptions

**Claim.** If every path capable of observing or changing governed data passes an unbypassable PEP; each PEP enforces a valid decision bound to the same principal, action, resource, context, policy revision, and effect; all required attributes are authoritative and sufficiently fresh; unknown/error states cannot permit; and derivatives remain inside governed PEPs or receive enforceable propagated obligations, then no governed observation/effect occurs without a corresponding permit under that model.

**Proof sketch.** Consider an arbitrary governed observation/effect $e$. By path completeness, its path contains a PEP. By enforcement, the PEP proceeds only with a valid bound permit whose constraints cover $e$. By fail-safe evaluation, unavailable required evidence cannot generate that permit. By binding, another principal, resource, action, context, expired interval, or changed relevant state cannot reuse it. If $e$ creates a derivative, propagation keeps subsequent observations within the invariant. Therefore $e$ has a corresponding permit. The result follows for every governed path.

The assumptions are strong and operational. An unregistered storage credential, administrator bypass, copied extract, stale group, shared BI cache, or ungoverned derivative violates path completeness or binding. The theorem does not prove that policy is ethical, lawful, correctly classified, free from inference, or resistant to compromised authorized principals. Those require governance, threat analysis, monitoring, and qualified review.

### Executable decision illustration

The following deterministic policy demonstrates role as necessary but insufficient, explicit deny precedence, required-attribute failure, and constrained permits. It is an illustration, not a production policy engine or legal-purpose evaluator.

<!-- bijux-verify: {"id":"analytical-access-decision","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"analyst_permit=permit rows=region:eu columns=customer_id,postal_area export=false\nwrong_purpose=deny\nmissing_training=indeterminate\ninvestigation_hold=deny\nrole_alone_is_sufficient=false\n","stderr":""}} -->
```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Request:
    role: str
    region: str
    purpose: str
    training_current: bool | None
    investigation_hold: bool


def decide(request: Request) -> tuple[str, dict[str, str]]:
    if request.training_current is None:
        return "indeterminate", {}
    if request.investigation_hold:
        return "deny", {}
    if request.role != "analyst" or request.purpose != "churn_analysis":
        return "deny", {}
    if not request.training_current or request.region not in {"eu", "us"}:
        return "deny", {}
    return "permit", {
        "rows": f"region:{request.region}",
        "columns": "customer_id,postal_area",
        "export": "false",
    }


base = Request("analyst", "eu", "churn_analysis", True, False)
outcome, constraints = decide(base)
print(
    "analyst_permit=" + outcome,
    "rows=" + constraints["rows"],
    "columns=" + constraints["columns"],
    "export=" + constraints["export"],
)
print("wrong_purpose=" + decide(Request("analyst", "eu", "marketing", True, False))[0])
print("missing_training=" + decide(Request("analyst", "eu", "churn_analysis", None, False))[0])
print("investigation_hold=" + decide(Request("analyst", "eu", "churn_analysis", True, True))[0])
print("role_alone_is_sufficient=false")
```

The output is reproducible because every input is explicit. A real system must authenticate them, version policy and attributes, produce a decision receipt, enforce constraints in its query engine and export path, and handle revocation.

## Alternatives and Trade-Offs

1. **Individual grants versus group/role grants.** Individual grants are precise for rare cases but hard to review and transfer. Groups and roles scale stable responsibility but hide nesting and can become overbroad. Prefer governed roles with bounded exceptions.
2. **RBAC versus ABAC.** RBAC is legible and stable; ABAC expresses context and classification without combinatorial roles. ABAC adds dependence on attribute quality and policy tooling. Many estates use RBAC for coarse eligibility and ABAC to narrow it.
3. **Embedded versus external PDP.** Embedded decisions reduce latency and network dependency; an external service centralizes behavior and updates. Both need versioned policy, health, caching rules, audit, and enforcement close to effects.
4. **Centralized versus distributed PEPs.** One gateway is easier to observe but cannot cover direct storage and engine access. Distributed PEPs cover effects near data but risk version drift. Central intent plus attested distributed enforcement is common.
5. **Authorized views versus native row policies.** Views are portable and expressive but proliferate and can be bypassed by base access. Native row policy applies transparently but may have engine limitations, owner bypass, performance cost, or surprising copy semantics.
6. **Column denial versus dynamic masking.** Denial gives a crisp boundary; masking supports legitimate limited use. Masks can preserve linkability, distort analyses, and leak through predicates or joins. Treat unmask as a separate action.
7. **Logical filtering versus physical separation.** Logical policy reduces duplication and supports flexible cohorts. Separate tables/accounts/storage create stronger fault and partner boundaries but increase pipelines, reconciliation, cost, and deletion work.
8. **Standing versus JIT access.** Standing grants reduce workflow latency and support frequent work but accumulate. JIT narrows exposure and produces intent evidence but depends on reliable approval and activation. Emergency and automation needs must be designed explicitly.
9. **Human approval versus policy automation.** Human judgment handles novel context; manual queues are slow and inconsistent. Automate complete low-risk cases, escalate ambiguity/consequence, and test both routes.
10. **Boolean decisions versus obligation-bearing decisions.** Boolean permit/deny is simple. Returning row, column, mask, export, logging, and expiry constraints is more expressive but requires every PEP to understand and enforce them consistently.
11. **Fail closed versus bounded cached decisions.** Immediate denial during dependency failure minimizes unauthorized access but can halt critical analysis. Explicitly bounded caches can preserve low-risk availability while increasing revocation exposure. Never improvise fail-open behavior.
12. **Detailed versus minimized decision logs.** Rich inputs aid replay and investigation but can create a sensitive shadow dataset. Store stable references, versions and reason codes where possible; protect any necessary values.

## Failure Modes and Misconceptions

1. **“Authenticated means authorized.”** Authentication supplies identity evidence only.
2. **“The analyst role can read analytics.”** A broad label omits resource, purpose, row, column, time, destination, and explicit denies.
3. **“The OAuth scope is the data grant.”** Scope can permit attempting an API action without granting every underlying object or row.
4. **“Network membership is trust.”** Location is at most one contextual signal; it is not resource authority.
5. **“Table ownership is harmless administration.”** Owners or powerful administrators may bypass ordinary policies and must be inventoried and separated.
6. **“A view secures its base table.”** The view helps only when direct and alternate base access is denied.
7. **“Row filters cannot leak hidden rows.”** Counts, timing, errors, joins, repeated queries, and small groups can disclose information.
8. **“Masking removes sensitivity.”** A mask changes representation; linkage, inference, predicates, source access, and obligations can remain.
9. **“If a column is not selected, it is unused.”** Filters, joins, orderings, functions, groups, models, and errors can depend on it.
10. **“Policy tags follow every copy.”** Copy, replace, export, replication, or tool conversion may drop or change enforcement metadata.
11. **“The dashboard owns authorization.”** Its shared service identity, cache, warehouse query, drill-through, export, and API all need controls.
12. **“One service account simplifies notebooks.”** It destroys attribution and gives every user the union of its authority unless delegated enforcement is preserved.
13. **“Purpose is whatever the user types.”** Self-declaration requires supporting project, contract, approval, and monitoring evidence.
14. **“Approval equals access.”** Provisioning may fail, overgrant, target the wrong scope, or omit an enforcement point.
15. **“A temporary ticket creates temporary privilege.”** The entitlement itself must activate and expire automatically.
16. **“No query log means no use.”** Logging may be incomplete; direct storage, caches, exports, and derived products need evidence too.
17. **“No recent use means safe automatic removal.”** Rare on-call or regulatory duties require contextual review, though inactivity is valuable evidence.
18. **“Review direct grants only.”** Nested groups, hierarchy, ownership, delegation, bypass roles, links, and cached authority determine effective access.
19. **“Deny and error are operationally identical.”** Both should prevent the effect, but remediation and incident signals differ.
20. **“Fail open preserves availability.”** It converts control-plane failure into exposure; any bounded continuity behavior must be explicit and risk-scoped.
21. **“Policy is current because the repository changed.”** Every PDP/PEP needs activation state and revision reconciliation.
22. **“A cached permit is valid until TTL.”** Revocation and relevant state changes may require invalidation sooner than generic TTL.
23. **“Revoking the person ends access.”** Sessions, tokens, scheduled workloads, shares, extracts, caches, and derivatives can survive.
24. **“Exports are ordinary reads.”** They create portable resources with destination, recipient, retention, and onward-sharing risk.
25. **“Aggregates are anonymous.”** Small groups, differencing, linkage, outliers, and auxiliary information can defeat this assumption.
26. **“Separate tables solve all policy.”** Isolation helps but copies still need lifecycle, purpose, export, and synchronization controls.
27. **“More denies prove better security.”** Denials may reveal broken policy, attack, bad usability, or false positives; outcomes and context matter.
28. **“Decision logs may contain everything.”** Policy inputs and query context can be highly sensitive and require minimization.
29. **“Break-glass should be unrestricted.”** Emergency access must be narrower, shorter, more observable, and independently reviewed.
30. **“Technical authorization proves compliance.”** Qualified authorities determine applicable obligations; controls provide scoped evidence, not universal legal conclusions.

## Worked Examples

### Example 1

**Situation.** Lina belongs to `analyst`, requests customer product G42 for churn analysis, has current training, and is assigned to region EU. Product policy denies raw contact fields and export.

**Reasoning.** Role supplies coarse query eligibility. The exact product generation and purpose match; training and region are authoritative and current. The PDP returns permit with `region=EU`, allowed columns excluding raw contacts, a contact mask for an approved coarse value, `export=false`, expiry, policy revision, and decision ID. The warehouse PEP applies the row predicate before aggregation and column policy before result delivery.

**Conclusion.** Lina may execute only the constrained analytical query; she does not receive generic read, unmask, or export authority.

### Example 2

**Situation.** Omar has the same analyst role and purpose, but the learning system that supplies required training status times out.

**Reasoning.** Absence of a required attribute is not `training=false`, and it is not permission. The PDP returns indeterminate. The PEP denies the query while operational telemetry distinguishes attribute failure from policy rejection. A bounded low-risk continuity rule could exist, but none applies to this sensitive product.

**Conclusion.** The effect is prevented safely, and responders repair the evidence path instead of adding an emergency broad allow.

### Example 3

**Situation.** A team exposes an authorized regional view but all analysts retain `SELECT` on its base table.

**Reasoning.** The view's PEP shapes only queries that use it. Direct table queries bypass its filter, so path completeness is false. Removing base privileges, constraining storage/replica paths, and testing both allowed view access and denied base access restores defense. An administrator bypass remains separately inventoried.

**Conclusion.** A secure view is not a security boundary while the unfiltered source remains reachable.

### Example 4

**Situation.** A BI dashboard executes as a shared privileged service account and caches results only by dashboard ID.

**Reasoning.** Per-viewer policy never reaches the warehouse; the service obtains the union of rows and columns. The first privileged result populates a cache reused for restricted viewers. Either the dashboard must delegate verified viewer context through the query PEP and partition cache keys by authorization context, or it must publish a single pre-governed audience-specific artifact with its own access policy.

**Conclusion.** UI login cannot repair a privileged shared query identity and cross-context cache.

### Example 5

**Situation.** A clinical researcher may see counts for cohorts of at least ten people. They issue counts for “all eligible” and “all eligible except Alice.”

**Reasoning.** Each query independently satisfies the minimum group threshold, yet their difference reveals Alice's contribution. Ordinary row access and group size do not account for query history. The design needs bounded query templates, overlap/differencing analysis, contribution controls, privacy budgets where suitable, or reviewed release—not a claim that threshold ten guarantees anonymity.

**Conclusion.** Inference is a sequence property; per-query authorization alone is insufficient.

### Example 6

**Situation.** An engineer receives a two-hour JIT grant to diagnose a failed protected pipeline, then starts a scheduled notebook that will run nightly.

**Reasoning.** The interactive grant permits diagnosis during its interval; it does not create perpetual workload authority. Scheduling is a separate action. The job needs an owned workload identity, declared inputs/output/purpose, its own bounded entitlement and expiry. When the human grant expires, sessions and cached permits are invalidated; the unapproved schedule is disabled.

**Conclusion.** A temporary interactive permit cannot be laundered into standing automation.

### Example 7

**Situation.** A product is reclassified from internal to restricted after a sensitive join is discovered.

**Reasoning.** The control plane identifies current source grants, views, row/column policies, semantic models, dashboards, extracts, shares, scheduled jobs, result caches, and downstream products through catalog and lineage. New high-risk reads are held until policy revision activates. Existing grants are re-evaluated; derivatives are reclassified or contained; consumers receive actions; decision and propagation receipts are reconciled.

**Conclusion.** Reclassification is an enforcement and derivative-remediation event, not merely a catalog tag edit.

### Example 8

**Situation.** A region transfer removes Mei from group `north`, yet she can still query northern data.

**Reasoning.** Effective-access explanation finds a second path: nested group `forecast-admin`, plus an active session with a cached decision. Direct-group review missed both. The response removes the inappropriate nested membership, invalidates session/cache, tests all query paths, and records latency from authoritative transfer to enforcement. It also assesses any derivatives made after transfer.

**Conclusion.** Revocation must eliminate every effective path, not only the expected direct grant.

### Example 9

**Situation.** An on-call responder invokes break-glass during an incident affecting a restricted financial product.

**Reasoning.** Strong reauthentication, incident ID, responder eligibility, exact tables/actions, 30-minute expiry, and independent notification are checked. The emergency role cannot change audit configuration or grant itself onward. Queries and exports receive decision IDs; after containment, sessions and credentials are revoked and a reviewer checks necessity, scope, output handling, and suspicious use.

**Conclusion.** Emergency access remains bounded and observable even when ordinary approval latency is unacceptable.

### Example 10

**Situation.** Before deploying policy B20, engineers compare it with B19 over recorded, synthetic, and adversarial decisions.

**Reasoning.** Simulation finds 1,204 unchanged permits, 31 intended denials for expired vendors, eight intended new permits, and two unexpected permits caused by a missing-classification fallback. The fallback is changed from allow to indeterminate, unit and path tests pass, a canary PEP activates B20, decision outcomes are compared, and only then is rollout expanded. Rollback remains available.

**Conclusion.** Policy-as-code needs semantic diffing and enforcement rollout evidence, not only syntax validation.

## Cross-Program Connections

- [API-034](../../28-api-and-service-engineering/modules/034-authorization-checks.md) owns request-level subject/action/object enforcement; analytical authorization adds query semantics, row/column constraints, result artifacts, and inference.
- [API-046](../../28-api-and-service-engineering/modules/046-object-level-authorization.md) supplies exact-object, tenant, batch, cache, and TOCTOU reasoning that also applies to datasets, jobs, dashboards, and extracts.
- Security Engineering modules [SEC-028](../../25-security-engineering/ROADMAP.md), SEC-029, and SEC-030 own general RBAC, ABAC, and resource/action authorization models; this chapter applies them to analytical planes rather than replacing those foundations.
- [DE-081](081-technical-operational-and-business-metadata.md), [DE-082](082-dataset-and-column-lineage.md), and [DE-083](083-data-catalogs.md) supply authoritative attributes, derivative reachability, policy discovery, and workflows.
- [DE-084](084-ownership-and-stewardship.md) determines who may approve or review access; ownership itself never implies data access.
- [DE-085](085-classification-and-sensitive-data.md) supplies contextual sensitivity and propagation evidence; authorization consumes classification but does not establish it.
- [DE-087](../ROADMAP.md) examines transformations used by column and release policy, including their residual linkability and inference risk.

## References

- National Institute of Standards and Technology, *Guide to Attribute Based Access Control (ABAC) Definition and Considerations*, SP 800-162, updated 2019. <https://csrc.nist.gov/pubs/sp/800/162/upd2/final>
- National Institute of Standards and Technology, *Zero Trust Architecture*, SP 800-207, 2020. <https://csrc.nist.gov/pubs/sp/800/207/final>
- National Institute of Standards and Technology, *A Zero Trust Architecture Model for Access Control in Cloud-Native Applications in Multi-Cloud Environments*, SP 800-207A, 2023. <https://csrc.nist.gov/pubs/sp/800/207/a/final>
- National Institute of Standards and Technology, *Security and Privacy Controls for Information Systems and Organizations*, SP 800-53 Rev. 5, updated 2020. <https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final>
- National Institute of Standards and Technology, “Role Based Access Control,” reference-model and standard history. <https://csrc.nist.gov/projects/role-based-access-control/faqs>
- Open Policy Agent, “How to Deploy OPA,” policy decision and enforcement architecture, current documentation. <https://www.openpolicyagent.org/docs/deploy>
- Open Policy Agent, “Decision Logs,” decision identifiers, bundle metadata, masking, and delivery behavior, current documentation. <https://www.openpolicyagent.org/docs/management-decision-logs>
- PostgreSQL Global Development Group, “Row Security Policies,” PostgreSQL 18 current documentation. <https://www.postgresql.org/docs/current/ddl-rowsecurity.html>
- Google Cloud, “Introduction to BigQuery Row-Level Security,” current documentation. <https://cloud.google.com/bigquery/docs/row-level-security-intro>
- Google Cloud, “Introduction to Column-Level Access Control,” current documentation. <https://cloud.google.com/bigquery/docs/column-level-security-intro>
- Google Cloud, “Using Row-Level Security with Other BigQuery Features,” current documentation. <https://cloud.google.com/bigquery/docs/using-row-level-security-with-features>
- Snowflake, “Understanding Row Access Policies,” current documentation. <https://docs.snowflake.com/en/user-guide/security-row-intro>
- Snowflake, “Manage Data Protection Policies in Snowsight,” current documentation. <https://docs.snowflake.com/en/user-guide/data-protection-policies-snowsight>
- Apache Ranger, “Apache Ranger Policy Model,” authorization, deny, masking, and row-filter concepts, current project documentation. <https://ranger.apache.org/blogs/policy_model.html>
- OWASP Foundation, “Authorization Cheat Sheet,” deny-by-default, per-request validation, testing, and logging guidance, current documentation. <https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html>

## Exercises

### Exercise 1

For a decision receipt, distinguish the minimum meaning of actor, effective subject, workload/client, action, resource generation, context, policy revision, outcome, constraints, expiry, and enforcement point. Explain why a direct grant list cannot replace this receipt.

### Exercise 2

Policy permits analysts with current training to query their assigned region for purpose `quality_review`, denies any product under investigation hold, masks `email`, and forbids export. Trace decisions for: (a) trained analyst in the correct region; (b) same analyst requesting export; (c) correct role with unknown training status; and (d) administrator role while the product is under hold.

### Exercise 3

A dashboard correctly filters rows by viewer region, yet users in region A see a cached total produced earlier by a region B administrator. Diagnose the violated invariants and propose an implementation and test strategy that preserves both security and comprehensible metric semantics.

### Exercise 4

Compare authorized views, native row/column policy, and physical dataset separation for sharing a restricted product with an external research partner. Design a justified hybrid, including base access, workload identity, joins, exports, derivatives, audit, expiry, and revocation.

### Exercise 5

A merger transfers 400 analysts, 60 service accounts, 90 dashboards, and 30 scheduled pipelines between domains while two products become more sensitive. Design an access migration and verification process that avoids both blanket carryover and uncontrolled outage. Include effective-access analysis, staged policy rollout, exceptions, artifact remediation, and success measures.

## Answers to the Exercises

### Answer 1

The **actor** is the authenticated human or service initiating the operation. The **effective subject** is the identity on whose behalf it acts; keeping both exposes impersonation or delegation. The **workload/client** is the notebook, BI service, scheduler, or application executing the request and constrains audience and channel. The **action** names the semantic effect, such as query, unmask, join, export, or grant. The **resource generation** identifies the exact product/table/field/version rather than a mutable name. **Context** holds governed purpose, tenant, environment, time, region, and other relevant facts with source versions. The **policy revision** identifies the evaluated rules. **Outcome** is permit, deny, or indeterminate; **constraints** specify allowed rows, columns, transformations, query shapes, destinations, logging, or rates. **Expiry** bounds reuse, and the **enforcement point** identifies the component that prevented or performed the effect.

A direct grant list omits role hierarchy, nested groups, relationships, explicit denies, attributes, policy revision, current context, cached authority, constraints, and actual enforcement. It can help explain one entitlement source but cannot prove why one exact observation was authorized or that a PEP enforced the result.

### Answer 2

(a) The trained analyst has role eligibility, current training, matching region, correct purpose, and no hold. The decision is permit with a region row predicate, `email` mask, and `export=false`; the PEP must apply every constraint. (b) Export is a distinct forbidden action, so the decision is deny even though query is permitted. (c) Unknown required training evidence yields indeterminate, which the PEP treats as no permission while telemetry routes the evidence failure. (d) The investigation hold is an overriding deny. An administrator role does not bypass it unless policy explicitly defines a separately governed emergency action; ordinary query is denied.

The trace demonstrates conjunction and precedence. Role alone never supplies the whole decision, and operational errors remain distinguishable from policy denials even though neither permits the effect.

### Answer 3

The row PEP may be correct for live queries, but the cache violates decision/effect binding and path completeness. Its key ignores authorization context, and a privileged result became an ungoverned derivative. Metric semantics are also wrong because region A receives a total over region B's authorized subset.

One design executes with verified viewer context, applies row policy before aggregation, and keys or partitions cached results by all policy-relevant dimensions plus product generation, semantic definition, and policy revision. Another publishes separately governed region artifacts, each with explicit audience and refresh identity. Base access remains protected in both designs. Tests should query identical SQL as multiple regions, administrators, missing-attribute identities, and transferred users; assert result differences and denial; attempt cache warming in every order; test direct warehouse and export paths; change policy and membership; and verify invalidation. UI labels should state the metric is computed over the viewer's authorized population without exposing hidden counts.

### Answer 4

Authorized views provide a clear partner contract and convenient projection, but they fail if base access exists and can proliferate. Native row/column policy gives defense across ordinary queries and handles changing partner mappings, but engine-specific limitations, owner bypass, copy behavior, and performance require testing. Physical separation gives the strongest boundary against inference about table presence or accidental policy bypass, at the cost of copying, synchronization, retention, correction, and deletion complexity.

A reasonable hybrid places the approved partner cohort and columns in a physically separate governed distribution for a high-risk external boundary, then applies native row/column and export policy inside it for partner projects and roles. The partner uses a dedicated federated human/workload identity; base source and unrelated storage are denied. Only approved joins and minimum-group/release rules are available. Exports require a distinct action, destination, encryption, recipient, expiry, and receipt. Every derivative inherits partner scope, owner, classification, retention, and onward-sharing prohibition. Query/access history and minimized decision receipts are reviewed. The contract end automatically disables identity/grants/jobs/shares, removes or quarantines extracts under retention rules, validates deletion, and tests that direct, view, storage, cache, and recovery paths deny access.

### Answer 5

First inventory stable principals, teams, workloads, products/generations, actions, classifications, owners, policies, direct/inherited grants, nested groups, role activation, bypass roles, sessions, tokens, dashboards, jobs, caches, extracts, shares, and lineage. Compute effective-access proof paths before and proposed after the merger. Owners and risk authorities define least-privilege target profiles; the two reclassified products default to hold or stricter profiles until eligibility is re-established.

Translate people through new durable groups without automatically copying every exception. Rebind each service account, dashboard, and pipeline to a named owner, purpose, exact inputs/outputs, environment, expiry, and workload identity. Simulate old/new policy over recorded and adversarial requests; investigate unexpected permits, denies, and indeterminate results. Deploy policy to canary PDPs/PEPs, attest revision activation, validate allowed business-critical paths and denied cross-domain/base/export routes, then expand in reversible cohorts. Time-bounded reviewed exceptions protect genuinely critical work; they never edit away the intended target policy.

Use lineage to reclassify or contain materialized outputs, caches, shares, notebook artifacts, and scheduled refreshes from the newly sensitive products. Revoke obsolete groups, grants, sessions, tokens, cached decisions and old jobs; independently test the removed paths. Measure resources and paths inventoried, policy activation convergence, unexpected effective-access delta, critical workflow success, denial/indeterminate errors, exception count/age, orphan workload count, derivative remediation coverage, revocation latency, cross-domain escape tests, and post-migration incidents. Completion requires enforced and observed convergence, not merely closed migration tickets.
