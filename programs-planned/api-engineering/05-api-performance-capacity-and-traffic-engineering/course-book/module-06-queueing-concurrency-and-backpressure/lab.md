# Module 06 lab — Force overload and make it bounded

## Objective

Drive run submissions and artifact streams beyond service capacity, observe hidden queues, then add bounded admission and fair per-tenant control.

## Setup conditions

- Module 1 open workloads are available
- slow worker/storage modes are deterministic
- queue and permit metrics are enabled
- two tenant fixtures are configured

## Failure action and investigation


1. Run an unbounded baseline at an offered load above measured completion capacity.
2. Record queue depth, memory, wait, completion, rejection, and timeout.
3. Add active and waiter caps with acquisition deadlines.
4. Add per-tenant limits and fair ordering.
5. Repeat with tenant A generating 90% of offered work.
6. Disconnect clients before and after durable commitment.
7. Slow artifact storage and verify worker claim backpressure.



### Investigation notes

Before editing, write a one-sentence hypothesis answering: **How do arrival rate, service time, queue depth, concurrency, fairness, and backpressure determine overload behavior?** Record the first observation that contradicts the expected model. After the repair, explain why the capstone can now claim: Implement bounded admission, per-operation limits, queue accounting, permit release, and recovery after pressure. A passing command without this causal explanation is insufficient.

## Operational oracle

- unbounded baseline shows growing waiting or memory
- bounded candidate limits queue and wait
- admitted work meets a better completion/freshness profile
- rejections are documented and counted
- tenant B retains service under tenant A burst
- committed jobs survive disconnect
- permits return to zero after cleanup

## Required evidence

Create:

```text
work/module-06/
├── queue-inventory.yaml
├── unbounded.json
├── bounded.json
├── fairness.json
├── cancellation.json
├── downstream-slow.json
└── decision.md
```

Include a conservation equation for offered, admitted, rejected, completed, failed, and remaining work. State maximum implied memory for each cap.

## Cleanup and reset

Disable slow modes, cancel waiting clients, drain or reset disposable jobs, and assert active permits, waiters, and local queues are zero.

## Completion gate

- [ ] all queues have owner and capacity
- [ ] unbounded failure is reproduced
- [ ] bounded candidate preserves correctness
- [ ] fairness is demonstrated under skew
- [ ] cancellation respects durable boundary
- [ ] downstream slowdown reduces upstream claims

The lab is incomplete when the candidate is merely faster. It must preserve the inherited correctness oracle and explain the observed resource change.
