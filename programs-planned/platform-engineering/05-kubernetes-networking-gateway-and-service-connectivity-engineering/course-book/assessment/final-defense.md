# Final defense

The final assessment is a live, evidence-driven defense of Atlas Connectivity Plane 1.0.

## Required demonstrations

1. Trace one external HTTPS request from logical name to API response and return path.
2. Remove one endpoint from readiness and prove that Service traffic stops selecting it.
3. Demonstrate a DNS negative-cache transition without restarting CoreDNS blindly.
4. Prove one intended NetworkPolicy allow and one intended deny in both directions.
5. Show a Route attachment failure, identify the failed condition, and repair only its owner.
6. Reject a wrong TLS hostname and an untrusted issuer.
7. Reject an unapproved egress peer or redirect.
8. Diagnose route and MTU failures that produce similar application symptoms.
9. Defend the direct-versus-mesh decision with retries, cost, and operator ownership.
10. Verify the exact Course 6 handoff.

## Oral questions

The reviewer may change an address family, endpoint condition, namespace, policy selector, listener hostname, certificate, or egress answer. The learner must predict the earliest affected transition before executing a command.

## Non-compensable failures

The course is not passed if the learner disables TLS verification, authorizes by Pod IP, uses broad allow-all policy as the final state, changes the predecessor workload silently, cannot distinguish object status from packet evidence, or presents local evidence as production proof.
