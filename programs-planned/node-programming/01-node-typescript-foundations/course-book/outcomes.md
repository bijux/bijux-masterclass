# Outcomes and Mastery Evidence

The course has fifty durable outcomes. They are grouped by module and tied to observable evidence. Completing a page is not evidence; predicting, building, testing, and explaining are.

## Module 1 — Runtime and toolchain

You can:

1. distinguish TypeScript source, static program, emitted JavaScript, and running process;
2. explain the respective roles of ECMAScript, Node.js, TypeScript, npm, ESM, and the operating system;
3. configure a strict NodeNext ESM package with explicit `.js` runtime specifiers;
4. use project-local tools and identify version/configuration drift;
5. select type-check, build, runtime, and process evidence for different claims.

**Evidence:** Runtime Report, eight investigations, one source-to-process diagram, and a process test for help/version.

## Module 2 — Values and control

You can:

6. predict primitive values, coercion, truthiness, equality, and logical-operator results;
7. separate textual acceptance, numeric conversion, and domain validation;
8. enforce finite, integer, safe-integer, sign, and range policies deliberately;
9. state the code-unit/code-point/byte distinction for strings;
10. use guard clauses and exhaustive branches to establish invariants.

**Evidence:** Usage Quote Policy, an exact StudyLedger numeric parser, and table-driven boundary tests.

## Module 3 — Functions and callbacks

You can:

11. describe parameter, result, receiver, timing, count, retention, and failure contracts;
12. distinguish closure binding capture from value snapshot;
13. predict method, extracted-function, bound-function, and arrow-function receiver behavior;
14. choose sequential or aggregate ownership for promise-returning callbacks;
15. inject meaningful effects through small callable boundaries.

**Evidence:** Callback Budget, explicit clock injection, and call-order/call-count tests.

## Module 4 — Identity and mutation

You can:

16. draw variables, references, arrays, objects, and nested aliases as a heap graph;
17. distinguish rebinding from mutation and shallow copy from deep isolation;
18. use readonly as a static capability without claiming runtime freezing;
19. implement path-local immutable updates with structural sharing;
20. build and publish candidate state without mutating prior values on failure.

**Evidence:** Inventory Transform identity assertions and immutable StudyLedger transitions.

## Module 5 — TypeScript domain modeling

You can:

21. reason about unions and intersections as sets of possible runtime values;
22. model state-specific fields through discriminated unions;
23. narrow `unknown` through runtime evidence rather than assertions;
24. audit user-defined predicates and assertion functions as proof-producing code;
25. use `never` to expose missing typed policy while retaining runtime defense.

**Evidence:** Review Workflow, exhaustive StudyLedger state handling, and hostile validator tests.

## Module 6 — Collections and generics

You can:

26. choose Array, Map, Set, or object from dominant operations and order policy;
27. trace item type, cardinality, identity, order, and allocation through iteration;
28. define duplicate-key behavior instead of inheriting silent overwrite;
29. write generics that preserve real relationships among inputs and outputs;
30. state and test the prefix invariant of a reduction.

**Evidence:** Record Query, deterministic StudyLedger queries, and summary tests.

## Module 7 — Modules and packages

You can:

31. trace static ESM linking, evaluation, and live bindings;
32. diagnose relative import, type-only import, default/named export, and cycle problems;
33. distinguish file reachability from supported package API;
34. control top-level side effects and initialization ownership;
35. add product context when errors cross a module authority boundary.

**Evidence:** Package Boundary, curated StudyLedger entry exports, and source graph review.

## Module 8 — Errors and persistence

You can:

36. handle thrown values as unknown and preserve causes when translating errors;
37. separate JSON syntax, structural validation, domain validation, and storage I/O;
38. collect path-aware independent issues without manufacturing partial trusted values;
39. version a storage format and state compatibility policy;
40. describe exactly what candidate loading and temporary-file replacement protect.

**Evidence:** Validated Configuration and adversarial StudyLedger codec/storage tests.

## Module 9 — Async effects and CLI

You can:

41. predict basic stack, microtask, timer, and I/O ownership without overclaiming order;
42. identify the owner of every promise and rejection;
43. choose sequential, concurrent-start, or later bounded execution intentionally;
44. model cancellation as a cooperative request rather than rollback;
45. bind typed application behavior to argument tokens, files, streams, and exit status.

**Evidence:** Async File Index and a complete StudyLedger process lifecycle test.

## Module 10 — Integration and change

You can:

46. map claims to unit, integration, fixture, filesystem, type-check, and process evidence;
47. isolate clocks, paths, environment, and mutable fixtures in tests;
48. review architecture as dependency direction and authority rather than folder names;
49. trace an independent feature through every affected layer and compatibility promise;
50. state the course product’s validated claims and remaining non-contracts honestly.

**Evidence:** Reading Ledger, final review, StudyLedger extension, and oral defense.

## Progress decision

A module is ready to mark complete when all five questions receive a yes:

1. Can I reconstruct the mental model without the chapter?
2. Can I predict at least seven of eight investigation cases and explain corrections?
3. Does my lab satisfy its failure and identity/time/order contract?
4. Did I apply the mechanism to StudyLedger without copying a prepared patch?
5. Can I explain which evidence would falsify my claim?

A weak answer should trigger repair before the next dependency-heavy module.

## How the outcomes depend on one another

The outcomes are not fifty interchangeable checklist items. Several are load-bearing.

The first dependency chain is **runtime truth**. You must distinguish source, static analysis, emitted JavaScript, and execution before a type error, module-resolution error, or runtime failure can be diagnosed correctly. Modules 2 through 5 then use that distinction to separate a JavaScript value from what TypeScript currently knows about it. If this chain is weak, assertions begin to replace validation and static confidence begins to hide malformed runtime values.

The second chain is **identity and authority**. Closure state, object aliases, collection membership, module exports, persistence, and asynchronous work all need an owner. Modules 3 and 4 make ownership informal but explicit: which binding can change, which aliases observe the same object, and which function owns a side effect? Modules 6 through 9 lift the same question to collection order, package surfaces, storage files, and promises.

The third chain is **boundary construction**. A complete Node program repeatedly converts one kind of evidence into another:

```text
argument token -> parsed command -> validated domain input
JSON text -> unknown JavaScript value -> trusted domain value
promise -> observed terminal result -> process status
internal module -> curated export -> supported public API
```

A later step may depend on an earlier step, but it must not pretend that the earlier evidence proves more than it does. Valid JSON syntax does not prove a valid ledger. A successful domain transition does not prove that saving succeeded. A successful type check does not prove that Node can resolve every emitted import.

The fourth chain is **independent change**. The final five outcomes depend on all preceding layers. A feature is not complete because one function exists. It is complete only when its command grammar, static model, runtime validation, persistence compatibility, output, asynchronous ordering, and tests agree. The impact map in Module 10 is therefore a compressed test of the whole course.

## Repair routes

Use the symptom to choose the repair route rather than rereading the entire course.

| Symptom | Return to | Repair evidence |
|---|---|---|
| You call a runtime failure a TypeScript failure | Module 1 | classify ten failures by phase and inspect emitted JavaScript |
| Numeric parsers accept surprising text | Module 2 | write the exact accepted grammar before conversion |
| A callback runs with the wrong state or receiver | Module 3 | fill the callable contract ledger and test call order/count |
| A “copy” changes the original structure | Module 4 | draw the identity graph and assert both value and identity |
| JSON is cast directly to an interface | Modules 5 and 8 | decode from `unknown` and construct a fresh trusted value |
| Output order changes across runs | Module 6 | state source order, sort key, duplicate policy, and tie-breaker |
| Imports work only in an editor or test tool | Modules 1 and 7 | inspect package metadata, source specifier, emitted specifier, and Node resolution |
| A CLI reports success before data is durable enough for its stated contract | Modules 8 and 9 | trace promise ownership and place success after the awaited effect |
| Tests pass but a cross-layer feature is incomplete | Module 10 | rebuild the claim-to-evidence and feature-impact maps |

Do not advance merely because a repair compiles. Repeat the relevant prediction cases, rerun the independent lab without the reference open, and explain the corrected rule in one paragraph. That sequence distinguishes repaired understanding from a remembered patch.
