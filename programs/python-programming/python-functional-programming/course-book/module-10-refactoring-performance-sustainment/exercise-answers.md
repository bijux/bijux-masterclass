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

## Performance budgeting: reject a one-dimensional win

The correct decision evaluates all declared dimensions. An observation of
`(latency=60 ms, peak memory=48 MB, throughput=30/s)` fails a budget of
`(80 ms, 32 MB, 25/s)` because memory is over its maximum. The latency and
throughput wins do not compensate for an independent hard limit.

Common wrong turns:

- timing inside the decision function makes tests depend on scheduler noise;
- averaging unlike dimensions invents a meaningless unit;
- returning only `False` hides the evidence needed to choose the next change;
- benchmarking non-equivalent outputs rewards a semantic regression.

The test proves deterministic threshold evaluation and complete violation
reporting for supplied values. It does not prove measurement validity, workload
representativeness, or statistical significance.

In FuncPipe, performance is a selection pressure on already-correct RAG behavior.
The budget can reject an implementation, but it cannot redefine what a valid
`Chunk` or ranked result means.

## Observability: preserve facts without creating hidden policy

Append `StageObservation("rank", processed=3, failures=0, latency_ms=1.5)` to
the observation tuple. The resulting stage order ends in `rank`, processed
increases by three, and latency increases by 1.5 ms.

Common wrong turns:

- raising inside `summarize_observations` when failures are nonzero makes metrics
  an undocumented control-flow boundary;
- storing observations in a module-global list makes tests order-dependent;
- sorting stage names destroys the execution trace;
- accepting more failures than processed records admits an impossible fact.

The test proves deterministic aggregation, validation, and encounter order for
supplied observations. It does not prove that the runtime emitted every event or
that an external telemetry sink delivered it.

In FuncPipe, `Result` still controls application failure. Observations explain what
happened; an explicit policy may later decide whether the evidence blocks a
release.

## Property-based regression: state equivalence in domain terms

Change one successful result's `ChunkMetadata.source`. A batch containing only
that chunk is sufficient to disprove equivalence; Hypothesis does not need a
large corpus because metadata equality is part of the predicate.

Common wrong turns:

- comparing only vector values loses identity and provenance contracts;
- applying `allclose` to identifiers or counts weakens exact domain semantics;
- comparing concrete optimized container types forbids safe implementation changes;
- testing only a hand-picked ASCII sentence misses useful generated cases.

The property proves pure and hybrid embedding parity across the generated text
and batch-size domain. It does not prove the hybrid route is faster, nor does it
cover numeric behavior outside the declared tolerances.

In FuncPipe, the equivalence predicate is the gate before performance evidence.
Optimization may change representation and execution, not the meaning of a RAG
chunk.
