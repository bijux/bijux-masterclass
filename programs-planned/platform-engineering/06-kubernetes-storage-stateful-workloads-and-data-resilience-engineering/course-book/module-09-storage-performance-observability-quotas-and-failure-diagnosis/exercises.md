# Exercises — Storage Performance, Observability, Quotas, and Failure Diagnosis

Work from the chapter and executable artifacts, but write your own reasoning before reading the solutions. Each answer should name the authoritative state, the unsafe shortcut, and the evidence that would decide the case.

## 1. Relate IOPS and throughput

A workload performs 1,200 operations/s with an average 16 KiB request. Calculate throughput and explain why this does not predict latency.

## 2. Use queue depth as evidence

A device completes 100 IOPS with average queue depth 5. What is the average outstanding time implied by Little’s Law, and how should it be interpreted?

## 3. Diagnose rising database latency

CPU is low, fsync p99 rises, backend queue depth rises, and snapshot count has doubled. Form a hypothesis and a safe experiment.

## 4. Design bounded metric dimensions

Which labels belong on `csi_operation_duration_seconds`, and which should remain in logs?

## 5. Enumerate capacity dimensions

Name at least eight ways a storage platform can be out of capacity while reporting free bytes.

## 6. Separate attach, mount, and I/O failure

A Pod shows `FailedMount`. What evidence distinguishes attachment failure, node-stage failure, and filesystem failure?

## 7. Model snapshot capacity risk

Why should a capacity alert include snapshot delta growth rather than only PVC requested and used bytes?

## 8. Design storage quotas

Create a quota policy for a tenant that uses PVCs, snapshots, backups, and object artifacts.

## 9. Evaluate a storage benchmark

A benchmark reports 100,000 IOPS from an empty volume for 30 seconds. What evidence is missing before using it for Atlas database sizing?

## 10. Turn an alert into an operator decision

Design an alert for stale backups that avoids firing on one delayed schedule yet catches loss of recoverability.

## 11. Classify a service-tier change

A VolumeAttributesClass change is accepted by Kubernetes but the native driver test was not run. What is the release state?

## 12. Defend the observability boundary

Why can Prometheus and CSI logs not prove that restored Atlas data is correct?
