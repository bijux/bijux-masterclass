# Case 1 — Bound but not usable

## Incident

`atlas-db-data-0` is Bound. The database Pod remains Pending after a Node replacement. The team assumes the CSI driver is broken because the claim looks healthy.

## Evidence

- PVC: Bound to `pv-atlas-db-0`.
- PV: node affinity requires `topology.kubernetes.io/zone=zone-a`.
- Pod: anti-affinity excludes the only remaining Node in `zone-a`.
- Nodes in `zone-b` have capacity but cannot access the existing volume.
- No attach or mount operation has started.

## Reasoning

Binding proves claim-to-volume identity, not complete schedulability. The earliest missing transition is Pod placement. Restarting CSI components cannot help because the controller has not requested attachment. Editing PV node affinity would misrepresent backend accessibility and risk data loss.

## Correct response

Preserve the existing volume and choose among explicit options: restore or replicate to a volume in another zone, add compatible capacity in `zone-a`, or change the workload topology policy through a reviewed migration. The chosen action depends on the service availability target and recovery evidence.

## Lesson

Always distinguish claim state, scheduler state, attachment state, and application state. A green object at one layer does not collapse the remaining control loops.
