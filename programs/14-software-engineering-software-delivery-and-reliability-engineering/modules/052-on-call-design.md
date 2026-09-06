---
module_id: SDRE-052
program: Software Engineering: Software Delivery & Reliability Engineering
level: 2
module_number: 52
title: On-Call Design
status: complete
last_verified: 2026-09-06
---

# On-Call Design

## One-Page Review

### Governing question

How should an organization design continuous human response as a reliable, humane, and auditable system whose coverage, competence, authority, workload, and recovery remain adequate during ordinary pages and compound incidents?

### Essential definitions

- **on-call** is an assigned period during which a named responder must remain reachable and prepared to act with declared urgency;
- a **rotation** maps time intervals and roles to qualified responders;
- the **primary** is the first responder for a scope; the **secondary** supplies backup, consultation, or simultaneous-incident capacity under defined rules;
- an **escalation policy** maps failed acknowledgement, missing competence, authority needs, or incident severity to the next reachable role;
- **coverage** means every required interval and role has an eligible, reachable assignee with viable notification and access;
- **acknowledgement time** is the interval from notification delivery to an accountable responder accepting ownership;
- **response time** is the interval to a declared response action, which is not necessarily mitigation or resolution;
- **pager load** is the volume, timing, clustering, and cognitive demand of urgent notifications and resulting incidents;
- **operational load** includes pages, investigation, mitigation, handoff, follow-up, routine production work, and interruption recovery;
- **handoff** transfers current incidents, risks, silences, changes, and obligations between responders;
- **shadowing** pairs a learner with an accountable qualified responder without making the learner the sole safety boundary;
- **fatigue risk** is increased error and health exposure associated with sleep disruption, long hours, stress, or demanding work;
- **rotation debt** is unresolved reliability, staffing, documentation, access, or follow-up work that makes future shifts less safe.

### Central model, mechanism, or theorem

Treat on-call as a control loop:

$$
\text{user harm}\rightarrow\text{signal}\rightarrow\text{notification}\rightarrow
\text{acknowledgement}\rightarrow\text{decision}\rightarrow\text{mitigation}\rightarrow\text{verification}.
$$

Every edge needs an owner, time expectation, failure detector, and alternate path. For interval $T$, let required role-minutes be $D(T)$ and verified eligible scheduled minutes be $K(T)$. The necessary coverage condition $K(T)\ge D(T)$ is not sufficient: overlapping minutes, unqualified people, unreachable devices, missing access, simultaneous incidents, and fatigue can leave effective capacity below nominal schedule capacity.

### Critical invariants

- start from service consequence and response objectives, not a calendar template;
- maintain exactly one accountable assignee per role and time, with explicit backup;
- verify notification delivery, acknowledgement escalation, access, and emergency authority end to end;
- page only for urgent human action that automation cannot safely complete;
- keep scope within the responder's competence and ability to mitigate or escalate;
- protect rest, health, fairness, accessibility, leave, and local employment obligations by design;
- preserve follow-up capacity so recurring pages cause engineering change;
- treat swaps, travel, handoffs, and daylight-saving transitions as controlled state changes;
- plan for correlated pages, simultaneous incidents, and loss of the paging system;
- measure user outcomes and responder load without surveilling or blaming individuals.

### Common failures

Failures include equating a populated calendar with coverage, putting one expert on every escalation path, paging for nonurgent work, routing alerts to teams that cannot act, allowing silent schedule gaps, making the secondary permanently busy, treating acknowledgement as mitigation, omitting dependency contacts, expecting responders to improvise access, normalizing repeated night interruption, blaming individuals for system load, hiding swaps in chat, losing incident state at handoff, and relaxing thresholds instead of fixing noise or service defects.

### Compact example

A service has a primary scheduled every minute, but only one person can operate the database failover. That expert is also primary for two other services and is unavailable during leave. Nominal calendar coverage is 100%; effective mitigation coverage is not. The team cross-trains responders, creates a tested constrained failover procedure, assigns a secondary with independent notification, verifies emergency access, and defines escalation to the database-owning team. Coverage is a capability path, not a colored calendar cell.

### Connections

[SDRE-051](051-incident-severity-and-classification.md) defines which response package and urgency apply. [SDRE-053](../ROADMAP.md) next develops operational alert triage, while [SDRE-054](../ROADMAP.md) separates incident command from hands-on service response.

## Governing Question

Production systems automate routine control, yet rare, ambiguous, or high-consequence failures still need human judgment. Someone must receive a signal, understand the user risk, gain access, choose a mitigation, coordinate dependencies, and verify recovery. Assigning names to a weekly calendar is necessary but says little about whether that chain works at 03:00 during a network partition.

On-call is also a human system. Sleep disruption, unpredictable interruption, excessive scope, inequitable schedules, hostile escalation, and missing follow-up capacity impair judgment and health. A rotation that appears inexpensive by ignoring those costs accumulates turnover, alert neglect, unsafe hero dependence, and recurrent incidents.

The governing question is therefore how to engineer both service coverage and sustainable human capacity. The design must survive absence, simultaneous incidents, failed notification infrastructure, knowledge gaps, and organizational change while preserving an accountable route from user harm to verified mitigation.

## Why This Matters

Google's SRE Workbook defines being on-call as being available during an assigned period and ready to respond with appropriate urgency. It emphasizes support procedures, escalation paths, training, handoffs, pager-load analysis, flexible swaps, and psychological safety [1]. These practices are experience reports, not universal staffing thresholds.

Google's earlier SRE chapter frames sustainable on-call around both quantity of assigned time and quality or incident burden, and discusses primary and secondary rotations, compensation, and engineering time for permanent improvements [2]. Its numerical staffing examples describe Google's model under explicit assumptions; this chapter does not treat them as laws for every team or jurisdiction.

The SRE Workbook's alerting guidance connects paging to significant user-facing events and error-budget consumption [3]. Its incident-response chapter distinguishes coordinated incident management from technical resolution and recommends prepared roles and exercises [4]. Together they imply that an on-call system must connect symptom-based evidence to an executable response organization.

Current NIOSH guidance states that work-related fatigue can arise from nonstandard schedules, extended hours, stress, and demanding work, and can impair reaction, attention, memory, and judgment [5]. This supports treating fatigue as an operational and worker-safety risk rather than personal weakness. Employment, compensation, privacy, and working-time rules remain jurisdiction-specific and require qualified local review.

NIST SP 800-61 Revision 3 integrates cybersecurity incident response preparation and coordination into organizational cybersecurity risk management [6]. Security escalation, evidence access, and notification authority therefore need explicit integration with general on-call, while specialist definitions and obligations remain separately governed. All six canonical URLs and current claims were checked on 2026-09-06.

## Prerequisites and Retrieval

Retrieve service ownership, user journey, SLI, SLO, alert, incident, severity, escalation, acknowledgement, mitigation, recovery, failure domain, least privilege, emergency access, runbook, playbook, handoff, toil, fatigue, and psychological safety.

From SDRE-038 retrieve actionable paging. From SDRE-042 through SDRE-045 retrieve user-centered signals and budget policy. From SDRE-046 retrieve toil and automation discipline. From SDRE-050 retrieve production-readiness ownership and response evidence. From SDRE-051 retrieve incident categories, severity, urgency, priority, coordination mode, and provisional escalation. This chapter designs coverage; SDRE-053 through SDRE-060 develop triage, command, investigation, mitigation, communication, evidence, analysis, and verified improvement.

## Learning Objectives

After completing this module, you should be able to:

1. model on-call as an end-to-end response control loop;
2. derive coverage requirements from service consequence, response objectives, scope, and incident concurrency;
3. distinguish nominal schedule coverage from effective qualified response capacity;
4. design primary, secondary, specialist, management, security, and dependency escalation paths;
5. verify notification, acknowledgement, access, authority, mitigation, and recovery communication;
6. construct controlled handoff, swap, leave, and schedule-change mechanisms;
7. measure pager and operational load without gaming or individual blame;
8. protect sleep, fatigue recovery, accessibility, fairness, compensation, and psychological safety;
9. train and qualify responders through shadowing, exercises, and progressive authority;
10. test and evolve the rotation under absence, correlated pages, and compound incidents.

## Core Exposition

**Start with protected outcomes and coverage objectives.** List the services and user journeys that require urgent human response. For each, name consequence, operating hours, geography, severity classes, maximum acknowledgement target, first safe actions, recovery objectives, and communication obligations. A 24/7 consumer payment path differs from a weekday internal report with a one-day deadline.

Do not infer coverage from availability targets alone. A service can have a strict SLO while safe automation handles most failures; another with modest availability may need immediate human action to prevent corruption. Ask which failures cannot be safely detected, contained, or recovered without a person and how delay changes harm.

Define the supported boundary. Include application, infrastructure, data, identity, observability, deployment, and third-party dependencies. Record what the on-call owns, what it can mitigate, and where it must escalate. Ownership without control produces helpless pages; control without accountable ownership produces unsafe intervention.

Separate customer support intake, operational response, security response, incident command, and vendor escalation. They may share tools but have different evidence, confidentiality, and authority. A customer report must reach operational responders without making customers debug the service. A suspected breach needs a restricted security path without losing the common incident identity.

**Specify the response roles.** The primary acknowledges, establishes immediate context, performs safe first actions, and escalates when scope, severity, competence, or concurrency requires it. The primary is not expected to know every component or command. Its strongest skill is recognizing user harm, preserving options, and mobilizing the correct system.

The secondary must have a declared purpose. It may cover failed acknowledgement, provide a second operator for risky actions, take a second incident, or supply deep service knowledge. One person cannot simultaneously be meaningful secondary for many correlated services. Model which rotations share people and failure domains.

Specialist escalation supplies expertise such as database, network, security, or vendor knowledge. Management escalation supplies staffing, business, communication, or risk authority—not necessarily technical command. Incident command coordinates multi-party response. Each path needs acknowledgement timing, alternates, and authority boundaries.

Keep one accountable assignee per role and interval. Multiple unnamed people “watching” creates diffusion; zero creates a gap. A shared queue can be a delivery mechanism, but ownership transfers only when a named responder accepts it. Record the transfer and continue escalation until acceptance.

**Design the schedule as interval coverage.** Store schedules in a canonical time basis, render local time for humans, and explicitly test daylight-saving transitions, leap dates, travel, and region holidays. Define whether endpoints are half-open intervals so adjacent shifts neither overlap ambiguously nor leave a minute uncovered.

For each required role, compute the union of eligible scheduled intervals. Verify that it covers the service interval and that simultaneous assignments do not violate local policy or human capacity. A backup assigned as primary elsewhere may not provide independent incident capacity.

Follow-the-sun rotations place shifts largely in local waking hours and can reduce night burden. They introduce more handoffs, cross-region dependency, language and context transfer, inconsistent authority, and regional holidays. Single-site rotations reduce handoffs but impose night and weekend disruption. Choose with measured response quality and worker input, not geography alone.

Shift length trades handoff frequency against fatigue and context continuity. A long shift has fewer transfers but exposes one person longer and can combine a full workday with interrupted sleep. A short shift creates more transitions and schedule complexity. Measure actual page timing, active work, sleep interruption, recovery, and follow-up rather than declaring one duration universally safe.

The following executable model checks minute coverage for a fictional day. It demonstrates interval arithmetic only; it does not establish responder eligibility or humane staffing.

<!-- bijux-verify: {"id":"check-on-call-coverage","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"complete_gap_minutes=0\ncomplete_overlap_minutes=0\nflawed_gap_minutes=30\nflawed_overlap_minutes=0\n","stderr":""}} -->
```python
DAY_MINUTES = 24 * 60

def coverage(shifts):
    active = [0] * DAY_MINUTES
    for start, end in shifts:
        for minute in range(start, end):
            active[minute] += 1
    gaps = sum(value == 0 for value in active)
    overlaps = sum(value > 1 for value in active)
    return gaps, overlaps

complete = [(0, 480), (480, 960), (960, 1440)]
flawed = [(0, 480), (510, 960), (960, 1440)]

complete_gaps, complete_overlaps = coverage(complete)
flawed_gaps, flawed_overlaps = coverage(flawed)
print(f"complete_gap_minutes={complete_gaps}")
print(f"complete_overlap_minutes={complete_overlaps}")
print(f"flawed_gap_minutes={flawed_gaps}")
print(f"flawed_overlap_minutes={flawed_overlaps}")
```

Observed execution under CPython 3.14.4 proves only these arrays and rules. A production schedule checker must handle time zones, recurring rules, overrides, eligibility, notification destinations, overlapping roles, leave, and tool failure.

**Engineer notification and escalation.** Use at least one primary notification route and a meaningfully independent alternate for critical services. A mobile push and SMS delivered through the same vendor may share a failure domain. Test devices, networks, identity, and provider outages. Publish a human-callable emergency route when automation fails.

Define time from event observation to notification, notification to acknowledgement, and acknowledgement to first response separately. An acknowledgement says a human accepted ownership; it does not prove diagnosis, mitigation, or user recovery. Continue severity-appropriate escalation when acknowledgement or progress is absent.

Escalation policy must cover no acknowledgement, explicit decline, missing access, insufficient expertise, simultaneous incidents, suspected security event, unavailable incident commander, and third-party failure. Avoid long serial chains. Parallel escalation is justified when harm is severe or time-sensitive, but too broad a page can create coordination noise.

Test the actual roster and devices. A syntactically valid phone number is not evidence of reachability. Periodically inject a bounded test notification, measure each stage, and verify fallback without waking people unnecessarily. Protect test data and distinguish exercises clearly from live incidents.

**Provide authority and safe controls.** Responders need least-privilege routine access plus governed emergency paths for exceptional actions. Provision and test access before shifts. Do not ask a tired responder to request a new account, find an approver, or discover that a hardware token expired during an outage.

Define which actions a primary may take immediately: stop a rollout, reduce traffic, disable an optional feature, fail closed, rotate a credential, or declare an incident. High-risk actions may require a secondary operator or incident-command approval. Emergency access needs authentication, audit, scope, expiry, and retrospective review.

Runbooks should begin with purpose, user symptom, safety warnings, prerequisites, evidence to preserve, reversible mitigations, stop conditions, escalation, and recovery verification. Commands without context are dangerous. Keep them versioned with the service and exercise them against current interfaces.

Maintain a service overview, architecture and dependency map, current dashboards, change history, known risks, contact directory, and incident workspace instructions. The responder should not need institutional memory to find the first safe action. Documentation must still admit uncertainty and prompt escalation rather than encouraging blind command execution.

**Control pager and operational load.** Count distinct incidents, pages, repeated notifications, active response time, follow-up time, night interruptions, handoffs, and clustering. Median pages per shift can hide rare storms. Report distributions, maximums, time of day, service, cause, actionability, severity, and responder recovery burden.

Let incident count $N$ per shift be an illustrative Poisson variable with mean $\lambda$. Under that restrictive model,

$$
P(N\ge2)=1-e^{-\lambda}(1+\lambda).
$$

At $\lambda=0.8$, the modeled probability is about 19.12%. Production incidents are often correlated, seasonal, and changed by releases, so the Poisson result can seriously understate clusters. Use empirical concurrency and stress scenarios for staffing.

Let mean active handling time be $h$, follow-up time be $f$, and expected incidents be $\lambda$. Expected labor $\lambda(h+f)$ helps expose hidden load but does not capture night recovery, context switching, long tails, or simultaneous demand. Reserve engineering time to eliminate repeat pages; otherwise every shift consumes capacity needed to improve the next.

Page only when a human must act now and automation cannot safely complete the action. Route informational or nonurgent work to tickets or scheduled review. Deduplicate symptoms of one incident, inhibit downstream alerts when appropriate, and preserve signals needed to detect independent harm. Do not fix overload by hiding real user-impact pages or raising thresholds without SLO and consequence review.

Every page should produce structured disposition: incident identity, action taken, usefulness, false or redundant status, missing context, follow-up owner, and prevention opportunity. Aggregate system trends; do not rank individuals by pages or speed without context. Such metrics encourage unsafe acknowledgement, under-declaration, and avoidance of complex shifts.

**Protect health, rest, fairness, and inclusion.** On-call design is an employer-controlled exposure. Fatigue can impair attention and judgment [5]. Set limits on consecutive shifts, active incident duration, night interruptions, post-incident work, and return to normal duties. Provide immediate relief and safe transport or recovery support where applicable. Exact requirements require local occupational, employment, and legal expertise.

Do not treat individual resilience as the primary control. Scheduling, staffing, automation, service quality, alert design, escalation, and relief are system controls. Encourage responders to declare fatigue or inability without penalty and make backup activation routine. Psychological safety increases early escalation and reduces concealment.

Design for part-time work, caregiving, disability, religious observance, time zones, and varied home conditions. Invite private accommodation routes and worker participation without requiring disclosure to peers. Fairness is not simply equal shift count; consider night, weekend, holiday, page intensity, recovery time, and constraints.

Compensate and record on-call according to applicable agreements and law. Avoid incentive structures that reward excessive shifts or discourage escalation. Ensure contractors and vendors have explicit coverage, response, access, data handling, and handoff obligations without assuming outsourced responsibility removes internal accountability.

After a severe or long incident, rotate people before judgment degrades. A fresh responder needs a structured handoff and must confirm understanding. Preserve continuity through incident logs and roles rather than keeping one exhausted expert indefinitely.

**Train and qualify progressively.** Define competency by observable tasks: explain service boundaries and user SLIs, acknowledge and classify a page, locate changes, use emergency controls, preserve evidence, escalate, communicate, and verify recovery. Tenure is not a competency measure.

New responders study service material, observe shifts, practice in simulations, act as supervised primary, and then qualify for independent duty. The shadow remains accountable until the transfer criterion is met. Avoid using production incidents as unsupervised training.

Exercise rare failures, notification outages, missing primary, concurrent incidents, compromised credentials, dependency escalation, and handoff across regions. Include stop conditions and psychological debrief. Tests should find system defects, not grade an individual under artificial humiliation.

Cross-train critical expertise and rotate service ownership enough to prevent hero dependence. Preserve specialist escalation for genuinely deep mechanisms. If safe response requires one person's memory, treat that as an availability defect and reduce service scope or add controls until competence is distributed.

**Control handoffs, swaps, and change.** A handoff records active incidents, recent changes, current degradations, risky silences, expiring certificates or quotas, deferred work, upcoming launches, relevant communications, and who owns each item. The incoming responder reads and acknowledges it; ambiguous ownership escalates before the outgoing responder leaves.

Swaps are schedule mutations. Require explicit request, eligible replacement acceptance, collision and rest checks, schedule-system update, notification verification, and audit. Chat agreement without authoritative roster update leaves automation pointing at the wrong person. Define emergency replacement for illness or lost connectivity.

Review schedule-generation changes like production code. Test interval coverage, time zones, recurring rules, holidays, overrides, and API failures. A manager dashboard and the paging engine must derive from one authoritative state or detect divergence.

At organizational handoff, transfer access, service knowledge, open risks, incident history, escalation contacts, and responsibility progressively. Do not switch the pager first and promise training later. Keep the former team as bounded backup until evidence shows the new rotation can operate.

**Design for system failure and scale.** The paging service, identity provider, chat, documentation, VPN, and status tooling can fail during the same event. Maintain minimal offline contact and emergency procedures, independent access where justified, and periodically verified alternate communication. Protect those artifacts because they contain sensitive operational data.

Correlated incidents can exhaust every primary and secondary. Define disaster staffing, incident grouping, service prioritization, relief cadence, and executive resource authority. Preserve independent command and technical roles. Do not page every engineer without assignments; uncontrolled participation increases communication and change risk.

Shared-platform on-call must represent tenant impact and offer clear workload escalation. Application teams must retain enough operational exposure to understand how their changes behave. A central team cannot sustainably absorb unlimited components without authority to reject ownership, improve interfaces, or require readiness.

Audit the loop periodically. Verify coverage, contacts, devices, access, runbooks, escalation, response outcomes, fatigue indicators, equitable load, follow-up closure, service scope, and dependency contracts. Reopen the design after reorganizations, new regions, major service growth, repeated incidents, staffing loss, or tool changes.

## Definitions and Notation

For time interval $T$, let required roles be $R$. Required coverage demand is

$$
D(T)=\sum_{r\in R}d_r(T),
$$

where $d_r(T)$ is required minutes for role $r$. Let $k_{e,r}(T)$ be minutes engineer $e$ is eligible and assigned to $r$. Nominal supply is $K(T)=\sum_e\sum_r k_{e,r}(T)$. The inequality $K(T)\ge D(T)$ is necessary but not sufficient because one minute or person may be double-counted across incompatible roles.

Let response chain edges have delays $\delta_1,\ldots,\delta_m$. End-to-end time to an action is $L=\sum_i\delta_i$ only when the path is serial and succeeds. Retries, parallel escalation, and missing edges require a richer distribution and failure model.

For shift incident count $N$ under the illustrative assumption $N\sim\operatorname{Poisson}(\lambda)$,

$$
P(N\ge2)=1-P(N=0)-P(N=1)=1-e^{-\lambda}(1+\lambda).
$$

Let incident $j$ require active handling $h_j$, follow-up $f_j$, and recovery allowance $r_j$. Observed operational load over window $W$ includes $\sum_j(h_j+f_j+r_j)$ plus scheduled duties and interruption cost. Do not infer health from aggregate hours without timing and distribution.

Let schedule state be version $v$ and assignment be half-open interval $[t_s,t_e)$. A valid handoff changes accountable ownership at exactly $t_e$ after replacement acceptance and notification-system synchronization.

## Mechanisms, Invariants, or Proof Structure

**Coverage-union invariant.** For every required role and instant, exactly one primary assignment covers that instant and at least one valid escalation route exists. Total scheduled hours cannot prove this because overlapping intervals can coexist with gaps.

**Capability-path argument.** A notification reaches useful mitigation only if delivery, acknowledgement, competence, access, authority, action, and verification edges succeed. Adding another recipient does not repair a shared identity failure or missing safe control. Test the end-to-end path and each fallback.

**Acknowledgement limitation.** Acknowledgement observes accepted responsibility, not correct diagnosis or mitigation. Optimizing acknowledgement alone can reward instant clicks while user harm continues. Track downstream action and outcome separately.

**Concurrency argument.** Primary and secondary coverage tolerates two incidents only when assignees, tools, dependencies, and authority are independent enough and each incident fits their capacity. Shared experts or one paging provider create common modes. Empirical clusters and compound exercises bound the claim.

**Load-feedback invariant.** Every actionable page consumes response and follow-up capacity. If recurring pages consume all engineering capacity, their causes remain and future load persists or grows. Protecting prevention time is part of rotation stability, not optional improvement.

**Fatigue-safety argument.** Sleep disruption and extended demanding work can impair attention and judgment [5]. Therefore relief and recovery rules protect both responders and users; relying on continued individual effort makes the control loop weaker as an incident continues.

**Handoff atomicity.** If schedule routing changes before the incoming responder accepts context, incidents can route to an uninformed owner. If context transfers but routing does not, the outgoing owner still receives pages. Treat acceptance and authoritative routing update as one controlled transition with reconciliation.

## Alternatives and Trade-Offs

**Single-site versus follow-the-sun.** Single-site reduces handoffs and can deepen shared context, but imposes night work. Follow-the-sun reduces circadian disruption but increases transfers, cross-region coordination, and regional dependency. Measure both health and response outcomes.

**Primary-only versus primary-secondary.** One role is simple and cheaper. A secondary supplies acknowledgement fallback, second-operator safety, and concurrency, but is not real capacity when already assigned conflicting work. Define its purpose and activation.

**Service-owned versus centralized operations.** Service ownership aligns change authority and production consequence. Central teams offer consistency and scale. Centralization fails when scope exceeds competence or control; hybrid models pair platform-wide response with service escalation.

**Long versus short shifts.** Long shifts reduce handoffs but increase exposure and fatigue risk. Short shifts distribute load but add schedule and context transitions. Incident timing and worker feedback matter more than one standard duration.

**Broad rotation versus specialist rotation.** Broad membership distributes burden and knowledge. Specialists act faster on rare complex faults. Combine general first response with tested specialist escalation and cross-training rather than permanent hero dependence.

**Strict automation versus human scheduling control.** Automation prevents gaps and checks constraints. Humans need swaps and accommodations. Use governed self-service mutations with eligibility, acceptance, conflict checks, audit, and reconciliation.

**Aggressive paging versus ticketing.** Paging shortens response for urgent harm but interrupts sleep and focused work. Tickets preserve attention but delay action. Route by required human urgency and consequence, then verify classifications against outcomes.

**Individual metrics versus system metrics.** Individual rankings appear accountable but encourage unsafe behavior and ignore shift context. System-level distributions improve services and schedules; individual data should support private health and accommodation, not blame.

## Failure Modes and Misconceptions

1. **“A filled calendar proves coverage.”** Eligibility, reachability, access, competence, authority, concurrency, and tooling can still fail.
2. **“Primary and secondary always mean two-incident capacity.”** Shared people, dependencies, or specialist bottlenecks can collapse them into one path.
3. **“Acknowledged means handled.”** Ownership acceptance is only one edge before mitigation and recovery verification.
4. **“Every production signal should page.”** Page only for urgent human action; route observation and nonurgent work elsewhere.
5. **“More people on a page improves response.”** Unassigned participants increase coordination and change risk; roles and command matter.
6. **“The best engineer should always be primary.”** This creates a common dependency and prevents knowledge distribution and rest.
7. **“Runbooks replace training.”** Responders need concepts, practice, access, judgment, and safe escalation as well as instructions.
8. **“Night work is just calendar time.”** Sleep disruption and fatigue alter health and operational risk [5].
9. **“Equal shift count is automatically fair.”** Timing, intensity, holidays, recovery, constraints, and accommodations differ.
10. **“Silencing pages fixes overload.”** Time-bounded silencing may create space, but real user-impact signals and causes still require owned correction.
11. **“Chat swaps are sufficient.”** The authoritative paging schedule and handoff must change and be verified.
12. **“A vendor owns our incident once paged.”** Internal user, communication, risk, and verification accountability remains.
13. **“Follow-the-sun eliminates fatigue.”** Handoffs, local peaks, incidents crossing shifts, and regional constraints still create load.
14. **“Responder mistakes are personal failures.”** Alert, access, documentation, interface, fatigue, staffing, and authority design shape behavior.
15. **“One successful test proves the rotation.”** Coverage changes continuously with people, services, tools, schedules, and incident distributions.

## Worked Examples

### Example 1

**Situation.** Three eight-hour primary shifts cover UTC day: `[00:00,08:00)`, `[08:00,16:00)`, and `[16:00,24:00)`.

**Reasoning.** Under half-open interval semantics, each minute belongs to exactly one shift. The executable model reports zero gap and overlap minutes. Moving the second start to 08:30 creates 30 uncovered minutes even though total spreadsheet hours may still look near 24. Qualification and notification remain separate checks.

**Conclusion.** Validate the interval union and endpoint convention; summed hours do not prove continuous ownership.

### Example 2

**Situation.** A rotation averages $\lambda=0.8$ incidents per 12-hour shift, and management assumes multiple incidents are negligible.

**Reasoning.** Under a Poisson model, $P(N\ge2)=1-e^{-0.8}(1+0.8)\approx0.1912$, about 19.12%. Even this idealized model gives a material concurrency chance. Releases and shared failures cluster incidents, violating independence and potentially raising the tail. Secondary capacity and disaster escalation need empirical testing.

**Conclusion.** Average count alone hides concurrency; even simple probability challenges primary-only staffing.

### Example 3

**Situation.** Primary and secondary are different people, but both require the same identity provider to reach production.

**Reasoning.** The schedule has human redundancy but the capability path shares authentication. During identity failure, neither can mitigate. The team provisions a tightly scoped, audited emergency identity path with independent recovery, tests it, and requires two-person use for high-risk actions.

**Conclusion.** Responder count does not remove shared technical failure domains in access and authority.

### Example 4

**Situation.** A team receives eight pages nightly, seven of which require no action after inspection.

**Reasoning.** The system records actionability, common incident identity, user SLI, trigger, and disposition. Redundant symptoms are grouped; nonurgent capacity warnings become tickets; one genuine user-impact page retains urgent routing. Service defects and alert rules get owners and due dates. Thresholds are not relaxed merely to lower the count.

**Conclusion.** Reduce pager load by improving signals and systems while preserving detection of urgent harm.

### Example 5

**Situation.** A responder has handled a critical incident for 14 hours and is the only person who remembers a database procedure.

**Reasoning.** Continued hero dependence raises fatigue and correctness risk. Incident command assigns a fresh qualified operator, captures state and hypotheses in the incident log, conducts a verbal read-back, and keeps the original responder briefly as consultant before protected rest. The missing distributed knowledge becomes a blocking rotation defect for follow-up.

**Conclusion.** Continuity belongs in roles and evidence, not indefinite wakefulness by one expert.

### Example 6

**Situation.** A follow-the-sun handoff says only “database unstable; watch dashboards.”

**Reasoning.** The incoming team cannot infer affected users, current severity, changes, hypotheses, mitigations, dangerous actions, silences, owners, or next decision. A complete handoff records incident ID, timeline, user impact, evidence links, actions and outcomes, open risks, communication commitment, access state, and explicit ownership. The receiver reads back critical facts.

**Conclusion.** Geographic coverage without state transfer creates a response gap at every boundary.

### Example 7

**Situation.** A part-time engineer is repeatedly assigned overnight shifts outside agreed working days because the scheduler optimizes equal count.

**Reasoning.** Equal count ignores availability, employment agreement, recovery, caregiving, and health constraints. The scheduler must encode eligible windows and protected rest, offer private accommodation, require voluntary acceptance for exceptions, and audit burden by night, weekend, holiday, and page intensity. Local qualified review determines legal and compensation rules.

**Conclusion.** Fair scheduling is constraint-aware and participatory, not a naive round-robin.

### Example 8

**Situation.** The primary loses connectivity while a critical page is sent; the tool retries the same push channel for ten minutes.

**Reasoning.** Retries do not create channel independence. The policy sends a secondary route after the acknowledgement deadline, escalates in parallel for critical severity, and exposes notification-provider health. A human-callable emergency number and offline roster cover provider failure. Tests verify delivery and ownership transfer without waking all staff.

**Conclusion.** Escalation must change responder or failure domain, not repeat one broken mechanism indefinitely.

### Example 9

**Situation.** An outsourced database vendor promises a 15-minute response, so the application team removes database expertise from its rotation.

**Reasoning.** Vendor response is one dependency. The internal primary still must recognize user impact, contain writes, preserve evidence, invoke the contract, communicate, and verify recovery. The PRR tests vendor contact, entitlement, authentication, severity mapping, after-hours coverage, and fallback. Internal staff retain enough knowledge for safe containment.

**Conclusion.** Outsourcing expertise changes escalation; it does not outsource accountability for users or dependency integration.

### Example 10

**Situation.** Managers rank responders by median acknowledgement time and reward the fastest.

**Reasoning.** Engineers can game the metric by acknowledging before reading, avoid declaring linked incidents, or take easy shifts. Median hides missed and long-tail pages. The team instead examines end-to-end notification, acknowledgement, first safe action, mitigation, user recovery, escalation quality, load distribution, and follow-up at system level. Individual data supports coaching and accommodation with context and privacy.

**Conclusion.** Optimize the response loop and working conditions, not a decontextualized personal speed score.

## Cross-Program Connections

- [SEME-002](../../10-software-engineering-methods-and-evolution/modules/002-lifecycle-activities-and-feedback-loops.md) establishes lifecycle feedback loops; SDRE-052 applies that idea to reliability mechanics, capability paths, and response evidence.
- [SEC-086](../../25-security-engineering/ROADMAP.md) supplies specialist security triage and restricted escalation requirements.
- [SYSENG-033](../../26-systems-engineering/modules/033-data-control-mechanical-electrical-and-human-interfaces.md) frames human participation as an explicit system interface with failure modes.
- [API-097](../../28-api-and-service-engineering/modules/097-api-metrics-logs-and-traces.md) provides service-boundary evidence that makes API paging actionable.
- [PLAT-087](../../29-platform-engineering/modules/087-incident-response-for-shared-platforms.md) examines shared-platform response and tenant coordination at broader scope.

## References

1. Ollie Cook, Sara Smollett, Andrea Spadaccini, Cara Donnelly, Jian Ma, Garrett Plasky, Stephen Thorne, and Jessie Yang, “On-Call,” in *The Site Reliability Workbook*, O'Reilly Media, 2018. [Official online edition](https://sre.google/workbook/on-call/). Accessed 2026-09-06.
2. Rob Ewaschuk, “Being On-Call,” in *Site Reliability Engineering: How Google Runs Production Systems*, O'Reilly Media, 2016. [Official online edition](https://sre.google/sre-book/being-on-call/). Accessed 2026-09-06.
3. Steven Thurgood et al., “Alerting on SLOs,” in *The Site Reliability Workbook*, O'Reilly Media, 2018. [Official online edition](https://sre.google/workbook/alerting-on-slos/). Accessed 2026-09-06.
4. Jennifer Mace et al., “Incident Response,” in *The Site Reliability Workbook*, O'Reilly Media, 2018. [Official online edition](https://sre.google/workbook/incident-response/). Accessed 2026-09-06.
5. National Institute for Occupational Safety and Health, “Fatigue and Work,” Centers for Disease Control and Prevention, current online edition, updated July 14, 2026. [Official guidance](https://www.cdc.gov/niosh/fatigue/about/index.html). Accessed 2026-09-06.
6. Alexander Nelson, Sanjay Rekhi, Murugiah Souppaya, and Karen Scarfone, *Incident Response Recommendations and Considerations for Cybersecurity Risk Management: A CSF 2.0 Community Profile*, NIST SP 800-61 Revision 3, April 2025. [Official publication](https://csrc.nist.gov/pubs/sp/800/61/r3/final). Accessed 2026-09-06.

Current source-specific claims were checked on 2026-09-06. Staffing numbers, schedules, load assumptions, thresholds, response times, and role designs in this chapter are educational examples, not employment or legal advice, universal safety limits, or production guarantees.

## Exercises

### Exercise 1

Distinguish nominal schedule coverage, notification coverage, qualified response capacity, mitigation authority, incident concurrency capacity, and sustainable operational capacity for a 24/7 service.

### Exercise 2

For an illustrative Poisson incident count with $\lambda=0.5$ per shift, calculate $P(N\ge2)$. If mean active handling is 2 hours and follow-up is 3 hours, calculate expected incident labor per shift. State why neither result determines safe staffing.

### Exercise 3

Design a primary-secondary escalation policy for a critical data service covering missed acknowledgement, lost identity access, simultaneous incidents, suspected breach, unavailable incident commander, and paging-provider failure.

### Exercise 4

A six-person rotation has equal weekly shift counts, but two people carry most nights and all database escalations. Diagnose fairness, fatigue, competence, and common-mode risks; propose measurable redesign and validation.

### Exercise 5

Your organization acquires a service whose sole expert is nine time zones away, documentation is stale, and every page currently routes to that expert. Design a safe progressive ownership transfer without treating live incidents as unsupervised training.

## Answers to the Exercises

### Answer 1

Nominal schedule coverage means every required interval has an assignment. Notification coverage means a working route can reach and escalate from that assignment. Qualified response capacity means the responder can interpret the service and perform or select safe actions. Mitigation authority means credentials and policy permit those actions. Concurrency capacity asks whether independent responders and tools can handle overlapping incidents. Sustainable capacity includes pager frequency, clustering, active response, follow-up, sleep interruption, recovery, normal work, fairness, and health over time. Each is necessary for a dependable rotation; a green calendar establishes only the first and may not even do that unless interval boundaries and eligibility are validated.

### Answer 2

Under the stated Poisson model, $P(N\ge2)=1-e^{-0.5}(1+0.5)\approx1-0.60653066\times1.5\approx0.090204$, or about 9.02%. Expected incident labor is $0.5(2+3)=2.5$ hours per shift. These are means under independent stationary arrivals and average durations. Real incidents cluster around releases and shared failures, duration has a long tail, night interruption imposes recovery cost, one responder cannot parallelize overlapping work, and qualifications or shared tools constrain capacity. Use empirical distributions, worst credible scenarios, worker input, relief rules, and end-to-end exercises.

### Answer 3

Notify the primary through the main route and require acknowledgement within the critical objective. On timeout or explicit decline, notify secondary through an alternate route and activate incident command in parallel. If identity is unavailable, invoke a pretested, audited, time-bounded emergency identity path requiring a second operator for destructive actions. A simultaneous incident transfers one incident to secondary and pages a specialist or disaster roster based on consequence. Suspected breach adds restricted security on-call without losing common incident identity. Missing command escalates to the alternate commander. Paging-provider failure invokes the independently documented phone or offline contact tree and a known incident workspace. Every branch records ownership, tests reachability, preserves evidence, and continues until a named qualified responder accepts.

### Answer 4

Equal counts conceal unequal circadian and expertise burden. Measure nights, weekends, holidays, page intensity, active hours, sleep interruptions, follow-up, recovery, and specialist calls by distribution, using individual data privately and system data for improvement. Two people carry fatigue risk; database expertise is a common dependency. Rebalance eligible shifts with worker participation and accommodations, compensate under local rules, protect post-incident rest, cross-train through simulation and supervised practice, create a tested database runbook and specialist secondary, and remove conflicting assignments. Validate schedule intervals, notification, access, database scenarios, simultaneous incidents, handoffs, and load trends. Do not solve inequity by hiding pages or compelling disclosure of personal circumstances.

### Answer 5

Keep the expert as bounded accountable backup while mapping service boundaries, user SLIs, dependencies, safe controls, access, incidents, and known risks. Build current runbooks from paired walkthroughs and verify them in a safe environment. Select several learners, provide theory and service study, run simulations, let them shadow real shifts, then serve as supervised primary with explicit stop and escalation rules. Distribute database, deployment, and incident-command competence rather than cloning one generalist. Test notification, emergency access, common failures, recovery, and handoffs across time zones. Transfer primary intervals progressively after observed qualification; monitor outcomes and workload. Set an end date and staffing plan for the expert dependency, but reduce service scope or launch exposure if safe competence cannot be established.
