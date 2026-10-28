# Module 10 — Network operations, conformance, and release

A network architecture becomes operational only when engineers can detect failure, identify the earliest broken transition, change implementations safely, and state exactly which environments and features have been proved. A collection of green manifests is not a release. A successful request is not conformance. A dashboard without a population definition is not an SLO.

The final engineering question is:

> Can Atlas Connectivity Plane 1.0 be diagnosed, upgraded, rolled back, and defended using evidence that is precise about both capability and limitation?

## Learning outcomes

By the end of this module, you can:

- diagnose from a layered packet-path ledger rather than a favorite tool;
- distinguish API status, controller status, data-plane state, packet evidence, and application evidence;
- define bounded network SLIs and SLO populations;
- scope conformance claims to version, feature, implementation, and environment;
- plan CNI, Service-plane, DNS, and Gateway upgrades with rollback and skew limits;
- run a failure-oriented game day with abort and cleanup criteria;
- classify release evidence as accepted, rejected, review-required, or not-executed;
- publish a precise Course 6 handoff without claiming storage durability.

## Diagnose the earliest failed transition

Start with one concrete flow:

```text
source process
→ source namespace/interface
→ source route
→ Node or tunnel path
→ destination Node
→ Service or Gateway data plane, if used
→ destination namespace/interface
→ listening socket
→ protocol exchange
```

Then compare desired and observed state in order. The first failed transition is usually the best repair boundary.

Examples:

- no DNS answer: do not inspect Gateway routes yet;
- correct DNS and failed TCP handshake: inspect route, policy, listener, and return path before HTTP;
- accepted Route but unprogrammed listener: do not change application paths;
- Service and endpoints correct but one Node stale: inspect that Node’s data-plane generation;
- TLS handshake succeeds but HTTP returns `421`: inspect authority, not CNI;
- small payload works and large payload stalls: test MTU before increasing application timeouts.

This method prevents a common incident pattern: restarting several unrelated components until the symptom disappears and the cause remains unknown.

## Observation surfaces and their limits

### Kubernetes API objects and status

Useful for desired state, generations, conditions, endpoint membership, and controller-reported reconciliation. They do not show whether packets traversed the installed path.

### Controller and agent logs

Useful for reconciliation errors, resource references, and implementation decisions. Absence of an error is not packet evidence. Logs may also lag, sample, or omit high-volume events.

### Metrics

Useful for rates, latency distributions, drops, saturation, DNS response codes, endpoint counts, and convergence duration. Metrics need bounded dimensions and exact populations.

### Flow logs or policy verdicts

Useful for source/destination, policy decision, translation, and data-plane path. They depend on implementation coverage and may not include payload/protocol semantics.

### Packet capture

Useful for exact packet timing, addresses, flags, retransmission, fragmentation, TLS handshake metadata, and where a packet disappears. Capture location matters. A packet absent at one interface may have taken another path.

Captures can contain secrets and personal data. Define interface, filter, snap length, duration, owner, storage, and deletion before collection.

### Application telemetry

Useful for protocol outcome, authenticated identity, request semantics, and backend behavior. It cannot prove a packet that never reached the process.

A strong incident uses several vantage points and records their clocks.

## A network decision tree

A reusable sequence is:

1. **Name resolution** — exact query, resolver, answer, TTL, family.
2. **Address and route** — chosen destination, source address, route, MTU.
3. **Attachment** — source/destination namespace interfaces and CNI state.
4. **Service/Gateway membership** — eligible endpoint and route attachment.
5. **Policy** — source egress and destination ingress verdicts.
6. **Transport** — SYN/SYN-ACK, retransmission, reset, timeout.
7. **TLS** — SNI, chain, hostname, ALPN, certificate version.
8. **HTTP or application protocol** — authority, route, status, deadline, body.
9. **Return path** — reverse route, NAT state, proxy response.

The sequence is not rigid; it is a way to avoid skipping prerequisite transitions.

## Runbooks should begin with a path, not a restart command

A runbook is useful when it turns an ambiguous symptom into bounded observations and decisions. Each Atlas network runbook includes:

- symptom and user-visible impact;
- exact path or flow in scope;
- expected owners and address families;
- first safe observations;
- decision points that separate DNS, route, policy, Service, Gateway, TLS, and application causes;
- evidence to preserve before mutation;
- bounded mitigation;
- rollback and validation;
- escalation owner;
- post-incident follow-up.

“Restart CoreDNS,” “restart the CNI,” or “recreate the Service” is not an opening diagnostic step. Restarts can destroy caches, logs, generations, and evidence while temporarily hiding the fault. Use them only after the failed transition and recovery mechanism are understood, or as a declared emergency mitigation with evidence preserved.

The course ships separate runbooks for missing endpoints, DNS failure, NetworkPolicy denial, Gateway route failure, TLS failure, and egress failure. Their common structure is deliberate; their diagnostic branches are specific to the path.

## Network SLIs need exact populations

Examples of useful indicators:

### Service connection success

```text
successful eligible connection attempts
÷ all eligible connection attempts
```

Define “eligible” so policy-denied negative probes, malformed requests, and client cancellations are not mixed accidentally with platform failures.

### DNS success

Separate:

- A and AAAA queries;
- positive and negative expected outcomes;
- SERVFAIL/timeouts;
- cache and authoritative paths;
- namespace or resolver class.

An expected NXDOMAIN for an unknown name is a successful negative control, not a platform error.

### Gateway request outcome

Separate:

- route-not-found or authority rejection;
- TLS handshake failure;
- backend connection failure;
- backend application status;
- client cancellation;
- request family and listener.

### Convergence duration

Measure time from desired-state change to:

- EndpointSlice update;
- data-plane programming;
- DNS/route status update;
- negative selection of removed endpoints;
- Gateway condition and listener readiness.

Do not use raw Pod IPs, hostnames, or unbounded paths as metric labels. Preserve detailed identities in traces/logs with access control when needed.

## Conformance is feature- and environment-scoped

A defensible conformance statement names:

```text
specification and version
+ API channel/profile
+ implementation and version
+ feature set
+ environment
+ test suite/version
+ passed, skipped, and failed cases
+ known deviations
```

For example, “Gateway API supported” is weak. A stronger statement is:

```text
Gateway API 1.6 Standard channel;
implementation X version Y;
HTTPRoute core profile plus named extended features;
kind cluster version Z;
conformance suite revision R;
all required cases passed, three optional cases not executed.
```

The same discipline applies to CNI lifecycle, NetworkPolicy, dual stack, traffic distribution, and cloud load-balancer behavior.

Semantic tests prove Atlas logic. A real cluster proves one installed environment. Neither should be promoted to a universal claim.

## Upgrade design

Networking upgrades modify live data-plane state. Plan them as compatibility and recovery events.

### CNI upgrade

Record:

- control/agent version skew;
- on-disk CNI config changes;
- existing attachment compatibility;
- route, tunnel, map, and policy migration;
- address-allocation state;
- Node drain/restart requirements;
- rollback support;
- observability continuity;
- test paths for same-Node, cross-Node, Service, DNS, policy, and egress.

A plugin binary rollback is unsafe if durable state or dataplane formats have already changed incompatibly.

### Service data-plane change

Changing kube-proxy mode or moving to eBPF can alter:

- rule/map ownership;
- source NAT behavior;
- session affinity;
- connection tracking;
- NodePort exposure;
- traffic policies;
- diagnostic commands;
- established connections.

Run old/new comparison and negative tests. Do not compare only median request latency.

### CoreDNS or NodeLocal DNS upgrade

Test:

- configuration syntax and plugin availability;
- A/AAAA/SRV/negative behavior;
- TCP fallback;
- cache behavior;
- upstream forwarding;
- policy dependencies;
- rolling capacity;
- per-Node failure if NodeLocal is used.

### Gateway API and controller upgrade

Separate:

- CRD schema/channel upgrade;
- controller upgrade;
- data-plane proxy upgrade;
- certificate and listener state;
- route status conversion;
- unsupported fields/features;
- existing connection behavior;
- rollback of each layer.

Changing CRDs, controller, and data plane simultaneously destroys isolation of cause.

## Canary and rollback for network changes

A safe network upgrade exposes a bounded population first and keeps the old path available long enough to compare behavior. Possible canary units include:

- one Node pool for a CNI agent version;
- one namespace or Service for a policy/data-plane mode;
- one Gateway address or hostname;
- one CoreDNS replica or NodeLocal cache cohort;
- one address family or topology domain.

The canary must measure correctness as well as latency. Compare:

- allowed and denied flow matrices;
- endpoint convergence;
- source translation;
- DNS positive/negative behavior;
- connection establishment and long-lived streams;
- MTU/large-payload behavior;
- resource saturation;
- error and retry amplification.

Rollback is possible only while old configuration, state formats, routes, CRDs, and binaries remain compatible. If an upgrade migrates durable IPAM state or removes old CRD fields, “redeploy the old image” may not be a rollback. State the point of no return and the recovery route before promotion.

## Failure injection and game days

A useful game day has a falsifiable hypothesis, bounded blast radius, abort conditions, expected signals, recovery owner, and cleanup proof.

Example faults:

- remove one endpoint from readiness;
- leave one Node on a stale Service generation;
- deny DNS TCP fallback;
- break one address-family route;
- present a wrong-hostname certificate;
- make an HTTPRoute reference invalid;
- exhaust a bounded NAT model;
- introduce a Gateway retry on an unsafe operation.

For each fault, record:

```text
baseline
→ injected change
→ earliest expected failed transition
→ expected API/status signal
→ expected data-plane evidence
→ expected user-visible effect
→ abort threshold
→ repair
→ proof of restored state
```

A game day that merely creates an outage and observes alerts is incomplete. It must test the diagnosis and recovery contract.

## Categorical release policy

Atlas classifies every required gate:

- **pass** — required evidence executed and satisfied;
- **fail** — requirement violated;
- **review-required** — evidence exists but a deliberate human decision is needed;
- **not-executed** — required environment or tool was unavailable.

Blocker gates cannot be averaged into a score. A release with perfect documentation but no policy enforcement evidence does not pass. A managed-cloud claim cannot pass based on kind.

The accepted dependency-light release can state:

- Course 4 handoff preserved exactly;
- packet-path, CNI, Service, DNS, policy, locality, Gateway, TLS, and egress semantics pass the Atlas models;
- real loopback DNS, Service proxying, TLS hostname validation, authority enforcement, endpoint withdrawal, and backend selection were executed;
- course manifests and handoffs are exact;
- cluster, CNI enforcement, Gateway-controller, and cloud behavior remain not executed where tools/environments were absent.

That is a strong and honest release, not a production certification.

## The network evidence dossier

The final release dossier is organized by claim rather than by tool output. For each claim, it records:

```text
claim
→ governing contract or specification
→ Atlas policy decision
→ implementation/version
→ executed evidence
→ negative control
→ unresolved limitation
→ owner and review date
```

Examples include “unauthorized namespaces cannot reach Atlas API,” “the Gateway rejects the wrong authority,” and “IPv6 cross-Node Service traffic works.” The first two can receive local or semantic evidence in this release; the third remains not executed without a suitable cluster.

This structure prevents a folder of command outputs from being mistaken for an argument. Evidence is useful only when tied to a precise claim and its falsification condition.

## Final game day

The cumulative lab combines several failures:

1. one backend becomes unready;
2. a DNS negative cache retains an old result;
3. one policy path denies expected egress;
4. an unauthorized Route attempts attachment;
5. a wrong-hostname TLS client is rejected;
6. an external redirect targets a forbidden peer.

The learner must identify each earliest failed transition, avoid broad rollback, and produce a release dossier that distinguishes semantic, local-network, cluster, and environment evidence.

## Course 6 handoff

Course 6 receives ten exact files describing:

- Service and DNS identities;
- ports and protocols;
- address families;
- NetworkPolicy requirements;
- Gateway/TLS expectations;
- topology and traffic assumptions;
- approved egress paths;
- storage-facing connectivity requirements;
- version ledger;
- known risks.

The handoff must not claim:

- volume durability;
- database replication;
- snapshot consistency;
- backup validity;
- restore success;
- storage fencing;
- zone-resilient data behavior.

Those are Course 6 responsibilities. Course 5 provides the network path and its failure semantics.

## Final defense

A learner completes Course 5 by defending one request end to end:

```text
external client
→ DNS
→ route and address family
→ TLS listener
→ Gateway attachment and HTTP route
→ Service data plane
→ eligible EndpointSlice endpoint
→ NetworkPolicy
→ Atlas API socket
→ approved external dependency or worker path
→ response and return path
```

For every transition, the defense must identify:

- desired state;
- owner;
- observed evidence;
- negative control;
- failure mode;
- rollback or recovery;
- strongest executed evidence class.

## Capstone implementation

Module 10 uses:

- `capstone/architecture/network-release-contract.json`;
- `capstone/architecture/conformance-profile.json`;
- `capstone/releases/`;
- `capstone/planted-defects/`;
- `capstone/runbooks/`;
- `capstone/scripts/final_game_day.py`;
- `capstone/handoff/`.

The release scripts reject mutable images, broad egress, absent enforcement evidence, and production overclaims. They also preserve `not-executed` as a first-class state rather than silently treating missing infrastructure as success.

## Operational evidence needs stable populations

A network indicator must define what enters its denominator: DNS queries, new TCP connections, Gateway requests, Service selections, or critical-journey attempts. Mixing these populations hides the failed transition.

For each indicator, define eligible attempts, success and failure outcomes, timeout treatment, address family, source and destination class, cluster and zone dimensions, exclusions, owner, and retention. Avoid raw Pod IPs, full hostnames, or request paths as unbounded metric labels; keep high-cardinality detail in controlled logs, traces, or incident artifacts.

## Upgrades require a compatibility matrix

A networking release may change Kubernetes APIs, CNI agents, node kernels, kube-proxy or its replacement, CoreDNS, Gateway API CRDs, Gateway controllers, cloud integrations, and PKI. These components rarely change atomically.

Record the overlap that actually occurs:

| Component | New reads old state | Old tolerates new state | Rollback question |
|---|---|---|---|
| CNI | can the new agent check old attachments? | can the old agent ignore new fields? | can old code clean new state safely? |
| Gateway API | can the old controller watch stored versions? | can the new controller preserve old behavior? | are conversions and status compatible? |
| Service data plane | do mixed Nodes preserve semantics? | are connection states compatible? | is old rule/map state restored? |
| DNS | do clients tolerate answer changes? | are old/new replicas aligned? | can old configuration parse restored data? |

Test mixed versions, new and established connections, failure during rollout, and rollback. “DaemonSet ready” or “controller Deployment available” is not workload-visible compatibility evidence.

## Packet capture is a controlled evidence procedure

Before capture, state the expected five-tuple, address family, interface or namespace, inner or outer encapsulation, duration, size bound, payload sensitivity, and clock reference. Capture at the narrowest useful point and prefer headers over payloads.

A missing packet means something only when the capture point and filter cover the expected path. A packet visible on one Node does not prove it reached the destination namespace. Preserve captures as sensitive incident artifacts.

## Conformance and Atlas evidence are complementary

Conformance proves a defined implementation profile in a test environment. It does not prove Atlas DNS, policy, certificates, cloud routes, or failure objectives. Atlas journeys prove local integration but do not replace upstream conformance.

The dossier therefore records both the implementation/API conformance profile and Atlas-specific packet, protocol, negative-control, upgrade, and rollback evidence. Statements such as “Gateway API supported” or “NetworkPolicy enabled” are rejected unless scoped to versions, features, implementation, and environment.

## The release decision is categorical

Each required lane is classified as:

- **pass** — executed and satisfied;
- **fail** — executed and violated;
- **review-required** — a deliberate trade-off needs accountable approval;
- **not-executed** — the required environment or tool was unavailable.

A blocker in `fail` rejects the release. A blocker in `not-executed` leaves that target unproven. Non-blocking environment lanes may remain not executed while the dependency-light educational reference is accepted for its stated scope. Documentation quality cannot compensate for disabled TLS verification, unenforced policy, mutable workload identity, or a false production claim.

## Course completion

Atlas Connectivity Plane 1.0 is complete when:

- all ten checkpoints pass;
- the predecessor remains exact;
- the final game day is explained from transition evidence;
- the release state is categorical and honest;
- the Course 6 handoff verifies byte-for-byte;
- no unexecuted cluster or cloud claim is presented as production proof.

The next course uses this network contract to study persistence, stateful identity, CSI, snapshots, backup, restore, and data resilience.
