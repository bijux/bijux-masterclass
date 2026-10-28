# Module 09 checkpoint — Capacity Modeling and Scaling Decisions

## Required result

- [ ] capacity vectors pass in both tracks
- [ ] three scenarios validate
- [ ] resource units and Decimal scale are explicit
- [ ] downstream effects of scale are included
- [ ] cost per useful outcome is reported
- [ ] model limitations and remeasurement triggers are documented

## Defend the design

Answer without reading from the chapter:

1. Which resource limits the expected scenario?
2. Why would adding API instances help or hurt?
3. What input uncertainty is most important to measure next?

## Demonstrate

- explain the governing question: What capacity does the current system have, what uncertainty surrounds it, and which resource becomes the first bottleneck as demand grows?
- show one accepted case and one rejected or failed case;
- identify the authoritative owner and decisive oracle;
- state one evidence limitation.

## Commands

```bash
make module-proof MODULE=09 TRACK=${TRACK:-python}
```

## Continue only when

The module fails if capacity is expressed as an unconditioned RPS number, ignores degraded operation, or assumes a backlog drains when completion does not exceed arrivals.

You may not compensate for a failed correctness, identity, or reproducibility gate with a better latency number.

The module is incomplete when the result is asserted but the failure path, authoritative evidence, or cross-language invariant is missing. Retain enough evidence for another reader to reproduce the decision that model CPU, connections, workers, queues, storage, egress, cost, headroom, and scaling decisions.
