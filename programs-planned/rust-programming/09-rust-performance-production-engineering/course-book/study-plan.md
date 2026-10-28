# Course 9 Study Plan — Rust Performance and Production Engineering

Ten dense study days fit into two calendar weeks. The goal is not to maximize reading time; it is to make **Which measurements, resource bounds, signals, security controls, artifact records, and operating policies make a Rust system defensible under representative load?** answerable through construction and explanation.

## Daily rhythm

Use a **production decision record** across the course. Each day begins by reconstructing yesterday’s decisive relationship and ends by tracing one capstone invariant. Preserve the first prediction, the observed result, the principled repair, and the shortcut you rejected.

## Day 1 — Module 81: Performance Contracts, Workloads, and Benchmark Design

**Question:** What exactly must become faster, under which workload and resource limits, and what experiment would distinguish improvement from noise or self-deception?

**Retrieval:** Without notes, restate the invariant carried from Module 80 — Integrated Async Service Architecture, Testing, and Audit. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 81](./module-81-performance-contracts-workloads-and-benchmark-design/index.md) with a **performance claim and workload record** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-81-performance-contracts-workloads-and-benchmark-design/workbook.md) before observation. The day’s minimum result is: **Turn an imprecise performance complaint into a falsifiable contract with workload, metric, percentile, resource budget, and correctness oracle.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Benchmark Integrity Clinic](../labs/module-01-benchmark-integrity-clinic/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 81 in the [MetricRail guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Turn an imprecise performance complaint into a falsifiable contract with workload, metric, percentile, resource budget, and correctness oracle.** End with one simpler design that would be preferable under a narrower requirement.

## Day 2 — Module 82: CPU Profiling, Cost Models, and Hot-Path Optimization

**Question:** Where does execution time actually go, why does it go there, and which change removes the dominant cost without moving it into an unmeasured phase?

**Retrieval:** Without notes, restate the invariant carried from Module 81 — Performance Contracts, Workloads, and Benchmark Design. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 82](./module-82-cpu-profiling-cost-models-and-hot-path-optimization/index.md) with a **profile and cost model** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-82-cpu-profiling-cost-models-and-hot-path-optimization/workbook.md) before observation. The day’s minimum result is: **Choose sampling, instrumentation, counters, and targeted tracing based on the question being asked.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Profile-Guided Query Engine](../labs/module-02-profile-guided-query-engine/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 82 in the [MetricRail guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Choose sampling, instrumentation, counters, and targeted tracing based on the question being asked.** End with one simpler design that would be preferable under a narrower requirement.

## Day 3 — Module 83: Allocation, Memory Footprint, and Ownership Cost

**Question:** Which bytes are owned, borrowed, reserved, retained, duplicated, or temporarily allocated, and which of those states actually dominate product cost?

**Retrieval:** Without notes, restate the invariant carried from Module 82 — CPU Profiling, Cost Models, and Hot-Path Optimization. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 83](./module-83-allocation-memory-footprint-and-ownership-cost/index.md) with a **allocation ledger** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-83-allocation-memory-footprint-and-ownership-cost/workbook.md) before observation. The day’s minimum result is: **Distinguish object size, heap allocation, capacity, live bytes, retained bytes, peak bytes, and allocation count.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Allocation-Budgeted Batch Parser](../labs/module-03-allocation-budgeted-batch-parser/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 83 in the [MetricRail guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Distinguish object size, heap allocation, capacity, live bytes, retained bytes, peak bytes, and allocation count.** End with one simpler design that would be preferable under a narrower requirement.

## Day 4 — Module 84: Data Movement, Buffering, and Zero-Copy Boundaries

**Question:** Where do bytes move, who owns them at each boundary, and when does avoiding a copy improve the whole system rather than merely relocate lifetime and retention cost?

**Retrieval:** Without notes, restate the invariant carried from Module 83 — Allocation, Memory Footprint, and Ownership Cost. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 84](./module-84-data-movement-buffering-and-zero-copy-boundaries/index.md) with a **byte journey** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-84-data-movement-buffering-and-zero-copy-boundaries/workbook.md) before observation. The day’s minimum result is: **Trace bytes across kernel, transport, framing, parsing, domain, storage, and response layers.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Borrowed Record Window](../labs/module-04-borrowed-record-window/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 84 in the [MetricRail guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Trace bytes across kernel, transport, framing, parsing, domain, storage, and response layers.** End with one simpler design that would be preferable under a narrower requirement.

## Day 5 — Module 85: Runtime Efficiency: Contention, Queueing, Batching, and Async Load

**Question:** When work is correct and bounded, where do contention, waiting, scheduling, queueing, batching, and blocking determine throughput and tail latency?

**Retrieval:** Without notes, restate the invariant carried from Module 84 — Data Movement, Buffering, and Zero-Copy Boundaries. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 85](./module-85-runtime-efficiency-contention-queueing-batching-and-async-load/index.md) with a **saturation and queueing curve** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-85-runtime-efficiency-contention-queueing-batching-and-async-load/workbook.md) before observation. The day’s minimum result is: **Separate service time, wait time, queue depth, concurrency, throughput, and utilization.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Bounded Throughput Tuner](../labs/module-05-bounded-throughput-tuner/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 85 in the [MetricRail guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Separate service time, wait time, queue depth, concurrency, throughput, and utilization.** End with one simpler design that would be preferable under a narrower requirement.

## Midpoint reconstruction

Do not add a sixth topic on the recovery day. Reconstruct **Performance Contracts, Workloads, and Benchmark Design, CPU Profiling, Cost Models, and Hot-Path Optimization, Allocation, Memory Footprint, and Ownership Cost, Data Movement, Buffering, and Zero-Copy Boundaries, Runtime Efficiency: Contention, Queueing, Batching, and Async Load** as one dependency chain, rerun the two investigations that changed your model most, and describe the current MetricRail state from an empty page. Repair incomplete work, then take a real break; consolidation is part of the course rather than unused time.

## Day 6 — Module 86: Observability: Structured Tracing, Metrics, and Diagnostic Context

**Question:** What must a running system reveal so that an operator can distinguish load, dependency delay, overload, malformed input, software defect, and expected rejection without reproducing the incident locally?

**Retrieval:** Without notes, restate the invariant carried from Module 85 — Runtime Efficiency: Contention, Queueing, Batching, and Async Load. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 86](./module-86-observability-structured-tracing-metrics-and-diagnostic-context/index.md) with a **signal dictionary** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-86-observability-structured-tracing-metrics-and-diagnostic-context/workbook.md) before observation. The day’s minimum result is: **Separate events, spans, metrics, profiles, and domain audit records by the questions they can answer.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Structured Observability Harness](../labs/module-06-structured-observability-harness/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 86 in the [MetricRail guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Separate events, spans, metrics, profiles, and domain audit records by the questions they can answer.** End with one simpler design that would be preferable under a narrower requirement.

## Day 7 — Module 87: Reliability Under Load: SLOs, Load Shedding, Retries, and Degradation

**Question:** How does the service preserve useful work and recover predictably when demand, dependency latency, error rate, or resource pressure exceeds the normal operating envelope?

**Retrieval:** Without notes, restate the invariant carried from Module 86 — Observability: Structured Tracing, Metrics, and Diagnostic Context. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 87](./module-87-reliability-under-load-slos-load-shedding-retries-and-degradation/index.md) with a **SLO and overload policy** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-87-reliability-under-load-slos-load-shedding-retries-and-degradation/workbook.md) before observation. The day’s minimum result is: **Write a service-level indicator and objective whose population, success condition, window, and exclusions are unambiguous.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Overload Control Simulator](../labs/module-07-overload-control-simulator/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 87 in the [MetricRail guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Write a service-level indicator and objective whose population, success condition, window, and exclusions are unambiguous.** End with one simpler design that would be preferable under a narrower requirement.

## Day 8 — Module 88: Security and Supply-Chain Engineering

**Question:** Which assets, trust boundaries, dependencies, build inputs, and operational capabilities could be abused, and which controls reduce that risk without relying on hidden assumptions?

**Retrieval:** Without notes, restate the invariant carried from Module 87 — Reliability Under Load: SLOs, Load Shedding, Retries, and Degradation. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 88](./module-88-security-and-supply-chain-engineering/index.md) with a **threat and dependency dossier** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-88-security-and-supply-chain-engineering/workbook.md) before observation. The day’s minimum result is: **Identify assets, actors, trust boundaries, entry points, privileges, and abuse cases for a Rust service.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Attack Surface and Supply-Chain Audit](../labs/module-08-attack-surface-and-supply-chain-audit/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 88 in the [MetricRail guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Identify assets, actors, trust boundaries, entry points, privileges, and abuse cases for a Rust service.** End with one simpler design that would be preferable under a narrower requirement.

## Day 9 — Module 89: Cargo Profiles, Binary Size, Packaging, CI, and Reproducible Releases

**Question:** How is one reviewed source state transformed into a tested, traceable, appropriately optimized artifact that can be installed and reproduced without hidden local assumptions?

**Retrieval:** Without notes, restate the invariant carried from Module 88 — Security and Supply-Chain Engineering. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 89](./module-89-cargo-profiles-binary-size-packaging-ci-and-reproducible-releases/index.md) with a **release manifest** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-89-cargo-profiles-binary-size-packaging-ci-and-reproducible-releases/workbook.md) before observation. The day’s minimum result is: **Explain how Cargo profile settings affect optimization, debug information, overflow checks, assertions, code generation, link-time optimization, panic behavior, and strip policy.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Release Matrix and Artifact Manifest](../labs/module-09-release-matrix-and-artifact-manifest/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 89 in the [MetricRail guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Explain how Cargo profile settings affect optimization, debug information, overflow checks, assertions, code generation, link-time optimization, panic behavior, and strip policy.** End with one simpler design that would be preferable under a narrower requirement.

## Day 10 — Module 90: Production Readiness, Capacity Planning, Rollouts, and Incident Learning

**Question:** What evidence is sufficient to put this system under real load, how is risk limited during rollout, and how does operational evidence change the next design?

**Retrieval:** Without notes, restate the invariant carried from Module 89 — Cargo Profiles, Binary Size, Packaging, CI, and Reproducible Releases. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 90](./module-90-production-readiness-capacity-planning-rollouts-and-incident-learning/index.md) with a **production decision record** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-90-production-readiness-capacity-planning-rollouts-and-incident-learning/workbook.md) before observation. The day’s minimum result is: **Write a production-readiness review that connects user behavior to capacity, dependencies, failure modes, observability, security, and recovery.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Production Readiness Review](../labs/module-10-production-readiness-review/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 90 in the [MetricRail guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Write a production-readiness review that connects user behavior to capacity, dependencies, failure modes, observability, security, and recovery.** End with one simpler design that would be preferable under a narrower requirement.

## Final integration

After Day 10, complete the [final review](final-review.md), run the strongest available course route, and implement this unseen capstone change: **Add one high-cardinality MetricRail query while preserving bounded memory, deterministic output, observability cardinality, overload behavior, and artifact traceability.**

Seven days later, rebuild the ten-module sequence and the core **production decision record** without the book. Write a fresh example for every relationship you cannot recover. Re-reading a solution without recreating the model does not count as retained learning.
