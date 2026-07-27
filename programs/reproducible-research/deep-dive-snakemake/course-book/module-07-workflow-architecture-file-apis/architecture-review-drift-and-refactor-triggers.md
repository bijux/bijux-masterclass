# Architecture Review, Drift, and Refactor Triggers

Architecture rarely collapses all at once.

It drifts.

That drift usually looks small in the moment:

- one more include
- one more helper
- one more path nobody documents yet
- one more rule file with a vague name

This page is about recognizing when those small moves have become an architecture problem.

## How to use this page

Read this page as a review tool, not as a manifesto.

You should be able to sit in front of one repository change and answer:

- which boundary drifted
- whether the drift is architectural or merely stylistic
- whether the next action is repair, refactor, or deliberate deferral

That is the practical skill this page is trying to build.

## Architecture review asks whether the repository still teaches itself

At this stage, the key question is not only:

> does the workflow run?

It is also:

> could a new reviewer explain the repository shape without oral rescue?

That is the real architecture bar.

## Drift becomes visible before the workflow is huge

Warning signs often appear early:

- new contributors cannot find the entrypoint quickly
- file names and directories stop signaling ownership clearly
- contract docs lag behind path and workflow changes
- the rule graph is technically present, but helper layers are easier to inspect than the rules

These are architecture signals, not mere tidiness complaints.

## Start from review pain, not from mood

Beginners often say things like:

- "the repo feels messy"
- "the structure is getting weird"
- "we should clean this up soon"

Those feelings may be pointing at something real, but they are not yet reviewable.

A stronger architecture discussion names the failing boundary:

- the entrypoint no longer shows visible assembly
- the file API no longer matches the real path contract
- the helper layer is easier to inspect than the rules
- one rule family no longer represents a coherent concern

Once the pain is named that clearly, refactoring stops being subjective.

## Refactors should be triggered by review pain, not by aesthetics alone

A repository refactor is justified when it improves one of these things:

- ownership clarity
- path-contract clarity
- onboarding and review speed
- separation between orchestration, implementation, and policy

It is weaker when the main reason is:

- “the tree feels messy”
- “this helper file looks too long”
- “we prefer more folders”

Those may be symptoms, but they are not yet architectural reasons.

## One useful review loop

```mermaid
flowchart LR
  pressure["review or maintenance pain"] --> locate["locate the unclear boundary"]
  locate --> classify["entrypoint, rules, file API, helper, or policy surface?"]
  classify --> refactor["refactor only the boundary that is lying or overloaded"]
  refactor --> verify["update contract docs and review routes"]
```

This loop matters because large refactors often fail by changing several boundaries at
once without making any of them clearer.

## One concrete architecture audit

Pick one change that made the repository harder to review.

Then force yourself to classify it:

- entrypoint drift
- rule-family drift
- file-API drift
- helper-coupling drift
- policy or config drift

If you cannot classify it, you may still be reacting to general discomfort instead of a
specific boundary failure.

## Strong refactor triggers

Strong triggers include:

- one rule family can no longer be reviewed as a coherent unit
- path contracts have changed but are no longer visible in docs
- helper code now hides workflow meaning
- the top-level assembly no longer explains how the repository is composed
- one architectural surface is doing multiple jobs badly

Those are good reasons to change the repository shape.

## Weak refactor triggers

Weak triggers include:

- rearranging folders with no ownership gain
- introducing modules or abstractions before reuse is real
- renaming files only because another layout feels trendier

These often increase churn without improving architecture.

## The beginner mistake to catch early

The most common beginner mistake is to launch a broad refactor before identifying the
smallest lying boundary.

That usually creates two problems:

- many surfaces change at once
- reviewers cannot tell what actually improved

Architecture repair is strongest when it narrows the scope first, even if the eventual
cleanup is larger.

## Common failure modes

| Failure mode | Why it hurts | Better repair |
| --- | --- | --- |
| refactor changes too many layers at once | reviewers cannot see what improved | isolate the overloaded or misleading boundary first |
| docs are updated after the architecture drift has already spread | review stays reactive | treat doc drift as an architecture defect early |
| repository shape follows personal taste more than workflow boundaries | maintenance becomes subjective | refactor around ownership and contract questions |
| new structure hides the visible DAG further | readability drops despite cleaner folders | preserve a clear entrypoint and named rule families |
| teams normalize confusion because the workflow still runs | architecture debt becomes invisible | use onboarding and review pain as a real signal |

## What a reviewer should hear

A strong explanation sounds like this:

> We are refactoring this boundary because it no longer teaches the truth: the repository
> structure and the actual ownership or contract surface have drifted apart.

That is stronger than "we want to make the tree cleaner," because it tells the reviewer
what architectural lie is being repaired.

## The explanation a reviewer trusts

Strong explanation:

> this refactor is needed because the current boundary no longer tells the truth: the rule
> family has outgrown its ownership surface, the file API is lagging the real paths, and a
> reviewer can no longer explain the repository without opening unrelated helper layers.

Weak explanation:

> we reorganized the repository to make it cleaner.

The strong explanation identifies the failing boundary. The weak one names only a mood.

## End-of-page checkpoint

Before leaving this page, you should be able to:

- explain how architecture drift appears before dramatic breakage
- name several strong triggers for architectural refactoring
- distinguish review pain from mere style preference
- explain why documentation lag is itself an architecture problem

If you still reach for "cleanup" before you can name the failing boundary, revisit the
page. This module wants refactor decisions to be explainable, not just intuitive.
