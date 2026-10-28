# Incident case — the tag moved after approval

## Situation

Security approved `registry.example/atlas-api:1.0.0`. Between approval and deployment, an automation defect retargeted the tag to another image index. The cluster pulled the new bytes while dashboards, release notes, and operator messages continued to display “1.0.0.”

Nothing in the registry protocol requires a tag to remain immutable. The defect was not that the registry violated the tag. The defect was that review and deployment treated mutable discovery metadata as release authority.

## Evidence needed

Investigators reconstruct four identities:

1. the digest resolved when the candidate was reviewed;
2. the digest selected by the promotion record;
3. the digest returned by the registry when deployment pulled;
4. the digest actually present on nodes/runtimes.

They also preserve tag audit history, automation identity, registry replication events, referrer/evidence subjects, and the deployment manifest. If the review system stored only a tag, it cannot prove which bytes were approved.

## Correct model

Review, policy, and deployment use immutable `repository@digest` identities. A human-readable version tag may be assigned after promotion for discovery. Tag movement is protected and audited, but tag protection is a secondary control; the deployment still remains safe if a tag changes because the approved digest is fixed.

Promotion between registries copies the exact graph, verifies every target blob, records the target repository/digest, and re-evaluates target-environment policy. Rebuilding in the destination is forbidden because it creates a new subject rather than promoting the reviewed one.

Rollback also uses a retained approved digest, not “whatever the old tag points to now.”

## Transfer lesson

A tag communicates intent. A digest identifies content. A release decision must authorize content. Mixing these roles produces deployments that are semantically named but cryptographically unrelated to the reviewed candidate.
