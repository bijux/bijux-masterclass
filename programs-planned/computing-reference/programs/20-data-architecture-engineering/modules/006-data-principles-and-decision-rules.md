---
module_id: DARCH-006
program: Data Architecture Engineering
level: 1
module_number: 6
title: Data Principles and Decision Rules
status: complete
last_verified: 2026-09-03
---

# Data Principles and Decision Rules

## One-Page Review

### Governing question

How can an organization turn broad data values into authorized, context-sensitive, testable decisions without replacing professional judgment with slogans or creating a contradictory rulebook?

### Essential definitions

- A **principle** is a durable proposition used to guide a recurring class of decisions and trade-offs.
- A **policy** is an authorized statement of required or prohibited outcomes within a declared scope.
- A **standard** narrows acceptable implementations, representations, or evidence for recurring situations.
- A **decision rule** maps a defined context and conditions to a required, preferred, permitted, or prohibited choice, with rationale and exception behavior.
- A **control** prevents, detects, or corrects departure from policy or a decision rule at a named enforcement point.
- An **exception** is a time-bounded, authorized departure with rationale, risk acceptance, compensating action, owner, and exit condition.
- **Evidence** is a reproducible observation used to determine whether the rule was applied and its intended outcome held.

### Central model, mechanism, or theorem

Represent every actionable rule as:

`r = (authority, scope, trigger, conditions, modality, outcome, rationale, evidence, exception, review)`

A decision is governable only if applicable rules can be identified, precedence and conflicts are resolved, the chosen outcome and evidence are recorded, and any deviation follows an authorized exception path. Principles guide; policies obligate; standards constrain implementation; controls operate; evidence supports review. These layers must trace without being collapsed.

### Critical invariants

- Every rule names its authority, subjects, decisions, contexts, effective interval, and owner.
- Terms such as “must,” “should,” and “may” have defined force within the governance system.
- Noncompensable legal, safety, rights, and security constraints cannot be traded away by aggregate scoring.
- Conflicting applicable rules are surfaced and routed through explicit precedence or authorized adjudication.
- Exceptions expire, retain compensating controls, and never silently redefine the baseline.
- Controls link to the rule and outcome they support; a green control does not prove the policy is sufficient.
- Rules have adoption, outcome, and review evidence plus triggers for revision or retirement.

### Common failures

Common failures include publishing aspirations as principles, copying generic lists without decision scope, using absolute language with no authority, hiding trade-offs, scoring away mandatory constraints, selecting technology inside an enduring principle, granting permanent exceptions, measuring document publication instead of behavior, encoding policy only in prose, and automating a rule whose semantics or appeals remain unresolved.

### Compact example

“Data is an asset” does not decide whether a team may copy customer history. A usable rule states that a cross-domain copy is permitted only for a registered purpose, named consumer, minimum necessary fields, approved policy basis, contract, retention, deletion path, and accountable owner; otherwise use a governed service or deny the share. The rule identifies evidence, exceptions, and review when purpose or regulation changes.

### Connections

[DARCH-005](005-operational-analytical-and-shared-data.md) supplies the cross-boundary uses governed by rules. [DARCH-007](../ROADMAP.md) derives rules from drivers and constraints. [Security Engineering](../../25-security-engineering/ROADMAP.md) develops policies and controls; [Systems Engineering](../../26-systems-engineering/ROADMAP.md) contributes requirements, verification, validation, and lifecycle governance.

## Governing Question

Architecture must guide repeated decisions made by many teams over time. A diagram cannot anticipate every project, and a central review board cannot decide every schema, copy, retention period, or interface. Principles and decision rules distribute intent—but only when their authority, scope, meaning, consequences, and evidence are precise.

Weak principles sound agreeable: “data is valuable,” “quality matters,” “share by default,” or “security first.” They conceal conflicts. Sharing may violate minimization; quality dimensions compete with latency and cost; central consistency may reduce domain autonomy; preservation may conflict with deletion. People facing a delivery deadline cannot derive an accountable choice from a slogan.

At the opposite extreme, an exhaustive prescriptive rulebook becomes stale, contradictory, and easy to evade. It can freeze a particular platform into permanent architecture or require controls disproportionate to consequence. The governing task is to create a small, coherent decision system: durable principles, authorized obligations, context-specific rules, observable controls, and learning from exceptions and outcomes.

## Why This Matters

Data persists across products and organizational changes. Decisions about identifiers, authority, history, access, sharing, quality, correction, preservation, and deletion create long-lived dependencies. If each project decides independently, the estate accumulates competing masters and incompatible meanings. If every choice is centralized, delivery and learning stop.

Good rules enable bounded autonomy. Teams know which outcomes are mandatory, which defaults embody accumulated experience, what evidence justifies a different choice, and who can resolve conflict. Review effort concentrates on high-consequence or genuinely novel decisions rather than routine conformance.

Rules also make architecture testable. A source-of-authority rule can be checked against registered write boundaries. A sharing rule can require consumer and purpose records. A retention rule can map assets to schedules and deletion evidence. Automation improves coverage while human reviewers retain responsibility for meaning, rights, exceptions, and trade-offs.

Poor rules create false assurance. A repository may show 100% compliance because controls test only metadata presence. A mandatory encryption setting may operate while keys are exposed. A quality threshold may pass while measuring the wrong population. Governance must distinguish rule conformance, control operation, and desired outcome.

## Prerequisites and Retrieval

You should understand data architecture views, stakeholder authority, risk, policies, standards, controls, contracts, and basic requirements language. Recall that business outcomes, technical mechanisms, and evidence are different objects.

Retrieve the concepts of scope, context, modality, precedence, invariant, quality attribute, risk acceptance, compensating control, exception, verification, validation, and traceability. Familiarity with policy-as-code helps, but no specific policy language is required.

## Learning Objectives

After completing this module, you should be able to:

- distinguish principles, policies, standards, decision rules, controls, and evidence;
- write a principle with statement, rationale, implications, scope, owner, and review triggers;
- express a decision rule with context, conditions, modality, outcome, and exception behavior;
- define the force of requirement terms and avoid accidental ambiguity;
- derive rules from stakeholder outcomes, obligations, risks, and architecture experience;
- identify conflicts and design precedence and adjudication;
- separate noncompensable constraints from weighted preferences;
- design time-bounded exceptions with compensating controls and exit;
- choose human, automated, and hybrid enforcement points;
- evaluate rules through adoption, conformance, outcome, exception, and revision evidence.

## Core Exposition

A **principle** states a durable belief about how architecture choices should be made. A complete principle record contains a short statement, rationale, implications, scope, owner, conflicts, examples, counterexamples, evidence, and review triggers. “Authoritative facts have an accountable write boundary” is more useful than “single source of truth” because it names the decision property without requiring one physical copy.

Principles should be few enough to remember and independent enough to diagnose. If two principles always produce the same implication, consolidate them. If one statement contains several unrelated obligations, split it. A long catalog reduces attention and increases contradictions.

A principle is not a timeless natural law. It is an organizational commitment derived from mission, stakeholder needs, law, risk, economics, and accumulated experience. Its authority and effective scope must be visible. A research consortium, bank, hospital, and game studio may adopt different principles even when using similar technology.

A **policy** carries formal authority. It states required or prohibited outcomes and the population to which they apply. Authority may come from a board, executive, regulator, statute, contract, domain body, or delegated policy owner. Architecture cannot invent legal authority; legal and policy professionals interpret applicable obligations.

A **standard** turns recurring intent into narrower acceptable choices. Examples include identifier syntax, event envelope fields, approved classification labels, required contract metadata, or cryptographic profiles. Standards reduce unnecessary variation. They should not freeze accidental vendor syntax when interoperability or outcome is the enduring concern.

A **decision rule** is closer to a decision procedure. It says when the rule applies, what observations matter, which choice is required or preferred, why, and what happens when the rule cannot be followed. Rules can be deterministic, threshold-based, ordered, or deliberative. Not every architectural decision can or should be reduced to a Boolean expression.

A **control** implements or monitors a rule. Preventive controls block an invalid deployment. Detective controls identify drift or violation. Corrective controls restore the required condition. Directive controls communicate required action. A single rule may need multiple controls across design, deployment, runtime, and lifecycle.

**Evidence** supports a claim about application or outcome. A schema registry can show that an interface used an approved envelope. Runtime traces can show enforcement. Consumer tests can show compatibility. Incident and exception records can show where the rule failed. Evidence needs identity, time, provenance, coverage, and retention.

Preserve the trace:

`outcome or obligation -> principle/policy -> decision rule -> standard/control -> evidence -> review`

Traceability works in both directions. A team should explain why a control exists; a reviewer should find how a high-level commitment is implemented. Orphan controls create cost without known purpose. Unimplemented policies create ceremonial governance.

Requirement language needs local definition. IETF [BCP 14](https://www.rfc-editor.org/info/rfc2119/) defines uppercase `MUST`, `SHOULD`, and `MAY` for standards that explicitly invoke it; RFC 8174 clarifies capitalization. An enterprise may adopt similar terms, but it must publish its own authority and interpretation. Typography alone cannot turn advice into policy.

A practical modality set is:

- **required**: the outcome must hold; deviation needs named exception authority;
- **prohibited**: the outcome must not occur; any exception follows the same formal path;
- **preferred**: the default applies unless a documented alternative better satisfies declared criteria;
- **permitted**: the choice is allowed but not required;
- **advisory**: experience to consider without conformance status.

Avoid `should` unless its force is defined. Some readers interpret it as mandatory, others as optional. State whether deviation needs evidence, approval, or merely explanation.

Scope is multidimensional. A rule may apply to production personal data shared outside a legal entity, not internal synthetic test data. Include subject, actor, operation, data category, environment, jurisdiction, risk or criticality, lifecycle stage, and effective time. Overbroad scope drives exceptions; narrow hidden scope leaves gaps.

Write rules in a structured form:

“When `trigger`, for `scope`, if `conditions`, the decision authority requires/prefers/permits/prohibits `outcome`, because `rationale`; demonstrate with `evidence`; deviations require `exception`; review on `triggers`.”

The outcome should be technology-neutral where possible. “Cross-domain consumers use a versioned contract” survives tool replacement. A standard may then name approved schema formats. Some rules legitimately constrain technology because interoperability, supply-chain, skill, or support evidence demands it; record that rationale and a review trigger.

Derive rules from concrete sources. Stakeholder outcomes reveal what must be enabled. Laws, contracts, safety duties, and policies create constraints. Threat and privacy analyses reveal unacceptable paths. Incidents and postmortems reveal recurring failure. Architecture decisions reveal successful patterns and costly exceptions. Metrics reveal where a default no longer works.

Do not copy a fashionable principle list without provenance. “Data should be shared” may be suitable for public open data under licensing and privacy review, but harmful for confidential investigations. W3C [Data on the Web Best Practices](https://www.w3.org/TR/dwbp/) describes intended outcomes for publishing data on the Web, including metadata, provenance, quality, versioning, identifiers, access, preservation, and feedback. Its scope is not every internal data decision.

Rules interact. “Reuse before build” can conflict with “minimize shared data.” “Centralize reference data” can conflict with “domains own meaning.” Create a conflict register and define precedence. External law may outrank internal preference; safety and rights constraints may be noncompensable; a more specific authorized rule may refine a general one; a newer rule may supersede an older one only if the authority says so.

Never resolve serious conflicts through an unlabeled weighted score. A high delivery-speed score cannot offset prohibited disclosure. Separate **hard constraints** from **preferences**. First filter options that violate applicable non-waivable constraints. Then compare feasible options across weighted or qualitative criteria with sensitivity analysis.

Some obligations can conflict without a universal precedence answer: preservation versus deletion, transparency versus confidentiality, availability versus emergency containment. Route them to named legal, policy, safety, security, or executive authority with context and evidence. The architecture record should not pretend the conflict disappeared.

Decision rules need inputs whose semantics are governed. “Critical data gets stronger controls” fails if criticality has no owner or classification procedure. Define the population, classification scale, evidence, effective time, and appeals. Unknown classification should have safe handling and a resolution deadline rather than defaulting silently.

Principles should include implications and costs. “Products own their contracts” implies staffing, compatibility support, consumer discovery, incident response, and retirement work. If the organization will not fund those consequences, the statement is aspirational. Record negative implications so decision makers understand trade-offs.

Examples and counterexamples teach boundaries. For a minimization rule, show a compliant aggregate, a prohibited full extract, and a case requiring human review. Counterexamples prevent a concise rule from being stretched into universal prohibition or permission.

Exceptions are part of the system, not embarrassing footnotes. A valid exception identifies the exact rule and scope, requester, rationale, consequence, alternatives considered, risk owner, approver, compensating controls, evidence, start and expiry, exit plan, and review events. Approval authority should match consequence and must be independent where required.

An exception never rewrites the principle. If the same exception recurs, investigate whether the rule is wrong, the standard lacks an implementable path, or incentives reward bypass. Exception rate alone is ambiguous: a low rate can mean good fit or hidden noncompliance; a high rate can mean poor rules or healthy reporting.

Expiration must be enforced. Send notice before expiry, require fresh evidence for renewal, and fail safely according to consequence. Permanent “temporary” waivers transfer risk to future teams. Some emergency exceptions may be short and retrospective, but the authorizing policy must define that path.

Automation is suitable when scope and inputs are machine-resolvable, the rule is stable, false outcomes are understood, and appeal or override is designed. Examples include presence of an owner, contract version, encryption setting, or expiry date. Automation is weaker at judging legitimate purpose, semantic equivalence, public interest, or whether a risk trade-off is acceptable.

Policy-as-code can improve consistency, versioning, tests, and deployment feedback. The code is an implementation, not the policy authority. Preserve linkage to the authorized text, version, decision owner, and interpretations. A compiler success does not establish legal correctness.

Use preventive controls for high-confidence prohibitions and detective controls where context or transition makes blocking risky. A deployment gate can prevent unclassified public storage; a detective query can find unregistered consumers. Corrective workflows need owners, deadlines, escalation, and evidence of closure.

Controls have failure modes. Metadata can be forged or stale. Scanners miss accounts. Runtime enforcement can be disabled. Human approvals become rubber stamps. Test bypass, source coverage, identity, fail-open/fail-closed behavior, alert delivery, remediation, recovery, and tamper resistance according to consequence.

Decision records capture application. Record context, applicable rule versions, evidence, options, constraints, chosen outcome, authority, dissent, exception, consequences, and review triggers. Routine automated decisions can retain compact machine records; high-consequence novel decisions need fuller rationale and human review.

Measure three layers. **Adoption measures** ask whether applicable decisions encounter the rule. **Conformance measures** ask whether required outcomes and controls held. **Outcome measures** ask whether the rule improved interoperability, quality, risk, cost, lead time, or another purpose without unacceptable harm. Do not confuse one layer for another.

Metrics can distort behavior. Counting exceptions may discourage disclosure. Counting reused datasets may encourage inappropriate reuse. Counting owners may produce meaningless group names. Pair measures with qualitative review, counter-metrics, sampling, and incident evidence.

Rules need lifecycle states: proposed, approved, effective, deprecated, retired, and superseded. Version statements and interpretations. State how in-flight work is treated. A deprecated standard may remain acceptable for an existing product until a trigger, while new products use its successor.

Review triggers include legal change, new threat, incident, repeated exception, technology end of support, failed outcome, organizational transfer, material scale change, merger, new data use, or better evidence. Calendar review catches quiet drift; event-driven review catches consequential change sooner.

Governance forums need bounded authority. A data architecture council may own architecture principles and cross-domain adjudication; domain owners govern meaning; security, privacy, legal, records, safety, and risk bodies govern their delegated constraints; platform teams own implementation mechanisms. Define escalation rather than assuming consensus.

Transparency should match audience and sensitivity. Publish principles, rules, rationale, versions, and safe examples broadly. Restrict evidence that reveals personal data, security topology, confidential contracts, or vulnerabilities. Stakeholders affected by consequential automated rules may require explanation, contestability, or participation beyond internal architecture review.

The best rule system reduces unnecessary decisions while preserving accountable judgment. It creates a paved path for common cases, makes prohibited paths clear, exposes trade-offs, and turns novel cases into evidence for learning. It does not try to eliminate architecture.

## Definitions and Notation

Let a rule be:

`r = (a, s, g, c, m, o, q, e, x, v)`

where `a` is authority, `s` scope, `g` trigger, `c` conditions, `m` modality, `o` outcome, `q` rationale, `e` required evidence, `x` exception procedure, and `v` review and validity metadata.

For decision context `d` at time `t`, let `Applicable(d,t)` be the set of effective rules whose scope and trigger match. Let `Hard(d,t)` contain required and prohibited constraints that the deciding authority may not trade away. An option is feasible only if it satisfies every applicable hard constraint or carries a valid authorized exception where exceptions are permitted.

For remaining feasible options, preferences may define a partial order rather than one numeric score. If criteria are weighted, preserve raw evidence, weights, uncertainty, and sensitivity. Never allow a weighted result to override `Hard(d,t)`.

An exception `x` is valid at time `t` only when its authority and scope match, `start <= t < expiry`, compensating controls are operating, and its conditions remain true. Renewal creates a new decision record; it does not erase the old expiry.

## Mechanisms, Invariants, or Proof Structure

Use nine gates to create and govern a decision rule.

**1. Source gate.** Identify the outcome, obligation, risk, incident, or repeated decision that motivates the rule. Record source authority and evidence.

**2. Statement gate.** Write one durable proposition or outcome. Remove slogans, compound duties, accidental tools, and undefined nouns.

**3. Scope gate.** Define actors, data, operations, environments, jurisdictions, lifecycle stages, effective time, exclusions, and unknown handling.

**4. Modality gate.** State required, prohibited, preferred, permitted, or advisory force. Name who can decide and who can authorize deviation.

**5. Conflict gate.** Find applicable higher, lower, general, and specific rules. Apply declared precedence or route unresolved conflicts to authority.

**6. Implementation gate.** Define standards, preventive, detective, and corrective controls, human procedures, evidence, coverage, and failure behavior.

**7. Exception gate.** Define eligibility, approver, risk owner, compensating controls, expiry, renewal, exit, and non-waivable cases.

**8. Validation gate.** Test examples, counterexamples, ambiguous inputs, false positives and negatives, bypass, outage, appeal, and high-consequence cases with affected experts.

**9. Lifecycle gate.** Publish version and interpretation, measure adoption/conformance/outcome, inspect incidents and exceptions, and revise, supersede, or retire on triggers.

The executable example reviews a tiny rule registry and exception set. It detects missing authority, ambiguous modality, conflicting equal-precedence rules, and an expired exception. Its output is deterministic; governance conclusions still require human authority.

<!-- bijux-verify: {"id":"decision-rule-integrity","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"rules=4\nvalid_rules=0\nvalid_exceptions=0\nfindings=copy-002:missing-authority,copy-003:ambiguous-modality,sharing:precedence-conflict,waiver-17:expired\nready=false\n","stderr":""}} -->
```python
today = "2026-09-03"
rules = (
    {"id": "copy-001", "topic": "sharing", "authority": "privacy-board", "modality": "prohibited", "precedence": 100},
    {"id": "copy-002", "topic": "retention", "authority": "", "modality": "required", "precedence": 90},
    {"id": "copy-003", "topic": "quality", "authority": "data-council", "modality": "should", "precedence": 80},
    {"id": "copy-004", "topic": "sharing", "authority": "data-council", "modality": "required", "precedence": 100},
)
exceptions = (
    {"id": "waiver-17", "authority": "privacy-board", "expiry": "2026-08-31", "controls_operating": True},
)

allowed_modalities = {"required", "prohibited", "preferred", "permitted", "advisory"}
findings = []
valid_rules = 0
for rule in rules:
    local = []
    if not rule["authority"]:
        local.append("missing-authority")
    if rule["modality"] not in allowed_modalities:
        local.append("ambiguous-modality")
    if local:
        findings.extend(f"{rule['id']}:{finding}" for finding in local)
    else:
        valid_rules += 1

for topic in sorted({rule["topic"] for rule in rules}):
    applicable = [rule for rule in rules if rule["topic"] == topic]
    top = max(rule["precedence"] for rule in applicable)
    outcomes = {rule["modality"] for rule in applicable if rule["precedence"] == top}
    if "required" in outcomes and "prohibited" in outcomes:
        findings.append(f"{topic}:precedence-conflict")
        valid_rules -= sum(rule["topic"] == topic for rule in rules)

valid_exceptions = 0
for exception in exceptions:
    if exception["expiry"] <= today:
        findings.append(f"{exception['id']}:expired")
    elif exception["authority"] and exception["controls_operating"]:
        valid_exceptions += 1

print(f"rules={len(rules)}")
print(f"valid_rules={valid_rules}")
print(f"valid_exceptions={valid_exceptions}")
print(f"findings={','.join(sorted(findings))}")
print(f"ready={str(not findings).lower()}")
```

The checker validates only a few syntactic and registry invariants. It cannot determine whether `privacy-board` has lawful authority, whether topics and scopes overlap, whether precedence is legitimate, whether controls are effective, or whether a prohibition is ethically or operationally sufficient. Those require governed records, evidence, and review.

## Alternatives and Trade-Offs

**Principles versus detailed rules.** Principles remain durable and support judgment but allow inconsistent interpretation. Detailed rules improve repeatability but expand maintenance and can mishandle context. Use principles for direction and rules for recurring consequential decisions.

**Central versus federated rule ownership.** Central ownership reduces contradiction across domains. Federated ownership preserves context and responsiveness. Shared precedence, minimum metadata, and adjudication allow federation without ambiguity.

**Outcome-based versus implementation-based rules.** Outcome rules survive technology change and enable local choice. Implementation rules simplify interoperability and verification. Constrain implementation only where evidence justifies uniformity.

**Preventive versus detective control.** Prevention blocks known unsafe states but can halt legitimate work on false positives. Detection preserves flow but allows exposure before correction. Match control to consequence, confidence, reversibility, and response time.

**Machine evaluation versus human judgment.** Machines provide scale and consistency over resolvable inputs. Humans interpret purpose, conflict, novelty, rights, and proportionality. Hybrid designs automate facts and preserve accountable decisions.

**Absolute prohibition versus managed exception.** Non-waivable obligations need true prohibition. Other rules may need a narrow exception to preserve continuity or learning. An easy exception destroys the baseline; no exception can drive hidden bypass.

**Scoring versus constraint filtering.** Scores compare trade-offs but hide noncompensable duties and uncertain weights. Filter hard constraints first, then compare feasible options transparently.

**Stable policy versus rapid learning.** Stability supports predictability and investment. Slow revision preserves obsolete assumptions. Versioned rules, evidence, and explicit review triggers reconcile stability with learning.

## Failure Modes and Misconceptions

1. **A value statement is a principle.** Without implications, scope, authority, and decisions, it is an aspiration.
2. **Principles are universally true.** They are governed commitments for a context and time.
3. **Policy, standard, and control are synonyms.** They occupy different authority and implementation layers.
4. **Uppercase MUST creates authority.** Requirement words have force only within an authorized document and defined convention.
5. **All principles can be balanced by score.** Some rights, safety, legal, and security constraints are noncompensable.
6. **The more rules, the stronger governance.** Excess rules create conflict, neglect, and performative conformance.
7. **Technology-neutral is always better.** Interoperability or risk may justify a technology constraint with review.
8. **An automated pass proves the outcome.** It proves only the tested predicate over observed inputs.
9. **Exceptions weaken governance.** Governed exceptions expose reality; hidden bypass weakens governance.
10. **An exception can be permanent.** A permanent change belongs in the baseline rule or explicit local policy.
11. **Low exception volume proves fit.** It may reveal fear, invisibility, or unused controls.
12. **Publication completes adoption.** Teams need accessible guidance, paved paths, feedback, support, and outcome review.

## Worked Examples

### Example 1

**Question:** Is “data is a strategic asset” an actionable principle?

**Reasoning:** It lacks scope, decision implications, ownership, trade-offs, and evidence. It may motivate stewardship but decides nothing alone.

**Conclusion:** Rewrite values into decision-relevant propositions.

### Example 2

**Question:** How should “reuse before build” interact with minimization?

**Reasoning:** First apply purpose, recipient, and minimization constraints. Reuse is a preference among permissible options, not a reason to expand access.

**Conclusion:** Hard policy constraints precede efficiency preferences.

### Example 3

**Question:** A standard says all events use one vendor schema registry.

**Reasoning:** Separate the enduring outcome—versioned interoperable schemas—from the current approved implementation, rationale, alternatives, and review trigger.

**Conclusion:** Keep durable intent above replaceable mechanisms.

### Example 4

**Question:** A control confirms every dataset has an owner string. Is ownership governed?

**Reasoning:** The string may name an inactive group with no decision authority. Sample accountability, contactability, decisions, and response evidence.

**Conclusion:** Metadata presence is weaker than outcome validation.

### Example 5

**Question:** When may a rule use `preferred`?

**Reasoning:** When alternatives can legitimately outperform the default under declared criteria and a deviation record captures evidence without formal risk waiver.

**Conclusion:** Modality should match actual decision authority.

### Example 6

**Question:** Two equal-precedence policies require and prohibit sharing.

**Reasoning:** Do not select one by implementation convenience. Clarify scope or route the conflict to the authorities that issued them.

**Conclusion:** Conflict is an explicit governance state.

### Example 7

**Question:** A migration exception expires during an outage.

**Reasoning:** Follow the predeclared expiry and emergency procedure. Do not silently extend; record fresh authority, consequence, controls, and short exit.

**Conclusion:** Expiry must produce behavior, not calendar decoration.

### Example 8

**Question:** Should a policy-as-code gate decide whether a new use has legitimate purpose?

**Reasoning:** It can verify that an approved purpose record exists and matches identifiers. Legitimate purpose itself requires authorized substantive review.

**Conclusion:** Automate resolvable evidence, not concealed judgment.

### Example 9

**Question:** Exception rate doubled after reporting became easier.

**Reasoning:** The change may indicate better visibility rather than worse conformance. Examine denominators, hidden bypass, rule fit, risks, and outcomes.

**Conclusion:** Governance metrics require causal and behavioral context.

### Example 10

**Question:** When should a principle be retired?

**Reasoning:** When its source obligation or outcome no longer applies, evidence contradicts its rationale, another principle supersedes it, or it produces unacceptable consequences.

**Conclusion:** Retire through versioned authority and transition, not silent deletion.

## Cross-Program Connections

[Software Engineering: Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) develops architectural decisions, quality attributes, constraints, trade-offs, and fitness functions. Data principles specialize these for meaning, authority, sharing, history, and lifecycle.

[Security Engineering](../../25-security-engineering/ROADMAP.md) develops security policy, threat analysis, control design, evidence, and exception risk. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) contributes requirement quality, traceability, verification, validation, configuration, and lifecycle review.

[API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) turns many rules into interface contracts, compatibility gates, identity policies, and deprecation behavior. [Platform Engineering](../../29-platform-engineering/ROADMAP.md) can provide paved paths and policy enforcement while preserving product authority.

## References

- The Open Group, [*The TOGAF Standard, 10th Edition*](https://www.opengroup.org/togaf), 2022, site checked 2026-09-03. Official enterprise-architecture standard family covering principles, governance, requirements, and architecture development.
- IEEE, [*IEEE/ISO/IEC 42010-2022 — Architecture Description*](https://standards.ieee.org/ieee/42010/6846/), 2022. Official standard record for stakeholder concerns, viewpoints, views, models, and architecture-description correspondence.
- Scott Bradner, [*RFC 2119: Key Words for Use in RFCs to Indicate Requirement Levels*](https://www.rfc-editor.org/info/rfc2119/), IETF BCP 14, 1997. Normative definitions for requirement terms when a specification explicitly invokes them.
- Barry Leiba, [*RFC 8174: Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words*](https://www.rfc-editor.org/info/rfc8174/), IETF BCP 14, 2017. Clarification of capitalization and applicability for requirement terminology.
- W3C, [*Data on the Web Best Practices*](https://www.w3.org/TR/dwbp/), W3C Recommendation, 2017. Intended outcomes and implementation guidance for metadata, licensing, provenance, quality, versioning, identifiers, access, preservation, and feedback.
- NIST, [*Privacy Framework*](https://www.nist.gov/privacy-framework), checked 2026-09-03. Official voluntary framework for identifying and managing privacy risk through outcomes, profiles, implementation tiers, and ecosystem responsibilities.
- NIST, [*Cybersecurity Framework (CSF) 2.0*](https://doi.org/10.6028/NIST.CSWP.29), NIST CSWP 29, 2024. Outcome-oriented governance, identification, protection, detection, response, and recovery framework.
- Rebekah Jones, [*Policy Language*](https://www.openpolicyagent.org/docs/policy-language), Open Policy Agent documentation, checked 2026-09-03. Official declarative policy-language reference; an implementation example rather than a source of organizational authority.

## Exercises

### Exercise 1

Rewrite “data should be shared” as a principle record with scope, rationale, implications, conflicts, evidence, owner, and review triggers.

### Exercise 2

Write a structured decision rule for creating a cross-domain customer-data copy. Include modality, hard constraints, preferred alternatives, exception, and evidence.

### Exercise 3

Resolve a conflict among “retain records for seven years,” “delete personal data after purpose ends,” and “preserve data under legal hold” without inventing legal authority.

### Exercise 4

Design preventive, detective, and corrective controls for the rule “production data products have an accountable owner and consumer-visible contract.”

### Exercise 5

Create a lifecycle and measurement plan for a principle requiring stable identifiers. Include adoption, conformance, outcome, counter-metrics, exceptions, and retirement triggers.

## Answers to the Exercises

### Answer 1

Statement: authorized data should be discoverable and reusable across accountable boundaries when reuse advances a named outcome. Scope: governed production products and registered internal or external consumers, excluding unapproved sensitive uses. Rationale: reduce duplicate acquisition and incompatible facts. Implications: stable identity, semantic and serving contracts, purpose, minimization, policy review, producer support, lineage, quality, correction, deletion, cost, and exit. Conflicts include confidentiality, privacy, sovereignty, intellectual property, safety, and domain autonomy; those constraints precede the reuse preference. Evidence includes registered consumers, avoided duplication, consumer fitness, incidents, harms, and lifecycle cost. The data council owns the architecture principle while policy authorities retain their mandates. Review on legal change, breach, repeated exception, failed outcome, or material new use.

### Answer 2

When a product proposes a persistent cross-domain copy of customer facts, the architecture requires a named producer and consumer, authorized purpose, minimum necessary fields, source authority, versioned semantic and serving contract, classification and access, source position, retention, correction, deletion/restriction path, incident contact, cost owner, and exit. Applicable legal, rights, security, and residency constraints are hard filters. Among feasible choices, prefer governed API, view, event, or in-place computation when they meet the use with less lifecycle burden. An exception names the exact scope, approvers and risk owner, compensating controls, expiry, and migration. Evidence includes contract, purpose approval, data-flow record, tests, runtime access, deletion rehearsal, and consumer acceptance.

### Answer 3

First determine the authority, scope, subject, jurisdiction, effective dates, definition of record, purpose, and whether legal hold suspends ordinary disposition. Do not rank the statements by architecture preference. Legal, privacy, records, and domain authorities interpret the applicable obligations and document precedence for the specific population. The resulting rule may retain required records for the authorized schedule, minimize or restrict processing after other purposes end, preserve held material while blocking ordinary deletion, and delete or anonymize eligible copies after hold release. Map decisions to systems and derivatives, record holds and releases, protect retained data, test disposition, and preserve evidence. This answer is a reasoning pattern, not legal advice.

### Answer 4

A preventive deployment gate requires product identity, role-based owner group, supported contact, contract version, and approved repository link. It should block only when identifiers are resolvable and an emergency path exists. Detective controls reconcile catalogs with organization directories, runtime consumers, source repositories, and support rotations; sample whether owners can make semantic, service, and lifecycle decisions. Corrective workflow assigns a deadline, escalation, interim risk owner, consumer notice, and retirement or reassignment path. Evidence includes gate decisions, source coverage, owner acknowledgements, contract tests, incident response, stale records, remediation time, and appeals. A populated owner field alone does not establish accountability.

### Answer 5

Define stable identifiers for products, versions, and distributions, with namespace authority, alias, merge, split, and retirement rules. Adoption measures count in-scope publications encountering the rule with explicit denominators. Conformance measures test uniqueness, persistence across version and relocation, alias resolution, references, and consumer migration. Outcome measures examine broken links, reconciliation effort, discovery success, and incident impact; counter-metrics include issuance lead time, central bottleneck, and inappropriate identity merging. Record exceptions for legacy or external schemes with mappings and expiry. Review after collisions, mergers, platform moves, namespace compromise, repeated exception, consumer failure, or new interoperability evidence. Supersede through versioned mapping and transition; never silently recycle identifiers.
