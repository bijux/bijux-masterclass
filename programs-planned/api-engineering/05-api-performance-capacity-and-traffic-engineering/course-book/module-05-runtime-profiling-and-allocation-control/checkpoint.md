# Checkpoint — Module 05: Runtime Profiling and Allocation Control

## Required result

Profile named phases, detect blocking work, bound profiling overhead, and prove mechanism-level improvements.

## Demonstrate

- explain the governing question: Which Python or Node.js runtime phase consumes wall time, CPU, allocations, event-loop capacity, or serialization effort?
- show one accepted case and one rejected or failed case;
- identify the authoritative owner and decisive oracle;
- state one evidence limitation.

## Commands

```bash
make module-proof MODULE=05 TRACK=${TRACK:-python}
```

## Evidence to retain

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

## Defend the design

Answer without reading from the chapter:

1. Which code path owns the limiting CPU demand?
2. How do you know the operation blocked unrelated work?
3. Where did the bottleneck move after the change?

## Continue only when

The module fails if response validation or security projection is bypassed, or if a profiler screenshot is presented without reproducible workload evidence.

You may not compensate for a failed correctness, identity, or reproducibility gate with a better latency number.

The module is incomplete when the result is asserted but the failure path, authoritative evidence, or cross-language invariant is missing. Retain enough evidence for another reader to reproduce the decision that profile named phases, detect blocking work, bound profiling overhead, and prove mechanism-level improvements.
