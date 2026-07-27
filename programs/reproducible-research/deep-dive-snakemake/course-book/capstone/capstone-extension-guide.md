# Capstone Extension Guide

Use this guide when changing the Snakemake capstone after the course is already in use.
The goal is not to forbid growth. The goal is to keep new work from weakening the rule
contracts, policy boundaries, publish surface, and review evidence the course depends on.

This page is about safe extension under educational stewardship.

## The question this page should help you answer

The useful extension question is not:

> Can I make this change work?

It is:

> Which boundary is moving, and what proof burden comes with that move?

That is what keeps the capstone from quietly drifting away from the course it is supposed
to support.

## How to use this guide

Work in this order:

1. name the intended change
2. choose the owning boundary
3. classify the risk
4. run the minimum proof set
5. decide whether to keep, revise, or reject the change

If the change still sounds like "just a small tweak," pause until you can state which
boundary is actually moving.

## Extension route

```mermaid
flowchart TD
  change["name the intended change"] --> owner["choose the owning boundary"]
  owner --> risk["classify the risk"]
  risk --> proof["run the minimum proof set"]
  proof --> decision["keep, revise, or reject the change"]
```

## Start by deciding whether the change is really local

Beginners often describe a capstone change as if it only affects one file.

That is frequently false for workflow repositories.

The better question is:

> Which boundary is actually moving: rule contract, discovery behavior, policy surface,
> publish contract, or review evidence?

Once that is named, the proof burden becomes much clearer.

## Boundaries that must stay legible

These boundaries should remain explicit:

- rule contracts versus helper implementation code
- dynamic discovery versus hidden side effects
- operating policy versus workflow meaning
- internal execution state versus `publish/v1/`
- public contract versus broader repository convenience

If an extension makes one of those harder to explain, the capstone probably got worse.

## Usually safer kinds of change

These changes are often safe when reviewed carefully:

- adding a new internal rule with explicit inputs, outputs, and logs
- enriching the publish bundle without breaking existing promoted files
- extending profiles while keeping their meaning operational rather than semantic
- strengthening walkthrough, tour, or verification evidence
- improving review surfaces without widening the public contract

Safe does not mean unreviewed. It means the boundary being moved is narrower.

## Changes that need stronger review

These changes need stronger review:

- changing the meaning of an existing published artifact
- adding a checkpoint that hides moving targets instead of recording them
- moving analytical meaning into profile or executor-specific settings
- adding repository structure that buries the visible rule graph under indirection
- weakening saved evidence because the new route feels more convenient

Use [Capstone File Guide](capstone-file-guide.md) when the main question is where a
change belongs. Use [Capstone Review Worksheet](capstone-review-worksheet.md) when the
question is whether the current repository can still defend the change honestly.

## One honest extension judgment

Suppose a change adds a new published TSV and also moves one analytical threshold into a
profile.

That is not one simple extension.

It moves two sensitive boundaries:

1. the publish contract
2. the policy-versus-semantics split

This guide should make that visible early enough that the change gets stronger review
instead of being waved through as routine growth.

## Minimum proof after a meaningful change

After any meaningful capstone change, rerun:

1. `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-walkthrough`
2. `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-wf-dryrun`
3. `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-verify-report`
4. `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-tour`

If any of those become harder to explain, the repository likely got worse even if it
still runs.

Add stronger routes such as `proof` or `capstone-confirm` when the changed boundary is
already broad enough to justify them.

## Good extension questions

Ask these before accepting the change:

- which boundary now owns the new behavior
- which existing proof route would fail if the change were dishonest
- whether the publish surface became wider, blurrier, or semantically different
- whether another maintainer could review the change without oral history
- whether the capstone still teaches the course rather than only serving local
  convenience

## Good final outcomes

At the end of this guide, land on one of these:

- keep the change because the boundary and proof burden stayed explicit
- revise the change because the owner is right but the evidence is weak
- reject the change because it weakens contract clarity, policy boundaries, or publish
  trust

That is stronger than "the tests still pass."

## Companion pages

- [Capstone Architecture Guide](capstone-architecture-guide.md)
- [Capstone File Guide](capstone-file-guide.md)
- [Capstone Review Worksheet](capstone-review-worksheet.md)
- [Proof Matrix](../guides/proof-matrix.md)
