---
module_id: SYSENG-005
program: Systems Engineering
level: 1
module_number: 5
title: Feedback Loops and Dynamic Behavior
status: complete
last_verified: 2026-08-30
---

# Feedback Loops and Dynamic Behavior

## One-Page Review

### Governing question

How do accumulations, rates, feedback polarity, gain, delay, nonlinear limits, and human response create growth, regulation, overshoot, oscillation, collapse, or resilience over time?

### Essential definitions

- **dynamic behavior** is a system's state trajectory over time under inputs, internal transitions, feedback, and constraints.
- A **stock** is an accumulation remembered by the system; a **flow** changes a stock per unit time.
- **feedback** occurs when consequences of system behavior return, directly or through measurement and interpretation, to influence later behavior.
- A **reinforcing loop** amplifies change in a direction: an increase ultimately promotes further increase, or a decrease promotes further decrease.
- A **balancing loop** opposes deviation from a goal, limit, or reference condition.
- **loop polarity** describes the sign of influence around a loop under stated conditions; it does not label a loop morally good or bad.
- A **delay** separates cause, observation, decision, action, or effect in time.
- **gain** describes response magnitude relative to perceived error or input.
- An **equilibrium** is a state or trajectory that remains unchanged under the modeled conditions; **stability** concerns whether nearby trajectories return, remain near, or diverge.
- **overshoot** crosses a target or carrying limit; **oscillation** repeatedly moves around a reference or regime.
- **saturation** bounds a flow or response; **hysteresis** makes switching depend on history through different entry and exit thresholds.
- A **causal-loop diagram** records hypothesized influence structure; a **stock-and-flow model** adds accumulations, rates, units, and equations needed for quantitative execution.

### Central model, mechanism, or theorem

For stocks $x(t)$, inflows $i(t)$, and outflows $o(t)$:

$$
\frac{dx}{dt}=i(t)-o(t),
\qquad
x_{k+1}=x_k+\Delta t\,[i_k-o_k]
$$

for a simple discrete approximation. A controller or policy observes $y(t-\tau_o)$, compares it with reference $r$, decides after delay $\tau_d$, and changes flow after actuation delay $\tau_a$. Even a balancing rule can oscillate or diverge if combined delay and gain make corrections too large for the state being corrected. The whole trajectory—not one snapshot—supports a dynamic claim.

### Critical invariants

- Every stock has defined units, boundary, initial condition, and conserved or created/destroyed quantities.
- Every flow has units of stock per time and identifies source, sink, capacity, and governing mechanism.
- Influence signs are conditional and must form dimensionally meaningful paths.
- Feedback requires a closed causal path; correlation or a one-way chain is not feedback.
- Loop polarity is evaluated around the complete loop and can change across operating regions.
- Delays identify what is delayed, by how much or by which distribution, and whether the delay affects observation, decision, transport, or state change.
- Stability claims state model, parameter range, time step, disturbance, and nonlinear constraints.
- Averages cannot replace transient maxima, tails, depletion, or recovery behavior.
- Human learning, adaptation, workarounds, and incentives can alter the loop structure.
- Simulation establishes behavior only for encoded equations, parameters, initial conditions, solver, and scenarios.

### Common failures

Failures include calling any repeated process feedback; drawing causal arrows without units or evidence; reading a balancing loop as necessarily stable; ignoring observation and action delay; correcting a stock using its current value when only stale measurements exist; using averages while queues or inventories accumulate; treating capacity as a flow rather than a bound; allowing negative stocks; confusing event sequence with causal loop; adding alarms that create attention feedback; tuning gain in one operating region and ignoring saturation; inferring causation from coincident time series; and trusting a smooth simulation more than its assumptions.

### Compact example

A controller wants stock $x=10$ and applies $0.6(10-\hat{x})$ per step, but $\hat{x}$ is two steps old. Starting at zero, it adds 6 while the delayed observation still says zero: states become 6, 12, and 18. When the controller finally sees 6, it still adds 2.4, reaching 20.4. Later negative corrections arrive after the stock has already fallen. The loop is balancing by intent but oscillatory because high response acts on stale state.

### Connections

Retrieve [elements, relationships, and emergent behavior](004-elements-relationships-and-emergent-behavior.md), plus the earlier boundary, mission, and value models. Continue to open and closed systems, complexity and uncertainty, assumptions, scenarios, and problem framing. Later state/mode, control-flow, reliability, resilience, verification, and adaptive-systems modules add formal and domain-specific depth.

## Governing Question

Static structure explains what can interact; dynamic reasoning explains what happens next, how fast, and whether the behavior settles or amplifies. A backlog can grow while throughput looks constant. A thermostat can oscillate while every component works. A maintenance policy can reduce preventive work, improve short-term availability, then increase failures and workload months later. How can engineers identify the feedback mechanisms behind such trajectories and test interventions without mistaking a plausible diagram for evidence?

The answer combines qualitative loop hypotheses with stocks, flows, delays, equations, scenarios, and observations. Begin with mechanisms and units. Execute or derive the model. Challenge parameters and boundaries. Compare predicted trajectories with real evidence. Revise both system and model when they disagree.

## Why This Matters

Many systems fail through time rather than at one instant. Capacity is consumed faster than replenished. Defects accumulate behind apparently stable release activity. A response policy arrives after the state changed. Operators compensate until workload crosses a threshold. Short-term optimization creates delayed harm outside the reporting window.

Systems engineering must therefore reason about trajectories, not only configurations. ISO/IEC/IEEE 15288:2023 frames systems through lifecycle processes and interacting elements; dynamic analysis supports architecture, risk, integration, operation, validation, and evolution across those processes. SEBoK's systems-thinking material treats feedback and dynamics as central to understanding system behavior. NASA's Systems Engineering Handbook uses margins, technical measures, risk, and lifecycle evidence that depend on change over time.

System dynamics, founded in engineering practice by Jay Forrester and developed pedagogically by John Sterman and Donella Meadows, supplies stocks, flows, feedback, delay, and nonlinear behavior. Classical control theory supplies mathematical stability and response analysis. This chapter builds the shared first-principles vocabulary; it does not replace domain-specific control, queueing, reliability, economic, ecological, or human-factors models.

Feedback is neither inherently good nor inherently cybernetic automation. A human review, price signal, immune response, incident learning process, or social norm can close a loop. What matters is which state is observed, how it is interpreted, who acts, with what delay and authority, and how that action changes the future state.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. state summarizes relevant history and changes through transition mechanisms;
2. relationships can carry information, control, material, energy, authority, and influence;
3. a global behavior can emerge from locally valid rules;
4. rates and accumulated quantities have different units;
5. a derivative or difference describes change, while an integral or sum accumulates it;
6. measurement has latency, error, missingness, and scope;
7. correlation alone does not establish a causal mechanism.

Check dimensional intuition: if a reservoir contains liters, inflow must be liters per time. Multiplying flow by time produces a stock change. Adding a rate directly to a stock without a time factor is dimensionally invalid except when the time step is explicitly one chosen unit.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish stock, flow, state, event, parameter, auxiliary variable, and output measure;
2. identify reinforcing and balancing loops from complete causal paths;
3. construct a dimensionally consistent stock-and-flow equation;
4. separate observation, interpretation, decision, actuation, and transport delays;
5. trace equilibrium, stability, overshoot, oscillation, exponential growth, and depletion;
6. explain why balancing feedback can destabilize under gain and delay;
7. model saturation, thresholds, hysteresis, and resource limits;
8. identify feedback in technical, organizational, human, and environmental systems;
9. design simulation and operational evidence appropriate to a dynamic claim;
10. diagnose interventions that move symptoms, shift burden, or create delayed side effects.

## Core Exposition

**Start with behavior over time.** Before drawing causes, plot the variable of concern: level, rate, backlog, temperature, availability, workload, adoption, or risk proxy. State unit, boundary, population, observation interval, missing data, and relevant events. A snapshot cannot distinguish stable high state from rapid growth crossing the same value.

Common trajectory shapes include linear growth, exponential growth/decay, goal seeking, S-shaped growth, overshoot, damped or sustained oscillation, collapse, step response, and regime switching. A visual resemblance does not prove mechanism; it suggests hypotheses to test.

**Identify stocks.** Stocks persist when flows stop. Inventory, energy, population, queued work, skill, cash, stored data, technical debt under a defined operational measure, and unresolved hazard actions can be modeled as stocks when their units and boundaries are explicit. “Quality” or “trust” may be useful concepts but need careful operationalization before numerical stock treatment.

A stock changes only through flows across its boundary or internal creation/destruction mechanisms included as flows. For backlog $B$:

$$
B_{k+1}=\max(0,B_k+Arrivals_k-Completions_k).
$$

The nonnegative bound matters. Completion capacity is not necessarily actual completion; when backlog is zero, unused capacity does not create negative work.

**Define flow mechanisms.** A flow can depend on stock, external input, capacity, policy, delay, and other state. Completion might be $\min(B,capacity)$. Failure occurrence may depend on population at risk and hazard rate. Hiring depends on approved positions, candidate supply, and onboarding capacity. Each equation encodes assumptions and must preserve units.

**Construct causal links carefully.** A positive link means an increase in source, all else equal, tends to increase target above what it otherwise would be; a negative link tends to decrease it. The sign is local and conditional. “Price +→ revenue” fails when demand changes strongly; specify the regime or intermediate variables.

A loop is reinforcing when the product of link signs is positive—zero or an even number of negative links. It is balancing when the product is negative—an odd number of negative links. This sign rule describes direction around a simple loop, not dynamic stability. Gain, delay, nonlinearities, and interacting loops determine trajectories.

**Reinforcing feedback.** Adoption can create more compatible services, which increases usefulness, which increases adoption. Defects can create firefighting, reducing preventive work, increasing defect introduction. Reinforcing loops amplify both growth and decline until constrained by another mechanism. Unbounded exponential growth signals a missing limit for most physical systems.

**Balancing feedback.** A thermostat compares temperature with a setpoint and changes heat input. Inventory policy compares stock with target and orders replenishment. Incident control compares service state with objectives and applies recovery. If observation and actuation were immediate, proportional response might converge. Real delay and gain can cause overshoot.

**Disaggregate delay.** Total delay often includes:

$$
\tau=\tau_{observe}+\tau_{transport}+\tau_{interpret}+\tau_{decide}+\tau_{actuate}+\tau_{effect}+\tau_{confirm}.
$$

These delays have different controls. Faster telemetry does not fix slow physical replenishment. Faster action can worsen behavior if interpretation uses noisy data. Model delay as a fixed lag only when justified; real delays may be distributed and variable.

**Analyze equilibrium.** In a stock-flow model, equilibrium requires net flow zero under constant inputs: $i(x^*)=o(x^*)$. It does not necessarily mean desirable, safe, or inactive. A hospital queue can be stable at an unacceptable wait. A system can also have a moving equilibrium or periodic attractor.

**Analyze local stability.** For the simple discrete no-delay rule

$$
x_{k+1}=x_k+K(r-x_k),
$$

the error $e_k=r-x_k$ evolves as $e_{k+1}=(1-K)e_k$. It converges when $|1-K|<1$, so $0<K<2$: monotone for $0<K\le1$, alternating with shrinking magnitude for $1<K<2$. At $K=2$ it alternates without decay; beyond 2 it diverges. This result applies only to this linear, discrete, instantaneous model.

With delay, the state dimension grows because history matters. Conditions change; applying the no-delay bound is invalid. Simulation can expose trajectories but does not replace formal analysis where safety depends on all reachable states.

**Trace delayed balancing feedback.** The executable model compares immediate and two-step-delayed observation for the same target and gain. It prints the delayed trace used in the review sheet and the maximum deviations. Negative control is permitted in this abstract reversible stock; real actuators may saturate or forbid negative flow.

<!-- bijux-verify: {"id":"delayed-balancing-loop","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"step=1 observed=0.00 action=6.00 state=6.00\nstep=2 observed=0.00 action=6.00 state=12.00\nstep=3 observed=0.00 action=6.00 state=18.00\nstep=4 observed=6.00 action=2.40 state=20.40\nstep=5 observed=12.00 action=-1.20 state=19.20\nstep=6 observed=18.00 action=-4.80 state=14.40\nstep=7 observed=20.40 action=-6.24 state=8.16\nstep=8 observed=19.20 action=-5.52 state=2.64\nstep=9 observed=14.40 action=-2.64 state=0.00\nstep=10 observed=8.16 action=1.10 state=1.10\nimmediate_final=10.00\ndelayed_final=1.10\nimmediate_max_error=4.00\ndelayed_max_error=10.40\nreal_controller_validated=false\nevidence=linear_discrete_teaching_model_only\n","stderr":""}} -->
```python
target = 10.0
gain = 0.6

def simulate(delay, report=False):
    state = 0.0
    history = [state] * (delay + 1)
    states = []
    for step in range(1, 11):
        observed = history[0]
        action = gain * (target - observed)
        state += action
        history = history[1:] + [state]
        states.append(state)
        if report:
            print(f"step={step} observed={observed:.2f} action={action:.2f} state={state:.2f}")
    return states

immediate = simulate(0)
delayed = simulate(2, report=True)
print(f"immediate_final={immediate[-1]:.2f}")
print(f"delayed_final={delayed[-1]:.2f}")
print(f"immediate_max_error={max(abs(target-x) for x in immediate):.2f}")
print(f"delayed_max_error={max(abs(target-x) for x in delayed):.2f}")
print("real_controller_validated=false")
print("evidence=linear_discrete_teaching_model_only")
```

**Add saturation and anti-windup concerns.** Real flows have bounds. A heater cannot deliver negative heat; a team cannot process infinite work; a battery has charge limits. If an integral controller accumulates error while the actuator is saturated, it may continue commanding excessive action after the state recovers—integrator windup. Model capacity, release of accumulated demand, and recovery.

**Add thresholds and hysteresis.** A controller that turns on below 10 and off above 10 can chatter under noise. Hysteresis might turn on below 9 and off above 11, encoding state/history in the switching rule. Thresholds create piecewise dynamics and can create abrupt regime change. Verify both boundary equality and noisy crossings.

**Model competing loops.** S-shaped growth often combines reinforcing adoption with balancing market/resource limits. Incident response can include a balancing recovery loop and a reinforcing overload loop: more incidents create more coordination load, slowing restoration and causing further incidents. Loop dominance can change over time.

**Avoid symptom treatment.** Increasing throughput can reduce backlog temporarily while increasing defect/rework inflow later. Adding staff can reduce workload after a hiring and learning delay but initially increases mentoring load. A good intervention changes a governing flow or information/decision relationship and checks delayed side effects.

**Treat measurement as part of the loop.** Metrics change behavior when linked to evaluation or reward. If teams are rewarded for ticket closure, closure classification changes; the observed metric can improve without the stock of unresolved customer problems falling. Measurement delay, sampling, filtering, and gaming belong in the model.

**Treat humans as adaptive.** People anticipate, learn, coordinate, resist, create workarounds, and change goals. A fixed response coefficient may fit one period and fail after policy changes. Combine models with observation and qualitative evidence. Do not assign a “human error rate” where authority, interface, staffing, incentives, or procedure explains the behavior.

**Validate dynamically.** Compare time series, event traces, delays, distributions, transient peaks, equilibrium, recovery, and response to disturbances. Calibrate on one dataset and validate on another where possible. Test structural alternatives, not only parameter fit. Many models reproduce one historical curve; stronger evidence discriminates mechanisms.

**Design safe experiments.** Perturbation can reveal dynamics, but high-consequence systems limit experimentation. Use analytical models, simulation, hardware-in-loop, fault injection, staged tests, exercises, and bounded operational trials under appropriate authority. A fitted model cannot authorize unsafe exploration.

## Definitions and Notation

Let $x(t)$ be a stock with unit $[X]$, and $i(t),o(t)$ flows with unit $[X]/[time]$. Continuous balance is:

$$
x(t)=x(t_0)+\int_{t_0}^{t}[i(s)-o(s)]\,ds.
$$

A discrete Euler approximation with step $\Delta t$ is:

$$
x_{k+1}=x_k+\Delta t(i_k-o_k).
$$

Changing $\Delta t$ without changing rate interpretation can alter behavior or numerical stability. Solver choice and step size are evidence metadata.

Let $r$ be reference, $y$ measured output, $e=r-y$ error, $u$ control/action, $K$ gain, $d$ disturbance, and $\tau$ delay. A general closed influence model is:

$$
\dot{x}=f(x,u,d),\quad y=h(x),\quad u(t)=\pi(r,y_{history},constraints).
$$

The policy $\pi$ can be automated, human, organizational, or hybrid. SYSENG-006 develops open/closed system boundaries; later modules formalize behavior and control allocation.

A causal-loop link sign $s_{ij}\in\{-1,+1\}$ is a conditional partial influence. Simple loop polarity is $\prod s_{ij}$. The product does not specify gain, time constant, delay, saturation, or stability.

## Mechanisms, Invariants, or Proof Structure

Use this dynamic-analysis procedure:

1. **Define behavior of concern.** Plot trajectories with units, time horizon, population, modes, and observation limitations.
2. **Set the dynamic boundary.** Include stocks, flows, decisions, environment, and stakeholders capable of producing the behavior.
3. **Identify stocks and flows.** Apply dimensional checks, conservation assumptions, initial conditions, sources, sinks, and capacity.
4. **Hypothesize causal links and loops.** State mechanisms, signs, conditions, and evidence; separate correlation.
5. **Disaggregate delays.** Locate observation, transport, interpretation, decision, actuation, effect, and confirmation delay.
6. **Write transition equations or executable rules.** Include ordering, step, saturation, thresholds, stochasticity, and human policy.
7. **Analyze equilibria and local response.** Derive what the model permits before relying on plots.
8. **Challenge trajectories.** Vary initial conditions, parameters, delay, disturbances, limits, noise, failure, and policies.
9. **Validate structure and behavior.** Compare mechanisms and trajectories with independent, operationally relevant evidence.
10. **Intervene and re-observe.** State expected near/long-term changes, guardrails, authority, and model revision triggers.

Five invariants guide review.

**Dimensional invariant.** Every equation preserves compatible units and every flow changes a named stock.

**Closure invariant.** A feedback claim traces a complete causal path back to a future input or decision; one-way influence is not a loop.

**Delay invariant.** State history used by a decision matches what could actually be observed and acted upon.

**Constraint invariant.** Stocks, flows, and actions obey physical, logical, legal, and operational bounds in applicable modes.

**Evidence invariant.** Stability, causality, effectiveness, and safety conclusions never exceed the analyzed model and observed scenarios.

## Alternatives and Trade-Offs

**Causal-loop diagrams versus stock-and-flow models.** Loop diagrams help elicit hypotheses and communicate polarity. Stock-flow equations force units, accumulation, and executable assumptions. Use diagrams for discovery and equations when quantitative claims matter.

**Continuous versus discrete models.** Continuous models fit many physical processes. Discrete event/time models fit sampled controllers, queues, and organizational decisions. Choose by mechanism and check discretization artifacts.

**Analytical versus simulation evidence.** Analysis can establish parameter-wide results for simplified models. Simulation explores richer nonlinear cases but samples. Combine them and validate fidelity separately.

**High gain versus smooth response.** High gain corrects quickly under current information but amplifies noise and delay. Lower gain may be stable but too slow for mission or disturbance. Add prediction, damping, feedforward, or better observation only with evidence.

**Central feedback versus local autonomy.** Central observation supports global coordination but adds latency and single-point dependence. Local loops respond quickly but interact and can fight. Define hierarchy, authority, and time-scale separation.

**Buffer versus immediate coupling.** Buffers absorb variability but add delay, inventory, and hidden work. Tight coupling reduces stock but propagates disruption. Size and monitor buffers against explicit service and failure goals.

**Robustness versus efficiency.** Spare capacity and margins damp disturbance; high utilization appears efficient but creates queues and slow recovery. Value lifecycle resilience rather than idle-resource optics alone.

## Failure Modes and Misconceptions

1. **Feedback means receiving comments.** Comments close a loop only if they inform an action that changes future observed behavior.
2. **Positive means beneficial.** Positive denotes reinforcing polarity, which can amplify growth or decline.
3. **Negative means harmful.** Negative denotes balancing polarity, which can regulate or oscillate.
4. **Balancing loops are stable.** Delay, gain, saturation, and interacting loops can destabilize them.
5. **Stocks and flows are interchangeable.** Backlog and throughput have different units and dynamics.
6. **A causal-loop diagram is a simulation.** It omits quantitative state, units, and transition semantics.
7. **Correlation identifies a loop.** Mechanism, direction, timing, and intervention evidence are needed.
8. **Faster response is always better.** Acting quickly on noise or stale state can increase oscillation.
9. **Average behavior is enough.** Peaks, tails, depletion, and recovery determine many failures.
10. **Model fit proves mechanism.** Different structures can reproduce the same history.
11. **Humans are fixed gains.** Learning, incentives, workload, and authority change response.
12. **Simulation validates intervention.** It supports model-conditioned predictions; real validation remains separate.

## Worked Examples

### Example 1

**Question:** A backlog is 40 items, arrivals are 12/day, and completions are 10/day for five days. What happens?

**Reasoning:** Net flow is $12-10=2$ items/day. With one-day steps and no other flow, $B_5=40+5\times2=50$. Throughput looks stable at 10, but the stock grows 25%. If reporting shows only completions, deterioration is hidden. If arrivals later fall below completions, the backlog can shrink only while work remains.

**Conclusion:** Rates can appear steady while an accumulated state moves materially; always connect flow measures to their stock.

### Example 2

**Question:** Classify the loop “more users → more shared content → greater usefulness → more users.”

**Reasoning:** Under a regime where content remains discoverable and useful, each link is positive, so the loop product is positive and reinforcing. It can amplify decline too: fewer users reduce content, usefulness, and users. It cannot grow indefinitely; moderation burden, congestion, market size, or low-quality content introduces balancing limits. Evidence must verify each conditional link rather than infer the loop from growth alone.

**Conclusion:** The loop is reinforcing within stated conditions, with missing balancing mechanisms required for realistic long-term behavior.

### Example 3

**Question:** Why does the delayed controller reach 20.4 when its target is 10?

**Reasoning:** For three steps, the two-step history still exposes zero, so the policy adds 6 each time: states 6, 12, 18. On step four it finally observes 6, still below target, and adds 2.4 to reach 20.4. The action is correct for the stale observation but wrong for current state. Later negative actions similarly arrive late and drive the state below target.

**Conclusion:** Overshoot follows from observation delay plus gain; the balancing sign alone does not imply convergence.

### Example 4

**Question:** Derive stability of the no-delay proportional teaching model.

**Reasoning:** With $x_{k+1}=x_k+K(r-x_k)$, define $e_k=r-x_k$. Then $e_{k+1}=r-x_{k+1}=r-x_k-K(r-x_k)=(1-K)e_k$. Error converges to zero exactly when $|1-K|<1$, giving $0<K<2$. For $K=0.6$, error shrinks by factor 0.4 per step. This proof excludes delay, saturation, noise, and nonlinear plants.

**Conclusion:** Stability is derived for a precise model and parameter range, not transferred automatically to the delayed or real system.

### Example 5

**Question:** Why can hiring initially worsen an overloaded team's delivery?

**Reasoning:** More staff is intended to increase completion capacity, a balancing response to backlog. Hiring has approval and search delay; onboarding consumes experienced staff attention, temporarily reducing effective completion; newcomers accumulate skill over time. Backlog and coordination load may rise before capacity improves. If management reacts to the temporary worsening by hiring more, it can amplify overload. Model candidate, onboarding, skill, work, and mentoring stocks/flows separately.

**Conclusion:** Delayed capacity and transition workload can reverse the short-term sign of an apparently balancing intervention.

### Example 6

**Question:** A tank switch turns a pump on below 10 liters and off above 10. Why might it chatter?

**Reasoning:** Near 10, measurement noise can alternate 9.99 and 10.01, rapidly switching the actuator. Add hysteresis: on below 9, off above 11, otherwise retain prior switch state. The dead band reduces switching but permits level variation and delays response. Test exact thresholds, sensor error, rate limits, pump minimum run time, overflow, and empty conditions.

**Conclusion:** Hysteresis trades tracking precision for stable switching and actuator protection by explicitly adding state/history.

### Example 7

**Question:** Closing more incidents raises the closure metric but customer-reported failures persist. What loop may exist?

**Reasoning:** A closure target increases pressure, which increases premature classification as resolved, which improves the measured rate and reinforces the target policy. Reopened incidents and customer harm may arrive later or in another system, so the balancing quality signal is delayed or excluded. Track unresolved-problem stock, reopen flow, recurrence, outcome confirmation, and workload; change incentives and closure authority, then re-observe.

**Conclusion:** Measurement can become part of a reinforcing gaming loop that decouples the metric from the intended system state.

### Example 8

**Question:** Why can high utilization create a reinforcing service collapse?

**Reasoning:** Near capacity, variability creates queues; queueing increases response time; timeouts and retries add arrivals; operators spend capacity on recovery; effective service rate falls; queues grow further. Admission control, retry budgets, spare capacity, and graceful degradation can interrupt links. A simple average utilization omits burst distribution and correlated dependencies.

**Conclusion:** Retry and recovery interactions can turn a capacity threshold into reinforcing overload even when demand growth is temporary.

### Example 9

**Question:** A flood-control simulation shows no overflow under average rainfall. Is the design validated?

**Reasoning:** Average inflow can conceal storm intensity, spatial correlation, saturated soil, blocked drains, pump failure, forecast delay, operator action, and downstream constraints. Check units and mass balance; use distributions and adversarial sequences; calibrate storage/outflow mechanisms; validate against independent events; inspect emergency modes. No external hydrological, safety, regulatory, or practitioner review is claimed.

**Conclusion:** Dynamic safety depends on transient and tail scenarios plus model fidelity, not average input or one successful simulation.

### Example 10

**Question:** An intervention reduces alerts immediately. When should success be evaluated?

**Reasoning:** Map delays. Threshold change immediately alters alert flow; operator attention and response may improve over days; missed detection may appear only when a rare event occurs; incident harm and learning may arrive later. Predeclare near-term noise/workload measures and longer-term detection, incident, subgroup, and safety guardrails. Preserve rollback and review triggers rather than waiting indefinitely for sparse harm.

**Conclusion:** Evaluation cadence follows each causal path and consequence delay; one immediate metric cannot close a long-horizon safety loop.

## Cross-Program Connections

- [Concurrent & Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) develops timing, synchronization, work queues, and local feedback in programs.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) handles delayed, partial, and inconsistent observation across machines.
- [Software Delivery & Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) applies feedback to release, observability, incidents, capacity, and reliability.
- [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md) analyzes backpressure, streaming state, and dynamic distributed workloads.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) shapes organizational feedback through self-service interfaces, policies, and developer experience.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) models adversaries who adapt to controls, producing strategic feedback absent from static threat lists.

## References

1. ISO/IEC/IEEE. [ISO/IEC/IEEE 15288:2023 — System life cycle processes](https://www.iso.org/standard/81702.html), second edition, May 2023. Consulted 2026-08-30.
2. SEBoK Editorial Board. [Systems Thinking](https://sebokwiki.org/wiki/Systems_Thinking), *Guide to the Systems Engineering Body of Knowledge*, version 2.14. Consulted 2026-08-30.
3. Jay W. Forrester. *Industrial Dynamics*. MIT Press, 1961.
4. John D. Sterman. *Business Dynamics: Systems Thinking and Modeling for a Complex World*. McGraw-Hill, 2000.
5. Donella H. Meadows. *Thinking in Systems: A Primer*. Chelsea Green, 2008.
6. Karl J. Åström and Richard M. Murray. [*Feedback Systems: An Introduction for Scientists and Engineers*](https://press.princeton.edu/books/hardcover/9780691193984/feedback-systems), second edition, Princeton University Press, 2021. Consulted 2026-08-30.
7. Katsuhiko Ogata. *Discrete-Time Control Systems*. Prentice Hall, second edition, 1995.
8. NASA. [*NASA Systems Engineering Handbook*, Rev. 2](https://www.nasa.gov/reference/systems-engineering-handbook/), NASA/SP-2016-6105 Rev2, 2016. Consulted 2026-08-30.

## Exercises

### Exercise 1

For a repair service, classify reported work, diagnosed work, completed repairs, technician skill, parts inventory, arrival rate, completion rate, and training as stocks, flows, parameters, or actions. State units.

### Exercise 2

For $x_{k+1}=x_k+K(r-x_k)$, trace $x_0=0,r=10$ for $K=0.5,1,2,2.5$ and relate each trajectory to the derived stability condition.

### Exercise 3

Diagnose a release process where escaped defects increase incidents, incidents increase urgent patches, urgent patches reduce review, and reduced review increases escaped defects. Add at least one balancing loop and delay.

### Exercise 4

Compare centralized and local feedback for building temperature across rooms. Address sensors, delays, coupling, capacity, occupant behavior, energy, stability, and degraded modes.

### Exercise 5

Design dynamic evidence for an automated medication-supply system that forecasts demand and changes replenishment. Separate executable model checks, simulation, operational trials, human authority, and claims that remain unproven.

## Answers to the Exercises

### Answer 1

Reported-undiganosed work, diagnosed-awaiting-parts work, ready-for-repair work, and completed-awaiting-return work are distinct work stocks measured in jobs; combining them hides constraints. Parts inventory is a stock measured in parts by type/location. Technician skill can be a latent capability stock only under an explicit measurement model, perhaps qualified task-hours or proficiency states; do not treat a vague score as physical quantity. Arrivals, diagnosis, repair completion, parts consumption/replenishment, and skill acquisition/decay are flows per time. Staffing, hours, task mix, failure distribution, and tool availability are parameters or state depending on whether they change. Training allocation is an action that consumes time now and changes skill later.

### Answer 2

With $e_{k+1}=(1-K)e_k$: for $K=0.5$, states are 5, 7.5, 8.75, ... and converge monotonically. For $K=1$, the first state is 10 and remains. For $K=2$, states alternate 20, 0, 20, 0: error factor is -1, so it does not decay. For $K=2.5$, states 25, -12.5, 43.75, ... have error multiplied by -1.5 and diverge. This matches convergence only for $0<K<2$. It does not apply unchanged with delay, saturation, or nonlinear response.

### Answer 3

The described loop is reinforcing: more escaped defects → more incidents → more urgent patches → less review → more escaped defects. Stocks include latent defects, unresolved incidents, queued change, and exhausted attention; flows include introduction, detection, repair, and review. Delays include defect-to-incident, incident diagnosis, patch verification, and recurrence observation.

A balancing loop could reserve review/test capacity or enforce an emergency-change risk gate: higher incident/defect evidence increases protected verification and root-cause work, which reduces introduction after a delay. It may initially slow patch throughput, so measure restoration separately from long-term recurrence. Limit work in progress, reduce patch batch, preserve emergency authority, and re-observe escaped-defect and incident stocks rather than only deployment count.

### Answer 4

Central control sees building-wide loads, shared plant capacity, tariffs, and room interactions; it can coordinate but suffers network/sensor delay and central failure. Local controllers respond quickly to room temperature but can fight through shared airflow/heating capacity, create simultaneous demand peaks, or ignore energy constraints. Occupants change windows, equipment, and setpoints; sunlight and occupancy are disturbances.

A layered design can give local loops safe ranges while a slower supervisory loop allocates capacity and adapts schedules. Define sampling, calibration, actuator lag, thermal inertia, cross-room coupling, saturation, hysteresis, communication loss, sensor failure, manual override, freeze/fire modes, and recovery. Analyze stability for simplified models, simulate diverse weather/occupancy, integrate real controllers, and monitor comfort distribution, energy, equipment cycling, and unsafe temperatures.

### Answer 5

Executable checks verify dimensional consistency, nonnegative stock, order/replenishment conservation, capacity, expiry, lead-time queues, threshold boundaries, deterministic replay, and declared forecast calculations. Simulation varies demand bursts, seasonality, substitution, supplier delay/failure, cold-chain loss, data latency, missingness, forecast error, hoarding, allocation policy, and multiple facilities; sensitivity identifies fragile rules.

Bounded operational trials use reversible cohorts, shadow recommendations, reconciliation, inventory/service/expiry guardrails, subgroup/facility distribution, alerts, rollback, and delayed outcome windows. Automation cannot establish clinical appropriateness, equitable allocation, legal compliance, acceptable shortage risk, or whether future crises match modeled distributions. No external clinical, pharmacy, regulatory, academic, or practitioner review is claimed. Named pharmacy, clinical, supply, safety, human-factors, data, security/privacy, operations, equity, and regulatory authorities must review objectives, constraints, evidence, override, incident response, rollout, residual risk, and monitoring.
