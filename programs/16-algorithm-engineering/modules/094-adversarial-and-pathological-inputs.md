---
module_id: ALGE-094
program: Algorithm Engineering
level: 2
module_number: 94
title: Adversarial and Pathological Inputs
status: complete
last_verified: 2026-09-05
---

# Adversarial and Pathological Inputs

## One-Page Review

### Governing question

How do we construct, validate, minimize, and govern inputs that expose an algorithm’s worst cases, implementation discontinuities, numeric failures, resource exhaustion, and attacker-controlled complexity without confusing them with representative frequency?

### Essential definitions

- A **boundary input** lies at or near a declared transition such as empty size, capacity, cutoff, integer width, or recursion limit.
- A **pathological input** triggers disproportionately poor behavior through an algorithm, representation, runtime, or machine mechanism.
- An **adversarial input** is deliberately chosen with knowledge of a target algorithm or implementation to maximize a cost or violate a property under stated constraints.
- An **adaptive adversary** chooses later values after observing earlier behavior; an **oblivious adversary** fixes the complete input first.
- A **complexity attack** uses small or cheap input to induce excessive victim work or space.
- **Shrinking** or **reduction** searches for a simpler failure-preserving counterexample.
- An **oracle** decides whether semantic, cost, resource, or safety properties hold.

### Central model, mechanism, or theorem

Let $C_A(x)$ be the cost of algorithm $A$ on legal input $x$ and let $\mathcal{X}_n$ be legal inputs of size $n$. Worst-case cost is

$$
W_A(n)=\max_{x\in\mathcal{X}_n}C_A(x).
$$

An adversarial generator is evidence about $W_A$ only if it respects the input contract, adversary knowledge, randomness model, and cost boundary. Finding one expensive $x$ proves a lower bound for that implementation at that size; failing to find one proves no upper bound. Frequency-weighted typical performance and guarantee-oriented adversarial performance are different estimands.

### Critical invariants

- Generated cases satisfy the same legal-input contract as ordinary cases unless explicitly testing rejection.
- The oracle checks output semantics before interpreting cost.
- Input size and adversary budget are defined independently of the victim’s measured work.
- Random seeds, secret state, adaptation, preprocessing, and feedback available to the adversary are stated.
- The stress harness enforces per-case time, memory, output, recursion, process, and storage limits.
- Typical, boundary, pathological, invalid, and malicious panels are reported separately.
- Shrinking preserves legality and the exact failure predicate.
- A defense is retested against benign distribution, known pathologies, adaptive variants, and resource ceilings.

### Common failures

Calling random data adversarial; using illegal inputs to claim a legal-domain worst case; testing only sorted arrays; assuming randomized pivoting eliminates adaptive attacks; leaking a secret hash seed in the generator; measuring generator time as victim cost; shrinking away graph connectivity or schema constraints; accepting a smaller input with a different failure; running unbounded exponential cases in-process; treating no discovered counterexample as proof; publishing weaponized production targets or secrets; and fixing one signature while leaving the mechanism intact.

### Compact example

First-pivot quicksort on a sorted length-$n$ array makes partitions of sizes $0$ and $n-1$, so comparisons satisfy $T(n)=T(n-1)+(n-1)$ and total $n(n-1)/2$. At $n=8$, that is 28 comparisons. This case is adversarial for the stated pivot and partition policy, not for every quicksort implementation.

### Connections

[ALGE-008](./008-lower-bounds-and-adversary-arguments.md) gives formal adversary reasoning, [ALGE-014](./014-quicksort-and-partitioning.md) supplies a concrete target, and [ALGE-091](./091-representative-workload-construction.md) separates prevalence from stress evidence. ALGE-095 next governs parameter tuning so pathology panels do not become an overfit target.

## Governing Question

For a named algorithm, implementation, attacker or environment model, and resource budget, which legal inputs falsify assumed average behavior or guarantees, and how can the resulting counterexample be reproduced and reduced safely?

## Why This Matters

Average-case performance rests on a distribution; production inputs need not follow it. Even without a malicious actor, sorted runs, duplicate keys, skewed graphs, cancellation, alignment, and capacity boundaries can activate rare mechanisms. With untrusted input, a client may intentionally search the input space for high amplification.

Adversarial testing connects theory to operations. A worst-case recurrence identifies what structure matters; profiling reveals the implementation mechanism; a generator reaches it; resource isolation prevents the experiment becoming an incident; shrinking turns a huge failure into an explanation. The result informs algorithm choice, randomization, limits, fallback, admission control, and observability.

## Prerequisites and Retrieval

Retrieve adversary lower bounds from [ALGE-008](./008-lower-bounds-and-adversary-arguments.md), partition behavior from [ALGE-014](./014-quicksort-and-partitioning.md), randomized assumptions from [ALGE-029](./029-randomization-as-a-design-tool.md) and [ALGE-068](./068-monte-carlo-and-las-vegas-algorithms.md), input constraints from [ALGE-080](./080-engineering-algorithms-under-one-pass-and-update-constraints.md), workload panels from [ALGE-091](./091-representative-workload-construction.md), and profiling from [ALGE-093](./093-profiling-time-memory-and-i-o.md).

## Learning Objectives

After this module, you should be able to:

1. distinguish boundary, pathological, adversarial, invalid, stochastic, and representative inputs;
2. specify adversary knowledge, control, adaptation, budget, and success predicate;
3. derive input structures from recurrences, invariants, representations, and machine thresholds;
4. build deterministic and search-based generators with legality and semantic oracles;
5. test worst-case time, space, numeric, concurrency, and I/O mechanisms under safe limits;
6. minimize failures without changing the mechanism or violating constraints;
7. evaluate mitigations for performance, guarantees, residual attack surface, and benign cost; and
8. report discovered lower-bound evidence without overstating an upper bound or prevalence.

## Core Exposition

### Define the target and adversary model

Name the exact artifact: mathematical algorithm, source implementation, compiled binary, service endpoint, or configured system. State legal inputs and cost metric. A target-specific comparator adversary is different from a fixed array; a remote client sees less feedback than an in-process test harness.

Specify knowledge: source code, algorithm family, parameters, secret seed, memory size, timing, and prior responses. Specify control: values, order, batch size, concurrency, updates, cancellations, or graph topology. Specify adaptation and budget. A claim against an oblivious adversary does not automatically survive an adaptive one.

### Build a taxonomy of stress mechanisms

Algorithmic structure includes unbalanced recursion, repeated relaxation, failed backtracking, dense frontiers, long augmenting paths, or hash collisions. Representation includes pointer chasing, duplicate-heavy buckets, tombstones, fragmentation, or giant keys. Numeric mechanisms include overflow, underflow, cancellation, NaN, ill-conditioning, and non-transitive comparators.

Machine mechanisms include cache conflict, translation pressure, false sharing, NUMA placement, branch unpredictability, and vector-width tails. System mechanisms include page-cache churn, storage amplification, queue buildup, retry storms, file descriptor exhaustion, and scheduler starvation. Concurrency mechanisms include cyclic waits, unfairness, livelock, and adversarial interleavings.

### Derive cases from proofs and invariants

Read the recurrence and identify what maximizes each term. First-pivot quicksort becomes quadratic when every partition removes one element. A union-find sequence can stress a missing compression or rank rule. Dijkstra’s behavior changes with graph density and queue operations. External algorithms stress memory just below and above spill thresholds.

Read correctness assumptions too. A comparator must implement the required ordering properties; violating them tests defensive rejection, not sorting correctness over legal comparators. Graph algorithms may require nonnegative weights or acyclicity. Keep legal-domain worst cases separate from invalid-input robustness.

### Cross threshold surfaces

Test zero, one, cutoff-minus-one, cutoff, cutoff-plus-one, maximum legal, and just-over-limit rejection. Combine thresholds: size near memory capacity with high duplication and large records; graph frontier density near representation switching with skew; request size near parser limit under concurrency.

One-dimensional sweeps miss interactions. Use pairwise or factorial stress designs, then guided search where cost is the objective. Record that search is optimizer-dependent and may overfit one build or machine.

### Use a target-specific constructive witness

The reference below counts comparisons for first-pivot quicksort. Sorted, reversed, and all-equal arrays force a chain under its two-way partition rule; a hand-balanced pivot order yields smaller recursive partitions. It is intentionally limited to this implementation.

<!-- bijux-verify: {"id":"first-pivot-pathology","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"sorted: comparisons=28 sorted=True\nreversed: comparisons=28 sorted=True\nall_equal: comparisons=28 sorted=True\nbalanced_order: comparisons=13 sorted=True\n","stderr":""}} -->
```python
def first_pivot_quicksort(values):
    if len(values) <= 1:
        return list(values), 0
    pivot = values[0]
    left = [value for value in values[1:] if value < pivot]
    right = [value for value in values[1:] if value >= pivot]
    left_sorted, left_cost = first_pivot_quicksort(left)
    right_sorted, right_cost = first_pivot_quicksort(right)
    return left_sorted + [pivot] + right_sorted, len(values) - 1 + left_cost + right_cost


cases = {
    "sorted": list(range(8)),
    "reversed": list(range(7, -1, -1)),
    "all_equal": [0] * 8,
    "balanced_order": [4, 2, 1, 0, 3, 6, 5, 7],
}
for name, values in cases.items():
    result, comparisons = first_pivot_quicksort(values)
    print(f"{name}: comparisons={comparisons} sorted={result == sorted(values)}")
```

The witness establishes exact comparison counts for four length-eight fixtures on the recorded interpreter. It does not characterize production sort behavior, randomized or three-way quicksort, recursion overhead, allocation, or machine time.

### Generate rather than enumerate

Exhaustive enumeration is powerful for small finite domains and can prove bounded statements when the oracle and enumeration are complete. For large spaces, use grammar-, model-, or property-based generation so legal invariants are constructed rather than obtained by rare rejection. Bias generators toward boundaries and structural features.

Coverage guidance explores execution novelty; cost guidance maximizes time, comparisons, allocations, depth, transfers, or queue size. Metamorphic generation transforms known inputs while preserving an expected relationship. Differential testing compares independent implementations but shared bugs or underspecified behavior remain possible.

### Adapt safely

An adaptive generator observes comparison outcomes, timings, counters, or failures and selects the next candidate. It can discover target-specific witnesses unavailable to a fixed corpus. The feedback channel is part of the adversary model. Timing is noisy and may expose secrets; run in an isolated laboratory with synthetic targets and explicit authorization.

Separate generator resource cost from victim amplification. Let input cost be bytes, requests, or construction work and victim cost be comparisons, CPU, memory, I/O, or latency. Report amplification with both boundaries. Do not point experiments at external services or production systems.

### Make resource limits part of the harness

Run risky cases in a disposable, local, nonprivileged worker with explicit wall, CPU, memory, output, recursion, file, process, and storage limits. Prefer terminating one worker and preserving its input over freezing the controller. Keep external networking disabled unless the authorized experiment needs a local endpoint.

Record timeout as a result. Use exponential size escalation with a safe stop before known explosive behavior. Estimate the next step from counts where possible. A generator must not create uncontrolled files, fork bombs, credential access, or external writes.

### Construct independent oracles

Semantic oracles check exact answers, certificates, invariants, or a trusted simple implementation at small size. Cost oracles count comparisons, probes, states, recursion, queue length, allocations, or transfers when wall time would be noisy. Resource oracles enforce ceilings. Security oracles express an allowed amplification or service budget.

Avoid using the same flawed code for generator and oracle. For sorting, verify ordering and permutation; stability needs identity tags. For approximate algorithms, verify error bounds and quality metrics. For concurrency, record schedules and distinguish safety failure from lack of progress.

### Shrink while preserving the failure

Define the exact predicate before reduction: legal input, same target/build, correct/incorrect status, and cost above a threshold or same exception/invariant. Delete chunks, simplify values, contract graph structures, reduce operation sequences, and minimize concurrency schedules while rechecking constraints.

A smaller case can activate a different mechanism. Preserve diagnostic signatures such as comparison pattern, stack, counter ratio, or failing phase. Report both smallest known and threshold-minimal status honestly; greedy shrinking may find only a local minimum.

### Evaluate defenses by mechanism

Possible defenses include stronger worst-case algorithms, introspection and fallback, keyed or universal hashing under stated assumptions, three-way partitioning, randomized choices, resource limits, admission control, bounded parsing, iterative traversal, backpressure, and circuit breaking. Every defense changes costs or guarantees.

Retest ordinary workloads for overhead, known witnesses for mitigation, nearby variants for signature overfitting, adaptive search for residual weaknesses, and maximum legal cases for resource ceilings. Randomization makes guarantees probabilistic and seed secrecy operational. Rate limiting bounds arrival but not necessarily per-item amplification.

### Keep evidence panels separate

Representative workloads estimate expected deployment behavior. Boundary panels validate transitions. Pathology panels expose known mechanisms. Adversarial panels test a threat model. Invalid panels test rejection. Combining them into one average invents a meaningless prevalence distribution.

Report each panel’s construction, identity, cost metrics, and success rate. A mitigation can improve adversarial worst case while slowing typical inputs; the decision needs both. Preserve historical counterexamples as regression cases, but continue searching beyond them.

### Interpret negative searches conservatively

Failure to find a bad input means only that a named generator, budget, seeds, target, and observation channel did not find one. It is not a complexity upper bound. A proof can establish an upper bound under its model; exhaustive enumeration can establish a finite-domain bound; testing supplies discovered witnesses.

When a witness shows cost $c$ at size $n$, it establishes $W_A(n)\ge c$ for the declared cost model. Extrapolating an asymptotic class requires a family of inputs and derivation, not a fitted line alone.

## Definitions and Notation

Let $\mathcal{X}_n$ be legal inputs of size $n$, $C_A(x)$ measured cost, $W_A(n)=\max_x C_A(x)$ worst-case cost, $G(\theta,s)$ a generator with parameters $\theta$ and seed $s$, and $P(x)$ the failure predicate. Let $B_g$ and $B_v$ denote generator and victim budgets; an amplification ratio must name which victim resource is divided by which input/generator resource.

A **witness** is a concrete input satisfying $P$. A **family** gives witnesses over sizes. A **metamorphic relation** specifies how outputs or costs should relate after a transformation. A **fallback** switches mechanisms after a trigger. A **reproducer** binds target, environment, command, seed, and input.

## Mechanisms, Invariants, or Proof Structure

### Quicksort witness derivation

For first-pivot two-way partitioning on sorted distinct input, the left side is empty and the right side has $n-1$ elements. Thus $T(n)=T(n-1)+(n-1)$ with $T(1)=0$, so $T(n)=\sum_{k=1}^{n-1}k=n(n-1)/2$. The same recurrence holds for all equal values when every non-pivot value enters one side.

### Counterexample logic

One legal witness with cost $c$ proves $W_A(n)\ge c$. It does not prove equality because another input may cost more. Conversely, $k$ unsuccessful generated trials prove neither absence nor an upper bound unless generation is exhaustive and the oracle complete.

### Shrink integrity

Every accepted shrink $x'$ must satisfy legality, the same failure predicate $P(x')$, and declared diagnostic equivalence. Because reduction can be nonmonotonic, a greedy local minimum need not be globally smallest. Preserve the reduction trace and original witness.

## Alternatives and Trade-Offs

| Method | Strength | Risk | Honest claim |
|---|---|---|---|
| proof-derived witness | mechanism clarity | model/implementation gap | lower bound under premises |
| exhaustive small domain | complete bounded search | state explosion | finite-domain result |
| random/property generation | broad diversity | sparse pathologies | tested seeds/budget |
| coverage guidance | explores new control flow | coverage is not cost | discovered paths |
| cost-guided search | targets resource use | machine/build overfit | target-specific witness |
| adaptive adversary | powerful feedback | stronger threat, noise | stated feedback model |
| hand boundary suite | reviewable | limited combinations | named transitions |
| trace mutation | realistic seed structure | privacy and validity drift | preserved properties only |

Use multiple methods because each exposes different blind spots. Keep their evidence and budgets identifiable.

## Failure Modes and Misconceptions

- **“Worst case means sorted input.”** Worst structure depends on algorithm and implementation.
- **“Random input tests randomness.”** A distribution sample is not an adversary model.
- **“Randomization removes worst cases.”** It changes guarantees and adversary knowledge; adaptive or leaked-state attacks may remain.
- **“Invalid input proves poor complexity.”** It tests rejection unless the contract admits it.
- **“Timeouts should be discarded.”** They are bounded evidence of excessive cost.
- **“Smaller is always the same bug.”** Reduction can change mechanism or violate constraints.
- **“No counterexample means safe.”** Search is incomplete unless proven otherwise.
- **“Rate limiting fixes complexity.”** It bounds arrival rate, not necessarily work per accepted unit.
- **“A secret implementation is a defense.”** Threat models should not rely on obscurity of source alone.
- **“One fixed attack corpus is assurance.”** Implementations can overfit signatures while mechanisms survive.

## Worked Examples

### Example 1

**Situation.** First-pivot quicksort receives sorted values $0$ through $7$.

**Reasoning.** Each pivot is smallest, producing sizes 0 and $n-1$. Comparisons are $7+6+\cdots+1=28$. Ordering and permutation still hold, so the case is a legal performance witness.

**Conclusion.** The input proves a 28-comparison lower bound for this implementation at $n=8$.

### Example 2

**Situation.** The same implementation receives eight equal values.

**Reasoning.** Its two-way rule sends every equal non-pivot value right, again forming a chain and 28 comparisons. A three-way partition would group equals and behave differently.

**Conclusion.** Duplicate policy, not the name “quicksort,” owns the pathology.

### Example 3

**Situation.** A generator gives Dijkstra’s algorithm a negative edge and observes a wrong answer.

**Reasoning.** Negative edges violate the algorithm’s prerequisite. The case is valuable for input validation but not a correctness counterexample over Dijkstra’s legal domain. Use Bellman–Ford or generate nonnegative stress graphs for the legal claim.

**Conclusion.** Contract classification precedes interpretation.

### Example 4

**Situation.** A hash table performs well on random keys but degrades on many attacker-chosen collisions.

**Reasoning.** Expected constant-time behavior depends on hash assumptions. State whether the attacker knows or can infer the mapping and controls enough keys. Count probes and victim CPU under bounded input. Test keyed/randomized hashing, balanced buckets, and admission limits.

**Conclusion.** Expected-case assumptions become security assumptions on untrusted input.

### Example 5

**Situation.** A backtracking regular-expression engine is tested with a near-match that forces many alternatives before final failure.

**Reasoning.** Escalate input length under a subprocess timeout, record the exact pattern/engine/version and steps or time, and avoid shared production targets. Compare a linear-time engine or revised expression while preserving language semantics.

**Conclusion.** Failure-at-the-end structures can amplify backtracking dramatically.

### Example 6

**Situation.** An external sort works at 3.9 GiB but collapses at 4.1 GiB under a 4 GiB memory budget.

**Reasoning.** The pair crosses a spill boundary. Record actual peak memory, run formation, transfer bytes, filesystem state, and storage capacity. Add values at and around the true threshold; do not average the panels.

**Conclusion.** Threshold neighbors expose discontinuities hidden by coarse size ladders.

### Example 7

**Situation.** A graph failure shrinks from 50,000 vertices to 12 but loses connectivity.

**Reasoning.** If connected graphs define the claim, the shrink is invalid. Use connectivity-preserving edge deletion or contraction and recheck the exact failure, weight constraints, and diagnostic signature after every step.

**Conclusion.** A shrinker must preserve domain invariants as well as failure.

### Example 8

**Situation.** A randomized defense passes 1,000 tests with its secret seed fixed and visible to the generator.

**Reasoning.** This evaluates a seed-aware adversary, which may be stronger than remote production but weaker than one with adaptive timing feedback. Run separate hidden-seed and known-seed panels, rotate seeds correctly, and state probability and compromise assumptions.

**Conclusion.** Random-state visibility is part of the threat model.

### Example 9

**Situation.** A cost-guided search finds a slow input only on one processor model.

**Reasoning.** Inspect whether cache conflict, branch behavior, or implementation layout drives the score. Preserve the witness and profile, then test across builds and machines. It is a target-specific pathology until a portable algorithmic family is derived.

**Conclusion.** Machine-specific evidence must not be promoted silently to an algorithm theorem.

### Example 10

**Situation.** Introspective sort falls back after excessive recursion and defeats the sorted witness.

**Reasoning.** Verify the fallback trigger and worst-case bound, measure ordinary overhead, mutate duplicates and comparator costs, and search for resource peaks during transition. Do not stop at one obsolete witness.

**Conclusion.** Defenses require mechanism-level regression and renewed search.

## Cross-Program Connections

- [Security Engineering SEC-001](../../25-security-engineering/modules/001-assets-adversaries-trust-and-security-goals.md) defines adversary capability and protected resources.
- [Software Testing and Quality Engineering STQE-002](../../13-software-engineering-testing-and-quality-engineering/modules/002-specifications-expectations-and-test-oracles.md) supplies oracle discipline.
- [Data Structures Engineering DSE-029](../../17-data-structures-engineering/modules/029-hash-flooding-resistance.md) links representation to worst-case cost.
- [Operating Systems OS-040](../../22-operating-systems/modules/040-diagnosing-memory-pressure-and-thrashing.md) explains resource collapse beyond a capacity boundary.
- [Concurrent and Parallel Programming CONPAR-004](../../04-programming-languages-concurrent-and-parallel-programming/modules/004-safety-liveness-and-progress.md) distinguishes safety failure from loss of progress.
- [API and Service Engineering API-050](../../28-api-and-service-engineering/modules/050-designing-an-api-against-expected-abuse-cases.md) applies bounded-work design at an untrusted service boundary.

## References

1. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein, *Introduction to Algorithms*, 4th ed., MIT Press, 2022. ISBN 978-0-262-04630-5.
2. M. Douglas McIlroy, “A Killer Adversary for Quicksort,” *Software: Practice and Experience* 29(4), 1999, 341–344. [Publisher record](https://doi.org/10.1002/(SICI)1097-024X(19990410)29:4%3C341::AID-SPE237%3E3.0.CO;2-R). Checked 2026-09-05.
3. Jon L. Bentley and M. Douglas McIlroy, “Engineering a Sort Function,” *Software: Practice and Experience* 23(11), 1993, 1249–1265. [doi:10.1002/spe.4380231105](https://doi.org/10.1002/spe.4380231105). Checked 2026-09-05.
4. Scott A. Crosby and Dan S. Wallach, “Denial of Service via Algorithmic Complexity Attacks,” *12th USENIX Security Symposium*, 2003. [USENIX paper record](https://www.usenix.org/conference/12th-usenix-security-symposium/denial-service-algorithmic-complexity-attacks). Checked 2026-09-05.
5. OWASP Foundation, *Regular Expression Denial of Service (ReDoS)*. [OWASP reference](https://owasp.org/www-community/attacks/Regular_expression_Denial_of_Service_-_ReDoS). Checked 2026-09-05; engine behavior is implementation dependent.
6. Koen Claessen and John Hughes, “QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs,” *ICFP 2000*, 268–279. [doi:10.1145/351240.351266](https://doi.org/10.1145/351240.351266). Checked 2026-09-05.
7. Leonidas Lampropoulos, Michael Hicks, and Benjamin C. Pierce, “Coverage Guided, Property Based Testing,” *Proceedings of the ACM on Programming Languages* 3(OOPSLA), 2019. [doi:10.1145/3360607](https://doi.org/10.1145/3360607). Checked 2026-09-05.
8. Andreas Zeller and Ralf Hildebrandt, “Simplifying and Isolating Failure-Inducing Input,” *IEEE Transactions on Software Engineering* 28(2), 2002, 183–200. [doi:10.1109/32.988498](https://doi.org/10.1109/32.988498). Checked 2026-09-05.

## Exercises

### Exercise 1

Define boundary, pathological, adversarial, invalid, adaptive, witness, and amplification for a graph service.

### Exercise 2

Derive the exact first-pivot quicksort comparison count for sorted input of size 10, and state precisely what it proves.

### Exercise 3

A cost-guided generator finds a 20-second input, but shrinking produces a syntactically valid input that violates the algorithm’s nonnegative-weight prerequisite. Diagnose and repair the reduction.

### Exercise 4

Compare proof-derived construction, exhaustive enumeration, property-based generation, and adaptive cost-guided search for testing a hash table.

### Exercise 5

Design a safe adversarial evaluation for a service that parses, indexes, and searches untrusted structured documents. Include contracts, adversary model, generators, oracles, budgets, isolation, shrinking, panels, defenses, and reporting.

## Answers to the Exercises

### Answer 1

A boundary input lies near a declared graph-size, degree, queue, memory, or timeout transition. A pathology legally triggers disproportionate work, such as repeated dense frontiers. An adversarial graph/request is chosen with target knowledge to maximize victim cost; an invalid graph violates schema or algorithm preconditions and tests rejection. An adaptive client selects later documents or queries after observing responses. A witness is one concrete legal case meeting the cost/failure predicate. Amplification is a named victim resource—CPU, bytes, memory, or latency—relative to named attacker/input cost; it is meaningless without both boundaries and units.

### Answer 2

Sorted input yields partitions 0 and $n-1$, so comparisons are $9+8+\cdots+1=10(9)/2=45$. This proves that the declared first-pivot, two-way implementation makes 45 comparisons on that legal length-ten input, hence its worst-case comparison cost at size ten is at least 45. The recurrence family supports a quadratic lower bound for that implementation. It does not prove 45 is worst for all cost dimensions or apply to randomized, median-selected, three-way, or introspective quicksort.

### Answer 3

The reduced input no longer belongs to the legal domain, so it may expose missing validation but cannot replace the original legal performance witness. Restore the last legal failing case, make nonnegative weights a generator and shrinker invariant, and allow edge deletion, weight reduction toward zero, or connectivity-preserving contraction only when the exact failure predicate remains. Recheck output correctness, cost threshold, target/build, and diagnostic signature after each shrink. Preserve the original and rejected reduction trace; report a locally minimal legal witness unless global minimality is established.

### Answer 4

Proof-derived collision or probe sequences give mechanism clarity and conditional lower bounds but can mismatch the implementation. Exhaustive enumeration can establish complete finite-domain results but scales poorly. Property-based generation covers diverse legal shapes and supports shrinking but may almost never hit a sparse collision family. Adaptive cost search uses probe/time feedback to discover target-specific cases but is budget-, noise-, build-, and threat-model dependent. Combine proof-derived known witnesses, exhaustive small tables, structured random legal workloads, and isolated adaptive search; keep seeds, budgets, state visibility, and claims separate.

### Answer 5

Define accepted grammar/schema, size/depth/key limits, index/search semantics, and invalid rejection. Model attacker control over bytes, nesting, keys, ordering, concurrency, and query feedback, including whether hash state or timing is visible. Generate valid deep/wide/repetitive/duplicate/collision-oriented documents, near-limit boundaries, parser near-matches, index-skew cases, query hot spots, and separate malformed inputs. Use independent parse/schema, index consistency, and query-result oracles plus CPU, comparisons/probes, allocations/live/RSS, I/O, output, and latency ceilings. Run disposable nonprivileged local workers with wall/CPU/memory/file/process/storage/output limits and no external network. Preserve every seed/input and shrink with grammar, schema, and exact failure predicates. Report representative, boundary, pathology, malicious, and invalid panels separately. Test bounded parsing, depth/size admission, keyed hashing, worst-case structures, quotas, timeout/backpressure, and fallbacks on benign and mutated adversarial cases. State discovered witnesses and budgets; claim no upper bound, prevalence, or production safety without corresponding proof and evidence.
