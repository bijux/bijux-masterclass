# NetworkPolicy truth table

Evaluate one flow with four questions:

1. Is the source selected by any egress policy?
2. If yes, does at least one applicable egress rule allow this peer/protocol/port?
3. Is the destination selected by any ingress policy?
4. If yes, does at least one applicable ingress rule allow this peer/protocol/port?

```text
allowed = source-egress-allowed AND destination-ingress-allowed
```

where an unisolated direction contributes `true`.

Within a peer, namespace and Pod selectors are an intersection. Multiple peers are alternatives. Policies are additive; there is no ordered “last rule wins.”

Include implementation/version, address family, NAT position, current labels, and existing-connection behavior in evidence.
