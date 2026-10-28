# Worked Answers — Module 08: Channels, Health, Discovery, Load Balancing, and Lifecycle

Use these solutions to audit your reasoning for **Channels, Health, Discovery, Load Balancing, and Lifecycle**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why should a gRPC channel normally outlive one call?

It reuses resolution, TLS, subchannels, HTTP/2 connections, configuration, and connectivity state. Per-call channels add cost and destroy coherent lifecycle management.

**Decisive evidence:** channel lifecycle trace

The chapter’s decisive distinction is this: A gRPC channel is not one TCP connection. It is a client-side abstraction that can resolve names, maintain subchannels, reconnect, select endpoints, and multiplex calls. Creating a channel for every request discards connection reuse, increases handshakes, amplifies DNS and TLS work, and makes connectivity state impossible to manage coherently.

## 2. Differentiate liveness, readiness, and gRPC serving status.

Liveness says the process should not be restarted; readiness says it should receive new traffic; gRPC health reports serving status for the server or named service. They are related but distinct.

**Decisive evidence:** health state table

In the cumulative capstone, the rule becomes concrete: Liveness answers whether the process should be restarted. Readiness answers whether it should receive new traffic. The standard gRPC health service exposes serving status for the whole server or named services. These signals overlap but are not identical.

## 3. What does a resolver do, and what does a load-balancing policy do?

The resolver turns a target into changing endpoint addresses and authority information. The load balancer selects among usable subchannels/endpoints.

**Decisive evidence:** resolver/LB simulation

A useful way to reason about the boundary is: The channel also needs discipline. It is reused across calls, carries one target and credential policy, and owns resolver and subchannel state. Applications do not create a new channel per request or spin on READY. During A’s shutdown, the resolver and balancer select B. B must be correct because idempotency and observation state are durable or explicitly resumable.

## 4. Why can round-robin expose an in-memory idempotency defect?

Retries may reach another instance that lacks the original in-memory record, creating duplicate effects. Idempotency must be durable/shared.

**Decisive evidence:** cross-instance idempotency test

The implementation consequence is: Round-robin or pick-first policies distribute calls among available endpoints according to channel and resolver behavior. They do not make in-memory idempotency, session state, watch history, or worker assignments consistent. Any state required across calls must be durable, replicated under an explicit protocol, or affinity-bound with acknowledged limitations.

## 5. When should a server report NOT_SERVING during graceful shutdown?

Before stopping admission, while allowing already accepted calls a bounded drain period. It remains live until shutdown completes.

**Decisive evidence:** drain timeline

The important nuance is: Shutdown begins by changing readiness/health to not serving so load balancers stop new calls. The server rejects or redirects new work according to policy, stops assigning new worker jobs, and allows admitted unary calls and streams a bounded drain period. It then cancels remaining calls, releases resources, and closes.

## 6. Why is keepalive not an application lease or heartbeat?

Transport pings only test connection behavior. Lease authority is durable application state with identity, generation, and expiry.

**Decisive evidence:** keepalive/lease distinction test

Under concurrency or failure, the distinction becomes: HTTP/2 keepalive pings can detect dead connections and keep intermediaries active, but aggressive settings can create load or violate server policy. Configure client ping interval, timeout, whether pings occur without active calls, and server enforcement. Do not use keepalive as application heartbeat or lease authority.

## 7. What risk comes from synchronized maximum connection age?

Many clients reconnect simultaneously, causing DNS, TLS, and server load spikes. Add jitter and bounded grace.

**Decisive evidence:** reconnect distribution model

The design remains honest only if: Idle timeout can close unused channels to conserve resources. Maximum connection age can encourage rebalancing and certificate rotation, with a grace period for active calls. Long-lived streams need a planned reconnect path. Settings must include jitter or fleet-level coordination to avoid synchronized reconnect storms.

## 8. Why should applications not poll channel READY state before every call?

Connectivity state changes concurrently and READY does not prove method success. Make bounded calls and handle status.

**Decisive evidence:** connectivity race test

The consumer-facing consequence is: Resetting backoff manually is an operator or test action, not a normal application loop. A tight reconnect loop can overload DNS, TLS, and recovering servers. Wait-for-ready is applied per method and call according to Course 5's deadline policy.

**Evidence.** Combine proto/descriptor validation, generated surface checks, shared vectors, and a live client/server RPC scenario.

## 9. Describe shutdown behavior for an active UploadDataset stream.

Stop new uploads, allow a bounded admitted upload to finish if policy permits, otherwise cancel, clean staging content, and return a truthful terminal status.

**Decisive evidence:** upload drain cleanup test

The operational consequence is: Clients also drain. Stop accepting new application work, cancel or finish active calls according to their value, flush required telemetry within a bound, close streams, and close channels. A process exit that simply abandons in-flight mutation calls creates ambiguous outcomes and noisy retries after restart.

## 10. How should a worker stream recover after its server instance disappears?

Reconnect with bounded backoff, re-authenticate, reconcile durable assignments and current lease generations, then resume readiness—not replay socket state.

**Decisive evidence:** worker recovery trace

The strongest engineering interpretation is: At the end of the grace period, A cancels remaining calls, releases permits and file handles, flushes bounded telemetry, and stops. The client records calls whose outcomes are ambiguous and reconciles them. Worker clients reconnect, authenticate, and compare durable lease generations. No socket buffer is treated as durable work.

## 11. When is server reflection appropriate?

In development or authenticated controlled operations when dynamic discovery is useful. Disable or restrict it where schema exposure is unacceptable.

**Decisive evidence:** reflection exposure policy

The defect-oriented view is: Server reflection allows tools such as grpcurl and dynamic clients to discover services and descriptors. It is valuable in development and controlled operations, but it can expose internal method, message, and package details. Enable it according to environment and security policy, not unconditionally.

## 12. Define a two-instance proof that reveals hidden local state.

Route repeated idempotent and observation calls through two identified instances, inject instance failure, and verify outcomes remain correct from durable/shared authority.

**Decisive evidence:** two-instance report

Across the Python and TypeScript tracks, the invariant is: Two Analysis Control instances share the authoritative database. A client channel resolves both and uses round-robin. Instance A receives a long WatchRun stream and several unary calls; instance B is idle. A deployment controller asks A to stop.
