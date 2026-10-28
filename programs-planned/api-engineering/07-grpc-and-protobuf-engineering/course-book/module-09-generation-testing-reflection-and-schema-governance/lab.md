# Lab — Regenerate, inventory, and prove the RPC surface

> **Module 09:** Generation, Testing, Reflection, and Schema Governance

## Objective

Publish a reproducible generation pipeline, checked descriptor inventory, generated-client build matrix, runtime catalogue comparison, and Course 7 RPC release gate.

## Why this lab matters

This lab turns the module’s governing question—**How do we make proto source, generated code, runtime services, tests, descriptors, reflection, and release policy agree without treating code generation as proof?**—into a falsifiable experiment. The versioned .proto files and their imported dependencies define the RPC contract. Handwritten DTOs, framework handlers, generated source, documentation, and reflection must derive from or be checked against them. Editing generated code to fix a behavior is a release defect: the next generation erases the change and other languages remain inconsistent.

It advances the cumulative Analysis Runs Platform by requiring this result: **Publish a reproducible generation pipeline, checked descriptor inventory, generated-client build matrix, runtime catalogue comparison, and Course 7 RPC release gate**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

Begin from a clean course tree. Use the checked descriptor projection and dependency-light builds, then enable pinned `protoc`, Buf, and grpcurl routes when available.

## Hypothesis

The clean implementation should satisfy this claim: **Generation is deterministic for the supported profile; descriptor, source, catalogue, generated clients, and runtime inventory agree; planted drift and uncatalogued exposure are detected; missing external tools remain explicitly unexecuted.** When the lab introduces this fault—**Inject generated-code drift and an uncatalogued method, then confirm assigned proofs fail**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Generate Python artifacts twice in separate temporary directories and compare bytes.
2. Compile the TypeScript semantic/client surface and optional grpc-js adapter.
3. Build or inspect the descriptor inventory and compare it with the RPC catalogue.
4. Start the live Python server and compare reflection inventory when enabled.
5. Regenerate representative consumers from an additive candidate and build them.
6. Inject generated-code drift and an uncatalogued method, then confirm assigned proofs fail.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Inject generated-code drift and an uncatalogued method, then confirm assigned proofs fail**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Publish a reproducible generation pipeline, checked descriptor inventory, generated-client build matrix, runtime catalogue comparison, and Course 7 RPC release gate**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

Generation is deterministic for the supported profile; descriptor, source, catalogue, generated clients, and runtime inventory agree; planted drift and uncatalogued exposure are detected; missing external tools remain explicitly unexecuted.

## Required evidence

- `capstone/contracts/descriptors/analysis-v1.json`
- `capstone/rpc-case/rpc-catalog.yaml`
- `reports/module-09-governance-proof.json`

## Interpretation and defense

1. Which state or effect is authoritative for **Generation, Testing, Reflection, and Schema Governance**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Inject generated-code drift and an uncatalogued method, then confirm assigned proofs fail** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Remove temporary generation directories, stop live servers, restore checked generated artifacts, and verify the repository manifest.

## Completion gate

No RPC release may proceed unless authoritative source, deterministic generation, descriptors, catalogue, supported clients, runtime inventory, and proof scope are mutually consistent.

A successful command without this evidence does not complete the lab.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Generation, Testing, Reflection, and Schema Governance**. A green command without the negative case and causal explanation does not satisfy this gate.
