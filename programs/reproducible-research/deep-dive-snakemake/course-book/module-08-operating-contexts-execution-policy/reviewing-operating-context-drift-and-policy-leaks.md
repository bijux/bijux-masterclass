# Reviewing Operating-Context Drift and Policy Leaks

Operating-context drift is rarely dramatic at first.

It usually arrives through small decisions that seem harmless:

- one more profile-specific tweak
- one more context-specific path override
- one more retry increase
- one more undocumented storage assumption

This page is about catching those leaks before they rewrite workflow behavior by accident.

## How to use this page

Read this page as a review checklist, not as a general warning.

When you finish, you should be able to answer:

- what changed between contexts
- whether the change stayed inside policy
- whether the evidence still supports one stable workflow meaning

That is the practical skill this page is trying to build.

## Operating-context review is different from ordinary workflow review

A normal workflow review asks:

- does the DAG still make sense?
- do the rules still declare the right contracts?

An operating-context review asks:

- do different contexts still mean the same workflow?
- are profile differences still policy rather than semantics?
- are storage, failure, and visibility assumptions still explicit?

Those questions overlap, but they are not the same.

## Drift becomes visible when contexts are compared side by side

The capstone's `profile-audit` route is valuable because it compares:

- profile config files
- dry-runs under multiple contexts
- review questions about policy versus meaning

That is exactly the right posture.

Drift stays harder to see when each context is inspected in isolation.

## Start from invariants before differences

The most common review mistake is to start by cataloging every environment difference.

A stronger review starts like this:

1. name the semantic invariants
2. compare dry-runs or planned work across contexts
3. classify each remaining difference as policy or leak
4. escalate leaks into workflow, config, or contract review

This order matters because without invariants, the review becomes a loose inventory
instead of a boundary check.

## One useful review loop

```mermaid
flowchart LR
  change["profile or context change"] --> compare["compare policy files and dry-runs"]
  compare --> classify["policy difference or semantic leak?"]
  classify --> keep["keep as operating policy"]
  classify --> escalate["escalate to workflow, config, or contract review"]
```

This loop matters because context drift often hides behind the phrase “environment-specific
adjustment.”

## What to inspect first

Start with four practical questions:

1. Do the context differences stay within executor, logging, latency, or retry policy?
2. Did any context introduce different paths, different semantic config, or different trusted outputs?
3. Are failures being explained better, or merely retried more often?
4. Are storage and visibility assumptions named clearly enough for another maintainer to audit them?

These questions make policy leaks visible early.

## One concrete review scenario

Imagine this drift set:

- CI raises `jobs` and changes log visibility
- SLURM increases `latency-wait`
- one profile also swaps in a different semantic config and trusted output path

The first two can still be operating policy.

The third is a leak because context configuration is now redefining workflow meaning and
contract surfaces.

This is the kind of comparison that turns vague unease into a clear review finding.

## A weak review posture

Weak shape:

- profiles are approved one at a time with no cross-context comparison
- “works on the cluster” is treated as sufficient justification
- policy changes are merged before anyone asks whether the workflow meaning drifted

This lets execution context become a hidden author of workflow behavior.

## A stronger review posture

Stronger shape:

- compare local, CI, and scheduler contexts side by side
- treat policy differences as acceptable only when workflow meaning remains stable
- escalate suspicious differences into config, contract, or workflow review
- keep evidence bundles or review notes that explain why the drift is acceptable or not

Now the repository can move across contexts without losing its semantic center.

## The beginner mistake to catch early

Beginners often think side-by-side comparison is unnecessary because each environment is
"supposed to be different."

That is exactly why comparison matters.

Without explicit comparison, policy leaks get normalized as local realism instead of being
reviewed as boundary failures.

## Common failure modes

| Failure mode | Why it is risky | Better repair |
| --- | --- | --- |
| context-specific semantic knobs are hidden in profiles | one workflow becomes several hidden variants | move semantics into visible workflow or config surfaces |
| cluster migration relies on unreviewed storage differences | path trust changes without being named | audit filesystem and visibility assumptions explicitly |
| retries rise as contexts get noisier | deterministic defects stay mislabeled as transient | classify failure modes before altering policy |
| dry-runs are never compared across contexts | semantic drift stays invisible | compare planned work across local, CI, and scheduler profiles |
| policy review happens without evidence | context changes become anecdotal | use audit bundles, dry-runs, and guide routes as review evidence |

## What a reviewer should hear

A strong explanation sounds like this:

> We compared the contexts side by side, confirmed that dry-run meaning and trusted
> outputs stayed stable, and treated the remaining differences as executor, observability,
> storage, or retry policy only.

That is stronger than "each environment needs its own behavior," because it names what was
actually checked.

## The explanation a reviewer trusts

Strong explanation:

> these context differences remain operating policy because the dry-run plan, contract
> paths, config meaning, and trusted outputs stay stable across local, CI, and SLURM; the
> remaining differences are executor and observability policy only.

Weak explanation:

> each environment needs its own behavior, so exact comparison is not very useful.

The strong explanation checks invariants. The weak explanation excuses drift before it is
examined.

## End-of-page checkpoint

Before leaving this page, you should be able to:

- explain how operating-context review differs from ordinary workflow review
- name several signs of a policy leak
- explain why side-by-side dry-run comparison is valuable
- describe when a profile change should escalate into semantic review

If you still think context review is mostly operations housekeeping, revisit the page.
This module treats it as part of reproducibility review.
