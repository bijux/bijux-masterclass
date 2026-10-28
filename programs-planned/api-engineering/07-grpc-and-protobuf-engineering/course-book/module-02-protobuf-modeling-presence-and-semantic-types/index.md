# Protobuf Modeling, Presence, and Semantic Types

**Module 02 of 10**

> **Governing question:** How do we encode domain meaning in Protobuf without allowing language defaults, JSON conventions, or storage models to erase important distinctions?

## Place in the program

Module 01 approved a deliberately small RPC boundary. This module gives that boundary a durable type system. The task is not to translate database columns into fields. It is to decide which distinctions must survive generation in Python and TypeScript, binary transport, ProtoJSON, logging, replay, and future schema evolution. Presence, identity, units, and one-of-many alternatives become explicit contract decisions.

## Learning outcomes

- design request and response messages around application decisions rather than persistence records
- distinguish absent, present-with-default, empty, unknown, and inapplicable values
- use enum zero values, `optional`, `oneof`, repeated fields, maps, and semantic wrappers deliberately
- model resource names, request identifiers, correlation identifiers, revisions, and lease generations as different concepts
- protect 64-bit integer meaning across Python, JavaScript, binary Protobuf, and ProtoJSON
- maintain a proto3 executable baseline while understanding the Editions 2024 frontier without pretending universal tool support

## Capstone result

Complete the Analysis RPC 1.0 message model, publish cross-language presence and integer vectors, and document every field whose absence changes behavior.

## Messages describe decisions, not rows

A Protobuf message is an API contract, not an object-relational mapping. A table may contain internal retry counters, normalized search columns, foreign keys, encryption metadata, and bookkeeping timestamps that callers must never control. Conversely, an RPC request may need a request identifier, expected revision, or deadline-related intent that is not stored as a simple column. Begin from the application decision: what information must the callee possess to decide, and what result must the caller be able to interpret?

`CreateRunRequest` therefore contains the parent resource, dataset resource, algorithm, and request identifier. It does not contain server-owned state, owner identifiers inferred from identity, creation time, or a caller-selected database primary key. `AnalysisRun` is an authoritative projection with a resource name, state, progress, revision, and optional terminal details. The response is not the mutable domain entity and must not become the repository record.

This separation prevents two recurring failures. Mass assignment occurs when a generated request is persisted directly and caller-controlled fields become trusted. Contract ossification occurs when internal storage changes require public field changes. Generated messages should be translated at the transport boundary into application commands and results. The mapping is visible, reviewed, and tested.

## Presence is part of the business meaning

Protobuf scalar defaults are convenient but dangerous when absence matters. The numeric default is zero, the string default is empty, and the boolean default is false. Without explicit presence, a receiver may be unable to distinguish “the caller did not set this” from “the caller deliberately selected the default.” That distinction changes patch semantics, preconditions, policy decisions, and terminal result interpretation.

Use `optional` when the application must distinguish absence from a present scalar. In `AnalysisRun`, `result_summary` is absent while work has not produced a result; an empty summary can still be a deliberate completed value. `failure_code` is absent for non-failed runs. Presence is not a substitute for state invariants: a completed run must satisfy the rule that failure information is absent, and a failed run must not claim a successful result.

Do not add `optional` reflexively. `CreateRunRequest.algorithm` can be required by validation even though proto3 cannot mark it required. The server rejects empty or unknown values. Contract documentation, generated validators, and application rules together establish requiredness. The wire format preserves presence only where the schema and runtime expose it.

## Enum zero values must mean unspecified

Every enum begins with a zero value. Make it an explicit `*_UNSPECIFIED` value and reject it where the operation requires a choice. A meaningful state such as `QUEUED = 0` makes an omitted field silently become a real state. That masks old-client behavior, malformed messages, and mapping defects.

Enum values are wire numbers with source names. Never renumber a published value, and do not reuse a removed number. Adding a new value is usually wire-compatible but can break exhaustive consumers. Course 7 therefore classifies enum additions as review-required unless consumers prove unknown-value handling. Python may preserve an unknown integer differently from generated TypeScript libraries; shared vectors must test what each supported runtime actually does.

Use enums for a governed, finite vocabulary with stable ownership. Do not turn every free-form string into an enum. Failure categories intended to evolve independently may require a namespaced string code and a catalogue rather than a frequently changing enum.

## Identity fields are not interchangeable

A resource name identifies durable state, for example `projects/p-1/runs/r-9`. A request identifier deduplicates one command intent. A trace identifier correlates telemetry. A correlation identifier groups a business workflow. A causation identifier links one message to the action that produced it. A worker assignment identifier identifies one leased attempt. A lease generation fences stale workers. A database row identifier may remain entirely private.

Using one UUID for all purposes destroys semantics. A retry with the same request identifier should refer to the same command intent even when it receives a new trace identifier. A replayed event preserves its event identity while producing a new delivery attempt. A new worker lease for the same run receives a new generation even if the assignment resource remains recognizable.

The proto comments and RPC catalogue define identity scope, creator, uniqueness boundary, retention, and whether the value is safe to expose. Tests verify that idempotency keys cannot be substituted for resource names and that stale generations cannot authorize completion.

## The JavaScript 64-bit boundary

Protobuf `int64`, `uint64`, and fixed-width 64-bit fields can represent values beyond JavaScript’s safe integer range. Python integers preserve them, but a JavaScript `number` cannot exactly represent every 64-bit integer. Dynamic loaders and JSON conversions may return strings, `Long` objects, or numbers depending on options. Treat this as a contract choice, not a library footnote.

The course uses 64-bit values for revisions, stream sequence numbers, byte offsets, and lease expiry instants where the range is justified. TypeScript boundary models represent them as decimal strings or `bigint` internally; JSON evidence uses canonical decimal strings. Conversion rejects fractions, signs where forbidden, leading ambiguity, and values outside the declared range. Never use `Number(value)` merely to make a test pass.

ProtoJSON represents 64-bit integers as decimal strings. That makes JSON diagnostics safer, but JSON is not the binary wire format and must not become a second source of truth. Golden binary fixtures and cross-language semantic vectors test both representations.

## Repeated fields, maps, and oneof

A repeated field distinguishes an ordered collection from a set only through contract semantics. If duplicates are forbidden or order is irrelevant, validate and document that property. A map is convenient for unbounded labels but creates governance and cardinality risks. Public or operational metadata should use an allowlist and size limits; arbitrary maps are not a free extension mechanism.

Use `oneof` for mutually exclusive wire alternatives, such as the first upload frame carrying metadata and later frames carrying bytes. It gives generated APIs an explicit union and prevents simultaneous alternatives. Adding fields to a published `oneof` is generally compatible on the wire, but moving an existing field into or out of a `oneof` can change presence and clearing behavior. Consumers must preserve unknown alternatives rather than treating them as empty known cases.

Do not use `oneof` as inheritance. Prefer explicit composition and small messages. A worker-to-control stream uses a `oneof` because each frame has one protocol role—hello, ready, progress, or result—not because these messages share an object-oriented superclass.

## Units, timestamps, and semantic types

A number without a unit is an eventual defect. Name units in fields when no standard semantic type exists: `heartbeat_interval_ms`, `lease_expires_unix_ms`, `offset_bytes`. For wall-clock instants that need calendar interoperability, use `google.protobuf.Timestamp` when supported by the generation profile. For durations, use `google.protobuf.Duration`. For monotonic local elapsed time, do not serialize a process clock as a timestamp.

Resource references use canonical names instead of embedding entire mutable objects. Monetary and arbitrary-precision decimal values require an explicit decimal representation; floating point is unsuitable when exact equality or signatures matter. Binary digests use bytes or a clearly defined lowercase hexadecimal string with an algorithm field. The contract states normalization, maximum length, and comparison rules.

Semantic comments are part of the source contract. They specify whether a timestamp is authoritative, whether an offset is inclusive, whether a byte count refers to uncompressed content, and which component creates an identifier. Generated types alone cannot communicate these rules.

## Proto3 baseline and Editions frontier

The executable course baseline uses proto3 because current Python and TypeScript tooling supports it broadly. The frontier file demonstrates Protobuf Editions 2024 syntax and feature settings. Editions provide an explicit mechanism for evolving language defaults without forcing a new syntax generation, but support varies across generators and runtimes.

The course does not label the frontier executable unless the local toolchain proves it. The capability matrix records parser, generator, runtime, and linter support separately. A learner may use a newer `protoc` or Buf toolchain to compile the frontier, but the baseline remains the source used by dependency-light proofs.

This two-profile approach mirrors Course 1’s OpenAPI baseline and frontier. It teaches current standards while preserving reproducible execution. Never silently down-convert an Editions source and claim the original was validated.

## Cross-language model proof

A schema is not proven by successful code generation. The model proof serializes boundary cases in one language, parses them in the other, and compares application meaning. Cases include absent optional values, present empty strings, unknown enum numbers, maximum safe JavaScript integers, values above that boundary, oneof alternatives, repeated duplicates, and invalid resource names.

Each vector records the source representation, expected binary digest, expected semantic projection, and whether ProtoJSON round-trip is part of the claim. The proof rejects libraries or options that coerce 64-bit values. It also detects generated-code settings that discard unknown fields when a compatibility workflow requires preservation.

The result is a model contract the service can rely on. Later modules layer status, deadline, streaming, and security behavior on top of these precise messages.

## Worked model review: terminal run details

Suppose a first draft models `AnalysisRun` with `string result_summary = 7` and `string failure_code = 8`, without explicit presence. The generated Python object returns empty strings when fields are absent. A dynamic TypeScript loader may also expose default empty strings depending on options. The application can no longer tell whether a completed analysis deliberately produced an empty summary, whether the provider omitted the field, or whether a mapper discarded it.

The corrected model uses explicit presence for both fields and combines that transport distinction with state invariants. A queued or running run must have neither field. A completed run may have `result_summary` present—even when its value is empty—and must not have `failure_code`. A failed run must have a governed failure code and no success summary. Presence answers “was it supplied?”; the state machine answers “is it legal here?” Neither mechanism replaces the other.

Now consider revision. The database uses a bigint and the RPC uses `int64 revision = 9`. Python can represent all valid values. JavaScript cannot safely use a `number` above 2^53−1. The TypeScript adapter therefore accepts a canonical decimal string from the loader or a `Long`-like representation, validates the signed 64-bit range, and converts to `bigint` for arithmetic. The course’s JSON evidence also uses a decimal string. A developer convenience option such as `longs: Number` is rejected because it can collapse two distinct revisions and make a stale ETag appear current.

Identity receives the same review. `name` is the durable resource identity. `request_id` belongs to a command and may be retained only for idempotency. `revision` orders authoritative snapshots. `sequence` orders one observation stream. `assignment_id` and `lease_generation` govern one worker attempt. Replacing all of them with “id” or reusing one UUID would make retries, replay, and fencing impossible to explain.

Finally examine `UploadDatasetRequest`. A `oneof` is justified because a frame has exactly one role. The first frame is metadata; later frames are chunks. This is not class inheritance. The application still validates legal sequence, total bytes, checksum, and duplicate metadata. Generated union APIs prevent simultaneous alternatives but cannot prove the conversation.

The review ends with two artifacts: a field-semantics table and cross-language vectors. Every field records creator, presence, unit, range, sensitivity, identity scope, and evolution rule. The vectors exercise absence, empty values, unknown enum numbers, oneof alternatives, and the complete int64 boundary. That evidence is more valuable than a screenshot of generated classes.

## Implementation reading

Study `capstone/contracts/proto/bijux/analysis/v1/analysis.proto`, the Editions frontier, `capstone/shared/vectors/presence.json`, and `int64.json`. Compare the Python message adapters with TypeScript decimal-string and `bigint` conversions. Generated code is a transport dependency; the semantic adapters are the course-owned boundary.

## Failure checklist

- Does absence carry different meaning from a present default?
- Can any enum silently treat an omitted field as a real state?
- Will every 64-bit value survive the supported TypeScript path exactly?
- Are resource, request, correlation, assignment, and lease identities distinct?
- Does a repeated or map field have bounded size and explicit duplicate/order semantics?
- Is every unit and timestamp interpretation unambiguous?

## Transition

After preserving the checkpoint evidence, continue to **Wire Format, Unknown Fields, and Compatibility Discipline**. Do not progress while the non-compensable gate remains unresolved.
