# Course Guide
Use this page when you want the big picture without losing the learner-first route. Deep
Dive Make has several surfaces, but they do not have equal teaching value at every stage.
The central rule is simple:

> Learn the idea in a small setting first, then use the capstone to confirm it in a
> larger repository.

Deep Dive Make has four durable surfaces:

1. course home and orientation for entry and reading order
2. modules for the course arc itself
3. capstone pages for executable corroboration
4. reference pages for durable review and repair maps

## The recommended reading order

```mermaid
flowchart LR
  start["Start Here"] --> orient["Module 00"]
  orient --> early["Modules 01-03"]
  early --> middle["Modules 04-06"]
  middle --> late["Modules 07-10"]
  late --> capstone["Capstone and review surfaces"]
```

That order matters because later skills assume earlier honesty:

- release work is weak without graph truth
- performance tuning is risky without determinism
- governance language is empty without working evidence

## A full module day

Each teaching module is designed to support a complete day of self-study:

1. run the smallest demonstration before reading the advanced case
2. read the five core lessons and reproduce their commands
3. work through the realistic example without skipping the evidence loop
4. complete Exercises 1-5 to establish the module contract
5. complete Exercises 6-10 to apply, pressure-test, and integrate it
6. compare your reasoning with the answers only after recording your own
7. keep the resulting commands, observations, and explanation in your portfolio

Module 00 is orientation rather than one of the ten exercise-bearing modules. Modules
01-10 contribute ten exercises each, for 100 exercises across the course.

## What belongs in each surface

| Surface | Use it for | Do not expect it to do |
| --- | --- | --- |
| orientation | getting ready, building study rhythm, seeing the whole arc | teaching advanced Make features |
| modules | learning one day-sized concept deeply | proving everything about the capstone |
| capstone | seeing the idea survive a realistic repository | acting as first contact for a beginner |
| reference | reviewing, repairing, and checking boundaries | replacing the lesson sequence |

## Choose the right surface

| If you need... | Start here | Do not start with |
| --- | --- | --- |
| first entry into the course | [Start Here](start-here.md) | the capstone repository |
| the module sequence explained | [Module 00](../module-00-orientation/index.md) | incident or governance pages |
| one support page for urgency | [Pressure Routes](pressure-routes.md) | random browsing through `guides/` |
| proof sizing | [Proof Ladder](proof-ladder.md) | the strongest available command |
| module-to-repository routing | [Capstone Map](../capstone/capstone-map.md) | raw repository files |
| durable review maps | [Reference](../reference/index.md) | course-home prose |

## The Course Arc

| Arc | Modules | What becomes legible |
| --- | --- | --- |
| graph truth | Modules 01-03 | truthful edges, publication boundaries, parallel safety, and self-testing |
| pressure and hardening | Modules 04-06 | precedence, portability, modeled hidden inputs, and generator boundaries |
| reusable build surfaces | Modules 07-08 | layered `mk/` design, public targets, and release contracts |
| incident and stewardship judgment | Modules 09-10 | observability, migration boundaries, and long-lived governance |

## The support shelf by job

- Read [Module Promise Map](module-promise-map.md) when module titles feel too compressed.
- Read [Module Checkpoints](module-checkpoints.md) when you need a visible exit bar.
- Read [Pressure Routes](pressure-routes.md) when the reading order is shaped by urgency.
- Read [Proof Matrix](proof-matrix.md) when you already know the claim and need the evidence surface.
- Read [Command Guide](../capstone/command-guide.md) when you know the route but not the command layer.
- Read [Capstone Guide](../capstone/index.md) when you need the capstone contract before opening repository files.

## Best defaults

Use these as your stable defaults unless the current pressure gives you a stronger reason:

1. enter with [Start Here](start-here.md)
2. anchor in [Module 00](../module-00-orientation/index.md)
3. read modules in order
4. keep [Proof Ladder](proof-ladder.md) nearby
5. enter the capstone through [Capstone Map](../capstone/capstone-map.md)
6. use the [Completion Rubric](../reference/completion-rubric.md) to review your exercise evidence

## A warning about skipping ahead

The course is intentionally cumulative. If you jump to a later module because it sounds
more advanced, you often borrow vocabulary without the model underneath it. The common
result is recognizable phrasing and weak decisions.

If a later module feels compelling, ask which earlier skill it depends on:

- parallel safety depends on truthful edges
- generator design depends on honest output ownership
- release discipline depends on stable artifact meaning
- migration judgment depends on all of the above

That is why the course begins with tiny file targets rather than with a large Make-based
application.

## Good stopping point

Stop when you can answer two questions clearly:

- which surface should answer the next question
- why the heavier surfaces would be premature right now
