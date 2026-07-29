# Module 10 Exercise Answers

Use these answers after producing your own evidence. A passing assertion is only
the start of the review: each answer explains the decision, common wrong turns,
what the result proves, and what remains outside the proof.

## Systematic refactor: make the starting observation trustworthy

The two configured paths are useful reading routes, but they are not disjoint sets.
`Path.rglob` under `rag/` already discovers files under `rag/domain/`. Summing both
counts therefore treats one source file as two observations.

A defensible implementation gathers resolved Python paths into a set and takes its
length. The configuration stays descriptive while file identity controls counting.

Common wrong turns:

- removing `rag/domain/` hides a useful high-signal review route;
- subtracting the current number of domain files makes the rule depend on today's tree;
- deduplicating path strings before discovery does not help because the parent and
  child strings are distinct.

The test proves that nested configured paths do not inflate the source count. It
does not prove that file count measures quality, complexity, or ownership. It is
only a trustworthy inventory observation.

In FuncPipe, this changes the review shell and leaves the Module 09 RAG contracts
untouched. That is the narrowest safe first refactor: repair the evidence before
using it to justify larger work.
