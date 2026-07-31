# Async Generators

`AsyncPlan[T]` describes one eventual `Result[T, ErrInfo]`. FuncPipe indexing
does not produce only one value: a document source can produce many documents,
each document can produce many chunks, and failures can appear between valid
items.

Module 08 therefore needs a second description:

```python
AsyncGen[T] = Callable[
    [],
    AsyncIterator[Result[T, ErrInfo]],
]
```

An `AsyncGen` is a factory for a fresh asynchronous result stream.

## Start from the application pressure

The synchronous Module 07 route already streams:

```text
RawDoc → CleanDoc → ChunkWithoutEmbedding → Chunk
```

Replacing that route with `async def build_index() -> list[Chunk]` would
materialize every result and lose demand-driven consumption. Module 08 instead
preserves the stream shape while allowing selected stages to wait.

```mermaid
flowchart LR
    docs["AsyncGen[RawDoc]"]
    expand["async_gen_and_then\none doc → many chunks"]
    chunks["AsyncGen[ChunkWithoutEmbedding]"]
    schedule["bounded async embedding"]
    embedded["AsyncGen[Chunk]"]

    docs --> expand --> chunks --> schedule --> embedded
```

The stream is asynchronous because pulling an item may wait. The individual
items still use `Result`, so expected failures remain visible data.

## Distinguish a stream factory from an iterator

This is an async generator function:

```python
async def numbers():
    yield Ok(1)
    yield Ok(2)
```

The function `numbers` can create a fresh iterator each time. The value
`numbers()` is one iterator with mutable traversal state.

FuncPipe stores the factory:

```python
source: AsyncGen[int] = numbers
```

This has the same replayability pattern as `AsyncPlan`:

| Description | One execution |
| --- | --- |
| `AsyncPlan[T]` | `Awaitable[Result[T, ErrInfo]]` |
| `AsyncGen[T]` | `AsyncIterator[Result[T, ErrInfo]]` |

Do not cache and reuse the iterator returned by `source()`. Ask the description
for a fresh one.

## Run a demand-driven example

The following example mirrors the tracked Module 08 proof:

```python
import asyncio
from collections.abc import AsyncIterator

from funcpipe_rag.domain.effects.async_ import AsyncGen, async_gen_map
from funcpipe_rag.result.types import ErrInfo, Ok, Result

pulled: list[int] = []


async def source_items() -> AsyncIterator[Result[int, ErrInfo]]:
    for value in (1, 2, 3):
        pulled.append(value)
        yield Ok(value)


source: AsyncGen[int] = source_items
doubled = async_gen_map(source, lambda value: value * 2)

print(pulled)


async def consume_prefix():
    iterator = doubled()
    first = await anext(iterator)
    second = await anext(iterator)
    await iterator.aclose()
    return first, second


print(asyncio.run(consume_prefix()))
print(pulled)
```

Expected output:

```text
[]
(Ok(value=2), Ok(value=4))
[1, 2]
```

Mapping the stream did not pull an item. Consuming two results did not pull the
third. This is observable laziness, not merely a claim that async generators
“are efficient.”

## Trace one pull

For `await anext(doubled())`, the control flow is:

```text
consumer requests one result
└── mapped stream requests one source result
    └── source resumes until its next yield
        └── Ok(1) returns to async_gen_map
            └── map applies value * 2
                └── consumer receives Ok(2)
```

No background producer exists. Demand moves upstream from the consumer.

This distinction becomes important in the next core: bounded mapping
intentionally introduces tasks, while ordinary `async_gen_map` does not.

## Preserve failures during transformation

`async_gen_map` delegates to `Result.map`:

```python
async for item in source():
    yield item.map(transform)
```

Therefore:

```text
Ok(value)  → Ok(transform(value))
Err(error) → Err(error)
```

The transform is not called for failed items. A learner should prove that with
a call log instead of relying on intuition.

`async_gen_and_then` supports one-to-many expansion:

```python
def expand(value: T) -> AsyncGen[U]: ...

expanded = async_gen_and_then(source, expand)
```

For each `Ok(value)`, the returned inner stream is consumed. An outer `Err`
passes through without calling `expand`.

## Read the shipped FuncPipe composition

`async_rag_chunks` uses `async_gen_and_then` to prepare chunks:

```python
def prepare_document(doc: RawDoc) -> AsyncGen[ChunkWithoutEmbedding]:
    async def generate():
        try:
            if keep is not None and not keep(doc):
                return
            cleaned = cleaner(doc)
            for chunk in gen_chunk_doc(cleaned, env):
                yield Ok(chunk)
        except (TypeError, ValueError) as exc:
            yield Err(ErrInfo.from_exception(exc))

    return generate


prepared = async_gen_and_then(docs, prepare_document)
```

This code makes four judgments explicit:

1. each successful document may yield zero or more chunks;
2. filtering, cleaning, and chunking remain synchronous domain work;
3. document validation failures become one stream item; and
4. a failed source item never enters document preparation.

The inner async generator contains no `await`. That is acceptable: it adapts a
demand-driven synchronous expansion into the `AsyncGen` shape needed by the
surrounding application. It does not pretend that cleaning is asynchronous.

## Partial consumption is an application behavior

Suppose the consumer stops after the first embedded chunk. A correct design
should not silently continue embedding the whole corpus.

For ordinary async generators, call `aclose()` when manually consuming a
prefix:

```python
iterator = stream()
try:
    first = await anext(iterator)
finally:
    await iterator.aclose()
```

An `async for` loop normally handles iterator shutdown when its own generator
frame exits, but adapters that acquire resources must still place cleanup in
`finally` or use `async_gen_using`.

The Module 08 proof
`test_service_stream_releases_resource_after_partial_consumption` records:

```text
enter
pull:0
exit
```

That trace is stronger than asserting only the returned value. It proves the
resource boundary closes after a partial pull.

## Counterexamples

### Eager materialization

```python
async def all_chunks(source):
    return [item async for item in source()]
```

This can be correct at a deliberate boundary, but it is not streaming. It
couples memory use and first-result latency to total input size.

### Hidden task creation

```python
async def mapped(source, transform):
    async for item in source():
        yield await asyncio.create_task(transform(item))
```

Creating one task and immediately awaiting it adds scheduling machinery without
concurrency. Creating all tasks up front is worse: it discards backpressure.

### Reusing an iterator

```python
iterator = source()


def broken_source():
    return iterator
```

The first traversal consumes state needed by later traversals. Keep the factory,
not the iterator.

### Swallowing stream failures

```python
async for item in source():
    if isinstance(item, Err):
        continue
```

Dropping failures may be a boundary policy, but it must not be hidden inside a
general transform. The caller otherwise cannot distinguish “no item” from “item
failed.”

## Compare the proof to the claim

Run:

```bash
make capstone-module-state-proof MODULE=08
```

Then focus on:

```text
test_async_stream_pulls_only_what_the_consumer_requests
test_service_stream_releases_resource_after_partial_consumption
test_async_stream_map_preserves_function_composition
test_async_rag_chunks_keeps_failures_in_the_application_stream
```

Together these tests establish:

- demand-driven pulls;
- cleanup after partial consumption;
- map composition over replayable streams; and
- application-level continuation across typed failures.

They do not establish a concurrency bound. Ordinary `AsyncGen` composition
creates no scheduling policy. Continue to [Backpressure](backpressure.md) for
the point where tasks and bounded windows enter the design.

## Move-forward criteria

You are ready for the next core when you can:

- expand the `AsyncGen` alias without guessing;
- distinguish a stream factory from one iterator;
- explain why mapping is lazy;
- show how `Err` bypasses a successful transform;
- close a partially consumed iterator;
- identify where `async_rag_chunks` expands documents into chunks; and
- state why none of those behaviors alone bounds concurrent embedding.
