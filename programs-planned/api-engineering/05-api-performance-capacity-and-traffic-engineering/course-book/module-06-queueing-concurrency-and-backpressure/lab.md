# Lab — Module 06 lab — Force overload and make it bounded

> **Module 06:** Queueing, Concurrency, and Backpressure

## Objective

Drive run submissions and artifact streams beyond service capacity, observe hidden queues, then add bounded admission and fair per-tenant control.

## Why this lab matters

This lab turns the module’s governing question—**How do arrival rate, service time, queue depth, concurrency, fairness, and backpressure determine overload behavior?**—into a falsifiable experiment. A client disconnect before admission can cancel waiting. After a run submission transaction commits, disconnecting the HTTP request must not erase durable work. The API may stop waiting for a response, but the job remains.

It advances the cumulative Analysis Runs Platform by requiring this result: **Implement bounded admission, per-operation limits, queue accounting, permit release, and recovery after pressure**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

- Module 1 open workloads are available
- slow worker/storage modes are deterministic
- queue and permit metrics are enabled
- two tenant fixtures are configured

## Hypothesis

The clean implementation should satisfy this claim: **unbounded baseline shows growing waiting or memory; bounded candidate limits queue and wait; admitted work meets a better completion/freshness profile; rejections are documented and counted; tenant B retains service under tenant A burst; committed jobs survive disconnect; permits return to zero after cleanup.** When the lab introduces this fault—**Disconnect clients before and after durable commitment**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Run an unbounded baseline at an offered load above measured completion capacity.
2. Record queue depth, memory, wait, completion, rejection, and timeout.
3. Add active and waiter caps with acquisition deadlines.
4. Add per-tenant limits and fair ordering.
5. Repeat with tenant A generating 90% of offered work.
6. Disconnect clients before and after durable commitment.
7. Slow artifact storage and verify worker claim backpressure.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Disconnect clients before and after durable commitment**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Drive run submissions and artifact streams beyond service capacity, observe hidden queues, then add bounded admission and fair per-tenant control**, and identify one attractive implementation that would pass the happy path while failing the oracle.

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

## Interpretation and defense

1. Which state or effect is authoritative for **Queueing, Concurrency, and Backpressure**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Disconnect clients before and after durable commitment** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

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

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Queueing, Concurrency, and Backpressure**. A green command without the negative case and causal explanation does not satisfy this gate.
