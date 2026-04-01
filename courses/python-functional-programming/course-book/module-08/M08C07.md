# M08C07: Integrating Pure FuncPipe Core with Async Edges Cleanly

**Module 08 – Main Track Core**  
> **Main track**: Cores 1–10 (Async / Concurrent Pipelines → Production).  
> This is a **required** core. The pure synchronous core is the crown jewel of the entire system — and it must never be polluted by `await`, event loops, or any knowledge that it is running asynchronously.

## Progression Note
Module 8 is **Async FuncPipe & Backpressure** — the lightweight, production-grade concurrency layer that sits directly on top of Module 7’s effect boundaries.

| Module | Focus                                          | Key Outcomes                                                                 |
|--------|------------------------------------------------|-------------------------------------------------------------------------------|
| 7      | Effect Boundaries & Resource Safety            | Ports & adapters, capability interfaces, resource-safe effect isolation      |
| 8      | Async FuncPipe & Backpressure                  | Async streams, bounded queues, timeouts/retries, fairness & rate limiting    |
| 9      | FP Across Libraries and Frameworks             | Stdlib FP, data/ML stacks, web/CLI/distributed integration                    |
| 10     | Refactoring, Performance, and Future-Proofing  | Systematic refactors, performance budgets, governance & evolution             |

**Core question**  
How do you keep the pure, synchronous FuncPipe core 100 % untouched and instantly unit-testable while still running it efficiently inside a real async, concurrent, backpressure-aware, resilient production pipeline?

We take the pure RAG core we have built since Module 1 and ask the question every scaling team eventually faces:

**“Why did my beautiful pure core turn into an untestable async mess full of `await`, `try/except httpx.TimeoutException`, and event-loop dependencies?”**

The naïve pattern everyone writes first:
```python
# BEFORE – async creep destroys the core
async def rag_god_async(path: str) -> list[EmbeddedChunk]:
    async with aiofiles.open(path) as f:
        lines = [l async for l in f]
    docs = [parse_sync(l) for l in lines]
    cleaned = [await clean_doc_async(d) for d in docs]      # await in core
    chunks = [c for d in cleaned for c in chunk_sync(d)]
    embeddings = await asyncio.gather(*[model.aencode(c.text) for c in chunks])
    ...
```

Async everywhere, core untestable without an event loop, impossible to reason about mathematically.

The production pattern: the core is 100 % synchronous and pure (all domain functions return `Result`). Async edges return descriptions. Lifts turn sync `Result`-returning functions into async descriptions. CPU-bound core steps run in a thread pool. The shell drives everything.

```python
# AFTER – pure sync core + thin async shell
def pure_rag_core(
    raw_lines: list[str],
    env: RagEnv,
) -> Result[list[EmbeddedChunk], ErrInfo]:
    return (
        Ok(raw_lines)
        .and_then(lambda lines: result_traverse(lines, parse_line_sync))
        .and_then(lambda docs: result_traverse(docs, lambda d: clean_doc_sync(d, env)))
        .and_then(lambda docs: result_traverse(docs, lambda d: chunk_doc_sync(d, env)))   # list[list[Chunk]]
        .and_then(lambda chunk_lists: Ok([chunk for chunks in chunk_lists for chunk in chunks]))  # explicit flatten
        .and_then(lambda chunks: result_traverse(chunks, prepare_embed_sync))
        .and_then(lambda reqs: result_traverse(reqs, embed_sync))  # fake sync embed for core tests
    )

def async_rag_description(
    storage: StoragePort,
    path: str,
    env: RagEnv,
    executor: Executor,
) -> AsyncGen[EmbeddedChunk]:
    raw_lines   = async_fetch_raw_lines(storage, path)
    parsed      = async_gen_map(raw_lines, lift_sync(parse_line_sync))
    cleaned     = async_gen_map(parsed, lambda doc: lift_sync_with_executor(clean_doc_sync, executor)(doc, env))
    chunked     = async_gen_flat_map(cleaned, lambda doc: lift_sync_gen_with_executor(chunk_doc_sync, executor)(doc, env))
    prepared    = async_gen_map(chunked, lift_sync_with_executor(prepare_embed_sync, executor))
    embedded    = async_gen_map(prepared, async_embed_request)
    return async_gen_rate_limited(async_gen_fair_merge([embedded]), rate_policy)
```

The core stays pure sync forever. The shell stays thin forever. Adding concurrency/retries/rate-limiting/fairness is a one-line policy change in the description.

**Audience**: Engineers who built a gorgeous pure core and then watched async creep destroy it.

**Outcome**
1. The pure core is 100 % synchronous and instantly unit-testable (no event loop needed).
2. All async, I/O, concurrency, retries, rate limiting, fairness live exclusively in thin adapters and combinators.
3. CPU-bound pure code runs efficiently without blocking the event loop.
4. The entire pipeline is still a pure description — composable, inspectable, and mathematically lawful.

## Tiny Non-Domain Example – Pure Core + Async HTTP

```python
# Pure sync core (binary, Result-returning)
def enrich_user_sync(user: User, posts: list[Post]) -> Result[UserProfile, ErrInfo]:
    top_posts = [p for p in posts if p.score > 50]
    return Ok(UserProfile(user.id, user.name, top_posts))

# Async edges
def async_fetch_user(id: int) -> AsyncAction[User]: ...
def async_fetch_posts(user_id: int) -> AsyncGen[Post]: ...

# Integration
def user_profile_description(user_id: int, executor: Executor) -> AsyncAction[UserProfile]:
    user  = async_fetch_user(user_id)
    posts = async_fetch_posts(user_id)
    enrich = lift_sync_with_executor(enrich_user_sync, executor)
    return async_bind(
        async_tuple(user, async_collect(posts)),
        lambda user_posts: enrich(user_posts[0], user_posts[1]),
    )
```

Core unchanged. Async completely isolated.

## Why Keep the Core 100 % Synchronous and Pure? (Three bullets every engineer should internalise)
- **Instant unit tests**: No event loop, no fakes, no `@pytest.mark.asyncio` — just pure functions, Hypothesis, done.
- **Mathematical reasoning**: Monad laws, equational reasoning, referential transparency — everything from Module 6 still applies exactly.
- **CPU efficiency**: Heavy pure transforms run in `ThreadPoolExecutor` without starving the event loop.

## 1. Laws & Invariants (machine-checked)

| Law                       | Statement                                                                                 | Enforcement                     |
|---------------------------|-------------------------------------------------------------------------------------------|---------------------------------|
| Core Purity               | Every function under `domain/core/` is synchronous and pure (no `await`, no I/O)         | mypy + CI grep forbid           |
| Lift Equivalence          | For any pure, non-raising Result-returning f: `lift_sync(f)(*args)()` ≡ `async_from_result(f(*args))()` (logical time) | Hypothesis + fake executor      |
| Description Purity        | All lifts and combinators return thunks that create fresh coroutines                     | Static analysis                 |
| Error Propagation         | Exceptions in lifted sync functions → `Err(ErrInfo.from_exc(e))`                         | Property tests                  |
| No Async in Core          | Zero `async def` or `await` under `domain/core/`                                          | CI forbid list                  |

`async_from_result(r: Result[T, ErrInfo]) -> AsyncAction[T]` is the canonical constructor that simply wraps an existing `Result` in the async layer (no computation).

## 2. Decision Table – Where Does Code Belong?

| Code Type                      | Synchronous? | Contains I/O? | Layer           | Reason                                    |
|--------------------------------|--------------|---------------|-----------------|-------------------------------------------|
| Business logic, parsing, chunking, validation | Yes          | No            | Pure Core       | Testable, composable, mathematical        |
| HTTP, DB, file reads           | No           | Yes           | Async Adapter   | Real concurrency, backpressure            |
| CPU-heavy pure transforms      | Yes          | No            | Core + Executor | Prevent event loop blocking               |
| Orchestration, policies        | No           | No            | Description     | Pure async wiring                         |

If it can be sync and pure → it must be in the core.

## 3. Public API – Canonical Types & Lifts

```python
# Repo implementation lives in:
# - funcpipe_rag/domain/effects/async_/plan.py  (AsyncPlan / AsyncAction)
# - funcpipe_rag/domain/effects/async_/stream.py (AsyncGen + chunking + fan-in)
# - funcpipe_rag/domain/effects/async_/lifts.py (lift_sync* helpers)

# Recap from earlier cores
AsyncAction[T] = Callable[[], Awaitable[Result[T, ErrInfo]]]   # thunk → fresh coroutine
AsyncGen[T]    = Callable[[], AsyncIterator[Result[T, ErrInfo]]]

# Domain/core functions return Result; Async adds the second layer (time/async)
def async_from_result(r: Result[T, ErrInfo]) -> AsyncAction[T]:
    async def _act() -> Result[T, ErrInfo]:
        return r
    return lambda: _act()

# Lifts accept Result-returning functions and simply add the async layer
def lift_sync(
    f: Callable[..., Result[T, ErrInfo]]
) -> Callable[..., AsyncAction[T]]:
    def lifted(*args: Any, **kwargs: Any) -> AsyncAction[T]:
        async def _act() -> Result[T, ErrInfo]:
            try:
                return f(*args, **kwargs)
            except Exception as e:
                return Err(ErrInfo.from_exc(e))
        return lambda: _act()
    return lifted

def lift_sync_with_executor(
    f: Callable[..., Result[T, ErrInfo]],
    executor: Executor,
) -> Callable[..., AsyncAction[T]]:
    def lifted(*args: Any, **kwargs: Any) -> AsyncAction[T]:
        async def _act() -> Result[T, ErrInfo]:
            loop = asyncio.get_running_loop()
            try:
                return await loop.run_in_executor(executor, lambda: f(*args, **kwargs))
            except Exception as e:
                return Err(ErrInfo.from_exc(e))
        return lambda: _act()
    return lifted

def lift_sync_gen_with_executor(
    f: Callable[..., Result[list[T], ErrInfo]],
    executor: Executor,
) -> Callable[..., AsyncGen[T]]:
    def lifted(*args: Any, **kwargs: Any) -> AsyncGen[T]:
        async def _gen() -> AsyncIterator[Result[T, ErrInfo]]:
            loop = asyncio.get_running_loop()
            try:
                res = await loop.run_in_executor(executor, lambda: f(*args, **kwargs))
                if isinstance(res, Ok):
                    for item in res.value:
                        yield Ok(item)
                else:
                    yield res
            except Exception as e:
                yield Err(ErrInfo.from_exc(e))
        return lambda: _gen()
    return lifted
```

## 4. Before → After – Pure Core RAG Pipeline

In the core, the chunking function has the explicit domain type:

```python
chunk_doc_sync: Callable[[Doc, RagEnv], Result[list[Chunk], ErrInfo]]
```

```python
# AFTER – pure sync core + thin async shell
def pure_rag_core(
    raw_lines: list[str],
    env: RagEnv,
) -> Result[list[EmbeddedChunk], ErrInfo]:
    return (
        Ok(raw_lines)
        .and_then(lambda lines: result_traverse(lines, parse_line_sync))
        .and_then(lambda docs: result_traverse(docs, lambda d: clean_doc_sync(d, env)))
        .and_then(lambda docs: result_traverse(docs, lambda d: chunk_doc_sync(d, env)))   # list[list[Chunk]]
        .and_then(lambda chunk_lists: Ok([chunk for chunks in chunk_lists for chunk in chunks]))  # explicit flatten
        .and_then(lambda chunks: result_traverse(chunks, prepare_embed_sync))
        .and_then(lambda reqs: result_traverse(reqs, embed_sync))  # fake sync embed for core tests
    )

def async_rag_description(
    storage: StoragePort,
    path: str,
    env: RagEnv,
    executor: Executor,
) -> AsyncGen[EmbeddedChunk]:
    raw_lines   = async_fetch_raw_lines(storage, path)
    parsed      = async_gen_map(raw_lines, lift_sync(parse_line_sync))
    cleaned     = async_gen_map(parsed, lambda doc: lift_sync_with_executor(clean_doc_sync, executor)(doc, env))
    chunked     = async_gen_flat_map(cleaned, lambda doc: lift_sync_gen_with_executor(chunk_doc_sync, executor)(doc, env))
    prepared    = async_gen_map(chunked, lift_sync_with_executor(prepare_embed_sync, executor))
    embedded    = async_gen_map(prepared, async_embed_request)
    return async_gen_rate_limited(async_gen_fair_merge([embedded]), rate_policy)
```

## 5. Property-Based Proofs (all pass in CI)

```python
@given(raw_lines=st.lists(st.text(), max_size=100), env=st.from_type(RagEnv))
def test_pure_core_deterministic(raw_lines, env):
    res1 = pure_rag_core(raw_lines, env)
    res2 = pure_rag_core(raw_lines, env)
    assert res1 == res2

@pytest.mark.asyncio
@given(raw_lines=st.lists(st.text(), max_size=50))
async def test_layered_pipeline_equivalence(raw_lines):
    env = RagEnv(chunk_size=512)
    mock_storage = MockStorage("\n".join(raw_lines))

    # Expected from pure core (using fake sync embed)
    # In this test, async_embed_request is wired to the same deterministic fake as embed_sync
    expected = pure_rag_core(raw_lines, env)

    with ThreadPoolExecutor() as executor:
        desc = async_rag_description(mock_storage, "path", env, executor)
        results: list[Result[EmbeddedChunk, ErrInfo]] = [r async for r in desc()]

    # Compare success values (ignore ordering if needed)
    if isinstance(expected, Ok):
        actual_values = [r.value for r in results if isinstance(r, Ok)]
        assert sorted(actual_values, key=lambda c: c.id) == sorted(expected.value, key=lambda c: c.id)
    else:
        assert any(isinstance(r, Err) for r in results)
```

## 6. Runtime Guarantees

| Component         | Synchronous? | Blocks Event Loop? | Memory   | Notes                                      |
|-------------------|--------------|--------------------|----------|--------------------------------------------|
| Pure Core         | Yes          | Never              | O(input) | Instant unit tests                         |
| Async Adapters    | No           | No                 | O(1)     | Real I/O                                   |
| Lifted CPU steps  | Yes (thread) | No                 | O(1)     | ThreadPoolExecutor prevents blocking       |

## 7. Anti-Patterns & Immediate Fixes

| Anti-Pattern                  | Symptom                          | Fix                                      |
|-------------------------------|----------------------------------|------------------------------------------|
| `await` or `async def` in core| Impossible sync tests            | Move to adapters, use lifts              |
| Blocking calls in async code  | Starved event loop               | `lift_sync_with_executor`                |
| Mixed sync/async in same file | Confusion, leaks                 | Strict layer separation                  |
| Direct I/O in core            | Untestable, impure               | Ports + adapters only                    |

## 8. Pre-Core Quiz

1. The pure core is…? → **100 % synchronous and pure**  
2. CPU-bound pure code runs in…? → **ThreadPoolExecutor via lifts**  
3. Async lives in…? → **Thin adapters and combinators only**  
4. Integration is done via…? → **Lifts that turn sync Result-returning functions → async descriptions**  
5. The golden rule? → **Core never knows it’s running async**

## 9. Post-Core Exercise

1. Extract your real pipeline’s business logic into pure sync functions returning `Result`.  
2. Write the async adapters for your real I/O.  
3. Lift everything and compose the description.  
4. Add the equivalence property test between pure core and layered pipeline.  
5. Delete every `await` that was previously in your core. Celebrate.

**Next** → M08C08: Designing Async Adapters for External Services (HTTP, DB) from Pure Interfaces

You now have a pure, synchronous, instantly testable core running efficiently inside a full async, backpressure-safe, resilient, rate-limited, fair pipeline — without a single line of async in the core.

**M08C07 is now frozen.**
