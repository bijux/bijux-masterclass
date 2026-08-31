---
module_id: SYSENG-043
program: Systems Engineering
level: 1
module_number: 43
title: Cost, Schedule, Performance, and Risk
status: complete
last_verified: 2026-08-31
---

# Cost, Schedule, Performance, and Risk

## One-Page Review

### Governing question

How can a systems team make a defensible commitment when cost, schedule, technical performance, and risk are coupled consequences of one evolving architecture, plan, resource model, and evidence base rather than four independent status reports?

### Essential definitions

- A **technical baseline** is the configuration-controlled description of scope, requirements, architecture, interfaces, operational concept, assumptions, maturity, and evidence to which estimates refer.
- A **work breakdown structure (WBS)** organizes the product and associated work into accountable elements; a product breakdown structure and organizational assignments provide complementary views.
- An **integrated master schedule (IMS)** is a logically linked, resource-informed network of activities, dependencies, constraints, milestones, and calendars that represents the authorized work.
- A **life-cycle cost estimate (LCCE)** includes the resources required across development, production/deployment, operations, support, and retirement within a declared boundary and price basis.
- A **technical performance measure (TPM)** tracks a decision-relevant technical quantity against time-phased planned value, tolerance, margin, and action thresholds.
- **Earned value management (EVM)** integrates authorized scope, schedule, and cost for objective performance measurement; it does not by itself establish technical adequacy or forecast a valid completion date.
- **Planned value (PV)** is budgeted cost for scheduled work, **earned value (EV)** is budgeted cost for performed work, and **actual cost (AC)** is recorded cost for performed work.
- **Cost performance index** is (CPI=EV/AC); **schedule performance index** is (SPI=EV/PV). SPI is a budget-based progress indicator, not elapsed-time efficiency.
- A **risk scenario** states what can happen, how likely it is under stated evidence, and the consequences/uncertainty across technical, safety, cost, and schedule objectives.
- **Margin** is controlled headroom within a technical allocation; **contingency** is planned response capacity; **reserve** is budget or schedule held by authorized management for uncertain in-scope work. These are not interchangeable hidden padding.
- A **joint cost and schedule confidence analysis** propagates uncertainty and discrete risks through a cost-loaded logical schedule to estimate the probability of meeting paired cost/date commitments.
- An **estimate at completion (EAC)** is a forecast of total cost under a declared method and assumptions, distinct from the authorized budget at completion (BAC).

### Central model, mechanism, or theorem

Represent the controlled program state at assessment time (t) as

\[
X_t=(B_t,W_t,S_t,C_t,P_t,R_t,E_t),
\]

where (B_t) is the technical/configuration baseline, (W_t) work scope, (S_t) schedule network, (C_t) cost/resource model, (P_t) technical-performance model, (R_t) risk/uncertainty model, and (E_t) evidence/provenance. A forecast is conditional:

\[
(C_f,T_f,P_f)\sim F(X_t,\Theta,U),
\]

where (\Theta) contains explicit estimating/model assumptions and (U) represents uncertainties and risk scenarios with preserved dependence. A commitment is credible only if every component refers to compatible scope, configuration, calendar, price basis, and data date.

For EVM status:

\[
CPI=\frac{EV}{AC},\qquad SPI=\frac{EV}{PV},\qquad EAC_{CPI}=\frac{BAC}{CPI}.
\]

These identities describe or extrapolate budgeted work under assumptions. They do not replace a network schedule forecast, technical-performance assessment, risk analysis, or bottom-up EAC.

### Critical invariants

- Cost, schedule, performance, risk, scope, and evidence use one declared technical baseline, data date, WBS/schedule mapping, lifecycle boundary, and configuration.
- Estimates include all authorized work and enabling products; exclusions, sunk costs, contributions, escalation, exchange rates, and operations/support boundaries are explicit.
- The schedule is complete enough, logically linked, resource-feasible, statused with actual evidence, and free of unexplained constraints or invalid open ends.
- Cost is time-phased through the schedule so delay, resource, escalation, and fixed-versus-variable effects can be represented.
- Technical measures trace to stakeholder outcomes and requirements, carry planned profiles/tolerances/margins, and cannot be inferred from spending or task completion alone.
- Risks are causal scenarios, not colors or generic multipliers; likelihood, technical/cost/schedule consequences, uncertainty, owners, responses, and affected WBS/activities are explicit.
- Shared causes and correlations are preserved. Cost, duration, performance, and risk samples from incompatible scenarios are not combined independently.
- Baseline, management reserve, schedule reserve, technical margin, and accepted risk remain distinct and governed by named authority.
- Actual cost, actual dates, physical accomplishment, configuration, and test evidence are reconciled at the same status date before variance interpretation.
- Forecasts state method, assumptions, confidence semantics, sensitivity, calibration evidence, and limitations; point estimates are never presented as certainty.
- Corrective action addresses causal work and technical evidence, not only favorable metric appearance.
- Replanning and rebaselining preserve original/current baselines, variance history, decision rationale, authorization, and effects on commitments.

### Common failures

Common failures include estimating a vague design; omitting integration, verification, transition, operations, or retirement work; forcing cost to an available budget; treating a target date as a schedule; using disconnected functional schedules; adding arbitrary percentage risk; counting the same risk in base estimates, discrete events, and reserves; assuming all uncertainties are independent; using EVM SPI as a completion-date forecast; earning value before objective accomplishment; reporting green cost while technical margin collapses; consuming technical margin without updating downstream work; hiding schedule reserve in lags; confusing budget with cost estimate; presenting P50 cost and P50 date as a joint 50-percent commitment; transferring risk without verifying supplier capability; and erasing variance history through frequent rebaselining.

### Compact example

Four mutually exclusive, jointly defined outcomes have probabilities 0.55, 0.25, 0.15, and 0.05. Their final cost/date/performance triples are `(118,22,97)`, `(135,27,94)`, `(128,25,96)`, and `(155,31,91)`, where cost is millions, duration is months, and performance is units. Expected values are 125.60, 24.15, and 95.80, but only the nominal outcome meets all three commitments `cost <= 130`, `duration <= 24`, and `performance >= 95`; joint confidence is therefore 0.55. Marginal confidence is 0.70 for cost, 0.55 for date, and 0.70 for performance. Expected values and marginal probabilities cannot substitute for the joint result.

### Connections

SYSENG-041–042 establish decision criteria and auditable trade studies. This module prevents cost, schedule, performance, and risk from becoming disconnected matrix cells. SYSENG-044–045 deepen sensitivity and uncertainty; SYSENG-046–048 deepen readiness and risk; SYSENG-049–050 connect evidence to decision records and architecture selection. Earlier requirements, architecture, interface, integration, and configuration modules define the baseline that makes integrated estimation meaningful.

## Governing Question

What evidence permits leaders to say that a system can deliver the required outcomes, by the needed date, within available resources and acceptable risk—and what should they do when those claims are no longer jointly credible?

The answer is not a dashboard with four colored boxes. Cost can look favorable because difficult work has slipped. Schedule can look favorable because activities are marked complete without passing technical exit criteria. Performance can look favorable because a point prediction ignores uncertainty or an obsolete configuration. A risk register can look controlled because consequences were scored qualitatively and never connected to the cost-loaded schedule. Integrated assessment asks whether all claims describe the same system and future.

## Why This Matters

Engineering decisions move all four dimensions simultaneously. Reducing mass may require expensive materials, supplier qualification, redesign, and verification. Compressing schedule can increase parallel work, coordination, rework exposure, staffing cost, fatigue, and safety risk. Deferring a reliability demonstration can preserve a milestone while widening performance and lifecycle-cost uncertainty. A cheaper architecture may create longer integration paths or recurring operational burdens. The relevant unit of analysis is the coupled scenario, not an isolated metric.

NASA's current Technical Planning guidance requires the technical effort, products, workflows, resources, cost, schedule, and risk constraints to be planned and synchronized with project plans. Its Technical Assessment guidance calls for compatible technical and programmatic status, including technical measures, cost, schedule, and risk. NASA Technical Risk Management defines risk as potential future shortfall across safety, technical, cost, and schedule domains and links risk-informed decisions with continuous risk management.

GAO's current Cost Estimating and Assessment Guide describes a reliable estimate as grounded in purpose/scope, a technical baseline, WBS, assumptions, data, estimating methods, sensitivity/risk analysis, documentation, presentation, and updates with actual cost. Its Schedule Assessment Guide treats a reliable schedule as a model of time and warns that credible cost must account for schedule slippage. NASA's Joint Cost and Schedule Confidence Level guidance similarly requires cost loaded onto a logical schedule, discrete risks mapped to activities, and uncertainty beyond the baseline plan.

Integration is therefore a traceability discipline. Every forecast should answer: which requirements and architecture; which work; which activity logic and resources; which cost basis; which performance profiles; which risk scenarios; which evidence date; and which decision authority? Without those answers, a precise number is merely precise ambiguity.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. stakeholder outcomes, ConOps, mission/use cases, lifecycle, requirements, verification/validation strategy, and success criteria;
2. configuration-controlled system definition, architecture, interfaces, product breakdown, make/buy/reuse decisions, maturity, and enabling products;
3. WBS dictionary, organizational responsibility, statement of work, integrated schedule, resource calendars, milestones, and entry/exit criteria;
4. cost-estimate basis, data sources, normalization, estimating relationships, learning/quantity assumptions, escalation, currencies, reserves, and actual costs;
5. MOEs, MOPs, TPMs, planned profiles, tolerances, margins, models, test results, and technical-debt/defect evidence;
6. risk register and underlying scenarios, likelihood/consequence bases, uncertainty, correlations/common causes, mitigations, triggers, and retirement evidence;
7. baseline-change records, EVM/control-account data where used, supplier reports, independent estimates, schedule-risk analysis, and prior calibration;
8. basic probability, conditional/joint events, expected value, networks/critical paths, cost phasing, sensitivity, and forecast-versus-baseline distinctions.

As a retrieval test, take the statement “we are 60 percent complete, on budget, and low risk.” Ask what physical products passed which criteria, against which configuration, at what data date; whether 60 percent is effort, EV, requirements, tests, or deliverables; which remaining critical-path work exists; what cost and schedule uncertainty remains; and which technical margins are declining. If the answers refer to different baselines or dates, the claim is not integrated.

## Learning Objectives

After completing this module, you should be able to:

1. establish a compatible technical, work, schedule, cost, performance, risk, and evidence baseline;
2. distinguish estimates, budgets, baselines, actuals, forecasts, margins, contingencies, and reserves;
3. build and challenge a logically linked, resource-informed schedule tied to technical exit criteria;
4. connect lifecycle cost to WBS, schedule, architecture, operations, and uncertainty;
5. define TPM profiles with tolerances, margin policy, evidence, and action thresholds;
6. write risk scenarios and map their dependent cost, schedule, and performance consequences;
7. calculate and interpret PV, EV, AC, CPI, SPI, variances, and simple EAC methods without overclaiming;
8. distinguish marginal cost/date/performance confidence from joint confidence;
9. identify double counting, false independence, optimism, baseline gaming, and metric-induced behavior;
10. recommend evidence-based corrective action, reserve use, replanning, or rebaselining with preserved history.

## Core Exposition

**Begin with a decision and commitment frame.** Name the system outcome, authority, lifecycle boundary, target/constraint ranges, decision dates, reversibility, affected stakeholders, funding/resource constraints, and acceptable risk. Separate externally imposed commitments from internal planning targets. A desired date is not evidence that a feasible network exists, and an appropriated budget is not an independent cost estimate.

**Control the technical baseline.** Record requirements, architecture, interfaces, operational scenarios, quantities, environments, quality/assurance level, verification/validation, maturity, supplier assumptions, transition, support, and retirement. Cost and schedule estimates for different configurations cannot be compared as though they describe one plan. When architecture changes, identify the exact WBS, activities, resources, performance predictions, tests, risks, and operational costs affected.

**Build a complete work model.** Derive work from products and lifecycle outcomes, then include systems engineering, management, integration, verification, validation, safety/security, data, facilities, tooling, training, spares, transition, operations, sustainment, and disposal as applicable. Use a WBS dictionary to define inclusions, exclusions, completion criteria, and responsible organization. Avoid both product-only omission and activity buckets that cannot trace to deliverables.

**Construct the schedule as a causal network.** Activities need scope, duration basis, predecessor/successor logic, resources/calendars, responsible owner, and objective finish evidence. Milestones have zero duration and explicit criteria. Minimize hard date constraints and unexplained lags; model real work and approvals. Identify critical and near-critical paths, convergence points, integration dependencies, long-lead items, resource bottlenecks, and external handoffs. Status actual starts/finishes and remaining duration from evidence, not the passage of time.

**Estimate lifecycle cost independently of affordability pressure.** State estimate purpose, technical baseline, WBS, ground rules, assumptions, data, normalization, methodology, time phasing, uncertainty, and documentation. Use analogy, parametric, engineering build-up, learning curves, vendor data, or extrapolation in ranges where they are defensible. Reconcile multiple methods when practical. Distinguish then-year/constant-year currency, price versus cost, sunk versus future, fixed versus time-dependent, recurring versus nonrecurring, and owner versus external contribution.

**Link cost to schedule and resources.** Assign labor, material, facility, contract, and other cost behavior to activities or WBS/schedule mappings. A delay can extend time-dependent labor/facility cost, change escalation, shift procurement quantities, invalidate staff availability, and defer benefits. Some costs remain fixed; some depend on duration, rate, or occurrence. Declare those behaviors rather than applying one uniform delay percentage.

**Plan technical performance through time.** Select measures that predict stakeholder outcomes and reveal design maturity: mass, power, latency, accuracy, throughput, availability, defect escape, reliability, maintainability, human workload, emissions, or domain-specific quantities. Each TPM needs unit, direction, requirement/goal, allocation, planned profile by review/date, current estimate and confidence, margin definition, measurement/model source, configuration, owner, tolerance/alert bands, and response. A favorable average can hide unsafe tails or scenario failures.

**Distinguish margin from uncertainty.** For an upper-bound requirement (L), current expected value (\hat x), and deliberate allocation (A), teams may define requirement margin (L-\hat x) or allocation margin (A-\hat x); the sign convention must be declared. Margin is not automatically confidence. If model uncertainty is (\pm 5) and nominal margin is 3, the requirement is not demonstrated merely because the point estimate passes. Preserve model-form, parameter, manufacturing, environmental, and operational uncertainty.

**Write causal risk scenarios.** A useful statement identifies a present source/condition, a credible future event or scenario, and consequences to named objectives. Record likelihood and consequence basis, affected requirements/WBS/activities, dependent effects, time window, owner, response actions, resources, triggers, residual risk, and retirement evidence. An issue already occurring belongs in issue/change control while its uncertain downstream consequences may remain risks.

**Map risks into the integrated model.** A supplier qualification failure may delay a component, require redesign, add engineering and test cost, consume mass/power margin, and reduce operational reliability depending on the replacement. These consequences belong to one sampled scenario. Mapping only the schedule delay and adding a separate generic cost-risk multiplier either omits or double counts causal effects.

**Represent correlation and common cause.** Labor-rate inflation affects several work packages; a shared test facility creates schedule dependence; one immature interface can drive software, hardware, integration, and performance outcomes; weather can affect multiple field activities. Use explicit common variables, conditional scenarios, or defensible correlations. Independent sampling should be a justified model choice, never a spreadsheet default.

**Separate base, uncertainty, contingency, and reserve.** The base plan represents identified scope under declared estimating semantics. Uncertainty describes imperfect knowledge and variability. Contingency is planned response work/resource for defined circumstances. Management reserve covers unknown-but-in-scope work under controlled authority; schedule reserve protects a commitment at an appropriate network location; technical margin protects allocations. Do not bury reserve as inflated durations, undisclosed cost factors, or relaxed performance.

**Use EVM as one evidence stream.** Establish an authorized, time-phased performance measurement baseline with objective earning methods. At a status date:

\[
CV=EV-AC,\qquad SV=EV-PV,
\]

\[
CPI=EV/AC,\qquad SPI=EV/PV.
\]

Positive/negative variances require causal investigation. A common cost extrapolation is (EAC=BAC/CPI) when cumulative cost efficiency is assumed to continue; another is (EAC=AC+(BAC-EV)) when remaining work is assumed to perform to plan. Bottom-up EAC should incorporate remaining scope, current architecture, resource plan, schedule, risks, and performance evidence. SPI approaches one at completion by construction and does not model activity logic, so use schedule network/risk analysis for dates.

**Tie earning to technical accomplishment.** Objective completion criteria may include approved design data, built units, passing tests, accepted interfaces, or verified requirements. Level-of-effort earning can be appropriate for genuinely time-based support but should not mask discrete product work. Reconcile EV with TPM trends, defects, rework, review findings, and delivered configuration. Spending less because a critical test slipped is not favorable performance.

**Forecast jointly.** Generate coherent cost/date/performance outcomes from the linked network, resource/cost behavior, performance model, discrete risks, and uncertainty. For thresholds (C^*,T^*,P^*) define:

\[
P_C=Pr(C_f\le C^*),\quad P_T=Pr(T_f\le T^*),\quad P_P=Pr(P_f\ge P^*),
\]

and

\[
P_J=Pr(C_f\le C^*,T_f\le T^*,P_f\ge P^*).
\]

Generally (P_J) is not the minimum, product, or average of marginals without special dependence assumptions. A P50 cost and P50 date selected from separate curves do not constitute 50-percent joint confidence.

**Use distributions responsibly.** Distribution shapes and ranges should come from historical data, estimating-method error, supplier evidence, structured expert judgment, or physical bounds. Document whether estimates are means, modes, medians, or deterministic baselines. Validate simulation convergence and impossible outcomes; inspect tail drivers and scenario traces. Numerical precision must not exceed input credibility.

**Analyze sensitivity and alternatives.** Vary technical baseline, quantity, architecture, staffing, productivity, learning, supplier, resource calendar, integration logic, test strategy, operational demand, uncertainty ranges, risk occurrence, correlation, escalation, and reserve strategy. Identify which changes improve the joint outcome rather than shifting harm between dimensions. Compare staged demonstrations, modularity, descoping, additional resources, schedule relief, alternate suppliers, and reversible decisions with their own transition risks.

**Assess trends and thresholds.** Review current value, planned profile, variance, forecast at completion, rate of change, uncertainty, and downstream impact. Green/yellow/red thresholds are routing aids, not conclusions. A measure inside tolerance but rapidly deteriorating may demand action; a red measure may be explainable and recoverable. Track risk burn-down by retired uncertainty and verified mitigation effect, not number of register rows closed.

**Choose corrective actions causally.** State the shortfall, root and contributing mechanisms, affected baseline, candidate actions, expected cost/schedule/performance/risk effects, evidence, owner, deadline, and success/stop criteria. Update the integrated forecast before approval. Adding people to a constrained integration task may increase coordination and rework; deleting verification may improve a date while reducing evidence and increasing operational risk.

**Govern change and reserve.** Define who can change scope, baseline dates, budgets, allocations, risk acceptance, and reserves. Record request, cause, alternatives, impacts, decision, source of funds/time/margin, and residual commitment confidence. Distinguish corrective replanning within control-account detail from rebaselining an approved measurement baseline. Never rewrite history to make past variance disappear.

**Conduct independent challenge.** Review baseline completeness, WBS/schedule logic, resource feasibility, cost data/methods, technical measures, risk mapping, correlation, uncertainty, reserves, EVM earning, status evidence, sensitivity, and calibration. Independence does not make assumptions true; it reduces motivated reasoning and hidden inconsistency.

**Communicate a bounded decision.** Show baseline and forecast, marginal and joint confidence, top drivers, technical margins, critical/near-critical paths, reserve posture, evidence gaps, alternate actions, thresholds, and dissent. State what is known, modeled, assumed, excluded, and undecided. If no alternative meets commitments with acceptable evidence, say so and request a commitment change or information-producing action.

The following checker evaluates four coherent scenarios. It deliberately keeps each scenario's cost, duration, and performance together.

<!-- bijux-verify: {"id":"integrated-outcome-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"probability_sum=1.00\nexpected_cost=125.60\nexpected_duration=24.15\nexpected_performance=95.80\nconfidence_cost=0.70\nconfidence_duration=0.55\nconfidence_performance=0.70\nconfidence_joint=0.55\nexpected_outcome_meets_all=0\nevidence=declared_scenarios_only\n","stderr":""}} -->
```python
scenarios = [
    {"name": "nominal", "p": 0.55, "cost": 118, "duration": 22, "performance": 97},
    {"name": "integration", "p": 0.25, "cost": 135, "duration": 27, "performance": 94},
    {"name": "supplier", "p": 0.15, "cost": 128, "duration": 25, "performance": 96},
    {"name": "combined", "p": 0.05, "cost": 155, "duration": 31, "performance": 91},
]
limits = {"cost": 130, "duration": 24, "performance": 95}

def expected(name):
    return sum(row["p"] * row[name] for row in scenarios)

def meets(row, names):
    checks = {
        "cost": row["cost"] <= limits["cost"],
        "duration": row["duration"] <= limits["duration"],
        "performance": row["performance"] >= limits["performance"],
    }
    return all(checks[name] for name in names)

def confidence(*names):
    return sum(row["p"] for row in scenarios if meets(row, names))

expected_row = {name: expected(name) for name in limits}
print(f"probability_sum={sum(row['p'] for row in scenarios):.2f}")
print(f"expected_cost={expected_row['cost']:.2f}")
print(f"expected_duration={expected_row['duration']:.2f}")
print(f"expected_performance={expected_row['performance']:.2f}")
for name in limits:
    print(f"confidence_{name}={confidence(name):.2f}")
print(f"confidence_joint={confidence(*limits):.2f}")
print(f"expected_outcome_meets_all={int(meets(expected_row, limits))}")
print("evidence=declared_scenarios_only")
```

The expected triple fails the duration threshold, but even an expected triple that passed would not establish joint confidence: it may combine averages that no realizable scenario produces.

## Definitions and Notation

Let (B) denote the technical baseline; (W) WBS/work scope; (G=(V,E)) the schedule network; (r) resources/calendars; (C_f,T_f,P_f) final cost, time, and technical performance; (R) risk scenarios; and (d) the common data date.

Compatibility predicate:

\[
K(B,W,G,C,P,R,E,d)=true
\]

only when scope, configuration, mappings, units, price basis, calendars, status, and evidence are mutually consistent. Arithmetic on incompatible inputs does not repair (K=false).

For activity (j), duration (D_j), cost behavior (C_j), predecessors (pred(j)), and finish (F_j):

\[
ES_j=\max_{k\in pred(j)}F_k,\qquad F_j=ES_j+D_j
\]

before calendar/resource effects. Criticality is scenario dependent when durations, logic, or resources vary.

At status date (d), EVM quantities are:

\[
PV_d=\text{budgeted work scheduled},\quad EV_d=\text{budgeted work accomplished},\quad AC_d=\text{actual cost incurred}.
\]

Common diagnostics:

\[
CV=EV-AC,\ SV=EV-PV,\ CPI=EV/AC,\ SPI=EV/PV,
\]

\[
EAC_1=AC+(BAC-EV),\qquad EAC_2=BAC/CPI.
\]

Neither EAC is universally correct. Select assumptions from causal evidence and compare with a bottom-up forecast.

For a lower-is-better TPM with limit (L), define margin (M=L-\hat x) under a declared convention. For upper-is-better, (M=\hat x-L). Report uncertainty and configuration with (M).

For scenarios (s\in S) with coherent joint probability (p_s):

\[
E[C_f]=\sum_sp_sC_s,\quad Pr(C_f\le C^*,T_f\le T^*,P_f\ge P^*)
=\sum_sp_sI_s,
\]

where (I_s=1) only if all three conditions hold in scenario (s).

## Mechanisms, Invariants, or Proof Structure

**Mechanism 1—baseline compatibility.** Frame commitments and control one technical baseline, work model, schedule, cost basis, performance model, risk model, evidence date, and mappings.

**Mechanism 2—causal planning.** Represent product work, activity logic, resources, cost behavior, technical profiles, integration/verification evidence, and operational consequences.

**Mechanism 3—status reconciliation.** At one data date reconcile actual cost/dates, objective physical accomplishment, technical configuration/results, issues, and risk changes.

**Mechanism 4—joint forecasting.** Propagate uncertainty and discrete scenarios through linked cost, schedule, and performance models while preserving common cause and correlation.

**Mechanism 5—challenge and action.** Compare forecast to commitments, examine drivers/sensitivity/alternatives, choose causal corrective actions, govern margin/reserve, and preserve baseline history.

The integrity argument is conditional: if the baseline is complete and compatible, models and mappings are adequate, evidence is current, uncertainty/dependence are credible, computation is correct, and governance is legitimate, then the forecast supports a bounded decision. No metric or simulation proves those premises automatically.

## Alternatives and Trade-Offs

**Bottom-up estimates** expose task detail and accountability but can inherit local optimism and omit system effects. **Parametric/analogy estimates** provide independent calibration but require comparable historical data and valid ranges. Reconcile them rather than averaging unexplained disagreement.

**Deterministic baselines** communicate a workable plan. **Probabilistic forecasts** show uncertainty and confidence. A probabilistic model built on broken logic is not more credible merely because it has many trials.

**Integrated detailed models** preserve traceability but may be expensive and fragile. **Analysis-level models** make uncertainty analysis tractable but must reconcile to the IMS, WBS, cost estimate, risks, and technical model without losing critical dependencies.

**Schedule compression** may use resequencing, scope change, additional capacity, shift work, parallelism, prototypes, or decision acceleration. Each affects rework, cost, quality, safety, and technical risk differently. “Work harder” is not a schedule strategy.

**Technical margin** can absorb variability and design evolution; aggressive allocations may reduce mass/power/capacity but increase redesign risk. Margin policy should match maturity and consequence.

**Risk avoidance, mitigation, transfer, acceptance, and research/prototyping** offer different expected outcomes and residual risks. Contract transfer does not transfer mission consequence when the supplier fails.

**One integrated dashboard** helps leadership see coupling. **Domain-specific analyses** retain depth. Link both through governed data and drill-down evidence; do not compress all judgment into one red/yellow/green cell.

## Failure Modes and Misconceptions

**“The budget is the cost estimate.”** A budget is an authorization/constraint; an estimate is an evidence-based forecast. Forcing one to equal the other hides the decision gap.

**“The milestone date proves the schedule.”** A date without complete work, logical dependencies, resources, uncertainty, and exit evidence is a target.

**“SPI 0.90 means ten percent late.”** SPI is EV/PV in budget units and does not measure elapsed-time slippage or network completion date.

**“Under budget means healthy.”** AC can be low because work is late, capability is missing, or defects/rework remain. Interpret AC with EV, schedule logic, TPMs, quality, and risks.

**“A passing point estimate satisfies the requirement.”** Margin must be interpreted with uncertainty, scenario range, model validity, and verification evidence.

**“The risk register already covers uncertainty.”** Discrete named events do not automatically cover estimating error, duration variability, correlation, model form, or unknown interactions.

**“Add twenty percent risk.”** An arbitrary factor has no causal mapping, dependence structure, or decision value and may duplicate hidden conservatism.

**“P50 cost plus P50 date is a P50 joint plan.”** Marginal quantiles do not state the probability of satisfying both conditions together.

**“Reserve is free scope.”** Reserve has defined ownership and purpose; using it changes remaining confidence and must be authorized and recorded.

**“Rebaseline to restore green status.”** Rebaselining may be legitimate after authorized scope/plan change, but it must preserve prior baselines and variance history.

## Worked Examples

### Example 1

**Baseline incompatibility.** Cost uses architecture revision C with two redundant processors; schedule uses revision B with one processor and no failover test; performance uses revision C simulation; the risk register assumes a reused processor that was removed. Summing these reports creates no valid forecast. Freeze a common configuration/data date, map deltas to WBS/activities/cost/TPMs/risks, then reassess.

### Example 2

**EVM with bounded interpretation.** At month 10, (PV=50), (EV=45), (AC=60), and (BAC=100) million. Thus (CV=-15), (SV=-5), (CPI=0.75), and (SPI=0.90). If cumulative cost efficiency continued, (EAC=100/0.75=133.33). These values warrant investigation; they do not prove a 22.22-month finish from a 20-month baseline or show whether delivered work meets performance.

### Example 3

**Critical-path migration.** A test activity has five days float, but a shared chamber becomes unavailable if supplier delivery slips six days. In that scenario test becomes critical and the delay also adds storage, facility, and engineering cost. Deterministic float and independent cost risk miss the coupled effect; model supplier delivery and chamber calendar in the same trace.

### Example 4

**Technical margin with uncertainty.** Maximum latency is 120 ms. Prediction is 116 ms with model/measurement uncertainty approximately ±8 ms. Nominal margin is 4 ms, but plausible outcomes exceed the limit. The team improves the model/test evidence, reduces latency, or changes allocation under authority; it does not label the requirement green from the mean alone.

### Example 5

**Risk double counting.** Base labor already includes expected integration rework from historical projects. A Monte Carlo model adds duration variability calibrated from the same projects, then a discrete “integration rework” event adds full cost/delay again. Review conditional definitions and data; separate ordinary variability from exceptional event consequences or explicitly model overlap.

### Example 6

**Marginal versus joint confidence.** The embedded four-scenario model gives cost confidence 0.70 and performance confidence 0.70, yet joint cost/date/performance confidence is 0.55 because the supplier scenario meets cost/performance but misses date. Multiplying marginals would give 0.2695 and is also wrong because outcomes are dependent.

### Example 7

**Reserve draw.** A verified new interface condition requires 4 million and three weeks of in-scope redesign/test. The authority approves cost and schedule reserve. The record shows cause, work, affected baseline, remaining reserves, technical margins, new joint forecast, and risk reduction. The team does not spread the variance across unrelated accounts or call reserve use cost avoidance.

### Example 8

**Schedule compression trade.** Parallel hardware/software integration saves a nominal month but freezes interface assumptions earlier, adds a simulator, and raises rework risk. Compare the coherent accelerated scenario—including simulator cost, interface-change probability, safety/test workload, staffing limits, and rollback—with serial integration. Calendar gain alone is not the decision criterion.

### Example 9

**Supplier “risk transfer.”** A fixed-price supplier owns overrun cost contractually, but late delivery can still delay system integration and replacement may degrade performance. The project models mission consequences, supplier financial/capacity evidence, surveillance, alternate source lead time, interface/data rights, and acceptance tests. Procurement allocation does not erase system risk.

### Example 10

**Corrective action and history.** A reliability-growth test finds twice the predicted failure rate. The team preserves the original baseline/result, updates the reliability model and operational cost, adds redesign and verification work, examines schedule/resource paths, forecasts confidence, and records authority choice among redesign, operational mitigation, requirement relief, or cancellation. It does not edit the old prediction and declare trend recovery.

## Cross-Program Connections

**Platform engineering.** Platform roadmaps integrate service objectives, adoption, migration, capacity, staffing, security, reliability, cloud/vendor cost, and developer performance; delayed adoption can alter both cost and realized value.

**API and service engineering.** Protocol or decomposition choices couple latency/availability, delivery sequencing, observability, operational staffing, migration, and incident risk. Story completion cannot substitute for contract/conformance evidence.

**Data engineering.** Data-platform plans couple throughput/freshness/correctness, storage/compute cost, backfill and replay duration, governance, schema migration, privacy, and operational risks through workload scenarios.

**Object-oriented programming.** Architecture quality, defects, build/test evidence, team capability, dependency choices, and evolution cost should be forecast together rather than treating code volume as accomplishment.

**Functional programming.** Immutability, effect management, type evidence, runtime behavior, ecosystem maturity, training, migration, and operations create coupled lifecycle tradeoffs that require workload and team evidence.

## References

1. NASA, *Systems Engineering Handbook, Section 6.1: Technical Planning*, current web edition. <https://www.nasa.gov/reference/6-1-technical-planning/>
2. NASA, *Systems Engineering Handbook, Section 6.4: Technical Risk Management*, current web edition. <https://www.nasa.gov/reference/6-4-technical-risk-management/>
3. NASA, *Systems Engineering Handbook, Section 6.7: Technical Assessment*, current web edition. <https://www.nasa.gov/reference/6-7-technical-assessment/>
4. NASA, *Systems Engineering Handbook, Section 6.8: Decision Analysis*, current web edition. <https://www.nasa.gov/reference/6-8-decision-analysis/>
5. NASA, *Cost Estimating Handbook Version 4.0*, official guidance page. <https://www.nasa.gov/ocfo/ppc-corner/nasa-cost-estimating-handbook-ceh/>
6. NASA, *Cost Estimating Handbook, Appendix G: Cost Risk and Uncertainty Methodologies*. <https://www.nasa.gov/wp-content/uploads/2020/11/ceh_appg.pdf>
7. NASA, *Cost Estimating Handbook, Appendix J: Joint Cost and Schedule Confidence Level Analysis*. <https://www.nasa.gov/wp-content/uploads/2020/11/ceh_appj.pdf>
8. U.S. GAO, *Cost Estimating and Assessment Guide: Best Practices for Developing and Managing Program Costs*, GAO-20-195G. <https://www.gao.gov/products/gao-20-195g>
9. U.S. GAO, *Schedule Assessment Guide: Best Practices for Project Schedules*, GAO-16-89G. <https://www.gao.gov/products/gao-16-89g>
10. NASA, *Earned Value Management*, current Project Planning and Control guidance. <https://www.nasa.gov/ocfo/ppc-corner/evm/>

## Exercises

### Exercise 1

At a status date, (PV=80), (EV=72), (AC=90), and (BAC=160) million. Compute CV, SV, CPI, SPI, (EAC_1=AC+(BAC-EV)), and (EAC_2=BAC/CPI). Explain what cannot be concluded about completion date and technical performance.

### Exercise 2

Three mutually exclusive outcomes have probabilities 0.50, 0.30, and 0.20. Their `(cost, duration, performance)` triples are `(90,18,102)`, `(110,21,98)`, and `(130,24,95)`. Commitments are cost at most 115, duration at most 20, and performance at least 97. Compute expected values, each marginal confidence, and joint confidence. Explain why expected values do not define a realizable outcome.

### Exercise 3

A power allocation is 800 W, current best estimate is 760 W, and uncertainty is approximately ±70 W. A proposed feature adds 25 W and two weeks, while mitigation costs 3 weeks now and is expected to reduce power by 60 W. Analyze margin, uncertainty, schedule, evidence, and decision authority without pretending the numbers alone select an action.

### Exercise 4

Audit a plan whose cost estimate omits operations; schedule contains 40 percent hard constraints and no resource calendars; EV is earned by percent elapsed; TPMs use an obsolete architecture; all risks receive a flat 15 percent cost factor; cost/date simulations are independent; and management reserve is embedded in task durations. Design the corrective assessment.

### Exercise 5

Design an integrated assessment for a hospital diagnostic platform facing a fixed regulatory submission window, uncertain algorithm performance across patient groups, supplier hardware lead time, cybersecurity work, clinician training, and lifecycle support. Include baseline, schedule, cost, TPMs, risk/dependence, evidence, reserves, corrective actions, governance, and bounded reporting.

## Answers to the Exercises

### Answer 1

\[
CV=EV-AC=72-90=-18,
\]

\[
SV=EV-PV=72-80=-8,
\]

\[
CPI=72/90=0.80,\qquad SPI=72/80=0.90.
\]

If all remaining work performs at planned cost efficiency,

\[
EAC_1=AC+(BAC-EV)=90+(160-72)=178.
\]

If cumulative cost efficiency persists,

\[
EAC_2=BAC/CPI=160/0.80=200.
\]

The 22-million difference is assumption sensitivity, not a rounding problem. Investigate variance causes and build a bottom-up EAC using remaining scope, resources, schedule, technical state, and risks. SPI 0.90 does not mean ten percent late or support dividing baseline duration by 0.90: it is budgeted-work progress. No values establish critical-path completion, resource feasibility, technical requirement satisfaction, quality, or configuration. Reconcile schedule logic, objective earning evidence, TPMs, defects/rework, and risk before action.

### Answer 2

Expected values are

\[
E[C]=0.50(90)+0.30(110)+0.20(130)=104,
\]

\[
E[T]=0.50(18)+0.30(21)+0.20(24)=20.1,
\]

\[
E[P]=0.50(102)+0.30(98)+0.20(95)=99.4.
\]

The first two outcomes meet cost, so cost confidence is 0.80. Only the first meets duration, so date confidence is 0.50. The first two meet performance, so performance confidence is 0.80. Only the first meets all three; joint confidence is 0.50.

The expected triple `(104,20.1,99.4)` is a probability-weighted summary and is not one of the modeled outcomes. It misses the duration threshold even though half the probability meets the date. Even if all expected values passed, that would not reveal joint confidence. The three quantities must remain together within each causal scenario.

### Answer 3

Under an upper-bound allocation, nominal margin is (800-760=40) W, but the ±70 W uncertainty extends beyond the allocation. Adding the feature changes the estimate to 785 W and nominal margin to 15 W, with unchanged uncertainty only if evidence supports that assumption; the plausible high outcome worsens. A mitigation expected to reduce 60 W would produce a point estimate near 725 W and 75 W nominal margin, but its three-week work, effectiveness uncertainty, interfaces, verification, and new failure modes belong in the integrated forecast. The feature's two-week consequence and mitigation timing may affect different paths; net calendar subtraction is invalid without network/resource logic.

The team should identify performance need/value of the feature, allocation authority, power-model/test evidence, correlated thermal/battery effects, maturity, schedule paths, cost/resources, and risks. It can prototype or test to reduce uncertainty, redesign, defer the feature, change another allocation, accept controlled risk, or request system-level relief. The authorized system/decision owner chooses with affected discipline and safety/operations input. Nominal margin alone neither proves feasibility nor selects the option.

### Answer 4

Pause commitment claims. Establish one current architecture, lifecycle boundary, data date, WBS dictionary, quantities, operations/support/retirement scope, verification/transition work, organizational responsibility, and mapping among products, work, activities, cost, TPMs, and risks. Rebuild or reconcile the LCCE using documented assumptions, normalized data, defensible methods, time phasing, actuals, sensitivity, and independent comparison; keep budget pressure visible rather than forcing equality.

Repair schedule completeness and logic: remove unjustified hard constraints, model real dependencies/approvals, add resources/calendars, objective milestones, actual status, remaining-duration evidence, critical/near-critical paths, and schedule uncertainty. Replace elapsed-time earning for discrete work with objective completion criteria and reconcile PV/EV/AC to the same date. Update TPM profiles to the controlled architecture with margins, uncertainty, models/tests, thresholds, and forecasts.

Replace the 15-percent factor with causal risk scenarios mapped to WBS/activities and dependent technical/cost/schedule consequences. Identify what ordinary estimating uncertainty already contains to prevent duplication. Couple simulations through shared resources, inflation, supplier, interface, test, and performance drivers. Extract hidden duration padding; establish explicit schedule and management reserves with owners, draw rules, and remaining-confidence reporting. Preserve old baselines and variance history, independently challenge the repaired model, disclose exclusions and limitations, then present corrective options or revised commitments.

### Answer 5

Baseline the intended clinical uses/populations/settings, regulatory pathway and submission content, algorithm/software/hardware configuration, data and interfaces, safety/privacy/security requirements, human workflow, supplier/hosting model, quantities, deployment, training, maintenance, updates, support, and retirement. Establish WBS/organization and a logically linked schedule covering representative data, subgroup analysis, design, supplier qualification, cybersecurity, usability/clinical validation, documentation, quality/regulatory reviews, deployment readiness, and lifecycle operations. Model regulator and supplier handoffs, resource calendars, objective exit evidence, critical/near-critical paths, and the fixed window without making it an artificial constraint on every activity.

Estimate lifecycle cost for engineering, data curation/labeling, compute, hardware, integration, verification/validation, quality/regulatory work, security/privacy, clinician time/training, deployment, monitoring, incident response, maintenance, model updates/revalidation, supplier change, and retirement. State price/escalation, volume, utilization, staffing, and time-dependent cost. TPMs include clinically relevant sensitivity/specificity or calibrated utility by patient group and operating point, latency/availability, data quality/drift, cybersecurity and safety evidence, usability/workload, false-alarm burden, maintainability, and submission completeness. Each has profile, threshold, margin, uncertainty, evidence configuration, owner, and action trigger; aggregate accuracy must not hide subgroup harm.

Create dependent scenarios for supplier delay, component substitution, data shift, underperformance in a group, security finding, workflow adoption, regulator questions, and combined events. Map each to affected activities, rework, cost, technical outcomes, deployment, and operational risk; preserve common causes such as one dataset influencing several measures. Distinguish technical margin, planned contingency, management/schedule reserve, and risk acceptance. Use prototypes, early regulator engagement, representative external validation, supplier qualification, threat testing, and clinician simulation as information actions.

At each data date reconcile actual cost/dates, objective accomplishment, current configuration, test/clinical evidence, open findings, TPM forecasts, and risks. Evaluate corrective options such as alternate hardware, staged claims, narrowed indication, schedule relief, more evidence, redesign, or stopping; include their transition and equity consequences. Named authorities govern scope, clinical/safety/security acceptance, regulatory strategy, baselines, and reserves while independent clinical, statistical, human-factors, cybersecurity, quality/regulatory, systems, cost, and schedule reviewers challenge evidence.

Report baseline and forecast, marginal and joint confidence, subgroup results, critical paths, top drivers, reserve/margin posture, evidence gaps, dissent, and reopening triggers. State explicitly that a passing simulation, favorable EVM index, or expected-value forecast does not prove clinical benefit, safety, fairness, cybersecurity, regulatory acceptance, supplier delivery, or lifecycle affordability.
