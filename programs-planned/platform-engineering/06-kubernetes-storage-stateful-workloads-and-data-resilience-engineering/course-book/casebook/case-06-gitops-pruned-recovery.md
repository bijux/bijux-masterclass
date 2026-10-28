# Case 6 — GitOps pruned the recovery copy

## Incident

A retained PVC and snapshot were removed from a repository after an application migration. The GitOps controller pruned both objects. The snapshot class used a Delete policy, so the backend recovery point was also removed.

## Evidence

- The application rollout was healthy.
- No retirement approval existed for the old data generation.
- Recovery resources were in the same ordinary reconciliation set as disposable workload objects.
- The controller acted exactly according to desired state.

## Failure

The desired-state system was given destructive authority without a data-retirement contract. Technical convergence conflicted with recovery governance.

## Correct response

Separate retained recovery assets from ordinary pruning, require explicit retirement intent and evidence, and use policies that preserve backend content until closure. Course 7’s handoff marks which resources are safe to reconcile automatically and which require controlled one-shot workflows.

## Lesson

Git is not a deletion approval system. Data transitions need identity, retention, authority, and irreversible-action gates beyond manifest absence.
