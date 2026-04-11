# Resource-Aware Streams


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Functional Programming"]
  section["Streaming Resilience Failure Handling"]
  page["Resource-Aware Streams"]
  capstone["Capstone evidence"]

  family --> program --> section --> page
  page -.applies in.-> capstone
```

```mermaid
flowchart LR
  orient["Orient on the page map"] --> read["Read the main claim and examples"]
  read --> inspect["Inspect the related code, proof, or capstone surface"]
  inspect --> verify["Run or review the verification path"]
  verify --> apply["Apply the idea back to the module and capstone"]
```
<!-- page-maps:end -->

Cleanup should feel first-class. Once a stream owns a connection, file handle, or GPU context, its behavior is no longer only about yielded values. It is also about what happens when the consumer stops early or something fails midway.

## Start With the Leak Risk

Resource leaks often hide behind otherwise elegant streaming code. Foreground that risk before wrapper APIs become the main focus.

- If the consumer can stop early, cleanup cannot rely on natural exhaustion alone.
- If a breaker or exception changes control flow, you need to know whether release still happens.
- If resource management is handwritten differently in each pipeline, correctness becomes hard to review and easy to miss.

> **Core question:**  
> How do you guarantee that every resource-holding generator (files, network connections, GPU contexts) is properly closed on normal completion, consumer exceptions, producer exceptions, or early termination from breakers — all while keeping the pipeline pure, lazy, and composable?

This lesson introduces resource-aware streams as explicit cleanup protocols:

- model cleanup obligations as part of the stream abstraction instead of scattered `try/finally` blocks
- guarantee closure under normal exhaustion, exceptions, and early termination
- keep the stream lazy so managing the resource does not accidentally force work early

The persistent-connection example matters because it captures the practical failure mode clearly: the values may look fine, but the lifecycle is wrong.

The naïve solution is manual try/finally around the whole pipeline:

```python
conn = open_connection()
try:
    for chunk in chunks:
        yield embed_via_connection(conn, chunk)
finally:
    conn.close()
```

This works once — but it forgets to close on early break, consumer exceptions, or when you later parallelise.

The production solution wraps the stream in small resource managers whose whole job is to guarantee cleanup on every exit path.

Use this when you open any long-lived resource inside a generator and refuse to leak sockets or memory on errors or aborts.

**Outcome:**  
1. You will wrap any resource-holding generator with automatic cleanup that works on all exit paths.  
2. You will compose nested resources safely and prove closure via Hypothesis.  
3. You will ship a RAG pipeline that never leaks resources — even when breakers abort early.

This section formalises exactly what you should review here: cleanup on all paths, scoped effects, preserved laziness, and compatibility with breakers and exceptions.

---

## Concrete Motivating Example

Same 100 000 chunk tree from previous cores, but now embedding uses a single persistent connection:

```python
def embed_via_connection_stream(chunks_with_path):
    conn = http_pool.acquire()          # long-lived connection
    try:
        for chunk, path in chunks_with_path:
            yield safe_remote_embed(conn, chunk, path)
    finally:
        http_pool.release(conn)         # must run even on early break!
```

If a breaker fires after 10 000 chunks, the `finally` block is not guaranteed to run promptly in a multi-stage pipeline → the connection can remain open until the generator is explicitly closed or garbage-collected.

Desired behaviour:

```python
with managed_stream(lambda: embed_via_connection_stream(chunks_with_path)) as safe_stream:
    for r in circuit_breaker_rate_emit(safe_stream, max_rate=0.2):
        if isinstance(r, Err) and isinstance(r.error, BreakInfo):
            report_circuit_break(r.error)
            break
        process(r)
# → Connection always released, even on early break
```

---

## 1. Laws & Invariants (machine-checked)

| Law                          | Formal Statement                                                                                            | Enforcement |
|------------------------------|-------------------------------------------------------------------------------------------------------------|-------------|
| **Cleanup on All Paths**     | Resource is closed on normal exhaustion, consumer exception, producer exception, and early breaker termination. | `test_cleanup_normal`, `test_cleanup_consumer_exc`, `test_cleanup_producer_exc`, `test_cleanup_on_break`. |
| **Scoped Effects**           | No side effects outside managed enter/exit; wrapper is pure except for the managed resource.               | Reproducibility + no global mutation. |
| **Laziness**                 | Entering manager does not advance the iterator; resource creation semantics match direct use.             | `test_manager_lazy_entry`. |
| **Composition (LIFO)**       | Nested managers close in reverse order (LIFO) on any exit path.                                            | `test_nested_manager_lifo`. |
| **Equivalence**              | Wrapped stream yields identical values to unwrapped (except cleanup).                                      | `test_managed_equivalence`. |

These laws guarantee zero resource leaks in real pipelines.

---

## 2. Decision Table – Which Resource Wrapper Do You Actually Use?

| Resource Type                  | Needs Factory? | Nested? | Recommended Wrapper |
|--------------------------------|----------------|---------|---------------------|
| Simple generator with .close() | No             | No      | `with_resource_stream` |
| Generator from factory         | Yes            | No      | `managed_stream` |
| Multiple resources             | Yes            | Yes     | `nested_managed` |
| Arbitrary closable object      | –              | –       | `auto_close` |

**Always** wrap resource-holding generators.  
**Never** use bare try/finally in pipeline code — use these wrappers.

---

## 3. Public API Surface (end-of-Module-04 refactor note)

Refactor note: resource wrappers live in `funcpipe_rag.policies.resources` (`capstone/src/funcpipe_rag/policies/resources.py`) and are re-exported from `funcpipe_rag.api.core`.

```python
from funcpipe_rag.api.core import auto_close, managed_stream, nested_managed, with_resource_stream

```

---

## 4. Reference Implementations

### 4.1 with_resource_stream – Auto-Close Existing Generator

```python
import contextlib
from types import TracebackType
from contextlib import AbstractContextManager
from typing import Any, Callable, ContextManager, Generic, Iterator, Sequence, TypeVar

R = TypeVar("R")

class _ResourceStream(Generic[R], AbstractContextManager[Iterator[R]]):
    def __init__(self, gen: Iterator[R]) -> None:
        self._gen = gen

    def __enter__(self) -> Iterator[R]:
        return self._gen

    def __exit__(self,
                 exc_type: type[BaseException] | None,
                 exc: BaseException | None,
                 tb: TracebackType | None) -> None:

        close = getattr(self._gen, "close", None)
        if callable(close):
            try:
                close()
            except Exception:
                pass  # swallow to never mask original exception
        return None

def with_resource_stream(gen: Iterator[R]) -> ContextManager[Iterator[R]]:
    return _ResourceStream(gen)
```

### 4.2 managed_stream – Factory-Based Resource

```python
class _ManagedStream(Generic[R], AbstractContextManager[Iterator[R]]):
    def __init__(self, factory: Callable[[], Iterator[R]]) -> None:
        self._factory = factory
        self._gen: Iterator[R] | None = None

    def __enter__(self) -> Iterator[R]:
        self._gen = self._factory()
        return self._gen

    def __exit__(self,
                 exc_type: type[BaseException] | None,
                 exc: BaseException | None,
                 tb: TracebackType | None) -> None:
        if self._gen is not None:
            close = getattr(self._gen, "close", None)
            if callable(close):
                try:
                    close()
                except Exception:
                    pass
        return None

def managed_stream(factory: Callable[[], Iterator[R]]) -> ContextManager[Iterator[R]]:
    return _ManagedStream(factory)
```

### 4.3 nested_managed – Compose Multiple Managers

```python
def nested_managed(managers: Sequence[ContextManager[Any]]) -> ContextManager[tuple[Any, ...]]:
    class _Nested(AbstractContextManager[tuple[Any, ...]]):
        def __init__(self, managers: Sequence[ContextManager[Any]]) -> None:
            self._managers = managers
            self._stack: contextlib.ExitStack | None = None

        def __enter__(self) -> tuple[Any, ...]:
            self._stack = contextlib.ExitStack()
            return tuple(self._stack.enter_context(m) for m in self._managers)

        def __exit__(self,
                     exc_type: type[BaseException] | None,
                     exc: BaseException | None,
                     tb: TracebackType | None) -> None:
            if self._stack is not None:
                self._stack.close()

    return _Nested(managers)
```

### 4.4 auto_close – Universal Closable Wrapper

```python
def auto_close(obj: Any) -> ContextManager[Any]:
    """Close obj if it has .close(); respect existing context protocol; otherwise no-op."""
    if hasattr(obj, "__enter__") and hasattr(obj, "__exit__"):
        return contextlib.nullcontext(obj)  # keep outer protocol in control
    if hasattr(obj, "close"):
        return contextlib.closing(obj)
    return contextlib.nullcontext(obj)
```

### 4.5 Idiomatic RAG Usage with Breakers

```python
def embed_via_connection_stream(chunks_with_path):
    conn = http_pool.acquire()          # long-lived connection
    try:
        for chunk, path in chunks_with_path:
            yield safe_remote_embed(conn, chunk, path)
    finally:
        http_pool.release(conn)         # must run even on early break!

with managed_stream(lambda: embed_via_connection_stream(chunks_with_path)) as safe_stream:
    for r in circuit_breaker_rate_emit(safe_stream, max_rate=0.2):
        if isinstance(r, Err) and isinstance(r.error, BreakInfo):
            report_circuit_break(r.error)
            break
        process(r)
# → Connection always released, even on early break
```

---

## 5. Property-Based Proofs (`capstone/tests/test_resources.py`)

```python
def test_cleanup_normal():
    closed = False
    def gen():
        nonlocal closed
        try:
            yield 1
            yield 2
        finally:
            closed = True
    with with_resource_stream(gen()) as it:
        list(it)
    assert closed

def test_cleanup_on_consumer_exception():
    closed = False
    def gen():
        nonlocal closed
        try:
            yield 1
            yield 2
        finally:
            closed = True
    with with_resource_stream(gen()) as it:
        with pytest.raises(ValueError):
            for x in it:
                if x == 2:
                    raise ValueError("boom")
    assert closed

def test_cleanup_on_partial_iteration():
    closed = False
    def gen():
        nonlocal closed
        try:
            yield from range(1000)
        finally:
            closed = True
    with with_resource_stream(gen()) as it:
        for _ in range(10):
            next(it)
    assert closed

def test_cleanup_on_producer_exception():
    closed = False
    def gen():
        nonlocal closed
        try:
            yield 1
            raise ValueError("producer fail")
        finally:
            closed = True
    with with_resource_stream(gen()) as it:
        with pytest.raises(ValueError):
            list(it)
    assert closed

def test_manager_lazy_entry():
    entered = False
    def factory():
        nonlocal entered
        entered = True
        yield 42
    mgr = managed_stream(factory)
    assert not entered
    with mgr as it:
        assert entered
        assert next(it) == 42

@given(items=st.lists(st.integers()))
def test_cleanup_on_break(items):
    closed = False
    def src():
        nonlocal closed
        try:
            for x in items:
                yield Ok(x) if x != 0 else Err("ZERO")
        finally:
            closed = True
    with with_resource_stream(src()) as s:
        list(short_circuit_on_err_truncate(s))
    assert closed

def test_nested_manager_lifo():
    order = []
    def m1():
        order.append("enter1")
        yield "a"
        order.append("exit1")
    def m2():
        order.append("enter2")
        yield "b"
        order.append("exit2")
    with nested_managed([contextlib.contextmanager(m1), contextlib.contextmanager(m2)]) as (a, b):
        pass
    assert order == ["enter1", "enter2", "exit2", "exit1"]

def test_managed_equivalence():
    def factory():
        yield from range(10)
    with managed_stream(factory) as it:
        assert list(it) == list(range(10))
```

---

## 6. Big-O & Allocation Guarantees

| Variant              | Time          | Heap          | Laziness |
|----------------------|---------------|---------------|----------|
| with_resource_stream | O(N)          | O(1)          | Yes      |
| managed_stream       | O(N)          | O(1)          | Yes      |
| nested_managed       | O(N)          | O(#managers)  | Yes      |
| auto_close           | O(1)          | O(1)          | Yes      |

Constant overhead; cleanup guaranteed on all paths.

---

## 7. Anti-Patterns & Immediate Fixes

| Anti-Pattern                   | Symptom                  | Fix                              |
|--------------------------------|--------------------------|----------------------------------|
| Manual try/finally in generators | Leaks on early break    | Use `with_resource_stream`       |
| Bare generators with resources | Leaks on exceptions     | Use `managed_stream` for factories |
| Nested manual cleanup          | Complex/error-prone     | Use `nested_managed`             |

---

## 8. Pre-Core Quiz

1. with_resource_stream for…? → **Auto-close existing generator**  
2. managed_stream for…? → **Factory-created resource streams**  
3. nested_managed for…? → **Compose multiple context managers**  
4. auto_close for…? → **Any object with .close()**  
5. Cleanup guaranteed on…? → **All exit paths including breakers**

## 9. Post-Core Exercise

1. Wrap a file-reading generator with `with_resource_stream` → test cleanup on partial iteration.  
2. Use `managed_stream` for temporary files → test on early breaker.  
3. Compose three nested resources → verify LIFO closure order.  
4. Add `auto_close` to your embedder → verify no leaks on OOM.

**Continue with:** [Functional Retries](../module-04-streaming-resilience-failure-handling/functional-retries.md)

You now have the complete toolkit to never leak a resource again — even when everything goes wrong. The rest of Module 4 is about retries and final reporting.
