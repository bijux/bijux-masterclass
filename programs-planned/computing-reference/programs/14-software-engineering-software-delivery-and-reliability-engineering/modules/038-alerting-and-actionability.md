---
module_id: SDRE-038
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 38
title: Alerting and Actionability
status: complete
last_verified: 2026-09-06
---

# Alerting and Actionability

## One-Page Review

### Governing question

How can a team turn uncertain telemetry into timely, low-noise notifications that reach the right owner and request a safe, specific action without confusing symptoms, causes, incidents, and evidence gaps?

### Essential definitions

- an **alert condition** is a predicate evaluated over explicitly scoped evidence;
- an **alert instance** is one condition and identifying label set in a lifecycle state;
- **pending** means the condition is active but has not satisfied its persistence policy;
- **firing** means the rule has satisfied its activation policy;
- **resolved** means a previously firing instance has satisfied its recovery policy;
- **unknown** means the evaluator lacks evidence sufficient to decide true or false;
- a **page** interrupts a responder because timely human action is required;
- a **ticket** requests action that can wait for normal work scheduling;
- an **informational event** records evidence without demanding human action;
- **actionability** means a recipient can identify why the notification matters, what bounded first action to take, and what authority and evidence support it;
- **grouping** combines related instances into one notification; **deduplication** suppresses repeated delivery of the same identity;
- **inhibition** suppresses a dependent notification while a higher-level condition is active;
- a **silence** is an explicit, scoped, expiring suppression policy;
- **hysteresis** uses different activation and recovery conditions to resist flapping;
- **precision** and **recall** compare alert decisions with an independently adjudicated set of significant events.

### Central model, mechanism, or theorem

Let $x_t$ be evidence at evaluation time $t$, $B(x_t)\in\{0,1,\bot\}$ a condition, and $\bot$ unknown. A rule moves from inactive to pending when $B=1$, then to firing only after its persistence policy is met. A recovery policy moves firing to resolved; missing evidence follows an explicit unknown policy rather than silently becoming healthy.

If the first satisfying evaluation occurs at $t_e$, pending time is $p$, grouping delay $g$, and delivery delay $d$, the earliest notification under that model is

$$
t_n=t_e+p+g+d.
$$

Every delay trades transient-noise rejection against response time. It must fit the harm being detected.

### Critical invariants

- a page corresponds to credible or imminent user harm and a time-sensitive human action;
- every notification has an owner, urgency, scope, evidence timestamp, and runbook entry;
- the rule's population, units, window, threshold, and missing-data policy are reviewable;
- symptom alerts initiate response; cause signals support diagnosis unless independently actionable;
- zero, absence, stale telemetry, query failure, and healthy evidence remain distinct;
- grouping preserves the dimensions needed to route and act;
- inhibition and silences suppress notifications, not evidence or lifecycle state;
- acknowledgment proves receipt, not mitigation or resolution;
- automation is bounded by authority, preconditions, postconditions, rollback, and audit evidence;
- alert quality is measured against outcomes and reviewed after incidents and false pages.

### Common failures

Common failures are paging on every component anomaly, using one threshold for all traffic levels, treating missing data as recovery, requiring the responder to invent the first action, routing to a stale team alias, creating one page per replica, grouping unrelated failures, silencing too broadly or indefinitely, inhibiting the only user-impact alert, repeating notifications faster than anyone can act, coupling alerts to dashboard colors, marking acknowledged alerts resolved, embedding dangerous remediation in a runbook, and retaining alerts whose owners or systems no longer exist.

### Compact example

A checkout alert evaluates the unsuccessful eligible-request ratio for one production service and region. It fires only when user-impact evidence persists long enough to reject a one-sample transient and traffic is sufficient to interpret the ratio. Missing telemetry produces a separate evidence-health state. The page names the affected population, value, threshold, start time, owner, and safe first diagnostic action. Related replica alerts are grouped; a region-outage notification inhibits redundant instance notifications but not the checkout symptom. The silence used for maintenance has a narrow matcher, owner, reason, and expiry.

### Connections

[SDRE-031](031-observability-versus-monitoring.md) supplies question-first evidence, [SDRE-033](033-metrics-and-dimensionality.md) supplies measurement semantics, and [SDRE-037](037-dashboards-for-questions-not-decoration.md) supplies passive operational views. [SDRE-039](../ROADMAP.md) next addresses selection loss and cost; [SDRE-042](../ROADMAP.md) through [SDRE-045](../ROADMAP.md) develop SLIs, SLOs, agreements, and error budgets.

## Governing Question

An alert is not merely a threshold crossed or a message sent. A telemetry condition can be mathematically true while requiring no human response. Conversely, user harm can demand response even when the suspected component metric is normal. The engineering problem is to join evidence, decision, recipient, urgency, and a safe action.

That join is difficult because telemetry is delayed, incomplete, aggregated, and sometimes wrong. Systems have transient failures and redundant components. A page competes with sleep, focused work, and other incidents. If a recipient repeatedly receives notifications that do not merit action, the channel loses credibility and a real failure may be ignored.

The governing question is therefore not “What can we detect?” It is: which condition justifies which intervention, by whom, within what time, under which evidence limitations, and how will the team learn whether the alert improved an outcome?

## Why This Matters

Google SRE distinguishes immediate alerts, non-urgent tickets, and informational records and argues that software should perform the alert-domain interpretation before interrupting a human [1]. Its monitoring guidance treats paging as expensive and recommends effective alerts with high signal and low noise [2]. These are design principles, not a claim that every organization must use the same channels.

The practical-alerting chapter describes regularly evaluated time-series rules, pending duration, routing, fan-in, deduplication, and inhibition [3]. Current Prometheus documentation exposes comparable rule states through an expression, optional `for` duration, and optional `keep_firing_for` recovery delay [4]. Current Alertmanager documentation separates evaluation from notification delivery and documents routing, grouping, deduplication, silences, and inhibition [5, 6]. Product details may change; the durable lesson is that detection lifecycle and delivery policy are different mechanisms.

Alerting on SLOs frames an alert as a decision about significant user-impact events and analyzes precision, recall, detection time, and reset time [7]. This chapter uses those concepts without preempting the formal SLI, SLO, and error-budget treatment in SDRE-042–045. Current NIST incident-response guidance places detection and response inside an organizational risk-management capability, reinforcing that a notification needs prepared roles and processes rather than an isolated tool [8].

## Prerequisites and Retrieval

Retrieve monitoring, observability, signal, symptom, cause, metric stream, label set, counter, gauge, histogram, ratio, population, window, evaluation interval, freshness, missingness, threshold, event, severity, owner, on-call rotation, runbook, incident, acknowledgment, mitigation, and resolution.

From SDRE-031 retrieve the distinction between a known operational question and exploratory diagnosis. From SDRE-033 retrieve ratios of compatible populations, low-traffic behavior, counter reset handling, staleness, and bounded dimensions. From SDRE-035 retrieve canonical change identity. From SDRE-037 retrieve visible scope, absolute time, freshness, and drill-down context.

## Learning Objectives

After completing this module, you should be able to:

1. classify operational outputs as pages, tickets, or informational evidence;
2. write an alert contract that joins symptom, population, urgency, owner, and action;
3. trace inactive, pending, firing, resolved, and unknown lifecycle states;
4. budget evaluation, persistence, grouping, and delivery delays;
5. distinguish symptom-based detection from cause-based diagnosis;
6. handle missing, stale, delayed, and low-volume evidence explicitly;
7. design routing, grouping, deduplication, inhibition, silencing, and escalation;
8. use persistence and hysteresis without hiding sustained harm;
9. assess precision, recall, detection time, and operational load honestly;
10. test, govern, review, and retire alerts as production code.

## Core Exposition

**Begin with the intervention.** State what becomes worse if nobody acts before a deadline. If no bounded action is needed, retain the observation for a dashboard, query, report, or ticket. An unusual value is not automatically page-worthy. Pages should normally correspond to current or imminent user harm for which a responder can improve the outcome [1, 2].

Choose urgency from consequence and response window. A page interrupts the current activity because delay matters. A ticket has an owner and due policy but waits for planned work. Informational evidence supports later reasoning without an assigned action. Severity of the eventual incident is related but not identical: the alert initially operates with uncertain evidence, while incident classification may change as impact becomes known.

Write an **alert contract** before writing a query. Include the governed question; service and user population; condition; units; aggregation; lookback window; evaluation interval; activation persistence; recovery rule; evidence-freshness limit; unknown policy; expected traffic assumptions; owner; route; urgency; grouping identity; inhibition relationships; safe silence scope; escalation; notification fields; runbook; verification plan; and retirement condition.

The contract should complete this sentence: “When this notification reaches role $R$, evidence $E$ indicates consequence $C$ within response window $T$, so the first safe action is $A$.” If the sentence says only “CPU is high, investigate,” it lacks a consequence and bounded action.

**Alert on symptoms and diagnose with causes.** A symptom is an externally meaningful failure such as rejected checkouts, unavailable reads, or excessive user-perceived latency. A cause is a possible mechanism such as CPU saturation, queue depth, certificate expiry, or dependency errors. Symptom alerts survive many implementation changes and better represent harm. Cause telemetry is valuable in the linked dashboard and runbook.

The rule is not absolute. A hard quota nearing exhaustion, an expiring certificate, an exhausted storage device, or loss of redundancy may be actionable before user harm appears. Such a predictive page needs a credible time-to-failure model, an intervention that fits that time, and guards against noisy forecasts. “CPU above 80%” is not predictive merely because it precedes some failures.

**Define evidence semantics.** Identify numerator and denominator, eligibility, exclusions, client or server boundary, unit, population, and time. A 50% error ratio from two requests is not equivalent evidence to 5% from a million. A traffic floor can prevent an unstable ratio from paging, but it also creates a blind spot; pair it with synthetic probes, longer windows, or absolute failure counts where appropriate.

Do not average per-instance percentages unless equal-instance weighting is the intended population. Do not alert directly on a histogram quantile without understanding aggregation and sample volume. Do not compare a gauge threshold across machines whose capacity differs. The query is part of the alert's claim and must be versioned and tested.

**Model lifecycle separately from notification.** Let $B(x_t)$ evaluate to true, false, or unknown for each alert identity. A true result creates or advances pending state. The instance fires only after an activation policy such as three consecutive observed breaches or five minutes continuously active. A false result clears pending state. After firing, recovery can require a separate threshold or duration. Unknown is its own evidence result.

Prometheus currently calls a condition active before the optional `for` interval is satisfied “pending” and supports retaining firing state for an optional `keep_firing_for` interval after the condition clears [4]. These are implementation examples. A team must document whether skipped evaluations pause, reset, or invalidate persistence; otherwise “five minutes” is ambiguous during collection loss.

The deterministic model below requires three observed breaches to fire and two observed healthy evaluations to recover. An unknown evaluation displays unknown and pauses streaks rather than proving health. This is one disclosed policy, not a universal alert algorithm.

<!-- bijux-verify: {"id":"alert-lifecycle-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"0 False inactive\n1 True pending\n2 True pending\n3 None unknown\n4 True firing\n5 False firing\n6 True firing\n7 False firing\n8 False inactive\n","stderr":""}} -->
```python
observations = [False, True, True, None, True, False, True, False, False]
state = "inactive"
breach_streak = 0
healthy_streak = 0

for minute, breached in enumerate(observations):
    if breached is None:
        visible_state = "unknown"
    elif state == "firing":
        if breached:
            healthy_streak = 0
        else:
            healthy_streak += 1
            if healthy_streak >= 2:
                state = "inactive"
                breach_streak = 0
        visible_state = state
    else:
        if breached:
            breach_streak += 1
            if breach_streak >= 3:
                state = "firing"
                healthy_streak = 0
            else:
                state = "pending"
        else:
            state = "inactive"
            breach_streak = 0
        visible_state = state
    print(minute, breached, visible_state)
```

At minute 3, telemetry absence does not produce a false recovery. The third observed breach at minute 4 fires. One healthy evaluation at minute 5 does not resolve; the breach at minute 6 cancels recovery. Two later healthy evaluations resolve. In a real system, prolonged unknown evidence usually needs a separate telemetry-health alert and a maximum-uncertainty policy.

**Budget detection and delivery latency.** Suppose the first evaluation that satisfies the condition occurs at $t_e$. If activation persistence is $p$, notification grouping delay $g$, and delivery delay $d$, the earliest notification under this simplified sequence is $t_e+p+g+d$. Query windows and evaluation phase also influence when $t_e$ occurs. A five-minute window, ten-minute persistence, and five-minute grouping delay cannot support a two-minute intervention objective.

Short persistence catches fast harm but pages on transients. Long persistence rejects noise but spends response time. Multi-window designs can combine a fast, high-severity burn with a slower, lower-severity burn [7]. There is no universally safe duration. Derive timing from how fast harm accumulates, measurement delay, recovery behavior, and human response.

Use **hysteresis** where a noisy value crosses a boundary repeatedly. An alert may fire when queue occupancy exceeds 90% for three evaluations and recover only below 70% for five. Activation and recovery asymmetry reduces toggling. It does not repair a meaningless threshold, and excessive recovery delay can keep obsolete incidents open.

**Treat missing evidence as a design branch.** No series can mean no traffic, target removal, service discovery failure, scrape loss, rejected export, query error, access denial, label migration, delayed ingestion, or retention expiry. Zero means a measurement procedure observed zero. Silence means notification delivery was suppressed. None of these is healthy by default.

Define a freshness limit and test the collection path. Where absence is itself actionable, create a separate evidence-health alert with an owner who can restore observability. Avoid circular dependence: if the alert pipeline uses the same failing service and network path as the monitored system, it may disappear during the event it must report. External probes and dead-man signals can reduce, but not eliminate, that risk.

**Separate alert identity from delivery fan-out.** An alert identity should include dimensions needed to distinguish independently actionable situations, not every telemetry label. Including pod ID may generate hundreds of instances for one regional failure. Excluding region may combine failures owned by different responders. Choose identity from action and ownership boundaries.

Evaluation sends alert instances to a notification layer. Deduplication suppresses repeated deliveries of the same identity. Grouping combines related identities into a comprehensible notification. Routing chooses receivers from ownership and urgency. Current Alertmanager documentation implements these as distinct concerns [5, 6]. Preserve enough context in the group to act; a single “many systems broken” page is no better than a storm if it hides affected services and regions.

**Use inhibition and silencing narrowly.** Inhibition suppresses notifications for dependent conditions while a higher-level alert is active: a confirmed cluster outage may inhibit per-instance reachability pages. The inhibiting alert must be at least as actionable and must not suppress independent user-impact symptoms. Test both presence and absence of the source alert.

A silence is an operational change with matchers, start, expiry, owner, reason, and review trail. It should mute notification delivery, not stop rule evaluation or erase evidence. Maintenance is not proof that impact is acceptable. Broad matchers, forgotten expiry, time-zone errors, and copied silences are failure modes. Prefer the narrowest scope and shortest justified duration.

**Escalate receipt, not truth.** A route needs a primary owner, fallback, and acknowledgment deadline. If nobody acknowledges, escalate to a secondary path. Acknowledgment only proves someone accepted responsibility. It does not prove the condition is valid, impact is understood, mitigation succeeded, or the system recovered.

Notification text should contain identity, severity, affected population, observed value and threshold, start time, evidence freshness, current state, likely consequence, owner, runbook, dashboard with preserved scope and time, and recent change links. Keep secrets and personal data out. The notification should support the first decision without becoming a full incident report.

**Write a decision-oriented runbook.** The runbook begins with safety constraints and how to confirm scope. It then supplies a bounded first action, branching diagnosis, mitigation options, required authority, rollback, verification, and escalation. Commands with destructive or external effects require explicit preconditions and confirmation. A copy-paste command with broad credentials is not actionability; it is a latent incident.

Automation uses the same contract. Safe automated remediation needs a narrow trigger, idempotent action where possible, concurrency control, rate limits, authority boundaries, postcondition, timeout, rollback or fail-safe behavior, audit event, and human escalation. If verification evidence comes from the failed signal path, the automation may repeat harm blindly.

**Measure outcomes, not rule count.** For an independently adjudicated set of significant events, let true positives $TP$ be alert decisions matched to significant events, false positives $FP$ unmatched alert decisions, and false negatives $FN$ significant events not detected by the evaluated alert. Then

$$
\text{precision}=\frac{TP}{TP+FP},\qquad
\text{recall}=\frac{TP}{TP+FN},
$$

when denominators are nonzero. These measures depend on an observation interval, event definition, matching window, and adjudication process. Incident records created only after pages will undercount false negatives. One alert may match several notifications, so measure alert decisions and human interruptions separately.

Also measure detection time, delivery time, acknowledgment time, actionability, repeat count, pages per shift, after-hours load, grouped fan-out, stale ownership, silence use, and time to resolution. These are diagnostic measures, not universal quotas. A low page count can mean excellent reliability or blind monitoring.

Review every page: was the condition significant, was routing correct, did the runbook help, could automation safely remove toil, and should the rule, system, or ownership change? Review missed incidents and long silent periods too. Version rules, tests, routes, and runbooks together where possible. Retire an alert when its action, owner, signal, or system disappears.

**Test the whole path.** Unit-test query fixtures for healthy, breach, low traffic, counter reset, partial population, stale data, missing data, delayed ingestion, label migration, and extreme values. Simulate state transitions and recovery. Validate labels, annotations, links, and secrets. Test route selection, grouping, deduplication, inhibition, silence scope, escalation, receiver failure, and notification retries.

Use controlled end-to-end tests to prove that a synthetic condition reaches the intended test receiver with the expected context. Do not page a production human merely to test plumbing without an agreed exercise. Monitor the monitoring system from an independent path, and record which failure combinations remain invisible.

## Definitions and Notation

Let evaluation times be $t_0,t_1,\ldots$ with nominal interval $\Delta>0$. Let $x_t$ be the evidence available at time $t$ for one alert identity and $B(x_t)\in\{0,1,\bot\}$ the alert predicate: false, true, or unknown.

Let $p\ge0$ be activation persistence, $r\ge0$ recovery persistence, $g\ge0$ first-notification grouping delay, and $d\ge0$ delivery delay. These durations operate after query semantics determine the first satisfying evaluation $t_e$. They do not bound the delay between real-world harm and $t_e$ unless collection, window, and evaluation delays are separately bounded.

For adjudicated significant events $S$ and alert decisions $A$ under a declared matching relation, $TP$ counts matched alert decisions, $FP$ unmatched alert decisions, and $FN$ unmatched significant events. Precision and recall are undefined when their denominators are zero; report the counts and interval rather than inventing a percentage.

Let $P$ be a page decision, $K$ the recipient's relevant knowledge and authority, $E$ the evidence supplied, and $U$ the response-time constraint. Actionability is a review judgment about whether $(P,K,E,U)$ supports a safe intervention. It is not proven merely by the presence of a runbook URL.

## Mechanisms, Invariants, or Proof Structure

**State-safety argument.** Assume $\bot$ means evidence is insufficient. Mapping $\bot$ to false makes unknown indistinguishable from observed health. Therefore a recovery derived from that mapping is not justified by the evidence. A rule must preserve unknown or apply a separately justified fail-open or fail-closed policy.

**Delay composition.** Once the first satisfying evaluation is fixed at $t_e$, serial persistence, grouping, and delivery mechanisms yield $t_n=t_e+p+g+d$ in the simplified no-retry path. Increasing any nonnegative component cannot make that notification earlier. Query and collection delays remain outside this equation and must not be hidden.

**Hysteresis argument.** If activation requires $x>h$ and recovery requires $x<l$ with $l<h$, values in $[l,h]$ cannot cause direct activation or recovery. This dead band prevents a single noisy boundary from toggling state, but it deliberately retains the previous state and therefore adds memory and recovery delay.

**Grouping invariant.** Grouping is safe only when all grouped instances share a recipient and compatible first action, and the notification retains distinguishing dimensions required for that action. Otherwise compression destroys decision information.

**Inhibition invariant.** A target notification may be inhibited only while the source condition explains its redundancy and provides an equal or better response path. If the source resolves or routing fails, target eligibility must be reevaluated. Inhibition never establishes that the target condition is false.

**Metric-identification argument.** Counts $TP$, $FP$, and $FN$ require an event universe and matching relation independent enough to discover missed events. Page-derived incident data alone cannot identify $FN$ because unpaged events are absent by construction. Thus alert quality review needs additional sources such as support reports, objective breaches, audits, or retrospective telemetry.

## Alternatives and Trade-Offs

**Symptom versus cause.** Symptoms align with user outcomes and survive implementation changes; causes can warn earlier and direct repair. Page primarily on symptoms, with narrowly justified predictive cause alerts and cause evidence attached for diagnosis.

**Static threshold versus dynamic baseline.** Static thresholds are explainable and testable but may ignore seasonality. Dynamic baselines adapt but introduce training data, drift, and uncertainty. A sophisticated detector is not actionable unless its output maps to consequence and response.

**Short versus long windows.** Short windows detect fast failures and amplify variance. Long windows stabilize estimates and delay detection. Multi-window designs cover different burn rates at the price of rule complexity and possible duplicate notification.

**Consecutive evaluations versus elapsed duration.** Evaluation counts are easy to simulate but their elapsed meaning changes with skipped runs. Wall-clock duration matches an operational promise but needs a documented missing-evaluation policy. Record both nominal interval and actual semantics.

**Single threshold versus hysteresis.** One threshold is simple but can flap. Hysteresis stabilizes state but retains memory and may delay resolution. Recovery should reflect when intervention is no longer needed, not when a graph looks calm.

**Fine versus coarse identity.** Fine labels isolate failures but create high cardinality and page storms. Coarse labels reduce volume but can merge owners and actions. Group delivery after retaining actionable identity when possible.

**Immediate notification versus group wait.** Immediate pages minimize delivery delay. A short group wait allows related evidence and inhibitions to arrive [6]. The wait must be inside the response budget.

**Manual versus automated remediation.** Humans adapt to novel conditions but are slow and inconsistent. Automation is fast and repeatable but can amplify a wrong trigger. Automate narrow, reversible, well-observed actions and escalate uncertain cases.

**Fail-open versus fail-closed on telemetry loss.** Suppressing a page during uncertainty avoids noise but risks blindness. Paging on every gap protects visibility but can overwhelm operators. Separate evidence-health ownership, use independent signals, and choose from consequence rather than convenience.

## Failure Modes and Misconceptions

1. **“Every anomaly deserves a page.”** Anomaly is difference from a model; actionability requires consequence, urgency, ownership, and intervention.
2. **“Every page is an incident.”** A page is a decision under uncertainty; incident declaration and severity are later operational judgments.
3. **“A dashboard panel can double as an alert unchanged.”** Visual exploration tolerates context a human supplies; an alert must encode that interpretation.
4. **“Component cause alerts find root cause.”** A correlated component metric is evidence, not causal proof.
5. **“No data means zero errors.”** Absence may be collection failure or no traffic and cannot establish health.
6. **“A `for` duration removes false positives.”** Persistence rejects some transients but may delay real detection and cannot repair a bad predicate.
7. **“Acknowledged means resolved.”** Acknowledgment assigns responsibility; mitigation and recovery need separate evidence.
8. **“Grouping always reduces noise safely.”** Grouping can merge unrelated owners or hide the affected dimension.
9. **“Inhibited alerts are false.”** Their notification is redundant under a source condition; their evidence may remain true.
10. **“Maintenance makes impact acceptable.”** A silence suppresses delivery; it does not change user harm or objective accounting.
11. **“A runbook link makes a page actionable.”** The runbook must be current, authorized, safe, and decision-oriented.
12. **“Automation makes a weak alert safe.”** Automation can execute a false decision faster and at greater scale.
13. **“High precision alone is enough.”** A system can achieve high precision by missing most significant events.
14. **“Low alert volume proves quality.”** It can also indicate blind telemetry, broken routing, or broad silences.
15. **“The alert system monitors itself.”** Shared dependencies can create correlated blindness; independent checks are required.
16. **“Rules need review only when they fail.”** service, traffic, ownership, objectives, and telemetry schemas drift continuously.

## Worked Examples

### Example 1

**Classify three operational outputs.** A production checkout failure is affecting 20% of eligible attempts and rollback can reduce harm now: page. A certificate expires in 21 days and renewal is a normal owned procedure: ticket with due date. A daily cache-hit change requires no decision: informational evidence. **Conclusion:** urgency follows the response window and action, not how surprising a metric looks.

### Example 2

**Trace activation and recovery.** For the code fixture, observed breaches occur at minutes 1, 2, and 4, with unknown evidence at minute 3. The declared policy pauses rather than resets the breach streak, so minute 4 fires. Healthy minute 5 begins recovery, breach minute 6 cancels it, and healthy minutes 7 and 8 resolve. **Conclusion:** lifecycle claims are reproducible only when unknown and recovery semantics are explicit.

### Example 3

**Compute notification timing.** The first satisfying evaluation is 12:00:30, persistence is 120 seconds, grouping delay 30 seconds, and delivery takes 10 seconds. Then $t_n=12{:}00{:}30+120+30+10=12{:}03{:}10$. This says nothing about how long harm existed before 12:00:30. **Conclusion:** delivery budgeting must separate evidence delay from post-evaluation delay.

### Example 4

**Avoid a low-traffic ratio trap.** Service A has one failed request out of two, a 50% ratio. Service B has 500 failures out of 10,000, a 5% ratio. A rule “ratio above 10%” pages A but not B, although B has far more harm. Add an eligible-volume model, an absolute failure guard, a longer window, or a synthetic user signal according to the service. **Conclusion:** a ratio threshold without population context is incomplete.

### Example 5

**Separate symptom from cause.** Checkout latency is violating the user-facing objective while database CPU is 93%. Page on the checkout symptom and attach database CPU, queue depth, recent deployment, and traces as diagnostic evidence. CPU might be cause, effect, or coincidence. **Conclusion:** response begins from observed harm without asserting an unproved root cause.

### Example 6

**Design identity and grouping.** A partition causes 80 replica reachability alerts in region `eu-north`, all owned by the same platform rotation and sharing one first action. Preserve each instance in evidence but group notification by service, region, and alert name. Keep a separate checkout user-impact alert visible. **Conclusion:** grouping reduces interruptions without discarding actionable scope.

### Example 7

**Check an inhibition rule.** `RegionUnreachable` inhibits `InstanceUnreachable` only when service and region labels match. It must not inhibit `CheckoutFailureRateHigh`, because the user-impact symptom remains the primary response signal. Tests cover source active, source absent, different region, and source resolved. **Conclusion:** inhibition expresses notification redundancy, not truth or health.

### Example 8

**Use hysteresis against flapping.** Queue occupancy samples are 89%, 91%, 88%, 92%, 90%, and 87%. A single 90% boundary toggles repeatedly. Fire only above 90% for three observed evaluations and recover only below 70% for five; this sequence does not fire. If urgent harm occurs at 91%, however, the persistence is too slow. **Conclusion:** hysteresis trades responsiveness for state stability and must follow the harm budget.

### Example 9

**Compute alert quality carefully.** During a reviewed quarter there are 18 alert decisions: 15 match adjudicated significant events and 3 do not. Two additional significant events were found from objective-breach and support evidence without matching alerts. Precision is $15/(15+3)=83.3\%$; recall is $15/(15+2)=88.2\%$. **Conclusion:** both denominators and the independent missed-event search must be disclosed.

### Example 10

**Bound automated remediation.** A storage-pressure alert proposes deleting temporary data. Safe automation restricts paths to an owned cache namespace, checks age and active references, caps bytes per run, acquires a single-writer lease, records candidates, deletes incrementally, verifies free space and service health, stops on uncertainty, and escalates if the postcondition fails. **Conclusion:** actionability includes authority, blast radius, verification, and recovery—not merely a command.

## Cross-Program Connections

1. [STQE-001](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) connects alert rule fixtures and end-to-end notification tests to testing discipline.
2. [SARCH-001](../../12-software-engineering-software-architecture/ROADMAP.md) connects alert identities, ownership, and failure boundaries to architecture.
3. [SEPAT-001](../../11-software-engineering-patterns/ROADMAP.md) connects state machines, policies, and anti-patterns to reusable design reasoning.
4. [SYSENG-001](../../26-systems-engineering/ROADMAP.md) connects evidence, intervention, feedback, and unintended consequences to systems engineering.
5. [DIST-001](../../27-distributed-systems-engineering/ROADMAP.md) connects missing observations, partial failure, clocks, and duplicated delivery to distributed-systems limits.
6. [NET-001](../../24-network-engineering/ROADMAP.md) connects independent probes, partitions, and alert-path reachability to networks.
7. [SEC-001](../../25-security-engineering/ROADMAP.md) connects notification confidentiality, response authority, audit records, and security incident detection.
8. [API-001](../../28-api-and-service-engineering/ROADMAP.md) connects user-facing operations and compatible populations to service symptoms.
9. [PLAT-001](../../29-platform-engineering/ROADMAP.md) connects standardized alert contracts and paved-road routing to platform products.
10. [OS-001](../../22-operating-systems/ROADMAP.md) connects saturation and resource signals to mechanisms that may diagnose, but do not alone prove, user harm.

## References

1. Beyer, B., Jones, C., Petoff, J., and Murphy, N. R., eds. “Introduction—Monitoring.” *Site Reliability Engineering*. O'Reilly/Google, 2016. <https://sre.google/sre-book/introduction/>. Retrieved 2026-09-06.
2. Beyer, B., Jones, C., Petoff, J., and Murphy, N. R., eds. “Monitoring Distributed Systems.” *Site Reliability Engineering*. O'Reilly/Google, 2016. <https://sre.google/sre-book/monitoring-distributed-systems/>. Retrieved 2026-09-06.
3. Wilkinson, J. “Practical Alerting from Time-Series Data.” *Site Reliability Engineering*. O'Reilly/Google, 2016. <https://sre.google/sre-book/practical-alerting/>. Retrieved 2026-09-06.
4. Prometheus Authors. “Alerting Rules.” Current Prometheus documentation. <https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/>. Retrieved 2026-09-06.
5. Prometheus Authors. “Alertmanager.” Current Prometheus documentation. <https://prometheus.io/docs/alerting/latest/alertmanager/>. Retrieved 2026-09-06.
6. Prometheus Authors. “Alertmanager Configuration.” Current Prometheus documentation. <https://prometheus.io/docs/alerting/latest/configuration/>. Retrieved 2026-09-06.
7. Thurgood, S., Frame, J., Lenton, A., Quinito, C., Tolchanov, A., and Trdin, N. “Alerting on SLOs.” *The Site Reliability Workbook*. O'Reilly/Google, 2018. <https://sre.google/workbook/alerting-on-slos/>. Retrieved 2026-09-06.
8. Nelson, A., Rekhi, S., Souppaya, M., and Scarfone, K. *Incident Response Recommendations and Considerations for Cybersecurity Risk Management: A CSF 2.0 Community Profile*. NIST SP 800-61 Rev. 3, final, April 2025. <https://doi.org/10.6028/NIST.SP.800-61r3>. Retrieved 2026-09-06.

## Exercises

### Exercise 1

Define an alert instance, pending, firing, resolved, unknown, page, ticket, inhibition, and silence. State why acknowledgment is not resolution.

### Exercise 2

An alert first evaluates true at 09:15:20. Its activation persistence is 180 seconds, group wait is 40 seconds, and delivery takes 15 seconds. Under the simplified serial model, compute the earliest notification time. Then explain one delay excluded from the result.

### Exercise 3

A request-ratio alert resolves whenever its query returns no series. Diagnose the defect and design fixtures for zero traffic, collection failure, target removal, query error, observed zero failures, and actual recovery.

### Exercise 4

Design a page contract for a multi-region document service whose writes can fail while reads remain healthy. Include population, condition, timing, missingness, identity, grouping, routing, inhibition, notification context, runbook first action, and verification.

### Exercise 5

Transfer the principles to a refrigerated medicine warehouse. Sensors report temperature and door state through one gateway; staff can move stock to a backup room. Design actionable notification classes and address sensor disagreement, gateway loss, persistence, escalation, silencing, and safe automation.

## Answers to the Exercises

### Answer 1

An alert instance is one evaluated condition plus its identifying label set and lifecycle state. Pending means true evidence has not yet met activation persistence; firing means it has. Resolved means a formerly firing condition met the recovery policy. Unknown means available evidence cannot justify true or false. A page requests immediate human intervention; a ticket requests owned but deferrable work. Inhibition suppresses a target notification while an explanatory source condition is active. A silence is an explicit matcher-based, time-bounded suppression. Acknowledgment establishes receipt and responsibility only; resolution requires recovery evidence under the alert contract.

### Answer 2

Add the serial components: $09{:}15{:}20+180\text{ s}=09{:}18{:}20$, plus 40 seconds gives 09:19:00, plus 15 seconds gives **09:19:15**. The model excludes the delay from real-world harm to the first satisfying evaluation, including collection, ingestion, query-window, and evaluation-phase delays. It also excludes delivery retries. A complete response states these limits rather than presenting 3 minutes 55 seconds as end-to-end detection time.

### Answer 3

The rule maps absence to healthy and can falsely resolve during telemetry failure. Preserve false, observed zero, and unknown separately. Fixtures should assert: zero traffic yields an explicitly low-volume or no-traffic result; collection failure yields stale or unknown; expected target removal follows an inventory/change policy; query error yields unavailable; observed requests with zero failures yields healthy evidence; and observed compatible requests below the recovery threshold for the declared duration yields resolved. Add a separate evidence-health alert, test prolonged unknown behavior, and verify the notification path independently.

### Answer 4

Page when the unsuccessful eligible-write ratio or a bounded synthetic write probe shows sustained production user harm; keep healthy reads as context, not a reason to suppress. Define client-visible eligible writes by service, region, tenant tier, and operation, with a traffic or probe strategy for low volume. Evaluate every minute, select persistence from the error-budget and intervention window, and define separate recovery. Unknown or stale write evidence cannot resolve and routes to evidence-health ownership. Identify instances by service and affected region, group replicas, route to the document-service on-call, and inhibit replica-cause pages under a region failure while retaining the write symptom. Include values, denominators, timestamps, freshness, recent changes, scoped dashboard, owner, and runbook. First action confirms user impact and chooses a tested traffic shift or write-disable safeguard within authority; post-action probes and user SLIs verify mitigation. Acceptable variants must preserve write/read distinction, missingness, bounded authority, and independent verification.

### Answer 5

Page for credible imminent medicine-safety risk when a trained responder can move stock within the remaining safe interval. Create tickets for battery degradation, scheduled calibration, or backup-capacity work; retain ordinary door events informationally. Require redundant sensor agreement or a conservative disagreement policy based on medicine risk, sensor calibration, and rate of temperature change. Gateway loss is unknown, not normal temperature, and needs an independent heartbeat or secondary communication path. Persistence must reject brief door openings without consuming the relocation window. Route to the staffed facility role, escalate on missed acknowledgment, and include location, affected inventory class, temperatures, evidence age, remaining safe-time estimate, and authorized procedure. Maintenance silences are narrow, owned, expiring, and accompanied by physical monitoring. Automation may start backup cooling if interlocked, reversible, capacity-checked, and independently verified; moving regulated stock remains within documented human authority. Evaluation rewards consequence-led urgency, evidence uncertainty, escalation, and safe verification rather than a particular numeric threshold.
