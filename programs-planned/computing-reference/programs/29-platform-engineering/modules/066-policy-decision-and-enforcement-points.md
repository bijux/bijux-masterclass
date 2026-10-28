---
module_id: PLAT-066
program: Platform Engineering
level: 2
module_number: 66
title: Policy Decision and Enforcement Points
status: complete
last_verified: 2026-09-02
---

# Policy Decision and Enforcement Points

## One-Page Review

### Governing question

How should a platform administer, evaluate, distribute, enforce, observe, and evolve policy so every protected action is mediated with current trustworthy context and no bypass, cache, obligation, or failure mode silently changes the intended decision?

### Essential definitions

- A **policy administration point (PAP)** governs policy authorship, review, testing, versioning, signing, distribution, rollback, and retirement.
- A **policy information point (PIP)** supplies subject, resource, action, relationship, and environment facts with authority, revision, freshness, and classification.
- A **policy decision point (PDP)** evaluates a named policy against a typed request and evidence to produce a decision.
- A **policy enforcement point (PEP)** intercepts a protected action, obtains or validates a decision, fulfills mandatory obligations, and permits or prevents the effect.
- A **decision** is a typed result such as permit, deny, not-applicable, or indeterminate, plus policy/input revisions, reason codes, obligations, and decision identity.
- An **obligation** is a mandatory action the PEP must understand and fulfill for the associated decision to be valid; **advice** is optional guidance.
- **complete mediation** means every protected attempt passes through an effective PEP at the correct time and granularity.
- **default deny** means absence, error, unknown policy, or unmatched protected action does not become permission unless an explicit availability policy says otherwise.
- **policy bundle** is a versioned, integrity-protected set of policies and supporting data distributed to evaluators.
- **decision cache** stores a result keyed by all decision-relevant inputs and revisions for a bounded validity period.
- **shadow evaluation** computes and records a candidate decision without allowing it to control the protected effect.
- **authorization freshness** is the acceptable age and causal position of facts and policy for the action's consequence.

### Central model, mechanism, or theorem

Let a decision request be

$$
q=(p,a,r,x,t),
$$

where $p$ is principal, $a$ action, $r$ resource, $x$ contextual evidence, and $t$ decision time. A PDP evaluates named policy under policy revision $b$ and authoritative evidence revisions $u$:

$$
D(q,b,u)=(z,o,c,d),
$$

where $z$ is outcome, $o$ mandatory obligations, $c$ reason/evidence metadata, and $d$ unique decision ID. Security of the path requires more than a correct $D$: every protected effect path must pass a PEP, the PEP must construct the intended $q$, validate freshness and response identity, deny on unsafe error, fulfill every obligation, and bind permit to the same action/resource state. If any path bypasses mediation, or if a PEP permits without satisfying an obligation, the system does not enforce the policy globally.

### Critical invariants

- Authentication establishes a principal; authorization separately evaluates action, resource, relationship, and context.
- Every protected path—including internal, asynchronous, batch, administrative, recovery, and direct-provider paths—has an identified PEP or is structurally unreachable.
- PEPs ask named, versioned decisions using canonical action/resource identities and typed, bounded input schemas.
- PIPs expose authoritative revision, observation time, freshness, sensitivity, and unavailable/unknown states; untrusted labels do not silently become grants.
- PDP output distinguishes deny, not-applicable, indeterminate, transport error, and malformed response; the PEP defines safe handling.
- A permit is useful only if it remains bound to the intended principal, action, resource state, policy revision, evidence revisions, and validity interval.
- Mandatory obligations are typed, bounded, idempotent where needed, and fail closed if the PEP cannot fulfill them.
- Distributed PDPs activate verified complete bundles atomically and expose active revision; partial or unknown policy never masquerades as a valid decision.
- Decision caches include every relevant input/revision and cannot outlive revocation or change tolerance for the action.
- List, search, graph, watch, export, and bulk operations enforce authorization without leaking hidden existence or applying one sample decision to unlike items.
- Policy and decision logs minimize or mask sensitive context, resist tampering, and connect decision to enforcement outcome.
- Shadow results never alter production enforcement; promotion requires semantic, safety, coverage, and performance evidence.

### Common failures

Authentication mistaken for authorization; one gateway PEP with bypassing internal paths; user-controlled owner or tenant labels as grant facts; ambiguous resource IDs; policy query chosen by caller; permit-by-default on undefined; fail-open copied across all actions; stale membership cache after revocation; decision cache missing policy/resource revision; PDP permit enforced after the resource changes; list endpoint filtering after counts; one decision reused for an entire heterogeneous batch; obligations ignored; response headers trusted without bounds; unsigned or partially loaded bundles; centralized PDP as latency/availability bottleneck; local PDPs with unknown versions; decision logs containing tokens or personal data; shadow denial treated as enforcement; and operator bypass without policy or audit.

### Compact example

A developer requests `environment.deploy` on `env:payments/prod`. The API PEP authenticates workload and user, canonicalizes action/resource, and asks `platform/deploy` with tenant, environment, change approval, group membership revision, resource version, and current incident mode. Local PDP revision `bundle-417` returns permit for 30 seconds with obligations `record_change(change-82)` and `inject_actor(principal-9)`. The PEP understands and completes both before dispatch, attaches decision ID, and binds the provider command to resource version 12. A replay after membership revocation misses cache because directory revision changed. Direct provider credentials are unavailable to the caller, so the API cannot be bypassed. Search uses per-result filtering before counts. Decision logs mask approval details.

### Connections

This module builds on platform API authorization in [PLAT-061](061-platform-api-layers.md), sensitive portal composition in [PLAT-062](062-developer-portal-architecture.md), catalog authority in [PLAT-063](063-software-catalogs.md), ownership versus permission in [PLAT-064](064-ownership-and-metadata.md), and authorized workflow actions in [PLAT-065](065-workflow-and-orchestration-layers.md). PLAT-074 through PLAT-079 deepen identity, workload identity, policy as code, admission, supply-chain policy, and audit.

## Governing Question

How can a platform make policy decisions consistent and reusable while ensuring that every real effect is intercepted, evaluated with trustworthy current facts, and enforced correctly across APIs, controllers, workflows, portals, clusters, and provider boundaries?

Policy engines solve evaluation, not protection by themselves. A perfectly evaluated denial has no effect if a direct API route bypasses the check, if an asynchronous worker does not carry the principal, if a list endpoint leaks filtered resources, or if the enforcer ignores a required obligation.

Conversely, embedding policy logic independently in every service creates divergence, weak audit, and slow policy evolution. The architecture must centralize semantics and governance without requiring one remote runtime call for every action or creating a global availability dependency.

The durable abstraction is a decision protocol plus enforcement contract: typed inputs, authoritative facts, versioned policy, explicit outcomes, obligations, error behavior, coverage, evidence, and compatibility.

## Why This Matters

Platforms concentrate privilege. They vend accounts, identities, networks, secrets, runtimes, databases, and deployment paths. A small authorization error can cross tenants or environments and create effects that later cleanup cannot fully reverse.

Self-service requires consistency. Developers should encounter the same policy whether they use portal, CLI, API, template, workflow, or controller. If one surface denies while another bypasses, users learn to route around controls and the platform loses credibility.

Authorization changes rapidly. People leave groups, incidents trigger freezes, resources change classification, approvals expire, policies roll back, and emergency modes begin or end. Caching and distributed evaluators must have explicit staleness and causal semantics.

Policy can also damage availability. A remote PDP outage, malformed bundle, slow PIP, or expensive rule can block every request. Fail-open and fail-closed are consequence-specific decisions, not slogans. Read-only public metadata and production secret access have different wrong-deny and wrong-allow costs.

Evidence matters after the fact. Operators need to know which policy and facts produced a decision, whether the PEP enforced it, and whether an obligation succeeded—without storing secrets or excessive personal data in logs.

## Prerequisites and Retrieval

Retrieve authentication and identity, RBAC and ABAC, relationship-based access control, capabilities, least privilege, complete mediation, default deny, separation of duty, policy languages, distributed caching, consistency and revocation, API gateways and service meshes, admission control, controllers and workflows, schema/version evolution, multi-tenancy, audit, privacy, cryptographic integrity, canary/shadow deployment, and fault injection.

You should distinguish authentication from authorization; policy administration from evaluation; PDP from PEP; PIP from arbitrary metadata; permit from successful enforcement; deny from not-applicable or indeterminate; obligation from advice; action identity from HTTP method; resource identity from path string; request-time authorization from continuing authority; decision cache from attribute cache; policy distribution from policy activation; shadow evaluation from enforcement; decision log from access/effect log; and complete mediation from a high percentage of checked requests.

## Learning Objectives

After completing this module, you should be able to:

1. decompose a platform policy system into administration, information, decision, enforcement, and audit responsibilities;
2. inventory all effect paths and place PEPs at non-bypassable boundaries;
3. design canonical decision requests, outcomes, obligations, evidence, and error handling;
4. select authoritative attributes and manage freshness, revocation, conflicts, and unknown states;
5. distribute and activate versioned policy safely across central, sidecar, embedded, and edge PDPs;
6. design cache keys and validity bounds appropriate to consequence and consistency;
7. authorize lists, searches, watches, graphs, batches, workflows, and long-lived sessions without leakage;
8. evolve policy through tests, impact analysis, shadowing, canaries, rollback, and compatibility;
9. observe decisions and enforcement while protecting sensitive inputs; and
10. test bypass, confused deputy, stale data, bundle failure, PEP defects, and disaster recovery.

## Core Exposition

### Begin with protected actions and effects

Inventory actions before choosing a policy engine: view catalog entity, list environments, create account, deploy workload, read secret, approve exception, cancel workflow, change quota, impersonate user, or invoke provider recovery. Give each action stable domain semantics.

HTTP verb and path are transport details. `POST /operations` may mean deploy, rotate, restore, or delete depending on payload. The PEP should map a validated request to a canonical action and resource identity rather than asking policy to reinterpret arbitrary raw traffic.

Classify consequence, latency budget, availability need, revocation tolerance, and obligation. A public read may tolerate a short stale cache; privilege grant or secret read may require current evidence and fail closed.

List every channel capable of the effect: public API, internal API, message consumer, scheduled job, controller, workflow activity, administrative tool, database procedure, cloud console, break-glass path, and recovery automation. Unknown paths are policy gaps.

### Separate authentication and authorization

Authentication proves or establishes an actor identity under an assurance level. It does not say that actor may perform the requested action. A valid token can belong to the wrong tenant, environment, role, device posture, or workload.

Build a principal model that distinguishes human, workload, service, automation, support, and delegated identities. Record issuer, subject, audience, authentication time, assurance, delegation chain, and tenant where relevant.

Do not trust caller-supplied identity headers unless a non-bypassable authenticated proxy strips and reconstructs them. Bind downstream identity assertions cryptographically or through a protected channel.

Authorization must evaluate the effective principal and delegation. A platform worker using broad provider credentials acts as a deputy; it must preserve the initiator, requested action, tenant, and approved scope so its capability cannot be abused.

### Define PAP, PIP, PDP, and PEP responsibilities

The PAP governs policy lifecycle: repositories or authoring UI, schema, ownership, review, tests, signing, bundle construction, distribution, rollout, rollback, deprecation, and emergency change. A source repository alone is not a complete administration plane.

PIPs provide decision facts. Identity directory owns membership; resource control plane owns tenant and lifecycle; approval system owns current approval; incident system owns freeze mode; catalog may provide low-consequence context. Every PIP contract states authority, revision, observation time, freshness, missing/error semantics, and sensitivity.

The PDP evaluates a named decision using supplied or fetched facts and active policy. It returns a typed result; it does not generally perform the protected action. Avoid hidden network I/O from individual rules when it destroys determinism, latency bounds, or provenance.

The PEP intercepts the action, constructs the request, calls or embeds the PDP, interprets outcomes, fulfills obligations, prevents bypass, and records enforcement. It remains responsible when the PDP is unavailable or returns malformed/unknown output.

### Design a stable decision contract

Define principal, action, resource, relationships, environment, request metadata, and evidence revisions in a versioned input schema. Bound size and cardinality. Normalize resource IDs before evaluation and reject ambiguous or cross-tenant references.

Use named decisions with owned semantics, such as `platform/environment/deploy`, instead of letting clients query arbitrary policy paths. The PEP selects the decision by protected operation, not a user parameter.

Return more than Boolean. Outcomes commonly distinguish permit, deny, not-applicable, and indeterminate. Include decision ID, policy/bundle revision, relevant evidence revisions, validity or recheck condition, reason codes safe for the audience, and typed obligations.

Keep internal explanation separate from user-facing denial. Detailed policy structure, group membership, or hidden resource existence can leak through error messages. Give operators an authorized diagnostic path keyed by decision ID.

### Make enforcement semantics explicit

For permit, the PEP validates that the response belongs to its request and expected PDP, is fresh, uses a compatible schema, and carries an active policy revision. Then it fulfills all mandatory permit obligations before or atomically with dispatch as defined.

For deny, the PEP prevents the effect and returns a bounded safe error. For not-applicable or indeterminate, protected actions normally deny unless an explicit higher-level policy specifies otherwise. A transport error is not a permit response.

Obligations might require recording change evidence, adding a tenant constraint, reducing granted duration, masking fields, obtaining a secondary approval, or attaching a principal identity to a downstream command. If the PEP does not recognize or cannot fulfill an obligation, it must not treat the decision as satisfied.

Advice can guide UI or remediation but does not determine enforcement. Keep it typed and bounded so an evaluator cannot inject arbitrary headers, URLs, or commands into a more privileged PEP.

### Achieve complete mediation

A PEP must sit where the protected effect cannot occur without it. An API gateway protects traffic passing through the gateway; it does not cover direct service addresses, background workers, database consoles, or provider credentials.

Use network and identity architecture to make bypass structurally difficult: private backends, mutually authenticated service paths, scoped provider roles available only to enforcing workers, admission controls, database permissions, and audited break-glass mechanisms.

Place checks at the layer with semantic context. A gateway can deny coarse routes; the application may know resource ownership and field-level action; a provider adapter may be the final place to constrain cloud scope. Defense in depth is useful when contracts agree and failure behavior is explicit.

Continuously discover bypasses through architecture inventory, credential analysis, traffic observation, mutation testing, and attempts from untrusted networks or identities. “All known routes checked” is evidence, not a permanent fact.

### Govern attributes and relationships

An attribute is trustworthy only relative to an authority and observation. User-controlled repository labels can describe intent but should not grant production privilege unless a stronger process validates them.

Define subject attributes, resource attributes, action attributes, relationships, and environment conditions with schemas and ownership. Separate missing, unknown, stale, conflict, and unauthorized-to-read; a default value can invert policy.

Relationship-based models express facts such as user member of group, group owner of project, project parent of resource. Define tuple writers, consistency, deletion, caveats, recursion limits, and tenant boundaries. Ownership still does not imply every action.

Minimize PIP fetching on the synchronous path. Precompute or distribute governed facts where latency requires it, but preserve revision and revocation behavior. The PDP should know whether input is current enough for the named decision.

### Compose policies predictably

Platforms combine organization, tenant, environment, capability, resource, and exception policies. Define precedence and combining algorithms. Deny-overrides is conservative but can make local exceptions impossible; permit-overrides can make one broad rule defeat a guardrail.

Separate eligibility, prohibitions, and obligations. For example: caller belongs to deployment group; resource is not frozen; change approval matches input; permitted duration is at most one hour; record audit evidence. A single opaque Boolean hides which layer failed.

Exceptions are policies with subject, resource/action scope, issuer, reason, effective interval, approval, monitoring, and expiry. Never implement them as undocumented branches or permanent allow lists.

Prevent policy recursion and circular dependencies. An authorization decision should not need an action that itself requires the same unresolved decision. Bootstrap administration and recovery rights narrowly and explicitly.

### Choose PDP placement deliberately

A centralized network PDP simplifies rollout and audit but adds latency and a shared availability dependency. Regional services reduce distance but require replication. Sidecars or node agents keep decisions near PEPs and tolerate network partitions, while increasing distribution and version-observation complexity.

Embedded libraries or compiled policy can reach low latency and reduce runtime dependencies, but every host must activate and report the correct version. Language/runtime divergence and update lag become risks.

Use logically centralized policy administration with physically distributed evaluation when appropriate. Define maximum version skew, activation readiness, rollback, and what the PEP does when its local evaluator lacks the required bundle.

Do not assume local means safe. Compromising the application may compromise its embedded PEP and evaluator. Stronger isolation may place enforcement in a proxy, kernel, admission controller, or provider boundary.

### Distribute policy bundles safely

Build immutable bundles with policy, supporting static data, schema/version, manifest, revision, compatibility range, issuer, and integrity signature. Validate size, syntax, types, tests, and dependency closure before publication.

Download into a staging area, authenticate source, verify digest/signature, compile or initialize, run readiness probes and smoke decisions, then atomically activate the complete bundle. Partial files must never become active policy.

Report active and downloaded revisions from every evaluator. Alert on lag, verification failure, rejected bundle, unknown revision, and divergent decisions. Retain last-known-good only under a defined policy; an evaluator starting with no valid bundle is not ready.

Rollback is a new governed activation with audit. Ensure older policy is compatible with current decision input and PIP schemas. Emergency rollback cannot resurrect deleted attributes or incompatible obligations without handling.

### Design failure behavior per action

Fail closed reduces wrong permits but can deny legitimate work during evaluator outage. Fail open preserves availability but can cross security and tenant boundaries. Decide using consequence and credible failure modes.

For high-risk mutations, secret reads, privilege grants, and cross-tenant access, deny on unavailable, malformed, unknown, or stale critical evidence. Provide a separate tightly governed break-glass path rather than a hidden automatic allow.

Some low-risk public or cached reads can use a previously valid result for a bounded interval. Label degraded enforcement, measure it, and ensure the cache was valid for the exact resource/action/principal context.

The PEP owns this behavior because an unavailable PDP cannot answer the question. Test policy absence, startup race, timeout, overload, partial bundle, signature failure, and PIP outage independently.

### Cache decisions with revocation in mind

A cache key includes named decision, input schema version, principal/delegation, action, canonical resource and version, relevant context, policy revision, and evidence revisions or validity token. Omitting a relevant input turns another request's permit into authority.

TTL must be no longer than tolerated staleness for every relevant fact and policy. Group removal, resource tenant move, incident freeze, approval expiry, or policy revocation can require immediate invalidation or causal consistency stronger than TTL.

Negative caching can reduce load but may delay newly granted access. Use separate permit and deny validity policies. Do not cache indeterminate or malformed output as a normal denial without observability, or an outage becomes an unexplained long lockout.

For long-lived streams or sessions, authorize establishment and define reauthorization triggers: time, policy revision, membership change, resource change, privilege escalation, or each consequential message.

### Close time-of-check/time-of-use gaps

Between decision and effect, the resource, membership, approval, or policy can change. Include resource version or precondition in the provider command when possible. The effect authority rejects if the state no longer matches.

Short validity reduces but does not eliminate races. Bind approvals and permits to immutable request digests. Perform final checks near the effect. Use transactions or conditional writes when decision-relevant state and effect share an authority.

For queued workflows, a start permit does not automatically authorize a later activity. Recheck consequential steps using current principal/delegation and resource context. Record which checks apply to intent, scheduling, and execution.

Revocation cannot always undo completed effects. Policy design must distinguish preventing future action, terminating continuing access, and compensating past changes.

### Authorize collections and bulk operations

List and search are not a single resource check. Filter unauthorized items before ranking, counts, facets, pagination tokens, autocomplete, graph traversal, and aggregation. Otherwise existence leaks even when detail fetch denies.

Options include query-time policy predicates, precomputed authorization indexes, batch/multiple-decision APIs, or per-item checks with bounded fan-out. Each must preserve current revisions and tenant separation.

Bulk mutation needs a decision for the set and often for each item. Atomic “all or none,” best-effort per item, and stop-on-denial have different semantics. Return item-level safe results without disclosing hidden objects.

Watches and subscriptions require authorization at creation and upon each emitted item or relevant policy/resource change. A long-lived permit must not stream newly restricted data forever.

### Treat obligations as part of the protocol

Register obligation types and PEP capabilities. Define ordering, failure, idempotency, timeout, and evidence. An evaluator should not return an obligation to a PEP version that cannot fulfill it.

Pre-effect obligations must complete before dispatch. In-effect obligations should be enforced atomically or at the final boundary. Post-effect audit obligations need durable delivery, but inability to record required evidence may mean the action cannot proceed.

Avoid overloading headers as arbitrary obligation transport. Allowlist names and values, bound sizes, prevent hop-by-hop ambiguity, and ensure downstream services cannot forge trusted enforcement metadata.

Record obligation result next to decision and effect. A PDP permit plus failed tenant constraint is an enforcement failure, not a successful authorized request.

### Evolve policy with evidence

Policy is executable production behavior. Require ownership, review, static checks, unit/property tests, representative decision fixtures, negative tests, and impact analysis against sampled or safely replayed decision inputs.

Shadow evaluation compares candidate and active policy but never controls effects. Classify permit-to-deny, deny-to-permit, obligation, explanation, latency, and error changes. Sample carefully and protect captured inputs.

Canary candidate bundles to bounded evaluators, tenants, or actions only when enforcement semantics remain clear. Monitor disagreement and error. Promote an immutable revision; do not mutate bundle contents under one version.

Compatibility covers policy language/runtime, decision input, output/obligations, PIP schemas, and PEP capabilities. Coordinate rollout so no PEP sees an obligation or outcome it cannot interpret.

### Observe decision and enforcement separately

Decision logs include decision ID, named decision, policy revision, evaluator identity, input/evidence revisions or masked digest, outcome, safe reason codes, obligations, latency, and error. They show evaluation, not necessarily effect.

PEP logs record request/effect identity, decision ID, validation, cache use, obligation results, enforcement action, downstream receipt, and final outcome. Correlate without assuming the same timestamp means causality.

Mask tokens, credentials, personal attributes, secret values, request bodies, and sensitive resource names. Apply field classification, minimization, access control, integrity, retention, and deletion to policy telemetry.

Metrics include decision latency/errors by path and revision, permits/denials/indeterminate, bundle lag, cache hit/staleness, obligation failures, bypass attempts, unenforced shadow disagreements, authorization-filter cost, and PEP/PDP coverage.

### Design break-glass and operator paths

Break-glass is an explicit policy path for exceptional conditions, not an unlogged bypass. Require strong identity, narrow action/resource scope, reason, short expiry, approval where possible, notification, enhanced logging, and retrospective review.

Separate recovery of the policy system from authorization of ordinary resources. Bootstrap credentials should be few, hardware- or vault-protected, tested, rotated, and unable to become routine application tokens.

Operator tools call the same or stricter PEPs. Administrative interfaces, database consoles, policy bundle publishers, and impersonation functions deserve more protection, not exemptions.

Audit use and non-use. A never-tested emergency path may fail during an incident; a frequently used one signals broken normal policy or excessive friction.

### Verify, recover, and retire

Test policy semantics and the whole enforcement chain. Mutation-test PEPs to ensure removing or bypassing a check is detected. Attempt direct routes and stolen deputy credentials in controlled environments.

Fault-test missing/old/corrupt bundles, unavailable PIP/PDP, latency, overload, clock skew, inconsistent replicas, cache invalidation loss, obligation failure, and telemetry outage. Verify consequence-specific fail behavior.

Back up policy source, review/audit, bundle artifacts, signing keys or recovery process, distribution state, schema registries, exception records, and PIP authority configuration. Evaluators should reconstruct from verified artifacts.

To retire a decision or PEP, inventory all callers and effect paths, migrate semantics, prove zero calls and zero bypass, revoke credentials/routes, retain historical decoders, and update recovery. Removing the visible gateway check while an old worker remains is not retirement.

## Definitions and Notation

Let $P$ be principals, $A$ actions, $R$ resources, $X$ context/evidence, $B$ policy bundle revisions, $U$ evidence-revision vectors, $O$ obligations, and $Z$ decision outcomes.

A request is $q=(p,a,r,x,t)$. A decision function is $D(q,b,u)=(z,o,c,d)$, where $z$ is outcome, $o$ obligations, $c$ reason/evidence metadata, and $d$ decision identity. The PEP enforcement function $E(q,D,y)$ also receives current effect precondition $y$ and yields enforced or prevented plus evidence.

Let $Paths(a,r)$ be all feasible paths capable of effecting action $a$ on resource $r$. Complete mediation requires every feasible path to include an effective PEP before the irreversible boundary. A checked-request percentage cannot prove this if an unobserved bypass path exists.

For cached decision entry $m$, let $K(m)$ contain all decision-relevant input and revision fields, and let $t_{exp}(m)$ be expiry. Reuse at time $t$ is sound only under the declared model when keys match, $t<t_{exp}(m)$, relevant facts have not invalidated it, and the effect precondition still holds.

Let false permit cost be $L_p$ and false deny cost be $L_d$ for an action class. Fail behavior is a risk-policy choice informed by these losses and outage likelihood; the equation does not reduce security to money or make estimates certain.

## Mechanisms, Invariants, or Proof Structure

### Policy decision and enforcement protocol

1. Inventory protected actions, resources, effects, paths, consequences, deadlines, and revocation tolerances.
2. Define canonical identities and versioned decision input/output/obligation schemas.
3. Assign policy administration, information authority, decision, enforcement, and audit ownership.
4. Place PEPs at non-bypassable semantic/effect boundaries and restrict direct credentials and routes.
5. Supply typed authoritative facts with revisions, freshness, sensitivity, and unknown/error states.
6. Evaluate named policy under an immutable verified bundle and return a traceable typed decision.
7. Validate response identity/version/freshness; apply consequence-specific error behavior.
8. Fulfill mandatory obligations and bind permit to resource state before the effect.
9. Filter collections and continuing streams without leaking hidden existence; reauthorize on change.
10. Distribute bundles atomically, constrain caches, observe active revisions, and preserve revocation.
11. Test semantics, bypass, confused deputy, failures, shadow/canary rollout, rollback, and recovery.
12. Retire decisions, attributes, exceptions, PEPs, and evaluators only after path and consumer disposition.

### Core invariants

- **Identity separation:** authentication facts do not themselves grant actions.
- **Named semantics:** the PEP, not untrusted input, selects a stable decision contract.
- **Complete mediation:** every protected effect path includes effective enforcement.
- **Authoritative context:** grant-relevant facts carry authority, revision, and acceptable freshness.
- **Outcome precision:** permit, deny, not-applicable, indeterminate, and error remain distinct.
- **Obligation completeness:** no permit is enforced if a mandatory obligation is unsupported or fails.
- **Bundle atomicity:** an evaluator exposes one verified complete active revision.
- **Cache binding:** reuse matches all relevant input/revisions and revocation constraints.
- **Use binding:** permit applies to the same resource/action state that was evaluated.
- **Collection confidentiality:** filtering precedes every derived disclosure.
- **Evidence correlation:** decision and enforcement outcomes connect through durable identity.
- **Exceptional accountability:** break-glass and overrides are narrower and more visible than normal access.

### Proof sketch: PDP correctness is insufficient without complete mediation

Assume PDP $D$ always returns the intended decision. Let resource $r$ be mutable by two feasible paths: API path $p_1$ includes a correct PEP, while direct provider path $p_2$ accepts a credential without consulting that PEP. Choose an action that policy denies. On $p_1$, correct evaluation and enforcement prevent it. On $p_2$, no decision is requested and the effect occurs. Therefore PDP correctness does not imply system policy enforcement while any feasible bypass exists. Complete mediation plus correct PEP behavior is necessary. This is a proof sketch of necessity, not proof that a particular architecture has discovered every path.

### Executable enforcement-outcome audit

This synthetic audit distinguishes decisions from enforcement outcomes. It demonstrates accounting categories, not a deployed PDP, PEP, or policy proof.

<!-- bijux-verify: {"id":"policy-enforcement-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"enforced_permit=3\nprevented=3\nobligation_failure=1\nindeterminate=1\nbypass=1\nstale=1\n"}} -->
```python
from collections import Counter

events = [
    "enforced_permit", "enforced_permit", "enforced_permit",
    "prevented", "prevented", "prevented",
    "obligation_failure", "indeterminate", "bypass", "stale",
]

counts = Counter(events)
for outcome in (
    "enforced_permit", "prevented", "obligation_failure",
    "indeterminate", "bypass", "stale",
):
    print(f"{outcome}={counts[outcome]}")
```

The ten events include three permits actually enforced, three prevented effects, and one each obligation failure, indeterminate decision, bypass, and stale decision. Production evidence must derive categories from correlated decision, PEP, and effect records with an independent path inventory.

### Verification strategy

Policy unit and property tests cover allow, deny, boundary, missing, conflict, stale, and malicious input. Differential tests compare active/candidate revisions and combining semantics. Type and static analysis bound unsafe built-ins and recursion.

PEP contract tests forge outcomes, omit decision IDs, change request/resource versions, return unknown obligations, exceed header/body bounds, time out, and return not-applicable/indeterminate. The effect must remain prevented under high-risk contracts.

Coverage tests enumerate routes, queues, jobs, workflows, controllers, consoles, provider roles, and recovery tools. Attempt bypass with direct network, old credentials, alternate verbs, batch endpoints, and asynchronous messages.

Consistency tests revoke membership, move tenant, expire approval, freeze environment, activate/roll back policy, and drop invalidations during cached sessions. Collection tests cover counts, pagination, sort, facets, autocomplete, watches, graphs, and exports.

Operational tests corrupt/partially load bundles, start evaluators empty, partition control plane, overload PIP/PDP, skew clocks, fail obligations/logging, restore artifacts, and rotate signing keys. Verify logs are masked and decision/effect correlation survives.

## Alternatives and Trade-Offs

1. **Central PDP versus distributed PDPs.** Central service simplifies consistency; local evaluators reduce latency and network dependency while increasing version coordination.
2. **Sidecar versus embedded evaluation.** Sidecars isolate language/runtime and update independently; embedded evaluation is fast but couples every host to policy runtime and rollout.
3. **Gateway PEP versus application PEP.** Gateways cover common ingress; applications understand domain actions. Layer them without assuming ingress is complete mediation.
4. **Provider-boundary PEP versus platform-only PEP.** Provider enforcement limits bypass; it may lack rich context. Use scoped credentials and conveyed constraints.
5. **RBAC versus ABAC versus relationship models.** Roles are understandable, attributes express context, relationships model sharing graphs. Composition increases expressiveness and complexity.
6. **Fail closed versus fail open.** Closed protects confidentiality/integrity; open protects availability. Choose per action and offer governed emergency access.
7. **Live PIP reads versus distributed attributes.** Live reads improve currency; distribution improves latency and resilience. Preserve revisions and consequence-specific freshness.
8. **Decision caching versus reevaluation.** Caching saves latency/capacity; reevaluation improves revocation and context currency. Bind keys and validity tightly.
9. **Boolean versus structured decisions.** Boolean is easy; structured outcomes support explanations and obligations but require PEP compatibility and validation.
10. **Deny-overrides versus permit-overrides.** Deny-overrides favors guardrails; permit-overrides supports explicit exception but can defeat broad constraints. Define layered semantics.
11. **Precomputed filtering versus per-item checks.** Precomputation scales collections but can lag; per-item checks are current but expensive. Batch predicates or revisioned indexes can bridge.
12. **Shadow versus canary enforcement.** Shadow is safe for comparison but misses behavioral consequences; canary yields real evidence with bounded risk.
13. **Rich decision logs versus minimization.** Rich context aids diagnosis; it increases privacy and secret exposure. Prefer revisions/digests and protected diagnostic retrieval.
14. **Short permits versus long sessions.** Short validity improves revocation; repeated checks cost latency. Reauthorize on meaningful triggers.
15. **Policy-language flexibility versus constrained subsets.** Flexibility supports domains; constrained evaluation improves performance, static analysis, and predictability.

## Failure Modes and Misconceptions

1. **A valid identity is authorized.** Authentication and authorization answer different questions.
2. **The PDP enforces policy.** It computes a decision; a PEP must prevent or allow the effect.
3. **One gateway mediates everything.** Internal, asynchronous, administrative, and provider paths can bypass it.
4. **High check coverage proves complete mediation.** An unknown bypass may produce no check event.
5. **HTTP method is the action.** Domain operations often share verbs and paths.
6. **The caller can choose the policy query.** This lets it select a weaker decision contract.
7. **Any catalog attribute can drive grants.** Authority and update permissions determine trust.
8. **Owner means administrator.** Accountability metadata does not imply permission.
9. **Missing equals false.** Unknown, hidden, stale, conflict, and not applicable require defined semantics.
10. **Undefined means allow.** Protected operations should not gain access from absent policy.
11. **Every outage should fail closed.** Wrong-deny availability cost differs by action; decide explicitly.
12. **Fail open is only a PDP configuration.** The PEP chooses behavior when no decision arrives.
13. **A permit response completes authorization.** The PEP must validate and fulfill obligations before effect.
14. **Advice and obligations are equivalent.** Obligations are mandatory conditions of enforcement.
15. **A TTL alone makes cache safe.** Policy and fact changes can require invalidation or causal position.
16. **Principal/resource/action are the whole cache key.** Environment, delegation, approvals, versions, and evidence may matter.
17. **Authorization at workflow start covers later actions.** Long-running execution requires current checks at consequential steps.
18. **List authorization can check one synthetic resource.** Items can have different policies and hidden existence.
19. **Filtering results after counting is safe.** Counts and facets leak protected membership.
20. **One bulk permit applies to all items.** Heterogeneous resources need defined set and item semantics.
21. **Downloaded bundle is active bundle.** Verification and atomic activation must complete first.
22. **Local PDPs always improve reliability.** Stale or divergent revisions can return incorrect decisions.
23. **Shadow policy protects resources.** Shadow never controls the effect.
24. **Decision logs prove enforcement.** They prove evaluation; correlate PEP and effect outcome.
25. **More decision context is always better.** Sensitive and irrelevant data increases leakage and instability.
26. **Break-glass means bypass.** It is a narrow, strong, logged exceptional policy path.

## Worked Examples

### Example 1

**Situation.** An API gateway denies an account-delete request, but a background worker can call the cloud provider directly.

**Reasoning.** Inventory the worker as a feasible effect path, move provider credentials to an enforcing adapter or add an authorized worker PEP, scope credentials by action/tenant, and test direct calls. Gateway correctness alone is insufficient.

**Conclusion.** Enforcement coverage follows effect capability, not traffic diagrams.

### Example 2

**Situation.** A repository owner label is editable by developers and a policy grants production administration to the listed owner.

**Reasoning.** Remove the direct grant input, resolve accountable ownership through governed transfer and directory authority, and define a separate production role/approval policy. Audit past owner changes for privilege escalation.

**Conclusion.** Attribute authority is part of authorization design.

### Example 3

**Situation.** A PDP returns permit with obligation `limit_duration=3600`, but the PEP ignores unknown obligations.

**Reasoning.** The permit is not enforceable. Reject or deny, alert on contract incompatibility, gate policy rollout on PEP capability, and record an obligation failure rather than permit success.

**Conclusion.** Mandatory obligations are conditions, not decoration.

### Example 4

**Situation.** Group membership is revoked, but a cached secret-read permit remains valid for 15 minutes.

**Reasoning.** Secret-read revocation tolerance is shorter than the cache TTL. Use membership revision/invalidation or a short freshness-bound token, reauthorize each read, and deny when current evidence is unavailable.

**Conclusion.** Cache policy must match revocation consequence.

### Example 5

**Situation.** A policy check permits deployment at resource version 7, while another actor freezes the environment before dispatch.

**Reasoning.** Bind the provider command to version 7 or freeze revision and reject on mismatch; then reevaluate. A short TTL alone cannot close the race.

**Conclusion.** Permit must bind to the state that was evaluated.

### Example 6

**Situation.** Search hides restricted services on the results page but shows a count of 12 and their names in autocomplete.

**Reasoning.** Filter before indexing or query aggregation, ranking, facets, counts, pagination, and suggestions. Test unauthorized principals against every derived surface and cache.

**Conclusion.** Collection authorization includes metadata about the collection.

### Example 7

**Situation.** Half the sidecars activate bundle 42 while the remainder retain bundle 41.

**Reasoning.** Report active revision per evaluator, route actions requiring 42 only to ready instances or tolerate declared skew, compare decisions, and roll forward/back atomically. Never label downloaded-but-unverified 42 active.

**Conclusion.** Distributed evaluation requires observable version semantics.

### Example 8

**Situation.** Candidate policy changes 3% of sampled denials to permits in shadow mode.

**Reasoning.** Classify changes by action, tenant, reason, evidence freshness, and expected intent; review the high-consequence subset; test obligations and latency; canary only after unexplained expansions reach zero or explicit acceptance.

**Conclusion.** Shadow difference is evidence to analyze, not proof of safety.

### Example 9

**Situation.** The remote PDP is unavailable during a production incident.

**Reasoning.** Secret reads and privilege grants fail closed; previously public runbook reads may use a bounded verified cache. Emergency production access uses a separate strong break-glass policy with short scope, notification, and audit.

**Conclusion.** Failure behavior is action-specific and predesigned.

### Example 10

**Situation.** Audit contains a PDP permit but the tenant-header obligation failed before the provider call.

**Reasoning.** Correlate decision ID, obligation failure, PEP prevention, and absence of provider receipt. Report prevented/obligation-failure, not authorized success. If provider receipt exists, investigate an enforcement bypass.

**Conclusion.** Decision and enforcement outcomes require separate evidence.

## Cross-Program Connections

1. **Security Engineering:** complete mediation, least privilege, default deny, separation of duty, capabilities, and audit provide the security foundation.
2. **Identity and Access Management:** authentication assurance, federation, groups, delegation, workload identity, and revocation supply principal evidence.
3. **Distributed Systems:** replication, causal consistency, caching, partitions, clocks, and failure modes govern distributed decisions.
4. **API & Service Engineering:** canonical actions/resources, typed schemas, batch/list semantics, errors, and compatibility define the decision protocol.
5. **Database Systems:** conditional writes, snapshot consistency, materialized authorization indexes, transactions, and retention close use-time gaps.
6. **Software Architecture:** gateways, sidecars, bounded contexts, deputies, provider adapters, and effect boundaries determine PEP placement.
7. **Formal Methods:** policy logic, combining algorithms, noninterference, invariants, model checking, and counterexamples strengthen assurance.
8. **Reliability Engineering:** latency budgets, local fallback, SLOs, backpressure, fault testing, and recovery keep policy available safely.
9. **Data Engineering:** attribute provenance, schemas, freshness, quality, privacy, and lineage govern PIP evidence.
10. **Compliance and Governance:** obligations, exceptions, decision evidence, retention, dual approval, and break-glass support accountability.

## References

1. NIST. [SP 800-162: Guide to Attribute Based Access Control](https://csrc.nist.gov/pubs/sp/800/162/upd2/final). January 2014, updated 2019. Retrieved 2026-09-02.
2. OASIS. [eXtensible Access Control Markup Language 3.0 Core Specification](https://docs.oasis-open.org/xacml/3.0/xacml-3.0-core-spec-os-en.html). January 2013. Retrieved 2026-09-02.
3. Open Policy Agent. [OPA Documentation](https://www.openpolicyagent.org/docs). Retrieved 2026-09-02.
4. Open Policy Agent. [Deployment](https://www.openpolicyagent.org/docs/deploy). Retrieved 2026-09-02.
5. Open Policy Agent. [Management APIs and Architecture](https://www.openpolicyagent.org/docs/management-introduction). Retrieved 2026-09-02.
6. Open Policy Agent. [Operational Readiness and Failure Modes](https://www.openpolicyagent.org/docs/operations). Retrieved 2026-09-02.
7. Open Policy Agent. [Decision Logs](https://www.openpolicyagent.org/docs/management-decision-logs). Retrieved 2026-09-02.
8. Envoy Project. [External Authorization](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/security/ext_authz_filter.html). Retrieved 2026-09-02.
9. Backstage. [Permission Framework Overview](https://backstage.io/docs/permissions/overview/). Retrieved 2026-09-02.
10. Kubernetes. [Admission Control in Kubernetes](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/). Retrieved 2026-09-02.
11. Kubernetes. [Dynamic Admission Control](https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/). Retrieved 2026-09-02.
12. Ruoming Pang et al. [Zanzibar: Google's Consistent, Global Authorization System](https://research.google/pubs/zanzibar-googles-consistent-global-authorization-system/). USENIX ATC, 2019.
13. Cedar Policy. [Cedar Policy Documentation](https://docs.cedarpolicy.com/). Retrieved 2026-09-02.
14. IETF. [RFC 6750: OAuth 2.0 Bearer Token Usage](https://datatracker.ietf.org/doc/html/rfc6750). October 2012. Retrieved 2026-09-02.

## Exercises

### Exercise 1

Define PAP, PIP, PDP, PEP, decision, obligation, advice, complete mediation, default deny, policy bundle, decision cache, shadow evaluation, and authorization freshness. State four non-equivalences.

### Exercise 2

Trace a production deployment decision from authentication through PIP evidence, PDP evaluation, PEP obligations, provider effect, and correlated audit. Include unavailable, indeterminate, stale, and changed-resource branches.

### Exercise 3

Design complete mediation for a platform exposed through portal, CLI, API, workflow, controllers, scheduled jobs, administrative tools, and cloud provider credentials. Specify bypass tests and break-glass.

### Exercise 4

Design distributed PDP rollout and caching for 50 regions with low latency, rapid revocation, long-lived watches, policy bundles, PIP revisions, shadow analysis, and rollback.

### Exercise 5

An acquired platform grants access from editable catalog tags, checks only its gateway, logs full inputs, and fails open globally. Design a migration that preserves service while establishing trustworthy decision and enforcement architecture.

## Answers to the Exercises

### Answer 1

The PAP governs policy lifecycle; PIPs supply authoritative facts; a PDP evaluates a named policy; and a PEP intercepts and enforces at the effect boundary. A decision is a typed evaluation result with identity/revisions. An obligation is mandatory for enforcement; advice is optional. Complete mediation means every protected attempt passes effective enforcement. Default deny prevents absence/error from becoming permission unless explicitly governed.

A policy bundle is an immutable verified policy/data unit. A decision cache stores a result keyed by all relevant inputs/revisions within bounded validity. Shadow evaluation computes but does not enforce a candidate. Authorization freshness is acceptable evidence/policy age and causal position for an action.

Non-equivalences include authentication $\ne$ authorization; PDP $\ne$ PEP; permit decision $\ne$ successfully enforced effect; obligation $\ne$ advice; downloaded bundle $\ne$ active verified bundle; and high observed check rate $\ne$ complete mediation.

### Answer 2

The API PEP authenticates user/workload, validates audience and delegation, canonicalizes `environment.deploy` and resource ID, and captures request digest/resource version. PIPs return current group membership, tenant, environment lifecycle/freeze, approval bound to digest, and policy context with authority, revision, observation, and sensitivity.

The PDP evaluates the named decision under active signed bundle revision and returns decision ID, permit/deny/not-applicable/indeterminate, safe reason, evidence revisions, validity, and obligations. For permit, the PEP validates request binding and schema, fulfills required audit and downstream-constraint obligations, and sends a provider command conditionally bound to resource version. It records provider receipt and effect outcome under the decision ID.

Unavailable or malformed PDP and indeterminate/unknown critical facts deny this high-risk mutation and expose a retry or governed break-glass path. Stale approval or membership denies with a repairable reason. If the resource version/freeze changes before use, the provider precondition rejects; the PEP reevaluates rather than replaying permit. A deny prevents dispatch. Logs mask sensitive evidence while an authorized diagnostic view can resolve revisions.

### Answer 3

Inventory every effect, not only entry surface. Portal and CLI call the canonical API, whose application PEP understands domain action/resource. Workflows reauthorize consequential activities with initiator/delegation and current context. Controllers and scheduled jobs use workload identities and named decisions per reconciliation/effect. Administrative tools call stricter APIs. Provider credentials exist only in scoped enforcing adapters; ordinary services/users cannot call providers directly.

Use a coarse ingress PEP for routing plus semantic API PEPs and final provider constraints. Private networking, mTLS, service identities, database/provider permissions, admission policy, and credential vault rules make bypass structurally difficult. Each PEP contract defines outcomes, obligations, timeouts, fail behavior, and audit.

Test direct backend/provider access, alternate ports/routes/verbs, message injection, old workers, stolen workload credentials, batch endpoints, database consoles, recovery jobs, and disabled filters. Compare traffic/credential inventories against decision logs, recognizing that absent logs can mean bypass. Break-glass uses a separate strong identity, narrow action/resource, short expiry, reason/approval, notification, enhanced audit, and review; it never distributes universal provider credentials.

### Answer 4

Use logically centralized PAP to build immutable signed bundles with policy, static data, schemas, compatibility, and revision. Distribute to regional or sidecar PDPs through authenticated staging, signature/digest verification, compile/smoke checks, and atomic activation. Report downloaded and active revisions; gate traffic needing a new contract on readiness. Define bounded version skew and retain verified last-known-good according to action policy.

Decision keys include decision name/schema, principal/delegation, action, canonical resource/version, context, policy revision, and PIP revision/validity. Secret/privilege decisions use current revision or short invalidatable evidence; low-risk reads may use longer bounded caches. Push revocation/invalidation with sequence or causal token and fall back safely on gaps. Reauthorize watches periodically and on policy, membership, resource, tenant, or privilege change; filter every emitted item.

Shadow candidate bundles against masked sampled traffic and categorize permit expansions, denials, obligation changes, errors, and latency. Canary regions/actions only after semantic review; preserve PEP output compatibility. Rollback activates a known compatible immutable bundle and invalidates caches. Fault-test control-plane partition, empty evaluator, partial/corrupt bundle, invalidation loss, clock skew, PIP outage, and regional restore.

### Answer 5

First inventory high-consequence actions and all effect paths. Freeze new grant dependencies on editable tags, but do not revoke unknown production access blindly. Classify current policies, credentials, outages, and wrong-allow/wrong-deny costs. Put provider credentials behind scoped adapters and add semantic PEPs to API, async workers, controllers, jobs, and administrative paths while retaining the gateway as defense in depth.

Replace tag grants with authoritative directory membership, governed ownership/transfer, resource tenant/classification from its control plane, and approval from its authority. Define versioned named decision contracts and explicit missing/stale/conflict semantics. Start with shadow comparison against old behavior, investigate privilege expansions, then canary by low-risk action/tenant. Maintain explicit temporary exceptions with owner and expiry.

Replace global fail-open with action-specific behavior: high-risk mutations, cross-tenant reads, secrets, and grants fail closed; selected low-risk reads may use bounded verified caches. Add a narrow audited break-glass policy. Distribute signed atomic bundles to local PDPs, expose active revisions, bind caches to policy and evidence revisions, and invalidate on revocation.

Minimize decision inputs and mask tokens, personal facts, hidden resource names, and bodies in logs. Correlate decision ID with PEP obligations and provider outcome. Test direct routes, tag forgery, confused deputy, cache staleness, collection leaks, bundle absence/corruption, and obligation failure. Retire old tag rules, broad credentials, global fail-open, and unmasked retention only after callers, histories, recovery tools, and effect paths show zero dependence.
