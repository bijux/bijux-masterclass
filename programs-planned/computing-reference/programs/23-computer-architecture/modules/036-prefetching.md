---
module_id: CA-036
program: Computer Architecture
level: 1
module_number: 36
title: Prefetching
status: complete
last_verified: 2026-09-04
---

# Prefetching

## One-Page Review

### Governing question

How can hardware or software predict future instruction/data demand early enough to hide latency while preventing inaccurate, late or redundant requests from consuming the cache capacity, bandwidth, tracking state, energy, coherence work and fault behavior needed by real demand?

### Essential definitions

- A **prefetch** requests data or instructions before an architecturally demanding access requires them.
- A **next-line prefetcher** predicts the block immediately after a trigger block.
- A **stride prefetcher** predicts repeated address differences, often per instruction or stream context.
- A **stream prefetcher** recognizes consecutive blocks and continues ahead of observed demand.
- A **correlation prefetcher** predicts from previously observed address or delta sequences.
- **degree** is the number of blocks requested per trigger or prediction event.
- **distance** is how far ahead of current demand a prefetch targets.
- **accuracy** is useful prefetched blocks divided by issued prefetches under a stated attribution rule.
- **coverage** is demand misses eliminated by useful prefetches divided by baseline demand misses under matched runs.
- **timeliness** describes whether a useful prefetch completes before demand, neither too late nor excessively early.
- A **late prefetch** targets a block demanded while its prefetch is still outstanding.
- A **redundant prefetch** requests a block already present, already outstanding or otherwise unnecessary.
- **pollution** is harmful displacement or state interference caused by prefetched content.
- **throttling** adapts issuance, distance, degree or insertion using resource pressure and observed quality.
- A **prefetch buffer** holds predicted blocks outside or before normal cache insertion.

### Central model, mechanism, or theorem

Prefetch value is constrained speculation: predict candidate block `p` from history `H`, reject duplicates/illegal targets, reserve finite resources, issue with lower priority, and attribute later demand or eviction to that prediction. A useful prefetch must be accurate and timely, but system benefit additionally requires saved demand stall to exceed added queueing, traffic, pollution, coherence, translation and energy costs. Correctness must be identical with prefetching disabled: speculative fills cannot create architectural faults, stale ownership, extra device operations or lost demand progress.

### Critical invariants

- Prefetch addresses obey exact block geometry, address-space, privilege, memory-type and translation rules.
- Suppressed or dropped prefetches never change architectural results.
- A prefetch cannot expose an exception that the corresponding demand never executes unless the ISA explicitly permits it.
- Demand and coherence traffic retain a progress path under maximum prefetch pressure.
- Duplicate demand/prefetch requests merge or serialize without conflicting transient copies.
- Prefetched data becomes visible only after identity, permissions, integrity and coherence state are valid.
- A prefetch cannot read non-idempotent device memory or cross forbidden protection/context boundaries.
- Attribution counts each issued prefetch and each useful demand benefit consistently and at most once.
- Pollution, bandwidth and queue costs are measured against an identical no-prefetch baseline.
- Training, tables and counters are partitioned, flushed or threat-modeled across security contexts.

### Common failures

Common failures include calling cache hits after prefetching “accuracy,” dividing useful prefetches by demand accesses, crediting requests that would have hit anyway, issuing next-page requests before safe translation, prefetching device registers, consuming every MSHR during a burst, treating a late merge as full latency removal, inserting speculative lines at highest priority, ignoring unused lines still resident at measurement end, letting killed-path accesses train forever, comparing different warm-up windows, counting traffic in transactions for one design and bytes for another, assuming higher coverage improves runtime, and allowing software prefetch hints to change correctness.

### Compact example

For trace `[0,1,2,3,10,12,14,16,20,21,22,23]` in a four-line fully associative LRU model, demand alone has 12 misses. An immediate next-line policy issues 12 prefetches, makes six later demands hit and causes four modeled demand-line evictions. Accuracy is `6/12=50%`; coverage is `(12-6)/12=50%`; total modeled line reads rise from 12 to 18, or 150% of baseline. The arithmetic demonstrates why useful predictions can still increase traffic and pollution; it assumes zero prefetch latency and is not a performance result.

### Connections

Prefetching connects sequential/stride/correlation prediction, cache replacement, virtual memory, coherence, MSHRs, DRAM row/bank scheduling, compiler hints, speculative execution, security isolation, feedback control and workload-driven performance evaluation.

## Governing Question

Memory latency can be overlapped only if the system begins work before demand becomes blocking. Prefetching guesses which work to begin. The prediction may be simple and cheap or context-rich and costly, but it always spends resources before usefulness is known.

A prefetcher is therefore not judged by prediction rate alone. It must deliver the right block early enough, preserve more valuable cache state, avoid delaying demand and remain architecturally invisible when wrong.

## Why This Matters

Regular loops can make prefetching highly effective, while pointer-rich or phase-changing programs defeat fixed patterns. Shared caches and memory make one requester's speculative traffic visible to others through contention.

Aggressive prefetching can reduce isolated miss counts while slowing the whole system. Bandwidth amplification, cache pollution, directory probes, translation walks and DRAM interference all matter.

Prefetch state also observes address histories. Cross-context predictor state and timing can create leakage, so quality control and security lifecycle must be designed together.

## Prerequisites and Retrieval

Before studying this module, be able to:

- trace multilevel-cache hit, miss, refill and eviction flows;
- distinguish local/global hit rates and AMAT limitations;
- explain cache replacement and MSHR/writeback resources;
- interpret virtual-to-physical translation and memory types;
- compare two runs using identical workloads and measurement windows.

Retrieve trigger event and address stage; block/sector geometry; instruction/data and virtual/physical identity; predictor type, table indexing, tags and confidence; history length; degree/distance; page-crossing policy; translation/TLB behavior; request priority and QoS; destination level/buffer; insertion/replacement policy; MSHR/fill/interconnect/memory resources and reservations; duplicate/late merge rules; coherence permissions and directory traffic; fault/poison/device behavior; training on speculative/killed/replayed accesses; throttling signals and epochs; security partition/flush behavior; counters and attribution definitions; simulator/RTL/compiler/ISA/OS/hardware revisions; workloads, warm-up, seeds and errata.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish next-line, stream, stride and correlation predictors;
2. define trigger, prediction context, confidence, degree and distance;
3. compute accuracy, coverage, timeliness, redundancy and traffic metrics;
4. detect misleading denominators and baseline mismatches;
5. integrate prefetches with translation, coherence and finite miss resources;
6. prevent pollution and demand starvation through insertion and throttling;
7. preserve architectural fault and device-access behavior;
8. evaluate prefetch benefit under queueing, bandwidth and application dependencies;
9. verify safety, accounting and conditional progress invariants;
10. choose a policy using representative workloads and physical/system evidence.

## Core Exposition

### Treat prefetch as speculation

A predicted request may never be used. Keep it distinguishable from demand in priority, accounting and fault delivery while using the same identity, integrity and coherence machinery needed for trustworthy data.

Turning a prediction into an ordinary high-priority demand loses the ability to protect required work from speculation.

### Define the trigger

Triggers may be cache accesses, misses, fills, retired loads, instruction fetches or software hints. Earlier triggers provide lead time but include more speculative or killed work.

Document whether replays, hits, stores and coherence events train or issue. Ensure one logical event does not trigger repeatedly through pipeline stalls.

### Implement next-line prediction

Next-line prefetching requests block `b+1` after observing `b`. It has little state and follows spatially sequential access.

It wastes traffic at region ends, interleaved streams and sparse accesses. Page, protection and memory-type boundaries constrain the arithmetic successor.

### Detect streams

A stream prefetcher waits for evidence of ascending or descending consecutive blocks, records direction and advances a lookahead window.

Confidence reduces startup waste but delays benefit. Multiple streams need tags, replacement and per-stream outstanding tracking.

### Detect strides

A stride prefetcher records recent addresses or deltas per load instruction/context. Repeated delta `d` predicts `a+d`, often extended by degree.

Aliasing two instructions into one table entry can fabricate patterns. Tags, confidence and context identity reduce destructive interference.

### Use correlation deliberately

Delta/path/correlation predictors learn sequences beyond one constant stride. They may capture recurring pointer or phase behavior at greater storage, lookup and training cost.

Report table sizes, history encoding, aliasing, update policy and fallback. A trace-oracle comparison helps bound opportunity but is not implementable performance.

### Choose prediction context

Instruction address, virtual/physical block, thread, address-space identifier and privilege may all be relevant. Too little context aliases unrelated streams; too much fragments learning.

Security boundaries may require partitioning or flushing predictor state even when accuracy would prefer sharing.

### Bound address generation

Check overflow, canonical form, block alignment and configured address width. Do not wrap a high address into a low one.

Degree expansion must independently validate every candidate. One valid prediction does not authorize later addresses.

### Respect translation

Virtual-address prediction can be early but must translate before physical cache/coherence access. A prefetch may use spare TLB capacity or create page-walk traffic.

Crossing a page needs a documented safe mechanism. Suppressing page crossings is conservative but can reduce coverage for sequential arrays.

### Respect protection and faults

A hardware prefetch generally must not expose a synchronous fault solely because a prediction targeted unmapped or disallowed memory. Drop or contain speculative faults according to the architecture.

When demand later arrives, it performs normal permission and fault handling. Never convert a failed speculative translation into a successful unauthorized fill.

### Exclude unsafe memory types

Device and non-idempotent reads may cause side effects. Prefetch only memory types for which speculative reads are permitted.

Memory attributes can change; revalidate at the correct stage and invalidate stale predictor/TLB assumptions.

### Deduplicate requests

Before issuing, check relevant caches, prefetch buffers, MSHRs and downstream outstanding state. A redundant target consumes traffic without adding coverage.

Races require atomic lookup/allocation or a merge protocol. Two requesters predicting the same block should not create conflicting ownership.

### Merge late prefetches

If demand arrives while its prefetch is outstanding, promote priority and attach the demand as a dependent. The prefetch was directionally correct but not fully timely.

Attribute saved latency from the actual remaining service, not as though the block had arrived before demand.

### Choose destination

A prefetch may enter L1, a lower cache or a dedicated buffer. Closer placement reduces demand lookup latency but increases pollution of scarce low-latency capacity.

A prefetch buffer requires tag lookup, promotion, eviction and coherence rules. It is part of the hierarchy, not free staging.

### Choose insertion priority

Low-priority insertion lets unused predictions leave quickly; high-priority insertion protects likely near-future demand. Confidence and reuse class can select between them.

Replacement metadata updates from speculative fills/hits must be explicitly defined and evaluated against demand reuse.

### Choose distance

Distance must cover prediction, queueing, translation and memory service before demand arrives. Too short yields late prefetches; too long increases eviction before use and crosses phases.

Express distance in blocks, iterations or estimated time and bind it to observed consumption rate.

### Choose degree

Higher degree can cover bursty sequential demand but multiplies requests and tracking. Stop at region limits, low confidence or pressure thresholds.

Degree and distance interact: many far-ahead blocks can monopolize capacity without improving timeliness.

### Preserve demand progress

Reserve MSHRs, fill buffers, interconnect credits and memory scheduling opportunity for demand/coherence/writeback traffic. Prefetch should yield under congestion.

Prove or stress that continuous confident streams cannot prevent an unrelated demand from completing under downstream fairness.

### Throttle with feedback

Feedback may use accuracy, lateness, pollution, bandwidth, queue occupancy, DRAM utilization or application slowdown. Adapt issuance, degree, distance or insertion.

Use stable epochs and hysteresis to avoid oscillation. Global throttling should consider cross-core harm, not only the issuer's hit improvement.

### Define usefulness attribution

Mark a prefetched block and credit at most the first qualifying demand that consumes data before eviction. If demand was already outstanding, classify it late/merged rather than fully useful.

Separate prefetched-line hits from hits that would have occurred without the prefetch using a baseline or shadow model when necessary.

### Measure accuracy

Accuracy is commonly `useful/issued`, but alternatives count filled or unique prefetches. State the denominator and treatment of canceled, merged and end-of-window residents.

High accuracy can have low coverage if the prefetcher issues rarely. It can still harm performance if correct requests arrive too late or delay more important traffic.

### Measure coverage

Coverage compares eliminated baseline misses with baseline misses. A matched no-prefetch run or shadow cache establishes counterfactual demand misses.

Do not calculate coverage from the prefetch-enabled miss count alone. Prefetch pollution may create new misses that need separate accounting.

### Measure timeliness

Classify early-enough, late and excessively early predictions. Record lead time from fill completion to demand and remaining latency for late merges.

A useful binary label hides whether latency was fully or partially removed. Distributions reveal tuning opportunities.

### Measure redundancy and pollution

Redundant requests target present or already-outstanding data. Pollution requires counterfactual evidence that a displaced line would have served later demand.

Shadow tags or paired runs can estimate harm. Attribute capacity, MSHR and bandwidth interference separately.

### Measure traffic and energy

Count requests and bytes by demand, prefetch, translation, coherence, retry and writeback class at every interface. Prefetched fills can trigger dirty evictions and directory work.

Measure predictor lookup/update energy plus cache/interconnect/memory work. Saved stall does not imply saved energy.

### Consider DRAM effects

Prefetch can expose bank parallelism and row locality or disrupt demand scheduling and row-buffer hits. Lower-priority queues can still occupy banks and credits.

Evaluate address mapping, scheduler priorities and read/write turnarounds with realistic contention.

### Handle stores and ownership

Read-prefetching a future store target may waste old data if full-line overwrite is imminent. Ownership prefetch can reduce later upgrade latency but creates coherence invalidations early.

Never acquire write authority across unsafe speculation boundaries without protocol, fairness and security analysis.

### Handle instructions

Instruction prefetchers follow control flow, streams or branch predictions. Wrong-path fetches consume instruction-cache, translation and bandwidth resources.

Code modification and instruction/data coherence require invalidation and synchronization; a stale prefetched instruction cannot become executable.

### Use software hints carefully

Compiler/programmer hints can expose semantic knowledge but should preserve correctness when ignored. Address computation itself must be safe under the language and ISA contract.

Tune locality and write/read intent only when supported; portable code needs guarded fallbacks and measurement.

### Manage lifecycle and security

Predictor tables survive phases unless aged, replaced or flushed. Context switches and privilege changes need a stated partition/flush policy.

Shared histories and timing can leak address patterns. Evaluate attacks through predictor aliasing, cache state and resource contention.

### Compare fairly

Use identical binaries, inputs, core/cache/memory, warm-up, measurement region, seeds and stopping rules. Record whether prefetch warms state before measurement.

Report accuracy, coverage, timeliness, pollution, traffic, energy, runtime and tails together. Geometric means do not replace per-workload regressions.

### Verify predictor and system behavior

Unit-test address sequences, confidence and table replacement. Use assertions for legal addresses, duplicate allocation, resource bounds, demand priority and exactly-once attribution.

Compare architectural results with prefetch disabled, inject full queues/errors/context changes and use formal checks for bounded control where feasible.

### Gather layered evidence

Start with deterministic traces and shadow models, then trace-driven and cycle simulation across suites and adversarial patterns. Validate model counters and timing against RTL or hardware where possible.

Include synthesis/STA/area/power for predictor structures and critical integration paths. Bind compiler, ISA, OS, simulator, RTL and silicon revisions.

## Definitions and Notation

- `I`: number of prefetch requests issued under the chosen denominator.
- `U`: number of prefetched blocks credited useful.
- `L`: number of late prefetches or late merges.
- `R`: number of redundant requests suppressed or issued, as stated.
- `M0`: baseline demand misses with prefetching disabled.
- `M1`: demand misses with prefetching enabled.
- `accuracy=U/I` when `I>0` under the documented attribution.
- `coverage=(M0-M1)/M0` is a simple paired-run form; pollution can make it negative.
- `lead(p)`: time from prefetch completion to consuming demand for prediction `p`.
- `degree`: maximum predictions generated per trigger.
- `distance`: address/iteration/time lookahead under a stated unit.
- `Qd` and `Qp`: demand- and prefetch-occupied finite resources.
- `traffic_ratio`: enabled total transferred bytes divided by baseline total bytes.
- `pollution_miss`: a demand miss attributable to prefetch displacement under a shadow/counterfactual model.

Metric definitions vary across tools. Always publish eligibility, denominator, attribution and measurement-window rules. When `I=0` or `M0=0`, report accuracy/coverage as undefined rather than inventing a perfect value.

## Mechanisms, Invariants, or Proof Structure

1. **Trigger obligation:** one defined event trains/issues at most the intended number of times.
2. **Address obligation:** generated candidates are aligned, in range and non-wrapping.
3. **Context obligation:** predictor lookup/training uses the intended thread, privilege and address-space identity.
4. **Translation obligation:** no physical access occurs before valid translation and attributes.
5. **Fault obligation:** speculative failure cannot create an otherwise absent architectural exception or authorization.
6. **Memory-type obligation:** prefetch never performs forbidden device/non-idempotent access.
7. **Duplicate obligation:** present/outstanding candidates suppress, merge or serialize coherently.
8. **Fill obligation:** only identified, integrity-checked, permission-valid data becomes available.
9. **Ownership obligation:** ownership prefetch and eviction conform to coherence and dirty-data rules.
10. **Resource obligation:** issued requests fit retained MSHR, buffer, credit and response state.
11. **Priority obligation:** demand, coherence and writeback retain a progress path under speculative load.
12. **Attribution obligation:** every issued/useful/late/redundant/polluting event follows one documented rule.
13. **Lifecycle obligation:** training and state flush/partition behavior match context/security policy.
14. **Equivalence obligation:** disabling or dropping all prefetches preserves architectural results.
15. **Evidence obligation:** quality/runtime claims share exact baselines, windows, configurations and revisions.

Prove address, resource and accounting safety locally around the predictor/queues. Compose with cache/coherence refinement to show speculative requests cannot change architectural outcomes. Progress proofs require downstream fairness and reserved demand paths. Performance remains empirical because prediction usefulness and contention depend on workloads.

## Alternatives and Trade-Offs

1. **Next-line versus stream:** next-line starts immediately; stream confidence reduces sparse-pattern waste.
2. **Stride versus correlation:** stride uses compact state; correlation captures richer sequences with more aliasing/storage.
3. **PC-indexed versus address-indexed:** PC context separates instructions; address context follows shared regions.
4. **Virtual versus physical prediction:** virtual starts early; physical avoids synonym/context ambiguity after translation.
5. **Cross-page versus stop-at-page:** crossing raises coverage; stopping avoids speculative translation/protection cost.
6. **Near versus far distance:** near reduces premature eviction; far provides more latency tolerance.
7. **Low versus high degree:** low protects bandwidth; high follows fast streams.
8. **L1 versus lower-level destination:** L1 minimizes hit latency; lower placement reduces scarce upper pollution.
9. **Cache insertion versus prefetch buffer:** cache reuse is direct; a buffer isolates capacity with extra lookup/movement.
10. **High versus low insertion priority:** high retains predictions; low limits harm from unused lines.
11. **Static versus adaptive control:** static is predictable; feedback responds to phases but can oscillate.
12. **Shared versus per-core state:** sharing learns common patterns; private/partitioned state improves isolation.
13. **Hardware versus software prefetch:** hardware observes dynamic streams; software exposes program intent with portability cost.
14. **Read versus ownership prefetch:** reads avoid early invalidation; ownership can hide upgrade latency for stores.
15. **Local versus system-aware throttling:** local optimizes issuer metrics; global control can protect other requesters.

## Failure Modes and Misconceptions

1. “Every prefetched-line hit is useful.” It may have displaced a line or would have hit without prediction.
2. “Accuracy is hits divided by demand accesses.” Its denominator is normally issued/filled prefetches.
3. “Coverage equals one minus enabled miss rate.” It needs baseline misses and a defined counterfactual.
4. “Correct address means timely.” A demand can arrive before the fill.
5. “Late prefetch has zero benefit.” Priority promotion may save some remaining latency.
6. “Unused residents at measurement end are useful.” They need an explicit censored/unused policy.
7. “Next block is safe across a page.” Translation, protection and memory type may change.
8. “Prefetch faults can be delivered normally.” Wrong-path predictions must not create absent architectural faults.
9. “Device reads are just cacheable reads.” They may have non-idempotent side effects.
10. “Duplicate prefetches only waste counters.” They consume queues, bandwidth and coherence work.
11. “All MSHRs may be used speculatively.” Demand can deadlock/starve without reservation or preemption.
12. “Low-priority memory scheduling prevents harm.” Requests still occupy finite upstream and bank resources.
13. “Insertion policy does not affect accuracy.” Eviction-before-use and pollution depend on it.
14. “Higher degree always increases coverage.” It can cause eviction, congestion and phase overshoot.
15. “Larger distance always improves timeliness.” It may arrive too early and be displaced.
16. “One stride table entry represents one load.” Aliasing can combine unrelated histories.
17. “Killed-path training is harmless.” It changes future predictions and may leak/speculate across contexts.
18. “A prefetch buffer is outside coherence.” Its valid copies and ownership still participate.
19. “Prefetching cannot affect writes.” It can cause dirty victims or premature ownership traffic.
20. “Miss reduction proves speedup.” Overlap, dependencies and contention determine runtime.
21. “More traffic means higher bandwidth use only.” It also changes queueing, DRAM rows and energy.
22. “Single-core gains predict multicore gains.” Shared interference and fairness can reverse results.
23. “Warm-up does not matter.” Predictor/cache state changes issuance and attribution.
24. “Compiler prefetch is always legal if ignored.” Computing or issuing an invalid address can violate language/ISA rules.
25. “Flush only caches on context switch.” Predictor state may retain sensitive histories.
26. “One benchmark average validates policy.” Phase and per-workload regressions require inspection.

## Worked Examples

### Example 1

Demand blocks `0,1,2,3` allow next-line prediction from 0 to make 1 available; the same policy wastes block 4 if the stream ends at 3.

### Example 2

A PC observes deltas `+8,+8`; after confidence rises it predicts the next address at `+8`. An aliasing PC with `-64` deltas can corrupt the entry without tags.

### Example 3

Demand arrives while its prefetch awaits DRAM. The MSHR promotes priority and merges the dependent; accounting marks it late, not an early useful fill.

### Example 4

A candidate is already valid in L2. Duplicate suppression avoids a memory request but may still record that the predictor generated a redundant candidate.

### Example 5

An ascending stream reaches a page boundary. The prefetcher stops unless it can safely translate and validate the next page's attributes.

### Example 6

Accuracy is 90% but only 9 of 1,000 baseline misses are removed because just ten requests issue. High accuracy and low coverage coexist.

### Example 7

Four aggressive prefetches evict a demand line that is reused immediately. One useful prediction and one new pollution miss can yield no miss-count gain.

### Example 8

An LLC prefetch avoids L1 pollution but demand later pays the L1 miss and promotion latency. Destination trades capacity harm against residual latency.

### Example 9

Queue occupancy crosses a high threshold, so feedback reduces degree; it restores degree only below a lower threshold to avoid oscillation.

### Example 10

This deterministic fully associative model audits immediate next-line usefulness, coverage, traffic and modeled demand-line evictions.

<!-- bijux-verify: {"id":"prefetch-quality-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"baseline_accesses=12 hits=0 misses=12\nprefetch_accesses=12 hits=6 misses=6 issued=12 useful=6 demand_line_evictions=4\naccuracy_pct=50.00 coverage_pct=50.00 baseline_line_reads=12 enabled_line_reads=18 traffic_ratio_pct=150.00\n"}} -->
```python
from collections import OrderedDict

def simulate(trace, capacity, prefetch_enabled):
    cache = OrderedDict()
    prefetched = set()
    hits = misses = issued = useful = demand_line_evictions = 0
    for block in trace:
        if block in cache:
            hits += 1
            if block in prefetched:
                useful += 1
                prefetched.discard(block)
            cache.move_to_end(block)
        else:
            misses += 1
            if len(cache) == capacity:
                victim, _ = cache.popitem(last=False)
                prefetched.discard(victim)
            cache[block] = None
        if prefetch_enabled:
            candidate = block + 1
            if candidate not in cache:
                issued += 1
                if len(cache) == capacity:
                    victim, _ = cache.popitem(last=False)
                    if victim not in prefetched:
                        demand_line_evictions += 1
                    prefetched.discard(victim)
                cache[candidate] = None
                prefetched.add(candidate)
    return hits, misses, issued, useful, demand_line_evictions

trace = [0, 1, 2, 3, 10, 12, 14, 16, 20, 21, 22, 23]
base = simulate(trace, capacity=4, prefetch_enabled=False)
enabled = simulate(trace, capacity=4, prefetch_enabled=True)
accuracy = 100 * enabled[3] / enabled[2]
coverage = 100 * (base[1] - enabled[1]) / base[1]
baseline_reads = base[1]
enabled_reads = enabled[1] + enabled[2]

print(f"baseline_accesses={len(trace)} hits={base[0]} misses={base[1]}")
print(f"prefetch_accesses={len(trace)} hits={enabled[0]} misses={enabled[1]} issued={enabled[2]} useful={enabled[3]} demand_line_evictions={enabled[4]}")
print(f"accuracy_pct={accuracy:.2f} coverage_pct={coverage:.2f} baseline_line_reads={baseline_reads} enabled_line_reads={enabled_reads} traffic_ratio_pct={100 * enabled_reads / baseline_reads:.2f}")
```

The model assumes instantaneous prefetch completion, fully associative LRU, unit line reads, no writes/coherence/translation/queueing and credits every first demand hit on a marked line. It exposes arithmetic and attribution assumptions, not measured speedup.

## Cross-Program Connections

- **Algorithms:** online sequence prediction trades state and false positives against future-hit opportunity.
- **Compilers:** software hints connect loop/access analysis to microarchitectural latency hiding.
- **Operating Systems:** translation, memory types, context switches and page placement bound legal prediction.
- **Concurrent Systems:** MSHRs, credits, arbitration and priority govern progress under speculation.
- **Machine Learning:** confidence and feedback adapt prediction while facing aliasing, drift and phase change.
- **Security Engineering:** shared predictor/cache histories and contention create leakage surfaces.
- **Performance Engineering:** counterfactual misses, timeliness, traffic, energy and runtime establish value.
- **Formal Methods:** equivalence with prefetch disabled and resource invariants establish safety.

## References

1. RISC-V International, [Cache Management Operations](https://docs.riscv.org/reference/isa/unpriv/cmo.html), current Zicbop prefetch-hint and cache-operation architectural context; retrieved 2026-09-04.
2. gem5, [Classic Caches](https://www.gem5.org/documentation/general_docs/memory_system/classic_caches/), current cache, prefetch, MSHR, write-buffer and port modeling context; retrieved 2026-09-04.
3. ChampSim, [ChampSim Repository](https://github.com/ChampSim/ChampSim), current trace-based cache/prefetch simulation framework and reproducibility context; retrieved 2026-09-04.
4. GCC, [Other Built-ins](https://gcc.gnu.org/onlinedocs/gcc/Other-Builtins.html), current `__builtin_prefetch` software-hint contract and locality/read-write arguments; retrieved 2026-09-04.
5. Clang, [Language Extensions](https://clang.llvm.org/docs/LanguageExtensions.html), current compiler built-in and feature-detection context for portable low-level code; retrieved 2026-09-04.
6. Valgrind, [Cachegrind Manual](https://valgrind.org/docs/manual/cg-manual.html), current cache simulation and event interpretation used for baseline reasoning; retrieved 2026-09-04.
7. Intel, [Intel 64 and IA-32 Architectures Software Developer Manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), current prefetch, cache, memory-type and ordering architectural context; retrieved 2026-09-04.

## Exercises

### Exercise 1

Trace next-line, stream and PC-stride prefetchers on interleaved ascending, descending and sparse accesses, recording confidence, issuance, usefulness and evictions.

### Exercise 2

Design a prefetch request path that handles TLB misses, page boundaries, device memory, duplicate MSHRs and speculative faults safely.

### Exercise 3

Specify a feedback controller for degree and distance using accuracy, lateness and resource pressure without rapid oscillation.

### Exercise 4

Extend the executable model with nonzero latency, a prefetch queue and a shadow cache to classify late predictions and pollution misses.

### Exercise 5

Write a verification and evaluation plan for deploying a shared-cache prefetcher in a multicore processor with security isolation requirements.

## Answers to the Exercises

### Answer 1

Build a per-access table containing PC/context, block, delta, predictor entry/tag/confidence, candidates, duplicate outcome, cache contents and whether prior prefetched blocks become useful or unused. Next-line issues immediately; stream waits for consecutive evidence; PC-stride separates interleaved instructions when entries do not alias.

Apply the same cache, insertion, degree, latency and end-window rules. Sparse regions expose next-line waste, direction changes expose stale confidence, and table collisions expose aliasing. Report accuracy, coverage and traffic rather than only demand hits.

### Answer 2

Generate bounded aligned virtual candidates, reject overflow, and submit each through speculative translation tagged with context/generation. Suppress or contain translation/protection faults, validate physical memory type, and drop device/non-idempotent targets. Probe cache/MSHR/prefetch state atomically and merge duplicates.

Reserve only quota-limited prefetch resources; demand may promote a matching request. Responses recheck generation, identity, permissions, coherence and integrity before insertion. Context invalidation cancels or quarantines stale work without exposing a fault or unauthorized data.

### Answer 3

Within sufficiently long epochs, compute useful/issued, late/useful, pollution estimates and demand/coherence queue pressure. Raise distance when accurate predictions are late and pressure is low; reduce degree/distance when accuracy falls or pressure/pollution rises. Use high/low thresholds, minimum residency and bounded increments for hysteresis.

Reserve demand resources independently of feedback. Evaluate convergence and phase changes using deterministic traces, then multicore applications. Record controller state and denominators so apparent improvements are reproducible.

### Answer 4

Associate each issued prediction with completion time and generation. Demand before completion merges and counts late; demand after completion consumes a marked line and records lead time. Maintain a parallel demand-only shadow cache; if a prefetched insertion evicts a block whose later access hits shadow but misses enabled state, classify a pollution miss.

Bound the prefetch queue and schedule demand first. Report issued, suppressed, redundant, useful, late, unused, pollution, bytes, lead/remaining-latency distributions and demand stall. Validate zero-latency behavior against the supplied model.

### Answer 5

Verify address/context tags, translation/protection/device exclusions, duplicate merging, coherence ownership, dirty victims, finite-resource reservations, demand progress, response generations, fault suppression, context flush/partition and architectural equivalence with prefetch disabled. Use assertions, reference/shadow models, formal bounded control checks and adversarial queues/errors.

Evaluate per-core and system runtime, tails, fairness, accuracy, coverage, lateness, pollution, traffic classes, DRAM interference, energy, area and timing across workloads/phases and attacker-victim placements. Bind ISA/compiler/OS/simulator/RTL/SRAM/silicon revisions and errata; internal testing does not claim external performance, security or silicon certification.
