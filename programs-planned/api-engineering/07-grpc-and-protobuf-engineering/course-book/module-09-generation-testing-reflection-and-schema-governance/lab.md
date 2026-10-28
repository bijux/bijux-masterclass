# Lab — Regenerate, inventory, and prove the RPC surface

**Module:** Generation, Testing, Reflection, and Schema Governance

## Objective

Publish a reproducible generation pipeline, checked descriptor inventory, generated-client build matrix, runtime catalogue comparison, and Course 7 RPC release gate.

## Setup

Begin from a clean course tree. Use the checked descriptor projection and dependency-light builds, then enable pinned `protoc`, Buf, and grpcurl routes when available.

## Controlled actions

1. Generate Python artifacts twice in separate temporary directories and compare bytes.
2. Compile the TypeScript semantic/client surface and optional grpc-js adapter.
3. Build or inspect the descriptor inventory and compare it with the RPC catalogue.
4. Start the live Python server and compare reflection inventory when enabled.
5. Regenerate representative consumers from an additive candidate and build them.
6. Inject generated-code drift and an uncatalogued method, then confirm assigned proofs fail.

## Correctness oracle

Generation is deterministic for the supported profile; descriptor, source, catalogue, generated clients, and runtime inventory agree; planted drift and uncatalogued exposure are detected; missing external tools remain explicitly unexecuted.

## Required evidence

- `capstone/contracts/descriptors/analysis-v1.json`
- `capstone/rpc-case/rpc-catalog.yaml`
- `reports/module-09-governance-proof.json`

## Cleanup

Remove temporary generation directories, stop live servers, restore checked generated artifacts, and verify the repository manifest.

## Completion gate

No RPC release may proceed unless authoritative source, deterministic generation, descriptors, catalogue, supported clients, runtime inventory, and proof scope are mutually consistent.

A successful command without this evidence does not complete the lab.
