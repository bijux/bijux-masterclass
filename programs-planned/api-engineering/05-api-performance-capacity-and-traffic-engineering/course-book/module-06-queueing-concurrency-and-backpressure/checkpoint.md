# Module 06 checkpoint — Queueing, Concurrency, and Backpressure

## Required result

- [ ] queueing and admission vectors pass in both tracks
- [ ] Little’s Law calculations use named units and intervals
- [ ] active and waiting work are bounded
- [ ] permit leak tests pass
- [ ] fairness evidence exists
- [ ] overload responses match the inherited contract

## Defend the design

Answer without reading from the chapter:

1. Which queue grew first and why?
2. What does Little’s Law say about your measured work in system?
3. How does your admission policy protect already accepted work?

## Demonstrate

- explain the governing question: How do arrival rate, service time, queue depth, concurrency, fairness, and backpressure determine overload behavior?
- show one accepted case and one rejected or failed case;
- identify the authoritative owner and decisive oracle;
- state one evidence limitation.

## Commands

```bash
make module-proof MODULE=06 TRACK=${TRACK:-python}
```

## Continue only when

The module fails if overload is hidden in an unbounded wait queue, if permits leak, or if committed work is cancelled on client disconnect.

You may not compensate for a failed correctness, identity, or reproducibility gate with a better latency number.

The module is incomplete when the result is asserted but the failure path, authoritative evidence, or cross-language invariant is missing. Retain enough evidence for another reader to reproduce the decision that implement bounded admission, per-operation limits, queue accounting, permit release, and recovery after pressure.
