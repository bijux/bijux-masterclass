# M08C06: Rate Limiting & Fairness – Cooperative Scheduling

**Module 08 – Main Track Core**  
> **Main track**: Cores 1–10 (Async / Concurrent Pipelines → Production).  
> This is a **required** core. Every production FuncPipe pipeline that shares an external metered resource (embedding API, third-party LLM, database, GPU fleet) uses explicit token-bucket rate limiting and weighted-fair merging as pure data — turning transient 429s and tenant starvation into predictable, configurable, mathematically well-behaved outcomes.

## Progression Note
Module 8 is **Async FuncPipe & Backpressure** — the final concurrency layer that makes the pure pipelines from Modules 1–7 scale to real-world production without ever compromising the laws we fought for.

| Module | Focus                                          | Key Outcomes                                                                 |
|--------|------------------------------------------------|-------------------------------------------------------------------------------|
| 7      | Effect Boundaries & Resource Safety            | Ports & adapters, capability interfaces, resource-safe effect isolation      |
| 8      | Async FuncPipe & Backpressure                  | Async streams, bounded queues, timeouts/retries, fairness & rate limiting    |
| 9      | FP Across Libraries and Frameworks             | Stdlib FP, data/ML stacks, web/CLI/distributed integration                    |
| 10     | Refactoring, Performance, and Future-Proofing  | Systematic refactors, performance budgets, governance & evolution             |

**Core question**  
How do you turn external rate limits and multi-tenant fairness requirements into pure, immutable data that are interpreted only when the async stream is driven — giving you hard throughput caps and starvation-free multiplexing without a single line of imperative scheduling logic in the core?

We take the resilient, bounded, backpressure-safe embedding stream from C03–C05 and ask the question every team faces at scale:

**“Why did we get globally rate-limited after adding two more tenants, and why is the biggest tenant getting 98 % of the capacity while the small one is completely starved?”**

The naïve pattern everyone writes first:
```python
# BEFORE – magic numbers, unfair, untestable
async def embed_with_hack(chunk: Chunk) -> EmbeddedChunk:
    await asyncio.sleep(0.125)                                      # "rate limit"
    return await model.aencode(chunk.text.content)

tasks = [embed_with_hack(c) for c in chunks]                        # largest tenant wins
results = await asyncio.gather(*tasks)
```

Magic numbers, no burst handling, no fairness, impossible to test deterministically, easy to forget the sleep.

The production pattern: policies are pure data → combinators return ordinary `AsyncGen` descriptions → enforcement (token bucket, WFQ selection, cooperative yields) happens only on iteration.

```python
# AFTER – pure policies, composable, testable, fair
rate_policy = RateLimitPolicy(tokens_per_second=8.0, burst_tokens=20)
fair_policy = FairnessPolicy(weights={0: 3, 1: 1, 2: 1}, max_buffer_per_stream=16)

def production_multi_tenant_stream(
    tenant_chunks: Mapping[int, AsyncGen[ChunkWithoutEmbedding]],
) -> AsyncGen[EmbeddedChunk]:
    per_tenant = [
        async_gen_bounded_map(                                  # C03
            chunks,
            lambda c: async_with_resilience(async_embed_chunk(c, embedder), retry_policy, timeout_policy),  # C04
            backpressure_policy,
        )
        for chunks in tenant_chunks.values()
    ]
    merged = async_gen_fair_merge(per_tenant, fair_policy)      # ← this core
    return async_gen_rate_limited(merged, rate_policy)          # ← this core
```

One line change → completely different scheduling behaviour. Zero duplication. Full deterministic testing via fake clock.

**Audience**: Engineers who have been globally banned from an API at 3 a.m. or had to explain to a customer why their job never progresses.

**Outcome**
1. Every hard-coded `await asyncio.sleep(...)` replaced with `RateLimitPolicy`.
2. Every unfair merge / starving tenant replaced with `FairnessPolicy`.
3. All scheduling proven to satisfy token-bucket and weighted-fair-queue laws (with explicit, documented assumptions) via Hypothesis + fake clock.
4. Linear, readable, refactor-safe flows that respect external constraints automatically.

## Tiny Non-Domain Example – Rate-limited & Fair Counter Merge

```python
def infinite_counter(tag: str) -> AsyncGen[str]:
    async def _gen():
        i = 0
        while True:
            yield Ok(f"{tag}-{i}")
            i += 1
            await asyncio.sleep(0)  # explicit cooperative yield
    return lambda: _gen()

streams = [infinite_counter("A"), infinite_counter("B")]  # A weight 1, B weight 4

fair   = async_gen_fair_merge(streams, FairnessPolicy(weights={0:1, 1:4}))
limited = async_gen_rate_limited(fair, RateLimitPolicy(tokens_per_second=100.0))

async for item in limited():   # B gets ~80 % share, total ≤ 100/s + burst
    print(item.value)
```

## Why Rate Limiting & Fairness as Pure Data? (Three bullets every engineer should internalise)
- **Mathematically hard rate cap**: Token bucket = proven never to exceed `tokens_per_second` long-term or `burst_tokens` instantaneously.
- **No starvation + proportional share among ready streams**: WFQ-style selection = every stream with buffered items is eventually selected; long-run ratio among contending streams matches weights.
- **Configuration = data**: Dev/staging/prod/tenant-specific behaviour is a one-line policy change, fully testable with fake clock.

## 1. Laws & Invariants (machine-checked where possible)

| Law                       | Statement & Assumptions                                                                                 | Enforcement                     |
|---------------------------|---------------------------------------------------------------------------------------------------------|---------------------------------|
| Token Bucket              | Long-term rate ≤ `tokens_per_second`; instantaneous burst ≤ `burst_tokens`                              | Fake clock + Hypothesis (global + sliding window) |
| No Starvation             | Assuming every live producer eventually yields a new item when selected repeatedly, every live stream with capacity to produce will emit infinitely often | Property tests                  |
| Proportional Share        | Among streams that always have items buffered, long-run emittedᵢ / weightᵢ is equal (empirical ε < 0.002 on large prefixes) | Deterministic property tests    |
| Description Purity        | Combinator construction performs zero side effects                                                       | Mock + static analysis          |
| Bounded Memory            | Memory = O(#streams × max_buffer_per_stream)                                                            | Property tests                  |

**Local laws (one-liner per combinator)**
- `async_gen_rate_limited`: each yielded item consumes exactly one token; if <1 token available, sleep exactly the minimum duration needed for one token to refill.
- `async_gen_fair_merge`: always selects the stream with the current minimum `emitted[i] / weight[i]` among streams with buffered items (lowest index on tie). When no stream has buffered items, yields control with `asyncio.sleep(0)`.

## 2. Decision Table – When to Apply Which Policy

| Scenario                               | Need Hard Rate Cap | Multiple Competing Streams | Policy Order                        |
|----------------------------------------|--------------------|----------------------------|-------------------------------------|
| Single embedding API                   | Yes                | No                         | RateLimit only                      |
| Multi-tenant batch processing          | Yes                | Yes                        | Fairness → RateLimit                |
| Internal unbounded work                | No                 | Yes                        | Fairness only                       |
| Shared LLM with per-tenant limits      | Yes                | Yes                        | Per-tenant RateLimit + global Fairness |

**Rule**: Apply fairness first (it balances load), then rate limiting on the merged stream (it caps total outbound).

## 3. Public API – Pure Scheduling Combinators

```python
import asyncio
from collections import deque
from collections.abc import AsyncIterator, Sequence, Mapping
from dataclasses import dataclass, field
from typing import TypeVar

from funcpipe_rag.domain.effects.async_ import AsyncGen
from funcpipe_rag.domain.effects.async_.resilience import ResilienceEnv
from funcpipe_rag.result.types import ErrInfo, Ok, Result

T = TypeVar("T")

@dataclass(frozen=True)
class RateLimitPolicy:
    tokens_per_second: float = 10.0
    burst_tokens: int = 10

@dataclass(frozen=True)
class FairnessPolicy:
    weights: Mapping[int, int] = field(default_factory=dict)  # stream index → weight, default 1
    max_buffer_per_stream: int = 16

def async_gen_rate_limited(
    stream: AsyncGen[T],
    policy: RateLimitPolicy,
    *,
    env: ResilienceEnv | None = None,
) -> AsyncGen[T]:
    local_env = env or ResilienceEnv.default()

    async def _limited() -> AsyncIterator[Result[T, ErrInfo]]:
        tokens = float(policy.burst_tokens)
        last_refill_s = local_env.clock.now_s()

        async for item in stream():
            now = local_env.clock.now_s()
            elapsed = now - last_refill_s
            tokens = min(policy.burst_tokens, tokens + elapsed * policy.tokens_per_second)
            last_refill_s = now

            if tokens < 1.0:
                await local_env.sleep((1.0 - tokens) / policy.tokens_per_second)
                # refill again after sleep
                now = local_env.clock.now_s()
                elapsed = now - last_refill_s
                tokens = min(policy.burst_tokens, tokens + elapsed * policy.tokens_per_second)
                last_refill_s = now

            tokens -= 1.0
            yield item

    return lambda: _limited()

def async_gen_fair_merge(
    streams: Sequence[AsyncGen[T]],
    policy: FairnessPolicy | None = None,
) -> AsyncGen[T]:
    policy = policy or FairnessPolicy()
    weights = [policy.weights.get(i, 1) for i in range(len(streams))]

    async def _fair() -> AsyncIterator[Result[T, ErrInfo]]:
        iterators = [s() for s in streams]
        buffers: list[deque[Result[T, ErrInfo]]] = [deque(maxlen=policy.max_buffer_per_stream) for _ in streams]
        active = [True] * len(streams)
        emitted = [0] * len(streams)

        # initial fill
        for i, it in enumerate(iterators):
            if active[i]:
                try:
                    buffers[i].append(await it.__anext__())
                except StopAsyncIteration:
                    active[i] = False

        while any(active):
            selected = -1
            best_ratio = float('inf')
            for i in range(len(streams)):
                if active[i] and buffers[i]:
                    ratio = emitted[i] / weights[i]
                    if ratio < best_ratio or (ratio == best_ratio and i < selected):
                        best_ratio = ratio
                        selected = i

            if selected != -1:
                yield buffers[selected].popleft()
                emitted[selected] += 1

                # greedily refill selected stream
                while len(buffers[selected]) < policy.max_buffer_per_stream and active[selected]:
                    try:
                        buffers[selected].append(await iterators[selected].__anext__())
                    except StopAsyncIteration:
                        active[selected] = False
                        break
            else:
                # no progress possible → cooperative yield
                await asyncio.sleep(0)

    return lambda: _fair()
```

## 4. Before → After – Multi-tenant Embedding Pipeline

```python
# AFTER – one pipeline, many policies
def multi_tenant_embedding_stream(
    tenant_chunks: Mapping[int, AsyncGen[ChunkWithoutEmbedding]],
    rate_policy: RateLimitPolicy,
    fair_policy: FairnessPolicy,
) -> AsyncGen[EmbeddedChunk]:
    per_tenant = [
        async_gen_bounded_map(
            chunks,
            lambda c: async_with_resilience(async_embed_chunk(c, embedder), retry, timeout),
            backpressure,
        )
        for chunks in tenant_chunks.values()
    ]
    fair   = async_gen_fair_merge(per_tenant, fair_policy)
    return async_gen_rate_limited(fair, rate_policy)
```

## 5. Key Tests & Empirical Proofs (all pass in CI)

```python
# FakeClock, ResilienceEnv, async_gen_from_list defined in testing helpers (C03–C05)
@given(tps=st.floats(0.5, 50.0), burst=st.integers(1, 50), n=st.integers(100, 5000))
@pytest.mark.asyncio
async def test_token_bucket_never_exceeds_policy(tps, burst, n):
    policy = RateLimitPolicy(tokens_per_second=tps, burst_tokens=burst)
    clock = FakeClock()

    async def fake_sleep(s: float) -> None:
        clock.advance_s(s)

    env = ResilienceEnv(clock=clock, sleep=fake_sleep, rng=Random(0))

    emission_times: list[float] = []

    def make_source() -> AsyncGen[None]:
        async def _gen():
            async for _ in async_gen_from_list(list(range(n)))():
                yield Ok(None)
        return lambda: _gen()

    stream = async_gen_rate_limited(make_source(), policy, env=env)

    # Record timestamps when the *rate-limited* stream actually yields items (after token checks & sleeps)
    async for _ in stream():
        emission_times.append(clock.now_s())

    # Global bound
    elapsed = clock.now_s()
    assert n <= (elapsed * tps) + burst + 1

    # Sliding 1-second window bound (O(n) two-pointer scan)
    right = 0
    n_times = len(emission_times)
    for i, start in enumerate(emission_times):
        end = start + 1.0
        while right < n_times and emission_times[right] <= end:
            right += 1
        items_in_window = right - i
        assert items_in_window <= tps * 1.0 + burst + 1
```

```python
@given(total=st.integers(5000, 20000), weight_a=st.integers(1, 10), weight_b=st.integers(1, 10))
@pytest.mark.asyncio
async def test_fair_merge_exact_proportional_when_all_ready(total, weight_a, weight_b):
    policy = FairnessPolicy(weights={0: weight_a, 1: weight_b}, max_buffer_per_stream=32)

    def instant_producer(tag: str, count: int) -> AsyncGen[str]:
        async def _gen():
            for i in range(count):
                yield Ok(f"{tag}{i}")
        return lambda: _gen()

    merged = async_gen_fair_merge([
        instant_producer("A", total * 10),
        instant_producer("B", total * 10),
    ], policy)

    counts = {"A": 0, "B": 0}
    async for item in merged():
        if isinstance(item, Ok):
            counts[item.value[0]] += 1
            if sum(counts.values()) >= total:
                break

    expected_ratio_b = weight_b / (weight_a + weight_b)
    actual_ratio_b = counts["B"] / sum(counts.values())
    assert abs(actual_ratio_b - expected_ratio_b) <= 0.002
    assert min(counts.values()) >= total // (weight_a + weight_b) - 10  # never starved
```

## 6. Runtime Guarantees

| Policy            | Long-term Rate          | Memory                              | Fairness (when all streams ready)                  |
|-------------------|-------------------------|-------------------------------------|----------------------------------------------------|
| RateLimitPolicy   | ≤ tokens_per_second     | O(1)                                | —                                                  |
| FairnessPolicy    | —                       | O(#streams × max_buffer_per_stream) | Empirical weight ratio within ε ≈ 0.002 on large prefixes |

## 7. Anti-Patterns & Immediate Fixes

| Anti-Pattern                     | Symptom                          | Fix                                      |
|----------------------------------|----------------------------------|------------------------------------------|
| Hard-coded `await sleep(...)`    | Untestable, forgotten, inflexible| `RateLimitPolicy` + `async_gen_rate_limited` |
| Naive merge of tenant streams    | Starvation, angry customers      | `async_gen_fair_merge` with weights      |
| Rate limiting after the call     | Still hits 429                   | Limit the metered step itself            |
| Unbounded per-stream buffers     | OOM under fast producers         | `max_buffer_per_stream` (enforced)      |

## 8. Pre-Core Quiz

1. Rate limiting is a…? → **Token bucket interpreted on yield**  
2. Fairness selects…? → **Stream with minimum emitted/weight among ready streams**  
3. Proportional share holds exactly when…? → **All streams always have buffered items**  
4. Memory is bounded by…? → **#streams × max_buffer_per_stream**  
5. The golden rule? → **One pipeline, many scheduling policies — zero duplication**

## 9. Post-Core Exercise

1. Add `RateLimitPolicy` + `FairnessPolicy` to your real multi-tenant pipeline.  
2. Replace any hard-coded sleeps or unfair merges.  
3. Run the sliding-window token-bucket test against your actual policy values.  
4. Run the proportional-share test with your tenant weights.  
5. Sleep well — your pipeline now respects the real world without selling your soul.

**Next** → M08C07: Integrating Pure FuncPipe Core with Async Edges Cleanly

You have completed the entire production-grade Async FuncPipe toolbox: pure descriptions, backpressure, resilience, deterministic testing, rate limiting, and fairness — all as composable, mathematically lawful combinators.

Module 9 begins integration with the wider Python ecosystem using exactly these primitives.

**M08C06 is now frozen.**
