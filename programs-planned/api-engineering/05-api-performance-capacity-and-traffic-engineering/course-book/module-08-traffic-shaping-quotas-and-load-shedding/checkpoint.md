# Module 08 checkpoint — Traffic Shaping, Quotas, and Load Shedding

## Required result

- [ ] traffic vectors pass in both tracks
- [ ] policy profile validates
- [ ] cost, rate, concurrency, and quota dimensions are explicit
- [ ] limiter state is bounded
- [ ] fairness and retry behavior are tested
- [ ] overload preserves inherited correctness

## Defend the design

Answer without reading from the chapter:

1. Why is one request not one unit of capacity?
2. Which stage of your shedding ladder activates first and why?
3. What aggregate limit does your deployment actually enforce?

## Demonstrate

- explain the governing question: How should quotas, priorities, cost budgets, and load shedding preserve fairness and truthful 429/503 outcomes?
- show one accepted case and one rejected or failed case;
- identify the authoritative owner and decisive oracle;
- state one evidence limitation.

## Commands

```bash
make module-proof MODULE=08 TRACK=${TRACK:-python}
```

## Continue only when

The module fails if budget reservations leak, one tenant can monopolize protected capacity, or overload is hidden by changing successful response semantics.

You may not compensate for a failed correctness, identity, or reproducibility gate with a better latency number.

The module is incomplete when the result is asserted but the failure path, authoritative evidence, or cross-language invariant is missing. Retain enough evidence for another reader to reproduce the decision that implement multi-dimensional fixed-point budgets, tenant isolation, staged shedding, and rollback of partial reservations.
