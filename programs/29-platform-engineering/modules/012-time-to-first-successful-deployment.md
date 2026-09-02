---
module_id: PLAT-012
program: Platform Engineering
level: 1
module_number: 12
title: Time to First Successful Deployment
status: complete
last_verified: 2026-09-02
---

# Time to First Successful Deployment

## One-Page Review

### Governing question

How should a platform team define, measure, explain, and improve the time from a consumer's eligible deployment need to the first deployment whose application behavior, platform state, evidence, and ownership are actually verified?

### Essential definitions

- **Time to first successful deployment (TTFSD)** is elapsed time from a declared start event for an eligible consumer-workload attempt to its first deployment that satisfies a published verification contract.
- An **eligible attempt** is an intent that belongs to the measured population and has enough identity, segment, workload, and start evidence to enter the denominator, whether it later succeeds, fails, is abandoned, or remains unresolved.
- A **start event** is the earliest observable event chosen to represent the real beginning of the measured journey. Its meaning and known exclusions must be explicit.
- A **successful deployment** is a deployment that satisfies environment, artifact, rollout, application-behavior, observability, ownership, and recovery criteria appropriate to the workload profile.
- A **verification contract** specifies the predicates and evidence required before success can be asserted, including who owns domain-specific acceptance.
- A **milestone** is an evidence-backed transition such as access ready, repository ready, first build passed, rollout complete, application probe passed, or consumer verification recorded.
- A **censored attempt** has no observed success or terminal failure before the observation window ends; it is not a zero-duration or successful attempt.
- **Conditional success time** summarizes duration only among observed successes. It must be reported with the eligible denominator and outcome distribution.

### Central model, mechanism, or theorem

Represent attempt $a$ as $A_a=(U,W,K,t_0,M,E,Q,t_v,O)$: consumer segment $U$, workload profile $W$, context $K$, start $t_0$, ordered milestone evidence $M$, exception and recovery trace $E$, verification contract $Q$, first verification time $t_v$, and outcome $O$. For a verified attempt, $T_a=t_v-t_0$. Never interpret the distribution of $T_a$ without the eligible count, outcome states, time window, segments, and exclusions: a fast conditional median can coexist with widespread failure or abandonment.

### Critical invariants

- The start boundary, eligibility rule, success contract, clock, observation window, and segmentation remain versioned and visible.
- Every eligible attempt enters the denominator exactly once; retries link to the original intent rather than silently becoming new successes.
- Success requires workload-relevant behavior and evidence, not merely repository creation, request acceptance, pipeline completion, or a green deployment controller.
- Failed, abandoned, unsupported, duplicate, and censored attempts remain distinguishable.
- Human work, queueing, approvals, provider waits, rework, and recovery remain in the end-to-end trace.
- Platform evidence cannot replace application-owner acceptance where domain knowledge is required.
- Improvement preserves security, reliability, accessibility, cost, compliance, operability, and operator sustainability.

### Common failures

Starting the clock at the final button; stopping it when a resource exists; measuring only successful template runs; excluding teams that never obtained access; resetting the timer on retry; mixing sandbox and production profiles; using averages across dissimilar cohorts; optimizing a toy service; treating missing final events as fast completion; incentivizing teams to avoid verification; and claiming causality from a before/after chart that ignores selection, seasonality, or concurrent changes.

### Compact example

A product team is eligible when an approved service owner begins the supported production-onboarding journey. The timer includes access, repository creation, ownership metadata, pipeline setup, policy feedback, build, deployment, application smoke test, telemetry check, and acknowledgement of rollback responsibility. A template finishes in six minutes, the first rollout completes at 24 minutes, and the application verification passes at 41 minutes after a configuration repair. TTFSD is 41 minutes. The failed rollout and repair remain in the trace; neither six nor 24 minutes is reported as success.

### Connections

Retrieve consumer segments from [PLAT-002](002-platform-consumers-and-jobs-to-be-done.md), self-service states from [PLAT-005](005-self-service-and-guardrails.md), capability and provider boundaries from [PLAT-007](007-platform-capabilities-versus-tool-catalogs.md), value hypotheses from [PLAT-010](010-defining-a-platform-s-value-proposition.md), and complete journey modeling from [PLAT-011](011-developer-journeys.md). Later modules apply the evidence contract through CLI, portal, API, template, documentation, diagnostic, observability, and developer-experience surfaces.

## Governing Question

When can a platform honestly say that a consumer reached a first successful deployment, how long did the whole attempt take, and which platform mechanisms caused a defensible improvement without hiding failure or transferring burden?

The phrase sounds simple but contains three contested boundaries: **first**, **successful**, and **deployment**. First relative to which consumer, workload, environment, repository, or platform version? Successful according to a controller, a health endpoint, the application owner, or an actual user outcome? Deployment beginning at code commit, platform signup, an approved need, or template submission?

TTFSD becomes useful only after those choices are explicit. It is a bounded product measure for one important developer journey, not a universal productivity score and not a replacement for software-delivery, reliability, security, cost, or experience measures.

## Why This Matters

The first verified deployment tests whether the platform proposition is coherent. Identity, discovery, documentation, templates, source control, build, policy, artifacts, runtime, networking, secrets, observability, feedback, support, and responsibility all meet in one journey. Friction at any boundary can invalidate a locally excellent interface.

Current DORA platform guidance describes a platform as an internal product and emphasizes clear feedback on task outcomes, independent work, reliable and secure delivery, and critical user journeys. DORA also reports that platform adoption can improve productivity while correlating with worse throughput or stability when implemented poorly. A fast first deployment therefore needs balancing evidence rather than celebration in isolation.

DORA's current software-delivery metrics define change lead time from a change committed to version control until deployment in production. TTFSD has a different purpose. It asks how a consumer crosses initial platform and organizational setup to the first verified deployment. After onboarding, DORA change lead time and deployment frequency are better repeated-flow measures. Keeping the clocks distinct prevents a platform onboarding metric from being mislabeled as an industry benchmark.

Software templates can load a skeleton, collect inputs, execute actions, publish source, and register a component. Current Backstage documentation exposes task identity, progress, failure logs, cancellation, and results. Those are useful milestones, but template completion is not necessarily deployment, and deployment is not necessarily application success. Treat scaffolding as one composable mechanism in the journey.

The metric also exposes exclusion. A reported median among four successful expert teams says nothing about six novices who abandoned, two regulated workloads rejected as unsupported, or a team blocked before the instrumented start. The denominator is a product decision. Honest measurement makes non-arrival and unresolved work visible.

## Prerequisites and Retrieval

Retrieve the platform system boundary from PLAT-001; segments, jobs, contexts, and non-users from PLAT-002; cognitive-load mechanisms from PLAT-003; product lifecycle from PLAT-004; self-service operations and guardrails from PLAT-005; build-or-buy routes from PLAT-006; capability contracts from PLAT-007; provider responsibility from PLAT-008; team interaction modes from PLAT-009; value hypotheses and counterfactuals from PLAT-010; and the complete journey/service-blueprint model from PLAT-011.

You should understand event timestamps, state machines, identifiers, continuous integration and delivery, deployment strategies, application health, telemetry, percentiles, sampling, cohorts, basic causal inference, privacy, accessibility, and service ownership. Familiarity with survival analysis helps with unresolved attempts but is not required.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish TTFSD from scaffolding duration, pipeline duration, rollout duration, DORA change lead time, and time to production value;
2. define an eligible attempt, start event, workload-specific verification contract, terminal outcomes, and observation window;
3. construct an event and identity model that preserves waits, retries, failures, abandonment, and censoring;
4. calculate and interpret completion rates, milestone durations, conditional percentiles, and deadline success without survivorship bias;
5. segment results without destroying comparability or exposing individuals;
6. identify mechanisms that improve the complete path while preserving safety, operability, accessibility, and authority; and
7. evaluate a TTFSD intervention using a predeclared hypothesis, comparison strategy, guardrails, and qualitative evidence.

## Core Exposition

### Define the unit before the stopwatch

Choose the consumer unit and workload unit. A consumer may be a team, not an individual, because ownership and operational duties are collective. A workload may be a new service, migrated service, scheduled job, data pipeline, client application, or machine-learning endpoint. “First” can mean first for the organization, team, platform, workload class, environment, or template version. State which one.

A useful default is the first eligible attempt by a defined team to deploy a new workload through a named platform profile into a named environment class. It is not automatically the first deployment of a developer's career. Preserve pseudonymous team and workload identifiers only where justified; the metric must not become individual surveillance.

Write inclusion and exclusion rules before examining the durations. Include both adopters and eligible non-completers. Exclusions may be legitimate for test traffic, synthetic probes, duplicate telemetry, or workloads outside the product contract. Record their counts and reasons. Excluding “difficult” attempts because they threaten the target destroys the measure.

### Set an honest start boundary

The ideal start is the real trigger: the moment a team has a valid need and begins work to obtain the outcome. That moment may not be directly observable. Possible proxies include an intake declaration, approved architecture record, platform enrollment, repository intent, template start, or first authenticated operation.

Select the earliest reliable event the platform can govern, document what precedes it, and measure upstream wait separately when possible. A portal cannot claim a five-minute journey by starting at its final submit action if access, policy interpretation, and metadata preparation took days.

The start event must be idempotent. Reopening a browser, rerunning a template, or switching from portal to CLI must not reset the original intent. Link retries and channel changes through a durable attempt identifier. When correlation is uncertain, label the trace uncertain instead of manufacturing precision.

### Specify successful deployment as a contract

Create verification contract $Q_W$ for each supported workload profile $W$. A defensible baseline typically requires:

1. the intended, immutable artifact or source revision is identified;
2. the target environment and configuration are the declared ones;
3. the deployment controller reaches a stable terminal state;
4. required policy, identity, network, secret, and data controls are satisfied;
5. workload-relevant behavior passes a bounded probe or acceptance check;
6. required logs, metrics, traces, ownership, and support evidence are discoverable;
7. rollback or recovery responsibility and method are known; and
8. the authorized application owner accepts any domain-specific criterion the platform cannot decide.

The contract should be demanding enough to represent useful readiness but small enough for a first milestone. A production payment service may require a synthetic transaction without settlement. A batch pipeline may require a bounded test input, output validation, lineage, and retry evidence. A static site may require successful content retrieval, TLS, telemetry, and ownership. One green health endpoint is not universal truth.

Version the contract. If criteria change, do not combine old and new durations without labeling them. A stricter definition can make the metric appear worse while the product becomes safer.

### Model attempts, milestones, and outcomes

Represent attempt $a$ as

$$
A_a=(U,W,K,t_0,M,E,Q,t_v,O),
$$

where $U$ is consumer segment, $W$ workload profile, $K$ context, $t_0$ start, $M$ milestone events, $E$ exception/recovery trace, $Q$ verification contract, $t_v$ first time $Q$ is satisfied, and $O$ outcome.

Use outcomes such as `verified`, `failed-terminal`, `abandoned`, `unsupported`, `duplicate`, and `censored`. Unsupported can reveal a product gap, so report it even when excluded from a profile's performance denominator. Duplicate is a telemetry determination, not an inconvenient outcome. Censored means observation ended before a terminal event.

Milestones might include eligible, identity ready, repository ready, declaration valid, first feedback, first build passed, artifact published, rollout started, controller stable, application probe passed, telemetry visible, owner acceptance, and verified. Emit timestamp, attempt ID, workload ID, event type, source, result, contract version, and correlation identifiers. Keep sensitive payloads out of measurement events.

### Calculate without erasing the denominator

For a verified attempt,

$$
T_a=t_v-t_0.
$$

Let $\mathcal{E}$ be eligible attempts and $\delta_a=1$ when attempt $a$ is verified in the observation window. The observed completion rate is

$$
C=\frac{\sum_{a\in\mathcal{E}}\delta_a}{|\mathcal{E}|}.
$$

Report duration percentiles among verified attempts only as **conditional** durations. Pair them with $|\mathcal{E}|$, outcome counts, observation window, segment, and contract version. Otherwise a system can improve its median by failing slow attempts early.

A simple deadline measure avoids pretending unresolved attempts succeeded:

$$
F(D)=\frac{|\{a\in\mathcal{E}:\delta_a=1\land T_a\le D\}|}{|\mathcal{E}|},
$$

the fraction of eligible attempts verified within deadline $D$. Choose $D$ from user needs or a declared service target, not after inspecting the curve. For mature analysis with staggered entry and right-censoring, use a time-to-event estimator and publish its assumptions; do not silently map censoring to failure or success.

The following synthetic cohort demonstrates why the denominator accompanies the conditional median.

<!-- bijux-verify: {"id":"ttfsd-cohort-summary","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"eligible=8\nverified=4\ncompletion_rate=0.500\nverified_by_60_rate=0.375\nconditional_median_minutes=38.0\nunresolved_or_unsuccessful=4\n","stderr":""}} -->
```python
from statistics import median

attempts = [
    ("a1", "verified", 28),
    ("a2", "verified", 42),
    ("a3", "failed-terminal", 17),
    ("a4", "verified", 65),
    ("a5", "censored", 90),
    ("a6", "verified", 34),
    ("a7", "abandoned", 12),
    ("a8", "failed-terminal", 53),
]

verified = [minutes for _, outcome, minutes in attempts if outcome == "verified"]
verified_by_60 = [minutes for minutes in verified if minutes <= 60]
eligible = len(attempts)
print(f"eligible={eligible}")
print(f"verified={len(verified)}")
print(f"completion_rate={len(verified) / eligible:.3f}")
print(f"verified_by_60_rate={len(verified_by_60) / eligible:.3f}")
print(f"conditional_median_minutes={median(verified):.1f}")
print(f"unresolved_or_unsuccessful={eligible - len(verified)}")
```

The 38-minute median describes four successes. It does not license the claim that a typical eligible attempt succeeds in 38 minutes; only half of the cohort verified during observation.

### Decompose time by evidence, not guesswork

Partition the journey into intervals such as discovery, access, preparation, validation, build, policy, queue, artifact transfer, rollout, application verification, and owner acceptance. Distinguish elapsed time, human active time, automated processing, queueing, and unknown time. Parallel intervals need interval-union or critical-path treatment rather than naive addition.

Record first-feedback latency as well as completion. A 40-minute operation that reports a useful validation error in 20 seconds differs from one that stays silent for 39 minutes. Measure retry and rework loops explicitly. The longest stage is not automatically the best intervention: a long provider operation may be predictable and unattended while a two-minute ambiguous denial causes hours of coordination.

Combine trace data with observation, interviews, support, and artifact review. Events show what the instrumented system recorded, not what the consumer understood or did outside it.

### Segment and compare responsibly

Segment before aggregating when profiles have materially different contracts: novice versus experienced platform users, new versus migrated workloads, sandbox versus production, stateless service versus data pipeline, ordinary versus regulated context, region, access route, template version, and voluntary versus mandated adoption.

Avoid publishing tiny cells or individual rankings. Use aggregation thresholds, purpose limitation, access controls, retention, and qualitative safeguards. Skill, disability, schedule, location, and support use can become sensitive employment signals. Measure the product, not worker worth.

Comparison requires stable definitions. Record changes in eligibility, contract, instrumentation, workload mix, staffing, policy, provider, and seasonality. Prefer staggered rollout, matched cohorts, interrupted time series, or another design suited to the intervention. A simple before/after comparison is a hypothesis check, not automatic causal proof.

### Improve mechanisms rather than the displayed number

Common improvement mechanisms include pre-provisioned identity, progressive discovery, validated templates, policy feedback before expensive work, reproducible local checks, cached dependencies, right-sized environments, asynchronous operations with durable state, automatic correlation, application-aware verification hooks, accessible diagnostics, and recoverable retries.

Remove duplicated declarations and encode deterministic decisions. Preserve meaningful domain decisions. Do not bypass a control merely because it adds elapsed time; reduce uncertainty, automate evidence, or run independent checks concurrently when safe. If human approval is required for a consequential judgment, make its authority, queue, evidence, and target visible.

Optimize templates for representative workloads rather than a theatrical hello world. A golden path is credible when its output is owned, operable, observable, secure, maintainable, and compatible with later change. Measure its upgrade and retirement consequences too.

### Balance speed with quality and sustainability

Pair TTFSD with verification completion, change failure, deployment rework, recovery, security exceptions, reliability, cost variance, accessibility, satisfaction, support dependency, cognitive load, and platform operator toil. DORA's current delivery metrics jointly consider throughput and instability; the same systems principle applies here.

A fast first deployment can be harmful if it creates an unsupported service, hides costs, omits telemetry, centralizes application operation on the platform team, or produces a brittle template consumers cannot update. Guardrails are not secondary metrics to add after launch. They define whether the speed improvement counts.

### Operate the measure as a product contract

Publish a metric card containing owner, purpose, decision supported, population, eligibility, start, end, contract version, outcomes, observation window, segmentation, exclusions, data sources, data quality, privacy controls, known blind spots, guardrails, and review date.

Provide an attempt-level diagnostic view to authorized consumers and support without exposing cohort data. Let teams see which milestone is current, what evidence failed, what state remains, how to retry or cancel, and whom to contact. Aggregate product analytics should link back to actionable mechanisms and a research backlog.

Review the definition after product, policy, provider, instrumentation, or workload changes. Retain historical definitions so trend breaks are explicit. Retire the measure when it no longer informs a decision; metrics without decisions accumulate incentives and surveillance risk.

## Definitions and Notation

$A_a=(U,W,K,t_0,M,E,Q,t_v,O)$ denotes attempt $a$ through segment, workload, context, start, milestones, exceptions/recovery, verification contract, first verification time, and outcome. $T_a=t_v-t_0$ exists as a completed duration only when verification occurs.

$\mathcal{E}$ is the eligible-attempt set for a declared cohort and observation window. $\delta_a$ is one for observed verification and zero otherwise when computing the bounded observed completion rate $C$. It is not a statement that every zero is a permanent failure.

$F(D)$ is the proportion of all eligible attempts observed verified within deadline $D$. Conditional percentiles $P_p(T\mid\delta=1)$ summarize observed successful durations and must not be confused with unconditional completion probability.

For milestone timestamps $t_{a,i}$, interval duration is $d_{a,i}=t_{a,i+1}-t_{a,i}$ only when the adjacent events and clock are valid. Concurrent intervals and missing events require explicit treatment.

## Mechanisms, Invariants, or Proof Structure

Use a repeating measurement loop: define decision and population; version eligibility and verification contracts; instrument stable identities and evidence events; validate traces against observed journeys; declare cohorts and windows; compute outcomes before durations; segment; inspect tails and missingness; triangulate qualitatively; choose a mechanism; predeclare hypothesis and guardrails; release safely; compare; and revise the product and metric card.

The denominator invariant prevents survivorship bias. The clock invariant prevents late starts and retry resets. The verification invariant prevents proxy milestones from becoming domain truth. The identity invariant joins channels, retries, providers, and support. The authority invariant reserves application acceptance for those with domain knowledge. The guardrail invariant rejects speed bought through unsafe omission or transferred toil.

Adversarial checks include: no final event; duplicate final event; clocks out of order; retry through another channel; reused repository; preexisting access; failed first rollout followed by success; consumer never begins after eligibility; unsupported workload; observation ending mid-attempt; contract revision; platform rollback; false-positive health check; missing telemetry; inaccessible instructions; provider outage; and a team optimizing solely to the target.

No formula proves platform value. The calculations establish internally consistent cohort summaries under stated definitions. Causal attribution requires a comparison design and mechanism evidence; organizational value requires later delivery and operational outcomes.

## Alternatives and Trade-Offs

**Template completion time** is easy to instrument and useful for scaffolder performance. It excludes preparation, deployment, verification, and non-template routes, so it is a milestone rather than TTFSD.

**Pipeline duration** precisely locates build and delivery bottlenecks. It starts after substantial setup and omits access, comprehension, ownership, and application acceptance.

**DORA change lead time** supports repeated production-delivery performance from commit to deployment. It should remain separately named and measured; TTFSD focuses on initial enablement.

**Time to first value** asks when an external or organizational outcome occurs. It is closer to product value but harder to attribute and may occur long after technically verified deployment. Link, do not collapse, the two measures.

**Conditional median** is robust to extreme successful durations and easy to explain. It hides unsuccessful and unresolved attempts unless paired with outcome counts and deadline completion.

**Survival analysis** can use right-censored observations and show probability over time. It requires careful assumptions, event definitions, and statistical communication. Small cohorts may support only descriptive traces.

**Synthetic journey tests** provide frequent, controlled signals and regression detection. They cannot represent human comprehension, access variation, organizational queues, or domain acceptance.

## Failure Modes and Misconceptions

- **“The template succeeded, so the workload deployed.”** A repository or catalog entity can exist without a runnable, verified application.
- **“The controller is green, so the application is successful.”** Controller state does not establish domain behavior, observability, or consumer acceptance.
- **“Only successful attempts have a duration.”** True for completed TTFSD, but unsuccessful and censored attempts still belong in the denominator and trace analysis.
- **“Retry starts a fresh clock.”** Resetting erases rework and rewards fragile flows; link retries to original intent.
- **“The median fell, therefore the platform improved.”** Population, contract, completion, workload mix, and guardrails may have changed.
- **“One number works for every workload.”** Profiles require different success predicates and should not be mixed without stratification.
- **“Fastest means best.”** A shortcut that omits ownership, policy, telemetry, recovery, or accessibility creates later risk and work.
- **“Missing events mean zero delay.”** Missingness is a data-quality state, not completion.
- **“A dashboard creates accountability.”** Accountability requires owners, decisions, diagnostics, hypotheses, and change mechanisms.
- **“Measure developers to motivate adoption.”** Individual ranking corrupts the metric and creates surveillance; measure the platform journey.

## Worked Examples

### Example 1

A stateless-service template publishes a repository in four minutes. The first build fails because the generated dependency lock is stale; a retry deploys at 31 minutes; an application probe and telemetry verification pass at 46 minutes. The attempt has one start, one failure loop, and TTFSD of 46 minutes. Template time remains a four-minute milestone.

### Example 2

A data pipeline reports “running,” but its test input produces a schema-invalid table. The workload contract requires bounded input, output quality checks, lineage, retry visibility, and owner acceptance. TTFSD ends after the corrected transformation produces valid output, not when the scheduler accepts the job.

### Example 3

Eight successful attempts have a 20-minute median, while twelve eligible teams abandoned before access. The platform reports eight of twenty completed and investigates identity and discoverability. Reporting only 20 minutes would reward the very exclusion the platform should remove.

### Example 4

A regulated production service waits six hours for a human risk decision. The platform cannot delete the judgment, but it can request evidence earlier, validate completeness, display queue state, and parallelize independent preparation. The production cohort remains separate from sandbox deployments.

### Example 5

A portal attempt fails, then the team switches to the CLI with copied configuration. Shared intent and operation identifiers preserve one journey. Without correlation, analytics would record a portal failure and a suspiciously fast new CLI success.

### Example 6

A provider outage leaves rollout operations pending when the weekly observation window closes. Those attempts are right-censored at the last known time, not assigned zero, infinity, or success. The incident cohort is shown separately and remains part of the product reliability analysis.

### Example 7

A platform replaces a detailed application probe with `/healthz` to hit a target. Times fall, but later smoke tests fail more often. The verification-contract change creates a trend break; the team restores workload-relevant acceptance and rejects the apparent improvement.

### Example 8

Instructions require visual interpretation of a topology diagram and block a screen-reader user before the instrumented template event. Journey observation reveals the blind spot. The start moves to enrollment, content becomes semantically accessible, and accessibility success joins the guardrails.

### Example 9

A migration team already has repositories, pipelines, and cloud access. Comparing it with new teams makes the platform look fast. Context fields identify preexisting assets, and separate cohorts make both reuse benefits and greenfield friction visible.

### Example 10

A first deployment is fast because the platform team manually repairs every policy error in chat. Independent completion and operator toil reveal transferred work. The product adds contextual diagnostics and a policy dry run, then evaluates both TTFSD and support demand.

## Cross-Program Connections

Statistics contributes cohort construction, conditional distributions, censoring, missingness, uncertainty, and comparison design. Data engineering contributes event schemas, quality checks, identity resolution, lineage, retention, and reproducible aggregation. Experimental design contributes predeclared hypotheses and guardrails.

Software delivery engineering contributes continuous integration, artifacts, deployment state, rollout, rollback, and DORA metrics. Reliability engineering contributes application-level indicators, observability, degraded operation, recovery, and error budgets. Distributed systems explains asynchronous operations, partial failure, idempotency, clock problems, and correlation.

Security, privacy, accessibility, and governance determine legitimate eligibility, evidence, measurement purpose, data minimization, human authority, and equitable access. Product management connects the milestone to consumer value and adoption. Organizational design reveals queues, interaction modes, ownership, and burden transferred between stream-aligned, platform, enabling, and provider teams.

## References

- DORA, [*Platform Engineering*](https://dora.dev/capabilities/platform-engineering/), updated January 12, 2026. Current internal-product guidance on clear task feedback, independent work, critical journeys, delivery outcomes, and the risks of poorly implemented platforms.
- DORA, [*DORA's Software Delivery Performance Metrics*](https://dora.dev/guides/dora-metrics/), current guide retrieved September 2, 2026. Definitions of change lead time, deployment frequency, failed deployment recovery time, change failure rate, and deployment rework rate.
- DORA, [*Value Stream Mapping for Software Delivery*](https://dora.dev/guides/value-stream-management/), current guide retrieved September 2, 2026. Happy-path and recovery value streams, outcome-first mapping, and use of throughput and stability evidence.
- DORA, [*2025 Research Questions*](https://dora.dev/research/2025/questions/), 2025 survey instrument. Primary wording for production deployment, change lead time, platform task feedback, automation, independence, reliability, security, and delivery constructs.
- DORA, [*2024 Accelerate State of DevOps Report*](https://dora.dev/research/2024/dora-report/), corrected edition v2024.3. Empirical platform adoption, productivity, independence, throughput, stability, and user-centeredness findings with survey limitations.
- Backstage Project, [*Software Templates*](https://backstage.io/docs/features/software-templates/), current documentation retrieved September 2, 2026. Template inputs, action execution, task identity, progress, results, failure logs, cancellation, and rerun behavior.
- Backstage Project, [*Create a Component*](https://backstage.io/docs/getting-started/create-a-component/), current documentation retrieved September 2, 2026. Repository scaffolding, catalog registration, generated metadata, and the boundary between component creation and deployment.
- Google Cloud, [*Automate and Manage Change*](https://cloud.google.com/architecture/framework/operational-excellence/automate-and-manage-change), last updated October 31, 2024. Testing, validation, controlled deployment, monitoring, rollout strategies, and rollback guidance.
- Edward L. Kaplan and Paul Meier, [“Nonparametric Estimation from Incomplete Observations”](https://doi.org/10.1080/01621459.1958.10501452), *Journal of the American Statistical Association* 53(282), 1958. Foundational estimator for time-to-event data with censored observations.
- Nicole Forsgren, Jez Humble, and Gene Kim, [*Accelerate: The Science of Lean Software and DevOps*](https://itrevolution.com/product/accelerate/), IT Revolution, 2018. Research and measurement foundations for software-delivery throughput, stability, capabilities, and outcomes.

## Exercises

### Exercise 1

Define TTFSD for a platform's stateless production-service profile. Specify consumer and workload units, eligibility, start, milestones, verification predicates, outcomes, deadline, exclusions, and balancing measures.

### Exercise 2

A dashboard includes only successful attempts: 12, 18, 21, and 49 minutes. Three attempts failed at 9, 15, and 40 minutes; one was abandoned at 7 minutes; two remain unresolved at 60 minutes. Compute the observed completion rate, conditional median, and fraction verified within 30 minutes. Explain the interpretation.

### Exercise 3

Design an event model that correlates a portal start, failed template, CLI retry, deployment provider operation, application verification, and support case without collecting source code or ranking individuals.

### Exercise 4

A team proposes removing ownership, telemetry, and rollback checks so that first-deployment time falls below ten minutes. Evaluate the proposal and design a safer intervention with a causal evaluation strategy.

### Exercise 5

Transfer the measure to the first successful deployment of a hospital medication-decision service. Define what the platform may verify and what must remain under clinical, privacy, safety, and operational authority.

## Answers to the Exercises

### Answer 1

Use the owning team as consumer and a new stateless service as workload. Eligibility begins when an authorized team declares a supported production-service intent with required domain ownership; start is the first durable enrollment event, while earlier known approval wait is reported separately. Milestones are identity ready, source ready, declaration valid, first feedback, build passed, artifact published, policy passed, rollout stable, application probe passed, telemetry discoverable, rollback confirmed, and owner accepted. Verification requires exact artifact/environment, stable rollout, workload-relevant probe, required controls, logs/metrics, owner/support metadata, and recovery evidence. Outcomes are verified, terminal failure, abandonment, unsupported, duplicate, and censored. Report verified within a predeclared two-hour deadline, full outcome counts, and conditional percentiles. Exclude synthetic and duplicate traffic with counts. Balance against change failure, rework, security exceptions, reliability, accessibility, cost, support dependence, satisfaction, and platform toil.

### Answer 2

There are ten eligible attempts and four observed successes, so completion is $4/10=0.40$. Sorted successful durations are 12, 18, 21, and 49; their conditional median is $(18+21)/2=19.5$ minutes. Three successes occurred within 30 minutes, so deadline success is $3/10=0.30$. The 19.5-minute figure describes observed successes only. It does not mean a typical eligible attempt succeeds in 19.5 minutes because six did not verify during observation. Failed, abandoned, and unresolved states must remain visible; the two unresolved observations may be right-censored in a time-to-event analysis.

### Answer 3

Create a pseudonymous `attempt_id` at portal enrollment and propagate it into `template_task_id`, `operation_id`, workload ID, deployment-provider correlation, verification record, and support-case reference. Emit event type, server timestamp, source channel, bounded outcome, contract version, error class, and evidence locator, not source content. The CLI accepts or discovers the existing attempt ID, so retry does not reset the clock. The provider callback maps to the operation; application owner acceptance signs the verification record; support uses the same correlation. Limit access, retention, and dimensions; aggregate by sufficiently large team/workload cohorts. Record correlation confidence and missing links. Never expose an individual leaderboard.

### Answer 4

Reject the redefinition because it changes success rather than improving the journey. It would create ownerless, unobservable, unrecoverable workloads and a misleading trend break. Keep the verification contract and move checks earlier: default ownership from authoritative metadata with confirmation, install telemetry through a maintained template, validate signal arrival automatically, generate rollback configuration, offer policy and observability dry runs, and provide immediate diagnostics. Roll out to comparable cohorts or staggered teams, predeclare expected reductions in milestone wait and TTFSD, and track completion, failure, rework, incidents, security exceptions, support, and operator toil. Record workload mix and contract version; combine traces with consumer observation. Claim causality only to the extent supported by the comparison and mechanism evidence.

### Answer 5

Eligibility requires an authorized clinical product owner, approved use case, defined data classification, safety ownership, and a supported workload profile. The platform may verify exact artifact, environment, identity, encryption, policy enforcement, deployment stability, technical health, telemetry, audit events, rollback mechanism, and availability of support evidence. A bounded synthetic test can verify technical routing with non-patient data. The platform must not declare clinical correctness, medication safety, lawful purpose, or fitness for patient care on controller state alone. Clinical safety officers and qualified clinicians own clinical validation; privacy authority owns lawful processing and access; application owners own domain acceptance and on-call readiness. First success occurs only when required technical evidence and authorized clinical/operational acceptance are both recorded. Patient data never enters measurement telemetry; failed, abandoned, censored, rollback, downtime, and incident paths remain governed and visible.
