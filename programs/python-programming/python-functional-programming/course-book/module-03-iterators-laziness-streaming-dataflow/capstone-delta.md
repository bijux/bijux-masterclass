# Module 03 FuncPipe Delta: Make Demand Explicit

Module 02 made the RAG core configurable without hiding its pure transformations.
It could filter, clean, chunk, embed, and deduplicate a finite collection. Module 03
keeps those value-level rules and changes the execution model: callers may now
request a bounded prefix without first materializing the entire input.

## The pressure

A document source may be large, slow, or unbounded. A list-based pipeline cannot
answer these operational questions:

- How many documents must be read to produce three chunks?
- Can chunking preserve offsets while emitting one item at a time?
- What happens when two consumers advance at different speeds?
- Can timing and observation be tested without real sleeping or eager collection?

The new concept is **demand-driven dataflow**. An iterator is both a sequence of
values and a protocol for deciding when upstream work may happen.

## The application change

The Module 03 reference state adds these responsibilities:

| Pressure | Source surface | Learner-visible behavior |
| --- | --- | --- |
| stream the RAG core | `api/core.py`, `api/config.py` | `stream_chunks`, `gen_bounded_chunks`, and `make_gen_rag_fn` return iterators |
| preserve chunk meaning | `pipeline_stages.py`, `rag_types.py` | lazy chunks retain document IDs and exact spans |
| compose generic stages | `streaming/compose.py`, `streaming/types.py` | transforms connect without intermediate lists |
| combine and split demand | `streaming/fanin.py`, `streaming/fanout.py`, `api/core.py` | ordering, lockstep, and bounded skew are explicit policies |
| make time testable | `streaming/time.py`, `fp.py` | clocks and sleepers are injected |
| observe without rewriting values | `streaming/observability.py`, `streaming/sampling.py` | taps, counters, peeks, and samples stay lazy |
| deduplicate during traversal | `core/structural_dedup.py` | first occurrences are emitted in encounter order |

The generic streaming package does not replace the RAG pipeline. It gives the RAG
pipeline small execution-policy tools while the domain stages still own cleaning,
chunk metadata, and embedding.

## What must not change

When the stream is fully materialized with the default non-overlapping chunk
configuration:

- filtering and cleaning follow the Module 02 configuration;
- chunk text, document identity, offsets, and order remain equal;
- deterministic embedding remains a pure boundary;
- a hard prefix fence never requests an item beyond that prefix;
- observation yields the same values in the same order.

Some new operations deliberately have different semantics. Streaming
deduplication preserves first-encounter order and retains a set of seen keys;
canonical Module 02 deduplication sorts before removing duplicates. “Lazy” does
not automatically mean constant space.

## Proof route

From `programs/python-programming/python-functional-programming`:

```bash
PYTHONPATH=capstone/module-reference-states/module-03/src \
  python -m pytest -q \
  capstone/module-reference-states/module-03/tests/learning/test_module_03_streaming_dataflow.py
```

The learning proof checks construction versus demand, exact prefix consumption,
overlapping chunk metadata, window bounds, reusable-stage independence, fan-in
ordering, fan-out skew recovery, injected time, custom iteration, neutral
observation, and equality with the Module 02 value contract.

For source-level comparison:

```bash
git diff --stat \
  capstone/module-reference-states/module-02 \
  capstone/module-reference-states/module-03
```

Read the stat first, then trace the focused files in the table. The delta is too
large for an unguided whole-tree reading.

## Reference and downstream states

`capstone/module-reference-states/module-03` is the completed state for this
module. Modules 04 through 09 and the live capstone inherit its streaming
contract. A correction to shared behavior or its cumulative learning proof must
therefore be carried through those states and followed by history verification.

## Review boundary

Module 03 proves synchronous demand, bounded traversal, and deterministic test
control. It does not prove:

- automatic resource cleanup when iteration stops early;
- typed per-item recovery;
- asynchronous backpressure or fairness;
- constant space for fan-out, deduplication, or every `itertools` recipe.

Those limits are intentional hand-offs to later modules. Move forward when you can
predict which upstream item a downstream `next()` will request, identify every
materialization point, and name the policy that bounds retained state.
