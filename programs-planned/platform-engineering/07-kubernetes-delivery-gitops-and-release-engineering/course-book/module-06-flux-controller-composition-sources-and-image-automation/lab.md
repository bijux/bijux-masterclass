# Laboratory — Trace a Flux reconciliation graph

## Goal

Follow a candidate through source artifact, Kustomization, HelmRelease, and image-automation resources and identify the first failed transition.

## Safety boundary

Use the semantic Flux fixtures or a disposable cluster. The image automation repository must be temporary.

## Baseline

All resources observe one immutable source and the dependency graph is Ready.

## Hypothesis

A stale generation, hidden substitution change, and unsafe direct-production image update should produce distinct failures.

## Controlled action

Inject each failure separately, collect conditions and revisions, then repair it. Attempt a concurrent human and automation Git update.

## Oracle

Diagnosis identifies the earliest failed resource. Hidden substitution is detected by render identity. Unsafe production write is rejected. Concurrent updates preserve history.

## Required evidence

Save source artifact status, dependency graph, conditions, render digests, Git commits, and release decisions.

## Interpretation

If only the final workload condition is inspected, the evidence is incomplete. The controller graph should explain causality.

## Cleanup

Restore the accepted source, remove temporary credentials and repository, and prove all reconcilers return to no-op Ready state.

## Completion gate

The learner can compare Flux and Argo CD without confusing implementation structure with the GitOps principles.
