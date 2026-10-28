# Lab — Operate two RPC instances through health transitions and graceful drain

> **Module 08:** Channels, Health, Discovery, Load Balancing, and Lifecycle

## Objective

Implement channel and server lifecycle state machines, standard health semantics, bounded reconnect behavior, two-instance routing evidence, graceful drain, and an operational service configuration.

## Why this lab matters

This lab turns the module’s governing question—**How do clients and servers manage long-lived channels, instance health, name resolution, load balancing, startup, draining, and shutdown without hiding failure or losing active work?**—into a falsifiable experiment. The lab’s two-instance trace records endpoint chosen, health phase, call admission, active calls, stream termination, reconnect delay, and authoritative result. This is more meaningful than showing that a Kubernetes pod eventually became Ready. It proves that the service lifecycle preserves RPC semantics.

It advances the cumulative Analysis Runs Platform by requiring this result: **Implement channel and server lifecycle state machines, standard health semantics, bounded reconnect behavior, two-instance routing evidence, graceful drain, and an operational service configuration**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

Start two Python reference servers on ephemeral ports with instance identifiers and shared authoritative fixture state. Use the deterministic TypeScript lifecycle model for parity cases.

## Hypothesis

The clean implementation should satisfy this claim: **New work stops entering a draining instance, admitted work either finishes or terminates within the declared bound, clients reconnect with bounded backoff, durable state remains correct across instances, and health/reflection exposure matches policy.** When the lab introduces this fault—**Implement channel and server lifecycle state machines, standard health semantics, bounded reconnect behavior, two-instance routing evidence, graceful drain, and an operational service configuration**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Create one reusable channel/client pool and route unary calls across both instances.
2. Mark one instance not serving and observe selection and call outcomes.
3. Open WatchRun and worker streams, then begin drain on the serving instance.
4. Attempt new unary and stream calls during drain.
5. Force the instance to stop after the drain bound and reconnect clients.
6. Compare runtime reflection or descriptor inventory with the checked-in catalogue when tooling is available.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Implement channel and server lifecycle state machines, standard health semantics, bounded reconnect behavior, two-instance routing evidence, graceful drain, and an operational service configuration**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Implement channel and server lifecycle state machines, standard health semantics, bounded reconnect behavior, two-instance routing evidence, graceful drain, and an operational service configuration**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

New work stops entering a draining instance, admitted work either finishes or terminates within the declared bound, clients reconnect with bounded backoff, durable state remains correct across instances, and health/reflection exposure matches policy.

## Required evidence

- `capstone/shared/vectors/lifecycle.json`
- `capstone/operations/service-config.json`
- `reports/module-08-lifecycle-proof.json`

## Interpretation and defense

1. Which state or effect is authoritative for **Channels, Health, Discovery, Load Balancing, and Lifecycle**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Implement channel and server lifecycle state machines, standard health semantics, bounded reconnect behavior, two-instance routing evidence, graceful drain, and an operational service configuration** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Close streams and channels, stop both servers, reset health state, remove ephemeral endpoint records, and confirm no background tasks remain.

## Completion gate

Channels, servers, health, reconnect, and shutdown must have bounded explicit lifecycles, and no correctness property may depend on one server's process memory.

A successful command without this evidence does not complete the lab.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Channels, Health, Discovery, Load Balancing, and Lifecycle**. A green command without the negative case and causal explanation does not satisfy this gate.
