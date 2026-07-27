# Review Checklist

Use this checklist when reviewing a Snakemake workflow, an exercise answer, or a
capstone change and you do not want the review to collapse into taste. A strong review
should end with a trust judgment, a boundary judgment, or a proof judgment. It should
not end with "this feels messy."

## The rule before the checklist

Start with one claim, not with the whole repository.

Examples of claims:

- this workflow change preserves publish trust
- this profile edit is policy-only
- this checkpoint keeps discovery reviewable
- this helper move clarifies ownership instead of hiding logic

If the claim is still vague, use a narrower review prompt before using the full
checklist.

## How to use this checklist

Work in this order:

1. write the claim under review in one sentence
2. choose the smallest section below that owns the claim
3. answer the questions with evidence, not guesses
4. end with a keep, change, or reject judgment

If you need to inspect five unrelated surfaces before answering one section, the real gap
is usually upstream in module understanding or proof-route choice.

## Workflow truth

Use this section when the claim is about what the workflow means or why it runs.

- Which file contracts are authoritative for this question?
- Would a dry-run still help a reviewer understand the workflow shape honestly?
- Does dynamic discovery leave durable evidence instead of runtime folklore?
- Are rule inputs, outputs, and targets explicit enough for another maintainer to reason
  from them without narration?
- Which artifact would prove the current rerun or non-rerun decision?

**Strong keep signal**

The claim can be explained from declared workflow contracts and reviewable evidence.

**Strong reject signal**

The workflow still depends on oral explanation, helper folklore, or runtime memory.

## Policy and operating context

Use this section when the claim is about profiles, executors, retries, storage, or
environment-specific behavior.

- Which differences belong to operating policy rather than workflow meaning?
- Does this profile or context change risk semantic drift?
- Would the same target still mean the same thing in local, CI, and scheduled contexts?
- Which changes affect cost, latency, or placement without changing analytical meaning?
- What evidence would prove that the context change is safe?

**Strong keep signal**

The workflow promise stays stable while execution context changes around it.

**Strong reject signal**

The context change silently alters the meaning of outputs, inputs, or expected behavior.

## Discovery and dynamic behavior

Use this section when the claim involves checkpoints, fan-out, or runtime-discovered
state.

- Which artifact records what discovery found?
- Can another maintainer inspect discovery without replaying the whole run?
- What would make you distrust the discovery result even if the run completed?
- Are wildcard limits and integrity checks explicit enough to prevent accidental fan-out?
- If logs disappeared, what file would still settle the discovery question?

**Strong keep signal**

Discovery changes the graph, but the changed graph remains reviewable after the run.

**Strong reject signal**

Discovery only makes sense while the terminal history is still visible.

## Publish trust

Use this section when the claim is about results, reports, bundles, manifests, or
downstream trust.

- Which outputs are safe for downstream trust and which remain internal run state?
- Does the published contract stay smaller and clearer than the whole repository?
- Which manifest, checksum, or report carries the real public contract?
- Could a downstream user understand what is stable without reading workflow internals?
- What evidence bundle should another maintainer inspect before approving change?

**Strong keep signal**

Public surfaces are explicit, smaller than the repository, and supported by durable
evidence.

**Strong reject signal**

Downstream trust still depends on knowing which files "usually matter."

## Ownership and layer boundaries

Use this section when the claim is about where behavior belongs.

- Which layer should own the next change: `Snakefile`, rules, modules, scripts, package
  code, or profiles?
- Is reusable code living in the right place instead of leaking workflow semantics into
  helpers?
- Would another maintainer know where this behavior belongs without oral explanation?
- Does the current structure clarify ownership or merely scatter the same meaning across
  more files?
- Which layer is authoritative for the behavior under review?

**Strong keep signal**

One layer clearly owns the behavior and adjacent layers consume rather than redefine it.

**Strong reject signal**

Multiple layers appear to co-own the same meaning and the split only looks cleaner.

## Incident and stewardship review

Use this section when the claim is about slowness, flakiness, migration, or long-lived
change.

- Which command or saved bundle gives the narrowest honest answer for the current claim?
- What failure class should be named before any repair begins?
- Which ambiguity must be made explicit before the workflow can be approved again?
- What evidence needs to survive the next change so trust is not reset to zero?
- Should this concern remain inside Snakemake at all?

**Strong keep signal**

The workflow can still defend itself under pressure and the next change preserves that
defense.

**Strong reject signal**

The proposed fix increases activity but decreases reviewability.

## What good review outcomes sound like

Good review outcomes usually sound like one of these:

- keep the current design because the boundary is explicit and the evidence is
  proportionate
- change one named surface because the current owner is wrong or too blurry
- reject the current claim because the workflow still cannot prove it honestly

If the outcome is only "this seems complicated," the review still needs sharper evidence.

## One honest example

Suppose a change moves a report helper into package code and also edits a profile.

A strong review does not say, "this looks more sophisticated now."

It asks:

1. does the helper move preserve the public contract and proof route
2. is the profile change really policy-only
3. which layer should own each edit
4. what keep, change, or reject judgment follows

That is the level of precision this checklist is meant to force.

## Companion pages

- [Boundary Review Prompts](boundary-review-prompts.md)
- [Anti-Pattern Atlas](anti-pattern-atlas.md)
- [Completion Rubric](completion-rubric.md)
- [Topic Boundaries](topic-boundaries.md)
