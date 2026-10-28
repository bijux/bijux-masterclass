# Ten-Day Study Plan

The course is designed for two calendar weeks: five dense instructional days, a repair Saturday, a rest Sunday, then five more instructional days. Plan for eight to ten focused hours per instructional day.

## Daily rhythm

| Time | Work |
|---|---|
| 08:30–09:00 | Reconstruct the previous module's model without notes |
| 09:00–10:30 | Read the first half of the authoritative chapter and trace examples on paper |
| 10:45–12:00 | Finish the chapter and complete the day's reasoning ledger |
| 13:00–14:00 | Predict all eight investigation cases before running tools |
| 14:00–15:00 | Run cases, identify decisive phase, and repair wrong predictions |
| 15:15–17:15 | Build the independent laboratory |
| 17:30–18:45 | Implement the ObjectAtlas increment |
| 19:30–20:15 | Add adversarial tests and compare with the written contract |
| 20:15–20:30 | Write five retrieval prompts and one unresolved question |

Do not use the solution page as a walkthrough. Compare only after an independent attempt exists.

## Day 1 — Properties, descriptors, and enumeration

**Morning:** Build a descriptor table for data and accessor properties. Trace assignment, definition, deletion, spread, `Object.keys`, `Reflect.ownKeys`, and JSON. Inspect an accessor without running it.

**Afternoon:** Complete Descriptor-Safe Settings. Prove hidden metadata remains hidden from ordinary enumeration while still visible to a deliberate reflection surface.

**ObjectAtlas:** establish the node shell, stable ID descriptor, hidden runtime metadata, and plain snapshot boundary.

**Exit evidence:** given an unfamiliar object, identify every own key, complete descriptor, observable enumeration surface, and effectful read.

## Day 2 — Prototypes, delegation, and lookup

**Morning:** Draw a prototype chain and trace reads, `in`, own-property checks, writes, inherited setters, and shadowing. Separate `Constructor.prototype` from `Object.getPrototypeOf(instance)`.

**Afternoon:** Complete Prototype-Based Policy Catalog. Test own override, inherited default, null-prototype dictionaries, and malicious `__proto__` input.

**ObjectAtlas:** add kind policies through explicit delegation without persisting runtime prototype objects.

**Exit evidence:** a complete lookup trace that preserves the original receiver.

## Day 3 — Functions, receivers, constructors, and `new`

**Morning:** Build a call-site matrix for methods, extracted functions, `call`, `apply`, bound functions, arrows, constructors, and non-constructible callables. Reconstruct `new` step by step.

**Afternoon:** Complete Receiver-Safe Command Adapter. Verify invocation count, receiver identity, bound-argument behavior, and constructor misuse.

**ObjectAtlas:** provide command handlers that retain application authority without binding the entire architecture indiscriminately.

**Exit evidence:** explain a receiver defect from the call site rather than from the function body.

## Day 4 — Classes, private state, and initialization

**Morning:** Translate class declarations into prototype methods, property descriptors, constructor calls, public field installation, and private-brand checks. Trace base and derived initialization.

**Afternoon:** Complete Private Counter Bank. Test private-brand enforcement and derived-constructor ordering.

**ObjectAtlas:** introduce `AtlasNode` with private mutable state, validated factories, and plain-record reconstruction.

**Exit evidence:** predict which state exists at each point in base and derived construction.

## Day 5 — Composition, capabilities, and mixins

**Morning:** Create an authority map for a multi-component product. Compare inheritance, forwarding, nested collaborators, closures, object copying, and constructor mixins.

**Afternoon:** Complete Capability-Composed Document. Replace a broad environment object with narrow capabilities and prove local replacement.

**ObjectAtlas:** separate graph authority, node invariants, codec, persistence, rendering, and CLI effects.

**Exit evidence:** defend who owns each mutable fact and each cleanup obligation.

## Repair Saturday

Rebuild Modules 11–15 from memory:

- descriptor matrix;
- prototype lookup trace;
- receiver matrix;
- class initialization timeline;
- capability authority map.

Repair every incomplete laboratory test. Reconstruct ObjectAtlas's current live-object graph and persisted-record graph separately. Do not add new features.

## Day 6 — Symbols and runtime protocols

**Morning:** Inventory local and well-known symbols. Trace primitive conversion hints, tags, iteration discovery, and Node custom inspection. Separate protocol opt-in from privacy.

**Afternoon:** Complete Protocol-Aware Value Object. Test default, string, and number conversion; tagging; inspection; and serialization separation.

**ObjectAtlas:** add stable user rendering, debug inspection, runtime tags, and symbol-keyed metadata without leaking persistence state.

**Exit evidence:** identify which operation requests each protocol and what fallback occurs when it is absent.

## Day 7 — Iterables, iterators, and generators

**Morning:** Draw iterator state transitions. Trace `next`, early `break`, `return`, generator `finally`, delegation with `yield*`, and one-shot versus repeatable iterable behavior.

**Afternoon:** Complete Hierarchy Walker in preorder, postorder, and breadth-first order. Add cycle policy, early close, and mutation tests.

**ObjectAtlas:** implement deterministic lazy traversal with structural-revision checks.

**Exit evidence:** explain ownership of traversal state and exactly when cleanup runs.

## Day 8 — Reflection, proxies, and invariants

**Morning:** Map property operations to `Reflect`. Test target invariants for non-configurable and non-extensible objects. Analyze private fields and proxy receivers.

**Afternoon:** Complete Transactional Draft Proxy. Limit interception to a plain attribute draft, expose explicit commit/rollback, and revoke after terminal transition.

**ObjectAtlas:** add transactional attribute edits without proxying branded nodes.

**Exit evidence:** state what the proxy may intercept, what it must report truthfully, and what authority the proxy grants.

## Day 9 — Graphs, cloning, reachability, and disposal

**Morning:** Compare shallow copy, descriptor copy, `structuredClone`, JSON, and domain reconstruction. Build an identity map for a graph with sharing and a cycle. Distinguish reachability from deterministic lifecycle.

**Afternoon:** Complete Graph Snapshot and Lease. Preserve sharing, remap domain IDs, and close a lease explicitly.

**ObjectAtlas:** implement subtree cloning, immutable snapshots, edit-session disposal, and bounded runtime-only metadata.

**Exit evidence:** identify every identity preserved, duplicated, remapped, or discarded by a copy operation.

## Day 10 — Integrated architecture and independent change

**Morning:** Produce a full ObjectAtlas runtime-object map, invariant register, representation table, protocol table, and lifecycle table. Run the architecture clinics in the final review.

**Afternoon:** Complete Object-Model Audit. Then implement the independent alias extension without reading a prepared implementation.

**ObjectAtlas:** finish process tests, storage tests, compatibility tests, and documentation. Run the strongest available proof route.

**Exit evidence:** defend the alias change across property representation, lookup, traversal, cloning, persistence, inspection, and compatibility.
