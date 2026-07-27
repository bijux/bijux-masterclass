# Reviewing Publish Drift and Downstream Risk

The publish boundary deserves the same seriousness as code review.

If a workflow changes what it publishes, how it names files, or what those files mean,
downstream trust can break even when the workflow still runs successfully.

This page is about catching that drift before it becomes a downstream incident.

## How to use this page

Treat this page like a review checklist, not just a reading page.

When you finish, you should be able to sit in front of a publish-related change and ask:

- what changed in the public contract
- whether the old contract still holds
- what a downstream user would notice first
- whether the bundle evidence still supports trust

That is the teaching goal.

## Publish drift is not only about missing files

Drift can look obvious:

- a published path disappears
- a new file appears unexpectedly

But it can also be quieter:

- a JSON field changes meaning
- a report stops matching the structured summary
- the manifest no longer inventories the full contract
- a notebook begins reading from `results/` because the publish bundle stopped being enough

Those are all publish-review problems.

## A publish review asks a different question than a workflow run review

Workflow run review asks:

- did the jobs complete?
- did the pipeline behave as expected?

Publish review asks:

- what is safe for downstream consumers to rely on now?
- what changed in the public contract?
- what evidence supports trusting the bundle?

Those questions overlap, but they are not identical.

## Start from the downstream user, not the author

The easiest way to miss publish drift is to review from the producer's perspective only.

The author thinks:

- the workflow still succeeds
- the file move was small
- the report still looks fine

The downstream user experiences something else:

- their notebook cannot find the old path
- their parser reads the old field meaning
- their validation step no longer matches the manifest

Good publish review is the discipline of preferring the second perspective.

## One useful review loop

```mermaid
flowchart LR
  change["publish-related change"] --> inspect["inspect paths, payloads, and artifact roles"]
  inspect --> compare["compare against the current public promise"]
  compare --> decide["keep version, bump version, or reject change"]
  decide --> evidence["verify manifest, provenance, report, and contract docs align"]
```

This loop helps because teams often jump from “the workflow passed” straight to “the
publish bundle is fine.”

That jump is exactly where drift hides.

## What to inspect first

Start with four practical questions:

1. Did the set of published files change?
2. Did any stable path move, disappear, or get renamed?
3. Did the meaning of an existing artifact change?
4. Do the manifest, provenance, report, and file API still tell the same story?

These questions make downstream risk visible early.

## A short audit you should be able to run quickly

For any publish-related change, try this sequence:

1. list the public files that a consumer is allowed to trust
2. compare those files and their meanings with the previous promise
3. check whether the manifest, provenance, report, and contract note still align
4. decide whether the current version is still honest

If any of those steps becomes vague, the review is not done yet.

## Drift often arrives through convenience

Common convenience moves:

- “just publish this extra JSON too”
- “the report already shows it, so we can skip updating the contract docs”
- “we only renamed the file, the contents are the same”
- “consumers can read directly from `results/` until we clean this up later”

Each shortcut makes the public contract less deliberate.

## A stronger review posture

Strong shape:

- treat every change inside `publish/v1/` as reviewable contract surface
- compare structured artifacts, human-readable artifacts, and integrity artifacts together
- treat contract ambiguity as a real defect, not just a documentation gap
- version the publish boundary when the previous promise is no longer true

This makes downstream trust an engineering decision rather than an accident.

## The beginner mistake to catch early

Beginners often treat publish drift as a documentation chore.

That is too weak.

If the bundle contract is ambiguous, a downstream user can make the wrong decision even
when every workflow job passed. That makes ambiguity a correctness issue, not a cosmetic
issue.

## Common failure modes

| Failure mode | Why it is risky | Better repair |
| --- | --- | --- |
| new public artifacts added with no reason | bundle scope expands by drift | require a downstream-use case and contract explanation |
| published path renamed casually | consumers break even if payloads are unchanged | treat path changes as compatibility review events |
| report and summary disagree | humans and tools see different truths | regenerate or repair the surfaces until they align |
| manifest omits part of the public bundle | integrity review becomes incomplete | keep manifest coverage aligned with the publish contract |
| downstream code starts reading internal files again | hidden contract escapes the publish boundary | repair the publish bundle rather than normalizing the shortcut |

## What a reviewer should hear

A strong publish review sounds something like this:

> The workflow still runs, but that is not the only question. We checked the published
> paths, the artifact meanings, and the supporting manifest, provenance, and contract
> surfaces. The old downstream promise still holds, so this remains inside the current
> version.

Or, when it does not hold:

> The workflow still runs, but the downstream promise changed, so the current version is
> no longer honest.

That is the mindset this page is trying to build.

## The explanation a reviewer trusts

Strong explanation:

> this change keeps the current publish contract because the stable paths and meanings are
> intact, and the manifest, provenance, report, and file API still align; if any of those
> promises changed, we would treat it as a versioned contract change.

Weak explanation:

> the workflow still runs, so the published outputs are probably fine.

The strong explanation reviews the bundle as a contract. The weak explanation mistakes
workflow success for downstream trust.

## End-of-page checkpoint

Before leaving this page, you should be able to:

- explain how publish review differs from basic workflow run review
- name several forms of publish drift beyond missing files
- describe what should trigger compatibility or versioning discussion
- explain why contract ambiguity is a real downstream risk

If you still find yourself saying “the pipeline passed, so the publish bundle is probably
fine,” read the page again. This entire module is trying to break that habit.
