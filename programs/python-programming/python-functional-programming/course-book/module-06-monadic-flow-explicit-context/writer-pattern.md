# Writer: Return Ordered Trace Data with the Value

Printing from the middle of a pure pipeline makes an observation hard to test:

```python
print(f"chunk={chunk.doc_id}:{chunk.start}-{chunk.end}")
```

The domain value does not contain that output, and a caller cannot compare or
transform it without capturing a process-wide stream.

Writer models a different contract:

```text
() -> (Value, ordered entries)
```

The trace is returned as data. No terminal, file, or logging service is touched.
Module 07 will decide where real emission belongs.

## Run the FuncPipe chunk trace

The Module 06 learning proof takes the first real chunk from
`iter_chunk_doc`:

```python
chunk = next(
    iter_chunk_doc(
        doc,
        RagEnv(chunk_size=4),
    )
)
```

It starts with that chunk as the payload and appends two entries:

```python
program = (
    writer_pure(chunk)
    .and_then(
        lambda current: tell(
            f"chunk:{current.doc_id}:"
            f"{current.start}-{current.end}"
        ).map(lambda _: current)
    )
    .and_then(
        lambda current: tell(
            f"characters:{len(current.text)}"
        ).map(lambda _: current)
    )
)
```

Running the description returns both channels:

```python
value, entries = run_writer(program)

assert value == chunk
assert entries == (
    "chunk:writer:0-4",
    "characters:4",
)
```

Run the proof:

```bash
cd capstone/module-reference-states/module-06
PYTHONPATH=src pytest -q tests/learning/test_module_06_explicit_context.py \
  -k writer_preserves_rag_chunk_while_accumulating_trace
```

The payload equality is as important as the entry assertion. A tracing wrapper
that silently replaces or modifies the chunk has violated its contract.

## Why `tell(...).map(lambda _: current)` appears

`tell(entry)` has the conceptual result:

```text
Writer[None]
```

Its meaningful output is the entry, not a new domain value. The following
`map` restores the current chunk to the value channel:

```python
tell(message).map(lambda _: current)
```

This separation makes the two channels explicit:

- the payload continues through dependent operations;
- entries append in observation order.

If this idiom dominates application code, introduce a named helper such as
`trace_chunk(current)` rather than repeating the plumbing.

## Read the implementation

The Module 06 Writer stores a delayed run function:

```python
@dataclass(frozen=True)
class Writer(Generic[T]):
    run: Callable[[], tuple[T, tuple[str, ...]]]
```

`map` changes only the payload:

```python
def map(self, f):
    def run():
        value, entries = self.run()
        return f(value), entries

    return Writer(run)
```

`and_then` runs both descriptions and concatenates the entries:

```python
def and_then(self, f):
    def run():
        value, first = self.run()
        next_value, second = f(value).run()
        return next_value, first + second

    return Writer(run)
```

Tuple concatenation makes the order visible and immutable. It also allocates a
new tuple. Very long left-associated Writer chains can copy earlier entries
repeatedly. This teaching implementation is suitable for small traces, not a
claim about high-volume operational logging performance.

## `listen` and `censor`

`listen(program)` makes the entries available inside the payload while
retaining them as entries:

```text
Writer[A] -> Writer[(A, entries)]
```

Use it when a pure decision needs to inspect the trace. Be careful not to make
domain behavior depend on incidental diagnostic text.

`censor(transform, program)` changes the returned entries while preserving the
payload. It can filter or normalize trace data before an outer boundary sees
it.

Neither helper emits anything.

## Writer is not operational logging

The Module 06 entries are strings. They do not provide:

- timestamps;
- severity;
- correlation identifiers;
- structured fields;
- delivery guarantees;
- backpressure;
- log rotation; or
- integration with a logging backend.

Those concerns require owned boundary types and effect execution. Module 07’s
functional logging lesson introduces a more appropriate separation.

Writer in this module answers a smaller question: can ordered diagnostic data
remain inspectable in a pure result?

## Layering Writer and Result

The reference state includes helpers for:

```text
Writer[Result[T, E]]
```

`wr_and_then` preserves entries created before a failure and skips the next
dependent operation when the inner Result is `Err`.

That is one explicit policy:

- trace entries may describe work before failure;
- Result owns short-circuiting of the value flow;
- Writer remains the outer context and returns the accumulated trace.

`Result[Writer[T], E]` would have different meaning: an outer `Err` contains no
Writer program to run. Choose the policy before choosing the layer order.

## Compare Writer with simpler values

An ordinary tuple may be enough:

```python
def inspect_chunk(
    chunk: Chunk,
) -> tuple[Chunk, tuple[str, ...]]:
    return chunk, (
        f"chunk:{chunk.doc_id}:"
        f"{chunk.start}-{chunk.end}",
    )
```

Choose Writer when several reusable operations append side information and
must compose while preserving one payload. Choose a tuple or a dedicated
domain record when there is one local observation or when named fields convey
more meaning than a generic entry sequence.

## Laws and application evidence

The Writer law suite checks:

- left identity;
- right identity;
- associativity;
- append order for `tell`; and
- the `listen` round trip.

Run it:

```bash
cd capstone/module-reference-states/module-06
PYTHONPATH=src pytest -q tests/test_writer_laws.py
```

The laws prove the append/composition structure for the generated entries.
The RAG learning test separately proves exact chunk preservation and expected
trace content.

## Common wrong turns

- **Calling `print` or a logger inside the Writer program.** The trace is no
  longer only a returned value.
- **Returning the message as the payload.** Diagnostic data replaces the RAG
  value.
- **Using one concatenated string.** Entry order and boundaries become harder
  to inspect.
- **Calling string entries production observability.** The teaching type has a
  deliberately narrow contract.
- **Ignoring allocation cost.** Tuple concatenation is clear but not a
  high-throughput logging structure.
- **Layering Writer and Result without a failure policy.** Reviewers cannot
  tell whether pre-failure entries should survive.

## What the focused proof establishes

The learning test proves that the Writer description returns the exact original
chunk and appends two exact string entries in order.

It does not prove delivery to a logging system, concurrency behavior,
performance at large trace sizes, or the adequacy of strings as an operational
log schema.

Continue with [Refactoring try/except](refactoring-try-except.md), where the
module applies its flow rules to an existing boundary without changing the
public result.
