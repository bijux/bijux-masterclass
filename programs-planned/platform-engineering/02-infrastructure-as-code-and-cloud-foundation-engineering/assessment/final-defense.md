# Final Defense — Atlas Cloud Foundation 1.0

The final defense is a 60-minute engineering review, not a slide presentation.
The learner works from the release dossier and must navigate to the source,
plan, policy, runtime, and recovery evidence behind every material claim.

## Required demonstrations

1. Explain the four-state model: configuration, state, remote control plane, and
   workload data plane.
2. Show how a resource address remains stable or is migrated explicitly.
3. Recover from a simulated stale/foreign state lineage without overwriting the
   authoritative backend.
4. Trace one packet from the public name to the private Atlas process and one
   egress packet from a private subnet.
5. Prove one allowed and one denied runtime-identity action.
6. Defend the host image, bootstrap, IMDSv2, data-volume, and replacement
   contract.
7. Restore an acknowledged result into an empty destination and verify its
   checksum.
8. Classify a provider-normalization change, emergency drift, and intentional
   migration correctly.
9. Reject the public-SSH release candidate and explain why the NAT candidate
   requires review rather than automatic rejection.
10. Verify the Course 3 handoff and state every unexecuted cloud claim.

## Non-compensable failures

The learner cannot pass if any of these remain:

- state recovery can overwrite another lineage;
- a workload or CI path uses an undisclosed long-lived cloud key;
- public host ingress bypasses the governed edge;
- durable data exists only on the root disk;
- a critical replacement is approved without a migration record;
- a missing real-cloud proof is described as passing;
- the Course 3 handoff omits identity, storage, network, or health contracts.
