# Worked answers — Network operations, conformance, and release

The final answers emphasize precise claims. A tool output is evidence only when tied to a transition and falsifiable expectation.

## 1. Why is kubectl describe insufficient packet proof?

`kubectl describe` shows API objects, events, and controller-reported status. It can reveal selectors, conditions, addresses, and reconciliation errors, but it does not show the route chosen by the source, policy verdict at the dataplane, packet arrival, NAT translation, TLS handshake, or application read. Use it as one control-plane vantage point and correlate with namespace/Node routes, data-plane state, captures, flow logs, and protocol-aware client evidence. A green object can coexist with a broken packet path.

## 2. What is the earliest-failed-transition method?

Draw the exact flow and list ordered transitions from name resolution through route, attachment, Service/Gateway selection, policy, transport, TLS, application protocol, and return path. Compare desired and observed state at each step. The first transition whose expected observation or negative control is absent defines the narrowest likely owner set. This prevents editing downstream objects before prerequisites work and avoids broad restarts that destroy evidence. The incident record should state why later transitions were not yet evaluated.

## 3. Why should network SLOs separate address family?

IPv4 and IPv6 use independent DNS answers, routes, policies, listeners, Service families, endpoints, and egress paths. Client fallback can hide one-family failure inside aggregate success. Separate eligible populations and outcomes by family, then also measure normal client selection/fallback. If dual stack is not promised, state the supported family rather than combining metrics. Bounded `family=ipv4|ipv6` labels are safe; raw addresses are not.

## 4. What makes Gateway conformance claim precise?

It names Gateway API version/channel, implementation and version, conformance profile, resources and features used, test-suite revision, environment, and passed/skipped/failed cases. It also distinguishes API conformance from cloud address, DNS, TLS, and application reachability. “Gateway API supported” is not precise enough for release. A required extended feature that was not tested should remain not executed or review-required even if core HTTPRoute tests pass.

## 5. Why can a kube-proxy mode migration change exposure?

Different modes or replacements program Services, NodePorts, source NAT, affinity, health checks, and connection tracking differently. A migration can alter which interfaces accept NodePort traffic, source-address preservation, existing connections, policy interaction, and diagnostic surfaces. Compare positive and negative flow matrices, not only latency. Record state cleanup and rollback compatibility so old and new data-plane rules do not coexist unpredictably.

## 6. What evidence should accompany a CNI upgrade?

Record old/new versions and skew, attachment compatibility, IPAM state, route/tunnel/map formats, policy behavior, Node rollout order, rollback point, and observability continuity. Execute same-Node, cross-Node, Service, DNS, policy, MTU/large-payload, egress, and cleanup tests on a bounded canary. Include existing Pods and newly attached Pods. If durable state migrates irreversibly, document that rollback requires recovery rather than an image downgrade.

## 7. Why are raw IP addresses dangerous metric labels?

Pod and client addresses have high, changing cardinality and may contain sensitive or tenant-identifying data. Using them as metric labels can overload the metrics system and create retention/privacy problems. Aggregate metrics by bounded dimensions such as workload, namespace, dependency, outcome, address family, or topology domain. Keep exact addresses in protected logs/traces with controlled retention when incident analysis requires them.

## 8. What distinguishes accepted from not-executed release state?

Accepted means all blocker requirements for the stated claim were executed and satisfied at the named evidence level. Not-executed means the required environment/tool/evidence was unavailable; it is neither pass nor fail. For example, semantic Gateway attachment tests can pass while managed-cloud load-balancer behavior remains not executed. The release must avoid promoting lower-level evidence to the absent claim. Review-required is different again: evidence exists but a deliberate human decision is needed.

## 9. Why must a game day have abort conditions?

Faults can exceed the intended blast radius, threaten management access, corrupt state, or create cascading load. Abort conditions define when to stop and restore before learning becomes uncontrolled damage. They should reference measurable thresholds such as unexpected namespaces affected, error rate, loss of recovery path, queue depth, or elapsed time. Prepare rollback and verify it before injection. A game day without bounded scope, evidence preservation, and cleanup is an outage rehearsal without safety engineering.

## 10. What should the Course 6 handoff avoid claiming?

It should not claim volume durability, database consistency or replication, snapshot correctness, backup validity, restore success, storage fencing, or zone-resilient data behavior. Course 5 can provide service names, ports, families, policy, TLS, topology, egress, and path failure semantics. A successful TCP connection to storage proves connectivity only. Course 6 owns persistent identity, CSI, write semantics, backup, restore, and data resilience.

## 11. Why can broad policy rollback be operationally harmful?

Deleting all policies can expose unrelated workloads, remove tenant boundaries, invalidate incident evidence, and create a second security incident while fixing connectivity. Rollback should reverse the specific change or apply a pre-reviewed bounded exception with owner and expiry. Test the rollback before rollout and verify intended denied flows remain denied afterward. Emergency access must be observable and removed explicitly.

## 12. What is the final release’s strongest claim when no real cluster was available?

It can claim that the Course 4 handoff was preserved; the documented Atlas network contracts and semantic models passed; Python and Go tests passed; real loopback DNS, Service proxying, TLS chain/hostname verification, authority enforcement, endpoint withdrawal, and egress controls were executed; manifests and handoffs verified exactly. It cannot claim CNI, NetworkPolicy, CoreDNS, Gateway-controller, cloud load-balancer, or multi-node production behavior. Those remain clearly `not-executed`, with complete native lab procedures for a suitable environment.
