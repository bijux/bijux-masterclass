# Pipeline Stage Review and Reuse


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Functional Programming"]
  section["Iterators Laziness Streaming Dataflow"]
  page["Pipeline Stage Review and Reuse"]
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

Read the first diagram as a placement map: this page is one concept inside its parent module, not a detached essay, and the capstone is the pressure test for whether the idea holds. Read the second diagram as the working rhythm for the page: name the problem, study the example, identify the boundary, then carry one review question forward.

This lesson closes the reusable-stage hotspot. The main lesson should teach you how to
build stage factories. This companion page explains how to review those factories and how
to decide whether the extra indirection is actually helping.

## Review route

Ask these questions of any reusable stage:

- does each factory call return a fresh iterator or transform?
- is the captured configuration immutable and explicit?
- can the stage still be explained as a simple input-output contract?
- did the abstraction remove duplication or just move it?

## Review contracts, not factory syntax

Reusable stages earn their keep when these claims hold:

- two runs with equal input and equal config return equal output
- calling the same factory twice yields independent executions
- a fenced stage returns the same prefix as the unfenced baseline
- the generic stage and the hand-written domain-specific stage stay equivalent

```python
from funcpipe_rag import as_source, make_chain

merged = make_chain(as_source((1, 2)), as_source((3,)))

assert list(merged()) == [1, 2, 3]
assert list(merged()) == [1, 2, 3]
```

`Source[T]` means `Callable[[], Iterator[T]]`. Calling a source starts a traversal.
`Transform[A, B]` means `Callable[[Iterable[A]], Iterator[B]]`. Calling a transform
wraps a supplied traversal.

| Question | `Source[T]` | `Transform[A, B]` |
| --- | --- | --- |
| Who owns input creation? | source | caller |
| What should a call create? | fresh input iterator | fresh output traversal |
| FuncPipe example | `as_source(docs)` | `fence_k(100)` |
| Common bug | captured exhausted iterator | retained mutable per-run state |

Determinism requires replayable input. Calling a transform twice with the same
already-consumed generator is not a valid determinism test. Use a tuple, list, or
fresh source call for each run.

## Audit `make_gen_rag_fn`

The real Module 03 signature captures `chunk_size`, `max_chunks`, cleaning config,
and keep rules, then returns a function from an `Iterable[RawDoc]` to an iterator of
chunks. It earns the abstraction because it:

- wires a stable RAG configuration once;
- leaves documents as the explicit varying input;
- creates `gen_bounded_chunks` inside every run;
- exposes the returned iterator rather than silently collecting it.

It does not promise restartability for an input generator supplied by the caller.
The factory owns output traversal state, not the caller's input.

## Test values and freshness separately

```python
def test_factory_value_contract():
    run = make_gen_rag_fn(chunk_size=50, max_chunks=3)
    assert list(run(replayable_docs)) == list(run(replayable_docs))


def test_factory_starts_no_work():
    run = make_gen_rag_fn(chunk_size=50, max_chunks=3)
    stream = run(counted_documents())
    assert requested_documents == 0
    next(stream)
    assert requested_documents == 1
```

The first test proves deterministic values for replayable input. The second proves
execution timing. Neither alone proves both.

## When reuse is worth it

Keep the factory form when:

- the same transformation logic appears in more than one route
- the configuration changes while the stage logic stays the same
- tests need to compare multiple variants cheaply
- the abstraction clarifies the pipeline taxonomy of source, transform, and sink

Do not force it when:

- the code is genuinely one local step
- the factory names are more abstract than the actual work
- the captured configuration is so large nobody can explain it quickly

## Capstone check

Before moving on:

1. inspect `streaming/types.py`, `streaming/compose.py`, and `api/config.py` in the
   Module 03 reference state;
2. classify `as_source`, `fence_k`, and `make_gen_rag_fn` by ownership;
3. run the fresh-source proof:

   ```bash
   PYTHONPATH=capstone/module-reference-states/module-03/src \
     python -m pytest -q \
     capstone/module-reference-states/module-03/tests/learning/test_module_03_streaming_dataflow.py \
     -k 'reusable_source'
   ```

4. reject any abstraction whose demand and retained-state behavior cannot be stated
   more simply than its implementation.

## Reflection

- Which repeated stage in your own codebase should become a factory?
- Which current factory should collapse back into a direct function?
- Which config object is being captured only because the stage boundary is still unclear?

**Continue with:** [Fan-In and Fan-Out](fan-in-and-fan-out.md)
