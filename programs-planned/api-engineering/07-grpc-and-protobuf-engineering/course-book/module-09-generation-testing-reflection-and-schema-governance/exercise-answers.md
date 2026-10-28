# Worked answers — Generation, Testing, Reflection, and Schema Governance

These are reference answers, not scripts to memorize. Compare the decision rule and evidence, then revise your answer.

## 1. Why is generated source not the contract source of truth?

It is derived from versioned proto source and generator settings. Editing it creates language drift and is erased by regeneration.

**Decisive evidence:** source/derived ownership check

## 2. What should be pinned for reproducible generation besides `protoc`?

Pin language plugins, runtime libraries, include dependencies, Buf version/config, generation options, package mappings, and well-known type sources.

**Decisive evidence:** tool-version manifest

## 3. Compare the roles of `protoc` and Buf.

`protoc` compiles schemas and emits descriptors/plugins; Buf adds module management, lint, generation orchestration, and baseline breaking analysis. Application proofs remain separate.

**Decisive evidence:** capability matrix

## 4. What does a descriptor set prove?

It proves the declared schema graph, field tags/types, services, methods, and streaming flags for the compiled source. It does not prove runtime registration or behavioral compatibility.

**Decisive evidence:** descriptor inventory

## 5. What does runtime reflection prove, and what does it not prove?

It shows what one running instance exposes now. It does not establish source authority, fleet consistency, compatibility, or policy approval.

**Decisive evidence:** reflection comparison

## 6. Why can a mock server not prove CreateRun idempotency?

A mock may replay the expected response without a database transaction or concurrent request binding. Idempotency is a durable application property.

**Decisive evidence:** persistence idempotency test

## 7. Name the minimum test layers for WatchRun.

Semantic sequence/resume tests, in-process service tests, real network server-streaming tests, generated-client consumption, cancellation/deadline tests, and lifecycle/reconnect cases.

**Decisive evidence:** test-layer matrix

## 8. Why can a binary-compatible field rename fail generated-client compatibility?

Generated accessor names and ProtoJSON keys change, so source and JSON consumers fail even when old binary bytes still parse.

**Decisive evidence:** consumer regeneration build

## 9. What information belongs in the RPC catalogue but not the `.proto`?

Ownership, callers, deadlines, retry/idempotency policy, consumers, SLOs, exposure, and operational runbooks; the proto carries wire contract and comments.

**Decisive evidence:** catalogue/schema join

## 10. When should generated source be checked into the repository?

When offline use, reproducibility, or consumer packaging justify it and deterministic regeneration verifies no drift. Otherwise generate in builds from pinned inputs.

**Decisive evidence:** generated-artifact policy

## 11. How should an unavailable Buf tool be represented in verification?

Record not executed with the missing capability, exact command, expected oracle, and independent local evidence. Never mark it passed.

**Decisive evidence:** not-executed report

## 12. Define the deterministic generation release gate.

Generate twice in clean directories, compare bytes/digests, compile supported clients, run lint/compatibility/descriptor checks, verify catalogue and reflection, and preserve reports.

**Decisive evidence:** generation reproducibility report
