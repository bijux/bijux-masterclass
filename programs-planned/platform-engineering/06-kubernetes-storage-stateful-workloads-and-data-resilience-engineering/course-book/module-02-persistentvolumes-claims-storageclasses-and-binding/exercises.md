# Exercises — PersistentVolumes, Claims, StorageClasses, and Binding

Work from the chapter and executable artifacts, but write your own reasoning before reading the solutions. Each answer should name the authoritative state, the unsafe shortcut, and the evidence that would decide the case.

## 1. Name the authoritative records in binding

Distinguish the PVC, PV, StorageClass, CSI backend volume, and application data. Which object owns intent, allocation identity, policy, physical effect, and business truth?

## 2. Explain delayed binding with a concrete conflict

A Pod is restricted to zone B, but an `Immediate` StorageClass provisions in zone A. Why can free global capacity not repair the workload?

## 3. Treat a StorageClass as a service contract

What should `atlas-rwo-durable` promise, and what must remain explicitly outside the StorageClass contract?

## 4. Compare static and dynamic provisioning

Choose static or dynamic provisioning for importing an existing production volume, and explain the protection controls required.

## 5. Analyze an idempotent provision retry

`CreateVolume` succeeds in the backend, but the controller times out before recording the PV. What must the next attempt do?

## 6. Design claim deletion safely

A developer deletes a StatefulSet and its PVC. Describe the state transitions for `Retain` and `Delete` reclaim policies and the operator decisions they imply.

## 7. Diagnose a Pending PVC without guessing

Give an ordered investigation for a Pending PVC whose backend reports free capacity.

## 8. Explain protection finalizers

What problem do PVC/PV protection finalizers solve, and what do they not solve?

## 9. Review access and volume modes

A PVC requests `ReadWriteMany` and `Block`, while the workload expects a mounted POSIX filesystem. Where should the incompatibility be rejected?

## 10. Prevent unsafe prebinding

An operator sets `volumeName` on a PVC to force it onto a retained PV. List the checks required before this can be safe.

## 11. Model multi-claim scheduling

A Pod needs a 20 GiB data claim and a 5 GiB WAL claim. Zone A has 22 GiB; zone B has 40 GiB but the Node has one remaining attach slot. Explain the result.

## 12. Defend the Course 7 handoff

What binding and retention facts must GitOps automation preserve?
