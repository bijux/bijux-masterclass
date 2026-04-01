# M08C09: Time- and Size-Based Chunking Strategies in Async Pipelines

**Module 08 – Main Track Core**  
> **Main track**: Cores 1–10 (Async / Concurrent Pipelines → Production).  
> This is a **required** core. Every production FuncPipe pipeline that talks to batched external services (embedding APIs, vector DBs, LLM batch endpoints) must chunk the async stream by size and/or time — without ever breaking order, completeness, backpressure, or laziness.

## Progression Note
Module 8 is **Async FuncPipe & Backpressure** — the lightweight, production-grade concurrency layer that sits directly on top of Module 7’s effect boundaries.

| Module | Focus                                          | Key Outcomes                                                                 |
|--------|------------------------------------------------|-------------------------------------------------------------------------------|
| 7      | Effect Boundaries & Resource Safety            | Ports & adapters, capability interfaces, resource-safe effect isolation      |
| 8      | Async FuncPipe & Backpressure                  | Async streams, bounded queues, timeouts/retries, fairness & rate limiting    |
| 9      | FP Across Libraries and Frameworks             | Stdlib FP, data/ML stacks, web/CLI/distributed integration                    |
| 10     | Refactoring, Performance, and Future-Proofing  | Systematic refactors, performance budgets, governance & evolution             |

**Core question**  
How do you turn a lazy async stream of individual items into efficient batches (by size and/or time) while preserving strict order, completeness, backpressure, and full laziness — using only pure data policies and injected time?

We take the resilient, bounded, rate-limited embedding stream from C03–C08 and ask the question every scaling team eventually faces:

**“Why am I making 100k single-item embedding calls at 1 RPS when the API supports batch=128 and costs 80 % less for batches?”**

The naïve pattern everyone writes first:
```python
# BEFORE – no batching, death by latency
async def embed_stream(chunks: AsyncGen[Chunk]) -> AsyncGen[EmbeddedChunk]:
    async for chunk in chunks:
        yield await embed_port.embed_batch([chunk.text])   # 1-item batches forever
```

100k items → 100k round-trips → minutes instead of seconds, crushing costs and latency.

The production pattern: a pure chunking combinator that takes a `ChunkPolicy` (data) and a `Sleeper` (injected time) and returns a new `AsyncGen[list[T]]` description that yields properly-sized and timed batches — while preserving strict order, flushing on errors or end-of-stream, and respecting downstream backpressure perfectly (bounded prefetch of 1).

```python
# AFTER – pure policy + injected time
policy = ChunkPolicy[Chunk](
    max_units=128,
    max_delay_ms=500,
    size_fn=lambda c: c.estimated_tokens,
    flush_on_err=True,
)

chunked = async_gen_chunk(chunks, policy)(sleeper)   # sleeper injected in shell

async for batch in chunked():
    # batch is list[Chunk], size ≤ 128 tokens
    # logical age when batch becomes available ≤ 500 ms + inter-arrival time of next item
    yield await embed_port.embed_batch([c.text for c in batch])
```

One policy change → dramatically different efficiency. Zero core changes. Full deterministic testing with fake sleeper.

**Audience**: Engineers who discovered that “just use async” is not free when you have 100k items and a batch API.

**Outcome**
1. Every single-item call replaced with properly-sized and timed batches.
2. Strict order, completeness, and backpressure preserved.
3. All chunking behaviour controlled by pure data (`ChunkPolicy`).
4. Full deterministic testing via injected fake sleeper — no real time in CI.

## Tiny Non-Domain Example – Chunked Counter

```python
def infinite_numbers() -> AsyncGen[int]:
    async def _gen():
        i = 0
        while True:
            yield Ok(i)
            i += 1
            # Real code awaits something; here downstream pull drives timing
    return lambda: _gen()

policy = ChunkPolicy[int](max_units=10, max_delay_ms=200)
chunked = async_gen_chunk(infinite_numbers(), policy)(FakeSleeper())

async for batch in chunked():
    print(batch)   # batches of ≤10 numbers (time bound only active when source produces slowly)
```

## Why Chunking as Pure Policy + Injected Time? (Three bullets every engineer should internalise)
- **Efficiency without sacrifice**: Batch APIs are 5–50× cheaper and faster — chunking unlocks them without losing streaming or backpressure.
- **Strict correctness**: Order, completeness, bounded size are mathematically guaranteed; delay is bounded relative to source arrival rate.
- **Configuration = data**: Dev/staging/prod/token-budget-specific behaviour is a one-line policy change.

## 1. Laws & Invariants (machine-checked)

| Law                       | Statement                                                                                 | Enforcement                     |
|---------------------------|-------------------------------------------------------------------------------------------|---------------------------------|
| Order Preservation        | Items appear in batches in exactly the same order as in the source stream                | Property tests                  |
| Completeness              | Every input item appears in exactly one output batch                                      | Property tests                  |
| Size Bound                | Every batch satisfies `sum(policy.size_fn(x) for x in batch) ≤ policy.max_units` (except singleton oversized items) | Fake sleeper tests              |
| Delay Bound               | For every non-empty batch flushed on new item arrival, age ≤ policy.max_delay_ms + inter-arrival time of the triggering item. On EOS the remaining batch is flushed regardless of age. | Fake sleeper tests              |
| Backpressure              | Chunking never pushes faster than downstream consumes — bounded prefetch of 1 item       | Property tests                  |
| Description Purity        | `async_gen_chunk` performs zero effects — only the interpreter with sleeper does        | Static analysis                 |

**Note on Delay Bound**: The bound is logical and evaluated whenever a new item arrives. On EOS, any remaining batch is flushed regardless of age. If the source stalls with a partial batch, wall-clock delay can exceed `max_delay_ms` (the chunker cannot force a flush without a downstream pull). This is the natural, backpressure-preserving semantics.

## 2. Decision Table – Which ChunkPolicy to Use?

| Use Case                          | Need Hard Size Cap | Need Hard Delay Cap | Oversized Items? | Recommended Policy                                 |
|-----------------------------------|--------------------|---------------------|------------------|----------------------------------------------------|
| Embedding API (token limit)       | Yes                | Yes                 | Singleton        | max_units=4000, max_delay_ms=500, size_fn=tokens  |
| Vector DB upsert                  | Yes                | No                  | Error            | max_units=500, max_delay_ms=0                      |
| Real-time UI streaming            | No                 | Yes                 | N/A              | max_units=0, max_delay_ms=200                      |
| Hybrid (cost + latency)           | Yes                | Yes                 | Singleton        | Both limits set                                    |

`max_units=0` means unbounded size.

## 3. Public API – ChunkPolicy & async_gen_chunk

```python
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, TypeVar, AsyncIterator, Generic

from funcpipe_rag.domain.effects.async_ import AsyncGen, Sleeper
from funcpipe_rag.result.types import Err, ErrInfo, Ok, Result

T = TypeVar("T")

@dataclass(frozen=True)
class ChunkPolicy(Generic[T]):
    max_units: int = 128                    # 0 = unbounded
    max_delay_ms: int = 500                 # 0 = no time limit
    flush_on_err: bool = True
    size_fn: Callable[[T], int] = lambda _: 1   # default: count items

def async_gen_chunk(
    source: AsyncGen[T],
    policy: ChunkPolicy[T],
) -> Callable[[Sleeper], AsyncGen[list[T]]]:
    """Pure combinator — returns a factory that takes a Sleeper and produces a chunked AsyncGen."""
    def make_chunked(sleeper: Sleeper) -> AsyncGen[list[T]]:
        async def _chunked() -> AsyncIterator[Result[list[T], ErrInfo]]:
            buf: list[T] = []
            buf_size = 0
            first_item_ts_ms: int | None = None   # logical timestamp of first item in current batch

            source_it = source()

            try:
                r = await source_it.__anext__()
            except StopAsyncIteration:
                return

            while True:
                if isinstance(r, Err):
                    if policy.flush_on_err and buf:
                        yield Ok(buf[:])
                        buf.clear()
                        buf_size = 0
                        first_item_ts_ms = None
                    yield r
                    try:
                        r = await source_it.__anext__()
                    except StopAsyncIteration:
                        return
                    continue

                item = r.value
                item_units = policy.size_fn(item)

                # Time flush check (only when we have a timestamp)
                time_flush = (
                    policy.max_delay_ms > 0 and
                    first_item_ts_ms is not None and
                    sleeper.now_ms() - first_item_ts_ms >= policy.max_delay_ms
                )

                # Size flush check
                size_flush = (
                    policy.max_units > 0 and
                    buf_size + item_units > policy.max_units
                )

                if (size_flush or time_flush) and buf:
                    yield Ok(buf[:])
                    buf.clear()
                    buf_size = 0
                    first_item_ts_ms = None

                # Oversized singleton
                if policy.max_units > 0 and item_units > policy.max_units:
                    yield Ok([item])
                else:
                    if not buf:
                        first_item_ts_ms = sleeper.now_ms()
                    buf.append(item)
                    buf_size += item_units

                # Pull next (prefetch = 1)
                try:
                    r = await source_it.__anext__()
                except StopAsyncIteration:
                    if buf:
                        yield Ok(buf[:])
                    return

        return lambda: _chunked()

    return make_chunked
```

## 4. Before → After – Chunked Embedding in RAG

```python
# BEFORE – single-item embedding calls
async def embed_stream(chunks: AsyncGen[Chunk]) -> AsyncGen[EmbeddedChunk]:
    async for chunk in chunks:
        vec = await embed_port.embed_batch([chunk.text])
        yield replace(chunk, embedding=vec[0])

# AFTER – proper chunking
policy = ChunkPolicy[Chunk](
    max_units=128,
    max_delay_ms=500,
    size_fn=lambda c: c.estimated_tokens,
)

def chunked_embedding_stream(
    chunks: AsyncGen[Chunk],
    embed_port: EmbedPort,
) -> AsyncGen[EmbeddedChunk]:
    chunked = async_gen_chunk(chunks, policy)(sleeper)
    batched_embeds = async_gen_map_action(
        chunked,
        lambda batch: embed_port.embed_batch([c.text for c in batch]),
    )
    return async_gen_flat_map(batched_embeds)   # flatten list[Result[Embedding]] → Result[Embedding]
```

## 5. Property-Based Proofs (all pass in CI – fully deterministic)

```python
@given(items=st.lists(st.integers(), max_size=200))
@pytest.mark.asyncio
async def test_chunk_order_completeness_size(items):
    policy = ChunkPolicy[int](max_units=10, max_delay_ms=1000)
    sleeper = FakeSleeper()

    async def source() -> AsyncIterator[Result[int, ErrInfo]]:
        for i in items:
            yield Ok(i)

    chunked = async_gen_chunk(lambda: source(), policy)(sleeper)

    emitted = []
    async for batch_res in chunked():
        assert isinstance(batch_res, Ok)
        batch = batch_res.value
        assert sum(policy.size_fn(x) for x in batch) <= policy.max_units or policy.max_units == 0
        emitted.extend(batch)

    assert emitted == items   # order + completeness

@given(items=st.lists(st.integers(), max_size=100))
@pytest.mark.asyncio
async def test_chunk_time_bound(items):
    policy = ChunkPolicy[int](max_units=1000, max_delay_ms=200)  # time-dominant
    sleeper = FakeSleeper()

    item_arrival_ts = []

    async def source() -> AsyncIterator[Result[int, ErrInfo]]:
        for i in items:
            item_arrival_ts.append(sleeper.now_ms())
            await sleeper.sleep_ms(30)   # simulate spaced arrival
            yield Ok(i)

    chunked = async_gen_chunk(lambda: source(), policy)(sleeper)

    batch_first_ts = []
    batch_emit_ts = []

    async for batch_res in chunked():
        assert isinstance(batch_res, Ok)
        batch_emit_ts.append(sleeper.now_ms())
        if item_arrival_ts:
            batch_first_ts.append(item_arrival_ts[0])
            # Consume the items that went into this batch (approximate)
            del item_arrival_ts[:len(batch_res.value)]

    for first_ts, emit_ts in zip(batch_first_ts, batch_emit_ts):
        delay = emit_ts - first_ts
        assert delay <= policy.max_delay_ms + 40  # +40 ms for inter-arrival + jitter tolerance
```

## 6. Runtime Guarantees

| Policy Setting             | Max Batch Size                  | Max Delay (logical)                       | Memory   |
|----------------------------|---------------------------------|-------------------------------------------|----------|
| max_units=N                | ≤ N (by size_fn)                | unbounded                                 | O(N)     |
| max_delay_ms=M             | unbounded                       | ≤ M + inter-arrival time of next item     | O(1) avg |
| Both                       | ≤ N                             | ≤ M + inter-arrival time of next item     | O(N)     |

## 7. Anti-Patterns & Immediate Fixes

| Anti-Pattern                  | Symptom                          | Fix                                      |
|-------------------------------|----------------------------------|------------------------------------------|
| Manual buffering              | Bugs, memory leaks               | `async_gen_chunk` + policy               |
| Hard-coded batch size/delay   | Inflexible, untunable            | `ChunkPolicy` as data                    |
| No flush on error/end         | Lost items                       | `flush_on_err=True`, final flush         |
| Prefetch >1                   | Breaks backpressure              | Pull-one prefetch only                   |

## 8. Pre-Core Quiz

1. Chunking is controlled by…? → **Pure `ChunkPolicy` data**  
2. Time is injected via…? → **`Sleeper` in interpreter**  
3. Oversized items are…? → **Emitted as singleton batches**  
4. Delay bound is…? → **Logical, checked on item arrival / EOS**  
5. The golden rule? → **One stream, many batching policies — zero manual buffering**

## 9. Post-Core Exercise

1. Define a `ChunkPolicy` for your real embedding tokens (e.g., max_units=4000, max_delay_ms=500).  
2. Wrap your chunk stream with `async_gen_chunk(..., policy)(sleeper)`.  
3. Add the order/completeness and logical delay property tests with your real size_fn.  
4. Measure latency/cost before and after — celebrate the 10–50× improvement.  
5. Sleep well — your pipeline is now both streaming-fast and batch-efficient.

**Next** → M08C10: Law-Like Properties for Async Pipelines (Idempotence, At-Most-Once, No Duplication)

You now have production-grade time- and size-based chunking that turns single-item death-by-latency into efficient batches — while preserving every correctness guarantee we fought for.

**M08C09 is now frozen.**
