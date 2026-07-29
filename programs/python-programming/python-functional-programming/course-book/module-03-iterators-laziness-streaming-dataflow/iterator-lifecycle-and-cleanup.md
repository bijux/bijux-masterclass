# Iterator Lifecycle and Cleanup


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Functional Programming"]
  section["Iterators Laziness Streaming Dataflow"]
  page["Iterator Lifecycle and Cleanup"]
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

This lesson closes the custom-iterator hotspot. The main lesson should teach you how to
build the cursor and factory pair. This companion page explains how to review the
lifecycle rules and when a custom iterator is a better choice than a plain generator.

## Lifecycle checklist

For every custom iterator, check these rules:

- iterables return a fresh cursor from `__iter__`
- iterators return `self` from `__iter__`
- exhausted iterators stay exhausted
- resource-backed iterators document whether exhaustion, `close()`, or context exit
  owns release
- two fresh cursors over the same source behave independently

If one of those rules is false, the class is probably carrying state in a way the caller
cannot trust.

## Useful properties

Custom iterators should satisfy:

- iterator parity: `iter(it) is it`
- iterable freshness: `iter(src) is not iter(src)`
- equivalence with the simpler generator baseline where one exists
- cleanup on early stop for resource-backed cursors, when that lifecycle is part of
  the implemented contract

```python
from hypothesis import given
import hypothesis.strategies as st


@given(st.lists(st.text(), max_size=40))
def test_iterable_returns_fresh_cursors(lines):
    src = MyIterable(lines)
    a = iter(src)
    b = iter(src)
    assert a is not b
    assert list(a) == list(b) == lines
```

The important part is not the exact helper name. The important part is the contract: a
reusable iterable must not secretly be a one-shot cursor.

## When a class iterator is worth it

Use the class form when:

- the lifecycle matters and must be explicit
- the iterator carries meaningful state across `next()` calls
- cleanup or context management is part of the contract
- the generator version would hide important mutable cursor state

Stay with a generator when:

- the logic is simple and single-pass
- there is no resource lifecycle to manage
- the class adds more ceremony than clarity

## Capstone check

Before moving on:

1. inspect `core/structural_dedup.py` in the Module 03 reference state;
2. verify that `DedupIterator` is a cursor, returns itself from `__iter__`, and
   remains exhausted;
3. compare its retained `seen` set with a generator implementation;
4. state explicitly that it owns no file, socket, or external resource.

## Cleanup is not automatic on early stop

Exhaustion and abandonment are different events. This loop does not guarantee that
an arbitrary underlying resource closes immediately:

```python
for chunk in resource_backed_chunks():
    if enough(chunk):
        break
```

A generator's `finally` block runs when the generator is closed or finalized, but
relying on eventual garbage collection is not a precise ownership policy. Prefer a
context manager when early stop must release promptly:

```python
with open_chunk_source(path) as chunks:
    for chunk in chunks:
        if enough(chunk):
            break
```

The context owns cleanup; iteration owns value demand. Keeping those contracts
separate makes both reviewable.

Module 03's `DedupIterator`, source factories, and fan helpers do not claim managed
external-resource cleanup. The lesson establishes the question learners must ask;
Module 07 later adds explicit resource policies. Do not infer a cleanup guarantee
from the presence of `yield`.

## Lifecycle evidence

Run the custom iterator proof:

```bash
PYTHONPATH=capstone/module-reference-states/module-03/src \
  python -m pytest -q \
  capstone/module-reference-states/module-03/tests/learning/test_module_03_streaming_dataflow.py \
  -k 'custom_dedup'
```

It proves stable exhaustion, not cleanup. A resource-backed implementation needs a
separate test that records release after normal exhaustion, exception, and early
exit.

## Reflection

- Which iterator in your own codebase really needs explicit cleanup?
- Which one should collapse back into a generator?
- Which review bug would appear if the iterable returned itself instead of a fresh cursor?

**Continue with:** [Streaming Observability](streaming-observability.md)
