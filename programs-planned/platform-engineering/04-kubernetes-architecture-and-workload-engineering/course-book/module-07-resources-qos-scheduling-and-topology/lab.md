# Lab — explain an impossible scheduling decision

## Goal

Identify every failed scheduler predicate and choose the minimum safe repair.

## Safety boundary

Use the semantic scheduler. The optional kind lane may label disposable Nodes but must not modify a shared cluster.

## Baseline

Create three Nodes with different capacity, labels, and taints. Confirm that the baseline Atlas API replicas can schedule.

## Hypothesis

Adding a large CPU request, hard general-pool affinity, strict hostname anti-affinity, and three-domain spread produces no feasible Node even though one Node has enough raw CPU.

## Controlled action

1. Submit the constrained Pod.
2. Record filter reasons for every Node.
3. Test candidate repairs one at a time: request change, capacity addition, affinity change, spread relaxation.
4. Reject repairs that violate the stated workload policy.

## Oracle

The initial Pod remains unscheduled with complete reasons. Exactly one selected repair restores feasibility while preserving the documented dedicated-node and failure-domain intent.

## Evidence

Preserve Node inventory, Pod request/constraints, per-Node filter results, chosen repair, rejected alternatives, and residual availability risk.

## Interpretation

Explain why deleting the Pending Pod or adding a toleration alone would not fix the constraints.

## Cleanup

Remove semantic state or restore disposable Node labels/taints and delete the kind cluster.

## Completion gate

Advance only after another learner can reproduce the scheduling decision from the recorded inputs.
