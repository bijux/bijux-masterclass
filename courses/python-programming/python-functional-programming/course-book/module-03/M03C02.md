# Module 3: Lazy Iteration and Streaming

## Progression Note
By the end of Module 3, you will master lazy generators, itertools mastery, and streaming pipelines that never materialize unnecessary data. This prepares you for safe recursion and error handling in streams (Module 4). See the series progression map in the repo root for full details.

Here's a snippet from the progression map:

| Module | Focus                                   | Key Outcomes                                           |
|--------|-----------------------------------------|--------------------------------------------------------|
| 2      | First-Class Functions & Expressive Python | Configurable pure pipelines without globals           |
| 3      | Lazy Iteration & Generators             | Memory-efficient streaming, itertools mastery, short-circuiting |
| 4      | Recursion & Error Handling in Streams   | Safe recursion, Result/Option, streaming errors        |

## M03C02: Generator Expressions vs List Comprehensions – Memory, Readability & Laws

> **Core question:**  
> How do you replace list comprehensions with generator expressions to eliminate unnecessary materialization, improve readability, and gain short-circuiting — while keeping mathematically tight equivalence laws to the eager version?

This core builds directly on **Core 1**’s generator functions by introducing **generator expressions** — the single most common laziness upgrade in real codebases:
- Use `(f(x) for x in xs if cond)` instead of `[f(x) for x in xs if cond]` for any simple map/filter.
- Achieve O(1) memory for the transform itself with identical syntax.
- Preserve full equivalence when materialised, with explicit prefix and order laws.

We continue the **running project** from `m03-rag.md`, now replacing every remaining list comprehension in the RAG pipeline with generator expressions.

**Audience:** Developers who already use generator functions but still sprinkle list comprehensions throughout their pipelines and wonder why memory usage is still high.

**Outcome:**
1. Spot any list comprehension that produces on the order of tens of thousands of items and instantly know it’s a likely memory footgun.
2. Refactor it to a generator expression (or wrapped gen function) in < 5 lines.
3. Write a Hypothesis property proving full equivalence + prefix equivalence + bounded memory.

---

## 1. Conceptual Foundation

### 1.1 The One-Sentence Rule

> **For any map/filter that does not require random access or multiple passes, use a generator expression with parentheses — never square brackets — unless the result is genuinely small and reused.**

### 1.2 Generator Expressions in One Precise Sentence

> A generator expression is the lazy twin of a list comprehension: identical syntax except `()` instead of `[]`, producing an iterator that yields values on demand with zero pre-allocation.

### 1.3 Why This Matters Now

Core 1 gave you generator functions for complex logic.  
In practice, 80 % of laziness wins come from simply changing `[]` → `()` in existing comprehensions.  
The memory savings are dramatic, the code reads the same, and you instantly gain short-circuiting.

### 1.4 Generator Expressions in 5 Lines

```python
# Eager — allocates everything
squares = [x*x for x in range(10**8)]   # ← multi-GB list on typical 64-bit CPython

# Lazy — allocates nothing until consumed
squares_gen = (x*x for x in range(10**8))   # ← ~100 bytes
print(next(squares_gen))                    # → 0 (only one computed)
```

Because the expression is evaluated lazily, the generator expression is the cheapest laziness upgrade you will ever make.

---

## 2. Mental Model: List Comps vs Gen Exps

### 2.1 One Picture

```text
List Comprehension (Eager)               Generator Expression (Lazy)
+---------------------------+            +------------------------------+
| [f(x) for x in xs]        |            | (f(x) for x in xs)           |
|        ↓                  |            |        ↓                     |
| full list allocated       |            | iterator — yields on pull    |
| memory O(n) instantly     |            | memory O(1)                  |
+---------------------------+            +------------------------------+
   ↑ OOM risk                               ↑ Safe default for pipelines
```

### 2.2 Contract Table

| Aspect                    | List Comprehension                          | Generator Expression                          |
|---------------------------|---------------------------------------------|-----------------------------------------------|
| Memory (transform)        | O(n) additional objects for the result      | O(1) additional transform state               |
| Speed (tiny n)            | Slightly faster                             | Slightly slower                               |
| Readability               | Familiar                                    | Identical syntax                              |
| Short-circuit             | No                                          | Yes                                           |
| Equivalence               | Trivial                                     | list(gen) == list_comp (L1)                   |
| Prefix equivalence        | N/A                                         | islice(gen, k) == list_comp[:k] (L2)          |

Here, “O(1)” is about the transform’s own memory footprint. If a downstream consumer materialises a list, that consumer is responsible for the O(n) allocation — not the generator expression itself.

**When List Comps Win:** ≤ 10 k items and you need random access or multiple passes. Everything else → generator expression.

**Known Pitfalls (memorise these):**
- Late-binding closures → capture with default arg: `lambda x, i=i: ...`
- Immediate `list(gen_exp)` defeats the purpose.
- Nested gen exps stay lazy all the way down.
- `dict(gen_exp)` and `set(gen_exp)` are fine — they materialise only at that point.

---

## 3. Running Project: Lazy Cleaning with Generator Expressions

### 3.1 Normalization Contract (Frozen for Module 3)

| Field      | Transform                                      |
|------------|------------------------------------------------|
| doc_id     | Preserved byte-for-byte                        |
| title      | Preserved byte-for-byte                        |
| abstract   | NFC → casefold → strip (idempotent, pure)      |
| categories | Preserved byte-for-byte                        |

This is the same normalization contract introduced in **M03C01** and reused in all Module 3 cores; any change here must be mirrored there to keep the RAG pipeline behaviour consistent.

### 3.2 Eager Start (Anti-Pattern)

```python
import unicodedata
from rag_types import RawDoc, CleanDoc

def normalize_abstract(s: str) -> str:
    return unicodedata.normalize("NFC", s).casefold().strip()

def eager_clean_docs(docs: list[RawDoc]) -> list[CleanDoc]:
    return [
        CleanDoc(d.doc_id, d.title, normalize_abstract(d.abstract), d.categories)
        for d in docs
    ]                                                               # ← full list
```

**Smells:** Allocates a complete new list of dataclasses even if downstream only needs the first 100 docs.

---

## 4. Refactor to Lazy: Generator Expressions in RAG

### 4.1 The One True Lazy Cleaning Stage

```python
from collections.abc import Iterable, Iterator
import unicodedata

def normalize_abstract(s: str) -> str:
    """Idempotent, pure, locale-agnostic text normalization."""
    return unicodedata.normalize("NFC", s).casefold().strip()

def gen_clean_docs(docs: Iterable[RawDoc]) -> Iterator[CleanDoc]:
    """
    Tight laws (enforced exactly):
      L1: For any finite re-iterable sequence xs:
            list(gen_clean_docs(xs)) == eager_clean_docs(list(xs))
      L2: For any finite re-iterable sequence xs and k ≥ 0:
            list(islice(gen_clean_docs(xs), k)) == eager_clean_docs(list(xs))[:k]
      L3: Output order == input order (doc_id sequence preserved)
      L4: normalize_abstract is idempotent
      L5: Memory during iteration grows only with the size of each element,
          not with the total number of elements (empirically observed on
          representative large inputs: lazy prefix uses much less memory
          than full eager materialisation)
    """
    return (
        CleanDoc(d.doc_id, d.title, normalize_abstract(d.abstract), d.categories)
        for d in docs
    )
```
**Note on input type:** `gen_clean_docs` accepts any `Iterable[RawDoc]`, so you can stream from files, databases, or other generators. Laws L1–L2 (full and prefix equivalence) are stated for finite, re-iterable sequences because they require traversing the input more than once. For one-shot iterables (like another generator), the single lazy traversal is still equivalent to the list comprehension you would have written, but you cannot compute both sides of the equality without materialising the input first.

**Single-use reminder:** Every call to `gen_clean_docs(docs)` returns a fresh generator; each generator instance is single-pass. Once you exhaust it, you must call `gen_clean_docs` again (on a re-iterable `docs`) to traverse the data a second time.


**Wins:**
- Zero pre-allocation of the full cleaned list.
- Same readability as the list comprehension.
- Full short-circuiting and composability with downstream stages.

**Full pipeline snippet (how it actually looks in real code):**

```python
from itertools import islice

cleaned   = gen_clean_docs(read_docs(path))                     # ← gen exp
chunked   = (c for cd in cleaned for c in gen_chunk_doc(cd, env))  # flatmap via gen exp
embedded  = (embed_chunk(c) for c in chunked)                   # map via gen exp
deduped   = structural_dedup_lazy(embedded)                     # later core
limited   = islice(deduped, top_k)                              # short-circuit fence
write_jsonl_atomic(output_path, limited)
```

Every stage is now a generator expression or generator function — the canonical Module 3 style.

---

## 5. Equational Reasoning: Substitution Exercise

```text
gen_clean_docs(docs)
≡ (CleanDoc(...) for d in docs)
≡ iterator that yields exactly the same sequence as the eager list comprehension
≡ list(gen_clean_docs(docs)) == eager_clean_docs(docs)    # L1 proven on re-iterable sequences
```

Because the generator expression is pure and deterministic, you can substitute it anywhere a list was used — as long as you materialise only when truly needed.

---

## 6. Property-Based Testing: Proving Equivalence & Memory Bounds

The tests below enforce:

* `test_equivalence_on_sequences` → L1  
* `test_prefix_equivalence` → L2  
* `test_order_preservation` → L3  
* `test_normalize_idempotent` → L4  
* `test_memory_lazy_vs_eager_prefix` → empirical evidence for L5  

`test_memory_lazy_vs_eager_prefix` is not a mathematical proof of O(1) transform memory — it is a regression guard demonstrating that, for a fixed large workload, the lazy prefix run uses asymmetrically less memory than the fully eager version on real CPython.

### 6.1 Custom Strategy

```python
import hypothesis.strategies as st
from rag_types import RawDoc

raw_doc_st = st.builds(
    RawDoc,
    doc_id=st.text(min_size=1, max_size=20),
    title=st.text(max_size=100),
    abstract=st.text(max_size=5000),
    categories=st.text(max_size=50),
)
doc_list_st = st.lists(raw_doc_st, max_size=500)
```

### 6.2 Full Suite (All Laws Enforced)

```python
from hypothesis import given
import itertools
import tracemalloc

@given(doc_list_st)
def test_equivalence_on_sequences(docs):
    # docs is a concrete list[RawDoc], so L1 applies directly
    assert list(gen_clean_docs(docs)) == eager_clean_docs(docs)

@given(doc_list_st, st.integers(min_value=0, max_value=500))
def test_prefix_equivalence(docs, k):
    eager_prefix = eager_clean_docs(docs)[:k]
    lazy_prefix  = list(itertools.islice(gen_clean_docs(docs), k))
    assert lazy_prefix == eager_prefix

@given(doc_list_st)
def test_order_preservation(docs):
    ids_in  = [d.doc_id for d in docs]
    ids_out = [c.doc_id for c in gen_clean_docs(docs)]
    assert ids_out == ids_in

@given(st.text())
def test_normalize_idempotent(s):
    assert normalize_abstract(normalize_abstract(s)) == normalize_abstract(s)

def test_memory_lazy_vs_eager_prefix():
    # Not a Hypothesis property: environment-dependent, used as a coarse guardrail.
    big_docs = [
        RawDoc(
            doc_id=str(i),
            title="t",
            abstract="x" * 50_000,  # stress abstract size
            categories="c",
        )
        for i in range(5_000)
    ]

    def peak_for(func):
        tracemalloc.start()
        func()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return peak

    eager_peak = peak_for(lambda: eager_clean_docs(big_docs))
    lazy_peak  = peak_for(lambda: list(itertools.islice(gen_clean_docs(big_docs), 100)))

    # Lazy prefix should be substantially cheaper than fully eager materialisation
    assert lazy_peak * 5 < eager_peak
```

### 6.3 Shrinking Demo: Catching a Real Bug

Bad version (forgot `strip`):

```python
def bad_normalize(s: str) -> str:
    return unicodedata.normalize("NFC", s).casefold()   # no strip
```

Property `test_equivalence_on_sequences` instantly fails and shrinks to:

```
Falsifying example:
docs=[RawDoc(doc_id='a', title='', abstract='  a  ', categories='')]
```

→ Bad version has leading/trailing spaces; Hypothesis finds it in < 0.1 s.

---

## 7. When Generator Expressions Aren’t Worth It

- Logic > 2 clauses or nested loops → extract to a proper generator function (readability).
- You genuinely need random access or multiple passes → materialise to list at the consumer.

Example of “too clever” gen exp (don’t do this):

```python
# Hard to read, hard to debug
result = (
    transform(d, i)
    for i, d in enumerate(docs)
    if d.score is not None and d.score > threshold and i % 7 == 0
)
```

Prefer:

```python
def interesting(d: RawDoc, i: int, threshold: float) -> bool:
    return d.score is not None and d.score > threshold and i % 7 == 0

def gen_interesting_docs(
    docs: Iterable[RawDoc], threshold: float
) -> Iterator[tuple[int, RawDoc]]:
    for i, d in enumerate(docs):
        if interesting(d, i, threshold):
            yield i, d
```

Use generator expressions for simple map/filter; lift anything denser into a named generator function.

Everything else → generator expression.

---

## 8. Pre-Core Quiz

1. `(f(x) for x in xs)` allocates the full result? → **No — never.**  
2. `list(gen_exp)` defeats laziness? → **Yes.**  
3. Memory difference on 1 M items? → **Potentially gigabytes vs kilobytes (depending on element size).**  
4. Syntax difference? → **Square brackets [...] vs parentheses (...) around the same comprehension.**  
5. When to prefer list comp? → **Tiny, reused data only.**

## 9. Post-Core Reflection & Exercise

**Reflect:** Audit your codebase — every `[...]` that produces tens of thousands of items or more is now technical debt. Replace it today.

**Project Exercise:** Replace all list comprehensions in the RAG pipeline with generator expressions. Measure peak memory on the full 10 k arXiv dataset (should drop from ~800 MB eager to < 50 MB lazy).

**Next:** M03C03 – Composing Lazy Pipelines with itertools.

You have just eliminated the most common memory leak in Python data code. The rest of Module 3 is pure composition power.
