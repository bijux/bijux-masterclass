# Review Checklist

<!-- page-maps:start -->
## Reference Position

```mermaid
flowchart TD
  family["Python Programming"] --> program["Python Metaprogramming"]
  program --> reference["Review Checklist"]
  reference --> review["Design or review decision"]
  review --> capstone["Capstone proof surface"]
```

```mermaid
flowchart TD
  trigger["Hit a naming, boundary, or trade-off question"] --> lookup["Use this page as a glossary, map, rubric, or atlas"]
  lookup --> compare["Compare the current code or workflow against the boundary"]
  compare --> decision["Turn the comparison into a keep, change, or reject call"]
```
<!-- page-maps:end -->

Read the first diagram as a lookup map: this page is part of the review shelf, not a first-read narrative. Read the second diagram as the reference rhythm: arrive with a concrete ambiguity, compare the current work against the boundary on the page, then turn that comparison into a decision.

Use this checklist when reviewing decorators, descriptors, metaclasses, dynamic execution,
or plugin registration code. The goal is not to punish dynamic design. The goal is to
force it to justify itself.

## Mechanism choice

- What lower-power tool was considered first?
- Which invariant actually requires this mechanism?
- Is the behavior local enough to explain without a live walkthrough?

## Escalation rule

- Could plain code, inspection, or an explicit class solve this before decorators or descriptors?
- If a descriptor or metaclass is involved, what exact invariant could not be owned at a lower rung?
- Is the stronger tool more invasive than the value it adds?

## Observability

- Does signature, docstring, name, and traceback visibility survive wrapping?
- Can a reviewer inspect the runtime shape without executing business actions?
- Are import-time side effects explicit and deterministic?

## Testability

- Is the registry, cache, or global hook resettable in tests?
- Are failure cases tested, not only happy paths?
- Can the proof route demonstrate the claim from the public surface?

## Security and governance

- Is dynamic execution excluded from untrusted input paths?
- Are plugin names, field contracts, and public hooks stable and documented?
- Is there a kill switch or rollback path if the mechanism causes trouble in production?

## Rejection signals

Reject or rewrite if:

- the mechanism is chosen because it feels advanced
- the design hides work at import time without explicit contracts
- the code becomes harder to debug than an ordinary explicit alternative
