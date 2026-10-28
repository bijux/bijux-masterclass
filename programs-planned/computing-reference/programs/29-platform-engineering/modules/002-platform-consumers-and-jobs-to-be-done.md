---
module_id: PLAT-002
program: Platform Engineering
level: 1
module_number: 2
title: Platform Consumers and Jobs to Be Done
status: complete
last_verified: 2026-08-29
---

# Platform Consumers and Jobs to Be Done

## One-Page Review

### Governing question

Who consumes an internal platform, what progress are they trying to make in a specific circumstance, what do they use today, and which recurring jobs should the platform help them accomplish without taking over domain authority?

### Essential definitions

- A **platform consumer** is a person or team that uses, depends on, supports, governs, or is materially affected by a platform capability while pursuing another outcome.
- A **consumer segment** groups people by relevant job, context, constraints, behavior, and required outcome—not merely job title, seniority, or demographic.
- A **job to be done (JTBD)** is progress a consumer seeks in a circumstance. It is more stable than a feature request and broader than one tool interaction.
- A **functional job** concerns accomplishing work; an **emotional job** concerns how the consumer wants to feel; a **social job** concerns how they need to be perceived or coordinate with others.
- A **job statement** names circumstance, desired progress, and outcome without embedding a solution: “When ..., I need to ..., so that ...”
- A **current alternative** is the process, tool, queue, workaround, or decision to do nothing that a consumer presently uses to make progress.
- A **struggle** is observable friction, risk, delay, uncertainty, rework, or exclusion in the current job.
- A **constraint** is a real boundary such as authority, accessibility, regulation, skill, workload, risk, locality, cost, or legacy integration.
- An **outcome criterion** describes how a consumer judges success, including quality, time, confidence, recoverability, autonomy, and risk.
- A **research finding** is a traceable synthesis supported by evidence; a feature request or stakeholder opinion is an input, not automatically a finding.

### Central model, mechanism, or theorem

Represent a candidate job as

\[
J=(C,A,P,O,K,E),
\]

where \(C\) is circumstance, \(A\) actor/segment, \(P\) desired progress, \(O\) outcome criteria, \(K\) constraints, and \(E\) current evidence. A platform capability hypothesis is defensible only if evidence shows recurring underserved progress, legitimate commonality across consumers, platform authority to act, and a bounded outcome:

\[
Eligible(J)=Recurring\land Underserved\land Commonable
\land Authorized\land Supportable.
\]

This is a review gate, not a numerical truth. A frequent job may remain outside platform ownership because its semantics differ by domain or the platform lacks authority.

### Critical invariants

- Consumer groups are evidence-based and can contain different roles sharing one job or one role performing several jobs.
- Job statements remain solution-neutral and preserve the consumer's real outcome.
- Research covers current behavior, triggers, alternatives, workarounds, failures, recovery, and non-use—not only desired features.
- Direct users, supporting actors, operators, reviewers, affected stakeholders, and excluded/non-adopters are considered.
- Findings preserve dissent, context, frequency, consequence, uncertainty, and evidence provenance.
- Platform hypotheses state which burden changes and which domain decisions remain with consumers.
- Adoption, satisfaction, interview count, ticket volume, or telemetry alone is never treated as proof of product value or representative need.

### Common failures

Teams call every employee “the developer”; build personas from stereotypes; interview only platform champions; ask “what feature do you want?”; translate a requested portal into a job; confuse a platform task with the consumer's broader outcome; ignore operators, reviewers, disabled users, novices, non-adopters, and teams that left; average incompatible contexts; prioritize loud executives or ticket volume; treat a workaround as irrational; or centralize domain decisions because consumers report pain.

### Compact example

A team asks for a “one-click database button.” Observation reveals the job: when launching a service that stores regulated records, the team needs a supported database environment with known ownership, access, backup, restore, cost, and readiness evidence so it can accept traffic confidently. The button is one proposed interface. The platform can own provisioning mechanics, status, safe defaults, and evidence; the team retains data meaning, classification, authorization, capacity intent, retention, and recovery objectives.

### Connections

[PLAT-001](001-platform-engineering-as-complexity-management.md) established capability and ownership boundaries. Later modules deepen cognitive load, platform-as-product, self-service, paved roads, developer journeys, interfaces, research, adoption, and outcome measurement. This module establishes whose work and which progress those mechanisms must serve.

## Governing Question

Which people and teams are trying to make what progress, under which conditions, and what evidence shows that a shared platform intervention is preferable to better documentation, a provider service, a team-local solution, an organizational change, or no new product?

The question prevents feature-first platform planning. “Build a portal,” “standardize Kubernetes,” and “offer every cloud service” begin with solutions. Consumer/job discovery begins with observed work and preserves the possibility that the right response is a smaller interface, a removed approval, clearer ownership, or an enabling engagement.

## Why This Matters

Platforms are products whose users are internal but not captive in any meaningful design sense. A mandate can force traffic through a platform while users create shadow automation, escalate every failure, or lose delivery capability. CNCF guidance emphasizes building capabilities and interfaces with users. DORA's platform research reports mixed effects and identifies user-centeredness and developer independence as important context. Neither tool installation nor adoption establishes useful progress.

“Developer” is too coarse. A new application engineer deploying a stateless service, a data scientist scheduling a GPU experiment, a security reviewer tracing an exception, an operator restoring shared state, and a finance partner investigating cost may touch the same platform but pursue different outcomes. Even one engineer changes jobs during creation, incident response, migration, and retirement.

Jobs-to-be-done reasoning shifts attention from attributes to circumstances and progress. Consumers “hire” current tools, tickets, scripts, colleagues, and manual checks because those alternatives satisfy something: control, familiarity, auditability, speed, or blame avoidance. A platform that removes visible steps but destroys trusted evidence can be worse. Study why the workaround persists before replacing it.

Internal research has power and risk. Employees may fear criticizing a mandated platform; telemetry can expose performance or sensitive work; managers may influence recruitment; accessibility needs can be hidden; contractors and distributed teams may be excluded. Consent, minimization, anonymization, safe reporting, and separation from performance evaluation are part of research validity.

## Prerequisites and Retrieval

Retrieve product hypotheses, qualitative and quantitative evidence, sampling, confounding, workflows, service boundaries, authorization, support, accessibility, and the capability/complexity model from [PLAT-001](001-platform-engineering-as-complexity-management.md).

Keep distinct:

- person, role, team, segment, and job;
- feature request, underlying job, and validated requirement;
- task completion and useful outcome;
- frequency and consequence;
- direct consumer and affected stakeholder;
- declared preference and observed behavior;
- correlation in telemetry and causal explanation;
- shared mechanism and domain-specific decision.

## Learning Objectives

By the end of this module, you should be able to:

1. identify direct, indirect, supporting, governing, affected, and excluded platform consumers;
2. segment consumers by relevant job, circumstance, constraints, and behavior;
3. write solution-neutral functional, emotional, and social job statements;
4. distinguish jobs, needs, tasks, journeys, features, and capabilities;
5. investigate triggers, current alternatives, struggles, workarounds, and switching forces;
6. combine interviews, contextual observation, artifacts, telemetry, tickets, surveys, and experiments appropriately;
7. synthesize findings with provenance, counterevidence, uncertainty, and segment limits;
8. assess recurrence, underserved outcomes, commonability, authority, supportability, consequence, and exclusion;
9. turn a validated job into a bounded platform hypothesis without absorbing domain ownership; and
10. bound internal research evidence and require named review for high-consequence platform decisions.

## Core Exposition

### Map the consumer system

Start beyond “end users.” **Direct consumers** invoke platform interfaces. **Application and product teams** own workloads and outcomes. **Supporting consumers** help with migration, troubleshooting, and enablement. **Operators** respond to shared failures. **Reviewers and governors** inspect policy and evidence. **Providers** supply underlying services. **Affected stakeholders** experience consequences without touching the platform. **Non-users** choose alternatives, cannot gain access, or abandon the platform.

For each group, record responsibilities, authority, incentives, knowledge, accessibility needs, risk exposure, work location/time, tools, dependencies, and consequences of failure. Do not equate organizational rank with product priority. A release manager who uses the platform weekly may have a high-consequence job; a developer who visits daily may have low-cost repetitive work.

Map relationships. One team's self-service request can create on-call work for another. A security guardrail can simplify audit while blocking an accessible workflow. A platform default can reduce application setup while concentrating provider cost. Consumer research must include downstream work and externalities.

### Segment by job and circumstance

Personas are useful when grounded in evidence and relevant variation. “Senior Sam likes terminals” is a stereotype. Better segments might be:

- a team launching its first externally reachable service under standard policy;
- an experienced team migrating a stateful service with a fixed outage window;
- an operator diagnosing cross-tenant identity failure during an incident;
- a reviewer assessing evidence for a regulated release;
- a contractor with time-limited access working through assistive technology.

One person can occupy several segments. Several titles can share a job. Segment only on differences likely to change need or solution: workload archetype, experience, regulatory context, failure consequence, frequency, authority, tool access, accessibility, geography, or support model.

### Define the job

A job describes progress, not a platform interaction. “Create a Kubernetes namespace” is a task or solution. “Establish an isolated, owned environment in which a team can safely test a service” is closer to the job. The enduring outcome can survive a move from Kubernetes to another substrate.

Use:

> When **circumstance/trigger**, I need to **make progress**, so that **outcome**,
> while **constraints and risks**.

Functional progress might be provisioning or recovery. Emotional progress can be confidence that a release is supportable. Social progress can be demonstrating responsible control to peers or auditors. These are not decorative: a technically fast path with opaque evidence may fail the confidence and accountability jobs.

Separate the **core job** from adjacent jobs. A team launching a service may also need budget approval, domain authorization, training, and incident ownership. The platform can support some steps without claiming the whole business outcome. Define start, finish, and authority.

### Study current alternatives and switching forces

Consumers already do something. They may use cloud consoles, copied scripts, tickets, spreadsheets, colleagues, an older platform, or delay work. Observe the alternative end to end. Record active time, waits, handoffs, errors, recovery, evidence, cost, and what users protect.

A switch has forces: dissatisfaction pushes away from the current approach; attraction pulls toward a candidate; anxiety makes change risky; habit and sunk integration preserve the status quo. For internal platforms, mandates and organizational incentives add pressure. A consumer can rationally retain a slower script because it is debuggable, locally owned, and proven during incidents.

Ask for specific recent events: “Tell me about the last production credential rotation.” Reconstruct trigger, steps, artifacts, surprises, decisions, people, outcome, and aftermath. Hypothetical preference questions invite politeness and solution fantasy.

### Use complementary research methods

**Contextual observation** exposes tacit steps, interruptions, artifacts, accessibility barriers, and workarounds. **Interviews** reveal motives, interpretation, anxiety, and consequences. **Artifact analysis** examines scripts, configuration, runbooks, tickets, chat, and review records. **Telemetry** shows paths, duration, errors, abandonments, and variation where instrumentation is valid. **Support data** reveals recurring confusion and ownership gaps. **Surveys** can estimate distribution after concepts are grounded. **Experiments and prototypes** test behavior.

No method is sufficient alone. Telemetry says what the instrument captured, not why. Tickets overrepresent people who know how and are willing to ask. Interviews suffer recall and status pressure. Observation changes behavior. Surveys encode the researcher's categories. Triangulate and preserve disagreements.

Recruit across relevant variation, including novices, experts, disabled users, remote/time-zone workers, contractors, regulated teams, high-consequence operators, non-adopters, and unsuccessful users. Do not use a universal sample-size ritual. Continue until priority decisions have adequate coverage and new evidence no longer changes the model materially; record unrepresented groups.

### Protect participants and evidence

State purpose, voluntary participation, recording, use, retention, access, and withdrawal. Minimize names, repository content, credentials, incident details, and performance signals. Aggregate carefully: a small internal segment can remain identifiable. Do not send raw criticism to line managers or use research as employee evaluation.

Research repositories need access controls, retention, provenance, and expiration. A finding records method, segment, date, context, evidence links, researcher, confidence, counterevidence, and decisions affected. Old findings become hypotheses when organization, platform, policy, or workforce changes.

### Synthesize without flattening

Code observations into triggers, jobs, struggles, alternatives, constraints, outcomes, and switching forces. Cluster only when commonality is supported. Preserve edge cases separately; a low-frequency accessibility or safety barrier can be critical.

A finding should say:

> In **segment/context**, evidence from **methods and cases** indicates **behavior or
> struggle**, affecting **outcome**, under **constraints**. Confidence is **bounded**
> because **gaps/counterevidence**.

Distinguish evidence, interpretation, and recommendation. “Seven teams wait for network approval” is evidence. “Policy ambiguity causes the wait” is an interpretation to test. “Build network automation” is one recommendation competing with clarifying policy or changing authority.

### Prioritize jobs, not votes

Assess:

- **recurrence:** how often and across how many relevant consumers;
- **consequence:** delay, failure, security, safety, exclusion, or cost;
- **underserved outcome:** current success and dissatisfaction;
- **commonability:** shared mechanism versus legitimate variation;
- **platform authority:** whether the platform may decide or only enable;
- **supportability:** ability to build, operate, evolve, and retire;
- **strategic fit:** connection to organizational outcomes;
- **equity and accessibility:** who gains, pays, or remains excluded.

Do not multiply uncertain scores into false precision. Use an evidence table and decision record. High-frequency low-consequence toil may justify automation; rare emergency recovery can justify capability because consequence is high. A common painful domain decision can remain outside platform ownership.

### Form a capability hypothesis

Translate a job into:

> For **segment** in **circumstance**, a platform capability that **changes a named
> burden** will improve **outcome criteria**, while preserving **guardrails,
> consumer authority, and escape**, as tested by **evidence**.

The hypothesis can fail. Specify current alternative and expected switching barrier. Begin with the thinnest intervention capable of testing it: documentation, a supported example, an API wrapper, an enabling engagement, or prototype before a custom control plane.

### Deterministic evidence gate

This synthetic artifact requires independent evidence types plus recurrence, consequence, commonability, authority, and supportability. It deliberately rejects a domain retention decision despite evidence of pain because the platform lacks decision authority.

<!-- bijux-verify: {"id":"job-evidence-gate","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"deploy_service evidence_types=4 qualified=True\nrotate_credential evidence_types=3 qualified=True\nchoose_business_retention evidence_types=2 qualified=False\nqualified_jobs=['deploy_service', 'rotate_credential']\n","stderr":""}} -->
```python
jobs = [
    {
        "name": "deploy_service",
        "evidence": ["observation", "interview", "telemetry", "support"],
        "recurring": True, "consequential": True, "commonable": True,
        "authorized": True, "supportable": True,
    },
    {
        "name": "rotate_credential",
        "evidence": ["observation", "incident", "telemetry"],
        "recurring": True, "consequential": True, "commonable": True,
        "authorized": True, "supportable": True,
    },
    {
        "name": "choose_business_retention",
        "evidence": ["interview", "policy_review"],
        "recurring": True, "consequential": True, "commonable": False,
        "authorized": False, "supportable": True,
    },
]

qualified = []
for job in jobs:
    evidence_types = len(set(job["evidence"]))
    gates = (
        evidence_types >= 2,
        job["recurring"],
        job["consequential"],
        job["commonable"],
        job["authorized"],
        job["supportable"],
    )
    passed = all(gates)
    if passed:
        qualified.append(job["name"])
    print(f"{job['name']} evidence_types={evidence_types} qualified={passed}")

print(f"qualified_jobs={qualified}")
```

The run proves only deterministic evaluation of synthetic Boolean inputs. It does not establish representative research, causal need, true frequency or consequence, platform authority, ethical collection, product fit, or roadmap priority.

## Definitions and Notation

Let \(A\) be actors, \(C\) circumstances, \(P\) desired progress, \(O\) outcome criteria, \(K\) constraints, \(X\) current alternatives, and \(D\) evidence items. A candidate job \(J=(A,C,P,O,K,X)\) is supported by evidence subset \(D_J\), not by the tuple's elegance.

A **need** is something required for a consumer to achieve an outcome. A **job** organizes needs around progress in context. A **task** is one action in current or proposed work. A **journey** orders interactions and transitions over time. A **feature** is product behavior. A **capability** is a supported outcome the platform offers. These can trace to one another but are not interchangeable.

Let \(source(d)\), \(segment(d)\), \(context(d)\), and \(date(d)\) preserve provenance for evidence item \(d\). **Triangulation** means a claim is examined through meaningfully different evidence sources or methods; repeating one survey question does not create independent evidence.

An **outlier** is an observation distant from a cluster, not automatically an error. An **extreme user** experiences constraints that can reveal hidden assumptions. A **non-user** is in scope but does not consume the platform; the reason can be access, fit, awareness, distrust, mandate avoidance, migration cost, or a superior alternative.

## Mechanisms, Invariants, or Proof Structure

Use this discovery-to-decision chain:

1. **State the decision.** Name what roadmap, capability, or boundary choice the research will inform.
2. **Map actors and effects.** Include direct, supporting, governing, affected, and absent voices.
3. **Declare assumptions and gaps.** Convert stakeholder opinions into research questions.
4. **Sample relevant variation.** Recruit by job circumstances and include non-success.
5. **Study current behavior.** Observe recent real work, artifacts, alternatives, failures, and recovery.
6. **Triangulate.** Combine qualitative explanation with behavioral, operational, and documentary evidence.
7. **Protect participants.** Obtain consent, minimize data, control access, and prevent performance use.
8. **Synthesize traceably.** Separate evidence, interpretation, counterevidence, and recommendation.
9. **Assess platform fit.** Recurrence, consequence, commonability, authority, supportability, and exclusion.
10. **Test the thinnest hypothesis.** Define outcomes, guardrails, disconfirmation, and review date.

The **solution-neutrality invariant** rejects a job statement that names the portal, cluster, template, command, or vendor it is meant to justify. The **authority invariant** prevents consumer pain from granting the platform authority over business meaning, legal policy, risk acceptance, or application promises.

The **representation invariant** requires every segment claim to name research coverage and gaps. The **provenance invariant** makes a finding traceable to protected evidence without exposing participants. The **disconfirmation invariant** states what evidence would weaken or reject the capability hypothesis.

Review high-consequence findings with relevant humans before changing a shared control. Automation can validate formatting, counts, and trace links. It cannot establish that research was coercion-free, interpretation fair, a marginalized group represented, or authority legitimate.

## Alternatives and Trade-Offs

**Role personas versus job segments.** Role personas are easy to communicate but can harden stereotypes. Job segments cross titles and remain tied to circumstances. Retain role only where authority or environment changes the outcome.

**Interviews versus observation.** Interviews reveal meaning, emotion, and remembered consequence. Observation reveals tacit behavior and workarounds. Use both when the decision matters; neither is an objective transcript of reality.

**Telemetry versus self-report.** Telemetry scales and shows instrumented behavior. It misses motives, offline work, inaccessible attempts, and uninstrumented alternatives. Self-report supplies interpretation but carries recall and status bias.

**Broad platform versus bounded segment.** A broad product promises leverage but averages incompatible jobs. Starting with one coherent segment enables learning but may exclude others. Publish scope and expansion evidence instead of calling the first path universal.

**High frequency versus high consequence.** Frequency identifies repeated toil. Consequence identifies rare but material recovery, safety, or compliance needs. Keep both dimensions visible rather than using one ranking.

**Common default versus legitimate variation.** A shared mechanism can reduce burden; forced sameness can destroy domain fit. Standardize invariant mechanics, expose declared choices, and retain accountable alternatives.

**Research depth versus delivery speed.** Excessive study can delay reversible learning; shallow research can scale the wrong control. Match evidence to reversibility, blast radius, cost, and affected people.

## Failure Modes and Misconceptions

1. **“Our consumer is the developer.”** Different jobs, constraints, and affected actors disappear.
2. **“A persona is a creative biography.”** Unverified traits create stereotype-driven design.
3. **“A job is a platform task.”** Tool steps are current means, not necessarily enduring progress.
4. **“Users asked for a portal.”** That is a solution request whose underlying job remains unknown.
5. **“The loudest team represents demand.”** Access, status, and familiarity distort feedback.
6. **“Tickets show all pain.”** Blocked, resigned, and excluded consumers may never file one.
7. **“Telemetry is objective.”** Instrumentation choices and missing paths shape the data.
8. **“Saturation means everyone agrees.”** It means new sampled evidence no longer changes the model materially; sampling gaps remain.
9. **“More interviews guarantee truth.”** Recruitment and interpretation quality matter more than ritual counts.
10. **“A recurring need belongs on the platform.”** Commonability, authority, supportability, and alternatives still decide fit.
11. **“Internal research needs no consent.”** Employment power and identifiable data increase ethical obligations.
12. **“One job has one solution.”** Documentation, organizational change, managed service, platform capability, or no intervention can compete.
13. **“Adoption validates the job.”** Mandate and absent alternatives confound use.
14. **“Edge users can wait.”** Accessibility and high-consequence constraints can reveal core defects.

## Worked Examples

### Example 1

**Question:** Is “backend developer” a sufficient platform consumer segment?

**Reasoning:** It does not distinguish first deployment, stateful migration, incident recovery, regulated release, experience, or accessibility. Those circumstances change outcomes and constraints.

**Conclusion:** Segment by job-relevant variation, not title alone.

### Example 2

**Question:** Ten teams request a web portal. Is the job validated?

**Reasoning:** They share a proposed interface, not necessarily one problem. Some need discovery, others status, evidence, or fewer approvals.

**Conclusion:** Reconstruct recent work before treating the request as common demand.

### Example 3

**Question:** Why study a team that abandoned the platform?

**Reasoning:** Successful-user telemetry cannot reveal failed access, migration cost, missing capability, distrust, accessibility barrier, or a better alternative.

**Conclusion:** Non-use is behavior requiring explanation, not noise.

### Example 4

**Question:** A copied script is slower than self-service. Why might consumers keep it?

**Reasoning:** It may be inspectable, versioned, locally repairable, and independent of a shared outage. Switching creates uncertainty and ownership loss.

**Conclusion:** Preserve valued outcomes while reducing burden.

### Example 5

**Question:** Ticket data shows database requests dominate. Should databases be first?

**Reasoning:** Perhaps, but tickets may reflect a mandatory process while invisible problems have no channel. Compare consumers, consequence, wait, recurrence, alternatives, and platform authority.

**Conclusion:** Volume is one evidence dimension.

### Example 6

**Question:** Can one interview support a job finding?

**Reasoning:** It can reveal a hypothesis or critical hazard. Generalization requires relevant additional evidence; a severe accessibility or safety defect may warrant action without prevalence estimates.

**Conclusion:** Match claim strength and action to evidence and consequence.

### Example 7

**Question:** Teams struggle to choose lawful retention. Should the platform choose it?

**Reasoning:** The platform can present approved classes, policy sources, evidence, and enforcement. Authorized data/domain owners choose based on purpose and law.

**Conclusion:** Enable a consequential decision without absorbing it.

### Example 8

**Question:** Satisfaction rises after a mandate. Does that prove fit?

**Reasoning:** Respondents may adapt, fear criticism, or compare against removed alternatives. Pair protected research with task outcomes, support, exceptions, reliability, and non-user evidence.

**Conclusion:** Preserve plausible rival explanations.

### Example 9

**Question:** Should raw interview recordings be linked from a platform roadmap?

**Reasoning:** Broad access can identify critics and expose incidents or credentials. Store protected evidence, publish de-identified findings, and retain consent/expiry controls.

**Conclusion:** Traceability does not require uncontrolled disclosure.

### Example 10

**Question:** A public-benefits platform team observes slow eligibility decisions. May it automate policy interpretation?

**Reasoning:** No. The job and burden are real, but statutory meaning, evidence standards, due process, adverse-action notice, accessibility, fairness, appeal, and public accountability require authorized program officials, caseworkers, administrative-law counsel, policy authors, civil-rights/privacy officers, accessibility and multilingual experts, affected communities, data/security/reliability specialists, oversight bodies, and independent legal/social/technical review. No external review is claimed.

**Conclusion:** Research evidence does not create domain or democratic authority.

## Cross-Program Connections

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies stakeholder, mission, context, measure, validation, and authority analysis. Consumer jobs specialize that work for an internal platform product but do not replace whole-system stakeholder analysis.

[Software Engineering: Patterns, Architecture, and Practice](../../11-software-engineering-patterns/ROADMAP.md) and [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) protect stable boundaries and domain authority. A platform job can justify shared mechanism without centralizing business semantics.

[Software Delivery and Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) supplies workflow, wait, failure, incident, and recovery evidence. [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) turns validated jobs into durable interfaces.

[Security Engineering](../../25-security-engineering/ROADMAP.md) governs research data, insider power, access, and high-consequence controls. [Cloud and Infrastructure Engineering](../../30-cloud-and-infrastructure-engineering/ROADMAP.md) supplies underlying mechanisms and alternatives that consumers currently use or the platform composes.

## References

- Clayton M. Christensen, Taddy Hall, Karen Dillon, and David S. Duncan, [*Know Your Customers' “Jobs to Be Done”*](https://hbr.org/2016/09/know-your-customers-jobs-to-be-done), *Harvard Business Review*, 2016. Circumstance, progress, current alternatives, and functional/social/emotional dimensions.
- CNCF TAG App Delivery, [*CNCF Platforms White Paper*](https://tag-app-delivery.cncf.io/whitepapers/platforms/), 2023. Platform-user research, product partnership, capability/interface ownership, feedback, and adoption guidance.
- DORA, [*2024 Accelerate State of DevOps Report*](https://dora.dev/research/2024/dora-report/), corrected edition v2024.3. Empirical user-centeredness, developer independence, platform effects, mixed outcomes, and methodological limitations.
- UK Government Digital Service, [*User Research for Government Services: An Introduction*](https://www.gov.uk/service-manual/user-research/how-user-research-improves-service-design), current Service Manual. Continuous inclusive research, observation, team exposure, and evidence use.
- UK Government Digital Service, [*Learning About Users and Their Needs*](https://www.gov.uk/service-manual/user-research/start-by-learning-user-needs), current Service Manual. Current behavior, evidence-based solution-neutral needs, broad users, and validation.
- Catherine Courage and Kathy Baxter, [*Understanding Your Users*](https://www.sciencedirect.com/book/9780128002322/understanding-your-users), second edition, Morgan Kaufmann, 2015. User-research planning, field methods, analysis, and ethical practice.
- Nicole Forsgren, Margaret-Anne Storey, Chandra Maddila, Thomas Zimmermann, Brian Houck, and Jenna Butler, [*The SPACE of Developer Productivity*](https://queue.acm.org/detail.cfm?id=3454124), *ACM Queue* 19(1), 2021. Multidimensional evidence and warnings against single developer-productivity metrics.
- ISO, [ISO 9241-210:2019 — Human-Centred Design for Interactive Systems](https://www.iso.org/standard/77520.html), reviewed and confirmed 2025. Current human-centered design principles and lifecycle framing.

## Exercises

### Exercise 1

Map consumers for an internal service-deployment platform. Include direct users, application owners, operators, security/reliability reviewers, enabling/support teams, providers, affected stakeholders, non-users, and excluded users. Define job-relevant segments without stereotypes.

### Exercise 2

Rewrite these feature requests as evidence-seeking job hypotheses: “build a portal,” “add one-click production,” “support every database,” “show a green compliance badge,” and “hide all cloud details.” State current alternative, outcome, constraints, and disconfirming evidence.

### Exercise 3

Design a research plan for credential rotation across application teams. Include decision, assumptions, recruitment, consent, observation, interviews, artifacts, telemetry, incidents, synthesis, privacy, evidence gaps, and stopping/review criteria.

### Exercise 4

Compare three candidate jobs—first deployment, routine database provisioning, and rare regional recovery—using recurrence, consequence, underserved outcomes, commonability, authority, supportability, strategic fit, and exclusion. Explain why a scalar vote is insufficient.

### Exercise 5

A hospital group proposes a platform capability for deploying clinical decision-support models. Identify consumers and jobs, research methods, platform/domain boundaries, evidence, guardrails, and named human reviews required before a roadmap or operational claim is accepted.

## Answers to the Exercises

### Answer 1

Direct segments include a novice team making its first standard deployment, an experienced team repeating routine changes, a stateful team migrating under an outage window, and an incident responder recovering service. Application owners choose domain behavior and service objectives. Platform operators handle control-plane reliability; security and reliability reviewers inspect evidence; enabling teams assist migrations; identity, cloud, and observability providers supply mechanisms. Leadership/finance may evaluate portfolio outcomes. Customers and support staff are affected by deployment failure without using the platform.

Research non-users who use direct cloud paths, copied automation, legacy platforms, or tickets; teams that abandoned migration; contractors and remote staff; users of assistive technology; regulated and high-consequence teams; and teams denied access. Segment by job circumstance, workload, experience, authority, consequence, regulatory and accessibility constraints—not invented personality. One person can move among segments.

### Answer 2

“Build a portal” becomes: when discovering and requesting supported capabilities across fragmented systems, consumers need one trustworthy view of eligibility, ownership, status, and next action so they can progress without searching or bouncing between queues. Current alternatives are wikis, chats, tickets, and provider consoles. A portal is rejected if better catalog/API integration solves the job or users still wait on hidden queues.

“One-click production” becomes: when a reviewed release is ready, an authorized owner needs to initiate and observe a bounded production change with known evidence, recovery, and responsibility. “Every database” becomes choosing a supported data capability that fits declared needs without relearning organizational integration; legitimate engine variation can disconfirm a universal catalog. A green badge becomes the reviewer's job of tracing which claims passed, failed, expired, or were accepted—not decorative compliance. Hiding cloud details becomes reducing irrelevant provider mechanics while preserving choices and diagnostics needed for capacity, cost, recovery, and incidents. Each hypothesis names measurable task/outcome, guardrails, and evidence that would reject the proposed interface.

### Answer 3

Decision: whether shared credential-rotation capability and which boundary should enter the roadmap. Assumptions include rotation being uniform, failures caused by tooling, and teams willing to delegate. Recruit across languages, workload types, secret stores, maturity, frequency, outages, regulatory contexts, contractors, accessibility needs, non-adopters, platform/security operators, and incident responders.

With informed voluntary consent, observe recent rotation in normal context; reconstruct last success/failure interviews; inspect sanitized scripts, runbooks, tickets, audit and incident records; analyze aggregate timing, error, retry, rollback, and support telemetry. Never collect secrets. Separate research from performance evaluation, de-identify reports, restrict raw evidence, and set retention. Synthesize triggers, authority, dependencies, waits, workarounds, confidence, recovery, and desired outcomes with counterexamples. Gaps include rare providers, emergencies, and silent failures. Stop a round when the decision has coverage and new cases no longer materially change the model; review after prototypes, incidents, policy/provider change, and segment expansion.

### Answer 4

First deployment may be frequent and underserved for new teams, commonable around identity/build/telemetry, within platform authority, and strategically useful, though experienced-team data must not dominate novice needs. Routine database provisioning may have high recurrence and wait, but commonability ends at supported service classes; applications retain data semantics, recovery and retention choices. Regional recovery may be rare but high consequence, cross-team, and operationally strategic; it needs exercises and provider/reliability authority rather than popularity.

Use a decision table with evidence provenance and ranges. A scalar hides whether high frequency compensates for catastrophic consequence, whether a painful job is outside platform authority, and who bears exclusion or operating cost. A defensible portfolio can select a thin first-deployment path, bounded database classes, and a recovery capability/exercise even with low observed frequency. Record trade-offs, missing evidence, owners, and review triggers.

### Answer 5

Consumers include model developers, data scientists, application teams, clinical informaticians, clinicians, pharmacists/nurses where relevant, platform and hospital operators, security/privacy/reliability reviewers, biomedical integration teams, regulators, and support/training staff. Patients are affected stakeholders; include accessible, multilingual, marginalized, and non-digital experiences through ethical representative research. Jobs include producing traceable artifacts, obtaining authorized review, deploying safely, monitoring model/data drift, understanding recommendations, overriding, recovering during downtime, investigating harm, and retiring versions.

Observe current model-to-care workflows, shadow review and downtime, interview each authority, inspect de-identified artifacts/incidents, analyze deployment/override/failure telemetry, test prototypes, and study non-use. The platform can own artifact provenance, isolated environments, release workflow, policy evidence, monitoring mechanisms, rollback, inventory, and technical status. It must not decide clinical purpose, validity, patient suitability, treatment, acceptable bias, consent, or residual clinical risk.

Guardrails require versioned model/data provenance, separation of duties, representative validation evidence, privacy/security, accessibility, human review and override, fail-safe downtime behavior, drift and adverse-event monitoring, rollback, and retirement. Named review includes clinical specialty and informatics, patient safety, pharmacy/nursing as applicable, data stewardship/statistics, human factors/accessibility, privacy/legal/ethics, cybersecurity, reliability/platform/biomedical engineering, operations/training, affected-patient representatives, regulators, and independent clinical/technical assurance. Internal research and platform tests cannot establish clinical validity, fairness, regulatory acceptance, or authorization; no external review is claimed.
