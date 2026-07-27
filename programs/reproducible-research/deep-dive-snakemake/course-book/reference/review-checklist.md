# Review Checklist

Use this checklist when reviewing a Snakemake workflow, exercise answer, or capstone
change and you do not want the review to collapse into taste. A strong review should end
with a clear trust judgment, not with vague discomfort.

## How to use this checklist

Use it in this order:

1. name the claim you are reviewing
2. find the smallest section below that owns the claim
3. answer those questions with evidence, not guesswork
4. record the next keep, change, or reject decision

If you cannot answer a section without opening five other pages, the real gap is usually
upstream in the module understanding or proof route.

## Workflow truth

- Which file contracts are authoritative for this question?
- Does dynamic discovery leave durable evidence instead of runtime folklore?
- Would a dry-run still help a reviewer understand the workflow shape honestly?

## Policy and repository boundaries

- Which differences belong to operating policy rather than workflow meaning?
- Does a profile or repository-layer change risk semantic drift?
- Is reusable code living in the right place instead of leaking workflow semantics into helpers?

## Authority and layer ownership

- Which surface is authoritative for this question: workflow contract, discovery evidence, policy, or publish boundary?
- Which layer should own the next change: `Snakefile`, rules, modules, scripts, package code, or profiles?
- Would another maintainer know where this behavior belongs without oral explanation?

## Publish trust

- Which outputs are safe for downstream trust and which remain internal run state?
- Does the published contract stay smaller and clearer than the whole repository?
- Which evidence bundle should another maintainer inspect before approving change?

## Stewardship

- Which command or saved bundle gives the narrowest honest answer for the current claim?
- Which layer owns the next change: `Snakefile`, rules, modules, scripts, package code, or profiles?
- Which ambiguity would you require the author to make explicit before accepting the workflow?

## Good review outcomes

The checklist is working when you can end the review with one of these:

- keep the current design because the boundary is explicit and evidence is proportionate
- change one named surface because the current owner is wrong or too blurry
- reject the current claim because the workflow cannot yet prove it honestly

If the result is only "this feels messy," the review still needs sharper evidence.
