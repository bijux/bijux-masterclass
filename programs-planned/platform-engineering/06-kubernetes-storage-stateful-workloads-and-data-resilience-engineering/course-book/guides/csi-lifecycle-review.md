# CSI lifecycle review

A CSI review should answer six groups of questions.

## Identity

How is a stable Kubernetes request mapped to one backend volume ID? Which parameters participate in idempotency? What happens if the same name is reused with incompatible capacity or capability?

## Capabilities

Which controller and node capabilities are advertised? Are snapshot, clone, expansion, raw block, multi-node access, volume health, topology, capacity, and modify-volume features actually implemented? Which Kubernetes sidecars and CRDs are required?

## Controller service

Review create/delete, attach/detach, controller expansion, snapshot, and list operations. Determine retry behavior, timeouts, pagination, error codes, and backend reconciliation.

## Node service

Review registration, staging, publication, unpublication, unstage, node expansion, statistics, and condition reporting. List host mounts, devices, privileges, socket paths, and cleanup behavior after Node restart.

## Upgrade

Record supported Kubernetes and CSI versions, sidecar matrix, leader-election behavior, CRD changes, rollback, and handling of volumes created by older versions.

## Incident evidence

Identify the API objects, logs, metrics, backend identifiers, and safe read-only commands required to diagnose each phase. A driver is not production-ready if the team cannot distinguish attach, stage, and publish failure.
