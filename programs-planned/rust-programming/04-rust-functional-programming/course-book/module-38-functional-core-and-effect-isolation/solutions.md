# Reasoned solutions — Module 38: Functional Core and Effect Isolation

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the LedgerFlow engineering guide](../capstone.md)

Use these explanations to review your reasoning about **Functional Core and Effect Isolation**, not to substitute for an attempt. The decisive question is: *Which decisions can remain pure, which effects must occur at the boundary, and what data should cross between them?* When your design differs, separate three possibilities: a Rust rule was applied incorrectly, the product contract changed, or two architectures satisfy the same contract with different trade-offs.

## Compiler specimen reasoning

### 1. `case-01.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** time can be injected as an explicit callable input.
- **Causal explanation:** The specimen compiles because time can be injected as an explicit callable input.
- **Principled repair:** accept an appropriate callable at the boundary
- **Weak repair to reject:** hide system time behind a global helper

### 2. `case-02.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** a stateful ID generator requires FnMut.
- **Causal explanation:** The specimen compiles because a stateful ID generator requires FnMut.
- **Principled repair:** use FnMut and call only for accepted work
- **Weak repair to reject:** use a global atomic counter in single-threaded core code

### 3. `case-03.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** an Fn boundary rejects an injected stateful generator.
- **Causal explanation:** The compiler rejects the specimen because an Fn boundary rejects an injected stateful generator.
- **Principled repair:** change the boundary to FnMut or inject an iterator of IDs
- **Weak repair to reject:** use interior mutability only to preserve the wrong signature

### 4. `case-04.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** an effect plan is an ordinary deterministic value.
- **Causal explanation:** The specimen compiles because an effect plan is an ordinary deterministic value.
- **Principled repair:** return typed actions and interpret them in the shell
- **Weak repair to reject:** print from inside analysis

### 5. `case-05.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** a stored static callback cannot borrow a local variable.
- **Causal explanation:** The compiler rejects the specimen because a stored static callback cannot borrow a local variable.
- **Principled repair:** move owned data into the closure or give the object a shorter lifetime
- **Weak repair to reject:** leak the local to satisfy static

### 6. `case-06.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** BTreeMap iteration provides key order for deterministic reports.
- **Causal explanation:** The specimen compiles because bTreeMap iteration provides key order for deterministic reports.
- **Principled repair:** choose an ordered structure when order is a contract
- **Weak repair to reject:** sort repeatedly after every insertion without need

### 7. `case-07.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** set insertion is idempotent for equal values.
- **Causal explanation:** The specimen compiles because set insertion is idempotent for equal values.
- **Principled repair:** test idempotence only where the operation has that law
- **Weak repair to reject:** claim file writes are idempotent without defining overwrite behavior

### 8. `case-08.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** consuming an effect plan transfers ownership to the executor.
- **Causal explanation:** The compiler rejects the specimen because consuming an effect plan transfers ownership to the executor.
- **Principled repair:** borrow the plan or stop using it after execution based on contract
- **Weak repair to reject:** clone every action without a replay requirement

## Exercise reasoning

### Exercise 1 — Classify effects

File reading and terminal output are shell effects. Parsing and validation are deterministic core operations when supplied text and policy. Current time and random/monotonic ID generation are unstable inputs; either perform them in the shell and pass values or inject a small capability. Sorting and rendering can be core when order and formatting policy are explicit. Exit-code choice can be a core decision represented as an enum, while actually terminating the process belongs to the shell.

### Exercise 2 — Refactor an effectful function

The shell reads text and maps I/O failures to operational errors. The core `analyze(&str) -> Analysis` returns accepted records and structured diagnostics. A pure `render(&Analysis) -> String` produces text, and `classify(&Analysis) -> ExitClass` decides clean versus data-error status. The shell writes the rendered bytes and converts write failure separately. `bool` is replaced by meaningful types, and tests can cover every core branch without temporary files.

### Exercise 3 — Inject unstable inputs

Acquire `timestamp` and `BatchId` once at the boundary and pass them as ordinary values. If multiple IDs are required in a deterministic call order, accept `F: FnMut() -> BatchId` at the narrow function that allocates them. A trait is justified only if several related operations or substitute implementations form a stable contract. Global clock access makes replay and exact-output testing impossible.

### Exercise 4 — Plan then execute

The core returns an ordered `Vec<Action>` such as `WriteAtomic { path, bytes }` followed by `Print { text }`. The executor validates paths, writes temporary files, flushes/synchronizes as required by the declared durability level, replaces targets, and only then executes success output. Cross-file atomicity is not automatically guaranteed; either document partial-commit risk, use a domain-specific transaction mechanism, or change product expectations. The plan clarifies order but does not magically provide atomic I/O.

### Exercise 5 — Idempotence and replay

Replay is idempotent only if stable event identities are recognized and duplicate policy prevents applying the same logical event twice, with policy/version held constant. Record input bytes, policy version, and any injected unstable values. Test by applying the same batch twice and comparing domain state, diagnostics, and audit semantics. A second duplicate warning means output may not be byte-identical even when state is idempotent; define the observation precisely.

### Exercise 6 — Core and shell evidence matrix

Core tests cover parsing, ordering, diagnostics, reduction, queries, report structure, and exit classification with in-memory values. Property/law tests can cover determinism and idempotence on bounded domains. CLI process tests cover argument parsing, file-not-found behavior, stdout versus stderr, exit status, and exact byte rendering. A small number of integration tests prove wiring; they should not duplicate every domain case already proven in the core.



## Laboratory comparison

The complete laboratory implementation is in [`module-08-deterministic-batch-runner/solution`](../../labs/module-08-deterministic-batch-runner/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **Functional Core and Effect Isolation**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Separate deterministic domain decisions from filesystem, time, environment, and terminal effects.
- Inject small effect capabilities through parameters, closures, or narrow traits without building a framework.
- Represent intended effects as data when plan-then-execute improves safety or testability.
- Design idempotent and replayable boundaries where the domain permits them.
- Test the core with values and test the shell with focused boundary evidence.

A complete explanation of **Functional Core and Effect Isolation** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.
