# Pressure Routes


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Object-Oriented Programming"]
  section["Guides"]
  page["Pressure Routes"]
  capstone["Capstone evidence"]

  family --> program --> section --> page
  page -.applies in.-> capstone
```

```mermaid
flowchart LR
  problem["Name the current design problem"] --> module["Choose the smallest module entry"]
  module --> support["Keep one support page nearby"]
  support --> capstone["Cross-check one capstone surface"]
  capstone --> proof["Use one proof step only if needed"]
```
<!-- page-maps:end -->

Use this page when the module titles are slower than the real problem in front of you.
It routes from design pressure to the smallest honest starting point.

## Route by problem

| If the real problem is... | Start with | Keep nearby | Capstone cross-check |
| --- | --- | --- | --- |
| I cannot explain what kind of object this is | Modules 01-03 | [Module Promise Map](module-promise-map.md) | `model.py` and lifecycle tests |
| I do not know where behavior belongs | Module 02 | [Module Checkpoints](module-checkpoints.md) | `application.py`, `model.py`, and policies |
| illegal states keep leaking through | Module 03 | [Module Checkpoints](module-checkpoints.md) | lifecycle tests and inspection bundle outputs |
| one invariant is scattered across several objects | Module 04 | [Proof Matrix](proof-matrix.md) | aggregate, projections, and architecture surfaces |
| retries, cleanup, or error handling feel accidental | Module 05 | [Proof Matrix](proof-matrix.md) | `runtime.py`, `repository.py`, and unit-of-work tests |
| persistence is flattening the domain | Module 06 | [Proof Ladder](proof-ladder.md) | repository boundaries and verification bundle artifacts |
| clocks, queues, threads, or async work are stealing ownership | Module 07 | [Proof Ladder](proof-ladder.md) | runtime tests and walkthrough artifacts |
| tests exist, but I do not trust what they prove | Module 08 | [Proof Matrix](proof-matrix.md) | test suite and verification bundle |
| I need a stable public route or extension seam | Module 09 | [Proof Ladder](proof-ladder.md) | application surface and extension guide |
| I need to review whether the design survives production pressure | Module 10 | [Proof Matrix](proof-matrix.md) | full proof route and review worksheet |

## Route by learner situation

| Situation | Start here | Why |
| --- | --- | --- |
| you missed class and only know the symptom | the table above | it lets you enter by pressure instead of by chapter order |
| you already know the module but the examples still feel vague | the named capstone cross-check | it forces one concrete executable surface |
| you keep jumping to late modules | [Module Promise Map](module-promise-map.md) | it reminds you what earlier modules were supposed to settle first |
| you keep over-proving everything | [Proof Ladder](proof-ladder.md) | it sizes the evidence to the question |

## Fast paths that are usually safe

- object meaning is weak: go to Modules 01, 02, then 03
- collaboration authority is weak: go to Modules 04, then 05
- persistence or runtime pressure is weak: go to Modules 06, then 07
- trust and governance are weak: go to Modules 08, then 09, then 10

## Bad route choices to reject

- starting at Module 09 when object roles are still unclear
- starting at Module 10 when authoritative ownership is still unsettled
- reading concurrency material when shared-state discipline is already broken
- using the capstone proof routes as a substitute for learning the earlier ownership lessons

## One-hour rescue route

1. Read [Course Guide](course-guide.md).
2. Pick one pressure from this page.
3. Read the matching module overview only.
4. Inspect the named capstone surface.
5. Stop after one design question becomes clearer.

## Exit check

Leave this page only when you can say:

> My real pressure is `____`, so I should start with `____`, keep `____` nearby, and
> cross-check it in `____`.
