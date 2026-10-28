# Casebook — The Private Subnet That Lost S3

Atlas continues to serve existing results, but new backup uploads fail in one
availability zone. General internet requests from the host still succeed.

## Initial hypotheses

The team considers IAM, KMS, DNS, S3 outage, NAT, and route-table drift. Because
internet egress works, one responder dismisses the network.

The route evidence shows that `private-b` has both:

```text
0.0.0.0/0 → nat-b
S3 prefix list → vpce-s3
```

Longest-prefix routing selects the gateway endpoint for S3, so NAT health is
irrelevant to this request. The endpoint association was removed from the
`private-b` route table during a refactor. DNS and IAM were healthy.

## Why the successful internet test misled

The test exercised a different destination and therefore a different route. It
proved the default route, not the service-specific endpoint route. “Network is
fine” was too broad a conclusion.

## Recovery

The team restores the endpoint association through the declared network module,
verifies the route-table identity, runs an S3 write/read/delete vector using the
Atlas role, and checks that data-subnet policies remain unchanged.

## Prevention

- model service endpoints as route dependencies in the network contract;
- test one packet path per critical destination class;
- retain route-table associations as plan evidence;
- avoid broad “connectivity” health claims;
- distinguish DNS, route, endpoint policy, IAM, KMS, and service behavior in the
  runbook.

## Lesson

Network evidence is destination-specific. A single successful connection does
not prove the paths used by other services, even from the same host.
