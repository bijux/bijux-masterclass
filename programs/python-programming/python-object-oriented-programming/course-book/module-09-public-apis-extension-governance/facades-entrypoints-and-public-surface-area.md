# Facades, Entrypoints, and Public Surface Area

<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Object-Oriented Programming"]
  section["Public Apis Extension Governance"]
  page["Facades, Entrypoints, and Public Surface Area"]
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

This lesson is about one governance promise:

- if another maintainer or consumer starts here, what exact surface are we prepared to
  support over time?

In Python, reachability is cheap. Support is expensive.

That is why a facade matters. It lets the package say:

- start here
- depend on this
- ignore the rest unless you are changing the internals

Without that sentence, a package teaches its directory layout instead of its supported
workflow.

## Keep one package and one task visible

Use the capstone package:

`service_monitoring`

Assume a newcomer wants to do one normal thing:

- run the supported monitoring workflow and inspect the stable result

The lesson question is not:

- what can be imported today?

It is:

- what is the narrowest surface that lets a learner do that job without learning runtime,
  repository, or adapter internals?

That is the real facade problem.

## Public surface is a support burden

A surface is public only if the maintainers are willing to:

- document it
- keep examples aligned with it
- review compatibility around it
- deprecate it honestly
- defend it with executable or reviewable proof

This is why a public API is not the same as an importable path.

An importable path may simply exist.
A public path creates an obligation.

When you think this way, a smaller surface stops looking restrictive and starts looking
responsible.

## A strong facade speaks in user tasks, not in file layout

A good facade is shaped by what users need to do.

For this capstone, that likely means:

- one package-level workflow entrypoint
- one stable outcome shape
- one documented extension seam type

It should not mean:

- exporting every useful-looking internal class
- making callers understand internal layering before they can start
- turning the current folder structure into the API design

The consumer story should remain coherent even if the internals are reorganized.

## The first copied import path is the real teaching surface

The highest-value beginner example matters disproportionately.

If the first example a learner copies imports:

- runtime workers
- repository wiring
- adapter helpers

then those internals have already become the accidental API.

That is why entrypoints are not only packaging decisions. They are teaching decisions.

The first public example should reinforce:

- where supported use begins
- what deeper layers can be ignored
- which path maintainers are prepared to defend later

## Facades protect refactor freedom

When consumers depend on one narrow facade:

- constructors can change internally
- helper modules can move
- policy composition can be reshaped
- orchestration details can disappear

without each internal change becoming visible breakage.

When consumers depend on deep imports, every one of those changes becomes risky.

This is the practical reason facades matter so much in long-lived Python packages:

- they preserve the right to improve internals without constantly renegotiating the
  public contract.

## Worked capstone surface

A strong public shape for this package might look like:

```python
from service_monitoring import run_monitoring, IncidentSink
```

What this teaches:

- `run_monitoring` is the supported consumer entrypoint
- `IncidentSink` is the narrow extension seam
- deeper layers are intentionally not part of the first public story

What it avoids teaching:

- repository implementations as public dependencies
- runtime coordinators as extension entrypoints
- internal layout as knowledge every caller must master

The exact names can vary. The public-shape discipline should not.

## Not every useful internal object deserves public status

Keep a surface private when it mainly exists for:

- internal composition
- translation between boundaries
- runtime orchestration
- helper logic
- replaceable implementation structure

If a real consumer use case still needs one of those objects, the usual answer is:

- add a better supported facade

not:

- bless the deep internal import because it is convenient today

This protects the package from publishing incidental structure as durable promise.

## Build a public-surface packet

For each package, keep a short packet with:

- supported user task
- supported import path
- stable result or command surface
- documented extension seam, if any
- important private zones that must stay outside the promise
- one example that teaches the supported start point

This packet gives another maintainer something concrete to defend during review. It also
reveals when the package is teaching more than it intends to support.

## Common failure modes

- treating every importable path as public because Python allows it
- exporting internal classes because they are convenient in the current version
- shaping the facade around the file tree instead of the user task
- widening the public surface before compatibility and documentation work exist
- calling a re-export list a facade without defining the supported use story

## Facade review card

Use this card when reviewing a public-surface change:

| Question | What a strong answer sounds like |
| --- | --- |
| what normal supported task does the facade serve? | "run monitoring and inspect stable outcomes" |
| can that task be completed without deep imports? | "yes, through one package-level entrypoint" |
| what stays private and movable? | "runtime orchestration, repository wiring, adapter helpers" |
| what example teaches the supported start point? | "the quickstart imports only `run_monitoring` and `IncidentSink`" |
| what refactor freedom does this preserve? | "internal layers can move without changing the public story" |

## Capstone connection

Use this page to answer all of these:

- which import path should become the only beginner-facing start point
- which deep path should remain private even if it is currently convenient
- what stable result or command surface would let consumers ignore internal layering
- which current example would accidentally publish the wrong layer

That is the first real governance decision in the module.

## Exit check

Leave this lesson only when you can do all of these:

- explain why import reachability is not the same as public support
- identify one capstone surface that should become the facade entrypoint
- identify one deep import that should stay private or be replaced by a supported path
