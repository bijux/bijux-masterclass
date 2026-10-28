# Reasoned Solutions — Module 10: Integration and Independent Change

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-10-inventory-ledger/README.md) · [Taskboard guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 10: Integration and Independent Change**. Compare the reasoning against this question: *Can you make and defend a cross-layer change without tutorial imitation or accidental contract regression?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Compiler specimen reasoning

### 1. `01-move-into-command.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** title ownership moved into enum payload.
- **Causal explanation:** The compiler rejects the specimen because title ownership moved into enum payload.
- **Principled repair:** Borrow the title when the command only needs a view, or accept that constructing the command transfers ownership.
- **Weak repair to reject:** Do not clone before every enum construction without a two-owner requirement.

### 2. `02-shared-view-blocks-mutation.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** shared element reference overlaps possible vector reallocation.
- **Causal explanation:** The compiler rejects the specimen because shared element reference overlaps possible vector reallocation.
- **Principled repair:** End the element view before pushing, or store an index/owned fact that remains valid across possible reallocation.
- **Weak repair to reject:** Do not reserve arbitrary extra capacity and treat it as a lifetime guarantee.

### 3. `03-iterator-terminal-consumes.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** count consumes the iterator.
- **Causal explanation:** The compiler rejects the specimen because count consumes the iterator.
- **Principled repair:** Create a fresh iterator for the second terminal operation, or combine the required statistics in one traversal.
- **Weak repair to reject:** Do not clone an expensive iterator pipeline without understanding its captured state.

### 4. `04-generic-sort-bound.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** sorting references requires an ordering bound on T.
- **Causal explanation:** The compiler rejects the specimen because sorting references requires an ordering bound on T.
- **Principled repair:** Add the ordering bound actually required by sorting, or accept a comparator supplied by the caller.
- **Weak repair to reject:** Do not stringify values to manufacture an unrelated ordering.

### 5. `05-incompatible-iterator-branches.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** branch iterator types differ.
- **Causal explanation:** The compiler rejects the specimen because branch iterator types differ.
- **Principled repair:** Use one concrete iterator type, an enum adapter, or a boxed trait object when runtime branch variation is required.
- **Weak repair to reject:** Do not collect both branches eagerly merely to erase their iterator types.

### 6. `06-local-rendered-output.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** returned slice would point into dropped local String.
- **Causal explanation:** The compiler rejects the specimen because returned slice would point into dropped local String.
- **Principled repair:** Return the owned `String`, write into caller-owned storage, or borrow from an owner that outlives the call.
- **Weak repair to reject:** Do not leak the rendered string or forge a longer lifetime.

## Exercise reasoning and worked answers
Module 10 answers are review frameworks rather than one prescribed implementation. The independent feature must remain your work.

### 1. Invariant map

A complete map includes positive/unique IDs, next-ID consistency/overflow, valid title bytes, typed status/priority, legal transitions, deterministic ordering, complete board restoration, canonical encoding, missing-file policy, state preservation on failure, and binary/library separation. Each must name authoritative code and at least one test.

A weak map says “validated in several places.” A strong map distinguishes early contextual checks from authoritative domain construction.

### 2. Add trace

Expected allocations include shell-owned argument strings supplied by the process API, a joined/owned title if multiple tokens are joined, task-owned title storage, vector growth when capacity requires it, encoded output buffers/line strings as implemented, and returned rendered output. No clone of the title is necessary if command ownership moves into `TaskBoard::add`.

Fallible boundaries include command arity, priority/ID/title parsing, storage load, ID allocation, serialization/write/commit, and stdout. Success must be printed only after commit.

### 3. Behavior matrices

Every matrix distinguishes syntax before load, load before domain mutation, domain failure before save, save failure after in-memory mutation but before confirmed persistent success, and output failure after possible commit. Illegal transitions preserve status. Unknown ID preserves board. Read-only operations do not save.

### 4. Rename review

A sound route adds `Command::Rename { id, title }`, validates title in a domain method, finds one mutable task through board API, returns structured unknown-ID/title errors, marks execution as changed, and lets application save. Version 1 already stores title, so encoded field count does not change. Tests cover 0/120/121-byte boundaries, tabs/newlines, unknown ID, successful persistence, failed validation preservation, command arity, public workflow, docs, and CLI streams/status.

### 5. Priority query review

Filtering can borrow tasks and compare typed `Priority`; output collects borrowed references or renders directly. Sort/order follows board ID contract. The application returns a read-only outcome, and an integration test compares file bytes before/after. Unknown priority fails during command parsing before load.

### 6. Transactional batch review

First collect matching indexes or IDs through shared traversal. Validate that every target can complete without mutation. If no matches, follow the specified no-match policy. Then mutate all through a second pass using a restricted transition known to succeed or re-run checked transitions under an invariant that no intervening mutation occurs. Save once. Any prevalidation failure leaves all statuses unchanged.

### 7. Version 2 plan

The answer must not use an ambiguous local-time string. Define a stable representation such as signed UTC epoch seconds plus documented range, or an RFC format with a selected parser crate in a later course. Header becomes `TASKBOARD-V2`. State whether the loader accepts both versions and supplies missing timestamps, rejects version 1, or performs explicit migration. Exact fixtures are required for both versions and unsupported future versions.

### 8. Semantic audit

Expected findings or verified mitigations:

- explicit ID order, no hash leakage;
- checked next-ID increment;
- physical line base tests;
- byte-based title rule documented;
- same-directory prepare/commit save;
- output failure documented as potentially post-commit;
- read-only commands skip save;
- `Error::source` preserves lower failures;
- deterministic temporary-path collision policy documented;
- public enums/types treated as contracts.

Not every risk must be eliminated in Course 1; each must be understood and bounded.

### 9. Refactor review

External tests should remain unchanged. Exact bytes and CLI output remain stable. Unit tests may change when they intentionally cover a private helper, but behavior-oriented unit tests often survive too. A changed public import or fixture indicates the refactor altered contract.

### 10. Release proof

The inventory should include relative path, byte size, and SHA-256 for every file. The report names toolchain version, commands executed, pass/fail, and any command not executable in the build environment. It must not claim Cargo success without running Cargo.

### 11. Oral defense questions
Answers receive credit for accurate rule, capstone application, and tradeoff. Reciting “borrow checker prevents data races” without tracing a concrete borrow earns little. Incorrect claims about `'static`, `Clone`, panic recovery, or persistence are hard failures.

### 12. Transfer project criteria
The new program should share reasoning methods, not necessarily source layout. Assess domain fit, ownership, errors, evidence, and restraint. Penalize copied task states, unnecessary versioned storage, or custom traits introduced solely to resemble the capstone.

### Final principle

Mastery is demonstrated by independent prediction, change, and defense. Reference code can prove one design, but it cannot substitute for your reasoning record.

### Post-key transfer

Implement an unseen command across every taskboard layer, add adversarial tests, and explain the ownership and failure model without running the code.

## Reference implementation comparison

The complete laboratory implementation is in [`module-10-inventory-ledger/solution`](../../labs/module-10-inventory-ledger/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **Integration and Independent Change**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Trace a behavioral change through grammar, types, domain rules, persistence, rendering, tests, and documentation.
- Preserve failure atomicity, deterministic behavior, and public invariants while refactoring across architectural layers.
- Review unfamiliar Rust for ownership workarounds, swallowed errors, invalid-state models, and missing evidence.
- Build a closed-book small program and an independent capstone feature from specification only.
- Defend design choices, rejected alternatives, known limitations, and verification boundaries with concrete evidence.

A complete explanation of **Integration and Independent Change** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.

## Deep reasoning and transfer

### Decisive model

> Can you make and defend a cross-layer change without tutorial imitation or accidental contract regression?

Build a **whole-program invariant map**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Trace a behavioral change through grammar, types, domain rules, persistence, rendering, tests, and documentation.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Preserve failure atomicity, deterministic behavior, and public invariants while refactoring across architectural layers.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Review unfamiliar Rust for ownership workarounds, swallowed errors, invalid-state models, and missing evidence.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Build a closed-book small program and an independent capstone feature from specification only.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Defend design choices, rejected alternatives, known limitations, and verification boundaries with concrete evidence.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Trace a behavioral change through grammar, types, domain rules, persistence, rendering, tests, and documentation.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the whole-program invariant map.

### Laboratory transfer review

For [Inventory Ledger](../../labs/module-10-inventory-ledger/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In Taskboard, Module 10 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Integration and Independent Change**, which relationship decides this question: “Can you make and defend a cross-layer change without tutorial imitation or accidental contract regression?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to Taskboard?
