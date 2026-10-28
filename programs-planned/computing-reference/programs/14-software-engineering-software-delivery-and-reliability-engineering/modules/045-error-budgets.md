---
module_id: SDRE-045
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 45
title: Error Budgets
status: complete
last_verified: 2026-09-06
---

# Error Budgets

## One-Page Review

### Governing question

How can a team convert a service-level objective into an exact, auditable tolerance for bad service and use that tolerance to govern engineering risk without treating unreliability as money to spend or a prediction of future safety?

### Essential definitions

- an **error budget** is the bad-service share allowed by an SLO over its evaluation window;
- the **budget rate** for a lower-bound target $\theta$ is $q=1-\theta$;
- a **valid event** belongs to the SLI denominator after the predeclared population and missing-data rules are applied;
- a **bad event** is a valid event that does not satisfy the SLI's good-event predicate;
- **allowed bad events** is the greatest integral bad-event count that can occur while the completed window still meets the target;
- **consumption** is classified bad service accumulated under the same SLI version and window;
- **remaining budget** is allowed bad service less consumption, floored at zero for display while overspend is reported separately;
- **budget-consumption fraction** compares consumed bad service with the completed window's allowance;
- **burn rate** is observed bad rate divided by the budget rate;
- a **budget policy** maps measured states to pre-agreed actions, owners, exceptions, and evidence;
- a **rolling window** changes continuously, whereas a **calendar window** closes and resets at declared boundaries;
- **forecast time to exhaustion** is a conditional projection that assumes future traffic and bad rate resemble the chosen observation window;
- an **error-budget credit** is engineering tolerance, not an SLA service credit, accounting balance, or permission to harm users.

### Central model, mechanism, or theorem

For $n>0$ valid events, $g$ good events, $b=n-g$ bad events, and target $\theta\in[0,1]$, the exact completed-window allowance is

$$
B(n,\theta)=n-\lceil\theta n\rceil.
$$

The SLO is met exactly when $b\le B$. If a recent observation has bad rate $e$, its burn rate is $r=e/(1-\theta)$ when $\theta<1$. Rate $r=1$ consumes budget at the rate that would use one whole window's allowance over one window; $r>1$ is faster. This rate does not say how much budget remains.

### Critical invariants

- bind the budget to one SLI version, target, scope, and window;
- calculate from valid events after applying declared classification and missing-data rules;
- use integral threshold arithmetic rather than rounded dashboard percentages;
- distinguish accumulated consumption, recent burn rate, and conditional forecast;
- preserve negative remaining budget as an explicit overspend amount;
- do not add overlapping budgets or bad-event counts as though they were disjoint;
- do not let traffic suppression, retries, or changing exclusions manufacture apparent health;
- pre-agree actions, authorities, exceptions, exit criteria, and audit evidence;
- continue urgent incident response and security or safety remediation regardless of budget state;
- treat policy as a learning control, never as punishment or a substitute for user judgment.

### Common failures

Failures include calling the budget planned downtime, using rounded percentages, dividing by zero at a 100% target, comparing counts across changing open-window denominators, assuming a new calendar period erases root causes, confusing remaining fraction with burn rate, forecasting from a burst as if stationary, summing overlapping availability and latency failures, counting retry attempts instead of user operations, excluding missing telemetry after the fact, freezing every change including reliability fixes, granting unlimited exceptions, rewarding teams for consuming budget, and confusing engineering tolerance with contractual credit.

### Compact example

A 99.9% event SLO evaluates 2,000,000 valid logical operations. At least $\lceil0.999\times2{,}000{,}000\rceil=1{,}998{,}000$ must be good, so 2,000 may be bad. After 1,500 bad operations, 500 remain and 75% is consumed. If the latest 50,000 operations contain 120 bad operations, the recent bad rate is 0.24%, hence burn rate is $0.0024/0.001=2.4$. The service has not yet exhausted its completed-window allowance, but the recent rate warrants the action specified for 2.4x burn. Neither number predicts that the rate will persist.

### Connections

[SDRE-043](043-service-level-objectives.md) defines the objective that creates the tolerance. [SDRE-044](044-service-level-agreements.md) separates contractual remedies from engineering controls. [SDRE-046](../ROADMAP.md) next examines toil and automation, including the operational work a budget policy can prioritize.

## Governing Question

Reliability is not free, and perfect reliability is usually neither feasible nor the best use of finite engineering capacity. Yet “some failure is acceptable” is too vague to govern change. An error budget makes the tolerance implied by a service-level objective explicit. It translates a normative target into count, duration, or another SLI-specific allowance that can be measured and connected to decisions.

That translation is easy to misuse. A budget is not an inventory of outages that a team should deliberately cause. It is not a promise that future releases are safe while any positive amount remains. It is not the service credit in an SLA. It cannot rescue a poor SLI, hide concentrated user harm, or tell an incident commander to delay restoration. The governing question is therefore both mathematical and organizational: what exactly is allowed, what has been consumed, how quickly is current behavior consuming it, and what proportionate action follows?

## Why This Matters

Google's SRE book frames error budgets as a way to balance reliability with the pace of change: a product target below 100% leaves a quantified tolerance, and exceeding that tolerance changes the priority given to reliability work [1]. The SRE Workbook makes the organizational preconditions clearer. Stakeholders must accept the SLO, the responsible teams must believe it is normally achievable, and a documented policy must say what happens when budget is exhausted [2]. A number without agreement and action is only reporting.

The published example policy is deliberately not punitive. Its goals are to protect customers from repeated misses and balance reliability with feature work; its example response permits urgent and security fixes while halting other changes after an SLO miss [3]. That exact policy is not universal. A medical system, batch analytics platform, internal developer service, and consumer game can have different harms, authorities, and safe actions. What transfers is the control structure: define state, choose evidence, precommit proportionate responses, record exceptions, and learn.

Burn rate improves time-scale reasoning. The SRE Workbook defines it relative to the SLO: for a 99.9% objective, a constant 0.1% bad rate is 1x, 0.2% is 2x, and 1% is 10x [4]. Multiwindow alerting then combines a long window that establishes material budget consumption with a short window that confirms the problem is still active [4]. This chapter derives the underlying quantities; an alert remains a prediction-and-response mechanism rather than the budget itself.

Error budgets also expose measurement defects. If retry attempts inflate the denominator, missing observations disappear, or a global aggregate hides one failed region, the budget can look healthy while users suffer. Sound budget arithmetic inherits every assumption in the SLI and SLO. Its value is not the elegance of $1-\theta$ but the quality of decisions made from faithfully classified user outcomes.

## Prerequisites and Retrieval

Retrieve service, reliability property, SLI, SLO, valid event, good event, bad event, target, inequality, population, scope, cohort, rolling window, calendar window, retry, missing data, classification, release, incident, risk, policy, owner, exception, evidence, and SLA.

From SDRE-041 retrieve the distinction among availability, reliability, and durability. From SDRE-042 retrieve population and goodness predicates, measurement points, retries, weighting, and unknown observations. From SDRE-043 retrieve target semantics, integral thresholds, window choice, commitment types, and versioning. From SDRE-044 retrieve contractual scope and service-credit calculations; those remedies must remain separate from the engineering budget in this chapter.

## Learning Objectives

After completing this module, you should be able to:

1. derive an event or time error budget from a precisely specified SLO;
2. calculate exact integral allowances without threshold-rounding errors;
3. distinguish allowed, consumed, remaining, and overspent budget;
4. compute and interpret recent burn rate;
5. state the assumptions and limits of exhaustion forecasts;
6. reason about rolling, calendar, and open-window budget semantics;
7. handle retries, missing data, low traffic, cohorts, and overlapping SLIs;
8. design a proportionate error-budget policy with explicit governance;
9. diagnose gaming and perverse incentives in budget use;
10. connect budget evidence to release, reliability, incident, and learning decisions.

## Core Exposition

**Start from a complete objective.** A budget exists only relative to a versioned SLI, comparison operator, target, population, scope, and evaluation window. “Our error budget is 0.1%” is incomplete. The statement must identify 0.1% of what: valid logical requests, scheduled processing intervals, acknowledged writes, or weighted user journeys. It must also declare where observations originate and how exclusions, unknowns, and late data are treated.

For a lower-bound ratio SLO $g/n\ge\theta$, the real-valued budget rate is $q=1-\theta$. The intuitive count $qn$ can be fractional even though events are integral. The correct minimum good count is $\lceil\theta n\rceil$, so the maximum bad count is $B=n-\lceil\theta n\rceil$. At a target of 99% over 101 events, $qn=1.01$ does not allow two failures: 99 good out of 101 is only about 98.0198%. Exact inequality semantics, not decimal formatting, decides.

For a time-based SLI over an evaluation duration $T$, the nominal allowance is $qT$. Time arithmetic must preserve the underlying sampling semantics. A monitor that samples once per minute cannot honestly distinguish every second of downtime; a probe also observes its path, not every user's path. Event-based and time-based budgets answer different questions under variable traffic. Ten unavailable minutes at peak traffic can harm far more operations than ten minutes overnight.

**Name each state explicitly.** Let $c$ be classified bad service accumulated in the window. `Allowed` is $B$. `Consumed` is $c$. `Remaining` for a nonnegative display is $R=\max(0,B-c)$. `Overspend` is $O=\max(0,c-B)$. Keeping both $R$ and $O$ avoids a dashboard that sticks at zero and conceals worsening failure. The consumption fraction $u=c/B$ is defined only when $B>0$; it may exceed 100%.

At target 100%, $q=0$ and no bad events are allowed. Consumption fractions and burn rate divide by zero and must be reported as undefined, not infinity masquerading as an operational metric. The SLO itself remains evaluable: any classified bad event misses it. Hazard-specific zero-tolerance requirements need appropriate safety mechanisms and escalation, not a conventional burn-rate dashboard.

**Separate cumulative state from recent velocity.** Remaining budget summarizes the selected evaluation window. Burn rate summarizes a chosen observation interval. For recent bad-event rate $e=b_h/n_h$ and budget rate $q>0$, burn is $r=e/q$. A 2x burn means the recent interval is consuming bad service twice as fast as the rate that would exactly use one window's allowance across one whole window. It does not mean 2% is consumed, two units remain, or the SLO has already failed.

If a stationary rate $r>0$ continued from the start of an otherwise empty window, the full budget would be consumed after approximately $T/r$. If fraction $f$ of the budget remains and future traffic mix and bad rate stay comparable, a rough time-to-exhaustion projection is $fT/r$. These are conditional counterfactuals. Deployments, repair, diurnal traffic, denominator growth, incident bursts, and delayed telemetry violate stationarity. Label the observation interval and uncertainty; never display a forecast as a deadline guaranteed by the system.

The executable example uses exact rational arithmetic for thresholds. It treats requests as complete logical operations and assumes the recent sample is representative only for calculating its observed burn, not for forecasting.

<!-- bijux-verify: {"id":"calculate-event-error-budget","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"allowed_bad=2000 consumed=1500 remaining=500\nconsumed_fraction=75.00%\nrecent_bad_rate=0.2400% burn_rate=2.40x\n","stderr":""}} -->
```python
from fractions import Fraction


def ceiling(value: Fraction) -> int:
    return -(-value.numerator // value.denominator)


target = Fraction(999, 1000)
valid = 2_000_000
bad = 1_500
allowed_bad = valid - ceiling(target * valid)
remaining = max(0, allowed_bad - bad)

recent_valid = 50_000
recent_bad = 120
recent_bad_rate = Fraction(recent_bad, recent_valid)
budget_rate = 1 - target
burn_rate = recent_bad_rate / budget_rate

print(f"allowed_bad={allowed_bad} consumed={bad} remaining={remaining}")
print(f"consumed_fraction={bad / allowed_bad:.2%}")
print(
    f"recent_bad_rate={float(recent_bad_rate):.4%} "
    f"burn_rate={float(burn_rate):.2f}x"
)
```

**Understand window semantics.** A closed calendar window has a final denominator and final allowance. An open request-based calendar window does not. As traffic arrives, both $n$ and $B(n,\theta)$ can grow. A dashboard that calculates current count allowance is describing the observations so far, not granting failures against unknown future requests. Forecasting period-end budget requires a separately labeled traffic model.

In a rolling window, old good and bad events age out while new ones enter. Remaining budget can increase without any repair because a prior incident leaves the window. That is correct for recent-window evaluation but not evidence that the root cause disappeared. Preserve incident history, longer-range trends, and corrective actions outside the current budget state.

Calendar reset has similar limits. The arithmetic resets at the declared boundary; organizational memory must not. An incident at 23:59 and another at 00:01 may consume two reporting periods while representing one continuing mechanism. Policy should connect repeated incidents, postmortem actions, and unresolved risks across boundaries.

**Keep classification stable.** Apply the SLI's valid-event, goodness, and missing-data rules before budget arithmetic. Reclassifying a known bad event as excluded after observing a miss destroys comparability and invites gaming. Legitimate corrections require provenance: preserve the original result, identify the defect, recompute under a new or corrected version, and explain the decision impact.

Retries are especially dangerous. If one user operation produces three attempts and succeeds on the third, an attempt-level SLI may count two bad and one good while the logical-operation SLI counts one good operation with extra latency. Neither definition is universally right, but the budget must match the user contract. Traffic amplification should not manufacture more allowed failures, and client-abandoned operations must not vanish merely because the server never completed them.

Unknown observations are not automatically good, bad, or invalid. Bound the result when material. If $g$ known good, $b$ known bad, and $u$ unknown observations all belong to the intended population, best-case success is $(g+u)/(g+b+u)$ and worst-case success is $g/(g+b+u)$. A budget decision can proceed only if the policy declares how unresolved uncertainty affects action.

**Protect cohorts and non-substitutable properties.** A global budget can pass while one region, tenant class, accessibility path, or operation fails. Use separately governed cohort objectives when harms or commitments differ. Do not fragment until sparse data becomes meaningless; choose cohorts from user consequence and ownership.

Several SLIs can mark the same operation bad. A request that is both incorrect and slow consumes both its correctness and latency budgets if those are separate objectives. Adding those consumption counts asserts disjointness that does not exist. Keep the budgets separate, use a joint predicate when complete success is the intended property, or compute the overlap explicitly with set operations.

Dependency budgets also do not compose by simple addition unless failure events, traffic, masking, and path selection support that model. An internal dependency target can allocate headroom, but the user-facing budget remains based on observed user outcomes. Caching, fallback, retries, redundancy, and graceful degradation can mask dependency failure; common-cause faults can defeat naive independence assumptions.

**Design policy before crisis.** A useful policy names its purpose, scope, evidence source, owners, decision authority, thresholds, actions, exceptions, escalation, exit criteria, and review cadence. It distinguishes urgent incident mitigation from discretionary change. It also states how measurement disputes are resolved and which artifact records each decision.

Actions should be proportional to risk and reversibility. Healthy budget might permit the normal release process. Rapid burn might require an incident response, rollback, or change hold before the cumulative budget is exhausted. High consumption with no active burn might prioritize corrective work and restrict high-risk launches rather than freeze every safe change. Exhaustion might shift capacity toward reliability until objective evidence and agreed exit criteria are met.

Do not freeze security fixes, safety remediation, or the changes needed to restore reliability merely because they are changes. Predeclare exception categories, approvers, safeguards, duration, and retrospective review. An exception without expiry or evidence is an alternate unwritten policy.

The policy should assign causes for learning and action, not blame. A dependency failure may still harm users and consume the user-facing budget even when another team owns the cause. The consuming team can strengthen fallback, negotiate dependency objectives, revise architecture, or escalate shared risk. Conversely, a measurement defect can produce apparent consumption without user harm; correct the measurement transparently rather than pretending the number is unquestionable.

**Resist perverse incentives.** Teams should not aim to “spend the whole budget.” Unused tolerance is not wasted capital, and deliberate failure can impose asymmetric harm. Nor should they reduce traffic, suppress telemetry, broaden exclusions, or split one population solely to improve the ratio. Evaluate user outcomes, change success, incident recurrence, learning completion, and delivery value together.

Budget policy is a feedback controller with humans in the loop. The SLI provides evidence, the SLO defines acceptable performance, the budget exposes distance and velocity, and policy selects action. Delayed, noisy, biased, or incomplete signals can destabilize that loop. Periodic review must ask whether actions protected users, whether teams could comply, whether thresholds were too sensitive or too slow, and whether the indicator still represents the service.

## Definitions and Notation

Let an event SLI over window $W$ have $n_W>0$ valid events, $g_W$ good events, and $b_W=n_W-g_W$ bad events. For lower-bound target $\theta\in[0,1]$,

$$
\frac{g_W}{n_W}\ge\theta
\quad\Longleftrightarrow\quad
b_W\le n_W-\lceil\theta n_W\rceil.
$$

Define budget rate $q=1-\theta$ and exact integral allowance

$$
B_W=n_W-\lceil\theta n_W\rceil=\lfloor qn_W\rfloor.
$$

The equality follows because $n_W$ is integral. For consumed bad count $c_W=b_W$, define signed balance $A_W=B_W-c_W$, remaining $R_W=\max(0,A_W)$, and overspend $O_W=\max(0,-A_W)$. If $B_W>0$, consumption fraction is $U_W=c_W/B_W$.

For observation interval $H$ with $n_H>0$, observed bad rate is $e_H=b_H/n_H$. When $q>0$, burn rate is

$$
r_H=\frac{e_H}{q}.
$$

For a time SLI with evaluation duration $T$ and bad duration $d_W$, nominal allowance is $D=qT$, signed balance is $D-d_W$, and burn over subwindow duration $h>0$ is $(d_H/h)/q$. Sampling and classification determine what $d_H$ means.

Let $A_j$ be the set of operations bad under objective $j$. For two objectives, the number of distinct affected operations is

$$
|A_1\cup A_2|=|A_1|+|A_2|-|A_1\cap A_2|.
$$

Therefore summing two bad counts double-counts their overlap unless the sets are disjoint.

## Mechanisms, Invariants, or Proof Structure

**Integral allowance proof.** The SLO holds when $g/n\ge\theta$. Multiplying by positive $n$ gives $g\ge\theta n$. Since $g$ is integral, this is equivalent to $g\ge\lceil\theta n\rceil$. Substituting $b=n-g$ yields $b\le n-\lceil\theta n\rceil$. No displayed rounding is part of the decision.

**Budget-rate identity.** For integral $n$, $n-\lceil\theta n\rceil=\lfloor n-\theta n\rfloor=\lfloor(1-\theta)n\rfloor$. This permits exact count computation from either good or bad orientation, provided the target and denominator are identical.

**Burn interpretation.** Over a duration $T$, constant event rate $\lambda$ and bad fraction $e=rq$ produce approximately $\lambda Trq$ bad events. The allowance is approximately $\lambda Tq$, so their ratio is $r$. This derivation assumes comparable event rate and population; under changing traffic, duration-to-exhaustion need not be $T/r$ even though event-rate burn remains correctly observed.

**State-velocity distinction.** Two services can each have 20% budget remaining while one is currently healthy and the other is at 100x burn. Conversely, two services can have 10x recent burn while one has nearly all budget remaining and the other is already overspent. Therefore neither remaining budget nor burn rate determines the other without cumulative history and window context.

**Rolling-window invariant.** A rolling budget is a function of the entire multiset of classified events in $(t-T,t]$. When an old bad event exits, balance improves even if current service does not. Consequently rolling recovery proves only that the current window meets its predicate; it does not prove remediation.

**Overlap proof.** If one operation is both slow and incorrect, it belongs to $A_{latency}\cap A_{correctness}$. Adding the two bad counts counts that operation twice. Inclusion-exclusion gives distinct affected operations, while separate budget states preserve the two non-substitutable properties.

**Policy invariant.** The same observed state should produce the same governed decision unless a recorded contextual input or authorized exception differs. If outcomes depend on who asks or which feature is favored, the policy is not auditable even if its arithmetic is exact.

## Alternatives and Trade-Offs

**Event versus time budgets.** Event budgets weight user operations and naturally reflect peak traffic. Time budgets are intuitive for continuous availability but can hide traffic concentration and inherit probe cadence. Choose the SLI that matches user consequence; report both diagnostically only when their meanings stay distinct.

**Rolling versus calendar windows.** Rolling windows continuously represent recent experience but make old incidents age out gradually. Calendar windows align with planning or contracts but create reset and boundary effects. The policy must match the objective's declared window rather than choosing whichever looks healthier.

**Count versus rate displays.** Counts make remaining operations concrete but change with open-window volume. Rates compare across scales but can obscure low denominators. Display target, valid count, bad count, exact allowance, balance, and window together.

**Single-window versus multiwindow burn.** A long window confirms material consumption but resets slowly after repair. A short window detects quickly but is noisy, especially under low traffic. Conjoining long and short burn conditions can improve actionability [4], but threshold selection remains service-specific.

**Freeze versus graded controls.** A blanket change freeze is simple and can stop repeated release-caused harm, but it may block low-risk or reliability-improving work. Graded controls use risk, reversibility, canary evidence, and remaining budget but require stronger governance. Predeclare the decision matrix.

**Central versus team-owned policy.** A central policy improves consistency and escalation. Team ownership captures domain harm and operational reality. A durable pattern defines organization-wide minimums while assigning service-specific targets, actions, and evidence to named owners.

**Joint versus separate objectives.** A joint good-event predicate measures complete success and prevents double-counted people or operations. Separate objectives preserve diagnosis and non-substitutable constraints. Use both only when each has an explicit decision purpose; do not combine percentages casually.

## Failure Modes and Misconceptions

- **“The budget is planned downtime.”** It is tolerance under an SLO, not a maintenance reservation or outage schedule.
- **“Positive balance makes the next release safe.”** Balance constrains cumulative reliability; release safety requires change-specific evidence and risk controls.
- **“Zero means stop all changes.”** Incident recovery, security fixes, safety work, and reliability changes may be the necessary response.
- **“A new month forgives the incident.”** The evaluation resets; causes, harms, and corrective commitments persist.
- **“Burn rate is percent consumed.”** Burn is normalized recent bad rate; consumption is cumulative bad service divided by allowance.
- **“Time to exhaustion is a promise.”** It is a conditional projection under assumptions that often change during incidents.
- **“More traffic always gives more safe failures.”** Open-window count allowance grows with valid volume, but traffic generation or retry amplification cannot be used to game user reliability.
- **“Unknown telemetry is good traffic.”** Missingness needs a declared rule or bounds; silent removal creates optimistic bias.
- **“Budgets across SLIs add.”** Overlap, weights, and non-substitutable harms make addition invalid without a joint model.
- **“Dependency-caused errors do not count.”** Ownership and user impact are different questions; user-facing SLIs ordinarily include the dependency experience.
- **“Teams should use all available budget.”** The objective defines a maximum tolerated bad share, not a utilization target.
- **“Error budget equals SLA credit.”** One governs engineering risk; the other is a contractual remedy under specific terms.
- **“The dashboard is objective truth.”** Classification, instrumentation, late data, and version choices remain part of the evidence.

## Worked Examples

### Example 1

**Situation.** A 99.9% success SLO closes with 2,000,000 valid logical operations and 1,500 bad operations. Find exact budget state.

**Reasoning.** Minimum good is $\lceil0.999\times2{,}000{,}000\rceil=1{,}998{,}000$, so $B=2{,}000$. Signed balance is $2{,}000-1{,}500=500$. Consumption is $1{,}500/2{,}000=75\%$ and overspend is zero.

**Conclusion.** The completed window meets its SLO with 500 bad operations of allowance remaining; this state alone does not assess a proposed release.

### Example 2

**Situation.** A small service targets 99% over 101 valid jobs. Can it tolerate two bad jobs because 1% of 101 is 1.01?

**Reasoning.** Minimum good is $\lceil0.99\times101\rceil=100$. Thus $B=101-100=1$. With two bad jobs, success is $99/101\approx98.0198\%$, below 99%.

**Conclusion.** Only one bad job is allowed. Rounding 1.01 upward would reverse the objective's exact inequality.

### Example 3

**Situation.** At midday, an open monthly 99.5% SLO has 80,000 valid requests and 250 bad. A dashboard says 150 remain. Is that the final monthly budget?

**Reasoning.** Current allowance is $\lfloor0.005\times80{,}000\rfloor=400$, so current balance is 150. Future valid volume is unknown; if another 40,000 valid requests arrive, the final allowance grows by 200, while their bad events also consume it. Calling 150 the final allowance assumes a denominator that has not yet occurred.

**Conclusion.** Report “150 against observations so far,” plus a separately labeled traffic forecast if needed.

### Example 4

**Situation.** A time-based availability SLO is 99.9% over 28 days. What nominal bad duration is allowed?

**Reasoning.** Twenty-eight days contain $28\times24\times60=40{,}320$ minutes. The budget rate is 0.001, so allowance is $40.32$ minutes, or 40 minutes 19.2 seconds. A one-minute probe cannot validate the 19.2-second precision, and peak-time impact may differ from overnight impact.

**Conclusion.** The mathematical allowance is 40.32 minutes, but evidence precision and user weighting remain properties of the time SLI.

### Example 5

**Situation.** A 99.9% SLO's latest 50,000 operations include 120 bad. Interpret the burn.

**Reasoning.** Observed bad rate is $120/50{,}000=0.0024=0.24\%$. Budget rate is 0.1%, so burn is $0.24/0.1=2.4$x. If that rate and population mix persisted from an empty 28-day window, exhaustion would occur in roughly $28/2.4\approx11.67$ days. If half the allowance currently remains, the simple stationary projection is about 5.83 days.

**Conclusion.** The observed interval burns at 2.4x; both exhaustion figures are conditional projections, not promises.

### Example 6

**Situation.** A four-hour outage leaves a 28-day rolling SLO overspent. Twenty-eight days later, the outage ages out and the dashboard turns green although the faulty deployment mechanism remains.

**Reasoning.** The evaluation is working as specified: the failed observations no longer belong to the window. The budget answers recent service performance, not causal remediation. Incident records, recurrence tracking, and open corrective actions carry the longer memory.

**Conclusion.** Green rolling state is not evidence that the defect was fixed; policy exit criteria must include causal evidence when appropriate.

### Example 7

**Situation.** Among 10,000 operations, 80 are slow, 50 are incorrect, and 20 are both. How many distinct operations experienced either failure?

**Reasoning.** Direct addition gives 130 and double-counts the overlap. Inclusion-exclusion gives $80+50-20=110$. The latency and correctness budgets should still remain separate if either property is non-substitutable.

**Conclusion.** There are 110 distinctly affected operations; “130 total user failures” would be false without defining failure marks rather than operations.

### Example 8

**Situation.** One logical purchase makes three server attempts: two time out and the third succeeds within the user's deadline. What consumes budget?

**Reasoning.** A logical-operation SLI classifies the purchase as good, perhaps with elevated latency. An attempt-level dependency SLI records two bad and one good attempts. Dividing one objective's bad count by the other's denominator is invalid, and retry amplification must not create extra user-facing allowance.

**Conclusion.** Each budget follows its own declared unit; user and dependency budgets reveal different mechanisms without being interchangeable.

### Example 9

**Situation.** A window has 99,700 known good, 100 known bad, and 200 unknown intended observations under a 99.8% target. Can the team decide the SLO before resolving unknowns?

**Reasoning.** Total intended observations are 100,000. Best case is $(99{,}700+200)/100{,}000=99.9\%$; worst case is $99{,}700/100{,}000=99.7\%$. The target lies inside the interval. Treating unknowns as excluded yields $99{,}700/99{,}800\approx99.8998\%$ and silently assumes they are missing completely at random or out of population.

**Conclusion.** Evidence is indeterminate under the stated facts; use the predeclared unknown-data policy and prioritize telemetry repair.

### Example 10

**Situation.** A service has exhausted its budget when an urgent authentication vulnerability requires a small configuration release. The normal policy pauses feature releases.

**Reasoning.** Blocking the security fix would conflict with the policy's purpose of reducing user risk. The predeclared exception path should name the security authority, require the narrowest reversible change, canary and rollback evidence, time-limited approval, and retrospective review. Exhaustion still blocks unrelated feature changes.

**Conclusion.** Authorize the governed security exception with safeguards; do not convert it into a blanket bypass or claim that positive budget was required.

## Cross-Program Connections

- **Software architecture:** dependency boundaries, fallback, isolation, and common-cause failure determine whether component behavior reaches users.
- **Testing and quality engineering:** change-specific confidence requires tests, canaries, and rollback evidence even when budget remains.
- **Systems engineering:** budgets are thresholds in a delayed feedback loop whose observability and control actions can be unstable.
- **Data engineering:** late, duplicate, missing, or reprocessed telemetry changes denominators and demands reproducible corrections.
- **Security engineering:** urgent remediation needs explicit exception governance rather than automatic inclusion in a change freeze.
- **Database engineering:** acknowledged-write durability and transaction correctness require property-specific SLIs; availability tolerance cannot compensate for lost data.
- **Platform engineering:** shared platforms need bounded cohort and tenant views so high-volume consumers do not hide smaller consumers' harm.
- **Algorithm engineering:** exact rational and integral arithmetic prevents threshold errors caused by floating-point or display rounding.
- **Organizational design:** policy assigns authority and incentives across product, reliability, dependency, and executive owners without turning measurement into blame.

## References

1. Marc Alvidrez, “Embracing Risk,” in *Site Reliability Engineering: How Google Runs Production Systems*, O'Reilly Media, 2016. [Official online edition](https://sre.google/sre-book/embracing-risk/). Accessed 2026-09-06.
2. Alex Hidalgo et al., “Implementing SLOs,” in *The Site Reliability Workbook*, O'Reilly Media, 2018. [Official online edition](https://sre.google/workbook/implementing-slos/). Accessed 2026-09-06.
3. Steven Thurgood, “Example Error Budget Policy,” in *The Site Reliability Workbook*, published 2018-02-19. [Official online edition](https://sre.google/workbook/error-budget-policy/). Accessed 2026-09-06.
4. Steven Thurgood et al., “Alerting on SLOs,” in *The Site Reliability Workbook*, O'Reilly Media, 2018. [Official online edition](https://sre.google/workbook/alerting-on-slos/). Accessed 2026-09-06.
5. Chris Jones et al., “Service Level Objectives,” in *Site Reliability Engineering: How Google Runs Production Systems*, O'Reilly Media, 2016. [Official online edition](https://sre.google/sre-book/service-level-objectives/). Accessed 2026-09-06.
6. Betsy Beyer, Niall Richard Murphy, David K. Rensin, Kent Kawahara, and Stephen Thorne, eds., *The Site Reliability Workbook: Practical Ways to Implement SRE*, O'Reilly Media, 2018. [Official online edition](https://sre.google/workbook/table-of-contents/). Accessed 2026-09-06.

All web-source claims and links above were checked against the official Google SRE site on 2026-09-06. The numerical examples were independently recomputed with exact or explicitly shown arithmetic. The policy examples are educational and must be adapted to the service's user harms, authority structure, and regulatory obligations.

## Exercises

### Exercise 1

A completed window has 240,003 valid events and a target of 99.95%. Derive the exact maximum bad count. Explain why rounding the displayed success percentage is not an acceptable decision method.

### Exercise 2

A 99.9% SLO has 40% of its budget remaining. The latest six-hour interval burns at 4x. Under a stationary approximation for a 30-day window, estimate time to exhaustion and list three assumptions that prevent treating it as a guarantee.

### Exercise 3

A dashboard reports 60 bad requests among 100,000 server attempts, but traces show 98,000 logical user operations, 120 abandoned operations with no terminal server record, and retries that created the extra attempts. Diagnose the denominator and missing-data problems and propose a defensible next calculation.

### Exercise 4

Design a concise policy response matrix for healthy budget, material rapid burn, exhaustion without active burn, and an urgent security fix during exhaustion. Name evidence, authority, action, and exit criteria for each state.

### Exercise 5

A multi-tenant platform meets its global 99.9% objective, but a low-volume tenant class experienced 4% failures for two hours. The platform team proposes removing that class from the global denominator because it contributes little volume. Evaluate the proposal and design a bounded alternative that avoids both hidden harm and an unmanageable objective per tenant.

## Answers to the Exercises

### Answer 1

Minimum good count is $\lceil0.9995\times240{,}003\rceil=\lceil239{,}882.9985\rceil=239{,}883$. Therefore maximum bad count is $240{,}003-239{,}883=120$. Equivalently, $\lfloor0.0005\times240{,}003\rfloor=\lfloor120.0015\rfloor=120$. With 121 bad events, the exact ratio misses even if a dashboard rounded it to the same displayed percentage. Evaluation uses integer counts and the declared inequality; formatting is presentation only.

### Answer 2

With remaining fraction $f=0.4$, window $T=30$ days, and burn $r=4$, the simple projection is $fT/r=0.4\times30/4=3$ days. It assumes at least: the future bad fraction matches the six-hour observation; event volume and population mix remain comparable; and classification, telemetry completeness, and SLI version remain stable. It also ignores repair, release, diurnal traffic, and rolling-window aging. Report “three days under stated stationary assumptions,” not “budget will run out in three days.”

### Answer 3

The attempt denominator measures server attempts, not logical user outcomes. Retries inflated it from at most the 98,120 observed or intended logical operations, and the 120 abandoned operations are unknown or bad depending on the declared user SLI. First reconstruct one record per logical operation using a stable correlation identity. Apply the predeclared terminal-success and deadline predicate, deduplicate retries, include abandoned intended operations, and classify the 120 according to the missing-data policy. If their outcomes remain unknown, report best- and worst-case bounds rather than silently excluding them. Keep the attempt-level ratio as a separate dependency diagnostic.

### Answer 4

A model matrix is: healthy budget—service owner uses the versioned budget dashboard and normal release evidence, normal risk-tiered delivery continues, exit when burn or consumption crosses a declared threshold; material rapid burn—on-call authority uses long- and short-window evidence, starts incident response and pauses implicated risky changes, exit after burn is controlled and mitigation is verified; exhaustion without active burn—product and reliability owners review incident history and open corrective work, prioritize reliability and restrict high-risk launches, exit on agreed recovery state plus evidence that required actions are complete; urgent security fix during exhaustion—security authority approves a narrow time-limited exception using vulnerability, canary, rollback, and blast-radius evidence, then requires retrospective review. Exact thresholds must be service-specific, and every override records approver, rationale, safeguards, expiry, and outcome.

### Answer 5

Removing the class after observing harm changes scope opportunistically and makes the global objective less representative. Low volume does create sparse-data volatility, so an objective per tenant may be noisy and operationally unmanageable. A bounded alternative defines a small number of consequence-based cohorts—such as standard low-volume interactive tenants—before evaluation, preserves them in the global denominator, and adds a cohort guardrail using a suitable longer window or minimum-event rule. Diagnostics drill down per tenant without promising a separate objective to every tenant. Acceptance requires that the cohort corresponds to a distinct user journey or harm, has named ownership, has enough evidence for decisions, and cannot be reclassified retroactively.
