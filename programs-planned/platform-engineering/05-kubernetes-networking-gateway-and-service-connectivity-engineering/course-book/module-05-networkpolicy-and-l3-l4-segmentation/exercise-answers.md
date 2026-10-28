# Worked answers — NetworkPolicy and L3/L4 segmentation

The effective policy is the composition of selection, isolation, all matching allows, both traffic directions, and an installed enforcement implementation.

## 1. When does a Pod become isolated for ingress?

A Pod becomes ingress-isolated when at least one NetworkPolicy in its namespace selects the Pod and includes ingress in its policy types. Once isolated, only ingress allowed by the union of all matching ingress rules is permitted by the NetworkPolicy model. A policy elsewhere in the namespace that does not select the Pod does not isolate it. Prove selection with labels and policy evaluation, then use an intended allow and unauthorized deny test on the actual implementation.

## 2. Why can adding a second policy not revoke traffic allowed by the first?

NetworkPolicy allow rules are additive. For an isolated direction, traffic is allowed if any applicable rule permits it. There is no priority-ordered deny rule in the standard API that overrides another allow. Therefore, a second policy can add permissions but cannot subtract an existing permission. To remove a flow, change or remove every rule that grants it. Effective-policy review must enumerate all policies selecting the endpoint, not only the newly edited file.

## 3. What is the semantic difference between one peer containing namespaceSelector plus podSelector and two separate peers?

When both selectors are in one peer, they form an intersection: Pods matching the Pod selector inside namespaces matching the namespace selector. When they are separate peer entries, they form a union: all Pods in selected namespaces plus selected Pods in the policy namespace or relevant scope. This can greatly broaden access. Translate the YAML into a truth table and test examples from matching/non-matching namespaces and Pods; indentation is part of security meaning.

## 4. Why is a label selector not proof of workload identity?

Labels are mutable Kubernetes metadata. Their authority depends on who can create Pods, edit labels, or label namespaces. If an untrusted tenant can assign a label trusted by policy, it can join the allowed set. Cryptographic workload identity is a separate mechanism. Use platform-controlled labels with admission governance for segmentation, and continue authenticating the caller at the workload/application layer. Evidence includes label mutation permissions and a negative test showing an unauthorized workload cannot self-label into the policy.

## 5. Why must DNS egress include TCP as well as UDP?

DNS commonly uses UDP, but valid behavior can fall back to TCP when responses are truncated or otherwise require it. Allowing only UDP/53 creates intermittent failures that depend on answer size and resolver behavior. The policy should cover the actual resolver path and both transports, without broadly allowing arbitrary DNS servers. Prove with a controlled query that forces or exercises TCP and record the resolver address, policy verdict, and answer.

## 6. What does an allowed TCP port fail to authorize?

It allows transport reachability to an address/selector and port. It does not authorize an HTTP path, method, JWT subject, tenant, database operation, gRPC method, or message action. A compromised allowed workload can still misuse the application unless the service authenticates and authorizes requests. NetworkPolicy reduces attack paths and blast radius; it does not replace Course 3’s domain policy. The decisive evidence is an unauthorized application request over an allowed connection being rejected.

## 7. Why is ipBlock behavior around Services dangerous to assume?

Policy may observe traffic before or after Service destination translation or source NAT, depending on implementation and path. A rule written for a ClusterIP might actually be evaluated against backend Pod addresses; external source addresses may be replaced by a load balancer or Node. Test the installed enforcement point with flow logs or capture and record the addresses it uses. Do not claim portable behavior from one CNI or cloud path.

## 8. What should be prepared before default deny?

Prepare an owned dependency inventory, controlled labels, narrow allow policies, positive and negative probes, observability at the enforcement layer, a bounded rollout scope, and a tested rollback. Include DNS UDP/TCP, Gateway-to-backend traffic, identity/telemetry dependencies, and any Node-local path. Apply default deny after the required allows are understood, not as a discovery mechanism followed by broad exceptions. The completion evidence is a truth table showing intended flows pass and unintended flows fail.

## 9. Why can 0.0.0.0/0 egress undermine the exercise?

It allows every IPv4 destination and can hide missing dependency ownership, SSRF paths, metadata access, and unintended Internet reachability. The application may “work,” but the segmentation objective has not been proved. It also says nothing about IPv6. Use narrowly owned destinations or an explicit review-required temporary exception with expiry and observability. A negative test to a forbidden external address should fail in the accepted release.

## 10. How do source egress and destination ingress policies combine?

If the source is egress-isolated, one of its applicable egress rules must permit the destination and port. If the destination is ingress-isolated, one of its applicable ingress rules must permit the source and port. Both required decisions must allow the connection. Diagnose them independently: a destination-side allow cannot override source egress denial. The proof should report two verdicts and include cases where only one direction is allowed.

## 11. Why might a node-local resolver require special handling?

It may use a link-local or Node address rather than the CoreDNS Service/Pod addresses expected by a namespace policy. Standard Pod selectors may not describe the Node-local listener, and host traffic semantics can be implementation-specific. Inventory the effective resolver configuration on every Node class, then write and test the appropriate egress rule or host policy. A one-Node DNS failure after default deny is strong evidence of inconsistent NodeLocal configuration or path coverage.

## 12. What evidence proves NetworkPolicy enforcement?

You need a supporting implementation, the exact source/destination identities, port/protocol/family, policy selection, expected verdict, and observed positive and negative connection behavior. Prefer policy verdict logs, counters, or captures at the enforcement point in addition to application outcomes. API acceptance and YAML review prove intent only. Include update/convergence and established-connection behavior if the claim covers live policy changes. A timeout without implementation evidence is ambiguous.
