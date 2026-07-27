# Self-Review Prompts

Use this page when you want short prompts that force recall, prediction, and judgment
instead of passive recognition. A useful prompt should make you prove that you understand
the workflow boundary without borrowing the page's wording.

## How to use these prompts

Pick three prompts only:

1. answer them without opening another page
2. check your answer against a command, file, or saved artifact
3. rewrite the answer in plainer language if it still sounds memorized

If you can answer every prompt only in course vocabulary, not in your own words, the idea
is not stable yet.

## Workflow truth

- Which file contract is doing the real work here?
- What durable evidence records checkpoint discovery instead of leaving it implicit?
- Which command would you run first to explain why the workflow wants to rerun?

## Policy and publish boundaries

- Which difference belongs to operating policy rather than workflow meaning?
- Which outputs are public for downstream trust, and which are only internal run state?
- What would another maintainer need to inspect before trusting a publish change?

## Stewardship

- Which repository layer should absorb the next non-trivial change?
- What would count as semantic drift rather than ordinary policy drift?
- Which saved evidence bundle would you trust first if logs disappeared?

## Layer prompts

- Should this behavior live in `Snakefile`, rules, modules, scripts, package code, or profiles?
- Would moving it make the workflow easier to review or only more indirect?
- Which layer would you inspect first before approving a boundary-heavy change?

## Good signs

These prompts are working when they make you do one of the following:

- predict a rerun before you execute it
- name the exact artifact that settles a discovery or publish question
- explain why a profile change is safe or unsafe
- choose a smaller proof route than the one you first wanted
