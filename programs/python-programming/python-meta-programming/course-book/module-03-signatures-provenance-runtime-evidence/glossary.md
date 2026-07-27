# Module Glossary

<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Meta-Programming"]
  section["Signatures Provenance Runtime Evidence"]
  page["Module Glossary"]
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

This glossary belongs to **Module 03: Signatures, Provenance, and Runtime Evidence** in
**Python Metaprogramming**. It keeps the language of this directory stable so the same
ideas keep the same names across lessons, practice, and capstone discussion.

## How to use this glossary

Use the glossary when a page or review discussion starts to blur together contract
evidence, provenance hints, structural inspection, and diagnostic stack data. Module 03
is meant to keep those evidence classes distinct.

If a discussion begins to sound vague, come back here and restate the claim with the
module's exact evidence language before you continue.

## Terms in this directory

| Term | Meaning in this directory |
| --- | --- |
| Attached-object truth | What is literally attached on the object or class before normal descriptor execution or dynamic lookup changes the result. |
| Argument binding | Using `Signature.bind()` or `bind_partial()` to simulate Python's call matching and produce explicit parameter/value relationships. |
| Best-effort provenance | Context recovered through helpers such as `getsource`, `getfile`, and `getmodule`, useful but not safe to treat as correctness-grade truth. |
| Bound arguments | The `BoundArguments` object produced by binding, mapping parameters to supplied values. |
| Bound method signature | The callable contract visible on an already-bound method, which omits the instance parameter because it is already attached. |
| Contract evidence | Structured runtime evidence about how a callable should be invoked, especially through `inspect.signature`. |
| Diagnostic-only evidence | Runtime evidence that belongs to debugging and tooling, such as frames and stack inspection, rather than ordinary application logic. |
| Dynamic member enumeration | Value-oriented inspection through `inspect.getmembers`, which can execute descriptors and other lookup behavior. |
| Evidence class | The category of proof being used for a runtime claim, such as contract evidence, best-effort provenance, static structure, or diagnostic-only evidence. |
| Frame retention hazard | The risk that retaining frame or traceback objects keeps locals and caller chains alive longer than intended. |
| Limitation statement | A sentence that names where a helper or recovery path can fail so the review does not overclaim certainty. |
| Parameter kind | The invocation category attached to a `Parameter`, such as positional-only or keyword-only. |
| Provenance helper | A helper such as `getsource`, `getfile`, or `getmodule` that tries to recover where an object came from. |
| Resolved-value truth | The value you get after normal attribute access, descriptor execution, or dynamic lookup logic has been allowed to run. |
| Review packet | The combined evidence table, examples, limitation notes, and boundary judgments another learner can inspect without guessing what was being proved. |
| Signature | An `inspect.Signature` object describing a callable's invocation contract. |
| Strong contract evidence | Evidence Python itself enforces at call time or exposes directly as part of the callable contract, such as signature shape and argument binding. |
| Static structure | The raw attached members or descriptors visible through static lookup rather than through normal dynamic resolution. |
| Static lookup | Inspection through `inspect.getattr_static`, which avoids normal attribute-protocol execution. |
| Convenience surface | A helpful but non-essential review aid that should not carry the main correctness claim when stronger evidence already exists. |
| `bind_partial()` | Partial argument binding that allows required parameters to remain unbound. |
| `getmembers()` | Dynamic enumeration that resolves values for discovered names. |
| `inspect.signature` | Structured callable introspection that exposes parameters, annotations, and binding helpers when available. |
| `inspect.stack()` | High-cost stack inspection that belongs to diagnostics, not routine application control flow. |
| `Parameter` | A single formal argument inside a `Signature`, carrying name, kind, default, and annotation data. |
| `POSITIONAL_ONLY` | A parameter kind that may be supplied only positionally. |
| `KEYWORD_ONLY` | A parameter kind that may be supplied only by keyword. |
| `__signature__` override | An explicit signature surface supplied by a callable or framework. |
| `__wrapped__` chain | Wrapper metadata used by tools such as `inspect.signature` to recover the underlying callable contract. |

## Quick repair prompts

Use these prompts when a review note in this module sounds technical but still weak:

| If your note says... | Repair it by asking... |
| --- | --- |
| "I inspected the callable." | Which evidence class did I actually use, and what runtime claim was I trying to support? |
| "The helper seems safe." | Did I prove call shape, inspect stored state, or just avoid seeing the side effect this time? |
| "The file path proves where it came from." | What limitation statement keeps that provenance claim honest in generated or interactive contexts? |
| "The stack shows the right answer." | What explicit parameter or owned state should carry this information outside diagnostics? |

## Boundary reminders

- Use signature and binding when the claim is about callable contract shape.
- Use provenance helpers when the claim is about review context, not correctness proof.
- Use static lookup when you need attached-object truth.
- Use dynamic lookup when you intentionally need resolved-value truth.
- Use frame inspection only when the evidence belongs in diagnostics and can be removed from production logic without changing correctness.

## Keep the module connected

- Return to [Module 03 Overview](index.md) for the full learning route.
- Use [Exercises](exercises.md) and [Exercise Answers](exercise-answers.md) to pressure-test the evidence language.
- Revisit the [Worked Example](worked-example-building-a-safe-signature-guided-repr.md) when a helper starts to blur strong evidence, best-effort provenance, and dynamic execution.
