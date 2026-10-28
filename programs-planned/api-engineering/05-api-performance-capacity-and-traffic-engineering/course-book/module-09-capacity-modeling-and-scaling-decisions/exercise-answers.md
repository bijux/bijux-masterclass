# Worked Answers — Module 09: Capacity Modeling and Scaling Decisions

Use these solutions to audit your reasoning for **Capacity Modeling and Scaling Decisions**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Four cores at 50% for 120 s complete 24,000 reads. Calculate CPU demand/read.

Busy CPU is `4×0.5×120=240` core-seconds. Demand is `240/24000=0.01` core-seconds, or 10 ms per read.

The chapter’s decisive distinction is this: For CPU measured in core-seconds, capacity units are cores. For database connections, use active service demand and concurrency rather than treating a connection as CPU. For network, use bytes per second plus protocol overhead and burst behavior.

**Evidence.** Use a correctness-gated baseline/candidate comparison that attributes CPU, wall time, allocations, event-loop delay, and downstream work to one hypothesis.

## 2. At 10 ms CPU demand/read and 8 cores, what throughput corresponds to 70% target utilization?

Available busy core-seconds per second at target is `8×0.70=5.6`. Throughput is `5.6/0.01=560 reads/s`, before other resources and uncertainty.

In the cumulative capstone, the rule becomes concrete: Running at measured maximum is not a production plan. Headroom absorbs bursts, skew, maintenance, noisy neighbors, model error, and recovery work. Define target utilization per resource, such as 60–75%, from operational evidence rather than copying a universal number.

## 3. Backlog is 18,000 jobs, completion 140/s, new arrivals 100/s. Estimate drain time.

Net drain is 40 jobs/s. `18000/40=450 s`, or 7.5 minutes, assuming rates remain stable and downstream stages keep up.

A useful way to reason about the boundary is: After an outage, the system must serve new arrivals and drain backlog. If completion capacity is μ and new arrival rate is λ, net drain rate is μ - λ when positive.

**Evidence.** Compare repeated runs with the same workload hash and environment fingerprint, account for offered/started/completed/rejected/failed/missing outcomes, and report uncertainty and tail latency.

## 4. What if new arrivals rise to 150/s?

Completion 140/s is below arrivals, so backlog does not drain; it grows at 10 jobs/s. Admission or capacity must change.

The implementation consequence is: After an outage, the system must serve new arrivals and drain backlog. If completion capacity is μ and new arrival rate is λ, net drain rate is μ - λ when positive.

**Evidence.** Compare repeated runs with the same workload hash and environment fingerprint, account for offered/started/completed/rejected/failed/missing outcomes, and report uncertainty and tail latency.

## 5. Why include N-1 instance capacity?

Deployments, failures, and maintenance remove capacity. If remaining instances cannot serve critical demand, routine operations trigger overload. N-1 is a scenario, not a universal architecture rule.

The important nuance is: Failure assumptions matter. If one of three API instances may be unavailable during deployment, remaining instances must serve critical load within objectives or the release process must reduce traffic. If database failover temporarily lowers capacity, queue and shedding policies must protect durable work.

## 6. How can an index alter capacity beyond read latency?

It adds storage, buffer pressure, WAL, write CPU/I/O, vacuum/maintenance work, and migration risk. It can shift the first bottleneck from reads to writes or storage.

Under concurrency or failure, the distinction becomes: Use daily creation rate, retention, replication factor, compression, and cleanup lag. Index changes from Module 4 increase storage and write demand. Artifact ranges and caching from Modules 3 and 7 may reduce network but not stored bytes.

## 7. What does 30% headroom mean?

The planned operating load uses at most 70% of the declared resource capacity, under the stated scenario. It does not guarantee 30% throughput growth if another resource becomes limiting.

The design remains honest only if: Running at measured maximum is not a production plan. Headroom absorbs bursts, skew, maintenance, noisy neighbors, model error, and recovery work. Define target utilization per resource, such as 60–75%, from operational evidence rather than copying a universal number.

## 8. Why model workload classes separately?

Each has different CPU, DB, network, storage, and concurrency demand. Growth in mix changes resource utilization. One average request can make a rare expensive class invisible.

The consumer-facing consequence is: For CPU measured in core-seconds, capacity units are cores. For database connections, use active service demand and concurrency rather than treating a connection as CPU. For network, use bytes per second plus protocol overhead and burst behavior.

**Evidence.** Drive overload across tenants and operation costs, then inspect admission, queue delay, bounded memory, fairness, 429/503 outcomes, and recovery.

## 9. A horizontal scale step doubles API instances. What downstream fields change?

Aggregate DB pool connections, cache state or shared-cache demand, outbound sockets, telemetry volume, limiter scope, network traffic, and possibly worker claim pressure. Recompute them.

The operational consequence is: Failure assumptions matter. If one of three API instances may be unavailable during deployment, remaining instances must serve critical load within objectives or the release process must reduce traffic. If database failover temporarily lowers capacity, queue and shedding policies must protect durable work.

## 10. How should uncertainty be represented?

Use low/expected/high scenarios or ranges with source dates. Run sensitivity to identify inputs that drive the result. Avoid adding decimal precision to uncertain forecasts.

The strongest engineering interpretation is: Use daily creation rate, retention, replication factor, compression, and cleanup lag. Index changes from Module 4 increase storage and write demand. Artifact ranges and caching from Modules 3 and 7 may reduce network but not stored bytes.

**Evidence.** Use a correctness-gated baseline/candidate comparison that attributes CPU, wall time, allocations, event-loop delay, and downstream work to one hypothesis.

## 11. Compare optimization and scaling.

Optimization reduces service demand and may benefit every instance but costs engineering and can add complexity. Scaling adds capacity more directly but may not help a downstream bottleneck and raises cost. Choose from measured first bottleneck and reversibility.

The defect-oriented view is: For CPU measured in core-seconds, capacity units are cores. For database connections, use active service demand and concurrency rather than treating a connection as CPU. For network, use bytes per second plus protocol overhead and burst behavior.

## 12. Define a capacity trigger.

Example: when 15-minute p95 DB pool utilization exceeds 70% in the expected workload and list-run shared reads remain within query budget, begin the prevalidated database scale step; remeasure after deployment. It names metric, window, threshold, condition, action.

Across the Python and TypeScript tracks, the invariant is: Running at measured maximum is not a production plan. Headroom absorbs bursts, skew, maintenance, noisy neighbors, model error, and recovery work. Define target utilization per resource, such as 60–75%, from operational evidence rather than copying a universal number.
