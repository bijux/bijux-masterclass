# Module 05 lab — Prove three runtime bottlenecks and reject one false one

## Objective

Profile list serialization, artifact preparation, and a blocking path in both runtimes; implement only changes supported by workload evidence.

## Setup conditions

- Module 2 benchmark envelopes are reproducible
- representative run pages and artifact fixtures are available
- unprofiled baseline is recorded
- profiling output directory is outside timed paths

## Failure action and investigation


1. Record wall and CPU time for list serialization at three page sizes.
2. Capture a Python cProfile and allocation snapshot, or Node CPU profile and event-loop metrics.
3. Inject a synchronous blocking operation into the async request path.
4. Measure lightweight request delay during that operation.
5. Form three bottleneck hypotheses and one deliberately false hypothesis.
6. Implement bounded changes for supported hypotheses.
7. Rerun focused and mixed critical workloads.



### Investigation notes

Before editing, write a one-sentence hypothesis answering: **Which Python or Node.js runtime phase consumes wall time, CPU, allocations, event-loop capacity, or serialization effort?** Record the first observation that contradicts the expected model. After the repair, explain why the capstone can now claim: Profile named phases, detect blocking work, bound profiling overhead, and prove mechanism-level improvements. A passing command without this causal explanation is insufficient.

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
