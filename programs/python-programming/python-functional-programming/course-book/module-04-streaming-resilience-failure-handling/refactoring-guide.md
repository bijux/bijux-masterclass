# Module 04 Refactoring Guide


<!-- page-maps:start -->
## Concept Position

```mermaid
flowchart TD
  family["Python Programming"] --> program["Python Functional Programming"]
  program --> module["Module 04: Streaming Resilience and Failure Handling"]
  module --> concept["Module 04 Refactoring Guide"]
  concept --> capstone["Capstone pressure point"]
```

```mermaid
flowchart TD
  problem["Start with the design or failure question"] --> example["Study the worked example and trade-offs"]
  example --> boundary["Name the boundary this page is trying to protect"]
  boundary --> proof["Carry that question into code review or the capstone"]
```
<!-- page-maps:end -->

Read the first diagram as a placement map: this page is one concept inside its parent module, not a detached essay, and the capstone is the pressure test for whether the idea holds. Read the second diagram as the working rhythm for the page: name the problem, study the example, identify the boundary, then carry one review question forward.

This guide closes Module 04. The goal is to leave the module knowing how a streaming
pipeline fails, retries, and cleans up without making those choices invisible.

## Stable comparison route

1. run `make PROGRAM=python-programming/python-functional-programming history-refresh`
2. open `capstone/_history/worktrees/module-04/src/funcpipe_rag/`
3. compare `result.py`, `policies/`, and the streaming helpers
4. read `capstone/_history/worktrees/module-04/tests/test_result_option.py`, `test_retries.py`, and `test_resources.py`

## What to refactor toward

- failures represented as values instead of hidden exceptions
- retry and cleanup rules expressed as policy, not scattered loops
- stream-level error handling that preserves evidence for each record
- reports that help a reviewer see what failed and why

## Exit standard

Before Module 05, you should be able to name which failures travel in the stream, which
stop the pipeline, and what code proves that cleanup still happens.
