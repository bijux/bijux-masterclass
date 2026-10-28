---
module_id: SDRE-051
program: Software Engineering: Software Delivery & Reliability Engineering
level: 2
module_number: 51
title: Incident Severity and Classification
status: complete
last_verified: 2026-09-06
---

# Incident Severity and Classification

## One-Page Review

### Governing question

How should an organization classify an uncertain, changing production incident so that response urgency, authority, staffing, communication, and obligations match user harm without turning a provisional label into false precision?

### Essential definitions

- an **event** is an observable occurrence or change; it may be expected, anomalous, benign, or harmful;
- an **alert** is a notification produced when a rule or judgment says attention may be required;
- an **incident** is an occurrence or condition managed through a defined response because it actually or plausibly threatens a service, user, organization, or protected property;
- **classification** assigns independent descriptors such as type, affected service, geography, data class, failure mode, status, and confidence;
- **severity** is a policy label for the consequence and urgency of an incident, used to select a proportionate response;
- **impact** is realized harm or loss of a protected outcome, including magnitude, affected population, duration, reversibility, and distribution;
- **potential impact** is credible harm that has not yet been observed but may occur given current state and propagation;
- **urgency** describes how response delay changes expected harm or recovery options;
- **priority** orders work under constrained resources; it is related to but distinct from severity;
- **confidence** records evidence strength for the current classification;
- **escalation** moves to a more intensive response; **de-escalation** reduces response only after declared evidence and authority support it;
- a **major incident** is an organization-defined class requiring coordinated incident management, which need not map one-to-one to a numeric severity label;
- a **regulatory or contractual classification** is an overlay governed by its own definitions and clocks, not something inferred solely from reliability severity.

### Central model, mechanism, or theorem

Represent observed and credible impact as a vector

$$
x=(a,d,i,c,s,f,r),
$$

where components may capture affected population $a$, duration $d$, integrity or durability harm $i$, confidentiality harm $c$, safety harm $s$, financial or mission consequence $f$, and reversibility $r$. Let urgency $u$ describe the consequence of delay, evidence confidence be $q$, and context be $z$. A local policy maps

$$
\sigma=g(x,u,q,z)
$$

to a response class. The map must contain hard overrides for prohibited or catastrophic properties, not only a weighted average. A monotonicity invariant is: if incident $A$ is no less harmful in every applicable dimension and no less urgent than $B$, then $A$ must not receive a less intensive response, absent an explicit contextual rule.

### Critical invariants

- classify user and protected-property consequences, not team embarrassment or cause prestige;
- keep category, severity, urgency, priority, status, and confidence as separate fields;
- make the first label provisional and easy to escalate under uncertainty;
- include credible potential harm, propagation, and lost recovery options—not only observed tickets;
- use hard overrides for safety, security, irreversible data loss, legal duties, or other non-substitutable properties;
- let severity drive a predefined response package without delaying incident declaration;
- never lower severity merely because staffing, dashboards, or diagnosis are inadequate;
- record who changed the classification, when, from what evidence, and why;
- de-escalate only after user harm and forward risk are controlled, not after symptoms briefly improve;
- review thresholds against incidents, near misses, unequal cohort harm, and response cost.

### Common failures

Failures include equating alert priority with incident severity, using affected-user percentage alone, ignoring one-person catastrophic harm, waiting for root cause before declaring, treating unknown as low, lowering severity to protect metrics, using duration only after a long wait, counting internal components rather than user outcomes, confusing “major incident” with one fixed severity, allowing each team to interpret labels differently, forgetting security or legal overlays, de-escalating on a transient recovery, and changing thresholds until historical reports look favorable.

### Compact example

A new release corrupts 20 of 100,000 uploaded documents. The affected percentage is 0.02%, but the operation is irreversible after a short replication window and additional writes continue. A volume-only rule calls this low severity. A property-aware policy sees active durability loss, increasing exposure, and shrinking recovery options; it invokes the critical-data override, declares a major incident, freezes writes, preserves evidence, and notifies data and incident leadership. Small population does not imply small consequence.

### Connections

[SDRE-050](050-writing-a-production-readiness-review.md) defines incident scenarios, authority, and launch-stop rules before production. [SDRE-052](../ROADMAP.md) next designs the on-call system that must enact severity-specific response. [SDRE-053](../ROADMAP.md) separates alert triage from the broader classification decision developed here.

## Governing Question

At the beginning of an incident, the most important facts are often unknown. Telemetry may be incomplete, reports may conflict, impact may be concentrated in a quiet cohort, and a destructive process may be advancing faster than visible symptoms. Yet the organization must decide whether to page one service owner, activate coordinated command, freeze changes, involve security or legal teams, notify customers, or invoke executive authority.

A severity label compresses this decision. Compression is useful only when the vocabulary has stable operational meaning. “SEV-1” should activate a known response, not start an argument about whether the issue feels important. The label must be revisable because evidence changes. It must also preserve dimensions that a scalar cannot: confidentiality loss is not equivalent to latency, irreversible corruption is not equivalent to a transient outage, and harm to one vulnerable user is not erased by a small global percentage.

The governing question asks how to make classification fast, conservative under uncertainty, specific to user and protected-property consequence, and disciplined enough for later analysis without pretending that a taxonomy can replace incident judgment.

## Why This Matters

Google's SRE Workbook distinguishes resolving an incident—mitigating impact or restoring service—from managing the coordinated response and communication [1]. Severity classification belongs to management of the response: it helps select coordination, authority, and communication while technical investigation proceeds. Waiting for root cause defeats that purpose.

Google's troubleshooting guidance says response should be proportionate to impact and emphasizes stopping user harm before pursuing root cause [2]. Its product-focused reliability material describes product-specific severity guidelines tied to user objectives and business indicators rather than one generic global scale [3]. These sources support consequence-centered local policy, not copying Google's internal labels.

NIST SP 800-61 Revision 3, finalized in April 2025, integrates cybersecurity incident response into broader cybersecurity risk management and supersedes the 2012 Revision 2 [4]. NIST's glossary reflects legal and standards-derived definitions for a cybersecurity incident [5]. A general reliability incident taxonomy must not overwrite those governed security definitions; instead, it links them through explicit overlays and notification paths.

PagerDuty's public incident-response documentation presents one concrete severity scheme, advises organizations to make definitions specific, and recommends choosing the higher response when uncertain [6]. It also separates triggering coordinated response from settling the exact severity label. This is a useful operational example, not a universal numbering standard. Current online claims and all six canonical URLs were checked on 2026-09-06.

## Prerequisites and Retrieval

Retrieve user journey, protected property, SLI, SLO, error budget, alert, event, failure, incident, blast radius, failure domain, degradation, recovery, risk, confidence, escalation, on-call, incident command, evidence, and status communication.

From SDRE-038 retrieve the distinction between actionable alerting and state observation. From SDRE-041 retrieve reliability, availability, and durability as separate properties. From SDRE-042 through SDRE-045 retrieve user-centered measurements, objectives, and policies. From SDRE-047 through SDRE-049 retrieve failure propagation, correlated loss, and degraded behavior. From SDRE-050 retrieve readiness scenarios and response authority. This module classifies the incident; later modules develop staffing, triage, command, investigation, mitigation, communication, evidence, and learning.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish events, alerts, incidents, problems, and planned operational states;
2. separate classification dimensions from severity, urgency, priority, status, and confidence;
3. define severity levels by user harm and required response rather than adjectives alone;
4. incorporate observed impact, credible potential impact, propagation, duration, reversibility, and unequal harm;
5. design hard overrides for non-substitutable safety, security, durability, and legal properties;
6. classify provisionally and escalate safely when evidence is incomplete;
7. specify severity-driven staffing, authority, communication, and evidence-preservation actions;
8. revise and de-escalate classification without hiding history or current risk;
9. connect reliability severity to security, privacy, contractual, and regulatory overlays;
10. validate a taxonomy against historical, synthetic, adversarial, and boundary scenarios.

## Core Exposition

**Separate signal, occurrence, and managed response.** An event is something observed: latency rose, a deployment completed, a certificate expired, or a customer reported wrong data. An alert is a notification mechanism. Neither automatically constitutes an incident. Conversely, an incident can exist before any alert fires—for example, when a customer provides credible evidence of silent corruption.

Declare an incident when a condition needs structured response because a protected outcome is harmed or credibly threatened. The declaration should be cheap and reversible. If responders must first win a severity debate, gather perfect evidence, or identify root cause, coordination starts too late. An incident can later be closed as benign without making the initial declaration a failure.

Keep a **problem** or underlying cause distinct from the incident response. One defect may cause several incidents; one incident may involve several causes. Severity describes current consequence and urgency, not the intellectual difficulty of the defect or the eventual cost of permanent remediation.

Planned maintenance and expected degraded operation may not be incidents when they remain within approved user and operational contracts. They become incidents when actual behavior violates those contracts, risk escapes containment, or required controls fail. Record planned state so responders can distinguish expected signals without suppressing unexpected harm.

**Use a multidimensional classification record.** Before assigning severity, capture independent descriptors: affected products and user journeys; geography, tenant, cohort, and accessibility impact; start and detection times; observed and potential properties harmed; deployment or configuration correlation; suspected failure domains; security or privacy indicators; current status; workaround; evidence confidence; and incident owner.

Category routes expertise. Examples include availability, latency, correctness, durability, confidentiality, integrity, abuse, capacity, dependency, release, and control-plane failure. Multiple categories may apply. Do not force a data-integrity incident into “availability” because the service returns HTTP 200.

Status tracks lifecycle—investigating, identified, mitigating, monitoring, resolved—under local definitions. Status is not severity. An incident can be “monitoring” and still critical while rollback effects or data repair remain uncertain. Likewise, a low-severity incident can remain under investigation for days.

Confidence should name evidence quality, not merely a percentage. A useful scale may distinguish confirmed impact, strongly supported inference, plausible report, and unknown. Record contradictory observations. Low confidence does not imply low severity; it changes how conservatively the team chooses and what evidence it seeks next.

**Define severity by consequence and response.** Each local severity class needs two linked definitions. The consequence definition names qualifying user or protected-property conditions. The response definition names paging urgency, incident-command activation, staffing, leadership, communication, change freeze, evidence preservation, and review obligations.

Avoid adjectives without discriminators. “Critical,” “major,” and “minor” drift across teams. Use scenario anchors such as global unavailability of a core journey, active unrecoverable corruption, unauthorized disclosure of a protected data class, loss of emergency control, regional degradation beyond an objective, or loss of all redundancy with imminent user impact. Thresholds need measurement populations, time windows, and exceptions.

Numbering direction varies. Some organizations make `SEV-1` highest; others use increasing numbers or named colors. The label itself is not portable. Every page, ticket, status API, partner contract, and post-incident dataset must carry or resolve the governing taxonomy version.

“Major incident” can be a coordination flag separate from severity. A novel cross-team fault with modest current user impact may need incident command. A well-understood localized outage may be severe for affected users but handled by one trained team. Do not force response topology and consequence into one brittle field.

**Measure impact from protected outcomes.** Count affected successful and failed user operations, not only hosts, pods, tickets, or errors. Denominators matter: 10,000 failed checkouts out of 20,000 attempts differs from 10,000 failed optional recommendations out of 100 million page views. Segment by region, tenant, plan, operation, accessibility need, and data class when harm is unequal.

Magnitude includes more than percentage. Consider absolute people or transactions, consequence per affected subject, duration, frequency, reversibility, workarounds, deadline sensitivity, financial or mission loss, safety, confidentiality, integrity, and trust. One incorrectly denied medical action can matter more than a million delayed decorative images.

Observe distribution. A global 0.1% failure rate could mean random minor failures or total failure for one tenant. Aggregation can conceal concentrated harm. Define severity overrides for strategic, vulnerable, contractual, or regulated cohorts only through authorized policy; avoid improvising importance based on who complains loudest.

Duration has both realized and forward-looking roles. Do not wait 60 minutes to classify an incident whose rule says “outage longer than 60 minutes.” Estimate whether mitigation and recovery can occur before the threshold, and escalate earlier when delay consumes options. Short catastrophic corruption can outrank a long low-consequence slowdown.

**Include potential impact and urgency.** Observed impact is a lower bound when telemetry is delayed or incomplete. Ask what happens if the current mechanism continues: Does corruption replicate? Will queues exhaust memory? Will a certificate expire globally? Will a legal reporting clock start? Will rollback cease to be compatible? Will the only remaining replica fail under load?

Urgency is the derivative of consequence with respect to response delay, not another name for magnitude. A low-current-impact certificate problem can be urgent when global expiry is ten minutes away. A widespread but stable cosmetic defect can have high impact and lower operational urgency. Both dimensions inform response.

Use credible worst-case reasoning, not unconstrained imagination. State mechanism, exposure path, time horizon, and evidence. “Could destroy everything” is not actionable without a path. “The schema migrator deletes one tenant per minute; 17 of 600 are affected; disabling job `m42` stops further deletion; the restore log expires in two hours” supports immediate escalation.

Reversibility changes urgency and consequence. A transient failed read may recover with no lasting effect. An acknowledged but lost write, disclosed secret, unsafe actuator command, or missed one-time deadline cannot be undone by later availability. Hard overrides should protect these properties even when volume is small.

**Use hard overrides before aggregation.** A weighted score can combine ordinary volume, duration, and degradation, but it can also average away prohibited outcomes. Apply explicit overrides first for locally defined cases such as credible safety threat, active unauthorized access, irreversible data loss, loss of incident controls, or mandated notification. Then apply the ordinary decision table to remaining incidents.

Let impact vector $x$ contain relevant dimensions and local context $z$ contain service criticality, time, contracts, and approved exceptions. The mapping $\sigma=g(x,u,q,z)$ is a policy, not a natural law. Publish examples at boundaries and review them with product, reliability, security, legal, support, and affected business owners.

Monotonicity is a useful invariant. If one scenario is at least as harmful in every applicable component and at least as urgent, the policy should not assign it a lower response. Context can create justified exceptions—for example, different safety obligations—but the rule and authority must be explicit. Hidden nonmonotonicity confuses responders and encourages metric gaming.

Avoid false precision. Multiplying guessed probabilities and impacts during an active incident can delay action and imply confidence not present. Use bounded ranges, scenario classes, or categorical evidence when better. Quantification is most useful for designing and validating policy before incidents, not litigating the last decimal during one.

**Classify early and revise visibly.** The initial classifier uses available evidence, assumes a conservative credible scenario, and records uncertainty. The cost of temporary over-response is usually bounded; the cost of delayed coordination can compound. Define which classes may be declared by any responder and which changes require incident-command, security, or executive authority.

Escalation should be immediate when a hard override appears, impact crosses a boundary, propagation accelerates, uncertainty remains high past a deadline, a mitigation fails, or the response system itself degrades. Automation may recommend or invoke response packages, but it must expose inputs, taxonomy version, missingness, and override behavior.

De-escalation needs stronger evidence than escalation. Require sustained control of user impact, stopped propagation, preserved recovery options, stable mitigation, no active hard override, and agreement from the role owning the incident. Do not downgrade merely because traffic dipped, the dashboard lost data, a public status message is inconvenient, or the on-call team is overloaded.

Preserve classification history. Record timestamp, old and new class, actor, evidence, rationale, taxonomy version, and actions triggered or canceled. Duration by severity should be derived from this timeline rather than overwriting the original field. That history supports later threshold calibration without blaming the first responder for uncertainty.

**Map severity to response packages.** A response class is valuable because it causes known action. Define notification latency, acknowledgement target, incident-command requirement, role composition, change freeze, stakeholder and customer communication, evidence preservation, update cadence, dependency escalation, and post-incident review.

Severity should generally increase available authority and coordination, not license arbitrary risk. A critical incident may justify faster changes and broader emergency access, but safety, authorization, audit, and two-person controls remain unless an explicit emergency policy governs them. Document the trade and expiry.

Do not make response dependent on scarce titles. If only one executive can declare a top-severity incident, nights and holidays create classification failure. Permit broad escalation, then use designated roles to confirm or de-escalate. The taxonomy must work with the actual on-call and communication system.

The following controlled model demonstrates hard overrides, ordinary thresholds, and conservative uncertainty. The thresholds are fictional and intentionally local.

<!-- bijux-verify: {"id":"classify-incident-severity","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"corruption=critical\noutage=high\nredundancy_risk=moderate\nuncertain=high\ncosmetic=low\n","stderr":""}} -->
```python
order = ["low", "moderate", "high", "critical"]

def classify(*, affected_fraction=0.0, core_unavailable=False,
             irreversible_data_loss=False, safety_threat=False,
             redundancy_lost=False, confidence="confirmed"):
    if irreversible_data_loss or safety_threat:
        severity = "critical"
    elif core_unavailable and affected_fraction >= 0.50:
        severity = "critical"
    elif core_unavailable and affected_fraction >= 0.10:
        severity = "high"
    elif redundancy_lost or affected_fraction >= 0.01:
        severity = "moderate"
    else:
        severity = "low"

    if confidence == "unknown" and severity != "critical":
        severity = order[order.index(severity) + 1]
    return severity

print("corruption=" + classify(irreversible_data_loss=True))
print("outage=" + classify(affected_fraction=0.20, core_unavailable=True))
print("redundancy_risk=" + classify(redundancy_lost=True))
print("uncertain=" + classify(redundancy_lost=True, confidence="unknown"))
print("cosmetic=" + classify(affected_fraction=0.001))
```

This execution establishes the snippet's behavior under CPython 3.14.4. It does not establish appropriate thresholds, categories, or response for a real service. A production classifier needs authoritative local policy, validated inputs, missing-data behavior, versioning, audit, and human override.

**Keep priority and obligations separate.** Severity communicates consequence and response intensity. Priority orders competing work. During two simultaneous severe incidents, one may receive scarce database expertise first because harm is accelerating faster; that does not make the other less severe. Record resource-allocation decisions separately so severity data remains interpretable.

Customer-visible status classifications may differ from internal severity because disclosure scope, terminology, and aggregation rules differ. Maintain a traceable mapping without promising that every internal incident is public or hiding material customer impact. Communication obligations can also arise from contracts, regulators, partners, or data-protection rules on clocks unrelated to operational severity.

Security incidents require their governed definitions, evidence handling, containment authority, and notification analysis. A service outage caused by suspected intrusion can carry both reliability severity and security classification. Do not lower one because the other team owns it. Use a joint incident identity and access-controlled subrecords where sensitive evidence cannot be broadly shared.

**Validate and evolve the taxonomy.** Tabletop historical incidents and boundary scenarios before adoption. Ask different roles to classify independently, explain their evidence, and select response actions. Disagreement reveals ambiguous wording or missing dimensions. Test silent corruption, one-user catastrophic harm, global cosmetic harm, imminent capacity exhaustion, telemetry loss, simultaneous incidents, and suspected breach with no confirmed exposure.

Measure classification latency, escalation latency, number and rationale of changes, response-package adherence, missed obligations, over-response cost, and harm before mitigation. Do not optimize for few reclassifications; early provisional labels should change when evidence improves. Look for systematic underclassification of quiet cohorts and threshold gaming near reporting boundaries.

After incidents, update scenario anchors and automation only when the lesson generalizes. Preserve taxonomy versions so historical data retains meaning. Train with realistic exercises and make the current policy available during outages. The aim is not perfect labels; it is timely, proportionate protection of users and recovery options.

## Definitions and Notation

Let $E_t$ be evidence available at time $t$. Let observed impact be $x_o(t)$ and credible potential impact over horizon $h$ be $x_p(t,h)$. The classification input may conservatively combine them componentwise:

$$
x(t,h)=\max\bigl(x_o(t),x_p(t,h)\bigr),
$$

where “max” applies only to dimensions with meaningful ordered scales. Non-comparable properties remain distinct and may invoke hard overrides.

Let $u(t)$ represent urgency—the expected loss of safety, data, service, or recovery opportunity from delay. Let confidence $q(t)$ summarize evidence quality under a declared scale, and context $z$ include service criticality, user distribution, time, contracts, and taxonomy version. Local policy returns severity $\sigma(t)=g(x,u,q,z)$.

For severity ranks $K=\{1,2,3,4\}$ ordered from least to most intensive response, a componentwise monotone policy satisfies

$$
x_A\succeq x_B\ \land\ u_A\ge u_B \implies g(x_A,u_A,q,z)\ge g(x_B,u_B,q,z),
$$

holding equal the confidence and context named in the comparison. Hard-override predicate $H_j(x,z)=1$ sets a minimum severity $k_j$ regardless of ordinary aggregate score.

For population segment $j$, affected fraction is $f_j=b_j/n_j$ for eligible population $n_j>0$ and bad outcomes $b_j$. Preserve $b_j$, $n_j$, operation, interval, and consequence; a global weighted fraction can conceal a segment with $f_j=1$.

Classification history is an ordered sequence $D=((t_0,\sigma_0,e_0),\ldots,(t_m,\sigma_m,e_m))$ of timestamp, class, and evidence/rationale. Never overwrite it with only the final class.

## Mechanisms, Invariants, or Proof Structure

**Declaration-before-diagnosis argument.** Root cause may require long investigation while coordination, mitigation, and communication are immediately valuable. Therefore incident declaration and provisional severity must depend on consequence and credible risk, not completed causal diagnosis.

**Aggregation counterexample.** Suppose 1,000 of 1,000 users in segment A fail and 0 of 999,000 in segment B fail. Global failure is $1{,}000/1{,}000{,}000=0.1\%$, while $f_A=100\%$. A global threshold above 0.1% would miss total exclusion of A. Segment-aware and consequence-aware overrides are necessary.

**Hard-override argument.** If a prohibited property such as safety or irreversible durability loss is represented only by a finite weight, enough unrelated successful traffic can reduce its average score below a threshold. Applying the prohibited predicate before aggregation prevents volume from erasing it.

**Monotonicity check.** For equal context and confidence, increasing every applicable harm dimension and urgency must not lower response intensity. Violations identify reversed thresholds, inconsistent special cases, or score normalization defects. Monotonicity does not compare unlike unscaled harms; hard rules and authority resolve those cases.

**Conservative-uncertainty argument.** When telemetry loss is correlated with failure, missing observations are not evidence of success. Escalating one class under a bounded unknown state can buy coordination and investigation time. The policy must cap and review this rule so prolonged observability gaps do not create arbitrary permanent emergency.

**De-escalation asymmetry.** Escalation responds to credible potential harm; de-escalation asserts that intensive response is no longer needed. The latter requires evidence that propagation stopped, impact is controlled, and recovery options remain. One healthy sample is insufficient when observations lag or mitigation can regress.

**Historical-meaning invariant.** A severity label has meaning only under taxonomy version $v$. Changing thresholds while treating old and new labels as identical corrupts trend analysis. Store version and, when reclassifying historical data, preserve both original and normalized interpretations.

## Alternatives and Trade-Offs

**Named levels versus numeric levels.** Names such as `critical` communicate direction; numbers are compact and familiar. Both drift without definitions, and numeric direction differs across organizations. Carry canonical machine identity plus rendered name and taxonomy version.

**Single severity versus consequence and coordination axes.** One field is fast and simplifies automation. It conflates user harm with response topology. Separate `impact_severity` and `coordination_mode` when cross-team novelty, security sensitivity, or communication scope varies independently, while keeping a simple declaration path.

**Measured thresholds versus scenario anchors.** Thresholds improve consistency and automation but create cliff effects and gaming. Scenario anchors capture qualitative consequence but require judgment. Combine explicit measurements with override scenarios and authority for edge cases.

**Observed versus worst-credible impact.** Observed impact limits speculation but systematically lags silent or fast-propagating faults. Worst-credible reasoning preserves options but can overmobilize. Require a mechanism, horizon, evidence, and reassessment time for potential-impact escalation.

**Conservative escalation versus alert fatigue.** Escalating uncertainty protects users and invites expertise. Habitual overclassification consumes responders and makes labels meaningless. Bound uncertainty rules, improve telemetry, track over-response cost, and de-escalate with evidence rather than weakening declarations informally.

**Global versus service-specific policy.** Global levels make cross-team coordination predictable. Service-specific thresholds reflect different user harms. Define common response semantics and hard organizational overrides, then attach product-specific consequence anchors.

**Automated versus human classification.** Automation is fast and consistent for measurable cases. It can inherit missing data, biased denominators, stale policy, and adversarial inputs. Let automation recommend or declare bounded cases, expose its evidence, and preserve immediate human escalation.

**Public versus internal classification.** One vocabulary reduces translation, but internal response and external communication have different confidentiality and aggregation constraints. Maintain an owned mapping and distinct clocks without using the difference to conceal customer harm.

## Failure Modes and Misconceptions

1. **“Every alert is an incident.”** Alerts are notifications; incidents are managed harmful or threatening conditions. Multiple alerts may describe one incident, and incidents can begin without alerts.
2. **“Severity is alert priority.”** Alert urgency routes a notification. Incident severity describes consequence and activates a response package after broader evidence is considered.
3. **“Severity is root-cause importance.”** Severity follows user and protected-property harm, not novelty, technical prestige, or the team that owns the cause.
4. **“Percentage affected is enough.”** Absolute harm, per-subject consequence, duration, distribution, reversibility, and potential propagation matter.
5. **“Unknown impact is low impact.”** Missing or delayed evidence can be correlated with failure; uncertainty must be explicit and may justify temporary escalation.
6. **“Wait for the duration threshold.”** Forward projection and shrinking mitigation windows can require escalation before realized duration crosses a boundary.
7. **“A workaround eliminates impact.”** Workarounds have discoverability, accessibility, correctness, cost, and capacity limits that must be measured.
8. **“A major incident is always SEV-1.”** Coordination mode and consequence severity may have a many-to-many local relationship.
9. **“Security severity can use the outage scale.”** Confidentiality, integrity, legal, evidence, and notification requirements need governed security overlays.
10. **“Staff shortage lowers severity.”** Resource scarcity affects priority and escalation; it does not reduce user harm.
11. **“One healthy graph permits de-escalation.”** Signal loss, delayed effects, queue debt, rollback regression, or continued corruption can remain.
12. **“Downgrading improves reliability.”** It changes reporting, not harm. Independent outcome measures and immutable classification history deter gaming.
13. **“Automation removes judgment.”** Classifiers encode policy and data assumptions; responders must see missingness, version, overrides, and limits.
14. **“Severity never changes.”** Early labels should be provisional. Visible changes are evidence of learning, not necessarily initial error.
15. **“One taxonomy transfers across organizations.”** Labels, products, obligations, and response capabilities differ; portable principles require local definitions.

## Worked Examples

### Example 1

**Situation.** A latency alert pages with “P1,” but investigation shows only an internal dashboard loads slowly; customer operations and deadlines are unaffected.

**Reasoning.** `P1` is the notification route chosen by the alert rule. The event still deserves triage because telemetry may be incomplete. Once scope is confirmed, incident classification records internal observability degradation, no current customer impact, intact diagnostic alternatives, and moderate potential risk if the dashboard is needed during another fault. Local policy may declare a low-severity incident or track an operational problem while adjusting alert routing.

**Conclusion.** Alert priority is evidence and routing context, not the incident severity itself.

### Example 2

**Situation.** One tenant with 800 users cannot sign in; the platform has one million users. The global failure fraction is 0.08%.

**Reasoning.** The global denominator hides $f_{tenant}=800/800=100\%$. Sign-in is a core journey, the tenant has a contractual deadline, and no workaround exists. The classifier uses tenant segmentation and consequence anchors rather than global average alone. It declares the locally defined high-severity response, involves identity and account teams, and communicates through the tenant channel.

**Conclusion.** Concentrated total failure can require intensive response even when global percentage is small.

### Example 3

**Situation.** A background process has silently corrupted 20 documents and continues at one document per minute. No user has opened a corrupted document yet.

**Reasoning.** Observed interactive availability is unaffected, but durability and integrity harm are realized and growing. Recovery metadata expires in two hours, so urgency rises with delay. The hard override for active irreversible data loss applies. Responders declare critical severity, stop writes, preserve logs, measure the affected set, and begin restore analysis before determining the code defect.

**Conclusion.** Actual user tickets are not required when protected data is already being damaged and recovery options are shrinking.

### Example 4

**Situation.** A certificate expires in 15 minutes. Current traffic is healthy, replacement is ready, but the automated deploy path is failing.

**Reasoning.** Observed impact is zero; potential impact is global authentication loss. Urgency is high because delay crosses a known cliff and the normal mitigation path is impaired. The incident is classified according to credible future impact, with explicit reassessment after manual replacement. If a tested alternate deploy succeeds and propagation is verified, responders may de-escalate before customer impact occurs.

**Conclusion.** Severity can be driven by imminent, mechanistically credible harm rather than only realized failures.

### Example 5

**Situation.** A 45-minute outage ends after rollback. The global success SLI is healthy for two minutes, and leadership asks to downgrade immediately.

**Reasoning.** The rollback may regress, caches and queues may still be recovering, and delayed writes may fail. The de-escalation rule requires 20 minutes of cohort-specific success, stable dependency saturation, bounded backlog, no ongoing data inconsistency, and incident-command approval. Communication remains at its current cadence until those conditions hold.

**Conclusion.** Symptom improvement begins monitoring; it does not by itself prove forward risk is controlled.

### Example 6

**Situation.** Two high-severity incidents occur simultaneously: global search latency is worsening, while a smaller payment cohort faces duplicated charges.

**Reasoning.** Both retain their consequence classifications. Scarce payment-database expertise goes first to duplicate charges because harm is irreversible and increasing; additional responders mitigate search through load shedding. The resource decision is recorded as priority, not implemented by downgrading search. Separate incident commands coordinate shared dependencies and leadership.

**Conclusion.** Priority allocates constrained response; it must not rewrite severity to make the queue convenient.

### Example 7

**Situation.** A suspected credential leak has no confirmed misuse and no service outage.

**Reasoning.** Reliability severity alone might appear low. The security overlay uses credential scope, data access, exploitability, evidence sensitivity, notification analysis, and containment urgency. The joint incident activates restricted evidence handling, revocation, audit review, and security command. Public communication follows authorized analysis rather than the outage taxonomy.

**Conclusion.** Independent security classification and a shared incident identity preserve both operational coordination and governed obligations.

### Example 8

**Situation.** Teams A and B classify the same 12% checkout failure as moderate and critical, respectively.

**Reasoning.** The taxonomy says only “significant impact.” A calibration exercise reveals that A considers affected fraction while B considers a time-limited sales event and no workaround. The organization rewrites the anchor with population, core journey, deadline sensitivity, duration, and response package. It retains an override for high financial or contractual consequence and publishes examples just below and above the boundary.

**Conclusion.** Disagreement is evidence that policy language or context is incomplete, not merely that one team is wrong.

### Example 9

**Situation.** A classifier uses an ordinary score and marks 0.02% document corruption low because 99.98% of documents are intact.

**Reasoning.** Any finite volume weight lets enough healthy items dilute corruption. The corrected policy applies `irreversible_data_loss` before percentage thresholds, yielding critical in the executable model. Ordinary scoring remains available for reversible latency and feature degradation after hard predicates are false.

**Conclusion.** Gate-before-aggregation prevents non-substitutable harm from disappearing in a large denominator.

### Example 10

**Situation.** The organization changes its critical threshold from 20% to 10% affected users but compares this year's incident counts directly with last year's.

**Reasoning.** Some events formerly labeled high would now be critical without any change in system behavior. The incident record must retain taxonomy version and original decision. Analysts may normalize old incidents under the new rules in a separate field and explain unavailable data. Trends should also use direct user-outcome measures rather than classification counts alone.

**Conclusion.** Versioned taxonomies preserve historical meaning and prevent policy changes from masquerading as reliability change.

## Cross-Program Connections

- [STQE-048](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) handles test-failure triage and artifact collection; production severity instead classifies live or credible protected-outcome harm.
- [SEC-086](../../25-security-engineering/ROADMAP.md) develops security alert triage, while SEC-087 through SEC-090 own forensics, containment, legal coordination, and security-incident learning.
- [SYSENG-061](../../26-systems-engineering/modules/061-failure-modes-and-effects-analysis.md) reasons prospectively about failure effects; incident severity classifies an unfolding operational condition from current evidence.
- [API-097](../../28-api-and-service-engineering/modules/097-api-metrics-logs-and-traces.md) supplies API-boundary evidence and populations needed for classification.
- [PLAT-087](../../29-platform-engineering/modules/087-incident-response-for-shared-platforms.md) addresses coordination and tenant consequences when one platform incident affects many workloads.

## References

1. Jennifer Mace, Jelena Oertel, Stephen Thorne, Arup Chakrabarti, Jian Ma, and Jessie Yang, “Incident Response,” in *The Site Reliability Workbook*, O'Reilly Media, 2018. [Official online edition](https://sre.google/workbook/incident-response/). Accessed 2026-09-06.
2. Rob Ewaschuk, “Effective Troubleshooting,” in *Site Reliability Engineering: How Google Runs Production Systems*, O'Reilly Media, 2016. [Official online edition](https://sre.google/sre-book/effective-troubleshooting/). Accessed 2026-09-06.
3. Google, “Building Product-Focused Reliability for SRE,” Google SRE Resources, current online edition. [Official resource](https://sre.google/resources/practices-and-processes/product-focused-reliability-for-sre/). Accessed 2026-09-06.
4. Alexander Nelson, Sanjay Rekhi, Murugiah Souppaya, and Karen Scarfone, *Incident Response Recommendations and Considerations for Cybersecurity Risk Management: A CSF 2.0 Community Profile*, NIST SP 800-61 Revision 3, April 2025. [Official publication](https://csrc.nist.gov/pubs/sp/800/61/r3/final). Accessed 2026-09-06.
5. National Institute of Standards and Technology, “Computer Security Incident,” CSRC Glossary, current online entry with source attributions. [Official glossary](https://csrc.nist.gov/glossary/term/Computer_Security_Incident). Accessed 2026-09-06.
6. PagerDuty, “Severity Levels,” PagerDuty Incident Response Documentation, current public edition. [Official documentation](https://response.pagerduty.com/before/severity_levels/). Accessed 2026-09-06.

Current source-specific claims were checked on 2026-09-06. The severity names, thresholds, escalation rule, response examples, and executable classifier in this chapter are educational models, not universal standards, legal advice, regulatory classification, or production guarantees.

## Exercises

### Exercise 1

For an alert reporting elevated database latency, distinguish event, alert priority, incident category, observed impact, potential impact, urgency, severity, coordination mode, status, confidence, and remediation priority.

### Exercise 2

Segment A has 600 failures among 600 attempts; segment B has 400 failures among 999,400 attempts. Compute each segment's failure fraction and the global fraction. Explain why one global threshold can underclassify the incident.

### Exercise 3

Design a classification rule for an asynchronous job service covering backlog delay, permanent job loss, duplicated side effects, loss of all redundancy, unknown telemetry, and a deadline-sensitive customer cohort. Include hard overrides and de-escalation evidence.

### Exercise 4

Two incidents compete for one specialist: a 30% reversible search slowdown and confirmed duplication of 25 payments. Classify impact dimensions and choose resource priority without manipulating severity. State assumptions and communication consequences.

### Exercise 5

Your organization discovers that incidents affecting users of one accessibility feature were repeatedly classified low because they represented 0.05% of total sessions. Redesign the taxonomy, measurements, calibration process, automation, and historical analysis to prevent recurrence.

## Answers to the Exercises

### Answer 1

The event is the measured latency increase. Alert priority is the notification route and urgency chosen by the rule. Incident category might be `latency`, `database`, and `dependency`; it remains separate from severity. Observed impact records which user operations exceeded their objective, with counts, denominators, segments, duration, and workaround. Potential impact records credible queue growth, timeout propagation, or loss of write capacity over a stated horizon. Urgency states how delay changes harm or recovery options. Severity applies the local consequence-and-response policy. Coordination mode says whether one team or incident command is needed. Status describes investigating, mitigating, or monitoring. Confidence records evidence quality and contradictions. Remediation priority orders this work against other incidents. Initial values are provisional and should retain timestamped revisions.

### Answer 2

For A, $f_A=600/600=1$, or 100%. For B, $f_B=400/999{,}400\approx0.00040024$, or about 0.040024%. Globally, failures are $600+400=1{,}000$ among $600+999{,}400=1{,}000{,}000$ attempts, so the rate is 0.1%. A rule based only on global fraction sees modest impact while every eligible attempt in A fails. The taxonomy must preserve segment denominators and core-journey consequence, with an authorized override for total exclusion or other severe concentrated harm.

### Answer 3

Define ordinary dimensions for oldest-job age relative to deadline, affected job fraction, backlog growth, retry amplification, customer segment, and workaround. Hard overrides make confirmed permanent loss or non-idempotent duplicated side effects critical regardless of volume. Loss of all redundancy with continued correct processing can be moderate or high according to time-to-exhaustion and recovery, but it escalates as margin shrinks. Unknown telemetry increases response one level for a bounded reassessment interval rather than implying health. A deadline-sensitive cohort uses its own denominator and consequence anchor. De-escalation requires stopped loss or duplication, stable admission and processing, bounded backlog with positive drain margin, restored redundancy, trustworthy telemetry, reconciled side effects, and sustained cohort-specific objectives under incident-owner approval.

### Answer 4

Assume search results remain correct and the slowdown is reversible, while duplicate charges create real financial harm requiring reconciliation. Search has broad availability or latency impact with a workaround; payments affect fewer users but violate correctness, may trigger financial or contractual duties, and worsen per duplicate. Both may meet the local high-severity definition. Give the payment specialist to containment of duplicate charging because marginal delay creates irreversible additional harm; use other responders to degrade or shed search safely. Record this as priority and resource allocation, not a search downgrade. Maintain each incident's appropriate update cadence, customer communication, and leadership path, coordinating shared dependencies if necessary.

### Answer 5

Add the accessibility journey as an explicit protected population with its own eligible denominator and consequence definition. Create an override for total or severe loss of an essential accessibility path, reviewed with affected users and accessibility owners rather than chosen from global volume. Instrument success and latency by feature without exposing sensitive identity, and alert on its outcome and telemetry missingness. Add boundary scenarios to tabletop calibration and compare classifications across roles. Make automation evaluate segment rules before global aggregation and expose taxonomy version and missing data. Reassess past incidents using available raw populations in a separate normalized field while preserving original labels; report data gaps rather than inventing values. Track classification and mitigation delay for the cohort, and require periodic review so product or population change does not make the rule stale.
