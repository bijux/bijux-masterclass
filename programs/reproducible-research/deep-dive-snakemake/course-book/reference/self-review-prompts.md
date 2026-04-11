# Self-Review Prompts

Use this page when you want short prompts that turn Snakemake concepts into active
workflow judgment instead of passive familiarity.

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
