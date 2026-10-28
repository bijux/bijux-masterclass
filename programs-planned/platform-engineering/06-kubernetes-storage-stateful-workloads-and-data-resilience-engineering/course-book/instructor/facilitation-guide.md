# Instructor facilitation guide

Course 6 should be taught through evidence transitions rather than API memorization.

## Before each module

Ask learners to name the authoritative state, controller owner, backend effect, application oracle, and destructive authority. Do not accept “Kubernetes handles it” as an answer.

## During labs

Allow diagnosis before hints. Require learners to preserve evidence before mutating the system. When a learner proposes deleting a PVC, VolumeAttachment, finalizer, or snapshot content, ask what history could become unrecoverable.

## Review style

Use counterfactuals:

- What if the timeout occurred after backend success?
- What if the old Node is partitioned rather than powered off?
- What if the backup key is lost?
- What if GitOps replays this action?
- What if the restore target is not empty?

## Track choice

The dependency-light semantic lane is mandatory. Native Kubernetes/CSI and cloud lanes strengthen evidence where available. Never punish a learner for marking an unavailable environment `not-executed`; penalize only unsupported claims.

## Completion

A learner passes when they can explain the complete data journey and defend authority, consistency, recovery, and evidence boundaries—not when every manifest applies successfully.
