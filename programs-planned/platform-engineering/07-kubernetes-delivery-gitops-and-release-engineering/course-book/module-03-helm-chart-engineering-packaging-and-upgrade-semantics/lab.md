# Laboratory — Break and repair a chart upgrade

## Goal

Evaluate a chart upgrade that introduces an unsafe value change and a non-idempotent migration hook.

## Safety boundary

Use the local chart and semantic release model. Do not point Helm at a shared cluster.

## Baseline

The accepted chart has a stable values API and deploys migration phases explicitly.

## Hypothesis

Renaming a required value without compatibility and hiding migration in a pre-upgrade hook should cause release rejection even when rendering succeeds.

## Controlled action

Create the candidate chart, render previous and new production values, run schema and upgrade checks, and simulate a failed main rollout after the hook commits.

## Oracle

The candidate is rejected for values incompatibility and unsafe side-effect ownership. The repaired candidate accepts both old and new values during a deprecation window and references a durable migration record.

## Required evidence

Save chart digests, values-schema results, rendered diffs, hook analysis, simulated side effects, and release decisions.

## Interpretation

A green `helm template` result proves only rendering. The release decision must explain compatibility and external effects.

## Cleanup

Restore the accepted chart, remove generated hook state, and prove the production render digest is unchanged.

## Completion gate

The learner can defend the chart API, dependency ownership, and upgrade boundary independently of Helm command success.
