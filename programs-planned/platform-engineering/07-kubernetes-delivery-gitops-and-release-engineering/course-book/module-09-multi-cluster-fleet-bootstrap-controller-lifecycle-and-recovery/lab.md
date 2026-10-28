# Laboratory — Recover delivery after source and controller failure

## Goal

Reconstruct Atlas delivery state from a clean semantic cluster while separately handling repository and controller outages.

## Safety boundary

Use temporary repositories, synthetic credentials, and the semantic fleet. Do not alter a real cluster fleet.

## Baseline

Three clusters run one accepted revision and the controller catalogue is healthy.

## Hypothesis

Repository outage should preserve runtime state; controller reconstruction should restore the same desired revision and inventory without broad credentials or prune.

## Controlled action

Simulate repository outage, controller loss, clean controller bootstrap, credential restoration, and catalogue recovery. Inject an empty generator result during the outage.

## Oracle

Workloads remain. Source age becomes stale. Empty generation does not delete Applications. Recovered controllers converge to the exact prior revision and inventory.

## Required evidence

Save cluster catalogue, source age, controller versions, bootstrap identity lifetime, inventory digests, generator decision, and recovery timeline.

## Interpretation

If recovery depends only on Git, identify the missing credential or bootstrap assumption. If empty generation prunes state, source uncertainty is mishandled.

## Cleanup

Revoke bootstrap credentials, restore ordinary reconciliation, and prove no fleet-wide drift or pending deletion remains.

## Completion gate

The learner can explain which parts of fleet operation continue during each control-plane outage and how authority is restored safely.
