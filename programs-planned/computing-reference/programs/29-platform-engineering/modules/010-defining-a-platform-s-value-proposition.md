---
module_id: PLAT-010
program: Platform Engineering
level: 1
module_number: 10
title: Defining a Platform's Value Proposition
status: complete
last_verified: 2026-09-02
---

# Defining a Platform's Value Proposition

## One-Page Review

### Governing question

For which consumers, jobs, and contexts should a platform be preferred over the current alternatives, through what mechanism, with which measurable outcomes, costs, harms, retained obligations, and evidence-based continuation conditions?

### Essential definitions

- A **value proposition** is a segment-specific, testable claim that an offering helps consumers accomplish an important job better than a named alternative under stated conditions.
- A **consumer job** is progress a consumer seeks in context; it is not a requested feature, tool, or implementation.
- A **current alternative** is how the job is done now, including tickets, local automation, provider-direct use, manual coordination, delay, abandonment, or deliberate non-action.
- A **pain** is evidenced difficulty, risk, wait, effort, uncertainty, exclusion, or undesired outcome in the current journey.
- A **gain** is a desired outcome or improved ability, not merely the presence of a feature.
- A **value mechanism** explains how a platform capability changes work or system behavior to produce the proposed outcome.
- A **value hypothesis** binds segment, job, context, alternative, capability, mechanism, outcome, horizon, evidence, guardrails, retained obligations, and stop or revision criteria.
- **Value realization** is observed improvement in the consumer and wider system after adoption, net of transferred burden, operating cost, harms, and alternative explanations.

### Central model, mechanism, or theorem

Represent a platform value hypothesis as $V=(U,J,K,A,C,M,O,T,E,G,R,S)$: consumer segment $U$, job $J$, context $K$, current alternative $A$, platform capability $C$, causal mechanism $M$, bounded outcomes $O$, horizon $T$, evidence plan $E$, guardrails $G$, retained obligations $R$, and stop or revision conditions $S$. Validate the chain from capability to task outcome before attributing downstream delivery or organizational effects. Value is relational and counterfactual: no capability is valuable in isolation.

### Critical invariants

- Every value claim names a segment, job, context, and credible current alternative.
- The mechanism explains why the offering should change an outcome; features and interfaces are not outcomes.
- Baselines and denominators are captured before success is inferred.
- Consumer benefit, organizational benefit, and platform operating sustainability are reviewed together without pretending they are interchangeable units.
- Mandatory adoption, auto-enrollment, subsidies, and removal of alternatives are disclosed when interpreting take-up.
- Safety, security, privacy, accessibility, reliability, cost, operator load, and domain obligations remain guardrails rather than being averaged away.
- Evidence can weaken, narrow, revise, or stop the proposition; the roadmap is not its own proof.

### Common failures

Writing “a single pane of glass for developer productivity”; listing tools instead of jobs; assuming internal users have no alternatives; monetizing every developer minute without causal evidence; claiming enterprise revenue from a portal release; using adoption or satisfaction alone; measuring only the happy path; hiding platform and migration cost; combining unlike consumers; coercing use and calling it product-market fit; and keeping a proposition after evidence shows the problem, mechanism, or scope is wrong.

### Compact example

For application teams creating short-lived development environments, the current ticket-and-script journey has a measured median elapsed time of two days, repeated identity errors, and uncertain cleanup. A governed environment capability accepts project, owner, data class, region, and expiry, then provisions and reconciles an observable environment. The hypothesis predicts more eligible requests will reach verified readiness without support within 20 minutes, without increasing isolation failures, abandoned resources, accessibility barriers, operator interrupts, or cost per active environment. Evidence is segmented by workload and experience; the proposition is revised if unsupported exceptions or recovery burden dominate.

### Connections

Retrieve consumer and job evidence from [PLAT-002](002-platform-consumers-and-jobs-to-be-done.md), load boundaries from [PLAT-003](003-developer-cognitive-load.md), product lifecycle from [PLAT-004](004-platform-as-product.md), capability distinctions from [PLAT-007](007-platform-capabilities-versus-tool-catalogs.md), and team ownership from [PLAT-009](009-platform-team-boundaries.md). The next block begins with [developer journeys](../roadmap.md#block-02--developer-experience-and-platform-interfaces). Later modules own adoption funnels, discovery, roadmaps, economics, outcome measurement, and strategy defense in depth.

## Governing Question

How can a platform team state why a particular group should choose and sustain use of a capability, in language precise enough to guide product scope, architecture, investment, measurement, and stopping decisions?

The proposition must work for three related perspectives. Consumers need a better way to accomplish a job. The organization needs improved flow, quality, risk, cost, or strategic capability. The platform team needs a supportable product whose benefits justify its own build and operating burden. A proposition that benefits one perspective by silently overloading another is incomplete.

Value is comparative. “Self-service environments are valuable” is not testable until the team knows which consumers, which environments, what they do today, what is wrong with that journey, and what the platform changes. The best decision may be better documentation, provider-direct enablement, an enabling-team engagement, or no new platform capability.

## Why This Matters

Platforms are indirect products. They rarely deliver revenue or public outcomes alone; they alter how other teams build and operate the products that do. This leverage is attractive, but it also makes attribution easy to exaggerate. A platform can plausibly influence a delivery outcome without being its sole or primary cause.

Current CNCF guidance defines a platform around user needs, recommends prioritizing common cases, and ties platform success to the success of users and products. Current DORA guidance emphasizes critical journeys, clear task feedback, task success, developer experience, adoption/retention, delivery outcomes, and balanced measurement; it also reports that platform effects can be mixed. These sources support a bounded claim, not “platform equals productivity.”

Discovery must precede solution commitment. Current GOV.UK service guidance asks teams to understand who users are, what they try to do, how they do it now, frustrations, the end-to-end journey, support work, and barriers including accessibility. Its benefits guidance requires a baseline because improvement cannot be demonstrated without a starting point, and explicitly allows stopping when evidence does not justify continuation.

The Value Proposition Canvas usefully separates consumer jobs, pains, and gains from products, pain relievers, and gain creators. It is a framing tool, not evidence. Interviews, observation, operational data, support logs, experiments, incidents, cost records, and task outcomes must test whether the proposed fit exists in the actual organization.

A precise proposition constrains architecture. If value comes from independent recovery, the platform needs observable state and recovery interfaces, not merely scaffolding. If value comes from policy consistency, it needs authoritative decisions and evidence, not a checklist. If value comes from reduced coordination, the normal path cannot depend on tickets. Product language without a mechanism cannot guide engineering.

## Prerequisites and Retrieval

Retrieve the complexity-transfer model from PLAT-001, segmentation and jobs from PLAT-002, cognitive-load evidence from PLAT-003, product lifecycle from PLAT-004, self-service semantics from PLAT-005, roads and alternatives from PLAT-006, capability-versus-tool distinctions from PLAT-007, provider responsibility from PLAT-008, and team boundaries from PLAT-009.

You should understand user research, workflow observation, product hypotheses, baselines, metrics, confounding, service ownership, total cost, risk, accessibility, and lifecycle decisions. Statistical inference is helpful but not required; the chapter emphasizes honest claim structure and evidence design.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish a platform value proposition from a vision, slogan, feature list, business case, mandate, and roadmap;
2. identify segment-specific jobs, contexts, alternatives, pains, gains, constraints, and retained obligations;
3. write a falsifiable value hypothesis with mechanism, outcomes, horizon, evidence, guardrails, and stop conditions;
4. trace claims from platform capability through task outcomes to delivery and organizational effects without over-attribution;
5. establish baselines and eligible denominators for adoption, task success, burden, quality, safety, and cost;
6. compare capability, enablement, provider-direct, local, and no-build alternatives; and
7. revise scope or stop investment when evidence contradicts the proposition.

## Core Exposition

### Start with a bounded consumer and job

“Developers” is usually too broad. Application developers, data scientists, security engineers, service owners, and platform providers perform different work under different obligations. Even application teams vary by workload, maturity, consequence, geography, and operating model.

Define the segment through characteristics that alter the job or product contract. “Teams deploying stateless internal HTTP services under the standard data policy” is actionable. “Java developers” may not be, unless language changes the journey. Include disabled people, new joiners, experts, support staff, and teams that do not currently use the platform when they are part of the affected population.

State the job as desired progress: create an operable environment, release a verified artifact, recover a service, obtain a short-lived credential, or understand production health. Do not translate a request such as “give us a dashboard” directly into the job. Ask what decision or outcome the dashboard enables.

### Observe the current alternative end to end

Every job already has an alternative, even if that alternative is delay, manual coordination, unsafe work, or abandonment. Map trigger, discovery, decisions, tools, handoffs, waits, execution, feedback, exceptions, failure, recovery, evidence, support, cost, and retirement.

Measure before redesign where feasible. Capture attempts, eligible population, completion, elapsed and active time, waits, rework, errors, support, incidents, quality, cost, accessibility barriers, operator effort, and abandoned or avoided work. Preserve distributions and contexts; a median can hide a small group experiencing severe harm.

Do not assume the current alternative is universally bad. Local scripts may be fast for expert teams. A ticket may contain legitimate human judgment. Provider-direct use may expose necessary specialist semantics. The platform must improve total experience for the segment it claims, not defeat every alternative.

### Separate jobs, pains, gains, and constraints

Jobs describe progress. Pains describe evidenced obstacles or undesired consequences in the present journey. Gains describe outcomes consumers value, including confidence, independence, reversibility, understandable status, predictable support, and preserved control. Constraints identify non-negotiable context such as data location, accessibility, latency, safety, budget, or authority.

Prioritize pains by frequency, severity, consequence, affected population, strategic relevance, and addressability. Frequency alone can favor minor annoyances over rare catastrophic failure. Severity alone can pull the platform into specialist work it cannot competently own. Preserve the judgment and uncertainty behind prioritization.

Some consumer pain is intrinsic to domain responsibility. A platform should not “reduce load” by deciding whether a medical result is valid, whether financial risk is acceptable, or which customer promise to make. Value often comes from making those decisions explicit and easier to execute, not hiding them.

### Write the complete value hypothesis

Use

$$
V=(U,J,K,A,C,M,O,T,E,G,R,S),
$$

where $U$ is segment, $J$ job, $K$ context, $A$ current alternative, $C$ capability, $M$ mechanism, $O$ bounded outcomes, $T$ horizon, $E$ evidence plan, $G$ guardrails, $R$ retained obligations, and $S$ stop or revision criteria.

A readable form is:

> For **segment $U$** doing **job $J$** in **context $K$**, compared with **alternative $A$**, capability **$C$** will use **mechanism $M$** to improve **outcomes $O$** within **horizon $T$**, evidenced by **$E$**, without violating **guardrails $G$** or absorbing **obligations $R$**. We will revise or stop when **$S$** occurs.

Each element can fail independently. The pain may be overstated; the segment may be incoherent; the mechanism may not change the bottleneck; adoption may be impossible; an outcome may improve while recovery regresses; or operating cost may exceed repeated burden removed.

The following synthetic gate checks structural completeness for four hypotheses. It does not validate the claims or rank their importance.

<!-- bijux-verify: {"id":"value-hypothesis-gate","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"hypotheses=4\nready=2\nsegments=3\nmissing-baseline=1\nmissing-stop=1\n","stderr":""}} -->
```python
hypotheses = [
    {"segment": "app", "baseline": True, "mechanism": True, "outcome": True, "horizon": True, "guardrail": True, "stop": True},
    {"segment": "app", "baseline": False, "mechanism": True, "outcome": True, "horizon": True, "guardrail": True, "stop": True},
    {"segment": "data", "baseline": True, "mechanism": True, "outcome": True, "horizon": True, "guardrail": True, "stop": False},
    {"segment": "ml", "baseline": True, "mechanism": True, "outcome": True, "horizon": True, "guardrail": True, "stop": True},
]

required = ("baseline", "mechanism", "outcome", "horizon", "guardrail", "stop")
ready = [item for item in hypotheses if all(item[field] for field in required)]
print(f"hypotheses={len(hypotheses)}")
print(f"ready={len(ready)}")
print(f"segments={len({item['segment'] for item in hypotheses})}")
print(f"missing-baseline={sum(not item['baseline'] for item in hypotheses)}")
print(f"missing-stop={sum(not item['stop'] for item in hypotheses)}")
```

### Explain the value mechanism

A mechanism connects what the platform does to how work changes. Common mechanisms include removing repeated translation, automating deterministic fulfillment, making state observable, composing providers, supplying safe defaults, shifting undifferentiated operation to specialists, shortening feedback, preserving evidence, enabling recovery, or creating a supported shared schema.

Avoid “the portal improves productivity.” A stronger chain is: one declaration replaces five handoffs; automated validation detects invalid requests immediately; durable status externalizes progress; supported rollback reduces recovery coordination; therefore eligible teams complete the deployment job with less wait and fewer ambiguous failures.

Mechanisms reveal missing architecture and ownership. If the proposition depends on reliable self-service, a request form backed by manual work cannot realize it. If it depends on reduced cognitive load, exposing every provider option contradicts it. If it depends on autonomy, a platform engineer in the loop for routine completion breaks the chain.

### Build a layered evidence chain

Separate four evidence layers:

1. **Problem evidence:** the job, current journey, frequency, pain, barriers, cost, risk, and affected segments exist.
2. **Solution evidence:** consumers can understand and complete the proposed journey; the mechanism operates as designed.
3. **Outcome evidence:** task success, time, effort, quality, recovery, support, safety, accessibility, and cost change relative to a baseline or comparison.
4. **System-effect evidence:** delivery, organizational, customer, regulatory, or financial outcomes change, with plausible attribution and alternatives considered.

Confidence usually weakens downstream. A platform can directly observe its operation and task completion. It may contribute to delivery performance. Revenue, mission outcome, or customer satisfaction usually depends on many additional variables. Report contribution and uncertainty rather than assigning all downstream change to the platform.

Combine methods. Observation reveals workarounds; interviews reveal meaning and context; telemetry measures operations; support logs reveal recurring friction; incidents reveal degraded journeys; cost records reveal allocation; experiments or staggered rollout strengthen comparisons. One method rarely covers the proposition.

### Define value for consumers, organization, and operators

Consumer value can include task completion, independence, lower active and wait time, clearer decisions, reliable feedback, safer defaults, recoverability, learning, and retained domain control. Organizational value can include delivery flow, quality, risk reduction, evidence, consistency, strategic option value, and reduced duplication.

Platform sustainability includes build and run cost, on-call load, support, change, provider cost, migration, retirement, and cognitive load. A capability that saves ten teams a little effort while permanently consuming a large specialist team may not be valuable. A costly capability can still be justified when it prevents high-consequence harm or enables a strategic class of work.

Do not force every effect into money. Monetized developer hours often assume every saved minute becomes productive output and that reported time is causally attributable. Keep time, safety, quality, autonomy, cost, and option value visible as separate dimensions unless a defensible economic model connects them.

### Design measures before building

For each outcome, define metric, population, unit, source, observation window, baseline, segmentation, uncertainty, owner, and interpretation limit. Use eligible denominators. A data-science workload outside a stateless-service contract should not reduce adoption, and a mandated repository should not count as voluntary choice.

Useful measures include:

- attempted and successful jobs, independent completion, abandonment, and recovery;
- active time, wait time, coordination steps, rework, and time to useful feedback;
- errors, policy decisions, incidents, recovery, drift, and unsafe bypass;
- satisfaction and perceived workload tied to a named journey;
- accessibility success across supported interfaces and assistive technologies;
- support demand, platform interrupts, on-call burden, roadmap displacement, and toil;
- capability and provider cost, consumer cost, cost per successful job, and migration cost; and
- adoption depth, retention, valid alternatives, exceptions, and reasons for non-use.

Metrics are signals, not the proposition. Faster provisioning with worse cleanup can shift cost into the future. High satisfaction can coexist with unsafe defaults. Low ticket volume can mean excellent self-service or abandonment. Interpret bundles through research and operational review.

### Compare alternatives and opportunity cost

Evaluate at least: improve the current process; documentation or enablement; provider-direct access; compose an existing internal service; build a platform capability; let teams own the work; or do nothing now. Include opportunity cost: what higher-value platform work will not happen?

Compare total lifecycle burden and authority fit, not only implementation speed. A thin integration may deliver most value. A full abstraction may be justified for a recurrent undifferentiated job. A specialist case may belong outside the platform. If no option produces sufficient value within guardrails and capacity, stop.

Leadership mandate can establish an organizational constraint but cannot prove consumer value. When use is mandatory, study task outcomes, workarounds, exceptions, depth, and retained alternatives. Make compliance and standardization goals explicit rather than presenting coerced adoption as preference.

### Revise, narrow, expand, or stop

A proposition is a living hypothesis. Narrow it when one segment benefits and another does not. Change the mechanism when the capability does not address the real bottleneck. Expand only after evidence shows adjacent jobs share enough semantics and the team has lifecycle capacity.

Set decision dates and thresholds before sunk cost dominates. Stop or replace a capability when the problem is absent, the alternative is better, harm or operator burden exceeds benefit, the mechanism cannot work under authority constraints, or providers make the custom layer unnecessary. Preserve migration and retirement obligations.

Publish what changed in the proposition: segment, job, promise, evidence, limitations, and decision. Trust improves when the platform team admits a disproven claim. Continuing to build is not evidence of persistence if the value hypothesis has failed.

## Definitions and Notation

$V=(U,J,K,A,C,M,O,T,E,G,R,S)$ is a value hypothesis comprising segment, job, context, alternative, capability, mechanism, outcomes, horizon, evidence, guardrails, retained obligations, and stop/revision conditions.

Let $Y_0$ denote a bounded baseline outcome for the current alternative and $Y_1$ the comparable outcome after or with the platform. $\Delta Y=Y_1-Y_0$ describes an observed difference only. It is not automatically the causal effect of the platform; selection, migration, time, experience, workload mix, mandates, and concurrent changes may explain some or all of it.

Let $B_c$ be consumer burden, $B_p$ platform burden, and $B_o$ burden elsewhere in the organization or among affected parties. A design that lowers $B_c$ by increasing $B_p+B_o$ more severely has transferred rather than necessarily reduced burden. These symbols organize review; they do not assert that unlike harms and benefits can be summed without judgment.

## Mechanisms, Invariants, or Proof Structure

Begin with inclusive research on a complete current journey. Write problem evidence before solution commitments. Create several alternatives and a value hypothesis for each serious candidate. Prototype the riskiest assumption: problem, comprehension, technical mechanism, operating capacity, policy authority, or adoption.

Trace the causal chain:

$$
C \rightarrow M \rightarrow O_{task} \rightarrow O_{delivery} \rightarrow O_{organization}.
$$

At each arrow, state assumptions and competing explanations. The platform controls more of the left side and less of the right. Validate task mechanics first, then examine broader effects with appropriately cautious attribution.

The invariants are segment specificity, a named counterfactual, an operative mechanism, bounded evidence, visible guardrails, retained authority, and a genuine stop path. A proposition that cannot fail is a slogan. A proposition whose only evidence is adoption after alternatives were removed is circular.

Test adversarial cases: novice success/expert slowdown; faster creation/slower recovery; high adoption/mandatory use; lower consumer effort/higher operator toil; standardization/shadow bypass; average improvement/accessibility regression; local cost saving/provider concentration; positive survey/low task success; and delivery improvement concurrent with unrelated team changes.

## Alternatives and Trade-Offs

**One enterprise proposition** is simple to communicate but hides different jobs and obligations. Prefer a portfolio of connected segment propositions under one platform mission.

**Pain-first prioritization** focuses effort on observed problems. It can overvalue frequent minor friction. Balance frequency with severity, consequence, strategic relevance, and addressability.

**Strategic top-down value** can fund cross-cutting capabilities before local demand is obvious. It risks coercive, untested products. Translate strategy into bounded consumer hypotheses and explicit organizational constraints.

**Consumer pull** provides direct demand evidence. Loud teams and current users can dominate, excluding quiet, disabled, new, or unsupported consumers. Research the eligible population, non-users, support staff, and affected parties.

**Economic valuation** helps compare investment and operating cost. False precision can conceal safety, autonomy, quality, and uncertainty. Publish assumptions and keep non-monetized outcomes visible.

**Rapid minimum capability** can test mechanism and task value early. A prototype cannot validate long-term reliability, upgrade, support, cost, or retirement; plan evidence across lifecycle stages.

## Failure Modes and Misconceptions

- **“Our value is developer productivity.”** This lacks segment, job, mechanism, baseline, and bounded outcome.
- **“The platform is the product; Kubernetes is the value.”** Technology is an implementation unless a consumer job depends on its exposed semantics.
- **“Internal users are captive, so alternatives do not matter.”** Tickets, local tools, workarounds, delay, abandonment, and political escalation are alternatives.
- **“Adoption proves fit.”** Mandates, defaults, subsidies, migrations, and removed choices can produce adoption without value.
- **“Satisfaction proves outcomes.”** Sentiment is useful but does not establish task success, safety, reliability, or cost.
- **“Time saved becomes revenue.”** That causal and economic conversion needs evidence; report measured time separately.
- **“More standardization is always valuable.”** It can reduce duplication or erase legitimate domain variation and concentrate risk.
- **“The platform reduces cognitive load.”** State whose load, for which task, and what burden moved to operators or providers.
- **“A business case is a value proposition.”** Funding logic may contain strategic assumptions; the proposition remains a consumer-and-outcome hypothesis.
- **“Stopping wastes prior investment.”** Continuing a disproven capability compounds waste and migration liability.

## Worked Examples

### Example 1

A namespace portal proposition initially claims “faster onboarding.” Research shows creation is quick but policy interpretation and cleanup cause most delay. The team changes the mechanism to declared data class, explainable policy, expiry, and reconciliation. The revised outcome measures verified readiness and cleanup, not form submission.

### Example 2

An expert infrastructure team already provisions provider resources efficiently. A full abstraction would remove features it needs. The platform offers account, identity, cost, and audit enablement instead. The proposition is reduced governance coordination while preserving provider-native control, not universal self-service.

### Example 3

A deployment template gains 95% adoption after leadership mandates it. Task observation finds teams fork generated files and wait for platform engineers during recovery. The platform reports reach but rejects preference and independence claims, then prioritizes lifecycle updates, diagnostics, and rollback evidence.

### Example 4

A database capability reduces median provisioning from two days to 15 minutes, while restore validation and operator pages worsen. The proposition is only partly supported. The team pauses expansion, fixes recovery and capacity, and retains the faster-provisioning result as one bounded outcome.

### Example 5

A platform claims cost savings by consolidating observability. Direct license cost falls, but application teams spend more time locating telemetry and the central on-call load doubles. Total burden evidence contradicts the original mechanism. The team creates workload profiles and clearer ownership before renewing the claim.

### Example 6

An accessible CLI and web journey serve the same environment contract. Keyboard-only and screen-reader tests reveal the web approval state is not announced, while CLI output is inaccessible to a non-terminal user. The proposition includes both segments and fixes each journey rather than averaging completion.

### Example 7

A security capability turns routine image-policy decisions into fast, explainable checks while security retains exception authority. Evidence shows shorter feedback and fewer invalid releases without more exceptions or false blocks. The mechanism and retained obligation are both supported.

### Example 8

A machine-learning team requests GPU self-service. Demand is rare, configurations are specialist, and an external provider already supports the job. A six-week enabling engagement plus governed account vending has lower burden than a managed abstraction. Discovery leads to no new capability.

### Example 9

A release capability launches during an unrelated reorganization and delivery lead time improves. The platform can show task completion and reduced wait in its journey, but cannot assign the entire delivery change to itself. It reports contribution, concurrent changes, and segmented comparisons.

### Example 10

A legacy build capability has declining use, high maintenance, and a better supported provider alternative. The stop condition triggers. The platform funds migration, preserves required provenance, publishes compatibility limits, and retires the service. Value realization includes ending obsolete products responsibly.

## Cross-Program Connections

Product management supplies discovery, segmentation, hypothesis, prioritization, lifecycle, and benefits reasoning. Economics and FinOps contribute opportunity cost, unit cost, allocation, uncertainty, and option value. Statistics and experimentation help distinguish observed differences from causal effects.

Developer experience contributes task observation, perceived workload, accessibility, and journey measures. Reliability and security engineering define guardrails that cannot be traded away by a happy-path speed metric. Organizational design reveals mandates, incentives, queues, authority, and burden transfer.

Systems engineering contributes boundary, feedback, emergent-effects, and lifecycle analysis. Ethics, privacy, accessibility, legal, and domain authorities identify affected parties and retained decisions. A platform value proposition is credible only when its success for internal consumers does not externalize unexamined harm.

## References

- CNCF TAG App Delivery, [*CNCF Platforms White Paper*](https://tag-app-delivery.cncf.io/whitepapers/platforms/), 2023. Current guidance on user needs, platform value, common-case priority, product partnership, measurement, provider composition, and platform-team sustainability.
- DORA, [*Platform Engineering*](https://dora.dev/capabilities/platform-engineering/), updated January 12, 2026. Current critical-journey, task-feedback, task-success, adoption, developer-experience, delivery-performance, and balanced-measurement guidance.
- DORA, [*2024 Accelerate State of DevOps Report*](https://dora.dev/research/2024/dora-report/), corrected edition v2024.3. Empirical platform, user-centeredness, developer-independence, productivity, throughput, and stability findings with survey limitations.
- Alexander Osterwalder, Yves Pigneur, Greg Bernarda, and Alan Smith, *Value Proposition Design*, Wiley, 2014. Practitioner framework for customer jobs, pains, gains, offerings, pain relievers, gain creators, and fit hypotheses.
- Strategyzer, [*The Value Proposition Canvas*](https://www.strategyzer.com/library/the-value-proposition-canvas), updated January 28, 2026. Current official summary of jobs, pains, gains, offerings, pain relievers, gain creators, and evidence-informed fit.
- Clayton M. Christensen, Taddy Hall, Karen Dillon, and David S. Duncan, *Competing Against Luck: The Story of Innovation and Customer Choice*, HarperBusiness, 2016. Practitioner foundation for jobs, circumstances, progress, competing alternatives, and outcome-oriented innovation.
- UK Government Digital Service, [*User Research in Discovery*](https://www.gov.uk/service-manual/user-research/user-research-in-discovery), current Service Manual retrieved 2026. End-to-end current experience, user diversity, barriers, support roles, observation, analytics, and needs discovery.
- UK Government Digital Service, [*Measuring the Benefits of Your Service*](https://www.gov.uk/service-manual/measuring-success/measuring-service-benefits), current Service Manual retrieved 2026. Problem sizing, baselines, alternatives, economic models, benefits evidence, iteration, continuation, and stopping.
- UK Government Digital Service, [*Using Performance Data to Improve Your Service*](https://www.gov.uk/service-manual/measuring-success/using-data-to-improve-your-service-an-introduction), current Service Manual retrieved 2026. Completion, satisfaction, take-up, cost, segmentation, and continuous performance improvement.
- ISO, [ISO 9241-210:2019 — *Human-Centred Design for Interactive Systems*](https://www.iso.org/standard/77520.html), reviewed and confirmed 2025. Human-centered lifecycle principles, multidisciplinary design, context of use, and evaluation against user and organizational requirements.

## Exercises

### Exercise 1

Rewrite “our developer portal creates a single pane of glass and improves productivity” as a complete value hypothesis for one segment and job. Include alternative, mechanism, outcome, horizon, evidence, guardrails, obligations, and stop conditions.

### Exercise 2

Design a baseline study for a database-provisioning journey that currently mixes tickets, provider consoles, team scripts, and abandoned requests. Define eligible denominator, segments, measures, data sources, and limitations.

### Exercise 3

A platform capability shows higher adoption and satisfaction, lower creation time, more policy exceptions, longer recovery, and rising operator interrupts. Decide which parts of its proposition are supported, contradicted, or unresolved and what to do next.

### Exercise 4

Compare a managed platform capability, provider-direct enablement, an enabling-team engagement, and no-build for a rare specialist workload. Evaluate mechanism, authority, total burden, risk, evidence, and option value.

### Exercise 5

Transfer the value-hypothesis model to a regional hospital platform offering clinical-result routing. Define consumers, job, alternative, mechanism, outcomes, guardrails, retained clinical authority, evidence, and stop conditions without equating technical delivery with clinical value.

## Answers to the Exercises

### Answer 1

For application teams deploying stateless internal services under the standard policy, the current journey spans CI configuration, identity requests, deployment scripts, telemetry setup, and support handoffs. A deployment capability accepts owner, workload profile, data class, exposure, and objective, then composes build, identity, rollout, telemetry, policy, and recovery through one observable contract. Within one quarter, more eligible releases should reach verified service readiness and recover from failed rollout without platform assistance, with lower wait and rework than the baseline. Evidence combines task observation, operation telemetry, support, incidents, workload segmentation, and interviews. Guardrails cover change failure, recovery, access, accessibility, cost, and platform on-call. Teams retain code, domain, release-intent, data, and application-recovery decisions. Revise or stop if unsupported workloads dominate, independent recovery does not improve, safety regresses, or operating burden exceeds repeated work removed.

### Answer 2

The eligible denominator is all requests for database classes the proposed capability could support, including attempts that never become tickets and teams using alternatives. Segment by engine semantics, environment, data class, region, experience, and consequence. Map trigger through retirement. Measure attempts, completion, abandonment, active and elapsed time, waits, handoffs, rework, errors, policy decisions, support, recovery, cost, and operator effort. Sources include observation, interviews, service desks, provider audit and billing, scripts, repositories, runtime inventory, incidents, and surveys tied to the job. Reconcile duplicate requests and distinguish human-judgment waits from avoidable coordination. Limitations include missing abandoned-work records, self-selection into alternatives, inaccurate active-time recall, concurrent provider changes, and small specialist segments. Publish uncertainty rather than manufacturing a single average.

### Answer 3

Higher adoption supports reach only after qualifying mandate, eligibility, and depth. Satisfaction supports a bounded experience claim. Lower creation time supports the creation mechanism for observed segments. Increased exceptions may contradict fit or guardrails, but could reflect better detection; classify reasons and denominators. Longer recovery contradicts an end-to-end speed or independence proposition. Rising interrupts contradict sustainability. Pause expansion and inspect workload fit, exception authority, failure states, diagnostics, and provider incidents. Preserve the supported creation result, repair recovery and operator load, and retest. If the capability inherently shifts more burden than it removes, narrow or retire it rather than averaging the metrics into success.

### Answer 4

A managed capability is justified when the job recurs, semantics can be standardized, and the platform can own fulfillment, operation, support, and lifecycle; it offers the strongest burden reduction but highest central commitment. Provider-direct enablement fits specialist semantics while centralizing account, identity, audit, cost, and support boundaries; consumers retain operation. An enabling engagement fits a temporary knowledge gap and should end with consumer capability or discovery evidence. No-build is valid when demand, consequence, or strategic value does not justify opportunity cost, or a current alternative is adequate. Compare authority, technical fit, frequency, severity, consumer and operator burden, provider maturity, reversibility, concentration, and learning value. Prototype the riskiest assumption and retain the least irreversible option until evidence supports deeper ownership.

### Answer 5

Consumers include clinicians, laboratory staff, care coordinators, records/privacy staff, support staff, and patients affected by delay or error. The job is to route an authorized, attributable result to the correct care context with understandable status and correction. Current alternatives may include point-to-point interfaces, phone escalation, manual reconciliation, and delayed records. The platform mechanism uses verified identities, canonical routing declarations, provenance, durable delivery state, reconciliation, audit, and escalation. Outcomes include fewer lost or duplicate messages, shorter bounded delay, faster correction, accessible status, and lower coordination. Guardrails include confidentiality, integrity, availability, patient matching, accessibility, clinical urgency, downtime, and human recourse. Laboratories retain result truth and correction; clinicians retain interpretation and treatment; privacy and records authorities retain disclosure and retention decisions. Evidence combines simulations, observed workflows, message traces, reconciliation, incident drills, accessibility research, and clinical-safety review. Stop or narrow if identity uncertainty, unsafe delay, alert burden, inaccessible workflows, or provider limitations cannot remain within approved bounds; successful message transport alone never proves clinical benefit.
