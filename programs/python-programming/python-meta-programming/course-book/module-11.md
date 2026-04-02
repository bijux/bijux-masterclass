# Module 11: Mastery Review


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Meta-Programming"]
  section["Module 11"]
  page["Module 11: Mastery Review"]
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

You have now moved through the full runtime ladder: observation, wrapping, attribute
control, class creation, and governance. This final module exists to turn that material
into review judgment and explicit exit criteria.

## What you should now be able to explain

- what happens at import time, class-definition time, instance time, and call time
- which metadata or signatures must remain visible after wrapping
- why a descriptor or metaclass is justified in one design and unjustified in another
- which dynamic mechanisms are too dangerous for routine application code

## What you should now be able to review

- a decorator that claims to preserve callable identity
- a descriptor that claims to own validation semantics
- a metaclass that claims to enforce class-definition-time invariants
- a plugin or registry design that claims to stay deterministic and testable

## Capstone exit checks

- run the course proof route
- inspect the public manifest before invoking a plugin action
- explain which file owns registration, field validation, and runtime invocation
- identify one change you would reject as making the system more magical than necessary

## What mastery means here

Mastery in this course does not mean reaching for metaclasses faster. It means reaching
for metaprogramming less often, and using it more precisely when the design truly needs it.
