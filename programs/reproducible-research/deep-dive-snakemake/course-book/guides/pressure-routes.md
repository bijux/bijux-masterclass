# Pressure Routes

Use this page when you cannot study the whole course in order because urgency is shaping
what you can realistically read. The goal is not to excuse shallow understanding. The
goal is to keep the route honest under pressure.

Pressure usually makes learners widen the surface too early. This page exists to stop
that.

## The rule under pressure

Under pressure, do four things in order:

1. name the pressure in plain language
2. choose one bounded route
3. use one matching proof surface
4. stop as soon as the owning workflow boundary becomes visible

If you keep widening the reading surface because the situation feels stressful, pressure
usually gets worse rather than better.

## Start by naming the pressure without drama

Pressure routes work badly when the problem is framed theatrically:

- everything is broken
- the repository is a mess
- I need the strongest route immediately

A better opening sounds like:

- I missed class and need an honest first entry tonight
- CI and local behavior differ and I need the owning boundary first
- I need to explain publish trust without rereading the whole course
- I need to tell whether this is workflow semantics or policy drift

Once the pressure is named that precisely, the first route becomes much easier to choose.

## How to use this page

Work in this order:

1. write the pressure in one sentence
2. choose one route from the table
3. use only the first proof surface that matches that route
4. stop as soon as you can name the owning workflow boundary

If you keep widening the route because the situation feels urgent, this page is being
used against its own purpose.

## Choose the route that matches the pressure

| Pressure | First page | First module or reference | First proof surface | Stop when you can name... |
| --- | --- | --- | --- | --- |
| first contact | [Start Here](start-here.md) | [Module 00](../module-00-orientation/index.md), [Module 01](../module-01-file-contracts-workflow-graph-truth/index.md) | [Capstone Walkthrough](../capstone/capstone-walkthrough.md) | one truthful file contract and one reason the capstone is not first contact |
| inherited workflow repair | [Anti-Pattern Atlas](../reference/anti-pattern-atlas.md) | [Module 03](../module-03-production-operations-policy-boundaries/index.md), [Module 04](../module-04-scaling-workflows-interface-boundaries/index.md) | [Command Guide](../capstone/command-guide.md) |
 whether the failure is workflow semantics, policy drift, interface sprawl, or execution context |
| publish and stewardship review | [Course Guide](course-guide.md) | [Module 06](../module-06-publishing-downstream-contracts/index.md), [Module 07](../module-07-workflow-architecture-file-apis/index.md), [Module 10](../module-10-governance-migration-tool-boundaries/index.md) | [Capstone Proof Guide](../capstone/capstone-proof-guide.md) | what downstream trust depends on and which route is strong enough to defend it |
| incident pressure | [Capstone Review Worksheet](../capstone/capstone-review-worksheet.md) | [Module 09](../module-09-performance-observability-incident-response/index.md), [Topic Boundaries](../reference/topic-boundaries.md) | [Capstone Proof Guide](../capstone/capstone-proof-guide.md) | the symptom, the owning boundary, and the next smallest confirming command |

## Read the table correctly

The table is not asking you to master a whole module sequence in one sitting. It is
giving you a first stable foothold.

- The first page should help you frame the problem.
- The first module or reference should teach the boundary that owns the problem.
- The first proof surface should give you evidence without overcommitting to a heavier
  run.
- The stopping point matters because pressure work expands fast when there is no explicit
  exit.

## Quick examples

| Situation | Good first move | Bad first move |
| --- | --- | --- |
| You inherited a workflow that runs locally but behaves strangely in CI. | Start with [Module 03](../module-03-production-operations-policy-boundaries/index.md) and route into `capstone-profile-audit`. | Jump to governance language before you can explain the policy drift. |
| You need to explain what the capstone publishes to another maintainer. | Start with [Module 06](../module-06-publishing-downstream-contracts/index.md) and the [Capstone Proof Guide](../capstone/capstone-proof-guide.md). | Treat the entire `results/` tree as the downstream contract. |
| You missed class and need a truthful entry point tonight. | Start with [Start Here](start-here.md), then [Module 00](../module-00-orientation/index.md). | Open the whole repository and hope the structure teaches itself. |

## What not to do under pressure

- do not start with the whole capstone repository
- do not escalate to the strongest proof route because the situation feels urgent
- do not read governance pages before the current workflow boundary is named
- do not open every support page when one route already matches the pressure

## The beginner mistake to catch early

The most common beginner mistake under pressure is assuming urgency justifies a broader
surface.

Most of the time urgency demands the opposite:

- fewer pages
- one bounded module route
- one proof surface
- one explicit stopping point

## Companion pages

- [Module Promise Map](module-promise-map.md) when the route needs a sharper module contract
- [Proof Ladder](proof-ladder.md) when the current command still feels too heavy
- [Capstone Map](../capstone/capstone-map.md) when you know the module but not the repository surface
- [Topic Boundaries](../reference/topic-boundaries.md) when the pressure is really outside the course boundary

## Good stopping point

Stop when you know:

- which workflow boundary owns the current problem
- which next page or command would test that claim directly
- why a broader route would be unnecessary right now

If you still cannot name the boundary, return to the table above instead of widening the
reading surface.
