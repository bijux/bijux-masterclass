# Lab — liveness spiral and disruption boundary

## Goal

Separate restart, readiness, voluntary eviction, and node-pressure loss.

## Safety boundary

Use the semantic lifecycle/disruption model. The optional kind lane may kill only fixture processes or drain a disposable worker node.

## Baseline

Three Atlas API replicas are ready and available; PDB minAvailable is two.

## Hypothesis

Dependency-based liveness creates synchronized restarts during an outage. Local-progress liveness plus dependency readiness preserves process stability. PDB blocks a second voluntary eviction but cannot block node-pressure loss.

## Controlled action

1. Make the database dependency unavailable under the bad liveness policy.
2. Record restarts and availability.
3. Apply repaired liveness/readiness semantics.
4. Evict one Pod through the PDB-aware path.
5. Attempt a second eviction.
6. Simulate node-pressure loss of another Pod.

## Oracle

Bad policy restarts containers repeatedly. Repaired policy leaves processes alive but unready/degraded. The first voluntary eviction succeeds, the second is blocked, and node-pressure loss bypasses the PDB.

## Evidence

Preserve probe timelines, restart counts, readiness/availability counts, PDB calculations, eviction decisions, termination events, and residual capacity.

## Interpretation

Explain why the same user-visible outage can involve four different owners: application, kubelet, Deployment controller, and disruption workflow.

## Cleanup

Restore dependencies and remove semantic/kind resources.

## Completion gate

Advance only after each failure is assigned to the correct mechanism and no PDB claim exceeds its real scope.
