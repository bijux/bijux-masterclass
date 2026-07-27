# Glossary

Publishing is where a workflow stops being only your private execution system and starts
becoming someone else's dependency. This glossary helps you describe that handoff with
terms that protect downstream trust instead of blurring it.

## When to stop and check the glossary

Use this page any time a review discussion starts to blur these boundaries:

- internal versus public
- compatible versus contract-changing
- machine-facing versus human-facing
- integrity evidence versus semantic meaning

If the discussion feels vague, it is usually because one of those terms has started doing
too many jobs at once.

## Terms

| Term | Meaning in this module |
| --- | --- |
| internal state | Workflow-owned outputs that help execution, debugging, or intermediate reasoning but are not the downstream contract. |
| public contract | The smaller set of published artifacts that downstream users are allowed to trust and depend on. |
| publish boundary | The directory and artifact set that define the downstream-facing contract, such as `publish/v1/`. |
| versioned boundary | A publish surface whose version communicates compatibility expectations over time. |
| compatible change | A change that preserves existing downstream expectations within the current publish version. |
| contract change | A change to paths, meanings, or required fields that alters the published promise and may require a new version. |
| manifest | The inventory of published artifacts, ideally including paths and digests. |
| checksum | A digest used to confirm file identity, detect corruption, or spot silent replacement. |
| bundle integrity | The degree to which a publish bundle can prove completeness and identity coherently. |
| provenance | Evidence about the software and execution context that produced the published outputs. |
| machine-readable artifact | A structured output designed for programmatic downstream use, such as `summary.json` or `summary.tsv`. |
| human-readable artifact | An output designed to help a person interpret the run, such as `report/index.html`. |
| file API | A document that explains what published artifacts exist, what they mean, and how stable they are. |
| publish drift | Any change that weakens or alters the downstream contract, whether through paths, semantics, or artifact-role confusion. |
| downstream trust | The confidence that another person or tool can use the published bundle without reverse engineering the workflow internals. |
| authoritative artifact | The published artifact a consumer should trust first for one job, such as the structured summary for programmatic reads. |
| consumer entrypoint | The first documented public artifact a downstream program or reviewer is expected to read when using the bundle. |
| reviewed discovery evidence | Public accepted and rejected discovery records that explain why the published result set has its exact membership when downstream review needs that reasoning. |
| artifact-role table | A compact table that names which published artifact is internal, machine-facing, human-facing, integrity-oriented, or provenance-oriented. |

## How to use these terms

If a publish review starts to feel vague, ask which term has become unclear:

- is the boundary internal or public?
- is the change compatible or contract-breaking?
- is this artifact for machines, humans, integrity, or provenance?

That question usually reveals the real problem quickly.

## Confusion pairs worth fixing early

These pairs matter because publish review weakens fast when one artifact is asked to play
too many roles:

- `internal state` versus `public contract`: internal state helps the workflow run or be
  debugged; the public contract is what downstream users may safely depend on.
- `compatible change` versus `contract change`: a compatible change stays inside the
  current published promise; a contract change alters that promise and may require a new
  versioned boundary.
- `manifest` versus `file API`: a manifest inventories what exists in one bundle; a file
  API explains what those artifacts mean and how stable they are.
- `machine-readable artifact` versus `human-readable artifact`: one is meant for program
  consumption; the other is meant to help a person interpret results.
- `authoritative artifact` versus `supporting artifact`: the authoritative artifact is
  the one a consumer or reviewer should trust first for a defined job; supporting
  artifacts help interpretation, review, or context but should not silently replace that
  authority.
- `reviewed discovery evidence` versus `manifest`: reviewed discovery evidence explains
  why the published set contains these members; the manifest proves the published bytes
  for those chosen members have not silently changed.

## When reviewed discovery evidence belongs in the bundle

Do not publish accepted and rejected discovery records by reflex. Publish them when a
downstream user needs to review, defend, or reproduce membership decisions rather than
only consume final summaries.

Typical signals that the evidence belongs in the public contract:

- the bundle's trust story depends on why some candidates were included and others were excluded
- downstream maintainers need to audit membership drift across releases
- a structured summary alone cannot answer "why this exact set?"
- the class misses the live instructor explanation, so the bundle itself must carry the review trail

Typical signals that the evidence can remain internal:

- downstream users only need final summaries and no one depends on the candidate-level selection logic
- the evidence is operational debug detail rather than part of the public review route
- publishing it would blur the boundary more than it would improve understanding

The decision rule is simple:

> Publish reviewed discovery evidence when membership reasoning is part of downstream trust,
> not merely because the workflow happened to generate those files.

## Authority questions to ask during publish review

If a publish conversation starts sounding vague, ask these in order:

1. which artifact is authoritative for this consumer task?
2. which artifact is the consumer entrypoint?
3. which artifacts support interpretation rather than carry authority?
4. which artifacts prove identity, context, or membership review separately?

Those four questions usually expose whether the bundle still has one coherent contract or
whether several artifacts are competing to be "the real output."

## Quick self-check

Before you leave Module 06, make sure you can answer these in a full sentence:

- If a downstream user depends on `publish/v1/summary.tsv`, what concept tells you that
  path is part of a trusted outward-facing promise rather than an internal convenience?
- If you add a new optional HTML report without changing existing published paths or field
  meanings, what class of publish change are you probably making?
- If a bundle contains checksums but no explanation of what each artifact means, which
  review document is still missing?
- If a publish tree mixes scratch leftovers with intended release artifacts, what kind of
  trust problem has appeared?
- If a consumer reads an HTML report first even though the structured summary is the real
  contract surface, which authority mistake has the bundle invited?
- If a downstream reviewer must explain why one candidate was published and another was
  not, which missing public evidence route is likely causing the review gap?

## Terms you should be able to use by the end of the day

By the end of Module 06, you should be comfortable using these in a full sentence:

- public contract
- publish boundary
- compatible change
- contract change
- manifest
- provenance
- machine-readable artifact
- downstream trust
- authoritative artifact
- consumer entrypoint
- reviewed discovery evidence
