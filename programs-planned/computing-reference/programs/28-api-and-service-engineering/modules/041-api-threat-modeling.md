---
module_id: API-041
program: API & Service Engineering
level: 1
module_number: 41
title: API Threat Modeling
status: complete
last_verified: 2026-09-01
---

# API Threat Modeling

## One-Page Review

### Governing question

How can a team identify, prioritize, mitigate, and continuously verify plausible attacks against an API by reasoning from assets, actors, trust boundaries, data flows, business capabilities, and operational reality?

### Essential definitions

- A **threat model** is a maintained representation of what must be protected, how the system works, who may attack it, what can go wrong, and how risk is controlled and verified.
- An **asset** is information, authority, capability, availability, money, safety, reputation, or evidence whose compromise matters.
- A **trust boundary** is a transition where identity, authority, integrity, confidentiality, ownership, or operational control assumptions change.
- An **attack surface** is the set of reachable interfaces, parsers, credentials, flows, dependencies, and administrative paths an adversary can influence.
- A **threat scenario** states an actor, prerequisites, entry point, action/path, targeted asset, and consequence.
- An **abuse case** describes a harmful use of valid or nearly valid product behavior, including business-flow automation.
- A **mitigation** changes likelihood, impact, detectability, or recovery for one or more named scenarios.
- **Residual risk** is the explicitly accepted, transferred, avoided, or still-unresolved risk after planned controls.

### Central model, mechanism, or theorem

Represent a threat model as

$$
M=(S,A,C,B,F,T,K,V,O),
$$

where $S$ is scope, $A$ assets, $C$ actors/capabilities, $B$ trust boundaries, $F$ data and control flows, $T$ threat scenarios, $K$ mitigations, $V$ verification evidence, and $O$ owners/decisions. Each scenario is a traceable tuple

$$
\tau=(c,p,e,x,a,q),
$$

for actor capability $c$, prerequisites $p$, entry $e$, attack path $x$, asset $a$, and consequence $q$. A model is actionable only when high-priority $\tau$ entries map to owned controls and observable verification, or to explicit time-bounded residual-risk decisions.

### Critical invariants

Scope includes deployed and operational paths, not only source code. Assets include authority and business capabilities, not only records. Every externally controlled flow crosses a named validation and authorization boundary. Identity assertions are trusted only from authenticated issuers over protected paths. Object and property authorization are evaluated for each target and action. Resource consumption and economically harmful valid behavior are modeled. Dependencies and callbacks are untrusted according to evidence, not network location. Every mitigation has an owner and a test or operational signal. Accepted risk states reason, approver, expiry, and review trigger. The model changes with architecture, contract, exposure, data, identity, dependencies, incidents, and controls.

### Common failures

Running a one-time workshop after implementation; drawing only boxes with no assets or attackers; equating a vulnerability list with attack paths; using the OWASP Top 10 as a complete model; assuming authenticated users are benign; ignoring business abuse, batch endpoints, old versions, admin APIs, webhooks, queues, and documentation; trusting an internal network; prioritizing by unsupported numeric precision; listing controls without testing them; accepting risk forever; recording secrets in diagrams; and letting the model drift away from the deployed system.

### Compact example

An order API accepts `POST /tenants/{tenant}/orders/{order}:cancel` through an edge proxy. A malicious tenant user changes `{order}` to another user's identifier. The asset is order authority and integrity; the entry is an authenticated public action; the path crosses tenant binding, repository scoping, and object authorization; the consequence is unauthorized cancellation. Controls are tenant-scoped lookup, target/action authorization, concealed denial, audit, and rate limits. Verification sends same-tenant and cross-tenant identifiers, including batched/racing variants, and asserts no state or existence disclosure. **Conclusion:** “requires authentication” does not address the actual threat scenario.

### Connections

[Implementing a Predictable Service Endpoint](040-implementing-a-predictable-service-endpoint.md) supplies a concrete system model. [Authentication Context Propagation](033-authentication-context-propagation.md), [Authorization Checks](034-authorization-checks.md), [Idempotency Keys](037-idempotency-keys.md), and [Rate Limits and Quotas](039-rate-limits-and-quotas.md) supply candidate controls. [Credential and Token Handling](../ROADMAP.md) next deepens one high-value attack surface.

## Governing Question

Given a particular API deployment and attacker capabilities, which reachable paths can violate the confidentiality, integrity, availability, authorization, privacy, financial, safety, or evidentiary properties of valued assets, and what owned evidence demonstrates that risk is controlled?

## Why This Matters

Security requirements do not emerge reliably from endpoint schemas. An OpenAPI document may say that bearer authentication is required while leaving object authorization, token audience, replay, administrative paths, dependency trust, and business abuse undefined. A scanner may find outdated software while missing that a valid low-privilege user can enumerate every invoice. A rate limiter may bound requests yet allow one request to trigger unbounded fan-out. Threat modeling connects the system the team intends to operate with the ways a capable adversary could use it.

APIs concentrate authority. They expose machine-speed access to data and actions, often through predictable identifiers, rich filters, bulk operations, callbacks, service credentials, and asynchronous work. An attacker does not need to violate a JSON schema if the documented business workflow permits harmful automation. Nor must the attacker be anonymous: ordinary users, tenant administrators, compromised clients, insiders, suppliers, and peer services have different useful capabilities.

Threat models also improve design economics. Discovering that tenant identity is caller-controlled before schema freeze is cheaper than repairing every repository query. Discovering that webhook destinations can reach metadata services before deployment is cheaper than responding to credential theft. The model focuses review and testing on the paths where design choices can still change risk.

A useful threat model is not a compliance picture or prediction of every future exploit. It is a versioned decision aid with declared scope and uncertainty. It makes assumptions challengeable, ties scenarios to controls, exposes residual risk, and identifies the evidence needed before release and during operation.

## Prerequisites and Retrieval

Retrieve confidentiality, integrity, availability, authenticity, authorization, accountability, privacy, non-repudiation limits, assets, actors, attack surface, trust boundaries, data-flow diagrams, STRIDE or another enumeration aid, abuse/misuse cases, risk likelihood and impact, defense in depth, least privilege, secure defaults, isolation, logging/detection, incident response, secure development lifecycle, and API inventory.

Before modeling, retrieve the deployed architecture and ownership, public and private contracts, gateways/proxies, DNS and TLS termination, authentication issuers and key distribution, tenant/delegation model, authorization policies, data classification and retention, state-changing workflows, bulk/batch/search/export operations, limits and budgets, caches/databases/queues/object stores, outgoing HTTP and webhook behavior, third-party APIs, administrative/debug/support interfaces, old versions, mobile/browser/service clients, secrets, build/deploy/control plane, regions and disaster recovery, observability pipelines, incident history, known abuse, and planned changes.

## Learning Objectives

By the end of this module, you should be able to:

1. define a bounded API threat-model scope and useful security properties;
2. inventory assets, actors, entry points, trust boundaries, stores, and flows;
3. write concrete attack and abuse scenarios rather than vague threat labels;
4. use STRIDE and the OWASP API Security Top 10 as prompts without mistaking either for completeness;
5. prioritize scenarios with explicit evidence, uncertainty, blast radius, and reversibility;
6. map controls to prevention, detection, response, recovery, and verification; and
7. maintain the model through architecture changes, releases, incidents, and operational feedback.

## Core Exposition

### Frame a decision-sized scope

“Threat model the API” is too broad. Choose a scope that one group can describe and change: a payment-refund capability, order API, public webhook receiver, partner ingestion interface, or identity-token exchange. Record purpose, owners, consumers, environments, included components, excluded components, deployment version, review date, and decisions the model must support.

Exclusions require interfaces and assumptions. If the identity provider is out of scope, the model still includes its issuer, audience, signing-key flow, availability, compromise assumptions, and the boundary where tokens enter. If the cloud control plane is covered elsewhere, reference its model and describe which deployment identities and secrets this API relies on. “Out of scope” never means “trusted by magic.”

Time matters. A pre-design model may compare architectures; a pre-release model validates controls; an incident model reconstructs attack paths. Mark planned components separately from deployed ones. Do not merge a desired future boundary with current production and then infer protection that does not yet exist.

Define explicit security properties. “Secure order data” is not testable. Better properties include:

- only an authorized principal in the bound tenant can observe an order;
- only permitted actions can change an order, and every change is attributable;
- a retry cannot apply one logical mutation twice;
- one tenant cannot exhaust another tenant's reserved capacity;
- cancellation reasons do not enter ordinary metrics or public errors;
- downstream events correspond to committed state; and
- recovery preserves tenant isolation and audit history.

These properties become the targets an attack might violate and the assertions verification must support.

### Inventory assets as value and authority

Start with what matters, not just database tables. API assets include:

- customer records, credentials, tokens, keys, personal and regulated data;
- resource state, balances, inventory, permissions, policy, and configuration;
- authority to refund, cancel, invite, export, approve, impersonate, or administer;
- availability of latency budgets, worker pools, downstream capacity, and human operations;
- financial allocations, promotion rules, scarce goods, and rate/quota entitlements;
- privacy properties, tenant separation, relationship/existence information, and metadata;
- audit trails, idempotency ledgers, event histories, and forensic evidence; and
- reputation, contractual commitments, safety, and legal obligations.

For each asset, name owner, classification, location, lifecycle, allowed actors/actions, required properties, maximum credible impact, and recovery constraints. An order identifier can be sensitive even if the order body is protected because existence and volume reveal business activity. An operation ledger is both a control and an asset: tampering could replay effects or disclose recorded responses.

Do not write “database” as the asset. The database contains differently protected facts and authority. Conversely, not all important assets are stored. The ability to trigger a costly export or send a message is valuable at the instant of action.

### Model actors by capability

List actors and the evidence-backed capabilities each begins with:

- unauthenticated internet user with many network origins;
- registered user in one tenant;
- tenant administrator with legitimate administrative APIs;
- user invited to multiple tenants;
- compromised browser, mobile app, API client, or service credential;
- malicious integration partner or webhook receiver;
- compromised downstream API or software dependency;
- support operator, developer, database operator, or cloud administrator;
- automated scraper, fraud group, botnet, or extortion actor; and
- accidental actor whose valid input or configuration causes harm.

Avoid omnipotent “hacker” stories. A scenario becomes designable when prerequisites are specific: valid low-privilege token, ability to select object IDs, control of a callback URL, stolen refresh token, read access to logs, or ability to race two requests. Also consider capability escalation and chaining. A harmless-looking inventory endpoint may reveal identifiers used in an authorization flaw elsewhere.

Insiders and operators are not accusations. Their privileged capabilities require separation of duties, approval, audit, short-lived access, and recovery. Trust should be proportional to technical and organizational evidence, not job title or network position.

### Draw deployed flows and trust boundaries

Create a data-flow view with external entities, processes, stores, flows, protocols, identities, and boundaries. For an order API, include client, DNS/CDN/WAF, gateway, service, authorization engine, database, cache, operation ledger, outbox, broker, consumers, identity provider, secrets/key service, logs/traces, deployment plane, support tool, and outbound webhooks.

Annotate flows with method/protocol, data classification, authentication, integrity/confidentiality protection, authorization context, size/rate, serialization/parser, timeout, retry, and owner. A line labeled “HTTPS” is incomplete: which peer is authenticated, where TLS terminates, what headers can be rewritten, and which identity survives the next hop?

Trust boundaries occur when any assumption changes:

- public client to edge;
- edge to service when forwarded identity is introduced;
- service to authorization decision point;
- one tenant partition to shared compute or storage;
- process to database, cache, queue, object store, or telemetry vendor;
- service to third-party API or caller-selected URL;
- runtime to build/deploy/control plane; and
- primary region to backup, analytics, or disaster-recovery systems.

For every crossing ask: who authenticates whom, what is authorized, what is validated, what can be replayed/reordered, what metadata leaks, what capacity is consumed, which failures are trusted, and what evidence exists? “Internal” is topology, not a security property.

### Enumerate entry points beyond public routes

The attack surface includes more than documented endpoints:

- current, deprecated, beta, regional, mobile, partner, and tenant-specific versions;
- GraphQL, RPC, WebSocket, streaming, upload, bulk, batch, and async job interfaces;
- callbacks, webhooks, redirect URIs, imports, parsers, URL fetches, and file processors;
- admin, support, debug, metrics, health, readiness, profiling, and feature-control routes;
- queues, event consumers, scheduled jobs, database imports, and replay tools;
- API documentation, schema discovery, examples, SDKs, and error responses;
- authentication, password recovery, invitation, account linking, and delegation;
- caches, logs, traces, dashboards, backups, analytics, and data exports; and
- CI/CD, artifact registries, dependency resolution, configuration, secrets, and infrastructure APIs.

Maintain an API inventory with owner, version, environment, exposure, authentication, data class, lifecycle, and observed traffic. Undocumented or forgotten versions are especially dangerous because patch and monitoring assumptions often exclude them. OWASP API9:2023 highlights improper inventory management, but a model must trace the concrete abandoned hosts and controls in this system.

### Write attack stories with consequences

A useful scenario has a causal sentence:

> A tenant user with a valid read token changes the object identifier on a bulk export request, causing the repository to select another tenant's records, which discloses customer data at machine speed.

This identifies capability, entry, action, control failure, asset, and consequence. “Broken access control” is only a category. “Attacker steals data” lacks a path. Write preconditions and variants: guessed IDs, identifiers learned from another endpoint, batch mixing, pagination, timing differences, cached responses, race conditions, and archived versions.

Use several complementary prompts:

- **STRIDE:** spoofing, tampering, repudiation, information disclosure, denial of service, and elevation of privilege across each element/flow;
- **security properties:** how could confidentiality, integrity, availability, authorization, privacy, accountability, financial, or safety properties fail?
- **attacker goals:** acquire authority, steal data, change state, evade evidence, exhaust resources, commit fraud, pivot, persist, or extort;
- **abuse cases:** how can valid features be automated, combined, raced, or scaled harmfully?
- **incident and intelligence evidence:** how have this system, similar systems, or dependencies actually failed?
- **OWASP API Security Top 10:** object/property/function authorization, authentication, resource consumption, sensitive business flows, server-side request forgery, configuration, inventory, and unsafe API consumption.

These are enumeration aids, not substitutes for the deployed model. A scenario can span categories; important threats may appear in none. The 2023 Top 10 is an awareness document, not a complete risk ranking for a particular organization.

### Model API-specific attack paths

**Object-level authorization:** Enumerate every endpoint that accepts or derives object identifiers, including nested, batched, filtered, cached, and indirect references. Test same-role cross-user, cross-tenant, deleted/archived, and timing/existence cases.

**Property-level authorization:** Separate readable, writable, server-owned, sensitive, computed, and role-dependent fields. Consider mass assignment, over-broad serialization, sparse fieldsets, expansions, patch paths, and old schemas.

**Function-level authorization:** Inventory administrative, support, bulk, moderation, billing, and lifecycle actions. A hidden route or UI restriction is not authorization. Consider method changes and alternate API versions.

**Authentication and session/token lifecycle:** Model issuance, audience, issuer, signature algorithms/keys, expiration, replay, refresh, revocation, logout, device/client binding, delegation, recovery, logging, storage, and key rotation. The following modules deepen these surfaces.

**Resource consumption:** Trace bytes, decompression, parser complexity, regex/backtracking, pagination, query fan-out, database locks, response size, downstream calls, queue growth, long-lived streams, and expensive error paths. Map cost before and after authentication.

**Sensitive business flows:** Identify scarce purchase, reservation, signup, invitation, content, referral, voting, messaging, pricing, and recovery capabilities. A sequence can be syntactically valid and authorized yet economically or socially abusive. Model automation rate, inventory, identities, reversibility, and human response.

**Server-side request forgery and unsafe consumption:** For caller-influenced URLs or external APIs, model DNS changes, redirects, IP forms, metadata/control-plane addresses, parser inconsistencies, response size, schema trust, signatures, timeouts, retries, and how returned data affects privileged decisions.

**Misconfiguration and inventory:** Include default credentials, verbose errors, permissive CORS, debug modes, unprotected docs, inconsistent gateways, stale hosts, shadow APIs, old keys, insecure transport, and missing hardening. Validate deployed configuration, not templates alone.

### Trace chains, not only isolated weaknesses

Attackers compose small observations. An unauthenticated schema endpoint reveals an old admin route. A low-privilege list call leaks sequential IDs. Different `404` timing confirms valid objects. A bulk endpoint accepts mixed tenant IDs. Verbose errors expose a storage bucket. A webhook fetcher reaches internal metadata. A log dashboard contains replayable credentials.

Represent chains as ordered preconditions and transitions. Ask what new capability each step grants and which independent control can break the chain. Defense in depth is meaningful only when controls fail independently enough: a gateway check and service check generated from the same mistaken tenant header are not independent.

Consider lateral movement between control and data planes, regions, tenants, and services. A service-to-service token with a broad audience can turn one compromised workload into many. A shared cache key missing tenant scope can bypass otherwise correct repository authorization. A disaster-recovery path may restore data into weaker controls.

### Prioritize without false precision

Priority should support decisions, not manufacture certainty. For each scenario assess:

- attacker capability and access already available;
- exposure and discoverability of the path;
- feasibility, prerequisites, and opportunity to automate;
- control strength and independence;
- consequence across confidentiality, integrity, availability, privacy, financial, legal, and safety dimensions;
- blast radius per object, tenant, region, or entire service;
- detection time, reversibility, and recovery cost;
- evidence quality and uncertainty; and
- whether the path is being changed or has incident history.

A small ordinal matrix (for example, low/medium/high likelihood and impact) can organize discussion. Multiplying subjective numbers does not make them measurements. Preserve rationale and confidence. A low-frequency, irreversible cross-tenant disclosure may outrank a frequent recoverable nuisance. A known exploitable path with weak detection should not wait because its score falls just below an arbitrary line.

Set treatment rules. Critical scenarios block release until mitigated or explicitly accepted by an authorized risk owner. Acceptance records rationale, compensating controls, affected assets, expiry, monitoring, and trigger for reconsideration. “Backlog” without an owner or date is silent acceptance.

### Design control sets around scenarios

For each priority scenario choose a layered control set:

- **prevent:** remove the feature/path, minimize authority, validate, isolate, authenticate, authorize, constrain egress, make states unrepresentable;
- **limit:** scope credentials, bound size/rate/cost/concurrency, partition tenants, reduce retention, add transaction/precondition/idempotency invariants;
- **detect:** audit decisions, alert on bounded signals, reconcile invariant violations, detect inventory drift and unusual sequences;
- **respond:** revoke credentials, disable an operation, isolate tenant/region, block destinations, rotate keys, preserve evidence;
- **recover:** restore known-good state/configuration, compensate effects, republish outbox, notify affected parties, verify isolation; and
- **assure:** code review, policy tests, contract tests, adversarial tests, fuzzing, SAST/DAST where applicable, configuration validation, race/fault tests, penetration tests, and production exercises.

Controls need placement and owner. “Validate input” must say which boundary, schema/semantic rule, canonical form, size, and failure behavior. “Use OAuth” must say issuer, audience, grant, scopes, token type, client authentication, storage, and verification. “Rate limit” must name key, cost, window/burst, enforcement location, distributed behavior, and outage policy.

Avoid one-control closure. Authentication does not solve object authorization. Encryption does not prevent authorized misuse or compromised endpoints. A web application firewall does not understand every business invariant. Logging without detection/response ownership merely records compromise.

### Attach verification and operational evidence

A mitigation is not complete because code exists. Define evidence at design time:

- property/unit tests for policy and domain decisions;
- integration tests for real routing, identity propagation, tenant scoping, and persistence;
- contract tests for status, errors, headers, and schema disclosure;
- negative authorization matrices across roles, objects, tenants, fields, actions, versions, and batches;
- race, replay, timeout, and failure injection for stateful controls;
- fuzzing/property tests for parsers and canonicalization;
- deployment checks for TLS, CORS, debug/admin exposure, keys, egress, and inventory;
- load/abuse tests for cost amplification and fairness;
- red-team or penetration evidence for priority paths; and
- monitoring, alert drills, credential revocation, isolation, and recovery exercises.

Record evidence identifiers and freshness. A test that covered version 1 may not cover version 2 or a new gateway. A policy engine unit test does not prove every handler calls it with the correct target. Combine control-local and end-to-end evidence.

Detection should follow the scenario. For identifier enumeration, observe denied and absent-object patterns without exposing raw object IDs as metric labels. For token replay, correlate issuer-safe token hashes, clients, geography, and timing under privacy controls. For SSRF, log normalized destination class and egress decision, not embedded credentials. Define who receives the signal and what they can do.

### Keep a traceable threat register

Each entry should contain stable scenario ID, assets/properties, actor/prerequisites, entry/flow/boundary, attack narrative, impact and likelihood rationale, uncertainty, existing controls, gaps, treatment, owner, due date, verification evidence, monitoring/response, residual risk, status, and last review. Link to architecture and tests without embedding secrets or exploitable production details in broadly visible documents.

The executable model below checks structural traceability for a tiny register. It does not discover threats or judge control quality; human and technical review must do that.

<!-- bijux-verify: {"id":"threat-register-traceability","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"scenarios=3\npriority_open=1\nall_assets_known=True\nall_boundaries_known=True\nall_controls_owned=True\nall_treated_verified=False\nmodel_traceable=True\n","stderr":""}} -->
```python
assets = {"order-authority", "tenant-data", "service-capacity"}
boundaries = {"internet-edge", "edge-service", "service-database"}
controls = {
    "object-authz": "identity-team",
    "tenant-scope": "order-team",
    "cost-admission": "platform-team",
}
scenarios = [
    {"id": "T-1", "asset": "order-authority", "boundary": "edge-service",
     "priority": "high", "controls": {"object-authz", "tenant-scope"},
     "evidence": {"cross-tenant-negative-test"}},
    {"id": "T-2", "asset": "service-capacity", "boundary": "internet-edge",
     "priority": "high", "controls": {"cost-admission"},
     "evidence": set()},
    {"id": "T-3", "asset": "tenant-data", "boundary": "service-database",
     "priority": "medium", "controls": {"tenant-scope"},
     "evidence": {"repository-scope-test"}},
]

known_assets = all(item["asset"] in assets for item in scenarios)
known_boundaries = all(item["boundary"] in boundaries for item in scenarios)
owned = all(all(control in controls for control in item["controls"]) for item in scenarios)
treated = all(item["controls"] and item["evidence"] for item in scenarios)
open_high = sum(item["priority"] == "high" and not item["evidence"] for item in scenarios)

print(f"scenarios={len(scenarios)}")
print(f"priority_open={open_high}")
print(f"all_assets_known={known_assets}")
print(f"all_boundaries_known={known_boundaries}")
print(f"all_controls_owned={owned}")
print(f"all_treated_verified={treated}")
print(f"model_traceable={known_assets and known_boundaries and owned}")
```

The output deliberately reports one high-priority scenario without evidence and therefore `all_treated_verified=False`. Structural validity does not authorize release. It helps reviewers find the unresolved decision.

### Integrate modeling with delivery and operations

Create the first model during requirements/design, refine it when contracts and architecture stabilize, verify before exposure, and review after deployment. Add change triggers to ordinary engineering workflow:

- new endpoint, method, field, expansion, batch, filter, or business action;
- authentication, authorization, tenant, delegation, or credential change;
- new data classification, retention, region, customer type, or compliance duty;
- new dependency, callback, queue, parser, protocol, or egress path;
- gateway, cache, database, deployment, observability, or control-plane change;
- public/private exposure or API version lifecycle change;
- material threat intelligence, vulnerability, abuse signal, near miss, or incident; and
- mitigation redesign, exception, expiry, or control-evidence failure.

Review diffs rather than restarting blindly. What assets, actors, flows, boundaries, scenarios, and assumptions changed? Preserve closed scenarios and decision history where useful, but remove obsolete deployment facts from the active view. Periodically reconcile the inventory against DNS, gateways, service catalogs, traffic, certificates, repositories, and cloud resources.

During incidents, use the model as a hypothesis map, not unquestionable truth. Record newly observed paths and failed assumptions. Afterward, update scenarios, controls, tests, signals, owners, and response playbooks. A model that never changes after an incident is not functioning as engineering evidence.

### Facilitate reviews that produce decisions

Invite people who know the consumer task, domain, API implementation, identity/authorization, data, platform/network, operations, testing, incident response, and privacy/risk context. Keep the group small enough to reason but consult specialists for cryptography, fraud, safety, or regulated data.

Send scope and diagrams beforehand. In the session, confirm reality, assets, properties, actors, boundaries, then enumerate concrete stories before debating controls. Capture unknowns as owned investigations. Separate brainstorming from prioritization so early confidence does not suppress plausible paths. Encourage challenges to trust assumptions without turning the review into blame.

End with decisions: scenario priority, treatment, control owner, evidence, due date, residual-risk authority, and next trigger. A long unowned list is not a completed threat model. Track work in normal delivery systems while keeping the model the coherent security rationale.

## Definitions and Notation

Let system scope be $S$, assets $A$, attacker/actor capabilities $C$, trust boundaries $B$, flows $F$, threat scenarios $T$, mitigations $K$, verification evidence $V$, and ownership/decisions $O$. A scenario $\tau=(c,p,e,x,a,q)$ binds capability, prerequisites, entry, path, asset, and consequence.

Define mappings $k:T\rightarrow 2^K$ from scenarios to controls and $v:K\rightarrow 2^V$ from controls to evidence. A priority scenario is **unresolved** when it has neither an approved avoidance/acceptance decision nor a sufficient owned control set with current evidence. These mappings establish traceability, not effectiveness by themselves.

An **assumption** is a proposition the model relies on and can later test or invalidate. **Blast radius** is the maximum credible affected scope. **Attack chain** is an ordered sequence in which each step grants prerequisites for the next. **Compensating control** reduces risk when the preferred control is unavailable. **Risk acceptance** is an authorized, bounded decision about residual risk—not the absence of work.

## Mechanisms, Invariants, or Proof Structure

1. Select a decision-sized deployed scope, owners, environments, and explicit exclusions.
2. State security properties and inventory assets, including authority, capacity, privacy, and evidence.
3. Enumerate actors by starting capability and plausible escalation.
4. Draw processes, stores, flows, entry points, and every changing trust assumption.
5. Write causal attack/abuse scenarios using property, STRIDE, attacker-goal, incident, and API-risk prompts.
6. Trace chains and variants across versions, batches, tenants, dependencies, and control/data planes.
7. Prioritize with evidence-based likelihood, consequence, blast radius, reversibility, detectability, and uncertainty.
8. Map scenarios to prevention, limitation, detection, response, recovery, and assurance controls.
9. Assign owners, dates, verification evidence, monitoring, and bounded residual-risk decisions.
10. Reconcile against deployment and update on architectural, contractual, operational, and threat changes.

Completeness cannot be proven for an open adversarial system. The defensible claim is narrower: the team used multiple systematic prompts over an accurate scoped model, recorded assumptions and uncertainty, treated priority scenarios, and maintains verification and change triggers.

## Alternatives and Trade-Offs

Diagram-first modeling exposes boundaries and flows but can underemphasize business semantics. Abuse-case-first modeling engages domain experts but can miss infrastructure paths. Asset-first modeling clarifies consequences but may overlook reachable entry points. Combine them for important APIs.

STRIDE is memorable and element-oriented but produces generic labels without concrete stories. Attack trees show multi-step attacker goals but take effort to maintain. Kill-chain or ATT&CK-style views help incident/adversary reasoning but may fit enterprise behavior better than endpoint-level business abuse. Use the lightest methods that improve coverage and decisions.

Central security teams provide consistency and cross-system intelligence, while product teams know the deployed behavior and own fixes. A federated model—product ownership with security facilitation and review—usually preserves both. Outsourced reviews add perspective but cannot replace internal ownership or continuous updates.

Quantitative risk methods can help when probabilities and loss data are defensible. Ordinal bands are faster but coarse. Either approach must preserve rationale, uncertainty, tail impact, and risk-owner judgment. Avoid treating arithmetic as evidence.

Detailed models help defenders but can expose sensitive architecture or attack paths. Classify artifacts, minimize secrets and exact production coordinates, separate broadly useful diagrams from restricted details, and maintain access/audit controls. Security through obscurity is not the control; responsible information handling is.

Modeling every minor change exhaustively is expensive; modeling too little lets architecture drift. Use change-based triage: high-authority, high-data, new-boundary, externally exposed, parser, identity, and business-flow changes receive deeper review, while established low-risk patterns reuse verified control libraries with explicit applicability checks.

## Failure Modes and Misconceptions

- **“The OWASP Top 10 is our threat model.”** It is a valuable awareness prompt, not this system's assets, paths, priorities, and evidence.
- **“We ran a scanner.”** Scanners find selected implementation symptoms, not authorization logic or business abuse comprehensively.
- **“The API requires login.”** Authenticated actors remain capable adversaries; object, property, and function authorization are distinct.
- **“Internal traffic is trusted.”** Workloads, operators, networks, proxies, and dependencies can be compromised or misconfigured.
- **“HTTPS protects the API.”** It protects selected transport properties between defined peers, not endpoint authorization or valid abuse.
- **“The diagram is the model.”** A diagram without assets, scenarios, decisions, and evidence is only one input.
- **“A STRIDE label is a scenario.”** State capability, path, targeted asset, and consequence.
- **“High score means truth.”** Priority is a decision under uncertainty; preserve rationale and tail impact.
- **“A control exists, so risk is closed.”** Placement, configuration, coverage, independence, and current evidence matter.
- **“Logging detects attacks.”** Signals require queries/alerts, ownership, response authority, and exercises.
- **“Valid requests are safe.”** Sensitive business flows can be abused with correct schemas and permissions.
- **“Out of scope means safe.”** Record the interface, reliance, owner, and assumption.
- **“Accepted risk is permanent.”** It requires authority, scope, rationale, expiry, monitoring, and triggers.
- **“Model once before launch.”** Inventory, attackers, architecture, controls, and exposure evolve.

## Worked Examples

### Example 1

**Situation:** Sequential order IDs are accepted by a detail route. **Reasoning:** A tenant user can change the ID; authentication succeeds but object authorization may not. Model cross-user, cross-tenant, batch, cache, and timing variants. **Conclusion:** tenant-scoped lookup plus target authorization and negative tests control the actual path.

### Example 2

**Situation:** A PATCH schema includes `role`, though the UI never sends it. **Reasoning:** The API, not the UI, is the boundary. Mass assignment can change a server-owned property. **Conclusion:** use command-specific allowlists/property authorization and test forbidden/unknown fields.

### Example 3

**Situation:** An export route is fully authorized but lets one tenant request unlimited joins and rows. **Reasoning:** Valid use amplifies database/worker cost and can deny others. **Conclusion:** model resource units, bounds, async concurrency, tenant/global admission, cancellation, and operational shedding.

### Example 4

**Situation:** A reservation API permits one account to hold scarce inventory repeatedly. **Reasoning:** Every call is syntactically valid and authorized, yet automation harms the business flow. **Conclusion:** model identities, inventory, hold duration, velocity, economic signals, reversibility, and abuse response beyond generic request rate.

### Example 5

**Situation:** A webhook tester fetches a caller-provided URL. **Reasoning:** DNS, redirects, alternate IP forms, and response parsing may reach metadata/control-plane services or consume unbounded bytes. **Conclusion:** constrain destinations/egress, revalidate each hop, bound time/bytes, isolate credentials, and test SSRF variants.

### Example 6

**Situation:** A gateway injects `X-Tenant`, but the public service also accepts that header directly. **Reasoning:** The trust boundary is ambiguous and clients can spoof authority. **Conclusion:** strip public values, authenticate the gateway-to-service channel, sign/bind context, and test direct reachability.

### Example 7

**Situation:** Version 1 is deprecated in documentation but still receives traffic on an old host. **Reasoning:** Inventory and patch/monitoring processes cover only version 2. **Conclusion:** discover from DNS/gateway/traffic, assign an owner, apply equivalent controls, migrate, and verifiably retire the host.

### Example 8

**Situation:** A partner API response controls an internal object identifier. **Reasoning:** Authenticated TLS does not guarantee the partner data is safe or uncompromised. **Conclusion:** schema/semantic validation, authorization of resulting action, bounded consumption, timeouts, and anomaly handling guard unsafe consumption.

### Example 9

**Situation:** Support staff can impersonate any tenant indefinitely. **Reasoning:** This high-authority operational path bypasses ordinary user assumptions. **Conclusion:** require approved just-in-time scope, short lifetime, dual identity in context/audit, customer policy, alerts, and revocation exercises.

### Example 10

**Situation:** A mitigation says “rate limit login” and is marked done. **Reasoning:** No key, cost, burst, distribution, outage policy, or verification exists; attackers rotate addresses and target accounts. **Conclusion:** rewrite it as layered source/device/account risk controls with measurable bounds, safe recovery, owners, tests, and signals.

## Cross-Program Connections

- **Security Engineering:** threat models connect security properties, attacker capabilities, defense in depth, residual risk, and assurance.
- **Systems Engineering:** scope, interfaces, assumptions, hazards, owners, evidence, and change control turn security into a lifecycle property.
- **Software Architecture:** data flows, ports/adapters, identity propagation, tenancy, and dependency boundaries determine reachable paths.
- **Database Engineering:** row/property scoping, isolation, conditional writes, audit integrity, backups, and analytics paths shape asset protection.
- **Distributed Systems:** retries, queues, partial failure, caches, regional failover, and service identities create chained threats and uncertainty.
- **Product and Economics:** valid business-flow abuse targets scarce inventory, incentives, money, attention, and human operations.
- **Testing and Verification:** negative matrices, properties, fuzzing, race/fault injection, deployment checks, and exercises turn mitigations into evidence.

## References

1. OWASP Foundation. [Threat Modeling](https://owasp.org/www-community/Threat_Modeling). Checked 2026-09-01.
2. OWASP Foundation. [OWASP Threat Modeling Project](https://owasp.org/www-project-threat-modeling/). Checked 2026-09-01.
3. OWASP Foundation. [OWASP API Security Top 10 — 2023](https://owasp.org/API-Security/editions/2023/en/0x00-header/). Checked 2026-09-01.
4. Rescorla, E., and Korver, B. [RFC 3552: Guidelines for Writing RFC Text on Security Considerations](https://www.rfc-editor.org/rfc/rfc3552.html). IETF BCP 72, July 2003. Checked 2026-09-01.
5. Souppaya, M., Scarfone, K., and Dodson, D. [NIST SP 800-218: Secure Software Development Framework (SSDF) Version 1.1](https://csrc.nist.gov/pubs/sp/800/218/final). NIST, February 2022. Checked 2026-09-01.
6. Microsoft. [Threat Modeling Security Fundamentals](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats). Microsoft Learn. Checked 2026-09-01.

## Exercises

### Exercise 1

Threat-model a multi-tenant document export endpoint. Define scope, five assets/security properties, actors, boundaries, three concrete attack stories, priority rationale, controls, and verification evidence.

### Exercise 2

Expand the scenario “attacker abuses password reset” into a causal attack chain covering account enumeration, token generation/delivery/storage, rate/resource abuse, session invalidation, audit, and recovery. Mark assumptions.

### Exercise 3

Review a service that accepts a caller URL, follows redirects, parses JSON, and uses one field to trigger an internal action. Produce prevention, limitation, detection, response, recovery, and assurance controls.

### Exercise 4

Design a threat-register schema and lifecycle for a team shipping weekly. Include change triggers, risk acceptance, evidence freshness, incident feedback, inventory reconciliation, and release rules.

### Exercise 5

Explain why neither STRIDE, the OWASP API Security Top 10, a vulnerability scanner, nor a penetration test alone is a complete API threat model. Propose a combined workflow that uses each appropriately.

## Answers to the Exercises

### Answer 1

Scope the deployed export route, gateway, service, authorization engine, job queue/worker, database/object store, download link, and telemetry. Assets/properties include tenant-confidential documents; export authority; tenant/global worker and storage availability; privacy/retention of artifacts; and attributable audit. Actors include anonymous callers, ordinary tenant users, tenant admins, compromised clients, support operators, and malicious document content. Boundaries include internet/edge, edge/service identity context, service/data, service/queue-worker, worker/object store, and link recipient/storage. Scenarios can include cross-tenant filters disclosing data, a valid tenant creating unbounded costly jobs, and malicious document content exploiting a converter. Prioritize from exposure, automation, data/blast radius, parser feasibility, controls, detection, and recovery. Controls include tenant-scoped query construction/object-property authorization, bounded rows/cost/concurrency and quotas, isolated patched conversion, short-lived audience-bound download authorization, retention cleanup, audit, and egress limits. Evidence includes negative tenant/field matrices, cost/load tests, parser fuzz/sandbox tests, queue-failure tests, link expiry/replay tests, configuration checks, and reconciliation of jobs, artifacts, and audits.

### Answer 2

An anonymous actor first compares responses or timing to enumerate accounts, then requests resets at scale to exhaust delivery or harass users. The service generates a predictable, long-lived, logged, or weakly scoped token; an attacker obtains it through compromised email/SMS, referrer/log leakage, or guessing; reset fails to revoke existing sessions or refresh tokens; weak audit/detection delays response. Assumptions include delivery-channel security, entropy source, single use, issuer storage, expiry clock, URL handling, user device, and support recovery. Controls normalize public responses/timing, layer source/account delivery limits, generate high-entropy hashed single-use short-lived audience/purpose-bound tokens, avoid URL leakage, confirm important changes, revoke/rotate applicable sessions, audit safe identifiers, notify users, detect unusual sequences, and provide rapid recovery. Verify enumeration equivalence, token properties, concurrency/single use, expiration, logs, revocation, abuse bounds, and recovery exercises.

### Answer 3

Prevent by removing arbitrary URLs where possible, allowlisting owned destinations, resolving and connecting through controlled egress, rejecting private/link-local/control-plane ranges across all address forms, rechecking redirects/DNS, authenticating the external API, and authorizing the internal action independently of returned data. Limit schemes, ports, redirects, time, bytes, decompression, parser depth, response schema, credentials, network reach, retries, concurrency, and action scope. Detect denied destination classes, unusual redirect/DNS behavior, response anomalies, egress volume, and privileged action patterns with safe labels. Respond by disabling the fetch feature, blocking destinations/egress, revoking workload credentials, isolating the service, and preserving evidence. Recover by rotating exposed credentials, validating control-plane state, compensating actions, and restoring known-good configuration. Assure with SSRF encoding/redirect/rebinding cases, malicious JSON/schema fuzzing, timeout/size tests, egress-policy validation, compromised-partner simulations, and end-to-end authorization tests.

### Answer 4

Use stable scenario IDs and fields for scope/version, assets/properties, actor/prerequisites, entry/flow/boundary, narrative, consequences, likelihood/impact rationale, uncertainty, existing controls, gaps, treatment, owner/date, evidence IDs and freshness, monitoring/response, residual decision/approver/expiry, status, and review history. Pull modeling into design for new authority/data/boundaries and use weekly change triage for endpoint/schema, identity, dependency, deployment, exposure, and configuration diffs. Release rules block unresolved critical scenarios unless the designated risk authority records bounded acceptance. CI links applicable control tests and configuration/inventory checks; periodic review expires stale evidence. Reconcile declared APIs against DNS, gateways, traffic, catalogs, certificates, and cloud resources. Incidents and near misses create/update paths, invalidate assumptions, add tests/signals, and trigger model review rather than merely closing a ticket.

### Answer 5

STRIDE prompts categories across model elements but does not supply deployed assets, business abuse, priority, or proof. The OWASP list highlights common API risks but is neither exhaustive nor system-specific. A scanner tests recognizable technical patterns and versions but usually lacks domain authority and flow context. A penetration test samples attackability at a time and scope, but cannot continuously establish completeness. First model scope, assets, actors, flows, boundaries, and properties; then use STRIDE, attacker goals, abuse cases, incident evidence, and OWASP categories to enumerate causal scenarios. Prioritize and design owned controls/evidence. Use scanners in CI/deployment for applicable technical classes and focused penetration/red-team work for high-risk chains. Feed findings back into scenarios, controls, automated tests, signals, response exercises, inventory, and change-triggered review.
