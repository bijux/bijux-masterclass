# M08C08: Designing Async Adapters for External Services (HTTP, DB) from Pure Interfaces

**Module 08 – Main Track Core**  
> **Main track**: Cores 1–10 (Async / Concurrent Pipelines → Production).  
> This is a **required** core. Every real-world FuncPipe pipeline talks to external services — and those services must be wrapped in thin, pure-protocol-conforming async adapters that are completely swappable, mockable, and composable with all the resilience machinery we built in C04–C06.

## Progression Note
Module 8 is **Async FuncPipe & Backpressure** — the lightweight, production-grade concurrency layer that sits directly on top of Module 7’s effect boundaries.

| Module | Focus                                          | Key Outcomes                                                                 |
|--------|------------------------------------------------|-------------------------------------------------------------------------------|
| 7      | Effect Boundaries & Resource Safety            | Ports & adapters, capability interfaces, resource-safe effect isolation      |
| 8      | Async FuncPipe & Backpressure                  | Async streams, bounded queues, timeouts/retries, fairness & rate limiting    |
| 9      | FP Across Libraries and Frameworks             | Stdlib FP, data/ML stacks, web/CLI/distributed integration                    |
| 10     | Refactoring, Performance, and Future-Proofing  | Systematic refactors, performance budgets, governance & evolution             |

**Core question**  
How do you turn flaky, imperative, library-specific service calls (HTTP APIs, databases, GPU queues) into thin, pure-protocol-conforming async adapters that are completely isolated, idempotent where possible, and trivially composable with retries, timeouts, rate-limiting, and fairness — while keeping the core 100 % unaware of the concrete service?

We take the layered RAG pipeline from C07 and finally connect it to the real world: OpenAI/Anthropic/Cohere embedding APIs, Pinecone/Weaviate/Qdrant/Chroma/PostgreSQL+pgvector — without ever letting a single `httpx.AsyncClient` or `asyncpg.Pool` touch the pure core.

The naïve pattern everyone writes first:
```python
# BEFORE – service cancer everywhere
async def embed_chunks(chunks: list[Chunk]) -> list[EmbeddedChunk]:
    resp = await httpx.post(                              # concrete library
        "https://api.openai.com/v1/embeddings",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"model": "text-embedding-3-large", "input": [c.text for c in chunks]},
        timeout=30.0,
    )
    resp.raise_for_status()                               # untyped exception
    data = resp.json()["data"]
    return [replace(c, embedding=Embedding(vec["embedding"], "openai")) for c, vec in zip(chunks, data)]
```

Concrete library, hardcoded timeout, untyped JSON parsing, no retry classification, no idempotence, impossible to mock cleanly.

The production pattern: pure protocol → factory that returns an adapter class implementing the protocol → adapter methods return pure async descriptions (thunks) → all resilience (retry/timeout/rate-limit/fairness) applied as data in the shell or higher-order combinators.

```python
# AFTER – pure protocol + thin adapter class
@runtime_checkable
class EmbedPort(Protocol):
    # AsyncAction already yields Result[..., ErrInfo] when driven.
    # Use the return type `list[Result[Embedding, ErrInfo]]` when you need per-item failures.
    def embed_batch(self, texts: list[str]) -> AsyncAction[list[Result[Embedding, ErrInfo]]]: ...

def make_openai_embed_adapter(client: AsyncClient, model: str) -> EmbedPort:
    class _Adapter:
        def embed_batch(self, texts: list[str]) -> AsyncAction[list[Result[Embedding, ErrInfo]]]:
            async def _act() -> Result[list[Result[Embedding, ErrInfo]], ErrInfo]:
                if not texts:
                    return Ok([])
                try:
                    resp = await client.post(
                        "/v1/embeddings",
                        json={"model": model, "input": texts},
                    )
                    if resp.status_code == 429:
                        return Err(ErrInfo(code="RATE_LIMIT", msg="rate limited", ctx={"retry_after": resp.headers.get("retry-after")}))
                    if resp.status_code == 401:
                        return Err(ErrInfo(code="AUTH", msg="invalid api key"))
                    if 500 <= resp.status_code < 600:
                        return Err(ErrInfo(code="TRANSIENT", msg="server error"))
                    resp.raise_for_status()
                    data = resp.json()["data"]
                    return Ok([Ok(Embedding(vec["embedding"], model)) for vec in data])
                except TimeoutException:
                    return Err(ErrInfo(code="TIMEOUT", msg="request timeout"))
                except RequestError as e:
                    return Err(ErrInfo(code="NETWORK", msg=str(e)))
                except Exception as e:  # JSON parse, unexpected shape, etc.
                    return Err(ErrInfo(code="SERVICE_SPECIFIC", msg=str(e)))
            
            return lambda: _act()
    
    return _Adapter()
```

One factory change → completely different provider. Zero core changes. Full resilience via policies applied outside.

**Audience**: Engineers who have been woken up at 3 a.m. because “the embedding API changed its JSON shape again”.

**Outcome**
1. Every external service wrapped in a pure protocol + thin adapter factory returning a class.
2. All resilience (retry/timeout/rate-limit/fairness) applied as pure data outside the adapter.
3. Idempotent writes via UPSERT + stable deterministic IDs (derived from content hash).
4. Full deterministic testing via sync mock implementations of the protocols.

## Tiny Non-Domain Example – HTTP Weather Adapter

```python
@runtime_checkable
class WeatherPort(Protocol):
    def get_forecast(self, city: str) -> AsyncAction[Result[Forecast, ErrInfo]]: ...
      # Single-item domain value; request-level Result only

def make_openweather_adapter(client: AsyncClient, api_key: str) -> WeatherPort:
    class _Adapter:
        def get_forecast(self, city: str) -> AsyncAction[Result[Forecast, ErrInfo]]:
            async def _act() -> Result[Forecast, ErrInfo]:
                try:
                    resp = await client.get(
                        f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}"
                    )
                    if resp.status_code == 401:
                        return Err(ErrInfo(code="AUTH", msg="invalid key"))
                    if resp.status_code == 429:
                        return Err(ErrInfo(code="RATE_LIMIT", msg="too many requests"))
                    resp.raise_for_status()
                    return Ok(parse_forecast(resp.json()))
                except TimeoutException:
                    return Err(ErrInfo(code="TIMEOUT", msg="request timeout"))
                except RequestError as e:
                    return Err(ErrInfo(code="NETWORK", msg=str(e)))
                except Exception as e:
                    return Err(ErrInfo(code="SERVICE_SPECIFIC", msg=str(e)))
            
            return lambda: _act()
    
    return _Adapter()
```

Swap in a mock → instant sync tests.

## Why Pure Protocols + Thin Async Adapter Classes? (Three bullets every engineer should internalise)
- **Zero vendor lock-in**: Swap OpenAI ↔ Cohere ↔ local Ollama with a one-line factory change.
- **Perfect testability**: Implement the protocol synchronously with fakes → no event loop in 99 % of tests.
- **Full resilience composability**: All policies (retry/timeout/rate-limit/fairness) applied uniformly outside the adapter.

Adapter methods must never be `async def` — they always return an `AsyncAction` thunk (fresh coroutine factory). This is the law that keeps us pure.

## 1. Laws & Invariants (machine-checked)

| Law                       | Statement                                                                                 | Enforcement                     |
|---------------------------|-------------------------------------------------------------------------------------------|---------------------------------|
| Adapter Purity            | Adapter methods return thunks (`lambda: ...`) — never executed on call; no effects on construction | Static analysis                 |
| Error Taxonomy            | Every external failure maps to one of: AUTH, RATE_LIMIT, TRANSIENT, TIMEOUT, NETWORK, SERVICE_SPECIFIC, DB_ERROR, FATAL_DB | Exhaustive match + catch-all    |
| Idempotence (writes)      | UPSERT + deterministic stable ID → repeated identical calls are no-ops                  | Property tests with mock DB     |
| Resource Safety           | Short-lived resources (connections, transactions) acquired via `async with`; long-lived clients owned by shell | Contextlib + cancellation tests |
| Mock Equivalence          | Real adapter ≡ mock adapter on golden inputs (with fake clock/RNG)                       | Hypothesis equivalence          |

## 2. Decision Table – Adapter Design Choices

| Service Type       | Idempotent? | Batch API? | Per-item Results? | Recommended Return Type                                      |
|--------------------|-------------|------------|-------------------|--------------------------------------------------------------|
| Embedding HTTP     | Yes         | Yes        | Rarely needed     | AsyncAction[Result[list[Result[Embedding, ErrInfo]], ErrInfo]] |
| Vector DB upsert   | Yes         | Yes        | No                | AsyncAction[Result[None, ErrInfo]]                           |
| Vector DB query    | Yes         | N/A        | No                | AsyncAction[Result[list[EmbeddedChunk], ErrInfo]]            |
| Non-idempotent POST| No          | Careful    | —                 | Disable retry or make idempotent via token                   |

## 3. Public API – Protocols & Adapter Factories

```python
from __future__ import annotations
from typing import Protocol, runtime_checkable
from collections.abc import AsyncGenerator

from httpx import AsyncClient, TimeoutException, RequestError
from asyncpg import Pool, PostgresError

AsyncGen = AsyncGenerator

@runtime_checkable
class EmbedPort(Protocol):
    def embed_batch(self, texts: list[str]) -> AsyncAction[Result[list[Result[Embedding, ErrInfo]], ErrInfo]]: ...
      # Outer Result: request-level failure (network/auth/rate-limit/transient)
      # Inner list[Result]: per-text failures (provider-specific, rare but possible)

@runtime_checkable
class VectorStorePort(Protocol):
    def upsert(self, chunks: list[EmbeddedChunk]) -> AsyncAction[Result[None, ErrInfo]]: ...
    def query(self, embedding: EmbeddingVector, top_k: int) -> AsyncAction[Result[list[EmbeddedChunk], ErrInfo]]: ...

# HTTP factory – returns adapter class instance
def make_openai_embed_adapter(
    client: AsyncClient,
    model: str = "text-embedding-3-large",
) -> EmbedPort:
    class _Adapter:
        def embed_batch(self, texts: list[str]) -> AsyncAction[Result[list[Result[Embedding, ErrInfo]], ErrInfo]]:
            async def _act() -> Result[list[Result[Embedding, ErrInfo]], ErrInfo]:
                if not texts:
                    return Ok([])
                try:
                    resp = await client.post(
                        "/v1/embeddings",
                        json={"model": model, "input": texts},
                    )
                    if resp.status_code == 429:
                        return Err(ErrInfo(code="RATE_LIMIT", msg="rate limited", meta={"retry_after": resp.headers.get("retry-after")}))
                    if resp.status_code == 401:
                        return Err(ErrInfo(code="AUTH", msg="invalid api key"))
                    if 500 <= resp.status_code < 600:
                        return Err(ErrInfo(code="TRANSIENT", msg="server error"))
                    resp.raise_for_status()
                    data = resp.json()["data"]
                    return Ok([Ok(Embedding(vec["embedding"], model)) for vec in data])
                except TimeoutException:
                    return Err(ErrInfo(code="TIMEOUT", msg="request timeout"))
                except RequestError as e:
                    return Err(ErrInfo(code="NETWORK", msg=str(e)))
                except Exception as e:  # JSON parse, unexpected shape, etc.
                    return Err(ErrInfo(code="SERVICE_SPECIFIC", msg=str(e)))
            
            return lambda: _act()
    
    return _Adapter()

# DB factory – returns adapter class instance
def make_pgvector_adapter(pool: Pool) -> VectorStorePort:
    class _Adapter:
        def upsert(self, chunks: list[EmbeddedChunk]) -> AsyncAction[Result[None, ErrInfo]]:
            async def _act() -> Result[None, ErrInfo]:
                if not chunks:
                    return Ok(None)
                try:
                    async with pool.acquire() as conn:
                        async with conn.transaction():
                            await conn.executemany(
                                """INSERT INTO chunks (id, embedding, metadata)
                                   VALUES ($1, $2, $3)
                                   ON CONFLICT (id) DO UPDATE
                                   SET embedding = EXCLUDED.embedding,
                                       metadata = EXCLUDED.metadata""",
                                [(c.id, c.embedding.vector, c.metadata) for c in chunks],
                            )
                    return Ok(None)
                except PostgresError as e:
                    # 08xxx = connection exception, 40xxx = transaction rollback (usually transient)
                    is_transient = bool(e.sqlstate and e.sqlstate.startswith(("08", "40")))
                    code = "TRANSIENT" if is_transient else "DB_ERROR"
                    return Err(ErrInfo(code=code, msg=str(e), meta={"sqlstate": e.sqlstate}))
                except Exception as e:
                    return Err(ErrInfo(code="FATAL_DB", msg=str(e)))
            
            return lambda: _act()
        
        def query(self, embedding: EmbeddingVector, top_k: int) -> AsyncAction[Result[list[EmbeddedChunk], ErrInfo]]:
            async def _act() -> Result[list[EmbeddedChunk], ErrInfo]:
                try:
                    async with pool.acquire() as conn:
                        rows = await conn.fetch(
                            """SELECT id, embedding, metadata
                               FROM chunks
                               ORDER BY embedding <-> $1
                               LIMIT $2""",
                            embedding, top_k,
                        )
                    return Ok([EmbeddedChunk.from_row(row) for row in rows])
                except PostgresError as e:
                    is_transient = bool(e.sqlstate and e.sqlstate.startswith(("08", "40")))
                    code = "TRANSIENT" if is_transient else "DB_ERROR"
                    return Err(ErrInfo(code=code, msg=str(e), meta={"sqlstate": e.sqlstate}))
                except Exception as e:
                    return Err(ErrInfo(code="FATAL_DB", msg=str(e)))
            
            return lambda: _act()
    
    return _Adapter()
```

## 4. Before → After – RAG with Real Services

```python
# BEFORE – concrete services everywhere
async def rag_with_openai_and_pg(chunks: list[Chunk]):
    resp = await httpx.post(...)                       # scattered
    # ... parse, handle 429 manually
    await pool.executemany(...)                        # different client

# AFTER – pure protocols only
def rag_with_services(
    embed_port: EmbedPort,
    vector_port: VectorStorePort,
) -> AsyncGen[None]:
    # ... same pipeline as C07, just pass ports
    embedded = async_gen_map(batches, embed_port.embed_batch)
    stored   = async_gen_map(embedded, vector_port.upsert)
    return stored

# Shell – owns concrete clients and policies
async def main():
    async with AsyncClient(base_url="https://api.openai.com", timeout=None) as client:
        embed_port = make_openai_embed_adapter(client)
        vector_port = make_pgvector_adapter(pool)
        desc = rag_with_services(embed_port, vector_port)
        resilient = async_gen_map_action(
            desc,
            lambda act: async_with_resilience(act, retry_policy, timeout_policy),
        )
        async for _ in resilient():
            pass
```

## 5. Property-Based Proofs (all pass in CI – fully deterministic, no network)

```python
@given(texts=st.lists(st.text(), max_size=20))
@pytest.mark.asyncio
async def test_openai_adapter_equivalence_with_mock(texts):
    # Real-style adapter with stubbed client (no network)
    stub_client = StubAsyncClient(responses=[{"data": [{"embedding": [0.1] * 1536} for _ in texts]}])
    real_style_adapter = make_openai_embed_adapter(stub_client)
    
    # Pure in-memory mock
    mock_adapter = make_in_memory_embed_adapter()  # returns fixed fake embeddings
    
    plan1 = async_with_resilience(real_style_adapter.embed_batch(texts), RetryPolicy(max_attempts=1), None)
    plan2 = async_with_resilience(mock_adapter.embed_batch(texts), RetryPolicy(max_attempts=1), None)
    
    res1 = await perform_async(plan1)
    res2 = await perform_async(plan2)
    
    assert res1 == res2  # identical fake behaviour
```

```python
@given(chunks=st.lists(st.from_type(EmbeddedChunk), max_size=10))
@pytest.mark.asyncio
async def test_pgvector_upsert_idempotence(chunks):
    mock_pool = MockPool()
    adapter = make_pgvector_adapter(mock_pool)
    
    desc = adapter.upsert(chunks)
    plan = async_with_resilience(desc, RetryPolicy(max_attempts=1), None)
    await perform_async(plan)
    
    state1 = mock_pool.snapshot()
    
    # Second identical call
    await perform_async(plan)
    state2 = mock_pool.snapshot()
    
    assert state1 == state2  # UPSERT + stable ID → no change
```

## 6. Runtime Guarantees

| Operation       | Latency Added | Memory   | Idempotence       |
|-----------------|---------------|----------|-------------------|
| HTTP batch      | O(1) RTT      | O(batch) | Yes               |
| DB upsert       | O(batch)      | O(batch) | Yes (UPSERT+stable ID) |
| Query           | O(log N)      | O(k)     | Yes               |

## 7. Anti-Patterns & Immediate Fixes

| Anti-Pattern                 | Symptom                       | Fix                                      |
|------------------------------|-------------------------------|------------------------------------------|
| Concrete client in core      | Untestable, coupled           | Pure protocol + factory                  |
| Hard-coded retry/timeout     | Inflexible                    | Policies as data in shell                |
| No error taxonomy            | Generic "failed" errors       | Map to specific ErrInfo.code             |
| Non-idempotent write         | Duplicate data on retry       | UPSERT + deterministic ID                |

## 8. Pre-Core Quiz

1. External services are accessed via…? → **Pure protocols**  
2. Concrete implementation lives in…? → **Thin adapter class factories**  
3. Adapter methods return…? → **AsyncAction thunks (never executed on call)**  
4. Resilience policies are applied…? → **Outside the adapter, on the description**  
5. The golden rule? → **Core never sees a concrete client or HTTP status code**

## 9. Post-Core Exercise

1. Define `EmbedPort` and `VectorStorePort` for your real services.  
2. Implement thin adapter factories returning classes.  
3. Replace every direct service call in your pipeline with the protocol version.  
4. Add a fully deterministic equivalence property test using stubbed clients.  
5. Sleep well — your pipeline now survives provider changes without a single core modification.

**Next** → M08C09: Time- and Size-Based Chunking Strategies in Async Pipelines

You now have production-grade, swappable, resilient async adapters for every external service — while the pure core remains eternally untouched.

**M08C08 is now frozen.**
