# Guide — packet-path analysis

A packet-path analysis is a falsifiable model of one flow. It is not a generic architecture diagram and not a dump of commands.

## 1. Fix the flow identity

Record:

- source process, Pod, namespace, node, and address family;
- logical destination name;
- selected destination address and port;
- protocol and application operation;
- exact time and request identifier;
- expected return path.

Without these fields, observations from different attempts can be combined accidentally.

## 2. Write the transformations

For an external Atlas request, a useful path is:

```text
client name
→ public DNS answer
→ load-balancer/Gateway address
→ TLS listener and HTTP authority
→ HTTPRoute match
→ Service virtual address
→ eligible EndpointSlice address
→ Pod interface
→ application listener
```

Add every expected DNAT, SNAT, encapsulation, proxy, and TLS termination point. State which component owns the transformation.

## 3. Collect evidence from both sides of a transition

A route lookup at the source and an empty capture at the destination can locate a forwarding failure. A request visible at the destination with no reply at the source points toward return routing, policy, or translation state. One capture point cannot establish an end-to-end path.

## 4. Use negative controls

A deliberately wrong port, hostname, selector, or policy peer proves that the tool can distinguish the condition being claimed. If correct and incorrect cases produce the same observation, the evidence is not sensitive enough.

## 5. Stop at the earliest failed transition

Do not restart CoreDNS when the name already resolved. Do not delete Pods when the selected endpoint is correct but the route is missing. Do not change the Gateway when TLS fails because of a wrong trust root. Repair the owner of the first false transition.

## Reusable worksheet

| Step | Desired state | Owner | Observation | Positive control | Negative control | Result |
|---|---|---|---|---|---|---|
| name selection | | | | | | |
| DNS | | | | | | |
| route | | | | | | |
| source policy | | | | | | |
| Service selection | | | | | | |
| destination policy | | | | | | |
| transport | | | | | | |
| TLS | | | | | | |
| application | | | | | | |

Complete the worksheet before changing configuration. The completed table is stronger incident evidence than an unstructured terminal transcript.
