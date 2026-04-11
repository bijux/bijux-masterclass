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

## Useful properties

Reusable stages earn their keep when these claims hold:

- two runs with equal input and equal config return equal output
- calling the same factory twice yields independent executions
- a fenced stage returns the same prefix as the unfenced baseline
- the generic stage and the hand-written domain-specific stage stay equivalent

```python
from hypothesis import given

from tests.conftest import raw_doc_list_strategy, rag_env_strategy


@given(raw_doc_list_strategy(), rag_env_strategy())
def test_stage_factory_is_deterministic(docs, env):
    mk = make_gen_rag_fn(env, 200)
    assert list(mk(docs)) == list(mk(docs))
```

The property is simple on purpose. A factory that cannot satisfy this is not a reusable
functional stage; it is hidden state in nicer clothing.

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

1. inspect the module-03 stage factories under `capstone/_history/worktrees/module-03/src/funcpipe_rag/`
2. compare them with the domain-specific RAG stage they replaced
3. decide whether the reusable surface reduced duplication without hiding behavior

## Reflection

- Which repeated stage in your own codebase should become a factory?
- Which current factory should collapse back into a direct function?
- Which config object is being captured only because the stage boundary is still unclear?

**Continue with:** [Fan-In and Fan-Out](fan-in-and-fan-out.md)
