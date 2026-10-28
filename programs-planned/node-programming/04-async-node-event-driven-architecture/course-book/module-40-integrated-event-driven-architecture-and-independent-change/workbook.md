# Module 40 Workbook — Integrated Event-Driven Architecture

## A. Build the authority map

For TaskHarbor, assign one authority to manifest shape, graph legality, readiness, task effects, time, cancellation, events, diagnostics, final rendering, and process exit. Identify any fact currently established by more than one component.

## B. Audit the graph scheduler

1. Prove duplicate IDs, unknown dependencies, self-dependency, and cycles fail before execution.
2. Prove no task starts before all dependencies succeed.
3. Prove each task has one terminal outcome.
4. Prove final output is manifest ordered under reverse completion.
5. Prove every active task is joined under continue, fail-fast, timeout, and external abort.

## C. Review error taxonomy

Separate usage error, malformed manifest, graph error, task failure, task timeout, run cancellation, observer failure, and process cleanup failure. Decide which produce CLI exit 0, 1, or 2. Preserve causes rather than reducing everything to text too early.

## D. Implement priority

Add `low | normal | high`, default normal. Priority applies only to the ready set. Sort by rank and then source index. Update validation, types, inspect output, scheduler tests, documentation, and compatibility fixtures. Old manifests remain valid.

## E. Independent laboratory

Complete [Event-Driven Job Engine](../../labs/module-40-event-driven-job-engine/README.md). Its domain differs from TaskHarbor enough that you must reconstruct graph and scheduler reasoning rather than copy filenames.

## F. Final independent construction

Build a bounded notification campaign runner with dependencies between preparation, delivery, and audit tasks. Recipient failures continue; campaign shutdown stops new campaign admission, cancels cooperative waits, joins accepted work, and emits a deterministic report. Do not use streams, workers, or a framework.

## G. Architecture defense

Prepare a ten-minute defense answering:

- where work can wait or accumulate;
- who owns every promise;
- what abort cannot undo;
- which events are synchronous;
- how context is isolated;
- what one grace deadline covers;
- which outputs are schedule independent;
- how a cross-layer change is mapped before code.

## I. Temporal-invariant test plan

For each temporal invariant listed in the chapter, choose the smallest evidence: unit test, controlled scheduler test, event trace, or spawned-process test. Explain why ordinary type checking cannot prove it.

## J. Retry impact matrix

Complete a table for `maxAttempts` across validator, task model, scheduler, executor, deadline, cancellation, event hub, async event stream, renderer, CLI, tests, and compatibility. Include at least three ways the feature could compile while being wrong.

## K. Course-boundary essay

Explain in 500 words why TaskHarbor should not introduce Node streams or worker threads “for completeness.” Connect each deferred mechanism to the prerequisite model Course 4 has now established.

## L. Cross-layer change matrix

Add a retry policy to TaskHarbor without implementing it. Complete an impact matrix for manifest grammar, validation, scheduler state, task attempt identity, cancellation, deadlines, events, context, reports, exit status, tests, and compatibility. Mark every row changed or unchanged by proof.

Then identify the exact point at which a task attempt becomes committed. Explain how a retry avoids duplicate terminal task outcomes while still preserving per-attempt diagnostics. State which problems require Course 8 network idempotency rather than this process-local design.

## M. Final oral examination

Without opening the source, explain TaskHarbor’s path from manifest bytes to terminal process status. Your explanation must name the validation boundary, graph authority, ready-set policy, capacity commitment, promise owner, cancellation tree, event publication points, context creation point, deterministic reconstruction, shutdown owner, and exit-code decision.

Then choose one feature from worker execution, persistent resumability, or network submission. Identify at least five new authorities or failure modes that Course 4 does not yet model. This answer should demonstrate a controlled course boundary rather than overclaiming completeness.

## N. Cross-course integration review

Select one invariant from each prior Node course that TaskHarbor still depends on: runtime/value semantics, object identity or lifecycle, and public TypeScript/package contracts. Show where Course 4 would fail if that earlier invariant were weakened. This prevents async architecture from becoming detached from the language model beneath it.

## H. Readiness for Course 5

Explain why async iterables are not yet Node streams, why EventEmitter is not backpressure, and why TaskHarbor does not solve filesystem or byte-pipeline concerns. These boundaries motivate Course 5 rather than leaving gaps in Course 4.
