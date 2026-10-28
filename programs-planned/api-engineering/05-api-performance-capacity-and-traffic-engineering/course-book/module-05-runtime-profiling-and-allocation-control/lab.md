# Lab — Module 05 lab — Prove three runtime bottlenecks and reject one false one

> **Module 05:** Runtime Profiling and Allocation Control

## Objective

Profile list serialization, artifact preparation, and a blocking path in both runtimes; implement only changes supported by workload evidence.

## Why this lab matters

This lab turns the module’s governing question—**Which Python or Node.js runtime phase consumes wall time, CPU, allocations, event-loop capacity, or serialization effort?**—into a falsifiable experiment. Choose the least intrusive tool that answers the question. Profile a representative workload, not a contrived one-line function unless isolating a mechanism. Run an unprofiled baseline because profiler overhead can change scheduling and cache behavior.

It advances the cumulative Analysis Runs Platform by requiring this result: **Profile named phases, detect blocking work, bound profiling overhead, and prove mechanism-level improvements**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

- Module 2 benchmark envelopes are reproducible
- representative run pages and artifact fixtures are available
- unprofiled baseline is recorded
- profiling output directory is outside timed paths

## Hypothesis

The clean implementation should satisfy this claim: **profile points to the claimed code or wait boundary; unrelated request delay exposes event-loop blocking; public response semantics remain equivalent; allocation and CPU reports state their scope; false hypothesis is rejected by evidence; mixed workload identifies any moved bottleneck.** When the lab introduces this fault—**Inject a synchronous blocking operation into the async request path**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Record wall and CPU time for list serialization at three page sizes.
2. Capture a Python cProfile and allocation snapshot, or Node CPU profile and event-loop metrics.
3. Inject a synchronous blocking operation into the async request path.
4. Measure lightweight request delay during that operation.
5. Form three bottleneck hypotheses and one deliberately false hypothesis.
6. Implement bounded changes for supported hypotheses.
7. Rerun focused and mixed critical workloads.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Inject a synchronous blocking operation into the async request path**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Profile list serialization, artifact preparation, and a blocking path in both runtimes; implement only changes supported by workload evidence**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

- profile points to the claimed code or wait boundary
- unrelated request delay exposes event-loop blocking
- public response semantics remain equivalent
- allocation and CPU reports state their scope
- false hypothesis is rejected by evidence
- mixed workload identifies any moved bottleneck

## Required evidence

Create:

```text
work/module-05/
├── hypotheses.md
├── unprofiled-baseline.json
├── cpu-profile/
├── allocation-or-event-loop.json
├── blocking-experiment.json
├── candidate.json
└── decision.md
```

For each accepted change, include the profiler observation, code change, focused result, mixed-workload result, and trade-off. Do not submit only screenshots.

## Interpretation and defense

1. Which state or effect is authoritative for **Runtime Profiling and Allocation Control**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Inject a synchronous blocking operation into the async request path** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Disable injected blocking, close profile sessions, remove large transient profiles not needed for evidence, and verify default worker/executor limits are restored.

## Completion gate

- [ ] wall and CPU time are separated
- [ ] profile overhead boundary is stated
- [ ] blocking impact on unrelated work is measured
- [ ] output conformance passes
- [ ] at least one false optimization hypothesis is rejected
- [ ] mixed workload is rerun after each accepted change

The lab is incomplete when the candidate is merely faster. It must preserve the inherited correctness oracle and explain the observed resource change.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Runtime Profiling and Allocation Control**. A green command without the negative case and causal explanation does not satisfy this gate.
