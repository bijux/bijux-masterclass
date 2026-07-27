# Public versus Internal Modules

<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Object-Oriented Programming"]
  section["Resources Failures Safe Evolution"]
  page["Public versus Internal Modules"]
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

Read the first diagram as a placement map: this page is one concept inside its parent
module, not a detached essay, and the capstone is the pressure test for whether the
idea holds. Read the second diagram as the working rhythm for the page: name the
problem, study the example, identify the boundary, then carry one review question
forward.

## Why this lesson matters

Code becomes hard to evolve when every import path is treated as if it were a promise to
the outside world.

If students do not learn the difference between a public module and an internal one,
they end up with two bad habits:

- changing internal structure becomes scary because callers may depend on anything
- new features get attached to whatever module was convenient rather than to a governed surface

This lesson teaches that module boundaries are part of the design contract, not just a
filesystem shape.

## A public module is a promise

A public module is a surface you intend other code to depend on.

That means changes to it should be reviewed as contract changes, not just local edits.

Public modules usually carry:

- stable names
- clearer documentation
- higher backward-compatibility pressure
- more deliberate export choices

The question is not whether a module is "important." The question is whether other code
is supposed to rely on it durably.

## An internal module is allowed to move

Internal modules exist to help the implementation stay readable and maintainable.

They may still be well-designed, but they are not automatically promises.

That distinction matters because internal structure should be refactorable without
forcing every downstream caller to change at the same time.

If everything is public, nothing is safely movable.

## Accidental public APIs are common

Many accidental public APIs start like this:

- a caller imports directly from a convenient low-level module
- a helper object becomes widely reused without an explicit decision
- a package exports more than it intended because nobody curates the surface

After a while, internal structure hardens into external dependency through habit rather
than design.

That is why naming and import paths are governance questions as much as coding questions.

## What to make public

Make a module public when you want callers to rely on it as an entry surface.

Typical candidates include:

- facades
- stable protocols or contracts
- intentionally supported value types
- composition-root entrypoints

Make a module internal when it mainly exists to support implementation detail, such as:

- helpers behind a facade
- persistence mechanics
- local translation utilities
- wiring details that should not define the outward contract

## Exports should be deliberate

One sign of a strong boundary is that exports are chosen deliberately instead of
incidentally.

That can mean:

- a package `__init__` exposing only the intended surface
- clear documentation that points readers to the supported import path
- tests that import through the same surface your users should use

The point is not ceremony. The point is that callers should not have to guess which path
is stable and which one is only convenient today.

## Why this matters for refactoring

When you know which modules are public, you can refactor the internals much more
aggressively and safely.

You can:

- rename helpers
- split files
- move implementation detail
- replace persistence mechanisms

without pretending every import path in the repository has equal compatibility status.

This is exactly why module boundary teaching belongs before compatibility evolution and
feature-preserving refactors.

## Common mistakes

- exposing internal modules because writing a facade felt unnecessary
- importing around the intended surface "just this once"
- changing public paths casually because the code still passes locally
- documenting internal implementation modules as if they were stable entrypoints
- using tests that depend on internals in ways real callers should not

These mistakes quietly turn local structure into long-term obligation.

## Review checklist

| Question | Good sign |
| --- | --- |
| can you name which modules are intended as stable entry surfaces? | yes |
| are internal modules free to move without breaking supported callers? | yes |
| are exports deliberate rather than incidental? | yes |
| do tests and docs steer readers toward the intended surface? | yes |

## Capstone connection

Review the capstone package and ask:

- which import paths should a downstream caller actually use?
- which modules are only there to support implementation structure?
- if you had to move internal code tomorrow, which callers should remain untouched?

That review is a better measure of module design maturity than counting how many files
exist.

## Exit check

Leave this lesson only when you can do all of these:

- explain why a public module is a compatibility promise
- identify one accidental public API risk created by convenience imports
- point to one capstone surface that should stay public and one that should stay internal
