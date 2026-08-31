---
module_id: SEPAT-039
program: Software Engineering: Patterns
level: 1
module_number: 39
title: Strategy
status: complete
last_verified: 2026-08-28
---

# Strategy

## One-Page Review

### Governing question

How can a family of algorithms vary independently from the context that uses them while every selected implementation preserves one behavioral contract, and selection, configuration, state, performance, failure, rollout, and governance remain explicit?

### Essential definitions

- A **strategy** encapsulates one algorithm behind a stable behavioral interface.
- The **context** supplies validated inputs and consumes results without depending on the concrete algorithm.
- A **strategy family** contains implementations intended to satisfy the same preconditions, postconditions, invariants, error, cancellation, and resource contract.
- **behavioral substitutability** means any strategy may replace another wherever the common contract applies without breaking client correctness.
- A **selection policy** chooses a strategy using trusted context/configuration; it is distinct from the strategy's algorithm.
- A **parameter** tunes one algorithm; a strategy changes the algorithm or policy implementation.
- A **stateful strategy** retains information across calls and therefore needs explicit instance scope, concurrency, reset, persistence, and reproducibility semantics.
- A **shadow/canary rollout** evaluates a candidate on limited traffic/effects before broader activation.

### Central model, mechanism, or theorem

Let common input predicate (P(x)), output relation (Q(x,y)), invariant (I), and cost envelope (B(x)) define contract (K). Strategy (sigma_i) is substitutable only if

$$
\forall x:P(x)\Rightarrow \sigma_i(x)\text{ terminates or fails as specified, }Q(x,\sigma_i(x)),I,Cost\le B(x).
$$

Selection policy (pi(ctx)=id/version/config) must return an allowed compatible strategy. Interface conformance or matching output types alone does not establish this obligation.

### Critical invariants

- Every strategy receives the same canonical owned input and satisfies common semantic/error/cancellation/resource obligations.
- Preconditions are no stronger and postconditions no weaker than the context contract permits.
- Strategy selection uses allowlisted identity/version/configuration and trusted current scope; callers cannot inject arbitrary executable code.
- Determinism, randomness seed/source, time, external data, and numeric tolerance are defined where reproducibility matters.
- Mutable strategy state has explicit lifetime, tenant/request scope, synchronization, and reset/persistence behavior.
- Result validation protects context invariants even when a plugin, model, or dynamically selected strategy is defective.
- Rollout compares correctness/safety before performance, isolates side effects, and supports bounded rollback/fallback.
- Metrics identify strategy/version/config/input cohort without leaking sensitive data or creating uncontrolled feedback.

### Common failures

Common failures include one interface whose implementations mean different things, strategies strengthening input assumptions, returning sentinel values inconsistently, hidden global/random/time state, sharing mutable instances across tenants, catching every error and silently falling back, selecting by untrusted class name, dynamic imports from payloads, configuration/schema drift, shadow code performing real effects, optimizing averages while violating tail/resource bounds, benchmarking different inputs, using experiments without guardrails, circular auto-selection feedback, and treating passing tests as universal algorithmic or high-stakes correctness.

### Compact example

A router accepts only healthy candidates and requires any strategy to return one member of that eligible set. `FirstHealthy` selects node A, `LowestLatency` selects node B, and a defective strategy returning an outsider is rejected by the context before use.

### Connections

[SEPAT-038](038-state.md) selects behavior by lifecycle state; [SEPAT-040](../ROADMAP.md) fixes an algorithm skeleton with controlled hooks. Strategy connects to [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md), [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md), and [Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md).

## Governing Question

Which algorithmic decisions genuinely vary behind one meaning, what contract makes them substitutable, and how is the concrete strategy selected, configured, observed, changed, and rejected safely?

Strategy is dependency inversion applied to algorithms. Its value comes from an honest family contract, not from replacing one `if` statement with many small classes.

## Why This Matters

Routing, scheduling, compression, validation, pricing, retry, ranking, optimization, and rendering often need alternative algorithms for environment, workload, regulation, or experimentation. A stable context should not embed every choice.

Runtime variability also expands risk. One strategy may be stateful, nondeterministic, slower, less accurate, or authorized for a different tenant. Production selection and rollout are part of correctness, not mere wiring.

## Prerequisites and Retrieval

You should understand interfaces, dependency inversion, contracts, complexity, concurrency, configuration, experiments, and observability. Retrieve these facts:

1. Same method signature does not imply the same semantics.
2. Subtypes/implementations must not demand inputs their client contract permits but they cannot handle.
3. Randomness, clocks, external services, floating point, and mutable state affect reproducibility.
4. A fallback can hide defects and change semantics unless its trigger/result are explicit.
5. Shadow execution is safe only when candidate effects are suppressed or isolated.
6. Performance comparisons require the same workload, environment, correctness constraints, and uncertainty treatment.

## Learning Objectives

After completing this module, you should be able to:

- identify a coherent strategy family rather than unrelated algorithms;
- write precondition, postcondition, invariant, error, and cost contracts;
- separate algorithm execution from selection policy and configuration;
- design stateless/stateful strategy ownership and concurrency;
- make randomness, time, external data, and numeric behavior reproducible;
- validate plugins/results and design fallback, shadow, canary, and rollback;
- compare correctness and performance with defensible evidence;
- govern high-stakes or learned strategies without overclaiming.

## Core Exposition

### Find the stable context and varying decision

The context owns workflow, input validation, authorization, and output integration. A strategy owns one decision such as selecting an eligible route or compressing a byte sequence. If implementations require entirely different inputs/outputs and clients interpret them differently, they are not one strategy family.

Name by the durable role—`RouteSelection`, `ConflictResolution`, `LayoutPolicy`—not by implementation technology. Concrete names describe behavior such as `LowestLatencyHealthy` rather than `NewAlgorithm`.

### Specify the semantic contract

Define accepted domain, canonicalization, output relation, tie-breaking, ordering, precision/tolerance, failure categories, cancellation/deadline, side effects, complexity/memory limits, and determinism. Include invariants the context will validate.

For selection among candidates, “returns a string” is insufficient. Require nonempty eligible input, returned member identity, health/capability constraints, stable tie rule, and no mutation. If no candidate is eligible, define rejection instead of each strategy inventing behavior.

### Apply behavioral substitutability

A concrete strategy may accept more inputs, provide a stronger result, or use fewer resources; it must not require stronger preconditions or weaken guarantees invisibly. A sorter that rejects duplicates cannot substitute for a contract allowing duplicates.

Different strategies may produce different valid answers where (Q) is relational—several routes may be eligible. Tests compare contract properties and reference results where unique, not always byte equality.

### Keep selection policy separate

Selection depends on tenant, workload class, feature/config version, capability, region, experiment cohort, regulatory approval, and operational health. Put that mapping in a policy/registry, not inside every algorithm and not in untrusted input.

Return stable strategy ID, implementation version, validated configuration version/digest, and reason. This makes replay, audit, rollback, and metrics possible.

### Prefer explicit construction and allowlists

Inject a concrete strategy or resolve a stable allowlisted identifier. Never instantiate arbitrary class/module names, expressions, scripts, or serialized objects supplied by clients.

Validate config schema, ranges, cross-field constraints, size, provenance, signature/integrity where required, and compatibility with implementation version. Unknown strategy/version/config fails closed or uses an explicitly approved fallback.

### Decide ownership of state

Stateless immutable strategies can be shared. Stateful adaptive/round-robin/cache/model strategies need declared scope: call, request, tenant, aggregate, worker, or global. State affects thread safety, fairness, recovery, and tests.

Do not hide state in global singletons. Provide synchronization or confinement, bounded memory, reset/eviction, persistence/migration if durable, and metrics for state age/cardinality. Cross-tenant learning/state requires an explicit privacy/fairness design.

### Make nondeterminism explicit

Inject a random source/seed and clock rather than reading ambient globals when reproducibility matters. Record strategy/version/config, seed or sampling decision, relevant input digest/version, and external-data/model version.

Parallel reductions and floating point may vary even with the same seed. Specify tolerances, ordering, hardware/runtime constraints, or reproducible algorithm where exact replay is required.

### Bound effects and failures

Pure strategies are easiest to compare and retry. If a strategy calls external services or mutates state, define idempotency, timeout, retry owner, circuit/bulkhead, authorization, and indeterminate outcomes. Often the strategy should return a plan and the context performs effects.

Use typed errors: invalid input, no feasible solution, deadline/cancelled, unavailable dependency, resource limit, unsupported config, and internal defect. Do not turn every defect into “no result.”

### Validate results at the context boundary

The context checks cheap critical postconditions: chosen item belongs to eligible set, schedule respects hard capacity, route begins/ends correctly, output size/format is bounded. This protects against plugins, stale models, configuration mistakes, and algorithm defects.

Validation is defense and evidence for one result, not proof of optimality or universal correctness. Expensive independent verification may be justified for high-consequence results.

### Treat fallback as a semantic transition

Define which failures permit fallback, whether inputs/effects are still safe to retry, which fallback is compatible, and how the outcome is labeled. Never fallback after an indeterminate non-idempotent effect without reconciliation.

Bound fallback chains and prevent cycles. Alert on rate/reason; prolonged fallback may satisfy availability while violating quality/cost objectives.

### Compare performance scientifically

First establish contract correctness on shared fixtures/properties/adversarial cases. Benchmark equivalent inputs, warmed/cold states as relevant, fixed resource limits, real toolchain/hardware, repeated trials, and distribution/tail metrics.

Report throughput, latency percentiles, memory/allocations, external calls/bytes, solution quality, failures, and uncertainty. Complexity analysis explains scaling; benchmarks provide empirical evidence for sampled workloads.

### Roll out safely

Offline replay compares deterministic or captured inputs without real effects. Shadow execution sends production-shaped inputs to a candidate while suppressing candidate effects and protecting data. Canary selects bounded cohorts with guardrails and rollback.

Correctness/safety/error/resource gates precede business/performance optimization. Maintain an independent kill switch/fallback, compatible old config, and rollback of strategy plus state/model/config—not just code.

### Avoid experiment contamination

Assign cohorts stably at an appropriate unit, prevent cross-over/interference where possible, predefine metrics/guardrails/stopping rules, and distinguish exploratory from confirmatory evidence. Multiple comparisons and adaptive allocation affect inference.

An experiment can compare outcomes under its population/period; it does not prove universal superiority, fairness, causal mechanisms beyond design, or safety for excluded groups.

### Govern learned or high-stakes strategies

ML strategies add training/data provenance, target definition, leakage, distribution shift, subgroup performance, calibration, explainability, monitoring, and retraining/rollback. The common output type does not make a model interchangeable with a rule-based strategy under all conditions.

For medical, financial, legal, safety, or rights-affecting decisions, define human/domain authority, contestability, audit, protected constraints, independent validation, and regulatory obligations. Strategy structure supplies no domain approval.

### Test and operate the family

Run one contract suite against every strategy. Add algorithm-specific proofs/fixtures, metamorphic/property/differential tests, invalid/resource/adversarial cases, determinism checks, concurrency/state isolation, cancellation/deadlines, selection/config migration, fallback cycles, and shadow-effect suppression.

Observe selections, version/config/cohort, contract violations, result quality, error/fallback, latency/resource, state size/age, and rollout guardrails with bounded low-cardinality labels and sensitive-data protection.

## Definitions and Notation

Let contract (K=(P,Q,I,F,B)): input predicate (P), output relation (Q), invariant (I), failure set/semantics (F), and resource envelope (B). Strategy family

$$
\Sigma_K=\{\sigma\mid\forall x:P(x)\Rightarrow Contract_K(\sigma,x)\}.
$$

Selection policy (pi:T\to(strategyId,implementationVersion,configVersion)) maps trusted context (T) into an allowlisted compatible member. Execution result records selection provenance (r=(selection,outcome,evidence)).

For optimization objective (f(x,y)), feasibility (Q(x,y)) and optimality differ. A strategy may return feasible (y) without proving (f) minimal; approximation ratio or tolerance needs a separate theorem/evidence.

## Mechanisms, Invariants, or Proof Structure

### Strategy design procedure

1. Name one stable algorithmic responsibility and canonical input/output.
2. Specify pre/post/invariant/error/cancellation/resource contract.
3. Implement strategies with explicit state, nondeterminism, and effects.
4. Separate allowlisted selection and versioned configuration.
5. Validate critical result properties at context boundary.
6. Define fallback, replay, shadow, canary, guardrails, and rollback.
7. Compare correctness first, then quality/performance on controlled workloads.
8. Run shared contract/adversarial/concurrency/rollout tests and operate by version/cohort.

### Executable mechanism

This router supplies one immutable candidate tuple and validates that any strategy returns a healthy member. It demonstrates relational substitutability and rejection of a defective implementation; it does not model concurrent health changes, networking, load, persistence, or distributed routing.

<!-- bijux-verify: {"id":"strategy-route-contract","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"first=node-a\nfastest=node-b\ninvalid=strategy contract violation\n","stderr":""}} -->
```python
class FirstHealthy:
    def choose(self, candidates):
        for name, healthy, latency in candidates:
            if healthy:
                return name
        raise ValueError("no healthy candidate")


class LowestLatencyHealthy:
    def choose(self, candidates):
        eligible = [(latency, name) for name, healthy, latency in candidates if healthy]
        if not eligible:
            raise ValueError("no healthy candidate")
        return min(eligible)[1]


class DefectiveStrategy:
    def choose(self, candidates):
        return "node-outside-contract"


class Router:
    def __init__(self, candidates):
        self.candidates = tuple(candidates)

    def route(self, strategy):
        choice = strategy.choose(self.candidates)
        eligible = {name for name, healthy, latency in self.candidates if healthy}
        if choice not in eligible:
            raise ValueError("strategy contract violation")
        return choice


router = Router([("node-a", True, 30), ("node-b", True, 10), ("node-c", False, 1)])
print(f"first={router.route(FirstHealthy())}")
print(f"fastest={router.route(LowestLatencyHealthy())}")
try:
    router.route(DefectiveStrategy())
except ValueError as error:
    print(f"invalid={error}")
```

### Contract argument

Eligible set is `{node-a,node-b}`. FirstHealthy returns the first eligible member node-a. LowestLatency filters the same set and minimizes lexicographic `(latency,name)`, returning node-b because 10<30. Context validation rejects the outsider. Both valid outputs satisfy membership/health, though they differ.

This finite argument assumes an immutable snapshot, accurate health/latency values, serialized execution, terminating algorithms, and no external effects. It proves neither live routing safety nor optimal network behavior.

### Evidence layers

Review family semantics, each algorithm, selection/configuration, state/concurrency, resource/performance, rollout/experiments, and domain/high-stakes governance independently. Shared tests cannot replace algorithm-specific proof or field evidence.

## Alternatives and Trade-Offs

| Approach | Strength | Cost or limitation | Prefer when |
|---|---|---|---|
| Conditional/table | All choices visible | Context grows; algorithms coupled | Few simple stable alternatives |
| Function/callable strategy | Minimal ceremony | State/identity/config can be implicit | Small local pure algorithms |
| Strategy object | Named contract, injection, state ownership | More types/wiring | Rich alternatives or lifecycle |
| Template Method | Reuses fixed skeleton | Inheritance/coupled variation points | Algorithm structure fixed by base |
| Policy/rules table | Auditable declarative choice | Expressiveness/tooling limits | Selection/decision rules dominate |
| Plugin boundary | Independent deployment/extensibility | Trust, compatibility, isolation complexity | Third-party/independent ownership required |
| Remote strategy service | Central rollout/model ownership | Latency, availability, data exposure | Shared heavy capability merits service |

## Failure Modes and Misconceptions

- **“Same interface means interchangeable.”** Behavioral and resource contracts determine substitution.
- **“Strategy removes conditionals.”** Selection policy still chooses; it should be explicit and cohesive.
- **“Any function parameter is the pattern.”** The durable value is the family contract and lifecycle, not syntax.
- **“Different valid outputs mean one is wrong.”** Relational contracts may allow several feasible answers.
- **“Fallback is harmless.”** It changes quality/cost/semantics and may be unsafe after partial effects.
- **“Stateless class means stateless algorithm.”** Ambient caches, randomness, clocks, services, and globals are state.
- **“Config is just data.”** It selects behavior and needs schema, provenance, rollout, and rollback.
- **“Fastest benchmark wins.”** Correctness, workload equivalence, tail/resource bounds, and uncertainty precede choice.
- **“Shadow has no effect.”** Candidate code may write, call, log secrets, or consume capacity unless isolated.
- **“An A/B winner is universally best.”** Population, time, interference, multiple tests, and guardrails limit inference.
- **“A model is a drop-in strategy.”** Data/model/version/shift/fairness and failure semantics expand the contract.
- **“Result validation proves optimality.”** It may prove feasibility for one result only.

## Worked Examples

### Example 1

Both route strategies return different healthy members. Because the contract requires feasibility rather than one unique route, both are substitutable. **Conclusion:** Specify a relation when multiple outputs are valid.

### Example 2

A sorting strategy rejects duplicate keys while the context permits them. It strengthens the precondition and is not substitutable despite matching types. **Conclusion:** Preconditions are part of the interface.

### Example 3

A retry strategy reads ambient random/time state, making replay diverge. Injecting seed/clock and recording version/config makes experiments reproducible within documented limits. **Conclusion:** Nondeterminism is a dependency.

### Example 4

A shared round-robin counter mixes tenants and races across threads. Per-scope instances or synchronized partitioned state restore fairness/isolation. **Conclusion:** Strategy state needs explicit ownership.

### Example 5

A plugin returns an ID outside the eligible set. Context postcondition validation rejects it before dispatch. **Conclusion:** Trust but verify cheap critical invariants.

### Example 6

Primary times out after possibly sending an external request; fallback repeats it. Stable effect identity and reconciliation are required before fallback. **Conclusion:** Fallback cannot erase uncertainty.

### Example 7

Candidate reduces median latency but doubles p99 and memory under large inputs. Resource/tail guardrails block rollout. **Conclusion:** Averages do not define production fitness.

### Example 8

Shadow recommendation code accidentally emails users. Replacing effect adapters with recording sinks makes shadow comparison non-effecting. **Conclusion:** Shadow isolation is a mechanism, not a label.

### Example 9

An adaptive selector routes more traffic to a fast strategy, reducing data for alternatives and biasing future estimates. Logged propensities and experiment design address the feedback. **Conclusion:** Online selection changes its own evidence.

### Example 10

A clinical triage model implements the same result type as rules but lacks calibrated/subgroup/domain/workflow validation. **Conclusion:** Structural substitutability does not establish clinical equivalence.

## Cross-Program Connections

- **Object-Oriented Programming:** interfaces, composition, ownership, generics, and behavioral subtyping implement Strategy.
- **Programming Languages and Semantics:** contracts, refinement, effects, and parametricity formalize substitution.
- **Algorithm Engineering:** complexity, approximation, profiling, benchmarking, and workload selection compare implementations.
- **Software Design and Domain Modeling:** policy ownership, value objects, bounded contexts, and domain invariants define families.
- **Testing and Quality Engineering:** contract/property/differential/metamorphic and rollout tests provide evidence.
- **Concurrency and Parallel Programming:** shared state, determinism, synchronization, and parallel reductions affect behavior.
- **Security Engineering:** allowlisted loading, configuration integrity, isolation, data minimization, and current authority constrain strategies.
- **Cloud and Platform Engineering:** feature/config rollout, canaries, shadowing, quotas, telemetry, and rollback operate selection.
- **Data and Machine Learning Engineering:** model/data/version/shift/evaluation/fairness expand learned-strategy obligations.
- **Systems Engineering:** high-consequence selection needs hazard/domain validation and independent controls.

## References

1. Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, [*Design Patterns: Elements of Reusable Object-Oriented Software*](https://www.pearson.com/en-us/subject-catalog/p/Gamma-Design-Patterns-Elements-of-Reusable-Object-Oriented-Software/P200000009480/9780321700698), Addison-Wesley, 1994. Canonical Strategy intent, structure, applicability, and consequences.
2. Barbara Liskov and Jeannette Wing, [“A Behavioral Notion of Subtyping”](https://doi.org/10.1145/197320.197383), *ACM TOPLAS* 16(6), 1994. Primary behavioral-subtyping and specification foundation.
3. David L. Parnas, [“On the Criteria To Be Used in Decomposing Systems into Modules”](https://doi.org/10.1145/361598.361623), *Communications of the ACM* 15(12), 1972. Primary information-hiding and changeability foundation.
4. Thomas H. Cormen et al., *Introduction to Algorithms*, fourth edition, MIT Press, 2022, ISBN 978-0-262-04630-5. Provides correctness and complexity foundations for algorithm comparison.
5. George E. P. Box, J. Stuart Hunter, and William G. Hunter, *Statistics for Experimenters*, second edition, Wiley, 2005, ISBN 978-0-471-71813-0. Provides experimental-design and inference foundations.
6. Ron Kohavi, Diane Tang, and Ya Xu, *Trustworthy Online Controlled Experiments*, Cambridge University Press, 2020, ISBN 978-1-108-72542-5. Provides online experimentation, guardrail, instrumentation, and interpretation practice.
7. D. Sculley et al., [“Hidden Technical Debt in Machine Learning Systems”](https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems), NeurIPS 2015. Primary analysis of ML-system coupling, feedback, data dependencies, and operational debt.
8. NIST, [AI Risk Management Framework 1.0](https://doi.org/10.6028/NIST.AI.100-1), 2023. Provides governance, mapping, measurement, and management guidance for AI risk without certifying a particular strategy.

## Exercises

### Exercise 1

Trace the executable strategies and state the common contract and exact proof limits.

### Exercise 2

Write a behavioral/resource contract for interchangeable sorting strategies, including duplicates, stability, cancellation, and memory.

### Exercise 3

Design ownership and reproducibility for a stateful adaptive routing strategy under concurrency.

### Exercise 4

Plan offline, shadow, canary, experiment, fallback, and rollback for replacing a production strategy.

### Exercise 5

Review a learned high-stakes strategy without claiming safety, fairness, or domain validity.

## Answers to the Exercises

### Answer 1

Eligible candidates are node-a latency 30 and node-b latency 10; node-c is unhealthy despite latency one. FirstHealthy scans in supplied order and returns node-a. LowestLatency constructs `(30,node-a),(10,node-b)`, selects minimum `(10,node-b)`, and returns node-b. Both satisfy “return one healthy member.” Defective returns an outsider, and context membership validation raises before use.

The trace proves membership/health for two accepted results and rejection of this outsider under one immutable snapshot and serialized run. It does not prove freshness of health/latency, fairness, live network reachability, thread safety, termination/resource bounds for arbitrary strategies, or optimal end-to-end routing.

### Answer 2

Input is an owned finite sequence of elements with a declared total comparator; duplicates and empty input are allowed. Output has equal length/multiset, is nondecreasing by comparator, and does not mutate input. Stable-family members preserve original relative order of comparator-equal elements; unstable members must not inhabit that narrower family. Comparator must be deterministic/total for supplied domain or return a specified invalid-comparator failure.

Define cancellation checks/work deadline, no partial result on cancellation unless tagged, exception safety, maximum input size, and cost envelope by strategy: e.g. comparison (O(n\log n)) worst case and auxiliary memory limit. Numeric overflow/index limits and adversarial comparator cost are bounded. Contract tests cover empty/singleton, duplicates, all equal, sorted/reverse, randomized/adversarial sizes, multiset/order/stability properties, cancellation, comparator failure, memory and scaling. Algorithm-specific proof establishes bounds beyond tests.

### Answer 3

Partition adaptive state by trusted routing scope such as service/region/tenant where evidence may be shared legitimately. Each update records candidate ID/version, observation definition, timestamp/sequence, sample count, and bounded sufficient statistics. One logical owner per partition or transactional/commutative update prevents lost updates; selection reads a versioned snapshot and records it. Bound cardinality/history, decay/reset rules, cold start, missing/stale observations, and candidate removal.

Inject/record random seed or assignment probability, strategy/model/config version, input cohort, and observation version. Avoid cross-tenant leakage and delayed-outcome misattribution. Persist/migrate only if recovery needs learning continuity; otherwise define reset. Test deterministic replay from recorded evidence, concurrent updates, duplicates/reorder, stale feedback, hot keys, clock changes, eviction, restart, config rollout, fairness/guardrail properties, and adversarial metrics. Adaptive selection affects evidence, so causal claims need appropriate randomized/exploration design.

### Answer 4

Freeze common contract, reference/adversarial corpus, quality/resource thresholds, dependency versions, and rollback criteria. Offline replay old/candidate on identical captured or synthetic inputs with effects disabled; verify postconditions first, then quality/latency/memory. Shadow a bounded production-shaped stream into isolated sinks, apply data controls/quotas, and compare outcomes while primary alone acts. Canary stable cohorts with health/correctness/safety/resource guardrails and automatic/manual stop.

If an experiment is justified, predefine unit/assignment, hypotheses, power, metrics, guardrails, duration, interference/multiple-testing handling, and analysis. Fallback triggers only on classified safe failures before uncertain effects, with stable identity/reconciliation and bounded chains. Rollback includes code, model/state/config and queued/in-flight compatibility. Observe selection/reason/version/cohort, contract violations, errors/fallback, quality, p50/p95/p99, resources, and external effects. Expand only after each evidence gate; retain audit and recovery drill.

### Answer 5

Define decision purpose/population, inputs/provenance, output meaning, action boundary, loss/utility, prohibited outcomes, uncertainty/calibration, human review/appeal, fallback, timing/resource, and current authority. Establish whether model and alternative rules truly share pre/post/error contracts. Review training/label legitimacy, representativeness, leakage, missingness, subgroup sample/performance, distribution shift, robustness, privacy/security, explainability needs, model/config/version lineage, and monitoring/retraining.

Evidence includes authoritative domain requirements, independent dataset and statistical review, locked external/temporal validation, subgroup/calibration/uncertainty results with intervals, adversarial/boundary testing, comparison to standard practice, workflow/human-factors trials, shadow/canary with non-harmful outputs, security/privacy assessment, incident/appeal/rollback drills, and ongoing drift/outcome monitoring. Named domain, statistics/ML, software verification, security/privacy, human-factors, ethics/rights, quality/regulatory, and operations reviewers approve. Strategy conformance and offline metrics establish no universal safety, fairness, efficacy, or regulatory fitness.
