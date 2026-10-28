# Evidence model

Networking claims are unusually easy to overstate because one successful request crosses many layers. Course 5 uses an explicit evidence ladder.

## Level 1 — semantic evidence

Deterministic models establish invariants such as longest-prefix route selection, idempotent CNI replay, additive NetworkPolicy evaluation, Gateway attachment, hostname verification, and release classification. These proofs are portable and reviewable. They do not show that a real kernel, CNI, or cloud controller implements the invariant.

## Level 2 — process and host evidence

Real sockets, DNS packets, TLS handshakes, HTTP messages, routes, namespaces, and captures show host behavior. The loopback capstone tour is in this class. It proves actual protocol mechanics on the build host, not Kubernetes integration.

## Level 3 — local-cluster evidence

A pinned kind+Cilium environment can prove Kubernetes admission, EndpointSlices, policy enforcement, Gateway programming, and local data-plane behavior for that implementation and topology. It cannot prove another CNI, managed load balancer, or multi-zone cloud.

## Level 4 — environment evidence

A real target environment can prove its CNI, routes, DNS, Gateway, TLS automation, load balancer, egress, and failure behavior. Record exact versions, configuration, topology, address families, and test time.

## Level 5 — operational evidence

Repeated incidents, upgrades, rotations, capacity events, and recovery exercises establish operated maturity. A one-time staging test is not this level.

## Evidence bundle

Every lab result should record:

```text
claim
scope
component versions
baseline
fault or action
expected oracle
observed result
timestamps
artifacts
cleanup
residual risk
evidence level
```

## Negative controls

A positive path is accepted only when the evidence system also detects an intentional negative case. Examples:

- wrong DNS name returns NXDOMAIN;
- unauthorized namespace is denied by policy;
- unattached Route reports rejection;
- wrong TLS hostname fails verification;
- egress peer mismatch is rejected;
- stale EndpointSlice programming is distinguishable from desired state.

This prevents a broken test harness from producing an empty but apparently successful report.

## Production language

Use precise verbs:

- **modeled** for semantic evidence;
- **observed locally** for process/host evidence;
- **verified in kind+Cilium** for the optional cluster lane;
- **verified in target environment** only when that proof ran;
- **operated** only when recurring operational evidence exists.

`FINAL-VERIFICATION.md` records executed and unexecuted routes. Missing tools produce `not-executed`, never a synthetic pass.
