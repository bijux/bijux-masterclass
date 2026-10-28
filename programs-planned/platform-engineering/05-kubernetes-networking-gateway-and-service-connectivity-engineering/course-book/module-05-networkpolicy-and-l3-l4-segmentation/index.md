# Module 5 — NetworkPolicy and L3/L4 segmentation

A default Kubernetes network is often broadly reachable among Pods. NetworkPolicy lets the platform isolate selected Pods for ingress, egress, or both, then admit traffic through additive allow rules. The YAML is compact; the effective policy is the composition of every matching policy, the labels that drive selection, the installed enforcement implementation, and the packet observation points around NAT and host traffic.

The engineering question is:

> How do we reduce reachability without deleting required dependencies, granting authority through mutable labels, or claiming enforcement that the installed data plane has not proved?

## Learning outcomes

By the end of this module, you can:

- determine when a Pod becomes isolated for ingress or egress;
- calculate the union of applicable allow rules;
- evaluate source egress and destination ingress independently;
- interpret Pod, namespace, CIDR, port, and protocol selectors precisely;
- explain why labels are policy inputs but not cryptographic identity;
- inventory DNS and platform dependencies before default deny;
- plan a staged rollout with negative controls and rollback;
- distinguish API validity, policy intent, and installed enforcement.

## Isolation begins with selection

A policy object does not automatically isolate an entire namespace. A Pod becomes isolated for a direction when at least one NetworkPolicy in its namespace selects the Pod and includes that direction in its policy types.

For ingress:

```text
no selecting ingress policy
→ Pod is not ingress-isolated by NetworkPolicy

at least one selecting ingress policy
→ Pod is ingress-isolated
→ only traffic allowed by the union of matching ingress rules is admitted
```

Egress is evaluated independently.

An empty ingress rule list on a selecting policy creates ingress isolation with no allowed ingress from the NetworkPolicy model. An empty egress rule list can do the same for egress.

Names such as `deny-all` have no special semantics. Denial comes from isolation plus the absence of an allow rule.

## Policies are additive

For a selected Pod, all matching allow rules are combined. Adding another NetworkPolicy can add allowed traffic; it cannot subtract a flow already allowed by another policy.

This has an important review consequence: reading one file cannot establish effective policy. You must enumerate every policy that selects the source and destination.

A Pod-to-Pod connection may need both directions to pass:

```text
if source is egress-isolated:
    at least one source-selected egress rule must allow the destination and port

if destination is ingress-isolated:
    at least one destination-selected ingress rule must allow the source and port

connection is allowed by NetworkPolicy only if every required direction passes
```

A correct destination ingress policy cannot override denied source egress.

## Selectors and their exact Boolean meaning

`podSelector` matches Pod labels in an appropriate namespace scope. `namespaceSelector` matches namespace labels. Their placement changes semantics.

One peer containing both:

```text
namespaceSelector: environment=platform
podSelector: role=gateway
```

means Pods with `role=gateway` inside namespaces matching `environment=platform`.

Two separate peers mean a union:

```text
all Pods in selected namespaces
OR
selected Pods in the policy namespace
```

Indentation and list structure are therefore security-sensitive. Translate non-trivial policy into a truth table during review.

## Labels are authority inputs

A selector trusts the labels it matches. If an application team can assign itself the label `platform.example/role=gateway`, then a policy allowing that label does not create a meaningful boundary.

For every label used in policy, record:

- who may create or mutate it;
- whether admission controls protect it;
- whether namespace owners can influence it;
- how it is removed during decommissioning;
- whether future workloads could match accidentally.

Prefer stable platform-controlled label keys. Course 8 will implement admission and multi-tenant governance; Course 5 records the dependency explicitly.

NetworkPolicy selection is not cryptographic workload identity. A compromised Pod retaining an allowed label can still use permitted network paths. Application and workload authentication remain necessary.

## Ports and protocols

NetworkPolicy primarily controls L3/L4 reachability. Rules can admit protocols and ports, including named ports in supported contexts.

An allowed TCP port does not authorize:

- HTTP paths or methods;
- JWT claims or users;
- database roles;
- gRPC methods;
- tenant records;
- message topics;
- application commands.

It permits a transport flow. Course 3’s application authorization remains authoritative after the connection is established.

Feature details such as end-port ranges or less common protocols depend on API and implementation support. A release claim must name the exact feature and evidence lane.

## `ipBlock` and translation ambiguity

`ipBlock` matches address ranges rather than Kubernetes workload selectors. It is appropriate for deliberately owned external networks and some infrastructure paths.

Its interaction with translated traffic must be proved in the selected implementation. Questions include:

- Is policy evaluated before or after Service destination translation?
- Is the source observed before or after load-balancer SNAT?
- Are Pod addresses or Node addresses visible at the hook?
- How are IPv4-mapped IPv6 addresses treated?
- Does the flow traverse a host-network component outside normal Pod policy?

Do not write a rule for a ClusterIP or public client range based on assumed observation points. Capture or policy-verdict evidence must show the addresses used by the enforcement hook.

## DNS is the first hidden egress dependency

Default-deny egress often breaks DNS before it tests any application dependency. A complete DNS allow design may need:

- the actual resolver address used by Pods;
- selected CoreDNS Pods/namespaces or a Service address, depending on implementation semantics;
- UDP and TCP port 53;
- a NodeLocal DNS address if used;
- both address families;
- separate CoreDNS upstream egress.

Allowing all UDP/53 egress is broad and incomplete: it permits arbitrary DNS destinations and misses valid TCP fallback.

The lab records the resolver path explicitly rather than adding exceptions until name resolution returns.

## Platform and application dependency inventory

Before default deny, create an owned flow inventory:

| Source | Destination | Protocol/port | Direction | Reason | Owner | Evidence |
|---|---|---|---|---|---|---|
| Gateway | Atlas API | TCP/8080 | API ingress | public HTTP backend | edge team | route + negative test |
| Atlas API | cluster DNS | UDP/TCP 53 | API egress | discovery | platform DNS owner | query evidence |
| Atlas API | identity endpoint | HTTPS | API egress | workload token exchange | identity team | trace + peer evidence |
| worker | object endpoint | HTTPS | worker egress | artifact storage | Course 6 owner | deferred contract |
| telemetry agent | collector | OTLP | egress | observability | platform ops | connection evidence |

Potential dependencies include the Kubernetes API, workload-identity endpoints, telemetry collectors, secret/certificate agents, queues, object stores, and private endpoints. Do not infer them only from successful traffic. Review configuration, traces, owner contracts, and failure modes.

## Host traffic and host-network boundaries

Standard NetworkPolicy is focused on Pod traffic. Behavior involving Node processes, host-network Pods, loopback, and implementation-specific host policy needs separate evidence.

A Gateway implementation running on host networking, a Node-local DNS cache, or a cloud metadata endpoint may not fit the same selector model as ordinary Pods. Course 8 will address broader host and cluster policy. Course 5 must not imply that namespace default deny secures every host path.

## Safe default-deny rollout

A production rollout should be staged:

1. **Inventory intended flows.** Name source, destination, port, owner, and evidence.
2. **Govern labels.** Ensure selectors rely on controlled metadata.
3. **Create positive and negative probes.** Test intended success and unauthorized denial.
4. **Add narrow allow policies while workloads are not yet isolated.** Verify selection.
5. **Introduce default deny to one bounded namespace or direction.** Avoid simultaneous unrelated changes.
6. **Observe implementation verdicts and application outcomes.** Distinguish policy denial from route or DNS failure.
7. **Test rollback.** Roll back only the intended policy change; do not delete all policies indiscriminately.
8. **Remove temporary exceptions with an owner and expiry.** Broad emergency allows must not become permanent architecture.

Rollback is an engineering artifact, not “delete policy and hope.” A broad rollback can expose unrelated workloads and destroy evidence.

## Existing connections and convergence

Policy changes must be programmed into a data plane. Propagation is not instantaneous, and established connections may behave differently from new ones depending on the implementation and enforcement hook.

Define the incident objective precisely:

- block new connections;
- terminate established connections;
- prevent future application requests;
- isolate one workload;
- isolate an entire tenant or namespace.

Then test that objective. A new-connection denial does not prove established streams were terminated.

## What proves enforcement?

A valid NetworkPolicy object proves only API acceptance. A selector truth table proves intended semantics. Enforcement evidence should include:

- selected source and destination identities;
- exact protocol, port, and address family;
- expected allow result;
- expected deny result;
- installed implementation and feature support;
- policy-programming status or verdicts where available;
- packet or connection evidence at the enforcement point;
- behavior after policy update and rollback.

A timeout alone is ambiguous: it can result from route, DNS, Service, application, or policy failure.

## Worked investigation — default deny breaks only one replica

After egress default deny, two Atlas API Pods resolve Service names and one does not. The policies are identical and select all three Pods.

The failing Pod is scheduled on a Node using NodeLocal DNS at a link-local address. The other Nodes still point directly to the CoreDNS Service because kubelet configuration drifted. The allow policy covers the Service path but not the Node-local address.

The policy behaved as declared. The platform had two resolver paths but documented one.

The repair is to restore consistent resolver configuration, decide which DNS path is authoritative, update the flow inventory, and prove UDP/TCP behavior on all Node classes. Adding `0.0.0.0/0` egress would conceal the configuration drift and invalidate the segmentation objective.

## Capstone implementation

Module 5 uses:

- `capstone/atlas_net/policy.py` for the additive ingress/egress model;
- `capstone/shared/vectors/policy.json` for selector and direction cases;
- `capstone/manifests/base/20-networkpolicy-default-deny.yaml`;
- `capstone/manifests/base/21-networkpolicy-dns.yaml`;
- `capstone/manifests/base/22-networkpolicy-gateway-api.yaml`;
- `capstone/scripts/network_policy_lab.py`.

The semantic evaluator proves the Atlas policy subset. It does not prove enforcement by a real CNI. The optional kind+Cilium lane is the next evidence class.

## Policy evaluation is endpoint selection plus rule union

For one traffic direction, first determine whether any policy selects the endpoint for that direction. If none does, standard NetworkPolicy leaves that direction non-isolated. If at least one does, the allowed traffic is the union of all matching allow rules for that direction.

A connection must satisfy both relevant sides:

```text
source egress permits destination
AND
destination ingress permits source
```

This explains two common mistakes. Adding another policy cannot subtract a flow already allowed by another standard policy; policies are additive within the isolated direction. Deleting a deny-looking policy may change nothing because the real allow remains elsewhere.

The Atlas evaluator reports selection and permission separately so the learner can distinguish “endpoint was never isolated” from “endpoint was isolated and this rule allowed the flow.”

## Selector authority is security authority

A label becomes a security principal attribute when policy selects it. The platform must govern who can set or mutate that label and which controller derives it.

For every policy-sensitive label, record:

- semantic meaning;
- owner and mutation authority;
- admission validation;
- whether tenants can self-assign it;
- how replacement workloads inherit it;
- how stale labels are removed;
- audit and incident evidence.

A policy allowing `role=gateway` is weak if any namespace owner can label an arbitrary Pod `role=gateway`. Namespace selectors have the same issue when namespace labels grant access to shared infrastructure.

## Stateful replies and existing connections need explicit tests

Many implementations permit reply traffic for an allowed connection without requiring a separate reverse rule, but the exact observation and enforcement points are implementation behavior. Existing connections may also survive a policy update for some period because of connection tracking.

A rollout test should include:

- a connection established before isolation;
- a new connection after policy creation;
- a connection after each node has acknowledged policy state;
- UDP and TCP where both are required;
- IPv4 and IPv6;
- policy deletion and rollback;
- node-agent restart with existing policy.

Do not infer policy behavior from one short request. Record whether the tested flow was new or established.

## Default deny is a dependency discovery exercise

The safe path to default deny is not “apply deny and add exceptions until alerts stop.” Build a dependency inventory first:

- DNS;
- API server or workload-identity endpoints where required;
- metrics, logs, and traces;
- time synchronization where the environment exposes it through the network;
- admission or sidecar dependencies;
- databases, queues, object stores, and private endpoints;
- health probes and management traffic;
- backup and restore paths;
- emergency support paths.

Then create positive and negative tests for each authorized flow. Roll out by namespace or workload class with an abort condition and a known rollback version. Broad allow-all rollback can expose unrelated tenants and erase the very negative controls the change was intended to establish.

## Policy portability has limits

The NetworkPolicy API defines a portable L3/L4 core, but implementations differ in enforcement points, host traffic, node-local traffic, service translation order, logging, named-port handling, and extension policies. A release claim must state the installed implementation and the behaviors actually tested.

If the design needs FQDN policy, L7 HTTP policy, cluster-wide administrative policy, host firewalling, or service-account-aware enforcement, identify that as an implementation or additional-API requirement. Do not hide it behind a standard NetworkPolicy manifest that cannot express the intended control.

## Transition

Module 5 constrains reachability. Module 6 studies which eligible endpoint receives allowed traffic, how source addresses change, and why locality and dual-stack preferences alter availability as well as latency.
