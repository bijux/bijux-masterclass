# Lab — Module 08 lab — Protect critical journeys under mixed-tenant overload

> **Module 08:** Traffic Shaping, Quotas, and Load Shedding

## Objective

Apply cost-weighted rate, concurrency, fairness, and shedding policy to a skewed workload while preserving accepted work and control operations.

## Why this lab matters

This lab turns the module’s governing question—**How should quotas, priorities, cost budgets, and load shedding preserve fairness and truthful 429/503 outcomes?**—into a falsifiable experiment. A rate limit controls how quickly work may arrive over a short horizon. A quota controls total consumption over a longer horizon. A concurrency limit bounds simultaneous active work. Capacity admission rejects when current downstream conditions cannot safely accept more work.

It advances the cumulative Analysis Runs Platform by requiring this result: **Implement multi-dimensional fixed-point budgets, tenant isolation, staged shedding, and rollback of partial reservations**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

- Module 6 bounded admission is active
- operation cost catalogue is versioned
- two tenant/service classes are configured
- the baseline can saturate database, worker, or stream capacity

## Hypothesis

The clean implementation should satisfy this claim: **offered/admitted/rejected/completed cost reconciles; no partial token leak occurs; tenant B retains the declared minimum service; status and cancellation remain available; accepted work is not abandoned; overload responses match policy and contract; local versus aggregate limiter scope is explicit.** When the lab introduces this fault—**the lab introduces its declared planted defect**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Run mixed traffic without traffic policy until a limiting resource saturates.
2. Add global and tenant cost buckets plus operation concurrency.
3. Verify atomic reservations with a planted partial-charge defect.
4. Offer 90% of cost from tenant A and 10% from tenant B.
5. Trigger each shedding stage by controlled resource signals.
6. Issue status and cancellation requests during maximum pressure.
7. Scale the local service to three processes and document aggregate limit behavior.

### Investigation notes

Before editing code, predict the first observable divergence caused by **the lab introduces its declared planted defect**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Apply cost-weighted rate, concurrency, fairness, and shedding policy to a skewed workload while preserving accepted work and control operations**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

- offered/admitted/rejected/completed cost reconciles
- no partial token leak occurs
- tenant B retains the declared minimum service
- status and cancellation remain available
- accepted work is not abandoned
- overload responses match policy and contract
- local versus aggregate limiter scope is explicit

## Required evidence

Create:

```text
work/module-08/
├── traffic-policy.yaml
├── cost-catalog.yaml
├── uncontrolled.json
├── controlled.json
├── fairness.json
├── shedding-stages.json
├── multi-process-scope.md
└── decision.md
```

Report both request counts and cost units. Include a table mapping each rejection reason to 429/503 behavior and retry guidance.

## Interpretation and defense

1. Which state or effect is authoritative for **Traffic Shaping, Quotas, and Load Shedding**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **the lab introduces its declared planted defect** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Clear local limiter state, disable injected saturation, drain or reset disposable work, and verify all reservations and active permits return to zero.

## Completion gate

- [ ] all control types are distinguished
- [ ] cost weights cite measurement evidence
- [ ] atomic reservation defect is rejected
- [ ] fairness under skew is demonstrated
- [ ] shedding ladder preserves critical controls
- [ ] multi-process scope is stated honestly

The lab is incomplete when the candidate is merely faster. It must preserve the inherited correctness oracle and explain the observed resource change.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Traffic Shaping, Quotas, and Load Shedding**. A green command without the negative case and causal explanation does not satisfy this gate.
