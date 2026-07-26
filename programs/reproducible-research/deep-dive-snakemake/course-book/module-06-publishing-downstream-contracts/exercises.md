# Exercises


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive Snakemake"]
  section["Publishing Downstream Contracts"]
  page["Exercises"]
  capstone["Capstone evidence"]

  family --> program --> section --> page
  page -.applies in.-> capstone
```

```mermaid
flowchart LR
  orient["Orient on the page map"] --> read["Read the main claim and examples"]
  read --> inspect["Inspect the related code, proof, or capstone surface"]
  inspect --> verify["Run or review the verification path"]
  verify --> apply["Apply the idea back to the module and capstone"]
```
<!-- page-maps:end -->

Use these exercises to practice publish judgment, not only publish vocabulary.

The strongest answers will make the downstream contract visible and defensible.

## Exercise 1: Separate internal state from the public bundle

You inherit a workflow with these outputs:

- `results/sample-a/qc.json`
- `results/sample-a/trim.json`
- `results/sample-b/qc.json`
- `logs/summarize.log`
- `publish/summary.tsv`
- `publish/report.html`

Write a short review note that explains:

- which files should remain internal
- which files could belong in the published contract
- what is still missing before the publish bundle is trustworthy

Your answer should justify the boundary rather than only list files.

## Exercise 2: Decide whether a change is compatible

A workflow currently publishes `publish/v1/summary.json`.

You are considering three changes:

1. add a new optional field to the JSON
2. rename the file to `published-summary.json`
3. remove an existing field because it seems redundant

Explain which of these may be compatible within `v1` and which should trigger a versioning
discussion.

## Exercise 3: Diagnose a weak integrity surface

A publish bundle contains:

- `summary.json`
- `report/index.html`

It does not contain:

- a manifest
- checksums
- provenance

Explain:

- what downstream trust questions this bundle cannot answer well
- why the report is not enough by itself
- what integrity surfaces you would add first

## Exercise 4: Clarify artifact roles

A team says:

> downstream users can scrape the report HTML, and maintainers can check the JSON if needed.

Write a short response that explains:

- why this is a weak contract design
- which artifact should be authoritative for machine use
- what role the report should play instead

## Exercise 5: Review publish drift

During a pull request review, you notice:

- `publish/v1/report/index.html` was renamed
- `manifest.json` was not updated
- a notebook in another repository reads from `results/`

Describe:

- the publish-boundary risks you see
- what should be repaired before approval
- whether this looks like a versioning discussion, a repair within the current version, or both

## Exercise 6: Build a minimal versioned bundle

Promote a machine-readable summary and a human report from internal results into
`publish/v1/`. Do not copy logs, scratch files, or unowned intermediates.

What to hand in:

- the internal and public trees
- an artifact-role table
- the rules that own publication
- an explanation of why each excluded file remains internal

## Exercise 7: Generate and verify a manifest

Create a manifest with relative paths, sizes, and SHA-256 checksums. Verify it from the
bundle root, then alter one byte in a published file and observe failure.

What to hand in:

- the manifest format and deterministic ordering rule
- successful and failed verification transcripts
- the corrupted path reported by the verifier
- an explanation of what checksum verification proves and does not prove

## Exercise 8: Write a downstream consumer test

Write a small program that receives only the bundle path, validates `summary.json`, and
uses one documented field. Prevent it from reading `results/` or repository configuration.

What to hand in:

- the consumer and schema
- a successful run against the bundle
- a failure against an invalid fixture
- one producer detail the consumer intentionally does not know

## Exercise 9: Classify compatible changes

Test an optional field addition, a required field addition, a type change, and a path
rename against the consumer from Exercise 8.

What to hand in:

- the outcome of each trial
- a compatibility classification with reasoning
- any schema or consumer adaptation needed
- the change that requires a new public version

## Exercise 10: Design a version migration

Create a `publish/v2/` contract for one deliberate breaking change while preserving a
clear route for existing `v1` consumers.

What to hand in:

- both contract trees
- a migration note and deprecation policy
- consumer tests for supported versions
- evidence that internal workflow layout is still not part of either API

## Mastery check

You have a strong grasp of this module if all ten answers consistently keep four ideas visible:

- internal workflow state is not automatically public
- publish paths and meanings are a contract
- manifests, checksums, provenance, and reports have different jobs
- downstream trust must be reviewed, not assumed
