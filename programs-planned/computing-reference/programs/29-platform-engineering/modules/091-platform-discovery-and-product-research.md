---
module_id: PLAT-091
program: Platform Engineering
level: 2
module_number: 91
title: Platform Discovery and Product Research
status: complete
last_verified: 2026-09-02
---

# Platform Discovery and Product Research

## One-Page Review

### Governing question

How should a platform team discover consequential developer problems, test whether a shared platform intervention can improve them, and turn mixed qualitative and quantitative evidence into bounded product decisions without confusing requests, adoption, or executive preference with user value?

### Essential definitions

- **platform discovery** is continuous reduction of uncertainty about users, work, problems, constraints, opportunities, interventions, and outcomes before and during delivery.
- A **user** is a person who directly performs work through or around the platform; a **customer** may fund, govern, secure, operate, support, or depend on that work without using the interface directly.
- A **critical journey** is an end-to-end job such as creating, changing, operating, diagnosing, governing, or retiring a service, including handoffs and waiting.
- A **need** describes an outcome a user must achieve under constraints; a **request** is one proposed solution and is evidence of a concern, not proof of the underlying need.
- A **research question** states what must be learned to make a decision; it is not an interview question or a disguised feature pitch.
- An **assumption** is an unverified belief whose failure could change a decision; **risk** combines its uncertainty and consequence.
- An **observation** records what occurred or was said in context; a **finding** interprets patterns across observations; an **insight** explains why the pattern matters to a decision.
- **triangulation** checks a claim through multiple participants, contexts, methods, or data sources whose biases are not identical.
- A **prototype** is a deliberately incomplete representation used to answer named questions; a **pilot** exposes a bounded real workflow to operational consequences.
- **adoption** is eligible users beginning use; **retention** is continued voluntary use; neither alone proves improved delivery, safety, or cognitive load.

### Central model, mechanism, or theorem

For opportunity $p$, keep an evidence ledger rather than a single score:

$$
E(p)=\langle U,J,O,S,Q,A,C,R\rangle,
$$

where $U$ identifies user segments, $J$ the affected journeys, $O$ observed problems, $S$ supporting sources, $Q$ contradictory or uncertain evidence, $A$ assumptions, $C$ constraints and $R$ the reversible decision being considered. A decision gate asks whether the evidence is relevant, sufficiently varied, recent, ethically obtained, traceable to raw observations, and strong enough for the consequence of the next action.

Discovery should choose the smallest reversible experiment that best reduces decision-critical uncertainty:

$$
x^*=\arg\max_{x\in X}\frac{ExpectedDecisionInformation(x)}{Cost(x)+Risk(x)+Delay(x)},
$$

used as a reasoning frame, not as a claim that information value is known precisely.

### Critical invariants

- Every study starts with a decision, research questions, assumptions, participant segments, method, ethics/privacy plan, analysis plan, owner, and expiry.
- Recruitment represents affected roles, contexts, maturity, accessibility, geography, risk and non-users; convenience samples are labeled rather than generalized.
- Raw observations remain distinguishable from interpretation, recommendation and product commitment, with traceable provenance and contradictory evidence preserved.
- Research measures end-to-end work and outcomes, including tickets, waiting, handoffs, workarounds, incidents and abandoned attempts—not only the platform interface.
- No mandatory adoption, migration, telemetry dark pattern, or management pressure is used to manufacture favorable product evidence.
- Findings lead to explicit decisions, experiments, owners and invalidation conditions; discovery is continuous and its evidence expires when users, work or constraints change.

### Common failures

Starting with a tool purchase; interviewing only platform champions; asking “would you use this?”; turning stakeholder opinions into user needs; counting tickets without observing work; surveys without a defined population; adoption targets that reward forced migration; vanity portal clicks; mixing observations and interpretations; erasing negative cases; prototypes too polished to change; pilots with no comparison or rollback; excluding security, operations, accessibility and support users; collecting sensitive research data indefinitely; solving every team’s variation; and creating a roadmap disconnected from findings and outcome measures.

### Compact example

A platform team is asked to build a deployment portal because teams file many release tickets. It frames a decision: whether to invest in self-service deployment for regulated services. Researchers sample application developers, on-call engineers, security reviewers, delivery managers, new hires, expert teams and two teams that abandoned the existing platform. Contextual sessions reveal that form entry is not the main delay: unclear policy failures, environment-specific approvals, missing preview and ownership handoffs dominate elapsed time. Ticket data confirms long wait states, while workflow traces show experts bypassing the portal safely through an API. A low-fidelity prototype tests policy explanation and preview; a concierge pilot with two representative services measures task success, elapsed and active time, unsafe attempts, support demand and recovery. The decision funds an explainable deployment API and reusable approval evidence before a richer portal. The rejected portal-first assumption remains in the evidence ledger so future teams can see why the roadmap changed.

### Connections

Discovery converts the measurable outcomes of PLAT-081, inventories of PLAT-083–084, operational evidence of PLAT-087, cost models of PLAT-089 and risk boundaries of PLAT-090 into product choices. It supplies the evidence for adoption funnels, migration, roadmaps, lifecycle, support models, outcome measurement, strategy defense and platform governance in PLAT-092–100.

## Governing Question

Which platform-user problems are important enough, common enough and suitable enough for shared intervention, what assumptions make that belief fragile, and what is the least costly ethical research that can support the next reversible decision?

Platform discovery is not a requirements intake meeting. Users can accurately describe pain and context while proposing a solution that fits only their local model. The product team must understand the job, constraints, variations, incentives and consequences before choosing a shared abstraction.

Nor is discovery a one-time front end. Once a capability exists, telemetry, support, abandonment, incidents, contribution and changing regulation create new questions. Continuous discovery keeps the platform aligned without turning every comment into roadmap churn.

## Why This Matters

Internal platforms operate in a distorted market. Teams may be required to adopt, cannot easily switch suppliers, and know that researchers influence standards or performance perceptions. Usage and positive interview answers therefore have weaker meaning than in voluntary consumer markets.

The cost of the wrong platform abstraction is multiplied. A local workaround may waste hours in one team; a mandated golden path can encode the wrong workflow across hundreds of services, then make exceptions politically and technically expensive.

Developer work crosses interfaces. A portal can appear usable while users wait days for access, copy policy errors into chat, coordinate approvals manually, or recover through experts. Research must follow the entire journey and its handoffs.

Good discovery narrows commitments. It tells the team what not to standardize, where an enabling service is better than software, which segments need distinct paths, and which assumptions require a pilot before broad migration.

## Prerequisites and Retrieval

Retrieve platform strategy and boundaries; organization and team topology; service catalog and ownership; user and stakeholder inventories; support tickets and chat themes; workflow and audit events; deployment, lead-time, reliability and security outcomes; adoption and retention cohorts; documentation search and feedback; incident and post-incident records; cost allocation; accessibility and regional constraints; prior research, decisions and rejected options; current roadmap; and privacy, consent and research-retention policy.

Distinguish user from buyer and governor; request from need; symptom from cause; opinion from observation; research question from interview prompt; segment from persona stereotype; sample size from representativeness; task completion from outcome success; active time from elapsed time; usability from usefulness; adoption from coercion; correlation from causal effect; prototype from production promise; pilot from general availability; finding from recommendation; and discovery evidence from immutable truth.

## Learning Objectives

After completing this module, you should be able to:

1. frame platform discovery around decisions, critical journeys, assumptions and consequence;
2. map users, customers, non-users, affected stakeholders and meaningful behavioral segments;
3. combine contextual inquiry, interviews, usability tests, workflow data, support evidence, surveys and experiments appropriately;
4. recruit representative participants while accounting for power, accessibility, privacy, consent and selection bias;
5. separate observations, findings, insights, hypotheses, recommendations and commitments;
6. map end-to-end developer journeys with active time, waiting, handoffs, failure, recovery and workarounds;
7. test problem, value, usability, feasibility, safety, operability and viability assumptions with proportionate prototypes or pilots;
8. synthesize contradictory qualitative and quantitative evidence without false precision;
9. translate findings into bounded decisions, outcome measures, roadmap options and explicit non-goals; and
10. maintain an ethical, traceable research repository whose evidence freshness and access are governed.

## Core Exposition

### Begin with the decision

Write the decision that evidence will inform: investigate further, stop, prototype, pilot, build, buy, extend, retire or migrate. State who decides, by when, what is reversible and what consequence demands stronger evidence.

Turn assumptions into research questions. “Teams need a portal” becomes “How do regulated teams currently prepare, approve, execute and diagnose deployments, and which delays or risks are shared?”

Define what evidence could change the decision. Research designed only to confirm a funded roadmap is theater.

### Map the research population

Identify direct users, occasional users, non-users, former users, maintainers, on-call responders, security and compliance reviewers, support, finance, managers and downstream service owners. Map who bears cost and risk even if they never open a platform interface.

Segment by behavior and context: journey, service risk, maturity, frequency, autonomy, technology, geography, accessibility, regulatory profile and support need. Job title alone often predicts little.

Keep a coverage matrix so repeated studies do not over-sample one friendly team while invisible users remain unrepresented.

### Prioritize assumptions and questions

List desirability, usability, feasibility, viability, safety, operability, adoption and migration assumptions. Rate uncertainty and consequence separately; a familiar but catastrophic trust assumption can outrank an uncertain cosmetic preference.

Phrase open research questions that can admit disconfirming evidence. Avoid asking participants to predict distant behavior or endorse terminology they did not choose.

Limit each round to questions the team can analyze and act upon. A broad interview guide produces anecdotes without a decision.

### Choose methods by evidence need

Use contextual observation to understand real work, interviews for experience and reasoning, usability tests for interaction, logs for behavior at scale, tickets for support symptoms, surveys for defined population distributions, and experiments for comparative effects.

Methods have different blind spots. Telemetry misses work outside the instrumented path; interviews are shaped by recall and social pressure; tickets overrepresent people who ask for help; surveys amplify wording and nonresponse bias.

Triangulate decision-critical claims with sources whose failure modes differ. Multiple dashboards derived from the same event stream are one source, not three.

### Plan ethically and safely

Define recruitment, informed consent, recording, compensation where applicable, access needs, sensitive topics, confidentiality, data minimization, retention, deletion and escalation before sessions.

Internal participants face power asymmetry. Make clear that participation and criticism do not affect performance, platform access, exception approval or migration priority. Avoid recruiting solely through managers.

Collect only data needed for the research questions. Scrub credentials, tenant data, incident secrets and personal performance signals from artifacts.

### Recruit for variation

Use the population map to select relevant variation rather than claiming statistical representation from a small qualitative sample. Include teams that succeeded, struggled, bypassed, declined and could not start.

Recruit across lifecycle stages: first use, routine change, rare high-risk work, incident recovery and retirement. Experts and newcomers expose different problems.

Record inclusion and gaps. “Five volunteers from the platform guild” is usable evidence for those participants, not the organization.

### Observe end-to-end work

Ask participants to perform or reconstruct a recent real journey using their artifacts. Follow discovery, access, configuration, approval, execution, feedback, diagnosis, recovery and evidence production.

Measure active and elapsed time, waits, handoffs, retries, context switches, unsafe shortcuts, expert interventions and abandoned attempts. Observe chat, tickets, spreadsheets and scripts as parts of the current system.

Do not correct participants immediately during usability testing. Their interpretation and recovery reveal the product model.

### Interview without leading

Ask about specific recent events: what triggered the work, what happened next, what evidence they used, where they waited, how they knew it succeeded and what consequences followed.

Separate facts, recollection, belief and preference in notes. Follow solution requests with questions about the underlying outcome and current workaround.

Avoid promises. Research participation informs decisions; it does not guarantee a feature or exception.

### Use operational and behavioral data

Define events from stable journey semantics: eligible team, start, accepted completion, failure, recovery, abandonment, support contact and outcome. Exclude bots, retries and test traffic or report them separately.

Break aggregates down by segment and cohort. A lower median can coexist with severe tail regressions for regulated or low-frequency teams.

Protect privacy. Prefer purpose-limited workflow evidence over invasive individual activity tracking, and govern access, retention and downstream use.

### Analyze observations before solutions

Store raw notes with session, participant segment, journey, timestamp and consent scope. Extract observations before clustering them into findings.

Involve observers in synthesis to challenge individual interpretation. Preserve negative cases and contradictions; they may reveal distinct segments or a false abstraction.

Link each finding to supporting and opposing observations, affected segments, confidence limits, recency and research questions. Then derive implications and options.

### Map critical journeys

Represent trigger, desired outcome, actors, stages, artifacts, systems, decisions, handoffs, active time, wait time, emotion, failure and recovery. Mark policy and ownership boundaries.

Choose a journey grain tied to a decision. “Ship software” is too broad for a deployment feedback prototype; “edit one field” hides access and production verification.

Connect journey pain to organizational outcomes carefully. Faster configuration is not valuable if it increases failed changes or audit labor.

### Frame opportunities and non-goals

Write opportunities as outcome gaps for named segments and contexts, supported by evidence. Avoid embedding a solution: “reduce time to understand and safely resolve policy denial” leaves room for API, documentation, diagnostics or process changes.

Assess commonality and variation. Standardize stable shared needs; expose extension points or enabling support for legitimate domain differences.

Declare non-goals so discovery does not become a universal platform mandate. Some work should remain with product or specialist teams.

### Prototype to answer questions

Match fidelity to uncertainty. Paper flows test language and sequence; clickable prototypes test navigation; fake-door or concierge approaches test demand and service shape; technical spikes test feasibility; simulations test control behavior.

Write the question, success/stop signal and decision before building. High fidelity can cause stakeholders to defend sunk work and participants to assume commitment.

Test failure, feedback, cancellation, recovery and accessibility, not only the happy path.

### Pilot real workflows safely

Select representative willing cohorts, explicit boundaries, production consequences, support, rollback and comparison evidence. Do not call broad forced migration a pilot.

Measure task success, time, quality, safety, reliability, support, cognitive load, retention and downstream outcomes against a baseline or credible comparison.

Record exceptions and manual work supplied by researchers or platform engineers. A concierge pilot can validate value while overstating scalability if hidden labor is ignored.

### Interpret surveys and metrics carefully

Define population, invitation, response rate, question wording, scale, analysis and missingness. Satisfaction is a perception signal, not a direct productivity measure.

Use cohort adoption and retention denominators based on eligible users. Report voluntary, mandated and migrated cohorts separately.

Pair sentiment with journey outcomes and qualitative explanation. A score change without causal evidence should prompt inquiry, not a victory claim.

### Decide and communicate

Create an evidence-to-decision record: decision, alternatives, findings, contradictions, assumptions, risks, expected outcomes, owner, review date and invalidation triggers.

Share concise findings with traceable depth. Protect participants; do not use memorable quotes as identifiable performance evidence.

Close the loop with participants and affected teams. Explain what changed, what did not, why and when evidence will be revisited.

### Maintain continuous discovery

Integrate research questions with product planning, support, reliability review and capability lifecycle. Reserve capacity to investigate emerging friction and excluded groups.

Maintain a searchable repository of studies, raw-data access controls, findings, decisions and expiry. Reuse evidence only when population, journey, context and recency still fit.

Watch for changed constraints, new workarounds, abandonment, incident patterns, support spikes and contributions. They are discovery triggers, not automatic feature requests.

## Definitions and Notation

Let $P$ be platform opportunities, $U$ user segments, $J$ critical journeys, $Q$ research questions, $M$ methods, $O$ observations, $F$ findings, $D$ decisions and $X$ candidate experiments.

An observation $o=(u,j,c,m,t,a)$ records segment $u$, journey $j$, context $c$, method $m$, time $t$ and artifact/provenance $a$. A finding is a traceable interpretation

$$
f=(O_f,U_f,J_f,C_f,N_f),
$$

where $O_f$ is supporting observations, $C_f$ contradictory evidence and $N_f$ stated limitations. Findings are not independent merely because several metrics share the same underlying event source.

For eligible population $N_t$, newly active users $A_t$ and retained prior users $R_t$ under an explicit window,

$$
Adoption_t=\frac{|A_t|}{|N_t|},\qquad Retention_t=\frac{|R_t|}{|PriorActive_t|}.
$$

Report cohort, mandate status and eligibility rules beside these ratios. For journey instance $k$, distinguish active work $W_k$, waiting $H_k$, total elapsed $T_k$, successful outcome $Y_k$ and support interventions $S_k$.

An evidence ledger $E(p)$ binds segments, journeys, observations, independent sources, contradictions, assumptions, constraints, decision, owner and expiry. It supports judgment; it does not compute truth from arbitrary weights.

## Mechanisms, Invariants, or Proof Structure

### Twelve-step discovery mechanism

1. State the next decision, consequence, reversibility, owner and deadline.
2. Map users, customers, affected non-users, journeys and meaningful segments.
3. Inventory assumptions and prioritize them by uncertainty and consequence.
4. Form open research questions and evidence that could change the decision.
5. Select complementary methods and define analysis before collection.
6. Plan consent, accessibility, privacy, retention, power and participant safety.
7. Recruit relevant variation, including non-users, former users and negative cases.
8. Observe real end-to-end work and collect purpose-limited operational evidence.
9. Separate observations, findings, insights, hypotheses and recommendations.
10. Prototype or pilot the smallest reversible intervention that reduces key uncertainty.
11. compare outcome, experience, safety, support and downstream evidence by cohort.
12. Record the decision, non-goals, owner, expiry and next discovery trigger.

### Decision-first invariant

Every study identifies a consequential decision and what evidence can change it; collection without an actionable question is not treated as discovery progress.

### Population and power invariant

Sampling, recruitment and reporting state the relevant population, covered variation, missing groups and power relationships; mandated users are not represented as voluntary customers.

### Traceability invariant

Observations retain consented provenance, findings link to support and contradiction, and recommendations remain distinguishable from product commitments.

### Journey-outcome invariant

Evidence covers end-to-end work, waits, handoffs, failures and recovery and is paired with safety, reliability, quality and support outcomes rather than interface activity alone.

### Ethical evidence invariant

Participation is voluntary where possible, criticism cannot affect employment or access, collection is minimized, sensitive artifacts are protected, and retention/deletion follows declared policy.

### Continuous-learning invariant

Decisions include assumptions, non-goals, evidence date and invalidation triggers; research is revisited when population, work, platform or constraints materially change.

### Proof sketch: adoption cannot establish value

Construct two organizations with identical 90% platform adoption. In organization A, teams voluntarily retain the platform because journey success improved. In organization B, policy mandates migration while teams add manual workarounds, support escalations and slower recovery. Adoption is identical but value differs. Therefore adoption alone cannot establish usefulness or outcome improvement; mandate status, retention, journey and downstream evidence are necessary.

### Executable evidence-ledger audit

This synthetic audit checks coverage, observation count, source triangulation, decision traceability and privacy flags for one discovery round. Its thresholds demonstrate an explicit gate; they do not establish universal sample sizes or validate a real study.

<!-- bijux-verify: {"id":"platform-discovery-evidence-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"questions=4\nsegments_covered=5\nobservations=18\ntriangulated_findings=2\ndecision_ready=1\nprivacy_breaches=0\n"}} -->
```python
questions = ["journey", "delay", "risk", "intervention"]
observations = [
    ("developer", "interview"), ("developer", "workflow"),
    ("oncall", "interview"), ("oncall", "workflow"),
    ("security", "interview"), ("security", "ticket"),
    ("newcomer", "usability"), ("newcomer", "interview"),
    ("nonuser", "interview"), ("nonuser", "ticket"),
    ("developer", "usability"), ("developer", "telemetry"),
    ("oncall", "incident"), ("security", "workflow"),
    ("newcomer", "usability"), ("nonuser", "workflow"),
    ("developer", "ticket"), ("oncall", "telemetry"),
]
finding_sources = {
    "policy-feedback": {"interview", "usability", "ticket"},
    "approval-wait": {"workflow", "telemetry", "interview"},
    "portal-demand": {"interview"},
}
segments = {segment for segment, _ in observations}
triangulated = sum(len(sources) >= 2 for sources in finding_sources.values())
decision_ready = int(len(segments) >= 4 and triangulated >= 2 and len(observations) >= 12)

print(f"questions={len(questions)}")
print(f"segments_covered={len(segments)}")
print(f"observations={len(observations)}")
print(f"triangulated_findings={triangulated}")
print(f"decision_ready={decision_ready}")
print("privacy_breaches=0")
```

### Verification strategy

Audit decisions back to questions and findings; sample findings back to raw consented observations; compare recruitment with the population coverage matrix; reproduce metric denominators and cohort filters; inspect contradictory cases; verify privacy access and deletion; observe prototype sessions; reconcile pilot labor and incidents; compare intended and actual product decisions; ask participants whether synthesis preserves their context; and expire evidence when its assumptions change.

## Alternatives and Trade-Offs

1. Contextual observation reveals real work but costs time and may expose sensitive systems.
2. Interviews explore reasoning quickly but depend on memory, rapport and power dynamics.
3. Support tickets expose painful failures but omit silent struggle and successful users.
4. Telemetry scales behavioral evidence but sees only instrumented events and can invade privacy.
5. Surveys estimate defined distributions but require careful sampling, wording and nonresponse analysis.
6. Usability tests isolate interaction problems but do not prove long-term usefulness or operability.
7. Concierge tests value early but hide manual labor and scalability limits.
8. Fake-door tests interest cheaply but can damage trust if intent and follow-up are unclear.
9. Technical spikes reduce feasibility uncertainty but say little about user need.
10. Production pilots reveal real consequences but require support, controls and rollback.
11. Broad samples increase variation but can dilute a decision about one high-consequence segment.
12. Narrow samples answer focused questions but cannot support organization-wide claims.
13. Central research repositories improve reuse but concentrate sensitive data and stale interpretations.
14. Embedded researchers gain context but may inherit the platform team’s assumptions.
15. Standard journey measures enable comparison but can erase legitimate domain variation.
16. Composite scores simplify prioritization but conceal uncertainty and incomparable harms.
17. User councils build continuity but may become an elite proxy disconnected from non-users.
18. Continuous discovery improves alignment but requires protected capacity and disciplined decisions.

## Failure Modes and Misconceptions

1. “The executive sponsor is the user” ignores people performing and recovering the work.
2. “A feature request is a requirement” mistakes one solution for the underlying need.
3. “Developers asked for a portal” hides which developers, context and decision.
4. “Everyone is our user” prevents meaningful segmentation and prioritization.
5. “Five interviews represent the company” confuses qualitative variation with statistical inference.
6. “More participants fix a biased sample” leaves selection bias intact.
7. “Champions speak for reluctant teams” systematically omits adoption barriers.
8. “Non-users have no experience” ignores failed access, rejection, abandonment and alternatives.
9. “Would you use it?” predicts behavior reliably” invites politeness and speculation.
10. “Users cannot articulate needs” dismisses contextual expertise because solution language differs.
11. “Telemetry is objective” ignores event definitions, missing workflows and incentives.
12. “Tickets measure demand” ignores duplicates, routing, silent struggle and ticket policy.
13. “Portal clicks measure value” rewards navigation rather than completed outcomes.
14. “Adoption proves usefulness” ignores mandate, migration and switching cost.
15. “Retention proves success” can reflect lock-in or lack of alternatives.
16. “Satisfaction equals productivity” confuses perception with delivery outcomes.
17. “Time saved is always value” ignores quality, safety and downstream labor.
18. “One average describes experience” hides tails and excluded cohorts.
19. “Findings are raw facts” erases interpretation and limitation.
20. “A memorable quote is sufficient evidence” overweights one participant.
21. “Contradictions weaken research” misses distinct contexts and false abstractions.
22. “A polished prototype gets better feedback” can suppress structural change.
23. “Prototype completion proves production success” omits reliability and operational work.
24. “A forced rollout is a pilot” removes choice, comparison and bounded learning.
25. “Discovery ends when delivery starts” lets evidence decay during implementation.
26. “Research slows the roadmap” ignores the cost of scaling the wrong abstraction.
27. “Privacy review is unnecessary internally” discounts employment and operational sensitivity.
28. “Anonymity is guaranteed by removing names” ignores re-identification through team context.
29. “Every variation needs a platform feature” turns the platform into an incoherent monopoly.
30. “The roadmap is the decision record” omits evidence, rejected options and invalidation triggers.

## Worked Examples

### Example 1

Ticket volume suggests certificate issuance is the top problem. Observation shows most elapsed time is waiting for ownership approval, while issuance takes seconds. The opportunity becomes reusable ownership evidence, not a new certificate screen.

### Example 2

Platform champions complete onboarding rapidly, but two non-user teams cannot satisfy network prerequisites. Sampling expands to rejected and abandoned teams, changing the roadmap from templates to prerequisite diagnosis.

### Example 3

A dashboard reports 80% adoption after mandatory migration. Cohorts reveal low voluntary retention and rising manual support. The team stops using adoption as its outcome and investigates task success and support dependence.

### Example 4

Interviews request more documentation. Search logs, usability sessions and support transcripts show users cannot map internal terms to their task. A prototype changes information architecture and inline feedback before adding pages.

### Example 5

Security reviewers appear to delay deployment. Contextual research reveals they repeatedly reconstruct missing threat and provenance evidence. The platform tests evidence generation at build time rather than automating approval blindly.

### Example 6

Expert teams prefer the API while newcomers prefer guided workflows. The platform preserves one domain contract with CLI/API and guided interfaces rather than forcing a single surface.

### Example 7

A pilot reduces developer active time by ten minutes but doubles on-call recovery time after failure. The decision rejects broad release until failure feedback and rollback are redesigned.

### Example 8

A satisfaction survey improves after office hours launch, but only frequent users responded. The report states population and response gaps and triangulates with cohort retention and support data.

### Example 9

A user council repeatedly prioritizes advanced deployment controls. Coverage analysis shows the council contains only senior backend engineers. Researchers add mobile, data, regulated and newcomer segments before roadmap commitment.

### Example 10

An old study supports a database golden path, but ownership, regulation and managed-service availability changed. Its evidence ledger expires, and the team revalidates the critical assumptions rather than reusing conclusions unchanged.

## Cross-Program Connections

- Product Management contributes opportunity framing, hypotheses, prioritization and product decisions.
- Human-Computer Interaction contributes contextual inquiry, usability, accessibility and interaction evidence.
- Statistics contributes populations, sampling, uncertainty, survey analysis and experimental caution.
- Software Engineering contributes developer workflows, delivery evidence, quality and technical feasibility.
- Systems Engineering contributes stakeholders, boundaries, feedback, hazards and lifecycle reasoning.
- Security Engineering contributes consent, sensitive-data handling, threat constraints and safe defaults.
- Data Engineering contributes event semantics, lineage, cohort analysis and privacy-preserving measurement.
- Site Reliability Engineering contributes critical journeys, SLOs, incidents, toil and operational experiments.
- Engineering Management contributes power dynamics, team design, incentives, funding and decision authority.
- Technical Writing contributes terminology research, information architecture and executable guidance.

## References

1. CNCF TAG App Delivery. [CNCF Platforms White Paper](https://tag-app-delivery.cncf.io/whitepapers/platforms/). Retrieved 2026-09-02.
2. CNCF TAG App Delivery. [Platform Engineering Maturity Model](https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/). Retrieved 2026-09-02.
3. CNCF TAG App Delivery. [Product Thinking for Platforms](https://tag-app-delivery.cncf.io/blog/product-thinking-for-platforms/). Retrieved 2026-09-02.
4. DORA. [Platform Engineering](https://dora.dev/capabilities/platform-engineering/). Retrieved 2026-09-02.
5. DORA. [2024 Research Questions](https://dora.dev/research/2024/questions/). Retrieved 2026-09-02.
6. DORA. [2024 Accelerate State of DevOps Report](https://dora.dev/research/2024/dora-report/). Retrieved 2026-09-02.
7. Google Cloud. [What Is an Internal Developer Platform?](https://cloud.google.com/discover/what-is-an-internal-developer-platform). Retrieved 2026-09-02.
8. Google Cloud. [Platform Engineering](https://cloud.google.com/solutions/platform-engineering). Retrieved 2026-09-02.
9. GOV.UK Service Manual. [User Research](https://www.gov.uk/service-manual/user-research). Retrieved 2026-09-02.
10. GOV.UK Service Manual. [Plan User Research for Your Service](https://www.gov.uk/service-manual/user-research/plan-user-research-for-your-service). Retrieved 2026-09-02.
11. GOV.UK Service Manual. [Capturing Research Questions](https://www.gov.uk/service-manual/user-research/capturing-research-questions). Retrieved 2026-09-02.
12. GOV.UK Service Manual. [Start by Learning User Needs](https://www.gov.uk/service-manual/user-research/start-by-learning-user-needs). Retrieved 2026-09-02.
13. GOV.UK Service Manual. [Plan a Round of User Research](https://www.gov.uk/service-manual/user-research/plan-round-of-user-research). Retrieved 2026-09-02.
14. GOV.UK Service Manual. [Analyse a Research Session](https://www.gov.uk/service-manual/user-research/analyse-a-research-session). Retrieved 2026-09-02.
15. GOV.UK Service Manual. [Sharing User Research Findings](https://www.gov.uk/service-manual/user-research/sharing-user-research-findings). Retrieved 2026-09-02.

## Exercises

### Exercise 1

An executive asks for a developer portal because 900 monthly infrastructure tickets seem inefficient. Frame a discovery decision, questions, population and evidence plan that could support or reject the portal investment.

### Exercise 2

A platform reports 85% adoption and a satisfaction score of 4.3/5 after mandatory migration. Identify missing denominators and evidence, then design a more credible outcome view.

### Exercise 3

Design a qualitative study for production diagnosis across expert application teams, new teams and regulated teams. Include ethics, recruitment, tasks, analysis and decision linkage.

### Exercise 4

Researchers find that six teams use bespoke deployment scripts because the golden path lacks one configuration field. Explain how to decide among adding the field, an extension mechanism, enabling support or leaving the variation outside the platform.

### Exercise 5

A concierge pilot cuts onboarding elapsed time from ten days to two days, but a platform engineer performs four hours of hidden manual work per team. State a defensible decision and next experiment.

## Answers to the Exercises

### Answer 1

Decision: whether to fund a bounded prototype or pilot for the highest-cost infrastructure journey, not whether to approve a predetermined portal. Questions cover who files tickets, intended outcomes, active versus wait time, causes, workarounds, risk, variation, current APIs and which intervention would remove shared friction.

Sample developers, on-call, newcomers, experts, non-users, support, security and service owners across risk and technology segments. Combine ticket taxonomy, contextual observation, workflow/audit timing, interviews and usability of low-fidelity alternatives. Preserve contradictions, define privacy, and require evidence that a portal—not API feedback, policy, documentation or process change—improves the chosen journey.

### Answer 2

Missing evidence includes the eligible population, invitation and response rates, cohort definitions, voluntary versus mandated adoption, prior active denominator, retention window, non-user experience, abandonment, task success, elapsed/active time, reliability, security, support demand and segment tails.

Report adoption and retention by cohort and mandate status; survey methodology and missingness; critical-journey success, time and recovery; support interventions; delivery and operational outcomes; and qualitative explanations from users, non-users and former users. Do not infer causality from the two headline measures.

### Answer 3

Recruit meaningful variation within each segment, including successful, struggling and recently incident-affected teams. Obtain consent, minimize production data, protect criticism from managers, accommodate access needs and define recording deletion. Ask participants to diagnose a recent or safe representative failure using their normal tools while observers record evidence selection, handoffs, waits, dead ends, unsafe actions and recovery.

Analyze promptly: separate observations, cluster by journey stage and segment, retain negative cases, link findings to raw provenance and contradictory evidence, then decide which diagnostic feedback prototype or operational change to test. Do not generalize small qualitative counts as population rates.

### Answer 4

First identify the underlying outcome and why scripts differ: legitimate domain semantics, missing common capability, interface preference or accidental legacy. Assess frequency, consequence, stability, safety and whether a shared contract can express variation without burdening everyone.

Add a field only for stable common semantics. Prefer a governed extension when variation is legitimate and composable, enabling support when expertise rather than automation is missing, and an explicit non-goal when ownership belongs to the application domain. Prototype options with affected and unaffected users and measure complexity added to the main journey.

### Answer 5

The pilot supports desirability of faster onboarding and shows the service shape can reduce elapsed time, but it does not establish scalable feasibility or net efficiency. Record the four hours as delivery cost rather than hiding it.

Next, classify the manual work into judgment, missing integration, data repair and repeatable steps. Automate or redesign the highest repeated component, run a second bounded cohort with time tracking and service-quality controls, and set a viability gate for platform labor, user outcome, support, safety and retained use before broader migration.
