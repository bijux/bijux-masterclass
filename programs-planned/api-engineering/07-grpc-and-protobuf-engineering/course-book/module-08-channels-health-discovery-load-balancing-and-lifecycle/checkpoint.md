# Checkpoint — Module 08: Channels, Health, Discovery, Load Balancing, and Lifecycle

## Required result

Implement channel and server lifecycle state machines, standard health semantics, bounded reconnect behavior, two-instance routing evidence, graceful drain, and an operational service configuration.

## Demonstrate

- [ ] Treat channels as long-lived managed resources rather than create-per-call sockets.
- [ ] Separate process liveness, service readiness, and standard grpc health status.
- [ ] Reason about name resolution, endpoint changes, load-balancing policy, and connection backoff.
- [ ] Configure keepalive, idle behavior, maximum connection age, and wait-for-ready safely.
- [ ] Drain unary and streaming rpcs during graceful shutdown.
- [ ] Expose reflection and diagnostics according to environment and authorization policy.

## Commands

```bash
make core-proof
```

## Evidence to retain

- [ ] `capstone/shared/vectors/lifecycle.json` exists, is reproducible, and you can explain its oracle.
- [ ] `capstone/operations/service-config.json` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-08-lifecycle-proof.json` exists, is reproducible, and you can explain its oracle.

## Defend the design

1. Answer the central question in one paragraph: How do clients and servers manage long-lived channels, instance health, name resolution, load balancing, startup, draining, and shutdown without hiding failure or losing active work?
2. Name the authoritative owner and smallest counterexample.
3. State what the available evidence does not prove.

## Continue only when

Continue only after you can demonstrate the **Channels, Health, Discovery, Load Balancing, and Lifecycle** increment, preserve the controlled counterexample as a regression, keep inherited checkpoints green, and explain which stronger claim remains outside the evidence you collected.
