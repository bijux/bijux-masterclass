---
module_id: PLAT-081
program: Platform Engineering
level: 2
module_number: 81
title: Platform Service-Level Objectives
status: complete
last_verified: 2026-09-02
---

# Platform Service-Level Objectives

## One-Page Review

### Governing question

How should a platform define, measure, and govern reliability for complete developer and operator journeys so that users know what to expect, teams can spend error budgets deliberately, and component health, telemetry gaps, dependency failures, low traffic, and hidden manual work cannot produce false confidence?

### Essential definitions

- A **service-level indicator (SLI)** is a precisely defined quantitative measure of delivered service behavior.
- A **service-level objective (SLO)** is a target or range for an SLI over a stated compliance window.
- A **service-level agreement (SLA)** is an agreement with explicit consequences for missing stated service levels; an internal SLO is not automatically an SLA.
- A **good event** is a valid event satisfying the SLI’s success criteria; a **valid event** is included in its population after declared exclusions.
- A **request-based SLO** measures the ratio of good events to valid events; a **window-based SLO** measures the ratio of good time slices to valid time slices.
- An **error budget** is the permitted fraction or count of non-good events implied by the objective, such as $1-SLO$ for a ratio target.
- **burn rate** is the observed bad-event rate divided by the permitted bad-event rate; burn rate 1 consumes budget at the planned pace.
- A **user journey** is an end-to-end outcome such as create environment, publish artifact, deploy, observe status, or roll back—not merely one internal API request.
- **measurement coverage** states which users, routes, stages, regions, tenants, and failure classes the SLI observes.
- **unknown** is a distinct measurement state caused by missing, delayed, contradictory, or invalid telemetry; it must not silently become good.
- **correctness** asks whether the intended result was produced; **availability** only asks whether an eligible operation was served according to its contract.
- A **dependency budget** is an allocated reliability assumption for a dependency edge, not a guarantee obtained by copying the dependency provider’s headline SLO.

### Central model, mechanism, or theorem

For journey $j$ over window $W$, let $V_j(W)$ be valid events and $G_j(W)\subseteq V_j(W)$ good events. Then

$$
SLI_j(W)=\frac{|G_j(W)|}{|V_j(W)|},\qquad
Budget_j(W)=(1-SLO_j)|V_j(W)|,
$$

and for subwindow $w$,

$$
Burn_j(w)=\frac{1-|G_j(w)|/|V_j(w)|}{1-SLO_j}.
$$

The equations are meaningful only if event eligibility, goodness, observation point, deadlines, exclusions, late data, and unknown telemetry are explicit. Platform SLOs should measure externally meaningful journey outcomes at the closest trustworthy user boundary, with diagnostic component SLIs underneath. A green component dashboard cannot prove a green user journey.

### Critical invariants

- Each SLO names the user/persona, journey, provider and accountable owner, good and valid event definitions, observation point, target, window, exclusions, data source, and response policy.
- Success includes correct outcome and deadline where relevant; accepted work that never converges is not automatically good.
- User-caused invalid requests, intentional policy denials, cancellations, retries, provider failures, and platform-generated mistakes are classified explicitly and consistently.
- Unknown or missing measurement is surfaced with coverage/error bounds and cannot improve compliance by removing bad events.
- SLIs are segmented enough to expose harmed tenants, regions, workflow types, and payload classes without creating unbounded cardinality.
- Async journeys correlate request, durable acceptance, reconciliation, terminal state, and deadline using stable identifiers.
- SLO targets reflect user/business needs, dependency reality, architecture, capacity, recovery, cost, and risk—not current performance or a desire for round numbers.
- Error-budget policy names allowed actions, escalation, incident thresholds, recovery investment, and exceptions before budget exhaustion.
- Alerts page on actionable threat to user objectives using burn and corroborating coverage; they do not page on every component symptom.
- SLO definitions, queries, recording rules, dashboards, alerts, exclusions, and policies are versioned, reviewed, tested, and reproducible.
- Measurement pipelines have their own freshness, completeness, correctness, and availability objectives plus independent synthetic checks.
- The platform and consuming teams share decisions at their boundary: platform owns delivered capability reliability; consumers own workload use and declared dependency needs.

### Common failures

Calling uptime an SLO without a user; measuring portal availability while workflows fail; accepting HTTP 202 as journey success; treating every denial as platform failure or every denial as user fault; excluding timeouts that lack status codes; denominator collapse during outage; counting retries as independent users; average latency hiding tails; averaging percentiles; aggregate fleet success hiding one broken region; sampling sparse failures; telemetry loss reported as 100 percent; alerting on instantaneous error rate; paging on budget already spent rather than fast burn; target copied from a cloud SLA; multiplying component SLOs without topology or correlation; double-counting dependent failures; setting 100 percent; rewarding overachievement; freezing all change mechanically; changing query mid-window; and publishing SLOs with no consequence.

### Compact example

For “deploy an approved service revision to production,” a valid event begins when an authenticated authorized request with complete inputs is durably accepted. It is good only if the exact artifact reaches the requested environment, required health gates pass, status becomes visible, and the workflow terminates within 15 minutes. Policy denial before acceptance is separately measured as decision latency/correctness; platform-generated invalid templates count bad. The objective is 99.5 percent good over rolling 28 days, segmented by region and workflow class. Unknown terminal correlation counts against a measurement-coverage objective and conservatively as bad for release decisions. Multi-window burn alerts page fast severe loss and ticket slow consumption. The error-budget policy balances feature change, platform reliability work, and customer communication.

### Connections

Platform SLOs turn the platform-as-product promise and autonomy model from PLAT-001–080 into measurable expectations. They consume event, catalog, workflow, policy, audit, identity, and artifact evidence from PLAT-061–079. They constrain control-plane capacity, fleet management, upgrades, overload, incidents, disaster recovery, cost, and scaling in PLAT-082–090.

## Governing Question

What observable behavior proves that a platform user successfully completed a valuable task—and what will provider and consumer teams do when that behavior becomes unreliable?

A platform is a distributed product composed of portals, APIs, workflow engines, controllers, cloud services, clusters, registries, identity, policy, and telemetry. Component uptime is useful for diagnosis, but users experience journeys across those components.

An SLO is therefore both a measurement contract and a decision mechanism. It creates a shared language for acceptable unreliability, investment, change velocity, escalation, and dependency expectations. Without the response policy, a percentage is decoration.

## Why This Matters

Platform failure blocks many teams simultaneously. A slow deployment workflow increases lead time; a broken rollback increases incident duration; stale ownership or policy status creates unsafe decisions. These harms are not captured by CPU, pod readiness, or portal HTTP success alone.

Internal users adapt to experienced reliability. If a platform promises 99.5 percent but silently delivers 99.999 percent, consumers may design without fallback and make later cost-saving changes politically impossible. If it routinely misses objectives without action, teams build shadow paths and lose trust.

Targets create economic consequences. Each extra nine may require redundancy, isolation, staffing, capacity, testing, and dependency contracts. Too loose wastes user time; too strict diverts engineering effort from capabilities and may encourage denominator manipulation.

Measurement itself can lie. Telemetry disappears during the same network partition that breaks the service; asynchronous jobs finish after the query window; failed requests lack response labels; aggregate success hides a harmed tenant. SLO engineering must include evidence quality.

## Prerequisites and Retrieval

Retrieve probability, ratios, percentiles, histograms, confidence intervals, sampling, time series, counters, monotonicity and resets; user journeys and product research; APIs, queues, workflows, reconciliation, deadlines and idempotency; distributed tracing and correlation; observability pipelines; SLIs, SLOs, SLAs and error budgets; burn-rate alerting; dependency graphs and failure correlation; retries, hedging, load shedding and backpressure; capacity planning; multi-tenancy and regional architecture; incident response; progressive delivery; policy and audit evidence; cost/risk decisions; and SLO-as-code/version control.

Distinguish user outcome from component state; availability from correctness; accepted from completed; valid from good; error from expected denial; provider fault from consumer invalid input; request-based from time-slice SLO; percentile threshold from “percent of events below threshold”; rolling from calendar window; budget remaining from burn rate; symptom alert from diagnostic alert; target from current performance; internal SLO from external SLA; dependency promise from observed edge behavior; telemetry absence from service success; and aggregate from segmented experience.

## Learning Objectives

After completing this module, you should be able to:

1. discover and prioritize platform user journeys that need reliability objectives;
2. define good, valid, bad, unknown, excluded, canceled, denied, retried, and late events at trustworthy observation points;
3. construct availability, latency, correctness, freshness, durability, throughput, and convergence SLIs for synchronous and asynchronous capabilities;
4. choose request- or window-based objectives, compliance windows, targets, segmentation, and error-budget policies;
5. calculate error budgets, burn rates, time to exhaustion, and multi-window alert conditions;
6. evaluate histogram/percentile aggregation, sparse traffic, retry bias, denominator loss, and measurement uncertainty;
7. allocate reliability across dependencies without assuming independence or copying provider SLAs;
8. manage SLO definitions, queries, alerts, and policies as reviewed, tested, reproducible artifacts;
9. use objectives in release, capacity, incident, support, roadmap, and deprecation decisions; and
10. migrate component-centric monitoring into a small portfolio of actionable journey SLOs.

## Core Exposition

### Discover consequential user journeys

Interview and observe developers, operators, security teams, and service owners. Map tasks such as discover capability, register service, provision environment, obtain identity, build, publish, deploy, view state, change quota, rotate secret, diagnose failure, roll back, and recover.

Prioritize journeys by frequency, blocked engineers, production consequence, time sensitivity, and availability of an alternate path. A rarely used disaster-recovery operation can deserve an objective because its failure cost is extreme, although continuous synthetic evidence may be more meaningful than request ratios.

Write the user and desired outcome. “Deployment API uptime” is component-centered; “authorized service owner can deploy an approved revision and observe healthy terminal state within 15 minutes” is a journey.

Keep the portfolio small enough to drive decisions. Component metrics remain diagnostic. Add an SLO only when missing it changes priority, behavior, or expectations.

### Draw the journey state machine

Define start, acceptance, intermediate states, terminal success, terminal failure, deadline, cancellation, retry, and reconciliation. For async work, an initial 202 response proves only acknowledgement.

Choose the unit of user intent. One intent may generate retries, controller reconciliations, provider API calls, and status polls. Count the intent once using an idempotency or workflow ID, otherwise platform retry behavior distorts both numerator and denominator.

State when an event becomes valid. Reject malformed requests before acceptance and measure usability separately. If the platform generated the malformed configuration through its template, classify it as a platform failure rather than hiding it as client error.

Retain final outcome after the compliance query closes. Late completion may remain bad for the original deadline but updates diagnostic state. Never rewrite the historical deadline criterion.

### Define goodness from the user's boundary

A good synchronous request may require correct response class and latency below a threshold measured from the external ingress. Server-side latency excludes DNS, network, gateway, or client-visible queuing; use it only if the boundary is explicit.

A good provisioning event requires the requested capability to reach usable state, not merely exist. Define functional probes or authoritative state: credentials issued, endpoint reachable, policy attached, backup scheduled, ownership recorded, and status discoverable.

Correctness often needs domain validation. A green HTTP status with the wrong artifact, tenant, region, policy revision, or resource parameters is bad. Use audit and workflow evidence to bind requested and observed subjects.

Measure degraded success separately when useful, but map it deterministically into the objective. A deployment completed in 8 minutes may be good, 8–15 tolerated for a secondary objective, and beyond 15 bad; do not improvise after incidents.

### Define valid events and exclusions

List all included sources, tenants, environments, methods, workflow types, payload classes, and status outcomes. Exclusions need rule, owner, rationale, evidence, and review date.

Expected policy denials can be valid and good for a policy-decision SLO while not entering a deployment-completion denominator because no workflow was accepted. A policy engine timeout or erroneous denial is bad for decision availability/correctness.

Client cancellation is ambiguous. If the platform exceeded the deadline before cancellation, counting it excluded rewards slowness. Define based on causal timing and server work. Load-test client behavior so disconnections do not erase provider errors.

Maintenance is not automatically excluded. If users were promised service during the interval, planned downtime consumes budget. A published non-service window may be excluded only when user expectations and dependent designs accept it.

### Choose request-based or window-based objectives

Request-based SLOs weight each event. They fit APIs and workflows with identifiable attempts and expose traffic-weighted user impact. A high-volume tenant may dominate aggregate results.

Window-based SLOs divide time into slices and call each good or bad. They fit continuous reachability or sparse services but lose detail: one and one thousand failed requests can make the same bad window. Define slice length and goodness threshold.

Use multiple objectives only for distinct decisions: perhaps 99.9 percent availability and 99 percent under 2 seconds. Avoid encoding a whole dashboard as SLOs.

For batch/freshness systems, define whether each scheduled output met correctness and freshness deadline. For durable resources, use periodic verified observations plus restore tests rather than claiming durability from availability metrics.

### Select target and compliance window

Start from user need and consequence. Ask how much failed work users tolerate, how long impairment may persist, what alternative exists, and what downstream reliability assumes. Then compare architecture, dependencies, capacity, recovery, and cost.

Do not set target equal to recent performance. It may ratify accidental overperformance or chronic failure. Measure a baseline, but make the objective a product/risk decision.

Rolling windows give continuously comparable recent experience. Calendar windows align reporting or contracts but reset boundaries can create perverse behavior. Record timezone and late-data closure for calendar calculations.

Maintain an internal margin between operating goal and external commitment where consequences justify it. Avoid 100 percent: it permits no learning or safe change and is usually unachievable across distributed dependencies.

### Calculate budget and burn

For target $S=0.995$ and 20,000 valid deployments, the error budget is $0.005\times20{,}000=100$ bad deployments. If a subwindow observes 2 percent bad, burn is $0.02/0.005=4$: four times planned consumption.

At constant burn $b>0$, approximate time to exhaust a fresh $W$-length budget as $W/b$. Remaining-budget forecasts use actual remaining fraction and observed rate; traffic-based budgets can disappear rapidly during high volume.

Budget remaining answers how much has been spent in the compliance window. Burn rate answers how quickly current behavior is spending it. Alert on burn early enough for action, not only after the SLO is already missed.

Keep arithmetic based on counters or event tables whose reset, delay, deduplication, and completeness behavior is understood. Recompute representative windows independently.

### Alert with multiple windows

A short window detects severe fresh failure but is noisy; a long window is stable but clears slowly. Multi-window, multi-burn-rate alerts pair a long window confirming meaningful budget threat with a short window confirming the problem is current.

Page for fast burn that threatens a substantial budget fraction within response time. Create tickets or daytime alerts for slower sustained burn. Attach journey, affected segments, budget/burn, coverage, recent changes, and diagnostic links.

Do not require every component alarm to page the platform on-call. Component saturation, queue depth, dependency errors, and reconciliation lag are diagnostic or predictive signals. Promote them to paging only when urgent and actionable before user harm.

Backtest alerts against incidents and quiet periods. Measure precision, recall for material user events, time to detect, time to clear, pages per incident, and operator action.

### Measure latency correctly

For threshold SLOs, directly count events below the threshold. This is often clearer than calculating a percentile and comparing it with a target. “99 percent under 2 seconds” is a good/valid ratio.

Do not average percentiles across instances or intervals. Prometheus summaries expose precomputed quantiles that generally cannot be aggregated; compatible histograms retain bucket counts that can be aggregated, with approximation error determined by bucket layout or resolution.

Place histogram boundaries around meaningful deadlines. Track overflow/timeouts explicitly. A request that times out without a duration observation must still enter the bad-event population.

Segment interactive, bulk, payload size, and operation class when their expectations differ. Do not allow arbitrary route or tenant labels to explode metric cardinality; compute detailed audit tables outside the hot metric path where necessary.

### Handle low traffic and missing data

With ten monthly operations, a 99.9 percent ratio offers no useful gradual budget: one failure produces 90 percent. Use longer evidence windows, per-operation success, synthetic transactions, readiness tests, or explicit maximum failures appropriate to consequence.

Zero valid events means no observed demand, not 100 percent success. Render “no data” and evaluate measurement health. Synthetic probes indicate probe-path health but do not replace real user diversity.

Telemetry loss can shrink denominators or remove timeouts. Compare ingress, workflow, queue, terminal, and audit counts; expose unmatched IDs and late events. Define conservative treatment for release decisions and a separate measurement coverage SLO.

Sampling requires known inclusion probabilities and confidence bounds. Avoid sampling sparse high-impact workflows. If exact event logs are available, use them as a reconciled SLO source rather than extrapolating a sampled trace.

### Segment without hiding fleet harm

Report global objective plus critical region, tenant tier, journey class, and platform version. A global 99.9 can coexist with a region at zero if its traffic share is small.

Define minimum traffic/evidence thresholds and escalation for small cohorts. Avoid promising a separate formal SLO for every tenant unless the architecture and reporting support it; still detect severe localized harm.

Weighting encodes values. Traffic-weighted ratios describe affected requests; tenant-weighted windows describe breadth; revenue or criticality weighting describes business priority. Label the choice rather than presenting it as neutral.

Preserve Simpson’s paradox checks: changes in traffic mix can improve an aggregate while every cohort worsens. Compare cohort and mix over time.

### Allocate dependency reliability

Draw the journey dependency graph with serial, parallel, fallback, cache, retry, and optional edges. Measure the platform’s actual calls at the edge; the provider’s external SLO may cover different regions, methods, quotas, maintenance, or observation points.

Multiplying availability assumes every dependency is required and failures are independent. Shared networks, identity, regions, and control planes create correlation; retries and fallback change effective behavior. Use fault trees, trace/event evidence, and experiments.

Set dependency expectations stricter than the end-to-end target where it is a necessary edge, leaving budget for platform code and other dependencies. Add caching, degradation, isolation, or alternate providers where needed.

Attribute failure for diagnosis and commercial follow-up, but do not remove dependency-caused user failures from the platform journey SLO if the platform promised the outcome.

### Define ownership and error-budget policy

The platform product owner and operational owner jointly own the journey objective. Component teams own diagnostic objectives and contributions. Consuming teams state their dependency needs and operate workload-specific behavior.

Write policy before exhaustion: thresholds for incident declaration, change review, rollout slowing, reliability work, dependency escalation, capacity addition, and leadership/customer communication. Avoid a universal automatic feature freeze; response should address the dominant risk while emergency fixes remain possible.

Treat budget as permission to take considered risk, not a quota that must be spent or an excuse for known harm. Repeated misses require architectural/product decisions; repeated vast overperformance may justify cost or target review.

Error-budget exceptions name decision owner, duration, rationale, expected consumption, guardrails, evidence, and exit. Never rewrite the SLI after an outage to recover budget.

### Manage SLOs as code

Store owner, service/journey, description, SLI query or event contract, data source, target, window, budgeting method, segmentation, exclusions, alert policies, error-budget policy, dashboard, runbook, and version. OpenSLO provides a portable declarative vocabulary; local extensions still require governance.

Test schema, query syntax, counter behavior, label sets, unit conversions, empty input, timeout inclusion, replay data, target math, and alert windows. Backtest changes over historical periods and show old/new compliance before approval.

Pin recording/query revisions for period reports. If an instrumentation semantic convention changes, dual-emit or translate with known boundaries before changing the SLI.

Use code review by platform owner, telemetry expert, user representative, and risk/business owner in proportion to consequence. Changes should take effect at a declared boundary rather than rewriting an active compliance window.

### Validate measurement and service behavior

Inject synthetic good, slow, wrong, denied, timed-out, canceled, duplicate, retried, and missing-terminal events. Verify numerator, denominator, exclusion, segment, budget, alert, and report.

Compare black-box probes, edge logs, workflow state, controller status, audit records, and user reports. No source is perfect; agreement and explained disagreement build confidence.

Fault-test dependencies, telemetry, queue, region, identity, policy, storage, and control plane. Confirm that user harm enters the journey SLI even if the failing component lacks metrics.

Restore monitoring rules, SLO definitions, long-term counters/event records, dashboards, alerts, ownership, and policy. A disaster-recovered platform without measurement cannot safely claim restored reliability.

### Evolve the SLO portfolio

Start with one or two critical journeys and imperfect but explicit indicators. Run them without consequences while validating data, then adopt error-budget decisions. Perfection before use creates endless metric design.

Review quarterly and after major incidents, architecture, user population, dependency, or product promise changes. Retire SLOs that drive no decision and add missing journeys exposed by user research.

Publish performance, budget, incidents, measurement gaps, and planned action. Do not expose sensitive tenant detail or use SLO reports to blame teams.

As PLAT-080 emphasizes, objectives mediate autonomy: reliable paved roads widen self-service, while exhausted budgets or unknown evidence trigger deliberate containment and investment.

## Definitions and Notation

For journey $j$, compliance window $W$, and subwindow $w\subseteq W$:

- $V_j(w)$: distinct valid user-intent events;
- $G_j(w)$: events meeting correctness and deadline criteria;
- $B_j(w)=V_j(w)-G_j(w)$: bad events;
- $U_j(w)$: events with unknown outcome or measurement;
- $S_j$: objective ratio;
- $e_j=1-S_j$: permitted error fraction;
- $E_j(W)=e_j|V_j(W)|$: total event error budget;
- $C_j(w)$: measurement coverage or reconciled fraction.

Observed compliance and burn are

$$
\hat{s}_j(w)=\frac{|G_j(w)|}{|V_j(w)|},\qquad
b_j(w)=\frac{|B_j(w)|/|V_j(w)|}{e_j}.
$$

When $|V|=0$, these ratios are undefined. When $U>0$, publish bounds. If unknowns could all be bad or good,

$$
\frac{|G|}{|V|+|U|}\le s_{true}\le\frac{|G|+|U|}{|V|+|U|}.
$$

For time-slice SLOs, replace events with valid slices and define a slice-good predicate. For latency threshold $L$, $G=\{x\in V: correct(x)\land latency(x)\le L\}$.

## Mechanisms, Invariants, or Proof Structure

### Platform SLO mechanism

1. Discover critical user/operator journeys and the decisions an objective should change.
2. Draw each journey’s state machine, user intent, deadlines, retry/cancel behavior, dependencies, and terminal outcomes.
3. Define good, valid, bad, excluded, and unknown events at the closest trustworthy user boundary.
4. Select request- or window-based budgeting, segmentation, target, rolling/calendar window, and measurement closure.
5. Instrument stable correlation across edge, workflow, controllers, dependencies, resource/artifact state, and audit.
6. Reconcile counts and unknowns; validate histogram, counter, reset, late-data, sampling, and cardinality behavior.
7. Calculate budget, remaining fraction, burn, uncertainty bounds, and dependency contributions from versioned queries.
8. Define multi-window paging/ticket alerts plus diagnostic signals, runbooks, and measurement-health alerts.
9. Agree ownership and an error-budget policy for change, incidents, capacity, reliability investment, and escalation.
10. Store definition, query, target, alerts, dashboard, exclusions, policy, owner, and revision as reviewed artifacts.
11. Backtest and fault-test good/bad/unknown cases, dependencies, telemetry loss, low traffic, and disaster recovery.
12. Publish outcomes and limitations, use them in decisions, and revise or retire objectives as journeys change.

### Journey invariant

Each objective measures a user-meaningful outcome from declared initiation to correct terminal state or deadline. Internal acceptance or component readiness cannot substitute for completion unless that is the promised outcome.

### Population invariant

Every potential event is deterministically included, excluded, or marked unknown under versioned rules. Failure mode cannot remove itself from the denominator.

### Measurement invariant

SLO reports bind to source coverage, query and schema revisions, late-data rule, and measurement health. Missing evidence narrows or bounds the conclusion rather than improving it.

### Decision invariant

Each SLO has a pre-agreed response policy and accountable owner. If meeting or missing it never changes a decision, it is a dashboard metric, not an effective objective.

### Dependency invariant

The platform owns the promised end-to-end journey even when a dependency causes failure. Attribution informs remediation; it does not erase user impact.

### Proof sketch: component averages cannot establish journey reliability

Consider a journey requiring components $A$ and $B$. Both report 99 percent availability. In world $W_1$, their one-percent outages overlap, so the serial journey can be available 99 percent. In world $W_2$, their outages are disjoint, so the journey can be available only 98 percent. Component figures are identical but journey reliability differs.

Topology adds further ambiguity: fallback, retries, partial operations, correlated dependencies, and mismatched observation populations. Therefore component SLOs or their average cannot determine end-to-end reliability. Measure the journey directly and use component/dependency indicators diagnostically. Multiplication gives a model only under explicit independence and required-edge assumptions, not a general proof.

### Executable budget audit

The synthetic program calculates classification for ten subwindows of a 99.5 percent objective. It treats unknown events conservatively as bad for the decision. It demonstrates arithmetic, not a production SLO or alert recommendation.

<!-- bijux-verify: {"id":"platform-slo-budget-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"healthy=5\nslow_burn=3\nfast_burn=2\nvalid=10000\ngood=9929\nunknown=3\noverall_burn=1.42\n"}} -->
```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Window:
    valid: int
    good: int
    unknown: int = 0


windows = [
    Window(1000, 998),
    Window(1000, 997),
    Window(1000, 999),
    Window(1000, 1000),
    Window(1000, 998),
    Window(1000, 992),
    Window(1000, 991),
    Window(1000, 980, 1),
    Window(1000, 985, 2),
    Window(1000, 989),
]

error_fraction = 1 - 0.995
counts = {"healthy": 0, "slow_burn": 0, "fast_burn": 0}
for window in windows:
    bad = window.valid - window.good + window.unknown
    burn = (bad / window.valid) / error_fraction
    if burn <= 1:
        counts["healthy"] += 1
    elif burn < 3:
        counts["slow_burn"] += 1
    else:
        counts["fast_burn"] += 1

valid = sum(window.valid for window in windows)
good = sum(window.good for window in windows)
unknown = sum(window.unknown for window in windows)
overall_burn = ((valid - good) / valid) / error_fraction

for name, count in counts.items():
    print(f"{name}={count}")
print(f"valid={valid}")
print(f"good={good}")
print(f"unknown={unknown}")
print(f"overall_burn={overall_burn:.2f}")
```

### Verification strategy

Create a truth table for every response/outcome, cancellation, retry, denial, timeout, late completion, and missing record. Generate controlled events and compare expected numerator, denominator, segment, compliance, budget, burn, and alerts. Independently recompute from raw audit/workflow events.

Test metric and event pipelines during the same faults that harm the platform: network partition, regional loss, full queue, collector restart, counter reset, schema migration, clock skew, duplicate delivery, storage delay, and dashboard restore. Verify unknown coverage alerts precede misleading green reports.

Backtest targets and multi-window alerts across incidents, maintenance, quiet periods, traffic spikes, and low-volume cohorts. Exercise error-budget decisions with platform, consumer, product, and risk owners. Confirm emergency fixes, rollback, and measurement repair remain possible when budget is exhausted.

## Alternatives and Trade-Offs

1. **Journey SLO versus component SLO:** journeys express user value; components localize diagnosis. Maintain both with different roles.
2. **Request-based versus window-based:** requests measure traffic-weighted impact; windows measure continuity but compress failure volume.
3. **Rolling versus calendar window:** rolling windows support current decisions; calendar windows align reporting but create reset edges.
4. **Server-side versus client/edge measurement:** server data is controllable; edge data covers more user experience but adds external variability.
5. **Real traffic versus synthetic probe:** real traffic reflects users; probes cover idle periods and known paths but lack diversity.
6. **Availability versus correctness:** availability is easier to automate; correctness is closer to value and needs domain evidence.
7. **Aggregate versus segmented objective:** aggregate is simple; segmentation exposes localized harm at greater data/cardinality cost.
8. **Traffic weighting versus tenant weighting:** traffic shows affected operations; tenant weighting prevents small cohorts disappearing.
9. **Percentile versus threshold ratio:** percentiles describe distributions; a threshold ratio maps directly to good events and budget.
10. **Histogram versus summary:** histograms support aggregation with approximation; summaries give local quantiles that generally cannot aggregate.
11. **Strict unknown-as-bad versus bounded reporting:** conservative treatment protects decisions; bounds preserve epistemic accuracy when sources fail.
12. **High target versus affordable target:** stronger expectation reduces tolerated harm but increases redundancy, capacity, and coordination cost.
13. **One end-to-end SLO versus stage SLOs:** end-to-end owns outcome; stages identify bottlenecks but can encourage local optimization.
14. **Provider SLO versus measured dependency edge:** provider terms are convenient; edge measurement reflects actual method, region, quota, and fallback.
15. **Fast burn page versus static threshold:** burn aligns urgency with budget; static thresholds can be simpler for hard safety limits.
16. **Automatic freeze versus contextual budget policy:** automation is predictable; context prevents blocking recovery and unrelated low-risk change.
17. **Central SLO tooling versus federated definitions:** central tooling standardizes evidence; federated ownership keeps journeys domain-relevant.
18. **Immutable period definition versus immediate correction:** immutability preserves accountability; errors require versioned correction and restatement, not silent rewrite.

## Failure Modes and Misconceptions

- **“SLO means SLA.”** An SLA includes explicit agreement consequences; not every internal objective does.
- **“Availability is uptime.”** User requests or journeys can fail while processes remain running.
- **“HTTP 2xx is success.”** Correct subject, effect, and deadline may still be wrong.
- **“Accepted means completed.”** Async acknowledgement is only one state transition.
- **“All 4xx responses are client fault.”** Platform-generated invalid inputs, erroneous policy, auth dependencies, or broken docs can be provider failures.
- **“Timeouts are absent from latency.”** Missing timeout observations must enter bad-event accounting.
- **“No requests means 100 percent.”** The ratio is undefined without a valid population.
- **“No telemetry means no errors.”** It means measurement is unknown.
- **“Retry success cancels first failure.”** Count user intent under a documented retry success contract.
- **“More retries always improve SLO.”** They add load, latency, duplication, and correlated failure.
- **“Average latency describes users.”** Skew and tails make averages misleading.
- **“Average of p99s is global p99.”** Precomputed quantiles generally cannot be averaged or aggregated.
- **“One global number is fair.”** Low-volume regions or tenants can disappear in traffic weighting.
- **“Every tenant needs a separate formal SLO.”** Detect cohorts, but promise only what can be operated and governed.
- **“Sampling is exact enough.”** Sparse severe events and confidence uncertainty may invalidate the conclusion.
- **“Current performance chooses the target.”** Targets express desired user/business trade-offs.
- **“100 percent is the safest target.”** It leaves no risk budget and encourages brittle behavior or measurement games.
- **“Overachievement is always good.”** Consumers may depend on it and costs may be unjustified.
- **“Budget is planned downtime.”** It is a risk-control mechanism, not a schedule to waste.
- **“Budget exhaustion always freezes releases.”** Response must preserve emergency repair and address actual causes.
- **“Burn rate equals budget remaining.”** One is current consumption velocity; the other is accumulated balance.
- **“Alert after the miss.”** Useful alerts predict material budget threat early enough for action.
- **“Every component alert should page.”** Page on urgent actionable user impact; use component signals for diagnosis/prediction.
- **“Provider SLA proves dependency fit.”** Scope, observation point, exclusions, topology, and correlation differ.
- **“Multiply component SLOs.”** Only under explicit required-edge and independence assumptions.
- **“Dependency failures do not count.”** Users experience the platform promise regardless of attribution.
- **“Planned maintenance never counts.”** It counts unless the service contract truly excludes that window.
- **“Changing the query fixes the SLO.”** It may rewrite history; use versioned prospective changes and corrections.
- **“A dashboard is an SLO.”** Objective, ownership, policy, and decisions are required.
- **“More SLOs improve reliability.”** Too many dilute attention and create contradictory incentives.

## Worked Examples

### Example 1

An environment-vending SLO begins after authorization and complete request validation. Good means account/project, network baseline, identity, budgets, audit, ownership, and usable credentials reach ready state within 30 minutes. A cloud API success without network convergence is bad. Requests denied by correct quota policy are measured under policy decision SLO, not provisioning completion.

### Example 2

A developer portal serves pages at 99.99 percent while deployments fail because workflow credentials expired. The platform replaces “portal uptime” as its primary objective with deploy and rollback journeys. Portal latency stays diagnostic. The new objective changes roadmap priority toward workflow identity and recovery rather than adding portal replicas.

### Example 3

A 99.9 percent API receives one million valid requests in 28 days, allowing 1,000 bad. During one hour, 2 percent of 10,000 requests fail: 200 bad and burn rate 20. The hour consumed 20 percent of the whole event budget. A fast-burn page is justified even though rolling compliance has not yet crossed 99.9 percent.

### Example 4

A low-volume disaster-restore workflow runs twice per quarter. A percentage SLO is unhelpful. The platform performs weekly synthetic restore of representative encrypted backups, verifies integrity and recovery objectives, and requires every real invocation to complete within its declared RTO/RPO. Results are reported as test coverage and maximum failures, not three decimal nines.

### Example 5

Global deployment success is 99.7 percent against 99.5, but one region is 91 percent and carries two percent of traffic. Region segmentation triggers an incident despite global compliance. The platform also reports tenant breadth so a few large tenants do not hide many small affected teams.

### Example 6

An SLI originally counts each controller retry. An outage creates ten retries for each failed user deployment, making the denominator and error count explode. The corrected event model deduplicates by accepted workflow ID, records retry count diagnostically, and declares a deploy good only when its exact revision reaches terminal healthy state by deadline.

### Example 7

The metrics pipeline partitions during a platform outage, so failed edge requests lack status labels. Reconciliation compares ingress counts, workflow starts, terminal records, and audit IDs. Missing outcomes enter `unknown`; the report shows worst/best bounds and blocks risky releases until coverage recovers. It never reports 100 percent from the surviving successes.

### Example 8

A workflow depends serially on identity and cloud provisioning, both advertising 99.9 percent. Their outages share a regional control-plane dependency, so multiplication is invalid. The platform measures end-to-end completion, tests regional failure, caches identity where safe, and allocates stricter internal dependency expectations with a degraded recovery path.

### Example 9

A team proposes changing latency instrumentation from milliseconds to seconds and route labels to templates. SLO-as-code tests units, label cardinality, histogram boundaries, timeout inclusion, and historical dual-query parity. The change takes effect at the next window boundary with old/new reports attached rather than silently changing current compliance.

### Example 10

A platform migrates from 140 component alerts. User research selects provisioning, build, deploy, status, rollback, and credential journeys. It runs new SLIs in shadow, validates incidents and telemetry loss, adopts multi-window pages, demotes component symptoms to diagnostic alerts, and writes error-budget policy. Page volume falls only after recall for material user incidents is verified.

## Cross-Program Connections

1. **Product management:** journey discovery, expectations, segmentation, and outcome decisions prevent metric-first objectives.
2. **Probability and statistics:** ratios, distributions, bounds, sampling, percentiles, and correlated failures determine validity.
3. **Distributed systems:** async state machines, retries, deadlines, queues, convergence, and partial failure shape event populations.
4. **Observability engineering:** metrics, traces, logs, events, histograms, cardinality, and pipeline coverage implement SLIs.
5. **Site reliability engineering:** error budgets, burn alerts, incident response, capacity, and change policy turn measurements into control loops.
6. **Software architecture:** dependency topology, isolation, fallback, caching, and degradation determine achievable reliability.
7. **Security engineering:** correct denial, identity, policy, audit, and fail behavior are user-visible reliability properties.
8. **Data engineering:** event deduplication, late data, watermarks, schema evolution, and reproducible queries protect SLO evidence.
9. **Economics:** higher targets trade engineering, capacity, opportunity, and dependency cost against user harm.
10. **Organizational design:** provider/consumer ownership and decision rights decide whether error budgets change real work.

## References

1. Google. [Site Reliability Engineering: Service Level Objectives](https://sre.google/sre-book/service-level-objectives/). Retrieved 2026-09-02.
2. Google. [The Site Reliability Workbook: Implementing SLOs](https://sre.google/workbook/implementing-slos/). Retrieved 2026-09-02.
3. Google. [The Site Reliability Workbook: Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/). Retrieved 2026-09-02.
4. Google. [The Site Reliability Workbook: Example Error Budget Policy](https://sre.google/workbook/error-budget-policy/). Retrieved 2026-09-02.
5. Google. [Site Reliability Engineering: Embracing Risk](https://sre.google/sre-book/embracing-risk/). Retrieved 2026-09-02.
6. OpenSLO. [OpenSLO Specification](https://github.com/OpenSLO/OpenSLO). Retrieved 2026-09-02.
7. Prometheus. [Histograms and Summaries](https://prometheus.io/docs/practices/histograms/). Retrieved 2026-09-02.
8. Prometheus. [Alerting Rules](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/). Retrieved 2026-09-02.
9. OpenTelemetry. [Semantic Conventions for HTTP Metrics](https://opentelemetry.io/docs/specs/semconv/http/http-metrics/). Retrieved 2026-09-02.
10. Google Cloud. [Concepts in Service Monitoring](https://cloud.google.com/stackdriver/docs/solutions/slo-monitoring). Retrieved 2026-09-02.
11. Cloud Native Computing Foundation TAG App Delivery. [CNCF Platforms White Paper](https://tag-app-delivery.cncf.io/whitepapers/platforms/). Retrieved 2026-09-02.
12. DORA. [Monitoring Systems](https://dora.dev/capabilities/monitoring-systems/). Retrieved 2026-09-02.
13. Kubernetes. [Metrics for Kubernetes System Components](https://kubernetes.io/docs/concepts/cluster-administration/system-metrics/). Retrieved 2026-09-02.
14. Internet Engineering Task Force. [RFC 9333: Quality of Outcome](https://www.rfc-editor.org/rfc/rfc9333). Retrieved 2026-09-02.

## Exercises

### Exercise 1

Define SLOs for platform environment provisioning, production deployment, rollback, policy decision, and service-status visibility. Specify event models, targets, windows, exclusions, unknowns, and owners.

### Exercise 2

For a 99.9 percent request SLO over 28 days, derive error budget, burn rate, and approximate exhaustion time for several traffic/failure windows. Design page and ticket alerts.

### Exercise 3

Design a measurement-integrity strategy for an asynchronous workflow whose telemetry can fail with the platform and whose users retry aggressively.

### Exercise 4

Evaluate an end-to-end journey with identity, registry, workflow, Kubernetes, and cloud dependencies. Explain why provider SLO multiplication may fail and allocate reliability work.

### Exercise 5

Plan migration from component uptime dashboards and threshold alerts to governed platform journey SLOs without losing incident detection.

## Answers to the Exercises

### Answer 1

Provisioning counts one authorized complete request at durable acceptance; good requires exact tenant/account, network, identity, budget, audit, ownership, credentials, and ready state within 30 minutes. Deployment counts accepted workflow ID; good requires exact digest, target, rollout health, visible terminal state within 15 minutes. Rollback starts at authorized request and ends when prior/current approved digest is healthy and traffic restored within the incident need.

Policy decision counts every valid evaluation; correct allow/deny under pinned policy/data and response under 500 ms are good, while expected denials remain good. Status visibility samples owned active workflows/resources and is good when authoritative state and age meet contract.

Choose targets from user consequence and architecture, perhaps 99.5 percent over rolling 28 days for provisioning/deploy, stricter policy availability/latency, and explicit restore targets. Exclude only malformed pre-acceptance input and published unsupported scopes. Mark missing correlations unknown, publish bounds and coverage. Platform product/operations own delivered journeys; policy owns rule correctness; consumers own valid inputs and workload health.

### Answer 2

At one million valid requests, $e=0.001$ permits 1,000 bad. A subwindow with 100,000 requests and 500 bad has error rate 0.005 and burn 5. At constant burn 5, a fresh 28-day budget exhausts in about 5.6 days. A window with 10,000 requests and 200 bad burns at 20 and consumes 20 percent of the full event budget.

Use paired long/short windows. Page when both show current high burn that can consume a material budget fraction within response time; use slower pairs for daytime tickets. Exact thresholds follow desired detection time, page precision, traffic, and incident response, and must be backtested. Alert on coverage loss independently because a missing denominator can suppress burn.

Report accumulated budget remaining separately. The same burn has different urgency when little budget remains or traffic changes; request budgets can exhaust faster under peak traffic.

### Answer 3

Define one user intent by idempotency/workflow ID and state machine from edge acceptance through queue, controller attempts, resource UID/generation, terminal outcome, and deadline. Count retries diagnostically rather than as new valid events unless the user creates a new intent.

Emit durable edge accepted count, queue IDs/offsets, workflow transitions, controller attempts, audit records, and terminal observations. Reconcile unique IDs and sequence/checkpoints; retain late events, duplicates, unmatched starts/terminals, collector drops, schema rejects, and disabled intervals. Use edge and independent black-box canaries so telemetry silence is not success.

Treat unknown outcome conservatively for risky change decisions and publish best/worst bounds plus coverage SLO. Fault-test simultaneous service/telemetry partitions, queue backlog, restart, counter reset, clock skew, and index rebuild. Independently recompute period results from raw workflow and audit evidence.

### Answer 4

Map required and optional edges, retries, fallback, caches, regions, quotas, and shared failure domains. Provider objectives may cover different APIs, traffic, locations, maintenance, or observation points. Identity and cloud may share regional network/control-plane failure; workflow retry changes edge success; cached registry data may remove a synchronous edge. Independence and simple serial topology are therefore unproven.

Measure the journey at the user boundary and each actual dependency edge with method, region, deadline, and outcome. Assign stricter dependency expectations where necessary, leaving budget for platform code. Improve weakest dominant paths using isolation, capacity, fallback, caching, degradation, or provider negotiation.

Dependency-caused failures remain bad for the promised platform journey. Attribution guides remediation and commercial action, not denominator exclusion. Fault injection and historical traces estimate correlation and validate fallback.

### Answer 5

Inventory alerts, incidents, pages, users, journeys, dependencies, and decisions. Select a few consequential journeys. Define state machines and good/valid/unknown contracts, implement correlation and reconciled event/metric sources, and run shadow calculations beside existing monitoring.

Replay known good and incident periods; inject timeout, wrong outcome, denial, retry, cancellation, dependency and telemetry-loss cases. Backtest targets and multi-window alerts for precision, recall, detection/clear time, and actionability. Retain component metrics and alerts as diagnostics until journey alerts demonstrate incident coverage.

Write ownership and error-budget policy, version definitions/queries/alerts as code, publish dashboards and runbooks, then progressively route pages. Demote noisy component symptoms rather than deleting diagnostic visibility. Review missed incidents, user reports, low-volume and regional cohorts, measurement gaps, page volume, and decision outcomes before expanding the portfolio.
