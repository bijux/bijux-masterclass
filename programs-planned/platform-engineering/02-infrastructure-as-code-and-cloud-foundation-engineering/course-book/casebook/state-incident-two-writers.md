# Casebook — Two Writers and a Green Pipeline

At 09:00, the foundation pipeline begins an apply. At 09:03, an engineer starts
a local recovery plan after seeing stale state in the console. Both jobs report
that they acquired a lock. At 09:07, the pipeline completes. At 09:08, the local
operation writes a state object with a different lineage. The next plan proposes
to recreate the VPC.

## What happened

The pipeline had migrated to S3 native lock files. The engineer's old checkout
still used a DynamoDB lock table. Each coordinated with a different lock system.
The backend object was shared, but the mutual-exclusion protocol was not.

The green apply log proves that one writer completed its actions. It does not
prove exclusive ownership of the state object after completion.

## First response

1. Stop every automated and local writer.
2. Record S3 object versions, lock objects, DynamoDB lock item, apply logs,
   caller identities, and CloudTrail events.
3. Do not force-unlock or push either local copy.
4. Compare the two lineages, serials, and remote IDs against read-only inventory.
5. Select the authoritative sequence based on target, actions, and actual remote
   resources—not simply the largest serial.
6. Restore the selected version in an isolated backend key and plan.
7. Peer-review the recovery before changing the authoritative key.

## Root cause

The migration changed configuration in one repository but did not inventory all
writers. There was no transition phase in which writers acquired both locks.
The organization treated a backend feature toggle as a local implementation
detail rather than a coordination protocol release.

## Corrective actions

- publish one backend profile and minimum OpenTofu version;
- make initialization fail when the backend profile digest is wrong;
- inventory scheduled drift jobs and recovery tooling;
- use an overlap migration if changing lock systems;
- test foreign-lineage rejection;
- document lock ownership and stale-lock investigation;
- alert on writes from unapproved role classes.

## Lesson

A lock is only meaningful when every writer participates in the same protocol.
A green pipeline can coexist with a corrupted coordination model. State safety
requires participant inventory, version governance, and recovery evidence.
