# Module 1: Foundational FP Concepts

## Progression Note
By the end of Module 1, you'll master purity laws, write pure functions, and refactor impure code using Hypothesis. This builds the foundation for lazy streams in Module 3. See the series progression map in the repo root for full details.

Here's a snippet from the progression map:

| Module | Focus | Key Outcomes |
|--------|-------|--------------|
| 1: Foundational FP Concepts | Purity, contracts, refactoring | Spot impurities, write pure functions, prove equivalence with Hypothesis |
| 2: ... | ... | ... |
| ... | ... | ... |

## M01C08: Extracting Side Effects – Passing Dependencies Explicitly Instead of Touching Globals

> **Core question:**  
> How do you eliminate hidden side effects (globals, env, time, RNG, I/O) by passing all dependencies explicitly—so that pure logic stays testable, composable, and free from “it works on my machine” bugs?

This core builds on **Core 1**'s mindset, **Core 2**'s contracts, **Core 3**'s immutability, **Core 4**'s composition, **Core 5**'s refactorings, **Core 6**'s combinators, and **Core 7**'s typed pipelines by **isolating impurities at the edges**:  
- Pass config, logger, DB, clock, RNG explicitly (or via frozen context).  
- Pure core: referentially transparent logic only (no effects).  
- Thin shell: effectful wrapper that uses context and delegates to pure core.  
- Use `with_context` (Core 7) + frozen dataclasses for dependency bundles.  
- Never touch `os.getenv`, `datetime.now`, or globals inside pure functions.  

We continue the **running project** from Core 1-7: refactoring the FuncPipe RAG Builder, now isolating effects.

**Audience:** Developers who mastered Core 7 typed pipelines but still see flaky tests from hidden globals, env vars, or time/RNG.  
**Outcome:**  
1. Refactor any function touching globals/env/time/RNG into a pure core + explicit dependency param in < 15 lines.  
2. Bundle dependencies into frozen `@dataclass` contexts (one per layer) and inject via `with_context`.  
3. Write tests (and optionally Hypothesis properties) proving determinism when dependencies are fixed.  
4. Spot and fix three classic effect leaks: implicit `print`/logging, `datetime.now()`, `random.random()`.  
5. Add property tests showing pure core ≡ old impure version (with mocked effects).

---

## 1. Conceptual Foundation

### 1.1 The One-Sentence Rule

> **Never touch globals, env, time, or RNG directly; pass everything explicitly via frozen context bundles—one per layer.**

### 1.2 Explicit Dependencies in One Precise Sentence

> Explicit dependencies mean every effectful operation receives its capabilities via frozen context objects—so the pure core remains deterministic and testable, while thin shells handle I/O, logging, and state.

### 1.3 Why This Matters Now

Explicit dependencies isolate effects, enabling equational reasoning (Core 9) and idempotence (Core 10); without it, hidden state breaks everything.

### 1.4 How This Relates to DI / Ports & Adapters / Clean Architecture

This approach aligns with known patterns:

- **Dependency Injection (DI):** Passing Env bundles is manual DI—simple and zero-deps.

- **Ports & Adapters:** Pure core is the domain; shells are adapters for effects (I/O, time).

- **Clean Architecture:** Core is entities/use-cases (pure); shells are interfaces/infra (effects).

We keep it lightweight: frozen dataclasses + `with_context` instead of full DI frameworks.

### 1.5 Purity Spectrum Table

| Level              | Description                          | Example                              |
|--------------------|--------------------------------------|--------------------------------------|
| Fully Pure         | Explicit inputs/outputs only         | `def add(x: int, y: int) -> int: return x + y` |
| Semi-Pure          | Observational taps (e.g., logging)   | `def add_with_log(x: int, y: int) -> int: log(f"Adding {x}+{y}"); return x + y` |
| Impure             | Globals/I/O/mutation                | `def read_file(path: str) -> str: ...` |

In this core we'll start moving even logging out of the core and into explicit artifacts.

---

## 2. Mental Model: Hidden Effects vs Explicit Context

### 2.1 One Picture

```text
Hidden Effects (globals)                   Explicit Context
+---------------------------+            +---------------------------+
| global LOG                |            | @dataclass(frozen=True)   |
| global CONFIG             |            | class CoreEnv:            |
| datetime.now()            |            |     log: Logger           |
| os.getenv("KEY")          |            |     cfg: Config           |
| random.random()           |            |                           |
| → Heisenbugs everywhere   |            | pure_core(cfg, data)      |
|                           |            | shell = with_context(env, |
|                           |            |         effectful_wrapper)|
+---------------------------+            +---------------------------+
```

### 2.2 Contract Table

| Clause                     | Violation Example                      | Detected By                              |
|----------------------------|----------------------------------------|------------------------------------------|
| Explicit dependencies      | `os.getenv`, `datetime.now()`          | Tests with frozen context                |
| No hidden prints           | `print` inside pure logic              | Code review + linter                     |
| Determinism when fixed     | Same inputs+deps → same outputs        | Tests with frozen context                |
| Mockable effects           | Direct DB calls                        | Unit tests with fake Env                 |
| Edge isolation             | Effects in pipeline middle             | Code review + linter                     |

**Note on Contracts:** Push effects to the edges; prove the core stays pure.

---

## 3. Running Project: Extracting Effects in RAG

Our **running project** (from `module-01/funcpipe-rag-01/README.md`) isolates effects in Core 7's typed pipelines.  
- **Goal:** Push I/O, logging, time/RNG to edges.  
- **Start:** Core 1-7's typed pure functions.  
- **End (this core):** Pure core with explicit values; effects in shell. Semantics aligned with Core 1-7.

### 3.1 Types (Canonical)

These are defined in `module-01/funcpipe-rag-01/src/funcpipe_rag/rag_types.py` (as in Core 1) and imported as needed. No redefinition here.

### 3.2 Effectful Variants (Anti-Patterns in RAG)

Full code:

```python
from funcpipe_rag import RawDoc, CleanDoc, ChunkWithoutEmbedding, Chunk, RagEnv
import hashlib
from datetime import datetime
import random
import logging

# Before refactors: implicit logging, time, RNG inside the pipeline
LOG = logging.getLogger("rag")


def effectful_clean_doc(doc: RawDoc) -> CleanDoc:
    abstract = " ".join(doc.abstract.strip().lower().split())
    LOG.info("Cleaned doc %s", doc.doc_id)
    return CleanDoc(doc.doc_id, doc.title, abstract, doc.categories)


def effectful_chunk_doc(doc: CleanDoc, env: RagEnv) -> list[ChunkWithoutEmbedding]:
    text = doc.abstract
    chunks = [
        ChunkWithoutEmbedding(doc.doc_id, text[i:i + env.chunk_size], i, i + len(text[i:i + env.chunk_size]))
        for i in range(0, len(text), env.chunk_size)
    ]
    random.shuffle(chunks)
    return chunks


def effectful_embed_chunk(chunk: ChunkWithoutEmbedding) -> Chunk:
    if datetime.now() > datetime(2025, 1, 1):
        raise ValueError("Expired")
    h = hashlib.sha256(chunk.text.encode("utf-8")).hexdigest()
    step = 4
    vec = tuple(int(h[i:i + step], 16) / (16 ** step - 1) for i in range(0, 64, step))
    return Chunk(chunk.doc_id, chunk.text, chunk.start, chunk.end, vec)
```

**Smells:** Static global LOG (hidden logging), RNG (nondeterministic), time (flaky).

---

## 4. Refactor to Explicit: Pure Core + Shell in RAG

### 4.1 Pure Core

Pure logic; return values + artifacts (logs, etc.); no effects in core.

Full code:

```python
# module-01/funcpipe-rag-01/src/funcpipe_rag/pipeline_stages.py (pure helpers)
from funcpipe_rag import RawDoc, CleanDoc, ChunkWithoutEmbedding, Chunk, RagEnv
from datetime import datetime
import random
import hashlib
from funcpipe_rag import structural_dedup_chunks


def clean_doc_pure(doc: RawDoc) -> tuple[CleanDoc, list[str]]:
    abstract = " ".join(doc.abstract.strip().lower().split())
    cleaned = CleanDoc(doc.doc_id, doc.title, abstract, doc.categories)
    return cleaned, [f"Cleaned doc {doc.doc_id}"]


def chunk_doc_pure(seed: int, doc: CleanDoc, env: RagEnv) -> tuple[ChunkWithoutEmbedding, ...]:
    # Use seed for deterministic shuffle if needed; here we demonstrate with shuffle
    text = doc.abstract
    chunks = [
        ChunkWithoutEmbedding(doc.doc_id, text[i:i + env.chunk_size], i, i + len(text[i:i + env.chunk_size]))
        for i in range(0, len(text), env.chunk_size)
    ]
    rng = random.Random(seed)
    rng.shuffle(chunks)
    return tuple(chunks)


def embed_chunk_pure(current_time: datetime, chunk: ChunkWithoutEmbedding) -> Chunk:
    if current_time > datetime(2025, 1, 1):
        raise ValueError(
            "Expired")  # We still throw here; in later modules we’ll model this as Result[Chunk, ExpiredError] instead.
    h = hashlib.sha256(chunk.text.encode("utf-8")).hexdigest()
    step = 4
    vec = tuple(int(h[i:i + step], 16) / (16 ** step - 1) for i in range(0, 64, step))
    return Chunk(chunk.doc_id, chunk.text, chunk.start, chunk.end, vec)


def full_rag_pure(seed: int, current_time: datetime, docs: list[RawDoc], env: RagEnv) -> tuple[
    tuple[Chunk, ...], list[str]]:
    cleaned_with_logs = [clean_doc_pure(doc) for doc in docs]
    cleaned = [cleaned for cleaned, _ in cleaned_with_logs]
    logs = [msg for _, messages in cleaned_with_logs for msg in messages]
    chunked = [chunk_doc_pure(seed, doc, env) for doc in cleaned]
    flattened = [chunk for doc_chunks in chunked for chunk in doc_chunks]
    embedded = [embed_chunk_pure(current_time, chunk) for chunk in flattened]
    # structural_dedup_chunks: pure helper that removes duplicate chunks; defined in Core 6
    deduped = structural_dedup_chunks(embedded)
    return tuple(deduped), logs
```

### 4.2 Impure Shell (Edge Only)

Handle effects; delegate to pure core.

Full code:

```python
# module-01/funcpipe-rag-01/src/funcpipe_rag/rag_shell.py (context bundle)
from dataclasses import dataclass
from typing import Callable
from funcpipe_rag import full_rag_pure
from funcpipe_rag import RawDoc, Chunk, RagEnv
from datetime import datetime


@dataclass(frozen=True)
class LogEnv:
    log: Callable[[str], None]


@dataclass(frozen=True)
class TimeEnv:
    now: Callable[[], datetime]


@dataclass(frozen=True)
class RandEnv:
    seed: int


@dataclass(frozen=True)
class RagCoreEnv:
    log_env: LogEnv
    time_env: TimeEnv
    rand_env: RandEnv


def full_rag_shell(env: RagCoreEnv, docs: list[RawDoc], rag_env: RagEnv) -> tuple[Chunk, ...]:
    chunks, logs = full_rag_pure(env.rand_env.seed, env.time_env.now(), docs, rag_env)
    for message in logs:
        env.log_env.log(message)
    return chunks
```

`module-01/funcpipe-rag-01/src/funcpipe_rag/rag_shell.py` remains the only effectful entry point, reading CSV input and writing JSONL output while calling `full_rag_shell` (which delegates into `full_rag_pure`).

**Wins:** Static (no effects in core), deterministic when fixed, semantics aligned with Core 1-7.

### 4.3 Real-World Integration

Frameworks (e.g., Django/Flask) often force globals (request, timezone.now()). Adapt by constructing Env from framework context:

Full code:

```python
# Flask example: Wrap request + timezone into Env
from flask import request, current_app
from datetime import datetime, timezone
from funcpipe_rag import full_rag_shell, RagCoreEnv, LogEnv, TimeEnv, RandEnv
from funcpipe_rag import RawDoc, RagEnv, Chunk
from funcpipe_rag import with_context


def rag_entry(env: RagCoreEnv, docs: list[RawDoc], rag_env: RagEnv) -> tuple[Chunk, ...]:
    return full_rag_shell(env, docs, rag_env)


def flask_handler() -> tuple[Chunk, ...]:
    env = RagCoreEnv(
        log_env=LogEnv(log=current_app.logger.info),
        time_env=TimeEnv(now=lambda: datetime.now(timezone.utc)),
        rand_env=RandEnv(seed=42)
    )
    body = request.json
    docs = [RawDoc(**d) for d in body["docs"]]

    # Freeze env so downstream call sites don't have to thread it through manually.
    full_rag = with_context(env, rag_entry)
    return full_rag(docs, RagEnv(chunk_size=512))
```

**Wins:** Framework globals → explicit Env; pure core stays isolated.

---

## 5. Equational Reasoning: Substitution Exercise

**Hand Exercise:** Replace expressions in `full_rag_pure`.  
1. Inline `clean_doc_pure(doc)` → (CleanDoc, logs).  
2. Substitute into chunk_doc_pure → tuple of chunks (seeded).  
**Bug Hunt:** In effectful_clean_doc, substitution fails (hidden log/time/RNG).

---

## 6. Property-Based Testing: Proving Equivalence (Advanced, Optional)

Use Hypothesis to prove behavior.

You can safely skip this on a first read and still follow later cores—come back when you want to mechanically verify your own refactors.

For side-effect extraction, a couple of simple tests with a fake Env are usually enough; Hypothesis is nice-to-have, not mandatory.

To bridge theory and practice, here's a simple Hypothesis example illustrating impurity detection:

```python
import random
from hypothesis import given
import hypothesis.strategies as st

def impure_random_add(x: int) -> int:
    return x + random.randint(1, 10)  # Non-deterministic

@given(st.integers())
def test_detect_impurity(x):
    assert impure_random_add(x) == impure_random_add(x)  # Falsifies due to randomness

# Hypothesis will quickly find differing outputs for the same x
```

This property test detects the impurity by showing outputs vary for identical inputs—run it to see Hypothesis in action.

### 6.1 Custom Strategy (RAG Domain)

From `module-01/funcpipe-rag-01/tests/conftest.py` (as in Core 1).

### 6.2 Equivalence Property

Properties for stages (using the helpers in `module-01/funcpipe-rag-01/src/funcpipe_rag/rag_shell.py`):

Full code:

```python
# module-01/funcpipe-rag-01/tests/test_laws.py (excerpt)
from hypothesis import given
import hypothesis.strategies as st
from funcpipe_rag import clean_doc_pure, chunk_doc_pure, embed_chunk_pure, full_rag_pure
from funcpipe_rag import RawDoc, CleanDoc, ChunkWithoutEmbedding, Chunk, RagEnv
from funcpipe_rag import RagCoreEnv, LogEnv, TimeEnv, RandEnv, full_rag_shell
from .conftest import raw_doc_strategy, env_strategy, doc_list_strategy
from datetime import datetime

fixed_seed = 42
fixed_time = datetime(2024, 1, 1)


@given(raw_doc_strategy())
def test_clean_doc_pure_deterministic(doc: RawDoc) -> None:
    res1, logs1 = clean_doc_pure(doc)
    res2, logs2 = clean_doc_pure(doc)
    assert res1 == res2 and logs1 == logs2


@given(st.builds(CleanDoc, doc_id=st.text(min_size=1), title=st.text(), abstract=st.text(), categories=st.text()),
       env_strategy())
def test_chunk_doc_pure_deterministic(doc: CleanDoc, env: RagEnv) -> None:
    assert chunk_doc_pure(fixed_seed, doc, env) == chunk_doc_pure(fixed_seed, doc, env)


@given(st.builds(ChunkWithoutEmbedding, doc_id=st.text(min_size=1), text=st.text(min_size=1),
                 start=st.integers(min_value=0), end=st.integers(min_value=1)))
def test_embed_chunk_pure_deterministic(chunk: ChunkWithoutEmbedding) -> None:
    assert embed_chunk_pure(fixed_time, chunk) == embed_chunk_pure(fixed_time, chunk)


@given(doc_list_strategy(), env_strategy())
def test_full_rag_shell_matches_pure(docs: list[RawDoc], env: RagEnv) -> None:
    messages: list[str] = []
    env_bundle = RagCoreEnv(
        log_env=LogEnv(log=messages.append),
        time_env=TimeEnv(now=lambda: fixed_time),
        rand_env=RandEnv(seed=fixed_seed),
    )
    shell_chunks = full_rag_shell(env_bundle, docs, env)
    pure_chunks, logs = full_rag_pure(fixed_seed, fixed_time, docs, env)
    assert shell_chunks == pure_chunks
    assert messages == logs
```

**Note:** Properties enforce determinism, equivalence (up to order, with mocks), invariants.

### 6.3 Shrinking Demo: Catching a Bug

Bad refactor (hidden RNG in chunk):

```python
from funcpipe_rag import CleanDoc, ChunkWithoutEmbedding, RagEnv
import random


def bad_chunk_doc(doc: CleanDoc, env: RagEnv) -> tuple[ChunkWithoutEmbedding, ...]:
    text = doc.abstract
    chunks = [
        ChunkWithoutEmbedding(doc.doc_id, text[i:i + env.chunk_size], i, i + len(text[i:i + env.chunk_size]))
        for i in range(0, len(text), env.chunk_size)
    ]
    random.shuffle(chunks)  # Hidden
    return tuple(chunks)
```

Property:

```python
from hypothesis import given
import hypothesis.strategies as st
from funcpipe_rag import CleanDoc, RagEnv
from .conftest import env_strategy


@given(st.builds(CleanDoc, doc_id=st.text(min_size=1), title=st.text(), abstract=st.text(min_size=1),
                 categories=st.text()), env_strategy())
def test_bad_chunk_doc_deterministic(doc: CleanDoc, env: RagEnv) -> None:
    assert bad_chunk_doc(doc, env) == bad_chunk_doc(doc, env)  # Falsifies due to randomness
```

Hypothesis failure trace (run to verify; example):

```
Falsifying example: test_bad_chunk_doc_deterministic(
    doc=CleanDoc(doc_id='a', title='', abstract='ab', categories=''), 
    env=RagEnv(chunk_size=1),
)
AssertionError
```

- Shrinks to doc with multiple chunks; different shuffles fail equality. Catches bug via shrinking.

---

## 7. When Explicit Dependencies Aren't Worth It

Rarely, for trivial scripts or hot paths, use globals; rely on properties in tests.

---

## 8. Pre-Core Quiz

1. `datetime.now()` inside pure func → violates? → **Explicit dependencies**  
2. Global logger → violates? → **No hidden prints**  
3. Same inputs+fixed env → same output? → **Determinism**  
4. Direct DB call → fix with? → **env.db**  
5. Tool to prove fixed-env determinism? → **Hypothesis**

## 9. Post-Core Reflection & Exercise

**Reflect:** In your code, find one function touching globals/env/time/random/print. Bundle into frozen Env; pull pure core; write shell; inject with `with_context`; add Hypothesis.  
**Project Exercise:** Isolate effects in RAG; run properties on sample data.

All claims (e.g., referential transparency) are verifiable via the provided Hypothesis examples—run them to confirm.

**Further Reading:** For more on purity pitfalls, see 'Fluent Python' Chapter on Functions as Objects. Check free resources like Python.org's FP section or Codecademy's Advanced Python course for readers wanting basics.

**Next:** Core 9 – Equational Reasoning and Local Rewrite Rules for Pure Code. (Builds on this RAG pure core.)
