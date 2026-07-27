# Provenance, Manifests, and Publish Boundaries

Discovery is only half the problem.

Once the workflow has learned a changing set of samples, another question appears:

> where does that fact live after the run, and which later consumer is allowed to trust it?

This page answers that question.

## How to read this page

Read this page with one pressure in mind:

> after a dynamic run finishes, which files are allowed to explain the run to someone who
> did not watch it happen?

If you keep that question visible, provenance and manifests stop sounding like bureaucracy
and start sounding like the final part of discovery honesty.

## Why this lesson belongs in Module 02

Dynamic DAGs create a special review burden. The run is no longer just "here are the
results." It is also "here is why these exact units became results at all."

That is why this lesson belongs in the same day as discovery and checkpoints:

- discovery decides what the workflow found
- checkpoints may change which jobs exist
- provenance and manifests preserve those facts at the public boundary

## Internal execution state is not automatically a public contract

Many workflows create useful files during execution:

- discovered sample registries
- per-sample summaries
- logs
- benchmarks
- intermediate reports

Those files may be valuable without all being safe to publish as downstream truth.

Module 02 wants a clean separation:

- internal workflow state helps the run remain inspectable
- published outputs define what downstream users may rely on

If you blur those together, review becomes harder.

## The three artifact roles

### 1. Discovery artifacts

These answer:

- what did the workflow discover
- from which declared surface
- in what normalized order

Typical example:

- `results/discovery/accepted_samples.json`
- `results/discovery/rejected_samples.json`

### 2. Provenance artifacts

These answer:

- what configuration actually ran
- which software or workflow version produced the outputs
- which runtime identity matters for review

Typical example:

- `publish/v1/provenance.json`

### 3. Publish artifacts

These answer:

- which outputs are now part of the downstream contract
- where they live
- how a reviewer can verify the published bundle

Typical examples:

- `publish/v1/accepted_samples.json`
- `publish/v1/rejected_samples.json`
- `publish/v1/manifest.json`
- `publish/v1/report/index.html`

The names can vary. The separation of roles should not.

## A quick self-check before you keep reading

Imagine a reviewer opens only `publish/v1/`.

Could they answer all of these without rummaging through internal execution state?

- what the workflow discovered
- what configuration and run identity produced the bundle
- which files are officially part of the contract

If not, the publish boundary is probably still underspecified.

## Why accepted and rejected discovery evidence deserves special treatment

The discovered sample set is not just one more intermediate file.

In a dynamic workflow it often explains:

- why certain jobs existed at all
- why some downstream outputs are present
- why some candidates never became downstream outputs
- why the publish surface contains the sample families it does

If those artifacts disappear or stay private forever, the run story becomes harder to
reconstruct.

That is why the capstone carries discovery into the publish boundary instead of treating it
as disposable setup state.

## A healthy boundary

```mermaid
flowchart LR
  manifest["config/samples.tsv"] --> raw["declared raw evidence"]
  raw --> accepted["results/discovery/accepted_samples.json"]
  raw --> rejected["results/discovery/rejected_samples.json"]
  accepted --> results["results/{sample}/..."]
  results --> publish["publish/v1/"]
  accepted --> publish
  rejected --> publish
  publish --> manifest["manifest.json"]
  publish --> provenance["provenance.json"]
```

This design does something subtle but important:

- dynamic discovery remains visible inside the run
- both accepted and rejected decisions are preserved at the public boundary
- manifest and provenance make the publish surface reviewable as a set

## A strong beginner habit

Do not wait until the end of a project to think about provenance and manifests.

If the workflow is already dynamic in Module 02, start teaching the habit here:

- discovery should be durable
- public outputs should be enumerated
- run identity should be explained while the workflow is still small enough to inspect

## What belongs in accepted and rejected discovery artifacts

A weak registry usually lists only names.

A stronger registry records enough context for later review, for example:

```json
{
  "schema_version": 1,
  "declared_source": "config/samples.tsv",
  "samples": [
    {
      "sample": "sampleA",
      "path": "data/raw/sampleA.fastq.gz"
    }
  ]
}
```

When rejection is possible, keep a companion record that explains non-membership too:

```json
{
  "schema_version": 1,
  "declared_source": "config/samples.tsv",
  "samples": [
    {
      "sample": "sampleB",
      "path": "data/raw/sampleB.fastq.gz",
      "reason": "empty input file"
    }
  ]
}
```

The exact schema is up to the workflow. The lesson is that the discovered set should be
specific enough to answer later review questions without forcing a second raw-data scan.

## What belongs in provenance

Provenance should capture resolved run facts, not vague aspirations.

Typical examples:

- the materialized config used for the run
- the Snakemake version
- the workflow commit or repository state
- the profile or execution context that matters for interpretation

This page is not asking for maximal metadata. It is asking for enough evidence to explain
what run produced the published boundary.

## The common beginner mistake

A common mistake is to think a timestamp alone counts as provenance.

It does not.

A timestamp may tell you *when* something happened, but not:

- which semantic configuration was resolved
- which workflow revision produced the output
- which operating context mattered for interpretation

## Why manifests matter

A manifest gives the publish boundary a durable inventory.

That usually means:

- which files belong to the boundary
- where they are relative to the publish root
- an integrity surface such as checksums or hashes

Without a manifest, a publish directory is often just a bag of files someone hopes is
complete.

With a manifest, the boundary becomes reviewable as a declared set.

## What a good Module 02 explanation sounds like

Strong:

> The run writes accepted and rejected discovery records, one provenance record, and one
> manifest so the publish bundle explains both its membership decisions and its origin.

Weak:

> We kept some extra JSON files for debugging.

## One useful publication pattern

Use the workflow in two stages:

1. produce internal execution artifacts under `results/`
2. promote selected artifacts into `publish/v1/`

That pattern makes review easier because it answers two different questions cleanly:

- what did the workflow need to run correctly
- what may a downstream consumer trust later

Those questions overlap, but they are not identical.

## Common integrity mistakes

| Mistake | Why it hurts | Better repair |
| --- | --- | --- |
| accepted or rejected discovery evidence is overwritten or discarded | later review cannot explain the DAG membership decisions | keep the discovery records as durable run artifacts |
| publish boundary omits discovery | downstream users cannot tell why sample outputs exist or why others are missing | promote accepted and rejected records into the publish bundle |
| provenance captures only a timestamp | run identity stays vague | record resolved config and software identity too |
| publish directory has no inventory | reviewers cannot tell what belongs there | add a manifest with explicit paths and checksums |
| internal and public files share the same location with no distinction | ownership and review scope blur together | keep `results/` and `publish/` responsibilities separate |

## The explanation a reviewer trusts

Strong explanation:

> the workflow records accepted candidates in `results/discovery/accepted_samples.json`,
> records rejected candidates in `results/discovery/rejected_samples.json`, publishes
> reviewed copies at `publish/v1/accepted_samples.json` and
> `publish/v1/rejected_samples.json`, records run identity in
> `publish/v1/provenance.json`, and inventories the bundle in
> `publish/v1/manifest.json`, so a reviewer can explain both why the DAG changed and what
> the public contract now contains.

Weak explanation:

> we keep a few JSON files around for debugging.

The strong version names ownership and trust. The weak version treats integrity as
optional decoration.

## End-of-page checkpoint

Before leaving this page, you should be able to:

- distinguish discovery artifacts from provenance artifacts from publish artifacts
- explain why accepted and rejected discovery records may belong both inside the run and at the publish boundary
- describe what a manifest adds that a directory listing does not
- explain why internal execution state should not automatically become the public contract
