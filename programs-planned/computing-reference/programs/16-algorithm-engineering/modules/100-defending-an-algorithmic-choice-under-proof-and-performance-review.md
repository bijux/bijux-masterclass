---
module_id: ALGE-100
program: Algorithm Engineering
level: 2
module_number: 100
title: Defending an Algorithmic Choice Under Proof and Performance Review
status: complete
last_verified: 2026-09-05
---

# Defending an Algorithmic Choice Under Proof and Performance Review

## One-Page Review

### Governing question

How do we defend an algorithmic choice as a bounded, reviewable engineering decision whose correctness, complexity, numerical, empirical, operational, security, and lifecycle claims are supported by the right evidence?

### Essential definitions

- A **decision claim** states what is chosen, for which domain, under which constraints, relative to which alternatives, and until which reassessment trigger.
- A **gate** is a noncompensable requirement such as correctness, maximum memory, deadline, privacy, or license compatibility.
- A **decision criterion** ranks candidates that pass every gate.
- A **warrant** explains why cited evidence supports a claim.
- A **rebuttal condition** identifies evidence or circumstances that would weaken or overturn the decision.
- An **evidence dossier** binds requirements, alternatives, claims, proofs, implementations, experiments, risks, and operations.
- **residual risk** remains after controls and evidence.
- A **review disposition** is accept, accept with conditions, gather evidence, restrict scope, or reject.

### Central model, mechanism, or theorem

Let candidate set $A$, required gates $g_j(a)$, feasible set

$$
F=\{a\in A:g_j(a)\le 0\ \text{for every required }j\},
$$

and declared ranking rule $r(a)$. The decision chooses $a^*=\arg\min_{a\in F}r(a)$, with deterministic tie-breaking, only after evidence supports each gate and comparison at the required confidence. This establishes optimality only relative to the evaluated candidates, evidence, constraints, and rule. It does not prove global superiority or future fitness.

### Critical invariants

- The decision question, stakeholders, consequences, domain, horizon, and authority are explicit.
- Semantic correctness and hard constraints are gates, not weighted score terms.
- Alternatives receive equivalent contracts, tuning opportunity, resources, and scrutiny.
- Every claim names evidence, assumptions, warrant, limitations, and rebuttal conditions.
- Formal guarantees map to the actual implementation and deployment domain.
- Performance comparisons include uncertainty, failures, overhead, total resources, and practical thresholds.
- Review findings and dissent remain recorded; decisions are not rewritten to appear inevitable.
- Deployment has a safe fallback, canary, observability, rollback, owner, expiry, and reassessment triggers.

### Common failures

Leading with benchmark rank before defining requirements; presenting one favored candidate and straw alternatives; using asymptotic bounds as latency predictions; citing tests as proof of correctness; citing a proof for a different implementation; hiding numeric or concurrency assumptions; averaging away deadline failures; trading correctness against speed in one score; interpreting absence of detected difference as equivalence; choosing weights after seeing the winner; calling a candidate Pareto-optimal without enumerating objectives; excluding integration and migration cost; dismissing reviewer counterexamples; and approving without fallback or expiry.

### Compact example

Four candidates face gates: correct output, valid numeric behavior, p99 at most 20 ms, and memory at most 120 MiB. Heap and hybrid pass; bucket uses 150 MiB and scan has p99 25 ms. Heap uses 80 MiB with mean 10 ms and adversarial cost 40 ms; hybrid uses 100 MiB with mean 9 ms and adversarial cost 35 ms. Both are Pareto-relevant because heap uses less memory, while the declared latency-first rule chooses hybrid by a 1 ms mean margin and retains heap as fallback. The defense is conditional on the evidence supporting these figures and on the gates remaining appropriate.

### Connections

[ALGE-070](./070-choosing-between-exact-approximate-and-heuristic-solutions.md) defines candidate obligations. [ALGE-091](./091-representative-workload-construction.md) through [ALGE-099](./099-reading-and-reproducing-an-algorithm-paper.md) provide the workload, benchmark, profile, adversary, tuning, statistics, portfolio, numerical, and reproduction evidence needed for final review.

## Governing Question

Given a real decision with competing implementations and imperfect evidence, what argument justifies one bounded choice, what would falsify that argument, and how will deployment detect when the decision must change?

## Why This Matters

Algorithm selection is where formal and operational worlds meet. A theorem can guarantee termination and approximation while the implementation violates numeric hypotheses. A benchmark winner can miss deadlines on adversarial inputs. A robust implementation can be too expensive to operate. Review must combine these facts without collapsing them into an opaque score.

A defensible decision is not a performance slide or a claim of certainty. It is a versioned argument that another expert can inspect, challenge, reproduce, and revise. Its quality is visible in the precision of its scope, the fairness of its alternatives, the independence of its evidence, and the safety of its response to uncertainty.

## Prerequisites and Retrieval

Retrieve specification and correctness from [ALGE-001](./001-problem-statements-inputs-outputs-and-constraints.md) through [ALGE-004](./004-inductive-correctness-proofs.md), computation-model limits from [ALGE-009](./009-machine-models-and-hidden-constants.md), mixed evidence from [ALGE-010](./010-combining-proof-and-measurement-in-algorithm-evaluation.md), route trade-offs from [ALGE-070](./070-choosing-between-exact-approximate-and-heuristic-solutions.md), and the complete experimental-judgment chain from [ALGE-091](./091-representative-workload-construction.md) through [ALGE-099](./099-reading-and-reproducing-an-algorithm-paper.md).

## Learning Objectives

After this module, you should be able to:

1. frame an algorithm decision by stakeholders, consequences, domain, obligations, horizon, and authority;
2. build a fair candidate set with semantic and hard-constraint gates;
3. construct claim-evidence-warrant-limit-rebuttal records across evidence types;
4. map proofs and complexity bounds to the exact implementation and supported inputs;
5. compare performance, resources, failure, uncertainty, and practical significance without hiding trade-offs;
6. conduct professor-style, practitioner-style, adversarial, and decision-owner review;
7. issue bounded dispositions with conditions, residual risks, dissent, and missing evidence; and
8. govern deployment through fallback, canary, monitoring, rollback, ownership, and expiry.

## Core Exposition

### Frame the decision before evaluating candidates

Write one sentence naming the decision, target population, service or batch context, time horizon, and accountable owner. Identify users, operators, maintainers, security/privacy stakeholders, cost owners, and downstream consumers. Record consequence of wrong output, missed deadline, excess memory, degraded quality, nondeterminism, and delayed delivery.

Separate requirements from preferences. A correctness invariant, regulatory constraint, or hard memory ceiling is a gate. Mean latency or operational simplicity may rank feasible candidates. State practical thresholds: a 0.2% speedup may not repay migration risk, while a small mean change can matter at enormous volume.

### Normalize the candidate contract

Each candidate must solve the same problem over the same accepted domain and return equivalent outputs under declared ties, numeric tolerances, randomness, and failure semantics. If a candidate is approximate, its quality guarantee and verification differ and must be authorized by the decision.

Document algorithm variant, data structures, parameters, compiler, libraries, precision, concurrency, hardware path, preprocessing, caches, and resource allocation. Give baselines equivalent tuning and expertise. Include “retain the current implementation” and a simpler option; they reveal whether change earns its cost.

### Build an obligation matrix

Create rows for semantic correctness, termination, complexity, numerical stability, concurrency, memory, I/O, latency, throughput, tails, energy/cost, resilience, security/privacy, reproducibility, maintainability, integration, and lifecycle. For each applicable row state requirement, claim, evidence, owner, status, limitation, and blocker.

Not every decision needs every row, but omission is explicit. Evidence types differ: proof for a universal mathematical claim under hypotheses; tests for observed cases; static analysis for specified defect classes; benchmarks for an environment/population; threat analysis for adversaries; operational evidence for deployment behavior.

### Construct the argument, not just the archive

For every material claim record:

- **claim:** precise assertion and scope;
- **evidence:** proof, check, measurement, source, or observation;
- **warrant:** why that evidence supports the claim;
- **assumptions:** premises and environment;
- **limitations:** what was not established;
- **rebuttal:** counterexample, drift, or new evidence that would overturn it.

An evidence directory without warrants forces reviewers to reverse engineer the logic. A polished narrative without artifacts cannot be checked. Link both directions: every decision claim reaches evidence, and every material result states which claim it informs.

### Map proof to implementation

Restate algorithm invariants, theorem hypotheses, termination argument, and complexity model. Then map abstract operations to code and data structures. If the proof assumes exact comparisons, nonnegative weights, atomic updates, or a priority queue operation, show how the implementation preserves them.

Separate universal guarantees from bounded verification. Property tests and exhaustive small cases can find counterexamples; they do not extend a theorem. A proof of pseudocode does not cover parsing, overflow, memory failure, cancellation, races, or output publication unless those mechanisms are modeled.

### Make empirical evidence decision-ready

Define the workload population and adversarial panels, freeze configurations, and compare complete implementations under equivalent resources. Report effects in natural units and ratios with denominators, uncertainty at the assignment unit, tails, failures, memory, I/O, energy, and overhead.

Connect speed to mechanism through profiling and complexity expectations. A significant difference without a plausible mechanism may still be real but deserves replication. A profile explanation without a controlled comparison does not establish benefit. State practical thresholds and sensitivity before choosing.

### Execute a gate-first illustration

The reference filters hard constraints, shows the surviving Pareto trade-off, applies the declared latency-first rule, and retains a lower-memory fallback.

<!-- bijux-verify: {"id":"gate-first-decision","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"admissible: ['heap', 'hybrid']\npareto_relevant: ['heap', 'hybrid']\nchosen: hybrid\nmean_margin_ms: 1.0\nfallback: heap\nall_gates_hold: True\n","stderr":""}} -->
```python
candidates = {
    "heap": {"correct": True, "numeric": True, "p99": 18, "memory": 80, "mean": 10.0, "adversarial": 40},
    "bucket": {"correct": True, "numeric": True, "p99": 12, "memory": 150, "mean": 7.0, "adversarial": 30},
    "scan": {"correct": True, "numeric": True, "p99": 25, "memory": 60, "mean": 14.0, "adversarial": 50},
    "hybrid": {"correct": True, "numeric": True, "p99": 15, "memory": 100, "mean": 9.0, "adversarial": 35},
}


def admissible(record):
    return record["correct"] and record["numeric"] and record["p99"] <= 20 and record["memory"] <= 120


eligible = [name for name, record in candidates.items() if admissible(record)]
chosen = min(eligible, key=lambda name: (candidates[name]["mean"], candidates[name]["adversarial"], candidates[name]["memory"]))
fallback = min(eligible, key=lambda name: candidates[name]["memory"])
pareto = []
for name in eligible:
    point = candidates[name]
    dominated = any(
        other != name
        and candidates[other]["mean"] <= point["mean"]
        and candidates[other]["adversarial"] <= point["adversarial"]
        and candidates[other]["memory"] <= point["memory"]
        and (
            candidates[other]["mean"] < point["mean"]
            or candidates[other]["adversarial"] < point["adversarial"]
            or candidates[other]["memory"] < point["memory"]
        )
        for other in eligible
    )
    if not dominated:
        pareto.append(name)

print("admissible:", eligible)
print("pareto_relevant:", pareto)
print("chosen:", chosen)
print("mean_margin_ms:", candidates[fallback]["mean"] - candidates[chosen]["mean"])
print("fallback:", fallback)
print("all_gates_hold:", all(admissible(candidates[name]) for name in eligible))
```

The result does not prove the input figures true or the rule socially appropriate. It demonstrates noncompensable gates and a transparent decision. Bucket's lower mean cannot buy back excess memory; scan's lower memory cannot buy back its deadline failure.

### Evaluate uncertainty and robustness

For every gate near a threshold, incorporate measurement uncertainty and worst supported cases. A point p99 estimate of 19.9 ms does not prove a 20 ms service obligation. Require an appropriate upper bound, larger sample, operational guard, or restricted claim. For deterministic resource bounds, distinguish proof from measured maximum.

Run sensitivity over workload weights, practical thresholds, failure penalties, numeric tolerance, hardware, and plausible models. If small defensible changes reverse the winner, report fragility and prefer more evidence, a portfolio, a simpler fallback, or a restricted domain.

### Compare multiple objectives visibly

Do not add milliseconds, MiB, dollars, failures, and maintainability points without normalization and authority. Show a Pareto frontier and dominated candidates. If a scalar rule is required, document units, transformations, weights, stakeholder authority, and sensitivity. Lexicographic rules are often clearer for gates followed by preferences.

Opportunity cost includes engineering time, dependency risk, training, observability, migration, and future option loss. A theoretically elegant candidate can lose on integration risk; a fast opaque portfolio can lose on auditability. Those are legitimate decision facts when stated precisely.

### Conduct layered review

A professor-style review challenges definitions, hypotheses, derivations, invariants, bounds, counterexamples, and evidence type. A practitioner-style review challenges failure, concurrency, cancellation, recovery, integration, observability, performance mechanism, and operability. Security/privacy review challenges hostile inputs, resource exhaustion, data exposure, supply chain, and abuse.

The decision owner confirms consequences and trade-off authority. Independent reviewers should be able to reproduce central checks. Record questions, responses, unresolved dissent, and dispositions. Review is not complete because everyone attended; it is complete when material objections have evidence-backed outcomes or explicit residual risk.

### Red-team the favored choice

Assign someone to construct the strongest case against the candidate: violated premise, near-threshold input, alternative baseline, selection leakage, workload shift, numeric branch, worst-case resource, concurrency schedule, dependency failure, exploit, or rollback failure.

A counterexample can invalidate a universal claim immediately. An empirical anomaly triggers scoped diagnosis and sampling, not deletion. Treat evidence that favors another candidate symmetrically. The goal is not consensus but detection of hidden assumptions before production does it.

### Issue a bounded disposition

**Accept** when gates and ranking have adequate evidence and residual risk is owned. **Accept with conditions** when a guard, canary, restricted domain, additional monitor, or expiry bounds a known uncertainty. **Gather evidence** when candidates remain indistinguishable or a near-gate claim lacks power. **Restrict scope** when fitness holds only for a regime. **Reject** when a gate fails or risk is unacceptable.

State the chosen version, supported domain, fallback, nonchosen alternatives and reasons, dissent, expiry, and triggers. Avoid “best algorithm.” Say “chosen for population P on platform class H under constraints C and evidence version E.”

### Turn review into an operational contract

Deploy behind validation, a canary or shadow path where safe, resource budgets, and automatic rollback. Monitor correctness discrepancies, quality, timeouts, tails, memory, I/O, cost, numeric exceptions, fallback, input drift, and adversarial indicators. Sampling must preserve enough provenance for diagnosis without violating privacy.

Define owner and response. A monitor without decision authority is decoration. Rollback must restore compatible state and outputs. Changes to compiler, dependency, hardware, configuration, workload, or problem semantics can invalidate evidence and require targeted re-review.

### Preserve a rational record

Real design is iterative; documentation should present the final requirements, alternatives, interfaces, claims, and reasons coherently without erasing discovery or pretending inevitability [2]. Preserve experiment and deviation history separately from the concise decision record.

The dossier includes immutable manifests, proof notes, source and build identity, test and snippet reports, workloads, raw benchmark rows, analysis, profiles, mathematical checks, risks, review minutes, decision, rollout, and reassessment. Generated summaries remain traceable to raw evidence.

## Definitions and Notation

Let candidate set be $A$, hard obligations $G=\{g_1,\ldots,g_m\}$, feasible set $F$, objective vector $q(a)$, decision rule $r$, evidence set $E$, and supported domain $D$. A candidate $a$ dominates $b$ for lower-is-better objectives if it is no worse in every objective and strictly better in at least one.

A **claim-evidence record** is $(c,e,w,h,\ell,r_b)$: claim, evidence, warrant, hypotheses, limitations, and rebuttal condition. A **decision margin** measures separation under the declared rule; it is meaningful only with uncertainty and practical thresholds. **Expiry** is the time or state after which the decision requires reassessment.

## Mechanisms, Invariants, or Proof Structure

### Gate soundness

If selection is restricted to $F$, then every chosen candidate satisfies each encoded gate. The conclusion depends on correct gate definitions and sound evidence for their values. Code that filters recorded booleans cannot prove the underlying implementation correct.

### Dominance argument

Under a fixed lower-is-better objective vector, a dominated candidate cannot be uniquely preferred by any strictly increasing scalarization of those same objectives. It can remain relevant through an omitted objective, uncertainty, fallback role, or changed constraints; therefore document the objective set before pruning.

### Argument-chain invariant

Every material decision claim has evidence and warrant; every warrant names hypotheses; every limitation and rebuttal maps to a monitor, condition, missing evidence, or accepted residual risk. Unsupported links block that portion of the decision.

### Lifecycle invariant

The deployed artifact matches the reviewed version; runtime inputs remain within supported domain; gates are continuously or periodically checked; fallback and rollback are executable; and any trigger creates a new decision version rather than silently extending the old claim.

## Alternatives and Trade-Offs

| Decision approach | Strength | Main risk | Appropriate use |
|---|---|---|---|
| gate then lexicographic rule | explicit noncompensation | priority order can be contentious | hard obligations |
| Pareto frontier | exposes trade-offs | does not choose alone | multi-objective review |
| scalar utility | produces one ranking | hides units and weight authority | agreed economic model |
| robust/minimax rule | protects hostile or uncertain cases | conservative average behavior | severe tail consequence |
| portfolio/fallback | handles regimes and uncertainty | coordination and lifecycle cost | complementary candidates |
| gather more evidence | avoids false certainty | delay and experiment cost | small or uncertain margins |

A decision can combine them: gates define admissibility, Pareto analysis exposes trade-offs, a declared rule selects, and fallback handles uncertainty. The simplest adequate structure is easier to review and operate.

## Failure Modes and Misconceptions

- **“The proof chooses the implementation.”** Proof establishes specified properties under hypotheses; engineering still evaluates constants, resources, integration, and risk.
- **“The benchmark winner passes review.”** Correctness, numeric, security, and operational gates precede ranking.
- **“A score makes trade-offs objective.”** Units, weights, and authority remain judgments.
- **“Pareto-optimal means best.”** It means nondominated under the chosen objective set.
- **“No counterexample was found.”** This is bounded evidence, not a universal guarantee.
- **“A tiny p-value justifies migration.”** Effect, uncertainty, practical value, and change risk still matter.
- **“Review eliminates risk.”** It identifies, reduces, transfers, accepts, or blocks risk.
- **“Dissent is a process failure.”** Recorded technical dissent exposes assumptions and future triggers.
- **“Rollback can be designed later.”** Irreversible state or incompatible output may make that impossible.
- **“The decision is permanent.”** Evidence expires as systems and workloads change.

## Worked Examples

### Example 1

**Situation.** An approximate solver is 4x faster but the service contract requires an exact optimum.

**Reasoning.** Exactness is a gate unless the decision owner changes the product contract with appropriate consequence review. A finite penalty cannot compensate an invalid output. The solver can be reconsidered as an incumbent generator if an exact verifier/certifier preserves the obligation.

**Conclusion.** Semantic requirements filter candidates before performance ranking.

### Example 2

**Situation.** A proof assumes nonnegative edge weights, while production ingestion can contain negative adjustments.

**Reasoning.** Map the input validator and failure policy to the hypothesis. Either reject negatives before dispatch, choose an algorithm supporting them, or narrow the domain. Tests on positive graphs cannot bridge the premise gap.

**Conclusion.** A theorem supports deployment only when mechanisms enforce its hypotheses.

### Example 3

**Situation.** Candidate A is 0.4 ms faster on average, with a confidence interval from -0.7 to 1.5 ms and migration cost equivalent to 2 ms per request for a year.

**Reasoning.** Evidence does not establish a practically useful benefit. Retain baseline or gather more representative data unless another objective supplies value. A significance threshold would not replace the economic comparison.

**Conclusion.** Uncertain effects below practical cost do not justify change.

### Example 4

**Situation.** Candidate B wins mean latency but exceeds the hard memory limit on 0.1% of adversarial inputs.

**Reasoning.** If the limit protects node stability, the observed violation fails a gate. Restrict B to a proven guarded domain with fallback or reject it. Averaging memory cannot compensate an out-of-memory event.

**Conclusion.** Rare hard-constraint failures remain disqualifying unless explicitly contained.

### Example 5

**Situation.** Two candidates are within noise on latency; one has half the dependency surface and an immediate rollback path.

**Reasoning.** If equivalence within the practical margin is supported, maintainability and reversibility can decide. Document them as criteria with evidence, not as vague preference. If equivalence is not established, say evidence is insufficient.

**Conclusion.** Operational simplicity is legitimate after performance uncertainty is treated honestly.

### Example 6

**Situation.** A review score adds 10 ms latency, 20 MiB memory, one security finding, and “3 maintainability points.”

**Reasoning.** Addition has no natural units or stakeholder authority and can let safety be compensated. Convert noncompensable items to gates, show objective dimensions separately, and use an agreed rule with sensitivity for the rest.

**Conclusion.** Transparent structure beats dimensionless arithmetic.

### Example 7

**Situation.** A red-team graph makes a supposedly linear implementation allocate quadratically.

**Reasoning.** Preserve the counterexample, trace representation and hidden operation, and determine whether the theorem covered that structure. Fix and re-run proofs/tests/benchmarks or restrict the supported domain. Do not remove the input as “unrepresentative” if users or attackers can supply it.

**Conclusion.** One valid counterexample can overturn a universal resource claim.

### Example 8

**Situation.** A parallel winner uses eight cores versus a one-core baseline but reports only wall time.

**Reasoning.** Re-run under the decision's resource contract and report wall time, core-seconds, memory, energy, and contention. It may remain right for latency-critical service, but the warrant must name the resource exchange.

**Conclusion.** Performance defense accounts for all resources relevant to the owner.

### Example 9

**Situation.** Reviewers disagree whether a numerical tolerance preserves downstream ranking.

**Reasoning.** Record dissent, construct boundary cases, derive an error-to-ranking condition, compare with higher precision, and use an indeterminate/fallback path near the boundary. Do not settle a mathematical dispute by majority vote.

**Conclusion.** Unresolved numeric uncertainty becomes a guard or blocker.

### Example 10

**Situation.** Six months after acceptance, workload density shifts and fallback use triples.

**Reasoning.** The original claim was conditioned on a population and route shares. Trigger reassessment, preserve the safe version, collect new governed evidence, and evaluate retuning or a different candidate on a fresh holdout. Historical approval does not authorize silent scope expansion.

**Conclusion.** A decision remains defensible only through active lifecycle evidence.

## Cross-Program Connections

- [Testing and Quality Engineering STQE-002](../../13-software-engineering-testing-and-quality-engineering/modules/002-specifications-expectations-and-test-oracles.md) supplies layered independent evidence.
- [Data Engineering DE-089](../../19-data-engineering/modules/089-auditability-and-provenance.md) supplies decision and evidence lineage.
- [Concurrent and Parallel Programming CONPAR-092](../../04-programming-languages-concurrent-and-parallel-programming/modules/092-roofline-and-operational-intensity-analysis.md) connects hardware mechanisms to performance arguments.
- [Systems Engineering SYSENG-100](../../26-systems-engineering/modules/100-conducting-a-whole-system-review-of-a-software-intensive-capability.md) expands the review to mission, lifecycle, and system interactions.
- [Platform Engineering PLAT-100](../../29-platform-engineering/modules/100-defending-a-platform-strategy-to-developers-security-and-leadership.md) connects technical evidence to multi-stakeholder decision authority.
- [Data Structures Engineering DSE-010](../../17-data-structures-engineering/modules/010-benchmarking-a-structure-without-misleading-results.md) reinforces representation-aware baselines and benchmarks.

## References

1. Catherine C. McGeoch, *A Guide to Experimental Algorithmics*, Cambridge University Press, 2012. [doi:10.1017/CBO9780511843747](https://doi.org/10.1017/CBO9780511843747). Authoritative experimental algorithmics and decision evidence; publisher record checked 2026-09-05.
2. David L. Parnas and Paul C. Clements, “A Rational Design Process: How and Why to Fake It,” *IEEE Transactions on Software Engineering* SE-12(2), 1986, 251–257. [doi:10.1109/TSE.1986.6312940](https://doi.org/10.1109/TSE.1986.6312940). Primary source on coherent rational design documentation; record checked 2026-09-05.
3. Association for Computing Machinery, *ACM Code of Ethics and Professional Conduct*, adopted 2018. [Official code](https://www.acm.org/code-of-ethics). Current principles on quality, professional review, comprehensive evaluation, and risk checked 2026-09-05.
4. ISO/IEC/IEEE, *ISO/IEC/IEEE 42010:2022 Software, Systems and Enterprise — Architecture Description*, 2nd ed., 2022. [Official standard record](https://www.iso.org/standard/74393.html). Current edition and concern/viewpoint framing checked 2026-09-05.
5. Joint Task Force Transformation Initiative, *NIST SP 800-30 Revision 1: Guide for Conducting Risk Assessments*, NIST, 2012. [doi:10.6028/NIST.SP.800-30r1](https://doi.org/10.6028/NIST.SP.800-30r1). Authoritative risk-assessment structure; current publication record checked 2026-09-05.
6. Stephen E. Toulmin, *The Uses of Argument*, updated ed., Cambridge University Press, 2003. [Publisher record](https://www.cambridge.org/core/books/uses-of-argument/26CF801BC12004587B66778297D5567C). Claim, warrant, qualifier, and rebuttal framework; record checked 2026-09-05.
7. Tomas Kalibera and Richard Jones, “Rigorous Benchmarking in Reasonable Time,” *ISMM 2013*, 63–74. [doi:10.1145/2464157.2464160](https://doi.org/10.1145/2464157.2464160). Primary performance-evidence method; ACM record checked 2026-09-05.
8. Nicholas J. Higham, *Accuracy and Stability of Numerical Algorithms*, 2nd ed., SIAM, 2002. [doi:10.1137/1.9780898718027](https://doi.org/10.1137/1.9780898718027). Authoritative numerical evidence and stability reference; publisher record checked 2026-09-05.

## Exercises

### Exercise 1

Define decision claim, gate, decision criterion, warrant, rebuttal condition, evidence dossier, residual risk, and review disposition for choosing a graph algorithm.

### Exercise 2

Candidates A, B, and C have (correct, p99 ms, memory MiB, mean ms): A=(yes,18,90,11), B=(yes,21,70,8), C=(yes,17,110,10). Gates are p99 at most 20 and memory at most 100; rank survivors by mean then memory. Determine admissibility and choice, then analyze a measured ±2 ms uncertainty on p99.

### Exercise 3

A design note cites a proof for exact arithmetic, random correctness tests, a one-host benchmark, and no adversarial or numeric evidence. Diagnose what each item does and does not establish and specify missing review evidence.

### Exercise 4

Compare gate-first lexicographic selection, Pareto review, scalar utility, minimax choice, and evidence-gathering for a latency/memory/energy/security decision.

### Exercise 5

Construct a defense package for replacing a production shortest-path implementation with a parallel adaptive portfolio. Include stakeholders, semantics, alternatives, proofs, numerics, workloads, tuning, statistics, resources, threats, review, dissent, disposition, rollout, rollback, monitoring, and expiry.

## Answers to the Exercises

### Answer 1

A decision claim names the chosen graph algorithm, supported graph population, constraints, alternatives, evidence version, and reassessment horizon. A gate is a requirement that cannot be compensated, such as exact distances or memory ceiling. A criterion ranks only feasible candidates. A warrant explains why a proof or measurement supports a claim. A rebuttal condition names a counterexample, drift, or finding that would overturn it. The dossier links requirements, candidates, claims, evidence, risks, reviews, and operations. Residual risk remains after controls. A disposition accepts, conditions, requests evidence, restricts, or rejects the choice.

### Answer 2

A passes both gates. B fails p99 because 21 exceeds 20. C fails memory because 110 exceeds 100, so A is the only admissible choice despite B and C having lower means. With p99 uncertainty ±2 ms, A's true or future p99 may exceed 20; a point estimate of 18 is not automatically a certified gate. Specify the interval meaning and sampling unit, gather enough tail evidence, use a conservative upper bound, or accept A only with a runtime deadline guard and fallback. If the gate requires a deterministic bound, statistical uncertainty cannot replace a proof.

### Answer 3

The exact-arithmetic proof supports the abstract algorithm only when its hypotheses and operations map to code; it does not cover finite precision, parsing, allocation, or concurrency. Random tests provide observed correctness cases and can find defects, not prove absence. A one-host benchmark supports scoped observed performance, not portability or population-wide tails. Missing evidence includes a numeric model and adversarial boundary tests, proof-to-code mapping, independent oracle/certificates, representative and pathological workloads, fair tuned baselines, repeated sessions/machines as required, failure/resource/tail measures, statistical analysis, profile mechanism, concurrency races, security/resource exhaustion, and deployment fallback.

### Answer 4

Gate-first lexicographic selection best protects security and hard limits, but priority order must be authorized. Pareto review exposes latency/memory/energy trade-offs without inventing units, but needs another choice rule. Scalar utility can encode economic exchange when units, weights, and sensitivity are legitimate; it must not compensate security gates. Minimax protects severe uncertain tails but may sacrifice ordinary efficiency. Gathering evidence is rational when margins or near-gate estimates are uncertain and delay cost is acceptable. A defensible design commonly uses security and resource gates, a Pareto view, a declared ranking among survivors, minimax/adversarial constraints for severe cases, and new evidence when the decision is fragile.

### Answer 5

Name users, operators, maintainers, security, cost, and decision owner; define exact shortest-path semantics, weights, ties, numeric behavior, failures, deadlines, resources, and supported graphs. Compare current, simple parallel, adaptive portfolio, and retain-current alternatives under equivalent tuning and hardware. Map nonnegative-weight and concurrency proofs to implementations; independently verify paths and distances, bound overflow/roundoff, and fall back on indeterminate comparisons. Use grouped representative and adversarial workloads, frozen tuning, held-out statistical effects, profiles, tails, failures, core-seconds, memory, energy, feature/dispatch/verification cost, and drift sensitivity. Threat-model hostile graphs, feature abuse, resource exhaustion, supply chain, and output publication races. Record professor, practitioner, security, and owner reviews plus dissent. Accept only with named gates, margin, residual risk, supported domain, safe fallback, canary/shadow validation, atomic publication, rollback-compatible state, and owners. Monitor correctness discrepancies, timeout/tails, resources, numeric exceptions, route/fallback shares, input drift, and security signals. Expire on time or any algorithm, compiler, dependency, hardware, workload, or contract change; re-evaluate the new version on fresh evidence.
