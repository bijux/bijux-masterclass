# Worked answers — Channels, Health, Discovery, Load Balancing, and Lifecycle

These are reference answers, not scripts to memorize. Compare the decision rule and evidence, then revise your answer.

## 1. Why should a gRPC channel normally outlive one call?

It reuses resolution, TLS, subchannels, HTTP/2 connections, configuration, and connectivity state. Per-call channels add cost and destroy coherent lifecycle management.

**Decisive evidence:** channel lifecycle trace

## 2. Differentiate liveness, readiness, and gRPC serving status.

Liveness says the process should not be restarted; readiness says it should receive new traffic; gRPC health reports serving status for the server or named service. They are related but distinct.

**Decisive evidence:** health state table

## 3. What does a resolver do, and what does a load-balancing policy do?

The resolver turns a target into changing endpoint addresses and authority information. The load balancer selects among usable subchannels/endpoints.

**Decisive evidence:** resolver/LB simulation

## 4. Why can round-robin expose an in-memory idempotency defect?

Retries may reach another instance that lacks the original in-memory record, creating duplicate effects. Idempotency must be durable/shared.

**Decisive evidence:** cross-instance idempotency test

## 5. When should a server report NOT_SERVING during graceful shutdown?

Before stopping admission, while allowing already accepted calls a bounded drain period. It remains live until shutdown completes.

**Decisive evidence:** drain timeline

## 6. Why is keepalive not an application lease or heartbeat?

Transport pings only test connection behavior. Lease authority is durable application state with identity, generation, and expiry.

**Decisive evidence:** keepalive/lease distinction test

## 7. What risk comes from synchronized maximum connection age?

Many clients reconnect simultaneously, causing DNS, TLS, and server load spikes. Add jitter and bounded grace.

**Decisive evidence:** reconnect distribution model

## 8. Why should applications not poll channel READY state before every call?

Connectivity state changes concurrently and READY does not prove method success. Make bounded calls and handle status.

**Decisive evidence:** connectivity race test

## 9. Describe shutdown behavior for an active UploadDataset stream.

Stop new uploads, allow a bounded admitted upload to finish if policy permits, otherwise cancel, clean staging content, and return a truthful terminal status.

**Decisive evidence:** upload drain cleanup test

## 10. How should a worker stream recover after its server instance disappears?

Reconnect with bounded backoff, re-authenticate, reconcile durable assignments and current lease generations, then resume readiness—not replay socket state.

**Decisive evidence:** worker recovery trace

## 11. When is server reflection appropriate?

In development or authenticated controlled operations when dynamic discovery is useful. Disable or restrict it where schema exposure is unacceptable.

**Decisive evidence:** reflection exposure policy

## 12. Define a two-instance proof that reveals hidden local state.

Route repeated idempotent and observation calls through two identified instances, inject instance failure, and verify outcomes remain correct from durable/shared authority.

**Decisive evidence:** two-instance report
