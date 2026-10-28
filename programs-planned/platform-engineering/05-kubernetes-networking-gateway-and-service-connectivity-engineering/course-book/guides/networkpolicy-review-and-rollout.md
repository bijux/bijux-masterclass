# Guide — review and roll out NetworkPolicy

NetworkPolicy review is a set-based authorization exercise. Reading one resource in isolation is insufficient because policies are additive.

## Review method

For each protected flow, record:

```text
source namespace and labels
source isolation state
source egress allow set
destination namespace and labels
destination isolation state
destination ingress allow set
protocol and port
implementation-specific behavior
```

Traffic is admitted only when both isolated directions allow it.

## Label authority

List every label used by a selector and who may change it. A policy that trusts an application-controlled label is not a reliable security boundary. Prefer platform-owned namespace and workload identity labels enforced by admission policy.

## Safe default-deny rollout

1. Observe real dependencies in a bounded namespace.
2. Convert them into a reviewed dependency matrix.
3. Add narrow allows for DNS, telemetry, identity, storage, and application paths.
4. Apply default deny.
5. Run positive and negative controls from known identities.
6. Inspect implementation verdicts where available.
7. Remove obsolete broad allows.
8. Record unexecuted environment cases.

Do not apply default deny to a broad shared environment and discover dependencies through outage.

## Common review errors

- assuming a policy name containing “deny” denies traffic;
- checking destination ingress but not source egress;
- using `ipBlock` for Pod identity;
- permitting an entire namespace when one workload is intended;
- forgetting TCP DNS fallback;
- relying on FQDN or L7 behavior that belongs to one implementation;
- treating network reachability as application authorization.

## Evidence package

A complete policy review contains the effective policy matrix, positive and negative probes, implementation/version, flow verdicts or captures, and a rollback path.
