# Laboratory — Prove render identity and overlay limits

## Goal

Render dev, staging, and production; detect an unsafe selector mutation and a mutable remote source.

## Safety boundary

Use the checked fixtures and semantic renderer. Native Kustomize is optional. No live cluster is required.

## Baseline

All overlays render deterministically and differ only in approved environment-owned fields.

## Hypothesis

A selector patch and a branch-pinned remote base should fail release review even when the YAML parses.

## Controlled action

Render all environments twice. Introduce the selector mutation and remote branch reference. Generate source diffs, render diffs, identity sets, and digests.

## Oracle

Clean renders are byte-equivalent across repeated runs. The selector mutation is rejected by the overlay field policy. The mutable remote reference is classified as non-reproducible.

## Required evidence

Save renderer version, input identities, output resources, canonical digest, field-policy result, and both rejected defects.

## Interpretation

A successful parse is not sufficient. The important evidence is the exact object change and why the environment overlay lacks authority to make it.

## Cleanup

Remove the defects and prove that production render returns to the accepted digest.

## Completion gate

The learner can reproduce all three environment renders from immutable inputs and explain every environment difference.
