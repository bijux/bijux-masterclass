---
module_id: CA-030
program: Computer Architecture
level: 1
module_number: 30
title: Measuring Pipeline Throughput and Latency
status: complete
last_verified: 2026-09-04
---

# Measuring Pipeline Throughput and Latency

## One-Page Review

### Governing question

How can pipeline throughput and latency be measured so the numerator, denominator, boundaries, counters, workload, clock behavior and uncertainty describe the same experiment—and improvements reflect useful retired work rather than frequency, speculative activity or counter artifacts?

### Essential definitions

- **latency** is elapsed time from a declared start event to its matching completion event.
- **throughput** is completed useful work divided by elapsed observation time.
- **instruction latency** is time for one instruction/token from a named pipeline boundary to another.
- **pipeline throughput** is the sustained completion/retirement rate under a declared workload and interval.
- **cycles per instruction** (`CPI`) is counted cycles divided by counted retired instructions.
- **instructions per cycle** (`IPC`) is retired instructions divided by cycles; for identical nonzero counts it is `1/CPI`.
- **clock frequency** converts cycles to time only when the relevant cycle duration/frequency behavior is known.
- **fill time** precedes first completion in an initially empty pipeline; **drain time** follows final admission.
- **steady state** is an interval where start/stop transients are excluded by an explicit rule.
- A **retired instruction** is an architectural completion, unlike fetched, issued or executed speculative work.
- A **hardware performance counter** counts architecture/implementation-defined events under enable, privilege and overflow rules.
- **multiplexing** time-shares limited physical counters among requested events and may require scaling.
- **measurement overhead** is work or perturbation introduced by instrumentation and collection.
- **warm-up** establishes cache, predictor, translation, runtime and frequency state before measured work.
- A **tail percentile** reports a latency distribution quantile; it is not derivable from the mean alone.

### Central model, mechanism, or theorem

For one aligned interval, let retired work delta be `Delta I`, cycle delta `Delta C`, and elapsed wall time `Delta t`. Then `CPI=Delta C/Delta I`, `IPC=Delta I/Delta C`, and throughput `X=Delta I/Delta t`. If a stable effective frequency `f_eff=Delta C/Delta t` applies, `X=IPC*f_eff`. For an ideal depth-`k` scalar pipeline processing `N` tokens from empty with `S` nonoverlapped stall cycles, cycles are `N+k-1+S`; this finite-run result approaches steady CPI only as `N` dominates transients. Every conclusion is conditional on event semantics, synchronized boundaries and workload/environment identity.

### Critical invariants

- Numerator and denominator cover the same threads, CPUs, privilege modes and time interval.
- Work counts architectural completions appropriate to the claim, not fetched/wrong-path activity.
- Counter deltas handle width, wrap, reset, migration, enable/inhibit and overflow.
- CPI and IPC are computed from identical nonzero counts and cross-check as reciprocals.
- Cycle-to-time conversion uses measured elapsed time or valid effective frequency, not an advertised maximum.
- Fill, drain, warm-up and steady-state boundaries are stated rather than mixed silently.
- Latency samples match each start with its own completion and include censoring/timeouts explicitly.
- Multiplexed events report time-enabled/time-running and scaling limitations.
- Repetitions preserve raw samples and environment metadata; summaries include dispersion/tails.
- Performance claims remain within tested configurations, workloads and statistical uncertainty.

### Common failures

Common failures include calling frequency throughput, using fetched instructions as work, dividing counters from different intervals, ignoring wrap, assuming `cycle` counts only core-active cycles, treating every event name as portable, scaling heavily multiplexed rare events, timing a short region dominated by measurement overhead, discarding warm-up without a rule, averaging percentiles, reporting only the fastest run, hiding timeouts, comparing different binaries/inputs, inferring per-instruction latency from CPI, and claiming a causal bottleneck from one correlated counter.

### Compact example

A measurement retires 5,000,000 instructions in 6,250,000 cycles and 2.500 ms: CPI 1.250, IPC 0.800 and 2,000.00 MIPS. A 32-bit counter moving from 4,294,967,200 to 400 has modular delta 496, not a negative value. An invented depth-seven pipeline processes 100 tokens with 20 stalls in 126 cycles at 0.40 ns: first ideal latency 2.80 ns, total 50.40 ns and finite throughput 1,984.13 MIPS. Eight latency samples have mean 119.62 ns, median 101.50 ns and nearest-rank p95 250 ns, revealing a tail hidden by the median.

### Connections

Pipeline measurement connects counter architecture, operating-system scheduling, statistics, benchmarking, caches/branch prediction, power/thermal management, compiler binaries, observability and reproducible performance engineering.

## Governing Question

Pipeline diagrams predict relationships under assumptions. Measurement tests an implemented system, where frequency changes, cache misses, interrupts, counter semantics and software boundaries affect observations.

The central discipline is alignment: what work completed, over which interval, on which hardware/software state, using which event definition? Arithmetic cannot rescue mismatched counters.

## Why This Matters

Two designs can trade CPI against clock period. One can retire more per cycle yet less per second. A deeper pipeline can improve steady throughput while increasing first-result latency and finite-batch overhead.

Hardware counters expose useful events but are not universal truths. Availability, privilege filtering, speculative counting and model-specific encodings vary. Counter collection itself can perturb execution.

Reliable decisions require distributions and replication. Tail latency, thermal drift or rare stalls can matter more than a small mean improvement.

## Prerequisites and Retrieval

Before studying this module, be able to:

- compute pipeline fill/drain, CPI, IPC and clock period;
- distinguish retirement from fetch/execute;
- identify stalls, flushes and overlapping causes;
- interpret basic descriptive statistics and percentiles;
- use monotonic timing and counter deltas.

Retrieve exact processor model/stepping/topology/microcode; ISA counter specification and implemented event guide; counter width, inhibit/filter/overflow, speculative and privilege semantics; PMU capacity and multiplex scaling; OS/kernel/perf/tool versions and permissions; clock source/frequency/governor/turbo/idle/thermal/power limits; affinity/isolation/SMT/NUMA; interrupts and background load; compiler/linker/runtime and flags; binary/build ID; input/trace/seed; caches/TLB/predictor preconditioning; benchmark start/stop/warm-up/repetition rules; raw counter/time/latency records; failures/timeouts/censoring; statistical method and predeclared thresholds; energy/power data; hardware errata; and exact commands/configuration timestamps.

## Learning Objectives

After completing this module, you should be able to:

1. define throughput and latency with explicit work and event boundaries;
2. compute and cross-check CPI, IPC, effective frequency and instruction time;
3. model finite pipeline fill, drain and stall effects;
4. collect safe counter deltas including width and wrap;
5. distinguish architectural, model-specific, speculative and multiplexed events;
6. design warm-up, steady-state and repetition protocols;
7. summarize latency with distributions, percentiles and uncertainty;
8. avoid double-counting overlapping stall causes;
9. separate correlation, attribution and causal experiments;
10. produce reproducible evidence scoped to exact systems and workloads.

## Core Exposition

### State the decision and claim

Begin with a decision such as choosing a pipeline configuration for a service-level objective. Define acceptable throughput, median/tail latency, energy and correctness constraints before collecting data.

A vague goal like “measure performance” encourages selective metrics. A claim should name workload, hardware/configuration and uncertainty.

### Define useful work

For instruction throughput, retired instructions are usually the numerator. For application value, operations, requests, records or transactions may be more meaningful.

Instructions per operation can change across compilers or algorithms. Report both layers when comparing systems rather than assuming instruction count is constant value.

### Define interval boundaries

Choose start/stop events from the same clock domain or account for synchronization. Record counters immediately around the same work region, with serialization/barriers required by the platform/tool.

If one count includes setup while elapsed time excludes it, derived rates are invalid. Threads migrating across CPUs can split or contaminate counter scope.

### Distinguish latency boundaries

Instruction latency might mean decode-to-result, issue-to-completion or acceptance-to-retirement. Request latency might be client send-to-response or server receive-to-completion.

Name both endpoints and clock. Per-token identity must match starts and completions; FIFO matching is valid only if completion order is guaranteed.

### Distinguish throughput from frequency

Frequency is cycles per second. Throughput also depends on useful completions per cycle. `X=IPC*f_eff` only when counts refer to the same interval/scope.

Advertised or nominal frequency ignores turbo, throttling, idle and virtualization. Prefer elapsed-time throughput and use cycle counts as explanation.

### Compute CPI and IPC consistently

From identical deltas, CPI and IPC are reciprocals. A mismatch reveals rounding, scope or event problems. Avoid division for zero retired work.

Aggregate by summing raw cycles/instructions before division when a global weighted result is intended. Averaging per-run CPI weights runs equally, not instructions.

### Model finite pipelines

An ideal depth-`k` scalar pipeline takes `N+k-1` cycles from empty for `N` tokens. Add nonoverlapped stalls and recovery cycles under a declared counting model.

For short batches, fill/drain materially reduce throughput. Steady IPC approaches capacity only for long work with stable resources.

### Measure instruction latency separately

CPI is an average throughput ratio, not one instruction's latency. A five-stage pipeline can approach CPI one while each instruction spans five cycles.

Latency for variable operations needs per-event timestamps or trace reconstruction, including queueing, stalls and completion/retirement differences.

### Understand counter semantics

Architectural counters such as cycle/time/instret have specified behavior and optional access controls; platform implementations can constrain them. Model-specific PMU events require exact event documentation.

Ask whether an event counts speculative, executed or retired work, which privilege modes, and whether idle/stall cycles count. Similar names across processors may differ.

### Compute deltas safely

For a `w`-bit monotonically wrapping counter with at most one unobserved wrap, `Delta=(end-start) mod 2^w`. Multiple wraps require a shorter interval or overflow tracking.

Detect reset, hotplug, migration or reprogramming; modular arithmetic cannot distinguish them from legitimate wrap without metadata.

### Handle overflow

Sampling PMUs may interrupt on overflow and reload counters. Lost samples, skid and throttling affect interpretation. Counting mode still has finite width.

Record tool/kernel lost-event and throttle indicators. Do not silently treat missing samples as zero activity.

### Handle multiplexing

If requested events exceed physical counters, tools time-share them. Scaling estimates full-interval counts from time running, assuming sampled intervals are representative.

Phase changes and rare bursts violate that assumption. Reduce event groups, run repeated matched passes or use traces; never combine incompatible passes without stability evidence.

### Validate event counts

Use microbenchmarks with known instruction classes and expected bounds. Check retired instruction/cycle counts against disassembly and controlled loops, accounting for setup, interrupts and runtime.

Validate counter response to enabling/disabling a feature. A plausible magnitude is not proof that the event means what its label suggests.

### Measure wall and CPU time deliberately

Wall time includes scheduling and waits; CPU time counts execution scheduled to the process under OS rules. Service latency generally needs wall time.

Monotonic clocks avoid civil-time adjustments. Clock-read overhead and resolution matter for short regions; batch repetitions and subtract only validated overhead.

### Warm up controlled state

Decide whether the target is cold start, warm steady state or both. Warm-up can populate caches/TLB/predictors, trigger JIT optimization, allocate memory and reach thermal/frequency equilibrium.

Use an objective stopping rule or fixed protocol chosen before outcomes. Do not discard slow early runs simply because they are inconvenient.

### Control the environment

Pin threads/interrupts as appropriate, record SMT/NUMA placement, background services, memory placement, governor/turbo, power/thermal limits and ambient conditions. Isolation changes realism, so state it.

Randomize comparison order or interleave variants to reduce temporal drift. Rebooting changes cold state and is not automatically greater control.

### Preserve binary and input identity

Record source commit/dirty state, compiler/runtime/linker and flags, build ID/hash, libraries, input digest, seed and command. Inspect generated code when instruction-level claims depend on it.

An optimization that changes work semantics or input is not a pipeline speedup. Correctness validation precedes performance comparison.

### Repeat independently

Within-process iterations reveal short-term variance but share state. Independent process/machine/time repetitions expose initialization and environmental variance.

Report raw samples and grouping. Avoid pseudoreplication that calls millions of loop iterations independent system experiments.

### Summarize latency distributions

Report count, failures/timeouts, min/max, median and relevant tail percentiles with a stated quantile convention. Means reveal total cost but are sensitive to outliers.

Do not average percentiles across shards/runs to get a global percentile. Merge raw samples or mergeable histograms with consistent buckets/ranges.

### Quantify uncertainty

Confidence intervals describe sampling uncertainty under assumptions; they do not cover systematic bias, wrong events or workload mismatch. Use paired analysis when variants share controlled conditions.

Effect size and decision threshold matter more than p-value alone. Predeclare a practically meaningful margin and regression constraints.

### Treat outliers and censoring honestly

Investigate outliers using trace/environment evidence. Keep them unless an exclusion rule defined independently applies, and report both exclusion and sensitivity.

Timeouts are right-censored or failed observations, not missing fast samples. Report their count/rate and use suitable survival/tail analysis when material.

### Attribute stalls without double counting

Data, structural, control and memory causes can coexist. Counter definitions may be event counts, cycles with condition, or lost slots.

Use exclusive priority attribution or simultaneous cause bitsets and compute set union. Summing nonexclusive counts can exceed elapsed cycles.

### Infer causality with interventions

A high miss counter correlates with a slow run but may not be causal. Change cache size, access pattern, prediction mode or hazard policy while holding other factors controlled.

Use multiple metrics and traces to test a mechanism. Avoid causal language when evidence is observational only.

### Compare configurations fairly

Keep correctness, workload, compiler and service constraints constant. Configuration can change frequency, cache capacity, instruction count or thermal behavior; record all.

Normalize rates only where the denominator represents equal useful work. Speedup is baseline time/candidate time for the same task.

### Measure energy and power

Throughput gains can raise power; shorter time can still reduce energy. Align energy counters/sensors with the same interval and record sampling/calibration/background subtraction policy.

Report energy per useful operation/instruction and thermal state. Package sensors include components beyond the pipeline and need scoped interpretation.

### Use traces for sequence questions

Aggregate counters cannot reveal which instruction caused which stall or whether events overlap. Pipeline/commit traces preserve temporal ordering at greater volume/perturbation.

Validate trace loss and clock alignment. Sampling reconstructs distributions probabilistically, not exact complete sequences.

### Cross-check accounting identities

Check elapsed time against cycles/effective frequency, CPI against IPC, retired instructions against known work, and categorized stall union against total lost opportunities.

Accounting mismatch is diagnostic evidence. Do not force residuals into a convenient category without explaining unknown/unmodeled time.

### Package reproducibility

Store raw data, schema, commands, environment inventory, source/binary/input digests, tool output, counter definitions, analysis code and generated summaries under governed artifacts.

Make analysis deterministic where possible. Record enough to rerun and to detect later event/erratum corrections.

### Review limitations

State unmeasured modes, excluded workloads, counter skid/multiplexing, timer resolution, virtualization, thermal range and hardware population. Distinguish simulation, FPGA and silicon evidence.

A benchmark result supports only the tested decision envelope. Generalization is a new claim needing evidence.

## Definitions and Notation

- `Delta I`: retired-instruction or useful-work delta over one aligned interval.
- `Delta C`: cycle delta over the same interval.
- `Delta t`: monotonic elapsed time for the same interval.
- `CPI=Delta C/Delta I`; `IPC=Delta I/Delta C` for nonzero counts.
- `f_eff=Delta C/Delta t`: effective counted-cycle rate under valid semantics.
- `X=Delta I/Delta t`: useful throughput.
- `k`: modeled pipeline depth; `N`: finite token count; `S`: distinct nonoverlapped stalls.
- `w`: counter width; modular delta is `(end-start) mod 2^w` under wrap assumptions.
- `p_q`: sample quantile under a named convention.
- **scope:** CPUs, threads, processes, modes and events included in a measurement.
- **skid:** distance between the causal event and sampled interrupt/record.
- **censoring:** exact latency is bounded but not observed, often due to timeout/end of window.
- **paired comparison:** baseline/candidate observations share matched controlled conditions.
- **residual:** elapsed work/time not explained by named additive/exclusive categories.

## Mechanisms, Invariants, or Proof Structure

1. **Decision obligation:** metric and acceptance threshold correspond to a stated engineering decision.
2. **Work obligation:** numerator counts the same useful/correct completion semantics for all variants.
3. **Boundary obligation:** time and all counter deltas use aligned start/stop scope.
4. **Counter obligation:** event semantics, width, wrap, inhibit, privilege, migration and overflow are handled.
5. **Identity obligation:** latency starts/completions and pipeline events match the same token/request.
6. **Arithmetic obligation:** CPI/IPC/time/frequency/fill/drain equations use compatible units/counts.
7. **Multiplex obligation:** time-sharing/scaling and rare-phase limitations are disclosed/validated.
8. **Environment obligation:** hardware/software/frequency/topology/background state is controlled and recorded.
9. **Workload obligation:** binary, input, seed, warm/cold state and correctness are fixed or explicitly varied.
10. **Replication obligation:** independent raw samples support the stated population and uncertainty method.
11. **Distribution obligation:** tails, failures, timeouts and quantile convention accompany relevant latency claims.
12. **Attribution obligation:** simultaneous stall causes are not double-counted as elapsed cycles.
13. **Causality obligation:** mechanism claims use controlled interventions or remain labeled correlational.
14. **Reproducibility obligation:** raw evidence, commands, identities and deterministic analysis are retained.
15. **Scope obligation:** conclusions and limitations do not exceed tested configurations/workloads/population.

## Alternatives and Trade-Offs

1. **Retired instructions versus operations:** instruction counts expose hardware work; operations better express application value.
2. **Wall time versus cycles:** wall time measures service; cycles explain microarchitecture under counter semantics.
3. **Throughput versus latency:** sustained capacity and per-request delay answer different decisions.
4. **Finite batch versus steady state:** finite runs include fill/drain; steady intervals characterize sustained behavior.
5. **Cold versus warm state:** cold captures startup; warm captures repeated service.
6. **Counters versus traces:** counters are low-volume; traces preserve order with overhead/volume.
7. **Counting versus sampling:** counting gives totals; sampling localizes behavior probabilistically.
8. **Pinned versus scheduler-realistic:** pinning reduces noise; real scheduling may match deployment.
9. **Isolated versus contended:** isolation diagnoses mechanisms; contention tests service reality.
10. **One-pass multiplexing versus matched passes:** multiplexing is convenient; matched passes improve event fidelity if workload stable.
11. **Mean versus median:** mean captures total expected cost; median describes typical center.
12. **Raw samples versus histograms:** raw data is flexible; bounded histograms scale if configuration is consistent.
13. **Exclusive versus multi-cause attribution:** exclusive counts add; multi-cause preserves overlap for union analysis.
14. **Microbenchmark versus application:** microbenchmarks isolate mechanisms; applications establish decision relevance.
15. **Maximum performance versus efficiency:** throughput may justify power; energy/thermal/service constraints can choose another point.

## Failure Modes and Misconceptions

1. “GHz is throughput.” Frequency omits useful work per cycle.
2. “CPI is instruction latency.” CPI is a throughput ratio over an interval.
3. “IPC and CPI can use different scopes.” Reciprocal checks require identical counts.
4. “Fetched instructions are completed work.” Wrong-path fetches may never retire.
5. “A cycle event has universal meaning.” Counter semantics and inhibition vary.
6. “Counter names are portable.” Model-specific encodings differ.
7. “End minus start always works.” Width wrap/reset/migration must be handled.
8. “A negative delta proves wrap.” Reprogramming or reset can look similar.
9. “Nominal frequency converts all cycles.” Turbo/throttle/idle/virtualization change effective behavior.
10. “Short timing regions are more precise.” Timer/instrumentation overhead can dominate.
11. “Warm-up is deleting slow runs.” It requires a predeclared state protocol.
12. “Many loop iterations are independent trials.” They share environment and state.
13. “The fastest run is representative.” Selective reporting biases conclusions.
14. “A mean describes tail latency.” Different distributions share a mean.
15. “Average shard percentiles give the global percentile.” Quantiles are nonlinear.
16. “Timeouts can be dropped.” They are material failures/censored tails.
17. “Multiplex scaling is exact.” Phase correlation creates bias.
18. “No lost-sample warning means no skid.” Sampling attribution remains approximate.
19. “Stall counters add to total cycles.” Causes can overlap and use different denominators.
20. “A high counter proves causality.” Controlled intervention is needed.
21. “Lower CPI guarantees faster time.” Clock period/frequency may change.
22. “More throughput guarantees lower latency.” Queueing and batching can worsen tails.
23. “Pinning makes results universal.” It defines a special placement condition.
24. “Same source means same work.” Compiler/binary/input identity matters.
25. “Statistical significance proves engineering value.” Effect size and threshold matter.
26. “One machine validates the fleet.” Hardware, firmware and environment populations vary.

## Worked Examples

### Example 1

Five million retired instructions over 6.25 million aligned cycles gives CPI 1.25 and IPC 0.8; their product is one aside from rounding.

### Example 2

The same interval lasts 2.5 ms, giving two billion instructions/s. Dividing by nominal frequency instead would be unnecessary and potentially wrong.

### Example 3

A 32-bit counter wraps between readings. Modular subtraction gives the small positive delta if at most one wrap and no reset occurred.

### Example 4

A seven-stage pipeline runs only 100 tokens; six fill/drain cycles remain visible even at ideal initiation interval one.

### Example 5

A tool multiplexes a rare miss event during alternating workload phases. Time scaling is biased because measured slices are not representative.

### Example 6

Two latency systems share median 100 microseconds; one has timeouts and p99 seconds. Median-only reporting misses the service risk.

### Example 7

Data and memory stall bits assert on the same cycle. Multi-label counts increase by two, while elapsed stall union increases by one.

### Example 8

A lower-CPI candidate runs at a lower effective frequency due to longer bypass paths. Wall-time throughput determines the winner.

### Example 9

A cache-miss counter correlates with slow runs; changing access locality while holding work fixed tests whether misses cause the slowdown.

### Example 10

This deterministic model cross-checks wrapped counters, CPI/IPC, finite pipeline performance and latency summaries.

<!-- bijux-verify: {"id":"pipeline-measurement-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"counter_delta=496\ncpi=1.250 ipc=0.800 elapsed_ms=2.500 throughput_mips=2000.00\nfinite_cycles=126 first_latency_ns=2.80 total_ns=50.40 throughput_mips=1984.13\nlatency_mean_ns=119.62 median_ns=101.50 p95_ns=250\n"}} -->
```python
from math import ceil
from statistics import mean, median

width = 32
start = 4_294_967_200
end = 400
delta = (end - start) % (1 << width)

retired = 5_000_000
cycles = 6_250_000
elapsed_s = 0.0025

tokens = 100
depth = 7
stalls = 20
period_ns = 0.40
finite_cycles = tokens + depth - 1 + stalls
total_ns = finite_cycles * period_ns

latencies_ns = [101, 99, 104, 100, 98, 103, 102, 250]
ordered = sorted(latencies_ns)
p95 = ordered[ceil(0.95 * len(ordered)) - 1]

print(f"counter_delta={delta}")
print(f"cpi={cycles / retired:.3f} ipc={retired / cycles:.3f} elapsed_ms={elapsed_s * 1000:.3f} throughput_mips={retired / elapsed_s / 1_000_000:.2f}")
print(f"finite_cycles={finite_cycles} first_latency_ns={depth * period_ns:.2f} total_ns={total_ns:.2f} throughput_mips={1000 * tokens / total_ns:.2f}")
print(f"latency_mean_ns={mean(latencies_ns):.2f} median_ns={median(latencies_ns):.2f} p95_ns={p95}")
```

The counts and samples are invented. The model establishes units and arithmetic, not an empirical processor claim.

## Cross-Program Connections

- **Statistics:** sampling units, quantiles, censoring, paired comparisons and uncertainty govern inference.
- **Operating Systems:** scheduling, affinity, PMU permissions, interrupts and tooling shape observations.
- **Compilers:** generated instructions and code layout change counts, hazards and branch behavior.
- **Data Engineering:** schemas, raw-event retention and deterministic pipelines support reproducibility.
- **Security Engineering:** counter access can expose information and therefore follows privilege policy.
- **Formal Methods:** accounting identities and event semantics can be asserted against traces.
- **Performance Engineering:** workload design, controls, causal interventions and decision thresholds are core methods.
- **Systems Engineering:** hardware/firmware/software/environment identities bound every conclusion.

## References

1. RISC-V International, [Counters](https://docs.riscv.org/reference/isa/unpriv/counters.html), current unprivileged counter/time interfaces and semantics; retrieved 2026-09-04.
2. RISC-V International, [Machine-Level ISA](https://docs.riscv.org/reference/isa/priv/machine.html), current machine counter enable/inhibit and privilege behavior; retrieved 2026-09-04.
3. lowRISC, [Ibex Performance Counters](https://ibex-core.readthedocs.io/en/latest/03_reference/performance_counters.html), current implemented event/counter definitions; retrieved 2026-09-04.
4. OpenTitan, [RV Core Ibex](https://opentitan.org/book/hw/ip/rv_core_ibex/), current integrated configuration, security and verification context; retrieved 2026-09-04.
5. Linux kernel, [Perf Events and Tool Security](https://docs.kernel.org/admin-guide/perf-security.html), current PMU access and security controls; retrieved 2026-09-04.
6. Linux perf community, [Perf Tutorial](https://perf.wiki.kernel.org/index.php/Tutorial), counting, sampling and event-group usage; retrieved 2026-09-04.
7. Standard Performance Evaluation Corporation, [SPEC CPU 2017 Overview](https://www.spec.org/cpu2017/Docs/overview.html), benchmark run/result context and rules overview; retrieved 2026-09-04.
8. Sarah L. Harris and David Money Harris, [Digital Design and Computer Architecture: RISC-V Edition Resources](https://pages.hmc.edu/harris/ddca/ddcarv.html), pipeline performance teaching resources; retrieved 2026-09-04.

## Exercises

### Exercise 1

Design a measurement record for CPI, IPC and throughput that detects interval, scope, counter-wrap and frequency inconsistencies.

### Exercise 2

Measure finite-batch and steady-state behavior for pipelines of depths five and nine under the same work and stall distribution.

### Exercise 3

Design a latency experiment reporting warm/cold behavior, tails, timeouts, overhead and uncertainty without pseudoreplication.

### Exercise 4

Extend the executable model to combine multiple runs correctly and explain why averaging their CPI values can differ from aggregate CPI.

### Exercise 5

Write an evidence plan for claiming that a forwarding change improves application throughput by at least 5% without latency, energy or correctness regression.

## Answers to the Exercises

### Answer 1

Record start/end retired and cycle counters, width, CPU, thread/process/privilege scope, enabled/running time, inhibit/filter state, overflow/lost indicators, monotonic timestamps and migration/hotplug/reset markers. Compute modular deltas only under a bounded-wrap/no-reset assumption. Reject zero denominators.

Cross-check CPI*IPC approximately one, throughput equals work/elapsed, and cycles/elapsed gives a plausible effective frequency under event semantics. Preserve raw readings and event-guide/tool/kernel/hardware identities.

### Answer 2

For each depth `k` and batch `N`, model/measure `N+k-1+S_union` cycles from an explicitly empty start; measure first-token and final-token times. For steady state, use a long interval after an objective warm-up and report admissions/completions, CPI/IPC and stall distribution.

Keep period, correctness, workload and environment recorded; depth changes may alter clock and stall penalties. Sweep short/long `N`, replicate independently, and report where fill/drain becomes negligible rather than deleting it.

### Answer 3

Define request start/completion and monotonic clock, identity matching, timeout and censoring. Run separately declared cold-start and warmed protocols; warm-up ends by fixed/predeclared stability rule. Batch enough work to quantify timestamp overhead, while preserving per-request samples or a configured mergeable histogram.

Use independent process/time/machine repetitions, randomized variant order and paired analysis. Report count, failures/timeouts, mean, median, p90/p95/p99/max, quantile convention and interval estimates. Preserve raw data and environment/thermal/background metadata; do not remove outliers post hoc.

### Answer 4

For runs `r`, aggregate CPI is `sum cycles_r / sum instructions_r`, which weights by instruction count. Arithmetic mean of `cycles_r/instructions_r` gives each run equal weight and differs when instruction counts vary. Extend the model with run tuples, sum raw counts first, then compare both summaries.

Choose aggregation by estimand: per-instruction population uses raw-weighted ratio; typical-run behavior may use per-run distribution. Never pool incompatible workloads/scopes. Keep elapsed throughput separately weighted by total work/total aligned time.

### Answer 5

Predeclare same correct application operation/input as work, at least 5% paired throughput improvement, no meaningful p95/p99 latency or energy-per-operation regression, and correctness gates. Build exact baseline/candidate binaries, record commits/configs, and validate generated code plus unit/ISA/application outputs.

Interleave paired runs across representative machines/workloads under recorded placement/frequency/thermal conditions. Collect wall throughput/latency/energy plus aligned retired/cycle and validated hazard/stall events; avoid multiplex bias. Use confidence intervals/effect sizes and mechanism intervention, preserve raw artifacts/commands, and scope the claim to tested populations. Internal evidence does not constitute independent certification.
