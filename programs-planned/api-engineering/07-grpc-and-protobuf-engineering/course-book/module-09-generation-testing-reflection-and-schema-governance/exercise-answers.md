# Worked Answers — Module 09: Generation, Testing, Reflection, and Schema Governance

Use these solutions to audit your reasoning for **Generation, Testing, Reflection, and Schema Governance**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why is generated source not the contract source of truth?

It is derived from versioned proto source and generator settings. Editing it creates language drift and is erased by regeneration.

**Decisive evidence:** source/derived ownership check

The chapter’s decisive distinction is this: The versioned .proto files and their imported dependencies define the RPC contract. Handwritten DTOs, framework handlers, generated source, documentation, and reflection must derive from or be checked against them. Editing generated code to fix a behavior is a release defect: the next generation erases the change and other languages remain inconsistent.

## 2. What should be pinned for reproducible generation besides `protoc`?

Pin language plugins, runtime libraries, include dependencies, Buf version/config, generation options, package mappings, and well-known type sources.

**Decisive evidence:** tool-version manifest

In the cumulative capstone, the rule becomes concrete: Record compiler, plugin, runtime, and option versions. Generation inputs include include paths, package mappings, TypeScript loader options, Editions support, and well-known type versions. A lock file or tool-version policy makes the process reviewable. Generate into a clean temporary directory, compare with checked-in or packaged artifacts, and fail on unexplained drift.

## 3. Compare the roles of `protoc` and Buf.

`protoc` compiles schemas and emits descriptors/plugins; Buf adds module management, lint, generation orchestration, and baseline breaking analysis. Application proofs remain separate.

**Decisive evidence:** capability matrix

A useful way to reason about the boundary is: protoc is the reference compiler and descriptor generator. Language plugins produce stubs and message classes. Buf can lint source, manage modules/dependencies, generate via templates, and compare breaking changes against a baseline. Neither tool proves application semantics.

## 4. What does a descriptor set prove?

It proves the declared schema graph, field tags/types, services, methods, and streaming flags for the compiled source. It does not prove runtime registration or behavioral compatibility.

**Decisive evidence:** descriptor inventory

The implementation consequence is: A descriptor set is a serialized schema graph containing files, messages, enums, services, methods, streaming flags, and options. Include imports when the consumer needs a self-contained inventory. Descriptor sets support dynamic tooling, release comparison, documentation, and reflection checks without parsing source text.

## 5. What does runtime reflection prove, and what does it not prove?

It shows what one running instance exposes now. It does not establish source authority, fleet consistency, compatibility, or policy approval.

**Decisive evidence:** reflection comparison

The important nuance is: Server reflection exposes descriptors for services actually registered in a runtime. It can reveal that the deployment serves an old package, omitted a method, or accidentally exposes an internal diagnostic service. It does not replace source governance because it reflects one process at one moment and may be disabled by policy.

## 6. Why can a mock server not prove CreateRun idempotency?

A mock may replay the expected response without a database transaction or concurrent request binding. Idempotency is a durable application property.

**Decisive evidence:** persistence idempotency test

Under concurrency or failure, the distinction becomes: The catalogue lists every fully qualified method, version, capability owner, state owner, allowed callers, deadline owner, retry policy, idempotency requirement, request and response sizes, streaming shape, status vocabulary, observability signals, and consumers. It is a review index, not a second schema.

## 7. Name the minimum test layers for WatchRun.

Semantic sequence/resume tests, in-process service tests, real network server-streaming tests, generated-client consumption, cancellation/deadline tests, and lifecycle/reconnect cases.

**Decisive evidence:** test-layer matrix

The design remains honest only if: Semantic tests exercise model adapters, status mapping, retry decisions, stream state machines, authorization policy, and lifecycle without a network. They are fast and deterministic. In-process service tests invoke generated handlers with controlled contexts and stores. Network conformance tests start a real gRPC server and prove serialization, metadata, deadlines, cancellation, streaming, health, and status over HTTP/2. Generated-client tests compile and run each supported language surface.

## 8. Why can a binary-compatible field rename fail generated-client compatibility?

Generated accessor names and ProtoJSON keys change, so source and JSON consumers fail even when old binary bytes still parse.

**Decisive evidence:** consumer regeneration build

The consumer-facing consequence is: A provider can compile while consumers fail after regeneration. Maintain a small consumer matrix: Python version/runtime, TypeScript loader or generator, method use, enum policy, JSON use, and supported upgrade window. Generate clients from the candidate schema and build representative consumer programs.

## 9. What information belongs in the RPC catalogue but not the `.proto`?

Ownership, callers, deadlines, retry/idempotency policy, consumers, SLOs, exposure, and operational runbooks; the proto carries wire contract and comments.

**Decisive evidence:** catalogue/schema join

The operational consequence is: Every method appears exactly once. Every contract service has an owner. Every catalogue method exists in the descriptor. Adding a method requires catalogue, policy, tests, and release evidence. Removing a method requires consumer migration and deprecation evidence.

**Evidence.** Combine proto/descriptor validation, generated surface checks, shared vectors, and a live client/server RPC scenario.

## 10. When should generated source be checked into the repository?

When offline use, reproducibility, or consumer packaging justify it and deterministic regeneration verifies no drift. Otherwise generate in builds from pinned inputs.

**Decisive evidence:** generated-artifact policy

The strongest engineering interpretation is: A candidate release records source digest, descriptor digest, generated artifact digests, tool versions, lint and compatibility results, language builds, conformance tests, reflection inventory where available, catalogue match, consumer declarations, and unexecuted capabilities. Reports are deterministic or separate volatile environment data from release identity.

## 11. How should an unavailable Buf tool be represented in verification?

Record not executed with the missing capability, exact command, expected oracle, and independent local evidence. Never mark it passed.

**Decisive evidence:** not-executed report

The defect-oriented view is: The dependency-light environment cannot pretend to execute missing tools. It imports a checked serialized descriptor into the Python runtime, compiles TypeScript semantic adapters, validates golden bytes and local schema invariants, and reports protoc, Buf, grpcurl, and grpc-js network routes as not executed. This is still useful evidence because its scope is explicit.

## 12. Define the deterministic generation release gate.

Generate twice in clean directories, compare bytes/digests, compile supported clients, run lint/compatibility/descriptor checks, verify catalogue and reflection, and preserve reports.

**Decisive evidence:** generation reproducibility report

Across the Python and TypeScript tracks, the invariant is: Generate twice from a clean checkout and compare bytes. Extract the course or release package and rerun proofs. Manifests cover source and intentionally checked-in derived artifacts. Temporary compiler output and caches are excluded.
