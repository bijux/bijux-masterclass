# Worked Answers — Module 06: Queueing, Concurrency, and Backpressure

Use these solutions to audit your reasoning for **Queueing, Concurrency, and Backpressure**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Use Little’s Law for 50 completed requests/s and 0.4 s average response time.

Average work in the system is `L = 50 × 0.4 = 20` requests. This includes waiting and active work within the chosen boundary.

The chapter’s decisive distinction is this: If a worker plane completes 20 jobs/s and jobs spend an average of 5 s from admission to completion, about 100 jobs are in the system on average. If the measured queue plus active jobs is 500, either the interval is not stable, the populations differ, or the time estimate is wrong.

## 2. A queue contains 300 jobs, 20 are active, throughput is 10 jobs/s. Estimate mean time in system if stable.

`L=320`; `W=L/λ=320/10=32 s`. This assumes the population and interval are compatible and the system is stable. If depth is growing, the estimate is not a steady-state claim.

In the cumulative capstone, the rule becomes concrete: If artifact storage slows, workers may finish computation but block publication. Claiming more jobs increases memory and lease pressure. Worker claim rate should respond to active work and downstream capacity, not simply queue depth.

## 3. For M/M/1 with service rate 100/s and arrival 80/s, approximate response time.

`W=1/(100-80)=0.05 s`, 50 ms. This is intuition only; real service distributions and parallelism differ.

A useful way to reason about the boundary is: Service time at a stage is time actively receiving service there. Waiting time is time queued before service. Response time for a journey includes both across stages. Service demand is resource time consumed per completed unit, such as CPU-seconds per request or database-seconds per query.

## 4. What happens to the same approximation at arrival 95/s?

`W=1/(100-95)=0.2 s`, 200 ms. A modest utilization increase causes a fourfold waiting/response estimate, illustrating the saturation knee.

The implementation consequence is: The practical objective is headroom. A resource at 95% average utilization may have no capacity for bursts, skew, maintenance, or failure. Tail latency and queue depth reveal the knee more reliably than average utilization alone.

**Evidence.** Compare repeated runs with the same workload hash and environment fingerprint, account for offered/started/completed/rejected/failed/missing outcomes, and report uncertainty and tail latency.

## 5. Why is an asyncio semaphore insufficient as a full admission controller?

It limits active holders but can accumulate unbounded waiting tasks. A controller also needs waiter capacity, acquisition timeout, cancellation cleanup, metrics, and rejection semantics.

The important nuance is: A client disconnect before admission can cancel waiting. After a run submission transaction commits, disconnecting the HTTP request must not erase durable work. The API may stop waiting for a response, but the job remains.

**Evidence.** Drive overload across tenants and operation costs, then inspect admission, queue delay, bounded memory, fairness, 429/503 outcomes, and recovery.

## 6. Calculate maximum application chunk buffers for 150 download permits, 128 KiB chunks, two buffers each.

`150 × 128 KiB × 2 = 38,400 KiB`, or 37.5 MiB. Add runtime, kernel, TLS, and proxy buffers separately.

Under concurrency or failure, the distinction becomes: where μ is service rate and λ < μ. Real API systems are not M/M/1: arrivals, service times, multiple servers, priorities, and retries differ. Use the formula to build intuition, not to publish exact predictions.

**Evidence.** Use a correctness-gated baseline/candidate comparison that attributes CPU, wall time, allocations, event-loop delay, and downstream work to one hypothesis.

## 7. When should a client disconnect cancel work?

Before admission or durable commitment, waiting and transient work may be cancelled. After a durable run/job transaction commits, disconnect should stop response work but preserve accepted intent. Downloads should stop reads and release permits.

The design remains honest only if: A client disconnect before admission can cancel waiting. After a run submission transaction commits, disconnecting the HTTP request must not erase durable work. The API may stop waiting for a response, but the job remains.

## 8. Why can increasing database pool size reduce throughput?

More concurrent queries can saturate CPU, memory, I/O, and locks, increasing service time and tail latency. Total pool capacity across instances must match measured database capacity.

The consumer-facing consequence is: Service time at a stage is time actively receiving service there. Waiting time is time queued before service. Response time for a journey includes both across stages. Service demand is resource time consumed per completed unit, such as CPU-seconds per request or database-seconds per query.

## 9. Design fair admission for tenants A and B.

Use a global cap plus per-tenant active/waiter caps, fair rotation or weighted policy, bounded waits, and metrics by policy class without leaking identities. Test that A’s burst cannot starve B and unused capacity can be borrowed under explicit rules.

The operational consequence is: Overload is not an internal 500. The service should reject before partial effects and use documented 429 or 503 behavior according to policy. Retry-After must align with the system’s actual recovery model; a precise value invented without capacity evidence can amplify retries.

## 10. How should queue depth affect worker claims?

Claims should consider active worker permits, lease duration, downstream storage/outbox capacity, and queue freshness. Claiming all queued jobs is not progress if downstream service cannot complete them.

The strongest engineering interpretation is: If artifact storage slows, workers may finish computation but block publication. Claiming more jobs increases memory and lease pressure. Worker claim rate should respond to active work and downstream capacity, not simply queue depth.

**Evidence.** Drive overload across tenants and operation costs, then inspect admission, queue delay, bounded memory, fairness, 429/503 outcomes, and recovery.

## 11. Distinguish 429 and 503 in a traffic policy.

429 generally indicates the client or principal exceeded an applicable rate/quota policy; 503 indicates service-level temporary inability to handle work. The contract and policy must define exact usage. Both need truthful retry guidance.

The defect-oriented view is: Overload is not an internal 500. The service should reject before partial effects and use documented 429 or 503 behavior according to policy. Retry-After must align with the system’s actual recovery model; a precise value invented without capacity evidence can amplify retries.

## 12. A system has zero rejections but rising queue wait and missed SLO. Is admission healthy?

No. Zero rejection may mean overload is hidden in waiting. Admission should bound delay and reject before accepted work becomes predictably late, preserving capacity for admitted journeys.

Across the Python and TypeScript tracks, the invariant is: If a worker plane completes 20 jobs/s and jobs spend an average of 5 s from admission to completion, about 100 jobs are in the system on average. If the measured queue plus active jobs is 500, either the interval is not stable, the populations differ, or the time estimate is wrong.
