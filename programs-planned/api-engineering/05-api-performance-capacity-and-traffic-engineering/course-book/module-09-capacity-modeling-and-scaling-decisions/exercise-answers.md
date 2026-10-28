# Reference Answers — Module 09: Module 09 exercise answers — Capacity Modeling and Scaling Decisions

Read after attempting all twelve Capacity Modeling and Scaling Decisions exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Four cores at 50% for 120 s complete 24,000 reads. Calculate CPU demand/read.

Busy CPU is `4×0.5×120=240` core-seconds. Demand is `240/24000=0.01` core-seconds, or 10 ms per read.

## 2. At 10 ms CPU demand/read and 8 cores, what throughput corresponds to 70% target utilization?

Available busy core-seconds per second at target is `8×0.70=5.6`. Throughput is `5.6/0.01=560 reads/s`, before other resources and uncertainty.

## 3. Backlog is 18,000 jobs, completion 140/s, new arrivals 100/s. Estimate drain time.

Net drain is 40 jobs/s. `18000/40=450 s`, or 7.5 minutes, assuming rates remain stable and downstream stages keep up.

## 4. What if new arrivals rise to 150/s?

Completion 140/s is below arrivals, so backlog does not drain; it grows at 10 jobs/s. Admission or capacity must change.

## 5. Why include N-1 instance capacity?

Deployments, failures, and maintenance remove capacity. If remaining instances cannot serve critical demand, routine operations trigger overload. N-1 is a scenario, not a universal architecture rule.

## 6. How can an index alter capacity beyond read latency?

It adds storage, buffer pressure, WAL, write CPU/I/O, vacuum/maintenance work, and migration risk. It can shift the first bottleneck from reads to writes or storage.

## 7. What does 30% headroom mean?

The planned operating load uses at most 70% of the declared resource capacity, under the stated scenario. It does not guarantee 30% throughput growth if another resource becomes limiting.

## 8. Why model workload classes separately?

Each has different CPU, DB, network, storage, and concurrency demand. Growth in mix changes resource utilization. One average request can make a rare expensive class invisible.

## 9. A horizontal scale step doubles API instances. What downstream fields change?

Aggregate DB pool connections, cache state or shared-cache demand, outbound sockets, telemetry volume, limiter scope, network traffic, and possibly worker claim pressure. Recompute them.

## 10. How should uncertainty be represented?

Use low/expected/high scenarios or ranges with source dates. Run sensitivity to identify inputs that drive the result. Avoid adding decimal precision to uncertain forecasts.

## 11. Compare optimization and scaling.

Optimization reduces service demand and may benefit every instance but costs engineering and can add complexity. Scaling adds capacity more directly but may not help a downstream bottleneck and raises cost. Choose from measured first bottleneck and reversibility.

## 12. Define a capacity trigger.

Example: when 15-minute p95 DB pool utilization exceeds 70% in the expected workload and list-run shared reads remain within query budget, begin the prevalidated database scale step; remeasure after deployment. It names metric, window, threshold, condition, action.
