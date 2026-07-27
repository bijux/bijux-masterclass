# Reports, File APIs, and Human Versus Machine Surfaces

A strong publish bundle usually needs more than one kind of artifact.

That is not a flaw. It is a sign that the bundle is serving more than one audience.

The important question is:

> which artifact is for machines, which artifact is for humans, and which artifact defines the contract?

If that answer is blurry, downstream users and reviewers start reading the wrong file for
the wrong job.

## How to use this page

Keep one downstream machine and one downstream human in mind while you read.

Ask two different questions:

- if a script wants to consume this bundle, what should it read?
- if a reviewer wants to understand the run quickly, what should they open first?

If you keep answering both questions with the same file, the bundle is probably mixing
roles.

## Human-readable and machine-readable are different needs

Downstream consumers often need stable machine-readable artifacts such as:

- `summary.json`
- `summary.tsv`
- `manifest.json`

Reviewers and collaborators often also need human-readable artifacts such as:

- `report/index.html`
- contract notes or file API documents

The mistake is not having both. The mistake is failing to say which one is authoritative
for which question.

## A report is valuable, but it is not automatically the contract

The capstone builds `report/index.html` from `summary.json`.

That is a healthy relationship:

- `summary.json` remains a structured machine-readable artifact
- the report turns that information into a readable explanation for humans

This means the report helps interpretation, but it should not become the only source of
truth for downstream automation.

## A file API answers a different question again

A file API or contract note helps a human understand:

- what artifacts exist in the public bundle
- what each one means
- which paths are stable
- what kind of change would count as a contract break

This is different from both the report and the manifest.

The report explains what happened in the run. The file API explains how to use the bundle.

## One artifact should not do every job

```mermaid
flowchart LR
  summary["summary.json / summary.tsv"] --> machine["machine-readable consumer surface"]
  report["report/index.html"] --> human["human-readable interpretation surface"]
  file_api["file API / contract note"] --> contract["artifact meaning and stability rules"]
  manifest["manifest.json"] --> validation["bundle inventory and identity checks"]
```

The point of this diagram is not to create bureaucracy. It is to prevent role confusion.

## A concrete way to assign roles

Use this pattern when you design a publish bundle:

| Question | Best artifact type | Why |
| --- | --- | --- |
| What should another program parse? | machine-readable summary such as JSON or TSV | stable structured fields are easier to version and validate |
| What should a human open first? | report or dashboard | people need explanation, framing, and visual context |
| Where do path meaning and stability rules live? | file API or contract note | consumers need an explicit statement of what is safe to depend on |
| How do we know the bundle is complete and untampered? | manifest and checksums | integrity is different from semantics |

This table is simple on purpose. It stops beginners from calling every file "the output."

## A weak publish explanation

Weak shape:

- the report is polished, so teams stop maintaining structured summaries
- the JSON exists, but no one documents whether it is stable
- consumers scrape the HTML because the machine-readable contract is unclear

This produces fragile downstream use and painful review discussions.

## A stronger publish explanation

Stronger shape:

- keep a structured artifact for machine consumption
- keep a readable report for human inspection
- keep a contract document that explains artifact roles and stability
- make sure those surfaces agree with each other

That gives each audience a proper interface.

## One teaching scenario that makes the difference obvious

Suppose a colleague wants to compare two published runs programmatically.

They should not need to:

- scrape values out of `report/index.html`
- guess which files inside the bundle are stable
- infer meaning from a checksum manifest alone

They should be able to:

- read a documented machine-facing file such as `summary.json`
- confirm the bundle inventory and integrity with `manifest.json` and checksums
- use a contract note to understand which fields and paths are part of the public promise

That scenario is the reason this distinction matters.

## A practical test

Ask these questions:

1. If a script wanted to consume this bundle, which file should it read?
2. If a reviewer wanted to understand the run quickly, which file should they open?
3. If a maintainer wanted to know whether a path is stable, where is that promised?

If one artifact is trying to answer all three questions, the publish design is probably
too vague.

## The beginner mistake to catch early

The most common beginner mistake is to confuse readability with API quality.

A beautiful HTML report may be excellent for humans while being a terrible machine
interface. A raw JSON file may be excellent for machines while still needing a clear
human-facing explanation around it. Quality comes from assigning the right role to each
artifact, not from forcing one file to satisfy every audience.

## Common failure modes

| Failure mode | What it causes | Better repair |
| --- | --- | --- |
| downstream tools scrape HTML reports | machine usage depends on presentation markup | keep a stable machine-readable artifact authoritative |
| JSON bundle exists but is undocumented | consumers guess which fields are stable | document contract roles in a file API or contract note |
| report and summary drift apart | humans and tools no longer see the same story | generate human-readable surfaces from structured artifacts where possible |
| manifest is used as a semantic guide | users know file names but not meanings | pair inventory evidence with contract explanations |
| every artifact is called “the output” | review discussions become imprecise | name whether an artifact is for machines, humans, validation, or provenance |

## What a reviewer should hear

When a bundle is designed well, the explanation sounds something like this:

> `summary.json` is the machine-facing contract, `report/index.html` helps people inspect
> the run, the file API explains what is stable, and the manifest plus checksums defend
> bundle integrity.

That sentence is useful because each artifact has one primary job.

## The explanation a reviewer trusts

Strong explanation:

> `summary.json` and `summary.tsv` are the machine-facing outputs, `report/index.html`
> helps humans inspect the run, and the file API explains the meaning and stability of the
> published artifacts.

Weak explanation:

> the report shows everything, so the rest is optional.

The strong explanation preserves clear roles. The weak explanation collapses them.

## End-of-page checkpoint

Before leaving this page, you should be able to:

- explain why reports and machine-readable summaries are both useful
- explain why a report should not become the only downstream surface
- describe what a file API contributes beyond a report or manifest
- explain how role confusion creates brittle downstream use

If you still describe the report as "the main output" without naming the machine-facing
contract separately, revisit the page. The whole point is to stop that ambiguity.
