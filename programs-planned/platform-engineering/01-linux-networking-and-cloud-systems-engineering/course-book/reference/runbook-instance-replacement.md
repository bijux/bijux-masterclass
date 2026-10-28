# Runbook — Atlas Instance Replacement

## Trigger

Host loss, failed maintenance, immutable-image release, unrecoverable OS state, or planned replacement.

## Preconditions

Known image/release identity, boot configuration, workload identity, durable-state source, DNS/load-balancer procedure, capacity quota, console or rollback route, and deletion policy.

## Procedure

Create replacement, verify instance and image identity, attach or restore durable state, start services, pass local readiness and verified HTTPS, add to routing, drain old instance, then delete obsolete resources after the rollback window.

## Evidence

Old/new IDs, image digest or ID, boot transcript, mount/state hashes, readiness, client result, routing change, drain completion, and deletion inventory.

## Abort

Abort cutover when state is ambiguous, identity is overprivileged, certificate verification fails, or the replacement cannot pass the same client oracle.
