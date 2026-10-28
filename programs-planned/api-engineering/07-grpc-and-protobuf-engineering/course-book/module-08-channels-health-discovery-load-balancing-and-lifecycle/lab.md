# Lab — Operate two RPC instances through health transitions and graceful drain

**Module:** Channels, Health, Discovery, Load Balancing, and Lifecycle

## Objective

Implement channel and server lifecycle state machines, standard health semantics, bounded reconnect behavior, two-instance routing evidence, graceful drain, and an operational service configuration.

## Setup

Start two Python reference servers on ephemeral ports with instance identifiers and shared authoritative fixture state. Use the deterministic TypeScript lifecycle model for parity cases.

## Controlled actions

1. Create one reusable channel/client pool and route unary calls across both instances.
2. Mark one instance not serving and observe selection and call outcomes.
3. Open WatchRun and worker streams, then begin drain on the serving instance.
4. Attempt new unary and stream calls during drain.
5. Force the instance to stop after the drain bound and reconnect clients.
6. Compare runtime reflection or descriptor inventory with the checked-in catalogue when tooling is available.

## Correctness oracle

New work stops entering a draining instance, admitted work either finishes or terminates within the declared bound, clients reconnect with bounded backoff, durable state remains correct across instances, and health/reflection exposure matches policy.

## Required evidence

- `capstone/shared/vectors/lifecycle.json`
- `capstone/operations/service-config.json`
- `reports/module-08-lifecycle-proof.json`

## Cleanup

Close streams and channels, stop both servers, reset health state, remove ephemeral endpoint records, and confirm no background tasks remain.

## Completion gate

Channels, servers, health, reconnect, and shutdown must have bounded explicit lifecycles, and no correctness property may depend on one server's process memory.

A successful command without this evidence does not complete the lab.
