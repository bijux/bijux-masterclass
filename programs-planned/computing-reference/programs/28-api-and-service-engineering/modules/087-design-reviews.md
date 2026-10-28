---
module_id: API-087
program: API & Service Engineering
level: 2
module_number: 87
title: Design Reviews
status: complete
last_verified: 2026-09-02
---

# Design Reviews

## One-Page Review

### Governing question

What evidence, participants, timing, questions, findings, and decision rules make an API design review an effective risk-reduction mechanism rather than a late syntax inspection, popularity vote, or ceremonial gate?

### Essential definitions

- An **API design review** is a structured, evidence-based evaluation of an interface decision before its cost of change becomes unacceptable.
- A **review scope** names the consumers, operations/events, protocol, exposure, lifecycle state, dependencies, risks, and decision being evaluated.
- **entry criteria** are the minimum artifacts and resolved discovery questions required for useful review.
- A **finding** is a traceable claim about a risk, requirement, ambiguity, or opportunity, with evidence, severity, owner, and closure condition.
- A **blocker** is an unresolved condition whose consequence/authority prevents the proposed decision from proceeding.
- **conditional approval** permits a defined next action only after or subject to explicit conditions; it is not “approved with forgotten comments.”
- A **dissent record** preserves a material unresolved technical judgment and escalation path rather than manufacturing consensus.
- A **re-review trigger** is a material change or new evidence that invalidates the scope, assumptions, or prior decision.

### Central model, mechanism, or theorem

Let required evidence domains for proposal $p$ be $D(p)$, supplied adequate evidence be $E(p)$, blockers be $B(p)$, and valid explicitly accepted risks/exceptions be $X(p)$. Approval is conjunctive:

$$
\operatorname{approve}(p) \Rightarrow D(p)\subseteq E(p) \land \forall b\in B(p):\operatorname{closed}(b)\lor b\in X(p).
$$

It is not a majority of checklist items or reviewers. Scope/authority determine which evidence and risks are mandatory. A decision record links proposal/version, participants/conflicts, evidence, findings, dispositions, dissent, conditions, expiry, and re-review triggers.

### Critical invariants

Review happens early enough to change resource/operation/event boundaries, then again at contract and launch readiness as risk demands. Consumer tasks and system behavior lead; schema cosmetics follow. Reviewers examine protocol semantics, domain/state, security/privacy, compatibility/lifecycle, reliability/distribution, operability/cost, documentation/SDK experience, and ownership/support.

Authors retain design ownership; reviewers own independent challenge and evidence quality; named authorities own nondelegable decisions. Findings are specific, risk-linked, non-duplicative, and closable. Approval names exact artifact revisions and conditions. Material changes trigger re-review. No linter, checklist score, seniority, meeting attendance, or silence substitutes for evidence.

### Common failures

Review after implementation; no consumer/problem evidence; giant meeting as first feedback; reviewers read during meeting; missing decision scope; bikeshedding names while ignoring authorization/state; style guide treated as complete; security/operations invited too late; absent consumer advocate; authority and advice confused; majority vote on correctness; status/title dominance; vague “consider” comments; duplicate/conflicting findings; approval with unresolved blockers; conditions not tracked; rubber-stamped exceptions; review queue with no SLO; redesign by committee; undocumented dissent; artifact changes after approval; no re-review triggers; and counting review completion rather than escaped defects/outcomes.

### Compact example

A payment API review sees a valid OpenAPI file and perfect style linting. A state-transition walkthrough reveals `POST /refunds` can be retried after a timeout without an idempotency key, while object authorization is specified only at collection level. Both are blocking because duplicate effects and cross-merchant access are plausible. The team adds idempotency semantics, object-scoped authorization evidence, failure tests, and operational reconciliation; reviewers then approve the exact revision. **Conclusion:** review evaluates behavior and risk, not document neatness.

### Connections

[Outside-In API Requirements](011-outside-in-api-requirements.md) supplies consumer tasks. [Reviewing a Contract](030-reviewing-a-contract-for-ambiguity-and-incompleteness.md) supplies contract interrogation. [API Threat Modeling](041-api-threat-modeling.md), [Compatibility](081-backward-and-forward-compatibility.md), [Consumer Inventory](085-consumer-inventory-and-usage-evidence.md), and [API Style Guides](086-api-style-guides.md) provide required evidence. The next module on schema registries will operationalize approved artifacts.

## Governing Question

How should teams prepare, conduct, decide, record, and follow through on API design reviews so important consumer, semantic, security, compatibility, reliability, operational, and lifecycle risks are found while change remains affordable?

## Why This Matters

API decisions harden early. Once consumers generate clients, store identifiers, build workflows, depend on errors, or interpret events, even a small correction can require coordinated migration. A review held after implementation often chooses between accepting known harm and delaying a launch; an early review can still reshape the model.

Yet early designs are incomplete. Requiring production-ready detail before feedback wastes work and creates false certainty. Review should be progressive: problem/task and boundaries first, contract semantics next, implementation/launch evidence later. The rigor and independence scale with exposure, reversibility, security/privacy, criticality, consumer count, and novelty.

An API spans disciplines. Domain experts know invariants, consumers know tasks, protocol experts recognize semantic traps, security reviewers challenge trust, reliability reviewers trace failure, and operators see observability/recovery gaps. None alone is sufficient. A large undirected meeting is also insufficient; it amplifies status and diffusion of responsibility.

The durable output is not the meeting. It is the decision and evidence graph: what was reviewed, which revision, against which rules and risks, who had authority, what findings exist, how each closes, what uncertainty was accepted, and what change requires reconsideration. That record accelerates later evolution and incident learning.

## Prerequisites and Retrieval

Retrieve [Outside-In API Requirements](011-outside-in-api-requirements.md), [Designing an API from Consumer Tasks](020-designing-an-api-from-consumer-tasks-rather-than-database-tables.md), [API Contracts and Behavioral Guarantees](021-api-contracts-and-behavioral-guarantees.md), [Reviewing a Contract for Ambiguity and Incompleteness](030-reviewing-a-contract-for-ambiguity-and-incompleteness.md), [API Threat Modeling](041-api-threat-modeling.md), [Choosing an Interface Style](060-choosing-an-interface-style-from-interaction-semantics.md), [Backward and Forward Compatibility](081-backward-and-forward-compatibility.md), [Consumer Inventory](085-consumer-inventory-and-usage-evidence.md), and [API Style Guides](086-api-style-guides.md).

Retrieve consumer/problem research; domain glossary/invariants/state transitions; context and sequence diagrams; protocol/style applicability; draft contract/examples; authorization/data classification/threat model; compatibility/version/deprecation plan; dependency and consumer inventory; latency/volume/failure/retry/idempotency/consistency budgets; quotas/cost/capacity; observability/SLO/incident/rollback/recovery plans; SDK/documentation/onboarding prototypes; alternatives and decisions; prior findings/incidents/exceptions; and exact artifact revisions.

## Learning Objectives

After completing this module, you can:

1. choose review timing, depth, independence, and authority from API risk and reversibility;
2. define scope, entry criteria, evidence bundle, participants, roles, and conflicts of interest;
3. run progressive discovery, contract, security/reliability, and launch-readiness reviews;
4. examine consumer tasks, domain/state semantics, protocol/style, security/privacy, compatibility, failure, operations, and product ownership;
5. turn comments into traceable findings with severity, evidence, owners, dispositions, and closure tests;
6. distinguish advisory feedback, blocking authority, accepted risk, exception, dissent, and conditional approval;
7. make decisions without checklist arithmetic, majority-vote theater, or title dominance;
8. define re-review triggers and protect approved artifact/revision integrity;
9. operate a responsive review system with asynchronous preparation, facilitation, SLOs, appeals, and feedback; and
10. measure risk reduction, escaped problems, rework timing, reviewer quality, and consumer outcomes.

## Core Exposition

### Classify the review and decision

Name the decision: validate the problem/boundary, select interaction style, approve a public contract, accept a compatibility exception, authorize a security-sensitive behavior, or verify launch readiness. “Review the API” is too broad.

Classify exposure, consumer diversity, criticality, data sensitivity, financial/safety effect, novelty, dependencies, distribution/failure complexity, expected longevity, reversibility, and migration cost. These determine required authorities and evidence—not how important the sponsoring executive considers the deadline.

Use progressive checkpoints. A discovery review tests consumer tasks, domain boundaries, alternatives, and interface style. A contract review tests exact semantics/evolution. A readiness review tests implementation, operations, capacity, security, documentation, and support. Low-risk changes can combine them; high-risk ones should not wait for one final council.

Write scope inclusions/exclusions and affected artifact revisions. A review of “v1 OpenAPI” does not approve an undocumented event stream or future behavior.

### Define roles, independence, and authority

The author/owner explains intent, supplies evidence, answers questions, and resolves findings. A facilitator sets scope, prepares reviewers, manages time/equity, separates findings from solution brainstorming, and records decisions. A scribe captures exact outcomes if tooling does not.

Select reviewers for consumer/product, domain/data, protocol/style, implementation, security/privacy, reliability/distribution, operations/platform, documentation/SDK, and compatibility/lifecycle concerns as applicable. Invite a real consumer or credible consumer advocate for consequential external APIs.

Name decision authority per domain. Security can block a non-waivable exposure; protocol governance can reject a contradiction; product ownership can accept bounded business risk within policy. A generic chair cannot silently overrule all domains.

Independence means someone outside the implementation’s incentives can challenge high-risk assumptions. Disclose conflicts, prior authorship, reporting pressure, and missing expertise. Independence does not require hostility or ignorance of context.

### Establish entry criteria and evidence

Entry criteria prevent meetings spent discovering the problem statement. Require decision/scope, consumer tasks, proposed semantics, key alternatives, known constraints, risk classification, exact draft artifacts, unanswered questions, and named owners. Later checkpoints require fuller evidence.

Reject false completeness. A syntactically valid OpenAPI document does not establish domain correctness, runtime authorization, compatibility, or operational readiness. Conversely, do not demand implementation details during boundary discovery.

Create a short reviewer brief with links to canonical artifacts, focused questions, changes since prior review, and deadline. Provide enough lead time for asynchronous reading. Mark confidential/security material and control access without hiding essential risk from authorized reviewers.

Validate evidence freshness and provenance. A capacity test on old schema, threat model before a new bulk operation, or consumer inventory missing a gateway cannot support the current decision.

### Review consumer tasks and domain semantics

Ask who the consumer is, what outcome they need, which workflows and failure/recovery paths exist, and why this boundary is owned here. Walk representative and adversarial stories, not only endpoint lists.

Trace domain identities, states, transitions, invariants, commands, queries, events, temporal rules, money/units, ownership, and source of truth. Challenge table-shaped APIs that leak persistence rather than stable consumer concepts.

For each operation/event, state preconditions, authorization, idempotency/safety, success effect, errors, partial outcomes, concurrency, consistency/visibility, retries, side effects, and observability. Draw state/sequence diagrams when prose hides ordering.

Review names after semantics are clear. A perfectly named resource with incoherent identity or lifecycle is still a bad interface.

### Review protocol, contract, and style

Confirm interaction style fits semantics: synchronous resource, RPC/command, GraphQL, stream, event, or webhook. Then apply its standards and scoped style profile. Never force a REST rule onto a different model.

For HTTP, inspect method safety/idempotency, status/error meaning, headers/metadata, negotiation, caching/conditions, long-running/batch behavior, pagination/filter/sort, concurrency, and redirects. For RPC/GraphQL/events, inspect their corresponding schema, deadlines/streaming, selection/cost, topic/key/order/delivery/replay semantics.

Interrogate required/optional/null/default, enum openness, unions/polymorphism, constraints, time/units/money, unknown fields, duplicate/reordered elements, examples, and ambiguity. Validate description syntax with the correct spec edition and lint profile.

Style findings should cite stable rule IDs and applicability. If the guide conflicts with protocol or consumer correctness, escalate the guide problem rather than force a harmful design.

### Review security, privacy, and abuse

Start from assets, actors, trust boundaries, attacker capabilities, entry points, and abuse cases. Trace authentication context through proxies/services; evaluate action and object/property authorization separately. Review tenant isolation and ownership at every identifier.

Challenge enumeration, overposting/mass assignment, excessive data exposure, unsafe upstream/downstream API consumption, unrestricted resource use, SSRF/injection, replay, signing, credential/token handling, rate/quota economics, and inventory/lifecycle. OWASP’s API Security Top 10 is a prompt set, not a complete threat model.

Review sensitive input/output/error/log/trace behavior, data minimization, retention, residency, deletion, consent/purpose, and support access. Examples and mocks must not embed real secrets or personal data.

Security findings include exploit path, affected asset/tenant, preconditions, consequence, evidence, control, verification, and residual risk. Severity is consequence-based, not a vote.

### Review compatibility and lifecycle

Classify existing consumers and every contract dimension: syntax, structure, semantics, timing, ordering, security, quota, errors, defaults, and operations. “Additive schema” can still be behaviorally breaking.

For new APIs, review how unknown fields/enums, optionality, defaulting, identifiers, pagination tokens, and error types can evolve. For changes, produce semantic diff, consumer inventory/use evidence, migration path, version selection, deprecation/sunset, and rollback.

Generated SDKs and documents are consumers of the description. Check whether operation IDs, names, unions, nullable patterns, or response variations produce usable artifacts.

An exception that preserves compatibility may be better than stylistic cleanup. Record the debt and prevent unsafe new adoption; do not authorize breaking changes merely because reviewers prefer uniformity.

### Review reliability and distributed behavior

Trace deadlines through call graphs, retry/backoff/hedging, idempotency keys, deduplication, concurrency control, partial results, load shedding, backpressure, circuit/bulkhead behavior, ordering, consistency, and read-after-write expectations.

Use failure scenarios: dependency slow/down, duplicate/reordered request/event, response lost after commit, client retry storm, regional partition, stale replica, queue backlog, poison event, schema skew, clock error, and telemetry loss. State who owns recovery and what consumers observe.

Quantify expected volume, concurrency, payload, fan-out, latency budget, retry amplification, quotas, capacity headroom, and cost. Numbers need provenance/distribution, not only averages.

Review failover, rollback, replay, reconciliation, data/state migration, and disaster paths. A rollback that restores code but cannot reverse schema/state or consumer effects is incomplete.

### Review operability and product experience

Require accountable owner, support/escalation, lifecycle tier, SLO/availability/latency/error semantics, dependency map, dashboards/alerts, correlation, audit, deployment/rollback, incident runbooks, capacity/cost, and deprecation communication.

Observe what happens for unknown operation/version, invalid auth, denied object, quota, overload, timeout, dependency failure, partial result, duplicate, and incompatible consumer. Operators need stable signals without secrets/high-cardinality leakage.

Walk first-use experience: discovery, access request, credentials, sandbox/mocks, docs/examples, SDK generation, successful call, error diagnosis, limits, support, and change subscription. A design can be semantically sound yet unusable.

Google SRE’s launch work describes cross-team launch coordination and reusable checklists for reliability. Use checklists as memory and preparation, not as arithmetic proof of readiness.

### Convert discussion into findings

Record findings during asynchronous review and meeting synthesis. Each has durable ID, category/authority, exact artifact revision/location, observation, evidence, violated requirement or risk, consequence, severity, required outcome (not overprescribed implementation), owner, due/checkpoint, verification, status, and related findings.

Use clear severity definitions: blocker before named action; major before launch or with approved bounded risk; minor improvement; question requiring answer; commendation/decision note when useful. Avoid “nit” volume that obscures risk.

Deduplicate and reconcile conflicts. If one reviewer requests caching and another forbids it for privacy, surface the underlying constraints and decide explicitly. Do not make the author arbitrate hidden authorities alone.

Disposition is fixed, accepted with remediation, accepted risk/exception, not applicable with evidence, superseded/duplicate, or unresolved/escalated. “Won’t fix” without authority/rationale is not closure.

### Make and record the decision

Possible decisions include approved for exact next step, conditionally approved with enumerated preconditions, changes required/re-review, rejected with reasons/alternatives, or deferred for missing evidence. Define them before the review system operates.

Do not vote on factual protocol/security correctness. Seek informed agreement, but named authority and evidence resolve decisions. Record material dissent, uncertainty, and escalation. Silence or absence is not approval when required expertise/authority is missing.

The decision record names proposal/artifact commits/digests, scope/exclusions, guide/spec versions, risk class, participants/roles/conflicts, evidence reviewed, findings/dispositions, authorities, conditions, accepted risks/exceptions, dissent, effective/expiry dates, and re-review triggers.

Conditional approval has machine-visible tracked conditions and blocks the named action until satisfied where required. Verify closure against evidence; checking a box or resolving a comment thread is insufficient.

### Define re-review and change control

Trigger re-review for material consumer/task/boundary changes; new operations/events/fields with risk; authentication/authorization/trust changes; data sensitivity/residency; protocol/spec/profile version; breaking or semantic change; retry/idempotency/consistency behavior; dependency/fan-out; scale/SLO/cost; deployment topology; major incident/vulnerability; exception expiry; or divergence between contract and runtime.

Not every typo requires the council. Define risk-based change categories and lightweight paths. Automated semantic diff and ownership routing help, but reviewers confirm materiality.

Protect approved revision integrity. Registries/CI compare the released artifact and governed generated outputs to the decision. Emergency changes follow an explicit expedited path with retrospective evidence and follow-up, not an undocumented bypass.

Invalidate or supersede old decisions rather than silently editing them. Later teams must reconstruct what evidence governed which release.

### Operate and improve the review system

Publish intake, entry criteria, templates, reviewer domains, office hours, service-level response targets, escalation/appeal, and status. Triage quickly and route narrowly; not every API needs every reviewer in one meeting.

Prefer asynchronous annotations and focused sessions for unresolved cross-domain trade-offs. Facilitation prevents status dominance, solution fixation, and endless restatement. Timebox without approving on deadline pressure.

Build reviewer calibration with paired reviews, example findings, incident retrospectives, and feedback. Rotate membership while maintaining domain continuity. Compensate review work; invisible volunteer governance becomes a bottleneck.

Measure lead/wait/touch time, stage when material issues found, rework avoided, finding recurrence/escape, false-positive/appeal outcomes, condition closure, exception age, post-launch incidents, consumer onboarding/support, and reviewer/author experience. Never reward number of comments or approval rate.

## Definitions and Notation

Let proposal $p$ identify exact artifacts and decision scope. $D(p)$ is the set of required evidence domains after risk/applicability classification; $E(p)$ is the subset supplied with adequate, fresh evidence. $B(p)$ is material blockers, and $X(p)$ valid accepted risks/exceptions issued by proper authority.

Necessary approval conditions include $D(p)\subseteq E(p)$ and every blocker closed or validly accepted. These are necessary, not a guarantee of future success. Let $t_f$ be time a material finding is discovered and $t_c$ the point its affected decision becomes costly/irreversible; useful early review seeks $t_f<t_c$.

A **condition** is a tracked prerequisite/obligation attached to a decision. **Closure evidence** proves its required outcome. A **review revision** is the immutable artifact identity evaluated. A **decision authority** owns a bounded risk domain; a **facilitator** owns process, not all technical risk.

## Mechanisms, Invariants, or Proof Structure

**Evidence-set argument.** If required domain $d\in D(p)$ is absent from $E(p)$, the review has no adequate basis for that domain. Many supplied naming/schema artifacts cannot logically establish the missing authorization or recovery claim. Therefore checklist percentage cannot substitute for required-domain coverage.

**Blocker conjunction.** Suppose ten blockers are identified and nine close. The remaining blocker permits cross-tenant access. A 90% blocker-closure score does not make release acceptable. Therefore approval requires every applicable blocker closed or accepted through proper explicit authority; risks are not averaged.

**Timing argument.** Before consumer/code/state commitments, boundary change cost is relatively low. After release, the same correction requires compatibility and migration. Therefore progressive review should challenge high-leverage assumptions before $t_c$, while later reviews verify exact contract/runtime readiness.

**Artifact-identity counterexample.** Revision A is approved; revision B later changes a field from optional to required without review. The decision record still says “approved,” but its evidence applies to A. Therefore approval without immutable artifact identity cannot establish that the released revision was reviewed.

Operational invariants are: decision/scope explicit; risk determines rigor; evidence fresh/provenanced; required expertise/authority present; consumer and semantics before cosmetics; findings traceable/closable; blockers conjunctive; dissent/accepted risk visible; decision bound to exact revision; conditions tracked; material changes re-reviewed; and outcomes used to improve the system.

## Alternatives and Trade-Offs

Central review boards improve consistency/independence but can bottleneck and lose domain context. Fully team-local review is fast but can miss systemic standards and conflict. Use federated domain reviewers with common policy, risk routing, and escalation.

Synchronous meetings resolve cross-domain trade-offs but consume scarce time and amplify status. Asynchronous review supports depth/time zones but can fragment discussion. Prepare asynchronously, meet only for decisions and unresolved interactions.

Comprehensive checklists reduce omission but encourage box-ticking and grow without bound. Principle-only review is flexible but inconsistent. Use risk-routed evidence prompts plus trained judgment and incident-driven calibration.

Mandatory consumer participation improves usability but may be impractical before a market exists or for confidential APIs. Use research/prototypes/consumer advocates, then validate assumptions through beta evidence.

Unanimous consensus reduces social conflict but gives hidden vetoes and false agreement. Majority vote is fast but inappropriate for standards/security facts. Name authorities, seek reasoned agreement, record dissent, and escalate bounded questions.

Strict re-review protects decisions but creates churn for trivial edits. Self-attestation is fast but can hide material drift. Define semantic/risk triggers, automate diffs, audit classifications, and keep expedited paths.

## Failure Modes and Misconceptions

- “The review is the meeting.” Preparation, findings, decision, closure, and change control are the review.
- “Valid OpenAPI means good design.” Syntax cannot prove domain, security, or runtime behavior.
- “The style guide covers everything.” It standardizes known patterns; judgment and evidence remain.
- “More reviewers means safer.” Missing ownership and focus create diffusion.
- “The senior person decides correctness.” Authority is bounded and evidence remains inspectable.
- “Consensus means no risk.” Groups can share assumptions or suppress dissent.
- “Ninety percent of blockers closed is enough.” One remaining blocker can dominate consequence.
- “Security can review before launch.” Trust and data boundaries may already be irreversible.
- “Names first.” Resource identity, state, effects, and consumer tasks come first.
- “Reviewers should redesign it.” They state risks/outcomes; authors retain coherent design ownership.
- “Approve with comments.” Conditions and findings need owners, gates, and closure evidence.
- “No response means approval.” Required absent authority/expertise is an evidence gap.
- “A checklist proves launch readiness.” It prompts questions; evidence supports decisions.
- “Approved once means approved forever.” Material changes and expired assumptions trigger re-review.
- “Comment count measures quality.” It rewards noise and discourages clear designs.
- “Deadline lowers risk.” Urgency changes process speed, not consequence or evidence needs.

## Worked Examples

### Example 1

Discovery review of a table-shaped orders API maps consumer tasks and reveals returns have a separate lifecycle/owner. The boundary changes before schema generation, avoiding a later breaking split.

### Example 2

An OpenAPI linter reports zero findings. Reviewers execute a state walkthrough and find `GET /activate` mutates state. Protocol semantics block approval despite perfect syntax conformance.

### Example 3

A bulk export adds unbounded fan-out. Reliability review computes dependency/capacity budgets, adds asynchronous job semantics, quotas, progress/cancel, and partial-failure evidence before contract approval.

### Example 4

Ten blockers are raised; nine close, but object authorization remains unspecified. The proposal stays changes-required: 90% closure cannot compensate for cross-tenant exposure.

### Example 5

Review revision A makes `currency` optional with a documented default. After approval, revision B makes it required. Registry digest mismatch blocks publication and routes a compatibility re-review.

### Example 6

A webhook design documents HMAC signing but not replay protection, retry schedule, duplicate handling, or receiver effects. Threat/failure walkthrough produces nonce/timestamp validation, delivery IDs, retry bounds, idempotent consumption, and reconciliation tests.

### Example 7

Two reviewers conflict: caching improves latency; privacy policy forbids shared caching of personalized responses. The finding records both constraints, and the design uses private/no-store behavior plus safer server-side optimization.

### Example 8

A public SDK generates awkward ambiguous union types from a valid schema. Consumer/tooling review changes the model additively before launch; schema validity alone would not have caught usability cost.

### Example 9

An emergency vulnerability requires disabling one operation. An expedited authority records scope, consumers, terminal response, communications, rollback, and retrospective re-review; urgency does not become an invisible bypass.

### Example 10

Review lead time falls while escaped compatibility incidents rise. Analysis shows teams submit after implementation and reviewers focus on style. Governance moves discovery review earlier, adds semantic-diff/consumer evidence, and measures finding timing rather than approval speed alone.

## Cross-Program Connections

[Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) supplies quality-attribute scenarios, architecture evaluation, decision records, boundaries, and trade-off reasoning.

[Software Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies review effectiveness, test evidence, static-analysis limits, adversarial cases, traceability, and escaped-defect learning.

[Security Engineering](../../25-security-engineering/ROADMAP.md) supplies threat modeling, trust boundaries, non-waivable authority, authorization/abuse analysis, privacy, and risk acceptance.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies lifecycle reviews, interface control, baselines, verification evidence, configuration/change control, risk, and independent assessment.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies failure models, ordering, consistency, idempotency, retries, partitions, recovery, and capacity interactions.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) supplies review intake/workflows, registries, semantic diff, policy gates, templates, catalogs, paved paths, and release evidence.

## References

1. Google Cloud, [Cloud API Design Guide](https://cloud.google.com/apis/design).
2. Google, [API Improvement Proposals](https://google.aip.dev/).
3. Microsoft, [Azure REST API Guidelines](https://github.com/microsoft/api-guidelines/tree/vNext/azure).
4. OpenAPI Initiative, [OpenAPI Specification](https://spec.openapis.org/oas/latest.html).
5. IETF, [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html).
6. OWASP, [OWASP API Security Top 10 — 2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/).
7. NIST, [SP 800-218: Secure Software Development Framework Version 1.1](https://csrc.nist.gov/pubs/sp/800/218/final).
8. Google, [Reliable Product Launches at Scale](https://sre.google/sre-book/reliable-product-launches/).

## Exercises

### Exercise 1

Design a progressive review plan for a public payment API that moves money, serves partners through generated SDKs, calls three dependencies, and must launch in four months. Define checkpoints, roles, authorities, entry/exit evidence, and re-review triggers.

### Exercise 2

Review a proposed `POST /transfers` whose response can time out after commit, whose client may retry, and whose authorization checks only account ownership. Produce prioritized findings and closure evidence.

### Exercise 3

A proposal supplies adequate evidence for 11 of 12 required domains and closes 9 of 10 blockers. The missing domain is disaster recovery; the remaining blocker is cross-tenant object authorization. Evaluate approval under the evidence/blocker model and contrast it with percentage scoring.

### Exercise 4

Design a finding, decision, conditional-approval, exception, dissent, and re-review record schema that remains auditable when artifacts, reviewers, owners, and guide versions change.

### Exercise 5

An API review program has short queue time, high approval rate, many style comments, rising post-launch compatibility incidents, and complaints about security review arriving late. Diagnose it and define an improvement/measurement plan.

## Answers to the Exercises

### Answer 1

Run discovery before contract commitment: payment/product consumer and domain owners, a partner/SDK advocate, architect, security/privacy, reliability, and facilitator review tasks, money/state invariants, identities, trust, alternatives, and reversibility. Contract checkpoint reviews exact OpenAPI/examples, idempotency/concurrency/error/compatibility/security semantics, generated SDK prototypes, dependency/failure budgets, and threat model. Readiness reviews runtime contract/security tests, capacity/failure injection, reconciliation, SLO/telemetry/audit, rollback/state migration, incident/support/docs/sandbox, consumer onboarding, and approvals. Finance/security authorities own money and non-waivable exposure; reliability owns launch risk within policy; product owns bounded business trade-offs. Entry/exit criteria and exact revisions are recorded at each checkpoint. Re-review triggers include money/state/boundary, auth/data, retry/idempotency, dependency/fan-out, generated-contract, consumer, scale/SLO, topology, vulnerability/incident, or material spec change. Four months controls scheduling and feedback SLO, not evidence strength.

### Answer 2

Blocker one: ambiguous outcome plus retry can duplicate a transfer. Require a client-scoped idempotency key, stable request fingerprint/conflict behavior, durable deduplication across timeout/retry horizon, same-result semantics, atomicity with the transfer effect, response-loss/retry/concurrency tests, and reconciliation/audit. Blocker two: account ownership alone may authorize transfer from a source but not to destination, amount/currency/action, tenant, role, limits, sanctions, or delegated context. Require an action/object/property authorization matrix and negative cross-tenant/IDOR tests at the effect boundary. Major findings cover conditional concurrency/balance invariants, stable error/outcome lookup, deadlines/retry guidance, rate/abuse controls, sensitive error/log redaction, audit/correlation, and dependency partial failure. Closure is test/runtime/design evidence tied to the exact revision, not comments marked resolved.

### Answer 3

Evidence coverage is $11/12\approx91.67\%$ and blocker closure is $9/10=90\%$, but neither percentage authorizes approval. Disaster recovery belongs to $D(p)$ and is absent from $E(p)$, so $D(p)\nsubseteq E(p)$. The authorization blocker is neither closed nor validly accepted; for a cross-tenant exposure it should normally be non-waivable, so the blocker conjunction also fails. Decision is changes required or deferred for evidence. Supply representative recovery/state/replay/RTO-RPO evidence and close object authorization with design plus adversarial tests. Percentages help summarize workload, not consequence: many low-risk passes cannot compensate for missing catastrophic domains.

### Answer 4

Use immutable review ID plus proposal/artifact URIs, commits/digests, scope/exclusions, risk/applicability, spec/style/tool versions, timestamps, owners, participants/roles/authorities/conflicts, and evidence links with provenance/freshness. Findings have stable ID, category/authority, location, observation/evidence, requirement/risk/consequence, severity, required outcome, owner/due state, disposition, closure evidence/reviewer, and supersession links. Decision records state allowed next action, findings snapshot, conditions, approving authorities, effective/expiry, accepted risks/exceptions, dissent, and triggers. Conditions are separately machine-tracked gates. Exceptions name exact rule/control/surface, rationale/alternatives, compensating control, residual risk, authority, owner, expiry/review/removal. Dissent records claim/evidence/consequence and escalation outcome. Re-review events link old/new artifacts, change classification, trigger, affected evidence/findings, and superseding decision; history is append-only/audited.

### Answer 5

The program optimizes throughput/approval and finds low-cost style issues while reviews occur too late for security and compatibility. Sample incidents and past reviews: compare first material-finding time with implementation/contract commitment, required-domain coverage, reviewer attendance/lead time, conditions/exceptions, semantic changes after approval, and escaped findings. Add an early risk/intake checkpoint, threat/consumer/compatibility evidence, asynchronous preparation, narrowly routed authorities, semantic diff, and readiness closure. Automate style so humans focus on behavior. Give security early capacity/SLO and escalate missing expertise rather than infer approval. Measure queue/wait/touch time alongside stage of discovery, severity/recurrence/escape, rework avoided, artifact drift, condition closure, false-positive/appeal, compatibility/security incidents, consumer onboarding/support, and author/reviewer experience. Do not target approval or comment counts; calibrate with incident retrospectives and representative paired reviews.
