---
module_id: PLAT-005
program: Platform Engineering
level: 1
module_number: 5
title: Self-Service and Guardrails
status: complete
last_verified: 2026-09-02
---

# Self-Service and Guardrails

## One-Page Review

### Governing question

How can a platform let an authorized consumer complete a supported job on demand, without hidden platform-team coordination, while preventing, detecting, explaining, and recovering from outcomes outside the organization's accepted boundary?

### Essential definitions

- **Self-service** is the ability of an eligible consumer to initiate, observe, and complete or safely terminate a supported journey through a documented contract without routine platform-team intervention.
- A **guardrail** is a preventive, detective, or corrective mechanism that constrains or responds to action at an explicit authority and risk boundary while preserving a usable path to valid outcomes.
- A **paved default** is a reviewed initial choice appropriate for a declared workload class. It is not universally safe merely because the platform selected it.
- **Validation** asks whether a request conforms to declared structural and semantic rules. **Authorization** asks whether a principal may perform the action on the target in the current context.
- A **policy decision point** evaluates facts and policy. A **policy enforcement point** mediates the action. A **control owner** has authority to define or accept the governed risk.
- An **exception path** handles legitimate cases outside the automated boundary with named ownership, evidence, time bounds, status, and re-entry or exit conditions.
- **Ambiguous commitment** means the consumer cannot tell whether an action took effect. A self-service contract must expose durable operation identity and observable state.
- **Revocation** removes previously granted access or capability; **reconciliation** moves observed state toward declared desired state.

### Central model, mechanism, or theorem

Model a self-service transaction as $X=(p,i,c,k)$: authenticated principal $p$, declared intent $i$, context $c$, and idempotency key $k$. The platform authenticates, validates, authorizes, plans, records a durable operation, enforces guardrails, executes or reconciles, exposes status and evidence, and supports cancellation, correction, revocation, and deletion. Guardrails are effective only when the valid path remains attainable and the denial or intervention is specific, safe to disclose, and actionable.

### Critical invariants

- Authentication, validation, and authorization remain distinct decisions with attributable evidence.
- The same declared intent receives compatible decisions across portal, CLI, API, and automation interfaces.
- Retries do not silently duplicate non-idempotent effects.
- Acceptance of an asynchronous request is not represented as completion.
- Defaults expose consequential assumptions; override and exception authority are explicit.
- Guardrails fail according to stated risk policy, not an accidental dependency timeout.
- Every created capability has ownership, observability, revocation, cleanup, and lifecycle controls.

### Common failures

Putting a form in front of a ticket queue; granting broad standing access to avoid friction; treating schema validity as authorization; hiding policy reasons; using warnings no one owns; blocking all work when a decision service fails; failing open by accident; making retries duplicate resources; automating creation but not deletion; and measuring request volume instead of independent safe outcomes.

### Compact example

A developer requests a production database by declaring application owner, data class, region, service tier, and recovery objectives. The platform authenticates workload and human identities, validates combinations, authorizes the owner and environment, previews cost and derived controls, returns a durable operation identifier, provisions through a reconciler, and exposes status, evidence, credentials, and deletion protection. An unsupported data class routes to a time-bounded specialist review. The journey is self-service for the supported class even though exceptions retain deliberate human authority.

### Connections

Retrieve the platform product and service promise from [PLAT-004](004-platform-as-product.md), cognitive-load boundaries from [PLAT-003](003-developer-cognitive-load.md), and consumer jobs from [PLAT-002](002-platform-consumers-and-jobs-to-be-done.md). The next module develops [paved roads and escape hatches](../roadmap.md#block-01--platform-engineering-foundations). Later modules own platform APIs, reconciliation, policy decision/enforcement architecture, admission control, and audit evidence in greater depth.

## Governing Question

When can an internal workflow honestly be called self-service, and how should guardrails constrain it without becoming hidden tickets, universal prohibitions, or unreviewed automation with a larger blast radius?

The answer must cover the whole journey. A request button is not self-service if fulfillment waits in a queue, failure requires private platform-team knowledge, or deletion needs an undocumented escalation. A preventive policy is not a useful guardrail if it cannot explain a valid route, distinguish risk classes, or survive its own failure mode. The design objective is safe independence within an explicit capability boundary.

## Why This Matters

Manual infrastructure and delivery workflows concentrate knowledge in specialist teams. Every routine request creates queueing, handoffs, status questions, duplicate interpretation, and inconsistent results. Human review is valuable where judgment and authority are genuinely required, but using it for deterministic translation and repeatable checks consumes specialist attention while teaching consumers to wait rather than operate independently.

Self-service changes coordination topology. Consumers act through a durable contract; automation handles repeatable mechanisms; control owners encode or expose policies; platform teams operate the capability rather than each request. The potential benefits are shorter feedback, consistent evidence, reduced toil, and greater autonomy. The same leverage magnifies defects: an unsafe default or authorization error can reach every consumer quickly.

Guardrails address that leverage by constraining the action space and detecting drift, but the metaphor can mislead. Real platform controls are not passive rails. They depend on identity, current context, policy data, enforcement placement, observability, ownership, and recovery. Some must prevent before action; some can detect after action; some restore or quarantine. Each has false-positive, false-negative, latency, availability, privacy, and bypass consequences.

Current CNCF platform guidance includes on-demand capabilities, self-service APIs, secure defaults, governance, and optionality. Google's SRE guidance recommends moving human-backed interfaces toward self-service while warning that automation safety checks can themselves dominate workload. NIST's current control catalog and zero-trust publications supply durable control and access principles. These sources justify explicit mechanisms and risk analysis; they do not prove that automation is safer than human review in every context.

## Prerequisites and Retrieval

Retrieve from PLAT-001 the rule that complexity moves rather than disappears. Retrieve from PLAT-002 the job, segment, alternative, evidence, and authority model. Retrieve from PLAT-003 the difference between removing avoidable burden and hiding accountable decisions. Retrieve from PLAT-004 product hypotheses, balanced outcomes, operating promises, and lifecycle ownership.

You should understand identity and access basics, APIs, asynchronous operations, idempotency, desired state, logging, service reliability, threat modeling, and the difference between policy and mechanism. Later modules deepen the implementation technologies; this chapter establishes the product and systems reasoning that those technologies must preserve.

## Learning Objectives

After completing this module, you should be able to:

1. test whether a journey is end-to-end self-service rather than a digital request channel;
2. separate authentication, structural and semantic validation, authorization, planning, execution, observation, and revocation;
3. classify preventive, detective, and corrective guardrails and choose placement from the risk and recovery model;
4. design honest asynchronous status, idempotent retry, diagnostics, and exception behavior;
5. distinguish safe defaults from concealed policy or universal configuration;
6. analyze fail-open, fail-closed, fail-static, degraded, and cached-decision behavior; and
7. measure safe independent outcomes, transferred burden, exceptions, and guardrail quality.

## Core Exposition

### Define end-to-end self-service

A journey is self-service when an eligible consumer can discover the capability, understand prerequisites and consequences, submit valid intent, receive an attributable decision, observe progress, use the outcome, diagnose expected failures, and terminate or revoke it without routine intervention by the platform team. “Routine” matters: rare exceptions and incident escalation do not invalidate self-service if the supported boundary and alternative path are explicit.

Self-service does not mean unauthenticated, unconstrained, instant, free, or implemented only by automation. A long-running environment build can be self-service when acceptance and progress are observable. A high-consequence change may deliberately require approval and therefore not be self-service at that boundary. Honesty is preferable to relabeling an approval queue as a guardrail.

Evaluate four dimensions:

- **initiation independence:** an eligible consumer can start through a stable contract;
- **decision independence:** deterministic valid cases do not wait for discretionary platform-team action;
- **execution independence:** progress does not depend on routine manual fulfillment;
- **recovery independence:** expected failure, retry, cancellation, cleanup, and support are documented and observable.

A workflow with three of four is partially automated, not fully self-service. This diagnosis identifies where coordination remains.

### Establish the capability contract

A self-service capability declares supported consumers, jobs, inputs, outputs, states, guarantees, errors, limits, costs, security responsibilities, evidence, support, compatibility, and lifecycle. It expresses consumer intent rather than exposing every provider field. The contract must also say what it does not support.

Model a request as $X=(p,i,c,k)$, where $p$ is the authenticated principal, $i$ declared intent, $c$ relevant context, and $k$ an idempotency key or equivalent request identity. Context can include tenant, environment, workload class, time, device or workload identity, data sensitivity, and current resource state. Authentication establishes evidence about $p$; it does not grant permission.

Process the request through distinguishable steps:

1. parse and structurally validate the representation;
2. resolve referenced resources and authoritative context;
3. semantically validate supported combinations and preconditions;
4. authorize $p$ to perform the action on the target under $c$;
5. derive a plan and make consequential defaults visible;
6. record the accepted operation and immutable request identity;
7. execute or reconcile while enforcing applicable controls;
8. publish status, evidence, outputs, errors, and next actions; and
9. support cancellation, compensation, revocation, deletion, and retention.

The order can be optimized to avoid information disclosure or cost, but the meanings must remain distinct. A malformed request is not an authorization denial. A valid request can be forbidden. An authorized request can be unsupported or conflict with current state.

### Use an explicit operation state model

For asynchronous work, distinguish request response from operation outcome. RFC 9110 defines `202 Accepted` as accepted for processing but not completed and notes that HTTP provides no later asynchronous response to that original exchange. A platform therefore needs an operation resource, event, callback, or other status mechanism rather than implying completion.

Let operation state $s$ belong to

$$
S=\{requested,validating,denied,accepted,reconciling,ready,degraded,failed,cancelling,cancelled,deleting,deleted\}.
$$

Define allowed transitions, terminal states, retry behavior, and what each state proves. `accepted` proves durable responsibility for attempting the operation under the contract; it does not prove the resource exists. `ready` must tie to capability-specific readiness, not mere provider object creation. `failed` needs a stable problem identity, safe detail, correlation, retry classification, and remediation or escalation.

An idempotency key binds retries to the same intended operation within a declared scope and lifetime. The service must define how it handles the same key with different intent. Idempotency prevents duplicate effects only when implemented through the entire side-effect boundary; deduplicating the first API handler while repeating a provider call is insufficient.

### Classify guardrails by control effect

A **preventive guardrail** blocks or transforms an action before the prohibited effect: authorization, schema and semantic validation, quotas, admission, safe parameter bounds, or deletion protection. A **detective guardrail** observes and reports undesirable state: drift detection, configuration scanning, cost anomaly alerts, expired ownership, or audit analysis. A **corrective guardrail** restores, quarantines, rolls back, rotates, or revokes after detection.

The categories can compose. A policy may prevent public exposure, detect provider-side drift, and correct it through reconciliation. Prevention is appropriate when consequence is unacceptable or recovery cannot restore the harmed state. Detection may be preferable when context is uncertain, blocking would create severe availability risk, and rapid correction is credible. Corrective automation requires an authority and conflict model; blindly reverting a legitimate emergency change can worsen an incident.

For each guardrail, record:

- the governed risk and control owner;
- authoritative policy and data sources;
- decision and enforcement locations;
- covered actions and explicit exclusions;
- failure behavior and cached or degraded modes;
- diagnostic disclosure and privacy limits;
- exception authority, duration, evidence, and review;
- detection and correction objectives; and
- tests, telemetry, false decisions, bypasses, and retirement.

### Design defaults and progressive constraints

A safe default reduces repeated decision work for a declared class while leaving consequential assumptions inspectable. It should be versioned, testable, observable, and reversible where possible. A default becomes hidden policy when consumers cannot discover its effect or owner. It becomes unsafe universalism when workload variation changes the right choice.

Use progressive constraint. First ask for domain declarations consumers own: service objective, data class, exposure, retention, or cost boundary. Derive implementation settings. Preview the plan and explain controls. Permit bounded configuration within the supported class. Route legitimate outliers to an extension or exception path. This preserves a small ordinary interface without denying complexity that actually matters.

Warnings are weak guardrails when consequences are severe, users are habituated, or no one owns response. Conversely, blocking every advisory issue can halt delivery and drive bypass. Match enforcement strength to consequence, evidence confidence, reversibility, and time sensitivity.

### Make denial and intervention actionable

A denial should identify the stable problem type, affected declaration, governing rule or category, relevant safe-to-disclose facts, remediation, documentation, exception path, decision time or policy version, and occurrence identifier. RFC 9457 supplies a standard problem-details model for HTTP APIs while warning against leaking implementation and sensitive information.

Separate “you are not authorized,” “this combination is unsupported,” “quota is exhausted,” “state changed,” “policy data is unavailable,” and “provider failed.” Consumers and automation need different next actions. Do not return a generic forbidden response merely because it is easier to implement.

Policy explanation has a security boundary. Revealing a secret detection rule, another tenant's existence, or sensitive resource attributes can create new risk. Provide the maximum actionable information allowed for the authenticated context, plus a correlation path for authorized support.

### Engineer failure behavior deliberately

A guardrail depends on identity, policy, data, and enforcement services. When one is unavailable, choices include:

- **fail closed:** reject or stop actions; protects against unreviewed change but can create a broad outage;
- **fail open:** permit action; preserves availability but accepts control risk;
- **fail static:** preserve last known safe state or allow only previously authorized operations;
- **cached decision:** reuse a time-bounded decision under strict identity, input, and revocation conditions;
- **degraded capability:** allow low-risk actions while blocking high-risk classes; or
- **manual emergency authority:** use a separately governed break-glass path with expiry and review.

There is no universal answer. Choose per action and consequence. A read-only catalog lookup and a production credential grant should not share accidental failure behavior. Exercise dependency loss, stale policy, clock skew, identity revocation, partial provider success, concurrent requests, and recovery after the decision system returns.

### Validate a small deterministic model

The following synthetic model separates validity, authorization, and supported risk class for four requests. It demonstrates decision ordering, not a production policy engine.

<!-- bijux-verify: {"id":"self-service-decision-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"dev-db=accepted\nbad-region=invalid\nforeign-owner=denied\nrestricted-data=exception\naccepted=1\n","stderr":""}} -->
```python
requests = [
    {"name": "dev-db", "valid": True, "authorized": True, "supported": True},
    {"name": "bad-region", "valid": False, "authorized": True, "supported": True},
    {"name": "foreign-owner", "valid": True, "authorized": False, "supported": True},
    {"name": "restricted-data", "valid": True, "authorized": True, "supported": False},
]

def decide(request):
    if not request["valid"]:
        return "invalid"
    if not request["authorized"]:
        return "denied"
    if not request["supported"]:
        return "exception"
    return "accepted"

decisions = [(request["name"], decide(request)) for request in requests]
for name, decision in decisions:
    print(f"{name}={decision}")
print(f"accepted={sum(decision == 'accepted' for _, decision in decisions)}")
```

The model ensures invalid input is not mislabeled as an authorization denial and an authorized but unsupported case does not silently enter the ordinary path. It does not authenticate identities, evaluate real policy, guarantee safe defaults, execute side effects, or prove exception legitimacy.

### Design exception and break-glass paths

An exception is part of the product, not an embarrassing side channel. It states eligibility, required evidence, decision owner, expected response time, status, expiry, compensating controls, audit, review, and how the case returns to the standard path or exits the platform. Recurring exceptions are product evidence: the contract may be too narrow, a segment may need a separate capability, or policy may be wrong.

Break-glass access is narrower. It exists for urgent conditions where ordinary control would cause greater harm. Require strong identity, reason, scope, time bound, notification, enhanced logging, automatic expiry, and independent post-event review. Do not make break glass the undocumented route for ordinary friction.

### Measure safe independence

Measure eligible end-to-end completion without intervention, time and waiting distributions, valid denial precision, remediation success, exception frequency and age, retry duplication, abandoned operations, revocation and cleanup, control bypass, incidents, consumer understanding, support demand, and platform/operator toil. Segment by journey, risk, experience, accessibility, and interface.

Request volume is ambiguous: growth can mean value, waste, loops, or automated retries. A low denial rate can mean good defaults or weak controls. A high denial rate can mean attacks, poor documentation, bad defaults, a mismatched capability, or an overbroad policy. Join quantitative signals with journey observation, support and incident review, and decision-owner analysis.

Protect telemetry from performance surveillance. Guardrail evidence often contains identity, resource, policy, and security-sensitive data. Minimize collection, control access, define retention, and separate individual investigation from aggregated product learning.

## Definitions and Notation

Let $P$ be principals, $I$ intents, $C$ contexts, and $K$ idempotency keys. A request is $X=(p,i,c,k)\in P\times I\times C\times K$. Let $V(X)$ mean semantically valid, $A(X)$ mean authorized, and $G(X)$ mean within the supported guardrail envelope. Ordinary acceptance requires $V(X)\land A(X)\land G(X)$, but acceptance still does not imply completed execution.

Let $S$ be operation states and $T\subseteq S\times S$ allowed transitions. A transition outside $T$ is invalid even if a provider reports a superficially similar state. Let $D$ be policy decisions, $F$ enforcement actions, and $E$ evidence. A decision is attributable when the platform can relate it to authenticated context, policy version, relevant inputs, enforcement result, and time without recording prohibited secrets.

A **control** is a safeguard or countermeasure selected to address risk. A **guardrail envelope** is the supported action and state space within which the platform can make its promise. A **quota** bounds consumption; it is not authorization by itself. A **precondition** protects an action against stale state. A **compensating action** addresses effects after partial success; it is not guaranteed rollback unless all relevant effects are reversible.

## Mechanisms, Invariants, or Proof Structure

Use this design and review sequence:

1. Define consumer job, eligibility, outcome, retained authority, and supported envelope.
2. Specify intent, identity, context, idempotency, states, outputs, errors, and lifecycle.
3. Separate structural validation, semantic validation, authentication, authorization, and supportability.
4. Threat-model ordinary, erroneous, malicious, concurrent, stale, partial, and dependency-failure cases.
5. Select preventive, detective, and corrective controls with named owners.
6. Define defaults, preview, decision explanation, exception, and break-glass behavior.
7. Implement durable operation identity, transitions, evidence, retry, cancellation, revocation, and cleanup.
8. Test all interfaces against one capability contract and policy meaning.
9. Observe safe independent outcomes and transferred burden, not request count alone.
10. Review decisions, exceptions, drift, incidents, versions, and retirement continuously.

The governing invariants are **decision separation**, **interface consistency**, **retry safety**, **state honesty**, **authority preservation**, **deliberate control failure**, and **lifecycle completeness**. Violating any one can create a superficially fast path that is not trustworthy self-service.

The claim “no human touched the request, therefore it is self-service” fails by counterexample. An automated request can create a resource, return success before readiness, provide no diagnostics, duplicate on retry, and require a private operator procedure to delete. Automation is therefore not sufficient. End-to-end independent, observable, and recoverable completion within a declared boundary is the stronger criterion.

## Alternatives and Trade-Offs

**Manual review versus encoded decision.** Human judgment handles ambiguity and novel high-consequence cases but introduces delay, inconsistency, and scaling limits. Encode stable repeatable policy; retain humans where evidence or authority cannot be reduced honestly to a deterministic rule.

**Prevent versus detect and correct.** Prevention avoids irreversible harm but can block legitimate work and become a critical dependency. Detection and correction preserve flow but accept exposure and require credible recovery. Choose from consequence and reversibility, not fashion.

**Broad standing privilege versus just-in-time grant.** Standing access avoids decision latency but expands misuse and compromise exposure. Time-bounded scoped grants reduce exposure but depend on reliable identity, policy, revocation, and emergency behavior.

**Central policy service versus distributed enforcement.** Central decision logic improves consistency and audit but can add latency and blast radius. Distributed controls improve locality and resilience but risk drift. Separate policy source, decision, distribution, enforcement, and evidence so the chosen topology remains testable.

**Fail closed versus availability.** Blocking on uncertainty suits some irreversible high-risk changes. It can be dangerous for recovery or safety operations. Define degraded and emergency modes per action rather than one global switch.

**Simple interface versus full control.** Meaningful defaults reduce ordinary choices. Experts and unusual workloads need inspection and bounded extension. Progressive disclosure and stable declarative APIs can serve both without exposing every provider detail to everyone.

## Failure Modes and Misconceptions

- **A portal makes a workflow self-service.** Interface location says nothing about fulfillment, recovery, or hidden coordination.
- **Authenticated means authorized.** Identity evidence is an input to a contextual permission decision.
- **Valid means safe.** Schema and semantic validity do not establish permission, truth, or acceptable risk.
- **Accepted means ready.** Asynchronous acceptance establishes responsibility for processing, not successful outcome.
- **Automation is deterministic.** Dependencies, concurrency, time, stale data, and partial effects still produce uncertainty.
- **Guardrails are only blockers.** Detection, correction, explanation, expiry, and recovery can be more appropriate mechanisms.
- **Fail closed is always secure.** A control outage can prevent incident response, revocation, or safety restoration.
- **Exceptions weaken governance.** Governed exceptions expose legitimate variance; secret bypasses weaken governance.
- **Defaults remove responsibility.** Consumers and control owners retain the decisions assigned to them.
- **Creation is the whole lifecycle.** Ownership, observation, change, revocation, deletion, retention, and retirement are part of self-service.

## Worked Examples

### Example 1

**Situation:** A web form creates a service ticket for namespace provisioning. **Reasoning:** Initiation is digital, but decision, execution, status, and recovery depend on a platform operator. Map the deterministic checks, define an intent contract, automate supported cases, and leave only explicit exceptions in the queue. **Conclusion:** The form is a request channel, not yet end-to-end self-service.

### Example 2

**Situation:** A retry after a timeout creates two databases. **Reasoning:** The client could not distinguish lost response from uncommitted action, and the provider call lacked end-to-end deduplication. Bind a durable operation to an idempotency key and intent digest, return the same operation on retry, and reject key reuse with different intent. **Conclusion:** Retry semantics are part of the capability contract.

### Example 3

**Situation:** An authenticated developer requests another team's production secret. **Reasoning:** Successful authentication proves an identity claim, not target permission. Authorization must evaluate subject, target owner, environment, purpose or role, and current policy; denial must avoid leaking secret existence beyond the authorized context. **Conclusion:** Authentication and authorization are distinct guardrails.

### Example 4

**Situation:** Policy evaluation is unavailable during a production incident. **Reasoning:** Globally failing closed may block recovery, while failing open may enable broad mutation. Permit predeclared low-risk reads, use a tightly scoped time-bound break-glass recovery role, block unrelated high-risk changes, and record independent review evidence. **Conclusion:** Degraded behavior must follow the action-specific risk model.

### Example 5

**Situation:** A linter warns that every service lacks ownership metadata, but teams ignore it. **Reasoning:** The organization relies on ownership for incidents and access review, so an unactioned warning is insufficient. Make ownership a validated declaration for new services, detect legacy gaps, assign a migration deadline, and define emergency correction. **Conclusion:** Enforcement strength should match the consequence and transition plan.

### Example 6

**Situation:** A cost quota blocks a legitimate seasonal workload. **Reasoning:** The quota controls consumption but does not determine business authority. Show current usage and forecast, identify the budget owner, support a time-bounded reviewed increase, and expire it automatically. **Conclusion:** A guardrail needs an explainable and governed exception path.

### Example 7

**Situation:** The portal permits a configuration that the CLI rejects. **Reasoning:** Each interface implemented its own defaults and validation. Move semantics into one versioned capability contract and decision service or shared conformance suite; keep interface-specific presentation only. **Conclusion:** Multiple interfaces must preserve one intent and guardrail meaning.

### Example 8

**Situation:** Reconciliation detects public exposure and immediately restores private access. **Reasoning:** Correction limits duration, but repeated drift may indicate another controller, an emergency action, or the wrong desired state. Record attribution, alert the owner, detect conflict, and pause destructive oscillation. **Conclusion:** Corrective guardrails need authority and conflict handling, not blind loops.

### Example 9

**Situation:** A deleted development environment leaves credentials and backups. **Reasoning:** Compute deletion is not lifecycle completion. The contract must enumerate dependent resources, retention duties, revocation order, evidence, and irreversibility. **Conclusion:** Self-service deletion includes governed cleanup and retained-record handling.

### Example 10

**Situation:** A clinical research platform self-serves access to sensitive cohorts. **Reasoning:** The platform can validate protocol identifiers, identity, approved purpose, minimum cohort rules, time bounds, audit, and revocation. Ethics, privacy, legal, and data-governance authorities decide whether the use is permissible; researchers remain responsible for interpretation and downstream handling. **Conclusion:** Automation enforces authorized declarations but cannot create ethical or legal authority.

## Cross-Program Connections

- **API engineering:** idempotency, asynchronous operation resources, status semantics, problem details, and compatibility make self-service contracts automatable.
- **Security engineering:** identity, contextual authorization, least privilege, decision/enforcement separation, audit, revocation, and break glass shape guardrails.
- **Distributed systems:** partial failure, retry, concurrency, reconciliation, stale policy, and ambiguous commitment govern real behavior.
- **Reliability engineering:** control dependencies, degraded modes, recovery, and blast radius determine whether safe defaults remain safe in production.
- **Human-computer interaction:** progressive disclosure, actionable errors, accessibility, confirmation, and mental models determine whether valid paths are attainable.
- **Data governance:** provenance, retention, purpose, disclosure, and deletion require authorities beyond platform mechanics.
- **Organizational design:** self-service removes routine coordination only when ownership and exception boundaries are explicit.

## References

- CNCF TAG App Delivery, [*CNCF Platforms White Paper*](https://tag-app-delivery.cncf.io/whitepapers/platforms/), 2023. Current platform guidance on on-demand capabilities, self-service interfaces, secure defaults, governance, optionality, and platform-team ownership.
- DORA, [*2024 Accelerate State of DevOps Report*](https://dora.dev/research/2024/dora-report/), corrected edition v2024.3. Empirical discussion of highly automated self-service golden paths, user-centeredness, developer independence, and mixed platform outcomes.
- Google, [*Operational Efficiency: Eliminating Toil*](https://sre.google/workbook/eliminating-toil/), *Site Reliability Workbook*, 2018. Human-backed interfaces, self-service automation, safety checks, maintenance, and automation trade-offs.
- NIST, [SP 800-53 Rev. 5, Release 5.2.0 — *Security and Privacy Controls for Information Systems and Organizations*](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final), 2025. Current control catalog covering access, audit, configuration, contingency, identity, incident response, privacy, risk, and integrity.
- NIST, [SP 800-207 — *Zero Trust Architecture*](https://csrc.nist.gov/pubs/sp/800/207/final), 2020. Resource-focused access, removal of implicit trust, and discrete authentication and authorization.
- NIST, [SP 800-207A — *A Zero Trust Architecture Model for Access Control in Cloud-Native Applications in Multi-Cloud Environments*](https://csrc.nist.gov/pubs/sp/800/207/a/final), 2023. Identity-tier and application/service-identity access control for cloud-native systems.
- IETF, [RFC 9110 — *HTTP Semantics*](https://www.rfc-editor.org/rfc/rfc9110.html), 2022. Request semantics, authorization, preconditions, status codes, and the bounded meaning of `202 Accepted`.
- IETF, [RFC 9457 — *Problem Details for HTTP APIs*](https://www.rfc-editor.org/rfc/rfc9457.html), 2023. Current standard for machine-readable problem types, occurrence details, extensions, remediation documentation, and security considerations.

## Exercises

### Exercise 1

Evaluate a workflow in which a consumer submits a portal request, a platform engineer approves it, automation provisions it, and deletion requires a ticket. Classify its four self-service dimensions and state the smallest honest improvement.

### Exercise 2

Derive an operation state model for rotating a service credential. Include validation, authorization, issuance, overlap, consumer rollout, revocation, failure, cancellation, and evidence. Identify which transitions must be idempotent.

### Exercise 3

A central policy decision service becomes unavailable. Design fail behavior for documentation reads, development environment creation, production deployment, credential revocation, and emergency rollback. Justify differences.

### Exercise 4

Compare a preventive policy that blocks all unapproved container images with a detective-and-corrective system that quarantines workloads after scanning. Evaluate irreversible harm, latency, availability, evidence confidence, and recovery.

### Exercise 5

Transfer the model to a municipal emergency shelter platform that lets authorized agencies request capacity, staff access, and sensitive resident-data views. Define self-service boundaries, guardrails, exceptions, and authorities.

## Answers to the Exercises

### Answer 1

Initiation independence exists because the consumer can submit through a stable interface. Decision independence does not exist because routine approval waits for a platform engineer. Execution independence exists after approval if automation completes without manual fulfillment. Recovery independence is incomplete because deletion requires a ticket and likely carries hidden status and cleanup. The honest label is a partially automated request workflow. The smallest improvement is not necessarily eliminating approval: first determine whether approval applies deterministic rules. Encode supported cases with explainable authorization, retain explicit human review only for genuine exceptions, and add observable governed deletion. If approval carries non-delegable judgment, say that the journey is approval-mediated rather than self-service.

### Answer 2

Use `requested → validating → denied|authorized → issuing → overlap_active → consumer_rollout → revoking_old → complete`, with `failed`, `cancelling`, and `cancelled` branches. Validation checks identifiers and supported overlap; authorization checks service ownership and environment; issuance creates the new version without revoking the old; overlap exposes both under a deadline; rollout evidence confirms consumers; revocation removes old access; completion records the active version and evidence. Retry of request, issuance, status update, and revocation must be idempotent. Cancellation before issuance can terminate directly; after issuance it must revoke the new credential or record why compensation failed. Failure must identify whether old access remains valid, because that determines service safety.

### Answer 3

Documentation reads can remain available because they do not grant or mutate resources. Development creation may use time-bounded cached policy for previously eligible low-risk classes, or pause if inputs cannot be verified. Production deployment should generally preserve current state and block new high-risk changes unless a separately governed emergency path applies. Credential revocation should remain available through a resilient direct path because blocking it can extend compromise. Emergency rollback needs predeclared, tightly scoped break-glass authority with strong identity, expiry, notification, and review. The distinctions follow consequence, reversibility, current versus new privilege, and the harm of inaction; one global fail-open or fail-closed setting is indefensible.

### Answer 4

Prevention is favored when an unapproved image can cause rapid irreversible disclosure or execution and the allow decision is reliable, low-latency, and highly available. It can block urgent recovery when scanners or metadata fail and may encourage bypass if explanations are poor. Detection and quarantine preserve startup availability and accommodate uncertain results, but accept an exposure window and require trustworthy isolation and fast response. A risk-tiered design can prevent known-malicious, unsigned, or prohibited sources; allow a narrow attested emergency set; and detect lower-confidence vulnerabilities with deadlines or quarantine. Measure false decisions, decision latency, exposure duration, bypass, recovery, and control outages.

### Answer 5

Agencies can self-serve ordinary capacity requests within declared jurisdiction, time, shelter class, staffing, and resource limits; the platform validates identity, authority, duplication, capacity, accessibility, and audit requirements and exposes durable status. Staff access can be time-bounded and role-scoped with automatic expiry and revocation. Sensitive resident-data views require purpose, minimum necessary scope, and policy authority; some may require explicit privacy or incident-command approval and should not be mislabeled self-service. Exceptions include cross-jurisdiction overflow, exhausted capacity, disconnected operation, and urgent life-safety access, each with named authority, expiry, compensating controls, and review. The platform cannot decide emergency policy, resident eligibility, medical suitability, or lawful disclosure; municipal incident command, shelter operators, privacy/legal authorities, accessibility specialists, and affected communities retain those decisions.
