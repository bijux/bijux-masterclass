# Module 3: Lazy Iteration and Streaming

## Progression Note
By the end of Module 3, you will master lazy generators, itertools mastery, and streaming pipelines that never materialize unnecessary data. This prepares you for safe recursion and error handling in streams (Module 4). See the series progression map in the repo root for full details.

Here's a snippet from the progression map:

| Module | Focus                                   | Key Outcomes                                           |
|--------|-----------------------------------------|--------------------------------------------------------|
| 2      | First-Class Functions & Expressive Python | Configurable pure pipelines without globals           |
| 3      | Lazy Iteration & Generators             | Memory-efficient streaming, itertools mastery, short-circuiting |
| 4      | Recursion & Error Handling in Streams   | Safe recursion, Result/Option, streaming errors        |

## M03C09: Designing Custom Iterator Types – Classes Implementing `__iter__` / `__next__`

> **Core question:**  
> How do you design custom iterator classes that implement `__iter__` and `__next__` for complex stateful logic, ensuring purity, laziness, and equivalence while enabling reuse beyond simple generators?

This core builds on **Core 8**'s time-aware patterns by introducing custom iterator classes:
- Use separate Iterable factories and Iterator cursors for reusability.
- Implement `__iter__` for factories (return fresh cursor), `__next__` for cursors.
- Handle resources with context managers and `.close()`.
- Preserve laziness, purity, and freshness.

We extend the **running project** from Core 8 (FuncPipe RAG Builder from `m03-rag.md`) and add cross-domain examples like stateful CSV readers, log followers with state, and API pagers to prove scalability.

**Audience:** Developers needing complex, stateful streams beyond generators.

**Outcome:**
1. Spot generator limits like no reuse.
2. Build class iterator in < 15 lines.
3. Prove iter laws with Hypothesis.

**Laws (frozen, used across this core):**
- E1 — Equivalence: iter(class_factory(S)) == gen_equiv(S).
- P1 — Purity: No globals; explicit state.
- R1 — Reusability: For any iterable X, iter(X) is not iter(X) and both iterators produce identical sequences.
- I1a — Iterator parity: iter(it) is it and after exhaustion, next(it) raises immediately.
- I1b — Iterable parity: iter(X) is not iter(X) and list(iter(X)) == list(iter(X)).
- CL1 — Cleanup: Resources released on `.close()` or `__exit__`.
- DTR — Determinism: Equal init/state → equal outputs.
- FR — Freshness: Factory calls independent.

**Iterator vs Iterable in Python (memorise):**
- **Iterable**: Has `__iter__` returning an iterator (may be self or fresh cursor). Supports `for x in obj:` and `iter(obj)`.
- **Iterator**: Has `__next__` (raise StopIteration at end) and `__iter__` returning self. Single-pass; exhausted after consumption.

Factories are Iterable; cursors are Iterator.

---

## 1. Conceptual Foundation

### 1.1 The One-Sentence Rule

> **Use separate Iterable factories and Iterator cursors for stateful, reusable iterators with explicit cleanup, when generators lack control.**

### 1.2 Custom Iter in One Precise Sentence

> Iterable factories return fresh Iterators; iterators implement `__next__` logic, `__iter__` return self.

In this series, enables resources; preserves laziness.

### 1.3 Why This Matters Now

Generators one-shot; classes reusable with state.

### 1.4 Custom Iter in 5 Lines

Class example:

```python
class MyIterable:
    def __init__(self, data):
        self.data = data
    def __iter__(self):
        return MyIter(self.data)

class MyIter:
    def __init__(self, data):
        self.data = data
        self.i = 0
    def __iter__(self): return self
    def __next__(self):
        if self.i >= len(self.data): raise StopIteration
        val = self.data[self.i]; self.i += 1; return val
```

Reusable.

### 1.5 Minimal Iter Harness (Extends Core 8)

Build on Core 8; add class patterns:

```python
from typing import Iterator, Iterable, TypeVar
T = TypeVar("T")

class BaseIterable(Iterable[T]):
    def __iter__(self) -> Iterator[T]:
        raise NotImplementedError

class BaseIter(Iterator[T]):
    def __iter__(self) -> 'BaseIter[T]':
        return self
    def __next__(self) -> T:
        raise NotImplementedError
    def close(self):
        pass
```

Use as base; e.g., class MyIterable(BaseIterable[T]): ...

---

## 2. Mental Model: Generator vs Class Iter

### 2.1 One Picture

```text
Generators (Simple)                     Class Iters (Powerful)
+-----------------------+               +------------------------------+
| one-shot, no reuse    |               | stateful, reusable           |
|        ↓              |               |        ↓                     |
| no cleanup control    |               | .close() resources, errors   |
| lightweight           |               | testable, composable         |
+-----------------------+               +------------------------------+
   ↑ Limited / Stateless                   ↑ Flexible / Stateful
```

### 2.2 Behavioral Contract

| Aspect | Generators | Class Iters |
|-------------------|------------------------------|------------------------------|
| Reuse | No (exhausted) | Yes (reset state) |
| Cleanup | Auto | Explicit .close() |
| State | Suspended | Explicit attrs |
| Equivalence | Simple | Via properties |

**Note on Generator Choice:** Simple logic; else class.

**When Not to Class:** No state; use gen.

**Known Pitfalls:**
- Forgotten __iter__ return self.
- State mutation leaks.

**Forbidden Patterns:**
- For iterators: __iter__ not returning self.
- For iterables: __iter__ returning self (violates R1/I1b).
- Enforce with type checks.

**Building Blocks Sidebar:**
- For iterators: __iter__ return self.
- For iterables: __iter__ return fresh cursor.
- __next__ logic/raise.
- .close() cleanup.

**Resource Semantics:** Classes handle close in .close().

**Error Model:** Raise in __next__; cleanup always.

**Purity Note:** Sources (files/APIs/logs) are effectful; purity claims apply to transforms. Cleanup is explicit via .close()/context managers.

---

## 3. Cross-Domain Examples: Proving Scalability

Production-grade examples using the harness. Each stateful, clean.

### 3.1 Example 1: Stateful CSV Reader (Class Iter)

```python
from __future__ import annotations
from typing import Iterator, Iterable, Dict
import csv
from io import TextIOBase

class CsvRows(Iterable[Dict[str, str]]):
    """DictReader: first row becomes header keys."""
    def __init__(self, path: str, *, dialect: str = "excel"):
        self._path = path
        self._dialect = dialect

    def __iter__(self) -> Iterator[Dict[str, str]]:
        return _CsvRowsIter(self._path, self._dialect)

class _CsvRowsIter(Iterator[Dict[str, str]]):
    def __init__(self, path: str, dialect: str):
        self._path = path
        self._dialect = dialect
        self._f: TextIOBase | None = None
        self._rdr: csv.DictReader | None = None

    def __iter__(self) -> "_CsvRowsIter":
        return self

    def __enter__(self):
        self._open()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

    def _open(self) -> None:
        if self._f is None:
            self._f = open(self._path, newline="")
            self._rdr = csv.DictReader(self._f, dialect=self._dialect)

    def __next__(self) -> Dict[str, str]:
        if self._rdr is None:
            self._open()
        try:
            return next(self._rdr)  # type: ignore[arg-type]
        except StopIteration:
            self.close()
            raise

    def close(self) -> None:
        if self._f is not None:
            self._f.close()
            self._f = None
            self._rdr = None
```

**Why it's good:** Cleanup on early stop/close; lazy open in __next__ means plain iteration works.

Usage with guaranteed cleanup:

```python
# Plain iteration (closes on natural exhaustion)
for row in CsvRows("data.csv"):
    process(row)

# Early-stop guaranteed cleanup
with iter(CsvRows("data.csv")) as rows:
    for row in rows:
        process(row)
        if done: break
```

### 3.2 Example 2: Stateful Log Follower (Class Iter)

```python
import io, os, time
from typing import Iterator

class LogFollower(Iterable[str]):
    def __init__(self, path: str, poll: float = 0.2):
        self.path = path
        self.poll = poll

    def __iter__(self) -> Iterator[str]:
        return _LogFollowerIter(self.path, self.poll)

class _LogFollowerIter(Iterator[str]):
    def __init__(self, path: str, poll: float):
        self.path = path
        self.poll = poll
        self._f: io.TextIOBase | None = None
        self._ino: int | None = None

    def __iter__(self) -> "_LogFollowerIter":
        return self

    def __enter__(self):
        self._open()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

    def _open(self):
        self._f = open(self.path, "r", encoding="utf8", errors="replace")
        self._f.seek(0, io.SEEK_END)
        self._ino = os.fstat(self._f.fileno()).st_ino

    def __next__(self) -> str:
        if self._f is None:
            self._open()
        while True:
            line = self._f.readline()
            if line:
                return line.rstrip("\n")
            time.sleep(self.poll)
            try:
                if os.stat(self.path).st_ino != self._ino:
                    self._f.close()
                    self._open()
            except FileNotFoundError:
                pass

    def close(self):
        if self._f is not None:
            self._f.close()
            self._f = None
```

**Why it's good:** Stateful rotation/cleanup.

### 3.3 Example 3: Stateful API Pager

```python
from typing import Iterator, Callable, Any, Optional

class ApiPager(Iterable[dict[str, Any]]):
    def __init__(self, fetch_page: Callable[[Optional[str]], dict[str, Any]]):
        self._fetch_page = fetch_page

    def __iter__(self) -> Iterator[dict[str, Any]]:
        return _ApiPagerIter(self._fetch_page)

class _ApiPagerIter(Iterator[dict[str, Any]]):
    def __init__(self, fetch_page: Callable[[Optional[str]], dict[str, Any]]):
        self._fetch_page = fetch_page
        self._token: Optional[str] = None
        self._current_items: list[dict[str, Any]] = []
        self._idx: int = 0
        self._done: bool = False

    def __iter__(self) -> "_ApiPagerIter":
        return self

    def __next__(self) -> dict[str, Any]:
        while self._idx >= len(self._current_items):
            if self._done:
                raise StopIteration
            page = self._fetch_page(self._token)
            self._current_items = page.get("items", [])
            self._idx = 0
            self._token = page.get("next")
            if not self._token:
                self._done = True
            if not self._current_items and self._done:
                raise StopIteration

        item = self._current_items[self._idx]
        self._idx += 1
        return item
```

**Why it's good:** Stateful token + intra-page cursor; no item loss or duplicate pages.

### 3.4 Example 4: Stateful Telemetry Window

```python
from collections import deque

class RollingAvgSource(Iterable[dict]):
    def __init__(self, src: Iterable[dict], w: int):
        self._src = src
        self._w = w

    def __iter__(self):
        return RollingAvgIter(self._src, self._w)

class RollingAvgIter(Iterator[dict]):
    def __init__(self, src: Iterable[dict], w: int):
        self._src = iter(src)
        self._w = w
        self._buf = deque(maxlen=w)

    def __iter__(self):
        return self

    def __next__(self) -> dict:
        if len(self._buf) < self._w:
            while len(self._buf) < self._w:
                self._buf.append(next(self._src))
        else:
            self._buf.append(next(self._src))
        avg = sum(d["value"] for d in self._buf) / self._w
        return {"avg": avg, "end_ts": self._buf[-1]["ts"]}
```

**Why it's good:** Stateful buffer; fresh on each iter(RollingAvgSource(...)).

### 3.5 Example 5: Stateful FS Walker

```python
import os

class FsWalker(Iterable[str]):
    def __init__(self, root: str):
        self.root = root

    def __iter__(self):
        return _FsWalkerIter(self.root)

class _FsWalkerIter(Iterator[str]):
    def __init__(self, root: str):
        self.walk = os.walk(root)
        self.dirpath = None
        self.files = []

    def __iter__(self):
        return self

    def __next__(self) -> str:
        while not self.files:
            self.dirpath, _, self.files = next(self.walk)
        fn = self.files.pop(0)
        return os.path.join(self.dirpath, fn)
```

**Why it's good:** Stateful walk; fresh on each iter(FsWalker(...)).

### 3.6 Example 6: Stateful N-Gram

```python
class NGramSource(Iterable[tuple[str, ...]]):
    def __init__(self, toks_iterables: Iterable[list[str]], n: int):
        self._toks_iterables = toks_iterables
        self._n = n

    def __iter__(self):
        return NGramIter(self._toks_iterables, self._n)

class NGramIter(Iterator[tuple[str, ...]]):
    def __init__(self, toks_iterables: Iterable[list[str]], n: int):
        self._outer = iter(toks_iterables)
        self._n = n
        self._buf: list[str] = []
        self._i = 0  # sliding index within buffer

    def __iter__(self):
        return self

    def __next__(self) -> tuple[str, ...]:
        while self._i + self._n > len(self._buf):
            self._buf.extend(next(self._outer))
        gram = tuple(self._buf[self._i:self._i + self._n])
        self._i += 1
        if self._i > 1024:
            self._buf = self._buf[self._i:]
            self._i = 0
        return gram
```

**Why it's good:** Stateful overlap; fresh on each iter(NGramSource(...)).

### 3.7 Running Project: Stateful RAG Chunker

Extend RAG with class chunker:

```python
class RagChunks(Iterable[ChunkWithoutEmbedding]):
    def __init__(self, docs: Iterable[RawDoc], env: RagEnv, max_chunks: int):
        self._docs = docs
        self._env = env
        self._max = max_chunks

    def __iter__(self):
        return RagChunker(self._docs, self._env, self._max)

class RagChunker(Iterator[ChunkWithoutEmbedding]):
    def __init__(self, docs: Iterable[RawDoc], env: RagEnv, max_chunks: int):
        self._docs = iter(docs)
        self._env = env
        self._max = max_chunks
        self._emitted = 0
        self._cur: Iterator[ChunkWithoutEmbedding] | None = None

    def __iter__(self):
        return self

    def __next__(self) -> ChunkWithoutEmbedding:
        if self._emitted >= self._max:
            raise StopIteration
        while True:
            if self._cur is None:
                d = next(self._docs)                     # may raise StopIteration
                self._cur = gen_overlapping_chunks(d.doc_id, d.abstract, k=self._env.chunk_size, o=self._env.overlap, tail_policy=self._env.tail_policy)
            try:
                ch = next(self._cur)
                self._emitted += 1
                return ch
            except StopIteration:
                self._cur = None
```

**Wins:** Stateful count/cleanup; fresh on each iter(RagChunks(...)).

---

## 4. Anti-Patterns and Fixes

- **Iterator without __iter__ returning self:** Breaks iterator parity (I1a). **Fix:** def __iter__(self): return self.
- **Iterable returning self in __iter__:** Violates reusability (R1/I1b). **Fix:** Return fresh cursor.
- **No Cleanup:** Leaks resources. **Fix:** .close() close.

---

## 5. Equational Reasoning: Substitution Exercise

**Hand Exercise:** Class to gen → equiv.

**Bug Hunt:** No cleanup; explicit del.

---

## 6. Property-Based Testing: Proving Equivalence (Advanced, Optional)

### 6.1 Custom Strategy

As previous.

### 6.2 Properties

```python
from hypothesis import given, strategies as st
import pytest

@given(st.lists(st.integers(), max_size=50))
def test_iter_self(xs):
    it = MyIter(xs)
    assert iter(it) is it

@given(st.lists(st.text(), max_size=50))
def test_iterable_freshness(lines):
    src = MyIterable(lines)
    it1 = iter(src)
    it2 = iter(src)
    assert it1 is not it2           # R1/I1b
    assert list(it1) == list(it2) == lines

@given(st.lists(st.integers(), max_size=50))
def test_iterator_parity(xs):
    it = MyIter(xs)
    assert iter(it) is it
    assert list(it) == xs
    with pytest.raises(StopIteration):
        next(it)

@given(st.text(min_size=1), st.lists(st.text(), max_size=20))
def test_csv_equiv(header, cells, tmp_path):
    p = tmp_path / "test.csv"
    with p.open("w", newline="") as f:
        f.write(header + "\n")
        for c in cells:
            f.write(c + "\n")

    rows = list(CsvRows(str(p)))
    assert rows == [{header: c} for c in cells]

def test_cleanup(tmp_path):
    p = tmp_path / "test.csv"
    p.write_text("a,b\n1,2\n")
    with iter(CsvRows(str(p))) as it:
        next(it)
    # file closed by __exit__ on the cursor
    # (in practice, test by attempting exclusive open or fd check)
```

### 6.3 Additional for Examples

Similar; e.g., class-CSV == gen equiv.

### 6.4 Shrinking Demo

Bad (no .close()): Leaks resources.

---

## 7. When Class Isn't Worth It

Simple logic; else class.

---

## 8. Pre-Core Quiz

1. Class for? → **Stateful iter.**
2. __iter__ for iterators? → **Return self.**
3. .close()? → **Cleanup.**
4. Equiv? → **Preserved.**
5. Reuse? → **Fresh init.**

## 9. Post-Core Reflection & Exercise

**Reflect:** Find gen limits; refactor to class.

**Project Exercise:** Make RAG chunker class; test cleanup.

**Final Notes:**
- Classes for control; gens for simple.
- Document state per class.
- Test cleanup/del.
- For async iters, see future.

**Next:** Core 10 – Observability for Streams. (Builds on this.)

### Repository Alignment

- Implementation: `module-03/funcpipe-rag-03/src/funcpipe_rag/core/structural_dedup.py::DedupIterator`.
- Tests: `module-03/funcpipe-rag-03/tests/test_module_03.py::test_dedup_iterator_preserves_order`.

## itertools Decision Table – Use This

| Tool       | Use When                                      | Memory   | Pitfall                              | Safe?   |
|------------|-----------------------------------------------|----------|--------------------------------------|---------|
| chain      | Concat many iterables                         | O(1)     | None                                 | Yes     |
| groupby    | Group **contiguous** equal items              | O(1)     | Must sort first if not contiguous    | Yes     |
| tee        | Multiple consumers of same iterator           | O(skew)  | Unbounded skew → memory explosion    | Careful |
| islice     | Skip/take without consuming                   | O(1)     | None                                 | Yes     |
| accumulate | Running totals/reductions                     | O(n)     | Default op is +                      | Yes     |
| compress   | Filter by boolean mask                        | O(1)     | None                                 | Yes     |

**Further Reading:** For the deepest itertools mastery, see the official docs and Dan Bader’s ‘Python Tricks’ chapter on iterators.

> **You now own the most powerful lazy streaming toolkit in Python. Module 4 will show you how to make even failure and resource cleanup lazy and pure.**
