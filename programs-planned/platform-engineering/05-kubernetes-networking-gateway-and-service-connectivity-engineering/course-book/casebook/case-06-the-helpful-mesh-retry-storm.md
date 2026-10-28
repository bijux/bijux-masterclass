# Case 6 — The helpful mesh retry storm

## Incident

During a brief external dependency slowdown, Atlas egress volume increases twelvefold. The dependency receives duplicate commands, worker queues grow, and the Gateway reports elevated latency. Every layer was configured to “improve reliability.”

## Hidden multiplication

The application retries twice, the Gateway retries once, and an experimental mesh policy retries once. Under the worst failure pattern, one original request can create:

```text
3 application attempts × 2 Gateway attempts × 2 mesh attempts = 12 downstream attempts
```

Each layer uses its own timeout, so attempts continue after the caller’s useful deadline. NAT and connection pools become saturated. The dependency slowdown is amplified into a platform incident.

## Investigation

Tracing reveals distinct attempt identifiers at each layer, but they were not linked to one total retry budget. The operation is a command with an idempotency key, so duplicates do not create twelve business effects, but they consume capacity and extend queue delay. Some dependency endpoints do not support the same idempotency contract, increasing risk.

The mesh was introduced for “standard retries and mTLS” without a quantified requirement or ownership decision. Kubernetes, the Gateway, and the application already provided parts of the requested behavior.

## Repair

The platform assigns retry ownership to the application client for this operation, with one absolute deadline and bounded backoff. Gateway and mesh retries are disabled for the command. Safe read requests retain a separately justified edge retry profile. Connection and queue metrics are added to the decision evidence.

The mesh proposal is rejected for Atlas Connectivity Plane 1.0. Workload identity and backend mTLS remain Course 8 concerns rather than reasons to add an unowned proxy layer now.

## Durable change

Every retrying component must declare:

- eligible methods/operations;
- idempotency precondition;
- maximum attempts;
- per-attempt and total deadline;
- backoff and jitter;
- cancellation behavior;
- attempt identity and telemetry;
- interaction with other retry layers.

A release check calculates worst-case amplification.

## Lesson

Reliability features compose multiplicatively unless one owner controls the budget. A service mesh is not a maturity badge. It is another control plane and data path that must solve a named problem better than existing mechanisms.
