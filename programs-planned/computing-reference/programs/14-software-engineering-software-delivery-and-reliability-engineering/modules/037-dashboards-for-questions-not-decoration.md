---
module_id: SDRE-037
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 37
title: Dashboards for Questions, Not Decoration
status: complete
last_verified: 2026-09-06
---

# Dashboards for Questions, Not Decoration

## One-Page Review

### Governing question

How can an operational dashboard turn telemetry into a reproducible answer to a named question and decision while preserving population, time, units, freshness, missingness, uncertainty, and drill-down evidence?

### Essential definitions

- a **dashboard** is a governed set of views for a named audience, question, and decision;
- a **panel** binds a query, transformation, visual encoding, scope, time window, and explanatory contract;
- a **population** is the exact set of observations represented by a value;
- a **filter** restricts observations; a **grouping** partitions them;
- a **time window** selects event intervals; a **step** or **resolution** controls evaluated points;
- **freshness** is age since the evidence was sampled or successfully evaluated;
- **coverage** is the proportion of expected observations with valid evidence under a stated model;
- **missingness** is absence of a value, distinct from a measured zero;
- a **baseline** or **reference** is the comparison used to interpret current value;
- a **drill-down** preserves scope and time while moving toward more detailed evidence;
- a **visual encoding** maps values to position, length, color, area, or other marks;
- a **dashboard contract** records owner, purpose, variables, queries, units, thresholds, dependencies, and failure behavior.

### Central model, mechanism, or theorem

Treat a displayed value as a function

$$
V=Q(D,P,W,t,r,m),
$$

where $D$ is the data source, $P$ population and filters, $W$ event-time window, $t$ evaluation time, $r$ resolution, and $m$ missing-data policy. Two panels are comparable only when differences in these inputs are intentional and visible.

For last valid sample time $t_s$, evidence age is $a=t-t_s$. If policy requires $a\le F$, an older value is stale and must not be rendered as current. For controlled expected points $E$ and valid observed points $O$, coverage is $C=|E\cap O|/|E|$ when $|E|>0$.

### Critical invariants

- every dashboard names its audience, governing question, decision, and owner;
- panel title, description, query, unit, scope, window, and visual encoding agree;
- numerator and denominator describe compatible populations;
- missing, stale, partial, delayed, and zero remain distinguishable;
- time zone, evaluation time, event window, resolution, and refresh behavior are visible;
- thresholds come from policy or evidence, not attractive colors;
- comparisons use like-for-like populations or disclose differences;
- variables cannot silently broaden tenant, environment, or production scope;
- annotations link to canonical change evidence;
- drill-down retains the originating time and scope unless the user changes them explicitly.

### Common failures

Failures include building panels before defining questions, displaying every available metric, mixing units on an unlabeled axis, truncating axes to exaggerate noise, hiding small cohorts in global aggregates, averaging percentages or quantiles incorrectly, carrying stale gauges forward, treating no data as zero, changing variable defaults silently, using red and green as the only distinction, stacking unrelated series, showing candidate and control with different windows, losing incident time on drill-down, and keeping ownerless copied dashboards after their queries have drifted.

### Compact example

An incident dashboard asks, “Which user population is failing, since which change, and where should the responder look next?” Its overview shows traffic, error ratio, and latency distribution for one explicit service, environment, region, release, and time range. Every panel displays query age and coverage. Candidate and control share windows and denominators. Change annotations link to event IDs. Clicking a region preserves time and release filters while opening dependency metrics, correlated traces, and structured logs. Missing evidence is a visible state, not a flat green line.

### Connections

[SDRE-031](031-observability-versus-monitoring.md) supplies questions and hypotheses; [SDRE-033](033-metrics-and-dimensionality.md) supplies aggregation semantics; [SDRE-035](035-events-and-change-annotations.md) supplies changes. [SDRE-038](../ROADMAP.md) next separates actionable alerts from passive views.

## Governing Question

A dashboard is often mistaken for a wall of charts. A chart can be technically correct yet operationally useless: it may answer no decision, omit scope, obscure missing data, or invite the viewer to infer causality from co-occurrence. More panels increase search space and query load. Decoration creates confidence without reducing uncertainty.

Start from an audience in a situation. A service owner reviewing a rollout, an on-call responder locating user harm, and a capacity planner selecting next quarter's headroom need different windows, comparisons, and detail. A dashboard may support several closely related questions, but a universal dashboard usually hides assumptions behind variables and scroll depth.

The governing question therefore joins semantics and human use: what decision will this view support, what evidence would change that decision, and can a tired operator determine scope, currency, and limitations without reverse-engineering queries?

## Why This Matters

Dashboards sit between measurement and action. A wrong denominator can approve a harmful release; a stale green panel can delay response; a global average can hide one failed region. Unlike a saved query, a dashboard repeatedly presents an interpretation and often becomes organizational memory.

Google SRE monitoring guidance recommends a small set of user-relevant signals such as latency, traffic, errors, and saturation and distinguishes symptoms from causes [1]. The SRE Workbook emphasizes monitoring built from explicit objectives and operational use [2]. These are starting structures, not universal panel quotas.

Current Grafana guidance says dashboards should answer a question, reduce cognitive load, compare like with like, support hierarchical drill-down, avoid unnecessary refresh, document panels, and govern dashboard sprawl [3]. Those recommendations are product documentation, so this chapter extracts durable principles rather than prescribing a vendor workflow.

Prometheus documents how selectors, evaluation timestamps, ranges, rates, absent series, and histogram functions affect query results [4, 5]. A dashboard tool cannot repair an incoherent query. OpenTelemetry's stable metrics data model reinforces that stream identity, temporality, units, and aggregation are part of meaning [6].

Operational views must also be perceivable. WCAG 2.2 provides current accessibility criteria for contrast, non-color cues, keyboard operation, text alternatives, reflow, and understandable interaction [7]. RFC 3339 gives an interoperable timestamp profile but does not remove time-zone, clock, or leap-second limitations [8].

## Prerequisites and Retrieval

Retrieve measurement, metric stream, counter, gauge, histogram, rate, ratio, quantile, population, sample, event time, evaluation time, window, resolution, interpolation, missing value, stale value, variable, threshold, baseline, cohort, annotation, correlation, accessibility, incident, and runbook.

From SDRE-031 retrieve question-first evidence and black-box versus white-box signals. From SDRE-033 retrieve valid aggregation, staleness, histogram error, and bounded dimensions. From SDRE-034 retrieve individual-operation drill-down. From SDRE-035 retrieve canonical change events and uncertainty.

## Learning Objectives

After completing this module, you should be able to:

1. write a dashboard contract from audience, question, and decision;
2. specify panel population, query, window, resolution, unit, and missingness;
3. choose visual encodings that fit the comparison;
4. distinguish current, stale, delayed, partial, missing, and zero evidence;
5. compare releases, regions, cohorts, and baselines without denominator errors;
6. design overview-to-detail navigation that preserves context;
7. use change annotations without causal overclaim;
8. make views accessible beyond color and mouse interaction;
9. test query semantics, rendering, variables, permissions, and degraded data;
10. version, own, review, and retire dashboards as production code.

## Core Exposition

**Write the contract first.** State the audience, situation, governing question, decision, evidence required, maximum acceptable evidence age, expected update frequency, owner, and escalation path. A rollout view might ask whether candidate users have worse error or latency outcomes than comparable control users. Its decision is continue, pause, roll back, or investigate—not “observe the system.”

List hypotheses the dashboard should distinguish. If error rises, is harm global, regional, release-specific, dependency-specific, or a telemetry gap? Each panel should eliminate or strengthen a hypothesis. A panel with no named use is a cost and maintenance liability.

Separate an operational overview from exploratory analysis. The overview must remain stable under pressure. Exploration needs flexible querying and may tolerate temporary views. Do not preserve every exploratory graph as a permanent dashboard.

**Specify each panel as a semantic unit.** Record source, exact query or governed query reference, population, filters, grouping, unit, aggregation, window, evaluation time, resolution, freshness threshold, missing-data policy, visual encoding, thresholds, annotations, links, and known limitations.

Title the claim rather than the raw metric: “checkout unsuccessful requests by release” is more useful than `requests_total`. A description should explain numerator and denominator, excluded traffic, window, and what no data means. Units belong in labels and values. Do not place seconds and bytes on one unlabeled axis.

Stable query identifiers and version control enable review. A dashboard definition without the recording rules it depends on is incomplete, so link metric owners and schema versions. Record backend assumptions where query languages interpret resets, staleness, or histograms differently.

**Preserve population.** Filters define who and what is counted. A success ratio needs successes and total eligible attempts over the same client/server boundary, interval, route, release, and exclusion rules. If control excludes retries but candidate includes attempts, the comparison is invalid even when both lines are percentages.

Global aggregates can hide harmed minorities. Pair an overall decision view with bounded partitions for region, release, tier, or operation when those distinctions are actionable. Do not render hundreds of series simultaneously; rank, filter, summarize, and provide drill-down while retaining a clear “other” or coverage account.

Variables change the query contract. Display selected environment, region, release, and tenant scope in the title or persistent header. Safe defaults should not silently switch from staging to all production. URL-shared views should preserve variables and time but must not bypass access control. Current Grafana documentation supports parameterized reuse and directed navigation [3].

**Make time explicit.** Distinguish event-time window from dashboard evaluation time. “Last hour” at 14:00 is not reproducible at 16:00 unless the original absolute range is preserved. Incident links should use absolute start and end. Display time zone and avoid ambiguous local timestamps around daylight-saving changes.

Resolution changes what is visible. An average over five minutes can hide a ten-second outage. A maximum can expose the peak but exaggerate one bad sample. A total depends on bucket coverage. Choose resolution from decision latency, event frequency, query capacity, and aliasing risk. Where downsampling occurs, disclose the function.

Refresh faster only when new evidence exists and the backend can support it. A 5-second refresh over hourly data creates load and visual motion without information. Show query completion and data timestamp separately; a newly rendered stale sample is still stale.

**Keep missingness visible.** No data may mean no traffic, failed discovery, scrape loss, exporter rejection, query error, permission denial, incompatible labels, expired retention, or an actually absent target. Zero means a producer observed a zero under its measurement procedure. Connecting across gaps or filling zero is a modeling decision, not display polish.

For last valid sample $t_s$, compute age $a=t-t_s$. If $a>F$, mark stale and remove current-state coloring. When an expected series set is known, display coverage. When it is not known, show collection health and scope inventory instead of inventing a percentage.

The deterministic model below shows how missingness, freshness, mean, and maximum answer different questions. It is not a query engine or production freshness guarantee.

<!-- bijux-verify: {"id":"panel-evidence-state","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"coverage: 75.0%\nobserved mean: 4.0\nobserved maximum: 8\nevidence age: 120 s\nstale: True\n","stderr":""}} -->
```python
points = [(0, 4), (60, None), (120, 0), (180, 8)]
evaluation_time = 300
freshness_limit = 90
known = [(time, value) for time, value in points if value is not None]
coverage = len(known) / len(points)
values = [value for time, value in known]
age = evaluation_time - known[-1][0]

print(f"coverage: {coverage:.1%}")
print(f"observed mean: {sum(values) / len(values):.1f}")
print("observed maximum:", max(values))
print("evidence age:", age, "s")
print("stale:", age > freshness_limit)
```

The mean is $(4+0+8)/3=4$, not $(4+0+0+8)/4=3$; filling missing with zero changes the estimand. The maximum 8 answers a different question. Despite successful rendering at $t=300$, the last evidence is 120 seconds old and stale under a 90-second policy.

**Choose visual encoding from the task.** Position on a shared scale supports precise comparison. Lines suit ordered time, bars suit category magnitude, distributions suit latency shape, tables suit exact mixed fields, and state timelines suit transitions. Gauges consume space and often hide history; use them only when a current value against a meaningful range is the decision.

Use zero baselines for bar-length comparisons unless a clearly marked alternative is necessary. A truncated line axis can reveal small variation, but label the range and pair it with policy context. Dual axes can manufacture apparent correlation; prefer aligned separate panels or normalized values, and never imply causal relation from similar shapes.

Stacking is valid when parts form a meaningful whole with compatible units. It makes interior series hard to compare and can hide an unchanged total with shifting composition. Pie area and decorative three-dimensional effects impair comparison. Limit simultaneous colors and use line styles, markers, labels, or patterns so meaning survives color-vision differences and monochrome rendering.

Threshold colors require a policy: SLO, capacity limit, error budget, safe operating range, or statistically justified baseline. Red is not a threshold definition. Show threshold value and provenance. Unknown must not inherit green because no condition evaluated.

**Build overview, comparison, then diagnosis.** The first screen should establish user impact, traffic context, freshness, and major scope. The second layer partitions by release, region, operation, or dependency. The third links to traces, logs, changes, and runbooks. This is directed investigation, not a forced story.

Preserve variables and absolute time through drill-down. A link from candidate region A to logs that defaults to all regions and the current 15 minutes changes the question. Encode safe filters, show them at destination, and provide a reset. Permission failures should produce an explicit unavailable state rather than an empty graph.

Change annotations come from canonical events, not manually copied labels. Render actual exposure windows and uncertainty when available. A nearby change is a candidate cause; pair it with candidate/control evidence and links to mechanisms. Avoid hundreds of low-value annotations that obscure the signal.

**Design for incident cognition and accessibility.** Put user impact and action-relevant context above implementation detail. Use consistent units, order, vocabulary, and colors across services. Include concise descriptions and direct runbook/owner links. Avoid scrolling past decorative fleet maps before reaching evidence.

Do not rely on color alone. Provide text state, icons with labels, line patterns, and adequate contrast. Ensure keyboard navigation, logical focus order, readable zoom/reflow, and text alternatives or tables for essential chart values, guided by WCAG 2.2 [7]. Test in dark and light themes and under common color-vision simulations.

**Test dashboards as software.** Parse and lint definitions. Validate queries against fixtures containing resets, zero traffic, missing data, stale data, partial labels, schema migration, and extreme values. Assert units, legends, thresholds, variables, default scope, permissions, links, time preservation, and annotation identity.

Snapshot or render tests catch empty panels, overlap, unreadable legends, and theme regressions but do not prove semantics. Review a panel's query and measurement contract independently. Exercise the dashboard during a game day with a question and record whether users reached the right evidence.

Measure query latency, errors, scanned series, refresh load, and panel timeout. A dashboard that overloads telemetry during an incident is unsafe. Precompute justified aggregates, cap variable fan-out, stagger refresh, and degrade with explicit partial states.

**Govern lifecycle.** Give every dashboard an owner, version, review date, intended audience, dependencies, and retirement condition. Review after schema, service, SLO, ownership, or incident changes. Usage is evidence but not the only criterion; rarely opened disaster-recovery views may still be essential.

Use reusable components where semantics truly match, but do not force different services into one misleading query. Delete superseded copies and redirect durable links. Preserve incident snapshots or query parameters when needed for later analysis rather than relying on a mutable dashboard's current definition.

## Definitions and Notation

Let $D$ identify source data, $P$ the selected population, $W=[u,v)$ the event-time window, $t$ evaluation time, $r$ resolution, and $m$ missing-data policy. A displayed value is $V=Q(D,P,W,t,r,m)$. Comparability requires compatible units, measurement boundaries, populations, and transformations.

For expected observation identities $E$ and valid observed identities $O$, controlled coverage is $C=|E\cap O|/|E|$ when $|E|>0$. Coverage is not availability of the service; it is evidence availability under the expectation model.

For last valid sample time $t_s$, age is $a=t-t_s$. A panel is fresh under threshold $F\ge0$ if $a\le F$. Query completion time is not $t_s$.

For groups with successes $s_i$ and totals $n_i>0$, aggregate success is $\sum_i s_i/\sum_i n_i$. An unweighted average of $s_i/n_i$ represents an equal-group estimand. Panel documentation must identify which question is intended.

## Mechanisms, Invariants, or Proof Structure

**Panel-function argument.** Changing source, population, window, evaluation time, resolution, or missingness can change $V$ while title remains identical. Therefore visible metadata is required to make the displayed claim reproducible.

**Missing-value counterexample.** Observed values 4, 0, and 8 average to 4. Treating one missing point as zero changes the mean to 3. Because both renderings can arise from the same evidence plus different policy, gap filling is a semantic transformation.

**Freshness argument.** A query at time 300 returning a last sample at 180 has age 120. If $F=90$, successful query execution cannot make the evidence current. Render and sample times are distinct.

**Aggregation argument.** Ratio of sums weights by exposure. Mean of group ratios weights groups equally. They coincide only under special relationships such as equal denominators, so a panel cannot label both “overall success.”

**Comparison condition.** Candidate and control trends support a release comparison only when measurement boundary, eligibility, time, units, and relevant confounders are compatible. Similar lines do not prove exchangeability or causality.

**Visual non-identification.** The same apparent slope can be produced by axis range, aggregation step, interpolation, population mix, or underlying values. A visual shape without query semantics does not uniquely identify system behavior.

## Alternatives and Trade-Offs

1. **Purpose-built versus universal dashboard.** Purpose-built views reduce ambiguity; universal variables reduce duplication but hide state.
2. **Live relative versus fixed absolute time.** Relative time supports ongoing operations; absolute time makes incident views reproducible.
3. **Aggregate versus partition.** Aggregate shows overall impact; partitions reveal harmed minorities at cognitive and query cost.
4. **Line versus distribution.** Lines show evolution; distributions preserve shape but are harder to scan quickly.
5. **Automatic versus fixed axes.** Automatic ranges reveal variation but impede comparison; fixed ranges support policy context but can flatten small changes.
6. **Gap versus interpolation.** Gaps preserve unknown evidence; interpolation aids trend reading only under justified continuity assumptions.
7. **Template reuse versus specialized panels.** Reuse improves consistency; specialization preserves service-specific meaning.
8. **Fresh queries versus recording rules.** Fresh queries preserve flexibility; precomputation lowers incident load but fixes transformations early.
9. **Dense overview versus hierarchical drill-down.** Density reduces clicks; hierarchy reduces cognitive load and preserves directed investigation.

## Failure Modes and Misconceptions

1. **“More panels mean more observability.”** Unfocused views increase search and maintenance.
2. **“The title defines the query.”** Hidden filters and transformations define the actual value.
3. **“No data is zero.”** Missing evidence has several mechanisms.
4. **“A fresh render is fresh data.”** Sample age can remain stale.
5. **“An average describes the tail.”** Distribution shape can differ radically.
6. **“Percentages compare automatically.”** Denominators and populations may differ.
7. **“Global health protects every cohort.”** small harmed populations can disappear in aggregates.
8. **“Two aligned lines are causally related.”** scale, aggregation, and common causes can align them.
9. **“Green means safe.”** Color needs policy and unknown-state handling.
10. **“Dual axes reveal correlation.”** independent scales can manufacture similarity.
11. **“Variables only improve reuse.”** hidden defaults can broaden scope dangerously.
12. **“Relative time links preserve incidents.”** the range moves as time passes.
13. **“Annotations prove what caused a symptom.”** they identify candidate changes.
14. **“Rendering tests prove correctness.”** a beautiful wrong query still passes.
15. **“Color is enough.”** accessibility and monochrome use require redundant cues.
16. **“Dashboards never harm production.”** expensive refresh and fan-out can overload telemetry.

## Worked Examples

### Example 1

**Question-first design.** “Is checkout healthy?” is narrowed to “Are eligible production users completing checkout within the latency objective over the last 30 minutes?” Panels now need traffic, success denominator, latency distribution, scope, and freshness. **Conclusion:** a precise question determines evidence.

### Example 2

**Missing versus zero.** Points are 4, missing, 0, and 8. Valid-value mean is 4 with 75% coverage; zero-filling gives 3. **Conclusion:** the dashboard must show the gap and policy.

### Example 3

**Stale green panel.** Last success value is 100% at 10:00; collector fails; dashboard renders it at 10:20. With $F=5$ minutes, age is 20 minutes and state is unknown/stale, not green. **Conclusion:** freshness gates state coloring.

### Example 4

**Unequal denominators.** Region A has 999/1,000 successes and B 90/100. Global success is 1,089/1,100=99%; equal-region mean is 94.95%. **Conclusion:** label overall and fairness views separately.

### Example 5

**Resolution aliasing.** Ten-second values 0, 0, 100, 0, 0, 0 average to 16.7 over one minute. A capacity limit of 80 was breached despite a low mean. **Conclusion:** resolution and summary function follow the decision.

### Example 6

**Truncated axis.** Latency moves from 100 to 102 ms. An axis 99–103 fills half the plot with the change; a 0–500 policy axis makes it small. Both are numerically valid. **Conclusion:** show axis and policy reference so scale cannot impersonate importance.

### Example 7

**Global masking.** Candidate harms a 1% cohort completely while 99% remain healthy. Overall success can stay near 99%. A bounded cohort panel exposes the loss and traffic count. **Conclusion:** retain actionable partitions.

### Example 8

**Broken drill-down.** An alert opens a dashboard at region A, release 43, 12:00–12:30. The logs link opens all regions at current time. Preserving absolute time and filters locates the failure. **Conclusion:** navigation is part of correctness.

### Example 9

**Change collision.** A deploy and traffic shift appear beside rising errors. Candidate/control panels, region scope, dependency traces, and event links keep both hypotheses visible. **Conclusion:** annotations guide investigation without selecting cause.

### Example 10

**Telemetry overload.** A dashboard expands 500 services by 50 regions with 10-second refresh during an incident. Query latency and backend saturation rise. Limit variables, precompute justified aggregates, and show partial results. **Conclusion:** dashboard cost is a reliability concern.

## Cross-Program Connections

1. [SDRE-031](031-observability-versus-monitoring.md) defines the questions and evidence limits.
2. [SDRE-033](033-metrics-and-dimensionality.md) owns metric types, populations, and aggregation.
3. [SDRE-034](034-distributed-tracing.md) provides individual-operation drill-down.
4. [SDRE-035](035-events-and-change-annotations.md) provides canonical change evidence.
5. Data Engineering owns source pipelines and late-data transformations.
6. Database Engineering owns query plans, indexes, and storage behavior.
7. Statistics and Data Science owns stronger inference and uncertainty methods.
8. Human-computer interaction owns perceptual and interaction research beyond this operational treatment.
9. Platform Engineering owns reusable dashboard components and access integration.
10. Security Engineering owns tenant isolation and authorization for shared views.

## References

1. Google, “Monitoring Distributed Systems,” *Site Reliability Engineering*, retrieved 2026-09-06. https://sre.google/sre-book/monitoring-distributed-systems/
2. Google, “Monitoring,” *Site Reliability Engineering Workbook*, retrieved 2026-09-06. https://sre.google/workbook/monitoring/
3. Grafana Labs, “Grafana dashboard best practices,” current documentation retrieved 2026-09-06. https://grafana.com/docs/grafana/latest/visualizations/dashboards/build-dashboards/best-practices/
4. Prometheus Authors, “Querying basics,” current Prometheus documentation retrieved 2026-09-06. https://prometheus.io/docs/prometheus/latest/querying/basics/
5. Prometheus Authors, “Query functions,” current Prometheus documentation retrieved 2026-09-06. https://prometheus.io/docs/prometheus/latest/querying/functions/
6. OpenTelemetry, “Metrics Data Model,” OpenTelemetry Specification 1.60.0, Stable, retrieved 2026-09-06. https://opentelemetry.io/docs/specs/otel/metrics/data-model/
7. W3C, *Web Content Accessibility Guidelines (WCAG) 2.2*, Recommendation, 12 December 2024. https://www.w3.org/TR/WCAG22/
8. IETF, RFC 3339, “Date and Time on the Internet: Timestamps,” July 2002. https://www.rfc-editor.org/rfc/rfc3339

## Exercises

### Exercise 1

Define population, filter, grouping, window, resolution, freshness, coverage, missingness, and drill-down. Explain why a panel title is insufficient.

### Exercise 2

At evaluation time 900, expected sample times are 600, 660, 720, 780, and 840. Valid samples exist at 600, 720, and 840 with values 2, 0, and 7. Compute coverage, observed mean, age, and freshness for $F=45$ seconds.

### Exercise 3

A candidate dashboard is green even though traffic disappeared, logs show permission errors, and panels retain last values. Give a diagnosis and a corrected state model.

### Exercise 4

Design a rollout dashboard comparing candidate and control. Specify population, ratios, latency, windows, variables, changes, missingness, drill-down, and decision.

### Exercise 5

Design an accessible incident dashboard for an intermittently connected medical-device fleet with late data, regional cohorts, and strict query limits.

## Answers to the Exercises

### Answer 1

Population is the represented observations; filter restricts them; grouping partitions them. Window selects event time and resolution selects evaluated granularity. Freshness is evidence age under policy. Coverage is valid observed evidence relative to a controlled expectation. Missingness is absence rather than measured zero. Drill-down moves to detail while preserving context. A title does not reveal source, filters, denominator, transformation, evaluation time, gap policy, or unit, so different values can carry the same label.

### Answer 2

There are three valid of five expected points, so coverage is 60%. Observed mean is $(2+0+7)/3=3$. Last valid sample is 840; age at 900 is 60 seconds. Since $60>45$, evidence is stale. The missing points must not be zero-filled, and successful evaluation at 900 does not change sample age.

### Answer 3

The dashboard confuses no traffic or inaccessible evidence with success, hides query errors, and carries stale gauges as current. Separate states: valid value with nonzero traffic, valid zero-traffic population, missing source, permission denied, query error, partial coverage, delayed, and stale. Gate green status on sufficient current evidence and an applicable policy result. Display traffic and evidence age, break lines across gaps, expose permission/query errors, and test collector loss plus access denial fixtures.

### Answer 4

Define eligible production attempts and stable assignment to candidate/control using the same client or server boundary. Show traffic counts; unsuccessful/eligible ratio as ratio of sums; latency histograms with policy thresholds; region and operation partitions; and one absolute evaluation window plus a stated resolution. Variables display environment, region, release, and cohort and cannot silently default to all production. Canonical deployment windows link to event IDs. Missing, stale, low-count, and partial evidence block an automatic green state. Drill-down preserves time and scope into traces and logs. Predeclare continue, pause, rollback, and investigate criteria. Acceptable variants must retain comparable populations and disclose sampling or exclusions.

### Answer 5

Begin with fleet user-safety status by region, device generation, and software release. Show last-contact coverage, event-time age distribution, delayed-arrival count, successful operation ratio with denominator, and safety-relevant latency or failure distributions. Never connect gaps or treat offline as healthy zero. Use explicit delayed, stale, and unknown states with text and patterns in addition to color; provide keyboard navigation, contrast, and a table/text alternative. Use absolute incident time and event-time/observed-time distinction. Precompute bounded regional/release aggregates, cap device-level queries, and link authorized drill-down to sampled device traces or logs. Avoid raw device identifiers in shared panels. Evaluation should reward user-impact focus, late-data honesty, accessibility, privacy, and query degradation behavior.
