# Module 37 Workbook — Async Context and Diagnostic Boundaries

## A. Predict propagation

1. A context is established with `run`, an async function awaits twice, and a timer created inside fires later. Which callbacks see the store?
2. A promise was created before entering the context but awaited inside it. Which creation boundary matters?
3. Two concurrent runs resume in reverse order. Why must their stores remain isolated?
4. What does the caller observe after `run` completes?

## B. Reject hidden authority

A repository reads tenant identity from AsyncLocalStorage to select a database partition.

5. Explain the security and testability risk.
6. Redesign the repository to accept explicit tenant capability while keeping correlation ambient.
7. State which context fields are safe to retain.

## C. Design diagnostics

Create a stable diagnostics channel for task start, end, and error.

8. Decide what happens when there are no subscribers.
9. Decide how subscriber throw is handled.
10. Explain why task IDs belong in the message rather than the channel name.
11. Keep domain state authoritative elsewhere.

## D. Construct a context manager

Implement `current`, `run`, and `child`. Freeze stores, restore parent context after nested work, preserve error identity, and publish optional diagnostics. Tests must interleave two contexts with controlled deferred promises.

## E. Independent laboratory

Complete [Correlation Context](../../labs/module-37-correlation-context/README.md). Add retention analysis for one leaked timer and verify that unsubscribing from diagnostics stops later observations.

## F. TaskHarbor transfer

Attach `runId`, `taskId`, and source index to executor context. Do not pass task domain state through AsyncLocalStorage. Diagnostic subscriber failure cannot change task outcome.

## G. Unseen transfer

Design correlation for a library used both inside and outside an HTTP server. The library may emit diagnostics but cannot install global subscribers or assume a request context exists. Specify fallback behavior.

## I. Mutable-store counterexample

Create a parent context object, run two child operations, and mutate `taskId` in place before each await. Predict the corruption. Repair with immutable derived stores and prove parent restoration.

## J. Broken-boundary investigation

A callback-based third-party API loses context. Design a focused reproduction and a wrapper boundary. State why installing broad raw `async_hooks` instrumentation is not the first repair.

## K. Signal design

Classify these fields as structured log field, trace attribute, metric label, or explicit domain parameter: run ID, task kind, tenant ID, user token, retry count, payload size. Defend cardinality and security choices.

## L. Context-boundary experiment

Run two concurrent logical operations that share one mutable context object. Interleave nested updates and predict the resulting diagnostic contamination. Repair the design with immutable run-scoped stores and prove isolation.

Define three diagnostic channels for TaskHarbor. For each, provide payload fields, publication point, cardinality limit, secret-handling rule, and behavior when no subscriber exists. Explain why none of the channels is an authorization mechanism.

## M. Context retention audit

A context store contains a request ID, user object, parsed document, and response builder. Estimate which values remain reachable while a timer and a pending promise created inside the context are alive. Redesign the store so it contains only bounded immutable diagnostic facts. State which values should be explicit arguments instead.

Write a boundary adapter for a callback API that loses context. The adapter may restore diagnostic context, but must not copy mutable authority into ambient state. Add a test that invokes the callback after the parent operation has otherwise completed and explain the intended retention policy.

## N. Context provenance review

For every proposed context field, record who created it, who validated it, whether descendants may replace it, and when it becomes invalid. Reject a field whose provenance cannot be explained. Then design a boundary that translates explicit request metadata into a small run-scoped diagnostic store without hiding the original request object.

## H. Defense

Explain resource-creation propagation, `run` versus `enterWith`, context lifetime, why correlation does not prove causality, and why ambient authorization is a design error.
