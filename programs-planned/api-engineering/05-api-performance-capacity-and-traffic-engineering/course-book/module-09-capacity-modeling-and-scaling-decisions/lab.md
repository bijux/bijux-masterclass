# Lab — Module 09 lab — Build a capacity model and predict the first bottleneck

> **Module 09:** Capacity Modeling and Scaling Decisions

## Objective

Use measured service demand for six workloads to model expected, high-growth, and degraded scenarios, then validate one prediction with controlled load.

## Why this lab matters

This lab turns the module’s governing question—**What capacity does the current system have, what uncertainty surrounds it, and which resource becomes the first bottleneck as demand grows?**—into a falsifiable experiment. For CPU measured in core-seconds, capacity units are cores. For database connections, use active service demand and concurrency rather than treating a connection as CPU. For network, use bytes per second plus protocol overhead and burst behavior.

It advances the cumulative Analysis Runs Platform by requiring this result: **Model CPU, connections, workers, queues, storage, egress, cost, headroom, and scaling decisions**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

- accepted results from Modules 3–8 are available
- workload mix and data-growth assumptions have sources/dates
- resource capacities and target utilizations are declared
- cost inputs are labeled estimates or actuals

## Hypothesis

The clean implementation should satisfy this claim: **all resource arithmetic has units; workload classes remain separate; normal and degraded headroom are reported; backlog drains only when completion exceeds arrivals; first bottleneck follows the model inputs; validation run is labeled by evidence class; decision includes uncertainty and cost.** When the lab introduces this fault—**the lab introduces its declared planted defect**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Calculate CPU, database, network, storage, and worker demand per workload.
2. Build expected, high-growth/high-payload, and N-1/degraded scenarios.
3. Compute utilization/headroom and identify first bottleneck.
4. Calculate job and webhook backlog drain after a 15-minute outage.
5. Compare optimize, vertical scale, horizontal scale, and shape-demand options.
6. Run one controlled workload near a predicted point.
7. Compare predicted and measured utilization; calibrate if necessary.
8. Write trigger metrics for the chosen staged action.

### Investigation notes

Before editing code, predict the first observable divergence caused by **the lab introduces its declared planted defect**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Use measured service demand for six workloads to model expected, high-growth, and degraded scenarios, then validate one prediction with controlled load**, and identify one attractive implementation that would pass the happy path while failing the oracle.

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

## Interpretation and defense

1. Which state or effect is authoritative for **Capacity Modeling and Scaling Decisions**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **the lab introduces its declared planted defect** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

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

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Capacity Modeling and Scaling Decisions**. A green command without the negative case and causal explanation does not satisfy this gate.
