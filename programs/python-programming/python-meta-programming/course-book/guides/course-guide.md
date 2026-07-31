# Course Guide

<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Meta-Programming"]
  section["Guides"]
  page["Course Guide"]
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

This guide explains what the course is trying to build inside the learner.

The point is not to collect advanced Python mechanisms. The point is to become the kind
of engineer who can inspect dynamic behavior calmly, choose the lowest-power tool that
owns a problem honestly, and reject "clever" designs that become harder to debug than to
justify.

If you keep that goal in view, the reading order makes sense. If you lose it, the course
can easily collapse into a pile of tricks.

## The course builds four abilities

The course moves through four linked abilities:

1. observe runtime behavior without guessing
2. transform behavior without hiding what changed
3. place ownership at the right boundary
4. govern dynamic power with explicit review standards

Those abilities matter more than the names of the mechanisms themselves.

## The ten-module progression

| Module range | What you are learning to do | Why it comes here |
| --- | --- | --- |
| Module 00 | understand the power ladder and the study stance | you need the course’s rules before the dense mechanisms arrive |
| Modules 01 to 03 | observe runtime objects, attributes, callables, and evidence safely | higher-power tools are dangerous if observation is weak |
| Modules 04 to 05 | wrap behavior while preserving signatures, provenance, and reviewability | wrappers are the first major temptation to hide behavior |
| Module 06 | try lower-power class customization before escalation | learners need a real stopping point before metaclasses |
| Modules 07 to 08 | reason about descriptors, lookup, validation, and reusable field systems | attribute ownership becomes explicit and mechanical here |
| Module 09 | justify class-creation control only when weaker options fail honestly | metaclasses should feel earned, not glamorous |
| Module 10 | turn mechanism knowledge into governance and review judgment | the course should end with restraint, not escalation |

## The three big arcs

### Observation arc

Modules 01 to 03 teach the floor that everything else stands on:

- what Python objects are at runtime
- how names, attributes, and signatures can be inspected safely
- how evidence becomes strong enough to support design or review claims

If this arc is weak, later modules feel magical rather than mechanical.

### Control arc

Modules 04 to 09 teach how behavior can be changed at different boundaries:

- wrappers at call boundaries
- class decorators and helper patterns before stronger hooks
- descriptors at attribute boundaries
- metaclasses at class-creation boundaries

This arc teaches placement and restraint, not just power.

### Governance arc

Module 10 teaches what many advanced courses skip:

- where syntax policy stops and process isolation begins
- why ABC, protocol, and subclass-hook claims have different strengths
- how rollback evidence differs from concurrency or crash safety
- when import hooks and AST transforms belong to tooling rather than applications
- how to publish approve, constrain, and reject decisions with executable proof

The Module 10 course lab is the first learning surface. It supplies five small,
deterministic experiments so each claim can be traced before the learner audits the
larger incident-plugin runtime.

## How the capstone fits the course

The lessons, runnable course labs, worked examples, exercises, and reasoned answers are
the primary product. The capstone is the integration and transfer surface that follows
them.

- Early modules explain how to inspect the capstone without accidental execution.
- Middle modules explain its wrappers, fields, and customization boundaries.
- Later modules explain why its metaclass and registry stay narrow.
- The final module first builds a governance packet in the course lab, then explains how
  to review or reject capstone decisions honestly through `capstone-governance`.

When you study a module, the capstone gives you one place where the module’s claim becomes
visible in code, commands, tests, and saved evidence.

## Which support page solves which study problem

| Study problem | Best page |
| --- | --- |
| I need the right entry route | [Start Here](start-here.md) |
| I need the course’s discipline made explicit | [Learning Contract](learning-contract.md) |
| I need to know what this module is supposed to settle | [Module Promise Map](module-promise-map.md) |
| I need to know whether I can move on | [Module Checkpoints](module-checkpoints.md) |
| I need a pressure-shaped reading path | [Pressure Routes](pressure-routes.md) |
| I need the smallest honest proof route | [Proof Ladder](proof-ladder.md) |
| I need a direct claim-to-evidence mapping | [Proof Matrix](proof-matrix.md) |
| I need to stabilize the environment before any proof work | [Platform Setup](platform-setup.md) |

## How to study the course well

### Before a module

- Read the module promise.
- Know what the module is supposed to settle.
- Know what it does not settle yet.

### During a module

- Keep one lower-power alternative in view.
- Ask what timing boundary the mechanism changes: import time, class-definition time, instance time, or call time.
- Refuse to treat jargon as understanding.

### After a module

- Use the checkpoints.
- Cross into the capstone only when the course question is explicit.
- Prove at least one claim in a real surface instead of trusting prose alone.

## Honest expectations

You should expect the course to feel slower than tutorial-style metaprogramming material.
That is intentional. Fast metaprogramming courses often teach mechanism recognition
without teaching boundary judgment.

By the end of this course, you should be able to answer:

- What changed at runtime?
- Where does that behavior belong?
- Which lower-power option was ruled out?
- What evidence proves the claim?
- What design would I reject as too magical?
