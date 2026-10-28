# Course 1 — Node.js and TypeScript Foundations

## JavaScript semantics, strict types, ESM, async effects, and complete programs

This course teaches modern Node.js from the inside out. JavaScript is the language that executes. TypeScript is a static reasoning layer whose annotations disappear before ordinary runtime behavior. Node.js is the host that supplies modules, processes, files, timers, tests, and operating-system boundaries. npm owns package installation and scripts. ESM defines how files become one executable graph.

The course keeps those mechanisms separate until you can explain how they cooperate.

> **Governing question:** How do JavaScript runtime behavior, TypeScript contracts, ESM packages, failures, asynchronous effects, and tests combine into a complete Node.js program that you can predict, build, diagnose, and extend?

## Who should begin here

You should already understand variables, branches, loops, functions, and basic collections in another language. You do not need prior JavaScript, TypeScript, browser, server-framework, npm, or Node experience.

This is not a general introduction to programming. The schedule is dense: one module per study day, eight to ten focused hours, and a cumulative product that grows throughout both weeks.

Before Day 1, you should be able to write a small program in another language that reads values, validates one condition, stores records in a collection, and contains a few tests. If those tasks are still difficult independently, repair that foundation first.

## What “TypeScript-first” means

All substantial construction uses strict TypeScript. Explanations still begin with JavaScript runtime behavior because types do not replace that behavior.

For every important line, keep two questions distinct:

1. **What JavaScript value and effect exist when Node executes this?**
2. **What relationship did TypeScript establish before execution?**

A type assertion can change the answer to the second question without changing the first. A JSON parser can produce malformed domain data even when the target variable has an interface annotation. A promise can be correctly typed and still have an unobserved rejection. The course returns to this boundary every day.

## The learning method

Reading is preparation, not completion. Each module follows this sequence:

```text
authoritative chapter
        ↓
closed-book prediction
        ↓
causal diagnosis and repair
        ↓
focused construction
        ↓
independent laboratory
        ↓
StudyLedger integration
        ↓
reconstruction and defense
```

Prediction happens before tools. When the prediction is wrong, record the exact mistaken model rather than only the correct answer.

Classify evidence precisely:

- `typecheck-pass` — the configured TypeScript checker should accept the source;
- `typecheck-fail` — the checker should reject it for the intended relationship;
- `run-pass` — emitted JavaScript should produce the named observable result;
- `run-fail` — execution should throw, reject, or exit unsuccessfully for the intended cause;
- design failure — the program may compile and run but violates the product contract.

The compiler laboratories contain eighty isolated investigations that make these distinctions executable.

## The ten-day progression

| Day | Module | Governing question | Independent product |
|---:|---|---|---|
| 1 | [Runtime, Toolchain, ESM, and the JavaScript/TypeScript Boundary](module-01-runtime-toolchain-and-execution/index.md) | What runs, what is checked, what is emitted, and which metadata controls each phase? | [Runtime Report](../labs/module-01-runtime-report/README.md) |
| 2 | [Values, Coercion, Equality, Control Flow, and Invariants](module-02-values-coercion-equality-and-control/index.md) | Which runtime value exists after each operation, and which conversions should the product allow? | [Usage Quote Policy](../labs/module-02-usage-quote-policy/README.md) |
| 3 | [Functions, Scope, Closures, Callbacks, and `this`](module-03-functions-scope-closures-and-this/index.md) | What does a callable capture, how may it be invoked, and who owns its effects? | [Callback Budget](../labs/module-03-callback-budget/README.md) |
| 4 | [Objects, Arrays, Identity, Mutation, and Immutable Updates](module-04-objects-arrays-identity-and-mutation/index.md) | Which references share an object, which updates are visible, and what does a copy actually copy? | [Inventory Transform](../labs/module-04-inventory-transform/README.md) |
| 5 | [TypeScript Modeling, Unions, Narrowing, `unknown`, and `never`](module-05-typescript-modeling-and-narrowing/index.md) | How can types express legal domain states while runtime checks establish external facts? | [Review Workflow](../labs/module-05-review-workflow/README.md) |
| 6 | [Collections, Iteration, Generic Relationships, and Deterministic Data](module-06-collections-iteration-and-generics/index.md) | What happens to item type, order, cardinality, identity, and uniqueness through a transformation? | [Record Query](../labs/module-06-record-query/README.md) |
| 7 | [Modules, Packages, Resolution, and Public API Boundaries](module-07-modules-packages-and-public-apis/index.md) | Which import causes which module to execute, and which paths are supported contracts? | [Package Boundary](../labs/module-07-package-boundary/README.md) |
| 8 | [Errors, JSON, Runtime Validation, and Persistence Contracts](module-08-errors-json-validation-and-persistence/index.md) | Where does untrusted data become trusted, and what remains visible after failure? | [Validated Configuration](../labs/module-08-validated-configuration/README.md) |
| 9 | [Promises, Event-Loop Ordering, CLI Boundaries, and Async Files](module-09-promises-event-loop-cli-and-files/index.md) | Who owns eventual work, rejection, cancellation requests, process behavior, and file effects? | [Async File Index](../labs/module-09-async-file-index/README.md) |
| 10 | [Testing, Architecture, Integration, and Independent Change](module-10-testing-architecture-and-change/index.md) | Can you change a complete program and prove every affected boundary without following a patch? | [Reading Ledger](../labs/module-10-reading-ledger/README.md) |

The sequence is cumulative. Module 5 does not replace runtime reasoning from Module 2; it gives the checker a better model of states whose runtime values still follow JavaScript semantics. Module 9 does not replace function and module boundaries; it adds time and external effects to them.

## Five forms of progress

Each day should produce five different artifacts:

1. **Model** — a diagram, table, or explanation reconstructed without the chapter.
2. **Prediction** — classifications made before running the investigation cases.
3. **Repair** — a broken program corrected without deleting the difficult requirement.
4. **Construction** — the independent lab and the day’s StudyLedger increment.
5. **Defense** — a short explanation connecting product requirement to implementation and evidence.

A passing test suite without a causal explanation is incomplete. A polished explanation without executable behavior is also incomplete.

Use [Outcomes and mastery evidence](outcomes.md) to see the exact skill and proof expected from each module.

## The cumulative product: StudyLedger

[StudyLedger](capstone.md) is a persistent CLI for planned, active, completed, and abandoned study sessions. It is intentionally built with Node’s standard library so the first course does not hide fundamental boundaries behind a framework or schema package.

The product forces all ten modules to cooperate:

```text
terminal argument tokens
          ↓
validated typed command
          ↓
legal domain transition
          ↓
immutable candidate ledger
          ↓
canonical versioned JSON
          ↓
asynchronous same-directory replacement
          ↓
stable stdout/stderr and exit status
```

Its architecture separates command grammar, domain state, runtime validation, persistence, application orchestration, rendering, and process adaptation. Tests operate at pure, module, filesystem, application, and real-process boundaries.

The capstone is complete for a declared single-user local-file contract. It does not claim crash durability, cross-process locking, hostile-input peak-memory bounds, or distributed consistency. Naming these non-contracts is part of the learning standard.

## Independent laboratories

The ten labs are smaller products, not capstone fragments. Their domains vary so that the mechanism must transfer:

- a runtime report exposes the source/check/emission/process route;
- a quote engine makes coercion and zero-value policy explicit;
- a callback budget reveals invocation contracts absent from function types;
- an inventory transform makes identity and structural sharing observable;
- a review workflow turns state legality into types and transitions;
- a record query library exercises order, uniqueness, narrowing, and generics;
- a package boundary makes ESM graph and public surface visible;
- a configuration decoder establishes trust from `unknown` data;
- a file index owns asynchronous operations and deterministic reconstruction;
- a reading ledger proves independent integration.

Starters are coherent baselines. Reference implementations are complete examples to compare after your own design is stable.

## Course boundaries

Course 1 includes:

- JavaScript values, operators, control flow, functions, objects, arrays, and promises;
- strict TypeScript fundamentals, unions, narrowing, generics, and module types;
- Node ESM, process, filesystem promises, CLI parsing, and built-in testing;
- complete small-program architecture.

It deliberately postpones:

- prototypes, descriptors, symbols, proxies, decorators, and deep runtime reflection;
- advanced conditional and mapped types and library-scale declaration design;
- streams and backpressure;
- HTTP services and databases;
- workers and high-throughput concurrency;
- security, observability, deployment, and performance engineering.

Those topics belong to later courses because they depend on the value, identity, type, module, error, promise, and evidence model built here.

## Completion standard

You have completed Course 1 when you can, without copying the reference layout:

- build a strict ESM Node package from an empty directory;
- state what TypeScript proves and what JavaScript can still do;
- parse external text without accidental coercion;
- draw object identity before and after a nested update;
- model legal alternatives with a discriminated union;
- validate unknown JSON into a newly constructed trusted value;
- select collections and generic relationships deliberately;
- keep package side effects and public exports explicit;
- preserve causal errors across layers;
- own every started promise;
- isolate time and filesystem effects in tests;
- exercise a real CLI process;
- implement one independent StudyLedger feature and defend its compatibility effects.

Proceed to the [ten-day plan](study-plan.md), inspect the [reference desk](reference.md), or begin [Module 1](module-01-runtime-toolchain-and-execution/index.md).
