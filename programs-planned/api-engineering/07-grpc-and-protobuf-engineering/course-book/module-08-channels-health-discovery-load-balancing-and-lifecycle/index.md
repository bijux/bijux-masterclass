# Module 08 — Channels, Health, Discovery, Load Balancing, and Lifecycle

> **Program stage:** Course 7 of 10 — Engineer typed internal invocation and streaming.

> **Central question:** How do clients and servers manage long-lived channels, instance health, name resolution, load balancing, startup, draining, and shutdown without hiding failure or losing active work?

## Where this module fits

Module 07 produced **Implement RPC security profile 1.0 with method policy, workload and user identity binding, tenant-isolation vectors, mTLS-ready configuration, and secure worker-stream authorization**. This module extends that result by asking: **How do clients and servers manage long-lived channels, instance health, name resolution, load balancing, startup, draining, and shutdown without hiding failure or losing active work?**

The new capstone increment is **Implement channel and server lifecycle state machines, standard health semantics, bounded reconnect behavior, two-instance routing evidence, graceful drain, and an operational service configuration**. It becomes the prerequisite for **Generation, Testing, Reflection, and Schema Governance**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Treat channels as long-lived managed resources rather than create-per-call sockets.
- Separate process liveness, service readiness, and standard gRPC health status.
- Reason about name resolution, endpoint changes, load-balancing policy, and connection backoff.
- Configure keepalive, idle behavior, maximum connection age, and wait-for-ready safely.
- Drain unary and streaming RPCs during graceful shutdown.
- Expose reflection and diagnostics according to environment and authorization policy.

## Capstone increment

Implement channel and server lifecycle state machines, standard health semantics, bounded reconnect behavior, two-instance routing evidence, graceful drain, and an operational service configuration.

## A channel is a managed relationship

A gRPC channel is not one TCP connection. It is a client-side abstraction that can resolve names, maintain subchannels, reconnect, select endpoints, and multiplex calls. Creating a channel for every request discards connection reuse, increases handshakes, amplifies DNS and TLS work, and makes connectivity state impossible to manage coherently.

Create channels at an application composition boundary, reuse them, and close them during shutdown. Configure credentials, target, service configuration, message limits, keepalive policy, and interceptors once. If different audiences or authorities require different credentials, use distinct channel pools; do not mutate authorization state on a globally shared client.

Measure channel state transitions and call outcomes without treating `READY` as proof that the application is healthy. A ready transport can reach a server that will reject or fail the method.

## Liveness, readiness, and gRPC health

Liveness answers whether the process should be restarted. Readiness answers whether it should receive new traffic. The standard gRPC health service exposes serving status for the whole server or named services. These signals overlap but are not identical.

A server can be live but not ready while migrations, required dependencies, or recovery checks are incomplete. During drain it remains live, reports not serving for new traffic, and allows admitted calls to finish within a bound. An optional diagnostic method may expose more detail to authorized operators; public health should remain bounded and non-sensitive.

Health checks must not execute expensive deep dependency tests on every probe. Use cached state derived from lifecycle and bounded background checks. A database transient should influence readiness according to whether methods can serve truthfully, not automatically kill the process.

## Name resolution and service discovery

A channel target is interpreted by a resolver. DNS, static endpoints, xDS, and custom resolvers have different update and authority semantics. Document the supported scheme and expected service identity. A bare host string that works locally is not a complete discovery strategy.

Resolution returns candidate addresses; load balancing chooses among ready subchannels. Endpoint churn, negative DNS caching, and resolver failure affect recovery. Clients need bounded backoff and observability of resolution state. Do not assume one DNS record means one connection or that a service mesh removes client behavior.

The dependency-light capstone uses a deterministic resolver model. The full topology can use two local servers and a simple target. Course 8 will study wider service discovery in distributed architecture.

## Load balancing preserves only stateless assumptions

Round-robin or pick-first policies distribute calls among available endpoints according to channel and resolver behavior. They do not make in-memory idempotency, session state, watch history, or worker assignments consistent. Any state required across calls must be durable, replicated under an explicit protocol, or affinity-bound with acknowledged limitations.

Unary queries can usually move between instances if both access authoritative storage. A resumed WatchRun may require shared observation history or a fallback to GetRun. A worker stream is a long-lived connection; if the server fails, the worker reconnects and durable leases reconcile the session.

Tests route calls across two instances with different instance identifiers and shared/different fixture state to expose hidden local assumptions.

## Keepalive and connection lifetime

HTTP/2 keepalive pings can detect dead connections and keep intermediaries active, but aggressive settings can create load or violate server policy. Configure client ping interval, timeout, whether pings occur without active calls, and server enforcement. Do not use keepalive as application heartbeat or lease authority.

Idle timeout can close unused channels to conserve resources. Maximum connection age can encourage rebalancing and certificate rotation, with a grace period for active calls. Long-lived streams need a planned reconnect path. Settings must include jitter or fleet-level coordination to avoid synchronized reconnect storms.

The course service configuration documents these values as examples tied to the local workload, not universal production defaults.

## Connectivity backoff and wait-for-ready

When connection attempts fail, channels use exponential backoff. A client may fail calls immediately or wait for readiness within each call's deadline. Backoff and retry interact: connection retries may happen before or between application attempts. Evidence must distinguish transport connection work from RPC attempts.

Resetting backoff manually is an operator or test action, not a normal application loop. A tight reconnect loop can overload DNS, TLS, and recovering servers. Wait-for-ready is applied per method and call according to Course 5's deadline policy.

Connectivity state is advisory and racy. Applications should make calls with deadlines and handle outcomes rather than spin until a channel reports READY.

## Graceful server drain

Shutdown begins by changing readiness/health to not serving so load balancers stop new calls. The server rejects or redirects new work according to policy, stops assigning new worker jobs, and allows admitted unary calls and streams a bounded drain period. It then cancels remaining calls, releases resources, and closes.

Streams need explicit behavior. Watch clients receive cancellation or a retryable status and resume elsewhere. Uploads that cannot finish are cleaned up without publication. Worker sessions stop receiving assignments; durable leases survive and later expire or reconcile. The server must not wait forever for a client that ignores cancellation.

The lifecycle state machine is `starting → accepting → draining → stopping → stopped`, with failure states and idempotent transitions. Tests verify permits, gauges, and health at every stage.

## Client shutdown

Clients also drain. Stop accepting new application work, cancel or finish active calls according to their value, flush required telemetry within a bound, close streams, and close channels. A process exit that simply abandons in-flight mutation calls creates ambiguous outcomes and noisy retries after restart.

Background control clients persist reconciliation identifiers before calling. Worker clients save only durable attempt state owned by the worker profile; they do not treat a socket buffer as a queue. The shutdown report lists unresolved calls requiring reconciliation.

Course 4's incident and lifecycle principles remain authoritative. gRPC adds channel and stream resources, not a separate operational philosophy.

## Reflection and diagnostics

Server reflection allows tools such as grpcurl and dynamic clients to discover services and descriptors. It is valuable in development and controlled operations, but it can expose internal method, message, and package details. Enable it according to environment and security policy, not unconditionally.

Health is standardized and narrowly exposed. Reflection may require an authenticated operator network or be disabled in production. Descriptor sets remain the release source of truth; runtime reflection proves what one instance currently serves.

The governance proof compares reflection inventory with the checked-in RPC catalogue when the live toolchain is available. Mismatch blocks release.

## Worked operations review: drain one of two instances

Two Analysis Control instances share the authoritative database. A client channel resolves both and uses round-robin. Instance A receives a long WatchRun stream and several unary calls; instance B is idle. A deployment controller asks A to stop.

The first action is not process termination. A changes service health to `NOT_SERVING` and lifecycle state to draining. New calls should select B or fail according to the caller’s bounded readiness policy. A stops assigning new worker jobs. Already admitted unary calls receive a finite grace period. Watch clients are told to reconnect with their resume sequence. Uploads may finish only when remaining bytes and deadline fit the drain budget; otherwise their stages are cleaned.

A common defect is to keep reporting serving until the process exits. Load balancers continue sending new work, the drain never converges, and forced termination creates ambiguous outcomes. The opposite defect is to use liveness failure to remove traffic: the platform restarts an otherwise healthy draining process and interrupts recovery. Liveness, readiness, and gRPC health have distinct meanings.

The channel also needs discipline. It is reused across calls, carries one target and credential policy, and owns resolver and subchannel state. Applications do not create a new channel per request or spin on `READY`. During A’s shutdown, the resolver and balancer select B. B must be correct because idempotency and observation state are durable or explicitly resumable. If the design stored request outcomes only in A’s memory, load balancing would expose duplicates.

Long-lived connections affect deployment. Maximum connection age can gradually move clients, but if every server uses the same exact age, a fleet reconnect storm can occur. Jitter and grace are required. Keepalive pings can detect dead connections but do not renew worker leases or prove application readiness. Connection backoff must remain bounded and observable.

At the end of the grace period, A cancels remaining calls, releases permits and file handles, flushes bounded telemetry, and stops. The client records calls whose outcomes are ambiguous and reconciles them. Worker clients reconnect, authenticate, and compare durable lease generations. No socket buffer is treated as durable work.

The lab’s two-instance trace records endpoint chosen, health phase, call admission, active calls, stream termination, reconnect delay, and authoritative result. This is more meaningful than showing that a Kubernetes pod eventually became Ready. It proves that the service lifecycle preserves RPC semantics.

## Implementation reading

Read `capstone/operations/service-config.json`, `lifecycle-policy.yaml`, and `capstone/shared/vectors/lifecycle.json`. Compare Python channel/server lifecycle adapters with the TypeScript deterministic channel model. The live Python proof starts two servers and exercises health and drain.

## Failure checklist

- Is a new channel created for each application request?
- Does health confuse process liveness with readiness to serve each service?
- Can discovery or reconnect loop without bounded backoff?
- Does load balancing depend on hidden in-memory state?
- Can graceful shutdown wait forever or accept new work during drain?
- Is reflection exposed more broadly than the descriptor policy allows?

## Transition

After preserving the checkpoint evidence, continue to **Generation, Testing, Reflection, and Schema Governance**. Do not progress while the non-compensable gate remains unresolved.

## Module synthesis

You are ready to leave this module when you can **treat channels as long-lived managed resources rather than create-per-call sockets, separate process liveness, service readiness, and standard gRPC health status, and reason about name resolution, endpoint changes, load-balancing policy, and connection backoff** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Implement channel and server lifecycle state machines, standard health semantics, bounded reconnect behavior, two-instance routing evidence, graceful drain, and an operational service configuration** and requiring the following oracle: **New work stops entering a draining instance, admitted work either finishes or terminates within the declared bound, clients reconnect with bounded backoff, durable state remains correct across instances, and health/reflection exposure matches policy.**

The cumulative platform now includes **Implement channel and server lifecycle state machines, standard health semantics, bounded reconnect behavior, two-instance routing evidence, graceful drain, and an operational service configuration**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [Generation, Testing, Reflection, and Schema Governance](../module-09-generation-testing-reflection-and-schema-governance/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
