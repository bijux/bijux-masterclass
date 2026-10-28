# Lab — Module 06: Durable Workers and Recovery

> **Module 06:** Durable Workers and Recovery

## Objective

Submit work, kill the worker after claim or partial progress, recover the expired lease, avoid duplicate artifacts, and resolve cancellation-versus-completion races deterministically.

## Why this lab matters

This lab turns the module’s governing question—**What makes a 202 Accepted operation honest after the API process or worker dies?**—into a falsifiable experiment. Implement job claim SQL and document lock, order, and lease predicates. Run API with workers stopped; submit and verify durable queued state after restart. Run multiple workers and verify distinct claims. Implement heartbeats, retry classification, attempt cap, and exponential delay. Implement generation-guarded progress and terminal transactions.

It advances the cumulative Analysis Runs Platform by requiring this result: **Add durable jobs, leases, heartbeats, fencing, cancellation, duplicate-safe effects, and abandoned-work recovery**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

The previous baseline is: **Project, dataset, and run listings are stable, owner-bound, and resistant to cursor tampering.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *What internal machinery makes `202 Accepted` honest after API or worker processes die?*

## Hypothesis

The clean implementation should satisfy this claim: **After a worker is killed, no terminal effect occurs before lease expiry; a new generation completes once, and the stale generation cannot overwrite it.** When the lab introduces this fault—**Plant a terminal update by run ID only; prove a stale worker overwrites, repair with generation fencing, and retain the process test**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. **Implement job claim SQL and document lock, order, and lease predicates.**
2. **Run API with workers stopped; submit and verify durable queued state after restart.**
3. **Run multiple workers and verify distinct claims.**
4. **Implement heartbeats, retry classification, attempt cap, and exponential delay.**
5. **Implement generation-guarded progress and terminal transactions.**
6. **Kill a worker after claim and after partial progress, then recover after expiry.**
7. **Exercise cancellation-before-completion and completion-before-cancellation races.**
8. **Plant a terminal update by run ID only; prove a stale worker overwrites, repair with generation fencing, and retain the process test.**

### Required planted defect

> Remove lease generation from terminal UPDATE and release a paused old worker after a recovered worker completes.

Preserve the following evidence:

```text
prediction:
change introduced:
minimal setup:
first failing command:
public symptom:
durable/process state:
root cause:
repair:
regression path:
remaining limitation:
```

### Investigation notes

Before editing code, predict the first observable divergence caused by **Plant a terminal update by run ID only; prove a stale worker overwrites, repair with generation fencing, and retain the process test**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Submit work, kill the worker after claim or partial progress, recover the expired lease, avoid duplicate artifacts, and resolve cancellation-versus-completion races deterministically**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

After a worker is killed, no terminal effect occurs before lease expiry; a new generation completes once, and the stale generation cannot overwrite it.

## Required evidence

- baseline transcript proving the previous checkpoint before **Durable Workers and Recovery** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Durable Workers and Recovery**
- focused result for: Separate durable acceptance from execution.
- public, durable, security, or operational observation showing: Analysis work survives restart, abandoned leases are recovered, and stale workers cannot overwrite newer results.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **durable job leasing and fencing**
- a limitation statement naming every live dependency required to support the strongest **Durable Workers and Recovery** claim but not exercised

## Interpretation and defense

1. Which state or effect is authoritative for **Durable Workers and Recovery**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Plant a terminal update by run ID only; prove a stale worker overwrites, repair with generation fencing, and retain the process test** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

1. Restore the control changed for **Durable Workers and Recovery**.
2. Remove the temporary data, faults, credentials, permits, files, or delivery state created by the **Durable Workers and Recovery** experiment.
3. Rerun the focused regression and `make module-proof MODULE=06`.
4. Confirm the system again provides this result: Analysis work survives restart, abandoned leases are recovered, and stale workers cannot overwrite newer results.

## Completion gate

- durable 202
- atomic claim
- lease recovery
- generation fencing
- short transactions
- idempotent effects
- bounded retry
- safe shutdown

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Durable Workers and Recovery**. A green command without the negative case and causal explanation does not satisfy this gate.
