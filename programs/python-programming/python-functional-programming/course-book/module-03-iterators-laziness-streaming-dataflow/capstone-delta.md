# Module 03 FuncPipe Delta: Make Complete RAG Demand Explicit

Module 02 provides a configurable eager API. It filters, cleans, chunks, embeds,
canonically sorts, deduplicates, and returns complete observations. Module 03 keeps
that API and adds a complete iterator route for callers that need bounded demand.

## New pressure

A large or slow document source makes “return all chunks” an incomplete execution
contract. A caller needs to know:

- whether constructing the pipeline requests input;
- where a prefix fence is placed;
- which stages run before an output appears;
- how deduplication changes upstream demand and retained state;
- whether fully consuming the stream preserves Module 02 values.

The concept introduced now is **demand-driven dataflow**: downstream requests
control upstream traversal, and fence placement is application behavior.

## Application delta

The completed Module 03 path is:

```text
RawDoc source
  -> filter
  -> clean
  -> chunk
  -> embed
  -> encounter-order structural dedup
  -> optional unique-output fence
  -> Chunk iterator
```

`stream_rag_chunks` owns that composition. `make_gen_rag_fn` captures immutable
policy and returns a fresh complete RAG iterator for each call. It returns `Chunk`,
including the deterministic embedding, rather than stopping at
`ChunkWithoutEmbedding`.

| Surface | Output | Fence meaning |
| --- | --- | --- |
| `stream_chunks` | pre-embedding `ChunkWithoutEmbedding` | none |
| `gen_bounded_chunks` | pre-embedding `ChunkWithoutEmbedding` | at most this many raw chunks |
| `gen_stream_embedded` | `Chunk` | none |
| `gen_stream_deduped` | unique encounter-ordered `Chunk` | none; retains seen keys |
| `stream_rag_chunks` | final unique `Chunk` | at most this many unique outputs |
| `make_gen_rag_fn` | fresh final unique `Chunk` iterator | configured unique-output limit |

The two fences are not interchangeable. A raw-chunk fence of two requests exactly
two raw chunks. A unique-output fence of two may request more when duplicates are
discarded before the second unique output appears.

## Source ownership

| Responsibility | Module 03 source |
| --- | --- |
| complete RAG iterator and RAG-specific stages | `api/core.py` |
| reusable configured factory | `api/config.py` |
| lazy structural deduplication | `core/structural_dedup.py` |
| overlap and tail policy | `pipeline_stages.py`, `rag_types.py` |
| generic source/transform composition | `streaming/compose.py`, `streaming/types.py` |
| fan-in, fan-out, time, and observation policies | `streaming/` |

The generic streaming package supplies execution-policy tools. RAG modules still
own document cleaning, chunk metadata, embedding, and structural identity.

## Preservation and deliberate difference

For input already ordered by `(doc_id, start)`, fully materializing
`stream_rag_chunks` equals the Module 02 eager API, including 16-component
embeddings.

For out-of-order documents, the APIs intentionally differ:

- the eager API sorts canonically before deduplication;
- the streaming API emits the first unique chunk in encounter order.

Sorting the complete streaming result by `(doc_id, start)` recovers the eager
result. The stream cannot promise canonical order without buffering and sorting the
whole input, which would defeat its demand contract.

Neither deduplication route is constant-space. The streaming route avoids retaining
all chunk values but retains every unique structural key seen so far.

## Executable laws

The Module 03 learning proof establishes 14 cases:

- construction does not request documents;
- a raw prefix fence does not pull one item too far;
- overlap and tail policies preserve their stated metadata;
- a sliding window pulls only the width needed for its next output;
- source factories create fresh traversals;
- multicast skew failure does not over-consume upstream;
- injected time makes pacing deterministic;
- custom deduplication is single-pass and encounter-ordered;
- observation is lazy, bounded, and value-neutral;
- the complete stream equals Module 02 for canonical input;
- encounter order is visibly different from eager canonical order;
- a unique-output fence may pull duplicates to fill its prefix.

Run the stable route from the repository root:

```bash
make PROGRAM=python-programming/python-functional-programming \
  capstone-streaming-rag-proof
```

## Reference-state route

`capstone/module-reference-states/module-03` is the completed state. Compare it
with Module 02:

```bash
diff -qr \
  programs/python-programming/python-functional-programming/capstone/module-reference-states/module-02/src \
  programs/python-programming/python-functional-programming/capstone/module-reference-states/module-03/src
```

Read `api/core.py`, `api/config.py`, `core/structural_dedup.py`, and `streaming/`
before expanding to the full tree.

Modules 04–09 and the live Module 10 capstone preserve the complete streaming
function, factory return type, and cumulative learning laws.

## Move-forward boundary

Module 03 proves synchronous demand, explicit fence placement, retained-key
reasoning, and deterministic test control. It does not prove automatic cleanup
after an abandoned iterator, typed per-item recovery, async backpressure, or
constant space for deduplication and fan-out.

Move to Module 04 when you can predict which source values a requested unique
prefix may consume, explain why streaming order differs from canonical order, and
point to the test that proves complete chunks still preserve Module 02 meaning.
