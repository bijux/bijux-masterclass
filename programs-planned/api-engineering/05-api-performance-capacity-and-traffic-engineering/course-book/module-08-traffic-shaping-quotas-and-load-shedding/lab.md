# Module 08 lab — Protect critical journeys under mixed-tenant overload

## Objective

Apply cost-weighted rate, concurrency, fairness, and shedding policy to a skewed workload while preserving accepted work and control operations.

## Setup conditions

- Module 6 bounded admission is active
- operation cost catalogue is versioned
- two tenant/service classes are configured
- the baseline can saturate database, worker, or stream capacity

## Failure action and investigation


1. Run mixed traffic without traffic policy until a limiting resource saturates.
2. Add global and tenant cost buckets plus operation concurrency.
3. Verify atomic reservations with a planted partial-charge defect.
4. Offer 90% of cost from tenant A and 10% from tenant B.
5. Trigger each shedding stage by controlled resource signals.
6. Issue status and cancellation requests during maximum pressure.
7. Scale the local service to three processes and document aggregate limit behavior.



### Investigation notes

Before editing, write a one-sentence hypothesis answering: **How should quotas, priorities, cost budgets, and load shedding preserve fairness and truthful 429/503 outcomes?** Record the first observation that contradicts the expected model. After the repair, explain why the capstone can now claim: Implement multi-dimensional fixed-point budgets, tenant isolation, staged shedding, and rollback of partial reservations. A passing command without this causal explanation is insufficient.

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
