# Reference Answers — Module 06: Module 06 exercise answers — Queueing, Concurrency, and Backpressure

Read after attempting all twelve Queueing, Concurrency, and Backpressure exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Use Little’s Law for 50 completed requests/s and 0.4 s average response time.

Average work in the system is `L = 50 × 0.4 = 20` requests. This includes waiting and active work within the chosen boundary.

## 2. A queue contains 300 jobs, 20 are active, throughput is 10 jobs/s. Estimate mean time in system if stable.

`L=320`; `W=L/λ=320/10=32 s`. This assumes the population and interval are compatible and the system is stable. If depth is growing, the estimate is not a steady-state claim.

## 3. For M/M/1 with service rate 100/s and arrival 80/s, approximate response time.

`W=1/(100-80)=0.05 s`, 50 ms. This is intuition only; real service distributions and parallelism differ.

## 4. What happens to the same approximation at arrival 95/s?

`W=1/(100-95)=0.2 s`, 200 ms. A modest utilization increase causes a fourfold waiting/response estimate, illustrating the saturation knee.

## 5. Why is an asyncio semaphore insufficient as a full admission controller?

It limits active holders but can accumulate unbounded waiting tasks. A controller also needs waiter capacity, acquisition timeout, cancellation cleanup, metrics, and rejection semantics.

## 6. Calculate maximum application chunk buffers for 150 download permits, 128 KiB chunks, two buffers each.

`150 × 128 KiB × 2 = 38,400 KiB`, or 37.5 MiB. Add runtime, kernel, TLS, and proxy buffers separately.

## 7. When should a client disconnect cancel work?

Before admission or durable commitment, waiting and transient work may be cancelled. After a durable run/job transaction commits, disconnect should stop response work but preserve accepted intent. Downloads should stop reads and release permits.

## 8. Why can increasing database pool size reduce throughput?

More concurrent queries can saturate CPU, memory, I/O, and locks, increasing service time and tail latency. Total pool capacity across instances must match measured database capacity.

## 9. Design fair admission for tenants A and B.

Use a global cap plus per-tenant active/waiter caps, fair rotation or weighted policy, bounded waits, and metrics by policy class without leaking identities. Test that A’s burst cannot starve B and unused capacity can be borrowed under explicit rules.

## 10. How should queue depth affect worker claims?

Claims should consider active worker permits, lease duration, downstream storage/outbox capacity, and queue freshness. Claiming all queued jobs is not progress if downstream service cannot complete them.

## 11. Distinguish 429 and 503 in a traffic policy.

429 generally indicates the client or principal exceeded an applicable rate/quota policy; 503 indicates service-level temporary inability to handle work. The contract and policy must define exact usage. Both need truthful retry guidance.

## 12. A system has zero rejections but rising queue wait and missed SLO. Is admission healthy?

No. Zero rejection may mean overload is hidden in waiting. Admission should bound delay and reject before accepted work becomes predictably late, preserving capacity for admitted journeys.
