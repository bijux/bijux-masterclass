# Lab — Module 02: Deadlines, Cancellation, and Retry Budgets

> **Module 02:** Deadlines, Cancellation, and Retry Budgets

## Objective

Add absolute deadlines, child budgets, safe retry classification, Retry-After handling, cancellation observation, and one retry owner per dependency.

## Why this lab matters

This lab turns the module’s governing question—**How is one absolute time budget propagated through retries, dependencies, and cancellation without multiplying work?**—into a falsifiable experiment. Apply Absolute deadline, Timeout scope, Cancellation to this module’s capstone increment: Add absolute deadlines, child budgets, safe retry classification, Retry-After handling, cancellation observation, and one retry owner per dependency. State one misleading green signal and the durable observation that would overrule it.

It advances the cumulative Analysis Runs Platform by requiring this result: **Implement monotonic deadlines, child budgets, safe retry classification, backoff, Retry-After handling, and cancellation**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

The previous baseline is: **The service gains a reliability case for create, submit, start, complete, retrieve, and notify journeys.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How does one request carry a finite time budget through dependencies without multiplying work or reporting success too late?*

## Hypothesis

The clean implementation should satisfy this claim: **No child exceeds parent expiry; Unsafe POST gets one attempt; Delay plus minimum attempt fits remaining time; Attempt count matches named owner policy; Committed work survives disconnect.** When the lab introduces this fault—**Plant a loop resetting timeout per attempt**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Implement absolute propagation.
2. Classify GET, idempotent update, idempotency-key POST, and unsafe POST.
3. Apply full jitter and Retry-After floor.
4. Plant a loop resetting timeout per attempt.
5. Plant a second retry owner and measure amplification.
6. Repair both and simulate disconnect after durable acceptance.

### Required planted defect

Remove or bypass the central control for **Deadlines, Cancellation, and Retry Budgets** in a temporary branch. Predict the first failing check before running it, then retain the minimized reproducer as a regression after repair.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Plant a loop resetting timeout per attempt**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Add absolute deadlines, child budgets, safe retry classification, Retry-After handling, cancellation observation, and one retry owner per dependency**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

- No child exceeds parent expiry.
- Unsafe POST gets one attempt.
- Delay plus minimum attempt fits remaining time.
- Attempt count matches named owner policy.
- Committed work survives disconnect.

## Required evidence

- baseline transcript proving the previous checkpoint before **Deadlines, Cancellation, and Retry Budgets** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Deadlines, Cancellation, and Retry Budgets**
- focused result for: Distinguish absolute deadlines from per-call timeouts.
- public, durable, security, or operational observation showing: Ingress requests, database calls, artifact operations, and webhooks share finite budgets without retry amplification.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **absolute deadline propagation**
- a limitation statement naming every live dependency required to support the strongest **Deadlines, Cancellation, and Retry Budgets** claim but not exercised

## Interpretation and defense

1. Which state or effect is authoritative for **Deadlines, Cancellation, and Retry Budgets**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Plant a loop resetting timeout per attempt** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

1. Reset fault injector.
2. Clear deterministic attempt records.
3. Retain before/after amplification report.

## Completion gate

The lab is complete only when every listed oracle passes after repair, cleanup restores the stated steady state, and `make module-proof MODULE=02` succeeds on the primary track.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Deadlines, Cancellation, and Retry Budgets**. A green command without the negative case and causal explanation does not satisfy this gate.
