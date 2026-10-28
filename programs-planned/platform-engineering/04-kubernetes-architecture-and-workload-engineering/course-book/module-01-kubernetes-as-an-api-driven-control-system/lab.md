# Lab — stop reconciliation without deleting desired state

## Goal

Demonstrate that persisted intent and controller convergence are separate responsibilities.

## Safety boundary

Use the dependency-light semantic cluster. The optional kind extension may use only a disposable cluster named `atlas-course4`.

## Baseline

Run `python3 capstone/scripts/run_capstone_tour.py --scenario steady-state`. Confirm one AtlasWorkload, two Deployments, expected ReplicaSets, and the target Pod count.

## Hypothesis

If the ReplicaSet reconciler is disabled, a Deployment replica change remains persisted but the Pod count does not converge. Re-enabling the reconciler restores convergence without duplicate Pods.

## Controlled action

1. Disable the ReplicaSet controller in the simulator.
2. Change API replicas from three to five.
3. Run several reconcile cycles.
4. Preserve the Deployment and ReplicaSet state.
5. Re-enable the controller and reconcile again.

## Oracle

While disabled, desired replicas are five and observed Pods remain three. After restart, exactly five owned Pods exist; no sixth Pod appears after repeated reconciliation.

## Evidence

Preserve the API-store snapshot, controller-cycle log, object ownership graph, and final convergence report.

## Interpretation

Explain why the API server, Deployment controller, and ReplicaSet controller can each be healthy or unhealthy independently. Identify the earliest failed transition.

## Cleanup

Run `make clean`. If using kind, delete only the disposable cluster.

## Completion gate

Advance only after repeated post-recovery reconciliation leaves the same five-child state.
