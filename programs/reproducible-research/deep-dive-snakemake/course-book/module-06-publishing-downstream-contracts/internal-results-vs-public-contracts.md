# Internal Results Versus Public Contracts

The first publishing decision is the most important one:

> which outputs belong to the workflow, and which outputs belong to the downstream world?

If that line is vague, the workflow becomes harder to review and downstream users are
forced to guess which files are safe to trust.

This page is about making that line explicit.

## How to use this page

Read this page with a real workflow tree in front of you.

You should be able to point at each file or directory and say one of these out loud:

- this exists so the workflow can keep running
- this exists so maintainers can inspect or debug the run
- this exists because a downstream user is allowed to trust it

If you cannot sort the tree that way, your publish boundary is not ready yet.

## A workflow usually produces more files than it should publish

A healthy workflow often creates many useful files:

- per-step logs
- benchmarks
- scratch intermediates
- per-sample result files
- validation artifacts
- final summaries and reports

Those files do not all make the same promise.

Some exist to help the workflow operate. Some exist to help maintainers review a run.
Some exist so another person or tool can rely on the results later.

Publishing begins when you decide which category a file belongs to.

## Internal state is still important, but it is not the public contract

Internal outputs are often necessary for:

- chaining rules together
- debugging failures
- inspecting detailed sample-level behavior
- supporting later aggregation

In the capstone, much of `results/` serves that purpose. It contains per-sample files that
help the workflow do its job, but it is not the main downstream promise.

That distinction matters because downstream consumers should not be forced to reverse
engineer the workflow layout to use the published results.

## Published outputs are an explicit promise

A published output says something stronger than "this file exists."

It says:

- this path is intentionally exposed
- this file meaning is stable enough for consumers to rely on
- this artifact belongs to a reviewable contract

That is why the capstone promotes a smaller surface under `publish/v1/`.

Files such as:

- `summary.json`
- `summary.tsv`
- `report/index.html`
- `manifest.json`
- `provenance.json`
- `discovered_samples.json`

are not just another directory. They are the deliberate public boundary.

## A practical sorting rule

When you are unsure whether a file belongs in the public bundle, ask these three
questions in order:

1. Would the workflow still need this file even if no downstream user ever saw it?
2. Would a maintainer mainly use this file to debug, inspect, or validate a run?
3. Would a downstream notebook, report pipeline, or external repository be justified in
   treating this file as a stable interface?

If the first or second answer is strongest, keep the file internal until you have a
clearer downstream reason.

If the third answer is strongest, you are no longer talking about a mere output. You are
talking about a contract.

## One simple contrast

```mermaid
flowchart LR
  results["results/"] --> internal["workflow-owned internal state"]
  publish["publish/v1/"] --> public["downstream-facing contract"]
  internal --> review["supports workflow execution and review"]
  public --> trust["supports downstream trust and reuse"]
```

This diagram matters because many publishing mistakes begin when both directories are
treated as if they made the same promise.

They do not.

## A concrete audit you should be able to perform

Imagine a repository with these artifacts after a run:

- `results/sample_A.tsv`
- `results/sample_B.tsv`
- `results/qc/coverage.png`
- `results/logs/aggregate.log`
- `publish/v1/summary.json`
- `publish/v1/report/index.html`

A strong learner should be able to say:

- the `results/` files help the workflow execute, inspect QC, or debug
- the `publish/v1/` files are intentionally promoted because a downstream consumer should
  not need to reverse engineer the internal layout
- the existence of a polished QC plot does not automatically make it part of the public
  contract

That is the beginning of publication discipline.

## A weak boundary

Weak shape:

- notebooks read directly from `results/`
- published files are chosen ad hoc after the run
- a path becomes “public” only because someone found it useful once

This feels flexible at first. It creates long-term fragility:

- internal layout changes break downstream use
- reviewers cannot tell which files are meant to stay stable
- publication discipline arrives only after confusion has already started

## A stronger boundary

Stronger shape:

- keep workflow-operational state under internal directories such as `results/`
- promote only the intended downstream artifacts into a versioned publish boundary
- treat every file inside that publish boundary as something a reviewer must be able to defend

That design gives both maintainers and consumers a clear answer to the same question:

> which files are safe to depend on?

## The beginner mistake to catch early

Many beginners think publishing means copying the most useful-looking files into a
`publish/` directory after the run.

That is still too producer-centered.

The real question is not which files feel important to the workflow author. The real
question is which files a downstream user should be encouraged to trust without learning
the internal workflow tree.

## A practical test

Ask these questions about any output:

1. Is this file mainly for the workflow to continue operating?
2. Is this file mainly for maintainers to debug or inspect a run?
3. Is this file intentionally exposed for downstream use?

If the answer is mostly the first or second, it probably does not belong in the publish
contract.

If the answer is the third, it needs stronger naming, stability, and review.

## Common failure modes

| Failure mode | What goes wrong | Better repair |
| --- | --- | --- |
| downstream notebooks read from `results/` | internal layout becomes a hidden public API | publish a smaller stable bundle and steer consumers there |
| publish directory copies too many internal files | contract grows without intention | publish only the outputs a consumer is meant to trust |
| reports are the only visible outputs | machine-readable contract becomes unclear | pair human-oriented reports with explicit machine-readable artifacts |
| logs or benchmarks leak into the public surface | consumers inherit maintenance noise | keep operational evidence separate from the downstream contract |
| no one can explain why a file is public | review becomes guesswork | require a clear downstream-use reason for promoted files |

## What a reviewer should hear

When a team promotes a file into `publish/v1/`, the explanation should sound like this:

> We are exposing this file because a downstream user needs a stable, documented surface
> for a real use case, and we do not want them reading internal `results/` paths.

If the explanation instead sounds like:

> We already had the file anyway, so we copied it over.

then the boundary is still accidental.

## The explanation a reviewer trusts

Strong explanation:

> these per-sample files remain under `results/` because they support workflow execution
> and detailed review, while `publish/v1/` contains the smaller bundle downstream users
> are allowed to trust as the stable contract.

Weak explanation:

> we copied the important files into `publish/` after the run finished.

The strong explanation defines ownership and intention. The weak explanation describes a
folder move without a contract.

## End-of-page checkpoint

Before leaving this page, you should be able to:

- explain why `results/` and `publish/v1/` make different promises
- give one example of an internal output that should not become public
- give one example of a file that belongs in the published contract
- explain why downstream consumers should not need to understand the whole workflow tree

If you still talk about publication mainly as "where final files go," keep working. The
stronger idea is that publication defines which outputs other people are allowed to rely
on.
