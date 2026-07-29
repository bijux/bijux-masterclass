# Module 03 Exercises: Review Demand, State, and Boundaries

Work against `capstone/module-reference-states/module-03`. Keep Module 02's
filtering, cleaning, chunk values, metadata, and order unchanged unless an exercise
explicitly names a different policy.

Run the focused learning proof before editing:

```bash
make PROGRAM=python-programming/python-functional-programming \
  capstone-streaming-rag-proof
```

Use [Exercise Answers](exercise-answers.md) only after recording your prediction and
evidence.

## Exercise 1: Locate demand

Starting context: `stream_chunks` connects filtering, cleaning, and chunking with
generators. The first accepted document can produce several chunks.

Objective: predict and then measure how many documents are requested for:

- construction only;
- one chunk;
- five chunks when each document produces four;
- one chunk when the first three documents are rejected.

Constraints:

- use a generator source that records document IDs immediately before each `yield`;
- do not add logging inside FuncPipe;
- do not infer demand only from output length.

Expected evidence: a test table containing requested document IDs and emitted chunk
IDs for all four cases.

Acceptance checks:

- no request occurs at generator construction;
- your explanation distinguishes filter scans from chunk output;
- the existing default-value preservation test still passes.

## Exercise 2: Defend chunk metadata

Starting context: `gen_overlapping_chunks` supports `emit_short`, `drop`, and `pad`.

Objective: add a table-driven test for source text whose length is shorter than the
chunk size and for empty text.

Constraints:

- assert text, start, and end together;
- state whether reconstruction is exact for each tail policy;
- do not normalize away NUL padding before checking metadata.

Expected evidence: test cases that make the policy decision visible rather than
asserting only the number of chunks.

Acceptance checks:

- invalid `k`, overlap, and policy values are tested separately from tail behavior;
- the test explains why padded `end` may exceed source length;
- Module 02's default non-overlapping `emit_short` behavior remains equal.

## Exercise 3: Audit fan-out overflow

Starting context: `multicast` permits bounded consumer skew. A `BufferError` escaping
a subscriber generator closes that subscriber.

Objective: review `pump_once` as a small transaction and prove that a rejected fast
consumer request does not request or partially distribute another upstream value.

Constraints:

- use two consumers and `maxlen=1`;
- record upstream requests outside `multicast`;
- do not claim that the failed subscriber can resume.

Expected evidence: an exact event trace up to overflow and a focused regression
test.

Acceptance checks:

- capacity is checked before `next(upstream)`;
- the trace identifies the lagging queue;
- your handoff states that overflow is terminal for the requesting generator;
- identical proof passes in every downstream reference state and the live capstone.

## Exercise 4: Choose a reusable boundary

Starting context: the module provides `Source`, `Transform`, and
`make_gen_rag_fn`.

Objective: audit `make_gen_rag_fn` as a configured complete RAG factory, then
classify one proposed helper as a source, transform, sink, or unnecessary factory.
Write each type and ownership contract before implementing anything.

Constraints:

- per-run mutable state must be created inside the run;
- configuration captured by a factory must be explicit;
- tests must use replayable input or call a source again for each run.
- distinguish a pre-embedding raw-chunk fence from a final unique-output fence.

Expected evidence:

- final factory values contain embeddings and equal `stream_rag_chunks`;
- canonical input order matches `full_rag_api_docs`;
- out-of-order input demonstrates encounter order rather than canonical sorting;
- duplicate input proves a two-output fence may request three documents;
- one construction-versus-demand test.

Acceptance checks:

- the helper's name describes domain behavior, not generic “processing”;
- two runs are independent when the input contract permits replay;
- the stated limit names what it bounds;
- no intermediate list is introduced without a stated consumer need.

## Exercise 5: Add safe observation

Starting context: `TraceLens`, `make_tap`, and `make_peek` observe values with
different retained state and callback behavior.

Objective: add an observation to `stream_chunks` that records document IDs, not
document bodies, while preserving yielded chunks.

Constraints:

- store at most five sampled IDs;
- state whether callback failure propagates or is suppressed;
- do not materialize the chunk stream to observe it.

Expected evidence:

- callback state is empty before demand;
- a two-chunk prefix records only work required for that prefix;
- wrapped and unwrapped outputs are equal for the requested prefix;
- the sample never contains abstract text.

Acceptance checks:

- value neutrality and demand alignment are tested separately;
- retained state is bounded in both the lens and any callback;
- your review states what the test does not prove about privacy or thread safety.

## Completion review

You are ready for Module 04 when you can present:

- a value assertion and a demand assertion for the same pipeline;
- a distinction between raw-chunk and final unique-output fences;
- one deliberate materialization boundary;
- one stateful streaming helper with its real space bound;
- a failure whose timing depends on demand;
- the focused Make command that proves Module 03 behavior.
