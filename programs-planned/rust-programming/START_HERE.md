# How to Study the One-Hundred-Module Program

## Who this program is for

The path begins for someone who already understands basic programming but is new to Rust. It then continues far beyond language introduction: memory relationships, architecture, functional dataflow, metaprogramming, unsafe systems boundaries, concurrency, async networking, production engineering, and advanced long-lived design.

The sequence is cumulative. Skipping a course is reasonable only when you can pass its final review and build its independent transfer without following the supplied solution. Familiarity with syntax is not the same as owning the mental model.

## Placement

| Course | Course title | Begin when… |
|---:|---|---|
| 1 | Rust Foundations | You should already understand variables, conditions, loops, functions, and collections in at least one programming language. No systems-programming or memory-management background is assumed. |
| 2 | Ownership, Lifetimes, and Memory | You should be able to build and test a complete safe-Rust program, explain moves and ordinary borrows, use structs and enums, propagate errors, and organize a library and binary. |
| 3 | Traits, Generics, and Architectural Design | You should be comfortable with ownership and borrowing, trait basics, generic functions, lifetime annotations, smart-pointer liveness, and private invariant-bearing types. |
| 4 | Functional Rust | You should be able to design trait boundaries, use static and dynamic dispatch, understand ownership through collections, and model state explicitly. |
| 5 | Rust Metaprogramming | You should be able to design traits and public APIs, reason about ordinary Rust expansion targets, write tests at several boundaries, and separate deterministic core logic from effects. |
| 6 | Rust Systems Programming | You should be able to model ownership and cleanup, design public traits and errors, isolate effects, understand generated code, and maintain deterministic formats and tests. |
| 7 | Rust Concurrency and Parallelism | You should be able to audit ownership, unsafe boundaries, cleanup, representation, and system calls, and to distinguish semantic state from observational or platform-dependent facts. |
| 8 | Rust Async and Networked Services | You should be able to reason about thread ownership, synchronization, backpressure, liveness, atomics, deterministic reconciliation, system I/O, and bounded resources. |
| 9 | Rust Performance and Production Engineering | You should be able to build bounded synchronous and asynchronous systems, state protocol and shutdown guarantees, separate live metrics from authoritative state, and preserve deterministic behavior under concurrency. |
| 10 | Advanced Rust Mastery | You should have completed the preceding nine courses or equivalent work. You should be able to explain ownership, memory, traits, functional dataflow, macros, unsafe systems boundaries, concurrency, async protocols, and production evidence without relying on API-name recall alone. |

A failed placement attempt is useful. Note whether the gap is vocabulary, prediction, implementation, transfer, or explanation; then study the smallest earlier module that supplies the missing relation.

## One dense study day

A realistic day contains eight to ten focused hours with real breaks:

| Time | Work |
|---|---|
| 08:30–09:00 | Closed-book retrieval from the previous module |
| 09:00–10:45 | Read and type the main chapter examples |
| 10:45–11:00 | Break |
| 11:00–12:30 | Freeze compiler or design predictions before running anything |
| 12:30–13:30 | Lunch and movement |
| 13:30–15:00 | Diagnose and repair the workbook cases |
| 15:00–15:15 | Break |
| 15:15–17:15 | Build the independent laboratory |
| 17:15–18:15 | Dinner and screen break |
| 18:15–19:45 | Apply the capstone increment and add adversarial tests |
| 19:45–20:30 | Reconstruct the model and record unresolved questions |

Do not turn the last block into extra reading. Retrieval is the part that reveals whether the explanation has become usable knowledge.

## How the four learning surfaces fit

### Chapter

Read the chapter as an argument, not a reference list. Before each example, state the expected type, owner, state transition, failure, order, capacity, or compiler phase. After the example, change one assumption and predict the consequence.

### Workbook

Complete the prediction section before compiling. For every incorrect prediction, record:

```text
what I expected:
decisive rule or event:
earliest phase that can know it:
smallest repair that preserves the requirement:
tempting repair that weakens the product:
```

A correct pass/fail guess with the wrong cause is not a successful prediction.

### Laboratory method

The lab is a smaller independent product, not a partially renamed capstone.

1. Copy `starter/` to your own workspace.
2. Run the baseline tests and read the public interface.
3. Write the first missing behavior and first adversarial case as tests.
4. Implement one invariant at a time.
5. Trace state after failure, not only the successful output.
6. Complete the transfer task in a different domain.
7. Open `solution/` only after preserving your design and test results.
8. Compare invariants, ownership, failure, and complexity—not only line-by-line code.

The reference implementation is one defended design. It is not proof that every different design is wrong.

### Capstone

Before each capstone increment, name the invariant that changes. After implementation, trace the change through types, ownership, errors, storage or protocol, tests, documentation, and public behavior. Later courses add compiler phases, unsafe assumptions, scheduling, network ambiguity, measurement, and compatibility to the same trace.

## The shared reasoning artifact

Each course uses a different working record:

| Course | Keep beside the code |
|---:|---|
| 1 | Type trace, ownership ledger, state table, error map, API map |
| 2 | Place and loan graph, lifetime relation, drop trace, liveness graph, layout claim |
| 3 | Trait-law table, coherence map, dispatch map, typestate graph, compatibility matrix |
| 4 | Capture map, iterator stage table, failure matrix, accumulator invariant, effect boundary |
| 5 | Grammar, authority map, expansion ledger, hygiene map, diagnostic contract, phase map |
| 6 | Byte/layout table, resource state, durability timeline, safety dossier, ABI contract |
| 7 | Thread ownership, protected invariant, wait-for graph, happens-before relation, shutdown tree |
| 8 | Future state, wake source, task tree, frame ledger, protocol state, capacity and deadline map |
| 9 | Claim, workload, cost model, allocation/byte ledger, signal dictionary, threat and release record |
| 10 | Compiler-phase record, trait-goal graph, unsafe dossier, verification and compatibility matrix, decision record |

The record should be small enough to use while coding. Its purpose is to stop an API name from replacing a causal argument.

## When you are stuck

Use this order:

1. Reduce the failing case without changing the requirement.
2. Classify the decisive phase: parsing, expansion, name resolution, type/borrow checking, build, runtime, operating system, foreign code, schedule, network peer, measurement, or compatibility policy.
3. Draw the smallest model that can decide it.
4. Read the full diagnostic and its secondary labels.
5. Consult the course chapter and the primary source linked there.
6. Test the smallest principled repair.
7. Reintroduce the product boundary and adversarial case.

Do not begin by adding `clone`, `Box`, `dyn`, `RefCell`, `unsafe`, a lock, a channel, an atomic, `spawn`, a macro, or a framework. Any of those can be correct, but only after you name the relationship it is meant to express.

## Reference solutions

Use solutions after a serious attempt. A disciplined comparison asks:

- Which invariant does each design make obvious?
- Which ownership or authority relationship differs?
- What happens on the first failure path?
- Which order, capacity, compatibility, or platform claim is made?
- Which design is simpler for the actual product contract?

Copying a finished implementation can teach syntax. Reconstructing why it is valid teaches Rust.

## Weekly rhythm

After Day 5, stop adding new material. Rebuild the five-module dependency chain from memory, rerun the two investigations that changed your model most, repair unfinished labs, and explain the capstone state to an empty page.

After Day 10, complete the final review and the independent change. One week later, reconstruct the course arc and one central proof without opening the book. Any missing relationship becomes the first repair target before the next course.

## Progress

Mark a module in [PROGRESS.md](PROGRESS.md) only after the chapter, workbook, lab, capstone increment, and closed-book reconstruction are complete. The optional progress tool records completion locally:

```bash
make progress
python3 tools/progress.py done 1
python3 tools/progress.py undo 1
```

Completion is useful for navigation. It is not a grade and it does not replace the course’s final transfer.
