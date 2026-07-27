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
