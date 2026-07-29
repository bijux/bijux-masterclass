# Module 05 Capstone Delta

Module 04 left FuncPipe able to stream documents while representing recoverable
failures with `Result`, absence with `Option`, and operational failures with
structured `ErrInfo` values. Those containers make failure visible, but they do
not decide which domain states are legal, how independent validation errors
should accumulate, or how a stored value retains its meaning across a boundary.

Module 05 gives those decisions explicit value shapes. It adds immutable product
types, closed sum types, legal state transitions, lawful mapping and
aggregation, accumulating validation, edge-only runtime validation, stable
serialization envelopes, and an equivalence-tested optimized representation.

## The application delta

| Delta question | Module 05 answer |
| --- | --- |
| Previous capability | Lazy and bounded RAG traversal with typed per-record failure, absence, retry, resource, and reporting policies |
| New pressure | Primitive fields, flags, partial constructors, and transport dictionaries permit invalid or ambiguous RAG states |
| Concept introduced | Product and sum types, state ADTs, functor mapping, applicative validation, monoidal aggregation, exhaustive matching, explicit codecs, and representation equivalence |
| Source surfaces | `fp/core.py`, `fp/functor.py`, `fp/validation.py`, `fp/monoid.py`, `rag/domain/`, and `boundaries/adapters/` |
| Proof surfaces | Module 05 law and boundary tests plus `tests/learning/test_module_05_data_modelling.py` |
| Preserved behavior | Module 04 cleaning, chunking, embedding, lazy order, bounded traversal, typed failures, retries, and resource cleanup |
| Completed state | `capstone/module-reference-states/module-05/` |
| Learner route | Run one named learning test, inspect the exact constructor or operation it exercises, then complete the matching exercise |
| Later states affected | Modules 06–09 and the live Module 10 capstone retain these value, validation, boundary, and equivalence contracts |

## Read the delta as ownership

```mermaid
flowchart LR
  input["Untrusted input"] --> adapters["Boundary adapters\nPydantic + codecs"]
  adapters --> model["RAG domain values\nproducts + sums"]
  model --> validate["Construction\nValidation"]
  model --> operate["Pure pipeline\nmap + match + fold"]
  operate --> output["Typed output"]
  model --> optimized["Optimized batch"]
  optimized --> proof["Observable-equivalence proof"]
  proof --> output
```

The arrows are ownership boundaries:

- boundary adapters reject malformed external data and then hand ordinary
  immutable values inward;
- domain constructors own cross-field invariants;
- `map` changes a successful value without inventing a failure policy;
- applicative validation evaluates independent checks and preserves every
  reported problem in declared order;
- monoids aggregate only when an associative operation and identity are honest;
- pattern matching consumes a closed set of variants; and
- an optimized representation is accepted only after its public observables
  agree with the clear reference path.

## Focus the reference-state comparison

The Module 04→05 snapshot includes a broad package reorganization. The meaningful
new teaching surface is narrower:

```text
src/funcpipe_rag/
├── fp/
│   ├── core.py
│   ├── functor.py
│   ├── validation.py
│   └── monoid.py
├── rag/domain/
│   ├── chunk.py
│   ├── text.py
│   ├── metadata.py
│   ├── embedding.py
│   └── perf.py
└── boundaries/adapters/
    ├── pydantic_edges.py
    └── serde.py
```

`rag/domain/` is a focused Module 05 modelling layer. It does not replace the
established pipeline values in `core/rag_types.py`; it lets learners study
construction and representation pressure without rewriting the cumulative RAG
pipeline. `boundaries/adapters/` owns external validation and serialization so
Pydantic and transport envelopes do not leak into that model.

These ownership paths begin in Module 05 and remain stable downstream. Package
movement that previously appeared only in the Module 05→06 comparison is not a
Module 06 flow concept and should not distract from that later delta.

## What changed in the RAG application

FuncPipe can now:

- construct immutable chunks and explicit success or failure variants;
- model processing as legal `Pending`, `Running`, `Done`, and `Failed`
  transitions;
- transform successful typed values without manual unboxing;
- report all independent construction errors in one validation result;
- aggregate chunk metrics with an explicit identity and associative operation;
- reject malformed embeddings at the external boundary;
- handle closed variants with structural pattern matching;
- preserve failure provenance through a versioned serialization envelope;
- assemble text, metadata, and embedding subsystems with cross-field checks; and
- choose a hybrid NumPy representation only when it preserves the clear pure
  path's observable results.

## What did not change

Module 05 does not turn the complete RAG application into one large algebraic
framework. Existing streaming and resilience behavior remains in place.
`Result` is still the right model for dependent fail-fast work; accumulating
`Validation` is for independent checks. Pydantic remains at the edge. A monoid
is not justified for every collection, and the NumPy path is not the default
merely because it is optimized.

## Working route

1. Compare `module-reference-states/module-04/` with
   `module-reference-states/module-05/`.
2. Read this page before interpreting the broad file diff.
3. Open the current lesson and its named test in
   `tests/learning/test_module_05_data_modelling.py`.
4. Run that one test with the Module 05 `src/` directory on `PYTHONPATH`.
5. Inspect the matching law or boundary test in the Module 05 test directory.
6. Complete the exercise and state what the evidence does not prove.
7. Confirm the learning proof remains present in every downstream state.

## Preservation checklist

Before accepting a modelling change, confirm that:

- previously valid RAG input still produces the same pipeline output;
- invalid states are rejected by the narrowest responsible constructor;
- `Result`, `Option`, and `Validation` keep distinct meanings;
- accumulated errors retain deterministic order and provenance;
- matching handles every declared variant;
- external schemas and codecs do not become core domain dependencies;
- serialization round-trips the public value, not incidental object layout;
- an optimized representation preserves identity, order, metadata, and numeric
  results within the declared tolerance; and
- later snapshots still satisfy the Module 05 learning proofs.

Continue with [Product and Sum Types](product-and-sum-types.md).
