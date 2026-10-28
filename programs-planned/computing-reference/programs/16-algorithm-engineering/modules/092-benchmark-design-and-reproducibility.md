---
module_id: ALGE-092
program: Algorithm Engineering
level: 2
module_number: 92
title: Benchmark Design and Reproducibility
status: complete
last_verified: 2026-09-05
---

# Benchmark Design and Reproducibility

## One-Page Review

### Governing question

How do we turn an algorithmic comparison into a controlled, repeatable, auditable experiment whose observations support a declared claim and whose artifacts let another investigator understand or rerun it?

### Essential definitions

- A **benchmark protocol** fixes hypotheses, factors, workload, metrics, correctness oracles, execution rules, analysis, exclusions, and reporting before results are selected.
- An **experimental unit** is the smallest independently assigned unit; repeated timings of one process are not automatically independent units.
- A **factor** is a controlled or observed variable, such as implementation, input class, thread count, compiler, or cache state.
- A **treatment** is one chosen combination of factor levels.
- A **block** groups runs exposed to a shared nuisance condition so treatment comparisons can be made within that condition.
- **Warm-up** is explicitly untimed or separately analyzed execution used to reach a declared runtime or system state.
- **Repeatability** here means rerunning under the same stated setup; **independent reproduction** requires a different team to obtain the result and cannot be self-awarded.

### Central model, mechanism, or theorem

For matched block $b$, let $Y_{b,A}$ and $Y_{b,B}$ be a metric for treatments A and B. The within-block contrast

$$
D_b=Y_{b,A}-Y_{b,B}
$$

removes an additive block effect shared by both observations. Randomizing treatment order within each block protects the contrast from a systematic time trend. Replication estimates variation; it does not repair biased workload selection, an invalid oracle, an asymmetric build, or a changed protocol.

### Critical invariants

- A benchmark reports correct outputs before performance.
- Compared treatments receive the same declared workload, stopping rules, resource boundaries, and measurement semantics.
- Run identity binds source revision, build recipe, dependencies, workload version, configuration, environment, random seed, command, raw output, and disposition.
- Primary hypotheses, metrics, aggregation, exclusions, and multiplicity handling are frozen before confirmatory analysis.
- Run order is randomized or counterbalanced within meaningful blocks.
- Raw observations remain immutable; processing and figures are regenerated from them.
- Failed, timed-out, throttled, and censored runs are retained and reported under predeclared rules.
- Reproducibility language never implies review that did not occur.

### Common failures

Timing only one run; benchmarking debug against optimized code; changing input, compiler, and algorithm together; treating iterations inside one process as independent machines; discarding the first or slowest observations after seeing them; relying on clock precision rather than measured duration; reporting only a winner or percentage; using an arithmetic mean for ratios without justification; omitting correctness checks; mixing cold and warm states; letting thermal or background trends follow fixed treatment order; recording package names without versions; preserving summaries but not raw data; and calling an author rerun an independent reproduction.

### Compact example

Run A then B on each of ten machines and suppose every machine becomes slower during the second run. The fixed order biases B. Instead, define machine-session blocks and randomize A/B order within each. Record both raw measurements and $D_b$, inspect order effects, and report the distribution and uncertainty of paired contrasts. More repetitions on one machine would not substitute for deployment diversity if the claim concerns machines.

### Connections

[ALGE-091](./091-representative-workload-construction.md) defines which cases support the decision. ALGE-093 next separates profiling channels, ALGE-095 governs tuning, and ALGE-096 develops statistical comparison.

## Governing Question

For a declared algorithmic claim, what protocol, execution controls, raw evidence, analysis, and artifact boundary are sufficient to detect meaningful differences, expose important variation and failures, and permit an honest rerun?

## Why This Matters

A stopwatch invocation is not yet an experiment. Algorithm performance depends on inputs, state, compiler decisions, allocation, placement, runtime adaptation, contention, clocks, power policy, and measurement code. A comparison that hides these choices may be precise yet answer no stable question.

Benchmarking also changes the object being measured. Instrumentation adds work. Repeated execution warms caches and trains runtimes. Random order limits systematic drift but changes state trajectories. Isolation improves control but may reduce production realism. Good design states these choices and bounds the conclusion.

Reproducibility is an evidence property, not a container checkbox. A container can preserve user-space dependencies while leaving processor model, firmware, kernel, topology, power state, filesystem, storage, and external services unspecified. Conversely, a carefully disclosed native setup may support a valuable scoped rerun. Artifacts must bind claims to the conditions that produced them.

## Prerequisites and Retrieval

Retrieve empirical evidence and machine-model limits from [ALGE-009](./009-machine-models-and-hidden-constants.md) and [ALGE-010](./010-combining-proof-and-measurement-in-algorithm-evaluation.md), randomization from [ALGE-029](./029-randomization-as-a-design-tool.md), resource mapping from [ALGE-090](./090-mapping-an-algorithm-across-memory-threads-and-storage.md), and workload scope from [ALGE-091](./091-representative-workload-construction.md).

## Learning Objectives

After this module, you should be able to:

1. translate an algorithmic decision into hypotheses, estimands, factors, treatments, blocks, and experimental units;
2. design pilot, tuning, confirmatory, and regression stages without outcome leakage;
3. control correctness, builds, process state, clocks, caches, placement, interference, and run order;
4. distinguish iteration, process, session, machine, and workload replication;
5. define stopping, timeout, failure, exclusion, and rerun rules before outcomes;
6. retain raw observations and construct a provenance-complete experiment manifest;
7. analyze paired and blocked comparisons without hiding practical magnitude or variation; and
8. state repeatability and reproduction claims no more strongly than the evidence permits.

## Core Exposition

### Write the claim before the command

Start with a decision and an estimand: the quantity the experiment intends to estimate. “A is faster” omits workload, platform, metric, aggregation, state, and horizon. A useful claim is: on the frozen confirmation suite and declared host class, candidate A reduces median wall time per correct cold-start invocation relative to baseline B, without exceeding a memory limit.

State a smallest effect of practical interest. A 0.3% change may be statistically distinguishable after thousands of runs but irrelevant beside operational noise or migration cost. Predeclare primary and secondary outcomes. Exploratory measurements are valuable, but label them and confirm new hypotheses on fresh evidence.

### Identify units, factors, treatments, and nuisance variables

The experimental unit is assigned a treatment independently at the level relevant to inference. Iterations within one long process share allocator, runtime, address layout, cache, and thermal history. Processes on one boot share kernel and machine state. Machines share a platform class but differ physically. Treat nested observations as nested, not as thousands of independent replicas.

List controlled factors such as implementation, algorithm parameter, threads, input class, and cold/warm state. List nuisance variables: run order, machine, boot, time, core, temperature, background activity, address layout, and storage condition. Control, block, randomize, or measure each important nuisance variable. Unknown nuisance variables motivate randomization and independent replication.

### Separate stages

A pilot checks feasibility, instrumentation, duration, variance, and correctness. A tuning stage selects cutoffs, compiler options, and parameters. A confirmation stage tests frozen primary comparisons on cases not used to choose the winner. A regression stage guards established behavior over time. Reusing the same observations for all four exaggerates evidence.

Choose run counts using the desired precision or power for the estimand, informed by pilot variation—not by repeatedly checking significance and stopping when a preferred result appears. If sequential analysis is required, specify an appropriate sequential rule. A fixed count is simple; a precision rule may stop when a predeclared interval width is reached, subject to minimum and maximum counts.

### Establish correctness before performance

Every timed treatment must satisfy the same semantic contract. Check results with an independent oracle, trusted reference, invariant, certificate, or cross-validation appropriate to the problem. Ensure the compiler cannot remove unused work. Separate setup only when the claim truly excludes it; otherwise include parsing, allocation, transfer, preprocessing, and teardown.

Incorrect, approximate, probabilistic, and lossy treatments require explicit quality or error metrics. A faster wrong answer is not a performance win. If a probabilistic algorithm has a failure probability, record random seeds and correctness outcomes rather than rerunning failures silently.

### Freeze build and treatment symmetry

Bind source commit, uncommitted diff state, compiler/interpreter and dependencies, optimization and target flags, link mode, generated code, and build log. Clean rebuilds reduce accidental state carryover. Inspect binaries or command lines when critical options must be verified.

Symmetry does not always mean identical flags: algorithms may need their natural supported configuration. It means that deviations are declared, justified by the estimand, and not selectively granted after results. Compare production-quality with production-quality, and disclose algorithm-specific tuning.

### Design blocks and run order

Blocks make nearby comparisons under shared nuisance conditions. A block might be one machine-session containing every treatment for one workload. Randomize order inside each block. With expensive state reset, use counterbalanced sequences or randomized blocks rather than running all A then all B.

Randomization is not a cure for interference. If A warms data used by B, reset state, isolate separate sessions, or model the carryover and randomize complete sequences. Record actual order, not merely the intended seed. Interrupted blocks remain identifiable.

### Construct a deterministic schedule

The reference below creates three complete randomized blocks and summarizes frozen observations. It demonstrates balanced scheduling and paired cell summaries; it is not a timing harness and does not simulate environmental noise.

<!-- bijux-verify: {"id":"blocked-benchmark-schedule","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"schedule: [(1, 'small', 'candidate'), (1, 'large', 'candidate'), (1, 'large', 'baseline'), (1, 'small', 'baseline'), (2, 'large', 'candidate'), (2, 'small', 'baseline'), (2, 'large', 'baseline'), (2, 'small', 'candidate'), (3, 'small', 'baseline'), (3, 'small', 'candidate'), (3, 'large', 'candidate'), (3, 'large', 'baseline')]\nmedians: [(('large', 'baseline'), 42.0), (('large', 'candidate'), 36.0), (('small', 'baseline'), 10.1), (('small', 'candidate'), 8.1)]\nreductions: [('large', 14.3), ('small', 19.8)]\n","stderr":""}} -->
```python
from random import Random
from statistics import median


rng = Random(20260905)
schedule = []
for block in range(1, 4):
    cells = [
        (case, system)
        for case in ["large", "small"]
        for system in ["baseline", "candidate"]
    ]
    rng.shuffle(cells)
    schedule.extend((block, case, system) for case, system in cells)

observations = {
    ("small", "baseline"): [10.2, 10.0, 10.1],
    ("small", "candidate"): [8.0, 8.2, 8.1],
    ("large", "baseline"): [42.0, 41.5, 42.5],
    ("large", "candidate"): [36.0, 35.8, 36.2],
}
medians = [(cell, median(values)) for cell, values in sorted(observations.items())]
reductions = []
for case in ["large", "small"]:
    base = median(observations[(case, "baseline")])
    candidate = median(observations[(case, "candidate")])
    reductions.append((case, round(100 * (base - candidate) / base, 1)))

print("schedule:", schedule)
print("medians:", medians)
print("reductions:", reductions)
```

The seed makes the schedule auditable, not random in a metaphysical sense. A real harness must persist per-run identity and actual state, execute the oracle, capture clocks and errors, and survive interruption without inventing observations.

### Define state and warm-up

Cold and warm are protocols, not adjectives. Define which caches, pools, runtime tiers, files, indexes, and connections are reset or retained. A filesystem cache is not flushed merely because a process restarts. A managed runtime may compile or optimize during early iterations. Measure and visualize state evolution in pilots.

Warm-up ends by a predeclared count, state criterion, or domain-specific event. Discarded warm-up is part of cost even if excluded from steady-state latency. If production processes are short-lived, steady-state-only results can mislead. Report both when both matter.

### Select clocks and measurement boundaries

Use a monotonic clock for elapsed duration. Ensure the measured region is long enough relative to timer overhead and resolution, but do not infer accuracy from resolution. Batch tiny operations while subtracting or separately measuring harness overhead, and prevent batching from changing the algorithmic state.

Wall time measures completion experienced by the caller; CPU time measures scheduled execution; throughput measures completed work per interval. They answer different questions. Record unit, scope, start/stop boundary, concurrency, and whether setup is included. Later profiling may explain results but should not silently replace the primary measurement.

### Control the environment without erasing the target

Record hardware model, processors, memory, storage, topology, firmware where accessible, operating system and kernel, power policy, frequency behavior, placement, affinity, NUMA binding, container/virtualization limits, and background activity. Capture temperature and throttling indicators when material.

Isolation reduces uncontrolled noise but changes co-tenancy. If production includes contention, use a controlled load factor or a separate production-realism panel. Do not let one treatment run alone and another under load. Environment control supports comparison within its scope; it does not establish portability.

### Treat repetition as a hierarchy

Inner iterations characterize within-process variability. Process repetitions include startup and address-layout changes. Session or boot repetitions include more system state. Machine repetitions support claims across physical instances. Workload repetitions support population variation. State which levels are sampled and which remain fixed.

Summaries should respect hierarchy and pairing. Do not feed every inner loop timing into a test that assumes independence. Aggregate or model at the assignment unit, preserve block identifiers, and report variation at relevant levels. More inner iterations cannot estimate between-machine variation.

### Predeclare failures, timeouts, exclusions, and reruns

Specify correctness failure, crash, timeout, out-of-memory, throttling, interrupted run, and harness failure handling. Timeouts are censored or failed outcomes, not blank cells. Rerun only under a symmetric predeclared rule, retaining both the original disposition and rerun link.

Outlier deletion based on performance magnitude is especially dangerous. Investigate with operational evidence—machine fault, unrelated daemon, corrupted input—then apply the declared rule to all treatments. Report sensitivity with and without justified exclusions. Never overwrite raw measurements.

### Analyze magnitude, uncertainty, and multiplicity

Report raw or sufficiently granular data, sample sizes, center, spread, effect size in natural units, relative effect where meaningful, and uncertainty appropriate to the design. A p-value alone neither measures importance nor proves equality. A non-significant result may be imprecise; an extremely precise tiny difference may be unimportant.

Use paired contrasts for paired designs. Inspect distributions and time/order plots. Ratios are asymmetric: A being twice B does not make B “minus 100%” A. Declare the denominator and aggregation. If many algorithms, workloads, metrics, and parameters are searched, separate primary comparisons or control multiplicity; do not select the smallest p-value after the fact.

### Build the artifact as an evidence graph

Give every run a stable ID linked to protocol version, source/build identity, treatment, workload, block/order, seed, host/session, command, timestamps, raw stdout/stderr, oracle result, metric record, and disposition. Hash immutable inputs and raw outputs where appropriate. Store analysis code and regenerate tables from raw data.

Include a README with exact commands, expected duration and resources, dependency acquisition, licenses, platform limitations, and a minimal smoke test. Containers and lockfiles help but do not replace environment disclosure. Archive durable snapshots when permissions allow; external URLs and mutable images can disappear.

### Use external rules as governance examples

SPEC CPU 2017 run rules treat results as observations whose conditions must be disclosed and prescribe repeated runs and output validation for that suite [1]. ACM artifact guidance distinguishes artifact qualities and independently obtained results [7]. These are useful governance patterns, not universal protocols and not evidence that an unevaluated artifact earned a badge.

Benchmark rules evolve. Record the exact revision used and recheck official policy when publishing or comparing governed results. A local benchmark may borrow disclosure discipline without calling itself SPEC-compliant or ACM-evaluated.

## Definitions and Notation

Let $Y_{b,t}$ be the observed metric in block $b$ under treatment $t$. For two treatments, $D_b=Y_{b,A}-Y_{b,B}$ is a paired contrast. Let $\Delta$ be the target effect, $\delta$ the smallest practically important magnitude, $n$ the number of independent assignment units, and $r$ inner repetitions within a unit.

A **protocol deviation** is any departure from the frozen plan. **Censoring** reveals a bound rather than an exact observation. **Carryover** occurs when an earlier treatment changes a later treatment. **Provenance** is the identity and derivation chain connecting a claim to code, data, environment, execution, and analysis.

## Mechanisms, Invariants, or Proof Structure

### Blocking argument

Suppose $Y_{b,t}=\mu_t+\beta_b+\epsilon_{b,t}$, where $\beta_b$ is an additive block effect. Then $D_b=Y_{b,A}-Y_{b,B}=\mu_A-\mu_B+\epsilon_{b,A}-\epsilon_{b,B}$; the shared $\beta_b$ cancels. This premise fails when treatment order creates unequal carryover or when the block effect interacts with treatment, so order and interaction diagnostics remain necessary.

### Random-order integrity

Generate the schedule from a recorded seed after freezing the cell set, persist the schedule, and log actual execution order. Each complete block contains every required treatment exactly once per designed cell. An interrupted run cannot be replaced silently; its disposition and any new randomized block remain visible.

### Evidence-chain integrity

The final claim must be regenerable from immutable raw observations through versioned analysis. A digest or stable identifier binds every edge. Manual spreadsheet edits, copied summary values, or overwritten reruns break the chain even when the final number looks plausible.

## Alternatives and Trade-Offs

| Choice | Strength | Risk | Appropriate use |
|---|---|---|---|
| isolated host | strong control | weak co-tenancy realism | mechanism comparison |
| controlled load | chosen realism | more variance and complexity | deployment scenario |
| fixed order | operationally simple | confounds drift with treatment | only with proven reset/no trend |
| randomized blocks | balances trends probabilistically | needs persistent scheduling | most A/B comparisons |
| many inner iterations | cheap precision within process | pseudo-replication | timer/harness characterization |
| many processes/machines | broader variation | cost | startup or platform claims |
| fixed run count | simple audit | may be over/under precise | stable pilot-informed designs |
| sequential precision rule | adaptive cost | invalid if improvised | predeclared sequential design |
| native environment | deployment fidelity | dependency drift | local production decision |
| container/VM | dependency capture | incomplete hardware/kernel capture | portable artifact layer |

No single design maximizes control, realism, cost, and generalization. Use separate panels when combining them would blur the estimand.

## Failure Modes and Misconceptions

- **“A precise timer makes an accurate benchmark.”** Boundary validity and environment matter more than timestamp digits.
- **“One thousand loop iterations means $n=1000$.”** Shared state can make the independent unit one process or session.
- **“Randomization removes all bias.”** It does not repair invalid workloads, carryover, asymmetric builds, or broken oracles.
- **“Warm means run once first.”** Warm state must identify what reached which condition.
- **“Drop outliers to reduce noise.”** Outcome-based deletion can remove real tails or treatment failures.
- **“Containers make results reproducible.”** They capture only part of the environment and artifact chain.
- **“Same mean means equivalent.”** Equivalence needs a declared tolerance and suitable evidence.
- **“Significant means important.”** Practical magnitude and uncertainty still govern the decision.
- **“No significant difference means equal.”** Low power or high variation can hide material differences.
- **“We reproduced our own run.”** Self-reruns support repeatability; independent review requires another team and recorded evidence.

## Worked Examples

### Example 1

**Situation.** A compares A then B in that order for twenty blocks while host temperature rises.

**Reasoning.** Treatment and time are confounded, so B inherits later, hotter conditions. Randomize order within each block or counterbalance AB and BA; record temperature and actual order. Analyze paired contrasts and test whether order changes the effect.

**Conclusion.** Replication cannot repair fixed-order confounding.

### Example 2

**Situation.** A microbenchmark reports 50,000 timings from one process as 50,000 independent samples.

**Reasoning.** Iterations share runtime, caches, allocation arenas, address layout, and machine session. The treatment was assigned once. Use inner timings to characterize that process, repeat independent processes or sessions, and analyze the hierarchy.

**Conclusion.** Observation count and independent sample size are different.

### Example 3

**Situation.** Candidate completes in 8.1 ms versus baseline 10.1 ms on small cases.

**Reasoning.** The absolute change is 2.0 ms. Relative to baseline, reduction is $100(10.1-8.1)/10.1=19.8\%$. Report both and their uncertainty; do not reverse the denominator casually. Confirm identical outputs and measurement boundaries.

**Conclusion.** Effect reporting must name units, denominator, and correctness.

### Example 4

**Situation.** The first five managed-runtime iterations are slower, so the engineer deletes them after plotting.

**Reasoning.** The rule was outcome-driven. Decide whether the estimand is cold start, steady state, or lifecycle cost. In a new confirmation run, use a frozen warm-up count or state detector validated during the pilot and retain warm-up records separately.

**Conclusion.** Pilot discovery informs a new protocol; it does not retroactively sanitize confirmation data.

### Example 5

**Situation.** A 60-second timeout affects seven candidate runs and no baseline runs.

**Reasoning.** Averaging completed candidate runs selects survivors. Apply the predeclared timeout rule, report seven censored/failure outcomes, and use failure-aware or censored analysis. A rerun is allowed only under the symmetric harness-failure rule and remains linked.

**Conclusion.** Timeout disposition belongs in the primary evidence.

### Example 6

**Situation.** A container image pins libraries, but reruns differ across processors.

**Reasoning.** The image did not fix processor microarchitecture, topology, kernel, firmware, power policy, or storage. Record those layers and bound the claim to compatible environments. If portability is central, sample machines and report between-machine variation.

**Conclusion.** Packaging improves artifact capture without eliminating platform dependence.

### Example 7

**Situation.** Ten configurations and twelve metrics are searched; only the best p-value is reported.

**Reasoning.** There are 120 opportunities for an apparently favorable result. Predeclare a primary configuration and metric or apply a suitable multiplicity strategy. Label the search exploratory and confirm the selected design on untouched observations.

**Conclusion.** Researcher choice is part of the experiment and must be governed.

### Example 8

**Situation.** Candidate excludes preprocessing but baseline timing includes it.

**Reasoning.** The treatments use different boundaries. Either time both end to end or report preprocessing and query phases separately under identical semantics. If candidate’s preprocessing is reusable, state the reuse count needed to amortize it.

**Conclusion.** Symmetric boundaries precede speed claims.

### Example 9

**Situation.** A benchmark run is interrupted by an unrelated backup.

**Reasoning.** Preserve the run as interrupted with host evidence. If the protocol permits rerun on infrastructure failure, allocate a new run ID and block, retain the link, and apply the same rule regardless of treatment. Never overwrite the raw record.

**Conclusion.** Auditable reruns preserve rather than erase deviations.

### Example 10

**Situation.** Another team uses the archived source and workload but obtains the same ranking at uniformly slower times.

**Reasoning.** Compare environment and protocol, then assess the claim: an absolute-latency claim failed, while a scoped ranking may have reproduced. Preserve both results and explain platform differences. Only the independent team or governed review can support an independent reproduction claim.

**Conclusion.** Reproduction is claim-specific, not byte-for-byte numerical identity.

## Cross-Program Connections

- [Software Testing and Quality Engineering STQE-002](../../13-software-engineering-testing-and-quality-engineering/modules/002-specifications-expectations-and-test-oracles.md) connects result validity to independent oracles.
- [Concurrent and Parallel Programming CONPAR-092](../../04-programming-languages-concurrent-and-parallel-programming/modules/092-roofline-and-operational-intensity-analysis.md) supplies a resource model whose parameters require careful measurement.
- [Computer Architecture CA-040](../../23-computer-architecture/modules/040-analyzing-cache-misses-from-an-access-trace.md) shows how trace evidence explains hierarchy behavior.
- [Data Structures Engineering DSE-010](../../17-data-structures-engineering/modules/010-benchmarking-a-structure-without-misleading-results.md) applies benchmark discipline to representation choices.
- [Large-Scale Data Systems Engineering LSDS-097](../../21-large-scale-data-systems-engineering/modules/097-cluster-benchmarking.md) extends experimental design to clustered systems.
- [Systems Engineering SYSENG-072](../../26-systems-engineering/modules/072-verification-planning.md) places empirical verification inside a broader assurance argument.

## References

1. Standard Performance Evaluation Corporation, *SPEC CPU 2017 Run and Reporting Rules*, revision dated 13 September 2021. [Official rules](https://www.spec.org/cpu2017/Docs/runrules.html). Checked 2026-09-05; the applicable posted revision must be checked at testing time.
2. Tomas Kalibera and Richard Jones, “Rigorous Benchmarking in Reasonable Time,” *ISMM 2013*, 63–74. [doi:10.1145/2464157.2464160](https://doi.org/10.1145/2464157.2464160). Checked 2026-09-05.
3. Andy Georges, Dries Buytaert, and Lieven Eeckhout, “Statistically Rigorous Java Performance Evaluation,” *OOPSLA 2007*, 57–76. [doi:10.1145/1297027.1297033](https://doi.org/10.1145/1297027.1297033). Checked 2026-09-05.
4. Todd Mytkowicz, Amer Diwan, Matthias Hauswirth, and Peter F. Sweeney, “Producing Wrong Data Without Doing Anything Obviously Wrong,” *ASPLOS 2009*, 265–276. [doi:10.1145/1508244.1508275](https://doi.org/10.1145/1508244.1508275). Checked 2026-09-05.
5. Charlie Curtsinger and Emery D. Berger, “Stabilizer: Statistically Sound Performance Evaluation,” *ASPLOS 2013*, 219–228. [doi:10.1145/2451116.2451141](https://doi.org/10.1145/2451116.2451141). Checked 2026-09-05.
6. Jan Vitek and Tomas Kalibera, “Repeatability, Reproducibility, and Rigor in Systems Research,” *EMSOFT 2011*, 33–38. [doi:10.1145/2038642.2038650](https://doi.org/10.1145/2038642.2038650). Checked 2026-09-05.
7. Association for Computing Machinery, *Artifact Review and Badging*. [Official policy](https://www.acm.org/publications/policies/artifact-review-and-badging-current). Checked 2026-09-05; badge claims require the applicable independent evaluation.
8. Raj Jain, *The Art of Computer Systems Performance Analysis*, Wiley, 1991. ISBN 978-0-471-50336-1.

## Exercises

### Exercise 1

Define the estimand, experimental unit, treatment, factor, block, nuisance variable, and smallest practical effect for comparing two shortest-path implementations on routing workloads.

### Exercise 2

Measurements in four matched sessions are A/B = 20/24, 30/33, 18/22, and 40/41 ms. Compute $D_b=A-B$, its mean, and the mean unpaired difference. Explain what pairing retains.

### Exercise 3

A harness runs 100 iterations in one process, deletes the first ten, reruns crashes, and preserves only the median. Diagnose the evidence failures and propose a repair.

### Exercise 4

Compare isolated native execution, a pinned container, and controlled co-tenant load for a benchmark intended to choose a production algorithm.

### Exercise 5

Design a reproducible confirmation protocol for two external-memory sorting implementations. Include correctness, workload, factors, units, blocks, order, state, clocks, resource boundaries, repetitions, failures, analysis, provenance, and limitations.

## Answers to the Exercises

### Answer 1

The estimand could be the distribution of per-query wall-time difference B minus A for correct answers on next quarter’s declared routing-session population and supported host class. The unit is an independently selected route-query session executed in a reset machine-session; implementation is the treatment, while graph family, query distance, cache state, and thread count are factors. A machine-session block runs both implementations on the same workload/state with randomized order. Temperature, background load, core placement, and time are nuisance variables to control, block, randomize, or record. A defensible smallest effect might be 2 ms at p95 or 10% fewer missed latency objectives, justified by the service budget—not by pilot significance.

### Answer 2

The contrasts are $-4,-3,-4,-1$ ms, with mean $(-12)/4=-3$ ms, so A is 3 ms faster on average within sessions. The unpaired means are $27$ ms for A and $30$ ms for B, also a $-3$ ms difference here. Pairing retains which observations shared session conditions; even though the point estimates happen to agree, paired contrasts can remove additive session effects and expose heterogeneous differences. Inference should use four assignment units, not eight independent timings.

### Answer 3

The 100 iterations share process state, the warm-up deletion was not justified by a frozen estimand, crashes vanished through selective reruns, and raw evidence cannot be audited. During a pilot, inspect state evolution and decide whether cold, steady, or lifecycle cost matters. Freeze warm-up and stopping rules for a new confirmation run. Repeat independent processes/sessions, retain every iteration with hierarchy IDs, record crashes/timeouts, issue new linked IDs for only predeclared infrastructure reruns, run correctness oracles, and regenerate summaries from immutable raw records.

### Answer 4

Isolated native execution best exposes algorithm mechanisms on the actual host but may understate production contention and dependency drift. A pinned container captures much user-space state and improves transportability but does not fix host kernel, processor, power, topology, or storage. Controlled co-tenancy estimates a declared load scenario but increases variance and requires identical load generation for treatments. Use isolated native runs for primary mechanism comparison, a pinned artifact layer for rerunability, and a separate controlled-load panel when the production decision depends on contention; do not merge their estimands into one unexplained score.

### Answer 5

Freeze a representative confirmation manifest with immutable files, hashes, size/entropy/run/duplicate features, memory-spill boundaries, and a separate stress panel. Require sorted-permutation equivalence and stable-order checks where promised. Treatments bind source revisions, clean builds, compiler/linker versions and flags, storage layout, memory limit, and thread count. Use complete file-sort invocations as units; block both treatments within machine-session and file, randomize order, and reset or explicitly preserve page cache and storage state. Measure monotonic end-to-end wall time plus separately defined CPU, bytes, and peak memory; record setup boundaries. Pilot only to choose duration and fixed repetitions, then use multiple processes, sessions, and target machines. Predeclare timeout, ENOSPC, crash, checksum failure, thermal-throttling, interruption, exclusion, and linked-rerun rules. Report paired effects by stratum, practical magnitude, uncertainty, failures, and sensitivity without deleting raw observations. Bind every run to protocol, workload, source/build, host/kernel/storage, state, order/seed, command, stdout/stderr, oracle, metrics, and disposition; regenerate tables with versioned code. Limit conclusions to declared workloads, host/storage class, configurations, and observation period, and claim no independent reproduction until another team documents it.
