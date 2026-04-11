# Worked Example: Reviewing a DVC Repository for Stewardship

This example shows the final course skill: reviewing a DVC repository as a steward, not
only as a user.

The goal is to produce a review that leads to safe change.

## The situation

A maintainer asks:

> Is this DVC repository ready for another team to inherit?

The reviewer does not start with formatting. The reviewer starts with state contracts.

## Step 1: Inspect evidence surfaces

The reviewer opens:

- `dvc.yaml`
- `dvc.lock`
- `params.yaml`
- `metrics/metrics.json`
- `publish/v1/`
- recovery and review guides
- verification commands in the Makefile

The reviewer asks whether the files agree, not whether each file looks nice alone.

## Step 2: Write findings as contracts

Finding:

> The promoted release bundle has metrics and params, but no review note explains why the
> selected threshold is accepted.

Risk:

> A downstream consumer can read the result but cannot defend the promotion decision.

Repair:

> Add a release review note that names the threshold, metric tradeoff, baseline, and
> downstream contract.

That is a useful stewardship finding because it is evidence-based and repairable.

## Step 3: Plan one migration safely

The repository wants to move from `publish/v1/` to `registry/incident-escalation/v1/`.

The reviewer proposes:

1. Inventory current `publish/v1/` files and manifest.
2. Copy the same supported bundle to the new registry boundary.
3. Keep the old boundary temporarily.
4. Run release audit and recovery review.
5. Update consumer documentation.
6. Remove the old boundary only after the new contract is verified.

The plan moves one boundary and preserves rollback.

## Step 4: Add a governance rule

The reviewer writes:

> Any future registry or release boundary change must include a manifest, matching params
> and metrics, a review note, and a passing release audit route.

This rule is small and directly tied to the problem found.

## Step 5: Decide tool ownership

The review closes with ownership:

> DVC should continue to own artifact lineage, params, metrics, lock evidence, and
> recovery of tracked outputs. The external registry should own consumer-facing lifecycle
> and deployment approval, but it must preserve links back to DVC evidence.

That division gives the next team a map.

## The final review note

> The repository has a workable DVC state model, but the release boundary needs stronger
> stewardship before handoff. The main repair is to add promotion rationale and manifest
> checks to the release review route. The proposed migration to a registry boundary should
> move only the promoted bundle first, keep `publish/v1/` temporarily, and verify recovery
> before changing consumer documentation. DVC remains the authority for artifact lineage;
> the registry should own consumer lifecycle.

## Why this is a mastery example

This one story exercises the whole module:

- Core 1: review began with evidence surfaces
- Core 2: migration moved one boundary with rollback
- Core 3: governance came from a real recurring risk
- Core 4: vague promotion was treated as an anti-pattern
- Core 5: tool ownership was split deliberately

The course ends with stewardship because reproducibility survives through reviewable
decisions, not only through commands.
