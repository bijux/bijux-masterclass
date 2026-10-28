# Module 09 lab — Build a capacity model and predict the first bottleneck

## Objective

Use measured service demand for six workloads to model expected, high-growth, and degraded scenarios, then validate one prediction with controlled load.

## Setup conditions

- accepted results from Modules 3–8 are available
- workload mix and data-growth assumptions have sources/dates
- resource capacities and target utilizations are declared
- cost inputs are labeled estimates or actuals

## Failure action and investigation


1. Calculate CPU, database, network, storage, and worker demand per workload.
2. Build expected, high-growth/high-payload, and N-1/degraded scenarios.
3. Compute utilization/headroom and identify first bottleneck.
4. Calculate job and webhook backlog drain after a 15-minute outage.
5. Compare optimize, vertical scale, horizontal scale, and shape-demand options.
6. Run one controlled workload near a predicted point.
7. Compare predicted and measured utilization; calibrate if necessary.
8. Write trigger metrics for the chosen staged action.



### Investigation notes

Before editing, write a one-sentence hypothesis answering: **What capacity does the current system have, what uncertainty surrounds it, and which resource becomes the first bottleneck as demand grows?** Record the first observation that contradicts the expected model. After the repair, explain why the capstone can now claim: Model CPU, connections, workers, queues, storage, egress, cost, headroom, and scaling decisions. A passing command without this causal explanation is insufficient.

## Operational oracle

- all resource arithmetic has units
- workload classes remain separate
- normal and degraded headroom are reported
- backlog drains only when completion exceeds arrivals
- first bottleneck follows the model inputs
- validation run is labeled by evidence class
- decision includes uncertainty and cost

## Required evidence

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

## Cleanup and reset

Stop controlled load, restore normal process and pool configuration, and preserve the model and validation envelopes. Remove only transient generated data.

## Completion gate

- [ ] capacity statements are conditioned
- [ ] service demand derives from measurements
- [ ] headroom and degraded capacity are explicit
- [ ] backlog recovery is feasible or admission action is named
- [ ] first bottleneck is identified
- [ ] one model point is calibrated
- [ ] decision has triggers and reversibility

The lab is incomplete when the candidate is merely faster. It must preserve the inherited correctness oracle and explain the observed resource change.
