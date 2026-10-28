# Checkpoint — Module 08: Traffic Shaping, Quotas, and Load Shedding

## Required result

Implement multi-dimensional fixed-point budgets, tenant isolation, staged shedding, and rollback of partial reservations.

## Demonstrate

- explain the governing question: How should quotas, priorities, cost budgets, and load shedding preserve fairness and truthful 429/503 outcomes?
- show one accepted case and one rejected or failed case;
- identify the authoritative owner and decisive oracle;
- state one evidence limitation.

## Commands

```bash
make module-proof MODULE=08 TRACK=${TRACK:-python}
```

## Evidence to retain

Create:

```text
work/module-08/
├── traffic-policy.yaml
├── cost-catalog.yaml
├── uncontrolled.json
├── controlled.json
├── fairness.json
├── shedding-stages.json
├── multi-process-scope.md
└── decision.md
```

Report both request counts and cost units. Include a table mapping each rejection reason to 429/503 behavior and retry guidance.

## Defend the design

Answer without reading from the chapter:

1. Why is one request not one unit of capacity?
2. Which stage of your shedding ladder activates first and why?
3. What aggregate limit does your deployment actually enforce?

## Continue only when

The module fails if budget reservations leak, one tenant can monopolize protected capacity, or overload is hidden by changing successful response semantics.

You may not compensate for a failed correctness, identity, or reproducibility gate with a better latency number.

The module is incomplete when the result is asserted but the failure path, authoritative evidence, or cross-language invariant is missing. Retain enough evidence for another reader to reproduce the decision that implement multi-dimensional fixed-point budgets, tenant isolation, staged shedding, and rollback of partial reservations.
