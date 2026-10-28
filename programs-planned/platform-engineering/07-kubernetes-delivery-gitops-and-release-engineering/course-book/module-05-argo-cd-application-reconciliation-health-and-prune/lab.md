# Laboratory — Reconcile, drift, order, and protect

## Goal

Exercise an Application-style inventory through sync, health, drift repair, sync waves, and prune rejection.

## Safety boundary

Use the semantic Argo lane or a disposable local cluster. Protected Course 6 resources must remain synthetic or disposable.

## Baseline

The accepted production revision has stable inventory and all gates pass.

## Hypothesis

A controller should repair ordinary workload drift, respect ordering, report stale custom-resource health, and refuse protected-resource prune.

## Controlled action

Apply the candidate, mutate one owned field, make one custom-resource status stale, remove a protected snapshot content from source, and execute the wave plan.

## Oracle

Owned drift is repaired, stale health blocks release, protected prune is rejected, and wave ordering is visible without claiming atomic rollback.

## Required evidence

Save desired/live diffs, inventory, health conditions, wave execution, prune decision, and no-op steady-state writes.

## Interpretation

If the Application becomes Healthy while observed generation is stale, the health rule is unsound. If protected resources disappear, prune authority is too broad.

## Cleanup

Restore source and status fixtures, close the release record, and prove zero writes at steady state.

## Completion gate

The learner can explain the Application inventory and every non-green status without relying on the UI alone.
