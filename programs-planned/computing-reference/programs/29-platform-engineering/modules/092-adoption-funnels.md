---
module_id: PLAT-092
program: Platform Engineering
level: 2
module_number: 92
title: Adoption Funnels
status: complete
last_verified: 2026-09-02
---

# Adoption Funnels

## One-Page Review

### Governing question

How should a platform team measure and improve the path from eligible user to sustained, outcome-producing platform use without treating page views, provisioned accounts, forced migration, or lock-in as evidence of product value?

### Essential definitions

- An **adoption funnel** is a cohort- and journey-specific sequence of observable states from eligibility through awareness, evaluation, first verified value, retained use, broader use, and safe exit.
- An **eligible population** contains teams or users for whom the capability fits declared technical, policy, lifecycle, and organizational constraints during a defined period.
- **awareness** means an eligible user encountered and understood the relevant proposition, not merely received a message.
- **evaluation** is a meaningful attempt to assess fit using documentation, a sandbox, consultation, prototype, or real workflow.
- **activation** or **first value** is the first accepted completion of the target outcome with required quality, safety, and independence—not account creation or button click.
- **retention** is repeated qualifying value in a declared later window among users who previously activated and remained eligible.
- **expansion** is additional qualifying journeys, services, or team members adopting after retained value; raw resource growth is not automatically expansion.
- **drop-off** is failure to reach a later state within its observation window; it can represent friction, ineligibility, changed need, deliberate exit, or missing instrumentation.
- A **cohort** groups entities by a stable entry event and relevant context such as voluntary/mandated status, segment, capability version, migration wave, or calendar period.
- A **guardrail metric** detects harm that an adoption intervention might create, including unsafe changes, incidents, support dependence, exclusion, cost transfer, and inability to exit.

### Central model, mechanism, or theorem

For journey $j$, cohort $c$, stage $k$, and observation window $W_k$, define a qualifying set

$$
S_{c,j,k}=\{u\mid Eligible(u,j,c)\land Qualifies(u,j,k,W_k)\}.
$$

For an ordered, closed funnel, $S_{k+1}\subseteq S_k$ and stage conversion is

$$
CR_k=\frac{|S_{k+1}|}{|S_k|},
$$

with raw counts, definitions, eligibility, cohort, window and censoring shown beside it. Open funnels and re-entry require explicit transition logic rather than this nesting assumption.

The objective is not to maximize conversion at any cost. Improve verified user and organizational outcomes subject to safety, reliability, security, cost, autonomy, accessibility and exit constraints.

### Critical invariants

- Every funnel names one user entity, one critical journey, eligibility rules, ordered stage semantics, identity rules, time windows, cohort dimensions and evidence revision.
- First value and retention require accepted outcome completion; retries, synthetics, duplicate events, provisioned resources and administrator actions are excluded or separately labeled.
- Voluntary discovery, mandated adoption, assisted migration and inherited use remain separate cohorts and are never blended into a market-like demand claim.
- Stage numerators and denominators align by entity, journey, cohort, eligibility, version and window; late arrivals and right censoring are explicit.
- Funnel optimization is paired with outcome and guardrail evidence, including failure, recovery, support, toil, security, reliability, cost and safe exit.
- Events are purpose-limited, privacy-preserving, traceable and correctable; no individual performance surveillance or dark-pattern adoption mechanism is permitted.

### Common failures

Using all employees as denominator; equating access with awareness; defining activation as portal login; counting retries as users; mixing teams and people between stages; blending voluntary and mandatory cohorts; measuring retention before enough time passes; ignoring teams that became ineligible; hiding support-assisted completion; treating resource count as value; rewarding lock-in; optimizing email clicks instead of journeys; averaging segments with opposite outcomes; changing event semantics silently; collecting identifiable developer telemetry for performance management; and celebrating conversion while reliability or cognitive load worsens.

### Compact example

A deployment capability has twelve eligible teams in a monthly voluntary cohort. Eleven encounter a proposition tied to their release journey, nine evaluate it, eight complete one policy-conformant production deployment without platform intervention, six repeat that outcome in the next 30-day window, and four extend it to a second service. The team reports counts and stage definitions, not “67% adoption.” Interviews and path evidence show the largest drop between evaluation and first value comes from opaque identity and policy errors. A redesigned preview explains missing evidence before execution. The next cohort improves first-value completion, while failed-change rate, support interventions, lead-time tails, accessibility, opt-out and service reliability remain within gates. Mandated migrations are reported separately and are evaluated through outcome parity, retention after the mandate, and exit safety.

### Connections

Adoption funnels operationalize the discovery evidence of PLAT-091 and use platform SLOs, dependency identities, incident evidence, cost allocation and blast-radius controls from PLAT-081–090. They provide cohort evidence for migration, support, roadmaps, lifecycle, outcomes, strategy defense, autonomy and monopoly review in PLAT-093–100.

## Governing Question

For a named platform journey and eligible cohort, where do users move from awareness to independently repeated value, where and why do they stop, and do interventions improve outcomes without coercion or transferred harm?

A funnel is a measurement model, not a universal product truth. Developer journeys branch, repeat, pause, move through APIs and human support, or intentionally exit. The team chooses a useful state model and must publish its limitations.

Internal adoption is especially easy to misread. A policy can create 100% account provisioning overnight while producing no value. Conversely, a small capability used by every relevant high-risk service may have complete adoption despite low organization-wide reach.

## Why This Matters

Aggregate use hides actionable transitions. “Forty teams use the platform” does not say how many were eligible, tried, succeeded, returned independently, expanded, or were forced to migrate.

Weak adoption metrics distort incentives. If portal visits are rewarded, teams build portals; if resource count is rewarded, abandoned resources accumulate; if percentage migrated is rewarded, coercion outruns readiness.

Correct funnels connect product learning with operational evidence. They locate friction, distinguish demand from support dependence, reveal segment exclusion, and show whether first success becomes durable behavior.

Funnel discipline also protects trust. Developers should know what journey telemetry exists, why it is collected, how long it is retained, and that it will not become individual productivity surveillance.

## Prerequisites and Retrieval

Retrieve platform strategy, target journeys, user/segment inventory, eligibility and exception policy, discovery findings, service catalog and ownership, identity model, interface events, audit logs, support/ticket records, documentation analytics, capability versions, migration waves, mandates, satisfaction research, delivery/reliability/security outcomes, cost and toil evidence, privacy assessment, retention policy, and prior metric definitions.

Distinguish eligible from reachable; account from user; awareness from message delivery; evaluation from curiosity; first use from first value; task completion from accepted outcome; team from person and service; voluntary adoption from mandate; migration from retention; return visit from repeated value; expansion from resource sprawl; abandonment from ineligibility; friction from deliberate choice; conversion from causation; closed from open funnel; event time from processing time; current absence from right-censored outcome; and healthy retention from lock-in.

## Learning Objectives

After completing this module, you should be able to:

1. define adoption stages from journey semantics and accepted outcomes rather than interface activity;
2. construct eligible populations and stable cohorts by segment, version, mandate, migration wave and entry time;
3. calculate stage conversion, time-to-value, retention, expansion and safe-exit measures with valid denominators;
4. model branching, repeated, open and multi-interface journeys without forcing misleading linearity;
5. design stable event identity, deduplication, ordering, attribution and semantic-version contracts;
6. diagnose drop-off by combining path evidence, support signals and user research;
7. distinguish voluntary product pull, assisted success, mandatory migration, inherited use and lock-in;
8. pair funnel changes with delivery, safety, reliability, security, cost, accessibility and support guardrails;
9. run bounded cohort experiments without contaminating users or overclaiming causality; and
10. govern platform analytics for privacy, transparency, correction, retention and non-surveillance.

## Core Exposition

### Start with one journey and decision

Choose a critical outcome such as creating a service, deploying a conformant change, diagnosing production, obtaining a secret, restoring data or retiring a workload. “Adopt the platform” is too broad.

State the decision: improve discovery, change onboarding, redesign feedback, alter support, pause migration, retire a path or test an intervention. Metrics without a decision become dashboards without action.

Name the user entity—team, service, person or workload—and keep it consistent through the funnel or define explicit mappings.

### Define eligibility

Eligibility includes need, lifecycle, supported technology, risk tier, geography, policy, data classification, organizational readiness and capability availability during the window.

Exclude teams for whom the journey is irrelevant, but publish excluded categories. Narrowing eligibility after failure can manufacture conversion.

Version eligibility rules and materialize them at cohort entry so later organization changes do not rewrite historical denominators silently.

### Choose meaningful stages

Typical stages are eligible, aware, evaluated, first value, retained value, expanded value and exited safely. Not every journey needs every stage.

Define observable qualification for each. Awareness might require visiting journey-specific guidance or attending an onboarding session; it cannot be inferred from an email being sent.

First value must include correctness and required policy. A created but unusable cluster, failed deployment or resource made by platform staff is not independent value.

### Model cohorts

Cohort by stable entry event, such as first eligibility or first evaluation, and retain calendar/version context. Cohorts permit sufficient follow-up and expose changes over time.

Separate voluntary, mandated, migrated, grandfathered and assisted users. A single team can enter different capability funnels but should not appear twice in one cohort without declared re-entry.

Segment by journey-relevant context: maturity, risk, stack, region, accessibility, frequency and service age. Avoid tiny identifiable slices in reports.

### Set observation windows

Give each stage a window consistent with natural frequency. A quarterly recovery task cannot demonstrate 14-day retention.

Report right censoring for cohorts not old enough to reach a later stage. Do not count them as drop-off or silently omit them.

Use event time for behavior and record processing delay. Late telemetry can change a provisional result; close and revise cohorts under explicit policy.

### Specify event semantics

Events need stable names, entity identity, journey, stage, capability version, interface, source, event time, outcome, attempt, actor class and correlation ID.

Separate attempt, accepted completion, reversal and recovery. Deduplicate retried delivery using event identity rather than timestamp proximity.

Version semantic changes. A dashboard that changes “deployed” from API acceptance to verified production health creates a new series or restatement.

### Unify multiple interfaces

Users may move through portal, CLI, API, infrastructure as code, GitOps, ticket and enabling-team assistance. The funnel follows the outcome, not one interface.

Normalize interface events into journey semantics while retaining channel. Portal-only analytics penalize expert API use and reward navigation.

Represent handoffs explicitly. A self-service attempt that ends in a support ticket is an assisted path, not independent activation.

### Calculate stage conversion

For a closed funnel, each later set must be a subset of the prior stage for the same cohort. Audit nested sets before calculating ratios.

Show raw counts and rates. A move from one to two users is 100% growth but weak evidence; a 2% decline among thousands may be operationally important.

Calculate uncertainty appropriate to sampling and event quality, but do not use confidence intervals to disguise systematic missingness.

### Measure time and effort

Track time from eligible/aware/evaluation to first value and between repeated values. Report distributions and tails, not only means.

Separate active work, waiting, platform execution, approval and recovery. A faster UI can leave total elapsed time unchanged.

Record support contacts, expert interventions, retries and workaround steps. Time-to-value achieved by hidden platform labor may not scale.

### Define retention

Retention requires another qualifying outcome after activation in a meaningful later window while the entity remains eligible.

Choose rolling, fixed-window or return-frequency measures based on journey cadence. Publish grace periods and reactivation rules.

Investigate non-return: completed one-time need, service retirement, tool switch, platform failure, coercion ending or telemetry loss are different outcomes.

### Define expansion and depth

Expansion may mean a second qualifying service, journey, environment or team member after retained value. It should represent broader useful capability.

Depth measures should not reward waste. More clusters, pipelines or log volume can increase cost without increasing outcomes.

Pair expansion with standardization, reliability, cost, support and autonomy evidence. A platform can spread while becoming more harmful.

### Measure safe exit

Healthy platforms allow users to export state, transfer ownership, remove credentials, delete resources and preserve audit under documented contracts.

Track exit success, elapsed time, residual resources, data portability, incident risk and support. Low churn caused by prohibitive exit is lock-in, not satisfaction.

Learn from voluntary exits without punishing teams. Departure can reveal unsupported needs or a platform boundary that should remain narrow.

### Diagnose drop-off

Start with event quality and eligibility before blaming user motivation. Missing identity, late events and semantic mismatch create artificial leakage.

Combine stage paths with support records, session observation and interviews. Quantitative location answers where; research helps explain why.

Distinguish friction from correct prevention. A security gate that stops unsafe deployment is not a conversion defect, though its feedback may be.

### Design interventions

Match intervention to cause: discoverability, prerequisite check, example, preview, clearer error, automation, support, policy change, integration, performance or capability gap.

Avoid dark patterns and forced defaults. The goal is easier verified value, not a metric increase detached from consent and fitness.

State expected stage effect and guardrails before release. An onboarding change may increase evaluation while reducing qualified first value.

### Run cohort experiments

Randomization may be infeasible or unethical internally. Use bounded rollout, matched cohorts, interrupted time series or stepped introduction with explicit assumptions.

Prevent contamination when teams share documentation or practices. Record concurrent migrations, outages and policy changes.

Estimate effects conservatively and follow long enough for retention and harm. Early conversion uplift can disappear after novelty.

### Pair funnels with outcomes

For each stage, monitor accepted task success, lead/elapsed time, change quality, reliability, security, cost, support, toil, cognitive load and satisfaction.

Use guardrail gates rather than post hoc explanation. Stop an intervention that raises activation by bypassing policy or transferring work to on-call teams.

Connect platform use to organizational outcomes cautiously. Selection, maturity and mandate confound comparisons between adopters and non-adopters.

### Govern privacy and trust

Publish event purpose, fields, access, aggregation, retention, correction and deletion. Minimize personal identifiers and prefer team/journey evidence.

Prohibit individual productivity scoring, ranking or employment decisions from product analytics. Internal users cannot freely consent when access or employment is at stake.

Use thresholds and suppression to avoid re-identifying small teams. Audit downstream queries and metric exports.

### Operate the metric product

Assign owners for event producers, semantic contracts, transformations, dashboards and decisions. Test schema and invariants in delivery pipelines.

Monitor event volume, missingness, delay, duplication, identity joins and stage monotonicity. Annotate outages and known gaps.

Review definitions with users and stakeholders. Retire metrics that no longer drive decisions rather than accumulating vanity dashboards.

## Definitions and Notation

Let $U$ be measured entities, $J$ critical journeys, $C$ cohorts, $K=(0,\ldots,m)$ ordered stages, $W_k$ observation windows and $S_{c,j,k}$ qualifying sets.

For a closed funnel,

$$
S_{c,j,k+1}\subseteq S_{c,j,k},\qquad CR_{c,j,k}=\frac{|S_{c,j,k+1}|}{|S_{c,j,k}|}.
$$

When $|S_k|=0$, conversion is undefined rather than zero. Overall first-value rate from awareness is $|S_{value}|/|S_{aware}|$ only when both share entity, cohort, journey and observation eligibility.

Let $t_{u,k}$ be the first qualifying event time for entity $u$ at stage $k$. Stage latency is

$$
\Delta t_{u,k}=t_{u,k+1}-t_{u,k},
$$

reported as a distribution with censored entities identified. Retention at window $r$ is $|S_{retained,r}|/|S_{value,eligible\ at\ r}|$.

Let $M(u)\in\{voluntary,mandated,migrated,inherited\}$ and $H(u)$ record independent, assisted or operator-completed success. These dimensions remain visible in analysis. Let $G$ be guardrails and $O$ outcome measures; a funnel change is acceptable only when its named conversion improves and $G,O$ remain within predeclared bounds.

## Mechanisms, Invariants, or Proof Structure

### Twelve-step adoption mechanism

1. Select one critical journey, measured entity and product decision.
2. Define eligibility and materialize the cohort with versioned rules.
3. Separate voluntary, mandated, migrated, inherited and assisted paths.
4. Specify ordered stages from awareness through safe exit using accepted outcomes.
5. Set observation, retention, censoring, re-entry and cohort-close rules.
6. Instrument stable, deduplicated, privacy-minimized semantic events across interfaces.
7. Validate identities, stage nesting, event time, completeness and known missingness.
8. Compute raw counts, conversions, time distributions, retention and expansion by cohort.
9. Diagnose drop-off with support, observation and research rather than path data alone.
10. Design a bounded intervention with expected effect, comparison and guardrails.
11. Evaluate value, safety, reliability, cost, support, autonomy and exit over sufficient time.
12. Record the decision, limitations, semantic revision and next review trigger.

### Semantic invariant

Every stage has one stable entity, journey, qualifying outcome, version and observation rule; interface events map to semantics without replacing them.

### Cohort invariant

Eligibility, entry, mandate, assistance, version and windows are fixed or explicitly revised; later stages cannot borrow entities from a different denominator.

### Evidence invariant

Retries, duplicates, synthetics, operator actions, reversals and missing events are excluded or labeled, and raw counts accompany ratios.

### Outcome invariant

Activation, retention and expansion require accepted user outcomes and remain paired with quality, safety, reliability, cost, support and autonomy.

### Ethical invariant

Measurement is purpose-limited, transparent, access-controlled and non-punitive; funnel interventions do not coerce, deceive or prevent safe exit.

### Decision invariant

Every funnel and intervention serves a named decision, declares uncertainty and guardrails, and cannot be generalized beyond its cohort, journey and evidence revision.

### Proof sketch: high retention cannot establish satisfaction

Construct two capabilities with identical 95% measured retention. Capability A is voluntarily reused because it improves the journey. Capability B is mandated, owns an irreplaceable state format and imposes prohibitive exit cost; dissatisfied teams must still return. Retention is identical while satisfaction and value differ. Therefore retention alone cannot establish product success; mandate, outcome, support, sentiment and exit evidence are necessary.

### Executable closed-funnel audit

This synthetic audit verifies nested team sets and computes selected conversions for one voluntary deployment cohort. The numbers demonstrate semantics and arithmetic, not a universal target or real adoption result.

<!-- bijux-verify: {"id":"adoption-funnel-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"eligible=12\naware=11\nevaluated=9\nfirst_value=8\nretained=6\nexpanded=4\nawareness_to_value=72.7%\nvalue_to_retention=75.0%\nfunnel_invariants=pass\n"}} -->
```python
stages = {
    "eligible": set(range(1, 13)),
    "aware": set(range(1, 12)),
    "evaluated": set(range(1, 10)),
    "first_value": set(range(1, 9)),
    "retained": set(range(1, 7)),
    "expanded": set(range(1, 5)),
}
order = ["eligible", "aware", "evaluated", "first_value", "retained", "expanded"]
nested = all(stages[b] <= stages[a] for a, b in zip(order, order[1:]))

for stage in order:
    print(f"{stage}={len(stages[stage])}")
awareness_to_value = len(stages["first_value"]) / len(stages["aware"])
value_to_retention = len(stages["retained"]) / len(stages["first_value"])
print(f"awareness_to_value={awareness_to_value:.1%}")
print(f"value_to_retention={value_to_retention:.1%}")
print(f"funnel_invariants={'pass' if nested else 'fail'}")
```

### Verification strategy

Reconcile eligibility to catalogs and policies; sample events to audit and outcome records; test deduplication and identity joins; reproduce stage sets and ratios; validate cohort age and censoring; compare portal, CLI, API, GitOps, tickets and support; inspect mandatory and assisted labels; investigate drop-off with users; verify guardrail queries; audit privacy access and retention; and compare intervention decisions with predeclared gates.

## Alternatives and Trade-Offs

1. Closed funnels make conversion simple but poorly represent branching and re-entry.
2. Open funnels model real journeys but require explicit transition and attribution rules.
3. Team-level identity protects privacy but can hide individual accessibility barriers.
4. Person-level identity diagnoses collaboration but raises surveillance and join risk.
5. Service-level funnels align production outcomes but miss learning before a service exists.
6. Calendar cohorts compare periods but mix eligibility and capability maturity.
7. Entry cohorts support retention but take longer to mature.
8. Short windows provide fast feedback but misclassify infrequent work as abandonment.
9. Long windows fit natural cadence but delay decisions and accumulate confounders.
10. Strict activation protects meaning but can overlook partial early value.
11. Broad activation increases signal volume but rewards incomplete outcomes.
12. Unified semantic events compare interfaces but require strong identity and governance.
13. Interface-specific funnels are easier but fragment end-to-end journeys.
14. Randomized experiments strengthen causal inference but may be infeasible or unfair internally.
15. Staged rollout supports learning but can be confounded by team and time differences.
16. Rich segmentation reveals exclusion but can re-identify small teams.
17. Mandatory migration accelerates standardization but destroys voluntary demand evidence.
18. Easy exit may reduce nominal retention while increasing trust and product discipline.

## Failure Modes and Misconceptions

1. “Every engineering team is eligible” ignores journey, technology and lifecycle fit.
2. “An account is an adopted user” confuses provisioning with behavior.
3. “Email delivery is awareness” does not show comprehension or relevance.
4. “Portal login is activation” measures an interface visit, not value.
5. “First success is retention” omits a later qualifying window.
6. “More resources means expansion” can reward waste and abandonment.
7. “Low churn means satisfaction” ignores mandate and exit cost.
8. “One funnel covers the platform” combines different journeys and semantics.
9. “People and teams are interchangeable” corrupts denominators.
10. “Retries are additional conversions” inflates counts.
11. “Operator completion is self-service success” hides dependence.
12. “All drop-off is friction” ignores ineligibility and correct safety gates.
13. “A later-stage user need not appear earlier” breaks a closed-funnel contract.
14. “Zero denominator means zero conversion” replaces undefined with misleading certainty.
15. “Immature cohorts can be compared” ignores right censoring.
16. “Processing time is event time” misorders delayed telemetry.
17. “Missing telemetry means abandonment” treats observation failure as behavior.
18. “Dashboards from one stream triangulate evidence” repeats the same source bias.
19. “Overall conversion describes every segment” hides opposite cohort outcomes.
20. “A larger percentage is always material” ignores raw counts and consequence.
21. “Statistical significance proves importance” ignores effect size and guardrails.
22. “Correlation with platform use proves impact” ignores selection and mandate.
23. “A/B tests are always ethical” ignores unequal access to safety capabilities.
24. “Documentation sharing does not contaminate cohorts” overlooks team communication.
25. “Novelty uplift will persist” skips retention follow-up.
26. “Forced migration is organic adoption” launders governance into demand.
27. “More support improves adoption” can create an unscalable assisted path.
28. “Developer telemetry can rank productivity” violates purpose and validity.
29. “Small segments should always be shown” risks re-identification.
30. “Metric definitions can evolve silently” destroys comparability and auditability.

## Worked Examples

### Example 1

An organization reports 1,000 platform accounts. Only 120 teams are eligible for the deployment journey, 90 evaluated it and 60 achieved accepted first value. The revised funnel replaces a vanity denominator with actionable stage evidence.

### Example 2

CLI users bypass the portal entirely. Outcome-normalized events show higher first value and retention for the CLI, preventing portal clicks from misclassifying experts as non-adopters.

### Example 3

A support engineer completes setup for half the cohort. The dashboard separates independent and assisted activation; the team investigates which prerequisite blocks self-service.

### Example 4

Quarterly disaster-recovery users appear to have zero 30-day retention. The window changes to match the journey cadence, with cohort maturity disclosed.

### Example 5

Evaluation drops after a policy preview is added, while unsafe deployment attempts fall sharply and qualified first value is stable. The team treats prevention as improvement rather than optimizing raw conversion.

### Example 6

A mandatory migration produces 98% use, but support demand triples and safe exit fails. Mandate and outcome cohorts prevent the headline from being called product pull.

### Example 7

Newcomers activate less often than experts because internal terms dominate errors. Research leads to task-oriented feedback; the intervention is gated on accessibility and support as well as conversion.

### Example 8

Late audit events move five teams from apparent drop-off to first value after cohort close. The metric publishes a correction and tracks event-latency health.

### Example 9

Expansion by service count rises because automation creates duplicate abandoned environments. Requiring retained accepted deployments and cost guardrails removes the false growth.

### Example 10

Teams retain a database capability only because export is unavailable. Measuring exit completion reveals lock-in, and portability becomes a product outcome before further migration.

## Cross-Program Connections

- Product Management contributes lifecycle funnels, activation hypotheses and outcome guardrails.
- Statistics contributes denominators, cohort analysis, censoring, uncertainty and causal limits.
- Data Engineering contributes semantic events, identity, deduplication, lineage and late-data correction.
- Privacy Engineering contributes minimization, purpose limitation, aggregation and access controls.
- Human-Computer Interaction contributes task success, accessibility, research and friction diagnosis.
- Software Engineering contributes delivery journeys, interface instrumentation and quality outcomes.
- Site Reliability Engineering contributes critical journeys, reliability guardrails and support/toil signals.
- Security Engineering contributes policy-conformant outcomes, safe gates and telemetry governance.
- Engineering Management contributes incentives, mandates, migrations and non-punitive measurement.
- Economics contributes switching cost, lock-in, cost transfer and revealed preference limits.

## References

1. DORA. [Platform Engineering](https://dora.dev/capabilities/platform-engineering/). Retrieved 2026-09-02.
2. DORA. [2024 Research Questions](https://dora.dev/research/2024/questions/). Retrieved 2026-09-02.
3. DORA. [2024 Accelerate State of DevOps Report](https://dora.dev/research/2024/dora-report/). Retrieved 2026-09-02.
4. CNCF TAG App Delivery. [CNCF Platforms White Paper](https://tag-app-delivery.cncf.io/whitepapers/platforms/). Retrieved 2026-09-02.
5. CNCF TAG App Delivery. [Platform Engineering Maturity Model](https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/). Retrieved 2026-09-02.
6. CNCF TAG App Delivery. [Product Thinking for Platforms](https://tag-app-delivery.cncf.io/blog/product-thinking-for-platforms/). Retrieved 2026-09-02.
7. Google Developers. [Google Analytics Data API Funnel Reporting](https://developers.google.com/analytics/devguides/reporting/data/v1/funnels). Retrieved 2026-09-02.
8. Google Cloud. [What Is an Internal Developer Platform?](https://cloud.google.com/discover/what-is-an-internal-developer-platform). Retrieved 2026-09-02.
9. GOV.UK Service Manual. [Measuring Success](https://www.gov.uk/service-manual/measuring-success). Retrieved 2026-09-02.
10. GOV.UK Service Manual. [Using Performance Data to Improve Your Service](https://www.gov.uk/service-manual/measuring-success/using-data-to-improve-your-service-an-introduction). Retrieved 2026-09-02.
11. GOV.UK Service Manual. [Measuring the Success of Your Service](https://www.gov.uk/service-manual/measuring-success/measuring-the-success-of-your-service). Retrieved 2026-09-02.
12. GOV.UK Service Manual. [How to Set Performance Metrics](https://www.gov.uk/service-manual/measuring-success/how-to-set-performance-metrics-for-your-service). Retrieved 2026-09-02.
13. GOV.UK Service Manual. [Measuring Completion Rate](https://www.gov.uk/service-manual/measuring-success/measuring-completion-rate). Retrieved 2026-09-02.
14. GOV.UK Service Manual. [Measuring Digital Take-Up](https://www.gov.uk/service-manual/measuring-success/measuring-digital-take-up). Retrieved 2026-09-02.
15. GOV.UK Service Manual. [Measuring User Satisfaction](https://www.gov.uk/service-manual/measuring-success/measuring-user-satisfaction). Retrieved 2026-09-02.

## Exercises

### Exercise 1

A platform reports 70% adoption because 700 of 1,000 employees logged into its portal. Redefine the denominator, entity, journey and first-value stage for a service-deployment capability.

### Exercise 2

A monthly cohort has 80 eligible teams, 60 aware, 48 evaluating, 36 first-value, 24 retained and 12 expanded. Compute selected conversion rates and state what cannot be concluded.

### Exercise 3

Design event semantics for a deployment funnel spanning portal, CLI, GitOps and support tickets. Include identity, deduplication, accepted outcome and assistance.

### Exercise 4

After an onboarding intervention, first-value conversion rises from 50% to 65%, but failed changes and support contacts also rise. Describe the decision process.

### Exercise 5

A database platform has 99% annual retention and almost no voluntary exits. Design evidence that distinguishes satisfaction from lock-in.

## Answers to the Exercises

### Answer 1

Use the team or owned service as the entity, not employee login. Eligibility includes teams with an active deployment need, supported stack, lifecycle, risk tier and capability availability during the cohort window. Exclude irrelevant roles but publish categories.

Define first value as the team’s first independently completed, policy-conformant deployment reaching verified healthy production state, with retries deduplicated and operator-completed paths labeled assisted. Awareness and evaluation require journey-specific evidence across all interfaces.

### Answer 2

Awareness-to-evaluation is $48/60=80\%$; evaluation-to-first-value is $36/48=75\%$; first-value-to-retention is $24/36\approx66.7\%$; retention-to-expansion is $12/24=50\%$; eligible-to-first-value is $36/80=45\%$.

The counts do not establish why teams dropped, whether windows matured, whether adoption was voluntary, whether outcomes improved, whether support performed work, whether telemetry is complete or whether safety/reliability/cost guardrails held.

### Answer 3

Emit one semantic attempt with team, service, journey, capability version, channel, event time, attempt/correlation ID and actor class. Portal, CLI and GitOps map to the same accepted-deployment contract while retaining channel. Audit-confirmed healthy production state emits completion; rollback emits reversal.

Use stable event IDs for delivery deduplication. Link support tickets by correlation where consent and purpose allow, labeling platform-assisted or operator-completed paths. Do not infer completion from UI response or API acceptance.

### Answer 4

First validate cohorts, event semantics, maturity and concurrent changes. Compare effect size by relevant segment and inspect whether the intervention attracts less-qualified attempts or obscures prerequisites.

Apply predeclared guardrails: if failed changes or support dependence exceed bounds, stop or constrain rollout despite conversion uplift. Research failure paths, redesign feedback or eligibility, and retest a bounded cohort. Optimize accepted independent value, not first-value percentage alone.

### Answer 5

Measure mandate status, switching options, export completeness, exit elapsed time, residual state/credentials, cost, incidents and support. Run governed export and ownership-transfer tests with representative teams. Ask about recent work, constraints and alternatives rather than hypothetical satisfaction alone.

Pair retained qualifying outcomes with task success, reliability, cost, support, satisfaction and workaround evidence. If teams return only because data cannot move or policy forbids alternatives, report retention as constrained use and prioritize portability before calling it product success.
