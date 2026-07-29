# Module 03 Exercise Answers

These are review routes, not files to copy wholesale. A defensible solution preserves
the same contracts even if its fixture names differ.

## Answer 1: Locate demand

A counted source should record immediately before yielding:

```python
def documents(specs):
    for doc_id, accepted in specs:
        requested.append(doc_id)
        abstract = "x" * 200 if accepted else ""
        yield RawDoc(doc_id, "title", abstract, "cs.AI")
```

Constructing `gen_bounded_chunks` requests nothing. One requested chunk pulls the
first accepted document. Five chunks with four chunks per document pull two
documents: four outputs from the first, then one from the second. If the keep rule
rejects the first three documents, one output requires scanning those three plus
the first accepted document.

The common wrong turn is asserting `len(output) == k` and calling that a boundedness
test. That proves output count, not source demand. Another wrong turn is using a
list of documents; list construction has already happened and cannot expose lazy
source requests.

This result proves demand propagation for the tested source, keep rule, and chunk
shape. It does not prove progress for an infinite source whose documents are all
rejected, nor cleanup after early stop. Architecturally, filtering and `flatmap`
mean chunk count is not a one-to-one proxy for document reads.

## Answer 2: Defend chunk metadata

For text `"abc"` with `k=5` and `o=0`:

| Policy | Expected |
| --- | --- |
| `emit_short` | `("abc", 0, 3)` |
| `drop` | no chunk |
| `pad` | `("abc\\0\\0", 0, 5)` |

Empty text emits no chunk for all three policies because there is no starting
position. Validate that separately from an incomplete non-empty tail.

```python
@pytest.mark.parametrize(
    ("policy", "expected"),
    [
        ("emit_short", [("abc", 0, 3)]),
        ("drop", []),
        ("pad", [("abc\0\0", 0, 5)]),
    ],
)
def test_short_tail(policy, expected):
    chunks = gen_overlapping_chunks("doc-a", "abc", k=5, tail_policy=policy)
    assert [(c.text, c.start, c.end) for c in chunks] == expected
```

A common wrong turn is comparing only reconstructed text after stripping NULs.
That can conceal an incorrect padded `end`. Another is expecting `drop` to preserve
all source text; dropping is the policy.

The table proves specified short-tail values and offsets. It does not prove demand
for a general iterable because this chunker indexes one in-memory string. The
architecture keeps chunk metadata coupled to text so later retrieval can explain
source location.

## Answer 3: Defend a document-source schedule

Use a source factory whose call and traversal are separately observable:

```python
def tracked_source(name, docs, events):
    def open_source():
        events.append(f"open:{name}")

        def iterate():
            for doc in docs:
                events.append(f"yield:{doc.doc_id}")
                yield doc

        return iterate()

    return open_source
```

For priority documents `p1`, `p2` and background document `b1`, the expected
trace is:

| Demand | Sequential | Round robin |
| --- | --- | --- |
| construct output iterator | no events | no events |
| request first final chunk | `open:priority`, `yield:p1` | `open:priority`, `open:background`, `yield:p1` |
| consume all final chunks | output `p1, p2, b1` | output `p1, b1, p2` |

The distinction between opening and pulling matters. `make_roundrobin` creates an
iterator for every source when its merged iterator first runs, but it does not
request `b1` before yielding `p1`.

```python
sources = (
    tracked_source("priority", (p1, p2), events),
    tracked_source("background", (b1,), events),
)
config = RagConfig(env=RagEnv(chunk_size=100))

chunks = stream_rag_sources(
    sources,
    config,
    get_deps(config),
    schedule="sequential",
    max_chunks=1,
)

assert events == []
assert [chunk.doc_id for chunk in chunks] == ["p1"]
assert events == ["open:priority", "yield:p1"]
```

Choose sequential scheduling when priority means “finish this source first.”
Choose round-robin when each active synchronous source should get one turn per
cycle. This is not async fairness: a blocking `next()` still blocks the thread.

For cross-source deduplication, place an identical `RawDoc` in each source. The
complete pipeline emits one structural `Chunk`, and the event trace identifies
which occurrence established the seen key. The output value cannot identify its
source because `Chunk` does not model source provenance. If provenance is required,
add it explicitly at a domain boundary before deduplication.

Common wrong turns are:

- pass iterators instead of source factories, making a second traversal empty;
- assume `make_merge` sorts arbitrary inputs rather than requiring locally sorted
  sources;
- treat round-robin as non-blocking concurrency;
- infer provenance from an output type that does not contain it;
- compare only output order and omit factory-opening and document-pull evidence.

These checks prove deterministic synchronous scheduling, per-source order, global
deduplication, and the tested prefix demand. They do not prove non-blocking I/O,
thread safety, async backpressure, or recoverable source failure.

## Answer 4: Audit fan-out overflow

With two consumers and `maxlen=1`, the event trace is:

```text
fast asks -> upstream 0 -> queues [0], [0] -> fast receives 0
slow asks -> slow receives 0
fast asks -> upstream 1 -> queues [1], [1] -> fast receives 1
fast asks -> slow queue is full -> BufferError before upstream 2
```

The implementation must check all queues before calling `next(upstream)`. Appending
as it checks is also unsafe: one queue could receive the new value before a later
queue rejects it.

The common wrong turn is attempting `next(fast)` after catching `BufferError`.
Because the exception escaped the subscriber generator, that generator is closed.
The correct operational response is to fail or rebuild the fan-out, not silently
resume it.

The cumulative learning test proves no over-pull at overflow in Modules 03 through
09 and the live capstone. It does not prove recovery, cross-thread safety, or async
fairness. The architectural lesson is that bounded fan-out includes an overflow
outcome, not merely a queue size.

## Answer 5: Choose a reusable boundary

`make_gen_rag_fn` is a configured application factory:

```python
run = make_gen_rag_fn(chunk_size=50, max_chunks=3)
factory_chunks = list(run(replayable_docs))

config = RagConfig(env=RagEnv(chunk_size=50))
deps = get_deps(config)
direct_chunks = list(
    stream_rag_chunks(
        replayable_docs,
        config,
        deps,
        max_chunks=3,
    )
)

assert factory_chunks == direct_chunks
assert all(len(chunk.embedding) == 16 for chunk in factory_chunks)
```

The factory captures policy and creates the complete
clean–chunk–embed–deduplicate chain inside each run. Documents remain caller-owned
input. For canonically ordered documents, the unfenced stream equals
`full_rag_api_docs`. For out-of-order documents, the streaming result retains
encounter order while the eager result sorts canonically.

`max_chunks` counts final unique outputs. With duplicate, duplicate, and unique
documents, producing two outputs requests all three documents. That is correct
because the fence follows deduplication. A helper that promises at most two
pre-embedding chunk operations must instead use `gen_bounded_chunks`.

A common wrong turn is comparing the factory only with `gen_bounded_chunks`. That
partial pipeline has no embeddings or deduplication and cannot prove a RAG result.
Another is calling both limits “bounded” without naming whether they bound raw
work or final unique values.

Factory/direct equality proves wiring. Eager equality under canonical order proves
qualified Module 02 preservation. A counted duplicate source proves fence demand.
None proves replayability of a caller-supplied generator, constant-space
deduplication, or canonical ordering without materialization.

## Answer 6: Add safe observation

Use a lens over derived metadata:

```python
from collections.abc import Iterable, Iterator
from funcpipe_rag import RawDoc, TraceLens


def trace_doc_ids(
    docs: Iterable[RawDoc],
    lens: TraceLens[str],
) -> Iterator[RawDoc]:
    for doc in docs:
        lens.note(doc.doc_id)
        yield doc
```

Then pass the wrapped documents into `stream_chunks`. Before iteration,
`lens.count == 0`. After a bounded prefix, the count reflects documents actually
requested and `lens.samples` contains at most five IDs. Compare requested chunk
values with an unwrapped run over replayable input.

The common wrong turn is tracing entire `RawDoc` values because it is convenient.
That retains abstracts and broadens disclosure. Another is a callback that appends
every peek to an unbounded list: the stage's deque is bounded, but the callback is
not.

This solution proves value neutrality for tested inputs, demand-aligned observation,
and a five-ID sample bound. It does not prove that document IDs are non-sensitive,
that an arbitrary callback is thread-safe, or that downstream metric storage is
bounded. Observation remains an effect at the application edge; the RAG value
transforms remain unchanged.

## Final self-review

A satisfactory Module 03 solution should let you say:

- which call causes each unit of upstream work;
- which state survives suspension and how it is bounded;
- which ordering policy fan-in or deduplication uses;
- which value boundary deliberately materializes;
- which failure is deferred until iteration;
- exactly which test proves each claim.

If your evidence contains only final lists, add a counted source. If it contains
only counters, add value and metadata assertions. Streaming correctness needs both.

Run the evidence owner from the repository root:

```bash
make PROGRAM=python-programming/python-functional-programming \
  capstone-streaming-rag-proof
```

For the source-policy review alone:

```bash
make PROGRAM=python-programming/python-functional-programming \
  capstone-source-scheduling-proof
```
