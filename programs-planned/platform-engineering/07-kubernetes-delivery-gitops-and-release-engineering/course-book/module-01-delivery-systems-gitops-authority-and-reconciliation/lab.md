# Laboratory — Classify drift before correcting it

## Goal

Create several kinds of divergence and prove that one global self-heal rule is insufficient.

## Safety boundary

Use the semantic Atlas cluster only. Do not perform direct edits on a shared or production cluster.

## Baseline

The accepted Atlas revision is synchronized. The application inventory contains workload resources and protected data resources.

## Hypothesis

Unauthorized changes to controller-owned fields should be repaired; protected-resource deletion and audited emergency drift should be escalated rather than blindly corrected.

## Controlled action

Apply four mutations: change a Deployment replica count, add an admission-owned label, remove a protected PVC from desired state, and add an emergency annotation while reconciliation is suspended. Run drift classification and reconciliation.

## Oracle

The replica drift is corrected, the admission-owned field is preserved, the PVC deletion is rejected, and emergency drift remains reported until a reviewed revision absorbs it.

## Required evidence

Save before/after resource documents, managed-field ownership, drift classifications, prune decision, and the final inventory.

## Interpretation

If every difference is force-corrected, ownership is too broad. If nothing is corrected, the controller is not enforcing desired state. The evidence should justify each distinct outcome.

## Cleanup

Restore the accepted desired revision, close the emergency record, resume reconciliation, and prove a no-op steady state.

## Completion gate

All four divergence classes receive distinct, defensible actions and the final reconciliation performs zero writes.
