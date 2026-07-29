# Module 01 Exercises

Work against:

```text
capstone/module-reference-states/module-01
```

Keep the tracked snapshot unchanged unless an exercise explicitly asks you to make a
local copy. Start by running:

```bash
PYTHONPATH=capstone/module-reference-states/module-01/src \
  python -m pytest -q \
  capstone/module-reference-states/module-01/tests/learning/test_module_01_purity_foundations.py
```

Your work is complete only when that baseline still passes.

## Exercise 1: Trace one value through the pure core

Starting context: `RawDoc`, `RagEnv`, and the four functions in
`pipeline_stages.py`.

Use this input:

```python
RawDoc(
    doc_id="paper-7",
    title="Substitution",
    abstract="  Pure   values compose  ",
    categories="cs.PL",
)
```

and `RagEnv(chunk_size=6)`.

Produce:

- the exact `CleanDoc`;
- every chunk's text, start, and end;
- the number and range of embedding components;
- the final canonical key order;
- a classification of each transition as pure value work or effect.

Constraints:

- derive values by calling the tracked implementation;
- do not hard-code an embedding tuple in application code;
- do not perform file I/O;
- preserve the exact-positive-integer `RagEnv` invariant.

Expected evidence:

- a runnable test with explicit assertions;
- a short explanation of why equal chunk text gets equal embedding even when identity
  differs.

Acceptance checks:

```text
cleaned abstract == "pure values compose"
concatenated chunk text == cleaned abstract
every embedding has 16 values in [0.0, 1.0]
structural deduplication of final output changes nothing
```

## Exercise 2: Repair a mixed transformation

Starting context: this deliberately mixed helper:

```python
seen_ids: list[str] = []


def normalize_batch(docs: list[RawDoc]) -> list[CleanDoc]:
    result: list[CleanDoc] = []
    for doc in docs:
        seen_ids.append(doc.doc_id)
        result.append(clean_doc(doc))
    return result
```

Objective: separate the returned-value transformation from audit recording.

Constraints:

- the pure function may depend only on its argument;
- it must not mutate the input list or its elements;
- do not hide `seen_ids` in a default argument, closure, class, or cache;
- preserve document order and `clean_doc` behavior;
- keep recording at an explicitly effectful caller.

Expected evidence:

- two calls with equal input return equal output;
- the pure call leaves `seen_ids` unchanged;
- the effectful caller records each ID once;
- a substitution explanation identifies why the original fails.

State what your tests prove and why they do not prove the absence of every possible
hidden effect.

## Exercise 3: Earn a typed composition

Starting context: `RagPipe`, `clean_doc`, and `chunk_doc`.

Implement in an exercise file:

```python
def chunk_count(env: RagEnv) -> Callable[[CleanDoc], int]:
    ...
```

Then build:

```python
count_chunks = RagPipe(clean_doc).then(chunk_count(RagEnv(chunk_size=5)))
```

Constraints:

- use exact annotations without `Any`;
- return a callable specialized to one immutable `RagEnv`;
- do not modify `RagPipe`;
- do not add a generic flat-map combinator;
- preserve empty-abstract behavior.

Expected evidence:

- examples for empty text, exact-size text, and a final short chunk;
- a static-review note showing why
  `RagPipe(clean_doc).then(embed_chunk)` is incompatible;
- a judgment about whether the adapter belongs in Module 01 production code.

The earlier contract that must remain true is full text coverage by `chunk_doc`.

## Exercise 4: Test the effect boundary

Starting context: `rag_shell.py`. Use pytest's `tmp_path`; do not write outside the
test directory.

Objective: prove the narrow CSV-to-JSONL adapter calls the same pure core used by
Module 01.

Cover:

- a valid two-row CSV;
- a header-only CSV;
- a row missing a required `RawDoc` field;
- a missing input path.

Constraints:

- derive expected valid output with `full_rag`;
- parse JSONL instead of comparing incidental whitespace;
- assert the documented exception type for each failure;
- do not add retry, atomic-write, logging, or protocol abstractions;
- do not weaken the pure-core learning proof.

Expected evidence:

- focused shell tests;
- a table classifying each operation in `rag_shell` as read effect, pure transform, or
  write effect;
- an explicit note that direct output may be partial if writing fails.

Acceptance checks:

- valid output content matches `full_rag`;
- header-only input creates an empty output file;
- malformed row translation mentions the source path;
- missing path behavior is reported exactly as implemented.

## Exercise 5: Review a false fixed-point claim

A reviewer proposes:

```python
assert full_rag(full_rag(docs, env), env) == full_rag(docs, env)
```

Objective: replace the claim with a well-typed law and explain the difference between
determinism, idempotence, and canonicalization.

Constraints:

- use the tracked public signatures;
- name the function to which idempotence actually applies;
- include a counterexample that is deterministic but not idempotent;
- include the unique-document-ID assumption for order independence.

Expected evidence:

- one type-based rejection of the proposed expression;
- one passing fixed-point assertion;
- one passing canonical-order assertion;
- one paragraph stating what neither assertion proves.

Preserve all Module 01 learning and property tests.

## Completion route

Run both proof surfaces:

```bash
PYTHONPATH=capstone/module-reference-states/module-01/src \
  python -m pytest -q \
  capstone/module-reference-states/module-01/tests/learning/test_module_01_purity_foundations.py \
  capstone/module-reference-states/module-01/tests/test_laws.py
```

Before reading the answers, be able to identify:

- the exact application behavior your work exercised;
- the earlier invariant each change preserved;
- the strongest claim your evidence supports;
- at least one claim it does not support.
