# Module 09 Refactoring Guide


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  module["Module 09"] --> guide["Refactoring Guide"]
  guide --> worktree["_history/worktrees/module-09"]
  worktree --> next["Module 10"]
```

```mermaid
flowchart TD
  wrapper["Inspect interop wrappers"] --> config["Check explicit configuration flow"]
  config --> stdlib["Review stdlib and library boundaries"]
  stdlib --> team["Compare team-facing adoption surfaces"]
  team --> move["Advance only when interop stays deliberate"]
```
<!-- page-maps:end -->

This guide closes Module 09. The real question is whether the course discipline survives
contact with normal Python libraries, service boundaries, and team conventions.

## Stable comparison route

1. run `make PROGRAM=python-programming/python-functional-programming history-refresh`
2. open `capstone/_history/worktrees/module-09/src/funcpipe_rag/`
3. compare `interop/`, `pipelines/`, and the surrounding core packages they protect
4. read the interop and configured-pipeline tests under `capstone/_history/worktrees/module-09/tests/`

## What to refactor toward

- wrappers that let outside libraries serve the design instead of rewriting it
- explicit configuration through CLI, file, and service surfaces
- adoption patterns a team can repeat without guessing where purity ends
- integration points that stay reviewable because the core contract remains visible

## Exit standard

Before Module 10, you should be able to explain how external tools fit the architecture
without being allowed to define the architecture.
