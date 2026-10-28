# Lab — Module 08: Transactional Outbox and Webhook Delivery

> **Module 08:** Transactional Outbox and Webhook Delivery

## Objective

Complete a run, atomically create its event/outbox record, survive receiver failure and dispatcher restart, verify HMAC signatures, deliver duplicates safely, and reject forbidden destinations.

## Why this lab matters

This lab turns the module’s governing question—**How can a committed business change reliably produce an external webhook without a dual write?**—into a falsifiable experiment. Implement terminal run/event/artifact/outbox atomic transaction. Implement outbox expansion into callback and subscription deliveries. Implement delivery claim, lease generation, bounded retry, and attempt recording. Implement serialize-once HMAC signing in the primary track. Run shared signature vectors against both tracks and receiver. Use receiver fail first, forced 4xx/5xx, duplicate, stale, and changed-body cases.

It advances the cumulative Analysis Runs Platform by requiring this result: **Add a transactional outbox, signed deliveries, retry state, deduplication, and destination constraints**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

The previous baseline is: **Dataset upload and artifact download are bounded, checksummed, atomic, and resumably observable.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How can a committed domain outcome produce an external notification without losing intent or duplicating effects unpredictably?*

## Hypothesis

The clean implementation should satisfy this claim: **If the terminal run transaction commits, exactly one logical outbox event exists; network failure may delay delivery but cannot erase or invent the domain event.** When the lab introduces this fault—**Plant direct send-after-commit without outbox, demonstrate lost notification on kill, repair, and retain the process proof**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. **Implement terminal run/event/artifact/outbox atomic transaction.**
2. **Implement outbox expansion into callback and subscription deliveries.**
3. **Implement delivery claim, lease generation, bounded retry, and attempt recording.**
4. **Implement serialize-once HMAC signing in the primary track.**
5. **Run shared signature vectors against both tracks and receiver.**
6. **Use receiver `fail_first`, forced 4xx/5xx, duplicate, stale, and changed-body cases.**
7. **Kill between commit and send, restart dispatcher, and prove eventual delivery.**
8. **Plant direct send-after-commit without outbox, demonstrate lost notification on kill, repair, and retain the process proof.**

### Required planted defect

> Remove the outbox insert and send only after commit; kill the process in the gap and prove the receiver never learns about the completed run.

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

Before editing code, predict the first observable divergence caused by **Plant direct send-after-commit without outbox, demonstrate lost notification on kill, repair, and retain the process proof**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Complete a run, atomically create its event/outbox record, survive receiver failure and dispatcher restart, verify HMAC signatures, deliver duplicates safely, and reject forbidden destinations**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

If the terminal run transaction commits, exactly one logical outbox event exists; network failure may delay delivery but cannot erase or invent the domain event.

## Required evidence

- baseline transcript proving the previous checkpoint before **Transactional Outbox and Webhook Delivery** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Transactional Outbox and Webhook Delivery**
- focused result for: Explain the dual-write failure.
- public, durable, security, or operational observation showing: Run completion and webhook intent cannot diverge; duplicate delivery is detectable and safe.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **transactional outbox delivery**
- a limitation statement naming every live dependency required to support the strongest **Transactional Outbox and Webhook Delivery** claim but not exercised

## Interpretation and defense

1. Which state or effect is authoritative for **Transactional Outbox and Webhook Delivery**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Plant direct send-after-commit without outbox, demonstrate lost notification on kill, repair, and retain the process proof** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

1. Restore the control changed for **Transactional Outbox and Webhook Delivery**.
2. Remove the temporary data, faults, credentials, permits, files, or delivery state created by the **Transactional Outbox and Webhook Delivery** experiment.
3. Rerun the focused regression and `make module-proof MODULE=08`.
4. Confirm the system again provides this result: Run completion and webhook intent cannot diverge; duplicate delivery is detectable and safe.

## Completion gate

- atomic outbox
- durable after crash
- stable event identity
- signed exact bytes
- freshness enforced
- receiver dedup
- bounded classified retry
- destination policy

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Transactional Outbox and Webhook Delivery**. A green command without the negative case and causal explanation does not satisfy this gate.
