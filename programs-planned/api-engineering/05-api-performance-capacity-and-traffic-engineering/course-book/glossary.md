# Glossary — API Performance, Capacity, and Traffic Engineering

These terms have precise meanings in Course 5. Use them with the program glossary at `program-book/glossary.md`, which preserves shared meanings across the complete sequence.

## latency

Elapsed time for a defined operation population, measured from a declared start point to a declared outcome.

## throughput

Useful completed work per unit time; offered requests, admitted requests, and successful completions must not be conflated.

## offered load

Demand presented by clients or a load generator whether or not the service accepts or completes it.

## admitted load

The subset of offered work accepted after authentication, policy, quotas, concurrency, and shedding decisions.

## saturation

The condition in which a limiting resource is fully utilized and additional demand primarily increases queues, rejections, or latency.

## tail latency

Latency in the slower end of a distribution, such as p95 or p99, where queueing and rare expensive paths become visible.

## coordinated omission

A measurement error in which a closed generator waits for slow responses and therefore fails to record requests that should have arrived during the delay.

## warmup

A pre-measurement period used to reach the intended runtime state, caches, pools, and code paths before collecting comparable data.

## steady state

A bounded interval during which workload and important resource behavior are sufficiently stable for the intended comparison.

## quantile

A value below which a stated fraction of observations falls under a specified quantile algorithm.

## confidence interval

A range produced by a stated statistical procedure to express uncertainty in an estimate; it does not guarantee truth for one environment.

## query plan

The database optimizer’s chosen access and join strategy, inspected with actual row and buffer evidence rather than cost numbers alone.

## selectivity

The fraction of rows expected to satisfy a predicate, which strongly influences whether an index is useful.

## connection budget

The maximum safe sum of database connections across replicas, workers, tools, and administrative reserves.

## backpressure

A mechanism that slows, blocks, bounds, or rejects upstream work when downstream capacity is unavailable.

## single-flight

A cache-fill pattern in which concurrent requests for the same missing key share one in-flight computation.

## load shedding

Deliberate rejection of lower-priority or excess work before saturation causes uncontrolled failure of all work.

## capacity model

An explicit relationship among workload demand, service demand, resource limits, queue growth, headroom, and uncertainty.

## headroom

Reserved capacity between expected demand and a resource limit to absorb variation, failure, growth, and recovery work.

## regression gate

A release decision that compares a candidate with an accepted baseline under matching identity, correctness, and evidence conditions.
