# Lab 02 — The claim that bound in the wrong zone

## Goal

Demonstrate why immediate provisioning can conflict with scheduling and why manual prebinding can worsen the state.

## Safety boundary

Run only in the course workspace or an explicitly disposable cluster and storage account. Do not force detach, delete retained volumes, modify snapshot classes, or restore over an authoritative environment. Record the target context before every destructive command.

## Baseline

Create two zones, a zonal class, one pod constraint, and an unbound claim.

## Hypothesis

The module’s governing invariant should predict the result before the failure is injected. Write that prediction and the first object or record expected to diverge.

## Controlled action

Provision immediately in the incompatible zone, observe rejection, reset, then bind through waitforfirstconsumer.

## Oracle

The delayed path produces a volume in the selected topology while the immediate path preserves an explicit unschedulable explanation.

## Required evidence

Binding transcript, claim/pv states, per-node predicate table, reclaim record.

## Interpretation

Explain why the observed result supports or falsifies the hypothesis. Separate Kubernetes object state, controller state, backend state, filesystem state, and application state. Record any evidence class that remained unavailable.

## Cleanup

Delete synthetic resources through the semantic controller and verify retained data is inventoried.

## Completion gate

The lab is complete only when the failure is reproduced, the earliest missing transition is identified, the unsafe intervention is rejected, cleanup is verified, and the evidence artifact can be reviewed without relying on terminal history.
