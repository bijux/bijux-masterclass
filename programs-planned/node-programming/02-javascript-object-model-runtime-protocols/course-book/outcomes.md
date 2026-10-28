# Outcomes and Mastery Evidence

The course defines fifty durable outcomes. They are phrased as observable abilities rather than topics encountered.

## Module 11 — Properties and descriptors

You can:

1. distinguish property keys, own properties, and inherited properties;
2. reconstruct a full data or accessor descriptor;
3. predict writable, enumerable, and configurable transitions;
4. choose an enumeration surface that matches a product claim;
5. inspect and copy object state without invoking accessors unintentionally.

**Evidence:** Descriptor-Safe Settings, descriptor matrices, getter-safe inspection tests, and ObjectAtlas node-property contracts.

## Module 12 — Prototypes and lookup

You can:

6. trace `[[Get]]`, `[[Set]]`, and `[[HasProperty]]` through a prototype chain;
7. distinguish a constructor's `.prototype` property from an object's internal prototype;
8. explain shadowing, inherited setters, and receiver-preserving lookup;
9. defend own-property validation for untrusted dictionaries;
10. identify prototype mutation and pollution risks.

**Evidence:** Prototype-Based Policy Catalog, lookup traces, null-prototype input policy, and ObjectAtlas kind-policy tests.

## Module 13 — Calls and construction

You can:

11. distinguish callability from constructibility;
12. derive `this` from invocation form;
13. predict arrow, bound, method, extracted, and explicit-receiver behavior;
14. reconstruct the steps performed by `new`;
15. design callbacks and command adapters whose receiver contract cannot be lost accidentally.

**Evidence:** Receiver-Safe Command Adapter, call-site tables, constructor-return tests, and ObjectAtlas command binding.

## Module 14 — Classes and private state

You can:

16. translate class syntax into prototype and construction behavior;
17. explain field initialization order across base and derived classes;
18. distinguish TypeScript `private` from JavaScript `#private` state;
19. preserve private brands and initialization invariants;
20. avoid fragile constructor override and partially initialized `this` designs.

**Evidence:** Private Counter Bank, initialization traces, forged-instance rejection, and branded ObjectAtlas nodes.

## Module 15 — Composition and capabilities

You can:

21. distinguish delegation, forwarding, method copying, inheritance, closures, and constructor-transforming mixins;
22. map each collaborator to the state and authority it owns;
23. design least-authority capability interfaces;
24. make conflict, construction, and lifecycle policy explicit in composed objects;
25. choose inheritance only where behavioral substitutability exists.

**Evidence:** Capability-Composed Document, authority maps, replacement tests, and ObjectAtlas layer boundaries.

## Module 16 — Symbols and protocols

You can:

26. choose symbols for collision-resistant protocol keys rather than privacy;
27. implement `Symbol.toPrimitive`, `Symbol.toStringTag`, `Symbol.iterator`, and Node custom inspection deliberately;
28. explain precedence and accepted hints in primitive conversion;
29. separate debug representation, user rendering, persistence, and coercion;
30. discover protocol capabilities without relying on fragile string names.

**Evidence:** Protocol-Aware Value Object, coercion matrices, custom-inspection tests, and ObjectAtlas protocol surfaces.

## Module 17 — Iteration and generators

You can:

31. distinguish iterable, iterator, and iterator-result objects;
32. implement lawful `next`, `return`, and single-pass state;
33. trace generator suspension and cleanup through `try...finally`;
34. design traversal order, mutation policy, and failure behavior explicitly;
35. prevent hidden eager materialization in lazy APIs.

**Evidence:** Hierarchy Walker, iterator traces, early-close tests, and three ObjectAtlas traversal orders.

## Module 18 — Reflection and proxies

You can:

36. use `Reflect` as a receiver-preserving operation surface;
37. state the target invariants that constrain proxy traps;
38. distinguish a proxy's identity and authority from its target;
39. avoid proxying private-field receivers as if they were transparent;
40. design a revocable proxy for one narrow transactional purpose.

**Evidence:** Transactional Draft Proxy, invariant-failure investigations, revocation tests, and ObjectAtlas attribute drafts.

## Module 19 — Graphs, cloning, and lifecycle

You can:

41. distinguish shallow copy, descriptor copy, structured clone, serialization, and domain reconstruction;
42. preserve or deliberately remap graph sharing, cycles, and domain identity;
43. explain reachability without treating garbage collection timing as a contract;
44. use weak references and finalization only for optional behavior;
45. design deterministic release around explicit ownership and disposal.

**Evidence:** Graph Snapshot and Lease, clone maps, lifecycle tests, and ObjectAtlas subtree-copy/session contracts.

## Module 20 — Integration and change

You can:

46. produce a runtime-object and invariant map for a package;
47. select evidence for descriptors, prototypes, brands, protocols, iteration, proxies, persistence, and lifecycle;
48. keep live instances, plain records, debug views, and persisted formats separate;
49. evaluate compatibility effects of changing object surfaces;
50. implement and defend an unseen cross-layer feature without bypassing invariants.

**Evidence:** Object-Model Audit, complete ObjectAtlas, final review, and the independent alias extension.
