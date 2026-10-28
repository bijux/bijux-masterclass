---
module_id: ALGE-091
program: Algorithm Engineering
level: 2
module_number: 91
title: Representative Workload Construction
status: complete
last_verified: 2026-09-05
---

# Representative Workload Construction

## One-Page Review

### Governing question

How do we construct a finite, reproducible workload suite that supports a specific algorithmic decision for a declared target population without hiding important frequency, correlation, scale, state, tail, or adversarial behavior?

### Essential definitions

- A **target population** is the set or process of future cases about which a result intends to generalize.
- A **workload unit** is the independently identified object being sampled: request, file, graph, query stream, snapshot, or scenario.
- A **feature** is a measured property expected to affect algorithm behavior, such as size, sparsity, skew, presortedness, or update ratio.
- A **stratum** is a feature-defined subgroup sampled separately to preserve coverage or estimate subgroup behavior.
- A **mixture weight** is the target frequency assigned to a workload class when aggregating results.
- A **stress case** deliberately probes a boundary or failure; it is not evidence of normal frequency.
- A **holdout** is excluded from selection and tuning and used to test generalization.

### Central model, mechanism, or theorem

For strata $h=1,\ldots,H$ with target weights $W_h$ summing to one and stratum means $\mu_h$, the mixture mean is

$$
\mu=\sum_{h=1}^{H}W_h\mu_h.
$$

An equal-count stratified suite does not imply equal target weights. It supports comparison within every stratum, then aggregation with declared $W_h$. Representativeness is therefore a relationship among target population, sampling frame, feature model, selection procedure, weights, time window, and decision—not an intrinsic property of a data set.

### Critical invariants

- Every case has immutable identity, provenance, schema, feature values, and expected semantics.
- Selection criteria are fixed before observing candidate algorithm winners.
- Stratum membership and mixture weights derive from the target population or an explicitly hypothetical scenario.
- Train/tune/validation/holdout identities are disjoint at the correct dependency unit.
- Synthetic and transformed cases preserve only the properties actually claimed.
- Stress and adversarial cases are reported separately from frequency-weighted typical results.
- Workload construction, exclusions, missingness, and updates are versioned and reproducible.

### Common failures

Calling convenient public data “representative”; sampling rows when correlated users or graphs are the independent units; matching marginal distributions while destroying correlations; omitting tiny, huge, empty, duplicate-heavy, or failure cases; using only average size; weighting equal-count strata equally; tuning on the test set; filtering timeouts after seeing results; duplicating near-identical traces across splits; scaling data without preserving locality or skew; changing workload and implementation simultaneously; and generalizing beyond the sampled population.

### Compact example

A production mix is 70% small, 25% medium, and 5% large. A suite takes ten cases from each class to estimate all three reliably. Its raw unweighted average describes an artificial 1/3–1/3–1/3 mix. To estimate production mean, compute $0.70\mu_s+0.25\mu_m+0.05\mu_l$ and report each stratum separately so the rare large tail remains visible.

### Connections

[ALGE-009](./009-machine-models-and-hidden-constants.md) limits generalization across machines, [ALGE-010](./010-combining-proof-and-measurement-in-algorithm-evaluation.md) separates evidence types, and [ALGE-090](./090-mapping-an-algorithm-across-memory-threads-and-storage.md) identifies behavior-driving features. ALGE-092 next develops benchmark execution and reproducibility; ALGE-094 later constructs adversarial inputs.

## Governing Question

For a named algorithmic choice, target users and systems, deployment horizon, and acceptable risks, which real, traced, synthetic, scaled, boundary, and adversarial cases—and which weights—produce evidence that is both decision-relevant and honest about its limits?

## Why This Matters

An experiment can be perfectly timed and still answer the wrong question. Sorting uniform random integers does not establish performance on nearly sorted records with costly string keys. A graph suite of social networks does not represent road networks. A point-query benchmark says little about mixed updates and ranges. Workload construction determines the domain of every later conclusion.

The challenge is compression. The future population may contain billions of inputs and evolving request streams; the experiment can run only a finite suite. Compression must preserve behavior-driving diversity, frequency, correlations, and tails relevant to the decision. It must also include cases that test guarantees even when those cases are rare.

Representative does not mean realistic-looking. A synthetic generator can produce plausible degree histograms while missing community structure and locality. A real trace can be authentic yet obsolete, geographically narrow, censored, or dominated by one tenant. The correct question is not “real or synthetic?” but “which properties are supported by provenance and validation, and which conclusion needs them?”

## Prerequisites and Retrieval

Retrieve input-contract reasoning from [ALGE-001](./001-problem-statements-inputs-outputs-and-constraints.md), expected and amortized cost from [ALGE-006](./006-best-worst-expected-and-amortized-cost.md), model limitations from [ALGE-009](./009-machine-models-and-hidden-constants.md), empirical evidence from [ALGE-010](./010-combining-proof-and-measurement-in-algorithm-evaluation.md), randomization from [ALGE-029](./029-randomization-as-a-design-tool.md), constrained-input reasoning from [ALGE-080](./080-engineering-algorithms-under-one-pass-and-update-constraints.md), and resource mapping from [ALGE-090](./090-mapping-an-algorithm-across-memory-threads-and-storage.md).

## Learning Objectives

After this module, you should be able to:

1. define a target population, sampling frame, workload unit, decision, and generalization boundary;
2. identify features and interactions that drive algorithmic behavior;
3. combine random, stratified, purposive boundary, and adversarial selection without confusing their roles;
4. construct deterministic, identity-preserving workload manifests;
5. assign and use target mixture weights separately from experimental sample counts;
6. prevent tuning leakage, correlated split leakage, survivor bias, and post-outcome exclusions;
7. validate synthetic and scaled workloads against the properties they claim; and
8. document provenance, licenses, privacy transformations, missingness, versions, and limitations.

## Core Exposition

### Start from the decision

Write the decision before collecting data: choose algorithm A or B, set a threshold, size capacity, select a layout, or accept a guarantee. Name the target population and deployment horizon. “Which sort is fastest?” is underspecified; “which implementation minimizes p99 latency for next quarter’s ingest distribution under a 4 GiB memory limit while preserving stable order?” constrains workload features and metrics.

List unacceptable failures. If correctness must hold for empty input, an empty case belongs in the suite even if production rarely sends it. If large tenants dominate cost but not request count, construct both request-weighted and byte/work-weighted views. The decision selects the unit of consequence.

### Define the workload unit and sampling frame

The workload unit must match dependence. Individual requests from one burst are not independent evidence about users. Rows from one graph are not multiple graphs. Repeated queries over one warmed index share state. Choose the unit at which selection, splitting, and uncertainty make sense: tenant-day, complete graph, data snapshot, query session, or fault scenario.

The sampling frame is the enumerable source from which units can be selected. It may exclude deleted data, failed jobs, offline customers, privacy-restricted regions, or new workloads. Record coverage and missingness. A random sample from a biased frame remains biased relative to the target.

### Build a behavior-feature model

Derive features from algorithm mechanisms, not merely available columns. Sorting features include $N$, record/key bytes, duplicate fraction, run lengths, entropy, skew, comparator cost, and payload movement. Graph features include vertices, edges, degree distribution, diameter proxies, component structure, direction, weights, and frontier evolution. Search features include key popularity, range selectivity, update mix, temporal locality, and concurrency.

Include system state when relevant: cold/warm cache, fragmentation, background load, NUMA placement, storage occupancy, queue depth, and failure timing. Features interact. Large input plus low entropy may favor counting; high degree plus dense frontier changes graph traversal. Matching separate feature histograms can miss their joint distribution.

### Profile before selecting—but avoid winner leakage

Use implementation-independent profiling to understand candidates: sizes, quantiles, joint plots, missingness, temporal drift, and cluster structure. Do not run competing algorithms and then select cases that make the preferred one win. If outcome-aware selection is scientifically necessary, label it exploratory and evaluate confirmatory claims on a fresh holdout.

Freeze feature extraction code and comparator/schema versions. Derived features can contain bugs. Validate them on hand-audited cases and recompute after source changes. Retain raw identity so a surprising measurement can be traced back.

### Combine probability and purposive selection

Probability sampling supports frequency estimates when inclusion probabilities are known. Simple random sampling works when the population is sufficiently homogeneous for the metric. Stratification deliberately allocates cases across meaningful subgroups, often oversampling rare but important strata. Aggregate using target weights rather than raw counts.

Purposive cases probe boundaries: empty, singleton, cache-sized, memory-exceeding, maximum key, all equal, disconnected, or extremely skewed. Adversarial cases target known mechanisms. These strengthen guarantee and diagnostic testing but do not estimate prevalence. Report typical, boundary, and adversarial panels separately.

### Execute deterministic stratified selection

This small reference sorts each family by size and selects its endpoints. It deliberately overrepresents every family equally and therefore produces a coverage suite, not a population-frequency sample.

<!-- bijux-verify: {"id":"stratified-workload-reference","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"selected: [('graph', 50, 'road'), ('graph', 500000, 'social'), ('search', 100, 'uniform'), ('search', 1000000, 'hot-key'), ('sort', 10, 'sorted'), ('sort', 10000000, 'duplicate-heavy')]\nfamily counts: [('graph', 2), ('search', 2), ('sort', 2)]\nproduction weighted mean: 18.0\n","stderr":""}} -->
```python
def endpoint_sample(records):
    families = sorted(set(record[0] for record in records))
    selected = []
    counts = []
    for family in families:
        group = sorted(record for record in records if record[0] == family)
        chosen = [group[0], group[-1]] if len(group) > 1 else group
        selected.extend(chosen)
        counts.append((family, len(chosen)))
    return selected, counts


records = [
    ("sort", 10, "sorted"), ("sort", 10000, "random"),
    ("sort", 10000000, "duplicate-heavy"),
    ("graph", 50, "road"), ("graph", 20000, "mesh"),
    ("graph", 500000, "social"),
    ("search", 100, "uniform"), ("search", 50000, "range-heavy"),
    ("search", 1000000, "hot-key"),
]
selected, counts = endpoint_sample(records)
means = [(10.0, 0.70), (30.0, 0.25), (70.0, 0.05)]
weighted_mean = sum(mean * weight for mean, weight in means)
print("selected:", selected)
print("family counts:", counts)
print("production weighted mean:", weighted_mean)
```

This execution verifies deterministic endpoint selection and one weighted calculation on the recorded interpreter. It does not establish representativeness, independence, feature validity, or statistical precision.

### Allocate samples across strata

Equal allocation makes cross-stratum comparisons convenient, especially for rare classes. Proportional allocation mirrors frequency but can leave rare strata with too few cases. Allocation based on cost variability can improve precision for a fixed budget. The design choice depends on whether the objective is population mean, subgroup diagnosis, tail assurance, or model training.

Always preserve $N_h$, sample size $n_h$, inclusion rule, and target weight $W_h$. When units have unequal inclusion probabilities, use appropriate weights and uncertainty methods. Do not invent target weights from the experimental sample after deliberate oversampling.

### Preserve correlations and temporal structure

For joint features, stratify or cluster on combinations supported by sufficient data. A generator that samples size and skew independently can create impossible or omit common combinations. Compare joint summaries and algorithm-relevant derived behavior, not only one-dimensional histograms.

Arrival order matters for caches, adaptive algorithms, queues, and compaction. Preserve sessions, bursts, seasonality, and dependencies when the decision concerns online behavior. Shuffling can answer a deliberate order-free question, but must be labeled. Use time-based holdouts when deployment faces future drift; random splits can leak near-duplicate temporal states.

### Use real traces responsibly

Record source system, collection window, instrumentation, filters, sampling, dropped events, clock behavior, anonymization, consent/license, and schema. Traces often omit failed requests or truncate large payloads—the very cases important to reliability. Compare trace totals with independent system counters where available.

Privacy transformations can change locality, equality, ordering, and length. Hashing keys may preserve equality but destroy prefix structure; bucketing timestamps changes burstiness; removing rare tenants trims tails. State precisely which properties remain and rerun feature validation after transformation.

### Generate synthetic workloads as controlled experiments

Synthetic generators are valuable because they vary one mechanism while holding others fixed, reach larger scales, and create known ground truth. Parameterize distributions, correlations, seeds, and structural constraints. Validate generator output, not merely input parameters: realized degree, duplicates, run lengths, locality, and component structure can differ.

Use factorial or space-filling designs to explore interactions, then add real cases to test external relevance. A generator should not copy quirks of the implementation being evaluated. Keep generator revision and seed in the workload identity.

### Scale without distorting mechanisms

Duplicating a file ten times preserves records but increases duplicates and periodicity. Random vertex replication can change graph diameter and communities. Multiplying arrival rate without changing key popularity may create unrealistic contention. Scale transformations need property-specific validation.

Construct size ladders around algorithm and hierarchy transitions: insertion-sort cutoff, cache capacity, memory spill, integer-width boundary, partition count, or storage level. Include values just below, at, and above thresholds. Powers of two alone can align unusually with allocators and partitions; add neighboring and irregular sizes.

### Separate tuning, confirmation, and regression

Use a tuning set for thresholds and parameters. Use a disjoint confirmation set for the primary comparison. Hold back a final set or future time window for generalization. Split by the dependency unit, not individual rows. Near-duplicate generated cases with the same base graph belong together.

A regression suite serves stability, not unbiased discovery. It can retain known failures and fixed cases indefinitely. Do not reuse it as fresh evidence after repeatedly optimizing against it. Rotate or supplement with blinded cases.

### Define exclusions before outcomes

Predeclare invalid input, measurement failure, timeout, resource exhaustion, and correctness-failure handling. A timeout is often a result, not missing data. Excluding only slow or failed runs creates survivor bias. Use censoring-aware reporting or failure counts when exact times are unavailable.

Record every candidate and disposition in a manifest: included, excluded with reason, unavailable, invalid, or reserved. Preserve the pre-outcome rule and the evidence that triggered it. Manual deletion of “outliers” is not a workload method.

### Version and audit the suite

Each workload unit needs stable identity, content hash where lawful, provenance, schema, feature extractor version, split, stratum, weight, license/privacy status, and expected-result oracle. The suite manifest records construction code, seed, source snapshot, exclusions, and retrieval date.

Audit duplicates and leakage across splits, feature missingness, stratum coverage, weight sum, identity/hash drift, corrupted archives, and oracle consistency. Render summary tables and inspect actual examples. Deterministic checks establish structure; domain experts must judge whether omitted features threaten the decision.

### Learn from governed benchmark suites

Established suites illustrate governance. SPEC run rules bind results to build, execution, disclosure, and reporting conditions rather than treating a binary timing as self-explanatory [1]. TPC publishes versioned benchmark specifications and fair-use policies [2]. The GAP Benchmark Suite sought standardized graph evaluation across several algorithms and graph families [3]. These suites are calibrations for process, not automatically representative of a local deployment.

Use an external suite when its population and metric align, and disclose modifications. If only a subset is run, do not quote a full-suite aggregate. Check current usage and reporting rules at measurement time; standards evolve.

## Definitions and Notation

Let population strata have sizes $N_h$, sample sizes $n_h$, target weights $W_h=N_h/\sum_jN_j$ when count weighting is intended, stratum metric means $\mu_h$, and mixture mean $\mu=\sum_hW_h\mu_h$. Let $x(u)$ be the feature vector of workload unit $u$, $y_a(u)$ an outcome for algorithm $a$, and $q_p$ a population quantile.

A **sampling frame** is the selectable representation of the population. **Coverage error** arises when frame and target differ. **Selection bias** relates inclusion to outcomes or their causes. **Concept drift** changes the population over time. **Censoring** reveals only a bound, such as runtime exceeding a timeout. **Oracle** is the independent expected semantic result.

## Mechanisms, Invariants, or Proof Structure

### Weighted-estimate derivation

Partition the target into disjoint strata. The law of total expectation gives $E[Y]=\sum_hP(H=h)E[Y\mid H=h]$. Replacing the population quantities with declared target weights and stratum estimates yields $\hat\mu=\sum_hW_h\hat\mu_h$. Equal $n_h$ affects precision, not $W_h$.

### Selection integrity

Freeze candidate identities, feature computation, strata, allocation, and exclusion rules before evaluating winners. Hash the resulting manifest. Any later change creates a new workload version and requires rerunning all compared algorithms. This prevents asymmetric case sets and outcome-driven selection.

### Split integrity

Define an equivalence relation capturing dependence or derivation—for example, all queries from one session or all scaled variants of one base graph. Every equivalence class belongs to exactly one split. Audit hashes, provenance links, and near-duplicate signatures so tuning information cannot cross into confirmation accidentally.

## Alternatives and Trade-Offs

| Design | Strength | Risk | Honest use |
|---|---|---|---|
| simple random sample | direct frequency inference | misses rare regimes | homogeneous populations |
| proportional stratification | preserves mix | small rare samples | population aggregates |
| equal/oversampled strata | subgroup precision | raw mean is biased | weighted aggregation |
| real traces | authentic correlations | frame bias, privacy, drift | scoped replay |
| synthetic generators | control and scale | realism gap | mechanism isolation |
| boundary suite | transition coverage | no prevalence estimate | robustness |
| adversarial suite | tests guarantees | may be unrealistic | worst-case diagnosis |
| standard benchmark | comparability and governance | local mismatch, overfitting | calibrated external comparison |

A sound evaluation usually combines several. Report panels rather than collapsing them into one unexplained score. If an aggregate is necessary, publish its weighting rule and sensitivity to plausible alternative weights.

## Failure Modes and Misconceptions

- **“Real data is representative.”** It represents only its source, window, capture, and exclusions unless stronger evidence exists.
- **“A large sample removes bias.”** More units from a biased frame estimate the wrong population more precisely.
- **“Matching averages is enough.”** Tails, correlations, and temporal order can drive algorithm behavior.
- **“Equal stratum counts mean equal weights.”** Experimental allocation and target frequency are different.
- **“Synthetic means invalid.”** Controlled synthetic cases are strong mechanism evidence when claims are bounded.
- **“Stress cases should enter the production mean.”** Not without a defensible production weight.
- **“Random row splitting prevents leakage.”** Shared users, sessions, graphs, or derivations can cross splits.
- **“Timeouts are missing data.”** They are censored performance or failure outcomes.
- **“One standard suite settles the choice.”** Its domain and rules may not match the target decision.
- **“Workloads are immutable.”** Population drift and corrected provenance require versioned reevaluation.

## Worked Examples

### Example 1

**Situation.** A service has 70% small, 25% medium, and 5% large jobs. A suite samples ten of each; stratum means are 10, 30, and 70 ms.

**Reasoning.** The raw equal-count mean is $(10+30+70)/3=36.67$ ms. The target-weighted mean is $0.70(10)+0.25(30)+0.05(70)=18$ ms. Equal allocation improves large-stratum evidence but cannot redefine production frequency.

**Conclusion.** Publish stratum results and the 18 ms weighted estimate, not 36.67 ms as production mean.

### Example 2

**Situation.** One million requests are randomly sampled from logs that omit all timed-out requests.

**Reasoning.** Randomness applies only within the survivor frame. If timeouts correlate with large or skewed inputs, their absence biases latency and failure estimates downward. Increasing the sample does not recover excluded units. Reconcile against request counters and collect timeout metadata.

**Conclusion.** Frame coverage precedes sample size.

### Example 3

**Situation.** Explain what the executable endpoint suite establishes.

**Reasoning.** It deterministically selects smallest and largest recorded size within graph, search, and sort families, giving two cases per family. It demonstrates coverage allocation and a separate weighted calculation. It does not prove endpoints capture skew, locality, or the target mixture.

**Conclusion.** Deterministic selection is reproducible; representativeness still needs a population argument.

### Example 4

**Situation.** A graph study randomly assigns BFS sources from the same graph to tuning and holdout.

**Reasoning.** Graph structure, layout, and preprocessing are shared, so tuning learns graph-specific behavior. If the claim generalizes to unseen graphs, split by graph, then sample sources within each assigned graph. If the claim concerns new sources on the same fixed graph, the original split may be appropriate.

**Conclusion.** The dependency unit follows the generalization claim.

### Example 5

**Situation.** A synthetic graph matches vertex count, edge count, and mean degree of a social graph but has no communities.

**Reasoning.** Mean degree is forced by edge/vertex counts, yet community structure affects frontier locality, cuts, and traversal. Validate degree quantiles, clustering, components, assortativity, and algorithm-specific frontier traces. Label the generator valid only for matched properties.

**Conclusion.** Marginal realism does not preserve structural mechanisms.

### Example 6

**Situation.** Benchmark sizes are only $2^{20}$, $2^{21}$, and $2^{22}$, while an algorithm switches representation at two million items.

**Reasoning.** The suite observes 1,048,576 then 2,097,152, nearly skipping the threshold. Add cases just below, at, and above two million, plus irregular sizes, to expose conversion and boundary effects. Keep the broad scale ladder as well.

**Conclusion.** Threshold-centered cases complement geometric scale coverage.

### Example 7

**Situation.** A 60-second timeout removes 12 runs of algorithm A and none of B; the report averages remaining runs.

**Reasoning.** A’s slowest outcomes disappeared, producing survivor bias. Report 12 censored/failure outcomes and use a metric compatible with censoring or assign the declared timeout/failure penalty. Apply the same predeclared rule to both algorithms.

**Conclusion.** Timeouts are decision-relevant results, not disposable noise.

### Example 8

**Situation.** Customer IDs are hashed for privacy before evaluating prefix compression.

**Reasoning.** Hashing may preserve equality but destroys shared prefixes and lexical locality, so compressed key sizes and page fanout no longer represent production. Use an approved transformation that preserves prefix-length distribution, run on protected infrastructure, or bound the claim to hashed keys.

**Conclusion.** Privacy transformations require property-by-property validity review.

### Example 9

**Situation.** An engineer tunes 40 parameters on a fixed public benchmark and then reports that benchmark as test evidence.

**Reasoning.** Repeated selection overfits suite quirks even without explicit model training. Keep the public suite as regression/comparability evidence, but confirm on blinded or time-separated cases selected under the same target definition. Record tuning budget and parameter search.

**Conclusion.** Benchmark familiarity can leak outcomes just like train/test reuse.

### Example 10

**Situation.** A standard suite and a local trace rank algorithms oppositely.

**Reasoning.** Compare feature distributions, operation mix, state, scale, and metrics. The suite may target cross-system comparability while the trace targets one deployment. Neither ranking is universally true. Make the local decision using the declared local population; report the standard result separately for external calibration.

**Conclusion.** Conflicting rankings expose different estimands rather than requiring one data set to be dismissed.

## Cross-Program Connections

- [Software Testing and Quality Engineering STQE-001](../../13-software-engineering-testing-and-quality-engineering/modules/001-why-software-testing-cannot-prove-absence-of-defects.md) distinguishes evidence from confidence.
- [Data Engineering DE-001](../../19-data-engineering/modules/001-data-producers-consumers-and-lifecycle.md) governs provenance and transformations.
- [Data Architecture DARCH-001](../../20-data-architecture-engineering/modules/001-data-architecture-as-structure-flow-ownership-and-policy.md) connects workload schemas to durable data decisions.
- [Computer Architecture CA-040](../../23-computer-architecture/modules/040-analyzing-cache-misses-from-an-access-trace.md) shows how access traces connect inputs to hierarchy behavior.
- [Systems Engineering SYSENG-003](../../26-systems-engineering/modules/003-stakeholders-and-value.md) ties evaluation populations to stakeholder decisions.
- [Database Engineering DBE-001](../../18-database-engineering/modules/001-database-systems-workloads-and-guarantees.md) supplies mixed workload and guarantee context.

## References

1. Standard Performance Evaluation Corporation, *SPEC CPU 2017 Run and Reporting Rules*, revision dated 13 September 2021. [Official rules](https://www.spec.org/cpu2017/Docs/runrules.html). Checked 2026-09-05; rules are versioned and must be rechecked when reporting.
2. Transaction Processing Performance Council, *Current Benchmark Specifications and Fair Use Policies*. [Official specifications index](https://www.tpc.org/tpc_documents_current_versions/current_specifications5.asp). Checked 2026-09-05.
3. Scott Beamer, Krste Asanović, and David Patterson, “The GAP Benchmark Suite,” 2015. [arXiv:1508.03619](https://arxiv.org/abs/1508.03619). Checked 2026-09-05.
4. Peter Sanders, “Algorithm Engineering—An Attempt at a Definition Using Sorting as an Example,” *ALENEX 2010*, 55–61. [doi:10.1137/1.9781611972900.6](https://doi.org/10.1137/1.9781611972900.6). Checked 2026-09-05.
5. Raj Jain, *The Art of Computer Systems Performance Analysis*, Wiley, 1991. ISBN 978-0-471-50336-1.
6. Tomas Kalibera and Richard Jones, “Rigorous Benchmarking in Reasonable Time,” *ISMM 2013*, 63–74. [doi:10.1145/2464157.2464160](https://doi.org/10.1145/2464157.2464160). Checked 2026-09-05.
7. Todd Mytkowicz, Amer Diwan, Matthias Hauswirth, and Peter F. Sweeney, “Producing Wrong Data Without Doing Anything Obviously Wrong,” *ASPLOS 2009*, 265–276. [doi:10.1145/1508244.1508275](https://doi.org/10.1145/1508244.1508275). Checked 2026-09-05.
8. A. Andronidis and Cristian Cadar, “Benchmarking Crimes: An Emerging Threat in Systems Security,” 2018. [arXiv:1801.02381](https://arxiv.org/abs/1801.02381). Checked 2026-09-05.

## Exercises

### Exercise 1

Define target population, sampling frame, workload unit, stratum, and mixture weight for an evaluation of shortest-path algorithms used by a national routing service.

### Exercise 2

A population is 80% read-only, 15% mixed, and 5% write-heavy. A suite samples 20 cases from each, with mean latency 4, 12, and 40 ms. Compute the raw suite mean and target-weighted mean and explain the difference.

### Exercise 3

A generated sorting suite matches input sizes but algorithm rankings fail to reproduce on production data. Give a diagnostic plan for missing workload features and generator defects.

### Exercise 4

Compare a replayed production trace, a standard benchmark, and a factorial synthetic design for selecting between two concurrent graph engines.

### Exercise 5

Design a versioned workload manifest for evaluating an external index builder. Include population, identity, provenance, features, splits, weights, boundaries, adversarial cases, privacy, exclusions, oracles, and drift monitoring.

## Answers to the Exercises

### Answer 1

The target population could be all routing queries expected on the service’s supported road network during the next seasonal planning window. The frame might be retained, privacy-approved query sessions plus enumerated map regions; disclose missing regions, offline clients, and deleted sessions. A unit should preserve dependence, such as a route-query session or origin/destination/time scenario rather than an individual edge. Strata can combine distance, urban/rural region, traffic regime, and update state. Mixture weights come from projected query-session frequencies, while safety panels separately include closures, disconnected routes, and maximum-distance cases.

### Answer 2

The equal-count raw mean is $(4+12+40)/3=18.67$ ms. The target-weighted mean is $0.80(4)+0.15(12)+0.05(40)=7$ ms. Oversampling the write-heavy class improves its estimate but makes it one third of the raw suite rather than its 5% population share. Report all three means, sample counts, weights, and the 7 ms aggregate.

### Answer 3

Compare production and generated distributions for presorted runs, duplicate fraction, key/payload bytes, comparator cost, entropy/skew, value correlation, record representation, arrival order, cache state, and memory-spill frequency. Inspect joint rather than only marginal distributions. Validate feature extractors on audited cases. Add controlled generator parameters for missing mechanisms, preserve correlations, and rerun held-out production cases. Do not tune the generator directly to reproduce the desired winner; freeze a revised generator, version it, and confirm on a fresh time window.

### Answer 4

Trace replay preserves authentic operation order, graph states, skew, and bursts but inherits frame bias, privacy transformations, and historical drift. A standard suite improves external comparability and governed reporting but may not match local graphs or concurrency. A factorial synthetic design isolates interactions among degree skew, frontier density, graph size, update rate, and threads, yet does not estimate their prevalence. Use trace-weighted results for the local decision, standard results as separate calibration, and synthetic panels to explain mechanisms and boundaries. Require identical correctness oracles and execution controls across engines.

### Answer 5

Record the decision and target snapshot/update population, frame coverage, unit as a complete index-build snapshot, source and retrieval time, lawful content hash or stable identity, comparator/schema, bytes, entry/key distributions, duplicates, presortedness, compression, expected index size, and system-state scenario. Assign related variants to one tune/confirm/holdout split; record stratum, inclusion probability, target weight, and selection seed. Add below/at/above-memory boundaries, empty/singleton/all-equal/giant-key cases, corrupt or short-input failures, and declared timeout/resource policies. Preserve privacy/license transformations and their property impact. Bind sorted-permutation and query oracles, feature extractor/generator revisions, exclusions with predeclared reasons, and source drift summaries. Hash and version the manifest; any membership or rule change creates a new version and requires symmetric reruns.
