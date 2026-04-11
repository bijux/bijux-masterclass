# Imperative to FP Refactor


<!-- page-maps:start -->
## Lesson Map

```mermaid
flowchart LR
  script["Start with one large imperative script"] --> split["Separate configuration, core logic, and boundaries"]
  split --> compose["Reconnect them through explicit modules"]
  compose --> verify["Verify the new structure still preserves behavior"]
```
<!-- page-maps:end -->

This lesson should feel like a trustworthy migration guide. Students are no longer learning isolated tools. They are learning how to use the whole module to reshape a script without losing behavior or creating a maze of half-finished abstractions.

## Start With the Refactor Fear

The hard part of a real refactor is rarely naming the target style. It is deciding where to cut first and how to keep the result understandable while the codebase is in motion.

- If the script mixes parsing, I/O, domain logic, and orchestration, you need a cutting order, not just a wish list.
- If "make it functional" means rewriting everything at once, the lesson is not giving a safe path.
- If a reviewer cannot compare old and new behavior while modules are being extracted, the refactor route is too vague.

## Keep This Question In View

> **Core question:**  
> How do you take a messy imperative script full of loops, globals, and side effects and refactor it into clean FP modules—so the whole codebase becomes composable, testable, and maintainable using only M02C01–M02C09 patterns?

This lesson introduces the refactor as a sequence you can apply:

- turn the entry point into a thin orchestrator instead of a place where all decisions happen
- extract pure logic before polishing abstractions so the behavior becomes easier to preserve
- isolate configuration and effects in explicit modules that support the core instead of dominating it

The running project matters because it shows a realistic end state: not "functional everything," but a codebase where responsibilities are separated clearly enough to test and evolve.

**Audience:** Developers with legacy imperative scripts who want a concrete route from mixed concerns to a modular functional design.  
**Outcome:**  
1. Refactor non-trivial scripts into FP modules + orchestrator in a few small modules.  
2. Spot and fix three refactor smells: global state, implicit I/O, god functions.  
3. Design systems where scripts are just boundaries around pure M02C01–M02C09 code.  
4. Use M02C01–M02C09 patterns to make modules trivially testable.  
5. Perform a full refactor of a real-world script using only M02C01–M02C10.

---

## 1. Conceptual Foundation

### 1.1 Refactoring to FP Modules in One Precise Sentence

> Refactoring imperative scripts turns god scripts with loops and globals into pure FP modules orchestrated by a thin boundary entry point—so the system becomes composable, testable, and maintainable using M02C01–M02C09 patterns.

### 1.2 The One-Sentence Rule

> **Never leave side effects or mutation in module core; push I/O to sealed boundaries, loops to pure functions over lazy pipelines, and orchestration to a single `main`—scripts become data-driven pure modules.**

### 1.3 Why This Matters Now

The previous lessons each removed one source of confusion: hidden config, flag-driven control flow, eager waste, leaky effects, scattered rules, opaque composition. This final lesson shows how those improvements fit together during a real refactor. Students need that synthesis so the module feels like a usable method instead of a stack of disconnected techniques.

### 1.3.1 Refactor Steps Checklist

Use this mechanical checklist to refactor imperative scripts:

- Step 1: Identify and externalize config (PATH, CHUNK_SIZE → AppConfig/RagConfig).
- Step 2: Extract pure core from main (no I/O).
- Step 3: Wrap I/O in boundary functions returning Result.
- Step 4: Build a thin orchestrator that composes boundary + core.

### 1.4 FP Modules as Values in 5 Lines

The next example matters because it demonstrates the final shape to aim for: small pure units that can be configured and reused without rebuilding the whole script around them.

```python
from collections.abc import Callable, Iterable
from functools import partial
from typing import TypedDict

class Item(TypedDict):
    price: float

def calculate_total(items: Iterable[Item], threshold: float) -> float:
    return sum(item["price"] for item in items if item["price"] > threshold)

Pipeline = Callable[[Iterable[Item]], float]
pipelines: dict[str, Pipeline] = {
    "standard": partial(calculate_total, threshold=100.0),
    "high": partial(calculate_total, threshold=500.0),
}
```

Pure modules, bound via partial, allow storage in dicts, composition with M02C01, and testing as values—explicit and modular.

---

## 2. Mental Model: Script Spaghetti vs FP Modules

### 2.1 One Picture

```text
Imperative Script (Messy)               FP Modules (Clean)
+-----------------------+               +---------------------------------------------+
| def main():           |               | # capstone/src/funcpipe_rag/rag/rag_api.py           |
|     data = load()     |               | def full_rag_api_docs(docs, cfg, deps): ... |
|     total = 0         |               | # capstone/src/funcpipe_rag/boundaries/shells/rag_api_shell.py |
|     for item in data: |               | def read_docs(path): ...                    |
|         total += ...  |               | def write_chunks(path, chunks): ...         |
|     save(total)       |               | # capstone/src/funcpipe_rag/boundaries/shells/rag_main.py      |
+-----------------------+               | def orchestrate(args): ...                  |
   ↑ Globals, Mutation                  +---------------------------------------------+
                                         ↑ Pure core + sealed I/O
```

### 2.2 Contract Table

| Aspect            | Imperative Scripts           | FP Modules                   |
|-------------------|------------------------------|------------------------------|
| Structure         | God main()                   | Pure + boundary + main       |
| State             | Globals/mutables             | Frozen config                |
| I/O               | Scattered                    | Sealed boundaries            |
| Testing           | Mock globals                 | Hypothesis pure              |
| Composability     | Monolith                     | Dynamic pipelines            |
| Mutable Defaults in Partials | Breaks Determinism | Use frozen dataclasses or immutable types for configs |

**Note on Script Choice:** Use scripts only for trivial one-offs; always refactor for reuse.

---

## 3. Running Project: FuncPipe RAG Builder

We extend the FuncPipe RAG Builder from `m02-rag.md`:  
- **Dataset:** 10k arXiv CS abstracts (`arxiv_cs_abstracts_10k.csv`).  
- **Goal:** Refactor imperative script to FP modules.  
- **Start:** Imperative version (`core10_start.py`).  
- **End:** Modular FP, preserving equivalence.

### 3.1 Types (Canonical, Used Throughout)

Extend with app config (full, runnable with imports; for reference, AppConfig is...):

```python
from funcpipe_rag import AppConfig, RagConfig, RagEnv, Result, Ok, Err
from funcpipe_rag import RulesConfig, DEFAULT_RULES
from funcpipe_rag import CleanConfig
from funcpipe_rag import DebugConfig  # From M02C09

# For reference, AppConfig is:
# @dataclass(frozen=True)
# class AppConfig:
#     input_path: str
#     output_path: str
#     rag: RagConfig
```

### 3.2 Imperative Start (Anti-Pattern)

```python
# core10_start.py: Imperative RAG script (full, runnable example with imports)
from funcpipe_rag import RawDoc, CleanDoc, Chunk, ChunkWithoutEmbedding
from funcpipe_rag import RagEnv
from funcpipe_rag import gen_chunk_doc, embed_chunk, structural_dedup_chunks
from funcpipe_rag import category_startswith
import csv
import sys

PATH = "arxiv_cs_abstracts_10k.csv"
CHUNK_SIZE = 512


def main():
    global PATH, CHUNK_SIZE
    try:
        with open(PATH) as f:
            reader = csv.DictReader(f)
            docs = [RawDoc(**row) for row in reader]
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    kept = [d for d in docs if category_startswith("cs.")(d)]
    cleaned = [CleanDoc(d.doc_id, d.title, d.abstract.strip().lower(), d.categories) for d in kept]
    chunks = [c for cd in cleaned for c in gen_chunk_doc(cd, RagEnv(CHUNK_SIZE))]
    embedded = [embed_chunk(c) for c in chunks]
    deduped = structural_dedup_chunks(embedded)
    print(f"Processed {len(deduped)} chunks")


if __name__ == "__main__":
    main()
```

**Smells:**  
- Globals (PATH, CHUNK_SIZE).  
- Imperative try/except.  
- Eager lists.  
- Hard-coded rules.

### 3.2.1 Before-and-After Refactoring Snippet (Toy Example)

To cement the transition from imperative script to FP modules, here's an explicit mini-example showing the "ugly before" with globals and loops (a simplified toy separate from the RAG script) and the "clean after" using pure functions and boundaries:

```python
# Before: Ugly imperative script with globals and loops
PATH = "data.csv"
CHUNK_SIZE = 512

def main():
    global PATH, CHUNK_SIZE
    with open(PATH) as f:
        reader = csv.DictReader(f)
        docs = [RawDoc(**row) for row in reader]
    kept = [d for d in docs if d.categories.startswith("cs.")]
    chunks = [c for cd in [CleanDoc(d.doc_id, d.title, d.abstract.strip().lower(), d.categories) for d in kept] for c in gen_chunk_doc(cd, RagEnv(CHUNK_SIZE))]
    print(f"Processed {len(chunks)} chunks")

# After: Pure FP modules with boundaries and orchestrator
# (Imports omitted for brevity; reuse the imports from §4.1/4.2/4.3.)
def rag_core_iter(docs: Iterable[RawDoc], config: RagConfig, deps: RagCoreDeps) -> Iterator[Chunk]:
    return flow(
        lambda: docs,
        ffilter(lambda d: eval_pred(d, config.keep.keep_pred)),
        fmap(deps.cleaner),
        flatmap(partial(gen_chunk_doc, env=config.env)),
        fmap(deps.embedder),
    )()

# Boundary module (see `capstone/src/funcpipe_rag/boundaries/shells/rag_api_shell.py`)
def read_docs(path: str) -> Result[list[RawDoc]]:
    try:
        with open(path) as f:
            reader = csv.DictReader(f)
            return Ok([RawDoc(**row) for row in reader])
    except Exception as e:
        return Err(str(e))

def write_chunks(path: str, chunks: list[Chunk]) -> Result[None]:
    try:
        with open(path, "w") as f:
            json.dump([c.__dict__ for c in chunks], f)
        return Ok(None)
    except Exception as e:
        return Err(str(e))

# Orchestrator (see `capstone/src/funcpipe_rag/boundaries/shells/rag_main.py`)
def orchestrate(args: list[str]) -> Result[None]:
    return result_and_then(boundary_app_config(args), _run)

def _run(cfg: AppConfig) -> Result[None]:
    deps = get_deps(cfg.rag)
    docs_res = read_docs(cfg.input_path)
    core_res = result_map(docs_res, lambda docs: rag_core(docs, cfg.rag, deps))  # rag_core as defined in §4.1 below
    return result_and_then(core_res, lambda res: write_chunks(cfg.output_path, res[0]))
```

This refactor eliminates globals and loops, making the core pure and easier to test—same inputs always yield the same outputs.

### 4.1 Pure Module (Core Logic)

```python
# capstone/src/funcpipe_rag/rag/rag_api.py + capstone/src/funcpipe_rag/rag/config.py
from funcpipe_rag import RagConfig, RagEnv, full_rag_api_docs, get_deps

config = RagConfig(env=RagEnv(512))
deps = get_deps(config)

chunks, obs = full_rag_api_docs(docs, config, deps)
```

**Properties:** Pure, lazy core; materialize for obs.

### 4.2 Boundary Module (Sealed I/O + Config)

```python
# capstone/src/funcpipe_rag/boundaries/shells/rag_main.py (CLI parsing + I/O edges)
from funcpipe_rag.boundaries.shells.rag_main import boundary_app_config, read_docs, write_chunks
```

**Properties:** Sealed effects; CLI parsing. Globals → config fields.

### 4.3 Orchestrator (Thin Main)

```python
# capstone/src/funcpipe_rag/boundaries/shells/rag_main.py (thin orchestrator)
from funcpipe_rag.boundaries.shells.rag_main import orchestrate

res = orchestrate(["--input", "in.csv", "--output", "out.jsonl", "--chunk_size", "512"])
```

**Properties:** Thin; chains Results. Orchestrator decides to run.

### 4.4 Configurator Tie-In (M02C01)

```python
from functools import partial

test_orchestrate = partial(orchestrate, ["--input", "test.csv", "--output", "test.json"])
```

**Wins:** Configurable; composes with partial.

---

## 5. Equational Reasoning: Substitution Exercise

**Hand Exercise:** Substitute in `full_rag_api_docs` / `iter_rag_core`.  
1. Inline `ffilter(partial(eval_pred))` → fixed predicate.  
2. Substitute into flow → pure pipeline.  
3. Result: Core fixed for fixed config/deps.  
**Bug Hunt:** In imperative, globals break substitution.

**Example:**  
- Imperative: `kept = [d for d in docs if ...]` → eager, mutable.  
- Modular: `bound_keep(docs)` → pure, lazy.

---

## 6. Property-Based Testing: Proving Refactor

Use Hypothesis to prove equivalence.

### 6.1 Custom Strategy

From `capstone/tests/conftest.py`.

### 6.2 Refactor Equivalence Property

See the repo’s end-of-Module-02 tests instead of creating new “module-specific” test files:

- `capstone/tests/unit/rag/test_api.py` proves `full_rag_api_docs` matches a baseline built from the pure stages.
- `capstone/tests/unit/rag/test_api.py` exercises the boundary shape (`full_rag_api_path` returns `Ok((chunks, obs))` with a `FakeReader`).
- `capstone/tests/unit/rag/test_api.py` proves `iter_rag_core` is deterministic.
- `capstone/tests/unit/rag/test_stages.py` contains properties for `clean_doc`, `chunk_doc`, `embed_chunk`, and `structural_dedup_chunks`.
- `capstone/tests/unit/fp/test_iter_helpers.py` contains laws and smoke tests for `fmap`, `ffilter`, `flatmap`, and `pipe`.

Baseline equivalence excerpt:

```python
# capstone/tests/unit/rag/test_api.py
from hypothesis import given

from funcpipe_rag import RagConfig, clean_doc, embed_chunk, full_rag_api_docs, gen_chunk_doc, get_deps, structural_dedup_chunks
from tests.conftest import doc_list_strategy, env_strategy


def _baseline_chunks(docs, env):
    cleaned = [clean_doc(d) for d in docs]
    embedded = [embed_chunk(c) for cd in cleaned for c in gen_chunk_doc(cd, env)]
    return structural_dedup_chunks(embedded)


@given(docs=doc_list_strategy(), env=env_strategy())
def test_full_rag_api_docs_matches_baseline(docs, env):
    config = RagConfig(env=env)
    deps = get_deps(config)
    chunks, _ = full_rag_api_docs(docs, config, deps)
    assert chunks == _baseline_chunks(docs, env)
```

---

## 7. When FP Modules Aren't Worth It

Use scripts only in:  
- **Trivial one-offs** (<50 lines).  
- **Legacy wrappers** around modules.  
**Guardrails:** Isolate; prefer modules for tests and reuse.

**Example:**

```python
# Trivial
print(sum([1, 2, 3]))  # OK for one-off
```

---

## 8. Pre-Core Quiz

1. God script? → **Unmaintainable.**  
2. Global state? → **Boundary config + partial.**  
3. Eager loop? → **Pure pipeline.**  
4. `open()` in core? → **Boundary module.**  
5. Prove refactor? → **Hypothesis equivalence.**

---

## 9. Post-Core Reflection & Exercise

**Reflect:** Find a god script. Refactor to pure + boundary + main; add Hypothesis equivalence.  
**Project Exercise:** Apply to RAG script; run properties.  
- Did modules clarify?  
- Did tests cover end-to-end?  
- New composable pipelines?

**End of Module 02.**

Verify all patterns with Hypothesis—examples provided show how to detect impurities like globals or non-determinism.

> **Further Reading:** For more on closures in Python, see 'Fluent Python' by Luciano Ramalho. Explore toolz for advanced partials once comfortable.
