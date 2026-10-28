# Module 05 checkpoint — Runtime Profiling and Allocation Control

## Required result

- [ ] runtime vectors pass in both tracks
- [ ] unprofiled and profiled evidence are distinct
- [ ] three code/resource hypotheses are evaluated
- [ ] event-loop responsiveness is measured
- [ ] allocation scope and limitations are documented
- [ ] accepted changes preserve public output

## Defend the design

Answer without reading from the chapter:

1. Which code path owns the limiting CPU demand?
2. How do you know the operation blocked unrelated work?
3. Where did the bottleneck move after the change?

## Demonstrate

- explain the governing question: Which Python or Node.js runtime phase consumes wall time, CPU, allocations, event-loop capacity, or serialization effort?
- show one accepted case and one rejected or failed case;
- identify the authoritative owner and decisive oracle;
- state one evidence limitation.

## Commands

```bash
make module-proof MODULE=05 TRACK=${TRACK:-python}
```

## Continue only when

The module fails if response validation or security projection is bypassed, or if a profiler screenshot is presented without reproducible workload evidence.

You may not compensate for a failed correctness, identity, or reproducibility gate with a better latency number.

The module is incomplete when the result is asserted but the failure path, authoritative evidence, or cross-language invariant is missing. Retain enough evidence for another reader to reproduce the decision that profile named phases, detect blocking work, bound profiling overhead, and prove mechanism-level improvements.
