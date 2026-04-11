# Contract Tests for Repositories and Adapters


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Object-Oriented Programming"]
  section["Testing Contracts Verification Depth"]
  page["Contract Tests for Repositories and Adapters"]
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

## Purpose

Prove that interchangeable infrastructure implementations honor the same semantic
contract instead of only passing their own hand-picked test cases.

## 1. A Contract Test Defines Shared Truth

If both an in-memory repository and a database repository claim to implement the same
interface, they should satisfy the same behavior:

- load missing object behavior
- duplicate handling
- optimistic conflict detection
- round-trip fidelity

## 2. Adapters Need Contract Tests Too

Metric sources, incident sinks, and file stores often differ in transport details but
share expectations around errors, timeouts, and accepted payload shapes.

## 3. Write the Shared Suite Once

Design tests around the promise, then run them against multiple implementations. This
prevents backend drift from hiding behind copy-pasted test files.

## 4. Keep Honest Differences Explicit

If one adapter supports batching and another does not, either widen the contract
deliberately or split the interfaces. Do not pretend all implementations are equal.

## Practical Guidelines

- Write one shared suite per honest contract.
- Run it against every implementation that claims compatibility.
- Include failure-path behavior, not only successful round-trips.
- Split contracts when capabilities differ materially.

## Exercises for Mastery

1. Extract one shared repository or adapter suite from duplicated tests.
2. Add one failure-path assertion to that shared suite.
3. Identify one interface that should be split because implementations do not truly match.
