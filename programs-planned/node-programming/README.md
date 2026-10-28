> Planned source collection. See [collection status](COLLECTION.md) for preservation and qualification limits.

# Node.js Programming — TypeScript-First, Runtime-Literate, and Production-Oriented

This program teaches JavaScript as the executed language, TypeScript as a static reasoning layer, Node.js as the host runtime, and package metadata and protocols as executable contracts. The course books are the primary product. Laboratories isolate one mechanism; capstones require mechanisms from the entire earlier path to coexist in complete software.

The authored curriculum currently contains six ten-module courses:

```text
JavaScript values, strict TypeScript, ESM, and complete programs
        ↓
object semantics, prototypes, protocols, reflection, and lifecycle
        ↓
advanced TypeScript relationships and public library contracts
        ↓
async scheduling, task ownership, cancellation, events, and process lifecycle
        ↓
bytes, streams, filesystems, subprocesses, and bounded data pipelines
        ↓
network identity, sockets, HTTP, TLS, clients, delivery, and service lifecycle
```

A later course does not replace earlier obligations. ServiceWire still depends on Course 1 validation and errors, Course 2 identity and lifecycle, Course 3 public type contracts, Course 4 task ownership and shutdown, and Course 5 framing, pressure, byte limits, and publication discipline.

## Available courses

| Course | Modules | Course book | Governing question | Capstone |
|---:|---:|---|---|---|
| 1 | 1–10 | [Node.js and TypeScript Foundations](01-node-typescript-foundations/course-book/index.md) | How do JavaScript values, strict types, ESM, external data, promises, files, and tests form a complete program? | **StudyLedger** |
| 2 | 11–20 | [JavaScript Object Model and Runtime Protocols](02-javascript-object-model-runtime-protocols/course-book/index.md) | How do objects acquire behavior, preserve identity, participate in protocols, and remain correct across reflection, cloning, persistence, and cleanup? | **ObjectAtlas** |
| 3 | 21–30 | [Advanced TypeScript and Library API Design](03-advanced-typescript-library-api-design/course-book/index.md) | How do runtime behavior, inferred types, declarations, exports, schemas, and compatibility remain one trustworthy library contract? | **SchemaKit** |
| 4 | 31–40 | [Async Node.js and Event-Driven Architecture](04-async-node-event-driven-architecture/course-book/index.md) | How do scheduling, promise ownership, cancellation, events, timing, context, supervision, and shutdown form a bounded asynchronous program? | **TaskHarbor** |
| 5 | 41–50 | [Node.js Streams, Filesystems, and Data Pipeline Architecture](05-node-streams-filesystems-data-pipelines/course-book/index.md) | How do bytes, pressure, framing, files, compression, child processes, and publication form a bounded, failure-safe dataflow system? | **FlowLedger** |
| 6 | 51–60 | [Node.js Networking, HTTP, and Service Architecture](06-node-networking-http-service-architecture/course-book/index.md) | How do network identity, transport state, HTTP semantics, TLS, clients, long-lived delivery, admission, and shutdown form a coherent service? | **ServiceWire** |

Courses 7–10 remain explicit boundaries in [COURSE_MAP.md]. They are not represented by empty directories or partial course shells.

## How the program teaches

Each module has one authoritative chapter, one workbook, and one reasoned solution set. The common learning sequence is:

```text
predict
    ↓
trace the responsible runtime, type, resource, or protocol relationship
    ↓
explain the causal failure
    ↓
repair without deleting the requirement
    ↓
build the independent laboratory
    ↓
transfer the mechanism into the cumulative capstone
    ↓
defend the resulting contract without notes
```

A successful type check, passing unit test, emitted event, completed stream, HTTP status, or zero process exit proves only the claim it observes. The books therefore separate static evidence, runtime behavior, resource completion, protocol correctness, semantic commit, compatibility, and product success.

## Start

1. Read [How to study the program](START_HERE.md).
2. Learn the shared [reasoning model](REASONING_MODEL.md).
3. Inspect the [course map](COURSE_MAP.md) and [skill map](SKILL_MAP.md).
4. Track completed learning in [PROGRESS.md].
5. Keep the [glossary](GLOSSARY.md) and [source notes](SOURCE_NOTES.md) nearby.

## Verification

```bash
make verify
```

This runs every available compatibility check for all authored courses and reports toolchain differences. `make proof` requires the exact pinned Node.js, npm, TypeScript, ambient-type, and documentation baseline.
