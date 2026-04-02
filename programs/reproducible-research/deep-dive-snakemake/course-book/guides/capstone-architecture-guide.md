<a id="top"></a>

# Capstone Architecture Guide


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  course["Course modules"] --> bridge["Capstone Architecture Guide"]
  bridge --> local["capstone/ARCHITECTURE.md"]
  local --> code["Workflow repository layers"]
```

```mermaid
flowchart LR
  module["Current module"] --> question["Which repository layer carries this idea?"]
  question --> guide["Read the architecture guide"]
  guide --> inspect["Inspect the matching files"]
  inspect --> verify["Use the matching proof route"]
```
<!-- page-maps:end -->

Use this page when a module asks you to review the capstone as a repository architecture,
not only as a runnable workflow.

---

## Recommended Route

1. Read `capstone/ARCHITECTURE.md`.
2. Compare it with [Repository Layer Guide](../repository-layer-guide.md) and [Capstone File Guide](capstone-file-guide.md).
3. Inspect the matching capstone files in the order the architecture guide names them.
4. Use [Proof Matrix](proof-matrix.md) to pick the strongest command for the boundary you are reviewing.

[Back to top](#top)

---

## What The Architecture Should Prove

- workflow meaning is still visible in `Snakefile` and `workflow/rules/`
- helper code has not swallowed the visible rule graph
- profiles and config stay operational rather than analytical
- the publish boundary remains smaller and clearer than the full repository state

[Back to top](#top)

---

## Best Moments To Use It

- after Module 04, when repository growth and interface boundaries become central
- after Module 07, when the full repository architecture becomes part of the lesson
- after Module 10, when reviewing the capstone as a long-lived workflow product

[Back to top](#top)
