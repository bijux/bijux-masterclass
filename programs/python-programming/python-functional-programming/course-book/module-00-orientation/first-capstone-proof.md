# First Capstone Proof

Module 00 does not have a RAG reference state. Orientation introduces the problem
domain and the study method; Module 01 is the first point where the application has
earned executable behavior. This page gives you one bounded route through that first
state before the live Module 10 endpoint adds later concerns.

## The first application delta

| Delta question | Answer at the Module 00 to Module 01 boundary |
| --- | --- |
| Previous RAG capability | no tracked implementation; only the document-processing problem and course question |
| New design pressure | cleaning, chunking, embedding, and deduplication must be predictable enough to reason about locally |
| Concept introduced | pure transforms, immutable values, explicit configuration, and canonical output |
| Source that changes | `rag_types.py`, `pipeline_stages.py`, `full_rag.py`, and the thin `rag_shell.py` boundary in the Module 01 state |
| Proof | six learning tests for validation, immutability, fixed points, chunk coverage, embedding determinism, and canonical output |
| Behavior to preserve later | the same input and configuration still determine the same pure-core result |
| Completed state | `capstone/module-reference-states/module-01/` |
| Learner route | inspect the four files below, then run `capstone-foundation-proof` |
| Later states affected | Modules 02 through 10 must preserve these laws while adding configuration, streaming, failures, effects, async work, and interop |

There is no fabricated “before” implementation to compare with Module 01. The honest
before-state is a set of application pressures without code. The first useful
comparison arrives in Module 02, where the same pipeline becomes configurable and more
data-first.

## Trace one result through the first state

Read these files in order:

1. `capstone/module-reference-states/module-01/src/funcpipe_rag/rag_types.py`
   defines the immutable document, chunk, and environment values.
2. `capstone/module-reference-states/module-01/src/funcpipe_rag/pipeline_stages.py`
   defines cleaning, chunking, embedding, and structural deduplication.
3. `capstone/module-reference-states/module-01/src/funcpipe_rag/full_rag.py`
   composes those transforms into the pure application core.
4. `capstone/module-reference-states/module-01/tests/learning/test_module_01_purity_foundations.py`
   states the six learner-facing laws in executable form.

Keep one document in mind while reading:

```text
RawDoc
  -> clean whitespace and case
  -> split the cleaned abstract at explicit offsets
  -> derive an embedding from chunk text
  -> sort and remove structural duplicates
  -> list[Chunk]
```

The arrows describe value transformations. File loading and printing belong in
`rag_shell.py`, outside this trace. That separation is the first architecture decision,
not an incidental file layout.

## Run the bounded proof

From the repository root:

```bash
make PROGRAM=python-programming/python-functional-programming capstone-foundation-proof
```

The target installs or reuses the capstone development environment, puts the tracked
Module 01 source state first on the import path, and runs only its learning proof. The
successful test result ends with:

```text
6 passed
```

The six tests establish that:

- invalid chunk sizes fail at construction
- frozen inputs reject in-place mutation
- cleaning is deterministic and reaches a fixed point
- chunk offsets reconstruct the cleaned abstract
- embeddings depend on text rather than document identity or position
- the composed pure core preserves inputs and produces canonical output

## Read a failure before changing code

If the command reports an import error, do not install the package globally or point
the test at the live capstone. Confirm that you ran it from the repository root and
that `capstone/module-reference-states/module-01/` exists.

If one law fails, read that test and the single owning stage before opening the composed
pipeline. A failed chunk reconstruction claim belongs in `chunk_doc`; a failed
canonical-output claim may involve composition or deduplication. Narrowing ownership is
part of the lesson.

## What this proof does not establish

Six passing tests do not prove that the live Module 10 endpoint is healthy, that every
possible input is covered, or that later effects and async boundaries are correct. They
prove the first cumulative contract in the tracked state. Use
`capstone-test`, `history-verify`, or the full course `test` target only when your claim
has grown beyond that boundary.

You are ready for Module 01 when you can explain why each test belongs to the first
state and why replacing its source with the live endpoint would weaken the learning
route.
