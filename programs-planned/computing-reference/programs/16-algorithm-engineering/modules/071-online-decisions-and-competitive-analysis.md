---
module_id: ALGE-071
program: Algorithm Engineering
level: 2
module_number: 71
title: Online Decisions and Competitive Analysis
status: complete
last_verified: 2026-09-05
---

# Online Decisions and Competitive Analysis

## One-Page Review

### Governing question

How can an algorithm make irrevocable or costly-to-reverse decisions before future input is known, and what does a competitive guarantee actually establish about those decisions?

### Essential definitions

- An **online algorithm** receives a request sequence incrementally and must act without seeing its unrevealed suffix.
- An **offline optimum**, $OPT(\sigma)$, sees the entire sequence $\sigma$ and is a comparison benchmark, not an implementable policy.
- For minimization, an algorithm is **$c$-competitive** when constants $c\ge1$ and $\alpha\ge0$ exist such that $ALG(\sigma)\le cOPT(\sigma)+\alpha$ for every allowed sequence.
- The **competitive ratio** is the smallest defensible $c$ under the declared model, including request timing, information, costs, randomization, and adversary.
- An **adversary** constructs or selects sequences. An **oblivious adversary** fixes the sequence before seeing random choices; an **adaptive adversary** may react to observed actions.
- A **deterministic** policy has no random choices. A **randomized competitive guarantee** bounds expected cost or another stated probability measure under a declared adversary.
- A **state** is the information retained from the observed prefix; a **transition** maps state and current request to action, cost, and next state.
- **Resource augmentation** compares the online method with extra capacity or speed against an offline benchmark with less.
- **Advice** is limited information about the future supplied to the online method; advice length is part of the model.
- **Regret** compares cumulative loss with a comparator from a class, while competitive analysis commonly compares with a sequence-specific offline optimum.

### Central model, mechanism, or theorem

In discrete ski rental, renting costs 1 per day and buying costs integer $B\ge1$. The deterministic threshold policy rents for the first $B-1$ days and buys at the start of day $B$ if skiing continues. For a season of $n$ days,

$$
ALG(n)=
\begin{cases}
n,&n<B,\\
2B-1,&n\ge B,
\end{cases}
\qquad
OPT(n)=\min(n,B).
$$

Thus $ALG(n)=OPT(n)$ for $n<B$, while for $n\ge B$,

$$
\frac{ALG(n)}{OPT(n)}=2-\frac1B<2.
$$

This proof depends on decision timing and indivisible days. Continuous time yields the familiar deterministic factor 2 as a supremum. The theorem does not predict average production cost without a workload distribution.

### Critical invariants

- The online action uses only the revealed prefix and explicitly permitted side information.
- Online and offline policies face the same feasible actions, costs, timing, and initial state unless augmentation is declared.
- Every cost—including switching, migration, rejection, observation, and rollback—is charged consistently.
- The offline benchmark is feasible and recomputed under the identical model.
- Randomized guarantees name expectation, tail or probability semantics and the adversary's power.
- Additive constants are reported and evaluated at operational scales.
- Tie-breaking, arrival order, cancellations, simultaneous requests, and end-of-sequence semantics are fixed.
- Lower-bound adversaries obey the same input rules and do not use forbidden knowledge.
- Empirical tests preserve full sequences, failures, deadlines, and comparator provenance.
- Deployment has a feasible fallback, state recovery, drift monitoring, and bounded action authority.

### Common failures

Common errors include calling an ordinary streaming parser online; letting the algorithm inspect future timestamps; comparing with an infeasible clairvoyant optimum; omitting switching costs; changing the offline model; claiming an expected bound against an adaptive adversary when only an oblivious result was proved; using random future traces as proof of worst-case competitiveness; treating a poor worst-case ratio as proof of poor practical value; ignoring the additive constant; using augmentation without disclosing it; training on test sequences; and evaluating only completed requests while dropping overload failures.

### Compact example

With buy cost $B=10$, a nine-day season costs the threshold policy 9, exactly optimal. A ten-day season costs 9 rentals plus 10 to buy, or 19, while offline buys immediately for 10. The ratio is 1.9. The one extra day changes the action because the policy must protect against an arbitrarily long future.

### Connections

[ALGE-070](./070-choosing-between-exact-approximate-and-heuristic-solutions.md) selects guarantee classes under service obligations. [ALGE-072](../ROADMAP.md#block-08--online-streaming-and-dynamic-algorithms) applies online analysis to paging, and [ALGE-073](../ROADMAP.md#block-08--online-streaming-and-dynamic-algorithms) applies it to scheduling.

## Governing Question

When requests, prices, jobs, or failures arrive over time, how do we specify the information boundary, design a causal policy, compare it fairly with clairvoyance, prove upper and lower bounds, and turn that worst-case evidence into a safe operational decision?

Online algorithms are about commitment under incomplete information. The difficulty is not simply that input is large or streamed. If a program can delay all decisions until the stream ends, it is an offline algorithm with incremental input. An online problem requires an action before relevant future facts are revealed, and that action affects cost or future feasibility.

Competitive analysis asks how much worse a causal policy can be than an offline optimum on the same sequence. It is deliberately distribution-free and often pessimistic. Its strength is protection against every legal sequence. Its weakness is that the worst legal sequence may be unlike production. Rigorous engineering uses the theorem as one evidence layer, then adds distributional, empirical, and operational evidence without confusing them.

## Why This Matters

Caching must evict before the next request is known. Schedulers place jobs before future arrivals. Admission controllers accept work before future load. Cloud systems reserve capacity before prices and demand are realized. Network routes react before failures unfold. Recommenders and markets act while their actions change later observations.

Small modeling choices can reverse a theorem. Does a request reveal its duration? Can a placement migrate later, and at what cost? Are randomized actions hidden from the input process? Can jobs be rejected? Does offline face the same capacity? Are costs known before action? A competitive ratio without these details is not a portable property of a named algorithm.

Production additionally cares about tails, fairness, stability, resource caps, and recovery. An algorithm with an elegant ratio can oscillate destructively when switching is omitted from the model. A policy with no useful classical ratio may be excellent under a stable workload and conservative fallback. The job is to align proof, experiment, and service semantics.

## Prerequisites and Retrieval

Retrieve [ALGE-061](./061-approximation-ratios-and-guarantees.md) for multiplicative guarantees, [ALGE-066](./066-randomized-selection-and-sampling.md) and [ALGE-068](./068-monte-carlo-and-las-vegas-algorithms.md) for randomization, and [ALGE-070](./070-choosing-between-exact-approximate-and-heuristic-solutions.md) for evidence-aware method choice. You should know induction, inequalities, expectations, state machines, amortized analysis, and adversarial counterexamples.

This chapter establishes the general model, ski-rental proof, adversaries, lower bounds, randomization semantics, resource augmentation, distribution-aware evaluation, and operations. Paging, online scheduling, and streaming structures receive dedicated treatment in ALGE-072 through ALGE-075.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish online decision-making from incremental input processing;
2. specify reveal, action, cost, state, and termination timing;
3. define a competitive guarantee with its additive constant;
4. derive the deterministic ski-rental upper bound;
5. construct legal adversarial sequences and interpret lower bounds;
6. state randomized guarantees against the correct adversary;
7. distinguish competitive ratio, regret, distributional performance, and service reliability;
8. evaluate resource augmentation, predictions, and advice honestly;
9. design empirical tests that complement rather than replace proofs; and
10. deploy an online policy with verification, fallback, telemetry, and drift controls.

## Core Exposition

### Specify the reveal-act-cost protocol

Represent a request sequence as $\sigma=(r_1,\ldots,r_T)$. Before round $t$, the algorithm has state $s_{t-1}$ derived only from the prefix $r_1,\ldots,r_{t-1}$. The environment reveals the information allowed at round $t$; the policy chooses action $a_t$; feasibility and cost are evaluated; then the state becomes $s_t$.

Write the order explicitly. “Price is known when buying” differs from “price is revealed after commitment.” If several events share a timestamp, define their order or simultaneous semantics. Define whether the horizon $T$ is known, whether cancellation is announced, and whether state can be migrated. Charge observation or prediction costs if they consume resources.

Causality is an invariant. A replay harness should detect reads of future events. Batch preprocessing, globally normalized features, and labels computed from the completed sequence are common leakage paths. A policy evaluated with leaked suffix information is not the deployable online policy.

### Define the comparator before the ratio

The offline optimum sees all of $\sigma$ but must obey the declared action space, capacity, transition costs, and initial state. It may not teleport state, violate service constraints, or ignore migration costs. Compute or certify its value independently. If exact offline solution is intractable, a lower bound for minimization can upper-bound the measured competitive ratio only in the wrong direction; distinguish proven guarantees from empirical ratios to a best-known comparator.

For minimization, $ALG$ is $c$-competitive with additive constant $\alpha$ when

$$
ALG(\sigma)\le c\,OPT(\sigma)+\alpha
$$

for every legal finite sequence. The additive constant absorbs initial-state effects independent of sequence length. It can dominate small workloads: $c=1.1$ with $\alpha=1000$ says little when $OPT=10$. Report the finite-scale implication, not only asymptotic $c$.

For maximization, a common convention is $OPT(\sigma)\le c\,ALG(\sigma)+\alpha$, but literature varies. State direction and zero cases. Competitive difference, asymptotic ratio, strict ratio, and high-probability variants are distinct definitions.

### Derive the ski-rental threshold

Suppose each day's rental costs 1 and permanent purchase costs integer $B$. Offline pays $OPT(n)=\min(n,B)$ for a season lasting $n$ days. A deterministic online policy chooses when to buy without knowing $n$.

The threshold policy rents days 1 through $B-1$ and buys at the start of day $B$ if that day arrives. If $n<B$, it never buys and pays $n=OPT(n)$. If $n\ge B$, it pays $B-1+B=2B-1$, while offline pays $B$. The ratio is $2-1/B<2$. Both cases cover every nonnegative integer $n$, so the proof is complete under the model.

<!-- bijux-verify: {"id":"ski-rental-threshold","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"days=0 online=0 offline=0 ratio=defined-together\ndays=1 online=1 offline=1 ratio=1.000\ndays=9 online=9 offline=9 ratio=1.000\ndays=10 online=19 offline=10 ratio=1.900\ndays=100 online=19 offline=10 ratio=1.900\ninvalid_buy_cost=rejected\n","stderr":""}} -->
```python
def threshold_cost(days: int, buy_cost: int) -> tuple[int, int]:
    if days < 0 or buy_cost < 1:
        raise ValueError("invalid ski-rental input")
    online = days if days < buy_cost else (buy_cost - 1) + buy_cost
    offline = min(days, buy_cost)
    return online, offline


for days in (0, 1, 9, 10, 100):
    online, offline = threshold_cost(days, 10)
    ratio = "defined-together" if offline == 0 else f"{online / offline:.3f}"
    print(f"days={days} online={online} offline={offline} ratio={ratio}")
try:
    threshold_cost(4, 0)
except ValueError:
    print("invalid_buy_cost=rejected")
```

At $n=0$, both costs are zero and a numerical ratio $0/0$ is undefined; the inequality still holds. This boundary illustrates why theorem statements should use inequalities rather than relying only on quotient code.

### Understand deterministic lower bounds

An upper bound analyzes a policy. A lower bound shows no policy in a class can do better under the model. For ski rental, observe a deterministic policy's planned purchase time. If it buys early, an adversary ends the season around that purchase and exposes rent-plus-buy cost. If it waits too long, the adversary continues and offline buys immediately. With continuous time, balancing the two threats yields the factor-2 barrier for deterministic policies.

The adversary must be legal. It may exploit the deterministic policy, whose actions are predictable, but it cannot retroactively change revealed requests. A lower bound against deterministic algorithms does not automatically apply to randomized algorithms. Likewise, a lower bound under unknown horizon need not survive advice that reveals one future bit.

Do not confuse an adversarial proof sequence with a claim that a malicious actor generates production requests. The sequence is a witness to the limits of the information model. Operational threat models can additionally include strategic or malicious inputs, but those are separate claims.

### State randomization and adversary power together

A randomized online algorithm maps a prefix and private random state to an action distribution. Against an oblivious adversary, the sequence is fixed independently of the realized random bits, and a typical guarantee is

$$
\mathbb E_R[ALG_R(\sigma)]\le cOPT(\sigma)+\alpha
$$

for every fixed $\sigma$. An adaptive online adversary may choose later requests after observing actions. If actions reveal random choices, proofs against oblivious sequences may fail. An adaptive offline adversary with access to all random bits is stronger still.

Specify whether expectation is over the algorithm, input distribution, or both. Expected total cost does not ensure a tail deadline. A high-probability statement needs its failure probability, horizon dependence, and independence conditions. Seeded reproducibility is experimental evidence, not a conversion from expected to deterministic guarantee.

Yao's minimax principle can prove randomized lower bounds by selecting a distribution over inputs and lower-bounding every deterministic algorithm's expected cost, under appropriate finite or regularity assumptions. It is a proof technique, not permission to test one convenient random generator and claim a universal lower bound.

### Separate competitive ratio from regret

Competitive analysis compares with a powerful sequence-specific offline optimum. Online learning often studies regret against the best fixed action or policy in a comparator class:

$$
Regret_T=\sum_{t=1}^T\ell_t(a_t)-\min_{a\in\mathcal A}\sum_{t=1}^T\ell_t(a).
$$

The best fixed action may be much weaker than a clairvoyant policy that changes every round. Consequently, sublinear regret and a constant competitive ratio answer different questions. Dynamic regret, switching-cost regret, and policy regret alter the comparator again. Choose the benchmark that reflects the obligation and state its power.

### Add predictions without hiding dependence

Learning-augmented online algorithms receive predictions and seek both **consistency** when predictions are accurate and **robustness** when they are wrong. The prediction source, timing, loss, update feedback, and adversarial corruption belong to the model. A policy can interpolate between trusting predictions and falling back to a classical robust algorithm.

Report a bound as a function of prediction error only when the error measure is available and causally meaningful. Calibration on the same traces used for final evaluation leaks evidence. Monitor prediction drift and ensure catastrophic prediction errors cannot bypass hard feasibility gates.

Advice complexity makes future information explicit: an oracle supplies bits computed from the full input, and analysis asks how much advice enables a target ratio. This clarifies the value of foresight but does not make the oracle implementable. In production, forecasts or contracts may approximate advice; their error and availability must be measured.

### Use resource augmentation transparently

Sometimes no useful ratio exists under equal resources, while a slightly faster server or larger cache yields a meaningful theorem. Resource augmentation can model real engineering headroom and reveal structural stability. It must be visible in the comparison: “1.1-speed online versus unit-speed offline,” not simply “competitive.”

Augmentation is not cheating when it answers the declared question. It is misleading when extra cores, capacity, migration privilege, or rejection authority are hidden. Evaluate whether the extra resource is actually provisioned at the same tail conditions and whether contention removes it during incidents.

### Combine proof with distributional evidence

A competitive bound protects against every legal sequence but rarely predicts the observed mean. Evaluate the frozen policy on representative, held-out, and adversarial traces. Report cost relative to a certified offline comparator when possible, plus absolute service outcomes, tails, switching, overload, and failures. Preserve chronological and source-group structure; randomly shuffling events can destroy the online problem.

Compare with simple baselines, the worst-case-optimal policy, prediction-aware variants, and an offline oracle labeled unattainable. Analyze ratios carefully when $OPT=0$ or tiny. Include the additive constant. A benchmark showing ratio 1.02 does not prove 1.02-competitiveness; a theorem showing ratio 2 does not claim observed ratios cluster near 2.

Trace replay is observational. If actions affect later arrivals, inventory, or user behavior, replaying a different policy on logged outcomes can be invalid. Use a simulator with validated causal assumptions, randomized experiments where ethical, or bounds that acknowledge missing counterfactuals.

### Engineer the stateful service

Persist input sequence number, policy version, random-stream identity, state digest, action, charged cost, deadline, and checker result. Make transitions idempotent or deduplicated because retries can otherwise apply an online decision twice. Define behavior for late, duplicated, reordered, or corrected events.

Guardrails enforce hard feasibility independent of the optimizing policy. A safe fallback handles missing forecasts, corrupted state, exhausted budgets, and out-of-distribution requests. Switching and rollback are actions with cost; include them in both analysis and telemetry.

Monitor contract satisfaction, not only objective. Track competitive proxy against delayed offline solutions where available, absolute outcomes, tail latency, rejection, fairness, churn, state divergence, prediction error, and resource use. Evidence expires after model, policy, infrastructure, or workload changes.

## Definitions and Notation

$\sigma=(r_1,\ldots,r_T)$ is a finite legal request sequence and $\sigma_{1:t}$ its revealed prefix through time $t$. $s_t$ is state after round $t$, $a_t$ the action, and $c_t$ the charged cost. $ALG(\sigma)=\sum_t c_t$ unless the model specifies another aggregation. $OPT(\sigma)$ is the feasible offline comparator under identical resources and costs.

For minimization, $(c,\alpha)$-competitiveness means $ALG(\sigma)\le cOPT(\sigma)+\alpha$ for all legal $\sigma$. For randomized $ALG_R$, probability is over declared random variables, and adversary class is part of the proposition. $B$ is ski purchase cost, $n$ season length, and $R$ private random state. $\mathcal F_t$ denotes information available when action $a_t$ is chosen.

A policy is **causal** when $a_t$ is measurable with respect to $\mathcal F_t$. **Consistency** and **robustness** describe performance with accurate and inaccurate predictions under explicit error definitions. **Resource augmentation** changes a named resource on one side of the comparison. **Empirical competitive ratio** is a descriptive statistic over tested sequences, not a worst-case theorem.

## Mechanisms, Invariants, or Proof Structure

### Upper-bound proof pattern

Partition legal sequences into exhaustive cases, derive online cost, lower-bound offline cost, and combine the inequalities. For ski rental, $n<B$ and $n\ge B$ are exhaustive. The proof uses no input distribution. Boundary $n=0$ is handled by the inequality because the quotient is undefined.

Potential functions often support more complex proofs. Choose $\Phi(s^{ALG},s^{OPT})\ge0$ so amortized online cost satisfies

$$
c_t^{ALG}+\Phi_t-\Phi_{t-1}\le c\,c_t^{OPT}.
$$

Summing telescopes. If $\Phi_0=0$ and $\Phi_T\ge0$, then $ALG(\sigma)\le cOPT(\sigma)$. If endpoints are merely bounded, they create an additive constant. The potential is analysis state; it need not be computed by the algorithm.

### Lower-bound proof pattern

Declare the algorithm class and adversary. Construct only legal requests based on permitted observations. Show every algorithm either incurs high cost in one branch or exposes itself to another. Relate the resulting online cost to a feasible offline strategy, which upper-bounds $OPT$ for a minimization lower-bound argument. Quantify limits, additive terms, and horizon.

### Information invariant

At action time, state and action depend only on the revealed prefix, authorized predictions or advice, configuration, and private randomness. The offline comparator may see $\sigma$ but receives no undeclared feasibility or resource privilege. Logs and replay enforce the boundary.

### Cost conservation

Every event that changes deployable state has the same modeled and measured charge on both sides when applicable. Migration, eviction, rejection, startup, observation, communication, and rollback cannot disappear from one ledger. This invariant prevents a favorable ratio created by accounting rather than algorithms.

## Alternatives and Trade-Offs

| Evidence or design | Protects against | Gives up or adds | Appropriate use |
|---|---|---|---|
| Deterministic competitive bound | Every legal sequence in the model | May be pessimistic; adversary predicts actions | Simple auditable worst-case protection |
| Randomized bound | Declared adversary with expectation or probability semantics | Randomness, tail analysis, seed governance | When randomization breaks deterministic lower bounds |
| Distributional optimization | Sampled or modeled workload | Relies on stable distribution | Repeated decisions with credible forecasting |
| Regret guarantee | Comparator class over repeated loss | Comparator may be weaker than offline optimum | Learning from repeated feedback |
| Learning-augmented policy | Good predictions plus robust fallback | Prediction pipeline and drift risk | Forecast-rich settings needing graceful degradation |
| Resource augmentation | Adversity with explicit extra capacity or speed | Unequal resources by design | Provisioned headroom and bicriteria guarantees |
| Human or offline escalation | Rare difficult or consequential requests | Queueing, cost, inconsistency | High-consequence exceptions with enough time |

Worst-case and distributional approaches can be combined. A robust policy supplies a floor; predictions improve common cases; an operational gate limits authority. The combination must be analyzed as one policy, including switching and fallback.

## Failure Modes and Misconceptions

- **“Streaming input makes the algorithm online.”** Only a decision before future revelation creates the online constraint.
- **“Offline can do anything.”** It has foresight but must obey the same declared feasibility and resource model.
- **“The ratio observed in tests is the competitive ratio.”** A finite sample is not a universal quantifier.
- **“A theorem predicts the average.”** A worst-case upper bound does not specify the workload distribution.
- **“Expected competitiveness controls tails.”** Expectation permits rare costly outcomes unless another bound is proved.
- **“Randomization always beats a deterministic adversary.”** The adversary model and information exposed by actions determine the result.
- **“Additive constants are negligible.”** They can dominate short sequences and startup-heavy services.
- **“Predictions are free advice.”** Acquisition time, errors, leakage, privacy, and drift belong to the system.
- **“More capacity is an implementation detail.”** It changes the theorem and must be disclosed as augmentation.
- **“The offline optimum is known.”** Hard comparator problems may yield only bounds or best-known values.
- **“Replay proves production impact.”** Policy actions may change subsequent observations, breaking counterfactual replay.
- **“Rollback restores the old world.”** Stateful actions and switching costs may be irreversible; prevention and bounded authority remain necessary.

## Worked Examples

### Example 1

**Situation.** Ski rental has $B=10$ and the season lasts nine days.

**Reasoning.** The threshold policy rents every day and pays 9. Offline compares renting for 9 with buying for 10 and also pays 9. The ratio is 1. The policy did not buy because day 10 was never revealed.

**Conclusion.** Short sequences incur no loss under this threshold.

### Example 2

**Situation.** The same season lasts ten days.

**Reasoning.** Online rents nine days and buys at day 10, paying 19. Offline buys initially for 10. The ratio is $19/10=1.9=2-1/10$. Buying one day earlier would reduce this sequence's cost but expose a shorter terminating sequence.

**Conclusion.** The threshold balances incompatible futures rather than predicting the horizon.

### Example 3

**Situation.** A claimed guarantee is $ALG(\sigma)\le1.1OPT(\sigma)+1000$, and a request trace has $OPT=10$.

**Reasoning.** The theorem permits cost up to 1011, a ratio of 101.1 on this trace. The asymptotic multiplier hides startup allowance at small scale. For $OPT=100{,}000$, the same inequality permits ratio 1.11.

**Conclusion.** Evaluate additive constants at real operating scales.

### Example 4

**Situation.** A caching evaluation lets offline evict for free but charges online 5 ms of writeback per dirty page.

**Reasoning.** The comparator is solving a cheaper problem. Even identical hit sequences produce distorted costs. Either charge both policies under the same dirty-state model or explicitly study an augmented comparator and label the asymmetry.

**Conclusion.** Model symmetry precedes ratio calculation.

### Example 5

**Situation.** A randomized policy has expected cost at most $1.6OPT$ against every sequence fixed before its coin flips.

**Reasoning.** This is an oblivious-adversary expectation guarantee. It does not imply every run costs at most $1.6OPT$, nor that an adaptive requester observing actions cannot cause larger expected cost. Tail and adaptive guarantees require separate proofs.

**Conclusion.** State randomness, quantifiers, and adversary in the claim.

### Example 6

**Situation.** An online scheduler is 2-competitive with processors 10% faster than offline's processors.

**Reasoning.** The result may directly model provisioned headroom, but equal-speed competitiveness has not been shown. Tests must verify that the 10% speed advantage persists under shared load. Report both speed factors and the cost metric.

**Conclusion.** Resource augmentation is useful evidence only when explicit and real.

### Example 7

**Situation.** Historical ski seasons last one day with probability 0.99 and 1,000 days with probability 0.01, with $B=10$.

**Reasoning.** Always renting has expected cost $0.99(1)+0.01(1000)=10.99$; always buying costs 10; the threshold policy costs $0.99(1)+0.01(19)=1.18$. These distributional expectations do not change its worst-case proof and depend completely on the assumed distribution.

**Conclusion.** Workload evidence can distinguish policies whose theorem labels alone do not predict the mean.

### Example 8

**Situation.** A selector labels traces using the cheaper of online policy and offline optimum, then includes final sequence length as a feature.

**Reasoning.** Final length is unrevealed when early actions occur. The learned policy receives clairvoyance and cannot be deployed as evaluated. Replace it with prefix features or an authorized forecast and include forecast error and acquisition cost.

**Conclusion.** Feature availability is part of online correctness.

### Example 9

**Situation.** A capacity controller alternates between two states whenever a one-unit price advantage appears, while migration costs 20.

**Reasoning.** An objective omitting migration rewards oscillation. Add transition cost to both online and offline ledgers; use hysteresis or a potential argument to control switching. Historical comparison must replay state transitions, not independent per-round choices.

**Conclusion.** State change is an action with cost, not free bookkeeping.

### Example 10

**Situation.** A prediction-aware admission policy sees a sudden feature shift and starts rejecting twice as many requests.

**Reasoning.** Route low-confidence or out-of-distribution cases to the robust baseline, preserve hard capacity and fairness guards, and record counterfactual limits. Investigate drift on a governed window. If observations guide retraining, they cannot also serve as untouched final evidence.

**Conclusion.** Robust fallback and evidence refresh bound the risk of learned online decisions.

## Cross-Program Connections

- **Theory of Computation and Complexity:** adversarial lower bounds and information restrictions characterize limits beyond ordinary runtime classes.
- **Operating Systems:** paging, admission, scheduling, and resource allocation expose irrevocable decisions and switching costs.
- **Network Engineering:** routing and congestion control act on delayed observations under failures and strategic traffic.
- **Distributed Systems Engineering:** partial information, event reordering, retries, and state recovery complicate the reveal-act protocol.
- **Data Engineering:** chronological provenance, leakage-resistant trace splits, and immutable replay data protect empirical conclusions.
- **Software Delivery and Reliability Engineering:** deadlines, safe fallback, load shedding, rollback, and tail telemetry govern deployment.
- **Security Engineering:** adaptive requesters, prediction poisoning, resource exhaustion, and side-channel leakage change adversary power.
- **Algorithm Engineering:** [ALGE-072](../ROADMAP.md#block-08--online-streaming-and-dynamic-algorithms) specializes the model to caching; ALGE-074 and ALGE-075 separate streaming summaries from online commitments.

## References

1. Allan Borodin and Ran El-Yaniv, *Online Computation and Competitive Analysis*, Cambridge University Press, 1998, ISBN 978-0-521-56392-5. [Publisher front matter](https://assets.cambridge.org/97805216/19462/frontmatter/9780521619462_frontmatter.pdf). Monograph reference for online models, adversaries, and competitive analysis; publisher record checked 2026-09-05.
2. Daniel D. Sleator and Robert E. Tarjan, “Amortized Efficiency of List Update and Paging Rules,” *Communications of the ACM* 28(2), 1985, 202–208. DOI: [10.1145/2786.2793](https://doi.org/10.1145/2786.2793). Primary source establishing classical competitive analysis for list update and paging; ACM record checked 2026-09-05.
3. Anna R. Karlin, Mark S. Manasse, Larry Rudolph, and Daniel D. Sleator, “Competitive Snoopy Caching,” *Algorithmica* 3, 1988, 79–119. DOI: [10.1007/BF01762111](https://doi.org/10.1007/BF01762111). Primary source for competitive caching and adversarial analysis; publisher record checked 2026-09-05.
4. Andrew Chi-Chih Yao, “Probabilistic Computations: Toward a Unified Measure of Complexity,” *FOCS 1977*, 222–227. DOI: [10.1109/SFCS.1977.24](https://doi.org/10.1109/SFCS.1977.24). Primary source for the minimax technique used in randomized lower bounds; IEEE record checked 2026-09-05.
5. Richard M. Karp, Umesh V. Vazirani, and Vijay V. Vazirani, “An Optimal Algorithm for On-line Bipartite Matching,” *STOC 1990*, 352–358. DOI: [10.1145/100216.100262](https://doi.org/10.1145/100216.100262). Primary result showing the role of randomization in online matching; ACM record checked 2026-09-05.
6. Nikhil Bansal, Niv Buchbinder, and Joseph Naor, “A Primal-Dual Randomized Algorithm for Weighted Paging,” *FOCS 2007*, 507–517. DOI: [10.1109/FOCS.2007.43](https://doi.org/10.1109/FOCS.2007.43). Primary reference for randomized online primal-dual analysis; IEEE record checked 2026-09-05.
7. Michael Mitzenmacher and Sergei Vassilvitskii, “Algorithms with Predictions,” in *Beyond the Worst-Case Analysis of Algorithms*, Cambridge University Press, 2021, 646–662. DOI: [10.1017/9781108637435.037](https://doi.org/10.1017/9781108637435.037). Durable survey chapter for learning-augmented algorithm principles; publisher record checked 2026-09-05.
8. Tim Roughgarden, *Beyond the Worst-Case Analysis of Algorithms*, Cambridge University Press, 2020. DOI: [10.1017/9781108637435](https://doi.org/10.1017/9781108637435). Edited reference for models combining worst-case guarantees with structure and predictions; publisher record checked 2026-09-05.

## Exercises

### Exercise 1

Distinguish these situations: (a) parsing a log line by line but deciding after EOF; (b) evicting a page before the next request; (c) solving tomorrow's schedule after every job is known; (d) accepting a request before later load arrives. Identify which are online decisions and why.

### Exercise 2

For discrete ski rental with integer $B\ge1$, derive the threshold policy's cost for $n<B$ and $n\ge B$, prove its ratio is below 2 when $OPT>0$, and handle $B=1$ and $n=0$ explicitly.

### Exercise 3

A randomized policy is evaluated on shuffled historical events using final request count as a feature, and failed runs are removed. Diagnose every violation of an online or empirical evidence requirement and propose a corrected evaluation.

### Exercise 4

Design an online capacity policy with predictions and a robust fallback. Specify reveal timing, state, costs, prediction error, consistency and robustness objectives, adversary or workload assumptions, resource augmentation, and operational guards.

### Exercise 5

A delivery platform's dispatch action changes driver availability and later order arrivals. Design a rigorous evidence plan that combines competitive analysis, observational logs, simulation, limited experiments, safety and fairness constraints, fallback, and drift response without claiming unavailable counterfactuals.

## Answers to the Exercises

### Answer 1

(a) is incremental input processing but not an online decision because action waits for the full sequence. (b) is online because eviction commits before the next request is known. (c) is offline for that scheduling horizon because all jobs precede the choice. (d) is online because acceptance consumes capacity before future demand is revealed. The implementation's streaming API does not decide classification; reveal and commitment timing do.

### Answer 2

The policy rents for days 1 through $B-1$ and buys on day $B$ if it occurs. For $0\le n<B$, it pays $n$, equal to $OPT(n)=n$. For $n\ge B$, it pays $(B-1)+B=2B-1$, while $OPT(n)=B$, so the ratio is $2-1/B\le2$. If $B=1$ and $n\ge1$, it buys immediately for 1 and is optimal. If $n=0$, both costs are zero; do not form $0/0$. Instead, the competitive inequality $0\le c0+\alpha$ holds for $\alpha\ge0$.

### Answer 3

Shuffling destroys chronological prefixes and may make future events appear before decisions. Final request count is unavailable at early action time and leaks the suffix. Removing failures conditions the sample on success and understates cost. Preserve original ordered sequences and source groups, expose only prefix or authorized forecast features, include feature time, freeze the policy, and retain every timeout, invalid action, and crash. Evaluate random seeds under a declared adversary or trace-sampling model, report cost and tail distributions against a feasible same-model offline comparator, and keep a separate untouched test period.

### Answer 4

At each interval, reveal current demand, available capacity, and a forecast generated before action. State includes committed capacity, pending work, recent prediction errors, and policy version. Charge provisioning, shortage, rejection, migration, and switching. Define a prediction error such as horizon-weighted absolute demand error; seek low cost when it is small while proving or testing a bound no worse than a named baseline when it is large. State whether arrivals are arbitrary, oblivious to private randomization, or sampled from a process. If online has extra capacity or speed, quantify it. Enforce hard capacity and safety checks, confidence-based routing to the baseline, deadline and budget limits, deduplicated transitions, complete logs, and rollback. Validate on chronological held-out traces and adversarial stress sequences.

### Answer 5

First specify the causal dispatch model and prove any feasible competitive bound against an offline dispatcher with identical constraints and switching costs. Logged replay can evaluate only outcomes whose counterfactual response is defensible; explicitly mark driver and order reactions as unidentified. Build a simulator from separate data and validate its conditional predictions on held-out interventions, reporting model error. Where ethical and authorized, use a limited randomized rollout with guardrails to estimate causal effects. Make safety, legal, and fairness constraints independent gates; use conservative fallback and human escalation for uncertain cases. Record state, input, action, policy, randomization, cost, override, and outcomes. Monitor service, safety, fairness, feature, and response drift. Stop or roll back on predetermined thresholds, and require fresh confirmation after policy or simulator retraining. Competitive, simulation, observational, and experimental evidence remain separately labeled.
