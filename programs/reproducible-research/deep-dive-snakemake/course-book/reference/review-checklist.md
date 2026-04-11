# Review Checklist

Use this checklist when reviewing a Snakemake workflow, module exercise, or capstone
change. The goal is to keep workflow trust tied to contracts and evidence.

## Workflow truth

- Which file contracts are authoritative for this question?
- Does dynamic discovery leave durable evidence instead of runtime folklore?
- Would a dry-run still help a reviewer understand the workflow shape honestly?

## Policy and repository boundaries

- Which differences belong to operating policy rather than workflow meaning?
- Does a profile or repository-layer change risk semantic drift?
- Is reusable code living in the right place instead of leaking workflow semantics into helpers?

## Publish trust

- Which outputs are safe for downstream trust and which remain internal run state?
- Does the published contract stay smaller and clearer than the whole repository?
- Which evidence bundle should another maintainer inspect before approving change?

## Stewardship

- Which command or saved bundle gives the narrowest honest answer for the current claim?
- Which layer owns the next change: `Snakefile`, rules, modules, scripts, package code, or profiles?
- Which ambiguity would you require the author to make explicit before accepting the workflow?
