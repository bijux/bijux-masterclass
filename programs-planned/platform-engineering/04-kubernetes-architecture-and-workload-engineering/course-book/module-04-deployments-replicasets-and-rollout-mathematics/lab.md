# Lab — diagnose a permanently unready revision

## Goal

Explain a stalled rollout using population mathematics and controller evidence, then perform a compatible rollback.

## Safety boundary

Use the semantic rollout model. The optional kind lane deploys only the course fixture in a disposable cluster.

## Baseline

Atlas API has three available old replicas with maxSurge one, maxUnavailable zero, and minReadySeconds ten.

## Hypothesis

A new revision whose readiness never succeeds creates one surge Pod, retains all old available replicas, and eventually reports a progress-deadline condition without automatically rolling back.

## Controlled action

1. Submit a new image/config revision with a missing required key.
2. Advance scheduler, kubelet, probe, and Deployment reconciliation cycles.
3. Record every replica population and condition transition.
4. Restore the previous compatible template.

## Oracle

The broken revision never becomes available; old replicas remain. The controller reports stalled progress. Rollback returns to three available replicas without exceeding surge bounds.

## Evidence

Preserve templates, digests, rollout calculation, ReplicaSet populations, Pod readiness reasons, Deployment conditions, and rollback compatibility record.

## Interpretation

Identify why apply success, updated replicas, ready replicas, and available replicas are different claims.

## Cleanup

Remove semantic output or the disposable kind cluster.

## Completion gate

Advance only after the report identifies the earliest failed transition and proves the availability bound throughout the exercise.
