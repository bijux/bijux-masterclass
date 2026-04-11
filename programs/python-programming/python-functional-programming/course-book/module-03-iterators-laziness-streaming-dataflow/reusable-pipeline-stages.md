# Reusable Pipeline Stages


<!-- page-maps:start -->
## Lesson Map

```mermaid
flowchart LR
  hardcoded["Start with a one-off streaming script"] --> config["Extract the choices into explicit captured configuration"]
  config --> factory["Return a fresh stage or source each time"]
  factory --> reuse["Reuse the stage without hidden globals or shared cursor state"]
```
<!-- page-maps:end -->

This lesson helps distinguish a reusable stage from a script fragment that only looks reusable. The key distinction is whether configuration and iterator freshness are explicit or merely assumed.

## Start With the Reuse Smell

Many codebases have "pipeline helpers" that still read globals, capture mutable state accidentally, or hand back iterators that cannot safely be reused. This lesson needs to make those failure modes obvious.

- If a stage depends on globals, it is configured implicitly rather than honestly.
- If calling the factory twice shares state, it is not producing fresh iterators.
- If you cannot explain what is captured and what is passed in, the reuse boundary is still blurry.

## Keep This Question In View

> **Core question:**  
> How do you build reusable, composable iterator stages using closures and higher-order functions to create configurable pipelines instead of rigid one-off scripts, while preserving purity and equivalence?

This lesson introduces reusable streaming stages as explicit factories:

- capture immutable configuration in a closure instead of reading hidden process state
- return fresh iterators each time so reuse is real rather than accidental
- keep the stage small enough that tests can exercise the contract independently of the full pipeline

The broader examples matter here because the lesson is not only about one RAG pipeline. It is about recognizing a reusable streaming shape that survives across domains.

**Audience:** Developers with ad-hoc streaming scripts who want reusable, testable stages instead of copy-pasted variants.

**Outcome:**
1. Spot hardcoding smells like globals.
2. Refactor to closure-factory in < 10 lines.
3. Prove reuse laws with Hypothesis.

**Laws (frozen, used across this core):**
- E1 — Equivalence: pipe(factory(S)) == eager_equiv(S).
- P1 — Purity: No globals; all config explicit (captured immutably).
- R1 — Reusability: factory() yields fresh iterator each call.
- C1 — Closure parity: partial(fn, a=1)(x) == fn(x, a=1).
- DTR — Determinism: For pure stages, given equal inputs/config, outputs are equal bit-for-bit.
- FR — Freshness: 
  - For Source factories: src() and src() are independent iterators.
  - For Transform factories: mk = factory(config); mk(xs) and mk(xs) are independent iterators.

---

## 1. Conceptual Foundation

### 1.1 The One-Sentence Rule

> **Use closures to make generator factories that take frozen config and return fresh iterators, eliminating globals for reusable pipelines.**

### 1.2 Reusable Stages in One Precise Sentence

> Closures capture immutable config in generator factories for composable, pure stages that are deterministic and fresh on every call.

### 1.3 Why This Matters Now

The previous lessons showed how to make one pipeline lazy and safe. This lesson shows how to keep those properties when a stage needs variants, tests, and reuse across several pipelines. Without an explicit factory boundary, teams often slide back into globals, shared cursors, or duplicated logic.

### 1.4 Reusable Stages in 5 Lines

The next snippet matters because it packages the configuration choice once and then leaves the actual stream input explicit.

```python
def make_gen(env):
    def gen(docs):
        for d in docs:
            yield process(d, env)
    return gen

rag_fn = make_gen(RagEnv(512))
chunks = list(rag_fn(docs))  # configurable
```

Reusable.

### 1.5 Minimal Stage Harness (Foundation for All Examples)

To ensure consistent, type-safe composition, use this protocol and helpers for all stages. We distinguish:
- **Source[T]**: `Callable[[], Iterator[T]]` – Produces data from nothing (e.g., file readers, pagers). Sources may be effectful (I/O, retry, sleep).
- **Transform[A, B]**: Takes input, transforms to output — must be pure.
- **Sink[B]**: Consumes for side-effects (not covered here; fence before sinks).

```python
from typing import TypeVar, Iterable, Iterator, Protocol, Generic, Callable
from itertools import islice
from functools import reduce

A = TypeVar("A"); B = TypeVar("B"); C = TypeVar("C")
Source = Callable[[], Iterator[A]]

class Transform(Protocol, Generic[A, B]):
    def __call__(self, xs: Iterable[A]) -> Iterator[B]: ...

def compose2(s1: Transform[A, B], s2: Transform[B, C]) -> Transform[A, C]:
    def pipe(xs: Iterable[A]) -> Iterator[C]:
        return s2(s1(xs))
    return pipe

def compose(*stages: Transform) -> Transform:
    # Note: intentionally loose typing for simplicity; in production use overloads or fixed-arity versions
    if not stages: raise ValueError("compose needs ≥1 stage")
    return reduce(compose2, stages)

def fmap(fn: Callable[[A], B]) -> Transform[A, B]:
    def stage(xs: Iterable[A]) -> Iterator[B]:
        for x in xs: yield fn(x)
    return stage

def ffilter(pred: Callable[[A], bool]) -> Transform[A, A]:
    def stage(xs: Iterable[A]) -> Iterator[A]:
        for x in xs:
            if pred(x): yield x
    return stage

def fence_k(k: int) -> Transform[A, A]:
    return lambda xs: islice(xs, k)

def source_to_transform(src: Source[A]) -> Transform[None, A]:
    def adapter(_: Iterable[None]) -> Iterator[A]:
        yield from src()
    return adapter
```

This harness promotes explicit composition, type safety, and purity. Use frozen dataclasses for configs to prevent mutation.

---

## 2. Mental Model: Hardcoded vs Reusable

### 2.1 One Picture

```text
Hardcoded Scripts (Rigid)               Reusable Factories (Flexible)
+-----------------------+               +------------------------------+
| globals/env in fn     |               | closure(frozen_config)       |
|        ↓              |               |        ↓                     |
| one-off, untestable   |               | factory() → fresh iter       |
| reuse = copy-paste    |               | composable, testable         |
+-----------------------+               +------------------------------+
   ↑ Brittle / Globals                     ↑ Pure / Configurable
```

### 2.2 Behavioral Contract

| Aspect | Hardcoded (Globals) | Reusable (Closures) |
|-------------------|------------------------------|------------------------------|
| Config | Globals/hardcode | Explicit frozen params |
| Reuse | Copy-paste | Factory call |
| Purity | Hidden state | Pure functions |
| Equivalence | Fragile | Via properties |

**Default to factories; hardcoded scripts are only defensible for tiny, throw-away one-offs.**

**When Not to Use Closures:** Complex state; use classes (later cores).

**Known Pitfalls:**
- Late binding in loops → capture with default args.
- Mutable captured config → use frozen dataclasses.

**Forbidden Patterns:**
- Globals in core.
- Enforce with grep for global.

**Building Blocks Sidebar:**
- Closures for currying.
- lambda for simple.
- def inner for complex.

**Resource Semantics:** Stages must handle cleanup (e.g., files close on early stop).

**Error Model:** Fail-fast; no swallowing. Expose retry as explicit wrappers for sources only.

**Backpressure:** Filter/map → fence → amplify. Enforce with CI guards.

**Taxonomy:** Sources (no input, may be effectful), transforms (pure in→out), sinks (side-effects). Retries only on sources; transforms idempotent.

---

## 3. Cross-Domain Examples: Proving Scalability

To demonstrate reuse beyond RAG, here are production-grade examples using the harness. Each is pure (transforms) or appropriately effectful (sources), configurable, and follows the laws.  
Each `make_*_pipeline` function returns a `Transform[...]` that you can either call directly (e.g. `list(pipeline(xs))`) or plug into larger chains via `compose(...)`.

### 3.1 Example 1: Streaming CSV ETL (Schema Map → Filter → Fence)

```python
import csv
from typing import Any, Callable, Iterator

def make_csv_source(path: str, *, dialect: str = "excel") -> Source[dict[str, str]]:
    def src() -> Iterator[dict[str, str]]:
        f = open(path, newline="")
        try:
            rdr = csv.DictReader(f, dialect=dialect)
            for row in rdr: yield row
        finally:
            f.close()
    return src

def make_project(cols: dict[str, str]) -> Transform[dict[str, str], dict[str, str]]:
    def stage(rows: Iterable[dict[str, str]]) -> Iterator[dict[str, str]]:
        for r in rows:
            yield {o: r[i] for o, i in cols.items()}
    return stage

def make_cast(spec: dict[str, Callable[[str], Any]], *, strict: bool = True) -> Transform[dict[str, str], dict[str, Any]]:
    def stage(rows: Iterable[dict[str, str]]) -> Iterator[dict[str, Any]]:
        for r in rows:
            out = dict(r)
            try:
                for k, caster in spec.items():
                    out[k] = caster(r[k])
                yield out
            except Exception as e:
                if strict: raise
                # else skip silently or log
    return stage

def make_csv_pipeline(path: str, max_rows: int) -> Transform[None, dict[str, Any]]:
    src = make_csv_source(path)
    return compose(
        source_to_transform(src),
        ffilter(lambda r: r.get("status") == "active"),
        make_project({"id": "user_id", "amount": "total"}),
        make_cast({"amount": float}),
        fence_k(max_rows),
    )
```

**Why it's good:** Single-pass, file closes on early stop, fence at the sink, no globals.

### 3.2 Example 2: Log Tail with Regex Filter and Rotation-Safe Reopen

```python
import io, os, re, time

def follow(path: str, poll: float = 0.2) -> Iterator[str]:
    f = open(path, "r", encoding="utf8", errors="replace")
    try:
        f.seek(0, io.SEEK_END)
        ino = os.fstat(f.fileno()).st_ino
        while True:
            line = f.readline()
            if line:
                yield line.rstrip("\n")
            else:
                time.sleep(poll)
                try:
                    if os.stat(path).st_ino != ino:
                        f.close()
                        f = open(path, "r", encoding="utf8", errors="replace")
                        ino = os.fstat(f.fileno()).st_ino
                except FileNotFoundError:
                    time.sleep(poll)
    finally:
        f.close()   # guaranteed cleanup even on early stop

def make_log_source(path: str) -> Source[str]:
    def src() -> Iterator[str]:
        yield from follow(path)
    return src

def make_regex_filter(pattern: str) -> Transform[str, str]:
    rx = re.compile(pattern)
    return ffilter(rx.search)

def make_log_pipeline(path: str, pattern: str, k: int) -> Transform[None, str]:
    src = make_log_source(path)
    return compose(
        source_to_transform(src),
        make_regex_filter(pattern),
        fence_k(k),
    )
```

**Why it's good:** Cleanup guaranteed, rotation handled, bounded output.

### 3.3 Example 3: API Pagination (Pure Generator + Explicit Retry)

```python
from typing import Any, Dict, Callable, Iterator
from time import sleep

def pager(fetch_page: Callable[[str|None], Dict[str, Any]], *, attempts=3) -> Iterator[Dict[str, Any]]:
    token = None
    while True:
        tries = 0
        while tries < attempts:
            try:
                page = fetch_page(token)
                break
            except Exception:
                tries += 1
                sleep(0.5 * tries)
        else:
            raise RuntimeError("page fetch failed")
        for item in page["items"]: yield item
        token = page.get("next")
        if not token: return

def make_api_pipeline(fetch_page: Callable[[str|None], Dict[str, Any]], pred: Callable[[Dict[str, Any]], bool], k: int) -> Transform[None, Dict[str, Any]]:
    raw_src: Source[Dict[str, Any]] = lambda: pager(fetch_page, attempts=3)
    return compose(
        source_to_transform(raw_src),
        ffilter(pred),
        fence_k(k),
    )
```

**Why it's good:** Retries explicit and local to page; no hidden loops or duplicates.

### 3.4 Example 4: Telemetry – Sliding Windows per Device (Contiguity Contract)

```python
from collections import deque
from itertools import groupby
from operator import itemgetter
from collections.abc import Hashable
from typing import Dict, Callable, Iterable, Iterator


def sliding(w: int) -> Transform[Dict, tuple[Dict,...]]:
    def stage(xs: Iterable[Dict]) -> Iterator[tuple[Dict,...]]:
        buf = deque(maxlen=w)
        for x in xs:
            buf.append(x)
            if len(buf) == w:
                yield tuple(buf)
    return stage

def ensure_contiguous(key: Callable[[Dict], Hashable]) -> Transform[Dict, Dict]:
    def stage(xs: Iterable[Dict]) -> Iterator[Dict]:
        seen, prev = set(), object()
        for i, x in enumerate(xs):
            k = key(x)
            if k != prev and k in seen:
                raise ValueError(f"Non-contiguous key {k!r} at index {i}")
            seen.add(k); prev = k
            yield x
    return stage

def make_rolling_avg_by_device(w: int) -> Transform[Dict, Dict]:
    def stage(xs: Iterable[Dict]) -> Iterator[Dict]:
        key = itemgetter("device_id")
        xs = ensure_contiguous(key)(xs)
        for did, grp in groupby(xs, key=key):
            for window in sliding(w)(grp):
                avg = sum(pt["value"] for pt in window) / w
                yield {"device_id": did, "avg": avg, "end_ts": window[-1]["ts"]}
    return stage
```

**Why it's good:** Bounded memory O(w), explicit contiguity guard, single pass.

### 3.5 Example 5: Filesystem Stream (Walk → Filter → Hash) Without Materialization

```python
import os, hashlib

def make_walk_source(root: str) -> Source[str]:
    def src() -> Iterator[str]:
        for dirpath, _, files in os.walk(root):
            for fn in files: yield os.path.join(dirpath, fn)
    return src

def make_ext_filter(exts: set[str]) -> Transform[str, str]:
    return ffilter(lambda p: os.path.splitext(p)[1].lower() in exts)

def make_sha256() -> Transform[str, tuple[str, str]]:
    def stage(paths: Iterable[str]) -> Iterator[tuple[str, str]]:
        for p in paths:
            h = hashlib.sha256()
            with open(p, "rb") as f:
                for chunk in iter(lambda: f.read(1024 * 1024), b""):
                    h.update(chunk)
            yield (p, h.hexdigest())
    return stage
```

**Why it's good:** No path lists; file handles close; chunked IO.

### 3.6 Example 6: Text N-Grams (Closure Config, Fence, Determinism)

```python
import re

def make_tokenize(rx=r"\w+") -> Transform[str, list[str]]:
    pat = re.compile(rx)
    return fmap(lambda s: pat.findall(s.lower()))

def make_ngrams(n: int) -> Transform[list[str], tuple[str,...]]:
    def stage(tokens_iterables: Iterable[list[str]]) -> Iterator[tuple[str,...]]:
        for toks in tokens_iterables:
            for i in range(len(toks) - n + 1):
                yield tuple(toks[i:i+n])
    return stage

def make_ngram_pipeline(n: int, k: int) -> Transform[str, tuple[str,...]]:
    return compose(
        make_tokenize(),
        make_ngrams(n),
        fence_k(k),
    )
```

**Why it's good:** Configurable amplification; fence prevents explosion.

### 3.7 Running Project: Reusable Stages in RAG (One Among Many)

For continuity, apply to RAG (from Core 5):

```python
from collections.abc import Iterable, Iterator, Callable
from rag_types import RawDoc, RagEnv, ChunkWithoutEmbedding
from core2 import gen_clean_docs
from core5 import gen_bounded_chunks

def make_gen_rag_fn(env: RagEnv, max_chunks: int) -> Callable[[Iterable[RawDoc]], Iterator[ChunkWithoutEmbedding]]:
    """Config → (docs -> chunks). Pure, reusable, single-pass."""
    def pipe(docs: Iterable[RawDoc]) -> Iterator[ChunkWithoutEmbedding]:
        cleaned = gen_clean_docs(docs)
        yield from gen_bounded_chunks(cleaned, env, max_chunks=max_chunks)
    return pipe

# Reusable: Variants
rag_512 = make_gen_rag_fn(RagEnv(512), 1000)
chunks_512 = list(rag_512(docs))
rag_256 = make_gen_rag_fn(RagEnv(256), 500)
chunks_256 = list(rag_256(docs))

# Integration with generic harness (optional but recommended)
rag_stage: Transform[RawDoc, ChunkWithoutEmbedding] = make_gen_rag_fn(env, max_chunks)
pipeline = compose(rag_stage, some_downstream_stage)
```

**Wins:** Configurable; testable. Integrates with harness via compose if needed.

---

## What comes next

The main lesson should leave you able to build a reusable stage from explicit config. The
next step is to test whether that factory is truly fresh, deterministic, and simpler than
the hardcoded alternative it replaced.

Continue with [Pipeline Stage Review and Reuse](pipeline-stage-review-and-reuse.md) before
you move into [Fan-In and Fan-Out](fan-in-and-fan-out.md).
