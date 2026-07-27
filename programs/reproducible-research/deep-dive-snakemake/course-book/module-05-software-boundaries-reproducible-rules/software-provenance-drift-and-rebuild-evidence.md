# Software Provenance, Drift, and Rebuild Evidence

Software boundaries are only half the story.

The other half is proving what changed when the software changes.

That matters because a workflow can become non-reproducible even when the file graph still
looks correct.

If a helper script, package function, environment file, or container image changes, the
repository needs a credible way to explain:

- what changed
- which outputs are now questionable
- what should be rebuilt
- what evidence will travel with the rebuilt results

That is the job of software provenance.

## How to read this page

Read this page with one trust question in mind:

> if the input files stayed the same, what software evidence would still justify rebuilding
> this output?

That is the question provenance answers. The page is not about extra metadata for its own
 sake. It is about defending rebuilds later.

## Why this lesson belongs in Module 05

Once the repository has scripts, package code, and runtime declarations, it also has more
ways for outputs to become stale without any input-file churn.

That is why provenance belongs in the same day as software ownership:

- ownership tells you which surface changed
- runtime contracts tell you where execution meaning lives
- provenance tells you how to defend the new artifact after the rebuild

## Drift does not begin only with input files

Learners often first meet Snakemake through file timestamps and declared dependencies.

That is a useful start, but it is incomplete.

Drift can also come from:

- edits to workflow scripts
- changes in package code under `src/`
- runtime declaration changes in environment files
- container image revisions
- tool upgrades that alter behavior without changing rule syntax

This is why software boundaries must stay explicit. You cannot review or rebuild what you
cannot name.

## A strong beginner habit

When software changes, ask two questions immediately:

1. which outputs might now be semantically stale
2. which evidence will let another maintainer understand the rebuild later

That habit is more important than memorizing every provenance field on day one.

## Reproducibility needs change evidence

A strong repository can answer questions like:

- did a software change invalidate published outputs?
- which rules are affected by a helper-code edit?
- what runtime changed between two runs?
- can we explain the software surface that produced this artifact?

Those are not luxury questions. They are the practical questions of trust.

## A quick self-check before you keep reading

Imagine this situation:

- the input data has not changed since last week
- the reporting helper changed this morning

Should you trust the old published summary automatically?

No. The software surface changed, and provenance is what keeps that change reviewable.

## One useful review loop

```mermaid
flowchart LR
  change["software change"] --> detect["detect affected rules or outputs"]
  detect --> rebuild["rebuild what is no longer trustworthy"]
  rebuild --> record["record provenance with the new artifact"]
  record --> review["review what changed and why"]
```

This loop is what turns reproducibility from a slogan into a working practice.

## What counts as software evidence

Good software evidence often includes:

- the git revision or release identifier of the repository
- the environment or container declaration used for execution
- tool or interpreter versions that materially affect behavior
- a provenance artifact that travels with published results

In the capstone, `workflow/scripts/provenance.py` points toward this idea. A workflow step
can emit an artifact that explains the software context of the publication outputs.

That is much stronger than relying on memory or a comment in a pull request.

## The common beginner mistake

People often assume provenance matters only for inputs, timestamps, or external data
identity.

Module 05 needs the opposite instinct:

- software changes are part of output meaning
- runtime changes are part of output meaning
- published outputs need to carry enough context to defend those facts later

## File freshness is not enough

Weak assumption:

> if the inputs are unchanged, the outputs are still trustworthy.

That assumption fails when:

- a script's transformation logic changes
- a library upgrade alters ordering, formatting, or statistical behavior
- a package helper fixes a bug that changes output meaning

The files may look fresh while the meaning is stale.

That is drift.

## The contrast that matters

The important contrast is not:

- old file
- new file

The important contrast is:

- unchanged bytes on disk
- changed software meaning behind those bytes

## A stronger practice

Stronger shape:

- keep software surfaces explicit enough that a reviewer can name them
- treat code and runtime changes as reasons to re-evaluate output trust
- generate provenance artifacts for outputs that will be shared or published
- use rebuild-oriented review commands when software changes are suspected

In practice, this is where commands such as `--list-changes code` or broader provenance
checks become valuable. They help the team connect software edits to output risk.

## What a good explanation sounds like

Strong:

> The input data stayed the same, but the software surface moved, so the old publication is
> stale until the repository rebuilds it and records the new runtime and revision context.

Weak:

> The files looked current, so we assumed they still were.

## A simple example

Imagine this sequence:

1. `src/capstone/reporting.py` changes how summary statistics are rounded.
2. No input files change.
3. Published tables still exist from the earlier run.

If the team only checks input freshness, those tables may appear valid.

If the team treats software as part of workflow meaning, it asks a better question:

> which outputs were produced with the old implementation, and where is the evidence for
> the new build?

That question is the difference between accidental and intentional reproducibility.

## Common failure modes

| Failure mode | What goes wrong | Better repair |
| --- | --- | --- |
| provenance only records input files | software drift stays invisible | record software context for important outputs |
| helper-code edits are treated as “internal only” | stale publications survive longer than they should | review software edits as output-affecting changes |
| environment updates are merged without rebuild thinking | runs become incomparable | connect runtime changes to rebuild and release review |
| publication artifacts omit software identity | external readers cannot trace the producing surface | emit provenance next to important deliverables |
| teams trust memory over recorded evidence | review becomes anecdotal | prefer generated evidence and versioned declarations |

## The explanation a reviewer trusts

Strong explanation:

> this output was rebuilt because the reporting helper changed under `src/`, and the new
> publication includes updated provenance that records the runtime and repository state.

Weak explanation:

> the code changed a bit, but the files looked current.

The first explanation defends trust. The second confuses absence of file churn with
absence of semantic drift.

## End-of-page checkpoint

Before leaving this page, you should be able to:

- explain how software drift differs from input drift
- name at least three kinds of software evidence worth keeping
- describe why published outputs need provenance that includes software context
- explain why unchanged input files do not guarantee trustworthy outputs
