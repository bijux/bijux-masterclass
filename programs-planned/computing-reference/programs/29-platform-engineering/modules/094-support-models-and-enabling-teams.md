---
module_id: PLAT-094
program: Platform Engineering
level: 2
module_number: 94
title: Support Models and Enabling Teams
status: complete
last_verified: 2026-09-02
---

# Support Models and Enabling Teams

## One-Page Review

### Governing question

How should a platform provide discoverable, equitable, sustainable assistance—from self-service through incident escalation and time-bounded enabling—while preserving product-team ownership, converting repeated demand into platform improvement, and avoiding a permanent ticket dependency?

### Essential definitions

- A **support model** defines supported users and capabilities, channels, ownership, hours, urgency, service objectives, escalation, evidence, privacy, cost and exit behavior.
- **self-service support** gives users sufficient contracts, feedback, documentation, diagnostics and recovery controls to complete work without synchronous platform-team intervention.
- A **service desk** receives, classifies, routes and tracks requests under a published contract; it is not automatically the team that resolves every request.
- A **community of practice** is a voluntary learning network that shares experience and patterns; it cannot own production incidents or substitute for funded product work.
- An **enabling team** temporarily collaborates with another team to close a capability gap, transfer practice and remove systemic obstacles, with explicit disengagement criteria.
- **embedded support** assigns a specialist into a stream-aligned team for a bounded outcome; ownership and authority remain explicit.
- **operational support** responds to platform faults and service degradation; **product assistance** helps users understand or adopt supported capabilities.
- **toil** is manual, repetitive, automatable, tactical work with limited enduring value that tends to scale with service growth.
- An **escalation** transfers attention or decision authority because urgency, expertise, access or impact exceeds the current path’s contract.
- A **handback** deliberately returns operational responsibility when an engagement no longer meets entry conditions or sustainable load, with continuity and remediation evidence.

### Central model, mechanism, or theorem

For support demand class $i$ in window $T$, let arrival rate be $\lambda_i$, mean effort $s_i$, burst factor $b_i$, and reserved incident/recovery load $r_i$. Required capacity is bounded below by

$$
D_T=\sum_i \lambda_i s_i b_i + \sum_i r_i.
$$

Capacity arithmetic is necessary but insufficient: each route must have qualified coverage, access, hours, queue limits, escalation and health protections. Enabling work is successful when a partner team can achieve the agreed outcome independently and reusable platform capability improves; ticket closure alone is not the objective.

### Critical invariants

- Every supported capability identifies product owner, operating owner, user owner, channel, hours, response semantics, severity, escalation, evidence and exclusions.
- Safety-critical incidents never depend on an unstaffed community channel, one expert, undocumented access or a user’s ability to classify the failing layer perfectly.
- Stream-aligned teams retain service and business-domain ownership; platform support does not silently absorb application changes, risk or on-call responsibility.
- Enabling engagements have shared outcomes, bounded scope and duration, partner participation, reusable learning, feedback cadence and explicit disengagement or handback.
- Interrupt, queue, on-call and toil load remain within measured capacity with protected engineering time; overload triggers shedding, reprioritization or contract change.
- Support evidence is privacy-respecting and feeds product discovery, documentation, diagnostics, reliability, roadmaps and retirement rather than optimizing closure counts.

### Common failures

One chat channel for every request; undocumented best-effort promises; 24/7 expectations with business-hours staffing; severity chosen by requester influence; tickets bouncing between platform and application teams; self-service that fails opaquely; documentation used to deflect product defects; office hours as the only accessible route; enabling specialists doing the work indefinitely; embedded staff becoming permanent operators; hero experts and shadow escalation; support queues consuming roadmap capacity; automation that closes rather than resolves; repetitive access/configuration work accepted as normal; handback used as punishment; and measuring ticket volume or speed without user outcome, recurrence, toil or incident evidence.

### Compact example

A platform supports deployment through task-oriented documentation, preflight diagnostics, a searchable knowledge base, an asynchronous help queue, weekly office hours, a staffed incident route and six-week enabling engagements for high-consequence adoption gaps. The catalog states that product teams own application behavior while the platform team owns deployment-control availability and correctness. Intake asks for journey, service, correlation ID, impact and safe-to-share evidence, then routes without requiring users to diagnose the layer. Repeated policy-denial tickets trigger a product problem record; a new preview removes most interventions. A regulated team enters an enabling engagement with joint goals: independent deployments, incident diagnosis and evidence production. The specialist pairs on real changes, improves shared diagnostics, verifies two unassisted exercises and disengages. Capacity dashboards combine arrival, effort, burst, on-call and project-time data; when a migration wave would exceed support headroom, the wave moves rather than borrowing incident capacity.

### Connections

Support uses SLOs, fleet ownership, dependency maps, upgrade/restore/incident evidence, cost, blast radius, discovery, funnels and migration signals from PLAT-081–093. It supplies product-demand and capability-transfer evidence for roadmaps, build/buy, lifecycle, outcome measurement, strategy defense, autonomy and anti-monopoly review in PLAT-095–100.

## Governing Question

Which assistance path should handle each platform need, who retains ownership and authority, how much qualified capacity is required, and what evidence shows the intervention reduces future dependence while improving user and service outcomes?

Support is part of the platform product. Error feedback, recovery controls, examples and service status are support mechanisms even when no person is involved. Human channels reveal where the product contract is incomplete.

Not every request belongs in the platform. Application bugs, domain decisions and local customization remain with stream-aligned teams; platform defects, shared capability behavior and platform incidents remain with platform owners. The model must help users navigate ambiguity without rewarding ticket deflection.

## Why This Matters

Platforms multiply both leverage and confusion. A shared capability can remove work from hundreds of teams, but one opaque failure can generate hundreds of near-identical interrupts and simultaneous escalations.

Support demand is bursty and correlated with change and incidents. Staffing to average ticket volume leaves no capacity during releases, migrations or outages; staffing every channel for worst case is unaffordable.

Enabling capacity is scarce. If specialists execute tasks for teams, dependency grows linearly. If they pair, teach, improve common tooling and exit on demonstrated independence, the same capacity can unlock multiple teams over time.

Trust depends on ownership. Users need a reliable path during impact, platform engineers need protected time to remove causes, and product teams need autonomy rather than a platform organization that takes control without accountability.

## Prerequisites and Retrieval

Retrieve platform capability catalog and ownership; service SLOs and incident routes; user segments and critical journeys; support tickets, chats, office-hour notes and escalations; documentation/search feedback; product telemetry and adoption cohorts; platform and application on-call rosters; access and privacy policy; response/restore history; toil studies; interrupt and project-time data; migrations and roadmap; vendor contracts; team skills and time zones; accessibility needs; postmortems; and existing engagement agreements.

Distinguish support from ownership; product assistance from incident response; response from resolution; severity from requester seniority; service objective from guarantee; self-service from abandonment; documentation gap from product defect; community advice from accountable operation; consultation from embedded work; enabling from outsourcing; temporary assistance from hidden labor; handoff from handback; escalation from queue jumping; utilization from sustainable capacity; ticket closure from outcome; and lower demand from inaccessible support.

## Learning Objectives

After completing this module, you should be able to:

1. define a layered support contract for capabilities, users, channels, hours, severity and escalation;
2. allocate ownership across platform, stream-aligned, enabling, security, SRE, service-desk and vendor teams;
3. design self-service feedback, diagnostics, documentation and recovery as primary product features;
4. route ambiguous requests without forcing users to understand internal platform boundaries;
5. scope enabling and embedded engagements around transferable outcomes and exit evidence;
6. estimate support, on-call, interrupt and burst capacity while protecting engineering work;
7. control toil through demand analysis, automation, product fixes and contract changes;
8. design equitable, accessible and privacy-preserving channels across time zones and user segments;
9. measure resolution, recurrence, independence, reliability, sentiment and downstream outcomes; and
10. execute escalation, disengagement and handback without abandoning users or masking ownership failure.

## Core Exposition

### Define the support promise

For each capability, publish supported users, lifecycle stage, environments, interfaces, hours, channels, response targets, severity rules, maintenance, exclusions and escalation.

Use plain outcome language. Users should not need to decide whether a failure belongs to Kubernetes, networking, identity or the application before asking for help.

Separate experimental, preview, general-availability and retiring capability support. A preview cannot inherit a production promise accidentally.

### Map ownership and responsibility

Name platform product and operating owners, consuming service owner, incident commander, data/security authority, service desk and vendor. Describe decisions each may make.

Stream-aligned teams own application semantics and service outcomes. Platform teams own the shared contract and its operation. Cross-boundary incidents require collaboration, not responsibility ping-pong.

Use current catalog identity and on-call schedules. A static responsibility matrix without reachable people is not operational evidence.

### Design a layered path

Use status and diagnostics first, then task-oriented docs and examples, searchable history, community discussion, asynchronous case intake, synchronous office hours, enabling engagement and incident escalation.

Each layer has a purpose. Community channels support learning; queues support accountable tracking; incident routes support urgent impact; enabling engagements close systemic capability gaps.

Avoid one front door that serializes everything. A shared intake can route to multiple paths while preserving urgency and ownership.

### Make self-service genuinely usable

Expose system state, accepted inputs, policy decisions, correlation IDs, dependency health, retry safety, cancellation, rollback and next actions at the point of work.

Write documentation around journeys and failure recovery, with tested examples and versioned contracts. Search and navigation are part of support quality.

Self-service ends when risk or ambiguity requires accountable judgment. A security incident should not be reduced to a FAQ.

### Build diagnostic contracts

Standardize error taxonomy, stable codes, user-safe detail, operator detail, trace linkage and ownership hints. Preserve sensitive boundaries.

Provide preflight and explainability so failures are prevented before long workflows. Diagnostics should identify evidence and remedy, not merely say “contact support.”

Test degraded diagnostics. If status, logs and support all depend on the failed control plane, the support path disappears during need.

### Design intake and triage

Collect capability, journey, service identity, time, environment, correlation ID, observed/expected outcome, impact and consented attachments. Do not demand a root cause.

Deduplicate correlated reports while preserving affected-user evidence. Link incident broadcasts so users do not repeat information.

Triage by impact, urgency, safety and support contract. Seniority, persistence and channel choice must not silently override severity.

### Define severity and escalation

Severity binds user/service impact, data/security consequence, scope, duration and workaround. Publish examples and allow responders to correct classification.

Escalation identifies trigger, current owner, next owner, authority transferred, evidence, communication and return condition. Avoid blind reassignment.

Provide an independently reachable urgent route. Test paging, access, vendor escalation and cross-time-zone handoff.

### Operate incidents collaboratively

Platform incidents need command, operations, communication, liaison and subject expertise. Consuming teams provide outcome context and verify recovery.

Communicate affected capabilities, known impact, safe actions, workarounds, update time and recovery evidence. Silence drives duplicate support demand.

Afterward, connect cases to the incident and systemic actions; do not close them without confirming user outcomes and recurrence prevention.

### Govern community support

Communities enable peer examples, discovery and contribution. Give them moderation, conduct, searchable summaries and a clear boundary from authoritative support.

Do not rely on unpaid volunteers for incidents or mandatory onboarding. Recognize contribution and route product defects into accountable backlogs.

Protect privacy: scrub credentials, customer data and incident-sensitive artifacts from public or broad channels.

### Use office hours deliberately

Office hours fit exploratory questions, design consultation and live learning. Publish agenda, access, time-zone rotation and async alternative.

Capture reusable findings without recording sensitive conversation by default. Convert repeated questions into docs, diagnostics or capability changes.

Do not make attendance a hidden approval gate. Users unable to attend must retain an equivalent route.

### Define enabling entry criteria

Enter when a consequential capability gap blocks outcomes and joint work can create reusable learning. Confirm partner ownership, time and leadership support.

Avoid engagements that merely add hands to a deadline or transfer an unsupported application into platform ownership.

Prioritize by outcome, leverage, risk, strategic fit and readiness, with transparent decisions for declined requests.

### Contract the engagement

Write shared outcomes, scope, roles, cadence, artifacts, access, duration, feedback, success, stop, extension and disengagement.

Require partner participation in design, implementation and operations. Work done invisibly by the enabler cannot transfer capability.

Connect common improvements to the platform backlog while keeping application-specific change with its owner.

### Teach through real work

Pair on representative delivery, incidents, failure tests and reviews. Use explanation, guided practice, independent practice and feedback.

Teach decision models and recovery, not only commands. A copied runbook fails when context changes.

Create reusable examples, automation or contract improvements as a by-product, without leaking team-specific data.

### Embed without capturing ownership

Embedded specialists can build context and momentum, but retain their enabling mission and home-team support. Define authority explicitly.

Rotate responsibility toward the partner over time. Measure work completed independently, not specialist throughput.

End or redesign when the specialist becomes the permanent approver, operator or sole expert.

### Establish disengagement evidence

Exit when agreed journeys succeed independently, incidents can be diagnosed/escalated, ownership is current, and remaining risks have owners.

Use observed exercises, not training attendance alone. Include aftercare window and re-entry conditions.

Celebrate completion without implying no future support. The standard product contract remains available.

### Design handback safely

Handback may be needed when entry conditions fail, toil exceeds limits, ownership is absent, reliability obligations are broken or engagement value ends.

Give advance notice where possible, state evidence and remediation, transfer access and knowledge, and protect service continuity.

Handback is a governance mechanism, not retaliation. Leadership owns unresolved capacity or reliability trade-offs.

### Model demand and capacity

Measure arrivals, effort distributions, burst correlation, queue age, severity, channel, recurrence, after-hours work and enabling commitments.

Reserve on-call and recovery capacity; protect uninterrupted engineering time. High nominal utilization creates queues and removes ability to automate toil.

Model skills and coverage, not only hours. Ten available people do not replace one required credential or specialist.

### Control overload

Define queue limits, priority, admission, deferral, redirection and incident-mode shedding before overload. Pause low-value consultations during major incidents.

Reduce concurrent migrations or launches when support headroom fails. Do not silently consume personal overtime.

Escalate structural mismatch: narrow promise, staff responsibly, improve product, transfer ownership or stop unsupported work.

### Eliminate toil and recurring demand

Classify cases by cause and recurrence. Automate safe repeated work, improve error feedback, change defaults, remove policy ambiguity or retire broken capability.

Track cases prevented and independent outcomes, not only automation executions. Bad automation can scale defects.

Allocate explicit product capacity to support-derived problems. Otherwise the queue remains a permanent buffer for product debt.

### Work with vendors

Map internal severity to vendor contracts, entitlement, hours, evidence and escalation. Retain internal outcome ownership.

Test vendor access and escalation before incidents. Sanitize artifacts and govern data transfer across contractual boundaries.

Provide internal fallback and communication when vendor response misses user needs; a support contract is not a recovery mechanism.

### Measure outcomes

Report response and resolution distributions, reopen/recurrence, user outcome restored, support-assisted versus independent completion, queue age and accessibility.

For enabling, measure partner independence, operational competence, reusable improvements and sustained outcome after exit.

Pair with SLOs, adoption/retention, lead time, incident load, toil, project capacity, cost and user research. Lower ticket volume can mean either improvement or inaccessible support.

### Govern evidence and privacy

Set purpose, access, retention and redaction for tickets, chat, recordings and diagnostics. Avoid individual productivity scoring.

Separate customer-sensitive incident material from reusable knowledge. Review summaries for re-identification.

Let users correct ownership, classification and resolution evidence. Audit automated triage for segment and severity bias.

## Definitions and Notation

Let $I$ be support demand classes, $\lambda_i$ arrivals per window, $s_i$ mean qualified effort, $b_i\ge1$ burst/correlation factor, and $r_i$ reserved incident or recovery effort.

$$
D_T=\sum_{i\in I}\lambda_i s_i b_i+\sum_{i\in I}r_i.
$$

Let $C_{q,t}$ be available capacity for skill/coverage dimension $q$ at time $t$. A plan is feasible only when demand in every required dimension stays within $C_{q,t}$ with declared headroom; total person-hours cannot compensate for missing authority or skill.

For case $x$, record arrival $a_x$, first qualified response $p_x$, restoration $r_x$, durable resolution $d_x$ and recurrence indicator $z_x$. These produce distinct response, restore and resolution distributions.

For enabling engagement $e$, define shared outcome set $O_e$, partner-performed evidence $P_e$, reusable change $R_e$, residual risks $K_e$ and exit gate $X_e$. Completion requires agreed $O_e$ and $P_e$, not a count of specialist-delivered tasks.

## Mechanisms, Invariants, or Proof Structure

### Twelve-step support mechanism

1. Define supported capabilities, users, lifecycle, hours, exclusions and ownership.
2. Map needs to self-service, community, queue, consultation, enabling and incident paths.
3. Publish severity, response semantics, escalation, communication and vendor boundaries.
4. Build diagnostic, documentation, status, correlation and recovery contracts into the product.
5. Collect minimal intake evidence and route by outcome/impact without demanding root cause.
6. Measure arrival, effort, bursts, skill, queue, on-call, toil and protected project capacity.
7. Operate overload controls and adjust launches or promises before headroom is exhausted.
8. Aggregate recurring demand into owned product, reliability and documentation problems.
9. Contract enabling engagements with shared work, reusable learning and exit evidence.
10. Verify independent practice, operational competence, aftercare and safe disengagement.
11. Measure restored outcomes, recurrence, independence, accessibility and transferred cost.
12. Review the support portfolio and change staffing, channels, product or ownership.

### Contract invariant

Each capability has current owners, routes, hours, severity, objectives, escalation, evidence and exclusions; users need not infer internal architecture to reach help.

### Ownership invariant

Platform, application, enabling, security, SRE, service-desk and vendor responsibilities remain explicit through normal work, incidents and handback.

### Sustainability invariant

Qualified demand, burst, on-call, toil and enabling commitments fit capacity with protected engineering time; overload changes work or contract rather than relying on hidden overtime.

### Enabling invariant

Engagements are bounded, jointly owned and oriented to independent partner outcomes plus reusable improvement, with explicit stop and exit conditions.

### Safety and equity invariant

Urgent paths are staffed and independently reachable; severity is impact-based; channels provide accessible, time-zone-aware alternatives; evidence use is non-punitive.

### Learning invariant

Cases and engagements feed owned product/reliability decisions, recurrence prevention and retirement; closure speed cannot substitute for restored durable outcomes.

### Proof sketch: lower ticket volume cannot prove better support

Construct two platforms with equal observed ticket reduction. Platform A improved diagnostics and prevented recurring defects. Platform B removed the accessible channel and required manager approval, so users abandoned attempts or used private workarounds. Ticket volume is identical while outcomes and access differ. Therefore lower demand alone cannot prove support improvement; journey success, accessibility, recurrence, shadow-channel and user evidence are necessary.

### Executable support-capacity audit

The synthetic audit routes twelve requests, weights their qualified effort, and checks one service window against capacity. It demonstrates arithmetic and routing categories, not universal staffing ratios.

<!-- bijux-verify: {"id":"support-capacity-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"requests=12\nself_service=4\ncommunity=2\nservice_desk=3\nenabling=2\nincident=1\nweighted_demand=23\ncapacity=24\nheadroom=1\ngate=pass\n"}} -->
```python
routes = {
    "self_service": [1, 1, 1, 1],
    "community": [1, 1],
    "service_desk": [2, 2, 2],
    "enabling": [3, 3],
    "incident": [5],
}
capacity = 24
demand = sum(sum(effort) for effort in routes.values())

print(f"requests={sum(len(items) for items in routes.values())}")
for route, items in routes.items():
    print(f"{route}={len(items)}")
print(f"weighted_demand={demand}")
print(f"capacity={capacity}")
print(f"headroom={capacity - demand}")
print(f"gate={'pass' if demand <= capacity else 'fail'}")
```

### Verification strategy

Test channels and paging from user contexts; reconcile catalog owners with schedules and permissions; sample cases from intake through durable outcome; recompute response/restore/resolution and capacity; inspect queue bursts and after-hours work; trace recurring cases to product decisions; observe enabling partner practice; verify exit/handback artifacts; survey excluded and silent users; audit privacy/access; and inject status, vendor and control-plane failures into the support path.

## Alternatives and Trade-Offs

1. Rich self-service scales well but requires continuing product investment and accessible design.
2. Central service desks simplify intake but can add routing delay and information loss.
3. Direct team channels build rapport but fragment evidence and favor insiders.
4. Communities spread peer knowledge but lack accountable incident ownership.
5. Office hours enable dialogue but exclude some time zones and create synchronous dependence.
6. Ticket queues preserve audit but can turn collaboration into transactional handoffs.
7. Embedded specialists gain context but risk becoming permanent local operators.
8. Short enabling engagements spread capacity but may end before durable practice forms.
9. Long engagements build depth but reduce portfolio reach and increase capture.
10. Follow-the-sun coverage reduces overnight load but complicates context handoff.
11. Local on-call preserves context but can be unsustainable for small teams.
12. Shared on-call pools improve coverage but may weaken product familiarity.
13. Strict support boundaries protect capacity but can produce user-facing gaps.
14. Broad ownership improves experience but can make the platform a monopoly.
15. Automation reduces repetition but may close cases or execute unsafe changes opaquely.
16. High headroom costs more but preserves incident and engineering capacity.
17. Vendor support supplies expertise but adds entitlement, privacy and response dependencies.
18. Handback restores incentives but can threaten continuity if executed abruptly.

## Failure Modes and Misconceptions

1. “One channel is simple” conflates learning, cases and incidents.
2. “Best effort needs no contract” creates invisible expectations and inequity.
3. “24/7 product means 24/7 support exists” ignores staffing and escalation.
4. “Users must route correctly” demands knowledge they seek from support.
5. “The loudest requester has highest severity” substitutes influence for impact.
6. “Fast response means fast restoration” confuses acknowledgement with outcome.
7. “Closed means resolved” ignores recurrence and user verification.
8. “Documentation replaces support” can deflect product defects.
9. “More documentation fixes opaque errors” ignores missing runtime evidence.
10. “Self-service means no humans” ignores accountable exceptions and incidents.
11. “Community volunteers own availability” assigns unfunded critical work.
12. “Office hours are accessible to everyone” ignores time, language and format.
13. “Enabling teams deliver projects” turns capability transfer into outsourcing.
14. “Embedding transfers ownership” confuses temporary location with accountability.
15. “Training attendance proves competence” omits independent practice.
16. “A copied runbook transfers judgment” fails outside rehearsed context.
17. “Long engagements create more value” can create permanent dependence.
18. “Disengagement means abandonment” ignores continuing product support.
19. “Handback is punishment” undermines a necessary sustainability control.
20. “Everyone can be on call” ignores health, training, compensation and coverage.
21. “Average arrivals determine staffing” misses correlated bursts and incidents.
22. “All engineer-hours are fungible” ignores skills, access and time zones.
23. “Full utilization is efficient” removes queue and recovery headroom.
24. “Overtime closes a capacity gap” hides structural overload.
25. “Automation eliminates toil” may simply automate a harmful process.
26. “Repeated requests are user error” overlooks product and contract defects.
27. “Lower ticket counts prove improvement” may signal inaccessible support.
28. “Vendor escalation transfers ownership” leaves internal outcomes unmanaged.
29. “Support data is harmless internally” ignores performance surveillance and secrets.
30. “Support is separate from roadmap” preserves recurring product debt.

## Worked Examples

### Example 1

Deployment errors provide a stable policy code, evidence link and correlation ID. Most users recover independently; unresolved cases arrive with actionable context rather than screenshots.

### Example 2

A shared chat channel is unavailable during control-plane failure. The team adds an independently hosted status page, paging route and incident bridge.

### Example 3

VIP requests repeatedly bypass the queue. Impact-based severity and visible escalation audit restore equitable prioritization.

### Example 4

Office-hour attendance grows while the same certificate question repeats. A preflight check and tested example remove the underlying need.

### Example 5

An enabling specialist performs every migration. The engagement resets around pairing, two independent cutovers and a reusable readiness check before exit.

### Example 6

A product team stops attending incidents after platform onboarding. The ownership contract restores application participation so domain failures remain visible.

### Example 7

Average queue load fits staffing, but launch-day requests are correlated. Burst modeling moves one launch and preserves incident headroom.

### Example 8

Ticket automation closes cases after sending a document link. Reopen and restored-outcome evidence shows no improvement, so automation changes to guided diagnosis.

### Example 9

A vendor meets its response target but the platform remains down. Internal incident command uses fallback and communicates outcomes while vendor escalation continues.

### Example 10

Ticket volume falls after a form adds manager approval. Research finds private messages and abandoned work; the gate is removed and privacy-safe intake restored.

## Cross-Program Connections

- Organizational Design contributes team boundaries, interaction modes and cognitive-load management.
- Site Reliability Engineering contributes engagement models, on-call, toil, incidents and handback.
- Product Management contributes service promises, discovery, segmentation and roadmap feedback.
- Human-Computer Interaction contributes help-seeking, accessible support and diagnostic usability.
- Operations Research contributes arrival, service, burst, queue and capacity models.
- Security Engineering contributes escalation authority, evidence handling and least privilege.
- Software Engineering contributes diagnostic contracts, automation, examples and ownership.
- Knowledge Management contributes searchable learning, provenance, currency and retirement.
- Engineering Management contributes staffing, health, compensation, expectations and conflict resolution.
- Vendor Management contributes entitlements, escalation, data sharing and contractual boundaries.

## References

1. CNCF TAG App Delivery. [CNCF Platforms White Paper](https://tag-app-delivery.cncf.io/whitepapers/platforms/). Retrieved 2026-09-02.
2. CNCF TAG App Delivery. [Platform Engineering Maturity Model](https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/). Retrieved 2026-09-02.
3. DORA. [Platform Engineering](https://dora.dev/capabilities/platform-engineering/). Retrieved 2026-09-02.
4. Team Topologies. [Team Interaction Modeling](https://teamtopologies.com/key-concepts-content/team-interaction-modeling-with-team-topologies). Retrieved 2026-09-02.
5. Google SRE. [SRE Engagement Model](https://sre.google/workbook/engagement-model/). Retrieved 2026-09-02.
6. Google SRE. [Evolving the SRE Engagement Model](https://sre.google/sre-book/evolving-sre-engagement-model/). Retrieved 2026-09-02.
7. Google SRE. [SRE Team Lifecycles](https://sre.google/workbook/team-lifecycles/). Retrieved 2026-09-02.
8. Google SRE. [On-Call](https://sre.google/workbook/on-call/). Retrieved 2026-09-02.
9. Google SRE. [Handling Operational Overload](https://sre.google/workbook/overload/). Retrieved 2026-09-02.
10. Google SRE. [Eliminating Toil](https://sre.google/workbook/eliminating-toil/). Retrieved 2026-09-02.
11. Google SRE. [Incident Response](https://sre.google/workbook/incident-response/). Retrieved 2026-09-02.
12. Google SRE. [Postmortem Culture](https://sre.google/workbook/postmortem-culture/). Retrieved 2026-09-02.
13. Google SRE. [Training Site Reliability Engineers](https://sre.google/resources/practices-and-processes/training-site-reliability-engineers/). Retrieved 2026-09-02.
14. Google SRE. [Service Best Practices](https://sre.google/sre-book/service-best-practices/). Retrieved 2026-09-02.
15. GOV.UK Service Manual. [Assisted Digital Support](https://www.gov.uk/service-manual/helping-people-to-use-your-service/assisted-digital-support-introduction). Retrieved 2026-09-02.

## Exercises

### Exercise 1

Design a support contract for a production deployment capability used across three time zones. Include self-service, cases, incidents, ownership, hours and escalation.

### Exercise 2

A team receives 40 weekly requests averaging 30 minutes, with burst factor 1.4, plus 8 reserved incident hours. Compute modeled demand and discuss missing capacity dimensions.

### Exercise 3

An enabling team has embedded with one application team for nine months and now performs all deployments. Design a recovery and disengagement plan.

### Exercise 4

Ticket volume falls 50% after a documentation redesign. Define evidence needed before claiming support improvement.

### Exercise 5

During overload, a platform team supports two migrations, a launch, a major incident and its normal queue. Design an ethical prioritization and shedding response.

## Answers to the Exercises

### Answer 1

Publish capability scope, supported lifecycle and owner. Provide versioned task/error documentation, preflight, status and correlation IDs; an asynchronous accountable case queue with impact-based triage; rotating office hours with async alternative; and an independently reachable 24/7 incident route only for production platform impact.

The product team owns application semantics and participates in incidents; platform on-call owns shared deployment-control health; security owns exceptional authorization; vendors are internal escalations. Define response/restoration semantics, severity examples, cross-time-zone handoff, user communications, privacy, exclusions and handback.

### Answer 2

Base effort is $40\times0.5=20$ hours. Applying the burst factor gives 28 hours; adding 8 reserved incident hours yields 36 qualified hours per week.

The scalar omits arrival timing, effort distribution/tails, simultaneous incidents, skill and access, time-zone coverage, handoff, leave, meetings, after-hours health, queue service objectives and protected engineering time. Capacity must pass each required dimension with headroom rather than dividing 36 by nominal engineer-hours.

### Answer 3

Reaffirm that the application team owns deployments. Inventory knowledge, access, automation and failure paths currently held by the enabler. Stop adding new specialist-only work, then pair on representative changes, incident diagnosis, rollback and evidence production.

Move execution progressively to application engineers; improve common platform diagnostics; require two unassisted deployments and one failure exercise; update ownership/on-call/runbooks; time-box aftercare; revoke unnecessary embedded authority; and set re-entry criteria. Escalate staffing or reliability gaps rather than abandoning service continuity.

### Answer 4

Verify channel accessibility and form/search changes so demand was not suppressed. Compare eligible journey volume, independent task success, time-to-resolution, restored outcomes, reopen and recurrence, shadow chats, abandonment, escalations, incidents, satisfaction and segment/accessibility outcomes.

Trace removed tickets to improved comprehension or prevention and inspect whether work shifted to product teams or private channels. Preserve cohort and seasonal context. Only claim improvement when outcomes and access improve without transferred toil or risk.

### Answer 5

Enter incident mode: reserve command/on-call capacity, pause office hours and noncritical consultations, communicate known impact and route duplicates to status. Reassess the launch and migration gates; delay work whose outcome does not justify consuming recovery headroom, with leaders owning the schedule trade-off.

Protect engineer health and shifts, request qualified surge help with explicit roles, retain urgent security paths, and keep the normal queue visible with revised expectations. After stabilization, measure hidden overtime and recurrence, reduce concurrent commitments, remove incident-generated toil and change capacity or support promises before resuming all work.
