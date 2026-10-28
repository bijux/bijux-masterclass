# Laboratory — Run the Atlas delivery incident defense

## Goal

Resolve a compound incident involving a moved image tag, protected-resource prune, canary segment failure, and repository outage.

## Safety boundary

Use the complete semantic capstone and disposable local Git repositories. Do not use real credentials or production clusters.

## Baseline

Production runs the accepted revision. All release records and recovery gates are current.

## Hypothesis

A sound delivery plane should reject the mutable artifact, block prune, abort the canary, preserve last-known-good state during source outage, and return emergency state to reviewed Git.

## Controlled action

Execute the staged incident timeline, assign roles, collect evidence, make categorical decisions, recover controller and repository state, and publish the Course 8 handoff.

## Oracle

No protected data is deleted; no unverified artifact reaches production; the harmed tenant segment triggers abort; source outage does not create empty desired state; final reconciliation is a no-op against a reviewed commit.

## Required evidence

Save the incident timeline, role decisions, source/artifact/render/live identities, prune and canary results, credential events, final release dossier, and handoff manifest.

## Interpretation

The defense should explain why each attractive shortcut was rejected. Tool output without ownership and evidence reasoning is insufficient.

## Cleanup

Remove temporary repositories and credentials, restore accepted desired state, run full course proof, and verify exact manifests.

## Completion gate

All non-compensable gates pass, the incident is closed with no unmanaged drift, and the Course 8 handoff verifies byte-for-byte.
