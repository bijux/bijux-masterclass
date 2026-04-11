# Module Dependency Map


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Functional Programming"]
  section["Reference"]
  page["Module Dependency Map"]
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

Use this page when you remember a functional-programming idea but not where it belongs in
the course sequence. The goal is to keep later modules attached to the foundations they
actually depend on.

## Main sequence

```mermaid
graph TD
  m01["01 Purity, Substitution, and Local Reasoning"]
  m02["02 Data-First APIs and Expression Style"]
  m03["03 Iterators, Laziness, and Streaming Dataflow"]
  m04["04 Streaming Resilience and Failure Handling"]
  m05["05 Algebraic Data Modelling and Validation"]
  m06["06 Monadic Flow and Explicit Context"]
  m07["07 Effect Boundaries and Resource Safety"]
  m08["08 Async Pipelines, Backpressure, and Fairness"]
  m09["09 Ecosystem Interop and Boundary Discipline"]
  m10["10 Refactoring, Performance, and Sustainment"]

  m01 --> m02 --> m03 --> m04 --> m05 --> m06
  m03 --> m07 --> m08 --> m09 --> m10
  m05 --> m10
  m06 --> m10
  m08 --> m10
```

## Why the sequence looks like this

| Module | Depends most on | Reason |
| --- | --- | --- |
| 01 | none | purity and substitution are the root of the course's design judgment |
| 02 | 01 | data-first APIs only stay honest when local reasoning is already clear |
| 03 | 01-02 | laziness and iterator pipelines rely on pure, composable steps |
| 04 | 03 | resilient streaming only makes sense once the dataflow is explicit |
| 05 | 01-04 | algebraic modelling and validation need stable pipeline and failure boundaries |
| 06 | 04-05 | explicit context and lawful chaining depend on visible failures and values |
| 07 | 01-06 | effect boundaries matter only after the pure core is legible |
| 08 | 03-07 | async coordination is safest when dataflow and effects are already bounded |
| 09 | 07-08 | interop is a boundary problem after the core and async shells are trustworthy |
| 10 | all earlier modules | sustainment review needs the whole functional design model |

## Fastest safe paths

- new to functional programming: read Modules 01 through 10 in order
- working maintainer: start with Modules 04, 07, 08, and 09, then backfill earlier modules when purity or failure boundaries feel shaky
- FP steward: start with Modules 05, 07, 09, and 10, then return to earlier modules when a boundary or law question points backward
