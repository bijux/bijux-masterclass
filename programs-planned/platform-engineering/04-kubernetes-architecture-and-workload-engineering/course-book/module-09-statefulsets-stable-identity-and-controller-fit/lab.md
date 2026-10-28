# Lab — stable identity without false durability

## Goal

Observe which identities StatefulSet preserves and reject an unsupported data-durability claim.

## Safety boundary

Use the semantic StatefulSet model or a disposable kind namespace with lab-only sentinel data.

## Baseline

Create three sentinel replicas with OrderedReady and ephemeral storage. Record ordinal names, UIDs, and data files.

## Hypothesis

Deleting ordinal 1 creates a replacement named `atlas-sentinel-1` with a new UID and no ephemeral file. A partitioned template update changes only selected ordinals.

## Controlled action

1. Write one fixture file per ordinal.
2. Delete ordinal 1.
3. Record replacement identity and file state.
4. Apply a rolling-update partition of 2.
5. Observe which ordinal adopts the new template.

## Oracle

The name/ordinal persists, UID changes, ephemeral data is lost, and only ordinals at or above the partition update.

## Evidence

Preserve StatefulSet spec/status, Pod names/UIDs/templates, storage sources, update partition, readiness order, and the rejected durability claim.

## Interpretation

Separate controller identity, object lifetime, network identity, volume association, and application data correctness.

## Cleanup

Remove the sentinel resources and ephemeral data.

## Completion gate

Advance only after the final architecture record explains why Atlas API and worker remain Deployments.
