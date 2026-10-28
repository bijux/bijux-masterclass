# Case 4 — The default deny that broke DNS

## Incident

The Atlas namespace adopts egress default deny. Ordinary API requests continue for several minutes because established connections and cached addresses remain usable. New worker processes then fail to resolve Services. Small DNS answers sometimes work; larger responses fail consistently.

## Why the symptoms look random

The allow policy permits UDP port 53 to CoreDNS but not TCP. Many answers fit in UDP, while truncated or larger responses require TCP fallback. Existing caches delay the onset. The policy is deterministic; the workload mix makes it appear intermittent.

## Investigation

The team writes the DNS path explicitly:

```text
worker Pod
→ egress policy
→ CoreDNS Service/data plane
→ CoreDNS Pod UDP/53 or TCP/53
→ Kubernetes plugin/upstream
```

A `dig +tcp` negative control fails. Implementation policy verdicts show an egress drop to TCP/53. CoreDNS logs never receive the TCP query. The failure is therefore before the DNS server, not an upstream timeout.

The review also finds that the namespace selector in the allow rule relies on a custom label absent from `kube-system` in one environment. A built-in namespace-name label is used deliberately instead, with the CoreDNS Pod selector reviewed for the actual distribution.

## Repair

The policy adds both UDP and TCP 53 to the intended DNS endpoints. The team verifies A, AAAA, negative, and large-answer cases. It retains default deny and does not add broad egress.

## Durable change

The rollout procedure now requires:

- a flow inventory before default deny;
- positive and negative DNS probes over both transports;
- observation of current namespace/Pod labels;
- fresh-process tests that avoid existing caches;
- evidence for IPv4 and IPv6 DNS paths where enabled;
- rollback to the previous policy set rather than deletion of all policies.

## Lesson

Default deny is not proven by one successful cached request. DNS is a dependency with two transports, several selectors, and cache-delayed symptoms. Security policy must be tested against protocol behavior, not against a simplified port list.
