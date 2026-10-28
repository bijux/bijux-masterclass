# How to Study the Node.js Program

## Choose the correct entry point

Begin Course 1 if you understand basic programming but have not independently built strict Node.js software.

Begin Course 2 only when you can build a strict TypeScript ESM package, validate external values, own asynchronous file effects, and test a complete CLI.

Begin Course 3 only when you can reason through descriptors, prototypes, receivers, classes, private brands, symbols, iteration, reflection, object graphs, persistence records, and explicit cleanup.

Begin Course 4 only when you can publish a small typed library whose runtime behavior, declarations, package exports, runtime validation, and compatibility policy agree.

Begin Course 5 only when you can own every started promise, propagate cancellation and deadlines, bound admission and active work, model process startup and shutdown, and prove one terminal outcome for every accepted operation. Streams do not replace those obligations; they add byte ownership, queue pressure, framing, file handles, child stdio, and publication state.

TypeScript-first does not mean TypeScript-only. Node executes JavaScript and erases types. Every important operation therefore asks:

1. What JavaScript value, identity, byte representation, effect, and failure exist at runtime?
2. What relationship did TypeScript establish before execution?
3. Which object, module, task, stream graph, process, or transaction owns the operation?
4. Where can demand or retained state accumulate, and what bounds it?
5. Which event, promise, digest, file replacement, or process status proves completion?
6. Which terminal paths release every owned promise, listener, timer, stream, file, process, and staged artifact?

## Daily method

| Time | Work |
|---|---|
| 08:30–09:00 | Reconstruct the previous model without notes |
| 09:00–11:00 | Read the authoritative chapter and trace its examples |
| 11:15–12:30 | Predict investigation outcomes before using tools |
| 13:30–15:00 | Diagnose and repair causal failures |
| 15:15–17:15 | Build the independent laboratory |
| 17:30–19:00 | Transfer the mechanism into the course capstone |
| 19:30–20:15 | Add adversarial evidence and inspect public, lifecycle, or representation artifacts |
| 20:15–20:30 | Write retrieval prompts for the next day |

## Investigation vocabulary

- `typecheck-pass` — the checker accepts the intended static relationship;
- `typecheck-fail` — the checker rejects the source for the named cause;
- `run-pass` — emitted JavaScript completes with the specified runtime result;
- `run-fail` — execution fails for the specified runtime rule;
- `design-review` — code may compile and run while violating a product contract.

A checker error, exception, orphaned promise, leaked listener, unbounded queue, malformed frame, partial file, unowned child process, compatibility break, and design defect are different evidence.

## How to work through a module

1. Write your prediction before running the compiler or program.
2. Name the responsible layer: JavaScript, TypeScript, Node API, package metadata, operating system, or product policy.
3. Trace ownership and state transitions. For Course 5, include the byte representation, queue, bound, completion authority, and commit point.
4. Repair the smallest causal defect without collecting the whole input, weakening a type to `any`, swallowing an error, or deleting cancellation.
5. Build the laboratory from the starter.
6. Add adversarial tests before reading the reference.
7. Compare only the first meaningful design difference with the reference and identify the invariant that forced it.
8. Transfer the mechanism into the cumulative capstone.
9. Reconstruct the model without notes.

### Networking and service trace

For Course 6, trace one operation through these layers:

```text
logical service identity
    ↓
address candidates and one connection budget
    ↓
transport state and message framing
    ↓
protocol syntax and semantics
    ↓
runtime validation and application authority
    ↓
semantic commit and response completion
    ↓
retry, replay, or long-lived delivery
    ↓
quiesce, drain, abort, join, and report
```

At each arrow, ask what can accumulate, who owns cancellation, and what evidence distinguishes success from a merely completed API call.

## Using official sources

The books are self-contained learning material. Official specifications and API documentation are verification routes for exact platform claims, version-conditioned behavior, and further reference. They are not homework required to fill missing explanations.

## Verification routes

```bash
cd programs/node-programming/01-node-typescript-foundations && make verify
cd ../02-javascript-object-model-runtime-protocols && make verify
cd ../03-advanced-typescript-library-api-design && make verify
cd ../04-async-node-event-driven-architecture && make verify
cd ../05-node-streams-filesystems-data-pipelines && make verify
```

At program root, `make verify` runs all five compatibility routes. Use `make proof` only when the exact pinned toolchain and MkDocs are installed.


Course 6 compatibility route:

```bash
make -C 06-node-networking-http-service-architecture verify
```
