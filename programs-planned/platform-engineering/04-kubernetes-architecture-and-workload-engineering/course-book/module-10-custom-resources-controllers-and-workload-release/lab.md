# Lab — build and break the AtlasWorkload controller

## Goal

Reconcile one custom resource into owned workload objects, then detect a status loop and finalizer failure.

## Safety boundary

Use the semantic controller and compiled Go reconciliation core. The optional kind lane installs only the course CRD/controller in a disposable cluster.

## Baseline

Create one AtlasWorkload with accepted digest references, configuration, replicas, and availability class. Reconcile to steady state.

## Hypothesis

Repeated reconciliation produces no object changes after convergence. A timestamp-on-every-cycle defect creates endless status writes. A cleanup authorization defect leaves deletion pending with a visible condition.

## Controlled action

1. Reconcile the valid object five times and record write count.
2. Enable the status-churn defect and repeat.
3. Repair semantic equality and transition times.
4. Delete the object with the release-reservation finalizer.
5. Inject cleanup denial, then restore authority and finish deletion.
6. Generate the Course 5 handoff.

## Oracle

Steady-state reconciliation produces zero writes. The defect is detected by repeated resource-version changes. Deletion remains pending during denied cleanup and completes exactly once after repair. Handoff files match their manifest.

## Evidence

Preserve CR generations, managed fields, child UIDs/owners, reconcile decisions, status diffs, finalizer events, release decision, and handoff manifest.

## Interpretation

Explain why controller success is a property of repeatable convergence and ownership, not the number of objects it can create.

## Cleanup

Remove semantic state or disposable CRD/controller/namespace after preserving evidence.

## Completion gate

Complete the final defense and pass all release gates before Course 5 handoff is accepted.
