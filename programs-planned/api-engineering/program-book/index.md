# API Engineering — Program Book

## The learner transformation

API engineering is not a sequence of framework tutorials. It is the discipline of making an externally visible promise precise, implementing it with durable mechanisms, preserving it against hostile behavior and ordinary failure, sustaining it under pressure, and extending it across asynchronous boundaries without losing meaning.

This program uses one Analysis Runs Platform because changing the application every ten days would hide the most valuable lesson: later concerns do not replace earlier ones. A valid event cannot repair a broken HTTP contract. A cache cannot repair an unsafe authorization query. A dashboard cannot prove that a database transaction committed. A broker cannot grant exactly-once effects by declaration. Each course adds one responsibility while retaining every earlier obligation.

## The responsibility ladder

| Stage | Responsibility | New proof question |
|---:|---|---|
| 1 | Public contract | Is the legal request, response, error, security, compatibility, and workflow surface precise? |
| 2 | Durable service | Does the implementation preserve that surface under transactions, concurrency, restart, and compatible release? |
| 3 | Security | Does the same behavior remain protected when identity, input, destinations, and traffic are adversarial? |
| 4 | Reliability and observability | Can operators detect, diagnose, contain, reconcile, and recover when dependencies and processes fail? |
| 5 | Performance, capacity, and traffic | Does the promise survive realistic load, growth, queueing, fairness, and resource limits? |
| 6 | Event-driven APIs | Can independent consumers rely on durable facts despite delay, duplication, bounded reordering, and replay? |

## One platform, not six toy applications

The platform lets principals create projects, register datasets, submit analysis runs, observe progress, retrieve verified artifacts, and receive completion notifications. That apparently small workflow is rich enough to exercise the real engineering boundaries:

- project and dataset ownership;
- asynchronous acceptance and status resources;
- idempotent run submission;
- optimistic concurrency;
- stable pagination;
- durable worker leasing and recovery;
- bounded upload and download;
- content-addressed artifacts;
- outbound webhook delivery;
- identity and authorization;
- telemetry, SLOs, and incident repair;
- workload models, traffic control, and capacity;
- event publication, consumer effects, replay, and governance.

The capstone is intentionally a modular service before it becomes an event producer. The program does not teach architecture by accumulation. New infrastructure appears only when a concrete guarantee requires it.

## What counts as understanding

Reading a chapter is preparation, not completion. For every important mechanism, you should be able to:

1. state the user-visible or operator-visible guarantee;
2. identify the authoritative owner of the decision;
3. name the failure that threatens it;
4. predict the smallest observation that would reveal the failure;
5. implement or inspect the mechanism in one primary language track;
6. compare the same invariant in the other track without demanding identical source shape;
7. retain a regression or evidence artifact;
8. state what the proof did not establish.

This method is repeated because it is the skill the program is teaching. The prose, examples, exercises, labs, and checkpoints all serve that progression.

## Course books, capstones, and proofs

The **course book** explains the subject from first principles and is sufficient for self-study. The **capstone** gives the ideas one coherent system in which to become concrete. The **lab** deliberately creates a failure or pressure condition. The **checkpoint** requires evidence before progression. The **proof routes** automate bounded claims. No generated report replaces understanding, and no explanation is allowed to claim more than its evidence.

Continue with [Start here](start-here.md), then keep the [six-course journey](six-course-journey.md) and [version ledger](version-and-handoff-ledger.md) available throughout the program.
