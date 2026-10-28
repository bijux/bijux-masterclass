# Module 15 Workbook

For each design, write an authority map before writing code. If a dependency can mutate state, register listeners, retain callbacks, or require cleanup, include that authority explicitly.

## A. False inheritance repair

A `ReportService` currently extends `FileStore` only to reuse `load` and `save`. Refactor it into composition. Decide:

- which storage operations become public through the report service;
- where storage errors are translated;
- whether callers may access the store directly;
- who owns store cleanup;
- how a test supplies an in-memory fake.

## B. Four composition mechanisms

Implement a counter using:

1. class with private field;
2. closure factory;
3. prototype delegation with per-instance own state;
4. copied method object.

Compare method identity, state privacy, reflection, `instanceof`, memory shape, replacement, and suitability for thousands of instances.

## C. Mixin conflict

Create `WithLabel` and `WithAudit`, both of which define `describe()`. Apply them in both orders. Then design a principled contract using either:

- distinct method names;
- explicit `super` composition;
- a composition object instead of mixins.

Explain why silent last-wins copying is a weak public policy.

## D. Least-authority renderer

A renderer currently receives the full mutable node. Design a `NodeReadView` capability containing only the operations required for rendering. Prove in TypeScript that ordinary caller code cannot mutate through that view. Then explain the runtime limitations of readonly structural views and when a wrapper is warranted.

## E. Cross-capability failure

Design an operation that updates an object graph and persists it. Compare:

- mutate then save;
- save then mutate;
- construct candidate, save candidate, publish candidate;
- transaction object with commit and rollback.

State the exact visible state after every failure point.

## F. Object assignment audit

Given an `Object.assign`-based mixin helper, identify what happens to:

- accessors;
- non-enumerable methods;
- symbols;
- descriptor flags;
- private-field methods;
- collisions.

Repair it only if copying methods is genuinely the chosen architecture. Otherwise replace it with explicit composition.

## G. Independent laboratory

Complete [Capability-Composed Document](../../labs/module-15-capability-composed-document/README.md). It combines search, tags, and version history without inheritance and requires a narrow read-only rendering capability.

## H. ObjectAtlas transfer

Separate node invariants, graph invariants, persistence, rendering, and node-kind policy. Tests must prove independent atlas instances, least-authority rendering, replaceable formatters, and failure-atomic application orchestration.

## I. Reconstruction and defense

Without notes, distinguish:

- delegation;
- forwarding;
- copying;
- closure composition;
- inheritance;
- constructor mixins;
- capability objects.

Then defend ObjectAtlas’s use of a class for nodes and composition for graph services.
