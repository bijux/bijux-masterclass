# Checkpoint — Module 09: Capacity Modeling and Scaling Decisions

## Required result

Model CPU, connections, workers, queues, storage, egress, cost, headroom, and scaling decisions.

## Demonstrate

- explain the governing question: What capacity does the current system have, what uncertainty surrounds it, and which resource becomes the first bottleneck as demand grows?
- show one accepted case and one rejected or failed case;
- identify the authoritative owner and decisive oracle;
- state one evidence limitation.

## Commands

```bash
make module-proof MODULE=09 TRACK=${TRACK:-python}
```

## Evidence to retain

Create:

```text
work/module-09/
├── assumptions.yaml
├── service-demand.json
├── expected-scenario.json
├── high-scenario.json
├── degraded-scenario.json
├── drain-model.json
├── validation-run.json
├── options.md
└── capacity-decision.md
```

Include a sensitivity table showing which input changes the first bottleneck or required scale step. Record the source date for each forecast.

## Defend the design

Answer without reading from the chapter:

1. Which resource limits the expected scenario?
2. Why would adding API instances help or hurt?
3. What input uncertainty is most important to measure next?

## Continue only when

The module fails if capacity is expressed as an unconditioned RPS number, ignores degraded operation, or assumes a backlog drains when completion does not exceed arrivals.

You may not compensate for a failed correctness, identity, or reproducibility gate with a better latency number.

The module is incomplete when the result is asserted but the failure path, authoritative evidence, or cross-language invariant is missing. Retain enough evidence for another reader to reproduce the decision that model CPU, connections, workers, queues, storage, egress, cost, headroom, and scaling decisions.
