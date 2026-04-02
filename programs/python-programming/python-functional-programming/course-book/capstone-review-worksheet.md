# Capstone Review Worksheet


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  claim["Course claim"] --> code["Capstone package or file"]
  code --> tests["Tests or tour artifact"]
  tests --> worksheet["Review worksheet"]
  worksheet --> decision["Accept or challenge the boundary"]
```

```mermaid
flowchart TD
  purity["What is still pure?"] --> effect["Where does effect begin?"]
  effect --> failure["How is failure represented?"]
  failure --> stream["Where does the code materialize or buffer?"]
  stream --> proof["What test or tour artifact proves the claim?"]
```
<!-- page-maps:end -->

Use this worksheet after a module or before changing the capstone. The goal is not only
to agree with the architecture. The goal is to inspect whether the evidence justifies it.

## Purity

- Which package or function is still pure here?
- Which value shapes keep local reasoning cheap?
- Which helper would become harder to trust if it pulled I/O inward?

## Effects

- Which shell, capability, or adapter is allowed to execute the effect?
- Is the effect boundary named clearly enough that another engineer would find it quickly?
- Does the functional core stay descriptive after the boundary is introduced?

## Failure and streaming

- Which failures are values, and which are still exceptions?
- Where does the pipeline materialize a sequence, and why there?
- Which retry, timeout, or backpressure choice is policy rather than accidental behavior?

## Proof

- Which test folder or tour artifact proves the current claim?
- Which command should you run before accepting the boundary?
- Which question from [Functional Review Checklist](reference/review-checklist.md) is most relevant to this review?
