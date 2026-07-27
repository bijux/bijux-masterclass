# Boundary Review Prompts

Use this page when a workflow review feels blurry and you need sharper keep, change, or
reject questions. The goal is not to produce longer review notes. The goal is to force a
clear decision about which layer should own behavior and which evidence is strong enough
to trust.

## Before you start

Pick one boundary only. Good candidates are:

- workflow meaning versus execution policy
- discovery logic versus discovery evidence
- public publish contract versus internal run state
- `Snakefile` versus helper script ownership
- repository module boundary versus cross-cutting coupling

If you review more than one boundary at once, your conclusion will usually collapse into
"this area feels messy."

## The one-sentence test

Your review should end with one sentence that starts with one of these:

- keep this boundary because...
- change this boundary because...
- reject this boundary because...

If you cannot finish one of those sentences, the review is still descriptive rather than
decisive.

## Workflow meaning versus execution policy

Use these prompts when the question is whether a change belongs in workflow code, config,
or profile policy.

- Does this change alter analytical meaning or only operating context?
- Would a dry-run reveal the important behavior honestly?
- If this profile disappeared, what meaning would the workflow still preserve?
- Which values are allowed to vary across local, CI, and cluster contexts?
- Has an executor, storage, or retry choice started deciding what counts as the result?

**Strong keep signal**

The workflow contract stays the same while profiles only shape where and how work runs.

**Strong reject signal**

Different profiles now imply different public answers, targets, or wildcard meaning.

## Discovery logic versus discovery evidence

Use these prompts when a checkpoint or runtime discovery step feels clever but hard to
audit.

- Which artifact records the discovered set durably?
- Can another maintainer inspect discovery without replaying the whole run?
- If logs vanished, what file would settle the discovery question?
- Does the checkpoint expose a reviewable staged contract, or only runtime behavior?
- What would make you conclude that the discovery boundary is still folklore?

**Strong keep signal**

The discovered set is explicit, inspectable, and tied to the workflow contract.

**Strong reject signal**

The graph changes in real life, but the reason for that change survives only in memory or
terminal output.

## Publish boundary versus internal run state

Use these prompts when outputs exist but downstream trust still feels weak.

- Which outputs are public, and which are only internal scaffolding?
- Can a downstream user tell what is stable without reading repository internals?
- Which file, manifest, or report defines the public contract?
- Are scratch files and publishable artifacts mixed together?
- What ambiguity would make you refuse to approve this publish surface?

**Strong keep signal**

The publish bundle is smaller than the repository and carries its own trust evidence.

**Strong reject signal**

Trust depends on knowing which files "usually matter" instead of on a stable published
interface.

## Workflow layer ownership

Use these prompts when the question is where behavior should live.

- Should this behavior live in `Snakefile`, rules, modules, scripts, package code, or
  profiles?
- Which layer can express the behavior most honestly with the least hidden coupling?
- Would moving it make the workflow easier to review or only more indirect?
- Which layer should own the invariants for this behavior a year from now?
- If a bug appears here again, which file would you expect to inspect first?

**Strong keep signal**

One layer has clear ownership, and adjacent layers only consume the contract.

**Strong reject signal**

Multiple layers appear to co-own the same meaning, and reviewers need folklore to decide
where a change belongs.

## Repository boundary prompts

Use these prompts when a module split or architectural change is under review.

- Does the split create a clearer file API or only more files?
- Which module now owns the next likely change in this area?
- What coupling still crosses the proposed boundary?
- Is the entrypoint easier to trust after the split?
- Would a new maintainer find the right surface faster or slower?

**Strong keep signal**

The split gives each area a smaller, durable responsibility and reduces search cost.

**Strong reject signal**

The repository is more fragmented, but ownership is not more legible.

## Evidence authority prompts

Use these when the disagreement is about what should settle the review.

- Which surface is actually allowed to answer this trust question?
- Is the claim being supported by workflow contracts, durable artifacts, or only runtime
  memory?
- Would the repository remain reviewable if logs disappeared?
- Are you looking at the smallest honest proof route, or just the loudest one?
- Which artifact should still matter three weeks from now?

## What strong review notes sound like

Prefer review notes like these:

- "change this boundary because the profile is now choosing semantic inputs"
- "keep this boundary because discovery is recorded in a durable registry"
- "reject this publish surface because downstream trust still depends on internal
  scratch files"

Avoid notes like these:

- "seems confusing"
- "feels over-engineered"
- "maybe split this more"

Those reactions may be accurate, but they do not help the next decision.

## Escalation signs

Pause and widen the audit if:

- one boundary failure appears to be causing another
- the best answer depends on unpublished runtime state
- local and CI reviews would reach different conclusions
- the repository can no longer name who owns the fix

At that point, review the companion pages before editing code.

## Companion pages

- [Anti-Pattern Atlas](anti-pattern-atlas.md)
- [Review Checklist](review-checklist.md)
- [Self-Review Prompts](self-review-prompts.md)
- [Module Dependency Map](module-dependency-map.md)
