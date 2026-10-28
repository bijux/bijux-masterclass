# Lab — Release and roll back the internal Analysis RPC control plane

**Module:** HTTP, Events, and gRPC in One Architecture: Release and Final Defense

## Objective

Release Analysis RPC API 1.0 behind the unchanged public HTTP API and Event API, execute the final defense, and publish a sanitized service-boundary dossier rather than prematurely splitting the system.

## Setup

Start from the Course 6-compatible local application path. Enable the Python live gRPC control plane, shared durable fixture, public HTTP adapter, event relay simulator, and deterministic routing controls.

## Controlled actions

1. Capture baseline HTTP, durable-state, event, security, reliability, and performance evidence.
2. Shadow eligible read calls through gRPC and compare semantic results.
3. Canary bounded CreateRun traffic using the same persistent request identity and no unsafe fallback.
4. Inject post-commit response loss, stale worker completion, slow WatchRun consumer, and server drain.
5. Cut over the eligible population, then roll back to the local path while preserving expanded migrations.
6. Run schema/generation, public HTTP, event, security, reliability, performance, and rollback gates and produce the Course 8 dossier.

## Correctness oracle

The public HTTP and Event APIs remain semantically unchanged; durable state is authoritative; retries and rollback do not duplicate effects; stale attempts fail; streams remain bounded; all release gates report their evidence boundary; and the dossier rejects unjustified decomposition.

## Required evidence

- `capstone/final-defense/trace.json`
- `capstone/releases/rpc-1.0/release-report.json`
- `capstone/handoff/service-boundary-dossier.yaml`

## Cleanup

Return routing to the documented baseline, stop servers and relays, clear temporary canary state, preserve only deterministic release evidence, and verify manifests.

## Completion gate

Analysis RPC 1.0 is complete only when it can be introduced and removed without changing the public promise, durable event truth, authoritative state, security, or recovery semantics.

A successful command without this evidence does not complete the lab.
